from __future__ import annotations

import json
from pathlib import Path
import unittest

from codie.cards.importer import ScryfallImporter
from codie.cards.lookup import CardLookup
from codie.cards.normalization import normalize_card_name
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.curated import CuratedRepository
from codie.db.repositories.core import CoreRepository
from codie.providers.scryfall.bulk import load_bulk_cards
from codie.providers.scryfall.models import ScryfallParseError


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "scryfall"


class ScryfallTruthTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.repo = CoreRepository(self.connection)
        self.imported_at = "2026-06-21T00:00:00+00:00"

    def tearDown(self) -> None:
        self.connection.close()

    def import_fixture(self) -> None:
        cards = load_bulk_cards(FIXTURE_DIR / "bulk_cards.json", imported_at=self.imported_at)
        count = ScryfallImporter(self.repo).import_cards(cards)
        self.assertEqual(count, 4)

    def test_loads_bulk_fixture_and_persists_scryfall_truth(self) -> None:
        self.import_fixture()
        tymna = self.repo.get_card("00000000-0000-0000-0000-000000000001")
        self.assertEqual(tymna["oracle_id"], "11111111-1111-1111-1111-111111111111")
        self.assertEqual(tymna["normalized_name"], "tymna the weaver")
        self.assertEqual(tymna["is_legal_commander"], 1)
        self.assertEqual(tymna["is_commander_candidate"], 1)
        self.assertEqual(json.loads(tymna["raw_json"])["name"], "Tymna the Weaver")

    def test_resolves_exact_alias_and_local_fuzzy_names(self) -> None:
        self.import_fixture()
        lookup = CardLookup(self.repo, aliases={"Bob": "Tymna the Weaver"})
        exact = lookup.resolve("Tymna the Weaver")
        alias = lookup.resolve("Bob")
        fuzzy = lookup.resolve("Kram Ludevics Opus")
        self.assertEqual(exact.status, "exact")
        self.assertEqual(alias.status, "alias")
        self.assertEqual(alias.card["name"], "Tymna the Weaver")
        self.assertEqual(fuzzy.status, "fuzzy")
        self.assertEqual(fuzzy.card["name"], "Kraum, Ludevic's Opus")

    def test_resolves_alias_from_curated_alias_registry(self) -> None:
        self.import_fixture()
        curated = CuratedRepository(self.connection)
        curated.create_alias(
            {
                "alias": "The Partner Cleric",
                "normalized_alias": "the partner cleric",
                "target_type": "card",
                "target_scryfall_id": "00000000-0000-0000-0000-000000000001",
                "target_oracle_id": "11111111-1111-1111-1111-111111111111",
                "target_name": "Tymna the Weaver",
                "normalized_target_name": "tymna the weaver",
                "source": "fixture",
                "created_at": self.imported_at,
                "updated_at": self.imported_at,
            }
        )
        result = CardLookup(self.repo, curated_repository=curated).resolve("The Partner Cleric")
        self.assertEqual(result.status, "alias")
        self.assertEqual(result.card["name"], "Tymna the Weaver")

    def test_handles_mdfc_card_faces_and_produced_mana(self) -> None:
        self.import_fixture()
        mdfc = self.repo.get_card("00000000-0000-0000-0000-000000000003")
        command_tower = self.repo.get_card("00000000-0000-0000-0000-000000000004")
        self.assertEqual(mdfc["layout"], "modal_dfc")
        self.assertEqual(json.loads(mdfc["produced_mana_json"]), ["G"])
        self.assertEqual(json.loads(command_tower["produced_mana_json"]), ["B", "G", "R", "U", "W"])
        self.assertEqual(json.loads(mdfc["card_faces_json"])[1]["name"], "Bala Ged Sanctuary")

    def test_upsert_refreshes_existing_card(self) -> None:
        cards = load_bulk_cards(FIXTURE_DIR / "bulk_cards.json", imported_at=self.imported_at)
        ScryfallImporter(self.repo).import_cards(cards)
        changed = cards[0].to_card_row()
        changed["name"] = "Tymna the Weaver Updated"
        self.repo.upsert_card(changed)
        self.assertEqual(self.repo.get_card(cards[0].scryfall_id)["name"], "Tymna the Weaver Updated")

    def test_fails_cleanly_on_malformed_and_missing_required_payloads(self) -> None:
        with self.assertRaises(ScryfallParseError):
            load_bulk_cards(FIXTURE_DIR / "malformed.json", imported_at=self.imported_at)
        with self.assertRaises(ScryfallParseError):
            load_bulk_cards(FIXTURE_DIR / "missing_required.json", imported_at=self.imported_at)

    def test_missing_optional_scryfall_fields_are_allowed(self) -> None:
        cards = load_bulk_cards(FIXTURE_DIR / "missing_optional.json", imported_at=self.imported_at)
        self.assertEqual(cards[0].name, "Minimal Fixture Card")
        self.assertIsNone(cards[0].oracle_id)
        self.assertIsNone(cards[0].legalities_json)
        ScryfallImporter(self.repo).import_cards(cards)
        stored = self.repo.get_card("00000000-0000-0000-0000-000000000099")
        self.assertEqual(stored["normalized_name"], "minimal fixture card")

    def test_unresolved_lookup_and_name_normalization(self) -> None:
        self.import_fixture()
        lookup = CardLookup(self.repo)
        unresolved = lookup.resolve("")
        missing = lookup.resolve("Xqzv Unmatchable Token")
        self.assertEqual(unresolved.status, "unresolved")
        self.assertEqual(missing.status, "unresolved")
        self.assertLess(missing.score, 0.74)
        self.assertEqual(normalize_card_name("Kraum, Ludevic's Opus"), "kraum ludevics opus")


if __name__ == "__main__":
    unittest.main()
