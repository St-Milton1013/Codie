"""Persistence adapter for simulator batch results."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from codie.db.repositories.simulation import SimulationRepository

from .batch import BatchRunResult, BatchTraceSample


COMPLETED = "completed"
COMPLETED_WITH_UNSUPPORTED = "completed_with_unsupported"
INVALID_TARGET = "invalid_target"
LIMIT_EXCEEDED = "limit_exceeded"
FAILED = "failed"


@dataclass(frozen=True)
class PersistedSimulationBatch:
    batch_id: str
    result_id: int
    trace_ids: tuple[int, ...]

    def __post_init__(self) -> None:
        if not self.batch_id:
            raise ValueError("batch_id is required")
        if self.result_id <= 0:
            raise ValueError("result_id must be positive")
        object.__setattr__(self, "trace_ids", tuple(self.trace_ids))

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "result_id": self.result_id,
            "trace_ids": list(self.trace_ids),
        }


def persist_batch_run_result(
    repository: SimulationRepository,
    batch_result: BatchRunResult,
    *,
    batch_id: str | None = None,
    created_at: str | None = None,
    completed_at: str | None = None,
    decklist_source: str | None = None,
    elapsed_ms: int | None = None,
) -> PersistedSimulationBatch:
    created = created_at or repository.now()
    completed = completed_at or created
    rows = batch_result_to_repository_rows(
        batch_result,
        batch_id=batch_id,
        created_at=created,
        completed_at=completed,
        decklist_source=decklist_source,
        elapsed_ms=elapsed_ms,
    )
    trace_rows = [
        trace_sample_to_repository_row(
            sample,
            batch_id=rows["batch"]["batch_id"],
            result_id=None,
            created_at=created,
            game_lookup=_game_lookup(batch_result),
        )
        for sample in _all_trace_samples(batch_result)
    ]

    with repository.transaction(repository.connection, "simulation_persist"):
        persisted_batch_id = repository.create_batch(rows["batch"])
        result_id = repository.create_result(rows["result"])
        trace_ids = tuple(
            repository.create_trace({**trace, "result_id": result_id})
            for trace in trace_rows
        )
    return PersistedSimulationBatch(
        batch_id=persisted_batch_id,
        result_id=result_id,
        trace_ids=trace_ids,
    )


def batch_result_to_repository_rows(
    batch_result: BatchRunResult,
    *,
    batch_id: str | None = None,
    created_at: str,
    completed_at: str,
    decklist_source: str | None = None,
    elapsed_ms: int | None = None,
) -> dict[str, dict[str, Any]]:
    assigned_batch_id = batch_id or deterministic_batch_id(batch_result, generated_at=completed_at)
    raw_config = {
        "batch_config": batch_result.batch_config.to_dict(),
        "mulligan_policy": batch_result.mulligan_policy.to_dict(),
        "search_config": batch_result.search_config.to_dict(),
        "target_condition": batch_result.target_condition.to_dict(),
        "batch_version": batch_result.batch_config.batch_version,
        "base_seed": batch_result.batch_config.base_seed,
        "game_index_start": batch_result.batch_config.game_index_start,
    }
    raw_payload = {
        "games_completed": batch_result.games_completed,
        "success_count": batch_result.success_count,
        "failure_count": batch_result.failure_count,
        "unsupported_count": batch_result.unsupported_count,
        "invalid_target_count": batch_result.invalid_target_count,
        "limit_exceeded_count": batch_result.limit_exceeded_count,
        "success_rate": batch_result.success_rate,
        "unsupported_rate": batch_result.unsupported_rate,
        "average_mulligan_count": batch_result.average_mulligan_count,
        "sample_successful_traces": len(batch_result.sample_successful_traces),
        "sample_failed_traces": len(batch_result.sample_failed_traces),
        "sample_unsupported_traces": len(batch_result.sample_unsupported_traces),
        "generated_at": batch_result.generated_at,
        "unsupported_cards": list(batch_result.unsupported_cards),
        "unsupported_actions": list(batch_result.unsupported_actions),
    }
    missing_payload = {
        "unsupported_cards": list(batch_result.unsupported_cards),
        "unsupported_actions": list(batch_result.unsupported_actions),
    }
    return {
        "batch": {
            "batch_id": assigned_batch_id,
            "deck_hash": batch_result.deck_hash,
            "decklist_source": decklist_source,
            "games_requested": batch_result.games_requested,
            "games_completed": batch_result.games_completed,
            "min_mulligan_keep": batch_result.mulligan_policy.minimum_keep_size,
            "mulligan_mode": batch_result.mulligan_policy.policy_name,
            "elapsed_ms": elapsed_ms,
            "status": _batch_status(batch_result),
            "created_at": created_at,
            "completed_at": completed_at,
            "raw_config_json": _json(raw_config),
        },
        "result": {
            "batch_id": assigned_batch_id,
            "target_card": batch_result.target_condition.target_card,
            "target_card_id": batch_result.target_condition.target_card_id,
            "target_zone": batch_result.target_condition.target_zone,
            "turn": batch_result.target_condition.turn,
            "win_count": batch_result.success_count,
            "win_rate": batch_result.success_rate,
            "margin_of_error": None,
            "missing_cards_json": _json(missing_payload),
            "raw_payload_json": _json(raw_payload),
        },
    }


def trace_sample_to_repository_row(
    sample: BatchTraceSample,
    *,
    batch_id: str,
    result_id: int | None,
    created_at: str,
    game_lookup: dict[int, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    game = (game_lookup or {}).get(sample.game_index, {})
    return {
        "batch_id": batch_id,
        "result_id": result_id,
        "game_index": sample.game_index,
        "success": 1 if sample.success else 0,
        "mulligan_count": game.get("mulligan_count"),
        "opening_hand_json": _json(game.get("kept_hand", [])),
        "final_state_json": _json(
            {
                "search_status": sample.search_status,
                "unsupported_cards": game.get("unsupported_cards", []),
                "unsupported_actions": game.get("unsupported_actions", []),
            }
        ),
        "action_trace_json": _json(sample.trace),
        "created_at": created_at,
    }


def deterministic_batch_id(batch_result: BatchRunResult, *, generated_at: str | None = None) -> str:
    payload = {
        "deck_hash": batch_result.deck_hash,
        "target_condition": batch_result.target_condition.to_dict(),
        "batch_config": batch_result.batch_config.to_dict(),
        "mulligan_policy": batch_result.mulligan_policy.to_dict(),
        "search_config": batch_result.search_config.to_dict(),
        "games_completed": batch_result.games_completed,
        "generated_at": generated_at or batch_result.generated_at,
    }
    return "sha256:" + hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()


def _batch_status(batch_result: BatchRunResult) -> str:
    if batch_result.invalid_target_count:
        return INVALID_TARGET
    if batch_result.limit_exceeded_count:
        return LIMIT_EXCEEDED
    if batch_result.unsupported_count:
        return COMPLETED_WITH_UNSUPPORTED
    if batch_result.games_completed == batch_result.success_count + batch_result.failure_count:
        return COMPLETED
    return FAILED


def _all_trace_samples(batch_result: BatchRunResult) -> tuple[BatchTraceSample, ...]:
    return (
        *batch_result.sample_successful_traces,
        *batch_result.sample_failed_traces,
        *batch_result.sample_unsupported_traces,
    )


def _game_lookup(batch_result: BatchRunResult) -> dict[int, dict[str, Any]]:
    return {game.game_index: game.to_dict() for game in batch_result.game_results}


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
