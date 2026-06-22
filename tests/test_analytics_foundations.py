from __future__ import annotations

import ast
import json
from math import isclose, log2
from pathlib import Path
import unittest

from codie.analytics import (
    AnalyticsError,
    AnalyticsFoundationBuilder,
    event_size_weight,
    placement_weight,
    normalize_time_window,
    recency_weight,
)
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.regional import RegionalRepository


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "analytics"
NOW = "2026-06-21T00:00:00+00:00"


def load_case() -> dict:
    return json.loads((FIXTURE_DIR / "foundation_cases.json").read_text(encoding="utf-8"))


def imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
    return imports


class AnalyticsWeightingTest(unittest.TestCase):
    def test_event_size_weight_follows_constitution_formula(self) -> None:
        self.assertTrue(isclose(event_size_weight(64), log2(64) / log2(128)))
        self.assertEqual(event_size_weight(None), 0.0)
        self.assertEqual(event_size_weight(8), 0.0)

    def test_placement_weight_exact_and_fallback_rules(self) -> None:
        self.assertEqual(placement_weight(1), 1.0)
        self.assertEqual(placement_weight(2), 0.90)
        self.assertEqual(placement_weight(4), 0.80)
        self.assertEqual(placement_weight(16), 0.60)
        self.assertEqual(placement_weight(17), 0.30)
        self.assertEqual(placement_weight(None, "Top 4"), 0.80)
        self.assertEqual(placement_weight(None, "Top 16"), 0.60)
        self.assertEqual(placement_weight(None, "Participant"), 0.30)

    def test_recency_weight_uses_window_half_life(self) -> None:
        self.assertTrue(isclose(recency_weight("2026-05-22", "2026-06-21", "30d"), 0.5))
        self.assertTrue(isclose(recency_weight("2026-04-22", "2026-06-21", "90d"), 0.5))
        self.assertEqual(normalize_time_window("90-day"), "90d")
        self.assertEqual(recency_weight(None, "2026-06-21", "all_time"), 1.0)
        with self.assertRaises(AnalyticsError):
            recency_weight("2026-06-01", "2026-06-21", "13d")


class AnalyticsFoundationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.core = CoreRepository(self.connection)
        self.canonical = CanonicalRepository(self.connection)
        self.analytics = AnalyticsRepository(self.connection)
        self.regional = RegionalRepository(self.connection)
        self.case = load_case()
        self.event_ids: list[int] = []
        self.deck_ids: list[int] = []
        self._seed_case()

    def _seed_case(self) -> None:
        cards = {card["scryfall_id"]: card for card in self.case["cards"]}
        for card in self.case["cards"]:
            self.core.insert_card(
                {
                    "scryfall_id": card["scryfall_id"],
                    "oracle_id": card["oracle_id"],
                    "name": card["name"],
                    "normalized_name": card["name"].lower(),
                    "raw_json": json.dumps(card, sort_keys=True),
                    "imported_at": NOW,
                }
            )

        for event in self.case["events"]:
            payload = dict(event)
            payload["created_at"] = NOW
            payload["updated_at"] = NOW
            self.event_ids.append(self.canonical.create_event(payload))

        for deck in self.case["decks"]:
            deck_id = self.canonical.create_deck(
                {
                    "deck_hash": deck["deck_hash"],
                    "commander_hash": deck["commander_hash"],
                    "card_count": deck["card_count"],
                    "commander_count": deck["commander_count"],
                    "created_at": NOW,
                    "updated_at": NOW,
                }
            )
            self.deck_ids.append(deck_id)
            for card_id in deck["cards"]:
                card = cards[card_id]
                self.canonical.add_deck_card(
                    {
                        "canonical_deck_id": deck_id,
                        "scryfall_id": card["scryfall_id"],
                        "oracle_id": card["oracle_id"],
                        "quantity": 1,
                        "zone": "mainboard",
                    }
                )

        for entry in self.case["entries"]:
            self.canonical.create_event_deck_entry(
                {
                    "canonical_event_id": self.event_ids[entry["event_index"]],
                    "canonical_deck_id": self.deck_ids[entry["deck_index"]],
                    "pilot_name": entry["pilot_name"],
                    "placement": entry["placement"],
                    "placement_label": entry["placement_label"],
                    "wins": entry["wins"],
                    "losses": entry["losses"],
                    "draws": entry["draws"],
                    "top_cut_made": entry["top_cut_made"],
                    "winner": entry["winner"],
                    "created_at": NOW,
                }
            )

    def test_build_card_metrics_from_canonical_records_only(self) -> None:
        result = AnalyticsFoundationBuilder(self.analytics, self.regional).build_card_metrics(
            self.case["time_window"],
            self.case["window_end_date"],
        )

        self.assertEqual(result.eligible_entry_count, 2)
        self.assertEqual(result.skipped_entry_count, 2)
        self.assertEqual(result.card_metric_count, 3)
        self.assertEqual(result.regional_metric_count, 3)
        self.assertEqual(result.evidence_count_count, 3)
        self.assertIsNotNone(result.historical_snapshot_id)

        mana = self.analytics.get_card_performance_metric(
            "oracle-mana-crypt",
            "90d",
            "2026-06-21",
        )
        self.assertEqual(mana["sample_size"], 2)
        self.assertEqual(mana["raw_inclusion_rate"], 1.0)
        self.assertEqual(mana["weighted_inclusion_rate"], 1.0)
        self.assertEqual(mana["confidence_score"], 2 / 30)

        tutor = self.analytics.get_card_performance_metric(
            "oracle-demonic-tutor",
            "90d",
            "2026-06-21",
        )
        self.assertEqual(tutor["sample_size"], 1)
        self.assertEqual(tutor["raw_inclusion_rate"], 0.5)
        self.assertTrue(isclose(tutor["weighted_inclusion_rate"], 0.625))
        self.assertEqual(tutor["winner_inclusion_rate"], 1.0)
        self.assertEqual(tutor["topcut_inclusion_rate"], 0.5)
        self.assertTrue(isclose(tutor["winrate_delta"], 0.4))

        evidence = self.analytics.get_evidence_count("card", "oracle-mana-crypt")
        self.assertEqual(evidence["tournament_evidence_count"], 2)

    def test_historical_and_regional_outputs_are_idempotent(self) -> None:
        builder = AnalyticsFoundationBuilder(self.analytics, self.regional)
        first = builder.build_card_metrics("90d", "2026-06-21")
        second = builder.build_card_metrics("90d", "2026-06-21")

        self.assertEqual(first.historical_snapshot_id, second.historical_snapshot_id)
        historical = self.analytics.list_historical_card_metrics(first.historical_snapshot_id)
        self.assertEqual(len(historical), 3)

        regional = self.regional.get_card_metric("NA", "US", "90d", "2026-06-21", "oracle-demonic-tutor")
        self.assertEqual(regional["sample_size"], 1)
        self.assertEqual(regional["inclusion_rate"], 0.5)
        self.assertTrue(isclose(regional["weighted_inclusion_rate"], 0.625))

    def test_entry_weights_are_persisted_for_eligible_entries(self) -> None:
        AnalyticsFoundationBuilder(self.analytics, self.regional).build_card_metrics("90d", "2026-06-21")
        rows = self.connection.execute(
            """
            SELECT pilot_name, placement, entry_weight
            FROM event_deck_entries
            ORDER BY event_deck_entry_id
            """
        ).fetchall()
        self.assertGreater(rows[0]["entry_weight"], rows[2]["entry_weight"])
        self.assertEqual(rows[3]["entry_weight"], 0.0)

    def test_empty_window_writes_no_metrics(self) -> None:
        result = AnalyticsFoundationBuilder(self.analytics, self.regional).build_card_metrics("30d", "2025-01-01")
        self.assertEqual(result.eligible_entry_count, 0)
        self.assertEqual(result.card_metric_count, 0)
        self.assertIsNone(result.historical_snapshot_id)


class AnalyticsBoundaryTest(unittest.TestCase):
    def test_analytics_package_does_not_import_providers_or_source_repositories(self) -> None:
        forbidden_prefixes = (
            "codie.providers",
            "codie.ingestion",
            "codie.db.repositories.source",
        )
        offenders = []
        for path in sorted((ROOT / "codie" / "analytics").rglob("*.py")):
            imports = imports_for(path)
            for module in imports:
                if module.startswith(forbidden_prefixes):
                    offenders.append(f"{path.relative_to(ROOT)} imports {module}")
        self.assertEqual(offenders, [])

    def test_analytics_repository_does_not_query_source_tables(self) -> None:
        text = (ROOT / "codie" / "db" / "repositories" / "analytics.py").read_text(encoding="utf-8")
        forbidden_fragments = (
            "FROM source_events",
            "JOIN source_events",
            "FROM source_decks",
            "JOIN source_decks",
            "FROM source_deck_cards",
            "JOIN source_deck_cards",
            "FROM provider_objects",
            "JOIN provider_objects",
        )
        offenders = [fragment for fragment in forbidden_fragments if fragment in text]
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
