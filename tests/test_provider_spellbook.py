from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.error import URLError

from codie.providers.errors import MissingRequiredFieldError, NetworkError, ParseError, RateLimitError
from codie.providers.models import SourceComboCandidate, SourceComboCardCandidate
from codie.providers.spellbook import client as spellbook_client
from codie.providers.spellbook.client import SpellbookClient
from codie.providers.spellbook.parser import SpellbookProvider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "spellbook"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class SpellbookProviderTest(unittest.TestCase):
    def test_parse_variants_success(self) -> None:
        combos = SpellbookProvider().parse_variants(load_fixture("variants_sample.json"))
        self.assertEqual(len(combos), 2)
        combo = combos[0]
        self.assertIsInstance(combo, SourceComboCandidate)
        self.assertEqual(combo.provider, "commander_spellbook")
        self.assertEqual(combo.provider_combo_id, "spellbook-1")
        self.assertEqual(combo.combo_url, "https://commanderspellbook.com/combo/spellbook-1/")
        self.assertEqual(combo.combo_name, "Thassa's Oracle + Demonic Consultation")
        self.assertEqual(combo.components, ("Thassa's Oracle", "Demonic Consultation"))
        self.assertEqual(combo.outputs, ("Win the game",))

    def test_combo_components_parse_into_card_candidates(self) -> None:
        combo = SpellbookProvider().parse_variants(load_fixture("variants_sample.json"))[0]
        self.assertTrue(all(isinstance(card, SourceComboCardCandidate) for card in combo.cards))
        self.assertEqual(combo.cards[0].raw_name, "Thassa's Oracle")
        self.assertEqual(combo.cards[0].role, "win_condition")
        self.assertTrue(combo.cards[0].required)
        self.assertEqual(combo.cards[1].raw_name, "Demonic Consultation")
        self.assertEqual(combo.cards[1].role, "enabler")

    def test_missing_optional_fields_are_allowed(self) -> None:
        combo = SpellbookProvider().parse_variants(load_fixture("missing_optional.json"))[0]
        self.assertEqual(combo.provider_combo_id, "spellbook-optional")
        self.assertEqual(combo.combo_url, "https://commanderspellbook.com/combo/spellbook-optional/")
        self.assertIsNone(combo.combo_name)
        self.assertEqual(combo.components, ("Thassa's Oracle",))
        self.assertEqual(combo.outputs, ())

    def test_missing_required_fields_fail_cleanly(self) -> None:
        with self.assertRaises(MissingRequiredFieldError):
            SpellbookProvider().parse_variants(load_fixture("missing_required.json"))

    def test_malformed_payload_fails_cleanly(self) -> None:
        with self.assertRaises(ParseError):
            SpellbookProvider().parse_variants(load_fixture("malformed_payload.json"))

    def test_raw_payload_hash_preserved(self) -> None:
        raw = load_fixture("variants_sample.json")
        combo = SpellbookProvider().parse_variants(raw)[0]
        self.assertEqual(combo.raw_payload.payload, raw["results"][0])
        self.assertTrue(combo.raw_payload.payload_hash.startswith("sha256:"))

    def test_client_fetch_success_with_fixture_transport(self) -> None:
        payload = (FIXTURE_DIR / "variants_sample.json").read_text(encoding="utf-8")
        client = SpellbookClient(transport=lambda url, headers, timeout: (200, payload), min_interval_seconds=0)
        parsed = SpellbookProvider(client).parse(SpellbookProvider(client).fetch())
        self.assertEqual(len(parsed["combos"]), 2)

    def test_client_fetch_network_error_and_rate_limit(self) -> None:
        network_client = SpellbookClient(
            transport=lambda url, headers, timeout: (_ for _ in ()).throw(NetworkError("offline")),
            min_interval_seconds=0,
        )
        rate_client = SpellbookClient(
            transport=lambda url, headers, timeout: (429, "slow down"),
            min_interval_seconds=0,
        )
        with self.assertRaises(NetworkError) as network:
            network_client.fetch_variants()
        with self.assertRaises(RateLimitError) as rate_limit:
            rate_client.fetch_variants()
        self.assertTrue(network.exception.retryable)
        self.assertTrue(rate_limit.exception.retryable)

    def test_client_invalid_json_fails_cleanly(self) -> None:
        client = SpellbookClient(transport=lambda url, headers, timeout: (200, "{"), min_interval_seconds=0)
        with self.assertRaises(ParseError):
            client.fetch_variants()

    def test_urllib_transport_maps_urlerror_to_network_error(self) -> None:
        with patch.object(spellbook_client, "urlopen", side_effect=URLError("offline")):
            with self.assertRaises(NetworkError) as error:
                spellbook_client._urllib_transport("https://spellbook.example.test/variants", {}, 0.1)
        self.assertTrue(error.exception.retryable)


if __name__ == "__main__":
    unittest.main()
