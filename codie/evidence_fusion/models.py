"""In-memory unified evidence packets for Evidence Fusion."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


ALLOWED_AUTHORITY_TYPES = frozenset(
    {
        "scryfall_card",
        "scryfall_ruling",
        "scryfall_legality",
        "commander_spellbook_combo",
        "official_rules",
        "official_oracle_ruling",
        "official_release_note",
        "official_ban_announcement",
    }
)

ALLOWED_OBSERVATION_TYPES = frozenset(
    {
        "canonical_event",
        "canonical_deck",
        "canonical_deck_card",
        "event_deck_entry",
        "user_deck_snapshot",
        "primer_metadata",
        "source_conflict",
        "unsupported_card_queue_item",
    }
)

ALLOWED_METRIC_TYPES = frozenset(
    {
        "frequency",
        "inclusion_rate",
        "win_rate",
        "top_cut_rate",
        "trend_delta",
        "co_occurrence",
        "lift",
        "support",
        "confidence",
        "similarity",
        "package_frequency",
        "card_performance",
        "innovation_signal",
        "simulator_statistic",
        "commander_staple_statistic",
    }
)

ALLOWED_PRIMER_CONTEXT_TYPES = frozenset(
    {
        "archetype_hint",
        "strategy_summary",
        "mulligan_philosophy",
        "pilot_priority",
        "meta_assumption",
        "flex_slot_explanation",
    }
)

ALLOWED_CAVEAT_TYPES = frozenset(
    {
        "low_sample",
        "low_coverage",
        "source_conflict",
        "unsupported_card",
        "stale_data",
        "primer_context_only",
        "simulator_limitation",
        "regional_bias",
        "missing_authority_ref",
    }
)

ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})
ALLOWED_AGREEMENT_LABELS = frozenset({"strong", "mixed", "weak", "unknown"})

ALLOWED_SUBJECT_TYPES = frozenset(
    {
        "card",
        "commander",
        "partner_pair",
        "deck",
        "package",
        "combo",
        "archetype",
        "event",
        "simulation_target",
        "tag",
    }
)

ALLOWED_EVIDENCE_LEVELS = frozenset({"high", "medium", "low", "unknown"})
ALLOWED_SPECULATION_LEVELS = frozenset({"none", "low", "medium", "high"})

ALLOWED_BUNDLE_TYPES = frozenset(
    {
        "deck_analysis",
        "commander_profile",
        "card_profile",
        "package_profile",
        "recommendation_input",
        "chat_context",
        "report_context",
        "dashboard_context",
        "simulation_context",
    }
)

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

STACK_TRACE_KEYS = frozenset({"traceback", "stack", "stack_trace", "exception_trace"})

FORBIDDEN_TEXT_FRAGMENTS = (
    "should " + "play",
    "should be " + "played",
    "should be " + "cut",
    "must " + "include",
    "correct " + "card",
    "breaks the " + "format",
    "secretly " + "optimal",
    "cut " + "this",
    "strict " + "upgrade",
    "auto-" + "include",
    "recommended " + "cut",
    "recommended " + "include",
)


class EvidenceFusionBuildError(ValueError):
    """Raised when unified evidence packets cannot be built safely."""


@dataclass(frozen=True)
class EvidenceFusionOptions:
    allow_sensitive: bool = False
    allow_local_user_data: bool = False
    allow_primer_context: bool = True
    allow_simulator_refs: bool = True
    allow_conflicts: bool = True
    maximum_refs_per_object: int = 256
    maximum_objects_per_bundle: int = 512
    evidence_version: str = "phase25a-contract"

    def __post_init__(self) -> None:
        for field_name in ("maximum_refs_per_object", "maximum_objects_per_bundle"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or value < 1:
                raise EvidenceFusionBuildError(f"{field_name} must be a positive integer")
        _require_text(self.evidence_version, "evidence_version")


@dataclass(frozen=True)
class EvidenceAuthorityRef:
    authority_ref_id: str
    authority_type: str
    authority_source: str
    authority_key: str
    authority_label: str
    authority_url: str | None
    authority_version: str
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.authority_ref_id, "authority_ref_id")
        object.__setattr__(self, "authority_type", _normalize_allowed(self.authority_type, ALLOWED_AUTHORITY_TYPES, "authority_type"))
        _require_text(self.authority_source, "authority_source")
        _require_text(self.authority_key, "authority_key")
        _require_text(self.authority_label, "authority_label")
        if self.authority_url is not None:
            _require_text(self.authority_url, "authority_url")
        _require_text(self.authority_version, "authority_version")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceObservationRef:
    observation_ref_id: str
    observation_type: str
    source_system: str
    source_record_id: str
    canonical_record_id: str | None
    source_label: str
    source_url: str | None
    observed_at: str
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.observation_ref_id, "observation_ref_id")
        object.__setattr__(self, "observation_type", _normalize_allowed(self.observation_type, ALLOWED_OBSERVATION_TYPES, "observation_type"))
        _require_text(self.source_system, "source_system")
        _require_text(self.source_record_id, "source_record_id")
        if self.canonical_record_id is not None:
            _require_text(self.canonical_record_id, "canonical_record_id")
        _require_text(self.source_label, "source_label")
        if self.source_url is not None:
            _require_text(self.source_url, "source_url")
        _require_text(self.observed_at, "observed_at")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceMetricRef:
    metric_ref_id: str
    metric_type: str
    metric_name: str
    metric_value: float
    metric_unit: str
    scope_type: str
    scope_key: str
    window_start: str
    window_end: str
    sample_size: int
    coverage_ratio: float
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.metric_ref_id, "metric_ref_id")
        object.__setattr__(self, "metric_type", _normalize_allowed(self.metric_type, ALLOWED_METRIC_TYPES, "metric_type"))
        _require_text(self.metric_name, "metric_name")
        _validate_number(self.metric_value, "metric_value")
        _require_text(self.metric_unit, "metric_unit")
        _require_text(self.scope_type, "scope_type")
        _require_text(self.scope_key, "scope_key")
        _require_text(self.window_start, "window_start")
        _require_text(self.window_end, "window_end")
        _validate_non_negative_int(self.sample_size, "sample_size")
        _validate_ratio(self.coverage_ratio, "coverage_ratio")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidencePrimerContextRef:
    primer_context_ref_id: str
    primer_ref_id: str
    context_type: str
    context_label: str
    commander_signature: str | None
    source_url: str | None
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.primer_context_ref_id, "primer_context_ref_id")
        _require_text(self.primer_ref_id, "primer_ref_id")
        object.__setattr__(self, "context_type", _normalize_allowed(self.context_type, ALLOWED_PRIMER_CONTEXT_TYPES, "context_type"))
        _require_text(self.context_label, "context_label")
        if self.commander_signature is not None:
            _require_text(self.commander_signature, "commander_signature")
        if self.source_url is not None:
            _require_text(self.source_url, "source_url")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceSimulatorRef:
    simulator_ref_id: str
    simulation_type: str
    result_id: str
    deck_hash: str
    target_label: str
    success_rate: float
    sample_size: int
    unsupported_cards_count: int
    review_status: str
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.simulator_ref_id, "simulator_ref_id")
        _require_text(self.simulation_type, "simulation_type")
        _require_text(self.result_id, "result_id")
        _require_text(self.deck_hash, "deck_hash")
        _require_text(self.target_label, "target_label")
        _validate_ratio(self.success_rate, "success_rate")
        _validate_non_negative_int(self.sample_size, "sample_size")
        _validate_non_negative_int(self.unsupported_cards_count, "unsupported_cards_count")
        _require_text(self.review_status, "review_status")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceCaveat:
    caveat_id: str
    caveat_type: str
    severity: str
    message: str
    related_ref_ids: tuple[str, ...]
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.caveat_id, "caveat_id")
        object.__setattr__(self, "caveat_type", _normalize_allowed(self.caveat_type, ALLOWED_CAVEAT_TYPES, "caveat_type"))
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(self, "message", _validate_text(self.message, "message"))
        object.__setattr__(self, "related_ref_ids", tuple(sorted(_require_text(item, "related_ref_id") for item in self.related_ref_ids)))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceConflict:
    conflict_id: str
    conflict_type: str
    summary: str
    ref_ids: tuple[str, ...]
    requires_manual_review: bool
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.conflict_id, "conflict_id")
        _require_text(self.conflict_type, "conflict_type")
        object.__setattr__(self, "summary", _validate_text(self.summary, "summary"))
        object.__setattr__(self, "ref_ids", tuple(sorted(_require_text(item, "ref_id") for item in self.ref_ids)))
        if not isinstance(self.requires_manual_review, bool):
            raise EvidenceFusionBuildError("requires_manual_review must be a bool")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class EvidenceSourceAgreement:
    agreement_id: str
    agreement_label: str
    supporting_ref_ids: tuple[str, ...]
    conflicting_ref_ids: tuple[str, ...]
    coverage_ratio: float
    sample_size: int
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.agreement_id, "agreement_id")
        object.__setattr__(self, "agreement_label", _normalize_allowed(self.agreement_label, ALLOWED_AGREEMENT_LABELS, "agreement_label"))
        object.__setattr__(self, "supporting_ref_ids", tuple(sorted(_require_text(item, "supporting_ref_id") for item in self.supporting_ref_ids)))
        object.__setattr__(self, "conflicting_ref_ids", tuple(sorted(_require_text(item, "conflicting_ref_id") for item in self.conflicting_ref_ids)))
        _validate_ratio(self.coverage_ratio, "coverage_ratio")
        _validate_non_negative_int(self.sample_size, "sample_size")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class UnifiedEvidenceSubject:
    subject_id: str
    subject_type: str
    subject_key: str
    display_name: str
    commander_signature: str | None = None
    oracle_id: str | None = None
    scryfall_id: str | None = None
    region_code: str | None = None
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.subject_id, "subject_id")
        object.__setattr__(self, "subject_type", _normalize_allowed(self.subject_type, ALLOWED_SUBJECT_TYPES, "subject_type"))
        _require_text(self.subject_key, "subject_key")
        _require_text(self.display_name, "display_name")
        for field_name in ("commander_signature", "oracle_id", "scryfall_id", "region_code"):
            value = getattr(self, field_name)
            if value is not None:
                _require_text(value, field_name)
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class UnifiedEvidenceObject:
    evidence_object_id: str
    subject: UnifiedEvidenceSubject
    authority_refs: tuple[EvidenceAuthorityRef, ...]
    observation_refs: tuple[EvidenceObservationRef, ...]
    metric_refs: tuple[EvidenceMetricRef, ...]
    primer_context_refs: tuple[EvidencePrimerContextRef, ...]
    simulator_refs: tuple[EvidenceSimulatorRef, ...]
    caveats: tuple[EvidenceCaveat, ...]
    conflicts: tuple[EvidenceConflict, ...]
    source_agreement: EvidenceSourceAgreement
    evidence_level: str
    speculation_level: str
    coverage_ratio: float
    sample_size: int
    generated_at: str
    evidence_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.evidence_object_id, "evidence_object_id")
        if not isinstance(self.subject, UnifiedEvidenceSubject):
            raise EvidenceFusionBuildError("subject must be a UnifiedEvidenceSubject")
        object.__setattr__(self, "authority_refs", _sort_tuple(self.authority_refs, "authority_ref_id", EvidenceAuthorityRef))
        object.__setattr__(self, "observation_refs", _sort_tuple(self.observation_refs, "observation_ref_id", EvidenceObservationRef))
        object.__setattr__(self, "metric_refs", _sort_tuple(self.metric_refs, "metric_ref_id", EvidenceMetricRef))
        object.__setattr__(self, "primer_context_refs", _sort_tuple(self.primer_context_refs, "primer_context_ref_id", EvidencePrimerContextRef))
        object.__setattr__(self, "simulator_refs", _sort_tuple(self.simulator_refs, "simulator_ref_id", EvidenceSimulatorRef))
        object.__setattr__(self, "caveats", _sort_tuple(self.caveats, "caveat_id", EvidenceCaveat))
        object.__setattr__(self, "conflicts", _sort_tuple(self.conflicts, "conflict_id", EvidenceConflict))
        if not isinstance(self.source_agreement, EvidenceSourceAgreement):
            raise EvidenceFusionBuildError("source_agreement must be an EvidenceSourceAgreement")
        object.__setattr__(self, "evidence_level", _normalize_allowed(self.evidence_level, ALLOWED_EVIDENCE_LEVELS, "evidence_level"))
        object.__setattr__(self, "speculation_level", _normalize_allowed(self.speculation_level, ALLOWED_SPECULATION_LEVELS, "speculation_level"))
        _validate_ratio(self.coverage_ratio, "coverage_ratio")
        _validate_non_negative_int(self.sample_size, "sample_size")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.evidence_version, "evidence_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _validate_evidence_quality(self)


@dataclass(frozen=True)
class UnifiedEvidenceBundle:
    bundle_id: str
    bundle_type: str
    subject: UnifiedEvidenceSubject
    evidence_objects: tuple[UnifiedEvidenceObject, ...]
    caveats: tuple[EvidenceCaveat, ...]
    conflicts: tuple[EvidenceConflict, ...]
    generated_at: str
    evidence_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.bundle_id, "bundle_id")
        object.__setattr__(self, "bundle_type", _normalize_allowed(self.bundle_type, ALLOWED_BUNDLE_TYPES, "bundle_type"))
        if not isinstance(self.subject, UnifiedEvidenceSubject):
            raise EvidenceFusionBuildError("subject must be a UnifiedEvidenceSubject")
        object.__setattr__(self, "evidence_objects", _sort_tuple(self.evidence_objects, "evidence_object_id", UnifiedEvidenceObject))
        object.__setattr__(self, "caveats", _sort_tuple(self.caveats, "caveat_id", EvidenceCaveat))
        object.__setattr__(self, "conflicts", _sort_tuple(self.conflicts, "conflict_id", EvidenceConflict))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.evidence_version, "evidence_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_unified_evidence_bundle(self)


def build_unified_evidence_object(
    evidence_object_id: str,
    subject: UnifiedEvidenceSubject,
    source_agreement: EvidenceSourceAgreement,
    generated_at: str,
    authority_refs: tuple[EvidenceAuthorityRef, ...] = (),
    observation_refs: tuple[EvidenceObservationRef, ...] = (),
    metric_refs: tuple[EvidenceMetricRef, ...] = (),
    primer_context_refs: tuple[EvidencePrimerContextRef, ...] = (),
    simulator_refs: tuple[EvidenceSimulatorRef, ...] = (),
    caveats: tuple[EvidenceCaveat, ...] = (),
    conflicts: tuple[EvidenceConflict, ...] = (),
    evidence_level: str = "unknown",
    speculation_level: str = "none",
    coverage_ratio: float = 0.0,
    sample_size: int = 0,
    evidence_version: str = "phase25a-contract",
    metadata: dict[str, Any] | None = None,
    options: EvidenceFusionOptions | None = None,
) -> UnifiedEvidenceObject:
    """Build one in-memory unified evidence object from already-available refs."""

    resolved_options = options or EvidenceFusionOptions()
    _validate_options_against_refs(resolved_options, primer_context_refs, simulator_refs, conflicts)
    total_refs = (
        len(authority_refs)
        + len(observation_refs)
        + len(metric_refs)
        + len(primer_context_refs)
        + len(simulator_refs)
        + len(caveats)
        + len(conflicts)
    )
    if total_refs > resolved_options.maximum_refs_per_object:
        raise EvidenceFusionBuildError("evidence object exceeds maximum_refs_per_object")
    return UnifiedEvidenceObject(
        evidence_object_id=evidence_object_id,
        subject=subject,
        authority_refs=authority_refs,
        observation_refs=observation_refs,
        metric_refs=metric_refs,
        primer_context_refs=primer_context_refs,
        simulator_refs=simulator_refs,
        caveats=caveats,
        conflicts=conflicts,
        source_agreement=source_agreement,
        evidence_level=evidence_level,
        speculation_level=speculation_level,
        coverage_ratio=coverage_ratio,
        sample_size=sample_size,
        generated_at=generated_at,
        evidence_version=evidence_version or resolved_options.evidence_version,
        metadata=metadata or {},
    )


def build_unified_evidence_bundle(
    bundle_id: str,
    bundle_type: str,
    subject: UnifiedEvidenceSubject,
    evidence_objects: tuple[UnifiedEvidenceObject, ...],
    generated_at: str,
    caveats: tuple[EvidenceCaveat, ...] = (),
    conflicts: tuple[EvidenceConflict, ...] = (),
    evidence_version: str = "phase25a-contract",
    metadata: dict[str, Any] | None = None,
    options: EvidenceFusionOptions | None = None,
) -> UnifiedEvidenceBundle:
    """Build one in-memory unified evidence bundle."""

    resolved_options = options or EvidenceFusionOptions()
    if len(evidence_objects) > resolved_options.maximum_objects_per_bundle:
        raise EvidenceFusionBuildError("bundle exceeds maximum_objects_per_bundle")
    if conflicts and not resolved_options.allow_conflicts:
        raise EvidenceFusionBuildError("conflicts are disabled")
    return UnifiedEvidenceBundle(
        bundle_id=bundle_id,
        bundle_type=bundle_type,
        subject=subject,
        evidence_objects=evidence_objects,
        caveats=caveats,
        conflicts=conflicts,
        generated_at=generated_at,
        evidence_version=evidence_version or resolved_options.evidence_version,
        metadata=metadata or {},
    )


def validate_unified_evidence_bundle(bundle: UnifiedEvidenceBundle) -> UnifiedEvidenceBundle:
    """Validate one unified evidence bundle."""

    if not bundle.evidence_objects:
        raise EvidenceFusionBuildError("UnifiedEvidenceBundle requires at least one evidence object")
    duplicates = _duplicates([item.evidence_object_id for item in bundle.evidence_objects])
    if duplicates:
        raise EvidenceFusionBuildError(f"duplicate evidence_object_id: {duplicates[0]}")
    if any(item.subject.subject_id != bundle.subject.subject_id for item in bundle.evidence_objects):
        raise EvidenceFusionBuildError("all evidence objects must match bundle subject")
    return bundle


def unified_evidence_object_to_dict(evidence_object: UnifiedEvidenceObject) -> dict[str, Any]:
    """Serialize one unified evidence object deterministically."""

    return {
        "evidence_object_id": evidence_object.evidence_object_id,
        "subject": _subject_to_dict(evidence_object.subject),
        "authority_refs": [_authority_ref_to_dict(item) for item in evidence_object.authority_refs],
        "observation_refs": [_observation_ref_to_dict(item) for item in evidence_object.observation_refs],
        "metric_refs": [_metric_ref_to_dict(item) for item in evidence_object.metric_refs],
        "primer_context_refs": [_primer_context_ref_to_dict(item) for item in evidence_object.primer_context_refs],
        "simulator_refs": [_simulator_ref_to_dict(item) for item in evidence_object.simulator_refs],
        "caveats": [_caveat_to_dict(item) for item in evidence_object.caveats],
        "conflicts": [_conflict_to_dict(item) for item in evidence_object.conflicts],
        "source_agreement": _source_agreement_to_dict(evidence_object.source_agreement),
        "evidence_level": evidence_object.evidence_level,
        "speculation_level": evidence_object.speculation_level,
        "coverage_ratio": evidence_object.coverage_ratio,
        "sample_size": evidence_object.sample_size,
        "generated_at": evidence_object.generated_at,
        "evidence_version": evidence_object.evidence_version,
        "metadata": _sorted_json_object(evidence_object.metadata),
    }


def unified_evidence_bundle_to_dict(bundle: UnifiedEvidenceBundle) -> dict[str, Any]:
    """Serialize one unified evidence bundle deterministically."""

    validated = validate_unified_evidence_bundle(bundle)
    return {
        "bundle_id": validated.bundle_id,
        "bundle_type": validated.bundle_type,
        "subject": _subject_to_dict(validated.subject),
        "evidence_objects": [unified_evidence_object_to_dict(item) for item in validated.evidence_objects],
        "caveats": [_caveat_to_dict(item) for item in validated.caveats],
        "conflicts": [_conflict_to_dict(item) for item in validated.conflicts],
        "generated_at": validated.generated_at,
        "evidence_version": validated.evidence_version,
        "metadata": _sorted_json_object(validated.metadata),
    }


def _subject_to_dict(subject: UnifiedEvidenceSubject) -> dict[str, Any]:
    return {
        "subject_id": subject.subject_id,
        "subject_type": subject.subject_type,
        "subject_key": subject.subject_key,
        "display_name": subject.display_name,
        "commander_signature": subject.commander_signature,
        "oracle_id": subject.oracle_id,
        "scryfall_id": subject.scryfall_id,
        "region_code": subject.region_code,
        "generated_at": subject.generated_at,
        "metadata": _sorted_json_object(subject.metadata),
    }


def _authority_ref_to_dict(ref: EvidenceAuthorityRef) -> dict[str, Any]:
    return {
        "authority_ref_id": ref.authority_ref_id,
        "authority_type": ref.authority_type,
        "authority_source": ref.authority_source,
        "authority_key": ref.authority_key,
        "authority_label": ref.authority_label,
        "authority_url": ref.authority_url,
        "authority_version": ref.authority_version,
        "generated_at": ref.generated_at,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _observation_ref_to_dict(ref: EvidenceObservationRef) -> dict[str, Any]:
    return {
        "observation_ref_id": ref.observation_ref_id,
        "observation_type": ref.observation_type,
        "source_system": ref.source_system,
        "source_record_id": ref.source_record_id,
        "canonical_record_id": ref.canonical_record_id,
        "source_label": ref.source_label,
        "source_url": ref.source_url,
        "observed_at": ref.observed_at,
        "generated_at": ref.generated_at,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _metric_ref_to_dict(ref: EvidenceMetricRef) -> dict[str, Any]:
    return {
        "metric_ref_id": ref.metric_ref_id,
        "metric_type": ref.metric_type,
        "metric_name": ref.metric_name,
        "metric_value": ref.metric_value,
        "metric_unit": ref.metric_unit,
        "scope_type": ref.scope_type,
        "scope_key": ref.scope_key,
        "window_start": ref.window_start,
        "window_end": ref.window_end,
        "sample_size": ref.sample_size,
        "coverage_ratio": ref.coverage_ratio,
        "generated_at": ref.generated_at,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _primer_context_ref_to_dict(ref: EvidencePrimerContextRef) -> dict[str, Any]:
    return {
        "primer_context_ref_id": ref.primer_context_ref_id,
        "primer_ref_id": ref.primer_ref_id,
        "context_type": ref.context_type,
        "context_label": ref.context_label,
        "commander_signature": ref.commander_signature,
        "source_url": ref.source_url,
        "generated_at": ref.generated_at,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _simulator_ref_to_dict(ref: EvidenceSimulatorRef) -> dict[str, Any]:
    return {
        "simulator_ref_id": ref.simulator_ref_id,
        "simulation_type": ref.simulation_type,
        "result_id": ref.result_id,
        "deck_hash": ref.deck_hash,
        "target_label": ref.target_label,
        "success_rate": ref.success_rate,
        "sample_size": ref.sample_size,
        "unsupported_cards_count": ref.unsupported_cards_count,
        "review_status": ref.review_status,
        "generated_at": ref.generated_at,
        "metadata": _sorted_json_object(ref.metadata),
    }


def _caveat_to_dict(caveat: EvidenceCaveat) -> dict[str, Any]:
    return {
        "caveat_id": caveat.caveat_id,
        "caveat_type": caveat.caveat_type,
        "severity": caveat.severity,
        "message": caveat.message,
        "related_ref_ids": list(caveat.related_ref_ids),
        "generated_at": caveat.generated_at,
        "metadata": _sorted_json_object(caveat.metadata),
    }


def _conflict_to_dict(conflict: EvidenceConflict) -> dict[str, Any]:
    return {
        "conflict_id": conflict.conflict_id,
        "conflict_type": conflict.conflict_type,
        "summary": conflict.summary,
        "ref_ids": list(conflict.ref_ids),
        "requires_manual_review": conflict.requires_manual_review,
        "generated_at": conflict.generated_at,
        "metadata": _sorted_json_object(conflict.metadata),
    }


def _source_agreement_to_dict(agreement: EvidenceSourceAgreement) -> dict[str, Any]:
    return {
        "agreement_id": agreement.agreement_id,
        "agreement_label": agreement.agreement_label,
        "supporting_ref_ids": list(agreement.supporting_ref_ids),
        "conflicting_ref_ids": list(agreement.conflicting_ref_ids),
        "coverage_ratio": agreement.coverage_ratio,
        "sample_size": agreement.sample_size,
        "generated_at": agreement.generated_at,
        "metadata": _sorted_json_object(agreement.metadata),
    }


def _validate_options_against_refs(
    options: EvidenceFusionOptions,
    primer_context_refs: tuple[EvidencePrimerContextRef, ...],
    simulator_refs: tuple[EvidenceSimulatorRef, ...],
    conflicts: tuple[EvidenceConflict, ...],
) -> None:
    if primer_context_refs and not options.allow_primer_context:
        raise EvidenceFusionBuildError("primer context refs are disabled")
    if simulator_refs and not options.allow_simulator_refs:
        raise EvidenceFusionBuildError("simulator refs are disabled")
    if conflicts and not options.allow_conflicts:
        raise EvidenceFusionBuildError("conflicts are disabled")


def _validate_evidence_quality(evidence_object: UnifiedEvidenceObject) -> None:
    if evidence_object.evidence_level == "high":
        if not evidence_object.metric_refs:
            raise EvidenceFusionBuildError("high evidence requires at least one metric ref")
        if evidence_object.source_agreement.agreement_label not in {"strong", "mixed"}:
            raise EvidenceFusionBuildError("high evidence requires strong or mixed source agreement")
    if evidence_object.evidence_level in {"high", "medium"} and evidence_object.speculation_level == "high":
        raise EvidenceFusionBuildError("high speculation cannot pair with medium or high evidence")


def _sort_tuple(items: tuple[Any, ...], id_field: str, item_type: type) -> tuple[Any, ...]:
    for item in items:
        if not isinstance(item, item_type):
            raise EvidenceFusionBuildError(f"{id_field} collection contains invalid item")
    return tuple(sorted(items, key=lambda item: getattr(item, id_field)))


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvidenceFusionBuildError(f"{field_name} is required")
    return value.strip()


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).lower()
    if normalized not in allowed:
        raise EvidenceFusionBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_number(value: float, field_name: str) -> None:
    if not isinstance(value, int | float):
        raise EvidenceFusionBuildError(f"{field_name} must be numeric")


def _validate_non_negative_int(value: int, field_name: str) -> None:
    if not isinstance(value, int) or value < 0:
        raise EvidenceFusionBuildError(f"{field_name} must be a non-negative integer")


def _validate_ratio(value: float, field_name: str) -> None:
    _validate_number(value, field_name)
    if value < 0 or value > 1:
        raise EvidenceFusionBuildError(f"{field_name} must be between 0 and 1")


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    normalized = " ".join(text.lower().split())
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment in normalized:
            raise EvidenceFusionBuildError(f"forbidden strategic language in {field_name}")
    return text


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise EvidenceFusionBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise EvidenceFusionBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise EvidenceFusionBuildError(f"{path} contains forbidden metadata key: {key}")
            if normalized_key in STACK_TRACE_KEYS:
                raise EvidenceFusionBuildError(f"{path} contains forbidden stack trace key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise EvidenceFusionBuildError(f"{path} must be JSON-compatible")


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates
