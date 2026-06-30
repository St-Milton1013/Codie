"""Repositories for deterministic simulation persistence."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class SimulationRepository(BaseRepository):
    def create_batch(self, batch: Mapping[str, Any]) -> str:
        self.require(batch, ("batch_id", "deck_hash", "games_requested", "min_mulligan_keep", "status", "created_at"))
        self.insert("simulation_batches", batch)
        return str(batch["batch_id"])

    def create_result(self, result: Mapping[str, Any]) -> int:
        self.require(result, ("batch_id", "target_card", "target_zone", "turn", "win_count", "win_rate"))
        return self.insert("simulation_batch_results", result)

    def create_trace(self, trace: Mapping[str, Any]) -> int:
        self.require(trace, ("batch_id", "created_at"))
        return self.insert("simulation_traces", trace)

    def upsert_line_review(self, review: Mapping[str, Any]) -> str:
        self.require(
            review,
            (
                "review_id",
                "challenge_id",
                "deck_hash",
                "target_card",
                "target_turn",
                "simulator_success",
                "simulator_status",
                "action_trace_json",
                "review_status",
                "review_reason",
                "affected_cards_json",
                "affected_actions_json",
                "created_at",
            ),
        )
        self.connection.execute(
            """
            INSERT INTO simulation_line_reviews (
                review_id,
                challenge_id,
                batch_id,
                result_id,
                trace_id,
                deck_hash,
                target_card,
                target_turn,
                simulator_success,
                simulator_status,
                action_trace_json,
                review_status,
                review_reason,
                review_note,
                affected_cards_json,
                affected_actions_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(review_id) DO UPDATE SET
                challenge_id = excluded.challenge_id,
                batch_id = excluded.batch_id,
                result_id = excluded.result_id,
                trace_id = excluded.trace_id,
                deck_hash = excluded.deck_hash,
                target_card = excluded.target_card,
                target_turn = excluded.target_turn,
                simulator_success = excluded.simulator_success,
                simulator_status = excluded.simulator_status,
                action_trace_json = excluded.action_trace_json,
                review_status = excluded.review_status,
                review_reason = excluded.review_reason,
                review_note = excluded.review_note,
                affected_cards_json = excluded.affected_cards_json,
                affected_actions_json = excluded.affected_actions_json,
                created_at = excluded.created_at
            """,
            (
                review["review_id"],
                review["challenge_id"],
                review.get("batch_id"),
                review.get("result_id"),
                review.get("trace_id"),
                review["deck_hash"],
                review["target_card"],
                review["target_turn"],
                review["simulator_success"],
                review["simulator_status"],
                review["action_trace_json"],
                review["review_status"],
                review["review_reason"],
                review.get("review_note"),
                review["affected_cards_json"],
                review["affected_actions_json"],
                review["created_at"],
            ),
        )
        return str(review["review_id"])

    def get_line_review(self, review_id: str):
        return self.fetch_by_id("simulation_line_reviews", "review_id", review_id)

    def list_line_reviews_for_challenge(self, challenge_id: str):
        cursor = self.connection.execute(
            """
            SELECT *
            FROM simulation_line_reviews
            WHERE challenge_id = ?
            ORDER BY created_at, review_id
            """,
            (challenge_id,),
        )
        return cursor.fetchall()

    def list_line_reviews_for_accuracy(self, filters: Mapping[str, Any] | None = None):
        filters = filters or {}
        clauses = []
        values = []
        exact_filters = {
            "deck_hash": "deck_hash",
            "target_card": "target_card",
            "batch_id": "batch_id",
            "challenge_id": "challenge_id",
            "trace_id": "trace_id",
            "review_status": "review_status",
            "review_reason": "review_reason",
        }
        for filter_key, column in exact_filters.items():
            value = filters.get(filter_key)
            if value in (None, ""):
                continue
            clauses.append(f"{column} = ?")
            values.append(value)
        created_at_from = filters.get("created_at_from")
        if created_at_from not in (None, ""):
            clauses.append("created_at >= ?")
            values.append(created_at_from)
        created_at_to = filters.get("created_at_to")
        if created_at_to not in (None, ""):
            clauses.append("created_at <= ?")
            values.append(created_at_to)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        cursor = self.connection.execute(
            f"""
            SELECT *
            FROM simulation_line_reviews
            {where}
            ORDER BY created_at, review_id
            """,
            tuple(values),
        )
        return cursor.fetchall()
