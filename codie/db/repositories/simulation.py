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
