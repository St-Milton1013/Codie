from __future__ import annotations

import json
import unittest

from codie.analytics import (
    InnovationFilter,
    detect_innovations_from_repository,
    innovation_observations_from_rows,
)
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.source import SourceRepository


NOW = "2026-06-22T00:00:00+00:00"
COMMANDER = "kraum-card|tymna-card"


class AnalyticsInnovationRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.canonical = CanonicalRepository(self.connection)
        self.analytics = AnalyticsRepository(self.connection)
        self.deck_sources: dict[str, int] = {}
        self.event_sources: dict[str, int] = {}
        self._seed_cards()
        self._seed_records()

    def _insert_card(
        self,
        *,
        scryfall_id: str,
        oracle_id: str,
        name: str,
        type_line: str = "Artifact",
        colors: list[str] | None = None,
        released_at: str | None = None,
    ) -> None:
        self.core.insert_card(
            {
                "scryfall_id": scryfall_id,
                "oracle_id": oracle_id,
                "name": name,
                "normalized_name": name.lower(),
                "type_line": type_line,
                "color_identity_json": json.dumps(colors or []),
                "released_at": released_at,
                "raw_json": json.dumps({"id": scryfall_id, "name": name}, sort_keys=True),
                "imported_at": NOW,
            }
        )

    def _seed_cards(self) -> None:
        self._insert_card(scryfall_id="common-card", oracle_id="oracle-common", name="Common Card")
        self._insert_card(scryfall_id="new-card", oracle_id="oracle-new", name="New Card")
        self._insert_card(scryfall_id="release-card", oracle_id="oracle-release", name="Release Card", released_at="2026-06-01")
        self._insert_card(scryfall_id="regional-card", oracle_id="oracle-regional", name="Regional Card", type_line="Instant", colors=["U"])
        self._insert_card(scryfall_id="commander-card", oracle_id="oracle-commander", name="Commander Card")

    def _source_pair(self, key: str) -> tuple[int, int]:
        source_event_id = self.source.create_source_event(
            {
                "provider": "topdeck",
                "provider_event_id": f"event-{key}",
                "source_url": f"https://topdeck.test/events/{key}",
                "imported_at": NOW,
            }
        )
        source_deck_id = self.source.create_source_deck(
            {
                "provider": "topdeck",
                "provider_deck_id": f"deck-{key}",
                "source_event_id": source_event_id,
                "source_url": f"https://topdeck.test/decks/{key}",
                "imported_at": NOW,
            }
        )
        self.event_sources[key] = source_event_id
        self.deck_sources[key] = source_deck_id
        return source_event_id, source_deck_id

    def _event(self, key: str, event_date: str, *, player_count: int = 64, region: str = "NA", country: str = "US") -> int:
        source_event_id, _ = self._source_pair(key)
        event_id = self.canonical.create_event(
            {
                "event_name": f"{key} Open",
                "normalized_event_name": f"{key} open",
                "event_date": event_date,
                "format": "commander",
                "region": region,
                "country": country,
                "player_count": player_count,
                "deck_count": 1,
                "dedupe_key": f"{key}|{event_date}",
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
        self.canonical.link_event_source(
            {
                "canonical_event_id": event_id,
                "source_event_id": source_event_id,
                "provider": "topdeck",
                "source_url": f"https://topdeck.test/events/{key}",
                "created_at": NOW,
            }
        )
        return event_id

    def _deck(self, key: str, cards: tuple[str, ...]) -> int:
        _, source_deck_id = self._source_pair(f"deck-{key}")
        deck_id = self.canonical.create_deck(
            {
                "deck_hash": f"hash-{key}",
                "commander_hash": COMMANDER,
                "card_count": 100,
                "commander_count": 2,
                "created_at": NOW,
                "updated_at": NOW,
            }
        )
        self.canonical.link_deck_source(
            {
                "canonical_deck_id": deck_id,
                "source_deck_id": source_deck_id,
                "provider": "topdeck",
                "source_url": f"https://topdeck.test/decks/{key}",
                "created_at": NOW,
            }
        )
        for scryfall_id in cards:
            card = self.core.get_card(scryfall_id)
            self.canonical.add_deck_card(
                {
                    "canonical_deck_id": deck_id,
                    "scryfall_id": scryfall_id,
                    "oracle_id": card["oracle_id"],
                    "quantity": 1,
                    "zone": "mainboard",
                }
            )
        return deck_id

    def _entry(self, key: str, event_id: int, deck_id: int, *, placement: int = 8, winner: int = 0) -> None:
        self.canonical.create_event_deck_entry(
            {
                "canonical_event_id": event_id,
                "canonical_deck_id": deck_id,
                "source_deck_id": self.deck_sources[f"deck-{key}"],
                "pilot_name": key,
                "placement": placement,
                "top_cut_made": 1 if placement <= 16 else 0,
                "winner": winner,
                "created_at": NOW,
            }
        )

    def _seed_records(self) -> None:
        for index in range(1, 11):
            event_id = self._event(f"baseline-{index}", "2026-04-15")
            deck_id = self._deck(f"baseline-{index}", ("common-card",))
            self._entry(f"baseline-{index}", event_id, deck_id)

        recent_event = self._event("recent", "2026-06-20")
        for index, cards in enumerate(
            (
                ("common-card", "new-card", "release-card", "regional-card", "commander-card"),
                ("common-card", "new-card", "release-card", "regional-card"),
            ),
            start=1,
        ):
            deck_id = self._deck(f"recent-{index}", cards)
            self._entry(f"recent-{index}", recent_event, deck_id, placement=index, winner=1 if index == 1 else 0)

        old_event = self._event("old", "2025-01-15")
        old_deck = self._deck("old", ("common-card",))
        self._entry("old", old_event, old_deck)

    def test_repository_rows_map_to_innovation_observations(self) -> None:
        rows = self.analytics.list_innovation_observation_rows(
            window_start_date="2026-06-01",
            window_end_date="2026-06-30",
        )
        observations = innovation_observations_from_rows(rows)
        new_observation = next(observation for observation in observations if observation.oracle_id == "oracle-release")

        self.assertEqual(new_observation.scryfall_id, "release-card")
        self.assertEqual(new_observation.event_date, "2026-06-20")
        self.assertEqual(new_observation.commander_signature, COMMANDER)
        self.assertEqual(new_observation.region_code, "NA")
        self.assertEqual(new_observation.country_code, "US")
        self.assertEqual(new_observation.placement, 1)
        self.assertTrue(new_observation.top_cut)
        self.assertTrue(new_observation.winner)
        self.assertEqual(new_observation.player_count, 64)
        self.assertEqual(new_observation.card_released_at, "2026-06-01")
        self.assertEqual(new_observation.source_deck_id, f"source_deck:{self.deck_sources['deck-recent-1']}")
        self.assertEqual(new_observation.source_event_id, f"source_event:{self.event_sources['recent']}")

    def test_recent_top_performing_rows_feed_detector_and_preserve_evidence_ids(self) -> None:
        signals = detect_innovations_from_repository(
            self.analytics,
            InnovationFilter(
                window_end_date="2026-06-30",
                low_baseline_inclusion_threshold=0.20,
                breakout_delta_threshold=0.05,
            ),
            generated_at=NOW,
        )
        signal_types = {(signal.oracle_id, signal.innovation_type) for signal in signals}
        self.assertIn(("oracle-new", "new_innovation"), signal_types)
        self.assertIn(("oracle-release", "new_release_adoption"), signal_types)
        self.assertIn(("oracle-regional", "regional_innovation"), signal_types)
        self.assertIn(("oracle-commander", "commander_specific_innovation"), signal_types)
        self.assertNotIn(("oracle-common", "new_innovation"), signal_types)

        release = next(signal for signal in signals if signal.oracle_id == "oracle-release" and signal.innovation_type == "new_release_adoption")
        self.assertEqual(release.card_released_at, "2026-06-01")
        self.assertTrue(release.is_new_release)
        self.assertEqual(release.region_code, None)

        regional = next(signal for signal in signals if signal.oracle_id == "oracle-regional" and signal.innovation_type == "regional_innovation")
        self.assertEqual(regional.region_code, "NA")

        commander = next(signal for signal in signals if signal.oracle_id == "oracle-commander" and signal.innovation_type == "commander_specific_innovation")
        self.assertEqual(commander.commander_signature, COMMANDER)

        self.assertEqual(
            json.loads(release.source_deck_ids_json),
            [f"source_deck:{self.deck_sources['deck-recent-1']}", f"source_deck:{self.deck_sources['deck-recent-2']}"],
        )
        self.assertEqual(json.loads(release.source_event_ids_json), [f"source_event:{self.event_sources['recent']}"])

    def test_failure_modes_and_empty_results_are_clean(self) -> None:
        with self.assertRaises(ValueError):
            detect_innovations_from_repository(
                self.analytics,
                InnovationFilter(window_end_date="2026-06-30"),
                generated_at="",
            )
        with self.assertRaises(ValueError):
            self.analytics.list_innovation_observation_rows(window_start_date="not-a-date")
        with self.assertRaises(ValueError):
            InnovationFilter(window_end_date="2026-06-30", baseline_window="45d")
        with self.assertRaises(ValueError):
            innovation_observations_from_rows(
                (
                    {
                        "oracle_id": "oracle-card",
                        "scryfall_id": "card",
                        "card_name": "Card",
                        "type_line": "Artifact",
                        "color_identity_json": "[]",
                        "source_deck_id": None,
                        "canonical_deck_id": None,
                        "source_event_id": "1",
                        "canonical_event_id": "1",
                        "event_date": "2026-06-20",
                        "commander_signature": COMMANDER,
                        "region": "NA",
                        "country": "US",
                        "placement": 1,
                        "top_cut_made": 1,
                        "final_pod": 0,
                        "winner": 0,
                        "player_count": 64,
                        "card_released_at": None,
                    },
                )
            )

        self.assertEqual(
            detect_innovations_from_repository(
                self.analytics,
                InnovationFilter(window_end_date="2024-01-01"),
                generated_at=NOW,
            ),
            (),
        )

    def test_repository_wiring_does_not_create_recommendation_rows(self) -> None:
        detect_innovations_from_repository(
            self.analytics,
            InnovationFilter(window_end_date="2026-06-30"),
            generated_at=NOW,
        )
        run_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
