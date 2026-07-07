"""Pure chat query planning for interactive intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


ALLOWED_PRIVACY_SCOPES = frozenset({"public", "local", "local_user_data", "sensitive"})

ALLOWED_SUBJECT_TYPES = frozenset(
    {
        "deck",
        "saved_deck",
        "commander",
        "partner_pair",
        "card",
        "package",
        "simulation_result",
        "source_conflict",
        "unsupported_card",
        "tag_graph",
        "unknown",
    }
)

ALLOWED_QUESTION_CLASSES = frozenset(
    {
        "deck_summary",
        "card_evidence",
        "commander_evidence",
        "comparison",
        "source_conflict",
        "unsupported_card",
        "simulation_review",
        "primer_metadata",
        "innovation_signal",
        "tag_graph",
        "export_request",
        "unknown",
    }
)

ALLOWED_EVIDENCE_NEED_TYPES = frozenset(
    {
        "evidence_graph",
        "evidence_input_records",
        "deck_memory",
        "saved_analysis",
        "source_conflicts",
        "unsupported_cards",
        "simulation_review_summary",
        "primer_metadata",
        "combo_evidence",
        "innovation_signal",
        "frequency_pool",
        "tag_graph",
        "manual_note",
    }
)

ALLOWED_OPERATIONS = frozenset(
    {
        "build_evidence_graph",
        "assemble_evidence_inputs",
        "inspect_source_conflicts",
        "inspect_unsupported_cards",
        "inspect_deck_memory",
        "inspect_saved_analysis",
        "inspect_simulation_review",
        "inspect_primer_metadata",
        "inspect_innovation_signal",
        "inspect_frequency_pool",
        "inspect_tag_graph",
        "return_caveated_unknown",
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


class ChatQueryPlanBuildError(ValueError):
    """Raised when a chat query plan cannot be built safely."""


@dataclass(frozen=True)
class ChatQuerySubject:
    subject_type: str
    subject_key: str | None = None
    display_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject_type", _normalize_allowed(self.subject_type, ALLOWED_SUBJECT_TYPES, "subject_type"))
        if self.subject_type != "unknown" and self.subject_key in (None, ""):
            raise ChatQueryPlanBuildError("subject_key is required unless subject_type is unknown")
        if self.subject_key is not None:
            _require_text(self.subject_key, "subject_key")
        if self.display_name is not None:
            _validate_text(self.display_name, "display_name")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatQueryConstraint:
    constraint_id: str
    constraint_type: str
    value: Any
    required: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.constraint_id, "constraint_id")
        _require_text(self.constraint_type, "constraint_type")
        object.__setattr__(self, "constraint_type", self.constraint_type.strip().lower())
        object.__setattr__(self, "value", _validate_json_value(self.value, "value"))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatQueryRequest:
    request_id: str
    question_text: str
    generated_at: str
    subject: ChatQuerySubject
    constraints: tuple[ChatQueryConstraint, ...] = ()
    allowed_privacy_scopes: tuple[str, ...] = ("public",)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.request_id, "request_id")
        object.__setattr__(self, "question_text", _validate_text(self.question_text, "question_text"))
        _require_text(self.generated_at, "generated_at")
        if not isinstance(self.subject, ChatQuerySubject):
            raise ChatQueryPlanBuildError("subject must be a ChatQuerySubject")
        object.__setattr__(self, "constraints", tuple(sorted(self.constraints, key=lambda item: item.constraint_id)))
        if not self.allowed_privacy_scopes:
            raise ChatQueryPlanBuildError("allowed_privacy_scopes must not be empty")
        object.__setattr__(
            self,
            "allowed_privacy_scopes",
            tuple(_normalize_allowed(scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope") for scope in self.allowed_privacy_scopes),
        )
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatEvidenceNeed:
    need_id: str
    need_type: str
    reason: str
    required: bool = True
    privacy_scope: str = "public"
    record_types: tuple[str, ...] = ()
    filters: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.need_id, "need_id")
        object.__setattr__(self, "need_type", _normalize_allowed(self.need_type, ALLOWED_EVIDENCE_NEED_TYPES, "need_type"))
        object.__setattr__(self, "reason", _validate_text(self.reason, "reason"))
        object.__setattr__(self, "privacy_scope", _normalize_allowed(self.privacy_scope, ALLOWED_PRIVACY_SCOPES, "privacy_scope"))
        object.__setattr__(self, "record_types", tuple(sorted(str(value).strip().lower() for value in self.record_types if str(value).strip())))
        object.__setattr__(self, "filters", _validate_metadata(self.filters))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatQueryPlan:
    plan_id: str
    request_id: str
    question_class: str
    subject: ChatQuerySubject
    evidence_needs: tuple[ChatEvidenceNeed, ...]
    constraints: tuple[ChatQueryConstraint, ...] = ()
    blockers: tuple[dict[str, Any], ...] = ()
    caveats: tuple[dict[str, Any], ...] = ()
    allowed_operations: tuple[str, ...] = ()
    generated_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.plan_id, "plan_id")
        _require_text(self.request_id, "request_id")
        object.__setattr__(self, "question_class", _normalize_allowed(self.question_class, ALLOWED_QUESTION_CLASSES, "question_class"))
        if not isinstance(self.subject, ChatQuerySubject):
            raise ChatQueryPlanBuildError("subject must be a ChatQuerySubject")
        object.__setattr__(self, "evidence_needs", tuple(sorted(self.evidence_needs, key=lambda item: item.need_id)))
        if self.question_class != "unknown" and not self.evidence_needs:
            raise ChatQueryPlanBuildError("evidence_needs must not be empty unless question_class is unknown")
        object.__setattr__(self, "constraints", tuple(sorted(self.constraints, key=lambda item: item.constraint_id)))
        object.__setattr__(self, "blockers", tuple(_validate_metadata(dict(item)) for item in self.blockers))
        object.__setattr__(self, "caveats", tuple(_validate_metadata(dict(item)) for item in self.caveats))
        object.__setattr__(
            self,
            "allowed_operations",
            tuple(sorted(_normalize_allowed(item, ALLOWED_OPERATIONS, "allowed_operation") for item in self.allowed_operations)),
        )
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class ChatQueryPlannerOptions:
    default_privacy_scope: str = "public"
    allow_sensitive: bool = False
    allow_local_user_data: bool = False
    maximum_evidence_needs: int = 8
    maximum_constraints: int = 12

    def __post_init__(self) -> None:
        object.__setattr__(self, "default_privacy_scope", _normalize_allowed(self.default_privacy_scope, ALLOWED_PRIVACY_SCOPES, "default_privacy_scope"))
        if self.maximum_evidence_needs < 1:
            raise ChatQueryPlanBuildError("maximum_evidence_needs must be at least 1")
        if self.maximum_constraints < 1:
            raise ChatQueryPlanBuildError("maximum_constraints must be at least 1")


def build_chat_query_plan(
    request: ChatQueryRequest,
    options: ChatQueryPlannerOptions | None = None,
) -> ChatQueryPlan:
    """Build one deterministic query plan from a sanitized request."""

    resolved_options = options or ChatQueryPlannerOptions()
    if len(request.constraints) > resolved_options.maximum_constraints:
        raise ChatQueryPlanBuildError("too many constraints")

    question_class = _classify_question(request)
    evidence_needs = _evidence_needs_for(request, question_class, resolved_options)
    if len(evidence_needs) > resolved_options.maximum_evidence_needs:
        raise ChatQueryPlanBuildError("too many evidence needs")
    blockers, caveats = _privacy_blockers_and_caveats(evidence_needs, request, resolved_options)
    operations = _operations_for(question_class, evidence_needs)
    if question_class == "unknown":
        caveats = caveats + (
            {
                "caveat_type": "unknown_question",
                "message": "The question could not be mapped to a supported query class.",
                "severity": "warning",
                "metadata": {"question_class": "unknown"},
            },
        )
        operations = ("return_caveated_unknown",)

    return ChatQueryPlan(
        plan_id=f"chat-query-plan:{request.request_id}",
        request_id=request.request_id,
        question_class=question_class,
        subject=request.subject,
        evidence_needs=evidence_needs,
        constraints=request.constraints,
        blockers=blockers,
        caveats=caveats,
        allowed_operations=operations,
        generated_at=request.generated_at,
        metadata={
            "planner_version": "phase20b",
            "request_metadata": request.metadata,
        },
    )


def chat_query_plan_to_dict(plan: ChatQueryPlan) -> dict[str, Any]:
    """Serialize one chat query plan deterministically."""

    return {
        "plan_id": plan.plan_id,
        "request_id": plan.request_id,
        "question_class": plan.question_class,
        "subject": _subject_to_dict(plan.subject),
        "evidence_needs": [_need_to_dict(need) for need in plan.evidence_needs],
        "constraints": [_constraint_to_dict(constraint) for constraint in plan.constraints],
        "blockers": [_sorted_json_object(item) for item in plan.blockers],
        "caveats": [_sorted_json_object(item) for item in plan.caveats],
        "allowed_operations": list(plan.allowed_operations),
        "generated_at": plan.generated_at,
        "metadata": _sorted_json_object(plan.metadata),
    }


def _classify_question(request: ChatQueryRequest) -> str:
    text = _normalized_text(request.question_text)
    subject_type = request.subject.subject_type
    if _contains_any(text, ("tag graph", "tag trend", "tags", "role graph")) or subject_type == "tag_graph":
        return "tag_graph"
    if _contains_any(text, ("source conflict", "conflict", "disagree", "mismatch")) or subject_type == "source_conflict":
        return "source_conflict"
    if _contains_any(text, ("unsupported", "unresolved", "missing model", "cannot model")) or subject_type == "unsupported_card":
        return "unsupported_card"
    if _contains_any(text, ("simulation", "simulator", "challenge", "opening hand")) or subject_type == "simulation_result":
        return "simulation_review"
    if _contains_any(text, ("primer", "moxfield primer")):
        return "primer_metadata"
    if _contains_any(text, ("innovation", "breakout", "resurgence", "new card")):
        return "innovation_signal"
    if _contains_any(text, ("export", "markdown", "csv", "json", "obsidian")):
        return "export_request"
    if _contains_any(text, ("compare", " vs ", "versus", "against")):
        return "comparison"
    if subject_type == "card" or _contains_any(text, ("why is this card", "card evidence", "evidence for card")):
        return "card_evidence"
    if subject_type in {"commander", "partner_pair"} or _contains_any(text, ("commander evidence", "commander staples", "top 16 average")):
        return "commander_evidence"
    if subject_type in {"deck", "saved_deck"} or _contains_any(text, ("deck summary", "summarize deck", "deck health")):
        return "deck_summary"
    return "unknown"


def _evidence_needs_for(
    request: ChatQueryRequest,
    question_class: str,
    options: ChatQueryPlannerOptions,
) -> tuple[ChatEvidenceNeed, ...]:
    filters = _filters_from_request(request)
    if question_class == "unknown":
        return ()
    if question_class == "deck_summary":
        return (
            _need("need:deck-memory", "deck_memory", "Inspect deck memory summaries.", options.default_privacy_scope, ("deck_memory_summary",), filters),
            _need("need:evidence-inputs", "evidence_input_records", "Assemble deck evidence records.", "public", ("deck_memory_summary", "saved_analysis_summary"), filters),
        )
    if question_class == "card_evidence":
        return (
            _need("need:evidence-graph", "evidence_graph", "Build card evidence graph.", "public", ("recommendation_candidate", "innovation_signal"), filters),
            _need("need:source-conflicts", "source_conflicts", "Inspect card-related source conflicts.", "public", ("source_conflict",), filters, required=False),
        )
    if question_class == "commander_evidence":
        return (
            _need("need:frequency-pool", "frequency_pool", "Inspect commander frequency evidence.", "public", ("recommendation_candidate",), filters),
            _need("need:evidence-graph", "evidence_graph", "Build commander evidence graph.", "public", ("recommendation_candidate", "innovation_signal"), filters),
        )
    if question_class == "comparison":
        return (
            _need("need:deck-memory", "deck_memory", "Inspect compared deck context.", options.default_privacy_scope, ("deck_memory_summary",), filters),
            _need("need:frequency-pool", "frequency_pool", "Inspect comparison pool evidence.", "public", ("recommendation_candidate",), filters),
        )
    if question_class == "source_conflict":
        return (_need("need:source-conflicts", "source_conflicts", "Inspect source conflict records.", "public", ("source_conflict",), filters),)
    if question_class == "unsupported_card":
        return (_need("need:unsupported-cards", "unsupported_cards", "Inspect unsupported relevant card queue.", "public", ("unsupported_card",), filters),)
    if question_class == "simulation_review":
        return (
            _need("need:simulation-review", "simulation_review_summary", "Inspect simulation review summaries.", "public", ("simulation_review_summary",), filters),
            _need("need:unsupported-cards", "unsupported_cards", "Inspect unsupported simulator card caveats.", "public", ("unsupported_card",), filters, required=False),
        )
    if question_class == "primer_metadata":
        return (_need("need:primer-metadata", "primer_metadata", "Inspect primer metadata records.", "public", ("primer_metadata",), filters),)
    if question_class == "innovation_signal":
        return (_need("need:innovation-signal", "innovation_signal", "Inspect innovation signal records.", "public", ("innovation_signal",), filters),)
    if question_class == "tag_graph":
        return (_need("need:tag-graph", "tag_graph", "Inspect functional tag graph evidence.", "public", ("manual_note",), filters),)
    if question_class == "export_request":
        return (_need("need:saved-analysis", "saved_analysis", "Inspect exportable saved analysis summaries.", options.default_privacy_scope, ("saved_analysis_summary",), filters),)
    return ()


def _need(
    need_id: str,
    need_type: str,
    reason: str,
    privacy_scope: str,
    record_types: tuple[str, ...],
    filters: dict[str, Any],
    required: bool = True,
) -> ChatEvidenceNeed:
    return ChatEvidenceNeed(
        need_id=need_id,
        need_type=need_type,
        reason=reason,
        required=required,
        privacy_scope=privacy_scope,
        record_types=record_types,
        filters=filters,
        metadata={},
    )


def _privacy_blockers_and_caveats(
    evidence_needs: tuple[ChatEvidenceNeed, ...],
    request: ChatQueryRequest,
    options: ChatQueryPlannerOptions,
) -> tuple[tuple[dict[str, Any], ...], tuple[dict[str, Any], ...]]:
    blockers: list[dict[str, Any]] = []
    caveats: list[dict[str, Any]] = []
    allowed = set(request.allowed_privacy_scopes)
    for need in evidence_needs:
        if need.privacy_scope == "sensitive" and not options.allow_sensitive:
            blockers.append(_privacy_blocker(need, "sensitive scope is disabled"))
        if need.privacy_scope == "local_user_data" and not options.allow_local_user_data:
            blockers.append(_privacy_blocker(need, "local_user_data scope is disabled"))
        if need.privacy_scope not in allowed:
            caveats.append(
                {
                    "caveat_type": "privacy_scope_not_allowed",
                    "message": "An evidence need requires a privacy scope outside the request allowance.",
                    "severity": "warning" if need.required else "info",
                    "metadata": {"need_id": need.need_id, "privacy_scope": need.privacy_scope},
                }
            )
    return tuple(blockers), tuple(caveats)


def _privacy_blocker(need: ChatEvidenceNeed, reason: str) -> dict[str, Any]:
    return {
        "blocker_type": "privacy_scope_blocked",
        "message": reason,
        "required": need.required,
        "metadata": {"need_id": need.need_id, "privacy_scope": need.privacy_scope},
    }


def _operations_for(question_class: str, evidence_needs: tuple[ChatEvidenceNeed, ...]) -> tuple[str, ...]:
    operations: set[str] = {"assemble_evidence_inputs"}
    if any(need.need_type == "evidence_graph" for need in evidence_needs):
        operations.add("build_evidence_graph")
    mapping = {
        "source_conflicts": "inspect_source_conflicts",
        "unsupported_cards": "inspect_unsupported_cards",
        "deck_memory": "inspect_deck_memory",
        "saved_analysis": "inspect_saved_analysis",
        "simulation_review_summary": "inspect_simulation_review",
        "primer_metadata": "inspect_primer_metadata",
        "innovation_signal": "inspect_innovation_signal",
        "frequency_pool": "inspect_frequency_pool",
        "tag_graph": "inspect_tag_graph",
    }
    for need in evidence_needs:
        operation = mapping.get(need.need_type)
        if operation:
            operations.add(operation)
    if question_class == "unknown":
        operations = {"return_caveated_unknown"}
    return tuple(sorted(operations))


def _filters_from_request(request: ChatQueryRequest) -> dict[str, Any]:
    return {constraint.constraint_type: constraint.value for constraint in request.constraints}


def _subject_to_dict(subject: ChatQuerySubject) -> dict[str, Any]:
    return {
        "subject_type": subject.subject_type,
        "subject_key": subject.subject_key,
        "display_name": subject.display_name,
        "metadata": _sorted_json_object(subject.metadata),
    }


def _need_to_dict(need: ChatEvidenceNeed) -> dict[str, Any]:
    return {
        "need_id": need.need_id,
        "need_type": need.need_type,
        "reason": need.reason,
        "required": need.required,
        "privacy_scope": need.privacy_scope,
        "record_types": list(need.record_types),
        "filters": _sorted_json_object(need.filters),
        "metadata": _sorted_json_object(need.metadata),
    }


def _constraint_to_dict(constraint: ChatQueryConstraint) -> dict[str, Any]:
    return {
        "constraint_id": constraint.constraint_id,
        "constraint_type": constraint.constraint_type,
        "value": constraint.value,
        "required": constraint.required,
        "metadata": _sorted_json_object(constraint.metadata),
    }


def _normalized_text(text: str) -> str:
    return " ".join(text.strip().lower().split())


def _contains_any(text: str, fragments: tuple[str, ...]) -> bool:
    return any(fragment in text for fragment in fragments)


def _validate_text(text: str, field_name: str) -> str:
    _require_text(text, field_name)
    normalized = _normalized_text(text)
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment in normalized:
            raise ChatQueryPlanBuildError(f"unsupported strategic claim text: {fragment}")
    return text.strip()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ChatQueryPlanBuildError(f"{field_name} is required")


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    _require_text(value, field_name)
    normalized = value.strip().lower()
    if normalized not in allowed:
        raise ChatQueryPlanBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise ChatQueryPlanBuildError("metadata must be an object")
    _reject_forbidden_metadata(metadata)
    return _validate_json_value(metadata, "metadata")


def _validate_json_value(value: Any, field_name: str) -> Any:
    _reject_forbidden_metadata(value)
    try:
        encoded = json.dumps(value, sort_keys=True)
        decoded = json.loads(encoded)
    except (TypeError, ValueError) as exc:
        raise ChatQueryPlanBuildError(f"{field_name} must be JSON-compatible") from exc
    return decoded


def _reject_forbidden_metadata(value: Any) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            normalized_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise ChatQueryPlanBuildError(f"metadata contains forbidden private field: {key}")
            _reject_forbidden_metadata(nested)
    elif isinstance(value, list):
        for item in value:
            _reject_forbidden_metadata(item)


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
