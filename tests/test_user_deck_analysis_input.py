from __future__ import annotations

import unittest

from codie.cards.lookup import CardLookup
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.user import UserRepository
from codie.user_decks import (
    UserDeckAnalysisInputError,
    UserDeckImporter,
    build_user_deck_analysis_input,
)


NOW = "2026-06-22T00:00:00+00:00"


class UserDeckAnalysisInputTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.user = UserRepository(self.connection)
        self._insert_card("tymna", "oracle-tymna", "Tymna the Weaver", "tymna the weaver")
        self._insert_card("lotus", "oracle-lotus", "Jeweled Lotus", "jeweled lotus")

    def tearDown(self) -> None:
        self.connection.close()

    def _insert_card(self, scryfall_id: str, oracle_id: str, name: str, normalized_name: str) -> None:
        self.core.insert_card(
            {
                "scryfall_id": scryfall_id,
                "oracle_id": oracle_id,
                "name": name,
                "normalized_name": normalized_name,
                "raw_json": "{}",
                "imported_at": NOW,
            }
        )

    def test_build_user_deck_analysis_input_from_imported_deck(self) -> None:
        imported = UserDeckImporter(self.user, CardLookup(self.core)).import_text(
            """
            Commander
            1 Tymna the Weaver

            Mainboard
            1 Jeweled Lotus
            """,
            deck_name="Analysis Fixture",
        )
        analysis_input = build_user_deck_analysis_input(
            self.user,
            imported.user_deck_id,
            analysis_session_id=imported.analysis_session_id,
        )
        self.assertEqual(analysis_input.deck_name, "Analysis Fixture")
        self.assertEqual(analysis_input.deck_hash, imported.deck_hash)
        self.assertEqual(analysis_input.commander_hash, "tymna the weaver")
        self.assertEqual(analysis_input.analysis_session_id, imported.analysis_session_id)
        self.assertTrue(analysis_input.is_temporary)
        self.assertEqual(analysis_input.commander_count, 1)
        self.assertEqual(analysis_input.mainboard_count, 1)
        self.assertEqual(analysis_input.total_card_count, 2)
        self.assertEqual(analysis_input.unresolved_cards, ())
        self.assertEqual(analysis_input.cards[1].oracle_id, "oracle-lotus")

    def test_missing_user_deck_fails_cleanly(self) -> None:
        with self.assertRaises(UserDeckAnalysisInputError):
            build_user_deck_analysis_input(self.user, 404)

    def test_session_must_belong_to_user_deck(self) -> None:
        imported = UserDeckImporter(self.user, CardLookup(self.core)).import_text("1 Jeweled Lotus")
        other_deck_id = self.user.create_user_deck(
            {
                "deck_hash": "other",
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
        with self.assertRaises(UserDeckAnalysisInputError):
            build_user_deck_analysis_input(
                self.user,
                other_deck_id,
                analysis_session_id=imported.analysis_session_id,
            )

    def test_unresolved_rows_are_exposed_for_future_partial_modes(self) -> None:
        deck_id = self.user.create_user_deck(
            {
                "deck_hash": "partial",
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
        self.user.add_user_deck_card(
            {
                "user_deck_id": deck_id,
                "raw_name": "Unknown Card",
                "quantity": 1,
                "zone": "mainboard",
                "resolution_status": "unresolved",
            }
        )
        analysis_input = build_user_deck_analysis_input(self.user, deck_id)
        self.assertEqual(len(analysis_input.unresolved_cards), 1)
        self.assertEqual(analysis_input.unresolved_cards[0].raw_name, "Unknown Card")


if __name__ == "__main__":
    unittest.main()
