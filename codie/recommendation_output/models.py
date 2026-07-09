"""In-memory deck health and recommendation output packets."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.decision_intelligence import DecisionPacket
from codie.evidence_fusion import EvidenceSourceAgreement, UnifiedEvidenceObject, UnifiedEvidenceSubject
from codie.weight_profiles import AnalysisProfile, WeightProfile


ALLOWED_OUTPUT_TYPES = frozenset(
    {"deck_health", "recommendation_candidate", "replacement_suggestion", "package_gap", "evidence_explanation"}
)
ALLOWED_HEALTH_CATEGORIES = frozenset(
    {
        "mana",
        "card_advantage",
        "interaction",
        "win_condition",
        "resilience",
        "speed",
        "consistency",
        "package",
        "legality",
        "data_quality",
    }
)
ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})
ALLOWED_RECOMMENDATION_TYPES = frozenset({"consider_include", "consider_replace", "monitor", "investigate", "no_action"})
ALLOWED_EXPECTED_IMPACTS = frozenset({"none", "low", "medium", "high", "unknown"})
ALLOWED_SPECULATION_LEVELS = frozenset({"none", "low", "medium", "high"})
ALLOWED_BUNDLE_TYPES = frozenset(
    {"deck_analysis", "commander_profile", "card_profile", "package_profile", "dashboard_context", "report_context"}
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
    "you " + "should " + "play",
    "should be " + "played",
    "should be " + "cut",
    "must " + "include",
    "correct " + "card",
    "breaks the " + "format",
    "secretly " + "optimal",
    "cut " + "this",
    "strict " + "upgrade",
    "strictly " + "better",
    "auto-" + "include",
    "recommended " + "cut",
    "recommended " + "include",
    "best " + "card",
)


class RecommendationOutputBuildError(ValueError):
    """Raised when recommendation output packets are unsafe."""


@dataclass(frozen=True)
class RecommendationOutputOptions:
    maximum_outputs_per_bundle: int = 256
    maximum_findings_per_packet: int = 64
    output_version: str = "phase28b-output-packets"

    def __post_init__(self) -> None:
        for field_name in ("maximum_outputs_per_bundle", "maximum_findings_per_packet"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or value < 1:
                raise RecommendationOutputBuildError(f"{field_name} must be a positive integer")
        _require_text(self.output_version, "output_version")


@dataclass(frozen=True)
class DeckHealthFinding:
    finding_id: str
    health_category: str
    severity: str
    finding_label: str
    finding_summary: str
    affected_cards: tuple[str, ...] = ()
    affected_roles: tuple[str, ...] = ()
    supporting_ref_ids: tuple[str, ...] = ()
    contradicting_ref_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.finding_id, "finding_id")
        object.__setattr__(
            self, "health_category", _normalize_allowed(self.health_category, ALLOWED_HEALTH_CATEGORIES, "health_category")
        )
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(self, "finding_label", _validate_text(self.finding_label, "finding_label"))
        object.__setattr__(self, "finding_summary", _validate_text(self.finding_summary, "finding_summary"))
        for field_name in (
            "affected_cards",
            "affected_roles",
            "supporting_ref_ids",
            "contradicting_ref_ids",
            "caveat_ids",
        ):
            object.__setattr__(self, field_name, _sorted_text_tuple(getattr(self, field_name), field_name))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class _OutputBase:
    output_id: str
    output_type: str
    subject: UnifiedEvidenceSubject
    summary: str
    confidence: float
    expected_impact: str
    source_agreement: EvidenceSourceAgreement
    evidence_object_ids: tuple[str, ...]
    decision_ids: tuple[str, ...]
    weight_profile_id: str
    weight_profile_version: str
    analysis_profile_id: str
    analysis_profile_version: str
    supporting_ref_ids: tuple[str, ...]
    contradicting_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    speculation_level: str
    generated_at: str
    output_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.output_id, "output_id")
        object.__setattr__(self, "output_type", _normalize_allowed(self.output_type, ALLOWED_OUTPUT_TYPES, "output_type"))
        if not isinstance(self.subject, UnifiedEvidenceSubject):
            raise RecommendationOutputBuildError("subject must be a UnifiedEvidenceSubject")
        object.__setattr__(self, "summary", _validate_text(self.summary, "summary"))
        _validate_ratio(self.confidence, "confidence")
        object.__setattr__(self, "expected_impact", _normalize_allowed(self.expected_impact, ALLOWED_EXPECTED_IMPACTS, "expected_impact"))
        if not isinstance(self.source_agreement, EvidenceSourceAgreement):
            raise RecommendationOutputBuildError("source_agreement must be an EvidenceSourceAgreement")
        for field_name in (
            "evidence_object_ids",
            "decision_ids",
            "supporting_ref_ids",
            "contradicting_ref_ids",
            "caveat_ids",
        ):
            object.__setattr__(self, field_name, _sorted_text_tuple(getattr(self, field_name), field_name))
        _require_text(self.weight_profile_id, "weight_profile_id")
        _require_text(self.weight_profile_version, "weight_profile_version")
        _require_text(self.analysis_profile_id, "analysis_profile_id")
        _require_text(self.analysis_profile_version, "analysis_profile_version")
        object.__setattr__(self, "speculation_level", _normalize_allowed(self.speculation_level, ALLOWED_SPECULATION_LEVELS, "speculation_level"))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.output_version, "output_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _validate_output_quality(self)


@dataclass(frozen=True)
class DeckHealthPacket(_OutputBase):
    findings: tuple[DeckHealthFinding, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.output_type != "deck_health":
            raise RecommendationOutputBuildError("DeckHealthPacket output_type must be deck_health")
        object.__setattr__(self, "findings", _sort_tuple(self.findings, "finding_id", DeckHealthFinding))
        if not self.findings:
            raise RecommendationOutputBuildError("DeckHealthPacket requires at least one finding")


@dataclass(frozen=True)
class RecommendationCandidatePacket(_OutputBase):
    candidate_card_oracle_id: str | None = None
    candidate_card_scryfall_id: str | None = None
    candidate_card_name: str = ""
    recommendation_type: str = "investigate"
    role_tags: tuple[str, ...] = ()
    evidence_summary: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.output_type != "recommendation_candidate":
            raise RecommendationOutputBuildError("RecommendationCandidatePacket output_type must be recommendation_candidate")
        if self.candidate_card_oracle_id is not None:
            _require_text(self.candidate_card_oracle_id, "candidate_card_oracle_id")
        if self.candidate_card_scryfall_id is not None:
            _require_text(self.candidate_card_scryfall_id, "candidate_card_scryfall_id")
        object.__setattr__(self, "candidate_card_name", _validate_text(self.candidate_card_name, "candidate_card_name"))
        object.__setattr__(
            self,
            "recommendation_type",
            _normalize_allowed(self.recommendation_type, ALLOWED_RECOMMENDATION_TYPES, "recommendation_type"),
        )
        object.__setattr__(self, "role_tags", _sorted_text_tuple(self.role_tags, "role_tags"))
        object.__setattr__(self, "evidence_summary", _validate_text(self.evidence_summary, "evidence_summary"))
        if not self.candidate_card_oracle_id and not self.candidate_card_scryfall_id:
            raise RecommendationOutputBuildError("RecommendationCandidatePacket requires a card identity")
        if self.recommendation_type in {"consider_include", "consider_replace"} and self.confidence < 0.5:
            raise RecommendationOutputBuildError("consider outputs require at least medium confidence")


@dataclass(frozen=True)
class ReplacementSuggestionPacket(_OutputBase):
    replace_card_oracle_id: str | None = None
    replace_card_scryfall_id: str | None = None
    replace_card_name: str = ""
    candidate_card_oracle_id: str | None = None
    candidate_card_scryfall_id: str | None = None
    candidate_card_name: str = ""
    shared_role_tags: tuple[str, ...] = ()
    reason_summary: str = ""
    impact_summary: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.output_type != "replacement_suggestion":
            raise RecommendationOutputBuildError("ReplacementSuggestionPacket output_type must be replacement_suggestion")
        for field_name in ("replace_card_oracle_id", "replace_card_scryfall_id", "candidate_card_oracle_id", "candidate_card_scryfall_id"):
            value = getattr(self, field_name)
            if value is not None:
                _require_text(value, field_name)
        object.__setattr__(self, "replace_card_name", _validate_text(self.replace_card_name, "replace_card_name"))
        object.__setattr__(self, "candidate_card_name", _validate_text(self.candidate_card_name, "candidate_card_name"))
        object.__setattr__(self, "shared_role_tags", _sorted_text_tuple(self.shared_role_tags, "shared_role_tags"))
        object.__setattr__(self, "reason_summary", _validate_text(self.reason_summary, "reason_summary"))
        object.__setattr__(self, "impact_summary", _validate_text(self.impact_summary, "impact_summary"))
        if not self.replace_card_oracle_id and not self.replace_card_scryfall_id:
            raise RecommendationOutputBuildError("ReplacementSuggestionPacket requires replaced-card identity")
        if not self.candidate_card_oracle_id and not self.candidate_card_scryfall_id:
            raise RecommendationOutputBuildError("ReplacementSuggestionPacket requires candidate-card identity")
        if not self.shared_role_tags:
            raise RecommendationOutputBuildError("ReplacementSuggestionPacket requires shared_role_tags")


@dataclass(frozen=True)
class PackageGapPacket(_OutputBase):
    package_id: str = ""
    package_label: str = ""
    missing_role_tags: tuple[str, ...] = ()
    related_card_names: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.output_type != "package_gap":
            raise RecommendationOutputBuildError("PackageGapPacket output_type must be package_gap")
        _require_text(self.package_id, "package_id")
        object.__setattr__(self, "package_label", _validate_text(self.package_label, "package_label"))
        object.__setattr__(self, "missing_role_tags", _sorted_text_tuple(self.missing_role_tags, "missing_role_tags"))
        object.__setattr__(self, "related_card_names", _sorted_text_tuple(self.related_card_names, "related_card_names"))


@dataclass(frozen=True)
class EvidenceExplanationPacket(_OutputBase):
    explanation_label: str = ""
    supporting_summary: str = ""
    contradiction_summary: str = ""
    caveat_summary: str = ""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.output_type != "evidence_explanation":
            raise RecommendationOutputBuildError("EvidenceExplanationPacket output_type must be evidence_explanation")
        object.__setattr__(self, "explanation_label", _validate_text(self.explanation_label, "explanation_label"))
        object.__setattr__(self, "supporting_summary", _validate_text(self.supporting_summary, "supporting_summary"))
        object.__setattr__(self, "contradiction_summary", _validate_text(self.contradiction_summary, "contradiction_summary"))
        object.__setattr__(self, "caveat_summary", _validate_text(self.caveat_summary, "caveat_summary"))


@dataclass(frozen=True)
class RecommendationOutputBundle:
    bundle_id: str
    bundle_type: str
    subject: UnifiedEvidenceSubject
    deck_health_packets: tuple[DeckHealthPacket, ...] = ()
    recommendation_candidates: tuple[RecommendationCandidatePacket, ...] = ()
    replacement_suggestions: tuple[ReplacementSuggestionPacket, ...] = ()
    package_gaps: tuple[PackageGapPacket, ...] = ()
    evidence_explanations: tuple[EvidenceExplanationPacket, ...] = ()
    generated_at: str = ""
    output_version: str = "phase28b-output-packets"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.bundle_id, "bundle_id")
        object.__setattr__(self, "bundle_type", _normalize_allowed(self.bundle_type, ALLOWED_BUNDLE_TYPES, "bundle_type"))
        if not isinstance(self.subject, UnifiedEvidenceSubject):
            raise RecommendationOutputBuildError("subject must be a UnifiedEvidenceSubject")
        object.__setattr__(self, "deck_health_packets", _sort_tuple(self.deck_health_packets, "output_id", DeckHealthPacket))
        object.__setattr__(
            self, "recommendation_candidates", _sort_tuple(self.recommendation_candidates, "output_id", RecommendationCandidatePacket)
        )
        object.__setattr__(
            self, "replacement_suggestions", _sort_tuple(self.replacement_suggestions, "output_id", ReplacementSuggestionPacket)
        )
        object.__setattr__(self, "package_gaps", _sort_tuple(self.package_gaps, "output_id", PackageGapPacket))
        object.__setattr__(self, "evidence_explanations", _sort_tuple(self.evidence_explanations, "output_id", EvidenceExplanationPacket))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.output_version, "output_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_recommendation_output_bundle(self)


def build_deck_health_packet(**kwargs: Any) -> DeckHealthPacket:
    context = _build_context(kwargs["subject"], kwargs["decision_packets"], kwargs["evidence_objects"], kwargs["weight_profile"], kwargs["analysis_profile"])
    return DeckHealthPacket(
        output_id=kwargs["output_id"],
        output_type="deck_health",
        subject=kwargs["subject"],
        summary=kwargs["summary"],
        confidence=kwargs["confidence"],
        expected_impact=kwargs["expected_impact"],
        source_agreement=kwargs["source_agreement"],
        evidence_object_ids=context["evidence_object_ids"],
        decision_ids=context["decision_ids"],
        weight_profile_id=kwargs["weight_profile"].profile_id,
        weight_profile_version=kwargs["weight_profile"].profile_version,
        analysis_profile_id=kwargs["analysis_profile"].analysis_profile_id,
        analysis_profile_version=kwargs["analysis_profile"].analysis_profile_version,
        supporting_ref_ids=kwargs.get("supporting_ref_ids") or context["supporting_ref_ids"],
        contradicting_ref_ids=kwargs.get("contradicting_ref_ids", ()),
        caveat_ids=kwargs.get("caveat_ids") or context["caveat_ids"],
        speculation_level=kwargs.get("speculation_level", "none"),
        generated_at=kwargs["generated_at"],
        output_version=kwargs.get("output_version", "phase28b-output-packets"),
        metadata=kwargs.get("metadata") or {},
        findings=kwargs["findings"],
    )


def build_recommendation_candidate_packet(**kwargs: Any) -> RecommendationCandidatePacket:
    context = _build_context(kwargs["subject"], kwargs["decision_packets"], kwargs["evidence_objects"], kwargs["weight_profile"], kwargs["analysis_profile"])
    return RecommendationCandidatePacket(
        **_base_kwargs(kwargs, context, "recommendation_candidate"),
        candidate_card_oracle_id=kwargs.get("candidate_card_oracle_id"),
        candidate_card_scryfall_id=kwargs.get("candidate_card_scryfall_id"),
        candidate_card_name=kwargs["candidate_card_name"],
        recommendation_type=kwargs["recommendation_type"],
        role_tags=kwargs["role_tags"],
        evidence_summary=kwargs["evidence_summary"],
    )


def build_replacement_suggestion_packet(**kwargs: Any) -> ReplacementSuggestionPacket:
    context = _build_context(kwargs["subject"], kwargs["decision_packets"], kwargs["evidence_objects"], kwargs["weight_profile"], kwargs["analysis_profile"])
    return ReplacementSuggestionPacket(
        **_base_kwargs(kwargs, context, "replacement_suggestion"),
        replace_card_oracle_id=kwargs.get("replace_card_oracle_id"),
        replace_card_scryfall_id=kwargs.get("replace_card_scryfall_id"),
        replace_card_name=kwargs["replace_card_name"],
        candidate_card_oracle_id=kwargs.get("candidate_card_oracle_id"),
        candidate_card_scryfall_id=kwargs.get("candidate_card_scryfall_id"),
        candidate_card_name=kwargs["candidate_card_name"],
        shared_role_tags=kwargs["shared_role_tags"],
        reason_summary=kwargs["reason_summary"],
        impact_summary=kwargs["impact_summary"],
    )


def build_package_gap_packet(**kwargs: Any) -> PackageGapPacket:
    context = _build_context(kwargs["subject"], kwargs["decision_packets"], kwargs["evidence_objects"], kwargs["weight_profile"], kwargs["analysis_profile"])
    return PackageGapPacket(
        **_base_kwargs(kwargs, context, "package_gap"),
        package_id=kwargs["package_id"],
        package_label=kwargs["package_label"],
        missing_role_tags=kwargs["missing_role_tags"],
        related_card_names=kwargs["related_card_names"],
    )


def build_evidence_explanation_packet(**kwargs: Any) -> EvidenceExplanationPacket:
    context = _build_context(kwargs["subject"], kwargs["decision_packets"], kwargs["evidence_objects"], kwargs["weight_profile"], kwargs["analysis_profile"])
    return EvidenceExplanationPacket(
        **_base_kwargs(kwargs, context, "evidence_explanation"),
        explanation_label=kwargs["explanation_label"],
        supporting_summary=kwargs["supporting_summary"],
        contradiction_summary=kwargs["contradiction_summary"],
        caveat_summary=kwargs["caveat_summary"],
    )


def build_recommendation_output_bundle(
    bundle_id: str,
    bundle_type: str,
    subject: UnifiedEvidenceSubject,
    generated_at: str,
    deck_health_packets: tuple[DeckHealthPacket, ...] = (),
    recommendation_candidates: tuple[RecommendationCandidatePacket, ...] = (),
    replacement_suggestions: tuple[ReplacementSuggestionPacket, ...] = (),
    package_gaps: tuple[PackageGapPacket, ...] = (),
    evidence_explanations: tuple[EvidenceExplanationPacket, ...] = (),
    output_version: str = "phase28b-output-packets",
    metadata: dict[str, Any] | None = None,
    options: RecommendationOutputOptions | None = None,
) -> RecommendationOutputBundle:
    resolved_options = options or RecommendationOutputOptions()
    outputs_count = (
        len(deck_health_packets)
        + len(recommendation_candidates)
        + len(replacement_suggestions)
        + len(package_gaps)
        + len(evidence_explanations)
    )
    if outputs_count > resolved_options.maximum_outputs_per_bundle:
        raise RecommendationOutputBuildError("RecommendationOutputBundle exceeds maximum_outputs_per_bundle")
    return RecommendationOutputBundle(
        bundle_id=bundle_id,
        bundle_type=bundle_type,
        subject=subject,
        deck_health_packets=deck_health_packets,
        recommendation_candidates=recommendation_candidates,
        replacement_suggestions=replacement_suggestions,
        package_gaps=package_gaps,
        evidence_explanations=evidence_explanations,
        generated_at=generated_at,
        output_version=output_version or resolved_options.output_version,
        metadata=metadata or {},
    )


def validate_recommendation_output_bundle(bundle: RecommendationOutputBundle) -> RecommendationOutputBundle:
    outputs = _all_outputs(bundle)
    if not outputs:
        raise RecommendationOutputBuildError("RecommendationOutputBundle requires at least one output")
    duplicates = _duplicates([item.output_id for item in outputs])
    if duplicates:
        raise RecommendationOutputBuildError(f"duplicate output_id: {duplicates[0]}")
    for item in outputs:
        if item.subject.subject_id != bundle.subject.subject_id:
            raise RecommendationOutputBuildError("all output packets must match bundle subject")
    return bundle


def deck_health_packet_to_dict(packet: DeckHealthPacket) -> dict[str, Any]:
    payload = _base_to_dict(packet)
    payload["findings"] = [_finding_to_dict(item) for item in packet.findings]
    return payload


def recommendation_candidate_packet_to_dict(packet: RecommendationCandidatePacket) -> dict[str, Any]:
    payload = _base_to_dict(packet)
    payload.update(
        {
            "candidate_card_oracle_id": packet.candidate_card_oracle_id,
            "candidate_card_scryfall_id": packet.candidate_card_scryfall_id,
            "candidate_card_name": packet.candidate_card_name,
            "recommendation_type": packet.recommendation_type,
            "role_tags": list(packet.role_tags),
            "evidence_summary": packet.evidence_summary,
        }
    )
    return payload


def replacement_suggestion_packet_to_dict(packet: ReplacementSuggestionPacket) -> dict[str, Any]:
    payload = _base_to_dict(packet)
    payload.update(
        {
            "replace_card_oracle_id": packet.replace_card_oracle_id,
            "replace_card_scryfall_id": packet.replace_card_scryfall_id,
            "replace_card_name": packet.replace_card_name,
            "candidate_card_oracle_id": packet.candidate_card_oracle_id,
            "candidate_card_scryfall_id": packet.candidate_card_scryfall_id,
            "candidate_card_name": packet.candidate_card_name,
            "shared_role_tags": list(packet.shared_role_tags),
            "reason_summary": packet.reason_summary,
            "impact_summary": packet.impact_summary,
        }
    )
    return payload


def package_gap_packet_to_dict(packet: PackageGapPacket) -> dict[str, Any]:
    payload = _base_to_dict(packet)
    payload.update(
        {
            "package_id": packet.package_id,
            "package_label": packet.package_label,
            "missing_role_tags": list(packet.missing_role_tags),
            "related_card_names": list(packet.related_card_names),
        }
    )
    return payload


def evidence_explanation_packet_to_dict(packet: EvidenceExplanationPacket) -> dict[str, Any]:
    payload = _base_to_dict(packet)
    payload.update(
        {
            "explanation_label": packet.explanation_label,
            "supporting_summary": packet.supporting_summary,
            "contradiction_summary": packet.contradiction_summary,
            "caveat_summary": packet.caveat_summary,
        }
    )
    return payload


def recommendation_output_bundle_to_dict(bundle: RecommendationOutputBundle) -> dict[str, Any]:
    validated = validate_recommendation_output_bundle(bundle)
    return {
        "bundle_id": validated.bundle_id,
        "bundle_type": validated.bundle_type,
        "subject": _subject_to_dict(validated.subject),
        "deck_health_packets": [deck_health_packet_to_dict(item) for item in validated.deck_health_packets],
        "recommendation_candidates": [
            recommendation_candidate_packet_to_dict(item) for item in validated.recommendation_candidates
        ],
        "replacement_suggestions": [
            replacement_suggestion_packet_to_dict(item) for item in validated.replacement_suggestions
        ],
        "package_gaps": [package_gap_packet_to_dict(item) for item in validated.package_gaps],
        "evidence_explanations": [evidence_explanation_packet_to_dict(item) for item in validated.evidence_explanations],
        "generated_at": validated.generated_at,
        "output_version": validated.output_version,
        "metadata": _sorted_json_object(validated.metadata),
    }


def _base_kwargs(kwargs: dict[str, Any], context: dict[str, tuple[str, ...]], output_type: str) -> dict[str, Any]:
    return {
        "output_id": kwargs["output_id"],
        "output_type": output_type,
        "subject": kwargs["subject"],
        "summary": kwargs["summary"],
        "confidence": kwargs["confidence"],
        "expected_impact": kwargs["expected_impact"],
        "source_agreement": kwargs["source_agreement"],
        "evidence_object_ids": context["evidence_object_ids"],
        "decision_ids": context["decision_ids"],
        "weight_profile_id": kwargs["weight_profile"].profile_id,
        "weight_profile_version": kwargs["weight_profile"].profile_version,
        "analysis_profile_id": kwargs["analysis_profile"].analysis_profile_id,
        "analysis_profile_version": kwargs["analysis_profile"].analysis_profile_version,
        "supporting_ref_ids": kwargs.get("supporting_ref_ids") or context["supporting_ref_ids"],
        "contradicting_ref_ids": kwargs.get("contradicting_ref_ids", ()),
        "caveat_ids": kwargs.get("caveat_ids") or context["caveat_ids"],
        "speculation_level": kwargs.get("speculation_level", "none"),
        "generated_at": kwargs["generated_at"],
        "output_version": kwargs.get("output_version", "phase28b-output-packets"),
        "metadata": kwargs.get("metadata") or {},
    }


def _build_context(
    subject: UnifiedEvidenceSubject,
    decision_packets: tuple[DecisionPacket, ...],
    evidence_objects: tuple[UnifiedEvidenceObject, ...],
    weight_profile: WeightProfile,
    analysis_profile: AnalysisProfile,
) -> dict[str, tuple[str, ...]]:
    if not decision_packets:
        raise RecommendationOutputBuildError("output requires at least one DecisionPacket")
    if not evidence_objects:
        raise RecommendationOutputBuildError("output requires at least one UnifiedEvidenceObject")
    if not isinstance(weight_profile, WeightProfile):
        raise RecommendationOutputBuildError("weight_profile must be a WeightProfile")
    if not isinstance(analysis_profile, AnalysisProfile):
        raise RecommendationOutputBuildError("analysis_profile must be an AnalysisProfile")
    if analysis_profile.weight_profile_id != weight_profile.profile_id:
        raise RecommendationOutputBuildError("analysis_profile weight_profile_id must match weight_profile")
    if analysis_profile.weight_profile_version != weight_profile.profile_version:
        raise RecommendationOutputBuildError("analysis_profile weight_profile_version must match weight_profile")
    decision_ids: list[str] = []
    evidence_object_ids: list[str] = []
    supporting_ref_ids: list[str] = []
    caveat_ids: list[str] = []
    for packet in decision_packets:
        if not isinstance(packet, DecisionPacket):
            raise RecommendationOutputBuildError("decision_packets must contain DecisionPacket")
        if packet.subject.subject_id != subject.subject_id:
            raise RecommendationOutputBuildError("all decision packets must match output subject")
        decision_ids.append(packet.decision_id)
        supporting_ref_ids.extend(packet.supporting_ref_ids)
        caveat_ids.extend(packet.caveat_ids)
    for evidence_object in evidence_objects:
        if not isinstance(evidence_object, UnifiedEvidenceObject):
            raise RecommendationOutputBuildError("evidence_objects must contain UnifiedEvidenceObject")
        if evidence_object.subject.subject_id != subject.subject_id:
            raise RecommendationOutputBuildError("all evidence objects must match output subject")
        evidence_object_ids.append(evidence_object.evidence_object_id)
        supporting_ref_ids.extend(ref.metric_ref_id for ref in evidence_object.metric_refs)
        caveat_ids.extend(caveat.caveat_id for caveat in evidence_object.caveats)
    return {
        "decision_ids": _sorted_text_tuple(tuple(decision_ids), "decision_ids"),
        "evidence_object_ids": _sorted_text_tuple(tuple(evidence_object_ids), "evidence_object_ids"),
        "supporting_ref_ids": _sorted_text_tuple(tuple(supporting_ref_ids), "supporting_ref_ids"),
        "caveat_ids": _sorted_text_tuple(tuple(caveat_ids), "caveat_ids"),
    }


def _validate_output_quality(packet: _OutputBase) -> None:
    if not packet.decision_ids:
        raise RecommendationOutputBuildError("output requires decision_ids")
    if not packet.evidence_object_ids:
        raise RecommendationOutputBuildError("output requires evidence_object_ids")
    if packet.confidence >= 0.75 and packet.source_agreement.agreement_label not in {"strong", "mixed"}:
        raise RecommendationOutputBuildError("high confidence requires strong or mixed source agreement")
    if packet.confidence >= 0.5 and not packet.supporting_ref_ids:
        raise RecommendationOutputBuildError("medium or high confidence requires supporting_ref_ids")
    if packet.speculation_level == "high" and packet.confidence >= 0.5:
        raise RecommendationOutputBuildError("high speculation cannot pair with medium or high confidence")
    if packet.source_agreement.coverage_ratio < 0.25 and not packet.caveat_ids:
        raise RecommendationOutputBuildError("low coverage requires a visible caveat")
    if packet.source_agreement.sample_size < 3 and not packet.caveat_ids:
        raise RecommendationOutputBuildError("low sample size requires a visible caveat")


def _base_to_dict(packet: _OutputBase) -> dict[str, Any]:
    return {
        "output_id": packet.output_id,
        "output_type": packet.output_type,
        "subject": _subject_to_dict(packet.subject),
        "summary": packet.summary,
        "confidence": packet.confidence,
        "expected_impact": packet.expected_impact,
        "source_agreement": _source_agreement_to_dict(packet.source_agreement),
        "evidence_object_ids": list(packet.evidence_object_ids),
        "decision_ids": list(packet.decision_ids),
        "weight_profile_id": packet.weight_profile_id,
        "weight_profile_version": packet.weight_profile_version,
        "analysis_profile_id": packet.analysis_profile_id,
        "analysis_profile_version": packet.analysis_profile_version,
        "supporting_ref_ids": list(packet.supporting_ref_ids),
        "contradicting_ref_ids": list(packet.contradicting_ref_ids),
        "caveat_ids": list(packet.caveat_ids),
        "speculation_level": packet.speculation_level,
        "generated_at": packet.generated_at,
        "output_version": packet.output_version,
        "metadata": _sorted_json_object(packet.metadata),
    }


def _finding_to_dict(finding: DeckHealthFinding) -> dict[str, Any]:
    return {
        "finding_id": finding.finding_id,
        "health_category": finding.health_category,
        "severity": finding.severity,
        "finding_label": finding.finding_label,
        "finding_summary": finding.finding_summary,
        "affected_cards": list(finding.affected_cards),
        "affected_roles": list(finding.affected_roles),
        "supporting_ref_ids": list(finding.supporting_ref_ids),
        "contradicting_ref_ids": list(finding.contradicting_ref_ids),
        "caveat_ids": list(finding.caveat_ids),
        "metadata": _sorted_json_object(finding.metadata),
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


def _all_outputs(bundle: RecommendationOutputBundle) -> tuple[_OutputBase, ...]:
    return (
        *bundle.deck_health_packets,
        *bundle.recommendation_candidates,
        *bundle.replacement_suggestions,
        *bundle.package_gaps,
        *bundle.evidence_explanations,
    )


def _sort_tuple(items: tuple[Any, ...], id_field: str, item_type: type) -> tuple[Any, ...]:
    for item in items:
        if not isinstance(item, item_type):
            raise RecommendationOutputBuildError(f"{id_field} collection contains invalid item")
    return tuple(sorted(items, key=lambda item: getattr(item, id_field)))


def _sorted_text_tuple(items: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(items, tuple):
        raise RecommendationOutputBuildError(f"{field_name} must be a tuple")
    return tuple(sorted({_require_text(item, field_name) for item in items}))


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecommendationOutputBuildError(f"{field_name} is required")
    return value.strip()


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).lower()
    if normalized not in allowed:
        raise RecommendationOutputBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_ratio(value: float, field_name: str) -> None:
    if not isinstance(value, int | float):
        raise RecommendationOutputBuildError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise RecommendationOutputBuildError(f"{field_name} must be between 0 and 1")


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    normalized = " ".join(text.lower().split())
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment in normalized:
            raise RecommendationOutputBuildError(f"forbidden strategic language in {field_name}")
    return text


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise RecommendationOutputBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise RecommendationOutputBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise RecommendationOutputBuildError(f"{path} contains forbidden metadata key: {key}")
            if normalized_key in STACK_TRACE_KEYS:
                raise RecommendationOutputBuildError(f"{path} contains forbidden stack trace key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise RecommendationOutputBuildError(f"{path} must be JSON-compatible")


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
