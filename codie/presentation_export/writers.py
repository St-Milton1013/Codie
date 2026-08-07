"""Local safe writer for rendered presentation/export artifacts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .renderers import RenderedPresentationArtifact


WRITER_VERSION = "phase43q-presentation-export-safe-writer"
MEDIA_TYPE_EXTENSIONS = {
    "application/json": ".json",
    "text/markdown": ".md",
}
FORBIDDEN_WRITER_KEYS = frozenset(
    {
        "path",
        "file_path",
        "output_path",
        "absolute_path",
        "provider_write",
        "provider_write_back",
        "publish",
        "sync",
        "upload",
        "api",
        "route",
        "stream_deck_write",
        "stream_deck_adapter",
        "device_api",
        "webhook",
        "url",
        "token",
        "credential",
        "secret",
    }
)


class PresentationArtifactWriteError(ValueError):
    """Raised when a rendered presentation artifact cannot be written safely."""


@dataclass(frozen=True)
class PresentationArtifactWriteOptions:
    basename: str | None = None
    overwrite: bool = False
    create_output_root: bool = False
    writer_version: str = WRITER_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.overwrite, bool):
            raise PresentationArtifactWriteError("overwrite must be a bool")
        if not isinstance(self.create_output_root, bool):
            raise PresentationArtifactWriteError("create_output_root must be a bool")
        _require_text(self.writer_version, "writer_version")
        if self.basename is not None:
            object.__setattr__(self, "basename", _safe_explicit_basename(self.basename))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationArtifactWriteReceipt:
    receipt_id: str
    root: str
    artifact_id: str
    artifact_class: str
    source_packet_id: str
    source_snapshot_id: str
    media_type: str
    encoding: str
    payload_hash: str
    byte_length: int
    files: tuple[dict[str, Any], ...]
    overwrite: bool
    writer_version: str = WRITER_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.receipt_id, "receipt_id")
        _require_text(self.root, "root")
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.artifact_class, "artifact_class")
        _require_text(self.source_packet_id, "source_packet_id")
        _require_text(self.source_snapshot_id, "source_snapshot_id")
        _require_text(self.media_type, "media_type")
        if self.encoding != "utf-8":
            raise PresentationArtifactWriteError("encoding must be utf-8")
        _require_text(self.payload_hash, "payload_hash")
        if not isinstance(self.byte_length, int) or self.byte_length < 0:
            raise PresentationArtifactWriteError("byte_length must be a non-negative integer")
        if not isinstance(self.overwrite, bool):
            raise PresentationArtifactWriteError("overwrite must be a bool")
        _require_text(self.writer_version, "writer_version")
        object.__setattr__(self, "files", tuple(_validate_receipt_file(item) for item in self.files))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


def write_rendered_presentation_artifact(
    artifact: RenderedPresentationArtifact,
    output_root: str | Path,
    *,
    options: PresentationArtifactWriteOptions | None = None,
) -> PresentationArtifactWriteReceipt:
    """Write one already-rendered presentation artifact plus a deterministic receipt."""

    resolved_options = options or PresentationArtifactWriteOptions()
    _validate_artifact(artifact)
    root = _resolve_output_root(output_root, create=resolved_options.create_output_root)
    basename = resolved_options.basename or _safe_filename_stem(artifact.artifact_id)
    artifact_relative_path = f"{basename}{_extension_for(artifact.media_type)}"
    receipt_relative_path = f"{basename}.receipt.json"
    receipt_payload = _receipt_payload(
        artifact,
        root=str(root),
        artifact_relative_path=artifact_relative_path,
        receipt_relative_path=receipt_relative_path,
        options=resolved_options,
    )
    prepared = (
        _prepared_write(artifact_relative_path, artifact.media_type, artifact.payload, root, overwrite=resolved_options.overwrite),
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

    return PresentationArtifactWriteReceipt(
        receipt_id=receipt_payload["receipt_id"],
        root=str(root),
        artifact_id=artifact.artifact_id,
        artifact_class=artifact.artifact_class,
        source_packet_id=artifact.source_packet_id,
        source_snapshot_id=artifact.source_snapshot_id,
        media_type=artifact.media_type,
        encoding=artifact.encoding,
        payload_hash=artifact.payload_hash,
        byte_length=artifact.byte_length,
        files=tuple(written),
        overwrite=resolved_options.overwrite,
        writer_version=resolved_options.writer_version,
        metadata=resolved_options.metadata,
    )


def rendered_presentation_write_receipt_to_dict(receipt: PresentationArtifactWriteReceipt) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "receipt_id": receipt.receipt_id,
            "root": receipt.root,
            "artifact_id": receipt.artifact_id,
            "artifact_class": receipt.artifact_class,
            "source_packet_id": receipt.source_packet_id,
            "source_snapshot_id": receipt.source_snapshot_id,
            "media_type": receipt.media_type,
            "encoding": receipt.encoding,
            "payload_hash": receipt.payload_hash,
            "byte_length": receipt.byte_length,
            "files": list(receipt.files),
            "overwrite": receipt.overwrite,
            "writer_version": receipt.writer_version,
            "metadata": receipt.metadata,
        }
    )


def _receipt_payload(
    artifact: RenderedPresentationArtifact,
    *,
    root: str,
    artifact_relative_path: str,
    receipt_relative_path: str,
    options: PresentationArtifactWriteOptions,
) -> dict[str, Any]:
    receipt_id = f"receipt:{artifact.artifact_id}:{artifact.payload_hash}"
    payload = {
        "receipt_id": receipt_id,
        "receipt_version": "phase43q-presentation-artifact-write-receipt",
        "root": root,
        "artifact_id": artifact.artifact_id,
        "artifact_class": artifact.artifact_class,
        "source_packet_id": artifact.source_packet_id,
        "source_snapshot_id": artifact.source_snapshot_id,
        "media_type": artifact.media_type,
        "encoding": artifact.encoding,
        "payload_hash": artifact.payload_hash,
        "byte_length": artifact.byte_length,
        "overwrite": options.overwrite,
        "receipt_path": receipt_relative_path,
        "writer_version": options.writer_version,
        "files": [
            {
                "path": artifact_relative_path,
                "media_type": artifact.media_type,
                "bytes": artifact.byte_length,
                "payload_hash": artifact.payload_hash,
            }
        ],
        "metadata": options.metadata,
    }
    return _sorted_json_object(payload)


def _validate_artifact(artifact: RenderedPresentationArtifact) -> None:
    if not isinstance(artifact, RenderedPresentationArtifact):
        raise PresentationArtifactWriteError("artifact must be a RenderedPresentationArtifact")
    if artifact.encoding != "utf-8":
        raise PresentationArtifactWriteError("artifact encoding must be utf-8")
    if artifact.media_type not in MEDIA_TYPE_EXTENSIONS:
        raise PresentationArtifactWriteError(f"unsupported artifact media_type: {artifact.media_type}")
    if artifact.payload_hash != _sha256(artifact.payload):
        raise PresentationArtifactWriteError("artifact payload_hash must match payload bytes")
    if artifact.byte_length != len(artifact.payload):
        raise PresentationArtifactWriteError("artifact byte_length must match payload bytes")
    _validate_metadata(artifact.metadata)


def _resolve_output_root(output_root: str | Path, *, create: bool) -> Path:
    if str(output_root).strip() == "":
        raise PresentationArtifactWriteError("output_root is required")
    root = Path(output_root).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise PresentationArtifactWriteError("output_root must be a directory")
    if not root.exists():
        if not create:
            raise PresentationArtifactWriteError("output_root does not exist; pass create_output_root=True to create it")
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
        raise PresentationArtifactWriteError("output file already exists; pass overwrite=True to replace it")
    return relative_path, target, media_type, payload


def _resolve_relative_target(relative_path: str, root: Path) -> Path:
    checked = _require_relative_path(relative_path)
    target = (root / checked).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise PresentationArtifactWriteError("output target must stay inside output_root") from exc
    return target


def _require_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationArtifactWriteError("output path is required")
    if "\\" in value or ":" in value:
        raise PresentationArtifactWriteError("output paths must be portable relative paths")
    path = Path(value)
    if path.is_absolute():
        raise PresentationArtifactWriteError("output paths must be relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise PresentationArtifactWriteError("output paths must not contain empty or traversal segments")
    if path.suffix.lower() not in {".json", ".md"}:
        raise PresentationArtifactWriteError("output paths must end with .json or .md")
    return value


def _safe_explicit_basename(value: str) -> str:
    text = _require_text(value, "basename")
    if "\\" in text or "/" in text or ":" in text:
        raise PresentationArtifactWriteError("basename must not contain path separators or drive markers")
    if text.lower().endswith((".json", ".md")):
        raise PresentationArtifactWriteError("basename must not include a file extension")
    return _safe_filename_stem(text)


def _safe_filename_stem(value: str) -> str:
    text = _require_text(value, "filename")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip(".-")
    if not safe:
        raise PresentationArtifactWriteError("filename cannot be normalized safely")
    return safe


def _extension_for(media_type: str) -> str:
    try:
        return MEDIA_TYPE_EXTENSIONS[media_type]
    except KeyError as exc:
        raise PresentationArtifactWriteError(f"unsupported artifact media_type: {media_type}") from exc


def _reject_duplicate_paths(prepared: tuple[tuple[str, Path, str, bytes], ...]) -> None:
    seen: set[str] = set()
    for relative_path, _, _, _ in prepared:
        if relative_path in seen:
            raise PresentationArtifactWriteError(f"duplicate output path: {relative_path}")
        seen.add(relative_path)


def _validate_receipt_file(item: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise PresentationArtifactWriteError("receipt file entries must be objects")
    path = _require_relative_path(item.get("path"))
    media_type = _require_text(item.get("media_type"), "media_type")
    if not isinstance(item.get("bytes_written"), int) or item["bytes_written"] < 0:
        raise PresentationArtifactWriteError("bytes_written must be a non-negative integer")
    payload_hash = _require_text(item.get("payload_hash"), "payload_hash")
    return {"path": path, "media_type": media_type, "bytes_written": item["bytes_written"], "payload_hash": payload_hash}


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise PresentationArtifactWriteError("metadata must be an object")
    _reject_forbidden_writer_authority(metadata)
    return _sorted_json_object(metadata)


def _reject_forbidden_writer_authority(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if _normalize_key(key) in FORBIDDEN_WRITER_KEYS:
                raise PresentationArtifactWriteError(f"writer metadata contains forbidden authority key: {key}")
            _reject_forbidden_writer_authority(child)
    elif isinstance(value, list):
        for child in value:
            _reject_forbidden_writer_authority(child)


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationArtifactWriteError(f"{field_name} is required")
    return value.strip()


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
