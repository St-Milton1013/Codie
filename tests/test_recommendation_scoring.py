from __future__ import annotations

import unittest

from codie.db.bootstrap import bootstrap_database
from codie.recommendations import (
    EvidenceItem,
    RecommendationScoreInput,
    build_evidence_bundle,
    build_recommendation_candidate_draft,
    low_sample_penalty,
    normalize_candidate_type,
    score_recommendation_candidate,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def evidence_bundle(entity_id: str = "oracle-remora"):
    item = EvidenceItem(
        claim_type="inclusion",
        claim_text="Card appears in 73% of comparable canonical decks.",
        source_type="analytics",
        source_name="canonical tournament analytics",
        source_record_id="metric:oracle-remora:180d",
        metric_value=0.73,
        metric_unit="inclusion",
        sample_size=41,
        confidence=0.68,
        recency_window="180d",
        generated_at=GENERATED_AT,
        reproducibility_notes="Computed from canonical deck/card observations.",
        formula="included decks / total comparable decks",
    )
    return build_evidence_bundle(
        entity_type="card",
        entity_id=entity_id,
        items=(item,),
        generated_at=GENERATED_AT,
    )


class RecommendationScoringTest(unittest.TestCase):
    def test_score_formula_uses_constitution_components(self) -> None:
        score_input = RecommendationScoreInput(
            entity_type="card",
            entity_id="oracle-remora",
            candidate_type="commander-specific",
            sample_size=41,
            commander_lift_score=1.4,
            inclusion_rate_score=0.73,
            confidence_score=0.68,
            similarity_score=0.31,
            package_completion_score=0.0,
            combo_completion_score=0.2,
            tournament_performance_score=0.15,
            simulation_delta_score=0.04,
            generic_staple_penalty=0.10,
            low_sample_penalty=0.0,
        )

        score = score_recommendation_candidate(score_input)

        self.assertEqual(score_input.candidate_type, "commander_specific")
        self.assertAlmostEqual(score.positive_total, 3.51)
        self.assertAlmostEqual(score.penalty_total, 0.10)
        self.assertAlmostEqual(score.recommendation_score, 3.41)
        self.assertEqual(score.confidence_label, "medium")
        self.assertEqual(
            [component.name for component in score.components],
            [
                "commander_lift_score",
                "inclusion_rate_score",
                "confidence_score",
                "similarity_score",
                "package_completion_score",
                "combo_completion_score",
                "tournament_performance_score",
                "simulation_delta_score",
                "generic_staple_penalty",
                "low_sample_penalty",
            ],
        )

    def test_confidence_score_defaults_from_sample_size(self) -> None:
        score = score_recommendation_candidate(
            RecommendationScoreInput(
                entity_type="card",
                entity_id="oracle-remora",
                candidate_type="meta_tech",
                sample_size=50,
                inclusion_rate_score=0.25,
            )
        )
        self.assertEqual(score.confidence_label, "medium")
        self.assertEqual(score.recommendation_score, 0.25 + 0.5)

    def test_low_sample_penalty_and_candidate_type_validation(self) -> None:
        self.assertEqual(low_sample_penalty(9), 0.25)
        self.assertEqual(low_sample_penalty(10), 0.0)
        self.assertEqual(normalize_candidate_type("combo-completion"), "combo_completion")
        with self.assertRaises(ValueError):
            normalize_candidate_type("oracle says so")
        with self.assertRaises(ValueError):
            low_sample_penalty(3, threshold=0)

    def test_candidate_draft_requires_matching_evidence_identity(self) -> None:
        score_input = RecommendationScoreInput(
            entity_type="card",
            entity_id="oracle-remora",
            candidate_type="commander_specific",
            sample_size=41,
            inclusion_rate_score=0.73,
        )
        draft = build_recommendation_candidate_draft(
            score_input=score_input,
            evidence=evidence_bundle(),
            generated_at=GENERATED_AT,
        )
        self.assertEqual(draft.entity_id, "oracle-remora")
        self.assertEqual(draft.score.recommendation_score, 0.73 + (41 / 100))

        with self.assertRaises(ValueError):
            build_recommendation_candidate_draft(
                score_input=score_input,
                evidence=evidence_bundle("oracle-other"),
                generated_at=GENERATED_AT,
            )

    def test_invalid_score_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            RecommendationScoreInput(
                entity_type="card",
                entity_id="oracle-remora",
                candidate_type="commander_specific",
                sample_size=1,
                inclusion_rate_score=1.5,
            )
        with self.assertRaises(ValueError):
            RecommendationScoreInput(
                entity_type="card",
                entity_id="oracle-remora",
                candidate_type="commander_specific",
                sample_size=1,
                commander_lift_score=-0.1,
            )
        with self.assertRaises(TypeError):
            RecommendationScoreInput(
                entity_type="card",
                entity_id="oracle-remora",
                candidate_type="commander_specific",
                sample_size=1.2,
            )

    def test_phase8e_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()
        build_recommendation_candidate_draft(
            score_input=RecommendationScoreInput(
                entity_type="card",
                entity_id="oracle-remora",
                candidate_type="commander_specific",
                sample_size=41,
                inclusion_rate_score=0.73,
            ),
            evidence=evidence_bundle(),
            generated_at=GENERATED_AT,
        )
        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
