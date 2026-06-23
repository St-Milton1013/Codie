from __future__ import annotations

import unittest
from pathlib import Path

from codie.pages import (
    UserWorkflowTableRow,
    saved_analysis_detail_page_model,
    saved_analysis_list_page_model,
)
from codie.user_decks import SavedAnalysisDetail, SavedAnalysisSummary


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def summary(saved_analysis_id: int = 1) -> SavedAnalysisSummary:
    return SavedAnalysisSummary(
        saved_analysis_id=saved_analysis_id,
        user_deck_id=7,
        deck_hash="deck-hash",
        analysis_type="user_deck_evidence_comparison",
        generated_at=GENERATED_AT,
        report_path="reports/comparison.md",
    )


def detail() -> SavedAnalysisDetail:
    return SavedAnalysisDetail(
        summary=summary(),
        summary_payload={
            "present_count": 1,
            "absent_count": 1,
            "rows": [
                {
                    "card_name": "Mystic Remora",
                    "evidence_type": "commander_staple",
                    "presence_status": "absent",
                    "quantity_in_deck": 0,
                    "zones": [],
                    "sample_size": 42,
                    "source_record_id": "staple:remora",
                    "source_url": "https://example.test/evidence",
                    "evidence_line": "Mystic Remora is absent in the imported user deck; evidence type commander_staple; sample size 42.",
                }
            ],
        },
    )


class UserWorkflowPageModelTest(unittest.TestCase):
    def test_saved_analysis_list_page_model_has_rows_and_summary_cards(self) -> None:
        model = saved_analysis_list_page_model((summary(1), summary(2)), user_deck_id=7)
        payload = model.to_dict()

        self.assertEqual(payload["title"], "Saved Analyses")
        self.assertEqual(payload["generated_at"], GENERATED_AT)
        self.assertEqual(payload["summary_cards"][0]["value"], "7")
        self.assertEqual(payload["summary_cards"][1]["value"], "2")
        self.assertEqual(payload["rows"][0]["saved_analysis_id"], 1)
        self.assertIsNone(payload["empty_state"])

    def test_saved_analysis_list_page_model_has_explicit_empty_state(self) -> None:
        model = saved_analysis_list_page_model((), user_deck_id=7)
        payload = model.to_dict()

        self.assertEqual(payload["rows"], [])
        self.assertEqual(payload["empty_state"], "No saved analyses exist for this user deck.")

    def test_saved_analysis_detail_page_model_preserves_evidence_metadata(self) -> None:
        model = saved_analysis_detail_page_model(detail())
        payload = model.to_dict()
        row = payload["rows"][0]

        self.assertEqual(payload["title"], "Saved Analysis Detail")
        self.assertEqual(payload["generated_at"], GENERATED_AT)
        self.assertEqual(payload["summary_cards"][2]["value"], "1")
        self.assertEqual(row["card_name"], "Mystic Remora")
        self.assertEqual(row["source_record_id"], "staple:remora")
        self.assertEqual(row["source_url"], "https://example.test/evidence")
        self.assertIn("is absent in the imported user deck", row["evidence_line"])

    def test_forbidden_strategic_language_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            UserWorkflowTableRow({"evidence_line": "You should play this card."})

    def test_pages_layer_has_no_forbidden_imports(self) -> None:
        import codie.pages.user_workflow as user_workflow_module

        source = Path(user_workflow_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie.providers",
            "codie.db",
            "codie.recommendations",
            "codie.analytics",
            "source_events",
            "source_decks",
            "provider_objects",
            "sqlite3",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
