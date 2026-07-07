"""Pure chat answer building for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.evidence_graph import EvidenceGraph
from codie.intelligence.evidence_inputs import EvidenceInputRecord
from codie.intelligence.query_planner import (
    ALLOWED_PRIVACY_SCOPES,
    ALLOWED_QUESTION_CLASSES,
    ChatEvidenceNeed,
    ChatQueryPlan,
)
from codie.intelligence.source_conflicts import SourceConflictReport
from codie.intelligence.unsupported_cards import UnsupportedCardQueue


ALLOWED_SECTION_TYPES = frozenset(
    {
        "summary",
        "evidence",
        "comparison",
        "conflict",
        "unsupported_cards",
        "simulation",
        "tag_graph",
        "missing_evidence",
        "caveat",
        "unknown",
    }
)

ALLOWED_CITATION_SOURCE_TYPES = frozenset(
    {
        "evidence_input_record",
        "evidence_graph_node",
        "evidence_graph_edge",
        "source_conflict",
        "unsupported_card",
        "deck_memory",
        "saved_analysis",
        "simulation_review",
        "frequency_pool",
        "tag_graph",
        "manual_note",
    }
)

ALLOWED_CAVEAT_TYPES = frozenset(
    {
        "low_evidence",
        "missing_evidence",
        "unsupported_card",
        "source_conflict",
        "privacy_scope",
        "unknown_question",
        "unavailable_input",
        "low_confidence",
        "manual_review_required",
    }
)

ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})

NEED_TYPE_TO_RECORD_TYPE = {
    "evidence_input_records": None,
    "evidence_graph": None,
    "deck_memory": "deck_memory_summary",
    "saved_analysis": "saved_analysis_summary",
    "source_conflicts": "source_conflict",
    "unsupported_cards": "unsupported_card",
    "simulation_review_summary": "simulation_review_summary",
    "primer_metadata": "primer_metadata",
    "combo_evidence": "combo_evidence",
    "innovation_signal": "innovation_signal",
    "frequency_pool": None,
    "tag_graph": None,
    "manual_note": "manual_note",
}

PLAN_CAVEAT_TYPE_MAP = {
    "unknown_question": "unknown_question",
    "privacy_scope_not_allowed": "privacy_scope",
}

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


class ChatAnswerBuildError(ValueError):
    """Raised when a chat answer cannot be built safely."""


@dataclass(frozen=True)
class ChatAnswerCitation:
    citation_id: str
    source_type: str
    source_id: str
    record_type: str
    generated_at: str
    source_label: str | None = None
    source_url: str | None = None
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.citation_id, "citation_id")
        object.__setattr__(self, "source_type", _normalize_allowed(self.source_type, ALLOWED_CITATION_SOURCE_TYPES, "source_type"))
        _require_text(self.source_id, "source_id")
        _require_text(self.record_type, "record_type")
        _require_text(self.generated_at, "generated_at")
        if self.source_label is not None:
            object.__setattr__(self, "source_label", _validate_text(self.source_label, "source_label"))
        if self.source_url is not None:
            _validate_text(self.source_url, "source_url")
        _validate_confidence(self.confidence, "confidence")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatAnswerCaveat:
    caveat_id: str
    caveat_type: str
    message: str
    severity: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.caveat_id, "caveat_id")
        object.__setattr__(self, "caveat_type", _normalize_allowed(self.caveat_type, ALLOWED_CAVEAT_TYPES, "caveat_type"))
        object.__setattr__(self, "message", _validate_text(self.message, "message"))
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatAnswerMissingEvidence:
    missing_evidence_id: str
    need_id: str
    need_type: str
    reason: str
    required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.missing_evidence_id, "missing_evidence_id")
        _require_text(self.need_id, "need_id")
        _require_text(self.need_type, "need_type")
        object.__setattr__(self, "reason", _validate_text(self.reason, "reason"))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatAnswerSection:
    section_id: str
    section_type: str
    title: str
    statements: tuple[str, ...]
    citation_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    missing_evidence_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.section_id, "section_id")
        object.__setattr__(self, "section_type", _normalize_allowed(self.section_type, ALLOWED_SECTION_TYPES, "section_type"))
        object.__setattr__(self, "title", _validate_text(self.title, "title"))
        statements = tuple(_validate_text(statement, "statement") for statement in self.statements)
        if not statements:
            raise ChatAnswerBuildError("section requires at least one statement")
        object.__setattr__(self, "statements", statements)
        object.__setattr__(self, "citation_ids", tuple(sorted(_require_text(item, "citation_id") for item in self.citation_ids)))
        object.__setattr__(self, "caveat_ids", tuple(sorted(_require_text(item, "caveat_id") for item in self.caveat_ids)))
        object.__setattr__(self, "missing_evidence_ids", tuple(sorted(_require_text(item, "missing_evidence_id") for item in self.missing_evidence_ids)))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        if _is_factual_section(self) and not self.citation_ids and not self.missing_evidence_ids:
            raise ChatAnswerBuildError("factual sections require citations or missing_evidence")


@dataclass(frozen=True)
class ChatAnswerInput:
    answer_input_id: str
    plan: ChatQueryPlan
    generated_at: str
    evidence_records: tuple[EvidenceInputRecord, ...] = ()
    evidence_graph: EvidenceGraph | None = None
    source_conflict_report: SourceConflictReport | None = None
    unsupported_card_queue: UnsupportedCardQueue | None = None
    context_summaries: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.answer_input_id, "answer_input_id")
        if not isinstance(self.plan, ChatQueryPlan):
            raise ChatAnswerBuildError("plan must be a ChatQueryPlan")
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "evidence_records", tuple(sorted(self.evidence_records, key=lambda item: item.record_id)))
        if self.evidence_graph is not None and not isinstance(self.evidence_graph, EvidenceGraph):
            raise ChatAnswerBuildError("evidence_graph must be an EvidenceGraph")
        if self.source_conflict_report is not None and not isinstance(self.source_conflict_report, SourceConflictReport):
            raise ChatAnswerBuildError("source_conflict_report must be a SourceConflictReport")
        if self.unsupported_card_queue is not None and not isinstance(self.unsupported_card_queue, UnsupportedCardQueue):
            raise ChatAnswerBuildError("unsupported_card_queue must be an UnsupportedCardQueue")
        object.__setattr__(self, "context_summaries", _validate_metadata(self.context_summaries))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatAnswer:
    answer_id: str
    request_id: str
    plan_id: str
    answer_mode: str
    sections: tuple[ChatAnswerSection, ...]
    citations: tuple[ChatAnswerCitation, ...] = ()
    caveats: tuple[ChatAnswerCaveat, ...] = ()
    blockers: tuple[dict[str, Any], ...] = ()
    missing_evidence: tuple[ChatAnswerMissingEvidence, ...] = ()
    privacy_scope: str = "public"
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.answer_id, "answer_id")
        _require_text(self.request_id, "request_id")
        _require_text(self.plan_id, "plan_id")
        object.__setattr__(self, "answer_mode", _normalize_allowed(self.answer_mode, ALLOWED_QUESTION_CLASSES, "answer_mode"))
        object.__setattr__(self, "sections", tuple(sorted(self.sections, key=lambda item: item.section_id)))
        if not self.sections:
            raise ChatAnswerBuildError("answer requires at least one section")
        object.__setattr__(self, "citations", tuple(sorted(self.citations, key=lambda item: item.citation_id)))
        object.__setattr__(self, "caveats", tuple(sorted(self.caveats, key=lambda item: item.caveat_id)))
        object.__setattr__(self, "missing_evidence", tuple(sorted(self.missing_evidence, key=lambda item: item.missing_evidence_id)))
        object.__setattr__(self, "blockers", tuple(_validate_metadata(dict(item)) for item in self.blockers))
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _validate_answer_links(self)


@dataclass(frozen=True)
class ChatAnswerBuilderOptions:
    maximum_sections: int = 8
    maximum_citations: int = 24
    maximum_statements_per_section: int = 8
    require_citations_for_factual_sections: bool = True
    allow_unknown_without_evidence: bool = True

    def __post_init__(self) -> None:
        if self.maximum_sections < 1:
            raise ChatAnswerBuildError("maximum_sections must be at least 1")
        if self.maximum_citations < 1:
            raise ChatAnswerBuildError("maximum_citations must be at least 1")
        if self.maximum_statements_per_section < 1:
            raise ChatAnswerBuildError("maximum_statements_per_section must be at least 1")


def build_chat_answer(
    answer_input: ChatAnswerInput,
    options: ChatAnswerBuilderOptions | None = None,
) -> ChatAnswer:
    """Build one deterministic structured answer from sanitized inputs."""

    resolved_options = options or ChatAnswerBuilderOptions()
    plan = answer_input.plan
    citations = _citations_from_input(answer_input)
    blockers = tuple(_validate_metadata(dict(blocker)) for blocker in plan.blockers)
    missing_evidence = _missing_evidence_for_plan(answer_input)
    caveats = _caveats_from_plan(answer_input) + _caveats_from_sanitized_inputs(answer_input) + _caveats_from_missing_evidence(missing_evidence)
    sections = _sections_for_answer(answer_input, citations, caveats, missing_evidence)

    if len(sections) > resolved_options.maximum_sections:
        raise ChatAnswerBuildError("too many answer sections")
    if len(citations) > resolved_options.maximum_citations:
        raise ChatAnswerBuildError("too many citations")
    for section in sections:
        if len(section.statements) > resolved_options.maximum_statements_per_section:
            raise ChatAnswerBuildError("too many statements in section")
        if resolved_options.require_citations_for_factual_sections and _is_factual_section(section):
            if not section.citation_ids and not section.missing_evidence_ids:
                raise ChatAnswerBuildError("factual sections require citations or missing_evidence")
    if plan.question_class == "unknown" and not resolved_options.allow_unknown_without_evidence and not citations:
        raise ChatAnswerBuildError("unknown answers without evidence are disabled")

    return ChatAnswer(
        answer_id=f"chat-answer:{plan.request_id}",
        request_id=plan.request_id,
        plan_id=plan.plan_id,
        answer_mode=plan.question_class,
        sections=sections,
        citations=citations,
        caveats=caveats,
        blockers=blockers,
        missing_evidence=missing_evidence,
        privacy_scope=_answer_privacy_scope(plan.evidence_needs),
        generated_at=answer_input.generated_at,
        metadata={
            "answer_input_id": answer_input.answer_input_id,
            "evidence_record_count": len(answer_input.evidence_records),
        },
    )


def chat_answer_to_dict(answer: ChatAnswer) -> dict[str, Any]:
    """Serialize one chat answer deterministically."""

    return {
        "answer_id": answer.answer_id,
        "request_id": answer.request_id,
        "plan_id": answer.plan_id,
        "answer_mode": answer.answer_mode,
        "sections": [_section_to_dict(section) for section in answer.sections],
        "citations": [_citation_to_dict(citation) for citation in answer.citations],
        "caveats": [_answer_caveat_to_dict(caveat) for caveat in answer.caveats],
        "blockers": [_sorted_json_object(blocker) for blocker in answer.blockers],
        "missing_evidence": [_missing_evidence_to_dict(item) for item in answer.missing_evidence],
        "privacy_scope": answer.privacy_scope,
        "generated_at": answer.generated_at,
        "metadata": _sorted_json_object(answer.metadata),
    }


def _citations_from_input(answer_input: ChatAnswerInput) -> tuple[ChatAnswerCitation, ...]:
    citations: list[ChatAnswerCitation] = []
    for record in answer_input.evidence_records:
        source_type = _citation_source_type_for_record(record.record_type)
        citations.append(
            ChatAnswerCitation(
                citation_id=f"citation:{record.record_id}",
                source_type=source_type,
                source_id=record.record_id,
                source_label=record.label,
                source_url=_record_source_url(record),
                record_type=record.record_type,
                confidence=record.confidence,
                generated_at=_record_generated_at(record, answer_input.generated_at),
                metadata={"privacy_scope": record.privacy_scope},
            )
        )
    if answer_input.evidence_graph is not None:
        for node in answer_input.evidence_graph.nodes:
            citations.append(
                ChatAnswerCitation(
                    citation_id=f"citation:{node.node_id}",
                    source_type="evidence_graph_node",
                    source_id=node.node_id,
                    source_label=node.label,
                    source_url=None,
                    record_type=node.node_type,
                    confidence=node.confidence,
                    generated_at=answer_input.evidence_graph.generated_at,
                    metadata={"privacy_scope": node.privacy_scope},
                )
            )
    for key in sorted(answer_input.context_summaries):
        if key in {"frequency_pool", "tag_graph"}:
            citations.append(
                ChatAnswerCitation(
                    citation_id=f"citation:context:{key}",
                    source_type=key,
                    source_id=f"context:{key}",
                    source_label=key.replace("_", " ").title(),
                    source_url=None,
                    record_type=key,
                    confidence=1.0,
                    generated_at=answer_input.generated_at,
                    metadata={"context_summary": key},
                )
            )
    return tuple(sorted(citations, key=lambda item: item.citation_id))


def _caveats_from_plan(answer_input: ChatAnswerInput) -> tuple[ChatAnswerCaveat, ...]:
    caveats: list[ChatAnswerCaveat] = []
    for index, caveat in enumerate(answer_input.plan.caveats):
        caveat_type = str(caveat.get("caveat_type", "unavailable_input"))
        caveats.append(
            ChatAnswerCaveat(
                caveat_id=f"caveat:plan:{index}",
                caveat_type=PLAN_CAVEAT_TYPE_MAP.get(caveat_type, "unavailable_input"),
                message=str(caveat.get("message", "Plan caveat is present.")),
                severity=str(caveat.get("severity", "warning")),
                metadata={"source": "chat_query_plan", "original_caveat_type": caveat_type},
            )
        )
    return tuple(caveats)


def _caveats_from_sanitized_inputs(answer_input: ChatAnswerInput) -> tuple[ChatAnswerCaveat, ...]:
    caveats: list[ChatAnswerCaveat] = []
    for record in answer_input.evidence_records:
        for index, caveat in enumerate(record.caveats):
            caveats.append(
                ChatAnswerCaveat(
                    caveat_id=f"caveat:record:{record.record_id}:{index}",
                    caveat_type=_input_caveat_type(str(caveat.get("caveat_type", "unavailable_input"))),
                    message=str(caveat.get("message", f"Evidence record {record.record_id} has a caveat.")),
                    severity=str(caveat.get("severity", "warning")),
                    metadata={"record_id": record.record_id},
                )
            )
    if answer_input.source_conflict_report is not None:
        caveats.append(
            ChatAnswerCaveat(
                caveat_id=f"caveat:source-conflict:{answer_input.source_conflict_report.report_id}",
                caveat_type="source_conflict",
                message="Source conflict report is present and requires visibility.",
                severity="warning",
                metadata={"report_id": answer_input.source_conflict_report.report_id},
            )
        )
    if answer_input.unsupported_card_queue is not None:
        caveats.append(
            ChatAnswerCaveat(
                caveat_id=f"caveat:unsupported-card:{answer_input.unsupported_card_queue.queue_id}",
                caveat_type="unsupported_card",
                message="Unsupported relevant card queue is present and requires visibility.",
                severity="warning",
                metadata={"queue_id": answer_input.unsupported_card_queue.queue_id},
            )
        )
    return tuple(sorted(caveats, key=lambda item: item.caveat_id))


def _missing_evidence_for_plan(answer_input: ChatAnswerInput) -> tuple[ChatAnswerMissingEvidence, ...]:
    missing: list[ChatAnswerMissingEvidence] = []
    for need in answer_input.plan.evidence_needs:
        if not need.required:
            if not _need_satisfied(answer_input, need):
                missing.append(_missing_from_need(need, "Optional evidence was unavailable."))
            continue
        if not _need_satisfied(answer_input, need):
            missing.append(_missing_from_need(need, "Required evidence was unavailable."))
    return tuple(sorted(missing, key=lambda item: item.missing_evidence_id))


def _caveats_from_missing_evidence(
    missing_evidence: tuple[ChatAnswerMissingEvidence, ...],
) -> tuple[ChatAnswerCaveat, ...]:
    caveats: list[ChatAnswerCaveat] = []
    for item in missing_evidence:
        caveats.append(
            ChatAnswerCaveat(
                caveat_id=f"caveat:{item.missing_evidence_id}",
                caveat_type="missing_evidence",
                message=item.reason,
                severity="warning" if item.required else "info",
                metadata={"need_id": item.need_id, "need_type": item.need_type},
            )
        )
    return tuple(caveats)


def _sections_for_answer(
    answer_input: ChatAnswerInput,
    citations: tuple[ChatAnswerCitation, ...],
    caveats: tuple[ChatAnswerCaveat, ...],
    missing_evidence: tuple[ChatAnswerMissingEvidence, ...],
) -> tuple[ChatAnswerSection, ...]:
    plan = answer_input.plan
    if plan.question_class == "unknown":
        caveat_ids = tuple(caveat.caveat_id for caveat in caveats if caveat.caveat_type == "unknown_question")
        if not caveat_ids:
            caveat_ids = ("caveat:unknown",)
            caveats = caveats + (
                ChatAnswerCaveat(
                    caveat_id="caveat:unknown",
                    caveat_type="unknown_question",
                    message="The question could not be mapped to a supported answer mode.",
                    severity="warning",
                ),
            )
        return (
            ChatAnswerSection(
                section_id="section:unknown",
                section_type="unknown",
                title="Unknown Question",
                statements=("No supported evidence-backed answer mode was available for this question.",),
                caveat_ids=caveat_ids,
            ),
        )

    citation_ids = tuple(citation.citation_id for citation in citations)
    missing_ids = tuple(item.missing_evidence_id for item in missing_evidence)
    if citation_ids:
        evidence_count = len(answer_input.evidence_records)
        statements = (
            f"{plan.question_class} answer uses {evidence_count} sanitized evidence record(s).",
            "Citations identify the evidence used for each factual section.",
        )
        section = ChatAnswerSection(
            section_id=f"section:{plan.question_class}:evidence",
            section_type=_section_type_for_question_class(plan.question_class),
            title=_title_for_question_class(plan.question_class),
            statements=statements,
            citation_ids=citation_ids,
            caveat_ids=tuple(caveat.caveat_id for caveat in caveats),
            missing_evidence_ids=missing_ids,
        )
    else:
        section = ChatAnswerSection(
            section_id=f"section:{plan.question_class}:missing-evidence",
            section_type="missing_evidence",
            title="Missing Evidence",
            statements=("No matching sanitized evidence was available for this question.",),
            caveat_ids=tuple(caveat.caveat_id for caveat in caveats),
            missing_evidence_ids=missing_ids,
        )
    return (section,)


def _missing_from_need(need: ChatEvidenceNeed, reason: str) -> ChatAnswerMissingEvidence:
    return ChatAnswerMissingEvidence(
        missing_evidence_id=f"missing:{need.need_id}",
        need_id=need.need_id,
        need_type=need.need_type,
        reason=reason,
        required=need.required,
        metadata={"privacy_scope": need.privacy_scope},
    )


def _need_satisfied(answer_input: ChatAnswerInput, need: ChatEvidenceNeed) -> bool:
    if need.need_type == "evidence_graph":
        return answer_input.evidence_graph is not None or bool(answer_input.evidence_records)
    if need.need_type == "evidence_input_records":
        return bool(answer_input.evidence_records)
    if need.need_type == "source_conflicts":
        return answer_input.source_conflict_report is not None or _has_record_type(answer_input, "source_conflict")
    if need.need_type == "unsupported_cards":
        return answer_input.unsupported_card_queue is not None or _has_record_type(answer_input, "unsupported_card")
    if need.need_type == "frequency_pool":
        return "frequency_pool" in answer_input.context_summaries
    if need.need_type == "tag_graph":
        return "tag_graph" in answer_input.context_summaries or _has_record_type(answer_input, "manual_note")
    mapped_record_type = NEED_TYPE_TO_RECORD_TYPE.get(need.need_type)
    if mapped_record_type is None:
        return bool(answer_input.evidence_records)
    return _has_record_type(answer_input, mapped_record_type)


def _has_record_type(answer_input: ChatAnswerInput, record_type: str) -> bool:
    return any(record.record_type == record_type for record in answer_input.evidence_records)


def _citation_source_type_for_record(record_type: str) -> str:
    if record_type == "source_conflict":
        return "source_conflict"
    if record_type == "unsupported_card":
        return "unsupported_card"
    if record_type == "deck_memory_summary":
        return "deck_memory"
    if record_type == "saved_analysis_summary":
        return "saved_analysis"
    if record_type == "simulation_review_summary":
        return "simulation_review"
    if record_type == "manual_note":
        return "manual_note"
    return "evidence_input_record"


def _record_source_url(record: EvidenceInputRecord) -> str | None:
    for ref in record.references:
        if ref.source_url:
            return ref.source_url
    return None


def _record_generated_at(record: EvidenceInputRecord, fallback: str) -> str:
    if record.references:
        return record.references[0].observed_at
    return fallback


def _input_caveat_type(caveat_type: str) -> str:
    if "unsupported" in caveat_type:
        return "unsupported_card"
    if "conflict" in caveat_type:
        return "source_conflict"
    if "privacy" in caveat_type:
        return "privacy_scope"
    if "missing" in caveat_type:
        return "missing_evidence"
    if "manual" in caveat_type:
        return "manual_review_required"
    if "confidence" in caveat_type or "sample" in caveat_type:
        return "low_confidence"
    return "unavailable_input"


def _section_type_for_question_class(question_class: str) -> str:
    if question_class == "comparison":
        return "comparison"
    if question_class == "source_conflict":
        return "conflict"
    if question_class == "unsupported_card":
        return "unsupported_cards"
    if question_class == "simulation_review":
        return "simulation"
    if question_class == "tag_graph":
        return "tag_graph"
    if question_class == "deck_summary":
        return "summary"
    return "evidence"


def _title_for_question_class(question_class: str) -> str:
    return question_class.replace("_", " ").title()


def _answer_privacy_scope(needs: tuple[ChatEvidenceNeed, ...]) -> str:
    rank = {"public": 0, "local": 1, "local_user_data": 2, "sensitive": 3}
    if not needs:
        return "public"
    return max((need.privacy_scope for need in needs), key=lambda scope: rank[scope])


def _validate_answer_links(answer: ChatAnswer) -> None:
    citation_ids = {citation.citation_id for citation in answer.citations}
    caveat_ids = {caveat.caveat_id for caveat in answer.caveats}
    missing_ids = {item.missing_evidence_id for item in answer.missing_evidence}
    for section in answer.sections:
        unknown_citations = [item for item in section.citation_ids if item not in citation_ids]
        if unknown_citations:
            raise ChatAnswerBuildError(f"unknown citation_id: {unknown_citations[0]}")
        unknown_caveats = [item for item in section.caveat_ids if item not in caveat_ids]
        if unknown_caveats:
            raise ChatAnswerBuildError(f"unknown caveat_id: {unknown_caveats[0]}")
        unknown_missing = [item for item in section.missing_evidence_ids if item not in missing_ids]
        if unknown_missing:
            raise ChatAnswerBuildError(f"unknown missing_evidence_id: {unknown_missing[0]}")


def _is_factual_section(section: ChatAnswerSection) -> bool:
    return section.section_type not in {"unknown", "caveat"}


def _section_to_dict(section: ChatAnswerSection) -> dict[str, Any]:
    return {
        "section_id": section.section_id,
        "section_type": section.section_type,
        "title": section.title,
        "statements": list(section.statements),
        "citation_ids": list(section.citation_ids),
        "caveat_ids": list(section.caveat_ids),
        "missing_evidence_ids": list(section.missing_evidence_ids),
        "metadata": _sorted_json_object(section.metadata),
    }


def _citation_to_dict(citation: ChatAnswerCitation) -> dict[str, Any]:
    return {
        "citation_id": citation.citation_id,
        "source_type": citation.source_type,
        "source_id": citation.source_id,
        "source_label": citation.source_label,
        "source_url": citation.source_url,
        "record_type": citation.record_type,
        "confidence": citation.confidence,
        "generated_at": citation.generated_at,
        "metadata": _sorted_json_object(citation.metadata),
    }


def _answer_caveat_to_dict(caveat: ChatAnswerCaveat) -> dict[str, Any]:
    return {
        "caveat_id": caveat.caveat_id,
        "caveat_type": caveat.caveat_type,
        "message": caveat.message,
        "severity": caveat.severity,
        "metadata": _sorted_json_object(caveat.metadata),
    }


def _missing_evidence_to_dict(item: ChatAnswerMissingEvidence) -> dict[str, Any]:
    return {
        "missing_evidence_id": item.missing_evidence_id,
        "need_id": item.need_id,
        "need_type": item.need_type,
        "reason": item.reason,
        "required": item.required,
        "metadata": _sorted_json_object(item.metadata),
    }


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).strip().lower()
    if normalized not in allowed:
        raise ChatAnswerBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ChatAnswerBuildError(f"{field_name} is required")
    return value.strip()


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    lowered = text.lower()
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment in lowered:
            raise ChatAnswerBuildError(f"forbidden strategic language in {field_name}")
    return text


def _validate_confidence(value: float, field_name: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0.0 or value > 1.0:
        raise ChatAnswerBuildError(f"{field_name} must be between 0.0 and 1.0")


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise ChatAnswerBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise ChatAnswerBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise ChatAnswerBuildError(f"{path} contains forbidden metadata key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise ChatAnswerBuildError(f"{path} must be JSON-compatible")


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
