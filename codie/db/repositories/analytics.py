"""Repositories for derived metrics and evidence counts."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from typing import Any

from .base import BaseRepository, RepositoryError


_OBSERVATION_SCOPES = {"all", "top_16", "winners"}


def _validate_date(value: str | None, field_name: str) -> None:
    if value in (None, ""):
        return
    try:
        date.fromisoformat(str(value)[:10])
    except ValueError as exc:
        raise ValueError(f"Invalid {field_name}: {value}") from exc


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

    def list_commander_card_observation_rows(
        self,
        *,
        commander_hash: str,
        window_start_date: str | None = None,
        window_end_date: str | None = None,
        placement_scope: str = "top_16",
        include_commanders: bool = False,
    ):
        """Return canonical card observations for downstream recommendation/report inputs."""
        if not isinstance(commander_hash, str) or not commander_hash.strip():
            raise RepositoryError("commander_hash is required")
        if placement_scope not in _OBSERVATION_SCOPES:
            raise RepositoryError(f"Unsupported placement_scope: {placement_scope}")

        filters = ["cd.commander_hash = ?"]
        params: list[Any] = [commander_hash]
        if window_start_date:
            filters.append("ce.event_date >= ?")
            params.append(window_start_date)
        if window_end_date:
            filters.append("ce.event_date <= ?")
            params.append(window_end_date)
        if placement_scope == "top_16":
            filters.append(
                """
                (
                    ede.top_cut_made = 1
                    OR ede.final_pod = 1
                    OR ede.winner = 1
                    OR (ede.placement IS NOT NULL AND ede.placement <= 16)
                )
                """
            )
        elif placement_scope == "winners":
            filters.append("(ede.winner = 1 OR ede.placement = 1)")
        if not include_commanders:
            filters.append("COALESCE(cdc.is_commander, 0) = 0")

        where_clause = " AND ".join(filters)
        return self.connection.execute(
            f"""
            SELECT
                ede.event_deck_entry_id,
                ede.canonical_event_id,
                ede.canonical_deck_id,
                cd.commander_hash,
                cdc.canonical_deck_card_id,
                cdc.scryfall_id,
                cdc.oracle_id,
                c.name AS card_name,
                c.type_line,
                c.color_identity_json,
                cdc.quantity,
                cdc.zone,
                cdc.is_commander,
                ede.entry_weight,
                ede.placement,
                ede.top_cut_made,
                ede.final_pod,
                ede.winner,
                ce.event_date,
                ce.region,
                ce.country,
                (
                    SELECT cds.source_url
                    FROM canonical_deck_sources cds
                    WHERE cds.canonical_deck_id = ede.canonical_deck_id
                        AND (
                            ede.source_deck_id IS NULL
                            OR cds.source_deck_id = ede.source_deck_id
                        )
                        AND cds.source_url IS NOT NULL
                    ORDER BY cds.canonical_deck_source_id
                    LIMIT 1
                ) AS deck_url,
                (
                    SELECT ces.source_url
                    FROM canonical_event_sources ces
                    WHERE ces.canonical_event_id = ede.canonical_event_id
                        AND ces.source_url IS NOT NULL
                    ORDER BY ces.canonical_event_source_id
                    LIMIT 1
                ) AS event_url,
                (
                    SELECT cds.provider
                    FROM canonical_deck_sources cds
                    WHERE cds.canonical_deck_id = ede.canonical_deck_id
                        AND (
                            ede.source_deck_id IS NULL
                            OR cds.source_deck_id = ede.source_deck_id
                        )
                    ORDER BY cds.canonical_deck_source_id
                    LIMIT 1
                ) AS provider
            FROM event_deck_entries ede
            JOIN canonical_events ce ON ce.canonical_event_id = ede.canonical_event_id
            JOIN canonical_decks cd ON cd.canonical_deck_id = ede.canonical_deck_id
            JOIN canonical_deck_cards cdc ON cdc.canonical_deck_id = ede.canonical_deck_id
            JOIN cards c ON c.scryfall_id = cdc.scryfall_id
            WHERE {where_clause}
            ORDER BY
                ce.event_date,
                ede.canonical_event_id,
                ede.placement,
                ede.event_deck_entry_id,
                cdc.zone,
                cdc.scryfall_id
            """,
            tuple(params),
        ).fetchall()

    def list_innovation_observation_rows(
        self,
        *,
        window_start_date: str | None = None,
        window_end_date: str | None = None,
        minimum_event_size: int | None = None,
        include_commanders: bool = False,
    ):
        """Return canonical tournament card rows for analytics innovation detection."""
        _validate_date(window_start_date, "window_start_date")
        _validate_date(window_end_date, "window_end_date")
        if minimum_event_size is not None and minimum_event_size < 0:
            raise ValueError("minimum_event_size must be non-negative")

        filters = ["ce.event_date IS NOT NULL"]
        params: list[Any] = []
        if window_start_date:
            filters.append("ce.event_date >= ?")
            params.append(window_start_date)
        if window_end_date:
            filters.append("ce.event_date <= ?")
            params.append(window_end_date)
        if minimum_event_size is not None:
            filters.append("(ce.player_count IS NULL OR ce.player_count >= ?)")
            params.append(minimum_event_size)
        if not include_commanders:
            filters.append("COALESCE(cdc.is_commander, 0) = 0")

        where_clause = " AND ".join(filters)
        return self.connection.execute(
            f"""
            SELECT
                ede.event_deck_entry_id,
                ede.canonical_event_id,
                ede.canonical_deck_id,
                COALESCE(ede.source_deck_id, cds.source_deck_id) AS source_deck_id,
                ces.source_event_id,
                cd.commander_hash AS commander_signature,
                cdc.canonical_deck_card_id,
                cdc.scryfall_id,
                cdc.oracle_id,
                c.name AS card_name,
                c.type_line,
                c.color_identity_json,
                c.released_at AS card_released_at,
                cdc.quantity,
                cdc.zone,
                cdc.is_commander,
                ede.placement,
                ede.top_cut_made,
                ede.final_pod,
                ede.winner,
                ce.event_date,
                ce.region,
                ce.country,
                ce.player_count
            FROM event_deck_entries ede
            JOIN canonical_events ce ON ce.canonical_event_id = ede.canonical_event_id
            JOIN canonical_decks cd ON cd.canonical_deck_id = ede.canonical_deck_id
            JOIN canonical_deck_cards cdc ON cdc.canonical_deck_id = ede.canonical_deck_id
            JOIN cards c ON c.scryfall_id = cdc.scryfall_id
            LEFT JOIN canonical_deck_sources cds
                ON cds.canonical_deck_id = ede.canonical_deck_id
                AND (
                    ede.source_deck_id IS NULL
                    OR cds.source_deck_id = ede.source_deck_id
                )
            LEFT JOIN canonical_event_sources ces
                ON ces.canonical_event_id = ede.canonical_event_id
            WHERE {where_clause}
            GROUP BY
                ede.event_deck_entry_id,
                cdc.canonical_deck_card_id
            ORDER BY
                ce.event_date,
                ede.canonical_event_id,
                ede.placement,
                ede.event_deck_entry_id,
                cdc.zone,
                cdc.scryfall_id
            """,
            tuple(params),
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

    def increment_evidence_count(
        self,
        *,
        entity_type: str,
        entity_id: str,
        tournament: int = 0,
        primer: int = 0,
        combo: int = 0,
        package: int = 0,
        simulation: int = 0,
        updated_at: str,
    ) -> int:
        self.connection.execute(
            """
            INSERT INTO evidence_counts (
                entity_type, entity_id, tournament_evidence_count, primer_evidence_count,
                combo_evidence_count, package_evidence_count, simulation_evidence_count, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(entity_type, entity_id) DO UPDATE SET
                tournament_evidence_count = evidence_counts.tournament_evidence_count + excluded.tournament_evidence_count,
                primer_evidence_count = evidence_counts.primer_evidence_count + excluded.primer_evidence_count,
                combo_evidence_count = evidence_counts.combo_evidence_count + excluded.combo_evidence_count,
                package_evidence_count = evidence_counts.package_evidence_count + excluded.package_evidence_count,
                simulation_evidence_count = evidence_counts.simulation_evidence_count + excluded.simulation_evidence_count,
                updated_at = excluded.updated_at
            """,
            (entity_type, entity_id, tournament, primer, combo, package, simulation, updated_at),
        )
        row = self.get_evidence_count(entity_type, entity_id)
        return int(row["evidence_id"])

    def rebuild_evidence_counts(self, *, updated_at: str) -> int:
        """Rebuild derived evidence counts from canonical and curated records."""
        with BaseRepository.transaction(self.connection, "evidence_rebuild"):
            self.connection.execute("DELETE FROM evidence_counts")
            for row in self.connection.execute(
                """
                SELECT
                    COALESCE(cdc.oracle_id, cdc.scryfall_id) AS entity_id,
                    COUNT(DISTINCT ede.event_deck_entry_id) AS evidence_count
                FROM canonical_deck_cards cdc
                JOIN event_deck_entries ede
                    ON ede.canonical_deck_id = cdc.canonical_deck_id
                WHERE COALESCE(cdc.oracle_id, cdc.scryfall_id) IS NOT NULL
                GROUP BY COALESCE(cdc.oracle_id, cdc.scryfall_id)
                """
            ).fetchall():
                self.increment_evidence_count(
                    entity_type="card",
                    entity_id=row["entity_id"],
                    tournament=int(row["evidence_count"]),
                    updated_at=updated_at,
                )
            for row in self.connection.execute(
                """
                SELECT
                    COALESCE(oracle_id, scryfall_id) AS entity_id,
                    COUNT(*) AS evidence_count
                FROM combo_cards
                WHERE COALESCE(oracle_id, scryfall_id) IS NOT NULL
                GROUP BY COALESCE(oracle_id, scryfall_id)
                """
            ).fetchall():
                self.increment_evidence_count(
                    entity_type="card",
                    entity_id=row["entity_id"],
                    combo=int(row["evidence_count"]),
                    updated_at=updated_at,
                )
            for row in self.connection.execute(
                """
                SELECT
                    COALESCE(c.provider_combo_id, c.combo_url, CAST(c.combo_id AS TEXT)) AS entity_id,
                    COUNT(cc.combo_card_id) AS evidence_count
                FROM combos c
                LEFT JOIN combo_cards cc ON cc.combo_id = c.combo_id
                GROUP BY c.combo_id
                HAVING COUNT(cc.combo_card_id) > 0
                """
            ).fetchall():
                self.increment_evidence_count(
                    entity_type="combo",
                    entity_id=row["entity_id"],
                    combo=int(row["evidence_count"]),
                    updated_at=updated_at,
                )
            for row in self.connection.execute(
                """
                SELECT primer_url AS entity_id, COUNT(*) AS evidence_count
                FROM primer_registry
                GROUP BY primer_url
                """
            ).fetchall():
                self.increment_evidence_count(
                    entity_type="primer",
                    entity_id=row["entity_id"],
                    primer=int(row["evidence_count"]),
                    updated_at=updated_at,
                )
            for row in self.connection.execute(
                """
                SELECT
                    pr.package_name AS entity_id,
                    COUNT(pc.package_card_id) AS evidence_count
                FROM package_registry pr
                LEFT JOIN package_cards pc ON pc.package_id = pr.package_id
                GROUP BY pr.package_id
                HAVING COUNT(pc.package_card_id) > 0
                """
            ).fetchall():
                self.increment_evidence_count(
                    entity_type="package",
                    entity_id=row["entity_id"],
                    package=int(row["evidence_count"]),
                    updated_at=updated_at,
                )
            for row in self.connection.execute(
                """
                SELECT
                    COALESCE(target_card_id, target_card) AS entity_id,
                    COUNT(*) AS evidence_count
                FROM simulation_batch_results
                WHERE COALESCE(target_card_id, target_card) IS NOT NULL
                GROUP BY COALESCE(target_card_id, target_card)
                """
            ).fetchall():
                self.increment_evidence_count(
                    entity_type="card",
                    entity_id=row["entity_id"],
                    simulation=int(row["evidence_count"]),
                    updated_at=updated_at,
                )
        row = self.connection.execute("SELECT COUNT(*) AS count FROM evidence_counts").fetchone()
        return int(row["count"])
