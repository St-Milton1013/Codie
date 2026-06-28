from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from codie.cli.user_deck import main
from codie.db.connection import connect
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.user import UserRepository
from codie.user_decks import UserDeckEvidenceComparison, UserDeckEvidenceComparisonRow, save_user_deck_comparison_analysis


NOW = "2026-06-22T00:00:00+00:00"


class UserDeckCliTest(unittest.TestCase):
    def test_init_db_bootstraps_sqlite_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "codie.sqlite"

            exit_code = main(["init-db", "--db", str(db_path)])

            self.assertEqual(exit_code, 0)
            connection = connect(db_path)
            try:
                row = connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
                    ("user_decks",),
                ).fetchone()
                self.assertIsNotNone(row)
            finally:
                connection.close()

    def test_import_user_deck_writes_comparison_exports(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            deck_path = root / "deck.txt"
            evidence_path = root / "evidence.json"
            json_out = root / "comparison.json"
            markdown_out = root / "comparison.md"
            main(["init-db", "--db", str(db_path)])
            self._seed_cards(db_path)
            deck_path.write_text(
                "Commander\n1 Tymna the Weaver\n\nMainboard\n1 Jeweled Lotus\n",
                encoding="utf-8",
            )
            evidence_path.write_text(
                json.dumps(
                    {
                        "candidates": [
                            {
                                "oracle_id": "oracle-lotus",
                                "card_name": "Jeweled Lotus",
                                "evidence_type": "generic_staple",
                                "score": 0.9,
                                "sample_size": 100,
                                "source_record_id": "staple:lotus",
                            },
                            {
                                "oracle_id": "oracle-remora",
                                "card_name": "Mystic Remora",
                                "evidence_type": "commander_staple",
                                "score": 0.8,
                                "sample_size": 42,
                                "source_record_id": "staple:remora",
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "import-user-deck",
                        "--db",
                        str(db_path),
                        "--deck-file",
                        str(deck_path),
                        "--deck-name",
                        "CLI Fixture",
                        "--evidence-json",
                        str(evidence_path),
                        "--json-out",
                        str(json_out),
                        "--markdown-out",
                        str(markdown_out),
                        "--output-root",
                        str(root),
                        "--generated-at",
                        NOW,
                    ]
                )

            self.assertEqual(exit_code, 0)
            summary = json.loads(stdout.getvalue())
            self.assertEqual(summary["card_count"], 2)
            self.assertEqual(summary["present_count"], 1)
            self.assertEqual(summary["absent_count"], 1)
            payload = json.loads(json_out.read_text(encoding="utf-8"))
            markdown = markdown_out.read_text(encoding="utf-8")
            self.assertEqual(payload["present_count"], 1)
            self.assertIn("Mystic Remora is absent in the imported user deck", markdown)

    def test_import_user_deck_without_export_paths_prints_inline_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            deck_path = root / "deck.txt"
            main(["init-db", "--db", str(db_path)])
            self._seed_cards(db_path)
            deck_path.write_text("1 Jeweled Lotus\n", encoding="utf-8")

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "import-user-deck",
                        "--db",
                        str(db_path),
                        "--deck-file",
                        str(deck_path),
                        "--generated-at",
                        NOW,
                    ]
                )

            self.assertEqual(exit_code, 0)
            summary = json.loads(stdout.getvalue())
            self.assertEqual(summary["present_count"], 0)
            self.assertEqual(summary["absent_count"], 0)
            self.assertEqual(summary["comparison"]["rows"], [])
            self.assertIn("# User Deck Evidence Comparison", summary["comparison_markdown"])

    def test_import_user_deck_requires_both_output_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            deck_path = root / "deck.txt"
            main(["init-db", "--db", str(db_path)])
            self._seed_cards(db_path)
            deck_path.write_text("1 Jeweled Lotus\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                main(
                    [
                        "import-user-deck",
                        "--db",
                        str(db_path),
                        "--deck-file",
                        str(deck_path),
                        "--json-out",
                        str(root / "comparison.json"),
                    ]
                )

    def test_list_saved_analyses_prints_deterministic_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            main(["init-db", "--db", str(db_path)])
            user_deck_id, saved_id = self._seed_saved_analysis(db_path)

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "list-saved-analyses",
                        "--db",
                        str(db_path),
                        "--user-deck-id",
                        str(user_deck_id),
                    ]
                )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["user_deck_id"], user_deck_id)
            self.assertEqual(payload["saved_analyses"][0]["saved_analysis_id"], saved_id)
            self.assertEqual(payload["saved_analyses"][0]["analysis_type"], "user_deck_evidence_comparison")

    def test_show_saved_analysis_prints_detail_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            main(["init-db", "--db", str(db_path)])
            _, saved_id = self._seed_saved_analysis(db_path)

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "show-saved-analysis",
                        "--db",
                        str(db_path),
                        "--saved-analysis-id",
                        str(saved_id),
                    ]
                )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["summary"]["saved_analysis_id"], saved_id)
            self.assertEqual(payload["summary_payload"]["absent_count"], 1)
            self.assertEqual(payload["summary_payload"]["rows"][0]["card_name"], "Mystic Remora")

    def test_export_ui_saved_analysis_list_writes_page_model_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            output = root / "ui" / "saved-analyses.json"
            main(["init-db", "--db", str(db_path)])
            user_deck_id, saved_id = self._seed_saved_analysis(db_path)

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "export-ui-saved-analysis-list",
                        "--db",
                        str(db_path),
                        "--user-deck-id",
                        str(user_deck_id),
                        "--output",
                        str(output),
                        "--output-root",
                        str(root),
                        "--exported-at",
                        NOW,
                    ]
                )

            self.assertEqual(exit_code, 0)
            summary = json.loads(stdout.getvalue())
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(summary["content_type"], "application/json")
            self.assertEqual(payload["source"]["export_type"], "saved_analysis_list")
            self.assertEqual(payload["rows"][0]["saved_analysis_id"], saved_id)

    def test_export_ui_saved_analysis_detail_writes_page_model_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            db_path = root / "codie.sqlite"
            output = root / "ui" / "saved-analysis-detail.json"
            main(["init-db", "--db", str(db_path)])
            _, saved_id = self._seed_saved_analysis(db_path)

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "export-ui-saved-analysis-detail",
                        "--db",
                        str(db_path),
                        "--saved-analysis-id",
                        str(saved_id),
                        "--output",
                        str(output),
                        "--output-root",
                        str(root),
                        "--exported-at",
                        NOW,
                    ]
                )

            self.assertEqual(exit_code, 0)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["source"]["export_type"], "saved_analysis_detail")
            self.assertEqual(payload["source"]["saved_analysis_id"], saved_id)
            self.assertEqual(payload["rows"][0]["card_name"], "Mystic Remora")

    def test_build_share_bundle_writes_static_index_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "comparison.md"
            report.write_text("# Evidence\n", encoding="utf-8")

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "build-share-bundle",
                        "--title",
                        "Codie Evidence Bundle",
                        "--generated-at",
                        NOW,
                        "--asset",
                        str(report),
                        "--asset-label",
                        "Comparison",
                        "--output-dir",
                        str(root / "bundle"),
                        "--output-root",
                        str(root),
                        "--qr-target",
                        "http://127.0.0.1:4173/index.html",
                    ]
                )

            self.assertEqual(exit_code, 0)
            result = json.loads(stdout.getvalue())
            self.assertTrue((root / "bundle" / "index.html").exists())
            self.assertTrue((root / "bundle" / "manifest.json").exists())
            self.assertTrue((root / "bundle" / "assets" / "comparison.md").exists())
            self.assertTrue((root / "bundle" / "assets" / "bundle-entry-qr.png").exists())
            self.assertEqual(result["asset_paths"], [str(root / "bundle" / "assets" / "comparison.md")])
            self.assertEqual(result["qr_asset_path"], str(root / "bundle" / "assets" / "bundle-entry-qr.png"))

    def test_cli_module_has_no_provider_or_recommendation_imports(self) -> None:
        import codie.cli.user_deck as cli_module

        source = Path(cli_module.__file__).read_text(encoding="utf-8")
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

    def _seed_cards(self, db_path: Path) -> None:
        connection = connect(db_path)
        try:
            core = CoreRepository(connection)
            core.insert_card(
                {
                    "scryfall_id": "tymna",
                    "oracle_id": "oracle-tymna",
                    "name": "Tymna the Weaver",
                    "normalized_name": "tymna the weaver",
                    "raw_json": "{}",
                    "imported_at": NOW,
                }
            )
            core.insert_card(
                {
                    "scryfall_id": "lotus",
                    "oracle_id": "oracle-lotus",
                    "name": "Jeweled Lotus",
                    "normalized_name": "jeweled lotus",
                    "raw_json": "{}",
                    "imported_at": NOW,
                }
            )
            connection.commit()
        finally:
            connection.close()

    def _seed_saved_analysis(self, db_path: Path) -> tuple[int, int]:
        connection = connect(db_path)
        try:
            user = UserRepository(connection)
            user_deck_id = user.create_user_deck(
                {
                    "deck_hash": "deck-hash",
                    "created_at": NOW,
                    "updated_at": NOW,
                }
            )
            result = save_user_deck_comparison_analysis(
                user,
                UserDeckEvidenceComparison(
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
                    generated_at=NOW,
                ),
            )
            connection.commit()
            return user_deck_id, result.saved_analysis_id
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
