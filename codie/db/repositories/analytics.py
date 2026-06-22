"""Repositories for derived metrics and evidence counts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class AnalyticsRepository(BaseRepository):
    def list_tournament_entry_inputs(self, window_end_date: str):
        return self.connection.execute(
            """
            SELECT
                ede.event_deck_entry_id,
                ede.canonical_event_id,
                ede.canonical_deck_id,
                ede.source_deck_id,
                ede.pilot_name,
                ede.placement,
                ede.placement_label,
                ede.record_text,
                ede.wins,
                ede.losses,
                ede.draws,
                ede.top_cut_made,
                ede.final_pod,
                ede.winner,
                ce.event_name,
                ce.event_date,
                ce.format,
                ce.region,
                ce.country,
                ce.player_count,
                cd.card_count,
                cd.commander_hash,
                COALESCE(MAX(cds.source_confidence), 1.0) AS source_confidence
            FROM event_deck_entries ede
            JOIN canonical_events ce ON ce.canonical_event_id = ede.canonical_event_id
            JOIN canonical_decks cd ON cd.canonical_deck_id = ede.canonical_deck_id
            LEFT JOIN canonical_deck_sources cds
                ON cds.canonical_deck_id = ede.canonical_deck_id
                AND (
                    cds.source_deck_id = ede.source_deck_id
                    OR ede.source_deck_id IS NULL
                )
            WHERE ce.event_date IS NULL OR ce.event_date <= ?
            GROUP BY ede.event_deck_entry_id
            ORDER BY ce.event_date, ede.event_deck_entry_id
            """,
            (window_end_date,),
        ).fetchall()

    def list_canonical_deck_cards(self, canonical_deck_id: int):
        return self.connection.execute(
            """
            SELECT canonical_deck_id, scryfall_id, oracle_id, quantity, zone, is_commander
            FROM canonical_deck_cards
            WHERE canonical_deck_id = ?
            ORDER BY zone, scryfall_id
            """,
            (canonical_deck_id,),
        ).fetchall()

    def update_event_deck_entry_weight(self, event_deck_entry_id: int, entry_weight: float) -> None:
        self.connection.execute(
            "UPDATE event_deck_entries SET entry_weight = ? WHERE event_deck_entry_id = ?",
            (entry_weight, event_deck_entry_id),
        )

    def upsert_card_performance_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("oracle_id", "time_window", "window_end_date", "updated_at"))
        columns = (
            "oracle_id",
            "scryfall_id",
            "time_window",
            "window_end_date",
            "raw_inclusion_rate",
            "weighted_inclusion_rate",
            "winner_inclusion_rate",
            "topcut_inclusion_rate",
            "winrate_with_card",
            "winrate_without_card",
            "winrate_delta",
            "topcut_delta",
            "confidence_score",
            "sample_size",
            "trend_30d",
            "trend_90d",
            "trend_180d",
            "trend_365d",
            "updated_at",
        )
        values = tuple(metric.get(column) for column in columns)
        self.connection.execute(
            """
            INSERT INTO card_performance_metrics (
                oracle_id, scryfall_id, time_window, window_end_date,
                raw_inclusion_rate, weighted_inclusion_rate, winner_inclusion_rate,
                topcut_inclusion_rate, winrate_with_card, winrate_without_card,
                winrate_delta, topcut_delta, confidence_score, sample_size,
                trend_30d, trend_90d, trend_180d, trend_365d, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(oracle_id, time_window, window_end_date) DO UPDATE SET
                scryfall_id = excluded.scryfall_id,
                raw_inclusion_rate = excluded.raw_inclusion_rate,
                weighted_inclusion_rate = excluded.weighted_inclusion_rate,
                winner_inclusion_rate = excluded.winner_inclusion_rate,
                topcut_inclusion_rate = excluded.topcut_inclusion_rate,
                winrate_with_card = excluded.winrate_with_card,
                winrate_without_card = excluded.winrate_without_card,
                winrate_delta = excluded.winrate_delta,
                topcut_delta = excluded.topcut_delta,
                confidence_score = excluded.confidence_score,
                sample_size = excluded.sample_size,
                trend_30d = excluded.trend_30d,
                trend_90d = excluded.trend_90d,
                trend_180d = excluded.trend_180d,
                trend_365d = excluded.trend_365d,
                updated_at = excluded.updated_at
            """,
            values,
        )
        row = self.get_card_performance_metric(
            str(metric["oracle_id"]),
            str(metric["time_window"]),
            str(metric["window_end_date"]),
        )
        return int(row["metric_id"])

    def get_card_performance_metric(self, oracle_id: str, time_window: str, window_end_date: str):
        return self.connection.execute(
            """
            SELECT * FROM card_performance_metrics
            WHERE oracle_id = ? AND time_window = ? AND window_end_date = ?
            """,
            (oracle_id, time_window, window_end_date),
        ).fetchone()

    def get_or_create_historical_snapshot(self, snapshot_date: str, window_type: str, created_at: str) -> int:
        self.connection.execute(
            """
            INSERT INTO historical_snapshots (snapshot_date, window_type, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(snapshot_date, window_type) DO NOTHING
            """,
            (snapshot_date, window_type, created_at),
        )
        row = self.connection.execute(
            """
            SELECT snapshot_id FROM historical_snapshots
            WHERE snapshot_date = ? AND window_type = ?
            """,
            (snapshot_date, window_type),
        ).fetchone()
        return int(row["snapshot_id"])

    def delete_historical_card_metrics(self, snapshot_id: int) -> None:
        self.connection.execute(
            "DELETE FROM historical_card_metrics WHERE snapshot_id = ?",
            (snapshot_id,),
        )

    def create_historical_card_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("snapshot_id", "oracle_id"))
        return self.insert("historical_card_metrics", metric)

    def list_historical_card_metrics(self, snapshot_id: int):
        return self.connection.execute(
            """
            SELECT * FROM historical_card_metrics
            WHERE snapshot_id = ?
            ORDER BY oracle_id
            """,
            (snapshot_id,),
        ).fetchall()

    def upsert_evidence_count(self, evidence: Mapping[str, Any]) -> int:
        self.require(evidence, ("entity_type", "entity_id", "updated_at"))
        columns = (
            "entity_type",
            "entity_id",
            "tournament_evidence_count",
            "primer_evidence_count",
            "combo_evidence_count",
            "package_evidence_count",
            "simulation_evidence_count",
            "updated_at",
        )
        values = tuple(evidence.get(column, 0 if column.endswith("_count") else None) for column in columns)
        self.connection.execute(
            """
            INSERT INTO evidence_counts (
                entity_type, entity_id, tournament_evidence_count, primer_evidence_count,
                combo_evidence_count, package_evidence_count, simulation_evidence_count, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entity_type, entity_id) DO UPDATE SET
                tournament_evidence_count = excluded.tournament_evidence_count,
                primer_evidence_count = excluded.primer_evidence_count,
                combo_evidence_count = excluded.combo_evidence_count,
                package_evidence_count = excluded.package_evidence_count,
                simulation_evidence_count = excluded.simulation_evidence_count,
                updated_at = excluded.updated_at
            """,
            values,
        )
        row = self.connection.execute(
            "SELECT evidence_id FROM evidence_counts WHERE entity_type = ? AND entity_id = ?",
            (evidence["entity_type"], evidence["entity_id"]),
        ).fetchone()
        return int(row["evidence_id"])

    def get_evidence_count(self, entity_type: str, entity_id: str):
        return self.connection.execute(
            "SELECT * FROM evidence_counts WHERE entity_type = ? AND entity_id = ?",
            (entity_type, entity_id),
        ).fetchone()
