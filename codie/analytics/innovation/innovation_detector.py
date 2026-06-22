"""Evidence-first innovation detection over canonical tournament observations."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date, timedelta
from typing import Any

from .innovation_filters import BASELINE_WINDOW_DAYS, InnovationFilter
from .innovation_models import InnovationObservation, InnovationSignal


FORBIDDEN_INNOVATION_WORDING = (
    "new tech",
    "is correct",
    "breaks the format",
    "secretly optimal",
    "should play",
)


def _parse_day(value: str | None, field_name: str = "date") -> date | None:
    if value in (None, ""):
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError as exc:
        raise ValueError(f"Invalid {field_name}: {value}") from exc


def _window_label(days: int) -> str:
    return f"{days}d"


def _is_top_performing(observation: InnovationObservation, filters: InnovationFilter) -> bool:
    if observation.top_cut or observation.winner:
        return True
    return observation.placement is not None and observation.placement <= filters.minimum_placement


def _matches_filters(observation: InnovationObservation, filters: InnovationFilter) -> bool:
    if observation.player_count is not None and observation.player_count < filters.minimum_event_size:
        return False
    if filters.commander_signature and observation.commander_signature != filters.commander_signature:
        return False
    if filters.region_code and observation.region_code != filters.region_code:
        return False
    if filters.card_type_contains:
        type_line = (observation.type_line or "").lower()
        if not any(fragment in type_line for fragment in filters.card_type_contains):
            return False
    if filters.color_identity:
        allowed = set(filters.color_identity)
        if not set(observation.color_identity).issubset(allowed):
            return False
    return True


def _distinct_decks(observations: list[InnovationObservation]) -> set[str]:
    return {observation.source_deck_id for observation in observations}


def _rate(count: int, total: int) -> float | None:
    if total == 0:
        return None
    return count / total


def _source_json(values: set[str]) -> str:
    return json.dumps(sorted(values), separators=(",", ":"))


def _stable_id(
    *,
    innovation_type: str,
    oracle_id: str,
    commander_signature: str | None,
    region_code: str | None,
    recent_window: str,
    baseline_window: str,
) -> str:
    payload = "|".join(
        (
            innovation_type,
            oracle_id,
            commander_signature or "",
            region_code or "",
            recent_window,
            baseline_window,
        )
    )
    return "innovation:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _confidence(sample_size: int) -> float:
    return min(1.0, sample_size / 30)


def _signal(
    *,
    innovation_type: str,
    oracle_id: str,
    scryfall_id: str | None,
    commander_signature: str | None,
    region_code: str | None,
    recent_window: str,
    baseline_window: str,
    recent_rate: float | None,
    baseline_rate: float | None,
    recent_observations: list[InnovationObservation],
    historical_before_recent: list[InnovationObservation],
    card_released_at: str | None,
    is_new_release: bool,
    generated_at: str,
) -> InnovationSignal:
    recent_dates = sorted(observation.event_date for observation in recent_observations)
    recent_decks = _distinct_decks(recent_observations)
    topcut_decks = {
        observation.source_deck_id
        for observation in recent_observations
        if observation.top_cut or (observation.placement is not None and observation.placement <= 16)
    }
    winner_decks = {observation.source_deck_id for observation in recent_observations if observation.winner}
    historical_dates = sorted(observation.event_date for observation in historical_before_recent)
    source_events = {observation.source_event_id for observation in recent_observations}
    usage_delta = None if recent_rate is None or baseline_rate is None else recent_rate - baseline_rate
    return InnovationSignal(
        innovation_id=_stable_id(
            innovation_type=innovation_type,
            oracle_id=oracle_id,
            commander_signature=commander_signature,
            region_code=region_code,
            recent_window=recent_window,
            baseline_window=baseline_window,
        ),
        oracle_id=oracle_id,
        scryfall_id=scryfall_id,
        commander_signature=commander_signature,
        region_code=region_code,
        innovation_type=innovation_type,
        recent_window=recent_window,
        baseline_window=baseline_window,
        recent_inclusion_rate=recent_rate,
        baseline_inclusion_rate=baseline_rate,
        usage_delta=usage_delta,
        recent_topcut_count=len(topcut_decks),
        recent_winner_count=len(winner_decks),
        first_recent_seen_at=recent_dates[0],
        last_seen_before_recent_window=historical_dates[-1] if historical_dates else None,
        card_released_at=card_released_at,
        is_new_release=is_new_release,
        sample_size=len(recent_decks),
        confidence_score=_confidence(len(recent_decks)),
        source_event_ids_json=_source_json(source_events),
        source_deck_ids_json=_source_json(recent_decks),
        generated_at=generated_at,
    )


def _card_metadata(observations: list[InnovationObservation]) -> tuple[str | None, str | None, bool]:
    scryfall_ids = sorted({observation.scryfall_id for observation in observations if observation.scryfall_id})
    releases = sorted({observation.card_released_at for observation in observations if observation.card_released_at})
    released_at = releases[0] if releases else None
    return (scryfall_ids[0] if scryfall_ids else None, released_at, bool(released_at))


def _append_if_new(signals: list[InnovationSignal], signal: InnovationSignal) -> None:
    if signal.innovation_id not in {existing.innovation_id for existing in signals}:
        signals.append(signal)


def detect_innovations(
    observations: list[InnovationObservation],
    filters: InnovationFilter,
    *,
    generated_at: str,
) -> tuple[InnovationSignal, ...]:
    """Detect emerging, breakout, resurgence, commander, and regional evidence signals."""
    if not isinstance(generated_at, str) or not generated_at.strip():
        raise ValueError("generated_at is required")
    window_end = _parse_day(filters.window_end_date, "window_end_date")
    assert window_end is not None
    recent_start = window_end - timedelta(days=filters.recent_window_days)
    baseline_days = BASELINE_WINDOW_DAYS.get(filters.baseline_window)
    baseline_start = None if baseline_days is None else recent_start - timedelta(days=baseline_days)
    recent_window = _window_label(filters.recent_window_days)

    filtered = [observation for observation in observations if _matches_filters(observation, filters)]
    dated: list[tuple[InnovationObservation, date]] = []
    for observation in filtered:
        day = _parse_day(observation.event_date, "event_date")
        assert day is not None
        if day <= window_end:
            dated.append((observation, day))

    recent_all = [observation for observation, day in dated if recent_start <= day <= window_end and _is_top_performing(observation, filters)]
    baseline_all = [
        observation
        for observation, day in dated
        if day < recent_start and (baseline_start is None or day >= baseline_start)
    ]
    historical_before_recent = [observation for observation, day in dated if day < recent_start]

    recent_total_decks = len(_distinct_decks(recent_all))
    baseline_total_decks = len(_distinct_decks(baseline_all))

    recent_by_card: dict[str, list[InnovationObservation]] = defaultdict(list)
    baseline_by_card: dict[str, list[InnovationObservation]] = defaultdict(list)
    historical_by_card: dict[str, list[InnovationObservation]] = defaultdict(list)
    for observation in recent_all:
        recent_by_card[observation.oracle_id].append(observation)
    for observation in baseline_all:
        baseline_by_card[observation.oracle_id].append(observation)
    for observation in historical_before_recent:
        historical_by_card[observation.oracle_id].append(observation)

    signals: list[InnovationSignal] = []
    for oracle_id, card_recent in sorted(recent_by_card.items()):
        recent_count = len(_distinct_decks(card_recent))
        if recent_count < filters.minimum_sample_size:
            continue
        card_baseline = baseline_by_card.get(oracle_id, [])
        card_historical = historical_by_card.get(oracle_id, [])
        baseline_count = len(_distinct_decks(card_baseline))
        recent_rate = _rate(recent_count, recent_total_decks)
        baseline_rate = _rate(baseline_count, baseline_total_decks)
        baseline_low = baseline_rate in (None, 0) or baseline_rate <= filters.low_baseline_inclusion_threshold
        usage_delta = None if recent_rate is None or baseline_rate is None else recent_rate - baseline_rate
        scryfall_id, released_at, has_release = _card_metadata(card_recent + card_baseline + card_historical)
        release_day = _parse_day(released_at, "card_released_at") if released_at else None
        first_recent_day = min(_parse_day(observation.event_date, "event_date") for observation in card_recent)
        assert first_recent_day is not None
        is_new_release = bool(release_day and first_recent_day >= release_day and first_recent_day - release_day <= timedelta(days=filters.adoption_window_days))

        common_kwargs: dict[str, Any] = {
            "oracle_id": oracle_id,
            "scryfall_id": scryfall_id,
            "recent_window": recent_window,
            "baseline_window": filters.baseline_window,
            "recent_rate": recent_rate,
            "baseline_rate": baseline_rate,
            "recent_observations": card_recent,
            "historical_before_recent": card_historical,
            "card_released_at": released_at,
            "is_new_release": is_new_release,
            "generated_at": generated_at,
        }

        if baseline_low:
            _append_if_new(
                signals,
                _signal(
                    innovation_type="new_innovation",
                    commander_signature=None,
                    region_code=None,
                    **common_kwargs,
                ),
            )
        if baseline_count > 0 and baseline_low and usage_delta is not None and usage_delta >= filters.breakout_delta_threshold:
            _append_if_new(
                signals,
                _signal(
                    innovation_type="recent_breakout",
                    commander_signature=None,
                    region_code=None,
                    **common_kwargs,
                ),
            )
        if filters.include_old_card_resurgences and card_historical:
            last_before_day = max(_parse_day(observation.event_date, "event_date") for observation in card_historical)
            assert last_before_day is not None
            if first_recent_day - last_before_day >= timedelta(days=filters.resurgence_inactive_days):
                _append_if_new(
                    signals,
                    _signal(
                        innovation_type="old_card_resurgence",
                        commander_signature=None,
                        region_code=None,
                        **common_kwargs,
                    ),
                )
        if filters.include_newly_released_cards and has_release and is_new_release:
            _append_if_new(
                signals,
                _signal(
                    innovation_type="new_release_adoption",
                    commander_signature=None,
                    region_code=None,
                    **common_kwargs,
                ),
            )

        for commander_signature in sorted({observation.commander_signature for observation in card_recent if observation.commander_signature}):
            commander_recent = [observation for observation in card_recent if observation.commander_signature == commander_signature]
            if len(_distinct_decks(commander_recent)) >= filters.minimum_sample_size and baseline_low:
                _append_if_new(
                    signals,
                    _signal(
                        innovation_type="commander_specific_innovation",
                        commander_signature=commander_signature,
                        region_code=None,
                        recent_observations=commander_recent,
                        **{key: value for key, value in common_kwargs.items() if key != "recent_observations"},
                    ),
                )
        for region_code in sorted({observation.region_code for observation in card_recent if observation.region_code}):
            regional_recent = [observation for observation in card_recent if observation.region_code == region_code]
            if len(_distinct_decks(regional_recent)) >= filters.minimum_sample_size and baseline_low:
                _append_if_new(
                    signals,
                    _signal(
                        innovation_type="regional_innovation",
                        commander_signature=None,
                        region_code=region_code,
                        recent_observations=regional_recent,
                        **{key: value for key, value in common_kwargs.items() if key != "recent_observations"},
                    ),
                )

    return tuple(sorted(signals, key=lambda signal: (signal.innovation_type, signal.oracle_id, signal.commander_signature or "", signal.region_code or "")))


def innovation_evidence_line(signal: InnovationSignal) -> str:
    if signal.innovation_type == "new_release_adoption":
        text = (
            f"Card was released on {signal.card_released_at} and appeared in {signal.sample_size} "
            f"top-performing tournament deck(s) within {signal.recent_window}."
        )
    elif signal.innovation_type == "old_card_resurgence":
        text = (
            f"Card reappeared in {signal.sample_size} top-performing tournament deck(s) in {signal.recent_window} "
            f"after last being seen on {signal.last_seen_before_recent_window}."
        )
    elif signal.innovation_type == "regional_innovation":
        text = (
            f"Card has regional adoption in {signal.region_code} with {signal.sample_size} top-performing deck(s) "
            f"in {signal.recent_window}."
        )
    elif signal.innovation_type == "commander_specific_innovation":
        text = (
            f"Card appeared in {signal.sample_size} top-performing {signal.commander_signature} deck(s) "
            f"in {signal.recent_window} after low baseline usage."
        )
    else:
        text = (
            f"Card usage changed from {signal.baseline_inclusion_rate or 0:.4f} to "
            f"{signal.recent_inclusion_rate or 0:.4f} in the selected evidence windows."
        )
    normalized = text.lower()
    for fragment in FORBIDDEN_INNOVATION_WORDING:
        if fragment in normalized:
            raise ValueError(f"unsupported innovation wording: {fragment}")
    return text
