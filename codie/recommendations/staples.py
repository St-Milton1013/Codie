"""Commander staples report primitives built from canonical observations."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from .statistics import inclusion_rate, weighted_inclusion_rate


_COLOR_ORDER = {"W": 0, "U": 1, "B": 2, "R": 3, "G": 4}


@dataclass(frozen=True)
class StapleObservation:
    deck_id: str
    oracle_id: str
    card_name: str
    quantity: int = 1
    scryfall_id: str | None = None
    type_line: str | None = None
    color_identity: tuple[str, ...] = ()
    entry_weight: float = 1.0
    placement: int | None = None
    top_cut: bool = False
    winner: bool = False
    event_date: str | None = None
    deck_url: str | None = None
    event_url: str | None = None
    provider: str | None = None
    region: str | None = None
    country: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.deck_id, "deck_id")
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.card_name, "card_name")
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.entry_weight < 0:
            raise ValueError("entry_weight must be non-negative")
        if self.placement is not None and self.placement <= 0:
            raise ValueError("placement must be positive when provided")
        object.__setattr__(self, "color_identity", _normalize_color_identity(self.color_identity))


@dataclass(frozen=True)
class StapleReportRow:
    card_name: str
    scryfall_id: str | None
    oracle_id: str
    type_line: str | None
    color_identity: tuple[str, ...]
    matching_deck_count: int
    total_matching_decks: int
    inclusion_percentage: float | None
    total_copies_observed: int
    average_copies_per_deck: float | None
    placement_weighted_usage: float | None
    best_finish_observed: int | None
    top16_count: int
    winner_count: int
    most_recent_appearance_date: str | None
    first_appearance_date: str | None
    deck_urls: tuple[str, ...]
    event_urls: tuple[str, ...]
    provider_breakdown: dict[str, int]
    region_breakdown: dict[str, int]


@dataclass(frozen=True)
class CommanderStaplesReport:
    commander_signature: str
    time_window: str
    placement_scope: str
    generated_at: str
    total_matching_decks: int
    rows: tuple[StapleReportRow, ...]


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _unique_sorted(values: Iterable[str | None]) -> tuple[str, ...]:
    return tuple(sorted({value.strip() for value in values if value and value.strip()}))


def _normalize_color_identity(values: Iterable[str]) -> tuple[str, ...]:
    colors = {str(value).strip().upper() for value in values if str(value).strip()}
    return tuple(sorted(colors, key=lambda color: (_COLOR_ORDER.get(color, len(_COLOR_ORDER)), color)))


def _region_key(observation: StapleObservation) -> str | None:
    region = (observation.region or "").strip()
    country = (observation.country or "").strip()
    if region and country:
        return f"{region}/{country}"
    return region or country or None


def _is_top16(observation: StapleObservation) -> bool:
    return observation.top_cut or (observation.placement is not None and observation.placement <= 16)


def build_commander_staples_report(
    *,
    commander_signature: str,
    observations: Iterable[StapleObservation],
    time_window: str,
    generated_at: str,
    placement_scope: str = "top_16",
    total_matching_decks: int | None = None,
    minimum_inclusion_percentage: float = 0.0,
) -> CommanderStaplesReport:
    _require_text(commander_signature, "commander_signature")
    _require_text(time_window, "time_window")
    _require_text(generated_at, "generated_at")
    _require_text(placement_scope, "placement_scope")
    if minimum_inclusion_percentage < 0 or minimum_inclusion_percentage > 1:
        raise ValueError("minimum_inclusion_percentage must be between 0 and 1")

    observation_list = tuple(observations)
    deck_weights: dict[str, float] = {}
    for observation in observation_list:
        deck_weights[observation.deck_id] = max(deck_weights.get(observation.deck_id, 0.0), observation.entry_weight)
    observed_deck_count = len(deck_weights)
    if total_matching_decks is None:
        total_decks = observed_deck_count
    else:
        if total_matching_decks < observed_deck_count:
            raise ValueError("total_matching_decks cannot be smaller than observed deck count")
        total_decks = total_matching_decks
    total_weight = sum(deck_weights.values())

    grouped: dict[str, list[StapleObservation]] = defaultdict(list)
    for observation in observation_list:
        grouped[observation.oracle_id].append(observation)

    rows = []
    for oracle_id, card_observations in grouped.items():
        by_deck: dict[str, list[StapleObservation]] = defaultdict(list)
        for observation in card_observations:
            by_deck[observation.deck_id].append(observation)
        deck_ids = set(by_deck)
        matching_deck_count = len(deck_ids)
        inclusion = inclusion_rate(matching_deck_count, total_decks)
        if inclusion is not None and inclusion < minimum_inclusion_percentage:
            continue
        weighted_with = sum(deck_weights[deck_id] for deck_id in deck_ids)
        placements = [observation.placement for observation in card_observations if observation.placement is not None]
        dates = [observation.event_date for observation in card_observations if observation.event_date]
        first = card_observations[0]
        provider_counts = Counter(
            observation.provider.strip()
            for deck_id in deck_ids
            for observation in by_deck[deck_id][:1]
            if observation.provider and observation.provider.strip()
        )
        region_counts = Counter(
            region
            for deck_id in deck_ids
            for observation in by_deck[deck_id][:1]
            if (region := _region_key(observation))
        )
        total_copies = sum(observation.quantity for observation in card_observations)
        rows.append(
            StapleReportRow(
                card_name=first.card_name,
                scryfall_id=first.scryfall_id,
                oracle_id=oracle_id,
                type_line=first.type_line,
                color_identity=first.color_identity,
                matching_deck_count=matching_deck_count,
                total_matching_decks=total_decks,
                inclusion_percentage=inclusion,
                total_copies_observed=total_copies,
                average_copies_per_deck=total_copies / matching_deck_count if matching_deck_count else None,
                placement_weighted_usage=weighted_inclusion_rate(weighted_with, total_weight),
                best_finish_observed=min(placements) if placements else None,
                top16_count=sum(1 for deck_id in deck_ids if any(_is_top16(observation) for observation in by_deck[deck_id])),
                winner_count=sum(1 for deck_id in deck_ids if any(observation.winner for observation in by_deck[deck_id])),
                most_recent_appearance_date=max(dates) if dates else None,
                first_appearance_date=min(dates) if dates else None,
                deck_urls=_unique_sorted(observation.deck_url for observation in card_observations),
                event_urls=_unique_sorted(observation.event_url for observation in card_observations),
                provider_breakdown=dict(sorted(provider_counts.items())),
                region_breakdown=dict(sorted(region_counts.items())),
            )
        )

    sorted_rows = tuple(
        sorted(
            rows,
            key=lambda row: (
                -row.matching_deck_count,
                -(row.placement_weighted_usage or 0.0),
                row.oracle_id,
            ),
        )
    )
    return CommanderStaplesReport(
        commander_signature=commander_signature,
        time_window=time_window,
        placement_scope=placement_scope,
        generated_at=generated_at,
        total_matching_decks=total_decks,
        rows=sorted_rows,
    )
