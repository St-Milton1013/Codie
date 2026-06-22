"""Deterministic tournament weighting formulas."""

from __future__ import annotations

from datetime import date
from math import log2


class AnalyticsError(ValueError):
    """Raised when analytics input cannot be evaluated safely."""


HALF_LIFE_DAYS = {
    "30d": 30,
    "90d": 60,
    "365d": 180,
}

TIME_WINDOW_ALIASES = {
    "30d": "30d",
    "30_day": "30d",
    "30-day": "30d",
    "90d": "90d",
    "90_day": "90d",
    "90-day": "90d",
    "365d": "365d",
    "1y": "365d",
    "1_year": "365d",
    "1-year": "365d",
}

ALL_TIME_WINDOWS = {"all", "all_time", "all-time", "lifetime"}


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value[:10])
    except ValueError as exc:
        raise AnalyticsError(f"Invalid analytics date: {value}") from exc


def normalize_time_window(time_window: str) -> str:
    normalized = time_window.strip().lower().replace(" ", "_")
    if normalized in ALL_TIME_WINDOWS:
        return "all_time"
    if normalized in TIME_WINDOW_ALIASES:
        return TIME_WINDOW_ALIASES[normalized]
    raise AnalyticsError(f"Unsupported time window: {time_window}")


def event_size_weight(player_count: int | None, *, minimum_player_count: int = 16) -> float:
    """Return the constitution event-size weight.

    Unknown or below-threshold events are ineligible for weighted analytics and
    receive zero weight.
    """

    if player_count is None or player_count < minimum_player_count:
        return 0.0
    return _clamp(log2(player_count) / log2(128), 0.25, 1.50)


def placement_weight(placement: int | None = None, placement_label: str | None = None) -> float:
    """Return deterministic placement weight with label fallbacks."""

    if placement is not None:
        if placement <= 1:
            return 1.0
        if placement == 2:
            return 0.90
        if placement <= 4:
            return 0.80
        if placement <= 16:
            return 0.60
        return 0.30

    label = (placement_label or "").strip().lower().replace("-", " ")
    if label in {"winner", "champion", "1st", "first"}:
        return 1.0
    if "top 4" in label or "top4" in label or label in {"semifinalist", "final pod"}:
        return 0.80
    if "top 16" in label or "top16" in label or "top cut" in label or "topcut" in label:
        return 0.60
    return 0.30


def recency_weight(event_date: str | None, window_end_date: str, time_window: str) -> float:
    """Return recency decay for supported current-meta windows."""

    normalized_window = normalize_time_window(time_window)
    if normalized_window == "all_time":
        return 1.0
    if not event_date:
        return 0.0

    event_day = _parse_date(event_date)
    window_end = _parse_date(window_end_date)
    days_old = max(0, (window_end - event_day).days)
    half_life_days = HALF_LIFE_DAYS[normalized_window]
    return 0.5 ** (days_old / half_life_days)


def source_confidence_weight(source_confidence: float | None) -> float:
    """Clamp source confidence to a usable multiplier."""

    if source_confidence is None:
        return 1.0
    return _clamp(float(source_confidence), 0.0, 1.0)


def decklist_completeness_weight(card_count: int | None) -> float:
    """Return a deterministic decklist completeness multiplier."""

    if not card_count:
        return 0.0
    if card_count >= 98:
        return 1.0
    if card_count >= 90:
        return 0.85
    return 0.50


def final_entry_weight(
    *,
    player_count: int | None,
    placement: int | None,
    placement_label: str | None,
    event_date: str | None,
    window_end_date: str,
    time_window: str,
    source_confidence: float | None,
    card_count: int | None,
    minimum_player_count: int = 16,
) -> float:
    """Return the final tournament entry weight."""

    return (
        event_size_weight(player_count, minimum_player_count=minimum_player_count)
        * placement_weight(placement, placement_label)
        * recency_weight(event_date, window_end_date, time_window)
        * source_confidence_weight(source_confidence)
        * decklist_completeness_weight(card_count)
    )
