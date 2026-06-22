from __future__ import annotations

import unittest

from codie.user_decks import (
    UserDeckAnalysisCard,
    UserDeckAnalysisInput,
    UserDeckEvidenceCandidate,
    UserDeckEvidenceComparisonRow,
    compare_user_deck_to_evidence,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def analysis_input() -> UserDeckAnalysisInput:
    return UserDeckAnalysisInput(
        user_deck_id=1,
        analysis_session_id=10,
        deck_name="Fixture",
        deck_hash="deck-hash",
        commander_hash="tymna the weaver",
        source_url=None,
        is_temporary=True,
        cards=(
            UserDeckAnalysisCard(
                raw_name="Tymna the Weaver",
                quantity=1,
                zone="commander",
                scryfall_id="tymna",
                oracle_id="oracle-tymna",
                resolution_status="exact",
            ),
            UserDeckAnalysisCard(
                raw_name="Jeweled Lotus",
                quantity=1,
                zone="mainboard",
                scryfall_id="lotus",
                oracle_id="oracle-lotus",
                resolution_status="exact",
            ),
        ),
        unresolved_cards=(),
        mainboard_count=1,
        commander_count=1,
        total_card_count=2,
    )


class UserDeckEvidenceComparisonTest(unittest.TestCase):
    def test_compare_user_deck_to_evidence_marks_present_and_absent_cards(self) -> None:
        comparison = compare_user_deck_to_evidence(
            analysis_input(),
            (
                UserDeckEvidenceCandidate(
                    oracle_id="oracle-remora",
                    card_name="Mystic Remora",
                    evidence_type="commander_staple",
                    score=0.8,
                    sample_size=42,
                    source_record_id="staple:remora",
                ),
                UserDeckEvidenceCandidate(
                    oracle_id="oracle-lotus",
                    card_name="Jeweled Lotus",
                    evidence_type="generic_staple",
                    score=0.9,
                    sample_size=100,
                    source_record_id="staple:lotus",
                ),
            ),
            generated_at=GENERATED_AT,
        )

        self.assertEqual(comparison.user_deck_id, 1)
        self.assertEqual(comparison.present_count, 1)
        self.assertEqual(comparison.absent_count, 1)
        present = next(row for row in comparison.rows if row.oracle_id == "oracle-lotus")
        absent = next(row for row in comparison.rows if row.oracle_id == "oracle-remora")
        self.assertEqual(present.presence_status, "present")
        self.assertEqual(present.quantity_in_deck, 1)
        self.assertEqual(present.zones, ("mainboard",))
        self.assertEqual(absent.presence_status, "absent")
        self.assertEqual(absent.quantity_in_deck, 0)
        self.assertIn("is absent in the imported user deck", absent.evidence_line)

    def test_candidate_validation_rejects_bad_score(self) -> None:
        with self.assertRaises(ValueError):
            UserDeckEvidenceCandidate(
                oracle_id="oracle-bad",
                card_name="Bad",
                evidence_type="fixture",
                score=1.5,
            )

    def test_comparison_text_rejects_strategic_claim_language(self) -> None:
        with self.assertRaises(ValueError):
            UserDeckEvidenceComparisonRow(
                oracle_id="oracle-card",
                card_name="Card",
                evidence_type="fixture",
                presence_status="absent",
                quantity_in_deck=0,
                zones=(),
                score=None,
                sample_size=None,
                source_record_id=None,
                source_url=None,
                evidence_line="You should play this card.",
            )

    def test_missing_generated_at_fails_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            compare_user_deck_to_evidence(analysis_input(), (), generated_at="")

    def test_user_deck_comparison_package_has_no_provider_or_db_imports(self) -> None:
        import codie.user_decks.evidence_comparison as comparison_module

        with open(comparison_module.__file__, encoding="utf-8") as handle:
            source = handle.read()
        forbidden = (
            "codie.providers",
            "codie.db",
            "codie.recommendations",
            "codie.analytics",
            "source_events",
            "source_decks",
            "provider_objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
