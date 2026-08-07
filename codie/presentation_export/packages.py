"""Pure local package manifests for presentation/export artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any

from .writers import PresentationArtifactWriteReceipt


MANIFEST_VERSION = "phase43w-presentation-export-local-package-manifest"
SUPPORTED_MEDIA_TYPES = frozenset({"application/json", "text/markdown"})
SUPPORTED_ENCODINGS = frozenset({"utf-8"})
FORBIDDEN_PACKAGE_KEYS = frozenset(
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


class PresentationPackageManifestError(ValueError):
    """Raised when presentation/export package manifests violate their contract."""


@dataclass(frozen=True)
class PresentationPackageManifestOptions:
    package_label: str = "presentation-export-package"
    manifest_version: str = MANIFEST_VERSION
    privacy_summary: tuple[str, ...] = ("privacy states preserved from source artifacts",)
    accessibility_summary: tuple[str, ...] = ("accessibility states preserved from source artifacts",)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "package_label", _safe_label(self.package_label))
        _require_text(self.manifest_version, "manifest_version")
        object.__setattr__(self, "privacy_summary", _validate_status_tuple(self.privacy_summary, "privacy_summary"))
        object.__setattr__(self, "accessibility_summary", _validate_status_tuple(self.accessibility_summary, "accessibility_summary"))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationPackageArtifactRef:
    artifact_id: str
    source_packet_id: str
    source_snapshot_id: str
    receipt_id: str
    relative_path: str
    media_type: str
    encoding: str
    payload_hash: str
    byte_length: int
    artifact_class: str
    writer_version: str
    renderer_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.source_packet_id, "source_packet_id")
        _require_text(self.source_snapshot_id, "source_snapshot_id")
        _require_text(self.receipt_id, "receipt_id")
        object.__setattr__(self, "relative_path", _require_relative_path(self.relative_path))
        if self.media_type not in SUPPORTED_MEDIA_TYPES:
            raise PresentationPackageManifestError(f"unsupported media_type: {self.media_type}")
        if self.encoding not in SUPPORTED_ENCODINGS:
            raise PresentationPackageManifestError("encoding must be utf-8")
        _require_hash(self.payload_hash, "payload_hash")
        if not isinstance(self.byte_length, int) or self.byte_length < 0:
            raise PresentationPackageManifestError("byte_length must be a non-negative integer")
        _require_text(self.artifact_class, "artifact_class")
        _require_text(self.writer_version, "writer_version")
        _require_text(self.renderer_version, "renderer_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationPackageManifest:
    manifest_id: str
    package_label: str
    artifact_refs: tuple[PresentationPackageArtifactRef, ...]
    source_packet_ids: tuple[str, ...]
    source_snapshot_ids: tuple[str, ...]
    receipt_ids: tuple[str, ...]
    aggregate_payload_hash: str
    aggregate_byte_length: int
    privacy_summary: tuple[str, ...]
    accessibility_summary: tuple[str, ...]
    manifest_version: str = MANIFEST_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.manifest_id, "manifest_id")
        object.__setattr__(self, "package_label", _safe_label(self.package_label))
        refs = _sort_artifact_refs(self.artifact_refs)
        _reject_duplicate_paths(refs)
        _reject_conflicting_artifacts(refs)
        object.__setattr__(self, "artifact_refs", refs)
        object.__setattr__(self, "source_packet_ids", _validate_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "source_snapshot_ids", _validate_text_tuple(self.source_snapshot_ids, "source_snapshot_ids"))
        object.__setattr__(self, "receipt_ids", _validate_text_tuple(self.receipt_ids, "receipt_ids"))
        _require_hash(self.aggregate_payload_hash, "aggregate_payload_hash")
        if not isinstance(self.aggregate_byte_length, int) or self.aggregate_byte_length < 0:
            raise PresentationPackageManifestError("aggregate_byte_length must be a non-negative integer")
        object.__setattr__(self, "privacy_summary", _validate_status_tuple(self.privacy_summary, "privacy_summary"))
        object.__setattr__(self, "accessibility_summary", _validate_status_tuple(self.accessibility_summary, "accessibility_summary"))
        _require_text(self.manifest_version, "manifest_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_presentation_package_manifest(self)


def build_presentation_package_artifact_ref(
    receipt: PresentationArtifactWriteReceipt,
    *,
    relative_path: str | None = None,
    renderer_version: str = "unknown-renderer-version",
    metadata: dict[str, Any] | None = None,
) -> PresentationPackageArtifactRef:
    if not isinstance(receipt, PresentationArtifactWriteReceipt):
        raise PresentationPackageManifestError("receipt must be a PresentationArtifactWriteReceipt")
    artifact_path = relative_path or _artifact_path_from_receipt(receipt)
    return PresentationPackageArtifactRef(
        artifact_id=receipt.artifact_id,
        source_packet_id=receipt.source_packet_id,
        source_snapshot_id=receipt.source_snapshot_id,
        receipt_id=receipt.receipt_id,
        relative_path=artifact_path,
        media_type=receipt.media_type,
        encoding=receipt.encoding,
        payload_hash=receipt.payload_hash,
        byte_length=receipt.byte_length,
        artifact_class=receipt.artifact_class,
        writer_version=receipt.writer_version,
        renderer_version=renderer_version,
        metadata=metadata or {},
    )


def build_presentation_package_manifest(
    artifact_refs: tuple[PresentationPackageArtifactRef, ...],
    *,
    options: PresentationPackageManifestOptions | None = None,
) -> PresentationPackageManifest:
    resolved_options = options or PresentationPackageManifestOptions()
    refs = _sort_artifact_refs(artifact_refs)
    if not refs:
        raise PresentationPackageManifestError("package manifest requires at least one artifact ref")
    manifest_payload = {
        "package_label": resolved_options.package_label,
        "artifact_refs": [presentation_package_artifact_ref_to_dict(ref) for ref in refs],
        "manifest_version": resolved_options.manifest_version,
    }
    aggregate_payload_hash = _sha256_json(manifest_payload)
    manifest_id = f"manifest:{resolved_options.package_label}:{aggregate_payload_hash}"
    return PresentationPackageManifest(
        manifest_id=manifest_id,
        package_label=resolved_options.package_label,
        artifact_refs=refs,
        source_packet_ids=_unique_sorted(ref.source_packet_id for ref in refs),
        source_snapshot_ids=_unique_sorted(ref.source_snapshot_id for ref in refs),
        receipt_ids=_unique_sorted(ref.receipt_id for ref in refs),
        aggregate_payload_hash=aggregate_payload_hash,
        aggregate_byte_length=sum(ref.byte_length for ref in refs),
        privacy_summary=resolved_options.privacy_summary,
        accessibility_summary=resolved_options.accessibility_summary,
        manifest_version=resolved_options.manifest_version,
        metadata=resolved_options.metadata,
    )


def presentation_package_artifact_ref_to_dict(ref: PresentationPackageArtifactRef) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "artifact_id": ref.artifact_id,
            "source_packet_id": ref.source_packet_id,
            "source_snapshot_id": ref.source_snapshot_id,
            "receipt_id": ref.receipt_id,
            "relative_path": ref.relative_path,
            "media_type": ref.media_type,
            "encoding": ref.encoding,
            "payload_hash": ref.payload_hash,
            "byte_length": ref.byte_length,
            "artifact_class": ref.artifact_class,
            "writer_version": ref.writer_version,
            "renderer_version": ref.renderer_version,
            "metadata": ref.metadata,
        }
    )


def presentation_package_manifest_to_dict(manifest: PresentationPackageManifest) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "manifest_id": manifest.manifest_id,
            "manifest_version": manifest.manifest_version,
            "package_label": manifest.package_label,
            "source_packet_ids": list(manifest.source_packet_ids),
            "source_snapshot_ids": list(manifest.source_snapshot_ids),
            "receipt_ids": list(manifest.receipt_ids),
            "artifact_refs": [presentation_package_artifact_ref_to_dict(ref) for ref in manifest.artifact_refs],
            "aggregate_payload_hash": manifest.aggregate_payload_hash,
            "aggregate_byte_length": manifest.aggregate_byte_length,
            "privacy_summary": list(manifest.privacy_summary),
            "accessibility_summary": list(manifest.accessibility_summary),
            "metadata": manifest.metadata,
        }
    )


def validate_presentation_package_manifest(manifest: PresentationPackageManifest) -> PresentationPackageManifest:
    refs = manifest.artifact_refs
    if not refs:
        raise PresentationPackageManifestError("package manifest requires at least one artifact ref")
    if manifest.source_packet_ids != _unique_sorted(ref.source_packet_id for ref in refs):
        raise PresentationPackageManifestError("source_packet_ids must match artifact refs")
    if manifest.source_snapshot_ids != _unique_sorted(ref.source_snapshot_id for ref in refs):
        raise PresentationPackageManifestError("source_snapshot_ids must match artifact refs")
    if manifest.receipt_ids != _unique_sorted(ref.receipt_id for ref in refs):
        raise PresentationPackageManifestError("receipt_ids must match artifact refs")
    if manifest.aggregate_byte_length != sum(ref.byte_length for ref in refs):
        raise PresentationPackageManifestError("aggregate_byte_length must match artifact refs")
    expected_hash = _sha256_json(
        {
            "package_label": manifest.package_label,
            "artifact_refs": [presentation_package_artifact_ref_to_dict(ref) for ref in refs],
            "manifest_version": manifest.manifest_version,
        }
    )
    if manifest.aggregate_payload_hash != expected_hash:
        raise PresentationPackageManifestError("aggregate_payload_hash must match artifact refs")
    if manifest.manifest_id != f"manifest:{manifest.package_label}:{manifest.aggregate_payload_hash}":
        raise PresentationPackageManifestError("manifest_id must be derived from package label and aggregate hash")
    return manifest


def _artifact_path_from_receipt(receipt: PresentationArtifactWriteReceipt) -> str:
    artifact_files = [
        item
        for item in receipt.files
        if item.get("media_type") == receipt.media_type
        and item.get("payload_hash") == receipt.payload_hash
        and item.get("bytes_written") == receipt.byte_length
    ]
    if len(artifact_files) != 1:
        raise PresentationPackageManifestError("receipt must contain exactly one artifact file entry")
    file_entry = artifact_files[0]
    return _require_relative_path(file_entry.get("path"))


def _sort_artifact_refs(refs: tuple[PresentationPackageArtifactRef, ...]) -> tuple[PresentationPackageArtifactRef, ...]:
    if not isinstance(refs, tuple):
        raise PresentationPackageManifestError("artifact_refs must be a tuple")
    for ref in refs:
        if not isinstance(ref, PresentationPackageArtifactRef):
            raise PresentationPackageManifestError("artifact_refs must contain PresentationPackageArtifactRef values")
    return tuple(sorted(refs, key=lambda ref: (ref.relative_path, ref.artifact_id, ref.payload_hash)))


def _reject_duplicate_paths(refs: tuple[PresentationPackageArtifactRef, ...]) -> None:
    seen: set[str] = set()
    for ref in refs:
        if ref.relative_path in seen:
            raise PresentationPackageManifestError(f"duplicate relative path: {ref.relative_path}")
        seen.add(ref.relative_path)


def _reject_conflicting_artifacts(refs: tuple[PresentationPackageArtifactRef, ...]) -> None:
    seen: dict[str, str] = {}
    for ref in refs:
        previous_hash = seen.get(ref.artifact_id)
        if previous_hash is not None and previous_hash != ref.payload_hash:
            raise PresentationPackageManifestError(f"conflicting duplicate artifact: {ref.artifact_id}")
        seen[ref.artifact_id] = ref.payload_hash


def _require_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationPackageManifestError("relative_path is required")
    text = value.strip()
    if "\\" in text or ":" in text:
        raise PresentationPackageManifestError("relative paths must be portable and cannot include drive markers")
    path = PurePosixPath(text)
    if path.is_absolute():
        raise PresentationPackageManifestError("relative paths must not be absolute")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise PresentationPackageManifestError("relative paths must not contain traversal segments")
    if path.suffix.lower() not in {".json", ".md"}:
        raise PresentationPackageManifestError("relative paths must point to JSON or Markdown artifacts")
    return text


def _safe_label(value: Any) -> str:
    text = _require_text(value, "package_label")
    if "\\" in text or "/" in text or ":" in text:
        raise PresentationPackageManifestError("package_label must not contain path separators or drive markers")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip(".-")
    if not safe:
        raise PresentationPackageManifestError("package_label cannot be normalized safely")
    return safe


def _validate_status_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    items = _validate_text_tuple(value, field_name)
    if not items:
        raise PresentationPackageManifestError(f"{field_name} requires at least one text status")
    return items


def _validate_text_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        raise PresentationPackageManifestError(f"{field_name} must be a tuple")
    return tuple(_require_text(item, field_name) for item in value)


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise PresentationPackageManifestError("metadata must be an object")
    _reject_forbidden_package_authority(metadata)
    return _sorted_json_object(metadata)


def _reject_forbidden_package_authority(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if _normalize_key(key) in FORBIDDEN_PACKAGE_KEYS:
                raise PresentationPackageManifestError(f"package metadata contains forbidden authority key: {key}")
            _reject_forbidden_package_authority(child)
    elif isinstance(value, list):
        for child in value:
            _reject_forbidden_package_authority(child)


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationPackageManifestError(f"{field_name} is required")
    return value.strip()


def _require_hash(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", text):
        raise PresentationPackageManifestError(f"{field_name} must be a sha256 digest")
    return text


def _unique_sorted(values: Any) -> tuple[str, ...]:
    return tuple(sorted({_require_text(value, "identity") for value in values}))


def _sha256_json(payload: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_json_bytes(payload)).hexdigest()


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
