from __future__ import annotations

import ast
import json
import math
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import codie.goal_engine as goal_engine
from codie.goal_engine import (
    EVIDENCE_REFERENCE_SCHEMA_VERSION,
    HEALTH_FINDING_SCHEMA_VERSION,
    HEALTH_MANIFEST_SCHEMA_VERSION,
    HEALTH_SIGNAL_DEFINITION_SCHEMA_VERSION,
    HEALTH_SIGNAL_OBSERVATION_SCHEMA_VERSION,
    IDENTIFIER_SCHEMA_VERSION,
    POLICY_RECORD_SCHEMA_VERSION,
    SUBSYSTEM_HEALTH_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
    SUBSYSTEM_HEALTH_ASSESSMENT_SCHEMA_VERSION,
    FindingIdentifier,
    GoalEngineHealthError,
    GoalEvidenceReference,
    GoalPolicyRecord,
    HealthFinding,
    HealthManifest,
    HealthSignalDefinition,
    HealthSignalObservation,
    SubsystemHealthAssessmentReference,
    build_subsystem_health_assessment,
    health_finding_from_dict,
    health_finding_to_dict,
    health_manifest_from_dict,
    health_manifest_semantic_hash,
    health_manifest_to_dict,
    health_signal_definition_from_dict,
    health_signal_definition_to_dict,
    health_signal_observation_from_dict,
    health_signal_observation_to_dict,
    subsystem_health_assessment_from_dict,
    subsystem_health_assessment_reference_from_dict,
    subsystem_health_assessment_reference_to_dict,
    subsystem_health_assessment_semantic_hash,
    subsystem_health_assessment_to_dict,
    validate_assessment_class,
    validate_finding_class,
    validate_health_domain,
    validate_health_manifest,
    validate_signal_status,
    validate_subsystem_health_assessment_revision,
)

UTC_0 = "2026-08-28T12:00:00Z"
UTC_1 = "2026-08-29T12:00:00Z"
UTC_2 = "2026-08-30T12:00:00Z"


def evidence(
    evidence_ref_id: str = "evidence:test:1",
    *,
    evidence_class: str = "TEST_RUN",
) -> GoalEvidenceReference:
    return GoalEvidenceReference(
        evidence_ref_id=evidence_ref_id,
        evidence_class=evidence_class,
        source_id="source:local-validator",
        source_version="1",
        observed_at=UTC_0,
        historical_validity="VALID_AT_OBSERVATION",
        current_applicability="CURRENT",
        review_state="REVIEWED",
        privacy_class="PUBLIC_METADATA",
        conflict_ref_ids=(),
        schema_version=EVIDENCE_REFERENCE_SCHEMA_VERSION,
    )


def definition(**overrides) -> HealthSignalDefinition:
    data = {
        "definition_id": "health-definition:tests",
        "definition_version": 1,
        "domain": "CODIE",
        "category": "TESTS",
        "assessment_class": "OBJECTIVE",
        "title": "Test execution",
        "description": "Records caller-supplied test evidence.",
        "pass_condition": "The cited test run passed.",
        "degraded_condition": "The cited test run contains a bounded degradation.",
        "fail_condition": "The cited test run failed.",
        "unknown_condition": "No current test evidence is available.",
        "allowed_evidence_classes": ("TEST_RUN",),
        "policy_ref_ids": (),
        "schema_version": HEALTH_SIGNAL_DEFINITION_SCHEMA_VERSION,
    }
    data.update(overrides)
    return HealthSignalDefinition(**data)


def manifest(
    signal_definition: HealthSignalDefinition | None = None,
    **overrides,
) -> HealthManifest:
    signal_definition = signal_definition or definition()
    data = {
        "manifest_id": f"health-manifest:{signal_definition.domain.lower()}",
        "revision": 1,
        "domain": signal_definition.domain,
        "subject_id": f"subject:{signal_definition.domain.lower()}",
        "scope_label": f"{signal_definition.domain} bounded health",
        "definition_ids": (signal_definition.definition_id,),
        "required_definition_ids": (signal_definition.definition_id,),
        "optional_definition_ids": (),
        "scope_manifest_ref_ids": (),
        "supersedes_manifest_hash": None,
        "created_at": UTC_0,
        "schema_version": HEALTH_MANIFEST_SCHEMA_VERSION,
    }
    data.update(overrides)
    return HealthManifest(**data)


def observation(
    signal_definition: HealthSignalDefinition | None = None,
    health_manifest: HealthManifest | None = None,
    **overrides,
) -> HealthSignalObservation:
    signal_definition = signal_definition or definition()
    health_manifest = health_manifest or manifest(signal_definition)
    data = {
        "signal_id": f"health-signal:{signal_definition.domain.lower()}:1",
        "definition_id": signal_definition.definition_id,
        "definition_version": signal_definition.definition_version,
        "domain": signal_definition.domain,
        "category": signal_definition.category,
        "subject_id": health_manifest.subject_id,
        "status": "PASS",
        "summary": "The caller-supplied test run passed.",
        "observed_value": 1345,
        "measurement_unit": "tests",
        "confidence": 1.0,
        "observed_at": UTC_0,
        "fresh_until": UTC_2,
        "evidence_ref_ids": ("evidence:test:1",),
        "conflict_ref_ids": (),
        "limitation": None,
        "not_applicable_reason": None,
        "schema_version": HEALTH_SIGNAL_OBSERVATION_SCHEMA_VERSION,
    }
    data.update(overrides)
    return HealthSignalObservation(**data)


def assessment(**overrides):
    signal_definition = overrides.pop("signal_definition", None) or definition()
    health_manifest = overrides.pop("health_manifest", None) or manifest(
        signal_definition
    )
    signal = overrides.pop("signal", None) or observation(
        signal_definition,
        health_manifest,
    )
    data = {
        "assessment_id": f"health-assessment:{signal_definition.domain.lower()}",
        "revision": 1,
        "domain": signal_definition.domain,
        "manifest": health_manifest,
        "as_of": UTC_1,
        "definitions": (signal_definition,),
        "signals": (signal,),
        "evidence_snapshot": (evidence(),),
    }
    data.update(overrides)
    return build_subsystem_health_assessment(**data)


class HealthVocabularyTest(unittest.TestCase):
    def test_exact_schema_versions_and_vocabularies(self) -> None:
        self.assertEqual(
            HEALTH_SIGNAL_DEFINITION_SCHEMA_VERSION,
            "codie.goal_engine.health_signal_definition.v1",
        )
        self.assertEqual(
            HEALTH_SIGNAL_OBSERVATION_SCHEMA_VERSION,
            "codie.goal_engine.health_signal_observation.v1",
        )
        self.assertEqual(
            SUBSYSTEM_HEALTH_ASSESSMENT_SCHEMA_VERSION,
            "codie.goal_engine.subsystem_health_assessment.v1",
        )
        self.assertEqual(
            {validate_health_domain(value) for value in goal_engine.HEALTH_DOMAINS},
            {"CODIE", "JIN", "THEORY_CORPUS"},
        )
        self.assertEqual(
            {
                validate_signal_status(value)
                for value in goal_engine.SIGNAL_STATUSES
            },
            {
                "PASS",
                "DEGRADED",
                "FAIL",
                "UNKNOWN",
                "CONFLICTED",
                "NOT_APPLICABLE",
            },
        )

    def test_invalid_vocabulary_fails_closed(self) -> None:
        for validator, value in (
            (validate_health_domain, "GLOBAL"),
            (validate_assessment_class, "AVERAGED"),
            (validate_signal_status, "HEALTHY"),
            (validate_finding_class, "GOAL"),
        ):
            with self.subTest(value=value):
                with self.assertRaises(GoalEngineHealthError):
                    validator(value)

    def test_codie_definitions_are_objective_only(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "OBJECTIVE"):
            definition(assessment_class="SEMI_OBJECTIVE")

    def test_jin_factual_and_subjective_categories_remain_distinct(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "OBJECTIVE"):
            definition(
                domain="JIN",
                category="FACTUAL_CORRECTNESS",
                assessment_class="SUBJECTIVE",
            )
        useful = definition(
            definition_id="health-definition:jin-usefulness",
            domain="JIN",
            category="USEFULNESS",
            assessment_class="SUBJECTIVE",
        )
        self.assertEqual(useful.assessment_class, "SUBJECTIVE")
        with self.assertRaisesRegex(GoalEngineHealthError, "SUBJECTIVE"):
            replace(useful, assessment_class="OBJECTIVE")

    def test_theory_interpretation_never_becomes_subjective_fact(self) -> None:
        interpretive = definition(
            definition_id="health-definition:theory-retrieval",
            domain="THEORY_CORPUS",
            category="RETRIEVAL_QUALITY",
            assessment_class="SEMI_OBJECTIVE",
        )
        self.assertEqual(interpretive.assessment_class, "SEMI_OBJECTIVE")
        with self.assertRaisesRegex(GoalEngineHealthError, "SUBJECTIVE"):
            replace(interpretive, assessment_class="SUBJECTIVE")

    def test_records_are_immutable(self) -> None:
        item = definition()
        with self.assertRaises(FrozenInstanceError):
            item.title = "Changed"  # type: ignore[misc]


class HealthObservationTest(unittest.TestCase):
    def test_pass_degraded_and_fail_require_supporting_evidence(self) -> None:
        for status in ("PASS", "DEGRADED", "FAIL"):
            with self.subTest(status=status):
                with self.assertRaisesRegex(GoalEngineHealthError, "supporting evidence"):
                    observation(status=status, evidence_ref_ids=())

    def test_unknown_requires_visible_limitation(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "limitation"):
            observation(status="UNKNOWN", evidence_ref_ids=(), limitation=None)
        item = observation(
            status="UNKNOWN",
            evidence_ref_ids=(),
            limitation="No current test evidence was supplied.",
        )
        self.assertEqual(item.status, "UNKNOWN")

    def test_conflicted_requires_two_separate_conflict_references(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "at least two"):
            observation(
                status="CONFLICTED",
                evidence_ref_ids=(),
                conflict_ref_ids=("evidence:test:1",),
            )
        with self.assertRaisesRegex(GoalEngineHealthError, "remain separate"):
            observation(
                status="CONFLICTED",
                conflict_ref_ids=("evidence:test:1", "evidence:test:2"),
            )

    def test_not_applicable_requires_reason_and_is_distinct_from_unknown(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "requires"):
            observation(
                status="NOT_APPLICABLE",
                evidence_ref_ids=(),
                not_applicable_reason=None,
            )
        item = observation(
            status="NOT_APPLICABLE",
            evidence_ref_ids=(),
            observed_value=None,
            measurement_unit=None,
            not_applicable_reason="Optional signal is outside this scope.",
        )
        self.assertIsNone(item.limitation)

    def test_nonfinite_numbers_and_non_utc_timestamps_fail_closed(self) -> None:
        for value in (math.nan, math.inf, -math.inf):
            with self.subTest(value=value):
                with self.assertRaisesRegex(GoalEngineHealthError, "finite"):
                    observation(observed_value=value)
        with self.assertRaisesRegex(GoalEngineHealthError, "finite"):
            observation(confidence=math.nan)
        with self.assertRaisesRegex(GoalEngineHealthError, "UTC"):
            observation(observed_at="2026-08-28T12:00:00")

    def test_fresh_until_cannot_precede_observation(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "precede"):
            observation(observed_at=UTC_1, fresh_until=UTC_0)


class HealthManifestTest(unittest.TestCase):
    def test_required_and_optional_sets_are_exact_and_disjoint(self) -> None:
        signal_definition = definition()
        with self.assertRaisesRegex(GoalEngineHealthError, "disjoint"):
            manifest(
                signal_definition,
                optional_definition_ids=(signal_definition.definition_id,),
            )
        with self.assertRaisesRegex(GoalEngineHealthError, "exactly cover"):
            manifest(signal_definition, required_definition_ids=())

    def test_theory_corpus_requires_declared_manifest_reference(self) -> None:
        theory_definition = definition(
            definition_id="health-definition:theory-manifest",
            domain="THEORY_CORPUS",
            category="MANIFEST_COMPLETENESS",
        )
        with self.assertRaisesRegex(GoalEngineHealthError, "corpus-manifest"):
            manifest(theory_definition)

    def test_manifest_revision_requires_exact_prior_hash(self) -> None:
        prior = manifest()
        current = replace(
            prior,
            revision=2,
            supersedes_manifest_hash=health_manifest_semantic_hash(prior),
            created_at=UTC_1,
        )
        self.assertEqual(validate_health_manifest(current, prior_manifest=prior), current)
        with self.assertRaisesRegex(GoalEngineHealthError, "does not match"):
            validate_health_manifest(
                replace(current, supersedes_manifest_hash="0" * 64),
                prior_manifest=prior,
            )


class HealthAssessmentBuildTest(unittest.TestCase):
    def test_pass_build_has_counts_without_overall_score_or_finding(self) -> None:
        result = assessment()
        self.assertEqual(result.required_signal_count, 1)
        self.assertEqual(result.observed_required_signal_count, 1)
        self.assertEqual(result.unknown_required_signal_count, 0)
        self.assertEqual(result.conflicted_required_signal_count, 0)
        self.assertEqual(result.findings, ())
        for forbidden in (
            "score",
            "overall_status",
            "grade",
            "rank",
            "recommendation",
            "priority",
            "goal_candidate",
            "action",
        ):
            self.assertFalse(hasattr(result, forbidden))

    def test_degraded_and_failed_signals_create_evidence_bounded_findings(self) -> None:
        for status, expected in (("DEGRADED", "DEGRADATION"), ("FAIL", "FAILURE")):
            with self.subTest(status=status):
                result = assessment(signal=observation(status=status))
                self.assertEqual(
                    {item.finding_class for item in result.findings},
                    {expected},
                )
                self.assertEqual(result.findings[0].evidence_ref_ids, ("evidence:test:1",))

    def test_privacy_failure_remains_bounded_privacy_finding(self) -> None:
        signal_definition = definition(
            definition_id="health-definition:jin-privacy",
            domain="JIN",
            category="PRIVACY",
        )
        health_manifest = manifest(signal_definition)
        result = assessment(
            signal_definition=signal_definition,
            health_manifest=health_manifest,
            signal=observation(
                signal_definition,
                health_manifest,
                status="FAIL",
            ),
        )
        self.assertEqual(result.findings[0].finding_class, "PRIVACY_OR_SECURITY")

    def test_unknown_required_signal_creates_gap_without_becoming_failure(self) -> None:
        result = assessment(
            signal=observation(
                status="UNKNOWN",
                evidence_ref_ids=(),
                observed_value=None,
                measurement_unit=None,
                limitation="No current evidence was supplied.",
            )
        )
        self.assertEqual(result.unknown_required_signal_count, 1)
        self.assertEqual(result.findings[0].finding_class, "EVIDENCE_GAP")

    def test_theory_manifest_unknown_creates_manifest_gap(self) -> None:
        signal_definition = definition(
            definition_id="health-definition:theory-manifest",
            domain="THEORY_CORPUS",
            category="MANIFEST_COMPLETENESS",
            allowed_evidence_classes=("CORPUS_MANIFEST",),
        )
        health_manifest = manifest(
            signal_definition,
            scope_manifest_ref_ids=("evidence:corpus-manifest:1",),
        )
        corpus_evidence = evidence(
            "evidence:corpus-manifest:1",
            evidence_class="CORPUS_MANIFEST",
        )
        signal = observation(
            signal_definition,
            health_manifest,
            status="UNKNOWN",
            evidence_ref_ids=(),
            observed_value=None,
            measurement_unit=None,
            limitation="Manifest completeness has not been established.",
        )
        result = assessment(
            signal_definition=signal_definition,
            health_manifest=health_manifest,
            signal=signal,
            evidence_snapshot=(corpus_evidence,),
        )
        self.assertEqual(result.findings[0].finding_class, "MANIFEST_GAP")

    def test_conflicted_signal_preserves_both_conflicting_references(self) -> None:
        signal = observation(
            status="CONFLICTED",
            evidence_ref_ids=(),
            conflict_ref_ids=("evidence:test:1", "evidence:test:2"),
        )
        result = assessment(
            signal=signal,
            evidence_snapshot=(evidence(), evidence("evidence:test:2")),
        )
        self.assertEqual(result.conflicted_required_signal_count, 1)
        self.assertEqual(result.findings[0].finding_class, "EVIDENCE_CONFLICT")
        self.assertEqual(
            result.findings[0].conflict_ref_ids,
            ("evidence:test:1", "evidence:test:2"),
        )

    def test_stale_pass_remains_pass_and_emits_stale_evidence_finding(self) -> None:
        signal = observation(fresh_until=UTC_0)
        result = assessment(signal=signal, as_of=UTC_1)
        self.assertEqual(result.signals[0].status, "PASS")
        self.assertEqual(result.findings[0].finding_class, "STALE_EVIDENCE")

    def test_not_applicable_is_allowed_only_for_optional_signal(self) -> None:
        signal_definition = definition()
        optional_manifest = manifest(
            signal_definition,
            required_definition_ids=(),
            optional_definition_ids=(signal_definition.definition_id,),
        )
        signal = observation(
            signal_definition,
            optional_manifest,
            status="NOT_APPLICABLE",
            evidence_ref_ids=(),
            observed_value=None,
            measurement_unit=None,
            fresh_until=None,
            not_applicable_reason="Outside the bounded optional scope.",
        )
        result = assessment(
            signal_definition=signal_definition,
            health_manifest=optional_manifest,
            signal=signal,
        )
        self.assertEqual(result.required_signal_count, 0)
        self.assertEqual(result.findings, ())
        with self.assertRaisesRegex(GoalEngineHealthError, "cannot hide"):
            assessment(
                signal=replace(
                    signal,
                    subject_id=manifest(signal_definition).subject_id,
                )
            )

    def test_missing_or_duplicate_required_observation_fails_closed(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "missing required"):
            assessment(signals=(), signal=observation())
        signal = observation()
        with self.assertRaisesRegex(GoalEngineHealthError, "duplicate observation"):
            assessment(
                signals=(signal, replace(signal, signal_id="health-signal:codie:2")),
                signal=signal,
            )

    def test_dangling_and_disallowed_evidence_fail_closed(self) -> None:
        with self.assertRaisesRegex(GoalEngineHealthError, "dangling evidence"):
            assessment(evidence_snapshot=())
        with self.assertRaisesRegex(GoalEngineHealthError, "not allowed"):
            assessment(
                evidence_snapshot=(
                    evidence(evidence_class="TOURNAMENT_RESULT"),
                )
            )

    def test_cross_domain_category_subject_and_version_mismatches_fail_closed(self) -> None:
        cases = (
            ("domain", "JIN"),
            ("category", "VALIDATORS"),
            ("subject_id", "subject:other"),
            ("definition_version", 2),
        )
        for field_name, value in cases:
            with self.subTest(field_name=field_name):
                signal = observation()
                with self.assertRaises(GoalEngineHealthError):
                    assessment(signal=replace(signal, **{field_name: value}))

    def test_policy_and_scope_manifest_references_must_resolve(self) -> None:
        signal_definition = definition(policy_ref_ids=("policy:health:1",))
        with self.assertRaisesRegex(GoalEngineHealthError, "dangling policy"):
            assessment(signal_definition=signal_definition)
        policy = GoalPolicyRecord(
            policy_id="policy:health:1",
            policy_version=1,
            schema_version=POLICY_RECORD_SCHEMA_VERSION,
            date="2026-08-28",
            reason="Bound this health definition.",
            rule="Use only caller-supplied evidence.",
            authority_ref_ids=("authority:human:1",),
            affected_policy_ids=(),
            superseded_policy_ref=None,
            regression_case_ids=("regression:health:1",),
        )
        result = assessment(
            signal_definition=signal_definition,
            signal=observation(signal_definition),
            policy_snapshot=(policy,),
        )
        self.assertEqual(result.definitions[0].policy_ref_ids, ("policy:health:1",))

    def test_generated_finding_identity_and_output_are_order_stable(self) -> None:
        signal_definition = definition(
            allowed_evidence_classes=("VALIDATOR_RUN", "TEST_RUN")
        )
        health_manifest = manifest(signal_definition)
        signal = observation(
            signal_definition,
            health_manifest,
            status="FAIL",
            evidence_ref_ids=("evidence:test:2", "evidence:test:1"),
        )
        first = assessment(
            signal_definition=signal_definition,
            health_manifest=health_manifest,
            signal=signal,
            evidence_snapshot=(
                evidence("evidence:test:2", evidence_class="VALIDATOR_RUN"),
                evidence(),
            ),
        )
        second = build_subsystem_health_assessment(
            assessment_id=first.assessment_id,
            revision=1,
            domain="CODIE",
            manifest=health_manifest,
            as_of=UTC_1,
            definitions=(signal_definition,),
            signals=(signal,),
            evidence_snapshot=tuple(reversed(first.evidence_snapshot)),
        )
        self.assertEqual(
            subsystem_health_assessment_to_dict(first),
            subsystem_health_assessment_to_dict(second),
        )
        self.assertEqual(
            subsystem_health_assessment_semantic_hash(first),
            subsystem_health_assessment_semantic_hash(second),
        )

    def test_generated_finding_identity_includes_full_evidence_semantics(self) -> None:
        failed_signal = observation(status="FAIL")
        first = assessment(signal=failed_signal)
        revised_evidence = replace(evidence(), source_version="2")
        second = assessment(
            signal=failed_signal,
            evidence_snapshot=(revised_evidence,),
        )
        self.assertNotEqual(
            first.findings[0].finding_id,
            second.findings[0].finding_id,
        )

    def test_three_domains_build_only_as_separate_assessments(self) -> None:
        cases = (
            ("CODIE", "TESTS", "OBJECTIVE", ()),
            ("JIN", "USEFULNESS", "SUBJECTIVE", ()),
            (
                "THEORY_CORPUS",
                "GRAPH_HEALTH",
                "OBJECTIVE",
                ("evidence:test:1",),
            ),
        )
        results = []
        for domain, category, assessment_class, scope_refs in cases:
            signal_definition = definition(
                definition_id=f"health-definition:{domain.lower()}",
                domain=domain,
                category=category,
                assessment_class=assessment_class,
            )
            health_manifest = manifest(
                signal_definition,
                scope_manifest_ref_ids=scope_refs,
            )
            results.append(
                assessment(
                    signal_definition=signal_definition,
                    health_manifest=health_manifest,
                    signal=observation(signal_definition, health_manifest),
                )
            )
        self.assertEqual({item.domain for item in results}, set(goal_engine.HEALTH_DOMAINS))
        self.assertFalse(hasattr(goal_engine, "build_combined_health_assessment"))

    def test_caller_finding_cannot_invent_evidence_or_use_pass_signal(self) -> None:
        failed_signal = observation(status="FAIL")
        caller = HealthFinding(
            finding_id=FindingIdentifier(
                "FINDING",
                "health:caller:1",
                IDENTIFIER_SCHEMA_VERSION,
            ),
            domain="CODIE",
            finding_class="FAILURE",
            signal_ids=(failed_signal.signal_id,),
            statement="Caller-supplied bounded finding.",
            why_it_matters="The cited signal failed.",
            evidence_ref_ids=("evidence:invented",),
            conflict_ref_ids=(),
            confidence=0.5,
            disconfirmation_criteria=("Supply passing evidence.",),
            limitations=("Caller supplied.",),
            created_at=UTC_1,
            schema_version=HEALTH_FINDING_SCHEMA_VERSION,
        )
        with self.assertRaisesRegex(GoalEngineHealthError, "exceeds"):
            assessment(signal=failed_signal, findings=(caller,))
        with self.assertRaisesRegex(GoalEngineHealthError, "PASS"):
            assessment(findings=(replace(caller, evidence_ref_ids=("evidence:test:1",)),))

    def test_caller_finding_class_must_match_signal_and_preserve_conflicts(self) -> None:
        failed_signal = observation(status="FAIL")
        caller = HealthFinding(
            finding_id=FindingIdentifier(
                "FINDING",
                "health:caller:class",
                IDENTIFIER_SCHEMA_VERSION,
            ),
            domain="CODIE",
            finding_class="DEGRADATION",
            signal_ids=(failed_signal.signal_id,),
            statement="Mismatched caller finding.",
            why_it_matters="The class must match the source status.",
            evidence_ref_ids=("evidence:test:1",),
            conflict_ref_ids=(),
            confidence=0.5,
            disconfirmation_criteria=("Supply passing evidence.",),
            limitations=("Caller supplied.",),
            created_at=UTC_1,
            schema_version=HEALTH_FINDING_SCHEMA_VERSION,
        )
        with self.assertRaisesRegex(GoalEngineHealthError, "does not match"):
            assessment(signal=failed_signal, findings=(caller,))
        conflicted_signal = observation(
            status="CONFLICTED",
            evidence_ref_ids=(),
            conflict_ref_ids=("evidence:test:1", "evidence:test:2"),
        )
        conflict_finding = replace(
            caller,
            finding_id=FindingIdentifier(
                "FINDING",
                "health:caller:conflict",
                IDENTIFIER_SCHEMA_VERSION,
            ),
            finding_class="EVIDENCE_CONFLICT",
            signal_ids=(conflicted_signal.signal_id,),
            evidence_ref_ids=(),
            conflict_ref_ids=("evidence:test:1",),
        )
        with self.assertRaisesRegex(GoalEngineHealthError, "at least two"):
            assessment(
                signal=conflicted_signal,
                findings=(conflict_finding,),
                evidence_snapshot=(evidence(), evidence("evidence:test:2")),
            )

    def test_revision_chain_requires_exact_prior_semantic_hash(self) -> None:
        prior = assessment()
        reference = SubsystemHealthAssessmentReference(
            assessment_id=prior.assessment_id,
            revision=prior.revision,
            domain=prior.domain,
            semantic_hash=subsystem_health_assessment_semantic_hash(prior),
            schema_version=SUBSYSTEM_HEALTH_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
        )
        prior_manifest = prior.manifest
        next_manifest = replace(
            prior_manifest,
            revision=2,
            supersedes_manifest_hash=health_manifest_semantic_hash(prior_manifest),
            created_at=UTC_1,
        )
        current = build_subsystem_health_assessment(
            assessment_id=prior.assessment_id,
            revision=2,
            domain=prior.domain,
            manifest=next_manifest,
            as_of=UTC_2,
            definitions=prior.definitions,
            signals=prior.signals,
            evidence_snapshot=prior.evidence_snapshot,
            supersedes_assessment=reference,
            prior_manifest=prior_manifest,
            prior_assessment=prior,
        )
        self.assertEqual(
            validate_subsystem_health_assessment_revision(current, prior),
            current,
        )
        with self.assertRaisesRegex(GoalEngineHealthError, "does not match"):
            validate_subsystem_health_assessment_revision(
                replace(
                    current,
                    supersedes_assessment=replace(reference, semantic_hash="0" * 64),
                ),
                prior,
            )


class HealthSerializationTest(unittest.TestCase):
    def test_all_records_round_trip_exactly(self) -> None:
        result = assessment(signal=observation(status="FAIL"))
        cases = (
            (
                result.definitions[0],
                health_signal_definition_to_dict,
                health_signal_definition_from_dict,
            ),
            (
                result.signals[0],
                health_signal_observation_to_dict,
                health_signal_observation_from_dict,
            ),
            (result.manifest, health_manifest_to_dict, health_manifest_from_dict),
            (result.findings[0], health_finding_to_dict, health_finding_from_dict),
            (
                result,
                subsystem_health_assessment_to_dict,
                subsystem_health_assessment_from_dict,
            ),
        )
        for record, to_dict, from_dict in cases:
            with self.subTest(record=type(record).__name__):
                self.assertEqual(from_dict(to_dict(record)), record)

    def test_assessment_reference_round_trip(self) -> None:
        result = assessment()
        reference = SubsystemHealthAssessmentReference(
            assessment_id=result.assessment_id,
            revision=1,
            domain=result.domain,
            semantic_hash=subsystem_health_assessment_semantic_hash(result),
            schema_version=SUBSYSTEM_HEALTH_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
        )
        self.assertEqual(
            subsystem_health_assessment_reference_from_dict(
                subsystem_health_assessment_reference_to_dict(reference)
            ),
            reference,
        )

    def test_exact_field_parsing_rejects_unknown_and_forbidden_fields(self) -> None:
        payload = health_signal_definition_to_dict(definition())
        payload["extra"] = True
        with self.assertRaisesRegex(GoalEngineHealthError, "unknown field"):
            health_signal_definition_from_dict(payload)
        payload = health_signal_definition_to_dict(definition())
        payload["raw_payload"] = {}
        with self.assertRaisesRegex(GoalEngineHealthError, "forbidden field"):
            health_signal_definition_from_dict(payload)
        payload = subsystem_health_assessment_to_dict(assessment())
        payload["score"] = 100
        with self.assertRaisesRegex(GoalEngineHealthError, "forbidden field"):
            subsystem_health_assessment_from_dict(payload)

    def test_canonical_json_is_byte_stable_and_contains_provenance(self) -> None:
        result = assessment()
        first = json.dumps(
            subsystem_health_assessment_to_dict(result),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        restored = subsystem_health_assessment_from_dict(
            subsystem_health_assessment_to_dict(result)
        )
        second = json.dumps(
            subsystem_health_assessment_to_dict(restored),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        self.assertEqual(first, second)
        self.assertIn(b"evidence:test:1", first)


class HealthBoundaryTest(unittest.TestCase):
    def test_module_uses_only_pure_standard_library_and_foundation_imports(self) -> None:
        source_path = Path(goal_engine.health.__file__)
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported_roots = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported_roots.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module is not None
            and node.module not in {"__future__", "foundation"}
        )
        self.assertEqual(
            imported_roots,
            {"collections", "dataclasses", "datetime", "math", "re", "types", "typing"},
        )
        forbidden_imports = {
            "asyncio",
            "http",
            "os",
            "pathlib",
            "random",
            "requests",
            "socket",
            "sqlite3",
            "subprocess",
            "time",
            "urllib",
            "uuid",
        }
        self.assertFalse(imported_roots & forbidden_imports)

    def test_public_surface_contains_no_authority_or_integration_methods(self) -> None:
        exported = "\n".join(goal_engine.health.__all__).lower()
        for forbidden in (
            "activate_goal",
            "aggregate_health",
            "build_graph",
            "ccpm",
            "fetch",
            "health_score",
            "moxfield",
            "persist",
            "provider",
            "recommend",
            "schedule",
            "scryfall",
            "stream_deck",
        ):
            self.assertNotIn(forbidden, exported)

    def test_assessment_has_no_mutating_or_later_phase_methods(self) -> None:
        result = assessment()
        for forbidden in (
            "execute",
            "save",
            "promote",
            "rank",
            "create_goal",
            "resolve_automatically",
        ):
            self.assertFalse(hasattr(result, forbidden))


if __name__ == "__main__":
    unittest.main()
