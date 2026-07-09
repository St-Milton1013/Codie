from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.recommendation_output import (
    RecommendationOutputBuildError,
    RecommendationReportOptions,
    build_deck_health_packet,
    build_evidence_explanation_packet,
    build_recommendation_candidate_packet,
    build_recommendation_output_bundle,
    build_recommendation_report_document,
    recommendation_report_document_to_dict,
    recommendation_report_document_to_markdown,
)
from tests.test_recommendation_output_boundary import (
    GENERATED_AT,
    evidence_object,
    finding,
    output_context,
    subject,
)


def report_bundle(**overrides):
    context = output_context()
    health = build_deck_health_packet(
        output_id="output:health:1",
        summary="Interaction density differs from comparison pool.",
        confidence=0.72,
        expected_impact="medium",
        findings=(finding(),),
        contradicting_ref_ids=("conflict:fixture",),
        **context,
    )
    candidate = build_recommendation_candidate_packet(
        output_id="output:candidate:monitor",
        summary="Candidate is tracked for review.",
        confidence=0.22,
        expected_impact="unknown",
        candidate_card_oracle_id="oracle-rhystic-study",
        candidate_card_name="Rhystic Study",
        recommendation_type="monitor",
        role_tags=("card_advantage",),
        evidence_summary="Evidence is below the action threshold.",
        **context,
    )
    explanation = build_evidence_explanation_packet(
        output_id="output:explanation:1",
        summary="Explanation keeps simulator and primer context separate.",
        confidence=0.62,
        expected_impact="medium",
        explanation_label="Evidence explanation",
        supporting_summary="Measured metrics support review.",
        contradiction_summary="No contradiction selected.",
        caveat_summary="Simulator comparison is model-derived and not tournament evidence.",
        metadata={"simulator_evidence_only": True, "primer_context_explanatory_only": True},
        **context,
    )
    data = {
        "bundle_id": "bundle:recommendation-output:1",
        "bundle_type": "deck_analysis",
        "subject": subject(),
        "deck_health_packets": (health,),
        "recommendation_candidates": (candidate,),
        "evidence_explanations": (explanation,),
        "generated_at": GENERATED_AT,
    }
    data.update(overrides)
    return build_recommendation_output_bundle(**data)


