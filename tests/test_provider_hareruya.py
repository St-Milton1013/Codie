from __future__ import annotations

from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.providers.errors import MissingRequiredFieldError, NetworkError, ParseError, RateLimitError
from codie.providers.hareruya import client as hareruya_client
from codie.providers.hareruya.client import HareruyaClient
from codie.providers.hareruya.parser import HareruyaProvider
from codie.providers.models import SourceDeckCandidate, SourceDeckCardCandidate, SourceEventCandidate


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "hareruya"


def load_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


class HareruyaProviderTest(unittest.TestCase):
    def test_parse_metagame_page_success(self) -> None:
        event = HareruyaProvider().parse_metagame_page(load_fixture("metagame_page_202.html"))
        self.assertIsInstance(event, SourceEventCandidate)
        self.assertEqual(event.provider, "hareruya")
        self.assertEqual(event.provider_event_id, "202")
        self.assertEqual(event.event_name, "Hareruya Fixture Commander Metagame")
        self.assertEqual(event.event_date, "2026-04-20")
        self.assertEqual(event.format, "Commander")
        self.assertEqual(event.country, "JP")
        self.assertEqual(event.region, "Tokyo")
        self.assertIsNone(event.player_count)
        self.assertEqual(event.deck_count, 12)
        self.assertEqual(event.source_url, "https://www.hareruyamtg.com/en/deck/202/metagame/")

    def test_parse_live_shape_commander_metagame_page(self) -> None:
        event = HareruyaProvider().parse_metagame_page(load_fixture("live_metagame_page_7.html"))
        self.assertIsInstance(event, SourceEventCandidate)
        self.assertEqual(event.provider_event_id, "7")
        self.assertEqual(event.event_name, "Commander Meta Game(2025/06/22～)")
        self.assertEqual(event.format, "Commander")
        self.assertEqual(event.country, "JP")
        self.assertEqual(event.region, "Japan")
        self.assertIsNone(event.event_date)
        self.assertEqual(event.deck_count, 221)
        self.assertEqual(event.source_url, "https://www.hareruyamtg.com/en/deck/7/metagame/")

    def test_parse_deck_page_success(self) -> None:
        deck = HareruyaProvider().parse_deck_page(load_fixture("deck_page_101.html"), event_key="202")
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider, "hareruya")
        self.assertEqual(deck.provider_deck_id, "101")
        self.assertEqual(deck.source_event_key, "202")
        self.assertEqual(deck.deck_title, "Hareruya Fixture Deck")
        self.assertEqual(deck.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(deck.pilot_name, "Fixture Pilot")
        self.assertEqual(deck.rank, 1)
        self.assertEqual(deck.rank_label, "1st Place")
        self.assertEqual(deck.record, "6-1")
        self.assertEqual(deck.source_url, "https://www.hareruyamtg.com/en/deck/101/show/")

    def test_parse_live_shape_deck_page_success(self) -> None:
        deck = HareruyaProvider().parse_deck_page(load_fixture("live_deck_page_100000.html"), event_key="7")
        self.assertIsInstance(deck, SourceDeckCandidate)
        self.assertEqual(deck.provider_deck_id, "100000")
        self.assertEqual(deck.source_event_key, "7")
        self.assertEqual(deck.deck_title, "Titan Valakut")
        self.assertEqual(deck.archetype_name, "Titan Valakut")
        self.assertEqual(deck.pilot_name, "GRACE LEGGE")
        self.assertEqual(deck.rank, 23)
        self.assertEqual(deck.rank_label, "23th")
        self.assertEqual(deck.source_url, "https://www.hareruyamtg.com/en/deck/100000/show/")
        self.assertEqual(deck.download_url, "https://www.hareruyamtg.com/en/deck/download?deck=100000")

    def test_deck_cards_parse_into_candidates_and_preserve_japanese_names(self) -> None:
        deck = HareruyaProvider().parse_deck_page(load_fixture("deck_page_101.html"), event_key="202")
        self.assertEqual(len(deck.cards), 6)
        self.assertTrue(all(isinstance(card, SourceDeckCardCandidate) for card in deck.cards))
        self.assertEqual(deck.cards[0].raw_name, "Tymna the Weaver")
        self.assertEqual(deck.cards[0].source_zone, "commanders")
        self.assertEqual(deck.cards[2].raw_name, "統率の塔")
        self.assertEqual(deck.cards[2].quantity, 1)
        self.assertEqual(deck.cards[2].source_zone, "mainboard")
        self.assertEqual(deck.cards[5].raw_name, "Silence")
        self.assertEqual(deck.cards[5].source_zone, "sideboard")

    def test_live_shape_deck_cards_parse_from_hareruya_sections(self) -> None:
        deck = HareruyaProvider().parse_deck_page(load_fixture("live_deck_page_100000.html"), event_key="7")
        self.assertEqual(len(deck.cards), 5)
        self.assertEqual(deck.cards[0].raw_name, "Cinder Glade")
        self.assertEqual(deck.cards[0].quantity, 3)
        self.assertEqual(deck.cards[0].source_zone, "mainboard")
        self.assertEqual(deck.cards[1].raw_name, "Mountain")
        self.assertEqual(deck.cards[1].quantity, 7)
        self.assertEqual(deck.cards[3].raw_name, "Lightning Bolt")
        self.assertEqual(deck.cards[4].raw_name, "Nature's Claim")
        self.assertEqual(deck.cards[4].source_zone, "sideboard")

    def test_commander_fallback_requires_commander_metadata(self) -> None:
        deck = HareruyaProvider().parse_deck_page(load_fixture("deck_page_fallback_commander.html"), event_key="202")
        self.assertEqual(deck.provider_deck_id, "102")
        self.assertEqual(deck.commander_text, "Najeela, the Blade-Blossom")

    def test_missing_optional_fields_are_allowed(self) -> None:
        deck = HareruyaProvider().parse_deck_page(load_fixture("deck_missing_optional.html"), event_key="202")
        self.assertEqual(deck.provider_deck_id, "103")
        self.assertIsNone(deck.commander_text)
        self.assertIsNone(deck.pilot_name)
        self.assertIsNone(deck.rank)
        self.assertIsNone(deck.record)
        self.assertEqual(len(deck.cards), 1)

    def test_missing_required_fields_fail_cleanly(self) -> None:
        provider = HareruyaProvider()
        with self.assertRaises(MissingRequiredFieldError):
            provider.parse_metagame_page(load_fixture("metagame_missing_required.html"))
        with self.assertRaises(MissingRequiredFieldError):
            provider.parse_deck_page(load_fixture("deck_missing_required.html"), event_key="202")

    def test_malformed_html_fails_cleanly(self) -> None:
        with self.assertRaises(ParseError):
            HareruyaProvider().parse_metagame_page(load_fixture("malformed_payload.html"))

    def test_hidden_unavailable_decklist_is_skipped(self) -> None:
        parsed = HareruyaProvider().parse(
            {
                "metagame_page": load_fixture("metagame_page_202.html"),
                "deck_pages": [
                    load_fixture("deck_page_101.html"),
                    load_fixture("deck_unavailable.html"),
                ],
            }
        )
        self.assertEqual(len(parsed["events"]), 1)
        self.assertEqual(len(parsed["decks"]), 1)
        self.assertEqual(parsed["decks"][0].provider_deck_id, "101")

    def test_raw_payload_hash_preserved(self) -> None:
        event_html = load_fixture("metagame_page_202.html")
        deck_html = load_fixture("deck_page_101.html")
        event = HareruyaProvider().parse_metagame_page(event_html)
        deck = HareruyaProvider().parse_deck_page(deck_html, event_key="202")
        self.assertEqual(event.raw_payload.payload, event_html)
        self.assertTrue(event.raw_payload.payload_hash.startswith("sha256:"))
        self.assertEqual(deck.raw_payload.payload, deck_html)
        self.assertTrue(deck.raw_payload.payload_hash.startswith("sha256:"))

    def test_client_fetch_success_with_fixture_transport(self) -> None:
        def transport(url, headers, timeout):
            if url.endswith("/en/deck/202/metagame/"):
                return 200, load_fixture("metagame_page_202.html")
            if url.endswith("/en/deck/101/show/"):
                return 200, load_fixture("deck_page_101.html")
            return 404, "missing"

        client = HareruyaClient(transport=transport, min_interval_seconds=0)
        provider = HareruyaProvider(
            client,
            metagame_url="https://www.hareruyamtg.com/en/deck/202/metagame/",
            deck_urls=("https://www.hareruyamtg.com/en/deck/101/show/",),
        )
        parsed = provider.parse(provider.fetch())
        self.assertEqual(parsed["events"][0].provider_event_id, "202")
        self.assertEqual(parsed["decks"][0].provider_deck_id, "101")

    def test_client_fetch_network_error_and_rate_limit(self) -> None:
        network_client = HareruyaClient(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = HareruyaClient(
            transport=lambda url, headers, timeout: (429, "slow down"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_metagame_page("https://hareruya.example/metagame")
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_metagame_page("https://hareruya.example/metagame")
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_client_maps_waf_challenge_to_retryable_rate_limit(self) -> None:
        waf_body = """
        <html><head><script>AwsWafIntegration.getToken()</script></head>
        <body><div id="challenge-container"></div></body></html>
        """
        client = HareruyaClient(transport=lambda url, headers, timeout: (202, waf_body), min_interval_seconds=0)
        with self.assertRaises(RateLimitError) as error:
            client.fetch_deck_page("https://www.hareruyamtg.com/en/deck/result?archetypeIds=3282")
        self.assertTrue(error.exception.retryable)

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(hareruya_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                hareruya_client._urllib_transport("https://hareruya.example.test/deck", {}, 0.1)
        self.assertTrue(error.exception.retryable)


if __name__ == "__main__":
    unittest.main()
