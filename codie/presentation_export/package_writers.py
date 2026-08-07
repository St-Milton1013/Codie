"""Local safe writer for presentation/export package manifests."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .packages import (
    PresentationPackageManifest,
    PresentationPackageManifestError,
    presentation_package_manifest_to_dict,
    validate_presentation_package_manifest,
)


PACKAGE_WRITER_VERSION = "phase43z-presentation-export-local-package-writer"
RECEIPT_VERSION = "phase43z-presentation-package-write-receipt"
FORBIDDEN_PACKAGE_WRITER_KEYS = frozenset(
    {
        "absolute_path",
        "api",
        "chain_of_thought",
        "cookie",
        "credential",
        "database",
        "device_api",
        "file_path",
        "model_prompt",
        "output_path",
        "path",
        "private_deck_text",
        "prompt",
        "provider_cookie",
        "provider_write",
        "provider_write_back",
        "publish",
        "raw_input",
        "repository",
        "route",
        "secret",
        "session",
        "stream_deck_adapter",
        "stream_deck_confirm",
        "stream_deck_consent",
        "stream_deck_retry",
        "stream_deck_write",
        "sync",
        "token",
        "trace",
        "upload",
        "url",
        "webhook",
    }
)


class PresentationPackageWriteError(ValueError):
    """Raised when a presentation/export package manifest cannot be written safely."""


@dataclass(frozen=True)
class PresentationPackageWriteOptions:
    manifest_basename: str | None = None
    overwrite: bool = False
    create_output_root: bool = False
    writer_version: str = PACKAGE_WRITER_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.overwrite, bool):
            raise PresentationPackageWriteError("overwrite must be a bool")
        if not isinstance(self.create_output_root, bool):
            raise PresentationPackageWriteError("create_output_root must be a bool")
        _require_text(self.writer_version, "writer_version")
        if self.manifest_basename is not None:
            object.__setattr__(self, "manifest_basename", _safe_explicit_basename(self.manifest_basename))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationPackageWriteReceipt:
    receipt_id: str
    receipt_version: str
    manifest_id: str
    manifest_version: str
    package_label: str
    manifest_payload_hash: str
    manifest_byte_length: int
    files: tuple[dict[str, Any], ...]
    overwrite: bool
    writer_version: str = PACKAGE_WRITER_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.receipt_id, "receipt_id")
        _require_text(self.receipt_version, "receipt_version")
        _require_text(self.manifest_id, "manifest_id")
        _require_text(self.manifest_version, "manifest_version")
        _safe_label(self.package_label)
        _require_hash(self.manifest_payload_hash, "manifest_payload_hash")
        if not isinstance(self.manifest_byte_length, int) or self.manifest_byte_length < 0:
            raise PresentationPackageWriteError("manifest_byte_length must be a non-negative integer")
        if not isinstance(self.overwrite, bool):
            raise PresentationPackageWriteError("overwrite must be a bool")
        _require_text(self.writer_version, "writer_version")
        object.__setattr__(self, "files", tuple(_validate_receipt_file(item) for item in self.files))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


def write_presentation_package_manifest(
    manifest: PresentationPackageManifest,
    output_root: str | Path,
    *,
    options: PresentationPackageWriteOptions | None = None,
) -> PresentationPackageWriteReceipt:
    """Write an already-built package manifest plus a deterministic local receipt."""

    resolved_options = options or PresentationPackageWriteOptions()
    _validate_manifest(manifest)
    root = _resolve_output_root(output_root, create=resolved_options.create_output_root)
    basename = resolved_options.manifest_basename or _safe_filename_stem(manifest.package_label)
    manifest_relative_path = f"{basename}.package-manifest.json"
    receipt_relative_path = f"{basename}.package-receipt.json"
    manifest_payload = presentation_package_manifest_to_dict(manifest)
    manifest_bytes = _json_bytes(manifest_payload)
    receipt_payload = _receipt_payload(
        manifest,
        manifest_payload_hash=_sha256(manifest_bytes),
        manifest_byte_length=len(manifest_bytes),
        manifest_relative_path=manifest_relative_path,
        receipt_relative_path=receipt_relative_path,
        options=resolved_options,
    )
    prepared = (
        _prepared_write(
            manifest_relative_path,
            "application/json",
            manifest_bytes,
            root,
            overwrite=resolved_options.overwrite,
        ),
        _prepared_write(
            receipt_relative_path,
            "application/json",
            _json_bytes(receipt_payload),
            root,
            overwrite=resolved_options.overwrite,
        ),
    )
    _reject_duplicate_paths(prepared)

    written: list[dict[str, Any]] = []
    for relative_path, target, media_type, payload in prepared:
        _atomic_write_bytes(target, payload)
        written.append(
            {
                "path": relative_path,
                "media_type": media_type,
                "bytes_written": len(payload),
                "payload_hash": _sha256(payload),
            }
        )

    return PresentationPackageWriteReceipt(
        receipt_id=receipt_payload["receipt_id"],
        receipt_version=RECEIPT_VERSION,
        manifest_id=manifest.manifest_id,
        manifest_version=manifest.manifest_version,
        package_label=manifest.package_label,
        manifest_payload_hash=receipt_payload["manifest_payload_hash"],
        manifest_byte_length=receipt_payload["manifest_byte_length"],
        files=tuple(written),
        overwrite=resolved_options.overwrite,
        writer_version=resolved_options.writer_version,
        metadata=resolved_options.metadata,
    )


def presentation_package_write_receipt_to_dict(receipt: PresentationPackageWriteReceipt) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "receipt_id": receipt.receipt_id,
            "receipt_version": receipt.receipt_version,
            "manifest_id": receipt.manifest_id,
            "manifest_version": receipt.manifest_version,
            "package_label": receipt.package_label,
            "manifest_payload_hash": receipt.manifest_payload_hash,
            "manifest_byte_length": receipt.manifest_byte_length,
            "files": list(receipt.files),
            "overwrite": receipt.overwrite,
            "writer_version": receipt.writer_version,
            "metadata": receipt.metadata,
        }
    )


def _receipt_payload(
    manifest: PresentationPackageManifest,
    *,
    manifest_payload_hash: str,
    manifest_byte_length: int,
    manifest_relative_path: str,
    receipt_relative_path: str,
    options: PresentationPackageWriteOptions,
) -> dict[str, Any]:
    receipt_id = f"package-receipt:{manifest.manifest_id}:{manifest_payload_hash}"
    return _sorted_json_object(
        {
            "receipt_id": receipt_id,
            "receipt_version": RECEIPT_VERSION,
            "manifest_id": manifest.manifest_id,
            "manifest_version": manifest.manifest_version,
            "package_label": manifest.package_label,
            "manifest_payload_hash": manifest_payload_hash,
            "manifest_byte_length": manifest_byte_length,
            "overwrite": options.overwrite,
            "writer_version": options.writer_version,
            "files": [
                {
                    "path": manifest_relative_path,
                    "media_type": "application/json",
                    "bytes": manifest_byte_length,
                    "payload_hash": manifest_payload_hash,
                },
                {
                    "path": receipt_relative_path,
                    "media_type": "application/json",
                    "receipt_self_reference": True,
                },
            ],
            "metadata": options.metadata,
        }
    )


def _validate_manifest(manifest: PresentationPackageManifest) -> None:
    if not isinstance(manifest, PresentationPackageManifest):
        raise PresentationPackageWriteError("manifest must be a PresentationPackageManifest")
    try:
        validate_presentation_package_manifest(manifest)
    except PresentationPackageManifestError as exc:
        raise PresentationPackageWriteError(str(exc)) from exc
    _validate_metadata(manifest.metadata)
    for ref in manifest.artifact_refs:
        _validate_metadata(ref.metadata)


def _resolve_output_root(output_root: str | Path, *, create: bool) -> Path:
    if str(output_root).strip() == "":
        raise PresentationPackageWriteError("output_root is required")
    root = Path(output_root).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise PresentationPackageWriteError("output_root must be a directory")
    if not root.exists():
        if not create:
            raise PresentationPackageWriteError("output_root does not exist; pass create_output_root=True to create it")
        root.mkdir(parents=True, exist_ok=True)
    return root


def _prepared_write(
    relative_path: str,
    media_type: str,
    payload: bytes,
    root: Path,
    *,
    overwrite: bool,
) -> tuple[str, Path, str, bytes]:
    target = _resolve_relative_target(relative_path, root)
    if target.exists() and not overwrite:
        raise PresentationPackageWriteError("output file already exists; pass overwrite=True to replace it")
    return relative_path, target, media_type, payload


def _resolve_relative_target(relative_path: str, root: Path) -> Path:
    checked = _require_relative_path(relative_path)
    target = (root / checked).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise PresentationPackageWriteError("output target must stay inside output_root") from exc
    return target


def _require_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationPackageWriteError("output path is required")
    if "\\" in value or ":" in value:
        raise PresentationPackageWriteError("output paths must be portable relative paths")
    path = Path(value)
    if path.is_absolute():
        raise PresentationPackageWriteError("output paths must be relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise PresentationPackageWriteError("output paths must not contain empty or traversal segments")
    if path.suffix.lower() != ".json":
        raise PresentationPackageWriteError("output paths must end with .json")
    return value


def _safe_explicit_basename(value: str) -> str:
    text = _require_text(value, "manifest_basename")
    if "\\" in text or "/" in text or ":" in text:
        raise PresentationPackageWriteError("manifest_basename must not contain path separators or drive markers")
    if text.lower().endswith(".json"):
        raise PresentationPackageWriteError("manifest_basename must not include a file extension")
    return _safe_filename_stem(text)


def _safe_filename_stem(value: str) -> str:
    text = _require_text(value, "filename")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip(".-")
    if not safe:
        raise PresentationPackageWriteError("filename cannot be normalized safely")
    return safe


def _safe_label(value: str) -> str:
    text = _require_text(value, "package_label")
    if "\\" in text or "/" in text or ":" in text:
        raise PresentationPackageWriteError("package_label must not contain path separators or drive markers")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip(".-")
    if not safe:
        raise PresentationPackageWriteError("package_label cannot be normalized safely")
    return safe


def _reject_duplicate_paths(prepared: tuple[tuple[str, Path, str, bytes], ...]) -> None:
    seen: set[str] = set()
    for relative_path, _, _, _ in prepared:
        if relative_path in seen:
            raise PresentationPackageWriteError(f"duplicate output path: {relative_path}")
        seen.add(relative_path)


def _validate_receipt_file(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise PresentationPackageWriteError("receipt file entries must be objects")
    path = _require_relative_path(item.get("path"))
    media_type = _require_text(item.get("media_type"), "media_type")
    if not isinstance(item.get("bytes_written"), int) or item["bytes_written"] < 0:
        raise PresentationPackageWriteError("bytes_written must be a non-negative integer")
    payload_hash = _require_hash(item.get("payload_hash"), "payload_hash")
    return {"path": path, "media_type": media_type, "bytes_written": item["bytes_written"], "payload_hash": payload_hash}


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise PresentationPackageWriteError("metadata must be an object")
    _reject_forbidden_package_writer_authority(metadata)
    return _sorted_json_object(metadata)


def _reject_forbidden_package_writer_authority(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if _normalize_key(key) in FORBIDDEN_PACKAGE_WRITER_KEYS:
                raise PresentationPackageWriteError(f"package writer metadata contains forbidden authority key: {key}")
            _reject_forbidden_package_writer_authority(child)
    elif isinstance(value, list):
        for child in value:
            _reject_forbidden_package_writer_authority(child)


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationPackageWriteError(f"{field_name} is required")
    return value.strip()


def _require_hash(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", text):
        raise PresentationPackageWriteError(f"{field_name} must be a sha256 digest")
    return text


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _atomic_write_bytes(target: Path, payload: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.tmp")
    temp.write_bytes(payload)
    os.replace(temp, target)


def _sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
