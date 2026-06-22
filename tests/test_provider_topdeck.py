from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.cards.lookup import CardLookup
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.source import SourceRepository
from codie.ingestion.pipeline import DeckIngestionPipeline
from codie.providers.errors import NetworkError, ParseError, RateLimitError
from codie.providers.models import SourceDeckCandidate, SourceDeckCardCandidate, SourceEventCandidate
from codie.providers.topdeck import client as topdeck_client
from codie.providers.topdeck.client import TopDeckClient
from codie.providers.topdeck.parser import TopDeckProvider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "topdeck"
NOW = "2026-06-21T00:00:00+00:00"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class TopDeckProviderTest(unittest.TestCase):
    def test_parse_event_success(self) -> None:
        candidate = TopDeckProvider().parse_event(load_fixture("event_12345.json"))
        self.assertIsInstance(candidate, SourceEventCandidate)
        self.assertEqual(candidate.provider, "topdeck")
        self.assertEqual(candidate.provider_event_id, "12345")
        self.assertEqual(candidate.event_name, "TopDeck Example cEDH Open")
        self.assertEqual(candidate.region, "north_america")
        self.assertEqual(candidate.player_count, 64)
        self.assertTrue(candidate.raw_payload.payload_hash.startswith("sha256:"))

    def test_parse_documented_v2_tournament_shape(self) -> None:
        provider = TopDeckProvider()
        parsed = provider.parse(load_fixture("tournament_v2_single.json"))
        event = parsed["events"][0]
        deck = parsed["decks"][0]
        self.assertEqual(event.provider_event_id, "abc123")
        self.assertEqual(event.event_name, "Documented EDH Open")
        self.assertEqual(event.format, "EDH")
        self.assertEqual(event.region, "WA")
        self.assertEqual(event.country, "US")
        self.assertEqual(event.deck_count, 1)
        self.assertEqual(deck.provider_deck_id, "player123")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.rank, 1)
        self.assertEqual(deck.win_rate, 0.83)
        self.assertEqual(len(deck.cards), 3)

    def test_parse_documented_bulk_tournament_shape(self) -> None:
        raw = {
            "TID": "bulk123",
            "tournamentName": "Bulk EDH Event",
            "startDate": 1780272000,
            "game": "Magic: The Gathering",
            "format": "EDH",
            "eventData": {"state": "TX", "address": "Example Address"},
            "standings": [],
        }
        event = TopDeckProvider().parse_event(raw)
        self.assertEqual(event.provider_event_id, "bulk123")
        self.assertEqual(event.event_name, "Bulk EDH Event")
        self.assertEqual(event.region, "TX")
        self.assertEqual(event.deck_count, 0)

    def test_parse_tournament_skips_standings_without_decklists(self) -> None:
        raw = {
            "TID": "bulk124",
            "tournamentName": "No Decklist Event",
            "format": "EDH",
            "standings": [{"standing": 1, "name": "Hidden Deck Pilot", "id": "hidden"}],
        }
        parsed = TopDeckProvider().parse(raw)
        self.assertEqual(parsed["events"][0].provider_event_id, "bulk124")
        self.assertEqual(parsed["decks"], ())

    def test_parse_tournament_skips_unstructured_decklists(self) -> None:
        raw = {
            "TID": "bulk125",
            "tournamentName": "Unstructured Decklist Event",
            "format": "EDH",
            "standings": [
                {
                    "name": "Deck Text Pilot",
                    "id": "deck-text",
                    "deckObj": None,
                    "decklist": "~~Commanders~~\nTymna the Weaver",
                    "wins": 1,
                    "losses": 0
                }
            ],
        }
        parsed = TopDeckProvider().parse(raw)
        self.assertEqual(parsed["decks"], ())

    def test_parse_live_structured_deck_event_success(self) -> None:
        raw = load_fixture("live_structured_deck_event.json")
        parsed = TopDeckProvider().parse(raw)
        event = parsed["events"][0]
        deck = parsed["decks"][0]

        self.assertEqual(event.provider_event_id, "dual-2")
        self.assertEqual(event.event_name, "Dual 2")
        self.assertEqual(event.format, "EDH")
        self.assertEqual(event.deck_count, 6)
        self.assertTrue(event.raw_payload.payload_hash.startswith("sha256:"))
        self.assertEqual(event.raw_payload.payload, raw)

        self.assertEqual(len(parsed["decks"]), 1)
        self.assertEqual(deck.provider_deck_id, "ZNEz6KlAZ0crALFMe1sCMyEtGL93")
        self.assertEqual(deck.pilot_name, "Jason Kroes")
        self.assertEqual(deck.commander_text, "Oskar, Rubbish Reclaimer")
        self.assertTrue(deck.raw_payload.payload_hash.startswith("sha256:"))
        self.assertEqual(deck.raw_payload.payload, raw["standings"][0])

    def test_parse_live_structured_deck_cards(self) -> None:
        deck = TopDeckProvider().parse(load_fixture("live_structured_deck_event.json"))["decks"][0]
        self.assertGreater(len(deck.cards), 50)
        self.assertTrue(all(isinstance(card, SourceDeckCardCandidate) for card in deck.cards))
        self.assertTrue(all(isinstance(card.quantity, int) for card in deck.cards))
        self.assertTrue(all(card.quantity > 0 for card in deck.cards))

        zones = {card.source_zone for card in deck.cards}
        quantities = {card.raw_name: card.quantity for card in deck.cards}
        self.assertIn("commanders", zones)
        self.assertIn("mainboard", zones)
        self.assertNotIn("metadata", zones)
        self.assertEqual(quantities["Oskar, Rubbish Reclaimer"], 1)
        self.assertEqual(quantities["An Offer You Can't Refuse"], 1)

    def test_live_structured_deck_fixture_skips_hidden_standings(self) -> None:
        raw = load_fixture("live_structured_deck_event.json")
        parsed = TopDeckProvider().parse(raw)

        self.assertEqual(len(raw["standings"]), 6)
        self.assertEqual(sum(1 for standing in raw["standings"] if standing.get("deckObj")), 1)
        self.assertEqual(len(parsed["decks"]), 1)
        self.assertNotIn("LYVKNk8mRqYPcZEAevwz2uyczXH3", {deck.provider_deck_id for deck in parsed["decks"]})

    def test_metadata_only_deck_obj_is_skipped_without_inventing_deck(self) -> None:
        raw = load_fixture("live_structured_deck_event.json")
        raw["standings"].append(
            {
                "id": "metadata-only",
                "name": "Metadata Only",
                "deckObj": {"metadata": {"format": "EDH", "importedFrom": "https://example.test/deck"}},
                "wins": 0,
                "losses": 0,
            }
        )
        parsed = TopDeckProvider().parse(raw)
        self.assertEqual(len(parsed["decks"]), 1)
        self.assertNotIn("metadata-only", {deck.provider_deck_id for deck in parsed["decks"]})

    def test_parse_event_missing_optional_fields(self) -> None:
        candidate = TopDeckProvider().parse_event(load_fixture("event_missing_optional.json"))
        self.assertEqual(candidate.provider_event_id, "12345")
        self.assertEqual(candidate.original_source, "TopDeck")
        self.assertIsNone(candidate.event_date)
        self.assertIsNone(candidate.player_count)

    def test_parse_event_malformed_and_missing_required(self) -> None:
        with self.assertRaises(ParseError):
            TopDeckProvider().parse_event(load_fixture("malformed_payload.json"))
        with self.assertRaises(ParseError):
            TopDeckProvider().parse_event(load_fixture("event_missing_required.json"))

    def test_parse_deck_success(self) -> None:
        decks = TopDeckProvider().parse_deck(load_fixture("deck_67890.json"), event_key="12345")
        self.assertEqual(len(decks), 1)
        deck = decks[0]
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider_deck_id, "67890")
        self.assertEqual(deck.source_event_key, "12345")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.rank, 1)
        self.assertEqual(len(deck.cards), 4)
        self.assertIsInstance(deck.cards[0], SourceDeckCardCandidate)
        self.assertEqual(deck.cards[2].raw_name, "Command Tower")
        self.assertEqual(deck.cards[2].source_zone, "mainboard")

    def test_parse_deck_missing_required(self) -> None:
        with self.assertRaises(ParseError):
            TopDeckProvider().parse_deck(load_fixture("deck_missing_required.json"), event_key="12345")

    def test_parse_deck_missing_optional_fields(self) -> None:
        deck = TopDeckProvider().parse_deck(load_fixture("deck_missing_optional.json"), event_key="12345")[0]
        self.assertEqual(deck.provider_deck_id, "67891")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.source_url, "https://topdeck.gg/deck/67891")
        self.assertIsNone(deck.download_url)
        self.assertIsNone(deck.deck_title)
        self.assertIsNone(deck.pilot_name)
        self.assertIsNone(deck.rank)
        self.assertIsNone(deck.record)
        self.assertIsNone(deck.win_rate)
        self.assertEqual(deck.cards[0].quantity, 1)
        self.assertEqual(deck.cards[0].source_zone, "mainboard")

    def test_fetch_network_error_and_rate_limit(self) -> None:
        network_client = TopDeckClient(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = TopDeckClient(
            transport=lambda url, headers, timeout: (429, "{}"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_event("12345")
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_event("12345")
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(topdeck_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                topdeck_client._urllib_transport("https://topdeck.example.test", {}, 0.1)
        self.assertTrue(error.exception.retryable)

    def test_urllib_transport_maps_timeout_to_network_error(self) -> None:
        with patch.object(topdeck_client, "urlopen", side_effect=TimeoutError("slow")):
            with self.assertRaises(NetworkError) as error:
                topdeck_client._urllib_transport("https://topdeck.example.test", {}, 0.1)
        self.assertTrue(error.exception.retryable)

    def test_topdeck_provider_fetch_and_parse_with_fixture_transport(self) -> None:
        def transport(url, headers, timeout):
            if url.endswith("/v2/tournaments/12345"):
                return 200, json.dumps(load_fixture("event_12345.json"))
            if url.endswith("/v2/tournaments/12345/players/67890"):
                return 200, json.dumps(load_fixture("deck_67890.json"))
            return 404, "{}"

        client = TopDeckClient(transport=transport, min_interval_seconds=0)
        provider = TopDeckProvider(client, event_id="12345", deck_ids=("12345:67890",))
        parsed = provider.parse(provider.fetch())
        self.assertEqual(parsed["events"][0].provider_event_id, "12345")
        self.assertEqual(parsed["decks"][0].provider_deck_id, "67890")

    def test_raw_payload_preservation_after_ingestion(self) -> None:
        connection = bootstrap_database()
        try:
            core = CoreRepository(connection)
            for scryfall_id, oracle_id, name, normalized in (
                ("tymna-card", "tymna-oracle", "Tymna the Weaver", "tymna the weaver"),
                ("kraum-card", "kraum-oracle", "Kraum, Ludevic's Opus", "kraum ludevics opus"),
                ("tower-card", "tower-oracle", "Command Tower", "command tower"),
                (
                    "bala-card",
                    "bala-oracle",
                    "Bala Ged Recovery // Bala Ged Sanctuary",
                    "bala ged recovery bala ged sanctuary",
                ),
            ):
                core.insert_card(
                    {
                        "scryfall_id": scryfall_id,
                        "oracle_id": oracle_id,
                        "name": name,
                        "normalized_name": normalized,
                        "raw_json": "{}",
                        "imported_at": NOW,
                    }
                )
            provider = TopDeckProvider()
            parsed = {
                "events": (provider.parse_event(load_fixture("event_12345.json")),),
                "decks": tuple(provider.parse_deck(load_fixture("deck_67890.json"), event_key="12345")),
            }

            class FixtureProvider(TopDeckProvider):
                def fetch(self):
                    return {}

                def parse(self, payload):
                    return parsed

            result = DeckIngestionPipeline(
                FixtureProvider(),
                SourceRepository(connection),
                CardLookup(core),
            ).run()
            self.assertEqual(result.status, "completed")
            deck_object = connection.execute(
                "SELECT * FROM provider_objects WHERE provider = ? AND object_type = ?",
                ("topdeck", "deck"),
            ).fetchone()
            self.assertIsNotNone(deck_object)
            self.assertTrue(deck_object["payload_hash"].startswith("sha256:"))
            self.assertIn("Tymna Kraum Example", deck_object["raw_payload_json"])
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
