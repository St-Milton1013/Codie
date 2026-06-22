from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.providers.edhtop16 import client as edhtop16_client
from codie.providers.edhtop16.client import EDHTop16Client
from codie.providers.edhtop16.parser import EDHTop16Provider
from codie.providers.errors import NetworkError, ParseError, RateLimitError
from codie.providers.models import SourceDeckCandidate, SourceDeckCardCandidate, SourceEventCandidate


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "edhtop16"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class EDHTop16ProviderTest(unittest.TestCase):
    def test_parse_event_success(self) -> None:
        provider = EDHTop16Provider()
        event = provider.parse_tournament(load_fixture("event_sample.json")["data"]["tournament"])
        self.assertIsInstance(event, SourceEventCandidate)
        self.assertEqual(event.provider, "edhtop16")
        self.assertEqual(event.provider_event_id, "edhtop16-fixture-open")
        self.assertEqual(event.event_name, "EDHTop16 Fixture Open")
        self.assertEqual(event.event_date, "2026-05-10T00:00:00.000Z")
        self.assertEqual(event.format, "EDH")
        self.assertEqual(event.player_count, 64)
        self.assertEqual(event.deck_count, 2)
        self.assertEqual(event.source_url, "https://topdeck.gg/bracket/edhtop16-fixture-open")
        self.assertTrue(event.raw_payload.payload_hash.startswith("sha256:"))

    def test_parse_tournament_with_visible_deck_and_hidden_entry(self) -> None:
        raw = load_fixture("event_sample.json")
        parsed = EDHTop16Provider().parse(raw)
        event = parsed["events"][0]
        deck = parsed["decks"][0]

        self.assertEqual(event.provider_event_id, "edhtop16-fixture-open")
        self.assertEqual(len(parsed["decks"]), 1)
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider_deck_id, "entry-1")
        self.assertEqual(deck.source_event_key, "edhtop16-fixture-open")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.pilot_name, "Fixture Pilot")
        self.assertEqual(deck.rank, 1)
        self.assertEqual(deck.record, "7-1-1")
        self.assertEqual(deck.download_url, "https://moxfield.com/decks/tymna-kraum-fixture")
        self.assertNotIn("hidden-entry", {candidate.provider_deck_id for candidate in parsed["decks"]})

    def test_parse_deck_success(self) -> None:
        raw = load_fixture("deck_sample.json")
        deck = EDHTop16Provider().parse(raw)["decks"][0]
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider_deck_id, "entry-standalone")
        self.assertEqual(deck.source_event_key, "edhtop16-fixture-open")
        self.assertEqual(deck.pilot_name, "Standalone Pilot")
        self.assertEqual(deck.rank, 4)
        self.assertEqual(deck.win_rate, 0.6666666667)
        self.assertEqual(deck.record, "4-2-0")
        self.assertEqual(len(deck.cards), 2)

    def test_deck_cards_parse_into_candidates(self) -> None:
        deck = EDHTop16Provider().parse(load_fixture("event_sample.json"))["decks"][0]
        self.assertEqual(len(deck.cards), 3)
        self.assertTrue(all(isinstance(card, SourceDeckCardCandidate) for card in deck.cards))
        self.assertEqual(deck.cards[0].raw_name, "Command Tower")
        self.assertEqual(deck.cards[0].quantity, 1)
        self.assertEqual(deck.cards[0].source_zone, "mainboard")
        self.assertEqual(deck.cards[2].raw_name, "Borne Upon a Wind")
        self.assertEqual(deck.cards[2].quantity, 1)

    def test_missing_optional_fields_are_allowed(self) -> None:
        parsed = EDHTop16Provider().parse(load_fixture("event_missing_optional.json"))
        event = parsed["events"][0]
        deck = parsed["decks"][0]
        self.assertEqual(event.provider_event_id, "edhtop16-minimal")
        self.assertEqual(event.source_url, "https://edhtop16.com/tournament/edhtop16-minimal")
        self.assertIsNone(event.event_date)
        self.assertIsNone(event.format)
        self.assertIsNone(event.player_count)
        self.assertEqual(deck.provider_deck_id, "minimal-entry")
        self.assertEqual(deck.commander_text, "Najeela, the Blade-Blossom")
        self.assertEqual(deck.cards, ())

    def test_missing_required_fields_fail_cleanly(self) -> None:
        provider = EDHTop16Provider()
        with self.assertRaises(ParseError):
            provider.parse(load_fixture("event_missing_required.json"))
        with self.assertRaises(ParseError):
            provider.parse(load_fixture("deck_missing_required.json"))

    def test_malformed_fixture_fails_cleanly(self) -> None:
        with self.assertRaises(ParseError):
            EDHTop16Provider().parse(load_fixture("malformed_payload.json"))

    def test_raw_payload_hash_preserved(self) -> None:
        raw = load_fixture("event_sample.json")
        parsed = EDHTop16Provider().parse(raw)
        event_payload = raw["data"]["tournament"]
        deck_payload = event_payload["entries"][0]
        self.assertEqual(parsed["events"][0].raw_payload.payload, event_payload)
        self.assertTrue(parsed["events"][0].raw_payload.payload_hash.startswith("sha256:"))
        self.assertEqual(parsed["decks"][0].raw_payload.payload, deck_payload)
        self.assertTrue(parsed["decks"][0].raw_payload.payload_hash.startswith("sha256:"))

    def test_client_fetch_tournaments_success_with_fixture_transport(self) -> None:
        seen: dict[str, object] = {}

        def transport(url, headers, timeout):
            seen["url"] = url
            seen["headers"] = headers
            seen["body"] = json.loads(headers["X-Codie-Body"])
            return 200, json.dumps(load_fixture("event_sample.json"))

        client = EDHTop16Client(transport=transport, min_interval_seconds=0)
        payload = client.fetch_tournaments({"minSize": 32}, first=1)
        self.assertIn("data", payload)
        self.assertEqual(seen["url"], "https://edhtop16.com/graphql")
        self.assertEqual(seen["body"]["variables"]["filters"], {"minSize": 32})
        self.assertEqual(seen["body"]["variables"]["first"], 1)

    def test_client_fetch_network_error_and_rate_limit(self) -> None:
        network_client = EDHTop16Client(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = EDHTop16Client(
            transport=lambda url, headers, timeout: (429, "{}"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_tournaments({})
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_tournaments({})
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_client_graphql_errors_without_data_fail_parse(self) -> None:
        client = EDHTop16Client(
            transport=lambda url, headers, timeout: (200, '{"errors":[{"message":"bad query"}]}'),
            min_interval_seconds=0,
        )
        with self.assertRaises(ParseError):
            client.fetch_tournaments({})

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(edhtop16_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                edhtop16_client._urllib_transport("https://edhtop16.example.test/graphql", {}, 0.1)
        self.assertTrue(error.exception.retryable)

    def test_edhtop16_provider_fetch_and_parse_with_fixture_transport(self) -> None:
        def transport(url, headers, timeout):
            body = json.loads(headers["X-Codie-Body"])
            if "CodieEDHTop16Tournaments" in body["query"]:
                return 200, json.dumps(load_fixture("event_sample.json"))
            if "CodieEDHTop16Decklist" in body["query"]:
                return 200, json.dumps(load_fixture("deck_sample.json"))
            return 400, "{}"

        client = EDHTop16Client(transport=transport, min_interval_seconds=0)
        provider = EDHTop16Provider(client, tournament_filters={"minSize": 32}, deck_ids=("entry-standalone",))
        parsed = provider.parse(provider.fetch())
        self.assertEqual(parsed["events"][0].provider_event_id, "edhtop16-fixture-open")
        self.assertEqual({deck.provider_deck_id for deck in parsed["decks"]}, {"entry-1", "entry-standalone"})


if __name__ == "__main__":
    unittest.main()
