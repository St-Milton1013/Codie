"""Pure unsupported relevant card queues for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.evidence_inputs import (
    EvidenceInputBuildError,
    EvidenceInputRecord,
    EvidenceRecordRef,
)


ALLOWED_REASONS = frozenset(
    {
        "simulator_unsupported",
        "card_lookup_unresolved",
        "model_gap",
        "rules_text_gap",
        "source_conflict",
        "privacy_redaction",
        "manual_review_required",
    }
)

ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})
SEVERITY_RANK = {"info": 0, "warning": 1, "blocking": 2}

ALLOWED_STATUSES = frozenset({"open", "in_review", "resolved", "ignored_by_policy"})

ALLOWED_PRIVACY_SCOPES = frozenset({"public", "local", "local_user_data", "sensitive"})
PRIVACY_RANK = {"public": 0, "local": 1, "local_user_data": 2, "sensitive": 3}

ALLOWED_DEDUPLICATION_MODES = frozenset({"none", "card_identity"})

FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "raw_input",
        "private_deck_text",
        "full_primer_body",
        "raw_" + "provider_payload",
        "provider_payload",
        "original_import_text",
    }
)


class UnsupportedCardQueueBuildError(ValueError):
    """Raised when an unsupported card queue cannot be built safely."""


@dataclass(frozen=True)
class UnsupportedCardEvidenceRef:
    evidence_id: str
    source_type: str
    source_name: str
    observed_at: str
    card_name: str
    source_record_id: str | None = None
    source_url: str | None = None
    oracle_id: str | None = None
    scryfall_id: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    privacy_scope: str = "public"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.evidence_id, "evidence_id")
        _require_text(self.source_type, "source_type")
        _require_text(self.source_name, "source_name")
        _require_text(self.observed_at, "observed_at")
        _require_text(self.card_name, "card_name")
        if self.source_record_id in (None, "") and self.source_url in (None, ""):
            raise UnsupportedCardQueueBuildError("source_record_id or source_url is required")
        if self.oracle_id is not None:
            _require_text(self.oracle_id, "oracle_id")
        if self.scryfall_id is not None:
            _require_text(self.scryfall_id, "scryfall_id")
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        object.__setattr__(self, "context", _validate_metadata(self.context))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _wrap_input_error(
            lambda: EvidenceRecordRef(
                source_type=self.source_type,
                source_name=self.source_name,
                source_record_id=self.source_record_id,
                source_url=self.source_url,
                observed_at=self.observed_at,
            )
        )


@dataclass(frozen=True)
class UnsupportedCardQueueItem:
    item_id: str
    card_name: str
    reason: str
    severity: str
    evidence_refs: tuple[UnsupportedCardEvidenceRef, ...]
    status: str = "open"
    oracle_id: str | None = None
    scryfall_id: str | None = None
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    caveats: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.item_id, "item_id")
        _require_text(self.card_name, "card_name")
        object.__setattr__(self, "reason", _normalize_allowed(self.reason, ALLOWED_REASONS, "reason"))
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(self, "status", _normalize_allowed(self.status, ALLOWED_STATUSES, "status"))
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))
        if not self.evidence_refs:
            raise UnsupportedCardQueueBuildError("item requires at least one evidence_ref")
        if self.oracle_id is not None:
            _require_text(self.oracle_id, "oracle_id")
        if self.scryfall_id is not None:
            _require_text(self.scryfall_id, "scryfall_id")
        if self.first_seen_at is not None:
            _require_text(self.first_seen_at, "first_seen_at")
        if self.last_seen_at is not None:
            _require_text(self.last_seen_at, "last_seen_at")
        object.__setattr__(self, "caveats", tuple(_validate_metadata(dict(caveat)) for caveat in self.caveats))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _wrap_input_error(
            lambda: EvidenceInputRecord(
                record_id=f"unsupported-card-validation:{self.item_id}",
                record_type="unsupported_card",
                label="Unsupported card validation",
                summary=f"{self.card_name} has an unresolved support gap.",
                confidence=1.0,
                references=(
                    EvidenceRecordRef(
                        source_type=self.evidence_refs[0].source_type,
                        source_name=self.evidence_refs[0].source_name,
                        source_record_id=self.evidence_refs[0].source_record_id,
                        source_url=self.evidence_refs[0].source_url,
                        observed_at=self.evidence_refs[0].observed_at,
                    ),
                ),
            )
        )


@dataclass(frozen=True)
class UnsupportedCardQueue:
    queue_id: str
    subject_type: str
    subject_id: str
    generated_at: str
    items: tuple[UnsupportedCardQueueItem, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.queue_id, "queue_id")
        _require_text(self.subject_type, "subject_type")
        _require_text(self.subject_id, "subject_id")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "items", tuple(sorted(self.items, key=lambda item: item.item_id)))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        build_unsupported_card_queue(self)


@dataclass(frozen=True)
class UnsupportedCardQueueOptions:
    include_resolved: bool = False
    include_sensitive: bool = False
    minimum_severity: str = "info"
    deduplicate_by: str = "card_identity"

    def __post_init__(self) -> None:
        object.__setattr__(self, "minimum_severity", _normalize_allowed(self.minimum_severity, ALLOWED_SEVERITIES, "minimum_severity"))
        object.__setattr__(self, "deduplicate_by", _normalize_allowed(self.deduplicate_by, ALLOWED_DEDUPLICATION_MODES, "deduplicate_by"))


def build_unsupported_card_queue(queue: UnsupportedCardQueue) -> UnsupportedCardQueue:
    """Validate one unsupported relevant card queue."""

    if not queue.items:
        raise UnsupportedCardQueueBuildError("UnsupportedCardQueue requires at least one item")
    item_ids = [item.item_id for item in queue.items]
    duplicates = _duplicates(item_ids)
    if duplicates:
        raise UnsupportedCardQueueBuildError(f"duplicate item_id: {duplicates[0]}")
    return queue


def unsupported_card_queue_to_input_records(
    queue: UnsupportedCardQueue,
    options: UnsupportedCardQueueOptions | None = None,
) -> tuple[EvidenceInputRecord, ...]:
    """Convert an unsupported-card queue into unsupported_card input records."""

    resolved_options = options or UnsupportedCardQueueOptions()
    records: list[EvidenceInputRecord] = []
    filtered_item_ids: list[str] = []
    deduplicated_item_ids: list[str] = []
    seen_identity_keys: set[str] = set()
    for item in queue.items:
        if _item_filtered(item, resolved_options):
            filtered_item_ids.append(item.item_id)
            continue
        identity_key = _identity_key(item)
        if resolved_options.deduplicate_by == "card_identity" and identity_key in seen_identity_keys:
            deduplicated_item_ids.append(item.item_id)
            continue
        seen_identity_keys.add(identity_key)
        included_refs, filtered_refs = _filter_refs(item.evidence_refs, resolved_options)
        if not included_refs:
            filtered_item_ids.append(item.item_id)
            continue
        records.append(_record_from_item(item, included_refs, filtered_refs))

    if not records:
        raise UnsupportedCardQueueBuildError("filtered queue has no remaining items")
    if filtered_item_ids or deduplicated_item_ids:
        records = records + [_filtered_items_record(queue, filtered_item_ids, deduplicated_item_ids)]
    return tuple(records)


def unsupported_card_queue_to_dict(queue: UnsupportedCardQueue) -> dict[str, Any]:
    """Serialize one unsupported relevant card queue deterministically."""

    validated = build_unsupported_card_queue(queue)
    return {
        "queue_id": validated.queue_id,
        "subject_type": validated.subject_type,
        "subject_id": validated.subject_id,
        "generated_at": validated.generated_at,
        "items": [_item_to_dict(item) for item in validated.items],
        "metadata": _sorted_json_object(validated.metadata),
    }


def _item_filtered(item: UnsupportedCardQueueItem, options: UnsupportedCardQueueOptions) -> bool:
    if item.status in {"resolved", "ignored_by_policy"} and not options.include_resolved:
        return True
    return SEVERITY_RANK[item.severity] < SEVERITY_RANK[options.minimum_severity]


def _filter_refs(
    refs: tuple[UnsupportedCardEvidenceRef, ...],
    options: UnsupportedCardQueueOptions,
) -> tuple[tuple[UnsupportedCardEvidenceRef, ...], tuple[UnsupportedCardEvidenceRef, ...]]:
    kept: list[UnsupportedCardEvidenceRef] = []
    filtered: list[UnsupportedCardEvidenceRef] = []
    for ref in refs:
        if ref.privacy_scope == "sensitive" and not options.include_sensitive:
            filtered.append(ref)
        else:
            kept.append(ref)
    return tuple(kept), tuple(filtered)


def _record_from_item(
    item: UnsupportedCardQueueItem,
    refs: tuple[UnsupportedCardEvidenceRef, ...],
    filtered_refs: tuple[UnsupportedCardEvidenceRef, ...],
) -> EvidenceInputRecord:
    caveats = tuple(item.caveats)
    if filtered_refs:
        caveats = caveats + (
            {
                "caveat_type": "privacy_redaction",
                "message": "Some unsupported-card evidence was filtered by assembly options.",
                "severity": "info",
                "metadata": {
                    "filtered_evidence_ids": [ref.evidence_id for ref in filtered_refs],
                    "filtered_count": len(filtered_refs),
                },
            },
        )
    metadata = {
        "card_name": item.card_name,
        "oracle_id": item.oracle_id,
        "scryfall_id": item.scryfall_id,
        "reason": item.reason,
        "severity": item.severity,
        "status": item.status,
        "first_seen_at": item.first_seen_at,
        "last_seen_at": item.last_seen_at,
        "contexts": [ref.context for ref in refs],
        **item.metadata,
    }
    return _wrap_input_error(
        lambda: EvidenceInputRecord(
            record_id=f"unsupported-card:{item.item_id}",
            record_type="unsupported_card",
            label=f"Unsupported card: {item.card_name}",
            summary=_summary_for_item(item),
            confidence=_confidence_for_severity(item.severity),
            references=tuple(_input_ref_from_card_ref(ref) for ref in refs),
            caveats=caveats,
            privacy_scope=_highest_privacy_scope(refs),
            metadata=metadata,
        )
    )


def _filtered_items_record(
    queue: UnsupportedCardQueue,
    filtered_item_ids: list[str],
    deduplicated_item_ids: list[str],
) -> EvidenceInputRecord:
    metadata = {
        "filtered_item_ids": list(filtered_item_ids),
        "filtered_count": len(filtered_item_ids),
        "deduplicated_item_ids": list(deduplicated_item_ids),
        "deduplicated_count": len(deduplicated_item_ids),
    }
    return _wrap_input_error(
        lambda: EvidenceInputRecord(
            record_id=f"unsupported-card-filtered:{queue.queue_id}",
            record_type="unsupported_card",
            label="Filtered unsupported-card queue items",
            summary="Some unsupported-card queue items were filtered by report options.",
            confidence=1.0,
            references=(
                EvidenceRecordRef(
                    source_type="manual",
                    source_name="Codie unsupported card queue",
                    source_record_id=queue.queue_id,
                    source_url=None,
                    observed_at=queue.generated_at,
                ),
            ),
            caveats=(
                {
                    "caveat_type": "missing_data",
                    "message": "Some unsupported-card queue items were filtered by report options.",
                    "severity": "info",
                    "metadata": metadata,
                },
            ),
            privacy_scope="local",
            metadata=metadata,
        )
    )


def _input_ref_from_card_ref(ref: UnsupportedCardEvidenceRef) -> EvidenceRecordRef:
    return _wrap_input_error(
        lambda: EvidenceRecordRef(
            source_type=ref.source_type,
            source_name=ref.source_name,
            source_record_id=ref.source_record_id,
            source_url=ref.source_url,
            observed_at=ref.observed_at,
        )
    )


def _item_to_dict(item: UnsupportedCardQueueItem) -> dict[str, Any]:
    return {
        "item_id": item.item_id,
        "card_name": item.card_name,
        "oracle_id": item.oracle_id,
        "scryfall_id": item.scryfall_id,
        "reason": item.reason,
        "severity": item.severity,
        "status": item.status,
        "first_seen_at": item.first_seen_at,
        "last_seen_at": item.last_seen_at,
        "evidence_refs": [_ref_to_dict(ref) for ref in sorted(item.evidence_refs, key=lambda ref: ref.evidence_id)],
        "caveats": [_sorted_json_object(caveat) for caveat in item.caveats],
        "metadata": _sorted_json_object(item.metadata),
    }


def _ref_to_dict(ref: UnsupportedCardEvidenceRef) -> dict[str, Any]:
    return {
        "evidence_id": ref.evidence_id,
        "source_type": ref.source_type,
        "source_name": ref.source_name,
        "source_record_id": ref.source_record_id,
        "source_url": ref.source_url,
        "observed_at": ref.observed_at,
        "card_name": ref.card_name,
        "oracle_id": ref.oracle_id,
        "scryfall_id": ref.scryfall_id,
        "context": _sorted_json_object(ref.context),
        "privacy_scope": ref.privacy_scope,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _summary_for_item(item: UnsupportedCardQueueItem) -> str:
    return f"{item.card_name} is tracked because Codie has a {item.reason.replace('_', ' ')} gap."


def _confidence_for_severity(severity: str) -> float:
    if severity == "blocking":
        return 1.0
    if severity == "warning":
        return 0.75
    return 0.5


def _highest_privacy_scope(refs: tuple[UnsupportedCardEvidenceRef, ...]) -> str:
    return max((ref.privacy_scope for ref in refs), key=lambda scope: PRIVACY_RANK[scope])


def _identity_key(item: UnsupportedCardQueueItem) -> str:
    if item.scryfall_id:
        return f"scryfall:{item.scryfall_id.strip().lower()}"
    if item.oracle_id:
        return f"oracle:{item.oracle_id.strip().lower()}"
    return f"name:{item.card_name.strip().lower()}"


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise UnsupportedCardQueueBuildError(f"{field_name} is required")


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    _require_text(value, field_name)
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise UnsupportedCardQueueBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise UnsupportedCardQueueBuildError("metadata must be an object")
    _reject_forbidden_metadata(metadata)
    return _validate_json_value(metadata, "metadata")


def _validate_json_value(value: Any, field_name: str) -> Any:
    _reject_forbidden_metadata(value)
    try:
        encoded = json.dumps(value, sort_keys=True)
        decoded = json.loads(encoded)
    except (TypeError, ValueError) as exc:
        raise UnsupportedCardQueueBuildError(f"{field_name} must be JSON-compatible") from exc
    return decoded


def _reject_forbidden_metadata(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise UnsupportedCardQueueBuildError(f"metadata contains forbidden private field: {key}")
            _reject_forbidden_metadata(nested)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_metadata(item)


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))


def _wrap_input_error(callback):
    try:
        return callback()
    except EvidenceInputBuildError as exc:
        raise UnsupportedCardQueueBuildError(str(exc)) from exc


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates
