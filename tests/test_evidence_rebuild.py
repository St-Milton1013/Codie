from __future__ import annotations

import json
from pathlib import Path
import unittest

from codie.cards.lookup import CardLookup
from codie.cards.normalization import normalize_card_name
from codie.combos import ComboEvidenceSync
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.curated import CuratedRepository
from codie.db.repositories.source import SourceRepository
from codie.primers import PrimerMetadataSync
from codie.providers.moxfield.parser import MoxfieldProvider
from codie.providers.spellbook.parser import SpellbookProvider


ROOT = Path(__file__).resolve().parents[1]
SPELLBOOK_FIXTURES = ROOT / "tests" / "fixtures" / "spellbook"
MOXFIELD_FIXTURES = ROOT / "tests" / "fixtures" / "moxfield"
NOW = "2026-06-21T00:00:00+00:00"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class EvidenceRebuildTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.curated = CuratedRepository(self.connection)
        self.canonical = CanonicalRepository(self.connection)
        self.analytics = AnalyticsRepository(self.connection)
        self._insert_card("thassa-oracle", "oracle-thassa", "Thassa's Oracle")
        self._insert_card("demonic-consultation", "oracle-consultation", "Demonic Consultation")
        self.lookup = CardLookup(self.core, curated_repository=self.curated)

    def _insert_card(self, scryfall_id: str, oracle_id: str, name: str) -> None:
        self.core.insert_card(
            {
                "scryfall_id": scryfall_id,
                "oracle_id": oracle_id,
                "name": name,
                "normalized_name": normalize_card_name(name),
                "raw_json": "{}",
                "imported_at": NOW,
            }
        )

    def _seed_canonical_tournament_evidence(self) -> None:
        event_id = self.canonical.create_event(
            {
                "event_name": "Fixture Open",
                "normalized_event_name": "fixture open",
                "event_date": "2026-06-21",
                "format": "commander",
                "dedupe_key": "fixture-open-2026",
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
        deck_id = self.canonical.create_deck(
            {
                "deck_hash": "deck-hash-1",
                "commander_hash": "tymna|kraum",
                "card_count": 1,
                "commander_count": 2,
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
        self.canonical.add_deck_card(
            {
                "canonical_deck_id": deck_id,
                "scryfall_id": "thassa-oracle",
                "oracle_id": "oracle-thassa",
                "quantity": 1,
                "zone": "mainboard",
            }
        )
        self.canonical.create_event_deck_entry(
            {
                "canonical_event_id": event_id,
                "canonical_deck_id": deck_id,
                "pilot_name": "Fixture Pilot",
                "placement": 1,
                "created_at": NOW,
            }
        )

    def test_rebuild_evidence_counts_from_canonical_and_curated_records(self) -> None:
        self._seed_canonical_tournament_evidence()
        combos = SpellbookProvider().parse_variants(load_json(SPELLBOOK_FIXTURES / "variants_sample.json"))
        ComboEvidenceSync(self.source, self.curated, self.analytics, self.lookup).sync_candidates(combos)
        primer = MoxfieldProvider().parse_deck(load_json(MOXFIELD_FIXTURES / "deck_with_primer.json"))
        PrimerMetadataSync(self.source, self.curated, self.analytics).sync_candidates((primer,))
        self.analytics.upsert_evidence_count(
            {
                "entity_type": "bogus",
                "entity_id": "stale-row",
                "combo_evidence_count": 99,
                "updated_at": NOW,
            }
        )

        rebuilt_count = self.analytics.rebuild_evidence_counts(updated_at="2026-06-22T00:00:00+00:00")

        self.assertEqual(rebuilt_count, 5)
        self.assertIsNone(self.analytics.get_evidence_count("bogus", "stale-row"))
        thassa = self.analytics.get_evidence_count("card", "oracle-thassa")
        self.assertEqual(thassa["tournament_evidence_count"], 1)
        self.assertEqual(thassa["combo_evidence_count"], 2)
        consultation = self.analytics.get_evidence_count("card", "oracle-consultation")
        self.assertEqual(consultation["combo_evidence_count"], 1)
        combo = self.analytics.get_evidence_count("combo", "spellbook-1")
        self.assertEqual(combo["combo_evidence_count"], 2)
        primer_evidence = self.analytics.get_evidence_count(
            "primer",
            "https://moxfield.com/decks/mox-primer-1/primer",
        )
        self.assertEqual(primer_evidence["primer_evidence_count"], 1)


if __name__ == "__main__":
    unittest.main()
