"""Repositories for recommendation run persistence."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .base import BaseRepository


class RecommendationRepository(BaseRepository):
    def create_recommendation_run(self, run: Mapping[str, Any]) -> int:
        self.require(run, ("input_deck_hash", "generated_at"))
        columns = (
            "input_deck_hash",
            "commander_hash",
            "generated_at",
            "config_json",
            "source_snapshot_id",
            "notes",
        )
        return self.insert("recommendation_runs", {column: run.get(column) for column in columns})

    def add_recommendation_candidate(self, candidate: Mapping[str, Any]) -> int:
        self.require(candidate, ("recommendation_run_id", "candidate_type", "evidence_json"))
        columns = (
            "recommendation_run_id",
            "scryfall_id",
            "oracle_id",
            "candidate_type",
            "recommendation_score",
            "inclusion_rate",
            "lift_score",
            "confidence_score",
            "similarity_score",
            "package_completion_score",
            "generic_staple_penalty",
            "evidence_json",
            "explanation_text",
        )
        return self.insert("recommendation_candidates", {column: candidate.get(column) for column in columns})

    def list_run_candidates(self, recommendation_run_id: int):
        return self.connection.execute(
            """
            SELECT *
            FROM recommendation_candidates
            WHERE recommendation_run_id = ?
            ORDER BY recommendation_score DESC, oracle_id, candidate_id
            """,
            (recommendation_run_id,),
        ).fetchall()

    def get_recommendation_run(self, recommendation_run_id: int):
        return self.fetch_by_id("recommendation_runs", "recommendation_run_id", recommendation_run_id)

    def find_recommendation_runs(self, *, input_deck_hash: str, generated_at: str):
        return self.connection.execute(
            """
            SELECT *
            FROM recommendation_runs
            WHERE input_deck_hash = ? AND generated_at = ?
            ORDER BY recommendation_run_id
            """,
            (input_deck_hash, generated_at),
        ).fetchall()

    def delete_recommendation_run(self, recommendation_run_id: int) -> None:
        self.connection.execute(
            "DELETE FROM recommendation_candidates WHERE recommendation_run_id = ?",
            (recommendation_run_id,),
        )
        self.connection.execute(
            "DELETE FROM recommendation_runs WHERE recommendation_run_id = ?",
            (recommendation_run_id,),
        )

    def replace_recommendation_run(
        self,
        *,
        run: Mapping[str, Any],
        candidates: Sequence[Mapping[str, Any]],
    ) -> int:
        self.require(run, ("input_deck_hash", "generated_at"))
        with self.transaction(self.connection, "recommendation_rebuild"):
            existing_runs = self.find_recommendation_runs(
                input_deck_hash=str(run["input_deck_hash"]),
                generated_at=str(run["generated_at"]),
            )
            for existing_run in existing_runs:
                self.delete_recommendation_run(int(existing_run["recommendation_run_id"]))
            recommendation_run_id = self.create_recommendation_run(run)
            for candidate in candidates:
                candidate_data = dict(candidate)
                candidate_data["recommendation_run_id"] = recommendation_run_id
                self.add_recommendation_candidate(candidate_data)
        return recommendation_run_id
