"""Static local share bundles for Codie reports."""

from __future__ import annotations

import html
import json
import shutil
from dataclasses import dataclass
from pathlib import Path

import qrcode


@dataclass(frozen=True)
class ShareBundleAsset:
    path: str
    label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.path, str) or not self.path.strip():
            raise ValueError("asset path is required")
        if self.label is not None and not self.label.strip():
            raise ValueError("asset label cannot be empty")


@dataclass(frozen=True)
class ShareBundleWriteResult:
    output_dir: str
    index_path: str
    print_path: str | None
    manifest_path: str
    asset_paths: tuple[str, ...]
    qr_asset_path: str | None = None

    def __post_init__(self) -> None:
        if not self.output_dir.strip():
            raise ValueError("output_dir is required")
        if not self.index_path.strip():
            raise ValueError("index_path is required")
        if self.print_path is not None and not self.print_path.strip():
            raise ValueError("print_path cannot be empty")
        if not self.manifest_path.strip():
            raise ValueError("manifest_path is required")
        if self.qr_asset_path is not None and not self.qr_asset_path.strip():
            raise ValueError("qr_asset_path cannot be empty")


def build_share_bundle_manifest(
    *,
    title: str,
    generated_at: str,
    assets: tuple[ShareBundleAsset, ...] | list[ShareBundleAsset],
    entry_file: str = "index.html",
    qr_target: str | None = None,
    qr_asset_path: str | None = None,
    include_print_entry: bool = False,
    print_entry: str = "print.html",
) -> dict:
    """Return deterministic metadata for a local static report bundle."""

    _require_text(title, "title")
    _require_text(generated_at, "generated_at")
    _require_text(entry_file, "entry_file")
    _require_text(print_entry, "print_entry")
    if not assets:
        raise ValueError("at least one asset is required")

    manifest = {
        "bundle_version": "1",
        "title": title,
        "generated_at": generated_at,
        "entry_file": entry_file,
        "qr_ready_entry": entry_file,
        "print_entry": print_entry if include_print_entry else None,
        "pdf_assets": [{"label": "PDF-ready print view", "bundle_path": print_entry}] if include_print_entry else [],
        "assets": [
            {
                "label": asset.label or Path(asset.path).name,
                "source_path": str(Path(asset.path)),
                "bundle_path": f"assets/{Path(asset.path).name}",
            }
            for asset in assets
        ],
        "notes": [
            "Open index.html from this folder on a trusted local device.",
            "The bundle is static and does not call providers, SQLite, analytics, or recommendations.",
            "A later packet may add QR image generation for the entry path.",
        ],
    }
    if qr_target is not None:
        _require_qr_target(qr_target)
        _require_text(qr_asset_path or "", "qr_asset_path")
        manifest["qr_assets"] = [
            {
                "label": "Bundle entry QR",
                "bundle_path": qr_asset_path,
                "encoded_target": qr_target,
            }
        ]
        manifest["encoded_targets"] = [qr_target]
        manifest["privacy_notes"] = [
            "QR payload encodes only the explicit target path or URL.",
            "Report contents and private deck contents are not encoded in the QR payload.",
        ]
    return manifest


