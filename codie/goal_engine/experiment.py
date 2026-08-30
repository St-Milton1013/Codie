"""Pure, immutable, caller-supplied Goal Experiment Engine records.

This module plans explicitly supplied expected experiments only.  It neither
discovers information nor grants authority, executes work, or reports results.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from .foundation import (
    GoalEvidenceReference,
    goal_evidence_reference_from_dict,
    goal_evidence_reference_to_dict,
    semantic_hash,
)
from .impact import (
    ChangeImpactAssessmentReference,
    RollbackAnalysis,
    change_impact_assessment_reference_from_dict,
    change_impact_assessment_reference_to_dict,
    rollback_analysis_from_dict,
    rollback_analysis_to_dict,
)

EXPERIMENT_QUESTION_SCHEMA_VERSION = "codie.goal_engine.experiment_question.v1"
EXPERIMENT_HYPOTHESIS_SCHEMA_VERSION = "codie.goal_engine.experiment_hypothesis.v1"
EXPERIMENT_INPUT_SCHEMA_VERSION = "codie.goal_engine.experiment_input.v1"
EXPERIMENT_BOUNDARY_SCHEMA_VERSION = "codie.goal_engine.experiment_boundary.v1"
EXPERIMENT_STOP_CRITERION_SCHEMA_VERSION = "codie.goal_engine.experiment_stop_criterion.v1"
EXPERIMENT_CLEANUP_PLAN_SCHEMA_VERSION = "codie.goal_engine.experiment_cleanup_plan.v1"
EXPERIMENT_APPROVAL_REFERENCE_SCHEMA_VERSION = "codie.goal_engine.experiment_approval_reference.v1"
EXPERIMENT_OBSERVATION_SCHEMA_VERSION = "codie.goal_engine.experiment_observation.v1"
EXPERIMENT_OUTCOME_SCHEMA_VERSION = "codie.goal_engine.experiment_outcome.v1"
GOAL_EXPERIMENT_SCHEMA_VERSION = "codie.goal_engine.goal_experiment.v1"
GOAL_EXPERIMENT_REFERENCE_SCHEMA_VERSION = "codie.goal_engine.goal_experiment_reference.v1"

EXPERIMENT_STATUSES = frozenset(
    {
        "DRAFT",
        "PROPOSED",
        "APPROVED_REFERENCE_RECORDED",
        "OBSERVED",
        "STOPPED",
        "CLOSED",
    }
)
INPUT_CLASSES = frozenset(
    {
        "CALLER_SUPPLIED",
        "FIXTURE",
        "SYNTHETIC",
        "PUBLIC_USER_INITIATED",
    }
)
BOUNDARY_KINDS = frozenset(
    {
        "SCOPE",
        "DATA",
        "PRIVACY",
        "SECURITY",
        "ZERO_COST",
        "MANUAL_BURDEN",
        "TIME",
        "RESOURCE",
        "NETWORK_DENIED",
        "PROVIDER_DENIED",
        "WRITE_DENIED",
    }
)
STOP_CRITERION_KINDS = frozenset(
    {
        "SAFETY",
        "PRIVACY",
        "COST",
        "SCOPE",
        "EVIDENCE",
        "HUMAN_REQUEST",
        "TIME",
        "RESOURCE",
        "VALIDATION",
    }
)
OBSERVATION_DISPOSITIONS = frozenset(
    {
        "OBSERVED",
        "NOT_OBSERVED",
        "INCONCLUSIVE",
        "BLOCKED",
    }
)
OUTCOME_DISPOSITIONS = frozenset(
    {
        "NOT_INTERPRETED",
        "SUPPORTS_HYPOTHESIS",
        "DOES_NOT_SUPPORT_HYPOTHESIS",
        "INCONCLUSIVE",
        "STOPPED",
    }
)

_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9:._/-]*\Z")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class GoalEngineExperimentError(ValueError):
    """Raised when a Goal Experiment record violates the v1 contract."""


@dataclass(frozen=True)
class ExperimentQuestion:
    question_id: str
    statement: str
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.question_id, "question_id")
        _require_text(self.statement, "statement")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_QUESTION_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentHypothesis:
    hypothesis_id: str
    statement: str
    expected_observation: str
    disconfirmation_criteria: tuple[str, ...]
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.hypothesis_id, "hypothesis_id")
        _require_text(self.statement, "statement")
        _require_text(self.expected_observation, "expected_observation")
        object.__setattr__(self, "disconfirmation_criteria", _text_tuple(self.disconfirmation_criteria, "disconfirmation_criteria", require_nonempty=True))
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_HYPOTHESIS_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentInput:
    input_id: str
    input_class: str
    subject: str
    description: str
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.input_id, "input_id")
        validate_input_class(self.input_class)
        _require_text(self.subject, "subject")
        _require_text(self.description, "description")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_INPUT_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentBoundary:
    boundary_id: str
    boundary_kind: str
    statement: str
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.boundary_id, "boundary_id")
        validate_boundary_kind(self.boundary_kind)
        _require_text(self.statement, "statement")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_BOUNDARY_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentStopCriterion:
    criterion_id: str
    criterion_kind: str
    statement: str
    human_review_required: bool
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.criterion_id, "criterion_id")
        validate_stop_criterion_kind(self.criterion_kind)
        _require_text(self.statement, "statement")
        _require_type(self.human_review_required, bool, "human_review_required")
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_STOP_CRITERION_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentCleanupPlan:
    cleanup_id: str
    statement: str
    preconditions: tuple[str, ...]
    validation_requirement_ids: tuple[str, ...]
    residual_risk_summary: str
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.cleanup_id, "cleanup_id")
        _require_text(self.statement, "statement")
        object.__setattr__(self, "preconditions", _text_tuple(self.preconditions, "preconditions"))
        object.__setattr__(self, "validation_requirement_ids", _id_tuple(self.validation_requirement_ids, "validation_requirement_ids"))
        _require_text(self.residual_risk_summary, "residual_risk_summary")
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_CLEANUP_PLAN_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentApprovalReference:
    approval_ref_id: str
    authority_kind: str
    decision_ref: str
    scope_statement: str
    recorded_at: str
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.approval_ref_id, "approval_ref_id")
        _require_text(self.authority_kind, "authority_kind")
        _require_text(self.decision_ref, "decision_ref")
        _require_text(self.scope_statement, "scope_statement")
        _require_utc_timestamp(self.recorded_at, "recorded_at")
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_APPROVAL_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentObservation:
    observation_id: str
    statement: str
    disposition: str
    observed_at: str
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.observation_id, "observation_id")
        _require_text(self.statement, "statement")
        validate_observation_disposition(self.disposition)
        _require_utc_timestamp(self.observed_at, "observed_at")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_OBSERVATION_SCHEMA_VERSION)


@dataclass(frozen=True)
class ExperimentOutcome:
    outcome_id: str
    disposition: str
    statement: str
    observation_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.outcome_id, "outcome_id")
        validate_outcome_disposition(self.disposition)
        _require_text(self.statement, "statement")
        object.__setattr__(self, "observation_ref_ids", _id_tuple(self.observation_ref_ids, "observation_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, EXPERIMENT_OUTCOME_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalExperimentReference:
    experiment_id: str
    revision: int
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.experiment_id, "experiment_id")
        _require_positive_int(self.revision, "revision")
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(self.schema_version, GOAL_EXPERIMENT_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalExperiment:
    experiment_id: str
    revision: int
    question: ExperimentQuestion
    hypothesis: ExperimentHypothesis
    inputs: tuple[ExperimentInput, ...]
    boundaries: tuple[ExperimentBoundary, ...]
    stop_criteria: tuple[ExperimentStopCriterion, ...]
    cleanup_plan: ExperimentCleanupPlan
    rollback: RollbackAnalysis
    approval_references: tuple[ExperimentApprovalReference, ...]
    observations: tuple[ExperimentObservation, ...]
    outcome: ExperimentOutcome | None
    impact_assessment_ref: ChangeImpactAssessmentReference | None
    evidence_snapshot: tuple[GoalEvidenceReference, ...]
    as_of: str
    supersedes_experiment: GoalExperimentReference | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.experiment_id, "experiment_id")
        _require_positive_int(self.revision, "revision")
        _require_type(self.question, ExperimentQuestion, "question")
        _require_type(self.hypothesis, ExperimentHypothesis, "hypothesis")
        object.__setattr__(self, "inputs", _record_tuple(self.inputs, ExperimentInput, "inputs", lambda item: item.input_id))
        object.__setattr__(self, "boundaries", _record_tuple(self.boundaries, ExperimentBoundary, "boundaries", lambda item: item.boundary_id))
        object.__setattr__(self, "stop_criteria", _record_tuple(self.stop_criteria, ExperimentStopCriterion, "stop_criteria", lambda item: item.criterion_id))
        _require_type(self.cleanup_plan, ExperimentCleanupPlan, "cleanup_plan")
        _require_type(self.rollback, RollbackAnalysis, "rollback")
        object.__setattr__(self, "approval_references", _record_tuple(self.approval_references, ExperimentApprovalReference, "approval_references", lambda item: item.approval_ref_id))
        object.__setattr__(self, "observations", _record_tuple(self.observations, ExperimentObservation, "observations", lambda item: item.observation_id))
        _require_optional_type(self.outcome, ExperimentOutcome, "outcome")
        _require_optional_type(self.impact_assessment_ref, ChangeImpactAssessmentReference, "impact_assessment_ref")
        _require_utc_timestamp(self.as_of, "as_of")
        _require_optional_type(self.supersedes_experiment, GoalExperimentReference, "supersedes_experiment")
        if self.revision == 1:
            if self.supersedes_experiment is not None:
                raise GoalEngineExperimentError("experiment revision 1 cannot supersede an earlier experiment")
        elif self.supersedes_experiment is None:
            raise GoalEngineExperimentError("later experiment revision requires supersedes_experiment")
        _require_schema(self.schema_version, GOAL_EXPERIMENT_SCHEMA_VERSION)
        validate_goal_experiment(self)


def validate_input_class(value: str) -> str:
    return _require_allowed(value, INPUT_CLASSES, "input class")


def validate_boundary_kind(value: str) -> str:
    return _require_allowed(value, BOUNDARY_KINDS, "boundary kind")


def validate_stop_criterion_kind(value: str) -> str:
    return _require_allowed(value, STOP_CRITERION_KINDS, "stop criterion kind")


def validate_observation_disposition(value: str) -> str:
    return _require_allowed(value, OBSERVATION_DISPOSITIONS, "observation disposition")


def validate_outcome_disposition(value: str) -> str:
    return _require_allowed(value, OUTCOME_DISPOSITIONS, "outcome disposition")


def validate_goal_experiment(experiment: GoalExperiment) -> GoalExperiment:
    _require_type(experiment, GoalExperiment, "experiment")
    evidence_ids = {item.evidence_ref_id for item in experiment.evidence_snapshot}
    # Validate that all references are resolved
    _require_resolved(experiment.question.evidence_ref_ids, evidence_ids, "question evidence_ref_ids")
    _require_resolved(experiment.hypothesis.evidence_ref_ids, evidence_ids, "hypothesis evidence_ref_ids")
    for input_item in experiment.inputs:
        _require_resolved(input_item.evidence_ref_ids, evidence_ids, "input evidence_ref_ids")
    for boundary in experiment.boundaries:
        _require_resolved(boundary.evidence_ref_ids, evidence_ids, "boundary evidence_ref_ids")
    # ExperimentStopCriterion carries no evidence_ref_ids field (contract §
    # "Required Immutable Records"), so stop criteria have nothing to resolve
    # here. ExperimentCleanupPlan.validation_requirement_ids reference
    # validation requirements on the associated Change/Impact assessment,
    # which is not itself part of this record (only a reference to it is,
    # via impact_assessment_ref) — there is no snapshot to resolve against
    # inside GoalExperiment, so those IDs remain caller-supplied and opaque
    # here, validated only as well-formed IDs at construction time.
    for _approval in experiment.approval_references:
        # No references to resolve here
        pass
    for observation in experiment.observations:
        _require_resolved(observation.evidence_ref_ids, evidence_ids, "observation evidence_ref_ids")
    if experiment.outcome is not None:
        _require_resolved(experiment.outcome.observation_ref_ids, {obs.observation_id for obs in experiment.observations}, "outcome observation_ref_ids")
    return experiment


def validate_goal_experiment_revision(
    experiment: GoalExperiment,
    prior_experiment: GoalExperiment,
) -> GoalExperiment:
    validate_goal_experiment(experiment)
    validate_goal_experiment(prior_experiment)
    if experiment.experiment_id != prior_experiment.experiment_id:
        raise GoalEngineExperimentError("experiment revision must retain experiment_id")
    if experiment.revision != prior_experiment.revision + 1:
        raise GoalEngineExperimentError("experiment revision must be the next exact revision")
    reference = experiment.supersedes_experiment
    if reference is None:
        raise GoalEngineExperimentError("later experiment revision requires supersedes_experiment")
    if reference.experiment_id != prior_experiment.experiment_id or reference.revision != prior_experiment.revision:
        raise GoalEngineExperimentError("supersedes_experiment must reference the immediately prior revision")
    if reference.semantic_hash != goal_experiment_semantic_hash(prior_experiment):
        raise GoalEngineExperimentError("supersedes_experiment semantic hash must match the immediately prior revision")
    if _timestamp(experiment.as_of, "as_of") < _timestamp(prior_experiment.as_of, "prior as_of"):
        raise GoalEngineExperimentError("later experiment as_of cannot precede the prior experiment")
    # Check that core components are unchanged
    if experiment.question != prior_experiment.question:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior question")
    if experiment.hypothesis != prior_experiment.hypothesis:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior hypothesis")
    if experiment.inputs != prior_experiment.inputs:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior inputs")
    if experiment.boundaries != prior_experiment.boundaries:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior boundaries")
    if experiment.stop_criteria != prior_experiment.stop_criteria:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior stop criteria")
    if experiment.cleanup_plan != prior_experiment.cleanup_plan:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior cleanup plan")
    if experiment.rollback != prior_experiment.rollback:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior rollback analysis")
    _require_append_only(
        experiment.approval_references,
        prior_experiment.approval_references,
        lambda item: item.approval_ref_id,
        "approval_references",
    )
    _require_append_only(
        experiment.observations,
        prior_experiment.observations,
        lambda item: item.observation_id,
        "observations",
    )
    # Outcome is not append-only, but we can't rewrite it if it exists
    if prior_experiment.outcome is not None and experiment.outcome != prior_experiment.outcome:
        raise GoalEngineExperimentError("experiment revision cannot rewrite the prior outcome")
    return experiment


def build_goal_experiment(
    *,
    experiment_id: str,
    revision: int,
    question: ExperimentQuestion,
    hypothesis: ExperimentHypothesis,
    inputs: tuple[ExperimentInput, ...],
    boundaries: tuple[ExperimentBoundary, ...],
    stop_criteria: tuple[ExperimentStopCriterion, ...],
    cleanup_plan: ExperimentCleanupPlan,
    rollback: RollbackAnalysis,
    approval_references: tuple[ExperimentApprovalReference, ...],
    observations: tuple[ExperimentObservation, ...],
    outcome: ExperimentOutcome | None,
    impact_assessment_ref: ChangeImpactAssessmentReference | None,
    evidence_snapshot: tuple[GoalEvidenceReference, ...],
    as_of: str,
    supersedes_experiment: GoalExperimentReference | None = None,
    prior_experiment: GoalExperiment | None = None,
) -> GoalExperiment:
    """Package explicitly supplied planning inputs into one immutable experiment."""
    experiment = GoalExperiment(
        experiment_id=experiment_id,
        revision=revision,
        question=question,
        hypothesis=hypothesis,
        inputs=inputs,
        boundaries=boundaries,
        stop_criteria=stop_criteria,
        cleanup_plan=cleanup_plan,
        rollback=rollback,
        approval_references=approval_references,
        observations=observations,
        outcome=outcome,
        impact_assessment_ref=impact_assessment_ref,
        evidence_snapshot=evidence_snapshot,
        as_of=as_of,
        supersedes_experiment=supersedes_experiment,
        schema_version=GOAL_EXPERIMENT_SCHEMA_VERSION,
    )
    if prior_experiment is not None:
        validate_goal_experiment_revision(experiment, prior_experiment)
    elif revision > 1:
        raise GoalEngineExperimentError("prior_experiment is required for a later experiment revision")
    return experiment


def experiment_question_to_dict(value: ExperimentQuestion) -> dict[str, Any]:
    _require_type(value, ExperimentQuestion, "value")
    return {
        "question_id": value.question_id,
        "statement": value.statement,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_question_from_dict(payload: Mapping[str, Any]) -> ExperimentQuestion:
    data = _fields(payload, {"question_id", "statement", "evidence_ref_ids", "limitations", "schema_version"})
    for name in ("evidence_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentQuestion(**data)


def experiment_hypothesis_to_dict(value: ExperimentHypothesis) -> dict[str, Any]:
    _require_type(value, ExperimentHypothesis, "value")
    return {
        "hypothesis_id": value.hypothesis_id,
        "statement": value.statement,
        "expected_observation": value.expected_observation,
        "disconfirmation_criteria": list(value.disconfirmation_criteria),
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_hypothesis_from_dict(payload: Mapping[str, Any]) -> ExperimentHypothesis:
    data = _fields(payload, {"hypothesis_id", "statement", "expected_observation", "disconfirmation_criteria", "evidence_ref_ids", "limitations", "schema_version"})
    for name in ("disconfirmation_criteria", "evidence_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentHypothesis(**data)


def experiment_input_to_dict(value: ExperimentInput) -> dict[str, Any]:
    _require_type(value, ExperimentInput, "value")
    return {
        "input_id": value.input_id,
        "input_class": value.input_class,
        "subject": value.subject,
        "description": value.description,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_input_from_dict(payload: Mapping[str, Any]) -> ExperimentInput:
    data = _fields(payload, {"input_id", "input_class", "subject", "description", "evidence_ref_ids", "limitations", "schema_version"})
    for name in ("evidence_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentInput(**data)


def experiment_boundary_to_dict(value: ExperimentBoundary) -> dict[str, Any]:
    _require_type(value, ExperimentBoundary, "value")
    return {
        "boundary_id": value.boundary_id,
        "boundary_kind": value.boundary_kind,
        "statement": value.statement,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_boundary_from_dict(payload: Mapping[str, Any]) -> ExperimentBoundary:
    data = _fields(payload, {"boundary_id", "boundary_kind", "statement", "evidence_ref_ids", "limitations", "schema_version"})
    for name in ("evidence_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentBoundary(**data)


def experiment_stop_criterion_to_dict(value: ExperimentStopCriterion) -> dict[str, Any]:
    _require_type(value, ExperimentStopCriterion, "value")
    return {
        "criterion_id": value.criterion_id,
        "criterion_kind": value.criterion_kind,
        "statement": value.statement,
        "human_review_required": value.human_review_required,
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_stop_criterion_from_dict(payload: Mapping[str, Any]) -> ExperimentStopCriterion:
    data = _fields(payload, {"criterion_id", "criterion_kind", "statement", "human_review_required", "limitations", "schema_version"})
    data["limitations"] = _json_tuple(data["limitations"], "limitations")
    return ExperimentStopCriterion(**data)


def experiment_cleanup_plan_to_dict(value: ExperimentCleanupPlan) -> dict[str, Any]:
    _require_type(value, ExperimentCleanupPlan, "value")
    return {
        "cleanup_id": value.cleanup_id,
        "statement": value.statement,
        "preconditions": list(value.preconditions),
        "validation_requirement_ids": list(value.validation_requirement_ids),
        "residual_risk_summary": value.residual_risk_summary,
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_cleanup_plan_from_dict(payload: Mapping[str, Any]) -> ExperimentCleanupPlan:
    data = _fields(payload, {"cleanup_id", "statement", "preconditions", "validation_requirement_ids", "residual_risk_summary", "limitations", "schema_version"})
    for name in ("preconditions", "validation_requirement_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentCleanupPlan(**data)


def experiment_approval_reference_to_dict(value: ExperimentApprovalReference) -> dict[str, Any]:
    _require_type(value, ExperimentApprovalReference, "value")
    return {
        "approval_ref_id": value.approval_ref_id,
        "authority_kind": value.authority_kind,
        "decision_ref": value.decision_ref,
        "scope_statement": value.scope_statement,
        "recorded_at": value.recorded_at,
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_approval_reference_from_dict(payload: Mapping[str, Any]) -> ExperimentApprovalReference:
    data = _fields(payload, {"approval_ref_id", "authority_kind", "decision_ref", "scope_statement", "recorded_at", "limitations", "schema_version"})
    data["limitations"] = _json_tuple(data["limitations"], "limitations")
    return ExperimentApprovalReference(**data)


def experiment_observation_to_dict(value: ExperimentObservation) -> dict[str, Any]:
    _require_type(value, ExperimentObservation, "value")
    return {
        "observation_id": value.observation_id,
        "statement": value.statement,
        "disposition": value.disposition,
        "observed_at": value.observed_at,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_observation_from_dict(payload: Mapping[str, Any]) -> ExperimentObservation:
    data = _fields(payload, {"observation_id", "statement", "disposition", "observed_at", "evidence_ref_ids", "limitations", "schema_version"})
    for name in ("evidence_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentObservation(**data)


def experiment_outcome_to_dict(value: ExperimentOutcome) -> dict[str, Any]:
    _require_type(value, ExperimentOutcome, "value")
    return {
        "outcome_id": value.outcome_id,
        "disposition": value.disposition,
        "statement": value.statement,
        "observation_ref_ids": list(value.observation_ref_ids),
        "limitations": list(value.limitations),
        "schema_version": value.schema_version,
    }


def experiment_outcome_from_dict(payload: Mapping[str, Any]) -> ExperimentOutcome:
    data = _fields(payload, {"outcome_id", "disposition", "statement", "observation_ref_ids", "limitations", "schema_version"})
    for name in ("observation_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ExperimentOutcome(**data)


def goal_experiment_reference_to_dict(value: GoalExperimentReference) -> dict[str, Any]:
    _require_type(value, GoalExperimentReference, "value")
    return {
        "experiment_id": value.experiment_id,
        "revision": value.revision,
        "semantic_hash": value.semantic_hash,
        "schema_version": value.schema_version,
    }


def goal_experiment_reference_from_dict(payload: Mapping[str, Any]) -> GoalExperimentReference:
    data = _fields(payload, {"experiment_id", "revision", "semantic_hash", "schema_version"})
    return GoalExperimentReference(**data)


def goal_experiment_to_dict(value: GoalExperiment) -> dict[str, Any]:
    _require_type(value, GoalExperiment, "value")
    return {
        "experiment_id": value.experiment_id,
        "revision": value.revision,
        "question": experiment_question_to_dict(value.question),
        "hypothesis": experiment_hypothesis_to_dict(value.hypothesis),
        "inputs": [experiment_input_to_dict(item) for item in value.inputs],
        "boundaries": [experiment_boundary_to_dict(item) for item in value.boundaries],
        "stop_criteria": [experiment_stop_criterion_to_dict(item) for item in value.stop_criteria],
        "cleanup_plan": experiment_cleanup_plan_to_dict(value.cleanup_plan),
        "rollback": rollback_analysis_to_dict(value.rollback),
        "approval_references": [experiment_approval_reference_to_dict(item) for item in value.approval_references],
        "observations": [experiment_observation_to_dict(item) for item in value.observations],
        "outcome": experiment_outcome_to_dict(value.outcome) if value.outcome else None,
        "impact_assessment_ref": change_impact_assessment_reference_to_dict(value.impact_assessment_ref) if value.impact_assessment_ref else None,
        "evidence_snapshot": [goal_evidence_reference_to_dict(item) for item in value.evidence_snapshot],
        "as_of": value.as_of,
        "supersedes_experiment": goal_experiment_reference_to_dict(value.supersedes_experiment) if value.supersedes_experiment else None,
        "schema_version": value.schema_version,
    }


def goal_experiment_from_dict(payload: Mapping[str, Any]) -> GoalExperiment:
    data = _fields(payload, {"experiment_id", "revision", "question", "hypothesis", "inputs", "boundaries", "stop_criteria", "cleanup_plan", "rollback", "approval_references", "observations", "outcome", "impact_assessment_ref", "evidence_snapshot", "as_of", "supersedes_experiment", "schema_version"})
    data["question"] = experiment_question_from_dict(_mapping(data["question"], "question"))
    data["hypothesis"] = experiment_hypothesis_from_dict(_mapping(data["hypothesis"], "hypothesis"))
    data["inputs"] = tuple(experiment_input_from_dict(_mapping(item, "input")) for item in _json_tuple(data["inputs"], "inputs"))
    data["boundaries"] = tuple(experiment_boundary_from_dict(_mapping(item, "boundary")) for item in _json_tuple(data["boundaries"], "boundaries"))
    data["stop_criteria"] = tuple(experiment_stop_criterion_from_dict(_mapping(item, "stop_criterion")) for item in _json_tuple(data["stop_criteria"], "stop_criteria"))
    data["cleanup_plan"] = experiment_cleanup_plan_from_dict(_mapping(data["cleanup_plan"], "cleanup_plan"))
    data["rollback"] = rollback_analysis_from_dict(_mapping(data["rollback"], "rollback"))
    data["approval_references"] = tuple(experiment_approval_reference_from_dict(_mapping(item, "approval_reference")) for item in _json_tuple(data["approval_references"], "approval_references"))
    data["observations"] = tuple(experiment_observation_from_dict(_mapping(item, "observation")) for item in _json_tuple(data["observations"], "observations"))
    if data["outcome"] is not None:
        data["outcome"] = experiment_outcome_from_dict(_mapping(data["outcome"], "outcome"))
    if data["impact_assessment_ref"] is not None:
        data["impact_assessment_ref"] = change_impact_assessment_reference_from_dict(_mapping(data["impact_assessment_ref"], "impact_assessment_ref"))
    data["evidence_snapshot"] = tuple(goal_evidence_reference_from_dict(_mapping(item, "evidence")) for item in _json_tuple(data["evidence_snapshot"], "evidence_snapshot"))
    if data["supersedes_experiment"] is not None:
        data["supersedes_experiment"] = goal_experiment_reference_from_dict(_mapping(data["supersedes_experiment"], "supersedes_experiment"))
    return GoalExperiment(**data)


def experiment_question_semantic_hash(value: ExperimentQuestion) -> str:
    return semantic_hash(experiment_question_to_dict(value))


def experiment_hypothesis_semantic_hash(value: ExperimentHypothesis) -> str:
    return semantic_hash(experiment_hypothesis_to_dict(value))


def experiment_input_semantic_hash(value: ExperimentInput) -> str:
    return semantic_hash(experiment_input_to_dict(value))


def experiment_boundary_semantic_hash(value: ExperimentBoundary) -> str:
    return semantic_hash(experiment_boundary_to_dict(value))


def experiment_stop_criterion_semantic_hash(value: ExperimentStopCriterion) -> str:
    return semantic_hash(experiment_stop_criterion_to_dict(value))


def experiment_cleanup_plan_semantic_hash(value: ExperimentCleanupPlan) -> str:
    return semantic_hash(experiment_cleanup_plan_to_dict(value))


def experiment_approval_reference_semantic_hash(value: ExperimentApprovalReference) -> str:
    return semantic_hash(experiment_approval_reference_to_dict(value))


def experiment_observation_semantic_hash(value: ExperimentObservation) -> str:
    return semantic_hash(experiment_observation_to_dict(value))


def experiment_outcome_semantic_hash(value: ExperimentOutcome) -> str:
    return semantic_hash(experiment_outcome_to_dict(value))


def goal_experiment_reference_semantic_hash(value: GoalExperimentReference) -> str:
    return semantic_hash(goal_experiment_reference_to_dict(value))


def goal_experiment_semantic_hash(value: GoalExperiment) -> str:
    return semantic_hash(goal_experiment_to_dict(value))


def _fields(payload: Mapping[str, Any], expected: set[str]) -> dict[str, Any]:
    mapping = _mapping(payload, "payload")
    actual = set(mapping)
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise GoalEngineExperimentError(f"payload fields must match exactly; missing={missing}, unexpected={unexpected}")
    return dict(mapping)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GoalEngineExperimentError(f"{field_name} must be a mapping")
    return value


def _json_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise GoalEngineExperimentError(f"{field_name} must be a JSON list")
    return tuple(value)


def _record_tuple(values: Any, expected_type: type, field_name: str, key: Any) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineExperimentError(f"{field_name} must be a tuple")
    for value in values:
        _require_type(value, expected_type, field_name)
    ordered = tuple(sorted(values, key=key))
    if len({key(value) for value in ordered}) != len(ordered):
        raise GoalEngineExperimentError(f"{field_name} cannot contain duplicate identities")
    return ordered


def _id_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineExperimentError(f"{field_name} must be a tuple")
    result = tuple(sorted(_require_id(value, field_name) for value in values))
    if len(set(result)) != len(result):
        raise GoalEngineExperimentError(f"{field_name} cannot contain duplicates")
    return result


def _text_tuple(values: Any, field_name: str, require_nonempty: bool = False) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineExperimentError(f"{field_name} must be a tuple")
    result = tuple(sorted(_require_text(value, field_name) for value in values))
    if require_nonempty and not result:
        raise GoalEngineExperimentError(f"{field_name} cannot be empty")
    if len(set(result)) != len(result):
        raise GoalEngineExperimentError(f"{field_name} cannot contain duplicates")
    return result


def _require_resolved(values: tuple[str, ...], allowed: set[str], field_name: str) -> None:
    missing = sorted(set(values) - allowed)
    if missing:
        raise GoalEngineExperimentError(f"{field_name} contains unresolved references: {missing}")


def _require_append_only(current: tuple[Any, ...], prior: tuple[Any, ...], key: Any, field_name: str) -> None:
    current_by_key = {key(item): item for item in current}
    for prior_item in prior:
        item_key = key(prior_item)
        if current_by_key.get(item_key) != prior_item:
            raise GoalEngineExperimentError(f"experiment revision cannot remove or rewrite prior {field_name}")


def _require_disjoint(left: tuple[str, ...], right: tuple[str, ...], left_name: str, right_name: str) -> None:
    overlap = sorted(set(left) & set(right))
    if overlap:
        raise GoalEngineExperimentError(f"{left_name} and {right_name} references must remain distinct: {overlap}")


def _require_allowed(value: Any, allowed: frozenset[str], field_name: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise GoalEngineExperimentError(f"{field_name} must be one of {sorted(allowed)}")
    return value


def _require_schema(value: Any, expected: str) -> str:
    if value != expected:
        raise GoalEngineExperimentError(f"schema_version must be exactly {expected}")
    return value


def _require_id(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise GoalEngineExperimentError(f"{field_name} must be a non-empty safe identifier")
    return value


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\\x00" in value or len(value) > 10000:
        raise GoalEngineExperimentError(f"{field_name} must be non-empty safe text")
    return value


def _require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GoalEngineExperimentError(f"{field_name} must be a positive integer")
    return value


def _require_sha256(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise GoalEngineExperimentError(f"{field_name} must be a lowercase SHA-256 hex digest")
    return value


def _require_utc_timestamp(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise GoalEngineExperimentError(f"{field_name} must be a UTC timestamp")
    parsed = _timestamp(value, field_name)
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise GoalEngineExperimentError(f"{field_name} must use UTC")
    return value


def _timestamp(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise GoalEngineExperimentError(f"{field_name} must be a UTC timestamp")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise GoalEngineExperimentError(f"{field_name} must be an ISO-8601 UTC timestamp") from error


def _require_type(value: Any, expected: type, field_name: str) -> None:
    if not isinstance(value, expected):
        raise GoalEngineExperimentError(f"{field_name} must be {expected.__name__}")


def _require_optional_type(value: Any, expected: type, field_name: str) -> None:
    if value is not None:
        _require_type(value, expected, field_name)

__all__ = [
    "EXPERIMENT_QUESTION_SCHEMA_VERSION",
    "EXPERIMENT_HYPOTHESIS_SCHEMA_VERSION",
    "EXPERIMENT_INPUT_SCHEMA_VERSION",
    "EXPERIMENT_BOUNDARY_SCHEMA_VERSION",
    "EXPERIMENT_STOP_CRITERION_SCHEMA_VERSION",
    "EXPERIMENT_CLEANUP_PLAN_SCHEMA_VERSION",
    "EXPERIMENT_APPROVAL_REFERENCE_SCHEMA_VERSION",
    "EXPERIMENT_OBSERVATION_SCHEMA_VERSION",
    "EXPERIMENT_OUTCOME_SCHEMA_VERSION",
    "GOAL_EXPERIMENT_SCHEMA_VERSION",
    "GOAL_EXPERIMENT_REFERENCE_SCHEMA_VERSION",
    "EXPERIMENT_STATUSES",
    "INPUT_CLASSES",
    "BOUNDARY_KINDS",
    "STOP_CRITERION_KINDS",
    "OBSERVATION_DISPOSITIONS",
    "OUTCOME_DISPOSITIONS",
    "GoalEngineExperimentError",
    "ExperimentQuestion",
    "ExperimentHypothesis",
    "ExperimentInput",
    "ExperimentBoundary",
    "ExperimentStopCriterion",
    "ExperimentCleanupPlan",
    "ExperimentApprovalReference",
    "ExperimentObservation",
    "ExperimentOutcome",
    "GoalExperimentReference",
    "GoalExperiment",
    "validate_input_class",
    "validate_boundary_kind",
    "validate_stop_criterion_kind",
    "validate_observation_disposition",
    "validate_outcome_disposition",
    "validate_goal_experiment",
    "validate_goal_experiment_revision",
    "build_goal_experiment",
    "experiment_question_to_dict",
    "experiment_question_from_dict",
    "experiment_hypothesis_to_dict",
    "experiment_hypothesis_from_dict",
    "experiment_input_to_dict",
    "experiment_input_from_dict",
    "experiment_boundary_to_dict",
    "experiment_boundary_from_dict",
    "experiment_stop_criterion_to_dict",
    "experiment_stop_criterion_from_dict",
    "experiment_cleanup_plan_to_dict",
    "experiment_cleanup_plan_from_dict",
    "experiment_approval_reference_to_dict",
    "experiment_approval_reference_from_dict",
    "experiment_observation_to_dict",
    "experiment_observation_from_dict",
    "experiment_outcome_to_dict",
    "experiment_outcome_from_dict",
    "goal_experiment_reference_to_dict",
    "goal_experiment_reference_from_dict",
    "goal_experiment_to_dict",
    "goal_experiment_from_dict",
    "experiment_question_semantic_hash",
    "experiment_hypothesis_semantic_hash",
    "experiment_input_semantic_hash",
    "experiment_boundary_semantic_hash",
    "experiment_stop_criterion_semantic_hash",
    "experiment_cleanup_plan_semantic_hash",
    "experiment_approval_reference_semantic_hash",
    "experiment_observation_semantic_hash",
    "experiment_outcome_semantic_hash",
    "goal_experiment_reference_semantic_hash",
    "goal_experiment_semantic_hash",
]
