"""Contract tests for the pure Goal Experiment Engine."""

from __future__ import annotations

import ast
import unittest
from dataclasses import fields, replace
from pathlib import Path

from codie.goal_engine.experiment import (
    EXPERIMENT_APPROVAL_REFERENCE_SCHEMA_VERSION,
    EXPERIMENT_BOUNDARY_SCHEMA_VERSION,
    EXPERIMENT_CLEANUP_PLAN_SCHEMA_VERSION,
    EXPERIMENT_HYPOTHESIS_SCHEMA_VERSION,
    EXPERIMENT_INPUT_SCHEMA_VERSION,
    EXPERIMENT_OBSERVATION_SCHEMA_VERSION,
    EXPERIMENT_OUTCOME_SCHEMA_VERSION,
    EXPERIMENT_QUESTION_SCHEMA_VERSION,
    EXPERIMENT_STOP_CRITERION_SCHEMA_VERSION,
    GOAL_EXPERIMENT_REFERENCE_SCHEMA_VERSION,
    ExperimentApprovalReference,
    ExperimentBoundary,
    ExperimentCleanupPlan,
    ExperimentHypothesis,
    ExperimentInput,
    ExperimentObservation,
    ExperimentOutcome,
    ExperimentQuestion,
    ExperimentStopCriterion,
    GoalEngineExperimentError,
    GoalExperiment,
    GoalExperimentReference,
    build_goal_experiment,
    experiment_approval_reference_from_dict,
    experiment_approval_reference_to_dict,
    experiment_boundary_from_dict,
    experiment_boundary_to_dict,
    experiment_cleanup_plan_from_dict,
    experiment_cleanup_plan_to_dict,
    experiment_hypothesis_from_dict,
    experiment_hypothesis_to_dict,
    experiment_input_from_dict,
    experiment_input_to_dict,
    experiment_observation_from_dict,
    experiment_observation_to_dict,
    experiment_outcome_from_dict,
    experiment_outcome_to_dict,
    experiment_question_from_dict,
    experiment_question_to_dict,
    experiment_stop_criterion_from_dict,
    experiment_stop_criterion_to_dict,
    goal_experiment_from_dict,
    goal_experiment_reference_from_dict,
    goal_experiment_reference_to_dict,
    goal_experiment_semantic_hash,
    goal_experiment_to_dict,
    validate_goal_experiment_revision,
)
from codie.goal_engine.foundation import EVIDENCE_REFERENCE_SCHEMA_VERSION, GoalEvidenceReference
from codie.goal_engine.impact import ROLLBACK_ANALYSIS_SCHEMA_VERSION, RollbackAnalysis

T1 = "2026-08-30T00:00:00Z"
T2 = "2026-08-30T00:01:00Z"


def evidence(ref_id: str = "evidence:one") -> GoalEvidenceReference:
    return GoalEvidenceReference(
        evidence_ref_id=ref_id,
        evidence_class="OBSERVATION",
        source_id="source:local",
        source_version="v1",
        observed_at=T1,
        historical_validity="RECORDED",
        current_applicability="UNKNOWN",
        review_state="UNREVIEWED",
        privacy_class="PROJECT_INTERNAL",
        conflict_ref_ids=(),
        schema_version=EVIDENCE_REFERENCE_SCHEMA_VERSION,
    )


def question() -> ExperimentQuestion:
    return ExperimentQuestion(
        question_id="question:one",
        statement="A caller proposes a bounded local adjustment.",
        evidence_ref_ids=("evidence:one",),
        limitations=("No scope discovery or authorization is implied.",),
        schema_version=EXPERIMENT_QUESTION_SCHEMA_VERSION,
    )


def hypothesis() -> ExperimentHypothesis:
    return ExperimentHypothesis(
        hypothesis_id="hypothesis:one",
        statement="A caller proposes a bounded local adjustment.",
        expected_observation="This remains an expectation, not an outcome.",
        disconfirmation_criteria=("No scope discovery or authorization is implied.",),
        evidence_ref_ids=("evidence:one",),
        limitations=("This declaration does not schedule review.",),
        schema_version=EXPERIMENT_HYPOTHESIS_SCHEMA_VERSION,
    )


def input_() -> ExperimentInput:
    return ExperimentInput(
        input_id="input:one",
        input_class="CALLER_SUPPLIED",
        subject="A caller-supplied subject.",
        description="A caller-supplied description.",
        evidence_ref_ids=("evidence:one",),
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_INPUT_SCHEMA_VERSION,
    )