class RecommendationOutputReportingTest(unittest.TestCase):
    def test_report_document_serializes_required_visibility_fields(self) -> None:
        document = build_recommendation_report_document(
            report_bundle(),
            report_id="report:1",
            generated_at=GENERATED_AT,
        )
        payload = recommendation_report_document_to_dict(document)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["source_bundle_id"], "bundle:recommendation-output:1")
        self.assertEqual(payload["output_version"], "phase28b-output-packets")
        health = [item for item in payload["sections"] if item["section_type"] == "deck_health"][0]
        self.assertEqual(health["confidence"], 0.72)
        self.assertEqual(health["expected_impact"], "medium")
        self.assertEqual(health["source_agreement"]["agreement_label"], "strong")
        self.assertEqual(health["caveats"], ["caveat:coverage"])
        self.assertEqual(health["contradictions"], ["conflict:fixture"])
        self.assertEqual(health["speculation_level"], "none")
        self.assertEqual(health["decision_ids"], ["decision:fixture:signal"])
        self.assertEqual(health["evidence_object_ids"], ["evidence:fixture"])
        self.assertEqual(health["weight_profile_refs"], ["competitive-default@1.0.0"])
        self.assertEqual(health["analysis_profile_refs"], ["analysis-profile:competitive-default@1.0.0"])

    def test_markdown_includes_evidence_and_non_action_labels(self) -> None:
        document = build_recommendation_report_document(
            report_bundle(),
            report_id="report:markdown",
            generated_at=GENERATED_AT,
        )
        markdown = recommendation_report_document_to_markdown(document)

        self.assertIn("Confidence", markdown)
        self.assertIn("Expected impact", markdown)
        self.assertIn("Source agreement", markdown)
        self.assertIn("Caveats", markdown)
        self.assertIn("Contradictions", markdown)
        self.assertIn("Speculation level", markdown)
        self.assertIn("competitive-default@1.0.0", markdown)
        self.assertIn("analysis-profile:competitive-default@1.0.0", markdown)
        self.assertIn("decision:fixture:signal", markdown)
        self.assertIn("evidence:fixture", markdown)
        self.assertIn("| Non-action output | review only. |", markdown)
        self.assertIn("Simulator comparison is model-derived and not tournament evidence.", markdown)
        self.assertIn("Primer context is explanatory only.", markdown)

    def test_report_can_be_built_from_validated_bundle_dict(self) -> None:
        bundle_dict = json.loads(json.dumps(recommendation_report_document_to_dict(
            build_recommendation_report_document(report_bundle(), report_id="report:source", generated_at=GENERATED_AT)
        )))
        source_bundle = report_bundle()
        from codie.recommendation_output import recommendation_output_bundle_to_dict

        document = build_recommendation_report_document(
            recommendation_output_bundle_to_dict(source_bundle),
            report_id="report:dict",
            generated_at=GENERATED_AT,
        )
        payload = recommendation_report_document_to_dict(document)

        self.assertEqual(bundle_dict["subject"]["subject_id"], payload["subject"]["subject_id"])

    def test_malformed_bundle_input_fails_cleanly(self) -> None:
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_report_document(
                {"bundle_id": "missing-fields"},
                report_id="report:bad",
                generated_at=GENERATED_AT,
            )

    def test_private_metadata_and_forbidden_language_are_rejected(self) -> None:
        from codie.recommendation_output import recommendation_output_bundle_to_dict

        payload = recommendation_output_bundle_to_dict(report_bundle())
        payload["metadata"] = {"safe": [{"private-deck-text": "hidden"}]}
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_report_document(payload, report_id="report:private", generated_at=GENERATED_AT)

        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_report_document(
                report_bundle(),
                report_id="report:bad-language",
                generated_at=GENERATED_AT,
                metadata={"summary": "you " + "should " + "play this"},
            )

    def test_markdown_table_pipes_are_escaped(self) -> None:
        context = output_context()
        candidate = build_recommendation_candidate_packet(
            output_id="output:candidate:pipe",
            summary="Candidate is tracked for review with pipe | character.",
            confidence=0.22,
            expected_impact="unknown",
            candidate_card_oracle_id="oracle-rhystic-study",
            candidate_card_name="Rhystic | Study",
            recommendation_type="monitor",
            role_tags=("card_advantage",),
            evidence_summary="Evidence is below the action threshold.",
            **context,
        )
        bundle = build_recommendation_output_bundle(
            bundle_id="bundle:pipes",
            bundle_type="deck_analysis",
            subject=subject(),
            recommendation_candidates=(candidate,),
            generated_at=GENERATED_AT,
        )
        markdown = recommendation_report_document_to_markdown(
            build_recommendation_report_document(bundle, report_id="report:pipes", generated_at=GENERATED_AT)
        )

        self.assertIn("pipe \\| character", markdown)

    def test_options_can_omit_provenance_section(self) -> None:
        document = build_recommendation_report_document(
            report_bundle(),
            report_id="report:no-provenance",
            generated_at=GENERATED_AT,
            options=RecommendationReportOptions(include_provenance_section=False),
        )
        payload = recommendation_report_document_to_dict(document)

        self.assertNotIn("provenance", {item["section_type"] for item in payload["sections"]})

    def test_report_rejects_empty_output_bundle_payload(self) -> None:
        empty = build_recommendation_output_bundle(
            bundle_id="bundle:empty-source",
            bundle_type="deck_analysis",
            subject=subject(),
            deck_health_packets=(
                build_deck_health_packet(
                    output_id="output:health:temporary",
                    summary="Interaction density differs from comparison pool.",
                    confidence=0.72,
                    expected_impact="medium",
                    findings=(finding(),),
                    **output_context(evidence_objects=(evidence_object(),)),
                ),
            ),
            generated_at=GENERATED_AT,
        )
        from codie.recommendation_output import recommendation_output_bundle_to_dict

        payload = recommendation_output_bundle_to_dict(empty)
        payload["deck_health_packets"] = []
        with self.assertRaises(RecommendationOutputBuildError):
            build_recommendation_report_document(payload, report_id="report:empty", generated_at=GENERATED_AT)

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_server_or_llm_calls(self) -> None:
        import codie.recommendation_output.reporting as reporting_module

        source = Path(reporting_module.__file__).read_text(encoding="utf-8")
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
