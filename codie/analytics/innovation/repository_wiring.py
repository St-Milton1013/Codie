"""Repository row wiring for innovation detection inputs."""

from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import date, timedelta
from typing import Any

from .innovation_detector import detect_innovations
from .innovation_filters import BASELINE_WINDOW_DAYS, InnovationFilter
from .innovation_models import InnovationObservation, InnovationSignal


def _row_value(row: Any, key: str) -> Any:
    try:
        return row[key]
    except (KeyError, IndexError, TypeError):
        try:
            return getattr(row, key)
        except AttributeError as exc:
            raise ValueError(f"{key} is required") from exc


def _required_text(row: Any, key: str) -> str:
    value = _row_value(row, key)
    if value in (None, ""):
        raise ValueError(f"{key} is required")
    return str(value)


def _optional_text(row: Any, key: str) -> str | None:
    value = _row_value(row, key)
    if value in (None, ""):
        return None
    return str(value)


def _stable_identity(row: Any, source_key: str, canonical_key: str, identity_name: str) -> str:
    source_value = _row_value(row, source_key)
    if source_value not in (None, ""):
        return f"{source_key.removesuffix('_id')}:{source_value}"
    canonical_value = _row_value(row, canonical_key)
    if canonical_value not in (None, ""):
        return f"{canonical_key.removesuffix('_id')}:{canonical_value}"
    raise ValueError(f"{identity_name} is required")


def _flag(row: Any, key: str) -> bool:
    return bool(_row_value(row, key) or 0)


def _optional_int(row: Any, key: str) -> int | None:
    value = _row_value(row, key)
    if value in (None, ""):
        return None
    return int(value)


def _parse_day(value: str | None, field_name: str) -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError as exc:
        raise ValueError(f"Invalid {field_name}: {value}") from exc


def _color_identity(value: Any) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    try:
        decoded = json.loads(str(value))
    except json.JSONDecodeError as exc:
        raise ValueError("color_identity_json must be valid JSON") from exc
    if not isinstance(decoded, list):
        raise ValueError("color_identity_json must decode to a list")
    return tuple(str(color) for color in decoded if str(color).strip())


def innovation_observations_from_rows(rows: Iterable[Any]) -> tuple[InnovationObservation, ...]:
    """Convert canonical repository rows into innovation detector observations."""
    observations: list[InnovationObservation] = []
    for row in rows:
        event_date = _required_text(row, "event_date")
        card_released_at = _optional_text(row, "card_released_at")
        _parse_day(event_date, "event_date")
        _parse_day(card_released_at, "card_released_at")
        observations.append(
            InnovationObservation(
                oracle_id=_required_text(row, "oracle_id"),
                scryfall_id=_optional_text(row, "scryfall_id"),
                card_name=_optional_text(row, "card_name"),
                type_line=_optional_text(row, "type_line"),
                color_identity=_color_identity(_row_value(row, "color_identity_json")),
                source_deck_id=_stable_identity(row, "source_deck_id", "canonical_deck_id", "deck identity"),
                source_event_id=_stable_identity(row, "source_event_id", "canonical_event_id", "event identity"),
                event_date=event_date,
                commander_signature=_optional_text(row, "commander_signature"),
                region_code=_optional_text(row, "region"),
                country_code=_optional_text(row, "country"),
                placement=_optional_int(row, "placement"),
                top_cut=_flag(row, "top_cut_made") or _flag(row, "final_pod"),
                winner=_flag(row, "winner"),
                player_count=_optional_int(row, "player_count"),
                card_released_at=card_released_at,
            )
        )
    return tuple(observations)


def _repository_window_start(filters: InnovationFilter) -> str | None:
    window_end = _parse_day(filters.window_end_date, "window_end_date")
    assert window_end is not None
    baseline_days = BASELINE_WINDOW_DAYS.get(filters.baseline_window)
    if baseline_days is None:
        return None
    recent_start = window_end - timedelta(days=filters.recent_window_days)
    return (recent_start - timedelta(days=baseline_days)).isoformat()


def detect_innovations_from_repository(
    repository: Any,
    filters: InnovationFilter,
    *,
    generated_at: str,
) -> tuple[InnovationSignal, ...]:
    """Read canonical innovation observations from a repository and run detection."""
    rows = repository.list_innovation_observation_rows(
        window_start_date=_repository_window_start(filters),
        window_end_date=filters.window_end_date,
    )
    return detect_innovations(
        list(innovation_observations_from_rows(rows)),
        filters,
        generated_at=generated_at,
    )
