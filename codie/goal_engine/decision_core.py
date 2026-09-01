"""Pure, immutable, caller-input Read-Only Decision Core records.

This module produces advisory assessments only.  It cannot select work, create
an active Goal, grant authority, persist data, or perform I/O.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from .foundation import semantic_hash

DECISION_INPUT_SCHEMA_VERSION = "codie.goal_engine.decision_input.v1"
DECISION_ASSESSMENT_SCHEMA_VERSION = "codie.goal_engine.decision_assessment.v1"
GOAL_CANDIDATE_SCHEMA_VERSION = "codie.goal_engine.goal_candidate.v1"
DRAFT_GOAL_CONTRACT_SCHEMA_VERSION = "codie.goal_engine.draft_goal_contract.v1"
DECISION_EVIDENCE_REFERENCE_SCHEMA_VERSION = "codie.goal_engine.decision_evidence_reference.v1"
DECISION_LIMITATION_SCHEMA_VERSION = "codie.goal_engine.decision_limitation.v1"
ASSESSMENT_VALUES = frozenset({"HEALTHY_IDLE", "GOAL_CANDIDATE"})
_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9:._/-]*\Z")
_SHA_RE = re.compile(r"[0-9a-f]{64}\Z")


class GoalEngineDecisionError(ValueError):
    """Raised when caller input violates the Decision Core v1 contract."""


@dataclass(frozen=True)
class DecisionEvidenceReference:
    evidence_ref_id: str
    semantic_hash: str
    evidence_class: str
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _id(self.evidence_ref_id, "evidence_ref_id"); _sha(self.semantic_hash, "semantic_hash")
        _text(self.evidence_class, "evidence_class")
        object.__setattr__(self, "limitations", _texts(self.limitations, "limitations", True))
        _schema(self.schema_version, DECISION_EVIDENCE_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class DecisionLimitation:
    limitation_id: str
    statement: str
    schema_version: str

    def __post_init__(self) -> None:
        _id(self.limitation_id, "limitation_id"); _text(self.statement, "statement")
        _schema(self.schema_version, DECISION_LIMITATION_SCHEMA_VERSION)


@dataclass(frozen=True)
class DecisionInput:
    decision_id: str
    observed_problem: str | None
    evidence: tuple[DecisionEvidenceReference, ...]
    conflict_ref_ids: tuple[str, ...]
    limitations: tuple[DecisionLimitation, ...]
    historical_attempt_ref_ids: tuple[str, ...]
    policy_ref_ids: tuple[str, ...]
    human_decision_ref_ids: tuple[str, ...]
    root_cause_hypothesis: str | None
    root_cause_confidence: float | None
    proposed_intervention: str | None
    alternatives: tuple[str, ...]
    disconfirmation_criteria: tuple[str, ...]
    expected_affected_systems: tuple[str, ...]
    expected_unaffected_systems: tuple[str, ...]
    dependencies: tuple[str, ...]
    experiment_needed: bool
    as_of: str
    schema_version: str

    def __post_init__(self) -> None:
        _id(self.decision_id, "decision_id"); object.__setattr__(self, "evidence", _records(self.evidence, DecisionEvidenceReference, "evidence", lambda x: x.evidence_ref_id))
        object.__setattr__(self, "conflict_ref_ids", _ids(self.conflict_ref_ids, "conflict_ref_ids"))
        object.__setattr__(self, "limitations", _records(self.limitations, DecisionLimitation, "limitations", lambda x: x.limitation_id))
        for name in ("historical_attempt_ref_ids", "policy_ref_ids", "human_decision_ref_ids", "dependencies"):
            object.__setattr__(self, name, _ids(getattr(self, name), name))
        for name in ("alternatives", "disconfirmation_criteria", "expected_affected_systems", "expected_unaffected_systems"):
            object.__setattr__(self, name, _texts(getattr(self, name), name))
        _optional_text(self.observed_problem, "observed_problem"); _optional_text(self.root_cause_hypothesis, "root_cause_hypothesis"); _optional_text(self.proposed_intervention, "proposed_intervention")
        if self.root_cause_confidence is not None and (not isinstance(self.root_cause_confidence, (int, float)) or isinstance(self.root_cause_confidence, bool) or not 0 <= self.root_cause_confidence <= 1): raise GoalEngineDecisionError("root_cause_confidence must be a ratio")
        if not isinstance(self.experiment_needed, bool): raise GoalEngineDecisionError("experiment_needed must be bool")
        _utc(self.as_of); _schema(self.schema_version, DECISION_INPUT_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalCandidate:
    candidate_id: str
    decision_id: str
    statement: str
    advisory: bool
    evidence_ref_ids: tuple[str, ...]
    limitation_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _id(self.candidate_id, "candidate_id"); _id(self.decision_id, "decision_id"); _text(self.statement, "statement")
        if self.advisory is not True: raise GoalEngineDecisionError("candidate must be advisory")
        object.__setattr__(self, "evidence_ref_ids", _ids(self.evidence_ref_ids, "evidence_ref_ids")); object.__setattr__(self, "limitation_ids", _ids(self.limitation_ids, "limitation_ids")); _schema(self.schema_version, GOAL_CANDIDATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class DraftGoalContract:
    draft_id: str
    candidate_id: str
    observed_problem: str
    acceptable_result: str
    maximum_acceptable_regressions: str
    root_cause_hypothesis: str | None
    root_cause_confidence: float | None
    proposed_intervention: str | None
    alternatives: tuple[str, ...]
    disconfirmation_criteria: tuple[str, ...]
    expected_affected_systems: tuple[str, ...]
    expected_unaffected_systems: tuple[str, ...]
    dependencies: tuple[str, ...]
    evidence_ref_ids: tuple[str, ...]
    historical_attempt_ref_ids: tuple[str, ...]
    limitation_ids: tuple[str, ...]
    approval_requirement: str
    advisory: bool
    schema_version: str

    def __post_init__(self) -> None:
        _id(self.draft_id, "draft_id"); _id(self.candidate_id, "candidate_id"); _text(self.observed_problem, "observed_problem"); _text(self.acceptable_result, "acceptable_result"); _text(self.maximum_acceptable_regressions, "maximum_acceptable_regressions"); _optional_text(self.root_cause_hypothesis, "root_cause_hypothesis"); _optional_text(self.proposed_intervention, "proposed_intervention"); _text(self.approval_requirement, "approval_requirement")
        if self.advisory is not True: raise GoalEngineDecisionError("draft must be advisory")
        for name in ("alternatives", "disconfirmation_criteria", "expected_affected_systems", "expected_unaffected_systems"): object.__setattr__(self, name, _texts(getattr(self, name), name))
        for name in ("dependencies", "evidence_ref_ids", "historical_attempt_ref_ids", "limitation_ids"): object.__setattr__(self, name, _ids(getattr(self, name), name))
        _schema(self.schema_version, DRAFT_GOAL_CONTRACT_SCHEMA_VERSION)


@dataclass(frozen=True)
class DecisionAssessment:
    decision_id: str
    disposition: str
    necessity: str
    evidence: str
    root_cause: str
    history: str
    actionability: str
    experiment_need: str
    intervention: str
    impact: str
    priority: str
    limitations: tuple[DecisionLimitation, ...]
    candidate: GoalCandidate | None
    draft_goal_contract: DraftGoalContract | None
    schema_version: str

    def __post_init__(self) -> None:
        _id(self.decision_id, "decision_id"); _allowed(self.disposition, ASSESSMENT_VALUES, "disposition")
        for name in ("necessity", "evidence", "root_cause", "history", "actionability", "experiment_need", "intervention", "impact", "priority"): _text(getattr(self, name), name)
        object.__setattr__(self, "limitations", _records(self.limitations, DecisionLimitation, "limitations", lambda x: x.limitation_id))
        if self.disposition == "HEALTHY_IDLE" and (self.candidate is not None or self.draft_goal_contract is not None): raise GoalEngineDecisionError("HEALTHY_IDLE cannot produce a candidate or draft")
        if self.disposition == "GOAL_CANDIDATE" and (self.candidate is None or self.draft_goal_contract is None): raise GoalEngineDecisionError("GOAL_CANDIDATE requires advisory candidate and draft")
        if self.candidate is not None and self.candidate.decision_id != self.decision_id: raise GoalEngineDecisionError("candidate decision mismatch")
        if self.candidate is not None and self.draft_goal_contract is not None and self.draft_goal_contract.candidate_id != self.candidate.candidate_id: raise GoalEngineDecisionError("draft candidate mismatch")
        _schema(self.schema_version, DECISION_ASSESSMENT_SCHEMA_VERSION)


def evaluate_read_only_decision(value: DecisionInput) -> DecisionAssessment:
    validate_decision_input(value)
    base = _assessment_text(value)
    actionable = bool(value.observed_problem and value.evidence and value.proposed_intervention)
    if not actionable:
        return build_healthy_idle_assessment(value, base)
    candidate = build_goal_candidate(value)
    draft = build_draft_goal_contract(value, candidate)
    return DecisionAssessment(value.decision_id, "GOAL_CANDIDATE", **base, limitations=value.limitations, candidate=candidate, draft_goal_contract=draft, schema_version=DECISION_ASSESSMENT_SCHEMA_VERSION)


def build_healthy_idle_assessment(value: DecisionInput, base: dict[str, str] | None = None) -> DecisionAssessment:
    validate_decision_input(value); base = base or _assessment_text(value)
    return DecisionAssessment(value.decision_id, "HEALTHY_IDLE", **base, limitations=value.limitations, candidate=None, draft_goal_contract=None, schema_version=DECISION_ASSESSMENT_SCHEMA_VERSION)


def build_goal_candidate(value: DecisionInput) -> GoalCandidate:
    validate_decision_input(value)
    if not (value.observed_problem and value.evidence and value.proposed_intervention): raise GoalEngineDecisionError("candidate requires observed problem, evidence, and proposed intervention")
    return GoalCandidate(f"candidate:{value.decision_id}", value.decision_id, value.observed_problem, True, tuple(x.evidence_ref_id for x in value.evidence), tuple(x.limitation_id for x in value.limitations), GOAL_CANDIDATE_SCHEMA_VERSION)


def build_draft_goal_contract(value: DecisionInput, candidate: GoalCandidate) -> DraftGoalContract:
    validate_decision_input(value)
    if candidate.decision_id != value.decision_id: raise GoalEngineDecisionError("candidate decision mismatch")
    return DraftGoalContract(f"draft:{value.decision_id}", candidate.candidate_id, value.observed_problem or "No observed problem supplied.", "Caller must supply acceptable result before approval.", "Caller must supply maximum acceptable regressions before approval.", value.root_cause_hypothesis, value.root_cause_confidence, value.proposed_intervention, value.alternatives, value.disconfirmation_criteria, value.expected_affected_systems, value.expected_unaffected_systems, value.dependencies, tuple(x.evidence_ref_id for x in value.evidence), value.historical_attempt_ref_ids, tuple(x.limitation_id for x in value.limitations), "Human review and separate approval remain required.", True, DRAFT_GOAL_CONTRACT_SCHEMA_VERSION)


def validate_decision_input(value: DecisionInput) -> DecisionInput:
    if not isinstance(value, DecisionInput): raise GoalEngineDecisionError("value must be DecisionInput")
    return value

def validate_decision_assessment(value: DecisionAssessment) -> DecisionAssessment:
    if not isinstance(value, DecisionAssessment): raise GoalEngineDecisionError("value must be DecisionAssessment")
    return value

def _assessment_text(value: DecisionInput) -> dict[str, str]:
    return {"necessity": "No evidence-backed actionability was established." if not value.observed_problem else "Caller-supplied consequence requires human review.", "evidence": "Caller-supplied support, conflicts, and limitations remain visible.", "root_cause": value.root_cause_hypothesis or "No root-cause hypothesis was supplied.", "history": "Caller-supplied historical references only.", "actionability": "A bounded investigation is advisory only.", "experiment_need": "A separate experiment remains unauthorized." if value.experiment_needed else "No experiment need was supplied.", "intervention": value.proposed_intervention or "No intervention was supplied.", "impact": "Caller-supplied expected effects only.", "priority": "Advisory rationale only; no rank, selection, or work order."}

def _id(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value): raise GoalEngineDecisionError(f"{name} must be a safe identifier")
    return value
def _sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _SHA_RE.fullmatch(value): raise GoalEngineDecisionError(f"{name} must be SHA-256")
    return value
def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\x00" in value or len(value) > 10000: raise GoalEngineDecisionError(f"{name} must be safe text")
    return value
def _optional_text(value: Any, name: str) -> None:
    if value is not None: _text(value, name)
def _schema(value: Any, expected: str) -> None:
    if value != expected: raise GoalEngineDecisionError(f"schema_version must be exactly {expected}")
def _allowed(value: Any, allowed: frozenset[str], name: str) -> str:
    if value not in allowed: raise GoalEngineDecisionError(f"{name} must be one of {sorted(allowed)}")
    return value
def _ids(values: Any, name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple): raise GoalEngineDecisionError(f"{name} must be tuple")
    result = tuple(sorted(_id(v, name) for v in values))
    if len(set(result)) != len(result): raise GoalEngineDecisionError(f"{name} duplicate")
    return result
def _texts(values: Any, name: str, required: bool = False) -> tuple[str, ...]:
    if not isinstance(values, tuple): raise GoalEngineDecisionError(f"{name} must be tuple")
    result = tuple(sorted(_text(v, name) for v in values))
    if required and not result: raise GoalEngineDecisionError(f"{name} cannot be empty")
    if len(set(result)) != len(result): raise GoalEngineDecisionError(f"{name} duplicate")
    return result
def _records(values: Any, expected: type, name: str, key: Any) -> tuple[Any, ...]:
    if not isinstance(values, tuple) or not all(isinstance(v, expected) for v in values): raise GoalEngineDecisionError(f"{name} must be tuple of {expected.__name__}")
    result = tuple(sorted(values, key=key))
    if len({key(v) for v in result}) != len(result): raise GoalEngineDecisionError(f"{name} duplicate")
    return result
def _utc(value: Any) -> None:
    try: parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as error: raise GoalEngineDecisionError("as_of must be UTC ISO-8601") from error
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed): raise GoalEngineDecisionError("as_of must be UTC")

def _to_dict(value: Any) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in value.__dataclass_fields__:
        item = getattr(value, name)
        result[name] = [_to_dict(x) if hasattr(x, "__dataclass_fields__") else x for x in item] if isinstance(item, tuple) else (_to_dict(item) if hasattr(item, "__dataclass_fields__") else item)
    return result
def decision_input_to_dict(value: DecisionInput) -> dict[str, Any]: return _to_dict(value)
def decision_assessment_to_dict(value: DecisionAssessment) -> dict[str, Any]: return _to_dict(value)
def goal_candidate_to_dict(value: GoalCandidate) -> dict[str, Any]: return _to_dict(value)
def draft_goal_contract_to_dict(value: DraftGoalContract) -> dict[str, Any]: return _to_dict(value)
def decision_evidence_reference_to_dict(value: DecisionEvidenceReference) -> dict[str, Any]: return _to_dict(value)
def decision_limitation_to_dict(value: DecisionLimitation) -> dict[str, Any]: return _to_dict(value)
def _fields(payload: Mapping[str, Any], expected: set[str]) -> dict[str, Any]:
    if not isinstance(payload, Mapping) or set(payload) != expected: raise GoalEngineDecisionError("payload fields must match exactly")
    return dict(payload)
def decision_evidence_reference_from_dict(payload: Mapping[str, Any]) -> DecisionEvidenceReference:
    data = _fields(payload, set(DecisionEvidenceReference.__dataclass_fields__))
    if not isinstance(data["limitations"], list): raise GoalEngineDecisionError("limitations must be JSON list")
    data["limitations"] = tuple(data["limitations"])
    return DecisionEvidenceReference(**data)
def decision_limitation_from_dict(payload: Mapping[str, Any]) -> DecisionLimitation:
    return DecisionLimitation(**_fields(payload, set(DecisionLimitation.__dataclass_fields__)))
def decision_input_from_dict(payload: Mapping[str, Any]) -> DecisionInput:
    data = _fields(payload, set(DecisionInput.__dataclass_fields__))
    for name in ("evidence", "limitations", "conflict_ref_ids", "historical_attempt_ref_ids", "policy_ref_ids", "human_decision_ref_ids", "alternatives", "disconfirmation_criteria", "expected_affected_systems", "expected_unaffected_systems", "dependencies"):
        if not isinstance(data[name], list): raise GoalEngineDecisionError(f"{name} must be JSON list")
    data["evidence"] = tuple(decision_evidence_reference_from_dict(x) for x in data["evidence"])
    data["limitations"] = tuple(decision_limitation_from_dict(x) for x in data["limitations"])
    for name in ("conflict_ref_ids", "historical_attempt_ref_ids", "policy_ref_ids", "human_decision_ref_ids", "alternatives", "disconfirmation_criteria", "expected_affected_systems", "expected_unaffected_systems", "dependencies"): data[name] = tuple(data[name])
    return DecisionInput(**data)
def goal_candidate_from_dict(payload: Mapping[str, Any]) -> GoalCandidate:
    data = _fields(payload, set(GoalCandidate.__dataclass_fields__))
    for name in ("evidence_ref_ids", "limitation_ids"):
        if not isinstance(data[name], list): raise GoalEngineDecisionError(f"{name} must be JSON list")
        data[name] = tuple(data[name])
    return GoalCandidate(**data)
def draft_goal_contract_from_dict(payload: Mapping[str, Any]) -> DraftGoalContract:
    data = _fields(payload, set(DraftGoalContract.__dataclass_fields__))
    for name in ("alternatives", "disconfirmation_criteria", "expected_affected_systems", "expected_unaffected_systems", "dependencies", "evidence_ref_ids", "historical_attempt_ref_ids", "limitation_ids"):
        if not isinstance(data[name], list): raise GoalEngineDecisionError(f"{name} must be JSON list")
        data[name] = tuple(data[name])
    return DraftGoalContract(**data)
def decision_assessment_from_dict(payload: Mapping[str, Any]) -> DecisionAssessment:
    data = _fields(payload, set(DecisionAssessment.__dataclass_fields__))
    if not isinstance(data["limitations"], list): raise GoalEngineDecisionError("limitations must be JSON list")
    data["limitations"] = tuple(decision_limitation_from_dict(x) for x in data["limitations"])
    if data["candidate"] is not None: data["candidate"] = goal_candidate_from_dict(data["candidate"])
    if data["draft_goal_contract"] is not None: data["draft_goal_contract"] = draft_goal_contract_from_dict(data["draft_goal_contract"])
    return DecisionAssessment(**data)
def decision_input_semantic_hash(value: DecisionInput) -> str: return semantic_hash(decision_input_to_dict(value))
def decision_assessment_semantic_hash(value: DecisionAssessment) -> str: return semantic_hash(decision_assessment_to_dict(value))
def goal_candidate_semantic_hash(value: GoalCandidate) -> str: return semantic_hash(goal_candidate_to_dict(value))
def draft_goal_contract_semantic_hash(value: DraftGoalContract) -> str: return semantic_hash(draft_goal_contract_to_dict(value))
