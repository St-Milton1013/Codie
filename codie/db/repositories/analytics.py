"""Repositories for derived metrics and evidence counts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class AnalyticsRepository(BaseRepository):
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
        cursor = self.connection.execute(
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
        if cursor.lastrowid:
            return int(cursor.lastrowid)
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
