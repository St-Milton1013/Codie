"""In-memory Decision Intelligence boundary packets."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.evidence_fusion import (
    EvidenceCaveat,
    EvidenceConflict,
    EvidenceSourceAgreement,
    UnifiedEvidenceObject,
    UnifiedEvidenceSubject,
)


ALLOWED_DECISION_TYPES = frozenset(
    {
        "evidence_summary",
        "deck_health_input",
        "replacement_input",
        "package_input",
        "dashboard_input",
        "candidate_signal",
    }
)

ALLOWED_EXPECTED_IMPACTS = frozenset({"none", "low", "medium", "high", "unknown"})
ALLOWED_SPECULATION_LEVELS = frozenset({"none", "low", "medium", "high"})
ALLOWED_BUNDLE_TYPES = frozenset(
    {
        "deck_analysis",
        "commander_profile",
        "card_profile",
        "package_profile",
        "dashboard_context",
        "report_context",
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


class DecisionIntelligenceBuildError(ValueError):
    """Raised when Decision Intelligence boundary packets are unsafe."""


@dataclass(frozen=True)
class DecisionIntelligenceOptions:
    maximum_evidence_objects_per_packet: int = 128
    maximum_packets_per_bundle: int = 256
    decision_version: str = "phase26b-boundary"

    def __post_init__(self) -> None:
        for field_name in ("maximum_evidence_objects_per_packet", "maximum_packets_per_bundle"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or value < 1:
                raise DecisionIntelligenceBuildError(f"{field_name} must be a positive integer")
        _require_text(self.decision_version, "decision_version")


@dataclass(frozen=True)
class DecisionEvidenceBreakdown:
    authority_ref_ids: tuple[str, ...] = ()
    measured_metric_ref_ids: tuple[str, ...] = ()
    tournament_observation_ref_ids: tuple[str, ...] = ()
    primer_context_ref_ids: tuple[str, ...] = ()
    simulator_ref_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    conflict_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for field_name in (
            "authority_ref_ids",
            "measured_metric_ref_ids",
            "tournament_observation_ref_ids",
            "primer_context_ref_ids",
            "simulator_ref_ids",
            "caveat_ids",
            "conflict_ids",
        ):
            object.__setattr__(self, field_name, _sorted_text_tuple(getattr(self, field_name), field_name))


@dataclass(frozen=True)
class DecisionPacket:
    decision_id: str
    decision_type: str
    subject: UnifiedEvidenceSubject
    summary: str
    confidence: float
    expected_impact: str
    source_agreement: EvidenceSourceAgreement
    evidence_object_ids: tuple[str, ...]
    supporting_ref_ids: tuple[str, ...]
    contradicting_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    speculation_level: str
    generated_at: str
    decision_version: str
    evidence_breakdown: DecisionEvidenceBreakdown
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.decision_id, "decision_id")
        object.__setattr__(self, "decision_type", _normalize_allowed(self.decision_type, ALLOWED_DECISION_TYPES, "decision_type"))
        if not isinstance(self.subject, UnifiedEvidenceSubject):
            raise DecisionIntelligenceBuildError("subject must be a UnifiedEvidenceSubject")
        object.__setattr__(self, "summary", _validate_text(self.summary, "summary"))
        _validate_ratio(self.confidence, "confidence")
        object.__setattr__(self, "expected_impact", _normalize_allowed(self.expected_impact, ALLOWED_EXPECTED_IMPACTS, "expected_impact"))
        if not isinstance(self.source_agreement, EvidenceSourceAgreement):
            raise DecisionIntelligenceBuildError("source_agreement must be an EvidenceSourceAgreement")
        object.__setattr__(self, "evidence_object_ids", _sorted_text_tuple(self.evidence_object_ids, "evidence_object_ids"))
        object.__setattr__(self, "supporting_ref_ids", _sorted_text_tuple(self.supporting_ref_ids, "supporting_ref_ids"))
        object.__setattr__(self, "contradicting_ref_ids", _sorted_text_tuple(self.contradicting_ref_ids, "contradicting_ref_ids"))
        object.__setattr__(self, "caveat_ids", _sorted_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "speculation_level", _normalize_allowed(self.speculation_level, ALLOWED_SPECULATION_LEVELS, "speculation_level"))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.decision_version, "decision_version")
        if not isinstance(self.evidence_breakdown, DecisionEvidenceBreakdown):
            raise DecisionIntelligenceBuildError("evidence_breakdown must be a DecisionEvidenceBreakdown")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _validate_decision_quality(self)


@dataclass(frozen=True)
class DecisionPacketBundle:
    bundle_id: str
    bundle_type: str
    subject: UnifiedEvidenceSubject
    decision_packets: tuple[DecisionPacket, ...]
    caveats: tuple[EvidenceCaveat, ...]
    conflicts: tuple[EvidenceConflict, ...]
    generated_at: str
    decision_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.bundle_id, "bundle_id")
        object.__setattr__(self, "bundle_type", _normalize_allowed(self.bundle_type, ALLOWED_BUNDLE_TYPES, "bundle_type"))
        if not isinstance(self.subject, UnifiedEvidenceSubject):
            raise DecisionIntelligenceBuildError("subject must be a UnifiedEvidenceSubject")
        object.__setattr__(self, "decision_packets", _sort_tuple(self.decision_packets, "decision_id", DecisionPacket))
        object.__setattr__(self, "caveats", _sort_tuple(self.caveats, "caveat_id", EvidenceCaveat))
        object.__setattr__(self, "conflicts", _sort_tuple(self.conflicts, "conflict_id", EvidenceConflict))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.decision_version, "decision_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_decision_packet_bundle(self)


def build_decision_packet(
    decision_id: str,
    decision_type: str,
    subject: UnifiedEvidenceSubject,
    summary: str,
    confidence: float,
    expected_impact: str,
    source_agreement: EvidenceSourceAgreement,
    evidence_objects: tuple[UnifiedEvidenceObject, ...],
    generated_at: str,
    supporting_ref_ids: tuple[str, ...] = (),
    contradicting_ref_ids: tuple[str, ...] = (),
    caveat_ids: tuple[str, ...] = (),
    speculation_level: str = "none",
    decision_version: str = "phase26b-boundary",
    metadata: dict[str, Any] | None = None,
    options: DecisionIntelligenceOptions | None = None,
) -> DecisionPacket:
    """Build one in-memory Decision Intelligence boundary packet."""

    resolved_options = options or DecisionIntelligenceOptions()
    if not evidence_objects:
        raise DecisionIntelligenceBuildError("DecisionPacket requires at least one UnifiedEvidenceObject")
    if len(evidence_objects) > resolved_options.maximum_evidence_objects_per_packet:
        raise DecisionIntelligenceBuildError("DecisionPacket exceeds maximum_evidence_objects_per_packet")
    _validate_evidence_objects(subject, evidence_objects)
    breakdown = _breakdown_from_evidence_objects(evidence_objects)
    resolved_caveat_ids = caveat_ids or breakdown.caveat_ids
    return DecisionPacket(
        decision_id=decision_id,
        decision_type=decision_type,
        subject=subject,
        summary=summary,
        confidence=confidence,
        expected_impact=expected_impact,
        source_agreement=source_agreement,
        evidence_object_ids=tuple(item.evidence_object_id for item in evidence_objects),
        supporting_ref_ids=supporting_ref_ids or breakdown.measured_metric_ref_ids,
        contradicting_ref_ids=contradicting_ref_ids,
        caveat_ids=resolved_caveat_ids,
        speculation_level=speculation_level,
        generated_at=generated_at,
        decision_version=decision_version or resolved_options.decision_version,
        evidence_breakdown=breakdown,
        metadata=metadata or {},
    )


def build_decision_packet_bundle(
    bundle_id: str,
    bundle_type: str,
    subject: UnifiedEvidenceSubject,
    decision_packets: tuple[DecisionPacket, ...],
    generated_at: str,
    caveats: tuple[EvidenceCaveat, ...] = (),
    conflicts: tuple[EvidenceConflict, ...] = (),
    decision_version: str = "phase26b-boundary",
    metadata: dict[str, Any] | None = None,
    options: DecisionIntelligenceOptions | None = None,
) -> DecisionPacketBundle:
    """Build one in-memory Decision Intelligence packet bundle."""

    resolved_options = options or DecisionIntelligenceOptions()
    if len(decision_packets) > resolved_options.maximum_packets_per_bundle:
        raise DecisionIntelligenceBuildError("DecisionPacketBundle exceeds maximum_packets_per_bundle")
    return DecisionPacketBundle(
        bundle_id=bundle_id,
        bundle_type=bundle_type,
        subject=subject,
        decision_packets=decision_packets,
        caveats=caveats,
        conflicts=conflicts,
        generated_at=generated_at,
        decision_version=decision_version or resolved_options.decision_version,
        metadata=metadata or {},
    )


def validate_decision_packet_bundle(bundle: DecisionPacketBundle) -> DecisionPacketBundle:
    """Validate one Decision Intelligence packet bundle."""

    if not bundle.decision_packets:
        raise DecisionIntelligenceBuildError("DecisionPacketBundle requires at least one packet")
    duplicates = _duplicates([item.decision_id for item in bundle.decision_packets])
    if duplicates:
        raise DecisionIntelligenceBuildError(f"duplicate decision_id: {duplicates[0]}")
    if any(item.subject.subject_id != bundle.subject.subject_id for item in bundle.decision_packets):
        raise DecisionIntelligenceBuildError("all decision packets must match bundle subject")
    return bundle


def decision_packet_to_dict(packet: DecisionPacket) -> dict[str, Any]:
    """Serialize one Decision Intelligence packet deterministically."""

    return {
        "decision_id": packet.decision_id,
        "decision_type": packet.decision_type,
        "subject": _subject_to_dict(packet.subject),
        "summary": packet.summary,
        "confidence": packet.confidence,
        "expected_impact": packet.expected_impact,
        "source_agreement": _source_agreement_to_dict(packet.source_agreement),
        "evidence_object_ids": list(packet.evidence_object_ids),
        "supporting_ref_ids": list(packet.supporting_ref_ids),
        "contradicting_ref_ids": list(packet.contradicting_ref_ids),
        "caveat_ids": list(packet.caveat_ids),
        "speculation_level": packet.speculation_level,
        "generated_at": packet.generated_at,
        "decision_version": packet.decision_version,
        "evidence_breakdown": _evidence_breakdown_to_dict(packet.evidence_breakdown),
        "metadata": _sorted_json_object(packet.metadata),
    }


def decision_packet_bundle_to_dict(bundle: DecisionPacketBundle) -> dict[str, Any]:
    """Serialize one Decision Intelligence packet bundle deterministically."""

    validated = validate_decision_packet_bundle(bundle)
    return {
        "bundle_id": validated.bundle_id,
        "bundle_type": validated.bundle_type,
        "subject": _subject_to_dict(validated.subject),
        "decision_packets": [decision_packet_to_dict(item) for item in validated.decision_packets],
        "caveats": [_caveat_to_dict(item) for item in validated.caveats],
        "conflicts": [_conflict_to_dict(item) for item in validated.conflicts],
        "generated_at": validated.generated_at,
        "decision_version": validated.decision_version,
        "metadata": _sorted_json_object(validated.metadata),
    }


def _validate_evidence_objects(
    subject: UnifiedEvidenceSubject, evidence_objects: tuple[UnifiedEvidenceObject, ...]
) -> None:
    for item in evidence_objects:
        if not isinstance(item, UnifiedEvidenceObject):
            raise DecisionIntelligenceBuildError("evidence_objects must contain UnifiedEvidenceObject")
        if item.subject.subject_id != subject.subject_id:
            raise DecisionIntelligenceBuildError("all evidence objects must match decision subject")


def _breakdown_from_evidence_objects(
    evidence_objects: tuple[UnifiedEvidenceObject, ...],
) -> DecisionEvidenceBreakdown:
    authority_ref_ids: list[str] = []
    measured_metric_ref_ids: list[str] = []
    tournament_observation_ref_ids: list[str] = []
    primer_context_ref_ids: list[str] = []
    simulator_ref_ids: list[str] = []
    caveat_ids: list[str] = []
    conflict_ids: list[str] = []
    for item in evidence_objects:
        authority_ref_ids.extend(ref.authority_ref_id for ref in item.authority_refs)
        measured_metric_ref_ids.extend(ref.metric_ref_id for ref in item.metric_refs)
        tournament_observation_ref_ids.extend(ref.observation_ref_id for ref in item.observation_refs)
        primer_context_ref_ids.extend(ref.primer_context_ref_id for ref in item.primer_context_refs)
        simulator_ref_ids.extend(ref.simulator_ref_id for ref in item.simulator_refs)
        caveat_ids.extend(ref.caveat_id for ref in item.caveats)
        conflict_ids.extend(ref.conflict_id for ref in item.conflicts)
    return DecisionEvidenceBreakdown(
        authority_ref_ids=tuple(authority_ref_ids),
        measured_metric_ref_ids=tuple(measured_metric_ref_ids),
        tournament_observation_ref_ids=tuple(tournament_observation_ref_ids),
        primer_context_ref_ids=tuple(primer_context_ref_ids),
        simulator_ref_ids=tuple(simulator_ref_ids),
        caveat_ids=tuple(caveat_ids),
        conflict_ids=tuple(conflict_ids),
    )


def _validate_decision_quality(packet: DecisionPacket) -> None:
    if not packet.evidence_object_ids:
        raise DecisionIntelligenceBuildError("DecisionPacket requires evidence_object_ids")
    if packet.confidence >= 0.75 and packet.source_agreement.agreement_label not in {"strong", "mixed"}:
        raise DecisionIntelligenceBuildError("high confidence requires strong or mixed source agreement")
    if packet.speculation_level == "high" and packet.confidence >= 0.5:
        raise DecisionIntelligenceBuildError("high speculation cannot pair with medium or high confidence")


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


def _evidence_breakdown_to_dict(breakdown: DecisionEvidenceBreakdown) -> dict[str, Any]:
    return {
        "authority_ref_ids": list(breakdown.authority_ref_ids),
        "measured_metric_ref_ids": list(breakdown.measured_metric_ref_ids),
        "tournament_observation_ref_ids": list(breakdown.tournament_observation_ref_ids),
        "primer_context_ref_ids": list(breakdown.primer_context_ref_ids),
        "simulator_ref_ids": list(breakdown.simulator_ref_ids),
        "caveat_ids": list(breakdown.caveat_ids),
        "conflict_ids": list(breakdown.conflict_ids),
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


def _sort_tuple(items: tuple[Any, ...], id_field: str, item_type: type) -> tuple[Any, ...]:
    for item in items:
        if not isinstance(item, item_type):
            raise DecisionIntelligenceBuildError(f"{id_field} collection contains invalid item")
    return tuple(sorted(items, key=lambda item: getattr(item, id_field)))


def _sorted_text_tuple(items: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(items, tuple):
        raise DecisionIntelligenceBuildError(f"{field_name} must be a tuple")
    return tuple(sorted(_require_text(item, field_name) for item in items))


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DecisionIntelligenceBuildError(f"{field_name} is required")
    return value.strip()


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).lower()
    if normalized not in allowed:
        raise DecisionIntelligenceBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_ratio(value: float, field_name: str) -> None:
    if not isinstance(value, int | float):
        raise DecisionIntelligenceBuildError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise DecisionIntelligenceBuildError(f"{field_name} must be between 0 and 1")


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    normalized = " ".join(text.lower().split())
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment in normalized:
            raise DecisionIntelligenceBuildError(f"forbidden strategic language in {field_name}")
    return text


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise DecisionIntelligenceBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise DecisionIntelligenceBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise DecisionIntelligenceBuildError(f"{path} contains forbidden metadata key: {key}")
            if normalized_key in STACK_TRACE_KEYS:
                raise DecisionIntelligenceBuildError(f"{path} contains forbidden stack trace key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise DecisionIntelligenceBuildError(f"{path} must be JSON-compatible")


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
