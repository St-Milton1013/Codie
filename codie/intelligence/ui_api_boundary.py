"""Pure UI/API boundary packets for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from codie.intelligence.answer_builder import (
    ChatAnswer,
    ChatAnswerCaveat,
    ChatAnswerCitation,
    ChatAnswerMissingEvidence,
    chat_answer_to_dict,
)
from codie.intelligence.llm_writer_auditor import (
    LLMAuditResult,
    LLMWriterDraft,
    LLMWriterInput,
    llm_audit_result_to_dict,
    llm_writer_draft_to_dict,
    llm_writer_input_to_dict,
)
from codie.intelligence.query_planner import (
    ALLOWED_PRIVACY_SCOPES,
    ALLOWED_QUESTION_CLASSES,
    ChatQueryConstraint,
    ChatQueryPlan,
    ChatQueryRequest,
    ChatQuerySubject,
    chat_query_plan_to_dict,
)


ALLOWED_CLIENT_SURFACES = frozenset({"local_ui", "local_api", "cli", "test_fixture"})
ALLOWED_ERROR_TYPES = frozenset(
    {
        "validation_error",
        "privacy_scope_blocked",
        "unsupported_question",
        "missing_evidence",
        "writer_audit_rejected",
        "internal_error",
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

STACK_TRACE_KEYS = frozenset({"traceback", "stack", "stack_trace", "exception_trace"})


class ChatUIBoundaryBuildError(ValueError):
    """Raised when UI/API boundary packets cannot be built safely."""


@dataclass(frozen=True)
class ChatUIBoundaryOptions:
    allow_local_user_data: bool = False
    allow_sensitive: bool = False
    allow_writer_draft: bool = False
    allow_unaudited_writer_draft: bool = False
    maximum_question_length: int = 1000
    maximum_constraints: int = 24
    require_citations_visible: bool = True
    require_caveats_visible: bool = True
    require_missing_evidence_visible: bool = True
    require_blockers_visible: bool = True

    def __post_init__(self) -> None:
        if self.maximum_question_length < 1:
            raise ChatUIBoundaryBuildError("maximum_question_length must be positive")
        if self.maximum_constraints < 1:
            raise ChatUIBoundaryBuildError("maximum_constraints must be positive")


@dataclass(frozen=True)
class ChatUIRequestPacket:
    request_packet_id: str
    request_id: str
    question_text: str
    subject: ChatQuerySubject
    constraints: tuple[ChatQueryConstraint, ...]
    allowed_privacy_scopes: tuple[str, ...]
    requested_answer_mode: str | None
    client_surface: str
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.request_packet_id, "request_packet_id")
        _require_text(self.request_id, "request_id")
        object.__setattr__(self, "question_text", _validate_text(self.question_text, "question_text"))
        if not isinstance(self.subject, ChatQuerySubject):
            raise ChatUIBoundaryBuildError("subject must be a ChatQuerySubject")
        constraints = [_require_type(item, ChatQueryConstraint, "constraint") for item in self.constraints]
        object.__setattr__(self, "constraints", tuple(sorted(constraints, key=lambda item: item.constraint_id)))
        if not self.allowed_privacy_scopes:
            raise ChatUIBoundaryBuildError("allowed_privacy_scopes must not be empty")
        scopes = tuple(_normalize_allowed(scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope") for scope in self.allowed_privacy_scopes)
        object.__setattr__(self, "allowed_privacy_scopes", scopes)
        if self.requested_answer_mode is not None:
            object.__setattr__(self, "requested_answer_mode", _normalize_allowed(self.requested_answer_mode, ALLOWED_QUESTION_CLASSES, "requested_answer_mode"))
        object.__setattr__(self, "client_surface", _normalize_allowed(self.client_surface, ALLOWED_CLIENT_SURFACES, "client_surface"))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatUIResponsePacket:
    response_packet_id: str
    request_packet_id: str
    request_id: str
    plan: ChatQueryPlan
    answer: ChatAnswer
    writer_input: LLMWriterInput | None = None
    writer_draft: LLMWriterDraft | None = None
    audit_result: LLMAuditResult | None = None
    citations: tuple[ChatAnswerCitation, ...] = ()
    caveats: tuple[ChatAnswerCaveat, ...] = ()
    missing_evidence: tuple[ChatAnswerMissingEvidence, ...] = ()
    blockers: tuple[dict[str, Any], ...] = ()
    privacy_scope: str = "public"
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.response_packet_id, "response_packet_id")
        _require_text(self.request_packet_id, "request_packet_id")
        _require_text(self.request_id, "request_id")
        if not isinstance(self.plan, ChatQueryPlan):
            raise ChatUIBoundaryBuildError("plan must be a ChatQueryPlan")
        if not isinstance(self.answer, ChatAnswer):
            raise ChatUIBoundaryBuildError("answer must be a ChatAnswer")
        object.__setattr__(self, "citations", _sorted_typed_tuple(self.citations, ChatAnswerCitation, "citation", "citation_id"))
        object.__setattr__(self, "caveats", _sorted_typed_tuple(self.caveats, ChatAnswerCaveat, "caveat", "caveat_id"))
        object.__setattr__(self, "missing_evidence", _sorted_typed_tuple(self.missing_evidence, ChatAnswerMissingEvidence, "missing_evidence", "missing_evidence_id"))
        object.__setattr__(self, "blockers", tuple(_validate_metadata(dict(item)) for item in self.blockers))
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        if self.writer_input is not None and not isinstance(self.writer_input, LLMWriterInput):
            raise ChatUIBoundaryBuildError("writer_input must be an LLMWriterInput")
        if self.writer_draft is not None and not isinstance(self.writer_draft, LLMWriterDraft):
            raise ChatUIBoundaryBuildError("writer_draft must be an LLMWriterDraft")
        if self.audit_result is not None and not isinstance(self.audit_result, LLMAuditResult):
            raise ChatUIBoundaryBuildError("audit_result must be an LLMAuditResult")
        _validate_packet_links(self)


@dataclass(frozen=True)
class ChatUIErrorPacket:
    error_packet_id: str
    request_packet_id: str
    request_id: str
    error_type: str
    message: str
    retryable: bool
    caveats: tuple[dict[str, Any], ...] = ()
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.error_packet_id, "error_packet_id")
        _require_text(self.request_packet_id, "request_packet_id")
        _require_text(self.request_id, "request_id")
        object.__setattr__(self, "error_type", _normalize_allowed(self.error_type, ALLOWED_ERROR_TYPES, "error_type"))
        object.__setattr__(self, "message", _validate_text(self.message, "message"))
        if not isinstance(self.retryable, bool):
            raise ChatUIBoundaryBuildError("retryable must be a bool")
        object.__setattr__(self, "caveats", tuple(_validate_metadata(dict(item)) for item in self.caveats))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_error_metadata(self.metadata))


def build_chat_ui_request_packet(
    request: ChatQueryRequest,
    client_surface: str,
    requested_answer_mode: str | None = None,
    options: ChatUIBoundaryOptions | None = None,
) -> ChatUIRequestPacket:
    """Build a deterministic UI/API request packet from a sanitized request."""

    resolved_options = options or ChatUIBoundaryOptions()
    if not isinstance(request, ChatQueryRequest):
        raise ChatUIBoundaryBuildError("request must be a ChatQueryRequest")
    if len(request.question_text) > resolved_options.maximum_question_length:
        raise ChatUIBoundaryBuildError("question_text is too long")
    if len(request.constraints) > resolved_options.maximum_constraints:
        raise ChatUIBoundaryBuildError("too many constraints")
    _validate_privacy_scopes(request.allowed_privacy_scopes, resolved_options)
    return ChatUIRequestPacket(
        request_packet_id=f"chat-ui-request:{request.request_id}",
        request_id=request.request_id,
        question_text=request.question_text,
        subject=request.subject,
        constraints=request.constraints,
        allowed_privacy_scopes=request.allowed_privacy_scopes,
        requested_answer_mode=requested_answer_mode,
        client_surface=client_surface,
        generated_at=request.generated_at,
        metadata={"source": "chat_query_request", "request_metadata": request.metadata},
    )


def build_chat_ui_response_packet(
    request_packet: ChatUIRequestPacket,
    plan: ChatQueryPlan,
    answer: ChatAnswer,
    writer_input: LLMWriterInput | None = None,
    writer_draft: LLMWriterDraft | None = None,
    audit_result: LLMAuditResult | None = None,
    options: ChatUIBoundaryOptions | None = None,
) -> ChatUIResponsePacket:
    """Build a deterministic UI/API response packet from structured outputs."""

    resolved_options = options or ChatUIBoundaryOptions()
    if not isinstance(request_packet, ChatUIRequestPacket):
        raise ChatUIBoundaryBuildError("request_packet must be a ChatUIRequestPacket")
    if plan.request_id != request_packet.request_id:
        raise ChatUIBoundaryBuildError("plan request_id does not match request packet")
    if answer.request_id != request_packet.request_id:
        raise ChatUIBoundaryBuildError("answer request_id does not match request packet")
    _validate_privacy_scope(answer.privacy_scope, resolved_options)
    _validate_writer_packets(writer_input, writer_draft, audit_result, resolved_options)
    return ChatUIResponsePacket(
        response_packet_id=f"chat-ui-response:{request_packet.request_id}",
        request_packet_id=request_packet.request_packet_id,
        request_id=request_packet.request_id,
        plan=plan,
        answer=answer,
        writer_input=writer_input,
        writer_draft=writer_draft,
        audit_result=audit_result,
        citations=answer.citations,
        caveats=answer.caveats,
        missing_evidence=answer.missing_evidence,
        blockers=answer.blockers,
        privacy_scope=answer.privacy_scope,
        generated_at=answer.generated_at,
        metadata={"source": "chat_answer", "answer_id": answer.answer_id},
    )


def build_chat_ui_error_packet(
    request_packet: ChatUIRequestPacket,
    error_type: str,
    message: str,
    retryable: bool = False,
    caveats: tuple[dict[str, Any], ...] = (),
    generated_at: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ChatUIErrorPacket:
    """Build a deterministic UI/API error packet without raw exception details."""

    if not isinstance(request_packet, ChatUIRequestPacket):
        raise ChatUIBoundaryBuildError("request_packet must be a ChatUIRequestPacket")
    return ChatUIErrorPacket(
        error_packet_id=f"chat-ui-error:{request_packet.request_id}",
        request_packet_id=request_packet.request_packet_id,
        request_id=request_packet.request_id,
        error_type=error_type,
        message=message,
        retryable=retryable,
        caveats=caveats,
        generated_at=generated_at or request_packet.generated_at,
        metadata=metadata or {},
    )


def chat_ui_request_packet_to_dict(packet: ChatUIRequestPacket) -> dict[str, Any]:
    """Serialize one request packet deterministically."""

    return {
        "request_packet_id": packet.request_packet_id,
        "request_id": packet.request_id,
        "question_text": packet.question_text,
        "subject": _subject_to_dict(packet.subject),
        "constraints": [_constraint_to_dict(item) for item in packet.constraints],
        "allowed_privacy_scopes": list(packet.allowed_privacy_scopes),
        "requested_answer_mode": packet.requested_answer_mode,
        "client_surface": packet.client_surface,
        "generated_at": packet.generated_at,
        "metadata": _sorted_json_object(packet.metadata),
    }


def chat_ui_response_packet_to_dict(packet: ChatUIResponsePacket) -> dict[str, Any]:
    """Serialize one response packet deterministically."""

    return {
        "response_packet_id": packet.response_packet_id,
        "request_packet_id": packet.request_packet_id,
        "request_id": packet.request_id,
        "plan": chat_query_plan_to_dict(packet.plan),
        "answer": chat_answer_to_dict(packet.answer),
        "writer_input": llm_writer_input_to_dict(packet.writer_input) if packet.writer_input is not None else None,
        "writer_draft": llm_writer_draft_to_dict(packet.writer_draft) if packet.writer_draft is not None else None,
        "audit_result": llm_audit_result_to_dict(packet.audit_result) if packet.audit_result is not None else None,
        "citations": [_citation_to_dict(item) for item in packet.citations],
        "caveats": [_caveat_to_dict(item) for item in packet.caveats],
        "missing_evidence": [_missing_evidence_to_dict(item) for item in packet.missing_evidence],
        "blockers": [_sorted_json_object(item) for item in packet.blockers],
        "privacy_scope": packet.privacy_scope,
        "generated_at": packet.generated_at,
        "metadata": _sorted_json_object(packet.metadata),
    }


def chat_ui_error_packet_to_dict(packet: ChatUIErrorPacket) -> dict[str, Any]:
    """Serialize one error packet deterministically."""

    return {
        "error_packet_id": packet.error_packet_id,
        "request_packet_id": packet.request_packet_id,
        "request_id": packet.request_id,
        "error_type": packet.error_type,
        "message": packet.message,
        "retryable": packet.retryable,
        "caveats": [_sorted_json_object(item) for item in packet.caveats],
        "generated_at": packet.generated_at,
        "metadata": _sorted_json_object(packet.metadata),
    }


def _validate_packet_links(packet: ChatUIResponsePacket) -> None:
    if packet.plan.request_id != packet.request_id:
        raise ChatUIBoundaryBuildError("plan request_id does not match response")
    if packet.answer.request_id != packet.request_id:
        raise ChatUIBoundaryBuildError("answer request_id does not match response")
    if packet.answer.plan_id != packet.plan.plan_id:
        raise ChatUIBoundaryBuildError("answer plan_id does not match plan")
    _require_visible_ids([item.citation_id for item in packet.answer.citations], [item.citation_id for item in packet.citations], "citation")
    _require_visible_ids([item.caveat_id for item in packet.answer.caveats], [item.caveat_id for item in packet.caveats], "caveat")
    _require_visible_ids(
        [item.missing_evidence_id for item in packet.answer.missing_evidence],
        [item.missing_evidence_id for item in packet.missing_evidence],
        "missing_evidence",
    )
    if len(packet.blockers) < len(packet.answer.blockers):
        raise ChatUIBoundaryBuildError("response hides answer blockers")
    if packet.writer_draft is not None and packet.audit_result is None:
        raise ChatUIBoundaryBuildError("writer_draft requires audit_result")
    if packet.audit_result is not None and packet.audit_result.verdict != "accepted":
        raise ChatUIBoundaryBuildError("audit_result must be accepted for response display")


def _validate_writer_packets(
    writer_input: LLMWriterInput | None,
    writer_draft: LLMWriterDraft | None,
    audit_result: LLMAuditResult | None,
    options: ChatUIBoundaryOptions,
) -> None:
    if writer_input is not None and not options.allow_writer_draft:
        raise ChatUIBoundaryBuildError("writer packets are disabled by default")
    if writer_draft is not None and not options.allow_writer_draft:
        raise ChatUIBoundaryBuildError("writer packets are disabled by default")
    if writer_draft is not None and audit_result is None and not options.allow_unaudited_writer_draft:
        raise ChatUIBoundaryBuildError("unaudited writer drafts are disabled by default")
    if audit_result is not None and audit_result.verdict != "accepted":
        raise ChatUIBoundaryBuildError("rejected writer audit cannot be displayed")
    if writer_input is not None and writer_draft is not None and writer_draft.writer_input_id != writer_input.writer_input_id:
        raise ChatUIBoundaryBuildError("writer_draft does not match writer_input")
    if writer_draft is not None and audit_result is not None and audit_result.draft_id != writer_draft.draft_id:
        raise ChatUIBoundaryBuildError("audit_result does not match writer_draft")


def _validate_privacy_scopes(scopes: tuple[str, ...], options: ChatUIBoundaryOptions) -> None:
    for scope in scopes:
        _validate_privacy_scope(scope, options)


def _validate_privacy_scope(scope: str, options: ChatUIBoundaryOptions) -> None:
    normalized = _normalize_allowed(scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope")
    if normalized == "local_user_data" and not options.allow_local_user_data:
        raise ChatUIBoundaryBuildError("local_user_data is disabled by default")
    if normalized == "sensitive" and not options.allow_sensitive:
        raise ChatUIBoundaryBuildError("sensitive scope is disabled by default")


def _require_visible_ids(required_ids: list[str], visible_ids: list[str], label: str) -> None:
    visible = set(visible_ids)
    for item_id in required_ids:
        if item_id not in visible:
            raise ChatUIBoundaryBuildError(f"response hides {label}: {item_id}")


def _sorted_typed_tuple(values: tuple[Any, ...], expected_type: type, field_name: str, sort_field: str) -> tuple[Any, ...]:
    typed = [_require_type(item, expected_type, field_name) for item in values]
    return tuple(sorted(typed, key=lambda item: getattr(item, sort_field)))


def _subject_to_dict(subject: ChatQuerySubject) -> dict[str, Any]:
    return {
        "subject_type": subject.subject_type,
        "subject_key": subject.subject_key,
        "display_name": subject.display_name,
        "metadata": _sorted_json_object(subject.metadata),
    }


def _constraint_to_dict(constraint: ChatQueryConstraint) -> dict[str, Any]:
    return {
        "constraint_id": constraint.constraint_id,
        "constraint_type": constraint.constraint_type,
        "value": _validate_json_value(constraint.value, "constraint.value"),
        "required": constraint.required,
        "metadata": _sorted_json_object(constraint.metadata),
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


def _validate_error_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_metadata(metadata)
    for key in _iter_keys(validated):
        if _normalize_metadata_key(key) in STACK_TRACE_KEYS:
            raise ChatUIBoundaryBuildError("error metadata must not expose stack traces")
    return validated


def _iter_keys(value: Any) -> tuple[str, ...]:
    if isinstance(value, dict):
        keys: list[str] = []
        for key, child in value.items():
            keys.append(key)
            keys.extend(_iter_keys(child))
        return tuple(keys)
    if isinstance(value, (list, tuple)):
        keys = []
        for child in value:
            keys.extend(_iter_keys(child))
        return tuple(keys)
    return ()


def _require_type(value: Any, expected_type: type, field_name: str) -> Any:
    if not isinstance(value, expected_type):
        raise ChatUIBoundaryBuildError(f"{field_name} has invalid type")
    return value


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).strip().lower()
    if normalized not in allowed:
        raise ChatUIBoundaryBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ChatUIBoundaryBuildError(f"{field_name} is required")
    return value.strip()


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    if _contains_forbidden_language(text.lower()):
        raise ChatUIBoundaryBuildError(f"forbidden strategic language in {field_name}")
    return text


def _contains_forbidden_language(text: str) -> bool:
    return any(fragment in text for fragment in FORBIDDEN_TEXT_FRAGMENTS)


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise ChatUIBoundaryBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise ChatUIBoundaryBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise ChatUIBoundaryBuildError(f"{path} contains forbidden metadata key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise ChatUIBoundaryBuildError(f"{path} must be JSON-compatible")


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