def share_bundle_index_html(manifest: dict) -> str:
    """Return a simple static HTML index for a local share bundle."""

    title = _html_text(manifest["title"])
    generated_at = _html_text(manifest["generated_at"])
    asset_items = []
    for asset in manifest["assets"]:
        label = _html_text(asset["label"])
        bundle_path = _html_attr(asset["bundle_path"])
        asset_items.append(f'<li><a href="{bundle_path}">{label}</a></li>')
    qr_items = []
    for qr_asset in manifest.get("qr_assets", []):
        label = _html_text(qr_asset["label"])
        bundle_path = _html_attr(qr_asset["bundle_path"])
        encoded_target = _html_text(qr_asset["encoded_target"])
        qr_items.append(f'<li><a href="{bundle_path}">{label}</a> encodes <code>{encoded_target}</code></li>')

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            f"  <title>{title}</title>",
            "  <style>",
            "    body { font-family: system-ui, sans-serif; margin: 2rem; color: #17212b; }",
            "    main { max-width: 760px; }",
            "    li { margin: 0.7rem 0; }",
            "    .meta { color: #52606d; }",
            "  </style>",
            "</head>",
            "<body>",
            "  <main>",
            f"    <h1>{title}</h1>",
            f'    <p class="meta">Generated at: {generated_at}</p>',
            "    <h2>Included Files</h2>",
            "    <ul>",
            *[f"      {item}" for item in asset_items],
            "    </ul>",
            *(
                [
                    "    <h2>PDF-Ready View</h2>",
                    f'    <p><a href="{_html_attr(manifest["print_entry"])}">Open print-friendly report view</a></p>',
                ]
                if manifest.get("print_entry")
                else []
            ),
            *(
                [
                    "    <h2>Phone Access</h2>",
                    "    <ul>",
                    *[f"      {item}" for item in qr_items],
                    "    </ul>",
                ]
                if qr_items
                else []
            ),
            "    <p class=\"meta\">Static local bundle. No network service is required by this page.</p>",
            "  </main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def share_bundle_print_html(manifest: dict) -> str:
    """Return print-friendly static HTML for browser Save as PDF workflows."""

    title = _html_text(manifest["title"])
    generated_at = _html_text(manifest["generated_at"])
    asset_rows = []
    for asset in manifest["assets"]:
        label = _html_text(asset["label"])
        bundle_path = _html_text(asset["bundle_path"])
        asset_rows.append(f"<tr><td>{label}</td><td><code>{bundle_path}</code></td></tr>")
    qr_rows = []
    for qr_asset in manifest.get("qr_assets", []):
        label = _html_text(qr_asset["label"])
        encoded_target = _html_text(qr_asset["encoded_target"])
        bundle_path = _html_text(qr_asset["bundle_path"])
        qr_rows.append(f"<tr><td>{label}</td><td><code>{encoded_target}</code></td><td><code>{bundle_path}</code></td></tr>")

    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="utf-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1">',
            f"  <title>{title} - Print View</title>",
            "  <style>",
            "    body { color: #111827; font-family: Georgia, 'Times New Roman', serif; margin: 2rem; }",
            "    main { max-width: 760px; }",
            "    h1, h2 { font-family: system-ui, sans-serif; }",
            "    table { border-collapse: collapse; width: 100%; }",
            "    th, td { border-bottom: 1px solid #d1d5db; padding: 0.55rem; text-align: left; }",
            "    code { overflow-wrap: anywhere; }",
            "    .meta { color: #4b5563; }",
            "    @media print {",
            "      body { margin: 0.65in; }",
            "      a { color: inherit; text-decoration: none; }",
            "      h2 { break-after: avoid; }",
            "      tr { break-inside: avoid; }",
            "    }",
            "  </style>",
            "</head>",
            "<body>",
            "  <main>",
            f"    <h1>{title}</h1>",
            f'    <p class="meta">Generated at: {generated_at}</p>',
            "    <h2>Included Files</h2>",
            "    <table>",
            "      <thead><tr><th>Label</th><th>Bundle path</th></tr></thead>",
            "      <tbody>",
            *[f"        {row}" for row in asset_rows],
            "      </tbody>",
            "    </table>",
            *(
                [
                    "    <h2>QR Targets</h2>",
                    "    <table>",
                    "      <thead><tr><th>Label</th><th>Encoded target</th><th>QR asset</th></tr></thead>",
                    "      <tbody>",
                    *[f"        {row}" for row in qr_rows],
                    "      </tbody>",
                    "    </table>",
                ]
                if qr_rows
                else []
            ),
            "    <p class=\"meta\">Use the browser print dialog or Save as PDF. This page does not call a remote conversion service.</p>",
            "  </main>",
            "</body>",
            "</html>",
            "",
        ]
    )


