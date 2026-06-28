"""Static local share bundles for Codie reports."""

from __future__ import annotations

import html
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


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
    manifest_path: str
    asset_paths: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.output_dir.strip():
            raise ValueError("output_dir is required")
        if not self.index_path.strip():
            raise ValueError("index_path is required")
        if not self.manifest_path.strip():
            raise ValueError("manifest_path is required")


def build_share_bundle_manifest(
    *,
    title: str,
    generated_at: str,
    assets: tuple[ShareBundleAsset, ...] | list[ShareBundleAsset],
    entry_file: str = "index.html",
) -> dict:
    """Return deterministic metadata for a local static report bundle."""

    _require_text(title, "title")
    _require_text(generated_at, "generated_at")
    _require_text(entry_file, "entry_file")
    if not assets:
        raise ValueError("at least one asset is required")

    return {
        "bundle_version": "1",
        "title": title,
        "generated_at": generated_at,
        "entry_file": entry_file,
        "qr_ready_entry": entry_file,
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


def share_bundle_index_html(manifest: dict) -> str:
    """Return a simple static HTML index for a local share bundle."""

    title = _html_text(manifest["title"])
    generated_at = _html_text(manifest["generated_at"])
    asset_items = []
    for asset in manifest["assets"]:
        label = _html_text(asset["label"])
        bundle_path = _html_attr(asset["bundle_path"])
        asset_items.append(f'<li><a href="{bundle_path}">{label}</a></li>')

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
            "    <p class=\"meta\">Static local bundle. No network service is required by this page.</p>",
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
) -> ShareBundleWriteResult:
    """Write a static local share bundle with copied report assets."""

    target_dir = _resolve_output_dir(output_dir, output_root=output_root)
    manifest = build_share_bundle_manifest(title=title, generated_at=generated_at, assets=assets)
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

    manifest_path = target_dir / "manifest.json"
    index_path = target_dir / "index.html"
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")
    index_path.write_text(share_bundle_index_html(manifest), encoding="utf-8", newline="\n")
    return ShareBundleWriteResult(
        output_dir=str(target_dir),
        index_path=str(index_path),
        manifest_path=str(manifest_path),
        asset_paths=tuple(copied_paths),
    )


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


def _html_text(value: object) -> str:
    return html.escape(str(value), quote=False)


def _html_attr(value: object) -> str:
    return html.escape(str(value), quote=True)
