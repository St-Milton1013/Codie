from __future__ import annotations

import unittest
from pathlib import Path

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.user import UserRepository
from codie.user_decks import (
    SavedAnalysisReadError,
    UserDeckEvidenceComparison,
    UserDeckEvidenceComparisonRow,
    get_saved_user_deck_analysis,
    list_saved_user_deck_analyses,
    save_user_deck_comparison_analysis,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def comparison(user_deck_id: int) -> UserDeckEvidenceComparison:
    return UserDeckEvidenceComparison(
        user_deck_id=user_deck_id,
        deck_hash="deck-hash",
        commander_hash="tymna the weaver",
        rows=(
            UserDeckEvidenceComparisonRow(
                oracle_id="oracle-remora",
                card_name="Mystic Remora",
                evidence_type="commander_staple",
                presence_status="absent",
                quantity_in_deck=0,
                zones=(),
                score=0.8,
                sample_size=42,
                source_record_id="staple:remora",
                source_url=None,
                evidence_line="Mystic Remora is absent in the imported user deck; evidence type commander_staple; sample size 42.",
            ),
        ),
        present_count=0,
        absent_count=1,
        generated_at=GENERATED_AT,
    )


class UserDeckSavedAnalysisListingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.user = UserRepository(self.connection)
        self.user_deck_id = self.user.create_user_deck(
            {
                "deck_hash": "deck-hash",
                "created_at": GENERATED_AT,
                "updated_at": GENERATED_AT,
            }
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_list_saved_user_deck_analyses_returns_summaries(self) -> None:
        first = save_user_deck_comparison_analysis(
            self.user,
            comparison(self.user_deck_id),
            analysis_type="first",
        )
        second = save_user_deck_comparison_analysis(
            self.user,
            comparison(self.user_deck_id),
            analysis_type="second",
            report_path="reports/second.md",
        )

        rows = list_saved_user_deck_analyses(self.user, self.user_deck_id)

        self.assertEqual([row.saved_analysis_id for row in rows], [first.saved_analysis_id, second.saved_analysis_id])
        self.assertEqual(rows[0].analysis_type, "first")
        self.assertEqual(rows[1].report_path, "reports/second.md")

    def test_get_saved_user_deck_analysis_parses_detail_payload(self) -> None:
        saved = save_user_deck_comparison_analysis(self.user, comparison(self.user_deck_id))

        detail = get_saved_user_deck_analysis(self.user, saved.saved_analysis_id)

        self.assertEqual(detail.summary.saved_analysis_id, saved.saved_analysis_id)
        self.assertEqual(detail.summary_payload["absent_count"], 1)
        self.assertEqual(detail.summary_payload["rows"][0]["card_name"], "Mystic Remora")

    def test_missing_saved_analysis_fails_cleanly(self) -> None:
        with self.assertRaises(SavedAnalysisReadError):
            get_saved_user_deck_analysis(self.user, 404)

    def test_malformed_summary_json_fails_cleanly(self) -> None:
        saved_analysis_id = self.user.create_saved_analysis(
            {
                "user_deck_id": self.user_deck_id,
                "deck_hash": "deck-hash",
                "analysis_type": "malformed",
                "generated_at": GENERATED_AT,
                "summary_json": "{",
            }
        )

        with self.assertRaises(SavedAnalysisReadError):
            get_saved_user_deck_analysis(self.user, saved_analysis_id)

    def test_listing_helper_has_no_provider_or_recommendation_imports(self) -> None:
        import codie.user_decks.saved_analysis_listing as listing_module

        source = Path(listing_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie.providers",
            "codie.recommendations",
            "codie.analytics",
            "codie.ingestion",
            "source_events",
            "source_decks",
            "provider_objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
