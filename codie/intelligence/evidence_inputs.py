"""Pure input assembly for interactive intelligence evidence graphs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.evidence_graph import (
    EvidenceCaveat,
    EvidenceCitation,
    EvidenceGraphBuildError,
    EvidenceGraphInput,
    EvidenceNode,
)


ALLOWED_RECORD_TYPES = frozenset(
    {
        "recommendation_candidate",
        "innovation_signal",
        "combo_evidence",
        "primer_metadata",
        "simulation_review_summary",
        "deck_memory_summary",
        "saved_analysis_summary",
        "manual_note",
        "source_conflict",
        "unsupported_card",
    }
)

RECORD_TYPE_TO_NODE_TYPE = {
    "recommendation_candidate": "card",
    "innovation_signal": "innovation_signal",
    "combo_evidence": "combo_evidence",
    "primer_metadata": "primer_metadata",
    "simulation_review_summary": "simulation_result",
    "deck_memory_summary": "user_deck_memory",
    "saved_analysis_summary": "saved_analysis",
    "manual_note": "manual_note",
    "source_conflict": "source_conflict",
    "unsupported_card": "unsupported_card",
}

FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "raw_input",
        "private_deck_text",
        "full_primer_body",
        "raw_provider_payload",
        "provider_payload",
        "original_import_text",
    }
)

ALLOWED_PRIVACY_SCOPES = frozenset({"public", "local", "local_user_data", "sensitive"})


class EvidenceInputBuildError(ValueError):
    """Raised when sanitized evidence input records cannot be assembled."""


@dataclass(frozen=True)
class EvidenceRecordRef:
    source_type: str
    source_name: str
    observed_at: str
    source_record_id: str | None = None
    source_url: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.source_type, "source_type")
        _require_text(self.source_name, "source_name")
        _require_text(self.observed_at, "observed_at")
        if self.source_record_id in (None, "") and self.source_url in (None, ""):
            raise EvidenceInputBuildError("source_record_id or source_url is required")
        _validate_metadata(
            {
                "source_type": self.source_type,
                "source_name": self.source_name,
                "source_record_id": self.source_record_id,
                "source_url": self.source_url,
                "observed_at": self.observed_at,
            }
        )
        _wrap_graph_error(
            lambda: EvidenceCitation(
                citation_id="citation:validation",
                source_type=self.source_type,
                source_name=self.source_name,
                source_record_id=self.source_record_id,
                source_url=self.source_url,
                observed_at=self.observed_at,
            )
        )


@dataclass(frozen=True)
class EvidenceInputRecord:
    record_id: str
    record_type: str
    label: str
    summary: str
    confidence: float
    references: tuple[EvidenceRecordRef, ...] = ()
    caveats: tuple[dict[str, Any], ...] = ()
    privacy_scope: str = "public"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.record_id, "record_id")
        object.__setattr__(self, "record_type", _normalize_record_type(self.record_type))
        _require_text(self.label, "label")
        _require_text(self.summary, "summary")
        _validate_confidence(self.confidence, "confidence")
        object.__setattr__(self, "privacy_scope", _normalize_privacy_scope(self.privacy_scope))
        object.__setattr__(self, "references", tuple(self.references))
        object.__setattr__(self, "caveats", tuple(_validate_metadata(dict(caveat)) for caveat in self.caveats))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        if self.record_type != "manual_note" and not self.references:
            raise EvidenceInputBuildError("non-manual records require at least one reference")
        _wrap_graph_error(
            lambda: EvidenceNode(
                node_id=f"node:{self.record_id}",
                node_type=RECORD_TYPE_TO_NODE_TYPE[self.record_type],
                label=self.label,
                summary=self.summary,
                confidence=self.confidence,
                citations=tuple(_citation_from_ref(self.record_id, ref, index) for index, ref in enumerate(self.references)),
                privacy_scope=self.privacy_scope,
                metadata=self.metadata,
            )
        )


@dataclass(frozen=True)
class EvidenceInputBundle:
    bundle_id: str
    claim_type: str
    claim_text: str
    subject_type: str
    subject_id: str
    generated_at: str
    records: tuple[EvidenceInputRecord, ...]
    bundle_caveats: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.bundle_id, "bundle_id")
        _require_text(self.claim_type, "claim_type")
        _require_text(self.claim_text, "claim_text")
        _require_text(self.subject_type, "subject_type")
        _require_text(self.subject_id, "subject_id")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "records", tuple(self.records))
        object.__setattr__(
            self,
            "bundle_caveats",
            tuple(_validate_metadata(dict(caveat)) for caveat in self.bundle_caveats),
        )
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_evidence_input_bundle(self)


@dataclass(frozen=True)
class EvidenceGraphAssemblyOptions:
    graph_id: str | None = None
    include_manual_notes: bool = True
    include_local_user_data: bool = True
    include_sensitive: bool = False
    minimum_confidence: float = 0.0

    def __post_init__(self) -> None:
        if self.graph_id is not None:
            _require_text(self.graph_id, "graph_id")
        _validate_confidence(self.minimum_confidence, "minimum_confidence")


def evidence_record_from_dict(payload: dict[str, Any]) -> EvidenceInputRecord:
    """Build one sanitized input record from JSON-compatible data."""

    if not isinstance(payload, dict):
        raise EvidenceInputBuildError("record payload must be an object")
    references = tuple(EvidenceRecordRef(**ref) for ref in payload.get("references", ()))
    data = dict(payload)
    data["references"] = references
    data["caveats"] = tuple(data.get("caveats", ()))
    return EvidenceInputRecord(**data)


def validate_evidence_input_bundle(bundle: EvidenceInputBundle) -> EvidenceInputBundle:
    """Validate one sanitized input bundle."""

    if not bundle.records:
        raise EvidenceInputBuildError("EvidenceInputBundle requires at least one record")
    record_ids = [record.record_id for record in bundle.records]
    duplicates = _duplicates(record_ids)
    if duplicates:
        raise EvidenceInputBuildError(f"duplicate record_id: {duplicates[0]}")
    return bundle


def build_graph_input_from_records(
    bundle: EvidenceInputBundle,
    options: EvidenceGraphAssemblyOptions | None = None,
) -> EvidenceGraphInput:
    """Assemble sanitized records into an EvidenceGraphInput."""

    assembly_options = options or EvidenceGraphAssemblyOptions()
    kept_records, filtered_records = _filter_records(bundle.records, assembly_options)
    if not kept_records:
        raise EvidenceInputBuildError("filtered bundle has no remaining records")

    nodes = tuple(_node_from_record(record) for record in kept_records)
    caveats = tuple(
        _caveat_from_dict(caveat, None, index, "bundle")
        for index, caveat in enumerate(bundle.bundle_caveats)
    )
    caveats = caveats + tuple(
        _caveat_from_dict(caveat, (f"node:{record.record_id}",), index, f"record:{record.record_id}")
        for record in kept_records
        for index, caveat in enumerate(record.caveats)
    )
    if filtered_records:
        caveats = caveats + (_filtered_records_caveat(filtered_records, nodes),)

    return EvidenceGraphInput(
        graph_id=assembly_options.graph_id or bundle.bundle_id,
        claim_type=bundle.claim_type,
        claim_text=bundle.claim_text,
        subject_type=bundle.subject_type,
        subject_id=bundle.subject_id,
        generated_at=bundle.generated_at,
        nodes=nodes,
        edges=(),
        caveats=caveats,
        metadata=bundle.metadata,
    )


def _filter_records(
    records: tuple[EvidenceInputRecord, ...],
    options: EvidenceGraphAssemblyOptions,
) -> tuple[tuple[EvidenceInputRecord, ...], tuple[EvidenceInputRecord, ...]]:
    kept: list[EvidenceInputRecord] = []
    filtered: list[EvidenceInputRecord] = []
    for record in records:
        should_filter = False
        if record.record_type == "manual_note" and not options.include_manual_notes:
            should_filter = True
        if record.privacy_scope == "local_user_data" and not options.include_local_user_data:
            should_filter = True
        if record.privacy_scope == "sensitive" and not options.include_sensitive:
            should_filter = True
        if record.confidence < options.minimum_confidence:
            should_filter = True
        if should_filter:
            filtered.append(record)
        else:
            kept.append(record)
    return tuple(kept), tuple(filtered)


def _node_from_record(record: EvidenceInputRecord) -> EvidenceNode:
    return _wrap_graph_error(
        lambda: EvidenceNode(
            node_id=f"node:{record.record_id}",
            node_type=RECORD_TYPE_TO_NODE_TYPE[record.record_type],
            label=record.label,
            summary=record.summary,
            confidence=record.confidence,
            citations=tuple(_citation_from_ref(record.record_id, ref, index) for index, ref in enumerate(record.references)),
            privacy_scope=record.privacy_scope,
            metadata={"record_type": record.record_type, **record.metadata},
        )
    )


def _citation_from_ref(record_id: str, ref: EvidenceRecordRef, index: int) -> EvidenceCitation:
    return _wrap_graph_error(
        lambda: EvidenceCitation(
            citation_id=f"citation:{record_id}:{index + 1}",
            source_type=ref.source_type,
            source_name=ref.source_name,
            source_record_id=ref.source_record_id,
            source_url=ref.source_url,
            observed_at=ref.observed_at,
        )
    )


def _caveat_from_dict(
    caveat: dict[str, Any],
    related_node_ids: tuple[str, ...] | None,
    index: int,
    prefix: str,
) -> EvidenceCaveat:
    data = {
        "caveat_id": f"caveat:{prefix}:{index + 1}",
        "caveat_type": "missing_data",
        "message": "Some supplied evidence has caveats.",
        "severity": "warning",
        "related_node_ids": related_node_ids or (),
        "metadata": {},
    }
    data.update(caveat)
    return _wrap_graph_error(lambda: EvidenceCaveat(**data))


def _filtered_records_caveat(
    filtered_records: tuple[EvidenceInputRecord, ...],
    kept_nodes: tuple[EvidenceNode, ...],
) -> EvidenceCaveat:
    return _wrap_graph_error(
        lambda: EvidenceCaveat(
            caveat_id="caveat:filtered-records",
            caveat_type="privacy_redaction",
            message="Some supplied evidence records were filtered by assembly options.",
            severity="info",
            related_node_ids=tuple(node.node_id for node in kept_nodes),
            metadata={
                "filtered_record_ids": [record.record_id for record in filtered_records],
                "filtered_count": len(filtered_records),
            },
        )
    )


def _normalize_record_type(value: str) -> str:
    _require_text(value, "record_type")
    normalized = value.strip().lower()
    if normalized not in ALLOWED_RECORD_TYPES:
        raise EvidenceInputBuildError(f"unsupported record_type: {value}")
    return normalized


def _normalize_privacy_scope(value: str) -> str:
    _require_text(value, "privacy_scope")
    normalized = value.strip().lower()
    if normalized not in ALLOWED_PRIVACY_SCOPES:
        raise EvidenceInputBuildError(f"unsupported privacy_scope: {value}")
    return normalized


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceInputBuildError(f"{field_name} is required")


def _validate_confidence(value: float, field_name: str) -> None:
    if not isinstance(value, int | float):
        raise EvidenceInputBuildError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise EvidenceInputBuildError(f"{field_name} must be between 0 and 1")


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise EvidenceInputBuildError("metadata must be an object")
    _reject_forbidden_metadata(metadata)
    try:
        encoded = json.dumps(metadata, sort_keys=True)
        decoded = json.loads(encoded)
    except (TypeError, ValueError) as exc:
        raise EvidenceInputBuildError("metadata must be JSON-compatible") from exc
    if not isinstance(decoded, dict):
        raise EvidenceInputBuildError("metadata must be an object")
    return decoded


def _reject_forbidden_metadata(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise EvidenceInputBuildError(f"metadata contains forbidden private field: {key}")
            _reject_forbidden_metadata(nested)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_metadata(item)


def _wrap_graph_error(callback):
    try:
        return callback()
    except EvidenceGraphBuildError as exc:
        raise EvidenceInputBuildError(str(exc)) from exc


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates
