from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.decision_intelligence import build_decision_packet
from codie.evidence_fusion import (
    EvidenceAuthorityRef,
    EvidenceCaveat,
    EvidenceMetricRef,
    EvidenceObservationRef,
    EvidencePrimerContextRef,
    EvidenceSimulatorRef,
    EvidenceSourceAgreement,
    UnifiedEvidenceSubject,
    build_unified_evidence_object,
)
from codie.recommendation_output import (
    DeckHealthFinding,
    RecommendationOutputBuildError,
    RecommendationOutputOptions,
    build_deck_health_packet,
    build_evidence_explanation_packet,
    build_package_gap_packet,
    build_recommendation_candidate_packet,
    build_recommendation_output_bundle,
    build_replacement_suggestion_packet,
    recommendation_candidate_packet_to_dict,
    recommendation_output_bundle_to_dict,
    replacement_suggestion_packet_to_dict,
)
from codie.weight_profiles import WeightComponent, build_analysis_profile, build_weight_profile


GENERATED_AT = "2026-07-08T00:00:00+00:00"


def subject(**overrides) -> UnifiedEvidenceSubject:
    data = {
        "subject_id": "subject:deck:fixture",
        "subject_type": "deck",
        "subject_key": "deck:fixture",
        "display_name": "Fixture Deck",
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return UnifiedEvidenceSubject(**data)


def source_agreement(**overrides) -> EvidenceSourceAgreement:
    data = {
        "agreement_id": "agreement:fixture",
        "agreement_label": "strong",
        "supporting_ref_ids": ("metric:inclusion:rhystic-study",),
        "conflicting_ref_ids": (),
        "coverage_ratio": 0.84,
        "sample_size": 50,
        "generated_at": GENERATED_AT,
        "metadata": {"sources": 2},
    }
    data.update(overrides)
    return EvidenceSourceAgreement(**data)


def caveat(**overrides) -> EvidenceCaveat:
    data = {
        "caveat_id": "caveat:coverage",
        "caveat_type": "low_coverage",
        "severity": "warning",
        "message": "Coverage is below preferred threshold.",
        "related_ref_ids": ("metric:inclusion:rhystic-study",),
        "generated_at": GENERATED_AT,
        "metadata": {"coverage_ratio": 0.84},
    }
    data.update(overrides)
    return EvidenceCaveat(**data)


def evidence_object(**overrides):
    item_subject = overrides.pop("subject", subject())
    data = {
        "evidence_object_id": "evidence:fixture",
        "subject": item_subject,
        "source_agreement": source_agreement(),
        "generated_at": GENERATED_AT,
        "authority_refs": (
            EvidenceAuthorityRef(
                authority_ref_id="authority:scryfall:rhystic-study",
                authority_type="scryfall_card",
                authority_source="scryfall",
                authority_key="scryfall-rhystic-study",
                authority_label="Rhystic Study",
                authority_url="https://scryfall.example/cards/rhystic-study",
                authority_version="fixture",
                generated_at=GENERATED_AT,
                metadata={"oracle_id": "oracle-rhystic-study"},
            ),
        ),
        "observation_refs": (
            EvidenceObservationRef(
                observation_ref_id="observation:deck:1",
                observation_type="canonical_deck_card",
                source_system="canonical",
                source_record_id="canonical_deck_card:1",
                canonical_record_id="canonical_deck:1",
                source_label="Fixture Top 16 Deck",
                source_url="https://example.test/deck/1",
                observed_at="2026-07-01",
                generated_at=GENERATED_AT,
                metadata={"placement": "top_16"},
            ),
        ),
        "metric_refs": (
            EvidenceMetricRef(
                metric_ref_id="metric:inclusion:rhystic-study",
                metric_type="inclusion_rate",
                metric_name="Top 16 inclusion rate",
                metric_value=0.42,
                metric_unit="ratio",
                scope_type="commander",
                scope_key="commander:fixture",
                window_start="2026-06-01",
                window_end="2026-07-01",
                sample_size=50,
                coverage_ratio=0.84,
                generated_at=GENERATED_AT,
                metadata={"window_days": 30},
            ),
        ),
        "primer_context_refs": (
            EvidencePrimerContextRef(
                primer_context_ref_id="primer-context:1",
                primer_ref_id="primer:1",
                context_type="strategy_summary",
                context_label="Primer context only.",
                commander_signature="Tymna the Weaver|Kraum, Ludevic's Opus",
                source_url="https://moxfield.example/primer/1",
                generated_at=GENERATED_AT,
                metadata={"body_stripped": True},
            ),
        ),
        "simulator_refs": (
            EvidenceSimulatorRef(
                simulator_ref_id="simulator:1",
                simulation_type="target_access",
                result_id="result:1",
                deck_hash="deck-hash-fixture",
                target_label="Cast Rhystic Study by turn 2",
                success_rate=0.18,
                sample_size=1000,
                unsupported_cards_count=2,
                review_status="unreviewed",
                generated_at=GENERATED_AT,
                metadata={"seed": "fixture-seed"},
            ),
        ),
        "caveats": (caveat(),),
        "conflicts": (),
        "evidence_level": "high",
        "speculation_level": "low",
        "coverage_ratio": 0.84,
        "sample_size": 50,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_unified_evidence_object(**data)


def decision_packet(**overrides):
    item_subject = overrides.pop("subject", subject())
    item_evidence = overrides.pop("evidence_objects", (evidence_object(subject=item_subject),))
    data = {
        "decision_id": "decision:fixture:signal",
        "decision_type": "candidate_signal",
        "subject": item_subject,
        "summary": "Evidence signal for fixture deck.",
        "confidence": 0.72,
        "expected_impact": "medium",
        "source_agreement": source_agreement(),
        "evidence_objects": item_evidence,
        "generated_at": GENERATED_AT,
        "speculation_level": "low",
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_decision_packet(**data)


def weight_profile(**overrides):
    component = WeightComponent(
        component_id="measured-metric",
        component_name="Measured Metrics",
        component_type="measured_metric",
        weight=1.0,
        enabled=True,
        minimum_threshold=0.0,
        maximum_threshold=1.0,
        applies_to_decision_types=("all",),
        description="Measured evidence signal.",
        metadata={"visible": True},
    )
    data = {
        "profile_id": "competitive-default",
        "profile_name": "competitive-default",
        "profile_version": "1.0.0",
        "profile_label": "Competitive Default",
        "profile_description": "Balanced competitive evidence profile.",
        "components": (component,),
        "normalization_rule": "none",
        "minimum_confidence": 0.25,
        "minimum_coverage_ratio": 0.1,
        "minimum_sample_size": 1,
        "generated_at": GENERATED_AT,
        "analysis_version": "phase27b-weight-profile",
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_weight_profile(**data)


def analysis_profile(**overrides):
    data = {
        "analysis_profile_id": "analysis-profile:competitive-default",
        "analysis_profile_name": "Competitive Default Analysis",
        "analysis_profile_version": "1.0.0",
        "weight_profile_id": "competitive-default",
        "weight_profile_version": "1.0.0",
        "decision_version": "phase26b-boundary",
        "evidence_version": "phase25a-contract",
        "analysis_scope": "deck_analysis",
        "default_filters": {"minimum_sample_size": 1},
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return build_analysis_profile(**data)


def output_context(**overrides):
    item_subject = overrides.pop("subject", subject())
    item_evidence = overrides.pop("evidence_objects", (evidence_object(subject=item_subject),))
    item_decisions = overrides.pop("decision_packets", (decision_packet(subject=item_subject, evidence_objects=item_evidence),))
    data = {
        "subject": item_subject,
        "source_agreement": source_agreement(),
        "decision_packets": item_decisions,
        "evidence_objects": item_evidence,
        "weight_profile": weight_profile(),
        "analysis_profile": analysis_profile(),
        "generated_at": GENERATED_AT,
    }
    data.update(overrides)
    return data


def finding(**overrides) -> DeckHealthFinding:
    data = {
        "finding_id": "finding:interaction",
        "health_category": "interaction",
        "severity": "warning",
        "finding_label": "Interaction density differs from comparison pool.",
        "finding_summary": "Interaction count is below the selected comparison pool.",
        "affected_cards": ("Rhystic Study",),
        "affected_roles": ("interaction",),
        "supporting_ref_ids": ("metric:inclusion:rhystic-study",),
        "caveat_ids": ("caveat:coverage",),
        "metadata": {"visible": True},
    }
    data.update(overrides)
    return DeckHealthFinding(**data)


class RecommendationOutputBoundaryTest(unittest.TestCase):
    def test_deck_health_packet_exposes_required_evidence_and_profile_versions(self) -> None:
        packet = build_deck_health_packet(
            output_id="output:health:1",
            summary="Interaction density differs from comparison pool.",
            confidence=0.72,
            expected_impact="medium",
            findings=(finding(),),
            **output_context(),
        )
        payload = recommendation_output_bundle_to_dict(
            build_recommendation_output_bundle(
                bundle_id="bundle:recommendation-output:1",
                bundle_type="deck_analysis",
                subject=subject(),
                deck_health_packets=(packet,),
                generated_at=GENERATED_AT,
            )
        )
        item = payload["deck_health_packets"][0]

        json.dumps(payload, sort_keys=True)
        self.assertEqual(item["decision_ids"], ["decision:fixture:signal"])
        self.assertEqual(item["evidence_object_ids"], ["evidence:fixture"])
        self.assertEqual(item["weight_profile_id"], "competitive-default")
        self.assertEqual(item["weight_profile_version"], "1.0.0")
        self.assertEqual(item["analysis_profile_id"], "analysis-profile:competitive-default")
        self.assertEqual(item["analysis_profile_version"], "1.0.0")
        self.assertEqual(item["source_agreement"]["agreement_label"], "strong")
        self.assertEqual(item["caveat_ids"], ["caveat:coverage"])
        self.assertEqual(item["speculation_level"], "none")

    def test_candidate_packet_allows_monitor_investigate_and_no_action(self) -> None:
        for recommendation_type in ("monitor", "investigate", "no_action"):
            packet = build_recommendation_candidate_packet(
                output_id=f"output:candidate:{recommendation_type}",
                summary="Candidate is tracked for review.",
                confidence=0.22,
                expected_impact="unknown",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type=recommendation_type,
                role_tags=("card_advantage",),
                evidence_summary="Evidence is below the action threshold.",
                **output_context(),
            )
            payload = recommendation_candidate_packet_to_dict(packet)

            self.assertEqual(payload["recommendation_type"], recommendation_type)
            self.assertEqual(payload["candidate_card_oracle_id"], "oracle-rhystic-study")

    def test_consider_output_requires_medium_confidence(self) -> None:
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_candidate_packet(
                output_id="output:candidate:low",
                summary="Candidate is tracked for review.",
                confidence=0.2,
                expected_impact="low",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type="consider_include",
                role_tags=("card_advantage",),
                evidence_summary="Evidence is below the action threshold.",
                **output_context(),
            )

    def test_replacement_suggestion_requires_both_card_identities_and_shared_roles(self) -> None:
        packet = build_replacement_suggestion_packet(
            output_id="output:replacement:1",
            summary="Replacement candidate shares the same role.",
            confidence=0.62,
            expected_impact="medium",
            replace_card_oracle_id="oracle-current",
            replace_card_name="Current Card",
            candidate_card_oracle_id="oracle-rhystic-study",
            candidate_card_name="Rhystic Study",
            shared_role_tags=("card_advantage",),
            reason_summary="Both cards occupy a card advantage role.",
            impact_summary="The candidate has stronger measured evidence.",
            **output_context(),
        )
        payload = replacement_suggestion_packet_to_dict(packet)

        self.assertEqual(payload["replace_card_oracle_id"], "oracle-current")
        self.assertEqual(payload["candidate_card_oracle_id"], "oracle-rhystic-study")
        self.assertEqual(payload["shared_role_tags"], ["card_advantage"])

        with self.assertRaises(RecommendationOutputBuildError):
            build_replacement_suggestion_packet(
                output_id="output:replacement:missing",
                summary="Replacement candidate shares the same role.",
                confidence=0.62,
                expected_impact="medium",
                replace_card_name="Current Card",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                shared_role_tags=("card_advantage",),
                reason_summary="Both cards occupy a card advantage role.",
                impact_summary="The candidate has stronger measured evidence.",
                **output_context(),
            )

    def test_low_coverage_and_low_sample_require_visible_caveats(self) -> None:
        low_agreement = source_agreement(coverage_ratio=0.1, sample_size=2)
        low_evidence = evidence_object(
            source_agreement=low_agreement,
            caveats=(),
            evidence_level="low",
            coverage_ratio=0.1,
            sample_size=2,
            metric_refs=(
                EvidenceMetricRef(
                    metric_ref_id="metric:small-sample",
                    metric_type="inclusion_rate",
                    metric_name="Small sample inclusion rate",
                    metric_value=0.1,
                    metric_unit="ratio",
                    scope_type="commander",
                    scope_key="commander:fixture",
                    window_start="2026-06-01",
                    window_end="2026-07-01",
                    sample_size=2,
                    coverage_ratio=0.1,
                    generated_at=GENERATED_AT,
                    metadata={},
                ),
            ),
        )
        low_decision = decision_packet(
            confidence=0.1,
            source_agreement=low_agreement,
            evidence_objects=(low_evidence,),
            supporting_ref_ids=("metric:small-sample",),
            caveat_ids=(),
        )

        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_candidate_packet(
                output_id="output:candidate:low-coverage",
                summary="Candidate is tracked for review.",
                confidence=0.1,
                expected_impact="unknown",
                source_agreement=low_agreement,
                decision_packets=(low_decision,),
                evidence_objects=(low_evidence,),
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type="monitor",
                role_tags=("card_advantage",),
                evidence_summary="Evidence is below the action threshold.",
                caveat_ids=(),
                subject=subject(),
                weight_profile=weight_profile(),
                analysis_profile=analysis_profile(),
                generated_at=GENERATED_AT,
            )

    def test_high_confidence_requires_source_agreement_and_low_speculation(self) -> None:
        weak_context = output_context()
        weak_context["source_agreement"] = source_agreement(agreement_label="weak")
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_candidate_packet(
                output_id="output:candidate:weak",
                summary="Candidate is tracked for review.",
                confidence=0.9,
                expected_impact="high",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type="consider_include",
                role_tags=("card_advantage",),
                evidence_summary="Evidence supports consideration.",
                **weak_context,
            )
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_candidate_packet(
                output_id="output:candidate:speculation",
                summary="Candidate is tracked for review.",
                confidence=0.5,
                expected_impact="medium",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type="consider_include",
                role_tags=("card_advantage",),
                evidence_summary="Evidence supports consideration.",
                speculation_level="high",
                **output_context(),
            )

    def test_simulator_and_primer_context_remain_labeled_in_packet_metadata(self) -> None:
        packet = build_evidence_explanation_packet(
            output_id="output:explanation:1",
            summary="Explanation keeps simulator and primer context separate.",
            confidence=0.62,
            expected_impact="medium",
            explanation_label="Evidence explanation",
            supporting_summary="Measured metrics support review.",
            contradiction_summary="No contradiction selected.",
            caveat_summary="Simulator comparison is model-derived and not tournament evidence.",
            metadata={"simulator_evidence_only": True, "primer_context_explanatory_only": True},
            **output_context(),
        )
        payload = recommendation_output_bundle_to_dict(
            build_recommendation_output_bundle(
                bundle_id="bundle:explanation:1",
                bundle_type="deck_analysis",
                subject=subject(),
                evidence_explanations=(packet,),
                generated_at=GENERATED_AT,
            )
        )

        item = payload["evidence_explanations"][0]
        self.assertTrue(item["metadata"]["simulator_evidence_only"])
        self.assertTrue(item["metadata"]["primer_context_explanatory_only"])
        self.assertIn("simulator", item["caveat_summary"].lower())

    def test_package_gap_packet_serializes_without_candidate_generation(self) -> None:
        packet = build_package_gap_packet(
            output_id="output:package-gap:1",
            summary="A package role differs from the comparison pool.",
            confidence=0.62,
            expected_impact="medium",
            package_id="package:draw-engine",
            package_label="Draw Engine",
            missing_role_tags=("card_advantage",),
            related_card_names=("Rhystic Study",),
            metadata={"candidate_generation_performed": False},
            **output_context(),
        )
        payload = recommendation_output_bundle_to_dict(
            build_recommendation_output_bundle(
                bundle_id="bundle:package-gap:1",
                bundle_type="deck_analysis",
                subject=subject(),
                package_gaps=(packet,),
                generated_at=GENERATED_AT,
            )
        )

        self.assertFalse(payload["package_gaps"][0]["metadata"]["candidate_generation_performed"])

    def test_private_metadata_and_forbidden_strategic_language_are_rejected(self) -> None:
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_candidate_packet(
                output_id="output:candidate:private",
                summary="Candidate is tracked for review.",
                confidence=0.22,
                expected_impact="unknown",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type="monitor",
                role_tags=("card_advantage",),
                evidence_summary="Evidence is below the action threshold.",
                metadata={"raw_" + "provider_payload": {"secret": True}},
                **output_context(),
            )

        bad = "you " + "should " + "play this card"
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_candidate_packet(
                output_id="output:candidate:language",
                summary=bad,
                confidence=0.22,
                expected_impact="unknown",
                candidate_card_oracle_id="oracle-rhystic-study",
                candidate_card_name="Rhystic Study",
                recommendation_type="monitor",
                role_tags=("card_advantage",),
                evidence_summary="Evidence is below the action threshold.",
                **output_context(),
            )

    def test_bundle_rejects_duplicates_mismatched_subjects_and_option_overflow(self) -> None:
        packet = build_recommendation_candidate_packet(
            output_id="output:candidate:duplicate",
            summary="Candidate is tracked for review.",
            confidence=0.22,
            expected_impact="unknown",
            candidate_card_oracle_id="oracle-rhystic-study",
            candidate_card_name="Rhystic Study",
            recommendation_type="monitor",
            role_tags=("card_advantage",),
            evidence_summary="Evidence is below the action threshold.",
            **output_context(),
        )
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_output_bundle(
                bundle_id="bundle:duplicate",
                bundle_type="deck_analysis",
                subject=subject(),
                recommendation_candidates=(packet, packet),
                generated_at=GENERATED_AT,
            )
        with self.assertRaises(RecommendationOutputBuildError):
            RecommendationOutputOptions(maximum_outputs_per_bundle=0)
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_output_bundle(
                bundle_id="bundle:overflow",
                bundle_type="deck_analysis",
                subject=subject(),
                recommendation_candidates=(packet,),
                generated_at=GENERATED_AT,
                options=RecommendationOutputOptions(maximum_outputs_per_bundle=1),
                deck_health_packets=(
                    build_deck_health_packet(
                        output_id="output:health:overflow",
                        summary="Interaction density differs from comparison pool.",
                        confidence=0.72,
                        expected_impact="medium",
                        findings=(finding(),),
                        **output_context(),
                    ),
                ),
            )

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_server_or_llm_calls(self) -> None:
        import codie.recommendation_output.models as models_module

        source = Path(models_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "repositories",
            "codie." + "ingestion",
            "codie." + "canonical",
            "codie." + "analytics",
            "codie." + "cards",
            "codie." + "probability_engine",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "open" + "ai",
            "anth" + "ropic",
            "fl" + "ask",
            "fast" + "api",
            "uvi" + "corn",
            "star" + "lette",
            "SEL" + "ECT ",
            "INS" + "ERT ",
            "UPD" + "ATE ",
            "DEL" + "ETE ",
            "exec" + "ute(",
            "execute" + "script(",
            "open(",
            "write_text(",
            "write_bytes(",
            "Path(",
            "mkdir(",
            "touch(",
            "unlink(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
