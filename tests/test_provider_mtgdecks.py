from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.providers.errors import MissingRequiredFieldError, NetworkError, ParseError, RateLimitError
from codie.providers.models import SourceDeckCandidate, SourceDeckCardCandidate, SourceEventCandidate
from codie.providers.mtgdecks import client as mtgdecks_client
from codie.providers.mtgdecks.client import MTGDecksClient
from codie.providers.mtgdecks.parser import MTGDecksProvider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "mtgdecks"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


class MTGDecksProviderTest(unittest.TestCase):
    def test_parse_event_page_success(self) -> None:
        event = MTGDecksProvider().parse_event_page(load_fixture("event_page_789.html"))
        self.assertIsInstance(event, SourceEventCandidate)
        self.assertEqual(event.provider, "mtgdecks")
        self.assertEqual(event.provider_event_id, "789")
        self.assertEqual(event.event_name, "MTGDecks Fixture Commander Open")
        self.assertEqual(event.event_date, "2026-04-12")
        self.assertEqual(event.format, "Commander")
        self.assertEqual(event.country, "ES")
        self.assertEqual(event.region, "Madrid")
        self.assertEqual(event.player_count, 48)
        self.assertEqual(event.deck_count, 8)
        self.assertEqual(event.source_url, "https://mtgdecks.net/events/mtgdecks-fixture-commander-open-789")
        self.assertEqual(event.original_source_url, "https://mtgdecks.net/events/mtgdecks-fixture-commander-open-789")

    def test_parse_deck_page_success(self) -> None:
        deck = MTGDecksProvider().parse_deck_page(load_fixture("deck_export.txt"), event_key="789")
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider, "mtgdecks")
        self.assertEqual(deck.provider_deck_id, "456")
        self.assertEqual(deck.source_event_key, "789")
        self.assertEqual(deck.deck_title, "Tymna Kraum Control")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.pilot_name, "Fixture Pilot")
        self.assertEqual(deck.rank, 1)
        self.assertEqual(deck.rank_label, "1st Place")
        self.assertEqual(deck.record, "7-1")
        self.assertEqual(deck.archetype_name, "Blue Farm")
        self.assertEqual(deck.source_url, "https://mtgdecks.net/Commander/tymna-kraum-control-decklist-by-fixture-pilot-456")

    def test_deck_cards_parse_into_candidates(self) -> None:
        deck = MTGDecksProvider().parse_deck_page(load_fixture("deck_export.txt"), event_key="789")
        self.assertEqual(len(deck.cards), 7)
        self.assertTrue(all(isinstance(card, SourceDeckCardCandidate) for card in deck.cards))
        self.assertEqual(deck.cards[0].raw_name, "Tymna the Weaver")
        self.assertEqual(deck.cards[0].source_zone, "commanders")
        self.assertEqual(deck.cards[2].raw_name, "Command Tower")
        self.assertEqual(deck.cards[2].quantity, 1)
        self.assertEqual(deck.cards[2].source_zone, "mainboard")
        self.assertEqual(deck.cards[5].raw_name, "Silence")
        self.assertEqual(deck.cards[5].source_zone, "sideboard")
        self.assertEqual(deck.cards[6].raw_name, "Sticker Sheet")
        self.assertEqual(deck.cards[6].source_zone, "auxiliary")

    def test_missing_optional_fields_are_allowed(self) -> None:
        deck = MTGDecksProvider().parse_deck_page(load_fixture("deck_missing_optional.txt"), event_key="789")
        self.assertEqual(deck.provider_deck_id, "457")
        self.assertIsNone(deck.commander_text)
        self.assertIsNone(deck.pilot_name)
        self.assertIsNone(deck.rank)
        self.assertIsNone(deck.record)
        self.assertEqual(len(deck.cards), 1)

    def test_missing_required_fields_fail_cleanly(self) -> None:
        provider = MTGDecksProvider()
        with self.assertRaises(MissingRequiredFieldError):
            provider.parse_event_page(load_fixture("event_missing_required.html"))
        with self.assertRaises(MissingRequiredFieldError):
            provider.parse_deck_page(load_fixture("deck_missing_required.txt"), event_key="789")

    def test_malformed_text_fails_cleanly(self) -> None:
        with self.assertRaises(ParseError):
            MTGDecksProvider().parse_deck_page(load_fixture("malformed_payload.txt"), event_key="789")

    def test_hidden_unavailable_decklist_is_skipped(self) -> None:
        parsed = MTGDecksProvider().parse(
            {
                "event_page": load_fixture("event_page_789.html"),
                "deck_pages": [
                    load_fixture("deck_export.txt"),
                    load_fixture("deck_unavailable.txt"),
                ],
            }
        )
        self.assertEqual(len(parsed["events"]), 1)
        self.assertEqual(len(parsed["decks"]), 1)
        self.assertEqual(parsed["decks"][0].provider_deck_id, "456")

    def test_raw_payload_hash_preserved(self) -> None:
        event_html = load_fixture("event_page_789.html")
        deck_text = load_fixture("deck_export.txt")
        event = MTGDecksProvider().parse_event_page(event_html)
        deck = MTGDecksProvider().parse_deck_page(deck_text, event_key="789")
        self.assertEqual(event.raw_payload.payload, event_html)
        self.assertTrue(event.raw_payload.payload_hash.startswith("sha256:"))
        self.assertEqual(deck.raw_payload.payload, deck_text)
        self.assertTrue(deck.raw_payload.payload_hash.startswith("sha256:"))

    def test_client_fetch_success_with_fixture_transport(self) -> None:
        def transport(url, headers, timeout):
            if url.endswith("/events/mtgdecks-fixture-commander-open-789"):
                return 200, load_fixture("event_page_789.html")
            if url.endswith("/Commander/tymna-kraum-control-decklist-by-fixture-pilot-456"):
                return 200, load_fixture("deck_export.txt")
            return 404, "missing"

        client = MTGDecksClient(transport=transport, min_interval_seconds=0)
        provider = MTGDecksProvider(
            client,
            event_url="https://mtgdecks.net/events/mtgdecks-fixture-commander-open-789",
            deck_urls=("https://mtgdecks.net/Commander/tymna-kraum-control-decklist-by-fixture-pilot-456",),
        )
        parsed = provider.parse(provider.fetch())
        self.assertEqual(parsed["events"][0].provider_event_id, "789")
        self.assertEqual(parsed["decks"][0].provider_deck_id, "456")

    def test_client_fetch_network_error_and_rate_limit(self) -> None:
        network_client = MTGDecksClient(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = MTGDecksClient(
            transport=lambda url, headers, timeout: (429, "slow down"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_event_page("https://mtgdecks.example/events/1")
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_event_page("https://mtgdecks.example/events/1")
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(mtgdecks_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                mtgdecks_client._urllib_transport("https://mtgdecks.example.test/event", {}, 0.1)
        self.assertTrue(error.exception.retryable)


if __name__ == "__main__":
    unittest.main()
