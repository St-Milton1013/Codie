"""Repositories for regional metrics."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class RegionalRepository(BaseRepository):
    def create_commander_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "commander_signature", "updated_at"))
        return self.insert("regional_commander_metrics", metric)

    def create_card_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "oracle_id", "updated_at"))
        return self.insert("regional_card_metrics", metric)

    def upsert_card_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "oracle_id", "updated_at"))
        columns = (
            "region_code",
            "country_code",
            "time_window",
            "window_end_date",
            "oracle_id",
            "inclusion_rate",
            "weighted_inclusion_rate",
            "sample_size",
            "updated_at",
        )
        values = tuple(metric.get(column) for column in columns)
        self.connection.execute(
            """
            INSERT INTO regional_card_metrics (
                region_code, country_code, time_window, window_end_date, oracle_id,
                inclusion_rate, weighted_inclusion_rate, sample_size, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(region_code, country_code, time_window, window_end_date, oracle_id)
            DO UPDATE SET
                inclusion_rate = excluded.inclusion_rate,
                weighted_inclusion_rate = excluded.weighted_inclusion_rate,
                sample_size = excluded.sample_size,
                updated_at = excluded.updated_at
            """,
            values,
        )
        row = self.get_card_metric(
            str(metric["region_code"]),
            metric.get("country_code"),
            str(metric["time_window"]),
            str(metric["window_end_date"]),
            str(metric["oracle_id"]),
        )
        return int(row["metric_id"])

    def get_card_metric(
        self,
        region_code: str,
        country_code: str | None,
        time_window: str,
        window_end_date: str,
        oracle_id: str,
    ):
        if country_code is None:
            return self.connection.execute(
                """
                SELECT * FROM regional_card_metrics
                WHERE region_code = ? AND country_code IS NULL
                    AND time_window = ? AND window_end_date = ? AND oracle_id = ?
                """,
                (region_code, time_window, window_end_date, oracle_id),
            ).fetchone()
        return self.connection.execute(
            """
            SELECT * FROM regional_card_metrics
            WHERE region_code = ? AND country_code = ?
                AND time_window = ? AND window_end_date = ? AND oracle_id = ?
            """,
            (region_code, country_code, time_window, window_end_date, oracle_id),
        ).fetchone()

    def create_package_metric(self, metric: Mapping[str, Any]) -> int:
        self.require(metric, ("region_code", "time_window", "window_end_date", "package_id", "updated_at"))
        return self.insert("regional_package_metrics", metric)
