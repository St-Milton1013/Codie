from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.user import UserRepository
from codie.pages import (
    PAGE_MODEL_VERSION,
    export_saved_analysis_detail_page_model,
    export_saved_analysis_list_page_model,
)
from codie.user_decks import (
    UserDeckEvidenceComparison,
    UserDeckEvidenceComparisonRow,
    save_user_deck_comparison_analysis,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"
EXPORTED_AT = "2026-06-28T00:00:00+00:00"


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
                source_url="https://example.test/evidence",
                evidence_line="Mystic Remora is absent in the imported user deck; evidence type commander_staple; sample size 42.",
            ),
        ),
        present_count=0,
        absent_count=1,
        generated_at=GENERATED_AT,
    )


class UserWorkflowPageModelExportTest(unittest.TestCase):
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
        self.saved = save_user_deck_comparison_analysis(
            self.user,
            comparison(self.user_deck_id),
            analysis_type="user_deck_evidence_comparison",
        )
        self.connection.commit()

    def tearDown(self) -> None:
        self.connection.close()

    def test_exports_saved_analysis_list_page_model_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "saved-analyses.json"

            result = export_saved_analysis_list_page_model(
                self.user,
                self.user_deck_id,
                path=output,
                output_root=root,
                exported_at=EXPORTED_AT,
            )

            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(result.content_type, "application/json")
            self.assertEqual(payload["page_model_version"], PAGE_MODEL_VERSION)
            self.assertEqual(payload["exported_at"], EXPORTED_AT)
            self.assertEqual(payload["source"]["export_type"], "saved_analysis_list")
            self.assertEqual(payload["source"]["user_deck_id"], self.user_deck_id)
            self.assertEqual(payload["title"], "Saved Analyses")
            self.assertEqual(payload["generated_at"], GENERATED_AT)
            self.assertEqual(payload["rows"][0]["saved_analysis_id"], self.saved.saved_analysis_id)

    def test_exports_saved_analysis_detail_page_model_json_with_evidence_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "saved-analysis-detail.json"

            export_saved_analysis_detail_page_model(
                self.user,
                self.saved.saved_analysis_id,
                path=output,
                output_root=root,
                exported_at=EXPORTED_AT,
            )

            payload = json.loads(output.read_text(encoding="utf-8"))
            row = payload["rows"][0]
            self.assertEqual(payload["source"]["export_type"], "saved_analysis_detail")
            self.assertEqual(payload["source"]["saved_analysis_id"], self.saved.saved_analysis_id)
            self.assertEqual(payload["source"]["deck_hash"], "deck-hash")
            self.assertEqual(payload["source"]["analysis_type"], "user_deck_evidence_comparison")
            self.assertEqual(row["card_name"], "Mystic Remora")
            self.assertEqual(row["sample_size"], 42)
            self.assertEqual(row["source_record_id"], "staple:remora")
            self.assertEqual(row["source_url"], "https://example.test/evidence")

    def test_empty_saved_analysis_list_exports_explicit_empty_state(self) -> None:
        empty_deck_id = self.user.create_user_deck(
            {
                "deck_hash": "empty-deck-hash",
                "created_at": GENERATED_AT,
                "updated_at": GENERATED_AT,
            }
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "empty.json"

            export_saved_analysis_list_page_model(
                self.user,
                empty_deck_id,
                path=output,
                output_root=root,
                exported_at=EXPORTED_AT,
            )

            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], [])
            self.assertEqual(payload["empty_state"], "No saved analyses exist for this user deck.")

    def test_output_root_containment_rejects_outside_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / "outside.json"

            with self.assertRaises(ValueError):
                export_saved_analysis_list_page_model(
                    self.user,
                    self.user_deck_id,
                    path=outside,
                    output_root=root,
                    exported_at=EXPORTED_AT,
                )

    def test_export_module_has_no_provider_recommendation_or_analytics_imports(self) -> None:
        import codie.pages.export_user_workflow as export_module

        source = Path(export_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie.providers",
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
