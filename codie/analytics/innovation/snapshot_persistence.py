"""Persistence helpers for innovation detector snapshot outputs."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass

from codie.db.repositories import AnalyticsRepository

from .innovation_models import InnovationSignal


@dataclass(frozen=True)
class InnovationSnapshotSpec:
    generated_at: str
    config: dict[str, object]
    notes: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.generated_at, "generated_at")
        if not isinstance(self.config, dict) or not self.config:
            raise ValueError("config is required")


@dataclass(frozen=True)
class PersistedInnovationSnapshot:
    innovation_snapshot_run_id: int
    signal_count: int
    config_hash: str


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def config_json(config: dict[str, object]) -> str:
    return json.dumps(config, sort_keys=True, separators=(",", ":"))


def config_hash(config: dict[str, object]) -> str:
    return hashlib.sha256(config_json(config).encode("utf-8")).hexdigest()


def innovation_snapshot_run_row(spec: InnovationSnapshotSpec) -> dict[str, object | None]:
    serialized = config_json(spec.config)
    return {
        "generated_at": spec.generated_at,
        "config_hash": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "config_json": serialized,
        "notes": spec.notes,
    }


def innovation_snapshot_item_row(signal: InnovationSignal) -> dict[str, object | None]:
    return {
        "innovation_id": signal.innovation_id,
        "oracle_id": signal.oracle_id,
        "scryfall_id": signal.scryfall_id,
        "commander_signature": signal.commander_signature,
        "region_code": signal.region_code,
        "innovation_type": signal.innovation_type,
        "recent_window": signal.recent_window,
        "baseline_window": signal.baseline_window,
        "recent_inclusion_rate": signal.recent_inclusion_rate,
        "baseline_inclusion_rate": signal.baseline_inclusion_rate,
        "usage_delta": signal.usage_delta,
        "recent_topcut_count": signal.recent_topcut_count,
        "recent_winner_count": signal.recent_winner_count,
        "first_recent_seen_at": signal.first_recent_seen_at,
        "last_seen_before_recent_window": signal.last_seen_before_recent_window,
        "card_released_at": signal.card_released_at,
        "is_new_release": 1 if signal.is_new_release else 0,
        "sample_size": signal.sample_size,
        "confidence_score": signal.confidence_score,
        "source_event_ids_json": signal.source_event_ids_json,
        "source_deck_ids_json": signal.source_deck_ids_json,
        "generated_at": signal.generated_at,
    }


def persist_innovation_snapshot(
    *,
    repository: AnalyticsRepository,
    snapshot: InnovationSnapshotSpec,
    signals: Iterable[InnovationSignal],
) -> PersistedInnovationSnapshot:
    signal_tuple = tuple(signals)
    run_row = innovation_snapshot_run_row(snapshot)
    innovation_snapshot_run_id = repository.replace_innovation_snapshot(
        run=run_row,
        items=tuple(innovation_snapshot_item_row(signal) for signal in signal_tuple),
    )
    return PersistedInnovationSnapshot(
        innovation_snapshot_run_id=innovation_snapshot_run_id,
        signal_count=len(signal_tuple),
        config_hash=str(run_row["config_hash"]),
    )