def boundary() -> ExperimentBoundary:
    return ExperimentBoundary(
        boundary_id="boundary:one",
        boundary_kind="SCOPE",
        statement="A caller-supplied boundary.",
        evidence_ref_ids=("evidence:one",),
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_BOUNDARY_SCHEMA_VERSION,
    )


def stop_criterion() -> ExperimentStopCriterion:
    return ExperimentStopCriterion(
        criterion_id="criterion:one",
        criterion_kind="SAFETY",
        statement="A caller-supplied stop criterion.",
        human_review_required=True,
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_STOP_CRITERION_SCHEMA_VERSION,
    )


def cleanup_plan() -> ExperimentCleanupPlan:
    return ExperimentCleanupPlan(
        cleanup_id="cleanup:one",
        statement="A caller-supplied cleanup plan.",
        preconditions=("Precondition one.",),
        validation_requirement_ids=("requirement:review",),
        residual_risk_summary="Residual uncertainty remains.",
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_CLEANUP_PLAN_SCHEMA_VERSION,
    )


def rollback(rollback_summary: str = "A caller-described rollback path.") -> RollbackAnalysis:
    return RollbackAnalysis(
        rollback_class="Easy",
        known_good_reference=None,
        rollback_summary=rollback_summary,
        preconditions=(),
        validation_requirement_ids=("requirement:review",),
        residual_risk_summary="Residual uncertainty remains.",
        limitations=("This is not a fact.",),
        schema_version=ROLLBACK_ANALYSIS_SCHEMA_VERSION,
    )


def approval_reference(approval_ref_id: str = "approval:one") -> ExperimentApprovalReference:
    return ExperimentApprovalReference(
        approval_ref_id=approval_ref_id,
        authority_kind="MANUAL_REVIEW",
        decision_ref="decision:review",
        scope_statement="A caller-supplied scope.",
        recorded_at=T1,
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_APPROVAL_REFERENCE_SCHEMA_VERSION,
    )


def observation(observation_id: str = "observation:one") -> ExperimentObservation:
    return ExperimentObservation(
        observation_id=observation_id,
        statement="An observation.",
        disposition="OBSERVED",
        observed_at=T1,
        evidence_ref_ids=("evidence:one",),
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_OBSERVATION_SCHEMA_VERSION,
    )


def outcome() -> ExperimentOutcome:
    return ExperimentOutcome(
        outcome_id="outcome:one",
        disposition="SUPPORTS_HYPOTHESIS",
        statement="An outcome.",
        observation_ref_ids=("observation:one",),
        limitations=("This is not a fact.",),
        schema_version=EXPERIMENT_OUTCOME_SCHEMA_VERSION,
    )


def experiment_reference() -> GoalExperimentReference:
    return GoalExperimentReference(
        experiment_id="experiment:one",
        revision=1,
        semantic_hash="a" * 64,
        schema_version=GOAL_EXPERIMENT_REFERENCE_SCHEMA_VERSION,
    )


def experiment(
    *,
    revision: int = 1,
    supersedes_experiment=None,
    prior=None,
    as_of: str = T2,
) -> GoalExperiment:
    return build_goal_experiment(
        experiment_id="experiment:one",
        revision=revision,
        question=question(),
        hypothesis=hypothesis(),
        inputs=(input_(),),
        boundaries=(boundary(),),
        stop_criteria=(stop_criterion(),),
        cleanup_plan=cleanup_plan(),
        rollback=rollback(),
        approval_references=(approval_reference(),),
        observations=(observation(),),
        outcome=outcome(),
        impact_assessment_ref=None,
        evidence_snapshot=(evidence(),),
        as_of=as_of,
        supersedes_experiment=supersedes_experiment,
        prior_experiment=prior,
    )


def next_reference(prior_experiment: GoalExperiment) -> GoalExperimentReference:
    """A valid GoalExperimentReference pointing at prior_experiment, for revision-2 tests."""
    return GoalExperimentReference(
        experiment_id=prior_experiment.experiment_id,
        revision=prior_experiment.revision,
        semantic_hash=goal_experiment_semantic_hash(prior_experiment),
        schema_version=GOAL_EXPERIMENT_REFERENCE_SCHEMA_VERSION,
    )


