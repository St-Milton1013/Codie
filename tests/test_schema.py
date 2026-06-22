from __future__ import annotations

import sqlite3
import unittest

from codie.canonical.signature import commander_signature
from codie.db.bootstrap import bootstrap_database
from codie.db.pragmas import foreign_keys_enabled
from codie.db.repositories import (
    AnalyticsRepository,
    CanonicalRepository,
    CoreRepository,
    CuratedRepository,
    RegionalRepository,
    SimulationRepository,
    SourceRepository,
    UserRepository,
)
from codie.db.repositories.base import RepositoryError


class SchemaFoundationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.now = "2026-06-21T00:00:00+00:00"

    def tearDown(self) -> None:
        self.connection.close()

    def test_schema_bootstraps_all_required_tables_and_foreign_keys(self) -> None:
        self.assertTrue(foreign_keys_enabled(self.connection))
        expected = {
            "cards",
            "commanders",
            "ingestion_runs",
            "provider_objects",
            "source_events",
            "source_decks",
            "source_deck_cards",
            "deck_auxiliary_cards",
            "source_primers",
            "source_combos",
            "canonical_events",
            "canonical_event_sources",
            "canonical_decks",
            "canonical_deck_sources",
            "canonical_deck_cards",
            "canonical_deck_commanders",
            "event_deck_entries",
            "tournament_rounds",
            "match_results",
            "commander_registry",
            "alias_registry",
            "archetype_label_registry",
            "primer_registry",
            "combos",
            "combo_cards",
            "package_registry",
            "package_cards",
            "card_performance_metrics",
            "historical_snapshots",
            "historical_commander_metrics",
            "historical_card_metrics",
            "evidence_counts",
            "card_statistics_snapshots",
            "card_statistics",
            "recommendation_runs",
            "recommendation_candidates",
            "regional_commander_metrics",
            "regional_card_metrics",
            "regional_package_metrics",
            "simulation_batches",
            "simulation_batch_results",
            "simulation_traces",
            "user_decks",
            "user_deck_cards",
            "saved_analysis",
            "user_labels",
            "custom_packages",
            "analysis_sessions",
        }
        rows = self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
        self.assertTrue(expected.issubset({row["name"] for row in rows}))

    def test_required_indexes_exist(self) -> None:
        expected = {
            "idx_cards_oracle_id",
            "idx_cards_normalized_name",
            "idx_provider_objects_lookup",
            "idx_canonical_decks_hash",
            "idx_commander_registry_signature",
            "idx_alias_registry_target_name",
            "idx_archetype_label_registry_label",
            "idx_evidence_counts_entity",
            "idx_regional_card_lookup",
            "idx_analysis_sessions_deck_hash",
        }
        rows = self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'index'"
        ).fetchall()
        self.assertTrue(expected.issubset({row["name"] for row in rows}))

    def test_late_constitution_tables_are_present(self) -> None:
        expected = {
            "analysis_sessions",
            "alias_registry",
            "commander_registry",
            "archetype_label_registry",
            "regional_commander_metrics",
            "regional_card_metrics",
            "regional_package_metrics",
            "evidence_counts",
            "historical_snapshots",
            "historical_commander_metrics",
            "historical_card_metrics",
            "card_performance_metrics",
        }
        rows = self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
        self.assertTrue(expected.issubset({row["name"] for row in rows}))

    def test_oracle_id_is_grouping_key_not_enforced_identity(self) -> None:
        core = CoreRepository(self.connection)
        for suffix in ("a", "b"):
            core.insert_card(
                {
                    "scryfall_id": f"print-{suffix}",
                    "oracle_id": "shared-oracle",
                    "name": f"Shared Oracle {suffix}",
                    "normalized_name": f"shared oracle {suffix}",
                    "raw_json": "{}",
                    "imported_at": self.now,
                }
            )
        self.connection.execute(
            """
            INSERT INTO card_performance_metrics (oracle_id, time_window, window_end_date, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            ("unresolved-oracle", "90d", "2026-06-21", self.now),
        )
        rows = self.connection.execute("SELECT * FROM cards WHERE oracle_id = ?", ("shared-oracle",)).fetchall()
        self.assertEqual(len(rows), 2)

    def test_duplicate_constraints_are_enforced(self) -> None:
        canonical = CanonicalRepository(self.connection)
        payload = {
            "event_name": "Unique Open",
            "normalized_event_name": "unique open",
            "dedupe_key": "unique-open",
            "created_at": self.now,
            "updated_at": self.now,
        }
        canonical.create_event(payload)
        with self.assertRaises(sqlite3.IntegrityError):
            canonical.create_event(payload)

    def test_provider_object_payload_hash_is_preserved(self) -> None:
        source = SourceRepository(self.connection)
        object_id = source.create_provider_object(
            {
                "provider": "topdeck",
                "object_type": "deck",
                "provider_id": "deck-1",
                "source_url": "https://example.test/deck-1",
                "retrieved_at": self.now,
                "payload_hash": "sha256:abc123",
                "raw_payload_json": '{"deck": true}',
            }
        )
        row = source.get_provider_object(object_id)
        self.assertEqual(row["payload_hash"], "sha256:abc123")
        self.assertEqual(row["raw_payload_json"], '{"deck": true}')

    def test_curated_registries_and_analysis_sessions(self) -> None:
        curated = CuratedRepository(self.connection)
        user = UserRepository(self.connection)
        curated.create_commander_registry_entry(
            {
                "commander_key": "tymna-kraum",
                "commander_signature": commander_signature(["Tymna the Weaver", "Kraum, Ludevic's Opus"]),
                "display_name": "Tymna the Weaver / Kraum, Ludevic's Opus",
                "source": "curated",
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        curated.create_archetype_label(
            {
                "label": "Source Label Only",
                "normalized_label": "source label only",
                "label_type": "source",
                "source": "fixture",
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        user_deck_id = user.create_user_deck(
            {
                "deck_hash": "analysis-deck",
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        session_id = user.create_analysis_session(
            {
                "user_deck_id": user_deck_id,
                "deck_hash": "analysis-deck",
                "session_type": "deck_import",
                "status": "completed",
                "started_at": self.now,
            }
        )
        self.assertGreater(session_id, 0)

    def test_schema_bootstraps_legacy_smoke_subset(self) -> None:
        expected = {
            "cards",
            "commanders",
            "provider_objects",
            "source_events",
            "source_decks",
            "canonical_events",
            "canonical_decks",
            "card_performance_metrics",
            "regional_card_metrics",
            "simulation_batches",
            "user_decks",
        }
        rows = self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
        self.assertTrue(expected.issubset({row["name"] for row in rows}))

    def test_card_and_commander_repository_paths(self) -> None:
        repo = CoreRepository(self.connection)
        repo.insert_card(
            {
                "scryfall_id": "card-1",
                "oracle_id": "oracle-1",
                "name": "Tymna the Weaver",
                "normalized_name": "tymna the weaver",
                "color_identity_json": '["B","W"]',
                "raw_json": "{}",
                "imported_at": self.now,
            }
        )
        commander_id = repo.insert_commander(
            {
                "scryfall_id": "card-1",
                "oracle_id": "oracle-1",
                "canonical_name": "Tymna the Weaver",
                "normalized_name": "tymna the weaver",
                "color_identity_json": '["B","W"]',
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        self.assertEqual(repo.get_commander(commander_id)["canonical_name"], "Tymna the Weaver")

    def test_foreign_key_failure_is_not_silent(self) -> None:
        with self.assertRaises(sqlite3.IntegrityError):
            CoreRepository(self.connection).insert_commander(
                {
                    "scryfall_id": "missing-card",
                    "canonical_name": "Missing",
                    "normalized_name": "missing",
                    "color_identity_json": "[]",
                    "created_at": self.now,
                    "updated_at": self.now,
                }
            )

    def test_source_payload_and_canonical_links(self) -> None:
        source = SourceRepository(self.connection)
        canonical = CanonicalRepository(self.connection)
        run_id = source.create_ingestion_run(
            {
                "provider": "topdeck",
                "pipeline_name": "fixture",
                "started_at": self.now,
                "status": "completed",
            }
        )
        object_id = source.create_provider_object(
            {
                "provider": "topdeck",
                "object_type": "event",
                "provider_id": "event-1",
                "source_url": "https://example.test/event-1",
                "retrieved_at": self.now,
                "payload_hash": "hash-1",
                "raw_payload_json": '{"ok": true}',
                "run_id": run_id,
            }
        )
        source_event_id = source.create_source_event(
            {
                "provider": "topdeck",
                "provider_event_id": "event-1",
                "provider_object_id": object_id,
                "raw_json": '{"event": true}',
                "imported_at": self.now,
            }
        )
        canonical_event_id = canonical.create_event(
            {
                "event_name": "Test Open",
                "normalized_event_name": "test open",
                "dedupe_key": "test-open|2026-06-21",
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        canonical.link_event_source(
            {
                "canonical_event_id": canonical_event_id,
                "source_event_id": source_event_id,
                "provider": "topdeck",
                "created_at": self.now,
            }
        )
        self.assertEqual(source.get_provider_object(object_id)["raw_payload_json"], '{"ok": true}')

    def test_canonical_deck_cards_and_evidence_counts(self) -> None:
        core = CoreRepository(self.connection)
        canonical = CanonicalRepository(self.connection)
        analytics = AnalyticsRepository(self.connection)
        core.insert_card(
            {
                "scryfall_id": "card-2",
                "oracle_id": "oracle-2",
                "name": "Kraum, Ludevic's Opus",
                "normalized_name": "kraum ludevics opus",
                "raw_json": "{}",
                "imported_at": self.now,
            }
        )
        deck_id = canonical.create_deck(
            {
                "deck_hash": "deck-hash",
                "commander_hash": "kraum ludevics opus",
                "card_count": 99,
                "commander_count": 1,
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        canonical.add_deck_card({"canonical_deck_id": deck_id, "scryfall_id": "card-2", "oracle_id": "oracle-2"})
        analytics.upsert_evidence_count(
            {
                "entity_type": "card",
                "entity_id": "oracle-2",
                "tournament_evidence_count": 1,
                "updated_at": self.now,
            }
        )
        self.assertEqual(analytics.get_evidence_count("card", "oracle-2")["tournament_evidence_count"], 1)

    def test_regional_simulation_and_user_repositories(self) -> None:
        regional = RegionalRepository(self.connection)
        simulation = SimulationRepository(self.connection)
        user = UserRepository(self.connection)
        regional.create_commander_metric(
            {
                "region_code": "north_america",
                "time_window": "90d",
                "window_end_date": "2026-06-21",
                "commander_signature": commander_signature(["Tymna the Weaver", "Kraum, Ludevic's Opus"]),
                "sample_size": 12,
                "updated_at": self.now,
            }
        )
        simulation.create_batch(
            {
                "batch_id": "batch-1",
                "deck_hash": "deck-hash",
                "games_requested": 100,
                "min_mulligan_keep": 5,
                "status": "completed",
                "created_at": self.now,
            }
        )
        simulation.create_result(
            {
                "batch_id": "batch-1",
                "target_card": "Ad Nauseam",
                "target_zone": "hand",
                "turn": 3,
                "win_count": 42,
                "win_rate": 0.42,
            }
        )
        user_deck_id = user.create_user_deck(
            {
                "deck_hash": "user-deck-hash",
                "raw_input": "1 Kraum, Ludevic's Opus",
                "created_at": self.now,
                "updated_at": self.now,
            }
        )
        user.add_user_deck_card({"user_deck_id": user_deck_id, "raw_name": "Kraum, Ludevic's Opus", "quantity": 1})
        self.assertGreater(user_deck_id, 0)

    def test_required_field_validation_and_commander_signature(self) -> None:
        with self.assertRaises(RepositoryError):
            SourceRepository(self.connection).create_provider_object({"provider": "topdeck"})
        self.assertEqual(commander_signature(["Kraum, Ludevic's Opus", "Tymna the Weaver"]), "kraum, ludevic's opus|tymna the weaver")
        self.assertEqual(commander_signature(["Tymna   the Weaver"]), "tymna the weaver")
        with self.assertRaises(ValueError):
            commander_signature([])


if __name__ == "__main__":
    unittest.main()
