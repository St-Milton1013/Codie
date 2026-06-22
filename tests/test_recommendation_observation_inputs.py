from __future__ import annotations

import json
import unittest

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories.analytics import AnalyticsRepository
from codie.db.repositories.base import RepositoryError
from codie.db.repositories.canonical import CanonicalRepository
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.source import SourceRepository
from codie.recommendations import (
    build_commander_staples_report,
    staple_observations_from_canonical_rows,
)


NOW = "2026-06-22T00:00:00+00:00"
COMMANDER_HASH = "kraum-card|tymna-card"


class RecommendationObservationInputTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.core = CoreRepository(self.connection)
        self.source = SourceRepository(self.connection)
        self.canonical = CanonicalRepository(self.connection)
        self.analytics = AnalyticsRepository(self.connection)
        self.event_ids: dict[str, int] = {}
        self.deck_ids: dict[str, int] = {}
        self.entry_ids: dict[str, int] = {}
        self._seed_cards()
        self._seed_canonical_records()

    def _insert_card(self, *, scryfall_id: str, oracle_id: str, name: str, type_line: str, colors: list[str]) -> None:
        self.core.insert_card(
            {
                "scryfall_id": scryfall_id,
                "oracle_id": oracle_id,
                "name": name,
                "normalized_name": name.lower(),
                "type_line": type_line,
                "color_identity_json": json.dumps(colors),
                "raw_json": json.dumps({"id": scryfall_id, "name": name}, sort_keys=True),
                "imported_at": NOW,
            }
        )

    def _seed_cards(self) -> None:
        self._insert_card(
            scryfall_id="mana-crypt",
            oracle_id="oracle-mana-crypt",
            name="Mana Crypt",
            type_line="Artifact",
            colors=[],
        )
        self._insert_card(
            scryfall_id="mystic-remora",
            oracle_id="oracle-remora",
            name="Mystic Remora",
            type_line="Enchantment",
            colors=["U"],
        )
        self._insert_card(
            scryfall_id="tymna-card",
            oracle_id="oracle-tymna",
            name="Tymna the Weaver",
            type_line="Legendary Creature",
            colors=["W", "B"],
        )

    def _source_event_and_deck(self, provider: str, event_url: str, deck_url: str) -> tuple[int, int]:
        source_event_id = self.source.create_source_event(
            {
                "provider": provider,
                "provider_event_id": event_url.rsplit("/", 1)[-1],
                "source_url": event_url,
                "imported_at": NOW,
            }
        )
        source_deck_id = self.source.create_source_deck(
            {
                "provider": provider,
                "provider_deck_id": deck_url.rsplit("/", 1)[-1],
                "source_event_id": source_event_id,
                "source_url": deck_url,
                "imported_at": NOW,
            }
        )
        return source_event_id, source_deck_id

    def _create_event(self, key: str, *, event_date: str, source_event_id: int) -> int:
        event_id = self.canonical.create_event(
            {
                "event_name": f"{key} Open",
                "normalized_event_name": f"{key} open",
                "event_date": event_date,
                "format": "commander",
                "region": "NA",
                "country": "US",
                "player_count": 64,
                "deck_count": 2,
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
        self.event_ids[key] = event_id
        return event_id

    def _create_deck(
        self,
        key: str,
        *,
        commander_hash: str,
        source_deck_id: int,
        card_ids: tuple[str, ...],
        include_commander_card: bool = False,
    ) -> int:
        deck_id = self.canonical.create_deck(
            {
                "deck_hash": f"hash-{key}",
                "commander_hash": commander_hash,
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
                "pilot_name": key,
                "created_at": NOW,
            }
        )
        for card_id in card_ids:
            card = self.core.get_card(card_id)
            self.canonical.add_deck_card(
                {
                    "canonical_deck_id": deck_id,
                    "scryfall_id": card_id,
                    "oracle_id": card["oracle_id"],
                    "quantity": 1,
                    "zone": "mainboard",
                }
            )
        if include_commander_card:
            commander = self.core.get_card("tymna-card")
            self.canonical.add_deck_card(
                {
                    "canonical_deck_id": deck_id,
                    "scryfall_id": "tymna-card",
                    "oracle_id": commander["oracle_id"],
                    "quantity": 1,
                    "zone": "commanders",
                    "is_commander": 1,
                }
            )
        self.deck_ids[key] = deck_id
        return deck_id

    def _create_entry(
        self,
        key: str,
        *,
        event_id: int,
        deck_id: int,
        source_deck_id: int | None,
        placement: int,
        winner: int,
        top_cut: int,
        entry_weight: float,
    ) -> int:
        entry_id = self.canonical.create_event_deck_entry(
            {
                "canonical_event_id": event_id,
                "canonical_deck_id": deck_id,
                "source_deck_id": source_deck_id,
                "pilot_name": key,
                "placement": placement,
                "placement_label": "Winner" if winner else "Participant",
                "top_cut_made": top_cut,
                "winner": winner,
                "entry_weight": entry_weight,
                "created_at": NOW,
            }
        )
        self.entry_ids[key] = entry_id
        return entry_id

    def _seed_canonical_records(self) -> None:
        source_event_id, source_deck_id = self._source_event_and_deck(
            "topdeck",
            "https://topdeck.test/events/live",
            "https://topdeck.test/decks/live-a",
        )
        live_event = self._create_event("live", event_date="2026-06-15", source_event_id=source_event_id)
        live_deck = self._create_deck(
            "live-a",
            commander_hash=COMMANDER_HASH,
            source_deck_id=source_deck_id,
            card_ids=("mana-crypt", "mystic-remora"),
            include_commander_card=True,
        )
        self._create_entry(
            "live-a",
            event_id=live_event,
            deck_id=live_deck,
            source_deck_id=source_deck_id,
            placement=1,
            winner=1,
            top_cut=1,
            entry_weight=0.9,
        )

        _, off_scope_source_deck_id = self._source_event_and_deck(
            "topdeck",
            "https://topdeck.test/events/live",
            "https://topdeck.test/decks/live-b",
        )
        off_scope_deck = self._create_deck(
            "live-b",
            commander_hash=COMMANDER_HASH,
            source_deck_id=off_scope_source_deck_id,
            card_ids=("mana-crypt",),
        )
        self._create_entry(
            "live-b",
            event_id=live_event,
            deck_id=off_scope_deck,
            source_deck_id=off_scope_source_deck_id,
            placement=24,
            winner=0,
            top_cut=0,
            entry_weight=0.2,
        )

        _, other_source_deck_id = self._source_event_and_deck(
            "topdeck",
            "https://topdeck.test/events/live",
            "https://topdeck.test/decks/other-commander",
        )
        other_deck = self._create_deck(
            "other-commander",
            commander_hash="thrasios-card|tymna-card",
            source_deck_id=other_source_deck_id,
            card_ids=("mana-crypt",),
        )
        self._create_entry(
            "other-commander",
            event_id=live_event,
            deck_id=other_deck,
            source_deck_id=other_source_deck_id,
            placement=2,
            winner=0,
            top_cut=1,
            entry_weight=0.8,
        )

        old_source_event_id, old_source_deck_id = self._source_event_and_deck(
            "topdeck",
            "https://topdeck.test/events/old",
            "https://topdeck.test/decks/old",
        )
        old_event = self._create_event("old", event_date="2026-01-01", source_event_id=old_source_event_id)
        self._create_entry(
            "old",
            event_id=old_event,
            deck_id=live_deck,
            source_deck_id=old_source_deck_id,
            placement=4,
            winner=0,
            top_cut=1,
            entry_weight=0.7,
        )

    def test_query_returns_canonical_rows_for_commander_window_and_top16_scope(self) -> None:
        rows = self.analytics.list_commander_card_observation_rows(
            commander_hash=COMMANDER_HASH,
            window_start_date="2026-06-01",
            window_end_date="2026-06-30",
        )
        self.assertEqual([row["card_name"] for row in rows], ["Mana Crypt", "Mystic Remora"])

        observations = staple_observations_from_canonical_rows(rows)
        self.assertEqual({observation.deck_id for observation in observations}, {f"event_entry:{self.entry_ids['live-a']}"})
        self.assertEqual(observations[0].entry_weight, 0.9)
        self.assertEqual(observations[0].provider, "topdeck")
        self.assertEqual(observations[0].event_url, "https://topdeck.test/events/live")
        self.assertEqual(observations[0].deck_url, "https://topdeck.test/decks/live-a")
        self.assertEqual(observations[1].color_identity, ("U",))

        report = build_commander_staples_report(
            commander_signature=COMMANDER_HASH,
            observations=observations,
            time_window="30d",
            generated_at=NOW,
        )
        self.assertEqual(report.total_matching_decks, 1)
        self.assertEqual([row.oracle_id for row in report.rows], ["oracle-mana-crypt", "oracle-remora"])

    def test_query_scopes_all_winners_and_commander_card_inclusion(self) -> None:
        all_rows = self.analytics.list_commander_card_observation_rows(
            commander_hash=COMMANDER_HASH,
            window_start_date="2026-06-01",
            window_end_date="2026-06-30",
            placement_scope="all",
        )
        all_observations = staple_observations_from_canonical_rows(all_rows)
        report = build_commander_staples_report(
            commander_signature=COMMANDER_HASH,
            observations=all_observations,
            time_window="30d",
            generated_at=NOW,
        )
        mana = next(row for row in report.rows if row.oracle_id == "oracle-mana-crypt")
        self.assertEqual(mana.matching_deck_count, 2)
        self.assertEqual(report.total_matching_decks, 2)

        winner_rows = self.analytics.list_commander_card_observation_rows(
            commander_hash=COMMANDER_HASH,
            window_start_date="2026-06-01",
            window_end_date="2026-06-30",
            placement_scope="winners",
        )
        self.assertEqual({row["event_deck_entry_id"] for row in winner_rows}, {self.entry_ids["live-a"]})

        rows_with_commanders = self.analytics.list_commander_card_observation_rows(
            commander_hash=COMMANDER_HASH,
            window_start_date="2026-06-01",
            window_end_date="2026-06-30",
            include_commanders=True,
        )
        self.assertIn("Tymna the Weaver", [row["card_name"] for row in rows_with_commanders])

    def test_query_rejects_missing_commander_and_unknown_scope(self) -> None:
        with self.assertRaises(RepositoryError):
            self.analytics.list_commander_card_observation_rows(commander_hash="")
        with self.assertRaises(RepositoryError):
            self.analytics.list_commander_card_observation_rows(
                commander_hash=COMMANDER_HASH,
                placement_scope="top_8",
            )

    def test_mapper_fails_cleanly_on_missing_identity_or_invalid_color_json(self) -> None:
        row = {
            "event_deck_entry_id": 1,
            "oracle_id": "oracle-card",
            "scryfall_id": "scryfall-card",
            "card_name": "Test Card",
            "quantity": 1,
            "type_line": "Artifact",
            "color_identity_json": "[]",
            "entry_weight": 1.0,
            "placement": 1,
            "top_cut_made": 1,
            "final_pod": 0,
            "winner": 0,
            "event_date": "2026-06-15",
            "deck_url": None,
            "event_url": None,
            "provider": None,
            "region": None,
            "country": None,
        }
        missing_oracle = dict(row)
        missing_oracle["oracle_id"] = None
        with self.assertRaises(ValueError):
            staple_observations_from_canonical_rows((missing_oracle,))

        invalid_color = dict(row)
        invalid_color["color_identity_json"] = "{"
        with self.assertRaises(ValueError):
            staple_observations_from_canonical_rows((invalid_color,))

    def test_phase8d_does_not_create_recommendation_rows(self) -> None:
        rows = self.analytics.list_commander_card_observation_rows(
            commander_hash=COMMANDER_HASH,
            window_start_date="2026-06-01",
            window_end_date="2026-06-30",
        )
        build_commander_staples_report(
            commander_signature=COMMANDER_HASH,
            observations=staple_observations_from_canonical_rows(rows),
            time_window="30d",
            generated_at=NOW,
        )
        run_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
