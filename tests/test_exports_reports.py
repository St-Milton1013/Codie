from __future__ import annotations

import unittest

from codie.analytics.innovation import InnovationSignal, InnovationSnapshotSpec, persist_innovation_snapshot
from codie.db.bootstrap import bootstrap_database
from codie.db.repositories import AnalyticsRepository, CoreRepository, RecommendationRepository
from codie.exports import (
    ExportMetadata,
    export_innovation_snapshot_json,
    export_recommendation_run_json,
    innovation_snapshot_markdown,
    outside_review_markdown,
    recommendation_run_markdown,
)
from codie.recommendations import (
    RecommendationCandidateSource,
    RecommendationGenerationConfig,
    RecommendationRunSpec,
    build_candidate_packet,
    persist_recommendation_packets,
)


GENERATED_AT = "2026-06-22T00:00:00+00:00"


def add_card(connection, scryfall_id: str = "scryfall-remora", oracle_id: str = "oracle-remora") -> None:
    CoreRepository(connection).upsert_card(
        {
            "scryfall_id": scryfall_id,
            "oracle_id": oracle_id,
            "name": "Mystic Remora",
            "normalized_name": "mystic remora",
            "raw_json": "{}",
            "imported_at": GENERATED_AT,
        }
    )


def recommendation_packet():
    return build_candidate_packet(
        source=RecommendationCandidateSource(
            oracle_id="oracle-remora",
            scryfall_id="scryfall-remora",
            card_name="Mystic Remora",
            sample_size=42,
            inclusion_rate=0.75,
            commander_lift=1.4,
            source_record_id="metric:oracle-remora:180d",
        ),
        config=RecommendationGenerationConfig(generated_at=GENERATED_AT, time_window="180d"),
    )


def innovation_signal() -> InnovationSignal:
    return InnovationSignal(
        innovation_id="innovation:remora",
        oracle_id="oracle-remora",
        scryfall_id="scryfall-remora",
        commander_signature="kraum-ludevics-opus|tymna-the-weaver",
        region_code="NA",
        innovation_type="new_innovation",
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
        confidence_score=0.06,
        source_event_ids_json='["event:1"]',
        source_deck_ids_json='["deck:1","deck:2"]',
        generated_at=GENERATED_AT,
    )


class ExportReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        add_card(self.connection)
        self.recommendations = RecommendationRepository(self.connection)
        self.analytics = AnalyticsRepository(self.connection)

    def test_recommendation_json_export_includes_run_and_candidates(self) -> None:
        persisted = persist_recommendation_packets(
            repository=self.recommendations,
            run=RecommendationRunSpec(
                input_deck_hash="deck-hash",
                commander_hash="kraum-ludevics-opus|tymna-the-weaver",
                generated_at=GENERATED_AT,
                config={"window": "180d"},
            ),
            packets=(recommendation_packet(),),
        )

        export = export_recommendation_run_json(
            run=self.recommendations.get_recommendation_run(persisted.recommendation_run_id),
            candidates=self.recommendations.list_run_candidates(persisted.recommendation_run_id),
            metadata=ExportMetadata(export_type="recommendation_run", generated_at=GENERATED_AT),
        )

        self.assertEqual(export["metadata"]["export_type"], "recommendation_run")
        self.assertEqual(export["run"]["input_deck_hash"], "deck-hash")
        self.assertEqual(export["candidates"][0]["oracle_id"], "oracle-remora")
        self.assertEqual(export["candidates"][0]["evidence"]["candidate"]["entity_id"], "oracle-remora")
        markdown = recommendation_run_markdown(export)
        self.assertIn("# Recommendation Run Export", markdown)
        self.assertIn("oracle-remora", markdown)

    def test_innovation_json_export_includes_snapshot_and_items(self) -> None:
        persisted = persist_innovation_snapshot(
            repository=self.analytics,
            snapshot=InnovationSnapshotSpec(
                generated_at=GENERATED_AT,
                config={"recent_window": "30d", "baseline_window": "180d"},
            ),
            signals=(innovation_signal(),),
        )

        export = export_innovation_snapshot_json(
            run=self.analytics.get_innovation_snapshot_run(persisted.innovation_snapshot_run_id),
            items=self.analytics.list_innovation_snapshot_items(persisted.innovation_snapshot_run_id),
            metadata=ExportMetadata(export_type="innovation_snapshot", generated_at=GENERATED_AT),
        )

        self.assertEqual(export["metadata"]["export_type"], "innovation_snapshot")
        self.assertEqual(export["items"][0]["innovation_id"], "innovation:remora")
        self.assertEqual(export["items"][0]["source_deck_ids"], ["deck:1", "deck:2"])
        markdown = innovation_snapshot_markdown(export)
        self.assertIn("# Innovation Snapshot Export", markdown)
        self.assertIn("new_innovation", markdown)

    def test_markdown_exports_are_deterministic_and_review_report_lists_exports(self) -> None:
        recommendation = {
            "metadata": {"export_type": "recommendation_run", "generated_at": GENERATED_AT, "schema_version": "1"},
            "run": {"recommendation_run_id": 1, "generated_at": GENERATED_AT, "input_deck_hash": "deck", "commander_hash": None, "config": None, "source_snapshot_id": None, "notes": None},
            "candidates": [],
        }
        innovation = {
            "metadata": {"export_type": "innovation_snapshot", "generated_at": GENERATED_AT, "schema_version": "1"},
            "snapshot": {"innovation_snapshot_run_id": 1, "generated_at": GENERATED_AT, "config_hash": "abc", "config": {}, "notes": None},
            "items": [],
        }

        first = outside_review_markdown(title="Codie Export Checkpoint", exports=(recommendation, innovation), generated_at=GENERATED_AT)
        second = outside_review_markdown(title="Codie Export Checkpoint", exports=(recommendation, innovation), generated_at=GENERATED_AT)

        self.assertEqual(first, second)
        self.assertIn("recommendation_run", first)
        self.assertIn("innovation_snapshot", first)

    def test_forbidden_wording_and_missing_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            ExportMetadata(export_type="", generated_at=GENERATED_AT)
        with self.assertRaises(ValueError):
            export_recommendation_run_json(run=None, candidates=(), metadata=ExportMetadata(export_type="recommendation_run", generated_at=GENERATED_AT))
        with self.assertRaises(ValueError):
            outside_review_markdown(title="You should play this card", exports=(), generated_at=GENERATED_AT)

    def test_exports_do_not_create_rows(self) -> None:
        before_runs = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()["count"]
        before_snapshots = self.connection.execute("SELECT COUNT(*) AS count FROM innovation_snapshot_runs").fetchone()["count"]

        outside_review_markdown(title="Codie Export Checkpoint", exports=(), generated_at=GENERATED_AT)

        after_runs = self.connection.execute("SELECT COUNT(*) AS count FROM recommendation_runs").fetchone()["count"]
        after_snapshots = self.connection.execute("SELECT COUNT(*) AS count FROM innovation_snapshot_runs").fetchone()["count"]
        self.assertEqual(before_runs, after_runs)
        self.assertEqual(before_snapshots, after_snapshots)


if __name__ == "__main__":
    unittest.main()
