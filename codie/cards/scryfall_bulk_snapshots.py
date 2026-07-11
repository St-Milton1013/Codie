"""Local Scryfall bulk snapshot manifest helpers.

This module is fixture-first and local-only. It does not download Scryfall
bulk data, write files, read SQLite, or replace the existing Phase 2 card truth
lookup/import path.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping


SCRYFALL_BULK_SNAPSHOT_VERSION = "scryfall-bulk-snapshot-v1"


class ScryfallBulkSnapshotError(ValueError):
    """Raised when a local Scryfall bulk snapshot cannot be represented safely."""


@dataclass(frozen=True)
class ScryfallBulkFileRef:
    """Reference to one local bulk snapshot fixture or source file."""

    filename: str
    content_hash: str
    card_count: int
    source_uri: str | None = None


@dataclass(frozen=True)
class ScryfallBulkSnapshotManifest:
    """Deterministic manifest for a local Scryfall bulk snapshot."""

    snapshot_id: str
    snapshot_version: str
    bulk_type: str
    source_uri: str | None
    generated_at: str | None
    imported_at: str | None
    content_hash: str
    card_count: int
    schema_version: str
    file_refs: tuple[ScryfallBulkFileRef, ...]
    raw_metadata: Mapping[str, Any]


@dataclass(frozen=True)
class ScryfallBulkSnapshotValidationReport:
    """Validation report for a local Scryfall bulk snapshot."""

    manifest: ScryfallBulkSnapshotManifest
    is_valid: bool
    validation_errors: tuple[str, ...]
    validation_warnings: tuple[str, ...]
    raw_cards: tuple[Mapping[str, Any], ...]


def build_scryfall_bulk_snapshot_manifest(
    *,
    snapshot_id: str,
    bulk_type: str,
    source_uri: str | None = None,
    generated_at: str | None = None,
    imported_at: str | None = None,
    content_hash: str | None = None,
    card_count: int | None = None,
    schema_version: str = SCRYFALL_BULK_SNAPSHOT_VERSION,
    file_refs: tuple[ScryfallBulkFileRef, ...] | list[ScryfallBulkFileRef] = (),
    raw_metadata: Mapping[str, Any] | None = None,
    cards: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
) -> ScryfallBulkSnapshotManifest:
    """Build a deterministic local Scryfall bulk snapshot manifest."""

    _require_text(snapshot_id, "snapshot_id")
    _require_text(bulk_type, "bulk_type")
    _require_text(schema_version, "schema_version")
    if card_count is not None and card_count < 0:
        raise ScryfallBulkSnapshotError("card_count must not be negative")

    frozen_cards = _freeze_cards(cards or ())
    resolved_hash = content_hash if content_hash is not None else _hash_json(_thaw_json(frozen_cards))
    resolved_count = card_count if card_count is not None else len(frozen_cards)
    if not isinstance(resolved_hash, str) or not resolved_hash.strip():
        raise ScryfallBulkSnapshotError("content_hash is required")

    frozen_file_refs = tuple(file_refs)
    for file_ref in frozen_file_refs:
        if not isinstance(file_ref, ScryfallBulkFileRef):
            raise ScryfallBulkSnapshotError("file_refs must contain ScryfallBulkFileRef values")

    return ScryfallBulkSnapshotManifest(
        snapshot_id=snapshot_id,
        snapshot_version=SCRYFALL_BULK_SNAPSHOT_VERSION,
        bulk_type=bulk_type,
        source_uri=source_uri,
        generated_at=generated_at,
        imported_at=imported_at,
        content_hash=resolved_hash,
        card_count=resolved_count,
        schema_version=schema_version,
        file_refs=frozen_file_refs,
        raw_metadata=_freeze_json(dict(raw_metadata or {})),
    )


def validate_scryfall_bulk_snapshot_manifest(
    manifest: ScryfallBulkSnapshotManifest,
    cards: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
) -> ScryfallBulkSnapshotValidationReport:
    """Validate a manifest and optional local card payloads."""

    if not isinstance(manifest, ScryfallBulkSnapshotManifest):
        raise ScryfallBulkSnapshotError("manifest must be a ScryfallBulkSnapshotManifest")

    frozen_cards = _freeze_cards(cards or ())
    errors: list[str] = []
    warnings: list[str] = []

    if cards is not None:
        for index, card in enumerate(frozen_cards):
            if not _card_scryfall_id(card):
                errors.append(f"card[{index}] missing required Scryfall id")
            if not _card_name(card):
                errors.append(f"card[{index}] missing required name")
        calculated_hash = _hash_json(_thaw_json(frozen_cards))
        if calculated_hash != manifest.content_hash:
            errors.append("manifest content_hash does not match card payload")
        if len(frozen_cards) != manifest.card_count:
            errors.append("manifest card_count does not match card payload")

    if manifest.file_refs:
        total_ref_cards = sum(file_ref.card_count for file_ref in manifest.file_refs)
        if total_ref_cards != manifest.card_count:
            warnings.append("file_refs card_count total differs from manifest card_count")

    return ScryfallBulkSnapshotValidationReport(
        manifest=manifest,
        is_valid=not errors,
        validation_errors=tuple(errors),
        validation_warnings=tuple(warnings),
        raw_cards=frozen_cards,
    )


def scryfall_bulk_snapshot_manifest_to_dict(
    manifest: ScryfallBulkSnapshotManifest,
) -> dict[str, Any]:
    """Serialize a manifest to a deterministic JSON-compatible dictionary."""

    if not isinstance(manifest, ScryfallBulkSnapshotManifest):
        raise ScryfallBulkSnapshotError("manifest must be a ScryfallBulkSnapshotManifest")
    return {
        "bulk_type": manifest.bulk_type,
        "card_count": manifest.card_count,
        "content_hash": manifest.content_hash,
        "file_refs": [
            {
                "card_count": file_ref.card_count,
                "content_hash": file_ref.content_hash,
                "filename": file_ref.filename,
                "source_uri": file_ref.source_uri,
            }
            for file_ref in manifest.file_refs
        ],
        "generated_at": manifest.generated_at,
        "imported_at": manifest.imported_at,
        "raw_metadata": _thaw_json(manifest.raw_metadata),
        "schema_version": manifest.schema_version,
        "snapshot_id": manifest.snapshot_id,
        "snapshot_version": manifest.snapshot_version,
        "source_uri": manifest.source_uri,
    }


def load_scryfall_bulk_snapshot_fixture(
    fixture_path: str | Path,
    *,
    snapshot_id: str | None = None,
    bulk_type: str | None = None,
    source_uri: str | None = None,
    generated_at: str | None = None,
    imported_at: str | None = None,
    raw_metadata: Mapping[str, Any] | None = None,
) -> ScryfallBulkSnapshotValidationReport:
    """Load and validate a local Scryfall bulk snapshot fixture."""

    path = Path(fixture_path)
    try:
        text = path.read_text(encoding="utf-8")
        payload = json.loads(text)
    except OSError as exc:
        raise ScryfallBulkSnapshotError(f"unable to read local fixture: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ScryfallBulkSnapshotError(f"malformed Scryfall bulk fixture: {path}") from exc

    cards, metadata = _extract_cards_and_metadata(payload)
    merged_metadata = dict(metadata)
    merged_metadata.update(dict(raw_metadata or {}))
    resolved_source_uri = source_uri or _optional_text(metadata.get("source_uri"))
    resolved_generated_at = generated_at or _optional_text(metadata.get("generated_at"))
    resolved_bulk_type = bulk_type or _optional_text(metadata.get("bulk_type")) or "default_cards"

    frozen_cards = _freeze_cards(cards)
    content_hash = _hash_json(_thaw_json(frozen_cards))
    file_ref = ScryfallBulkFileRef(
        filename=path.name,
        content_hash=content_hash,
        card_count=len(frozen_cards),
        source_uri=resolved_source_uri,
    )
    manifest = build_scryfall_bulk_snapshot_manifest(
        snapshot_id=snapshot_id or path.stem,
        bulk_type=resolved_bulk_type,
        source_uri=resolved_source_uri,
        generated_at=resolved_generated_at,
        imported_at=imported_at,
        content_hash=content_hash,
        card_count=len(frozen_cards),
        file_refs=(file_ref,),
        raw_metadata=merged_metadata,
    )
    return validate_scryfall_bulk_snapshot_manifest(manifest, frozen_cards)


def _extract_cards_and_metadata(payload: Any) -> tuple[list[Mapping[str, Any]], Mapping[str, Any]]:
    if isinstance(payload, list):
        return payload, {}
    if isinstance(payload, dict):
        cards = payload.get("cards")
        if not isinstance(cards, list):
            raise ScryfallBulkSnapshotError("Scryfall bulk fixture object requires a cards list")
        metadata = {key: value for key, value in payload.items() if key != "cards"}
        return cards, metadata
    raise ScryfallBulkSnapshotError("Scryfall bulk fixture must be a list or object")


def _card_scryfall_id(card: Mapping[str, Any]) -> str | None:
    value = card.get("id") or card.get("scryfall_id")
    return value if isinstance(value, str) and value.strip() else None


def _card_name(card: Mapping[str, Any]) -> str | None:
    value = card.get("name")
    return value if isinstance(value, str) and value.strip() else None


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ScryfallBulkSnapshotError(f"{field_name} is required")


def _optional_text(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _freeze_cards(cards: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(cards, (list, tuple)):
        raise ScryfallBulkSnapshotError("cards must be a list or tuple")
    frozen = []
    for index, card in enumerate(cards):
        if not isinstance(card, Mapping):
            raise ScryfallBulkSnapshotError(f"card[{index}] must be an object")
        frozen.append(_freeze_json(dict(card)))
    return tuple(frozen)


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(value[key]) for key in sorted(value)})
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_json(item) for item in value)
    return value


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _hash_json(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()