def write_local_share_bundle(
    *,
    title: str,
    generated_at: str,
    assets: tuple[ShareBundleAsset, ...] | list[ShareBundleAsset],
    output_dir: str | Path,
    output_root: str | Path | None = None,
    qr_target: str | None = None,
    include_print_entry: bool = True,
) -> ShareBundleWriteResult:
    """Write a static local share bundle with copied report assets."""

    target_dir = _resolve_output_dir(output_dir, output_root=output_root)
    qr_asset_path = "assets/bundle-entry-qr.png" if qr_target is not None else None
    manifest = build_share_bundle_manifest(
        title=title,
        generated_at=generated_at,
        assets=assets,
        qr_target=qr_target,
        qr_asset_path=qr_asset_path,
        include_print_entry=include_print_entry,
    )
    assets_dir = target_dir / "assets"
    target_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    copied_paths: list[str] = []
    for asset in assets:
        source = Path(asset.path).expanduser().resolve()
        if not source.is_file():
            raise ValueError(f"asset does not exist: {asset.path}")
        destination = assets_dir / source.name
        shutil.copyfile(source, destination)
        copied_paths.append(str(destination))

    qr_path: Path | None = None
    if qr_target is not None:
        qr_path = assets_dir / "bundle-entry-qr.png"
        write_qr_png(qr_target, qr_path, output_root=target_dir)

    manifest_path = target_dir / "manifest.json"
    index_path = target_dir / "index.html"
    print_path = target_dir / "print.html" if include_print_entry else None
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    index_path.write_text(share_bundle_index_html(manifest), encoding="utf-8", newline="\n")
    if print_path is not None:
        print_path.write_text(share_bundle_print_html(manifest), encoding="utf-8", newline="\n")
    return ShareBundleWriteResult(
        output_dir=str(target_dir),
        index_path=str(index_path),
        print_path=str(print_path) if print_path is not None else None,
        manifest_path=str(manifest_path),
        asset_paths=tuple(copied_paths),
        qr_asset_path=str(qr_path) if qr_path is not None else None,
    )


def write_qr_png(target: str, path: str | Path, *, output_root: str | Path | None = None) -> str:
    """Write a local QR PNG for an explicit target path or URL."""

    _require_qr_target(target)
    output_path = _resolve_qr_path(path, output_root=output_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image = qrcode.make(target)
    image.save(output_path)
    return str(output_path)


def _resolve_output_dir(path: str | Path, *, output_root: str | Path | None) -> Path:
    target = Path(path)
    if str(target).strip() == "":
        raise ValueError("output_dir is required")
    resolved_target = target.expanduser().resolve()
    if output_root is not None:
        resolved_root = Path(output_root).expanduser().resolve()
        try:
            resolved_target.relative_to(resolved_root)
        except ValueError as exc:
            raise ValueError("output_dir must stay inside output_root") from exc
    return resolved_target


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _require_qr_target(value: str) -> None:
    _require_text(value, "qr_target")
    if len(value) > 2048:
        raise ValueError("qr_target is too long")
    if "\n" in value or "\r" in value:
        raise ValueError("qr_target must be a single line")


def _resolve_qr_path(path: str | Path, *, output_root: str | Path | None) -> Path:
    target = Path(path)
    if str(target).strip() == "":
        raise ValueError("QR path is required")
    resolved_target = target.expanduser().resolve()
    if resolved_target.suffix.lower() != ".png":
        raise ValueError("QR asset path must end with .png")
    if output_root is not None:
        resolved_root = Path(output_root).expanduser().resolve()
        try:
            resolved_target.relative_to(resolved_root)
        except ValueError as exc:
            raise ValueError("QR asset path must stay inside output_root") from exc
    return resolved_target


def _html_text(value: object) -> str:
    return html.escape(str(value), quote=False)


def _html_attr(value: object) -> str:
    return html.escape(str(value), quote=True)
