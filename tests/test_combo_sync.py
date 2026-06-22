from __future__ import annotations

import json
from pathlib import Path
import unittest

from codie.cards.lookup import CardLookup
from codie.cards.normalization import normalize_card_name
from codie.combos import ComboEvidenceSync
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.curated import CuratedRepository
from codie.db.repositories.source import SourceRepository
from codie.providers.spellbook.parser import SpellbookProvider


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "spellbook"
NOW = "2026-06-21T00:00:00+00:00"


def load_fixture(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class ComboEvidenceSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.curated = CuratedRepository(self.connection)
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

    def _sync(self):
        candidates = SpellbookProvider().parse_variants(load_fixture("variants_sample.json"))
        return ComboEvidenceSync(self.source, self.curated, self.analytics, self.lookup).sync_candidates(candidates)

    def test_sync_persists_source_combos_and_curated_combos(self) -> None:
        result = self._sync()
        self.assertEqual(result.source_combo_count, 2)
        self.assertEqual(result.combo_count, 2)
        combo = self.curated.get_combo("commander_spellbook", "spellbook-1")
        self.assertEqual(combo["combo_url"], "https://commanderspellbook.com/combo/spellbook-1/")
        self.assertEqual(combo["combo_name"], "Thassa's Oracle + Demonic Consultation")
        source_combo = self.source.get_source_combo("commander_spellbook", "spellbook-1")
        self.assertEqual(source_combo["combo_name"], "Thassa's Oracle + Demonic Consultation")
        self.assertIn("Thassa's Oracle", source_combo["components_json"])
        self.assertIn("Win the game", source_combo["outputs_json"])

    def test_sync_persists_resolved_and_unresolved_combo_cards(self) -> None:
        result = self._sync()
        self.assertEqual(result.combo_card_count, 4)
        self.assertEqual(result.resolved_card_count, 3)
        self.assertEqual(result.unresolved_card_count, 1)

        combo = self.curated.get_combo("commander_spellbook", "spellbook-2")
        cards = self.curated.list_combo_cards(combo["combo_id"])
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["card_name"], "Thassa's Oracle")
        self.assertEqual(cards[0]["scryfall_id"], "thassa-oracle")
        self.assertEqual(cards[0]["oracle_id"], "oracle-thassa")
        self.assertEqual(cards[1]["card_name"], "Card Not In Local Cache")
        self.assertIsNone(cards[1]["scryfall_id"])
        self.assertIsNone(cards[1]["oracle_id"])

    def test_sync_updates_combo_evidence_counts(self) -> None:
        result = self._sync()
        self.assertEqual(result.evidence_count_count, 4)
        card_evidence = self.analytics.get_evidence_count("card", "oracle-thassa")
        self.assertEqual(card_evidence["combo_evidence_count"], 2)
        combo_evidence = self.analytics.get_evidence_count("combo", "spellbook-1")
        self.assertEqual(combo_evidence["combo_evidence_count"], 2)

    def test_sync_is_idempotent_for_combo_and_combo_cards(self) -> None:
        first = self._sync()
        second = self._sync()
        self.assertEqual(first.combo_count, 2)
        self.assertEqual(second.combo_count, 2)
        combo = self.curated.get_combo("commander_spellbook", "spellbook-1")
        cards = self.curated.list_combo_cards(combo["combo_id"])
        self.assertEqual(len(cards), 2)
        combo_rows = self.connection.execute(
            """
            SELECT COUNT(*) AS count FROM combos
            WHERE provider = 'commander_spellbook' AND provider_combo_id = 'spellbook-1'
            """
        ).fetchone()
        self.assertEqual(combo_rows["count"], 1)

    def test_sync_does_not_create_recommendations_or_packages(self) -> None:
        self._sync()
        recommendation_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        package_count = self.connection.execute("SELECT COUNT(*) AS count FROM package_registry").fetchone()
        self.assertEqual(recommendation_count["count"], 0)
        self.assertEqual(package_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
