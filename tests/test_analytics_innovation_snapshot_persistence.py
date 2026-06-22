from __future__ import annotations

import json
import unittest

from codie.analytics.innovation import (
    InnovationSignal,
    InnovationSnapshotSpec,
    config_hash,
    config_json,
    innovation_snapshot_item_row,
    innovation_snapshot_run_row,
    persist_innovation_snapshot,
)
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories import AnalyticsRepository, CoreRepository


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def add_card(connection, scryfall_id: str = "scryfall-remora", oracle_id: str = "oracle-remora") -> None:
    CoreRepository(connection).upsert_card(
        {
            "scryfall_id": scryfall_id,
            "oracle_id": oracle_id,
            "name": "Mystic Remora",
            "normalized_name": "mystic remora",
            "type_line": "Enchantment",
            "color_identity_json": '["U"]',
            "raw_json": "{}",
            "imported_at": GENERATED_AT,
        }
    )


def signal(
    *,
    innovation_id: str = "innovation:remora",
    oracle_id: str = "oracle-remora",
    scryfall_id: str | None = "scryfall-remora",
    innovation_type: str = "new_innovation",
) -> InnovationSignal:
    return InnovationSignal(
        innovation_id=innovation_id,
        oracle_id=oracle_id,
        scryfall_id=scryfall_id,
        commander_signature="kraum-ludevics-opus|tymna-the-weaver",
        region_code="NA",
        innovation_type=innovation_type,
        recent_window="30d",
        baseline_window="180d",
        recent_inclusion_rate=0.20,
        baseline_inclusion_rate=0.0,
        usage_delta=0.20,
        recent_topcut_count=2,
        recent_winner_count=1,
        first_recent_seen_at="2026-06-01",
        last_seen_before_recent_window=None,
        card_released_at="1995-06-03",
        is_new_release=False,
        sample_size=2,
        confidence_score=0.0666666667,
        source_event_ids_json='["event:1"]',
        source_deck_ids_json='["deck:1","deck:2"]',
        generated_at=GENERATED_AT,
    )


def snapshot() -> InnovationSnapshotSpec:
    return InnovationSnapshotSpec(
        generated_at=GENERATED_AT,
        config={"recent_window": "30d", "baseline_window": "180d", "minimum_sample_size": 2},
        notes="fixture snapshot",
    )


class InnovationSnapshotPersistenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        add_card(self.connection)
        self.repository = AnalyticsRepository(self.connection)

    def test_config_serialization_is_deterministic(self) -> None:
        left = {"baseline_window": "180d", "recent_window": "30d"}
        right = {"recent_window": "30d", "baseline_window": "180d"}

        self.assertEqual(config_json(left), config_json(right))
        self.assertEqual(config_hash(left), config_hash(right))

    def test_row_mappers_preserve_snapshot_and_signal_fields(self) -> None:
        run_row = innovation_snapshot_run_row(snapshot())
        item_row = innovation_snapshot_item_row(signal())

        self.assertEqual(json.loads(str(run_row["config_json"]))["recent_window"], "30d")
        self.assertEqual(run_row["config_hash"], config_hash(snapshot().config))
        self.assertEqual(item_row["innovation_id"], "innovation:remora")
        self.assertEqual(item_row["oracle_id"], "oracle-remora")
        self.assertEqual(item_row["scryfall_id"], "scryfall-remora")
        self.assertEqual(item_row["is_new_release"], 0)
        self.assertEqual(item_row["source_event_ids_json"], '["event:1"]')

    def test_persist_innovation_snapshot_writes_run_and_items(self) -> None:
        result = persist_innovation_snapshot(
            repository=self.repository,
            snapshot=snapshot(),
            signals=(signal(),),
        )

        run = self.repository.get_innovation_snapshot_run(result.innovation_snapshot_run_id)
        items = self.repository.list_innovation_snapshot_items(result.innovation_snapshot_run_id)
        self.assertEqual(result.signal_count, 1)
        self.assertEqual(run["config_hash"], config_hash(snapshot().config))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["innovation_id"], "innovation:remora")
        self.assertEqual(items[0]["recent_topcut_count"], 2)

    def test_repeated_persistence_replaces_existing_snapshot_for_same_key(self) -> None:
        first = persist_innovation_snapshot(
            repository=self.repository,
            snapshot=snapshot(),
            signals=(signal(),),
        )
        second_signal = signal(
            innovation_id="innovation:other",
            oracle_id="oracle-other",
            scryfall_id=None,
            innovation_type="regional_innovation",
        )
        second = persist_innovation_snapshot(
            repository=self.repository,
            snapshot=snapshot(),
            signals=(second_signal,),
        )

        runs = self.repository.find_innovation_snapshot_runs(
            generated_at=GENERATED_AT,
            config_hash=config_hash(snapshot().config),
        )
        items = self.repository.list_innovation_snapshot_items(second.innovation_snapshot_run_id)
        orphan_count = self.connection.execute(
            "SELECT COUNT(*) AS count FROM innovation_snapshot_items WHERE innovation_snapshot_run_id = ?",
            (first.innovation_snapshot_run_id,),
        ).fetchone()
        self.assertEqual(len(runs), 1)
        self.assertNotEqual(first.innovation_snapshot_run_id, second.innovation_snapshot_run_id)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["innovation_id"], "innovation:other")
        self.assertEqual(orphan_count["count"], 0)

    def test_failed_item_insert_rolls_back_snapshot(self) -> None:
        bad_signal = signal(scryfall_id="missing-scryfall")

        with self.assertRaises(Exception):
            persist_innovation_snapshot(
                repository=self.repository,
                snapshot=snapshot(),
                signals=(bad_signal,),
            )

        run_count = self.connection.execute("SELECT COUNT(*) AS count FROM innovation_snapshot_runs").fetchone()
        item_count = self.connection.execute("SELECT COUNT(*) AS count FROM innovation_snapshot_items").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(item_count["count"], 0)

    def test_invalid_snapshot_spec_fails_cleanly_and_recommendations_untouched(self) -> None:
        with self.assertRaises(ValueError):
            InnovationSnapshotSpec(generated_at="", config={"window": "30d"})
        with self.assertRaises(ValueError):
            InnovationSnapshotSpec(generated_at=GENERATED_AT, config={})

        persist_innovation_snapshot(
            repository=self.repository,
            snapshot=snapshot(),
            signals=(signal(),),
        )
        run_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()
        candidate_count = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_candidates").fetchone()
        self.assertEqual(run_count["count"], 0)
        self.assertEqual(candidate_count["count"], 0)


if __name__ == "__main__":
    unittest.main()
