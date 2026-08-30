"""Pure, immutable, caller-supplied Change / Impact Engine records.

This module plans explicitly supplied expected effects only.  It neither
discovers information nor grants authority, executes work, or reports results.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from .foundation import (
    ROLLBACK_VALUES,
    GoalContractRevisionReference,
    GoalEvidenceReference,
    GoalIdentifier,
    goal_contract_revision_reference_from_dict,
    goal_contract_revision_reference_to_dict,
    goal_evidence_reference_from_dict,
    goal_evidence_reference_to_dict,
    goal_identifier_from_dict,
    goal_identifier_to_dict,
    semantic_hash,
)
from .idea_ledger import (
    LedgerEntityReference,
    ledger_entity_reference_from_dict,
    ledger_entity_reference_to_dict,
)

CHANGE_CANDIDATE_SCHEMA_VERSION = "codie.goal_engine.change_candidate.v1"
IMPACT_SUBJECT_REFERENCE_SCHEMA_VERSION = "codie.goal_engine.impact_subject_reference.v1"
IMPACT_EFFECT_SCHEMA_VERSION = "codie.goal_engine.impact_effect.v1"
DEPENDENCY_EFFECT_SCHEMA_VERSION = "codie.goal_engine.dependency_effect.v1"
IMPACT_ASSUMPTION_SCHEMA_VERSION = "codie.goal_engine.impact_assumption.v1"
ROLLBACK_ANALYSIS_SCHEMA_VERSION = "codie.goal_engine.rollback_analysis.v1"
IMPACT_VALIDATION_REQUIREMENT_SCHEMA_VERSION = (
    "codie.goal_engine.impact_validation_requirement.v1"
)
HISTORICAL_ATTEMPT_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.historical_attempt_reference.v1"
)
CHANGE_IMPACT_ASSESSMENT_SCHEMA_VERSION = (
    "codie.goal_engine.change_impact_assessment.v1"
)
CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.change_impact_assessment_reference.v1"
)

EFFECT_LIKELIHOODS = frozenset({"DIRECT", "INDIRECT", "POSSIBLE"})
SUBJECT_EXPECTATIONS = frozenset(
    {"EXPECTED_AFFECTED", "EXPECTED_UNTOUCHED", "UNKNOWN"}
)
IMPACT_DIMENSIONS = frozenset(
    {
        "FUNCTIONAL",
        "DATA",
        "ARCHITECTURE",
        "DEPENDENCY",
        "PRIVACY",
        "SECURITY",
        "ZERO_COST",
        "MANUAL_BURDEN",
        "OPERATIONAL_BURDEN",
        "PERFORMANCE",
        "RELIABILITY",
        "COMPATIBILITY",
        "VALIDATION",
        "ROLLBACK",
    }
)
DEPENDENCY_EFFECT_KINDS = frozenset(
    {"REQUIRES", "CONSTRAINS", "MAY_DEGRADE", "BLOCKS", "REPLACES", "COMPATIBILITY_RISK"}
)
VALIDATION_REQUIREMENT_KINDS = frozenset(
    {
        "EVIDENCE_REVIEW",
        "UNIT_TEST",
        "REGRESSION_TEST",
        "SCHEMA_CHECK",
        "SECURITY_REVIEW",
        "PRIVACY_REVIEW",
        "ZERO_COST_REVIEW",
        "MANUAL_REVIEW",
        "OBSERVATION_WINDOW",
        "ROLLBACK_REHEARSAL",
    }
)
HISTORICAL_COMPARISON_DISPOSITIONS = frozenset(
    {
        "NOT_COMPARED",
        "SIMILAR_SUCCESS",
        "SIMILAR_LIMITATION",
        "SIMILAR_FAILURE",
        "SIMILAR_REWIND",
        "MATERIAL_DIFFERENCE_DOCUMENTED",
    }
)

_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9:._/-]*\Z")
_SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class GoalEngineImpactError(ValueError):
    """Raised when a Change / Impact record violates the v1 contract."""


@dataclass(frozen=True)
class ChangeCandidate:
    change_id: str
    subject: LedgerEntityReference
    goal_ref: GoalIdentifier | None
    goal_contract_ref: GoalContractRevisionReference | None
    proposed_change_summary: str
    baseline_summary: str
    expected_result_summary: str
    evidence_ref_ids: tuple[str, ...]
    conflict_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    created_at: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.change_id, "change_id")
        _require_type(self.subject, LedgerEntityReference, "subject")
        _require_optional_type(self.goal_ref, GoalIdentifier, "goal_ref")
        _require_optional_type(
            self.goal_contract_ref, GoalContractRevisionReference, "goal_contract_ref"
        )
        for name in (
            "proposed_change_summary",
            "baseline_summary",
            "expected_result_summary",
        ):
            _require_text(getattr(self, name), name)
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "conflict_ref_ids", _id_tuple(self.conflict_ref_ids, "conflict_ref_ids"))
        _require_disjoint(self.evidence_ref_ids, self.conflict_ref_ids, "evidence", "conflict")
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_utc_timestamp(self.created_at, "created_at")
        _require_schema(self.schema_version, CHANGE_CANDIDATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ImpactSubjectReference:
    subject: LedgerEntityReference
    expected_state: str
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_type(self.subject, LedgerEntityReference, "subject")
        validate_subject_expectation(self.expected_state)
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, IMPACT_SUBJECT_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ImpactEffect:
    effect_id: str
    subject: LedgerEntityReference
    dimension: str
    likelihood: str
    expected_state: str
    statement: str
    evidence_ref_ids: tuple[str, ...]
    conflict_ref_ids: tuple[str, ...]
    assumption_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.effect_id, "effect_id")
        _require_type(self.subject, LedgerEntityReference, "subject")
        validate_impact_dimension(self.dimension)
        validate_effect_likelihood(self.likelihood)
        validate_subject_expectation(self.expected_state)
        _require_text(self.statement, "statement")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "conflict_ref_ids", _id_tuple(self.conflict_ref_ids, "conflict_ref_ids"))
        _require_disjoint(self.evidence_ref_ids, self.conflict_ref_ids, "evidence", "conflict")
        object.__setattr__(self, "assumption_ids", _id_tuple(self.assumption_ids, "assumption_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, IMPACT_EFFECT_SCHEMA_VERSION)


@dataclass(frozen=True)
class DependencyEffect:
    dependency_effect_id: str
    subject: LedgerEntityReference
    dependency: LedgerEntityReference
    effect_kind: str
    statement: str
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.dependency_effect_id, "dependency_effect_id")
        _require_type(self.subject, LedgerEntityReference, "subject")
        _require_type(self.dependency, LedgerEntityReference, "dependency")
        if _subject_key(self.subject) == _subject_key(self.dependency):
            raise GoalEngineImpactError("dependency subject and dependency must be distinct")
        validate_dependency_effect_kind(self.effect_kind)
        _require_text(self.statement, "statement")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, DEPENDENCY_EFFECT_SCHEMA_VERSION)


@dataclass(frozen=True)
class ImpactAssumption:
    assumption_id: str
    statement: str
    evidence_ref_ids: tuple[str, ...]
    disconfirmation_criteria: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.assumption_id, "assumption_id")
        _require_text(self.statement, "statement")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "disconfirmation_criteria", _text_tuple(self.disconfirmation_criteria, "disconfirmation_criteria", require_nonempty=True))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, IMPACT_ASSUMPTION_SCHEMA_VERSION)


@dataclass(frozen=True)
class RollbackAnalysis:
    rollback_class: str
    known_good_reference: LedgerEntityReference | None
    rollback_summary: str
    preconditions: tuple[str, ...]
    validation_requirement_ids: tuple[str, ...]
    residual_risk_summary: str
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_allowed(self.rollback_class, ROLLBACK_VALUES, "rollback_class")
        _require_optional_type(self.known_good_reference, LedgerEntityReference, "known_good_reference")
        _require_text(self.rollback_summary, "rollback_summary")
        object.__setattr__(self, "preconditions", _text_tuple(self.preconditions, "preconditions"))
        object.__setattr__(self, "validation_requirement_ids", _id_tuple(self.validation_requirement_ids, "validation_requirement_ids"))
        _require_text(self.residual_risk_summary, "residual_risk_summary")
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, ROLLBACK_ANALYSIS_SCHEMA_VERSION)


@dataclass(frozen=True)
class ImpactValidationRequirement:
    requirement_id: str
    requirement_kind: str
    statement: str
    evidence_ref_ids: tuple[str, ...]
    expected_subject_refs: tuple[LedgerEntityReference, ...]
    human_review_required: bool
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.requirement_id, "requirement_id")
        validate_validation_requirement_kind(self.requirement_kind)
        _require_text(self.statement, "statement")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "expected_subject_refs", _record_tuple(self.expected_subject_refs, LedgerEntityReference, "expected_subject_refs", _subject_key))
        _require_type(self.human_review_required, bool, "human_review_required")
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, IMPACT_VALIDATION_REQUIREMENT_SCHEMA_VERSION)


@dataclass(frozen=True)
class HistoricalAttemptReference:
    attempt_ref: LedgerEntityReference
    disposition: str
    material_difference_summary: str | None
    evidence_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_type(self.attempt_ref, LedgerEntityReference, "attempt_ref")
        disposition = validate_historical_comparison_disposition(self.disposition)
        if disposition == "MATERIAL_DIFFERENCE_DOCUMENTED":
            _require_text(self.material_difference_summary, "material_difference_summary")
        elif self.material_difference_summary is not None:
            _require_text(self.material_difference_summary, "material_difference_summary")
        object.__setattr__(self, "evidence_ref_ids", _id_tuple(self.evidence_ref_ids, "evidence_ref_ids"))
        object.__setattr__(self, "limitations", _text_tuple(self.limitations, "limitations", require_nonempty=True))
        _require_schema(self.schema_version, HISTORICAL_ATTEMPT_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ChangeImpactAssessmentReference:
    assessment_id: str
    revision: int
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.assessment_id, "assessment_id")
        _require_positive_int(self.revision, "revision")
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(self.schema_version, CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ChangeImpactAssessment:
    assessment_id: str
    revision: int
    change: ChangeCandidate
    as_of: str
    affected_subjects: tuple[ImpactSubjectReference, ...]
    effects: tuple[ImpactEffect, ...]
    dependency_effects: tuple[DependencyEffect, ...]
    assumptions: tuple[ImpactAssumption, ...]
    rollback: RollbackAnalysis
    validation_requirements: tuple[ImpactValidationRequirement, ...]
    historical_attempts: tuple[HistoricalAttemptReference, ...]
    evidence_snapshot: tuple[GoalEvidenceReference, ...]
    supersedes_assessment: ChangeImpactAssessmentReference | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.assessment_id, "assessment_id")
        _require_positive_int(self.revision, "revision")
        _require_type(self.change, ChangeCandidate, "change")
        _require_utc_timestamp(self.as_of, "as_of")
        object.__setattr__(self, "affected_subjects", _record_tuple(self.affected_subjects, ImpactSubjectReference, "affected_subjects", lambda item: _subject_key(item.subject)))
        object.__setattr__(self, "effects", _record_tuple(self.effects, ImpactEffect, "effects", lambda item: item.effect_id))
        object.__setattr__(self, "dependency_effects", _record_tuple(self.dependency_effects, DependencyEffect, "dependency_effects", lambda item: item.dependency_effect_id))
        object.__setattr__(self, "assumptions", _record_tuple(self.assumptions, ImpactAssumption, "assumptions", lambda item: item.assumption_id))
        _require_type(self.rollback, RollbackAnalysis, "rollback")
        object.__setattr__(self, "validation_requirements", _record_tuple(self.validation_requirements, ImpactValidationRequirement, "validation_requirements", lambda item: item.requirement_id))
        object.__setattr__(self, "historical_attempts", _record_tuple(self.historical_attempts, HistoricalAttemptReference, "historical_attempts", lambda item: _subject_key(item.attempt_ref)))
        object.__setattr__(self, "evidence_snapshot", _record_tuple(self.evidence_snapshot, GoalEvidenceReference, "evidence_snapshot", lambda item: item.evidence_ref_id))
        _require_optional_type(self.supersedes_assessment, ChangeImpactAssessmentReference, "supersedes_assessment")
        if self.revision == 1:
            if self.supersedes_assessment is not None:
                raise GoalEngineImpactError("assessment revision 1 cannot supersede an earlier assessment")
        elif self.supersedes_assessment is None:
            raise GoalEngineImpactError("later assessment revision requires supersedes_assessment")
        _require_schema(self.schema_version, CHANGE_IMPACT_ASSESSMENT_SCHEMA_VERSION)
        validate_change_impact_assessment(self)


def validate_effect_likelihood(value: str) -> str:
    return _require_allowed(value, EFFECT_LIKELIHOODS, "effect likelihood")


def validate_subject_expectation(value: str) -> str:
    return _require_allowed(value, SUBJECT_EXPECTATIONS, "subject expectation")


def validate_impact_dimension(value: str) -> str:
    return _require_allowed(value, IMPACT_DIMENSIONS, "impact dimension")


def validate_dependency_effect_kind(value: str) -> str:
    return _require_allowed(value, DEPENDENCY_EFFECT_KINDS, "dependency effect kind")


def validate_validation_requirement_kind(value: str) -> str:
    return _require_allowed(value, VALIDATION_REQUIREMENT_KINDS, "validation requirement kind")


def validate_historical_comparison_disposition(value: str) -> str:
    return _require_allowed(value, HISTORICAL_COMPARISON_DISPOSITIONS, "historical comparison disposition")


def validate_change_candidate(candidate: ChangeCandidate) -> ChangeCandidate:
    _require_type(candidate, ChangeCandidate, "candidate")
    return candidate


def validate_change_impact_assessment(assessment: ChangeImpactAssessment) -> ChangeImpactAssessment:
    _require_type(assessment, ChangeImpactAssessment, "assessment")
    evidence_ids = {item.evidence_ref_id for item in assessment.evidence_snapshot}
    _require_resolved(assessment.change.evidence_ref_ids, evidence_ids, "change evidence_ref_ids")
    _require_resolved(assessment.change.conflict_ref_ids, evidence_ids, "change conflict_ref_ids")
    assumption_ids = {item.assumption_id for item in assessment.assumptions}
    requirement_ids = {item.requirement_id for item in assessment.validation_requirements}
    affected_keys = {_subject_key(item.subject) for item in assessment.affected_subjects}
    for subject in assessment.affected_subjects:
        _require_resolved(subject.evidence_ref_ids, evidence_ids, "affected subject evidence_ref_ids")
    for effect in assessment.effects:
        _require_resolved(effect.evidence_ref_ids, evidence_ids, "effect evidence_ref_ids")
        _require_resolved(effect.conflict_ref_ids, evidence_ids, "effect conflict_ref_ids")
        _require_resolved(effect.assumption_ids, assumption_ids, "effect assumption_ids")
        if _subject_key(effect.subject) not in affected_keys:
            raise GoalEngineImpactError("each effect subject must be an explicit affected_subject")
    for dependency_effect in assessment.dependency_effects:
        _require_resolved(
            dependency_effect.evidence_ref_ids,
            evidence_ids,
            "dependency evidence_ref_ids",
        )
        if _subject_key(dependency_effect.subject) not in affected_keys:
            raise GoalEngineImpactError("each dependency subject must be an explicit affected_subject")
    for assumption in assessment.assumptions:
        _require_resolved(assumption.evidence_ref_ids, evidence_ids, "assumption evidence_ref_ids")
    _require_resolved(assessment.rollback.validation_requirement_ids, requirement_ids, "rollback validation_requirement_ids")
    for requirement in assessment.validation_requirements:
        _require_resolved(requirement.evidence_ref_ids, evidence_ids, "validation requirement evidence_ref_ids")
        for expected_subject in requirement.expected_subject_refs:
            if _subject_key(expected_subject) not in affected_keys:
                raise GoalEngineImpactError("validation requirement subject must be an explicit affected_subject")
    for attempt in assessment.historical_attempts:
        _require_resolved(attempt.evidence_ref_ids, evidence_ids, "historical attempt evidence_ref_ids")
    return assessment


def validate_change_impact_assessment_revision(
    assessment: ChangeImpactAssessment,
    prior_assessment: ChangeImpactAssessment,
) -> ChangeImpactAssessment:
    validate_change_impact_assessment(assessment)
    validate_change_impact_assessment(prior_assessment)
    if assessment.assessment_id != prior_assessment.assessment_id:
        raise GoalEngineImpactError("assessment revision must retain assessment_id")
    if assessment.revision != prior_assessment.revision + 1:
        raise GoalEngineImpactError("assessment revision must be the next exact revision")
    reference = assessment.supersedes_assessment
    if reference is None:
        raise GoalEngineImpactError("later assessment revision requires supersedes_assessment")
    if reference.assessment_id != prior_assessment.assessment_id or reference.revision != prior_assessment.revision:
        raise GoalEngineImpactError("supersedes_assessment must reference the immediately prior revision")
    if reference.semantic_hash != change_impact_assessment_semantic_hash(prior_assessment):
        raise GoalEngineImpactError("supersedes_assessment semantic hash must match the immediately prior revision")
    if _timestamp(assessment.as_of, "as_of") < _timestamp(prior_assessment.as_of, "prior as_of"):
        raise GoalEngineImpactError("later assessment as_of cannot precede the prior assessment")
    if assessment.change != prior_assessment.change:
        raise GoalEngineImpactError("assessment revision cannot rewrite the prior change candidate")
    if assessment.rollback != prior_assessment.rollback:
        raise GoalEngineImpactError("assessment revision cannot rewrite the prior rollback analysis")
    _require_append_only(
        assessment.affected_subjects,
        prior_assessment.affected_subjects,
        lambda item: _subject_key(item.subject),
        "affected_subjects",
    )
    _require_append_only(
        assessment.effects,
        prior_assessment.effects,
        lambda item: item.effect_id,
        "effects",
    )
    _require_append_only(
        assessment.dependency_effects,
        prior_assessment.dependency_effects,
        lambda item: item.dependency_effect_id,
        "dependency_effects",
    )
    _require_append_only(
        assessment.assumptions,
        prior_assessment.assumptions,
        lambda item: item.assumption_id,
        "assumptions",
    )
    _require_append_only(
        assessment.validation_requirements,
        prior_assessment.validation_requirements,
        lambda item: item.requirement_id,
        "validation_requirements",
    )
    _require_append_only(
        assessment.historical_attempts,
        prior_assessment.historical_attempts,
        lambda item: _subject_key(item.attempt_ref),
        "historical_attempts",
    )
    _require_append_only(
        assessment.evidence_snapshot,
        prior_assessment.evidence_snapshot,
        lambda item: item.evidence_ref_id,
        "evidence_snapshot",
    )
    return assessment


def build_change_impact_assessment(
    *,
    assessment_id: str,
    revision: int,
    change: ChangeCandidate,
    as_of: str,
    affected_subjects: tuple[ImpactSubjectReference, ...],
    effects: tuple[ImpactEffect, ...],
    dependency_effects: tuple[DependencyEffect, ...],
    assumptions: tuple[ImpactAssumption, ...],
    rollback: RollbackAnalysis,
    validation_requirements: tuple[ImpactValidationRequirement, ...],
    historical_attempts: tuple[HistoricalAttemptReference, ...],
    evidence_snapshot: tuple[GoalEvidenceReference, ...],
    supersedes_assessment: ChangeImpactAssessmentReference | None,
    prior_assessment: ChangeImpactAssessment | None = None,
) -> ChangeImpactAssessment:
    """Package explicitly supplied planning inputs into one immutable assessment."""
    assessment = ChangeImpactAssessment(
        assessment_id=assessment_id,
        revision=revision,
        change=change,
        as_of=as_of,
        affected_subjects=affected_subjects,
        effects=effects,
        dependency_effects=dependency_effects,
        assumptions=assumptions,
        rollback=rollback,
        validation_requirements=validation_requirements,
        historical_attempts=historical_attempts,
        evidence_snapshot=evidence_snapshot,
        supersedes_assessment=supersedes_assessment,
        schema_version=CHANGE_IMPACT_ASSESSMENT_SCHEMA_VERSION,
    )
    if prior_assessment is not None:
        validate_change_impact_assessment_revision(assessment, prior_assessment)
    elif revision > 1:
        raise GoalEngineImpactError("prior_assessment is required for a later assessment revision")
    return assessment


def change_candidate_to_dict(value: ChangeCandidate) -> dict[str, Any]:
    _require_type(value, ChangeCandidate, "value")
    return {
        "change_id": value.change_id,
        "subject": ledger_entity_reference_to_dict(value.subject),
        "goal_ref": goal_identifier_to_dict(value.goal_ref) if value.goal_ref else None,
        "goal_contract_ref": goal_contract_revision_reference_to_dict(value.goal_contract_ref) if value.goal_contract_ref else None,
        "proposed_change_summary": value.proposed_change_summary,
        "baseline_summary": value.baseline_summary,
        "expected_result_summary": value.expected_result_summary,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "conflict_ref_ids": list(value.conflict_ref_ids),
        "limitations": list(value.limitations),
        "created_at": value.created_at,
        "schema_version": value.schema_version,
    }


def change_candidate_from_dict(payload: Mapping[str, Any]) -> ChangeCandidate:
    data = _fields(payload, {"change_id", "subject", "goal_ref", "goal_contract_ref", "proposed_change_summary", "baseline_summary", "expected_result_summary", "evidence_ref_ids", "conflict_ref_ids", "limitations", "created_at", "schema_version"})
    data["subject"] = ledger_entity_reference_from_dict(_mapping(data["subject"], "subject"))
    if data["goal_ref"] is not None:
        data["goal_ref"] = goal_identifier_from_dict(_mapping(data["goal_ref"], "goal_ref"))
    if data["goal_contract_ref"] is not None:
        data["goal_contract_ref"] = goal_contract_revision_reference_from_dict(_mapping(data["goal_contract_ref"], "goal_contract_ref"))
    for name in ("evidence_ref_ids", "conflict_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ChangeCandidate(**data)


def impact_subject_reference_to_dict(value: ImpactSubjectReference) -> dict[str, Any]:
    _require_type(value, ImpactSubjectReference, "value")
    return {"subject": ledger_entity_reference_to_dict(value.subject), "expected_state": value.expected_state, "evidence_ref_ids": list(value.evidence_ref_ids), "limitations": list(value.limitations), "schema_version": value.schema_version}


def impact_subject_reference_from_dict(payload: Mapping[str, Any]) -> ImpactSubjectReference:
    data = _fields(payload, {"subject", "expected_state", "evidence_ref_ids", "limitations", "schema_version"})
    data["subject"] = ledger_entity_reference_from_dict(_mapping(data["subject"], "subject"))
    data["evidence_ref_ids"] = _json_tuple(data["evidence_ref_ids"], "evidence_ref_ids")
    data["limitations"] = _json_tuple(data["limitations"], "limitations")
    return ImpactSubjectReference(**data)


def impact_effect_to_dict(value: ImpactEffect) -> dict[str, Any]:
    _require_type(value, ImpactEffect, "value")
    return {"effect_id": value.effect_id, "subject": ledger_entity_reference_to_dict(value.subject), "dimension": value.dimension, "likelihood": value.likelihood, "expected_state": value.expected_state, "statement": value.statement, "evidence_ref_ids": list(value.evidence_ref_ids), "conflict_ref_ids": list(value.conflict_ref_ids), "assumption_ids": list(value.assumption_ids), "limitations": list(value.limitations), "schema_version": value.schema_version}


def impact_effect_from_dict(payload: Mapping[str, Any]) -> ImpactEffect:
    data = _fields(payload, {"effect_id", "subject", "dimension", "likelihood", "expected_state", "statement", "evidence_ref_ids", "conflict_ref_ids", "assumption_ids", "limitations", "schema_version"})
    data["subject"] = ledger_entity_reference_from_dict(_mapping(data["subject"], "subject"))
    for name in ("evidence_ref_ids", "conflict_ref_ids", "assumption_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ImpactEffect(**data)


def dependency_effect_to_dict(value: DependencyEffect) -> dict[str, Any]:
    _require_type(value, DependencyEffect, "value")
    return {"dependency_effect_id": value.dependency_effect_id, "subject": ledger_entity_reference_to_dict(value.subject), "dependency": ledger_entity_reference_to_dict(value.dependency), "effect_kind": value.effect_kind, "statement": value.statement, "evidence_ref_ids": list(value.evidence_ref_ids), "limitations": list(value.limitations), "schema_version": value.schema_version}


def dependency_effect_from_dict(payload: Mapping[str, Any]) -> DependencyEffect:
    data = _fields(payload, {"dependency_effect_id", "subject", "dependency", "effect_kind", "statement", "evidence_ref_ids", "limitations", "schema_version"})
    data["subject"] = ledger_entity_reference_from_dict(_mapping(data["subject"], "subject"))
    data["dependency"] = ledger_entity_reference_from_dict(_mapping(data["dependency"], "dependency"))
    for name in ("evidence_ref_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return DependencyEffect(**data)


def impact_assumption_to_dict(value: ImpactAssumption) -> dict[str, Any]:
    _require_type(value, ImpactAssumption, "value")
    return {"assumption_id": value.assumption_id, "statement": value.statement, "evidence_ref_ids": list(value.evidence_ref_ids), "disconfirmation_criteria": list(value.disconfirmation_criteria), "limitations": list(value.limitations), "schema_version": value.schema_version}


def impact_assumption_from_dict(payload: Mapping[str, Any]) -> ImpactAssumption:
    data = _fields(payload, {"assumption_id", "statement", "evidence_ref_ids", "disconfirmation_criteria", "limitations", "schema_version"})
    for name in ("evidence_ref_ids", "disconfirmation_criteria", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return ImpactAssumption(**data)


def rollback_analysis_to_dict(value: RollbackAnalysis) -> dict[str, Any]:
    _require_type(value, RollbackAnalysis, "value")
    return {"rollback_class": value.rollback_class, "known_good_reference": ledger_entity_reference_to_dict(value.known_good_reference) if value.known_good_reference else None, "rollback_summary": value.rollback_summary, "preconditions": list(value.preconditions), "validation_requirement_ids": list(value.validation_requirement_ids), "residual_risk_summary": value.residual_risk_summary, "limitations": list(value.limitations), "schema_version": value.schema_version}


def rollback_analysis_from_dict(payload: Mapping[str, Any]) -> RollbackAnalysis:
    data = _fields(payload, {"rollback_class", "known_good_reference", "rollback_summary", "preconditions", "validation_requirement_ids", "residual_risk_summary", "limitations", "schema_version"})
    if data["known_good_reference"] is not None:
        data["known_good_reference"] = ledger_entity_reference_from_dict(_mapping(data["known_good_reference"], "known_good_reference"))
    for name in ("preconditions", "validation_requirement_ids", "limitations"):
        data[name] = _json_tuple(data[name], name)
    return RollbackAnalysis(**data)


def impact_validation_requirement_to_dict(value: ImpactValidationRequirement) -> dict[str, Any]:
    _require_type(value, ImpactValidationRequirement, "value")
    return {"requirement_id": value.requirement_id, "requirement_kind": value.requirement_kind, "statement": value.statement, "evidence_ref_ids": list(value.evidence_ref_ids), "expected_subject_refs": [ledger_entity_reference_to_dict(item) for item in value.expected_subject_refs], "human_review_required": value.human_review_required, "limitations": list(value.limitations), "schema_version": value.schema_version}


def impact_validation_requirement_from_dict(payload: Mapping[str, Any]) -> ImpactValidationRequirement:
    data = _fields(payload, {"requirement_id", "requirement_kind", "statement", "evidence_ref_ids", "expected_subject_refs", "human_review_required", "limitations", "schema_version"})
    data["evidence_ref_ids"] = _json_tuple(data["evidence_ref_ids"], "evidence_ref_ids")
    data["expected_subject_refs"] = tuple(ledger_entity_reference_from_dict(_mapping(item, "expected_subject_ref")) for item in _json_tuple(data["expected_subject_refs"], "expected_subject_refs"))
    data["limitations"] = _json_tuple(data["limitations"], "limitations")
    return ImpactValidationRequirement(**data)


def historical_attempt_reference_to_dict(value: HistoricalAttemptReference) -> dict[str, Any]:
    _require_type(value, HistoricalAttemptReference, "value")
    return {"attempt_ref": ledger_entity_reference_to_dict(value.attempt_ref), "disposition": value.disposition, "material_difference_summary": value.material_difference_summary, "evidence_ref_ids": list(value.evidence_ref_ids), "limitations": list(value.limitations), "schema_version": value.schema_version}


def historical_attempt_reference_from_dict(payload: Mapping[str, Any]) -> HistoricalAttemptReference:
    data = _fields(payload, {"attempt_ref", "disposition", "material_difference_summary", "evidence_ref_ids", "limitations", "schema_version"})
    data["attempt_ref"] = ledger_entity_reference_from_dict(_mapping(data["attempt_ref"], "attempt_ref"))
    data["evidence_ref_ids"] = _json_tuple(data["evidence_ref_ids"], "evidence_ref_ids")
    data["limitations"] = _json_tuple(data["limitations"], "limitations")
    return HistoricalAttemptReference(**data)


def change_impact_assessment_reference_to_dict(value: ChangeImpactAssessmentReference) -> dict[str, Any]:
    _require_type(value, ChangeImpactAssessmentReference, "value")
    return {"assessment_id": value.assessment_id, "revision": value.revision, "semantic_hash": value.semantic_hash, "schema_version": value.schema_version}


def change_impact_assessment_reference_from_dict(payload: Mapping[str, Any]) -> ChangeImpactAssessmentReference:
    return ChangeImpactAssessmentReference(**_fields(payload, {"assessment_id", "revision", "semantic_hash", "schema_version"}))


def change_impact_assessment_to_dict(value: ChangeImpactAssessment) -> dict[str, Any]:
    _require_type(value, ChangeImpactAssessment, "value")
    return {
        "assessment_id": value.assessment_id,
        "revision": value.revision,
        "change": change_candidate_to_dict(value.change),
        "as_of": value.as_of,
        "affected_subjects": [impact_subject_reference_to_dict(item) for item in value.affected_subjects],
        "effects": [impact_effect_to_dict(item) for item in value.effects],
        "dependency_effects": [dependency_effect_to_dict(item) for item in value.dependency_effects],
        "assumptions": [impact_assumption_to_dict(item) for item in value.assumptions],
        "rollback": rollback_analysis_to_dict(value.rollback),
        "validation_requirements": [impact_validation_requirement_to_dict(item) for item in value.validation_requirements],
        "historical_attempts": [historical_attempt_reference_to_dict(item) for item in value.historical_attempts],
        "evidence_snapshot": [goal_evidence_reference_to_dict(item) for item in value.evidence_snapshot],
        "supersedes_assessment": change_impact_assessment_reference_to_dict(value.supersedes_assessment) if value.supersedes_assessment else None,
        "schema_version": value.schema_version,
    }


def change_impact_assessment_from_dict(payload: Mapping[str, Any]) -> ChangeImpactAssessment:
    data = _fields(payload, {"assessment_id", "revision", "change", "as_of", "affected_subjects", "effects", "dependency_effects", "assumptions", "rollback", "validation_requirements", "historical_attempts", "evidence_snapshot", "supersedes_assessment", "schema_version"})
    data["change"] = change_candidate_from_dict(_mapping(data["change"], "change"))
    data["affected_subjects"] = tuple(impact_subject_reference_from_dict(_mapping(item, "affected_subject")) for item in _json_tuple(data["affected_subjects"], "affected_subjects"))
    data["effects"] = tuple(impact_effect_from_dict(_mapping(item, "effect")) for item in _json_tuple(data["effects"], "effects"))
    data["dependency_effects"] = tuple(dependency_effect_from_dict(_mapping(item, "dependency_effect")) for item in _json_tuple(data["dependency_effects"], "dependency_effects"))
    data["assumptions"] = tuple(impact_assumption_from_dict(_mapping(item, "assumption")) for item in _json_tuple(data["assumptions"], "assumptions"))
    data["rollback"] = rollback_analysis_from_dict(_mapping(data["rollback"], "rollback"))
    data["validation_requirements"] = tuple(impact_validation_requirement_from_dict(_mapping(item, "validation_requirement")) for item in _json_tuple(data["validation_requirements"], "validation_requirements"))
    data["historical_attempts"] = tuple(historical_attempt_reference_from_dict(_mapping(item, "historical_attempt")) for item in _json_tuple(data["historical_attempts"], "historical_attempts"))
    data["evidence_snapshot"] = tuple(goal_evidence_reference_from_dict(_mapping(item, "evidence")) for item in _json_tuple(data["evidence_snapshot"], "evidence_snapshot"))
    if data["supersedes_assessment"] is not None:
        data["supersedes_assessment"] = change_impact_assessment_reference_from_dict(_mapping(data["supersedes_assessment"], "supersedes_assessment"))
    return ChangeImpactAssessment(**data)


def change_candidate_semantic_hash(value: ChangeCandidate) -> str:
    return semantic_hash(change_candidate_to_dict(value))


def impact_subject_reference_semantic_hash(value: ImpactSubjectReference) -> str:
    return semantic_hash(impact_subject_reference_to_dict(value))


def impact_effect_semantic_hash(value: ImpactEffect) -> str:
    return semantic_hash(impact_effect_to_dict(value))


def dependency_effect_semantic_hash(value: DependencyEffect) -> str:
    return semantic_hash(dependency_effect_to_dict(value))


def impact_assumption_semantic_hash(value: ImpactAssumption) -> str:
    return semantic_hash(impact_assumption_to_dict(value))


def rollback_analysis_semantic_hash(value: RollbackAnalysis) -> str:
    return semantic_hash(rollback_analysis_to_dict(value))


def impact_validation_requirement_semantic_hash(value: ImpactValidationRequirement) -> str:
    return semantic_hash(impact_validation_requirement_to_dict(value))


def historical_attempt_reference_semantic_hash(value: HistoricalAttemptReference) -> str:
    return semantic_hash(historical_attempt_reference_to_dict(value))


def change_impact_assessment_reference_semantic_hash(value: ChangeImpactAssessmentReference) -> str:
    return semantic_hash(change_impact_assessment_reference_to_dict(value))


def change_impact_assessment_semantic_hash(value: ChangeImpactAssessment) -> str:
    return semantic_hash(change_impact_assessment_to_dict(value))


def _fields(payload: Mapping[str, Any], expected: set[str]) -> dict[str, Any]:
    mapping = _mapping(payload, "payload")
    actual = set(mapping)
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise GoalEngineImpactError(f"payload fields must match exactly; missing={missing}, unexpected={unexpected}")
    return dict(mapping)


def _mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GoalEngineImpactError(f"{field_name} must be a mapping")
    return value


def _json_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise GoalEngineImpactError(f"{field_name} must be a JSON list")
    return tuple(value)


def _record_tuple(values: Any, expected_type: type, field_name: str, key: Any) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineImpactError(f"{field_name} must be a tuple")
    for value in values:
        _require_type(value, expected_type, field_name)
    ordered = tuple(sorted(values, key=key))
    if len({key(value) for value in ordered}) != len(ordered):
        raise GoalEngineImpactError(f"{field_name} cannot contain duplicate identities")
    return ordered


def _id_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineImpactError(f"{field_name} must be a tuple")
    result = tuple(sorted(_require_id(value, field_name) for value in values))
    if len(set(result)) != len(result):
        raise GoalEngineImpactError(f"{field_name} cannot contain duplicates")
    return result


def _text_tuple(values: Any, field_name: str, require_nonempty: bool = False) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineImpactError(f"{field_name} must be a tuple")
    result = tuple(sorted(_require_text(value, field_name) for value in values))
    if require_nonempty and not result:
        raise GoalEngineImpactError(f"{field_name} cannot be empty")
    if len(set(result)) != len(result):
        raise GoalEngineImpactError(f"{field_name} cannot contain duplicates")
    return result


def _subject_key(value: LedgerEntityReference) -> tuple[str, str, int | None, str]:
    return (value.entity_kind, value.entity_id, value.revision, value.semantic_hash)


def _require_resolved(values: tuple[str, ...], allowed: set[str], field_name: str) -> None:
    missing = sorted(set(values) - allowed)
    if missing:
        raise GoalEngineImpactError(f"{field_name} contains unresolved references: {missing}")


def _require_append_only(current: tuple[Any, ...], prior: tuple[Any, ...], key: Any, field_name: str) -> None:
    current_by_key = {key(item): item for item in current}
    for prior_item in prior:
        item_key = key(prior_item)
        if current_by_key.get(item_key) != prior_item:
            raise GoalEngineImpactError(f"assessment revision cannot remove or rewrite prior {field_name}")


def _require_disjoint(left: tuple[str, ...], right: tuple[str, ...], left_name: str, right_name: str) -> None:
    overlap = sorted(set(left) & set(right))
    if overlap:
        raise GoalEngineImpactError(f"{left_name} and {right_name} references must remain distinct: {overlap}")


def _require_allowed(value: Any, allowed: frozenset[str], field_name: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise GoalEngineImpactError(f"{field_name} must be one of {sorted(allowed)}")
    return value


def _require_schema(value: Any, expected: str) -> str:
    if value != expected:
        raise GoalEngineImpactError(f"schema_version must be exactly {expected}")
    return value


def _require_id(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        raise GoalEngineImpactError(f"{field_name} must be a non-empty safe identifier")
    return value


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\\x00" in value or len(value) > 10000:
        raise GoalEngineImpactError(f"{field_name} must be non-empty safe text")
    return value


def _require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GoalEngineImpactError(f"{field_name} must be a positive integer")
    return value


def _require_sha256(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise GoalEngineImpactError(f"{field_name} must be a lowercase SHA-256 hex digest")
    return value


def _require_utc_timestamp(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise GoalEngineImpactError(f"{field_name} must be a UTC timestamp")
    parsed = _timestamp(value, field_name)
    if parsed.tzinfo is None or parsed.utcoffset() != UTC.utcoffset(parsed):
        raise GoalEngineImpactError(f"{field_name} must use UTC")
    return value


def _timestamp(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise GoalEngineImpactError(f"{field_name} must be a UTC timestamp")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise GoalEngineImpactError(f"{field_name} must be an ISO-8601 UTC timestamp") from error


def _require_type(value: Any, expected: type, field_name: str) -> None:
    if not isinstance(value, expected):
        raise GoalEngineImpactError(f"{field_name} must be {expected.__name__}")


def _require_optional_type(value: Any, expected: type, field_name: str) -> None:
    if value is not None:
        _require_type(value, expected, field_name)


__all__ = [
    "CHANGE_CANDIDATE_SCHEMA_VERSION",
    "IMPACT_SUBJECT_REFERENCE_SCHEMA_VERSION",
    "IMPACT_EFFECT_SCHEMA_VERSION",
    "DEPENDENCY_EFFECT_SCHEMA_VERSION",
    "IMPACT_ASSUMPTION_SCHEMA_VERSION",
    "ROLLBACK_ANALYSIS_SCHEMA_VERSION",
    "IMPACT_VALIDATION_REQUIREMENT_SCHEMA_VERSION",
    "HISTORICAL_ATTEMPT_REFERENCE_SCHEMA_VERSION",
    "CHANGE_IMPACT_ASSESSMENT_SCHEMA_VERSION",
    "CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION",
    "EFFECT_LIKELIHOODS",
    "SUBJECT_EXPECTATIONS",
    "IMPACT_DIMENSIONS",
    "DEPENDENCY_EFFECT_KINDS",
    "VALIDATION_REQUIREMENT_KINDS",
    "HISTORICAL_COMPARISON_DISPOSITIONS",
    "GoalEngineImpactError",
    "ChangeCandidate",
    "ImpactSubjectReference",
    "ImpactEffect",
    "DependencyEffect",
    "ImpactAssumption",
    "RollbackAnalysis",
    "ImpactValidationRequirement",
    "HistoricalAttemptReference",
    "ChangeImpactAssessmentReference",
    "ChangeImpactAssessment",
    "validate_effect_likelihood",
    "validate_subject_expectation",
    "validate_impact_dimension",
    "validate_dependency_effect_kind",
    "validate_validation_requirement_kind",
    "validate_historical_comparison_disposition",
    "validate_change_candidate",
    "validate_change_impact_assessment",
    "validate_change_impact_assessment_revision",
    "build_change_impact_assessment",
    "change_candidate_to_dict",
    "change_candidate_from_dict",
    "impact_subject_reference_to_dict",
    "impact_subject_reference_from_dict",
    "impact_effect_to_dict",
    "impact_effect_from_dict",
    "dependency_effect_to_dict",
    "dependency_effect_from_dict",
    "impact_assumption_to_dict",
    "impact_assumption_from_dict",
    "rollback_analysis_to_dict",
    "rollback_analysis_from_dict",
    "impact_validation_requirement_to_dict",
    "impact_validation_requirement_from_dict",
    "historical_attempt_reference_to_dict",
    "historical_attempt_reference_from_dict",
    "change_impact_assessment_reference_to_dict",
    "change_impact_assessment_reference_from_dict",
    "change_impact_assessment_to_dict",
    "change_impact_assessment_from_dict",
    "change_candidate_semantic_hash",
    "impact_subject_reference_semantic_hash",
    "impact_effect_semantic_hash",
    "dependency_effect_semantic_hash",
    "impact_assumption_semantic_hash",
    "rollback_analysis_semantic_hash",
    "impact_validation_requirement_semantic_hash",
    "historical_attempt_reference_semantic_hash",
    "change_impact_assessment_reference_semantic_hash",
    "change_impact_assessment_semantic_hash",
]
