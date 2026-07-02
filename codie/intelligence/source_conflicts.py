"""Pure source conflict reports for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.evidence_inputs import (
    EvidenceInputBuildError,
    EvidenceInputRecord,
    EvidenceRecordRef,
)


ALLOWED_CONFLICT_TYPES = frozenset(
    {
        "identity_mismatch",
        "metadata_mismatch",
        "source_disagreement",
        "missing_evidence",
        "privacy_redaction",
        "unsupported_behavior",
        "stale_data",
        "manual_review_required",
    }
)

ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})
SEVERITY_RANK = {"info": 0, "warning": 1, "blocking": 2}

ALLOWED_RESOLUTION_STATUSES = frozenset(
    {
        "unresolved",
        "needs_review",
        "resolved_externally",
        "ignored_by_policy",
    }
)

ALLOWED_PRIVACY_SCOPES = frozenset({"public", "local", "local_user_data", "sensitive"})
PRIVACY_RANK = {"public": 0, "local": 1, "local_user_data": 2, "sensitive": 3}

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


class SourceConflictBuildError(ValueError):
    """Raised when a source conflict report cannot be built safely."""


@dataclass(frozen=True)
class SourceConflictEvidenceRef:
    evidence_id: str
    source_type: str
    source_name: str
    observed_at: str
    field_name: str
    field_value: Any
    source_record_id: str | None = None
    source_url: str | None = None
    privacy_scope: str = "public"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.evidence_id, "evidence_id")
        _require_text(self.source_type, "source_type")
        _require_text(self.source_name, "source_name")
        _require_text(self.observed_at, "observed_at")
        _require_text(self.field_name, "field_name")
        if self.source_record_id in (None, "") and self.source_url in (None, ""):
            raise SourceConflictBuildError("source_record_id or source_url is required")
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        object.__setattr__(self, "field_value", _validate_json_value(self.field_value, "field_value"))
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
class SourceConflictItem:
    conflict_id: str
    conflict_type: str
    summary: str
    severity: str
    evidence_refs: tuple[SourceConflictEvidenceRef, ...]
    resolution_status: str = "unresolved"
    caveats: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.conflict_id, "conflict_id")
        object.__setattr__(self, "conflict_type", _normalize_allowed(self.conflict_type, ALLOWED_CONFLICT_TYPES, "conflict_type"))
        _require_text(self.summary, "summary")
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(
            self,
            "resolution_status",
            _normalize_allowed(self.resolution_status, ALLOWED_RESOLUTION_STATUSES, "resolution_status"),
        )
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))
        if not self.evidence_refs:
            raise SourceConflictBuildError("conflict requires at least one evidence_ref")
        object.__setattr__(self, "caveats", tuple(_validate_metadata(dict(caveat)) for caveat in self.caveats))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _wrap_input_error(
            lambda: EvidenceInputRecord(
                record_id=f"conflict-validation:{self.conflict_id}",
                record_type="source_conflict",
                label="Source conflict validation",
                summary=self.summary,
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
class SourceConflictReport:
    report_id: str
    subject_type: str
    subject_id: str
    generated_at: str
    conflicts: tuple[SourceConflictItem, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.report_id, "report_id")
        _require_text(self.subject_type, "subject_type")
        _require_text(self.subject_id, "subject_id")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "conflicts", tuple(sorted(self.conflicts, key=lambda item: item.conflict_id)))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        build_source_conflict_report(self)


@dataclass(frozen=True)
class SourceConflictReportOptions:
    include_info: bool = True
    include_resolved: bool = False
    include_sensitive: bool = False
    minimum_severity: str = "info"

    def __post_init__(self) -> None:
        object.__setattr__(self, "minimum_severity", _normalize_allowed(self.minimum_severity, ALLOWED_SEVERITIES, "minimum_severity"))


def build_source_conflict_report(report: SourceConflictReport) -> SourceConflictReport:
    """Validate one source conflict report."""

    if not report.conflicts:
        raise SourceConflictBuildError("SourceConflictReport requires at least one conflict")
    conflict_ids = [conflict.conflict_id for conflict in report.conflicts]
    duplicates = _duplicates(conflict_ids)
    if duplicates:
        raise SourceConflictBuildError(f"duplicate conflict_id: {duplicates[0]}")
    return report


def source_conflict_report_to_input_records(
    report: SourceConflictReport,
    options: SourceConflictReportOptions | None = None,
) -> tuple[EvidenceInputRecord, ...]:
    """Convert a conflict report into source_conflict input records."""

    resolved_options = options or SourceConflictReportOptions()
    records: list[EvidenceInputRecord] = []
    filtered_conflict_ids: list[str] = []
    for conflict in report.conflicts:
        if _conflict_filtered(conflict, resolved_options):
            filtered_conflict_ids.append(conflict.conflict_id)
            continue
        included_refs, filtered_refs = _filter_refs(conflict.evidence_refs, resolved_options)
        if not included_refs:
            filtered_conflict_ids.append(conflict.conflict_id)
            continue
        records.append(_record_from_conflict(conflict, included_refs, filtered_refs))

    if not records:
        raise SourceConflictBuildError("filtered report has no remaining conflicts")
    if filtered_conflict_ids:
        records = records + [_filtered_conflicts_record(report, filtered_conflict_ids)]
    return tuple(records)


def source_conflict_report_to_dict(report: SourceConflictReport) -> dict[str, Any]:
    """Serialize one source conflict report deterministically."""

    validated = build_source_conflict_report(report)
    return {
        "report_id": validated.report_id,
        "subject_type": validated.subject_type,
        "subject_id": validated.subject_id,
        "generated_at": validated.generated_at,
        "conflicts": [_conflict_to_dict(conflict) for conflict in validated.conflicts],
        "metadata": _sorted_json_object(validated.metadata),
    }


def _conflict_filtered(conflict: SourceConflictItem, options: SourceConflictReportOptions) -> bool:
    if conflict.resolution_status in {"resolved_externally", "ignored_by_policy"} and not options.include_resolved:
        return True
    if conflict.severity == "info" and not options.include_info:
        return True
    return SEVERITY_RANK[conflict.severity] < SEVERITY_RANK[options.minimum_severity]


def _filter_refs(
    refs: tuple[SourceConflictEvidenceRef, ...],
    options: SourceConflictReportOptions,
) -> tuple[tuple[SourceConflictEvidenceRef, ...], tuple[SourceConflictEvidenceRef, ...]]:
    kept: list[SourceConflictEvidenceRef] = []
    filtered: list[SourceConflictEvidenceRef] = []
    for ref in refs:
        if ref.privacy_scope == "sensitive" and not options.include_sensitive:
            filtered.append(ref)
        else:
            kept.append(ref)
    return tuple(kept), tuple(filtered)


def _record_from_conflict(
    conflict: SourceConflictItem,
    refs: tuple[SourceConflictEvidenceRef, ...],
    filtered_refs: tuple[SourceConflictEvidenceRef, ...],
) -> EvidenceInputRecord:
    caveats = tuple(conflict.caveats)
    if filtered_refs:
        caveats = caveats + (
            {
                "caveat_type": "privacy_redaction",
                "message": "Some source conflict evidence was filtered by assembly options.",
                "severity": "info",
                "metadata": {
                    "filtered_evidence_ids": [ref.evidence_id for ref in filtered_refs],
                    "filtered_count": len(filtered_refs),
                },
            },
        )
    metadata = {
        "conflict_type": conflict.conflict_type,
        "severity": conflict.severity,
        "resolution_status": conflict.resolution_status,
        "field_names": sorted({ref.field_name for ref in refs}),
        **conflict.metadata,
    }
    return _wrap_input_error(
        lambda: EvidenceInputRecord(
            record_id=f"source-conflict:{conflict.conflict_id}",
            record_type="source_conflict",
            label=f"Source conflict: {conflict.conflict_type}",
            summary=conflict.summary,
            confidence=_confidence_for_severity(conflict.severity),
            references=tuple(_input_ref_from_conflict_ref(ref) for ref in refs),
            caveats=caveats,
            privacy_scope=_highest_privacy_scope(refs),
            metadata=metadata,
        )
    )


def _filtered_conflicts_record(report: SourceConflictReport, conflict_ids: list[str]) -> EvidenceInputRecord:
    return _wrap_input_error(
        lambda: EvidenceInputRecord(
            record_id=f"source-conflict-filtered:{report.report_id}",
            record_type="source_conflict",
            label="Filtered source conflicts",
            summary="Some source conflicts were filtered by report options.",
            confidence=1.0,
            references=(
                EvidenceRecordRef(
                    source_type="manual",
                    source_name="Codie source conflict report",
                    source_record_id=report.report_id,
                    source_url=None,
                    observed_at=report.generated_at,
                ),
            ),
            caveats=(
                {
                    "caveat_type": "missing_data",
                    "message": "Some source conflicts were filtered by report options.",
                    "severity": "info",
                    "metadata": {
                        "filtered_conflict_ids": list(conflict_ids),
                        "filtered_count": len(conflict_ids),
                    },
                },
            ),
            privacy_scope="local",
            metadata={"filtered_conflict_ids": list(conflict_ids), "filtered_count": len(conflict_ids)},
        )
    )


def _input_ref_from_conflict_ref(ref: SourceConflictEvidenceRef) -> EvidenceRecordRef:
    return _wrap_input_error(
        lambda: EvidenceRecordRef(
            source_type=ref.source_type,
            source_name=ref.source_name,
            source_record_id=ref.source_record_id,
            source_url=ref.source_url,
            observed_at=ref.observed_at,
        )
    )


def _conflict_to_dict(conflict: SourceConflictItem) -> dict[str, Any]:
    return {
        "conflict_id": conflict.conflict_id,
        "conflict_type": conflict.conflict_type,
        "summary": conflict.summary,
        "severity": conflict.severity,
        "resolution_status": conflict.resolution_status,
        "evidence_refs": [_ref_to_dict(ref) for ref in sorted(conflict.evidence_refs, key=lambda item: item.evidence_id)],
        "caveats": [_sorted_json_object(caveat) for caveat in conflict.caveats],
        "metadata": _sorted_json_object(conflict.metadata),
    }


def _ref_to_dict(ref: SourceConflictEvidenceRef) -> dict[str, Any]:
    return {
        "evidence_id": ref.evidence_id,
        "source_type": ref.source_type,
        "source_name": ref.source_name,
        "source_record_id": ref.source_record_id,
        "source_url": ref.source_url,
        "observed_at": ref.observed_at,
        "field_name": ref.field_name,
        "field_value": ref.field_value,
        "privacy_scope": ref.privacy_scope,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _confidence_for_severity(severity: str) -> float:
    if severity == "blocking":
        return 1.0
    if severity == "warning":
        return 0.75
    return 0.5


def _highest_privacy_scope(refs: tuple[SourceConflictEvidenceRef, ...]) -> str:
    return max((ref.privacy_scope for ref in refs), key=lambda scope: PRIVACY_RANK[scope])


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SourceConflictBuildError(f"{field_name} is required")


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    _require_text(value, field_name)
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise SourceConflictBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise SourceConflictBuildError("metadata must be an object")
    _reject_forbidden_metadata(metadata)
    return _validate_json_value(metadata, "metadata")


def _validate_json_value(value: Any, field_name: str) -> Any:
    _reject_forbidden_metadata(value)
    try:
        encoded = json.dumps(value, sort_keys=True)
        decoded = json.loads(encoded)
    except (TypeError, ValueError) as exc:
        raise SourceConflictBuildError(f"{field_name} must be JSON-compatible") from exc
    return decoded


def _reject_forbidden_metadata(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise SourceConflictBuildError(f"metadata contains forbidden private field: {key}")
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
        raise SourceConflictBuildError(str(exc)) from exc


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates
