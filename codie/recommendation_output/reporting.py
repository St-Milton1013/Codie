"""Reporting documents for recommendation output packets."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from .models import RecommendationOutputBuildError, RecommendationOutputBundle, recommendation_output_bundle_to_dict


ALLOWED_SECTION_TYPES = frozenset(
    {
        "deck_health",
        "recommendation_candidate",
        "replacement_suggestion",
        "package_gap",
        "evidence_explanation",
        "caveats",
        "contradictions",
        "provenance",
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


@dataclass(frozen=True)
class RecommendationReportOptions:
    report_version: str = "phase29b-report-document"
    include_provenance_section: bool = True

    def __post_init__(self) -> None:
        _require_text(self.report_version, "report_version")
        if not isinstance(self.include_provenance_section, bool):
            raise RecommendationOutputBuildError("include_provenance_section must be a bool")


@dataclass(frozen=True)
class RecommendationReportSection:
    section_id: str
    section_type: str
    title: str
    summary: str
    source_output_ids: tuple[str, ...]
    decision_ids: tuple[str, ...]
    evidence_object_ids: tuple[str, ...]
    weight_profile_refs: tuple[str, ...]
    analysis_profile_refs: tuple[str, ...]
    confidence: float | None
    expected_impact: str | None
    source_agreement: dict[str, Any] | None
    caveats: tuple[str, ...]
    contradictions: tuple[str, ...]
    speculation_level: str | None
    body_lines: tuple[str, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.section_id, "section_id")
        object.__setattr__(self, "section_type", _normalize_allowed(self.section_type, ALLOWED_SECTION_TYPES, "section_type"))
        object.__setattr__(self, "title", _validate_text(self.title, "title"))
        object.__setattr__(self, "summary", _validate_text(self.summary, "summary"))
        for field_name in (
            "source_output_ids",
            "decision_ids",
            "evidence_object_ids",
            "weight_profile_refs",
            "analysis_profile_refs",
            "caveats",
            "contradictions",
            "body_lines",
        ):
            object.__setattr__(self, field_name, _sorted_text_tuple(getattr(self, field_name), field_name))
        if self.confidence is not None:
            _validate_ratio(self.confidence, "confidence")
        if self.expected_impact is not None:
            object.__setattr__(self, "expected_impact", _validate_text(self.expected_impact, "expected_impact"))
        if self.source_agreement is not None:
            object.__setattr__(self, "source_agreement", _validate_metadata(self.source_agreement))
        if self.speculation_level is not None:
            object.__setattr__(self, "speculation_level", _validate_text(self.speculation_level, "speculation_level"))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class RecommendationReportDocument:
    report_id: str
    source_bundle_id: str
    bundle_type: str
    subject: dict[str, Any]
    generated_at: str
    report_version: str
    output_version: str
    sections: tuple[RecommendationReportSection, ...]
    caveat_count: int
    contradiction_count: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.report_id, "report_id")
        _require_text(self.source_bundle_id, "source_bundle_id")
        _require_text(self.bundle_type, "bundle_type")
        object.__setattr__(self, "subject", _validate_metadata(self.subject))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.report_version, "report_version")
        _require_text(self.output_version, "output_version")
        object.__setattr__(self, "sections", _sort_tuple(self.sections, "section_id", RecommendationReportSection))
        if not self.sections:
            raise RecommendationOutputBuildError("RecommendationReportDocument requires at least one section")
        _validate_non_negative_int(self.caveat_count, "caveat_count")
        _validate_non_negative_int(self.contradiction_count, "contradiction_count")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_recommendation_report_document(self)


def build_recommendation_report_document(
    bundle: RecommendationOutputBundle | dict[str, Any],
    report_id: str,
    generated_at: str,
    options: RecommendationReportOptions | None = None,
    metadata: dict[str, Any] | None = None,
) -> RecommendationReportDocument:
    """Build one deterministic in-memory report document from an output bundle."""

    resolved_options = options or RecommendationReportOptions()
    payload = recommendation_output_bundle_to_dict(bundle) if isinstance(bundle, RecommendationOutputBundle) else _validate_bundle_dict(bundle)
    sections = _sections_from_bundle_payload(payload)
    if resolved_options.include_provenance_section:
        sections.append(_provenance_section(payload))
    caveat_count = sum(len(section.caveats) for section in sections)
    contradiction_count = sum(len(section.contradictions) for section in sections)
    return RecommendationReportDocument(
        report_id=report_id,
        source_bundle_id=payload["bundle_id"],
        bundle_type=payload["bundle_type"],
        subject=payload["subject"],
        generated_at=generated_at,
        report_version=resolved_options.report_version,
        output_version=payload["output_version"],
        sections=tuple(sections),
        caveat_count=caveat_count,
        contradiction_count=contradiction_count,
        metadata=metadata or {},
    )


def validate_recommendation_report_document(document: RecommendationReportDocument) -> RecommendationReportDocument:
    section_ids = [section.section_id for section in document.sections]
    duplicates = _duplicates(section_ids)
    if duplicates:
        raise RecommendationOutputBuildError(f"duplicate section_id: {duplicates[0]}")
    return document


def recommendation_report_document_to_dict(document: RecommendationReportDocument) -> dict[str, Any]:
    """Serialize a report document deterministically."""

    validated = validate_recommendation_report_document(document)
    return {
        "report_id": validated.report_id,
        "source_bundle_id": validated.source_bundle_id,
        "bundle_type": validated.bundle_type,
        "subject": _sorted_json_object(validated.subject),
        "generated_at": validated.generated_at,
        "report_version": validated.report_version,
        "output_version": validated.output_version,
        "sections": [_section_to_dict(section) for section in validated.sections],
        "caveat_count": validated.caveat_count,
        "contradiction_count": validated.contradiction_count,
        "metadata": _sorted_json_object(validated.metadata),
    }


def recommendation_report_document_to_markdown(document: RecommendationReportDocument) -> str:
    """Render a report document as evidence-first Markdown."""

    payload = recommendation_report_document_to_dict(document)
    subject = payload["subject"]
    lines = [
        "# Recommendation Output Report",
        "",
        f"- Report ID: `{payload['report_id']}`",
        f"- Source bundle ID: `{payload['source_bundle_id']}`",
        f"- Subject: {_escape_markdown_text(subject.get('display_name') or subject.get('subject_key') or subject.get('subject_id'))}",
        f"- Generated at: {payload['generated_at']}",
        f"- Report version: `{payload['report_version']}`",
        f"- Output version: `{payload['output_version']}`",
        f"- Caveat count: {payload['caveat_count']}",
        f"- Contradiction count: {payload['contradiction_count']}",
        "",
    ]
    for section in payload["sections"]:
        lines.extend(_section_markdown(section))
    return "\n".join(lines).rstrip() + "\n"


def _sections_from_bundle_payload(payload: dict[str, Any]) -> list[RecommendationReportSection]:
    sections: list[RecommendationReportSection] = []
    for key, section_type, title in (
        ("deck_health_packets", "deck_health", "Deck Health"),
        ("recommendation_candidates", "recommendation_candidate", "Candidate Packet"),
        ("replacement_suggestions", "replacement_suggestion", "Replacement Suggestion"),
        ("package_gaps", "package_gap", "Package Gap"),
        ("evidence_explanations", "evidence_explanation", "Evidence Explanation"),
    ):
        for item in payload[key]:
            sections.append(_section_from_output(item, section_type, title))
    if not sections:
        raise RecommendationOutputBuildError("RecommendationOutputBundle payload has no reportable outputs")
    return sections


def _section_from_output(item: dict[str, Any], section_type: str, title: str) -> RecommendationReportSection:
    recommendation_type = item.get("recommendation_type")
    non_action = recommendation_type in {"monitor", "investigate", "no_action"}
    caveats = tuple(item.get("caveat_ids", ()))
    contradictions = tuple(item.get("contradicting_ref_ids", ()))
    body_lines = [
        f"Summary: {item['summary']}",
        f"Confidence: {item['confidence']}",
        f"Expected impact: {item['expected_impact']}",
        f"Source agreement: {item['source_agreement']['agreement_label']}",
        f"Speculation level: {item['speculation_level']}",
        f"Weight profile: {item['weight_profile_id']}@{item['weight_profile_version']}",
        f"Analysis profile: {item['analysis_profile_id']}@{item['analysis_profile_version']}",
    ]
    if recommendation_type:
        body_lines.append(f"Recommendation type: {recommendation_type}")
    if non_action:
        body_lines.append("Non-action output: review only.")
    if item.get("metadata", {}).get("simulator_evidence_only"):
        body_lines.append("Simulator comparison is model-derived and not tournament evidence.")
    if item.get("metadata", {}).get("primer_context_explanatory_only"):
        body_lines.append("Primer context is explanatory only.")
    if caveats:
        body_lines.append("Caveats remain visible.")
    if contradictions:
        body_lines.append("Contradictions remain visible.")
    return RecommendationReportSection(
        section_id=f"section:{item['output_id']}",
        section_type=section_type,
        title=f"{title}: {item['output_id']}",
        summary=item["summary"],
        source_output_ids=(item["output_id"],),
        decision_ids=tuple(item["decision_ids"]),
        evidence_object_ids=tuple(item["evidence_object_ids"]),
        weight_profile_refs=(f"{item['weight_profile_id']}@{item['weight_profile_version']}",),
        analysis_profile_refs=(f"{item['analysis_profile_id']}@{item['analysis_profile_version']}",),
        confidence=item["confidence"],
        expected_impact=item["expected_impact"],
        source_agreement=item["source_agreement"],
        caveats=caveats,
        contradictions=contradictions,
        speculation_level=item["speculation_level"],
        body_lines=tuple(body_lines),
        metadata={"non_action": non_action, "source_output_type": item["output_type"]},
    )


def _provenance_section(payload: dict[str, Any]) -> RecommendationReportSection:
    output_ids: list[str] = []
    decision_ids: list[str] = []
    evidence_object_ids: list[str] = []
    weight_refs: list[str] = []
    analysis_refs: list[str] = []
    for key in (
        "deck_health_packets",
        "recommendation_candidates",
        "replacement_suggestions",
        "package_gaps",
        "evidence_explanations",
    ):
        for item in payload[key]:
            output_ids.append(item["output_id"])
            decision_ids.extend(item["decision_ids"])
            evidence_object_ids.extend(item["evidence_object_ids"])
            weight_refs.append(f"{item['weight_profile_id']}@{item['weight_profile_version']}")
            analysis_refs.append(f"{item['analysis_profile_id']}@{item['analysis_profile_version']}")
    return RecommendationReportSection(
        section_id="section:provenance",
        section_type="provenance",
        title="Provenance",
        summary="Packet provenance and version references.",
        source_output_ids=tuple(output_ids),
        decision_ids=tuple(decision_ids),
        evidence_object_ids=tuple(evidence_object_ids),
        weight_profile_refs=tuple(weight_refs),
        analysis_profile_refs=tuple(analysis_refs),
        confidence=None,
        expected_impact=None,
        source_agreement=None,
        caveats=(),
        contradictions=(),
        speculation_level=None,
        body_lines=(
            f"Source bundle: {payload['bundle_id']}",
            f"Output version: {payload['output_version']}",
            "All recommendations remain packet-derived and evidence-cited.",
        ),
        metadata={"provenance_only": True},
    )


def _section_to_dict(section: RecommendationReportSection) -> dict[str, Any]:
    return {
        "section_id": section.section_id,
        "section_type": section.section_type,
        "title": section.title,
        "summary": section.summary,
        "source_output_ids": list(section.source_output_ids),
        "decision_ids": list(section.decision_ids),
        "evidence_object_ids": list(section.evidence_object_ids),
        "weight_profile_refs": list(section.weight_profile_refs),
        "analysis_profile_refs": list(section.analysis_profile_refs),
        "confidence": section.confidence,
        "expected_impact": section.expected_impact,
        "source_agreement": None if section.source_agreement is None else _sorted_json_object(section.source_agreement),
        "caveats": list(section.caveats),
        "contradictions": list(section.contradictions),
        "speculation_level": section.speculation_level,
        "body_lines": list(section.body_lines),
        "metadata": _sorted_json_object(section.metadata),
    }


def _section_markdown(section: dict[str, Any]) -> list[str]:
    lines = [
        f"## {_escape_markdown_text(section['title'])}",
        "",
        f"- Section type: `{section['section_type']}`",
        f"- Confidence: `{section['confidence']}`",
        f"- Expected impact: `{section['expected_impact']}`",
        f"- Speculation level: `{section['speculation_level']}`",
        f"- Source agreement: `{_agreement_label(section['source_agreement'])}`",
        f"- Decision IDs: `{', '.join(section['decision_ids'])}`",
        f"- UnifiedEvidenceObject IDs: `{', '.join(section['evidence_object_ids'])}`",
        f"- Weight profiles: `{', '.join(section['weight_profile_refs'])}`",
        f"- Analysis profiles: `{', '.join(section['analysis_profile_refs'])}`",
        f"- Caveats: `{', '.join(section['caveats'])}`",
        f"- Contradictions: `{', '.join(section['contradictions'])}`",
        "",
        "| Detail | Value |",
        "| --- | --- |",
    ]
    for line in section["body_lines"]:
        label, _, value = line.partition(":")
        lines.append(f"| {_escape_table(label)} | {_escape_table(value.strip() or line)} |")
    lines.append("")
    return lines


def _agreement_label(source_agreement: dict[str, Any] | None) -> str:
    if source_agreement is None:
        return "none"
    return str(source_agreement.get("agreement_label", "unknown"))


def _validate_bundle_dict(value: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RecommendationOutputBuildError("bundle must be a RecommendationOutputBundle or dict")
    required = (
        "bundle_id",
        "bundle_type",
        "subject",
        "deck_health_packets",
        "recommendation_candidates",
        "replacement_suggestions",
        "package_gaps",
        "evidence_explanations",
        "generated_at",
        "output_version",
    )
    for key in required:
        if key not in value:
            raise RecommendationOutputBuildError(f"bundle payload missing required key: {key}")
    return _validate_metadata(value)


def _escape_table(value: str) -> str:
    return str(value).replace("|", "\\|")


def _escape_markdown_text(value: Any) -> str:
    return str(value).replace("|", "\\|")


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


def _validate_non_negative_int(value: int, field_name: str) -> None:
    if not isinstance(value, int) or value < 0:
        raise RecommendationOutputBuildError(f"{field_name} must be a non-negative integer")


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
