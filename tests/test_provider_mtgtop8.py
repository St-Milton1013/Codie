from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.providers.errors import MissingRequiredFieldError, NetworkError, ParseError, RateLimitError
from codie.providers.models import SourceDeckCandidate, SourceDeckCardCandidate, SourceEventCandidate
from codie.providers.mtgtop8 import client as mtgtop8_client
from codie.providers.mtgtop8.client import MTGTop8Client
from codie.providers.mtgtop8.parser import MTGTop8Provider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "mtgtop8"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


class MTGTop8ProviderTest(unittest.TestCase):
    def test_parse_event_page_success(self) -> None:
        event = MTGTop8Provider().parse_event_page(load_fixture("event_page_123.html"))
        self.assertIsInstance(event, SourceEventCandidate)
        self.assertEqual(event.provider, "mtgtop8")
        self.assertEqual(event.provider_event_id, "123")
        self.assertEqual(event.event_name, "MTGTop8 Fixture cEDH Challenge")
        self.assertEqual(event.event_date, "2026-03-30")
        self.assertEqual(event.format, "Commander")
        self.assertEqual(event.country, "US")
        self.assertEqual(event.region, "CA")
        self.assertEqual(event.player_count, 72)
        self.assertEqual(event.deck_count, 16)
        self.assertEqual(event.source_url, "https://www.mtgtop8.com/event?e=123&f=EDH")
        self.assertEqual(event.original_source_url, "https://www.mtgtop8.com/event?e=123&f=EDH")

    def test_parse_deck_page_success(self) -> None:
        deck = MTGTop8Provider().parse_deck_page(load_fixture("decklist_page_456.html"), event_key="123")
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider, "mtgtop8")
        self.assertEqual(deck.provider_deck_id, "456")
        self.assertEqual(deck.source_event_key, "123")
        self.assertEqual(deck.deck_title, "Tymna Kraum Control")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.pilot_name, "Fixture Pilot")
        self.assertEqual(deck.rank, 1)
        self.assertEqual(deck.rank_label, "1st Place")
        self.assertEqual(deck.record, "7-1")
        self.assertEqual(deck.source_url, "https://www.mtgtop8.com/event?e=123&d=456&f=EDH")

    def test_deck_cards_parse_into_candidates(self) -> None:
        deck = MTGTop8Provider().parse_deck_page(load_fixture("decklist_page_456.html"), event_key="123")
        self.assertEqual(len(deck.cards), 4)
        self.assertTrue(all(isinstance(card, SourceDeckCardCandidate) for card in deck.cards))
        self.assertEqual(deck.cards[0].raw_name, "Command Tower")
        self.assertEqual(deck.cards[0].quantity, 1)
        self.assertEqual(deck.cards[0].source_zone, "mainboard")
        self.assertEqual(deck.cards[3].raw_name, "Silence")
        self.assertEqual(deck.cards[3].source_zone, "sideboard")

    def test_missing_optional_fields_are_allowed(self) -> None:
        deck = MTGTop8Provider().parse_deck_page(load_fixture("decklist_missing_optional.html"), event_key="123")
        self.assertEqual(deck.provider_deck_id, "457")
        self.assertIsNone(deck.commander_text)
        self.assertIsNone(deck.pilot_name)
        self.assertIsNone(deck.rank)
        self.assertIsNone(deck.record)
        self.assertEqual(len(deck.cards), 1)

    def test_missing_required_fields_fail_cleanly(self) -> None:
        provider = MTGTop8Provider()
        with self.assertRaises(MissingRequiredFieldError):
            provider.parse_event_page(load_fixture("event_missing_required.html"))
        with self.assertRaises(MissingRequiredFieldError):
            provider.parse_deck_page(load_fixture("deck_missing_required.html"), event_key="123")

    def test_malformed_html_fails_cleanly(self) -> None:
        with self.assertRaises(ParseError):
            MTGTop8Provider().parse_event_page(load_fixture("malformed_payload.html"))

    def test_hidden_unavailable_decklist_is_skipped(self) -> None:
        parsed = MTGTop8Provider().parse(
            {
                "event_page": load_fixture("event_page_123.html"),
                "deck_pages": [
                    load_fixture("decklist_page_456.html"),
                    load_fixture("decklist_unavailable.html"),
                ],
            }
        )
        self.assertEqual(len(parsed["events"]), 1)
        self.assertEqual(len(parsed["decks"]), 1)
        self.assertEqual(parsed["decks"][0].provider_deck_id, "456")

    def test_raw_payload_hash_preserved(self) -> None:
        event_html = load_fixture("event_page_123.html")
        deck_html = load_fixture("decklist_page_456.html")
        event = MTGTop8Provider().parse_event_page(event_html)
        deck = MTGTop8Provider().parse_deck_page(deck_html, event_key="123")
        self.assertEqual(event.raw_payload.payload, event_html)
        self.assertTrue(event.raw_payload.payload_hash.startswith("sha256:"))
        self.assertEqual(deck.raw_payload.payload, deck_html)
        self.assertTrue(deck.raw_payload.payload_hash.startswith("sha256:"))

    def test_client_fetch_success_with_fixture_transport(self) -> None:
        def transport(url, headers, timeout):
            if url.endswith("event?e=123&f=EDH"):
                return 200, load_fixture("event_page_123.html")
            if url.endswith("event?e=123&d=456&f=EDH"):
                return 200, load_fixture("decklist_page_456.html")
            return 404, "missing"

        client = MTGTop8Client(transport=transport, min_interval_seconds=0)
        provider = MTGTop8Provider(
            client,
            event_url="https://www.mtgtop8.com/event?e=123&f=EDH",
            deck_urls=("https://www.mtgtop8.com/event?e=123&d=456&f=EDH",),
        )
        parsed = provider.parse(provider.fetch())
        self.assertEqual(parsed["events"][0].provider_event_id, "123")
        self.assertEqual(parsed["decks"][0].provider_deck_id, "456")

    def test_client_fetch_network_error_and_rate_limit(self) -> None:
        network_client = MTGTop8Client(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = MTGTop8Client(
            transport=lambda url, headers, timeout: (429, "slow down"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_event_page("https://www.mtgtop8.example/event")
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_event_page("https://www.mtgtop8.example/event")
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(mtgtop8_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                mtgtop8_client._urllib_transport("https://mtgtop8.example.test/event", {}, 0.1)
        self.assertTrue(error.exception.retryable)


if __name__ == "__main__":
    unittest.main()
