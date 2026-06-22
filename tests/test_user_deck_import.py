from __future__ import annotations

import unittest

from codie.cards.lookup import CardLookup
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.user import UserRepository
from codie.user_decks import UserDeckImportError, UserDeckImporter, parse_user_deck_text


NOW = "2026-06-22T00:00:00+00:00"


class UserDeckImportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.user = UserRepository(self.connection)
        self._insert_card("tymna", "oracle-tymna", "Tymna the Weaver", "tymna the weaver")
        self._insert_card("kraum", "oracle-kraum", "Kraum, Ludevic's Opus", "kraum ludevics opus")
        self._insert_card("lotus", "oracle-lotus", "Jeweled Lotus", "jeweled lotus")
        self._insert_card("study", "oracle-study", "Rhystic Study", "rhystic study")

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

    def importer(self) -> UserDeckImporter:
        return UserDeckImporter(self.user, CardLookup(self.core))

    def test_parse_user_deck_text_sections_and_cards(self) -> None:
        parsed = parse_user_deck_text(
            """
            Commander
            1 Tymna the Weaver
            1 Kraum, Ludevic's Opus

            Mainboard
            1 Jeweled Lotus
            2 Rhystic Study
            """,
            deck_name="Fixture Deck",
        )
        self.assertEqual(parsed.deck_name, "Fixture Deck")
        self.assertEqual(len(parsed.cards), 4)
        self.assertEqual(parsed.cards[0].zone, "commander")
        self.assertEqual(parsed.cards[2].zone, "mainboard")
        self.assertEqual(parsed.cards[3].quantity, 2)

    def test_import_text_persists_user_deck_cards_and_analysis_session(self) -> None:
        result = self.importer().import_text(
            """
            Commander:
            1 Kraum, Ludevic's Opus
            1 Tymna the Weaver

            Deck:
            1 Jeweled Lotus
            1 Rhystic Study
            """,
            deck_name="Blue Farm Test",
            source_url="https://example.test/deck",
        )
        deck = self.connection.execute("SELECT * FROM user_decks").fetchone()
        cards = self.connection.execute("SELECT * FROM user_deck_cards ORDER BY user_deck_card_id").fetchall()
        session = self.connection.execute("SELECT * FROM analysis_sessions").fetchone()

        self.assertEqual(result.card_count, 4)
        self.assertEqual(deck["deck_name"], "Blue Farm Test")
        self.assertEqual(deck["source_url"], "https://example.test/deck")
        self.assertEqual(deck["deck_hash"], result.deck_hash)
        self.assertEqual(deck["commander_hash"], "kraum, ludevic's opus|tymna the weaver")
        self.assertEqual(len(cards), 4)
        self.assertEqual(cards[0]["zone"], "commander")
        self.assertEqual(cards[0]["resolution_status"], "exact")
        self.assertEqual(cards[2]["scryfall_id"], "lotus")
        self.assertEqual(session["analysis_session_id"], result.analysis_session_id)
        self.assertEqual(session["status"], "created")
        self.assertEqual(session["session_type"], "deck_import")

    def test_unresolved_card_rolls_back_entire_import(self) -> None:
        with self.assertRaises(UserDeckImportError):
            self.importer().import_text(
                """
                Commander
                1 Tymna the Weaver

                Mainboard
                1 Unknown Card
                """
            )
        self.assertEqual(self.connection.execute("SELECT COUNT(*) AS count FROM user_decks").fetchone()["count"], 0)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) AS count FROM user_deck_cards").fetchone()["count"], 0)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) AS count FROM analysis_sessions").fetchone()["count"], 0)

    def test_malformed_deck_text_fails_cleanly(self) -> None:
        with self.assertRaises(UserDeckImportError):
            parse_user_deck_text("Commander\nTymna the Weaver")

    def test_user_deck_package_has_no_provider_or_recommendation_imports(self) -> None:
        import codie.user_decks.importer as importer_module

        source_path = importer_module.__file__
        with open(source_path, encoding="utf-8") as handle:
            source = handle.read()
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
