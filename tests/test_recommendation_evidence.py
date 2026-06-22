from __future__ import annotations

import unittest

from codie.db.bootstrap import bootstrap_database
from codie.recommendations import (
    EvidenceBundle,
    EvidenceItem,
    build_evidence_bundle,
    evidence_stack_summary,
    validate_claim_text,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def evidence_item(**overrides) -> EvidenceItem:
    data = {
        "claim_type": "inclusion",
        "claim_text": "Comparable canonical decks most frequently include Mystic Remora.",
        "source_type": "tournament",
        "source_name": "canonical card performance metrics",
        "source_record_id": "card_performance_metrics:oracle-mystic-remora:90d",
        "metric_value": 0.73,
        "metric_unit": "inclusion_rate",
        "sample_size": 421,
        "confidence": 0.91,
        "recency_window": "90d",
        "generated_at": GENERATED_AT,
        "reproducibility_notes": "Calculated from canonical tournament deck entries for the selected window.",
        "formula": "included_decks / total_decks",
    }
    data.update(overrides)
    return EvidenceItem(**data)


class RecommendationEvidenceTest(unittest.TestCase):
    def test_evidence_item_preserves_required_provenance_fields(self) -> None:
        item = evidence_item()
        self.assertEqual(item.claim_type, "inclusion")
        self.assertEqual(item.source_type, "tournament")
        self.assertEqual(item.source_record_id, "card_performance_metrics:oracle-mystic-remora:90d")
        self.assertEqual(item.metric_value, 0.73)
        self.assertEqual(item.metric_unit, "inclusion_rate")
        self.assertEqual(item.sample_size, 421)
        self.assertEqual(item.confidence, 0.91)
        self.assertEqual(item.recency_window, "90d")
        self.assertEqual(item.generated_at, GENERATED_AT)
        self.assertEqual(item.formula, "included_decks / total_decks")

    def test_evidence_item_requires_source_attribution(self) -> None:
        with self.assertRaises(ValueError):
            evidence_item(source_url=None, source_record_id=None)

    def test_evidence_item_rejects_unsupported_strategic_claim_text(self) -> None:
        forbidden = (
            "This deck is trying to win with Mystic Remora.",
            "The game plan is to draw cards.",
            "This deck should play Mystic Remora.",
            "You should play Mystic Remora.",
            "Mystic Remora is strictly better here.",
            "Cut this card for Mystic Remora.",
            "Always include Mystic Remora.",
        )
        for claim_text in forbidden:
            with self.subTest(claim_text=claim_text):
                with self.assertRaises(ValueError):
                    evidence_item(claim_text=claim_text)

    def test_allowed_evidence_language_passes_validation(self) -> None:
        self.assertEqual(
            validate_claim_text("Evidence Stack shows 421 decks and 17 primers."),
            "Evidence Stack shows 421 decks and 17 primers.",
        )
        self.assertEqual(
            evidence_item(claim_text="Known primers found for this commander pair.").claim_text,
            "Known primers found for this commander pair.",
        )

    def test_evidence_item_validates_source_type_sample_size_and_confidence(self) -> None:
        with self.assertRaises(ValueError):
            evidence_item(source_type="unsupported")
        with self.assertRaises(ValueError):
            evidence_item(sample_size=-1)
        with self.assertRaises(ValueError):
            evidence_item(confidence=1.1)

    def test_bundle_requires_items_and_sorts_deterministically(self) -> None:
        tournament = evidence_item(source_type="tournament", claim_type="inclusion")
        primer = evidence_item(
            source_type="primer",
            claim_type="primer_route",
            source_name="primer metadata",
            source_url="https://example.test/primer",
            source_record_id=None,
            metric_value=1,
            metric_unit="route_present",
            sample_size=1,
            confidence=1.0,
        )
        bundle = build_evidence_bundle(
            entity_type="card",
            entity_id="oracle-mystic-remora",
            items=(tournament, primer),
            generated_at=GENERATED_AT,
        )
        self.assertIsInstance(bundle, EvidenceBundle)
        self.assertEqual(bundle.entity_type, "card")
        self.assertEqual(bundle.entity_id, "oracle-mystic-remora")
        self.assertEqual([item.source_type for item in bundle.items], ["primer", "tournament"])
        with self.assertRaises(ValueError):
            build_evidence_bundle(entity_type="card", entity_id="oracle-x", items=(), generated_at=GENERATED_AT)

    def test_evidence_stack_summary_counts_volume_without_ai_scoring(self) -> None:
        bundle = build_evidence_bundle(
            entity_type="card",
            entity_id="oracle-mystic-remora",
            items=(
                evidence_item(source_type="tournament"),
                evidence_item(source_type="tournament", claim_type="topcut"),
                evidence_item(source_type="primer", claim_type="primer_route", metric_unit="route_present"),
            ),
            generated_at=GENERATED_AT,
        )
        summary = evidence_stack_summary(bundle, cap_per_type=2)
        self.assertEqual(summary.total_evidence_count, 3)
        self.assertEqual(summary.source_type_counts, {"primer": 1, "tournament": 2})
        self.assertAlmostEqual(summary.volume_score, 3 / 18)
        self.assertIn("evidence volume only", summary.reproducibility_notes)
        with self.assertRaises(ValueError):
            evidence_stack_summary(bundle, cap_per_type=0)

    def test_phase8b_does_not_create_recommendation_rows(self) -> None:
        connection = bootstrap_database()
        bundle = build_evidence_bundle(
            entity_type="card",
            entity_id="oracle-mystic-remora",
            items=(evidence_item(),),
            generated_at=GENERATED_AT,
        )
        evidence_stack_summary(bundle)
        run_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
