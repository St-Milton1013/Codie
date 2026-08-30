"""Contract tests for the pure Phase44O Change / Impact Engine."""

from __future__ import annotations

import ast
import unittest
from dataclasses import fields, replace
from pathlib import Path

from codie.goal_engine.foundation import EVIDENCE_REFERENCE_SCHEMA_VERSION, GoalEvidenceReference
from codie.goal_engine.idea_ledger import (
    LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
    LedgerEntityReference,
)
from codie.goal_engine.impact import (
    CHANGE_CANDIDATE_SCHEMA_VERSION,
    CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
    HISTORICAL_ATTEMPT_REFERENCE_SCHEMA_VERSION,
    IMPACT_ASSUMPTION_SCHEMA_VERSION,
    IMPACT_EFFECT_SCHEMA_VERSION,
    IMPACT_SUBJECT_REFERENCE_SCHEMA_VERSION,
    IMPACT_VALIDATION_REQUIREMENT_SCHEMA_VERSION,
    ROLLBACK_ANALYSIS_SCHEMA_VERSION,
    ChangeCandidate,
    ChangeImpactAssessmentReference,
    DependencyEffect,
    GoalEngineImpactError,
    HistoricalAttemptReference,
    ImpactAssumption,
    ImpactEffect,
    ImpactSubjectReference,
    ImpactValidationRequirement,
    RollbackAnalysis,
    build_change_impact_assessment,
    change_impact_assessment_from_dict,
    change_impact_assessment_semantic_hash,
    change_impact_assessment_to_dict,
    validate_change_impact_assessment_revision,
)

T1 = "2026-08-30T00:00:00Z"
T2 = "2026-08-30T00:01:00Z"


def subject(entity_id: str = "idea:impact") -> LedgerEntityReference:
    return LedgerEntityReference(
        entity_kind="IDEA",
        entity_id=entity_id,
        revision=1,
        semantic_hash="a" * 64,
        schema_version=LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
    )


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


def candidate() -> ChangeCandidate:
    return ChangeCandidate(
        change_id="change:one",
        subject=subject(),
        goal_ref=None,
        goal_contract_ref=None,
        proposed_change_summary="A caller proposes a bounded local adjustment.",
        baseline_summary="The supplied baseline is incomplete.",
        expected_result_summary="This remains an expectation, not an outcome.",
        evidence_ref_ids=("evidence:one",),
        conflict_ref_ids=(),
        limitations=("No scope discovery or authorization is implied.",),
        created_at=T1,
        schema_version=CHANGE_CANDIDATE_SCHEMA_VERSION,
    )


def assessment(
    *,
    revision: int = 1,
    supersedes: ChangeImpactAssessmentReference | None = None,
    prior=None,
):
    main = subject()
    unknown = subject("idea:unknown")
    requirement = ImpactValidationRequirement(
        requirement_id="requirement:review",
        requirement_kind="MANUAL_REVIEW",
        statement="A later human review is required.",
        evidence_ref_ids=("evidence:one",),
        expected_subject_refs=(main,),
        human_review_required=True,
        limitations=("This declaration does not schedule review.",),
        schema_version=IMPACT_VALIDATION_REQUIREMENT_SCHEMA_VERSION,
    )
    return build_change_impact_assessment(
        assessment_id="assessment:one",
        revision=revision,
        change=candidate(),
        as_of=T2,
        affected_subjects=(
            ImpactSubjectReference(main, "EXPECTED_AFFECTED", ("evidence:one",), ("Caller-supplied only.",), IMPACT_SUBJECT_REFERENCE_SCHEMA_VERSION),
            ImpactSubjectReference(unknown, "UNKNOWN", (), ("The gap remains visible.",), IMPACT_SUBJECT_REFERENCE_SCHEMA_VERSION),
        ),
        effects=(
            ImpactEffect("effect:possible", main, "PRIVACY", "POSSIBLE", "EXPECTED_AFFECTED", "Privacy impact is caller-supplied as possible.", ("evidence:one",), (), ("assumption:one",), ("No causal claim is made.",), IMPACT_EFFECT_SCHEMA_VERSION),
            ImpactEffect("effect:direct", main, "FUNCTIONAL", "DIRECT", "EXPECTED_AFFECTED", "Functional impact is caller-supplied as direct.", ("evidence:one",), (), (), ("Expected impact is not an observed result.",), IMPACT_EFFECT_SCHEMA_VERSION),
            ImpactEffect("effect:indirect", unknown, "SECURITY", "INDIRECT", "UNKNOWN", "Security impact remains caller-supplied and unknown.", (), (), (), ("No safety guarantee is made.",), IMPACT_EFFECT_SCHEMA_VERSION),
        ),
        dependency_effects=(
            DependencyEffect("dependency:one", main, subject("finding:dependency"), "REQUIRES", "A caller supplied dependency is required.", ("evidence:one",), ("No work is scheduled.",), "codie.goal_engine.dependency_effect.v1"),
        ),
        assumptions=(
            ImpactAssumption("assumption:one", "A supplied environment condition remains uncertain.", (), ("A later observation contradicts the condition.",), ("This is not a fact.",), IMPACT_ASSUMPTION_SCHEMA_VERSION),
        ),
        rollback=RollbackAnalysis("Moderate", None, "A caller supplied rollback plan exists.", ("Preserve the known caller reference.",), ("requirement:review",), "Residual uncertainty remains.", ("The plan does not execute rollback.",), ROLLBACK_ANALYSIS_SCHEMA_VERSION),
        validation_requirements=(requirement,),
        historical_attempts=(),
        evidence_snapshot=(evidence(),),
        supersedes_assessment=supersedes,
        prior_assessment=prior,
    )


