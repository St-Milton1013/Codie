from __future__ import annotations

import unittest

from codie.db.bootstrap import bootstrap_database
from codie.recommendations import (
    EvidenceItem,
    RecommendationScoreInput,
    build_candidate_audit_report,
    build_evidence_bundle,
    build_recommendation_candidate_draft,
    candidate_explanation_lines,
    validate_candidate_explanation_lines,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def evidence_item(sample_size: int = 41, confidence: float = 0.68) -> EvidenceItem:
    return EvidenceItem(
        claim_type="inclusion",
        claim_text="Card appears in 73% of comparable canonical decks.",
        source_type="analytics",
        source_name="canonical tournament analytics",
        source_record_id="metric:oracle-remora:180d",
        metric_value=0.73,
        metric_unit="inclusion",
        sample_size=sample_size,
        confidence=confidence,
        recency_window="180d",
        generated_at=GENERATED_AT,
        reproducibility_notes="Computed from canonical deck/card observations.",
        formula="included decks / total comparable decks",
    )


def candidate(sample_size: int = 41):
    bundle = build_evidence_bundle(
        entity_type="card",
        entity_id="oracle-remora",
        items=(evidence_item(sample_size=sample_size),),
        generated_at=GENERATED_AT,
    )
    return build_recommendation_candidate_draft(
        score_input=RecommendationScoreInput(
            entity_type="card",
            entity_id="oracle-remora",
            candidate_type="commander_specific",
            sample_size=sample_size,
            commander_lift_score=1.2,
            inclusion_rate_score=0.73,
            confidence_score=0.68 if sample_size >= 10 else 0.04,
            similarity_score=0.2,
            generic_staple_penalty=0.1,
            low_sample_penalty=0.25 if sample_size < 10 else 0.0,
        ),
        evidence=bundle,
        generated_at=GENERATED_AT,
    )


class RecommendationCandidateAuditTest(unittest.TestCase):
    def test_audit_report_explains_candidate_with_source_attribution(self) -> None:
        draft = candidate()
        report = build_candidate_audit_report(draft, generated_at=GENERATED_AT)

        self.assertTrue(report.is_valid)
        self.assertTrue(report.rank_eligible)
        self.assertEqual(report.entity_id, "oracle-remora")
        self.assertEqual(report.evidence_count, 1)
        self.assertEqual(report.source_type_counts, {"analytics": 1})
        self.assertEqual(report.issues, ())
        self.assertIn("commander_lift_score", report.formula)
        self.assertTrue(any("Score" in line and "formula" in line for line in report.explanation_lines))
        self.assertTrue(any("Source: canonical tournament analytics" in line for line in report.explanation_lines))
        self.assertTrue(any("Metric: 0.73 inclusion" in line for line in report.explanation_lines))

    def test_low_sample_size_warns_and_blocks_rank_eligibility(self) -> None:
        report = build_candidate_audit_report(candidate(sample_size=4), generated_at=GENERATED_AT)

        self.assertTrue(report.is_valid)
        self.assertFalse(report.rank_eligible)
        self.assertEqual(len(report.issues), 1)
        self.assertEqual(report.issues[0].severity, "warning")
        self.assertEqual(report.issues[0].code, "low_sample_size")

    def test_candidate_explanation_lines_reject_unsupported_language(self) -> None:
        lines = candidate_explanation_lines(candidate())
        self.assertGreaterEqual(len(lines), 2)
        with self.assertRaises(ValueError):
            validate_candidate_explanation_lines(("This deck should play this card.",))

    def test_audit_report_validates_threshold_inputs(self) -> None:
        with self.assertRaises(ValueError):
            build_candidate_audit_report(candidate(), generated_at="")
        with self.assertRaises(ValueError):
            build_candidate_audit_report(candidate(), generated_at=GENERATED_AT, minimum_ranked_sample_size=0)
        with self.assertRaises(TypeError):
            build_candidate_audit_report(candidate(), generated_at=GENERATED_AT, minimum_ranked_sample_size=1.5)

    def test_phase8f_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()
        build_candidate_audit_report(candidate(), generated_at=GENERATED_AT)
        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
