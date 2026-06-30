"""Deterministic Monte Carlo batch runner for probability simulations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .card_definition_manager import CardDefinitionManager
from .models import SimulationCardModel, SimulationDeck, SimulationTargetCondition
from .mulligan import MulliganPolicyConfig, MulliganResult, simulate_london_mulligan
from .search import (
    FAILURE,
    INVALID_TARGET,
    LIMIT_EXCEEDED,
    SUCCESS,
    UNSUPPORTED,
    SearchConfig,
    SearchResult,
    find_target_access_line,
)
from .shuffle import ExpandedLibraryCard, OpeningHand, opening_hand_id, shuffle_library


BATCH_VERSION = "codie-batch-runner-v1"


@dataclass(frozen=True)
class BatchRunConfig:
    batch_version: str = BATCH_VERSION
    base_seed: str = "codie"
    games_requested: int = 100
    game_index_start: int = 0
    sample_successful_traces: int = 3
    sample_failed_traces: int = 0
    sample_unsupported_traces: int = 3
    include_failed_trace_samples: bool = False
    include_unsupported_trace_samples: bool = True

    def __post_init__(self) -> None:
        if not self.batch_version:
            raise ValueError("batch_version is required")
        if not self.base_seed:
            raise ValueError("base_seed is required")
        if self.games_requested <= 0:
            raise ValueError("games_requested must be positive")
        if self.game_index_start < 0:
            raise ValueError("game_index_start cannot be negative")
        for field_name in ("sample_successful_traces", "sample_failed_traces", "sample_unsupported_traces"):
            value = getattr(self, field_name)
            if value < 0:
                raise ValueError(f"{field_name} cannot be negative")

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_version": self.batch_version,
            "base_seed": self.base_seed,
            "games_requested": self.games_requested,
            "game_index_start": self.game_index_start,
            "sample_successful_traces": self.sample_successful_traces,
            "sample_failed_traces": self.sample_failed_traces,
            "sample_unsupported_traces": self.sample_unsupported_traces,
            "include_failed_trace_samples": self.include_failed_trace_samples,
            "include_unsupported_trace_samples": self.include_unsupported_trace_samples,
        }


@dataclass(frozen=True)
class BatchTraceSample:
    game_index: int
    search_status: str
    success: bool
    trace: dict[str, Any]

    def __post_init__(self) -> None:
        if self.game_index < 0:
            raise ValueError("game_index cannot be negative")
        if self.search_status not in {SUCCESS, FAILURE, UNSUPPORTED, INVALID_TARGET, LIMIT_EXCEEDED}:
            raise ValueError("unsupported search status")
        object.__setattr__(self, "trace", dict(self.trace))

    def to_dict(self) -> dict[str, Any]:
        return {
            "game_index": self.game_index,
            "search_status": self.search_status,
            "success": self.success,
            "trace": dict(self.trace),
        }


@dataclass(frozen=True)
class BatchGameResult:
    game_index: int
    derived_seed: str
    opening_hand_id: str
    mulligan_count: int
    kept_hand: tuple[str, ...]
    bottomed_cards: tuple[str, ...]
    search_status: str
    success: bool
    actions_taken: int
    branches_evaluated: int
    unsupported_cards: tuple[str, ...] = ()
    unsupported_actions: tuple[str, ...] = ()
    trace: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.game_index < 0:
            raise ValueError("game_index cannot be negative")
        if not self.derived_seed:
            raise ValueError("derived_seed is required")
        if not self.opening_hand_id:
            raise ValueError("opening_hand_id is required")
        if self.mulligan_count < 0:
            raise ValueError("mulligan_count cannot be negative")
        if self.search_status not in {SUCCESS, FAILURE, UNSUPPORTED, INVALID_TARGET, LIMIT_EXCEEDED}:
            raise ValueError("unsupported search status")
        object.__setattr__(self, "kept_hand", tuple(self.kept_hand))
        object.__setattr__(self, "bottomed_cards", tuple(self.bottomed_cards))
        object.__setattr__(self, "unsupported_cards", tuple(dict.fromkeys(self.unsupported_cards)))
        object.__setattr__(self, "unsupported_actions", tuple(dict.fromkeys(self.unsupported_actions)))
        object.__setattr__(self, "trace", dict(self.trace))

    def to_dict(self) -> dict[str, Any]:
        return {
            "game_index": self.game_index,
            "derived_seed": self.derived_seed,
            "opening_hand_id": self.opening_hand_id,
            "mulligan_count": self.mulligan_count,
            "kept_hand": list(self.kept_hand),
            "bottomed_cards": list(self.bottomed_cards),
            "search_status": self.search_status,
            "success": self.success,
            "actions_taken": self.actions_taken,
            "branches_evaluated": self.branches_evaluated,
            "unsupported_cards": list(self.unsupported_cards),
            "unsupported_actions": list(self.unsupported_actions),
            "trace": dict(self.trace),
        }


@dataclass(frozen=True)
class BatchRunResult:
    deck_hash: str
    target_condition: SimulationTargetCondition
    batch_config: BatchRunConfig
    mulligan_policy: MulliganPolicyConfig
    search_config: SearchConfig
    games_requested: int
    games_completed: int
    success_count: int
    failure_count: int
    unsupported_count: int
    invalid_target_count: int
    limit_exceeded_count: int
    success_rate: float
    unsupported_rate: float
    average_mulligan_count: float
    sample_successful_traces: tuple[BatchTraceSample, ...] = ()
    sample_failed_traces: tuple[BatchTraceSample, ...] = ()
    sample_unsupported_traces: tuple[BatchTraceSample, ...] = ()
    unsupported_cards: tuple[str, ...] = ()
    unsupported_actions: tuple[str, ...] = ()
    game_results: tuple[BatchGameResult, ...] = ()
    generated_at: str | None = None

    def __post_init__(self) -> None:
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        if self.games_completed < 0:
            raise ValueError("games_completed cannot be negative")
        object.__setattr__(self, "sample_successful_traces", tuple(self.sample_successful_traces))
        object.__setattr__(self, "sample_failed_traces", tuple(self.sample_failed_traces))
        object.__setattr__(self, "sample_unsupported_traces", tuple(self.sample_unsupported_traces))
        object.__setattr__(self, "unsupported_cards", tuple(dict.fromkeys(self.unsupported_cards)))
        object.__setattr__(self, "unsupported_actions", tuple(dict.fromkeys(self.unsupported_actions)))
        object.__setattr__(self, "game_results", tuple(self.game_results))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "target_condition": self.target_condition.to_dict(),
            "batch_config": self.batch_config.to_dict(),
            "mulligan_policy": self.mulligan_policy.to_dict(),
            "search_config": self.search_config.to_dict(),
            "games_requested": self.games_requested,
            "games_completed": self.games_completed,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "unsupported_count": self.unsupported_count,
            "invalid_target_count": self.invalid_target_count,
            "limit_exceeded_count": self.limit_exceeded_count,
            "success_rate": self.success_rate,
            "unsupported_rate": self.unsupported_rate,
            "average_mulligan_count": self.average_mulligan_count,
            "sample_successful_traces": [sample.to_dict() for sample in self.sample_successful_traces],
            "sample_failed_traces": [sample.to_dict() for sample in self.sample_failed_traces],
            "sample_unsupported_traces": [sample.to_dict() for sample in self.sample_unsupported_traces],
            "unsupported_cards": list(self.unsupported_cards),
            "unsupported_actions": list(self.unsupported_actions),
            "game_results": [result.to_dict() for result in self.game_results],
            "generated_at": self.generated_at,
        }


def run_simulation_batch(
    deck: SimulationDeck,
    target_condition: SimulationTargetCondition,
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
    mulligan_policy: MulliganPolicyConfig,
    search_config: SearchConfig,
    batch_config: BatchRunConfig,
    *,
    generated_at: str | None = None,
) -> BatchRunResult:
    manager = _manager(card_definitions)
    game_results = tuple(
        run_single_simulation_game(
            deck,
            target_condition,
            manager,
            mulligan_policy,
            search_config,
            batch_config,
            game_offset=index,
        )
        for index in range(batch_config.games_requested)
    )
    return summarize_batch_results(
        deck,
        target_condition,
        mulligan_policy,
        search_config,
        batch_config,
        game_results,
        generated_at=generated_at,
    )


def run_single_simulation_game(
    deck: SimulationDeck,
    target_condition: SimulationTargetCondition,
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
    mulligan_policy: MulliganPolicyConfig,
    search_config: SearchConfig,
    batch_config: BatchRunConfig,
    *,
    game_offset: int = 0,
) -> BatchGameResult:
    if game_offset < 0:
        raise ValueError("game_offset cannot be negative")
    manager = _manager(card_definitions)
    first_game_index = batch_config.game_index_start + game_offset
    mulligan = simulate_london_mulligan(
        deck,
        batch_config.base_seed,
        mulligan_policy,
        game_index_offset=first_game_index,
    )
    final_game_index = first_game_index + mulligan.mulligan_count
    shuffled = shuffle_library(deck, batch_config.base_seed, game_index=final_game_index)
    kept_hand = _kept_hand_after_bottom(mulligan)
    library = _remaining_library_after_mulligan(shuffled.shuffled_cards, mulligan.bottomed_cards)
    search_result = find_target_access_line(
        kept_hand,
        target_condition,
        manager,
        library=library,
        config=search_config,
    )
    return _game_result_from_search(final_game_index, kept_hand, mulligan, search_result)


def summarize_batch_results(
    deck: SimulationDeck,
    target_condition: SimulationTargetCondition,
    mulligan_policy: MulliganPolicyConfig,
    search_config: SearchConfig,
    batch_config: BatchRunConfig,
    game_results: Iterable[BatchGameResult],
    *,
    generated_at: str | None = None,
) -> BatchRunResult:
    results = tuple(game_results)
    games_completed = len(results)
    success_count = sum(1 for result in results if result.search_status == SUCCESS)
    unsupported_count = sum(1 for result in results if result.search_status == UNSUPPORTED)
    invalid_target_count = sum(1 for result in results if result.search_status == INVALID_TARGET)
    limit_exceeded_count = sum(1 for result in results if result.search_status == LIMIT_EXCEEDED)
    failure_count = sum(1 for result in results if result.search_status == FAILURE)
    unsupported_cards = tuple(dict.fromkeys(card for result in results for card in result.unsupported_cards))
    unsupported_actions = tuple(dict.fromkeys(action for result in results for action in result.unsupported_actions))
    average_mulligan_count = (
        sum(result.mulligan_count for result in results) / games_completed if games_completed else 0.0
    )
    return BatchRunResult(
        deck_hash=deck.deck_hash,
        target_condition=target_condition,
        batch_config=batch_config,
        mulligan_policy=mulligan_policy,
        search_config=search_config,
        games_requested=batch_config.games_requested,
        games_completed=games_completed,
        success_count=success_count,
        failure_count=failure_count,
        unsupported_count=unsupported_count,
        invalid_target_count=invalid_target_count,
        limit_exceeded_count=limit_exceeded_count,
        success_rate=success_count / games_completed if games_completed else 0.0,
        unsupported_rate=unsupported_count / games_completed if games_completed else 0.0,
        average_mulligan_count=average_mulligan_count,
        sample_successful_traces=_samples(results, SUCCESS, batch_config.sample_successful_traces),
        sample_failed_traces=_samples(
            results,
            FAILURE,
            batch_config.sample_failed_traces if batch_config.include_failed_trace_samples else 0,
        ),
        sample_unsupported_traces=_samples(
            results,
            UNSUPPORTED,
            batch_config.sample_unsupported_traces if batch_config.include_unsupported_trace_samples else 0,
        ),
        unsupported_cards=unsupported_cards,
        unsupported_actions=unsupported_actions,
        game_results=results,
        generated_at=generated_at,
    )


def _manager(
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
) -> CardDefinitionManager:
    if isinstance(card_definitions, CardDefinitionManager):
        return card_definitions
    rows = list(card_definitions)
    if all(isinstance(row, SimulationCardModel) for row in rows):
        return CardDefinitionManager(
            overlays_by_id={row.card_id: row for row in rows},  # type: ignore[union-attr]
            overlays_by_name={_normalize(row.name): row for row in rows},  # type: ignore[union-attr]
        )
    return CardDefinitionManager.from_overlay_rows(rows)  # type: ignore[arg-type]


def _kept_hand_after_bottom(mulligan: MulliganResult) -> OpeningHand:
    final_step = mulligan.steps[-1]
    kept_cards = final_step.kept_cards_after_bottom or mulligan.kept_hand.cards
    hand = OpeningHand(
        deck_hash=mulligan.kept_hand.deck_hash,
        base_seed=mulligan.kept_hand.base_seed,
        game_index=mulligan.kept_hand.game_index,
        derived_seed=mulligan.kept_hand.derived_seed,
        shuffle_algorithm_version=mulligan.kept_hand.shuffle_algorithm_version,
        hand_size=len(kept_cards),
        cards=tuple(kept_cards),
        hand_id="sha256:pending",
        remaining_library_size=mulligan.kept_hand.remaining_library_size + len(mulligan.bottomed_cards),
        unresolved_cards=mulligan.kept_hand.unresolved_cards,
    )
    return OpeningHand(
        deck_hash=hand.deck_hash,
        base_seed=hand.base_seed,
        game_index=hand.game_index,
        derived_seed=hand.derived_seed,
        shuffle_algorithm_version=hand.shuffle_algorithm_version,
        hand_size=hand.hand_size,
        cards=hand.cards,
        hand_id=opening_hand_id(hand),
        remaining_library_size=hand.remaining_library_size,
        unresolved_cards=hand.unresolved_cards,
    )


def _remaining_library_after_mulligan(
    shuffled_cards: tuple[ExpandedLibraryCard, ...],
    bottomed_cards: tuple[ExpandedLibraryCard, ...],
) -> tuple[ExpandedLibraryCard, ...]:
    bottomed_ids = {card.physical_id for card in bottomed_cards}
    after_opening_hand = tuple(card for card in shuffled_cards[7:] if card.physical_id not in bottomed_ids)
    return (*after_opening_hand, *bottomed_cards)


def _game_result_from_search(
    game_index: int,
    kept_hand: OpeningHand,
    mulligan: MulliganResult,
    search_result: SearchResult,
) -> BatchGameResult:
    return BatchGameResult(
        game_index=game_index,
        derived_seed=kept_hand.derived_seed,
        opening_hand_id=kept_hand.hand_id,
        mulligan_count=mulligan.mulligan_count,
        kept_hand=tuple(card.name for card in kept_hand.cards),
        bottomed_cards=tuple(card.name for card in mulligan.bottomed_cards),
        search_status=search_result.status,
        success=search_result.success,
        actions_taken=search_result.actions_taken,
        branches_evaluated=search_result.branches_evaluated,
        unsupported_cards=search_result.unsupported_cards,
        unsupported_actions=search_result.unsupported_actions,
        trace=search_result.trace.to_dict(),
    )


def _samples(
    results: tuple[BatchGameResult, ...],
    status: str,
    limit: int,
) -> tuple[BatchTraceSample, ...]:
    if limit <= 0:
        return ()
    samples = [
        BatchTraceSample(
            game_index=result.game_index,
            search_status=result.search_status,
            success=result.success,
            trace=result.trace,
        )
        for result in results
        if result.search_status == status
    ]
    return tuple(samples[:limit])


def _normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())
