from __future__ import annotations

import unittest
from pathlib import Path

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.user import UserRepository
from codie.user_decks import (
    DeckMemoryFilters,
    DeckMemoryReadError,
    get_deck_memory_detail,
    list_deck_memory,
)


class UserDeckMemoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.user = UserRepository(self.connection)
        self.first_deck_id = self._create_deck(
            deck_hash="deck-a",
            commander_hash="tymna|kraum",
            deck_name="Tymna Kraum July",
            created_at="2026-07-01T10:00:00+00:00",
            updated_at="2026-07-02T10:00:00+00:00",
            is_temporary=0,
            raw_input="1 Mystic Remora\n1 Chrome Mox",
        )
        self.second_deck_id = self._create_deck(
            deck_hash="deck-b",
            commander_hash="thrasios|tymna",
            deck_name="Thrasios Tymna Test",
            created_at="2026-07-02T09:00:00+00:00",
            updated_at="2026-07-03T09:00:00+00:00",
            is_temporary=1,
            raw_input="1 Sol Ring",
        )
        self.third_deck_id = self._create_deck(
            deck_hash="deck-c",
            commander_hash="tymna|kraum",
            deck_name="Tymna Kraum Older",
            created_at="2026-06-15T09:00:00+00:00",
            updated_at="2026-06-15T10:00:00+00:00",
            is_temporary=0,
            raw_input="1 Dark Ritual",
        )

        self.user.add_user_deck_card(
            {
                "user_deck_id": self.first_deck_id,
                "raw_name": "Mystic Remora",
                "quantity": 1,
                "zone": "mainboard",
                "oracle_id": "oracle-remora",
                "resolution_status": "resolved",
            }
        )
        self.user.add_user_deck_card(
            {
                "user_deck_id": self.first_deck_id,
                "raw_name": "Chrome Mox",
                "quantity": 1,
                "zone": "mainboard",
                "oracle_id": "oracle-mox",
                "resolution_status": "resolved",
            }
        )
        self.user.add_user_deck_card(
            {
                "user_deck_id": self.second_deck_id,
                "raw_name": "Sol Ring",
                "quantity": 1,
                "zone": "mainboard",
                "resolution_status": "resolved",
            }
        )

        self.user.create_saved_analysis(
            {
                "user_deck_id": self.first_deck_id,
                "deck_hash": "deck-a",
                "analysis_type": "first",
                "generated_at": "2026-07-02T11:00:00+00:00",
                "summary_json": "{}",
                "report_path": "reports/first.md",
            }
        )
        self.user.create_saved_analysis(
            {
                "user_deck_id": self.first_deck_id,
                "deck_hash": "deck-a",
                "analysis_type": "second",
                "generated_at": "2026-07-02T12:00:00+00:00",
                "summary_json": "{}",
                "report_path": "reports/second.md",
            }
        )
        self.user.create_analysis_session(
            {
                "user_deck_id": self.first_deck_id,
                "deck_hash": "deck-a",
                "commander_hash": "tymna|kraum",
                "session_type": "evidence_comparison",
                "status": "complete",
                "started_at": "2026-07-02T10:30:00+00:00",
                "completed_at": "2026-07-02T10:31:00+00:00",
            }
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_list_deck_memory_returns_deterministic_summaries(self) -> None:
        summaries = list_deck_memory(self.user)

        self.assertEqual(
            [summary.user_deck_id for summary in summaries],
            [self.second_deck_id, self.first_deck_id, self.third_deck_id],
        )
        self.assertEqual(summaries[1].deck_name, "Tymna Kraum July")
        self.assertEqual(summaries[1].card_count, 2)
        self.assertEqual(summaries[1].saved_analysis_count, 2)
        self.assertEqual(
            summaries[1].latest_analysis_generated_at,
            "2026-07-02T12:00:00+00:00",
        )

    def test_list_deck_memory_filters_by_commander_hash(self) -> None:
        summaries = list_deck_memory(
            self.user,
            DeckMemoryFilters(commander_hash="tymna|kraum"),
        )

        self.assertEqual(
            [summary.user_deck_id for summary in summaries],
            [self.first_deck_id, self.third_deck_id],
        )

    def test_list_deck_memory_filters_by_deck_hash(self) -> None:
        summaries = list_deck_memory(self.user, DeckMemoryFilters(deck_hash="deck-b"))

        self.assertEqual(len(summaries), 1)
        self.assertEqual(summaries[0].user_deck_id, self.second_deck_id)

    def test_list_deck_memory_includes_and_excludes_temporary_decks(self) -> None:
        persistent = list_deck_memory(
            self.user,
            DeckMemoryFilters(include_temporary=False),
        )
        temporary = list_deck_memory(
            self.user,
            DeckMemoryFilters(include_persistent=False),
        )

        self.assertEqual(
            [summary.user_deck_id for summary in persistent],
            [self.first_deck_id, self.third_deck_id],
        )
        self.assertEqual([summary.user_deck_id for summary in temporary], [self.second_deck_id])

    def test_list_deck_memory_filters_by_created_at_window(self) -> None:
        summaries = list_deck_memory(
            self.user,
            DeckMemoryFilters(
                created_at_from="2026-07-01T00:00:00+00:00",
                created_at_to="2026-07-01T23:59:59+00:00",
            ),
        )

        self.assertEqual([summary.user_deck_id for summary in summaries], [self.first_deck_id])

    def test_list_deck_memory_validates_limit(self) -> None:
        with self.assertRaises(DeckMemoryReadError):
            DeckMemoryFilters(limit=0)

        summaries = list_deck_memory(self.user, DeckMemoryFilters(limit=1))
        self.assertEqual(len(summaries), 1)

    def test_get_deck_memory_detail_returns_raw_input(self) -> None:
        detail = get_deck_memory_detail(self.user, self.first_deck_id)

        self.assertEqual(detail.raw_input, "1 Mystic Remora\n1 Chrome Mox")
        self.assertEqual(detail.summary.user_deck_id, self.first_deck_id)

    def test_get_deck_memory_detail_returns_cards_in_import_order(self) -> None:
        detail = get_deck_memory_detail(self.user, self.first_deck_id)

        self.assertEqual([card.raw_name for card in detail.cards], ["Mystic Remora", "Chrome Mox"])
        self.assertEqual(detail.cards[0].oracle_id, "oracle-remora")
        self.assertEqual(detail.cards[0].resolution_status, "resolved")

    def test_get_deck_memory_detail_returns_saved_analyses(self) -> None:
        detail = get_deck_memory_detail(self.user, self.first_deck_id)

        self.assertEqual(
            [analysis.analysis_type for analysis in detail.saved_analyses],
            ["first", "second"],
        )
        self.assertEqual(detail.saved_analyses[0].report_path, "reports/first.md")

    def test_get_deck_memory_detail_returns_analysis_sessions(self) -> None:
        detail = get_deck_memory_detail(self.user, self.first_deck_id)

        self.assertEqual(len(detail.analysis_sessions), 1)
        self.assertEqual(detail.analysis_sessions[0].session_type, "evidence_comparison")
        self.assertEqual(detail.analysis_sessions[0].status, "complete")

    def test_get_deck_memory_detail_rejects_unknown_deck(self) -> None:
        with self.assertRaises(DeckMemoryReadError):
            get_deck_memory_detail(self.user, 999)

    def test_deck_memory_has_no_forbidden_imports_or_source_table_reads(self) -> None:
        import codie.user_decks.deck_memory as deck_memory_module

        source = Path(deck_memory_module.__file__).read_text(encoding="utf-8")
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
            "provider_" + "objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)

    def _create_deck(
        self,
        *,
        deck_hash: str,
        commander_hash: str,
        deck_name: str,
        created_at: str,
        updated_at: str,
        is_temporary: int,
        raw_input: str,
    ) -> int:
        return self.user.create_user_deck(
            {
                "deck_name": deck_name,
                "source_url": "https://moxfield.com/decks/example",
                "deck_hash": deck_hash,
                "commander_hash": commander_hash,
                "raw_input": raw_input,
                "created_at": created_at,
                "updated_at": updated_at,
                "is_temporary": is_temporary,
            }
        )


if __name__ == "__main__":
    unittest.main()
