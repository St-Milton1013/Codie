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


if __name__ == "__main__":
    unittest.main()
