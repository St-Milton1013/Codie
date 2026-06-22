from __future__ import annotations

import json
from pathlib import Path
import unittest

from codie.canonical.canonicalizer import Canonicalizer
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.source import SourceRepository
from codie.db.repositories.validation import ValidationRepository
from codie.validation import build_canonical_coverage_report


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "canonicalization"
NOW = "2026-06-21T00:00:00+00:00"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class CanonicalCoverageReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.canonical = CanonicalRepository(self.connection)
        self.validation = ValidationRepository(self.connection)
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

    def create_source_event(self, payload: dict) -> int:
        data = dict(payload)
        data.setdefault("imported_at", NOW)
        return self.source.create_source_event(data)

    def create_source_deck(self, deck: dict) -> int:
        source_deck_id = self.source.create_source_deck(
            {
                "provider": deck["provider"],
                "provider_deck_id": deck["provider_deck_id"],
                "source_url": f"https://example.test/{deck['provider_deck_id']}",
                "deck_title": deck["provider_deck_id"],
                "commander_text": deck.get("commander_text"),
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

    def test_canonical_coverage_report_shows_dedupe_merge_and_unresolved_rates(self) -> None:
        event_case = load_fixture("event_dedupe_cases.json")["cases"][0]
        for event in event_case["source_events"]:
            self.canonicalizer.canonicalize_event(self.create_source_event(event))
        deck_case = self.deck_cases["cases"][0]
        for deck in deck_case["decks"]:
            self.canonicalizer.canonicalize_deck(self.create_source_deck(deck))
        unresolved_deck = next(
            case for case in self.deck_cases["cases"] if case["id"] == "unresolved_card_blocks_canonicalization"
        )["deck"]
        self.create_source_deck(unresolved_deck)

        report = build_canonical_coverage_report(self.validation)

        self.assertEqual(report.source_event_count, 2)
        self.assertEqual(report.canonical_event_count, 1)
        self.assertEqual(report.canonicalized_source_event_count, 2)
        self.assertEqual(report.canonical_event_source_link_count, 2)
        self.assertEqual(report.event_canonicalization_rate, 1.0)
        self.assertEqual(report.event_merge_rate, 0.5)
        self.assertEqual(report.source_deck_count, 3)
        self.assertEqual(report.canonical_deck_count, 1)
        self.assertEqual(report.canonicalized_source_deck_count, 2)
        self.assertEqual(report.canonical_deck_source_link_count, 2)
        self.assertEqual(report.deck_merge_rate, 0.5)
        self.assertEqual(report.unresolved_source_deck_count, 1)
        self.assertAlmostEqual(report.unresolved_deck_rate, 1 / 3)


if __name__ == "__main__":
    unittest.main()
