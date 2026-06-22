from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.providers.errors import MissingRequiredFieldError, NetworkError, ParseError, RateLimitError
from codie.providers.models import SourcePrimerCandidate
from codie.providers.moxfield import client as moxfield_client
from codie.providers.moxfield.client import MoxfieldClient
from codie.providers.moxfield.parser import MoxfieldProvider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "moxfield"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class MoxfieldProviderTest(unittest.TestCase):
    def test_parse_deck_with_primer_success(self) -> None:
        candidate = MoxfieldProvider().parse_deck(load_fixture("deck_with_primer.json"))
        self.assertIsInstance(candidate, SourcePrimerCandidate)
        self.assertEqual(candidate.provider, "moxfield")
        self.assertEqual(candidate.primer_url, "https://moxfield.com/decks/mox-primer-1/primer")
        self.assertEqual(candidate.deck_url, "https://moxfield.com/decks/mox-primer-1")
        self.assertEqual(candidate.commander_text, "Tymna the Weaver / Kraum, Ludevic's Opus")
        self.assertEqual(candidate.primer_title, "Tymna Kraum Primer")
        self.assertEqual(candidate.author, "PrimerAuthor")
        self.assertEqual(candidate.author_url, "https://moxfield.com/users/PrimerAuthor")
        self.assertEqual(candidate.likes, 42)
        self.assertEqual(candidate.views, 9001)
        self.assertEqual(candidate.comments, 7)
        self.assertEqual(candidate.objective_metadata["source_tags"], ["cEDH", "Competitive"])
        self.assertEqual(candidate.objective_metadata["has_primer_route"], 1)
        self.assertEqual(candidate.objective_metadata["primer_heading_count"], 6)

    def test_parse_returns_primer_collection(self) -> None:
        parsed = MoxfieldProvider().parse(load_fixture("deck_with_primer.json"))
        self.assertEqual(len(parsed["primers"]), 1)
        self.assertEqual(parsed["primers"][0].provider, "moxfield")

    def test_raw_metadata_sanitizes_primer_body(self) -> None:
        candidate = MoxfieldProvider().parse_deck(load_fixture("deck_with_primer.json"))
        raw_json = candidate.raw_payload.raw_payload_json
        self.assertTrue(candidate.raw_payload.payload_hash.startswith("sha256:"))
        self.assertNotIn("DO NOT STORE", raw_json)
        self.assertNotIn("description", raw_json)
        self.assertNotIn("body", raw_json)
        self.assertNotIn("sections", raw_json)

    def test_deck_without_primer_keeps_source_candidate_without_route_signal(self) -> None:
        candidate = MoxfieldProvider().parse_deck(load_fixture("deck_without_primer.json"))
        self.assertEqual(candidate.primer_url, "https://moxfield.com/decks/mox-no-primer")
        self.assertEqual(candidate.commander_text, "Najeela, the Blade-Blossom")
        self.assertEqual(candidate.objective_metadata["has_primer_route"], 0)
        self.assertEqual(candidate.objective_metadata["primer_content_present"], 0)

    def test_missing_required_identity_fails_cleanly(self) -> None:
        with self.assertRaises(MissingRequiredFieldError):
            MoxfieldProvider().parse_deck(load_fixture("missing_required.json"))

    def test_malformed_payload_fails_cleanly(self) -> None:
        with self.assertRaises(ParseError):
            MoxfieldProvider().parse_deck(load_fixture("malformed_payload.json"))

    def test_client_fetch_success_with_fixture_transport(self) -> None:
        payload = (FIXTURE_DIR / "deck_with_primer.json").read_text(encoding="utf-8")
        seen: dict[str, object] = {}

        def transport(url, headers, timeout):
            seen["url"] = url
            seen["headers"] = headers
            return 200, payload

        client = MoxfieldClient(transport=transport, min_interval_seconds=0)
        fetched = client.fetch_deck("mox-primer-1")
        self.assertEqual(fetched["publicId"], "mox-primer-1")
        self.assertEqual(seen["url"], "https://api.moxfield.com/v2/decks/all/mox-primer-1")
        self.assertEqual(seen["headers"]["Accept"], "application/json")

    def test_client_fetch_network_error_and_rate_limit(self) -> None:
        network_client = MoxfieldClient(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = MoxfieldClient(
            transport=lambda url, headers, timeout: (429, "{}"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_deck("offline")
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_deck("slow")
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_client_invalid_json_fails_cleanly(self) -> None:
        client = MoxfieldClient(transport=lambda url, headers, timeout: (200, "{"), min_interval_seconds=0)
        with self.assertRaises(ParseError):
            client.fetch_deck("bad-json")

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(moxfield_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                moxfield_client._urllib_transport("https://moxfield.example.test/decks/abc", {}, 0.1)
        self.assertTrue(error.exception.retryable)

    def test_provider_fetch_and_parse_with_fixture_transport(self) -> None:
        payload = (FIXTURE_DIR / "deck_with_primer.json").read_text(encoding="utf-8")
        client = MoxfieldClient(transport=lambda url, headers, timeout: (200, payload), min_interval_seconds=0)
        provider = MoxfieldProvider(client, deck_id="mox-primer-1")
        parsed = provider.parse(provider.fetch())
        self.assertEqual(parsed["primers"][0].primer_title, "Tymna Kraum Primer")


if __name__ == "__main__":
    unittest.main()