class ExperimentRecordTest(unittest.TestCase):
    def test_experiment_question_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(question(), schema_version="wrong")

    def test_experiment_question_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(question(), statement="")

    def test_experiment_question_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "question_id must be a non-empty safe identifier"):
            replace(question(), question_id="")

    def test_experiment_hypothesis_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(hypothesis(), schema_version="wrong")

    def test_experiment_hypothesis_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(hypothesis(), statement="")

    def test_experiment_hypothesis_rejects_empty_expected_observation(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "expected_observation must be non-empty safe text"):
            replace(hypothesis(), expected_observation="")

    def test_experiment_hypothesis_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "hypothesis_id must be a non-empty safe identifier"):
            replace(hypothesis(), hypothesis_id="")

    def test_experiment_input_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(input_(), schema_version="wrong")

    def test_experiment_input_rejects_empty_subject(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "subject must be non-empty safe text"):
            replace(input_(), subject="")

    def test_experiment_input_rejects_empty_description(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "description must be non-empty safe text"):
            replace(input_(), description="")

    def test_experiment_input_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "input_id must be a non-empty safe identifier"):
            replace(input_(), input_id="")

    def test_experiment_input_rejects_bad_input_class(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "input class must be one of"):
            replace(input_(), input_class="WRONG")

    def test_experiment_boundary_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(boundary(), schema_version="wrong")

    def test_experiment_boundary_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(boundary(), statement="")

    def test_experiment_boundary_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "boundary_id must be a non-empty safe identifier"):
            replace(boundary(), boundary_id="")

    def test_experiment_boundary_rejects_bad_boundary_kind(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "boundary kind must be one of"):
            replace(boundary(), boundary_kind="WRONG")

    def test_experiment_stop_criterion_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(stop_criterion(), schema_version="wrong")

    def test_experiment_stop_criterion_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(stop_criterion(), statement="")

    def test_experiment_stop_criterion_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "criterion_id must be a non-empty safe identifier"):
            replace(stop_criterion(), criterion_id="")

    def test_experiment_stop_criterion_rejects_bad_stop_criterion_kind(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "stop criterion kind must be one of"):
            replace(stop_criterion(), criterion_kind="WRONG")

    def test_experiment_cleanup_plan_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(cleanup_plan(), schema_version="wrong")

    def test_experiment_cleanup_plan_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(cleanup_plan(), statement="")

    def test_experiment_cleanup_plan_rejects_empty_residual_risk_summary(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "residual_risk_summary must be non-empty safe text"):
            replace(cleanup_plan(), residual_risk_summary="")

    def test_experiment_cleanup_plan_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "cleanup_id must be a non-empty safe identifier"):
            replace(cleanup_plan(), cleanup_id="")

    def test_experiment_approval_reference_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(approval_reference(), schema_version="wrong")

    def test_experiment_approval_reference_rejects_empty_authority_kind(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "authority_kind must be non-empty safe text"):
            replace(approval_reference(), authority_kind="")

    def test_experiment_approval_reference_rejects_empty_decision_ref(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "decision_ref must be non-empty safe text"):
            replace(approval_reference(), decision_ref="")

    def test_experiment_approval_reference_rejects_empty_scope_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "scope_statement must be non-empty safe text"):
            replace(approval_reference(), scope_statement="")

    def test_experiment_approval_reference_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "approval_ref_id must be a non-empty safe identifier"):
            replace(approval_reference(), approval_ref_id="")

    def test_experiment_observation_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(observation(), schema_version="wrong")

    def test_experiment_observation_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(observation(), statement="")

    def test_experiment_observation_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "observation_id must be a non-empty safe identifier"):
            replace(observation(), observation_id="")

    def test_experiment_observation_rejects_bad_disposition(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "observation disposition must be one of"):
            replace(observation(), disposition="WRONG")

    def test_experiment_outcome_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(outcome(), schema_version="wrong")

    def test_experiment_outcome_rejects_empty_statement(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "statement must be non-empty safe text"):
            replace(outcome(), statement="")

    def test_experiment_outcome_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "outcome_id must be a non-empty safe identifier"):
            replace(outcome(), outcome_id="")

    def test_experiment_outcome_rejects_bad_disposition(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "outcome disposition must be one of"):
            replace(outcome(), disposition="WRONG")

    def test_goal_experiment_reference_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(experiment_reference(), schema_version="wrong")

    def test_goal_experiment_reference_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment_id must be a non-empty safe identifier"):
            replace(experiment_reference(), experiment_id="")

    def test_goal_experiment_reference_rejects_non_positive_revision(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "revision must be a positive integer"):
            replace(experiment_reference(), revision=0)

    def test_goal_experiment_reference_rejects_bad_sha256(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "semantic_hash must be a lowercase SHA-256 hex digest"):
            replace(experiment_reference(), semantic_hash="f" * 63)

    def test_goal_experiment_rejects_bad_schema_version(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "schema_version must be exactly"):
            replace(experiment(), schema_version="wrong")

    def test_goal_experiment_rejects_non_positive_revision(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "revision must be a positive integer"):
            replace(experiment(), revision=0)

    def test_goal_experiment_rejects_bad_id(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment_id must be a non-empty safe identifier"):
            replace(experiment(), experiment_id="")

    def test_goal_experiment_rejects_revision_1_with_supersedes(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision 1 cannot supersede an earlier experiment"):
            experiment(supersedes_experiment=experiment_reference())

    def test_goal_experiment_rejects_later_revision_without_supersedes(self) -> None:
        with self.assertRaisesRegex(GoalEngineExperimentError, "later experiment revision requires supersedes_experiment"):
            experiment(revision=2)

    def test_goal_experiment_rejects_unresolved_evidence(self) -> None:
        # GoalExperiment.__post_init__ already runs validate_goal_experiment,
        # so the error surfaces at construction time via replace(), not on a
        # separately-constructed object passed to validate_goal_experiment.
        with self.assertRaisesRegex(GoalEngineExperimentError, "unresolved references"):
            replace(experiment(), question=replace(question(), evidence_ref_ids=("evidence:missing",)))

    def test_goal_experiment_round_trip_preserves_distinctions(self) -> None:
        value = experiment()
        restored = goal_experiment_from_dict(goal_experiment_to_dict(value))
        self.assertEqual(restored, value)
        self.assertEqual(goal_experiment_semantic_hash(restored), goal_experiment_semantic_hash(value))

    def test_goal_experiment_round_trip_preserves_distinctions_with_none_fields(self) -> None:
        value = replace(experiment(), outcome=None, impact_assessment_ref=None, supersedes_experiment=None)
        restored = goal_experiment_from_dict(goal_experiment_to_dict(value))
        self.assertEqual(restored, value)
        self.assertEqual(goal_experiment_semantic_hash(restored), goal_experiment_semantic_hash(value))

    def test_goal_experiment_round_trip_preserves_distinctions_with_all_fields(self) -> None:
        value = experiment()
        restored = goal_experiment_from_dict(goal_experiment_to_dict(value))
        self.assertEqual(restored, value)
        self.assertEqual(goal_experiment_semantic_hash(restored), goal_experiment_semantic_hash(value))

    def test_experiment_question_round_trip_preserves_distinctions(self) -> None:
        value = question()
        restored = experiment_question_from_dict(experiment_question_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_hypothesis_round_trip_preserves_distinctions(self) -> None:
        value = hypothesis()
        restored = experiment_hypothesis_from_dict(experiment_hypothesis_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_input_round_trip_preserves_distinctions(self) -> None:
        value = input_()
        restored = experiment_input_from_dict(experiment_input_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_boundary_round_trip_preserves_distinctions(self) -> None:
        value = boundary()
        restored = experiment_boundary_from_dict(experiment_boundary_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_stop_criterion_round_trip_preserves_distinctions(self) -> None:
        value = stop_criterion()
        restored = experiment_stop_criterion_from_dict(experiment_stop_criterion_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_cleanup_plan_round_trip_preserves_distinctions(self) -> None:
        value = cleanup_plan()
        restored = experiment_cleanup_plan_from_dict(experiment_cleanup_plan_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_approval_reference_round_trip_preserves_distinctions(self) -> None:
        value = approval_reference()
        restored = experiment_approval_reference_from_dict(experiment_approval_reference_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_observation_round_trip_preserves_distinctions(self) -> None:
        value = observation()
        restored = experiment_observation_from_dict(experiment_observation_to_dict(value))
        self.assertEqual(restored, value)

    def test_experiment_outcome_round_trip_preserves_distinctions(self) -> None:
        value = outcome()
        restored = experiment_outcome_from_dict(experiment_outcome_to_dict(value))
        self.assertEqual(restored, value)

    def test_goal_experiment_reference_round_trip_preserves_distinctions(self) -> None:
        value = experiment_reference()
        restored = goal_experiment_reference_from_dict(goal_experiment_reference_to_dict(value))
        self.assertEqual(restored, value)


class ExperimentRevisionTest(unittest.TestCase):
    def test_build_goal_experiment_happy_path(self) -> None:
        value = experiment()
        self.assertEqual(goal_experiment_semantic_hash(value), goal_experiment_semantic_hash(value))

    def test_revision_chain_rules_rejects_wrong_supersedes_id(self) -> None:
        prior = experiment()
        reference = replace(experiment_reference(), experiment_id="wrong")
        with self.assertRaisesRegex(GoalEngineExperimentError, "supersedes_experiment must reference the immediately prior revision"):
            experiment(revision=2, supersedes_experiment=reference, prior=prior)

    def test_revision_chain_rules_rejects_wrong_supersedes_revision(self) -> None:
        prior = experiment()
        reference = replace(experiment_reference(), revision=2)
        with self.assertRaisesRegex(GoalEngineExperimentError, "supersedes_experiment must reference the immediately prior revision"):
            experiment(revision=2, supersedes_experiment=reference, prior=prior)

    def test_revision_chain_rules_rejects_wrong_semantic_hash(self) -> None:
        prior = experiment()
        reference = replace(experiment_reference(), semantic_hash="f" * 64)
        with self.assertRaisesRegex(GoalEngineExperimentError, "supersedes_experiment semantic hash must match the immediately prior revision"):
            experiment(revision=2, supersedes_experiment=reference, prior=prior)

    def test_revision_chain_rules_rejects_later_as_of_preceding_prior(self) -> None:
        prior = experiment()
        with self.assertRaisesRegex(GoalEngineExperimentError, "later experiment as_of cannot precede the prior experiment"):
            experiment(revision=2, supersedes_experiment=next_reference(prior), prior=prior, as_of=T1)

    def test_revision_chain_rules_rejects_question_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), question=replace(question(), statement="Changed"))
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior question"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_hypothesis_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), hypothesis=replace(hypothesis(), statement="Changed"))
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior hypothesis"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_inputs_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), inputs=())
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior inputs"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_boundaries_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), boundaries=())
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior boundaries"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_stop_criteria_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), stop_criteria=())
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior stop criteria"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_cleanup_plan_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), cleanup_plan=replace(cleanup_plan(), statement="Changed"))
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior cleanup plan"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_rollback_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), rollback=rollback("A different rollback path."))
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior rollback analysis"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_rejects_outcome_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), outcome=None)
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot rewrite the prior outcome"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_allows_approval_references_append_only(self) -> None:
        prior = experiment()
        later = replace(
            prior,
            revision=2,
            supersedes_experiment=next_reference(prior),
            approval_references=prior.approval_references + (approval_reference("approval:two"),),
        )
        self.assertIs(validate_goal_experiment_revision(later, prior), later)

    def test_revision_chain_rules_rejects_approval_references_remove_or_rewrite(self) -> None:
        prior = experiment()
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), approval_references=())
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot remove or rewrite prior approval_references"):
            validate_goal_experiment_revision(later, prior)

    def test_revision_chain_rules_allows_observations_append_only(self) -> None:
        prior = experiment()
        later = replace(
            prior,
            revision=2,
            supersedes_experiment=next_reference(prior),
            observations=prior.observations + (observation("observation:two"),),
        )
        self.assertIs(validate_goal_experiment_revision(later, prior), later)

    def test_revision_chain_rules_rejects_observations_remove_or_rewrite(self) -> None:
        prior = experiment()
        # outcome references "observation:one", so it must also be cleared here to
        # isolate the observations-removal check from the separate outcome-resolution
        # check (both are real, independent invariants; this test targets the former).
        later = replace(prior, revision=2, supersedes_experiment=next_reference(prior), observations=(), outcome=None)
        with self.assertRaisesRegex(GoalEngineExperimentError, "experiment revision cannot remove or rewrite prior observations"):
            validate_goal_experiment_revision(later, prior)


class ExperimentBoundaryTest(unittest.TestCase):
    def test_module_imports_only_standard_library_and_accepted_goal_engine_helpers(self) -> None:
        module_path = Path(__file__).parents[1] / "codie" / "goal_engine" / "experiment.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imports: set[str] = set()
        relatives: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level and node.module:
                    relatives.add(node.module)
                elif node.module:
                    imports.add(node.module.split(".")[0])
        self.assertLessEqual(
            imports,
            {"__future__", "collections", "dataclasses", "datetime", "re", "typing"},
        )
        self.assertEqual(relatives, {"foundation", "impact"})

    def test_records_have_no_authority_or_execution_fields(self) -> None:
        # "outcome" is intentionally excluded: GoalExperiment.outcome is a
        # contract-required reference to a caller-supplied ExperimentOutcome
        # record (interpretation, not authority) -- see Hard Boundaries.
        forbidden = {"score", "rank", "priority", "authority", "approval", "work_order", "result"}
        for record_type in (
            ExperimentQuestion,
            ExperimentHypothesis,
            ExperimentInput,
            ExperimentBoundary,
            ExperimentStopCriterion,
            ExperimentCleanupPlan,
            ExperimentApprovalReference,
            ExperimentObservation,
            ExperimentOutcome,
            GoalExperimentReference,
            GoalExperiment,
        ):
            self.assertTrue({item.name for item in fields(record_type)}.isdisjoint(forbidden), record_type.__name__)


if __name__ == "__main__":
    unittest.main()
