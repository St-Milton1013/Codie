from __future__ import annotations

import json
from pathlib import Path
import unittest

from codie.canonical.deck_hash import commander_hash, deck_hash
from codie.canonical.event_matcher import event_dedupe_key
from codie.canonical.canonicalizer import CanonicalizationError, Canonicalizer
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.source import SourceRepository


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "canonicalization"
NOW = "2026-06-21T00:00:00+00:00"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class CanonicalizationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.canonical = CanonicalRepository(self.connection)
        self.canonicalizer = Canonicalizer(self.source, self.canonical)
        self.deck_cases = load_fixture("deck_hash_cases.json")
        for card in self.deck_cases["cards"].values():
            self.core.insert_card(
                {
                    "scryfall_id": card["scryfall_id"],
                    "oracle_id": card["oracle_id"],
                    "name": card["name"],
                    "normalized_name": card["name"].lower().replace(",", "").replace("'", ""),
                    "raw_json": "{}",
                    "imported_at": NOW,
                }
            )

    def tearDown(self) -> None:
        self.connection.close()

    def create_source_event(self, payload: dict) -> int:
        data = dict(payload)
        data.setdefault("imported_at", NOW)
        return self.source.create_source_event(data)

    def create_source_deck(self, deck: dict, source_event_id: int | None = None) -> int:
        source_deck_id = self.source.create_source_deck(
            {
                "provider": deck["provider"],
                "provider_deck_id": deck["provider_deck_id"],
                "source_event_id": source_event_id,
                "source_url": f"https://example.test/{deck['provider_deck_id']}",
                "deck_title": deck["provider_deck_id"],
                "commander_text": deck.get("commander_text"),
                "source_player_name": deck.get("pilot_name", "Fixture Pilot"),
                "source_rank": deck.get("rank", 1),
                "source_rank_label": deck.get("rank_label", "1st"),
                "source_record": deck.get("record", "4-0"),
                "raw_json": json.dumps(deck, sort_keys=True),
                "imported_at": NOW,
            }
        )
        for index, card in enumerate(deck["cards"], start=1):
            self.source.create_source_deck_card(
                {
                    "source_deck_id": source_deck_id,
                    "raw_name": card.get("raw_name") or card.get("scryfall_id") or "Unknown",
                    "quantity": card["quantity"],
                    "source_zone": card["source_zone"],
                    "source_order": index,
                    "scryfall_id": card.get("scryfall_id"),
                    "oracle_id": card.get("oracle_id"),
                    "resolution_status": "exact" if card.get("scryfall_id") else "unresolved",
                    "raw_entry": json.dumps(card, sort_keys=True),
                }
            )
        return source_deck_id

    def test_event_dedupe_cases_match_expectations(self) -> None:
        for case in load_fixture("event_dedupe_cases.json")["cases"]:
            keys = [event_dedupe_key(event) for event in case["source_events"]]
            self.assertEqual(keys[0] == keys[1], case["expected_same_canonical_event"], case["id"])

    def test_deck_hash_cases_match_expectations(self) -> None:
        for case in self.deck_cases["cases"]:
            if "decks" not in case:
                continue
            hashes = [deck_hash(deck["cards"], self.commander_cards(deck), format="commander") for deck in case["decks"]]
            self.assertEqual(hashes[0] == hashes[1], case["expected_same_deck_hash"], case["id"])

    def test_commander_hash_uses_normalized_alphabetical_signature(self) -> None:
        commanders = [
            {"scryfall_id": "kraum-card", "oracle_id": "kraum-oracle", "name": "Kraum, Ludevic's Opus"},
            {"scryfall_id": "tymna-card", "oracle_id": "tymna-oracle", "name": "Tymna the Weaver"},
        ]
        self.assertEqual(commander_hash(commanders), "kraum-card|tymna-card")

    def test_same_event_across_sources_dedupes_and_links_provenance(self) -> None:
        case = load_fixture("event_dedupe_cases.json")["cases"][0]
        first_id = self.create_source_event(case["source_events"][0])
        second_id = self.create_source_event(case["source_events"][1])
        first = self.canonicalizer.canonicalize_event(first_id)
        second = self.canonicalizer.canonicalize_event(second_id)
        self.assertEqual(first.canonical_id, second.canonical_id)
        self.assertEqual(self.source.get_source_event(first_id)["canonical_event_id"], first.canonical_id)
        self.assertEqual(self.source.get_source_event(second_id)["canonical_event_id"], first.canonical_id)
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM canonical_event_sources").fetchone()["count"],
            2,
        )

    def test_event_canonicalization_is_idempotent(self) -> None:
        case = load_fixture("event_dedupe_cases.json")["cases"][0]["source_events"][0]
        source_event_id = self.create_source_event(case)
        first = self.canonicalizer.canonicalize_event(source_event_id)
        second = self.canonicalizer.canonicalize_event(source_event_id)
        self.assertEqual(first.canonical_id, second.canonical_id)
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM canonical_event_sources").fetchone()["count"],
            1,
        )

    def test_similar_events_do_not_dedupe(self) -> None:
        for case in load_fixture("event_dedupe_cases.json")["cases"][1:]:
            ids = [self.create_source_event(event) for event in case["source_events"]]
            results = [self.canonicalizer.canonicalize_event(source_event_id) for source_event_id in ids]
            self.assertNotEqual(results[0].canonical_id, results[1].canonical_id, case["id"])

    def test_canonical_deck_persists_cards_commanders_and_source_links(self) -> None:
        event_payload = load_fixture("event_dedupe_cases.json")["cases"][0]["source_events"][0]
        source_event_id = self.create_source_event(event_payload)
        canonical_event = self.canonicalizer.canonicalize_event(source_event_id)
        deck_payload = self.deck_cases["cases"][0]["decks"][0]
        source_deck_id = self.create_source_deck(deck_payload, source_event_id)
        result = self.canonicalizer.canonicalize_deck(source_deck_id)
        self.assertTrue(result.created)
        source_deck = self.source.get_source_deck(source_deck_id)
        self.assertEqual(source_deck["canonical_deck_id"], result.canonical_id)
        self.assertEqual(source_deck["dedupe_status"], "canonicalized")
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM canonical_deck_cards").fetchone()["count"],
            5,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM canonical_deck_commanders").fetchone()["count"],
            2,
        )
        entry = self.connection.execute("SELECT * FROM event_deck_entries").fetchone()
        self.assertEqual(entry["canonical_event_id"], canonical_event.canonical_id)
        self.assertEqual(entry["canonical_deck_id"], result.canonical_id)
        self.assertEqual(entry["source_deck_id"], source_deck_id)

    def test_same_deck_across_sources_links_to_one_canonical_deck(self) -> None:
        case = self.deck_cases["cases"][0]
        ids = [self.create_source_deck(deck) for deck in case["decks"]]
        results = [self.canonicalizer.canonicalize_deck(source_deck_id) for source_deck_id in ids]
        self.assertEqual(results[0].canonical_id, results[1].canonical_id)
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM canonical_deck_sources").fetchone()["count"],
            2,
        )

    def test_unresolved_source_card_blocks_canonicalization(self) -> None:
        deck = next(case for case in self.deck_cases["cases"] if case["id"] == "unresolved_card_blocks_canonicalization")["deck"]
        source_deck_id = self.create_source_deck(deck)
        with self.assertRaises(CanonicalizationError):
            self.canonicalizer.canonicalize_deck(source_deck_id)
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) AS count FROM canonical_decks").fetchone()["count"],
            0,
        )

    def test_raw_provider_payloads_are_not_modified(self) -> None:
        deck_payload = self.deck_cases["cases"][0]["decks"][0]
        source_deck_id = self.create_source_deck(deck_payload)
        before = self.source.get_source_deck(source_deck_id)["raw_json"]
        self.canonicalizer.canonicalize_deck(source_deck_id)
        after = self.source.get_source_deck(source_deck_id)["raw_json"]
        self.assertEqual(before, after)

    def commander_cards(self, deck: dict) -> list[dict]:
        return [card for card in deck["cards"] if card["source_zone"] == "commanders"]


if __name__ == "__main__":
    unittest.main()
