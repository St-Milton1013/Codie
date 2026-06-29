"""Deterministic zip packaging for local Codie share bundles."""

from __future__ import annotations

import hashlib
import json
import mimetypes
import zipfile
from dataclasses import dataclass
from pathlib import Path


_ZIP_EPOCH = (1980, 1, 1, 0, 0, 0)
_FORBIDDEN_SUFFIXES = {
    ".db",
    ".env",
    ".key",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite" + "3",
}
_FORBIDDEN_NAMES = {
    ".env",
    ".gitignore",
    "local.config.json",
    "local_settings.json",
}


@dataclass(frozen=True)
class ShareBundleZipResult:
    zip_path: str
    bytes_written: int
    file_count: int
    total_bytes: int
    rejected_files: tuple[dict, ...]

    def __post_init__(self) -> None:
        if not self.zip_path.strip():
            raise ValueError("zip_path is required")
        if self.bytes_written < 0:
            raise ValueError("bytes_written cannot be negative")
        if self.file_count < 0:
            raise ValueError("file_count cannot be negative")
        if self.total_bytes < 0:
            raise ValueError("total_bytes cannot be negative")


def build_share_bundle_zip_manifest(
    *,
    bundle_dir: str | Path,
    generated_at: str,
) -> dict:
    """Return deterministic zip manifest metadata for a local share bundle."""

    _require_text(generated_at, "generated_at")
    root = _resolve_bundle_dir(bundle_dir)
    entries, rejected = _scan_bundle_files(root)
    if not entries:
        raise ValueError("share bundle has no accepted files to zip")
    total_bytes = sum(entry["byte_size"] for entry in entries)
    return {
        "zip_manifest_version": "1",
        "generated_at": generated_at,
        "source_bundle_dir": str(root),
        "entry_file": "index.html",
        "file_count": len(entries),
        "total_bytes": total_bytes,
        "files": entries,
        "rejected_files": rejected,
        "privacy_notes": [
            "Zip contains only accepted files from the selected local share bundle.",
            "No outbound delivery, public link, provider call, or database access is performed by zip packaging.",
            "Rejected files are excluded from the archive.",
        ],
    }


def validate_share_bundle_zip_payload(*, bundle_dir: str | Path, generated_at: str) -> dict:
    """Validate and describe the payload that would be written into a zip."""

    return build_share_bundle_zip_manifest(bundle_dir=bundle_dir, generated_at=generated_at)


def write_share_bundle_zip(
    *,
    bundle_dir: str | Path,
    output: str | Path,
    output_root: str | Path | None = None,
    generated_at: str,
) -> ShareBundleZipResult:
    """Write a deterministic local zip package for a share bundle."""

    manifest = build_share_bundle_zip_manifest(bundle_dir=bundle_dir, generated_at=generated_at)
    root = Path(manifest["source_bundle_dir"])
    zip_path = _resolve_zip_output(output, output_root=output_root)
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    file_payloads: dict[str, bytes] = {}
    for entry in manifest["files"]:
        bundle_path = entry["bundle_path"]
        file_payloads[bundle_path] = (root / Path(bundle_path)).read_bytes()
    file_payloads["zip-manifest.json"] = json.dumps(manifest, sort_keys=True, indent=2).encode("utf-8") + b"\n"

    seen: set[str] = set()
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for archive_name in sorted(file_payloads):
            _validate_archive_name(archive_name)
            if archive_name in seen:
                raise ValueError(f"duplicate archive path: {archive_name}")
            seen.add(archive_name)
            info = zipfile.ZipInfo(archive_name)
            info.date_time = _ZIP_EPOCH
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file_payloads[archive_name])

    return ShareBundleZipResult(
        zip_path=str(zip_path),
        bytes_written=zip_path.stat().st_size,
        file_count=manifest["file_count"],
        total_bytes=manifest["total_bytes"],
        rejected_files=tuple(manifest["rejected_files"]),
    )


def _scan_bundle_files(root: Path) -> tuple[list[dict], list[dict]]:
    required = (root / "index.html", root / "manifest.json")
    for path in required:
        if not path.is_file():
            raise ValueError(f"share bundle missing required file: {path.name}")

    entries: list[dict] = []
    rejected: list[dict] = []
    seen_archive_paths: set[str] = set()
    for path in sorted(root.rglob("*"), key=lambda item: _bundle_path(root, item)):
        if path.is_dir():
            continue
        bundle_path = _bundle_path(root, path)
        if path.is_symlink():
            rejected.append(_rejected_file(bundle_path, "symlink"))
            continue
        if _is_forbidden_payload(path, bundle_path):
            rejected.append(_rejected_file(bundle_path, "forbidden_payload"))
            continue
        _validate_archive_name(bundle_path)
        if bundle_path in seen_archive_paths:
            raise ValueError(f"duplicate archive path: {bundle_path}")
        seen_archive_paths.add(bundle_path)
        data = path.read_bytes()
        entries.append(
            {
                "bundle_path": bundle_path,
                "byte_size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "content_type_guess": mimetypes.guess_type(bundle_path)[0],
            }
        )
    return entries, rejected


def _resolve_bundle_dir(bundle_dir: str | Path) -> Path:
    if str(bundle_dir).strip() == "":
        raise ValueError("bundle_dir is required")
    root = Path(bundle_dir).expanduser().resolve()
    if not root.is_dir():
        raise ValueError("bundle_dir must be an existing directory")
    return root


def _resolve_zip_output(path: str | Path, *, output_root: str | Path | None) -> Path:
    if str(path).strip() == "":
        raise ValueError("output is required")
    target = Path(path).expanduser().resolve()
    if target.suffix.lower() != ".zip":
        raise ValueError("output path must end with .zip")
    if output_root is not None:
        root = Path(output_root).expanduser().resolve()
        try:
            target.relative_to(root)
        except ValueError as exc:
            raise ValueError("output path must stay inside output_root") from exc
    return target


def _bundle_path(root: Path, path: Path) -> str:
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ValueError("share bundle file is outside bundle root") from exc
    return relative.as_posix()


def _validate_archive_name(name: str) -> None:
    if not name or name.startswith("/") or name.startswith("\\"):
        raise ValueError("archive paths must be relative")
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe archive path: {name}")
    if "\\" in name:
        raise ValueError(f"archive path must use forward slashes: {name}")


def _is_forbidden_payload(path: Path, bundle_path: str) -> bool:
    lower_name = path.name.lower()
    lower_path = bundle_path.lower()
    if lower_name in _FORBIDDEN_NAMES:
        return True
    if path.suffix.lower() in _FORBIDDEN_SUFFIXES:
        return True
    return "raw_provider_payload" in lower_path or "provider_payload" in lower_path


def _rejected_file(bundle_path: str, reason: str) -> dict:
    return {"bundle_path": bundle_path, "reason": reason}


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
