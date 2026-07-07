"""Pure writer/auditor packet validation for structured chat answers."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.answer_builder import (
    ChatAnswer,
    ChatAnswerCaveat,
    ChatAnswerCitation,
    ChatAnswerMissingEvidence,
    ChatAnswerSection,
)
from codie.intelligence.query_planner import ALLOWED_PRIVACY_SCOPES


ALLOWED_FINDING_TYPES = frozenset(
    {
        "uncited_claim",
        "missing_citation",
        "hidden_caveat",
        "hidden_missing_evidence",
        "hidden_blocker",
        "private_data",
        "forbidden_language",
        "unsupported_card_treated_as_modeled",
        "source_conflict_resolved",
        "recommendation_language",
        "metadata_violation",
        "structure_violation",
    }
)

ALLOWED_SEVERITIES = frozenset({"info", "warning", "blocking"})
ALLOWED_VERDICTS = frozenset({"accepted", "rejected", "needs_manual_review"})

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

UNSUPPORTED_CARD_MODELED_MARKERS = (
    ("unsupported", "modeled"),
    ("unsupported", "supported"),
    ("unsupported", "resolved"),
)

SOURCE_CONFLICT_RESOLUTION_MARKERS = (
    ("source conflict", "resolved"),
    ("source conflict", "winner"),
    ("conflicting sources", "resolved"),
    ("manual review", "not needed"),
)


class LLMWriterAuditorBuildError(ValueError):
    """Raised when writer/auditor packets cannot be built safely."""


@dataclass(frozen=True)
class LLMWriterAuditorOptions:
    allow_cloud_llm: bool = False
    allow_local_user_data: bool = False
    allow_sensitive: bool = False
    maximum_sections: int = 8
    maximum_draft_statements: int = 24
    require_all_citations_visible: bool = True
    require_all_caveats_visible: bool = True
    require_all_missing_evidence_visible: bool = True
    require_all_blockers_visible: bool = True

    def __post_init__(self) -> None:
        if self.maximum_sections < 1:
            raise LLMWriterAuditorBuildError("maximum_sections must be at least 1")
        if self.maximum_draft_statements < 1:
            raise LLMWriterAuditorBuildError("maximum_draft_statements must be at least 1")


@dataclass(frozen=True)
class LLMWriterInput:
    writer_input_id: str
    answer_id: str
    request_id: str
    plan_id: str
    answer_mode: str
    sections: tuple[ChatAnswerSection, ...]
    citations: tuple[ChatAnswerCitation, ...]
    caveats: tuple[ChatAnswerCaveat, ...]
    blockers: tuple[dict[str, Any], ...]
    missing_evidence: tuple[ChatAnswerMissingEvidence, ...]
    privacy_scope: str
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.writer_input_id, "writer_input_id")
        _require_text(self.answer_id, "answer_id")
        _require_text(self.request_id, "request_id")
        _require_text(self.plan_id, "plan_id")
        _require_text(self.answer_mode, "answer_mode")
        sections = [_require_type(item, ChatAnswerSection, "section") for item in self.sections]
        citations = [_require_type(item, ChatAnswerCitation, "citation") for item in self.citations]
        caveats = [_require_type(item, ChatAnswerCaveat, "caveat") for item in self.caveats]
        missing = [_require_type(item, ChatAnswerMissingEvidence, "missing_evidence") for item in self.missing_evidence]
        object.__setattr__(self, "sections", tuple(sorted(sections, key=lambda item: item.section_id)))
        if not self.sections:
            raise LLMWriterAuditorBuildError("writer input requires at least one section")
        object.__setattr__(self, "citations", tuple(sorted(citations, key=lambda item: item.citation_id)))
        object.__setattr__(self, "caveats", tuple(sorted(caveats, key=lambda item: item.caveat_id)))
        object.__setattr__(self, "missing_evidence", tuple(sorted(missing, key=lambda item: item.missing_evidence_id)))
        object.__setattr__(self, "blockers", tuple(_validate_metadata(dict(item)) for item in self.blockers))
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class LLMWriterDraft:
    draft_id: str
    writer_input_id: str
    answer_id: str
    sections: tuple[ChatAnswerSection, ...]
    citation_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    missing_evidence_ids: tuple[str, ...] = ()
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.draft_id, "draft_id")
        _require_text(self.writer_input_id, "writer_input_id")
        _require_text(self.answer_id, "answer_id")
        sections = [_require_type(item, ChatAnswerSection, "section") for item in self.sections]
        object.__setattr__(self, "sections", tuple(sorted(sections, key=lambda item: item.section_id)))
        if not self.sections:
            raise LLMWriterAuditorBuildError("draft requires at least one section")
        object.__setattr__(self, "citation_ids", tuple(sorted(_require_text(item, "citation_id") for item in self.citation_ids)))
        object.__setattr__(self, "caveat_ids", tuple(sorted(_require_text(item, "caveat_id") for item in self.caveat_ids)))
        object.__setattr__(self, "missing_evidence_ids", tuple(sorted(_require_text(item, "missing_evidence_id") for item in self.missing_evidence_ids)))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class LLMAuditFinding:
    finding_id: str
    finding_type: str
    severity: str
    message: str
    section_id: str | None = None
    citation_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.finding_id, "finding_id")
        object.__setattr__(self, "finding_type", _normalize_allowed(self.finding_type, ALLOWED_FINDING_TYPES, "finding_type"))
        object.__setattr__(self, "severity", _normalize_allowed(self.severity, ALLOWED_SEVERITIES, "severity"))
        object.__setattr__(self, "message", _validate_text(self.message, "message"))
        if self.section_id is not None:
            _require_text(self.section_id, "section_id")
        object.__setattr__(self, "citation_ids", tuple(sorted(_require_text(item, "citation_id") for item in self.citation_ids)))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class LLMAuditResult:
    audit_id: str
    draft_id: str
    writer_input_id: str
    answer_id: str
    verdict: str
    findings: tuple[LLMAuditFinding, ...]
    accepted_section_ids: tuple[str, ...] = ()
    rejected_section_ids: tuple[str, ...] = ()
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.audit_id, "audit_id")
        _require_text(self.draft_id, "draft_id")
        _require_text(self.writer_input_id, "writer_input_id")
        _require_text(self.answer_id, "answer_id")
        object.__setattr__(self, "verdict", _normalize_allowed(self.verdict, ALLOWED_VERDICTS, "verdict"))
        findings = [_require_type(item, LLMAuditFinding, "finding") for item in self.findings]
        object.__setattr__(self, "findings", tuple(sorted(findings, key=lambda item: item.finding_id)))
        object.__setattr__(self, "accepted_section_ids", tuple(sorted(_require_text(item, "section_id") for item in self.accepted_section_ids)))
        object.__setattr__(self, "rejected_section_ids", tuple(sorted(_require_text(item, "section_id") for item in self.rejected_section_ids)))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _validate_verdict(self)


def build_writer_input_from_answer(
    answer: ChatAnswer,
    options: LLMWriterAuditorOptions | None = None,
) -> LLMWriterInput:
    """Build a sanitized presentation packet from one structured answer."""

    resolved_options = options or LLMWriterAuditorOptions()
    if not isinstance(answer, ChatAnswer):
        raise LLMWriterAuditorBuildError("answer must be a ChatAnswer")
    if answer.privacy_scope == "local_user_data" and not resolved_options.allow_local_user_data:
        raise LLMWriterAuditorBuildError("local_user_data writer input is disabled by default")
    if answer.privacy_scope == "sensitive" and not resolved_options.allow_sensitive:
        raise LLMWriterAuditorBuildError("sensitive writer input is disabled by default")
    if len(answer.sections) > resolved_options.maximum_sections:
        raise LLMWriterAuditorBuildError("too many writer input sections")
    return LLMWriterInput(
        writer_input_id=f"writer-input:{answer.answer_id}",
        answer_id=answer.answer_id,
        request_id=answer.request_id,
        plan_id=answer.plan_id,
        answer_mode=answer.answer_mode,
        sections=answer.sections,
        citations=answer.citations,
        caveats=answer.caveats,
        blockers=answer.blockers,
        missing_evidence=answer.missing_evidence,
        privacy_scope=answer.privacy_scope,
        generated_at=answer.generated_at,
        metadata={"source": "chat_answer", "answer_metadata": answer.metadata},
    )


def validate_writer_draft(
    draft: LLMWriterDraft,
    writer_input: LLMWriterInput,
    options: LLMWriterAuditorOptions | None = None,
) -> LLMWriterDraft:
    """Validate draft structure before audit."""

    resolved_options = options or LLMWriterAuditorOptions()
    if not isinstance(draft, LLMWriterDraft):
        raise LLMWriterAuditorBuildError("draft must be an LLMWriterDraft")
    if not isinstance(writer_input, LLMWriterInput):
        raise LLMWriterAuditorBuildError("writer_input must be an LLMWriterInput")
    if draft.writer_input_id != writer_input.writer_input_id:
        raise LLMWriterAuditorBuildError("draft writer_input_id does not match writer input")
    if draft.answer_id != writer_input.answer_id:
        raise LLMWriterAuditorBuildError("draft answer_id does not match writer input")
    if len(draft.sections) > resolved_options.maximum_sections:
        raise LLMWriterAuditorBuildError("too many draft sections")
    if _statement_count(draft.sections) > resolved_options.maximum_draft_statements:
        raise LLMWriterAuditorBuildError("too many draft statements")
    _require_known_ids(draft.citation_ids, {item.citation_id for item in writer_input.citations}, "citation_id")
    _require_known_ids(draft.caveat_ids, {item.caveat_id for item in writer_input.caveats}, "caveat_id")
    _require_known_ids(draft.missing_evidence_ids, {item.missing_evidence_id for item in writer_input.missing_evidence}, "missing_evidence_id")
    for section in draft.sections:
        _validate_section_links(section, writer_input)
    return draft


def audit_writer_draft(
    draft: LLMWriterDraft,
    writer_input: LLMWriterInput,
    options: LLMWriterAuditorOptions | None = None,
) -> LLMAuditResult:
    """Audit whether a draft faithfully preserves the structured answer packet."""

    resolved_options = options or LLMWriterAuditorOptions()
    validate_writer_draft(draft, writer_input, resolved_options)
    findings: list[LLMAuditFinding] = []
    findings.extend(_visibility_findings(draft, writer_input, resolved_options))
    findings.extend(_section_findings(draft))
    findings.extend(_content_findings(draft))
    findings = sorted(findings, key=lambda item: item.finding_id)
    rejected = tuple(sorted({finding.section_id for finding in findings if finding.section_id is not None}))
    accepted = () if findings else tuple(section.section_id for section in draft.sections)
    verdict = "accepted" if not findings else "rejected"
    if findings and not any(finding.severity == "blocking" for finding in findings):
        verdict = "needs_manual_review"
    return LLMAuditResult(
        audit_id=f"audit:{draft.draft_id}",
        draft_id=draft.draft_id,
        writer_input_id=writer_input.writer_input_id,
        answer_id=writer_input.answer_id,
        verdict=verdict,
        findings=tuple(findings),
        accepted_section_ids=accepted,
        rejected_section_ids=rejected,
        generated_at=draft.generated_at,
        metadata={"finding_count": len(findings)},
    )


def llm_writer_input_to_dict(writer_input: LLMWriterInput) -> dict[str, Any]:
    """Serialize writer input deterministically."""

    return {
        "writer_input_id": writer_input.writer_input_id,
        "answer_id": writer_input.answer_id,
        "request_id": writer_input.request_id,
        "plan_id": writer_input.plan_id,
        "answer_mode": writer_input.answer_mode,
        "sections": [_section_to_dict(section) for section in writer_input.sections],
        "citations": [_citation_to_dict(citation) for citation in writer_input.citations],
        "caveats": [_caveat_to_dict(caveat) for caveat in writer_input.caveats],
        "blockers": [_sorted_json_object(blocker) for blocker in writer_input.blockers],
        "missing_evidence": [_missing_evidence_to_dict(item) for item in writer_input.missing_evidence],
        "privacy_scope": writer_input.privacy_scope,
        "generated_at": writer_input.generated_at,
        "metadata": _sorted_json_object(writer_input.metadata),
    }


def llm_writer_draft_to_dict(draft: LLMWriterDraft) -> dict[str, Any]:
    """Serialize writer draft deterministically."""

    return {
        "draft_id": draft.draft_id,
        "writer_input_id": draft.writer_input_id,
        "answer_id": draft.answer_id,
        "sections": [_section_to_dict(section) for section in draft.sections],
        "citation_ids": list(draft.citation_ids),
        "caveat_ids": list(draft.caveat_ids),
        "missing_evidence_ids": list(draft.missing_evidence_ids),
        "generated_at": draft.generated_at,
        "metadata": _sorted_json_object(draft.metadata),
    }


def llm_audit_result_to_dict(result: LLMAuditResult) -> dict[str, Any]:
    """Serialize audit result deterministically."""

    return {
        "audit_id": result.audit_id,
        "draft_id": result.draft_id,
        "writer_input_id": result.writer_input_id,
        "answer_id": result.answer_id,
        "verdict": result.verdict,
        "findings": [_finding_to_dict(finding) for finding in result.findings],
        "accepted_section_ids": list(result.accepted_section_ids),
        "rejected_section_ids": list(result.rejected_section_ids),
        "generated_at": result.generated_at,
        "metadata": _sorted_json_object(result.metadata),
    }


def _visibility_findings(
    draft: LLMWriterDraft,
    writer_input: LLMWriterInput,
    options: LLMWriterAuditorOptions,
) -> tuple[LLMAuditFinding, ...]:
    findings: list[LLMAuditFinding] = []
    if options.require_all_citations_visible:
        findings.extend(_missing_id_findings(draft.citation_ids, [item.citation_id for item in writer_input.citations], "missing_citation", "citation"))
    if options.require_all_caveats_visible:
        findings.extend(_missing_id_findings(draft.caveat_ids, [item.caveat_id for item in writer_input.caveats], "hidden_caveat", "caveat"))
    if options.require_all_missing_evidence_visible:
        findings.extend(
            _missing_id_findings(
                draft.missing_evidence_ids,
                [item.missing_evidence_id for item in writer_input.missing_evidence],
                "hidden_missing_evidence",
                "missing_evidence",
            )
        )
    if options.require_all_blockers_visible:
        combined_text = _combined_draft_text(draft)
        for index, blocker in enumerate(writer_input.blockers):
            if not _metadata_text_visible(blocker, combined_text):
                findings.append(
                    LLMAuditFinding(
                        finding_id=f"finding:hidden-blocker:{index}",
                        finding_type="hidden_blocker",
                        severity="blocking",
                        message="Draft hides a source answer blocker.",
                        metadata={"blocker_index": index},
                    )
                )
    return tuple(findings)


def _missing_id_findings(
    visible_ids: tuple[str, ...],
    required_ids: list[str],
    finding_type: str,
    label: str,
) -> tuple[LLMAuditFinding, ...]:
    findings = []
    visible = set(visible_ids)
    for item_id in sorted(required_ids):
        if item_id not in visible:
            findings.append(
                LLMAuditFinding(
                    finding_id=f"finding:{finding_type}:{item_id}",
                    finding_type=finding_type,
                    severity="blocking",
                    message=f"Draft hides required {label} visibility.",
                    metadata={f"{label}_id": item_id},
                )
            )
    return tuple(findings)


def _section_findings(draft: LLMWriterDraft) -> tuple[LLMAuditFinding, ...]:
    findings: list[LLMAuditFinding] = []
    for section in draft.sections:
        if not section.citation_ids and not section.caveat_ids and not section.missing_evidence_ids:
            findings.append(
                LLMAuditFinding(
                    finding_id=f"finding:uncited:{section.section_id}",
                    finding_type="uncited_claim",
                    severity="blocking",
                    message="Draft section contains unsupported statements.",
                    section_id=section.section_id,
                )
            )
    return tuple(findings)


def _content_findings(draft: LLMWriterDraft) -> tuple[LLMAuditFinding, ...]:
    findings: list[LLMAuditFinding] = []
    for section in draft.sections:
        text = " ".join(section.statements).lower()
        if _contains_forbidden_language(text):
            findings.append(
                LLMAuditFinding(
                    finding_id=f"finding:forbidden-language:{section.section_id}",
                    finding_type="forbidden_language",
                    severity="blocking",
                    message="Draft contains forbidden strategic language.",
                    section_id=section.section_id,
                )
            )
        if _matches_pair_markers(text, UNSUPPORTED_CARD_MODELED_MARKERS):
            findings.append(
                LLMAuditFinding(
                    finding_id=f"finding:unsupported-modeled:{section.section_id}",
                    finding_type="unsupported_card_treated_as_modeled",
                    severity="blocking",
                    message="Draft treats unsupported card behavior as modeled.",
                    section_id=section.section_id,
                )
            )
        if _matches_pair_markers(text, SOURCE_CONFLICT_RESOLUTION_MARKERS):
            findings.append(
                LLMAuditFinding(
                    finding_id=f"finding:source-conflict:{section.section_id}",
                    finding_type="source_conflict_resolved",
                    severity="blocking",
                    message="Draft resolves a source conflict instead of preserving it.",
                    section_id=section.section_id,
                )
            )
    return tuple(findings)


def _validate_section_links(section: ChatAnswerSection, writer_input: LLMWriterInput) -> None:
    _require_known_ids(section.citation_ids, {item.citation_id for item in writer_input.citations}, "citation_id")
    _require_known_ids(section.caveat_ids, {item.caveat_id for item in writer_input.caveats}, "caveat_id")
    _require_known_ids(section.missing_evidence_ids, {item.missing_evidence_id for item in writer_input.missing_evidence}, "missing_evidence_id")


def _require_known_ids(ids: tuple[str, ...], known_ids: set[str], field_name: str) -> None:
    for item_id in ids:
        if item_id not in known_ids:
            raise LLMWriterAuditorBuildError(f"unknown {field_name}: {item_id}")


def _statement_count(sections: tuple[ChatAnswerSection, ...]) -> int:
    return sum(len(section.statements) for section in sections)


def _combined_draft_text(draft: LLMWriterDraft) -> str:
    return " ".join(statement for section in draft.sections for statement in section.statements).lower()


def _metadata_text_visible(metadata: dict[str, Any], combined_text: str) -> bool:
    text_values = [value.lower() for value in _iter_text_values(metadata) if len(value.strip()) >= 4]
    if not text_values:
        return True
    return any(value in combined_text for value in text_values)


def _iter_text_values(value: Any) -> tuple[str, ...]:
    if isinstance(value, dict):
        values: list[str] = []
        for child in value.values():
            values.extend(_iter_text_values(child))
        return tuple(values)
    if isinstance(value, (list, tuple)):
        values = []
        for child in value:
            values.extend(_iter_text_values(child))
        return tuple(values)
    if isinstance(value, str):
        return (value,)
    return ()


def _matches_pair_markers(text: str, markers: tuple[tuple[str, str], ...]) -> bool:
    return any(first in text and second in text for first, second in markers)


def _contains_forbidden_language(text: str) -> bool:
    return any(fragment in text for fragment in FORBIDDEN_TEXT_FRAGMENTS)


def _validate_verdict(result: LLMAuditResult) -> None:
    has_blocking = any(finding.severity == "blocking" for finding in result.findings)
    has_warning = any(finding.severity == "warning" for finding in result.findings)
    if result.verdict == "accepted" and (has_blocking or has_warning):
        raise LLMWriterAuditorBuildError("accepted audit result cannot contain blocking or warning findings")
    if has_blocking and result.verdict != "rejected":
        raise LLMWriterAuditorBuildError("blocking findings require rejected verdict")


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


def _caveat_to_dict(caveat: ChatAnswerCaveat) -> dict[str, Any]:
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


def _finding_to_dict(finding: LLMAuditFinding) -> dict[str, Any]:
    return {
        "finding_id": finding.finding_id,
        "finding_type": finding.finding_type,
        "severity": finding.severity,
        "message": finding.message,
        "section_id": finding.section_id,
        "citation_ids": list(finding.citation_ids),
        "metadata": _sorted_json_object(finding.metadata),
    }


def _require_type(value: Any, expected_type: type, field_name: str) -> Any:
    if not isinstance(value, expected_type):
        raise LLMWriterAuditorBuildError(f"{field_name} has invalid type")
    return value


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).strip().lower()
    if normalized not in allowed:
        raise LLMWriterAuditorBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LLMWriterAuditorBuildError(f"{field_name} is required")
    return value.strip()


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    if _contains_forbidden_language(text.lower()):
        raise LLMWriterAuditorBuildError(f"forbidden strategic language in {field_name}")
    return text


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise LLMWriterAuditorBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise LLMWriterAuditorBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise LLMWriterAuditorBuildError(f"{path} contains forbidden metadata key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise LLMWriterAuditorBuildError(f"{path} must be JSON-compatible")


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
