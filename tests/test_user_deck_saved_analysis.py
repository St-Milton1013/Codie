from __future__ import annotations

import json
import sqlite3
import unittest
from pathlib import Path

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.user import UserRepository
from codie.user_decks import (
    UserDeckEvidenceComparison,
    UserDeckEvidenceComparisonRow,
    save_user_deck_comparison_analysis,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def comparison(user_deck_id: int = 1) -> UserDeckEvidenceComparison:
    return UserDeckEvidenceComparison(
        user_deck_id=user_deck_id,
        deck_hash="deck-hash",
        commander_hash="tymna the weaver",
        generated_at=GENERATED_AT,
        present_count=1,
        absent_count=1,
        rows=(
            UserDeckEvidenceComparisonRow(
                oracle_id="oracle-lotus",
                card_name="Jeweled Lotus",
                evidence_type="generic_staple",
                presence_status="present",
                quantity_in_deck=1,
                zones=("mainboard",),
                score=0.9,
                sample_size=100,
                source_record_id="staple:lotus",
                source_url=None,
                evidence_line="Jeweled Lotus is present in the imported user deck; evidence type generic_staple; sample size 100.",
            ),
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
    )


class UserDeckSavedAnalysisTest(unittest.TestCase):
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

    def test_save_user_deck_comparison_analysis_persists_summary(self) -> None:
        result = save_user_deck_comparison_analysis(
            self.user,
            comparison(self.user_deck_id),
            report_path="reports/comparison.md",
        )

        row = self.user.get_saved_analysis(result.saved_analysis_id)
        summary = json.loads(row["summary_json"])
        self.assertEqual(row["user_deck_id"], self.user_deck_id)
        self.assertEqual(row["deck_hash"], "deck-hash")
        self.assertEqual(row["analysis_type"], "user_deck_evidence_comparison")
        self.assertEqual(row["report_path"], "reports/comparison.md")
        self.assertEqual(summary["present_count"], 1)
        self.assertEqual(summary["absent_count"], 1)
        self.assertEqual(summary["rows"][1]["card_name"], "Mystic Remora")
        self.assertIn("is absent in the imported user deck", summary["rows"][1]["evidence_line"])

    def test_list_saved_analysis_for_deck_orders_by_generated_at(self) -> None:
        save_user_deck_comparison_analysis(
            self.user,
            comparison(self.user_deck_id),
            analysis_type="first",
        )
        save_user_deck_comparison_analysis(
            self.user,
            comparison(self.user_deck_id),
            analysis_type="second",
        )

        rows = self.user.list_saved_analysis_for_deck(self.user_deck_id)

        self.assertEqual([row["analysis_type"] for row in rows], ["first", "second"])

    def test_saved_analysis_rejects_invalid_user_deck_fk(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            save_user_deck_comparison_analysis(self.user, comparison(999))

    def test_saved_analysis_rejects_missing_analysis_type(self) -> None:
        with self.assertRaises(ValueError):
            save_user_deck_comparison_analysis(
                self.user,
                comparison(self.user_deck_id),
                analysis_type="",
            )

    def test_saved_analysis_helper_has_no_provider_or_recommendation_imports(self) -> None:
        import codie.user_decks.saved_analysis as saved_analysis_module

        source = Path(saved_analysis_module.__file__).read_text(encoding="utf-8")
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
