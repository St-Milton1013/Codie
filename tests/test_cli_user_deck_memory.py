from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from codie.cli.user_deck_memory import main
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.user import UserRepository


class UserDeckMemoryCliTest(unittest.TestCase):
    def test_list_command_prints_deterministic_json_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, first_id, second_id = self._seed_memory(Path(directory))

            exit_code, stdout, _ = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(db_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout)
            self.assertEqual(
                [deck["user_deck_id"] for deck in payload["decks"]],
                [second_id, first_id],
            )
            self.assertEqual(payload["decks"][1]["deck_name"], "Tymna Kraum")
            self.assertEqual(payload["decks"][1]["card_count"], 2)
            self.assertNotIn("raw_input", payload["decks"][1])

    def test_list_command_filters_by_commander_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, first_id, _ = self._seed_memory(Path(directory))

            exit_code, stdout, _ = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(db_path),
                    "--commander-hash",
                    "tymna|kraum",
                ]
            )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout)
            self.assertEqual([deck["user_deck_id"] for deck in payload["decks"]], [first_id])

    def test_list_command_filters_by_deck_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, _, second_id = self._seed_memory(Path(directory))

            exit_code, stdout, _ = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(db_path),
                    "--deck-hash",
                    "deck-b",
                ]
            )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout)
            self.assertEqual([deck["user_deck_id"] for deck in payload["decks"]], [second_id])

    def test_list_command_include_exclude_temporary_flags_work(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, first_id, second_id = self._seed_memory(Path(directory))

            persistent_exit, persistent_stdout, _ = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(db_path),
                    "--exclude-temporary",
                ]
            )
            temporary_exit, temporary_stdout, _ = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(db_path),
                    "--exclude-persistent",
                ]
            )

            self.assertEqual(persistent_exit, 0)
            self.assertEqual(temporary_exit, 0)
            self.assertEqual(
                [deck["user_deck_id"] for deck in json.loads(persistent_stdout)["decks"]],
                [first_id],
            )
            self.assertEqual(
                [deck["user_deck_id"] for deck in json.loads(temporary_stdout)["decks"]],
                [second_id],
            )

    def test_list_command_validates_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, _, _ = self._seed_memory(Path(directory))

            exit_code, stdout, stderr = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(db_path),
                    "--limit",
                    "0",
                ]
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stdout, "")
            self.assertIn("limit", stderr)

    def test_show_command_prints_deck_detail_without_raw_input_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, first_id, _ = self._seed_memory(Path(directory))

            exit_code, stdout, _ = self._run_cli(
                [
                    "show-deck-memory",
                    "--db",
                    str(db_path),
                    "--user-deck-id",
                    str(first_id),
                ]
            )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout)
            deck = payload["deck"]
            self.assertEqual(deck["summary"]["user_deck_id"], first_id)
            self.assertNotIn("raw_input", deck)
            self.assertEqual([card["raw_name"] for card in deck["cards"]], ["Mystic Remora", "Chrome Mox"])
            self.assertEqual(deck["saved_analyses"][0]["analysis_type"], "user_deck_evidence_comparison")
            self.assertEqual(deck["analysis_sessions"][0]["session_type"], "evidence_comparison")

    def test_show_command_includes_raw_input_only_with_explicit_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, first_id, _ = self._seed_memory(Path(directory))

            exit_code, stdout, _ = self._run_cli(
                [
                    "show-deck-memory",
                    "--db",
                    str(db_path),
                    "--user-deck-id",
                    str(first_id),
                    "--include-raw-input",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(json.loads(stdout)["deck"]["raw_input"], "1 Mystic Remora\n1 Chrome Mox")

    def test_unknown_user_deck_id_exits_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, _, _ = self._seed_memory(Path(directory))

            exit_code, stdout, stderr = self._run_cli(
                [
                    "show-deck-memory",
                    "--db",
                    str(db_path),
                    "--user-deck-id",
                    "999",
                ]
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stdout, "")
            self.assertIn("Unknown user_deck_id", stderr)

    def test_missing_database_path_exits_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.sqlite"

            exit_code, stdout, stderr = self._run_cli(
                [
                    "list-deck-memory",
                    "--db",
                    str(missing),
                ]
            )

            self.assertEqual(exit_code, 1)
            self.assertEqual(stdout, "")
            self.assertIn("database path does not exist", stderr)

    def test_cli_module_has_no_forbidden_imports_or_source_table_reads(self) -> None:
        import codie.cli.user_deck_memory as cli_module

        source = Path(cli_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "codie." + "canonical",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "source_" + "events",
            "source_" + "decks",
            "source_" + "deck_cards",
            "provider_" + "objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)

    def test_cli_output_contains_no_recommendation_language(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path, first_id, _ = self._seed_memory(Path(directory))

            _, list_stdout, _ = self._run_cli(["list-deck-memory", "--db", str(db_path)])
            _, show_stdout, _ = self._run_cli(
                [
                    "show-deck-memory",
                    "--db",
                    str(db_path),
                    "--user-deck-id",
                    str(first_id),
                ]
            )

            output = list_stdout + show_stdout
            forbidden = (
                "should " + "play",
                "must " + "include",
                "correct " + "card",
                "breaks " + "the format",
                "secretly " + "optimal",
                "cut " + "this",
                "strict " + "upgrade",
                "auto-" + "include",
                "recommended " + "cut",
                "recommended " + "include",
            )
            for phrase in forbidden:
                self.assertNotIn(phrase, output)

    def _run_cli(self, argv: list[str]) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(argv)
        return exit_code, stdout.getvalue().strip(), stderr.getvalue().strip()

    def _seed_memory(self, root: Path) -> tuple[Path, int, int]:
        db_path = root / "codie.sqlite"
        connection = bootstrap_database(db_path)
        try:
            user = UserRepository(connection)
            first_id = user.create_user_deck(
                {
                    "deck_name": "Tymna Kraum",
                    "source_url": "https://moxfield.com/decks/one",
                    "deck_hash": "deck-a",
                    "commander_hash": "tymna|kraum",
                    "raw_input": "1 Mystic Remora\n1 Chrome Mox",
                    "created_at": "2026-07-01T00:00:00+00:00",
                    "updated_at": "2026-07-02T00:00:00+00:00",
                    "is_temporary": 0,
                }
            )
            second_id = user.create_user_deck(
                {
                    "deck_name": "Rograkh Silas",
                    "source_url": "https://moxfield.com/decks/two",
                    "deck_hash": "deck-b",
                    "commander_hash": "rograkh|silas",
                    "raw_input": "1 Sol Ring",
                    "created_at": "2026-07-02T00:00:00+00:00",
                    "updated_at": "2026-07-03T00:00:00+00:00",
                    "is_temporary": 1,
                }
            )
            user.add_user_deck_card(
                {
                    "user_deck_id": first_id,
                    "raw_name": "Mystic Remora",
                    "quantity": 1,
                    "zone": "mainboard",
                    "oracle_id": "oracle-remora",
                    "resolution_status": "resolved",
                }
            )
            user.add_user_deck_card(
                {
                    "user_deck_id": first_id,
                    "raw_name": "Chrome Mox",
                    "quantity": 1,
                    "zone": "mainboard",
                    "oracle_id": "oracle-mox",
                    "resolution_status": "resolved",
                }
            )
            user.create_saved_analysis(
                {
                    "user_deck_id": first_id,
                    "deck_hash": "deck-a",
                    "analysis_type": "user_deck_evidence_comparison",
                    "generated_at": "2026-07-02T01:00:00+00:00",
                    "summary_json": "{}",
                    "report_path": "reports/tymna-kraum.md",
                }
            )
            user.create_analysis_session(
                {
                    "user_deck_id": first_id,
                    "deck_hash": "deck-a",
                    "commander_hash": "tymna|kraum",
                    "session_type": "evidence_comparison",
                    "status": "complete",
                    "started_at": "2026-07-02T00:30:00+00:00",
                    "completed_at": "2026-07-02T00:31:00+00:00",
                }
            )
            connection.commit()
            return db_path, first_id, second_id
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