class ChangeImpactRoundTripTest(unittest.TestCase):
    def test_canonical_round_trip_preserves_distinctions(self) -> None:
        value = assessment()
        restored = change_impact_assessment_from_dict(change_impact_assessment_to_dict(value))
        self.assertEqual(restored, value)
        self.assertEqual([item.likelihood for item in value.effects], ["DIRECT", "INDIRECT", "POSSIBLE"])
        self.assertEqual([item.expected_state for item in value.affected_subjects], ["EXPECTED_AFFECTED", "UNKNOWN"])
        self.assertEqual(change_impact_assessment_semantic_hash(restored), change_impact_assessment_semantic_hash(value))

    def test_exact_field_parsing_rejects_hidden_input(self) -> None:
        payload = change_impact_assessment_to_dict(assessment())
        payload["score"] = 1
        with self.assertRaisesRegex(GoalEngineImpactError, "fields must match exactly"):
            change_impact_assessment_from_dict(payload)

    def test_candidate_keeps_supporting_and_conflicting_evidence_distinct(self) -> None:
        with self.assertRaisesRegex(GoalEngineImpactError, "remain distinct"):
            replace(candidate(), conflict_ref_ids=("evidence:one",))

    def test_unresolved_evidence_is_rejected(self) -> None:
        bad = replace(candidate(), evidence_ref_ids=("evidence:missing",))
        with self.assertRaisesRegex(GoalEngineImpactError, "unresolved"):
            build_change_impact_assessment(
                assessment_id="assessment:bad",
                revision=1,
                change=bad,
                as_of=T2,
                affected_subjects=(),
                effects=(),
                dependency_effects=(),
                assumptions=(),
                rollback=RollbackAnalysis("Easy", None, "Plan only.", (), (), "Risk remains.", ("No execution occurs.",), ROLLBACK_ANALYSIS_SCHEMA_VERSION),
                validation_requirements=(),
                historical_attempts=(),
                evidence_snapshot=(evidence(),),
                supersedes_assessment=None,
            )

    def test_effect_subject_must_be_explicit(self) -> None:
        value = assessment()
        with self.assertRaisesRegex(GoalEngineImpactError, "explicit affected_subject"):
            replace(value, affected_subjects=value.affected_subjects[1:])


class ChangeImpactHistoryAndRevisionTest(unittest.TestCase):
    def test_material_difference_disposition_requires_text(self) -> None:
        with self.assertRaisesRegex(GoalEngineImpactError, "material_difference_summary"):
            HistoricalAttemptReference(
                attempt_ref=subject("idea:history"),
                disposition="MATERIAL_DIFFERENCE_DOCUMENTED",
                material_difference_summary=None,
                evidence_ref_ids=(),
                limitations=("No automatic applicability follows.",),
                schema_version=HISTORICAL_ATTEMPT_REFERENCE_SCHEMA_VERSION,
            )

    def test_later_revision_requires_immediate_prior_hash(self) -> None:
        prior = assessment()
        reference = ChangeImpactAssessmentReference(
            assessment_id=prior.assessment_id,
            revision=prior.revision,
            semantic_hash=change_impact_assessment_semantic_hash(prior),
            schema_version=CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
        )
        later = assessment(revision=2, supersedes=reference, prior=prior)
        self.assertIs(validate_change_impact_assessment_revision(later, prior), later)
        with self.assertRaisesRegex(GoalEngineImpactError, "semantic hash"):
            validate_change_impact_assessment_revision(
                replace(later, supersedes_assessment=replace(reference, semantic_hash="f" * 64)),
                prior,
            )

    def test_later_revision_cannot_skip_predecessor(self) -> None:
        with self.assertRaisesRegex(GoalEngineImpactError, "prior_assessment"):
            assessment(revision=2, supersedes=ChangeImpactAssessmentReference("assessment:one", 1, "a" * 64, CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION))

    def test_later_revision_cannot_remove_or_rewrite_prior_records(self) -> None:
        prior = assessment()
        reference = ChangeImpactAssessmentReference(
            prior.assessment_id,
            prior.revision,
            change_impact_assessment_semantic_hash(prior),
            CHANGE_IMPACT_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
        )
        later = assessment(revision=2, supersedes=reference, prior=prior)
        with self.assertRaisesRegex(GoalEngineImpactError, "remove or rewrite prior effects"):
            validate_change_impact_assessment_revision(replace(later, effects=()), prior)


class ChangeImpactBoundaryTest(unittest.TestCase):
    def test_module_imports_only_standard_library_and_accepted_goal_engine_helpers(self) -> None:
        module_path = Path(__file__).parents[1] / "codie" / "goal_engine" / "impact.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imports = set()
        relatives = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    relatives.add(node.module)
                elif node.module:
                    imports.add(node.module.split(".")[0])
        self.assertLessEqual(
            imports,
            {"__future__", "collections", "dataclasses", "datetime", "re", "typing"},
        )
        self.assertEqual(relatives, {"foundation", "idea_ledger"})

    def test_records_have_no_authority_or_execution_fields(self) -> None:
        forbidden = {"score", "rank", "priority", "authority", "approval", "work_order", "outcome", "result"}
        for record_type in (
            ChangeCandidate,
            ImpactSubjectReference,
            ImpactEffect,
            DependencyEffect,
            ImpactAssumption,
            RollbackAnalysis,
            ImpactValidationRequirement,
            HistoricalAttemptReference,
        ):
            self.assertTrue({item.name for item in fields(record_type)}.isdisjoint(forbidden), record_type.__name__)


if __name__ == "__main__":
    unittest.main()
