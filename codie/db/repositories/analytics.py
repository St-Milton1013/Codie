"""Repositories for derived metrics and evidence counts."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from datetime import date
from typing import Any

from .base import BaseRepository, RepositoryError


_OBSERVATION_SCOPES = {"all", "top_16", "winners"}
_PRIVATE_RELATIONSHIP_KEYS = {
    "raw_import_text",
    "raw_deck_text",
    "private_note",
    "private_notes",
    "user_notes",
}
_PRIVATE_RELATIONSHIP_KEY_MARKERS = (
    "private",
    "usernote",
    "rawdeck",
    "rawimport",
    "importeddecktext",
)
_MAX_RELATIONSHIP_JSON_DEPTH = 20
_RELATIONSHIP_METRICS = {
    "support",
    "directional_confidence",
    "dependence_delta",
    "lift",
    "leverage",
    "jaccard_similarity",
    "pmi",
}


def _canonical_json(
    value: Any,
    field_name: str,
    *,
    expected_type: type[dict] | type[list],
) -> str:
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RepositoryError(f"{field_name} must contain valid JSON") from exc
    else:
        decoded = value

    if not isinstance(decoded, expected_type):
        expected_name = "object" if expected_type is dict else "array"
        raise RepositoryError(f"{field_name} must be a JSON {expected_name}")

    def validate(item: Any, depth: int = 0) -> None:
        if depth > _MAX_RELATIONSHIP_JSON_DEPTH:
            raise RepositoryError(f"{field_name} exceeds maximum JSON depth")
        if isinstance(item, Mapping):
            for key, nested in item.items():
                if not isinstance(key, str):
                    raise RepositoryError(f"{field_name} object keys must be strings")
                normalized_key = "".join(character for character in key.casefold() if character.isalnum())
                if (
                    key.casefold() in _PRIVATE_RELATIONSHIP_KEYS
                    or any(marker in normalized_key for marker in _PRIVATE_RELATIONSHIP_KEY_MARKERS)
                ):
                    raise RepositoryError(f"{field_name} contains private user data")
                validate(nested, depth + 1)
        elif isinstance(item, (list, tuple)):
            for nested in item:
                validate(nested, depth + 1)
        elif isinstance(item, float) and not math.isfinite(item):
            raise RepositoryError(f"{field_name} numbers must be finite")
        elif item is not None and not isinstance(item, (str, int, float, bool)):
            raise RepositoryError(f"{field_name} must be JSON-compatible")

    validate(decoded)
    return json.dumps(decoded, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _same_row(row: Mapping[str, Any], data: Mapping[str, Any], columns: tuple[str, ...]) -> bool:
    return all(row[column] == data.get(column) for column in columns)


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

    def create_innovation_snapshot_run(self, run: Mapping[str, Any]) -> int:
        self.require(run, ("generated_at", "config_hash", "config_json"))
        columns = ("generated_at", "config_hash", "config_json", "notes")
        return self.insert("innovation_snapshot_runs", {column: run.get(column) for column in columns})

    def add_innovation_snapshot_item(self, item: Mapping[str, Any]) -> int:
        self.require(
            item,
            (
                "innovation_snapshot_run_id",
                "innovation_id",
                "oracle_id",
                "innovation_type",
                "recent_window",
                "baseline_window",
                "first_recent_seen_at",
                "source_event_ids_json",
                "source_deck_ids_json",
                "generated_at",
            ),
        )
        columns = (
            "innovation_snapshot_run_id",
            "innovation_id",
            "oracle_id",
            "scryfall_id",
            "commander_signature",
            "region_code",
            "innovation_type",
            "recent_window",
            "baseline_window",
            "recent_inclusion_rate",
            "baseline_inclusion_rate",
            "usage_delta",
            "recent_topcut_count",
            "recent_winner_count",
            "first_recent_seen_at",
            "last_seen_before_recent_window",
            "card_released_at",
            "is_new_release",
            "sample_size",
            "confidence_score",
            "source_event_ids_json",
            "source_deck_ids_json",
            "generated_at",
        )
        return self.insert("innovation_snapshot_items", {column: item.get(column) for column in columns})

    def find_innovation_snapshot_runs(self, *, generated_at: str, config_hash: str):
        return self.connection.execute(
            """
            SELECT *
            FROM innovation_snapshot_runs
            WHERE generated_at = ? AND config_hash = ?
            ORDER BY innovation_snapshot_run_id
            """,
            (generated_at, config_hash),
        ).fetchall()

    def get_innovation_snapshot_run(self, innovation_snapshot_run_id: int):
        return self.fetch_by_id(
            "innovation_snapshot_runs",
            "innovation_snapshot_run_id",
            innovation_snapshot_run_id,
        )

    def list_innovation_snapshot_items(self, innovation_snapshot_run_id: int):
        return self.connection.execute(
            """
            SELECT *
            FROM innovation_snapshot_items
            WHERE innovation_snapshot_run_id = ?
            ORDER BY innovation_type, oracle_id, commander_signature, region_code, innovation_id
            """,
            (innovation_snapshot_run_id,),
        ).fetchall()

    def delete_innovation_snapshot_run(self, innovation_snapshot_run_id: int) -> None:
        self.connection.execute(
            "DELETE FROM innovation_snapshot_items WHERE innovation_snapshot_run_id = ?",
            (innovation_snapshot_run_id,),
        )
        self.connection.execute(
            "DELETE FROM innovation_snapshot_runs WHERE innovation_snapshot_run_id = ?",
            (innovation_snapshot_run_id,),
        )

    def replace_innovation_snapshot(
        self,
        *,
        run: Mapping[str, Any],
        items: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...],
    ) -> int:
        self.require(run, ("generated_at", "config_hash", "config_json"))
        with self.transaction(self.connection, "innovation_snapshot_rebuild"):
            existing_runs = self.find_innovation_snapshot_runs(
                generated_at=str(run["generated_at"]),
                config_hash=str(run["config_hash"]),
            )
            for existing_run in existing_runs:
                self.delete_innovation_snapshot_run(int(existing_run["innovation_snapshot_run_id"]))
            innovation_snapshot_run_id = self.create_innovation_snapshot_run(run)
            for item in items:
                item_data = dict(item)
                item_data["innovation_snapshot_run_id"] = innovation_snapshot_run_id
                self.add_innovation_snapshot_item(item_data)
        return innovation_snapshot_run_id

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

    def insert_relationship_population_spec(self, spec: Mapping[str, Any]) -> int:
        required = (
            "population_spec_version",
            "population_spec_hash",
            "observation_unit",
            "scope_type",
            "deduplication_policy",
            "concentration_policy",
            "spec_json",
            "created_at",
        )
        self.require(spec, required)
        data = dict(spec)
        data["spec_json"] = _canonical_json(
            data["spec_json"], "spec_json", expected_type=dict
        )
        columns = tuple(data)
        existing = self.connection.execute(
            """
            SELECT * FROM relationship_population_specs
            WHERE population_spec_hash = ? AND population_spec_version = ?
            """,
            (data["population_spec_hash"], data["population_spec_version"]),
        ).fetchone()
        if existing is not None:
            if not _same_row(existing, data, columns):
                raise RepositoryError("Conflicting immutable population specification identity")
            return int(existing["population_spec_id"])
        return self.insert("relationship_population_specs", data)

    def get_relationship_population_spec(
        self, population_spec_hash: str, population_spec_version: str
    ):
        return self.connection.execute(
            """
            SELECT * FROM relationship_population_specs
            WHERE population_spec_hash = ? AND population_spec_version = ?
            """,
            (population_spec_hash, population_spec_version),
        ).fetchone()

    def insert_relationship_population_manifest(
        self, manifest: Mapping[str, Any], members: list[Mapping[str, Any]]
    ) -> int:
        required = (
            "population_manifest_version",
            "population_manifest_hash",
            "population_spec_id",
            "population_spec_version",
            "population_spec_hash",
            "source_snapshot_refs_json",
            "candidate_population_count",
            "usable_population_count",
            "unknown_or_excluded_count",
            "deduplicated_population_count",
            "generated_at",
        )
        self.require(manifest, required)
        data = dict(manifest)
        data["source_snapshot_refs_json"] = _canonical_json(
            data["source_snapshot_refs_json"],
            "source_snapshot_refs_json",
            expected_type=list,
        )
        for field in (
            "candidate_population_count",
            "usable_population_count",
            "unknown_or_excluded_count",
            "deduplicated_population_count",
        ):
            if int(data[field]) < 0:
                raise RepositoryError(f"{field} must be non-negative")
        existing = self.connection.execute(
            """
            SELECT * FROM relationship_population_manifests
            WHERE population_manifest_hash = ? AND population_manifest_version = ?
            """,
            (data["population_manifest_hash"], data["population_manifest_version"]),
        ).fetchone()
        if existing is not None:
            if not _same_row(existing, data, tuple(data)):
                raise RepositoryError("Conflicting immutable population manifest identity")
            existing_members = self.list_relationship_population_members(
                int(existing["population_manifest_id"])
            )
            normalized_members = []
            for sequence, member in enumerate(members):
                normalized = dict(member)
                normalized.setdefault("member_sequence", sequence)
                normalized_members.append(normalized)
            if len(existing_members) != len(normalized_members) or any(
                not _same_row(row, member, tuple(member))
                for row, member in zip(existing_members, sorted(
                    normalized_members, key=lambda item: int(item["member_sequence"])
                ))
            ):
                raise RepositoryError("Conflicting immutable population manifest members")
            return int(existing["population_manifest_id"])

        with BaseRepository.transaction(self.connection, "relationship_manifest"):
            manifest_id = self.insert("relationship_population_manifests", data)
            for sequence, member in enumerate(members):
                member_data = dict(member)
                member_data.setdefault("member_sequence", sequence)
                member_data["population_manifest_id"] = manifest_id
                self.require(
                    member_data,
                    (
                        "observation_unit_type",
                        "observation_unit_id",
                        "inclusion_status",
                        "deduplication_key",
                    ),
                )
                self.insert("relationship_population_members", member_data)
        return manifest_id

    def get_relationship_population_manifest(self, population_manifest_id: int):
        return self.fetch_by_id(
            "relationship_population_manifests",
            "population_manifest_id",
            population_manifest_id,
        )

    def list_relationship_population_members(self, population_manifest_id: int):
        return self.connection.execute(
            """
            SELECT * FROM relationship_population_members
            WHERE population_manifest_id = ?
            ORDER BY member_sequence, population_member_id
            """,
            (population_manifest_id,),
        ).fetchall()

    def insert_relationship_measurement(
        self, measurement: Mapping[str, Any], metrics: list[Mapping[str, Any]]
    ) -> int:
        required = (
            "relationship_measurement_version",
            "relationship_measurement_hash",
            "relationship_type",
            "source_endpoint_type",
            "source_endpoint_id",
            "target_endpoint_type",
            "target_endpoint_id",
            "directionality",
            "population_manifest_id",
            "population_manifest_version",
            "N",
            "nA",
            "nB",
            "nAB",
            "candidate_population_count",
            "usable_population_count",
            "unknown_or_excluded_count",
            "deduplicated_population_count",
            "observed_co_occurrence",
            "expected_co_occurrence",
            "metric_bundle_version",
            "provenance_refs_json",
            "caveat_refs_json",
            "generated_at",
        )
        self.require(measurement, required)
        data = dict(measurement)
        data["provenance_refs_json"] = _canonical_json(
            data["provenance_refs_json"], "provenance_refs_json", expected_type=list
        )
        data["caveat_refs_json"] = _canonical_json(
            data["caveat_refs_json"], "caveat_refs_json", expected_type=list
        )
        n, na, nb, nab = (int(data[key]) for key in ("N", "nA", "nB", "nAB"))
        if n <= 0 or not (0 <= nab <= na <= n and 0 <= nab <= nb <= n):
            raise RepositoryError("Relationship counts violate N/nA/nB/nAB invariants")
        existing = self.connection.execute(
            """
            SELECT * FROM relationship_measurements
            WHERE relationship_measurement_hash = ?
              AND relationship_measurement_version = ?
            """,
            (
                data["relationship_measurement_hash"],
                data["relationship_measurement_version"],
            ),
        ).fetchone()
        if existing is not None:
            if not _same_row(existing, data, tuple(data)):
                raise RepositoryError("Conflicting immutable relationship measurement identity")
            existing_metrics = self.list_relationship_measurement_metrics(
                int(existing["relationship_measurement_id"])
            )
            normalized_metrics = sorted(
                (dict(metric) for metric in metrics),
                key=lambda item: (
                    str(item["metric_name"]),
                    str(item["orientation"]),
                    str(item["metric_version"]),
                ),
            )
            if len(existing_metrics) != len(normalized_metrics) or any(
                not _same_row(row, metric, tuple(metric))
                for row, metric in zip(existing_metrics, normalized_metrics)
            ):
                raise RepositoryError("Conflicting immutable relationship measurement metrics")
            return int(existing["relationship_measurement_id"])

        with BaseRepository.transaction(self.connection, "relationship_measurement"):
            measurement_id = self.insert("relationship_measurements", data)
            for metric in metrics:
                metric_data = dict(metric)
                metric_data["relationship_measurement_id"] = measurement_id
                self.require(metric_data, ("metric_name", "metric_version", "orientation"))
                if metric_data["metric_name"] not in _RELATIONSHIP_METRICS:
                    raise RepositoryError("Unsupported relationship metric name")
                value = metric_data.get("metric_value")
                reason = metric_data.get("undefined_reason")
                if (value is None) == (reason in (None, "")):
                    raise RepositoryError(
                        "Metric value and undefined reason must be mutually exclusive"
                    )
                self.insert("relationship_measurement_metrics", metric_data)
        return measurement_id

    def get_relationship_measurement(self, relationship_measurement_id: int):
        return self.fetch_by_id(
            "relationship_measurements",
            "relationship_measurement_id",
            relationship_measurement_id,
        )

    def list_relationship_measurements(
        self,
        *,
        population_manifest_id: int | None = None,
        source_endpoint_id: str | None = None,
        target_endpoint_id: str | None = None,
    ):
        filters: list[str] = []
        params: list[Any] = []
        for column, value in (
            ("population_manifest_id", population_manifest_id),
            ("source_endpoint_id", source_endpoint_id),
            ("target_endpoint_id", target_endpoint_id),
        ):
            if value is not None:
                filters.append(f"{column} = ?")
                params.append(value)
        where = f"WHERE {' AND '.join(filters)}" if filters else ""
        return self.connection.execute(
            f"""
            SELECT * FROM relationship_measurements
            {where}
            ORDER BY generated_at, relationship_measurement_id
            """,
            tuple(params),
        ).fetchall()

    def list_relationship_measurement_metrics(self, relationship_measurement_id: int):
        return self.connection.execute(
            """
            SELECT * FROM relationship_measurement_metrics
            WHERE relationship_measurement_id = ?
            ORDER BY metric_name, orientation, metric_version
            """,
            (relationship_measurement_id,),
        ).fetchall()
