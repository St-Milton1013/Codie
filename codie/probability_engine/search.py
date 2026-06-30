"""Bounded deterministic target access search for simulator hands."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .card_definition_manager import CardDefinitionManager
from .models import MANA_COLOR_KEYS, ManaCost, ManaOption, SimulationCardModel, SimulationTargetCondition
from .shuffle import ExpandedLibraryCard, OpeningHand


SEARCH_VERSION = "codie-target-search-v1"

SUCCESS = "success"
FAILURE = "failure"
UNSUPPORTED = "unsupported"
INVALID_TARGET = "invalid_target"
LIMIT_EXCEEDED = "limit_exceeded"

TARGET_CONDITION_TYPES = {
    "access",
    "cast",
    "cast_or_access",
    "draw",
    "find_to_hand",
    "find_to_top",
    "put_onto_battlefield",
}

SUPPORTED_ACTION_TYPES = {
    "play_land",
    "tap_for_mana",
    "sacrifice_for_mana",
    "cast_spell",
    "resolve_spell",
    "draw_cards",
    "search_library",
    "move_to_hand",
    "put_on_top",
    "put_onto_battlefield",
    "add_mana",
    "unsupported_marker",
}


@dataclass(frozen=True)
class SearchConfig:
    search_version: str = SEARCH_VERSION
    max_turn: int = 1
    max_actions: int = 20
    max_branches: int = 250
    trace_limit: int = 50
    stop_at_first_success: bool = True
    allow_unsupported_relevant: bool = False
    deterministic_tie_breakers: bool = True

    def __post_init__(self) -> None:
        if not self.search_version:
            raise ValueError("search_version is required")
        for field_name in ("max_turn", "max_actions", "max_branches", "trace_limit"):
            value = getattr(self, field_name)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"{field_name} must be a positive integer")

    def to_dict(self) -> dict[str, Any]:
        return {
            "search_version": self.search_version,
            "max_turn": self.max_turn,
            "max_actions": self.max_actions,
            "max_branches": self.max_branches,
            "trace_limit": self.trace_limit,
            "stop_at_first_success": self.stop_at_first_success,
            "allow_unsupported_relevant": self.allow_unsupported_relevant,
            "deterministic_tie_breakers": self.deterministic_tie_breakers,
        }


@dataclass(frozen=True)
class SearchAction:
    action_index: int
    turn: int
    phase_label: str
    action_type: str
    source_card: str | None = None
    source_zone: str | None = None
    destination_zone: str | None = None
    mana_before: dict[str, int] = field(default_factory=dict)
    mana_after: dict[str, int] = field(default_factory=dict)
    cards_moved: tuple[str, ...] = ()
    target_status_after: str | None = None
    reason: str | None = None
    unsupported_card: str | None = None
    unsupported_action: str | None = None

    def __post_init__(self) -> None:
        if self.action_index < 0:
            raise ValueError("action_index cannot be negative")
        if self.turn <= 0:
            raise ValueError("turn must be positive")
        if not self.phase_label:
            raise ValueError("phase_label is required")
        if self.action_type not in SUPPORTED_ACTION_TYPES:
            raise ValueError("unsupported search action type")
        object.__setattr__(self, "mana_before", _mana_pool(self.mana_before))
        object.__setattr__(self, "mana_after", _mana_pool(self.mana_after))
        object.__setattr__(self, "cards_moved", tuple(self.cards_moved))

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_index": self.action_index,
            "turn": self.turn,
            "phase_label": self.phase_label,
            "action_type": self.action_type,
            "source_card": self.source_card,
            "source_zone": self.source_zone,
            "destination_zone": self.destination_zone,
            "mana_before": dict(self.mana_before),
            "mana_after": dict(self.mana_after),
            "cards_moved": list(self.cards_moved),
            "target_status_after": self.target_status_after,
            "reason": self.reason,
            "unsupported_card": self.unsupported_card,
            "unsupported_action": self.unsupported_action,
        }


@dataclass(frozen=True)
class SearchTrace:
    actions: tuple[SearchAction, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "actions", tuple(self.actions))

    def to_dict(self) -> dict[str, Any]:
        return {"actions": [action.to_dict() for action in self.actions]}


@dataclass(frozen=True)
class SearchState:
    turn: int
    phase_label: str
    hand: tuple[ExpandedLibraryCard, ...]
    library: tuple[ExpandedLibraryCard, ...]
    battlefield: tuple[ExpandedLibraryCard, ...] = ()
    graveyard: tuple[ExpandedLibraryCard, ...] = ()
    exile: tuple[ExpandedLibraryCard, ...] = ()
    stack: tuple[ExpandedLibraryCard, ...] = ()
    mana_pool: dict[str, int] = field(default_factory=dict)
    land_played_this_turn: bool = False
    actions_taken: int = 0
    target_condition: SimulationTargetCondition | None = None
    target_events: tuple[str, ...] = ()
    unsupported_cards: tuple[str, ...] = ()
    unsupported_actions: tuple[str, ...] = ()
    tapped_ids: tuple[str, ...] = ()
    trace: tuple[SearchAction, ...] = ()

    def __post_init__(self) -> None:
        if self.turn <= 0:
            raise ValueError("turn must be positive")
        if not self.phase_label:
            raise ValueError("phase_label is required")
        object.__setattr__(self, "hand", tuple(self.hand))
        object.__setattr__(self, "library", tuple(self.library))
        object.__setattr__(self, "battlefield", tuple(self.battlefield))
        object.__setattr__(self, "graveyard", tuple(self.graveyard))
        object.__setattr__(self, "exile", tuple(self.exile))
        object.__setattr__(self, "stack", tuple(self.stack))
        object.__setattr__(self, "mana_pool", _mana_pool(self.mana_pool))
        object.__setattr__(self, "target_events", tuple(self.target_events))
        object.__setattr__(self, "unsupported_cards", tuple(dict.fromkeys(self.unsupported_cards)))
        object.__setattr__(self, "unsupported_actions", tuple(dict.fromkeys(self.unsupported_actions)))
        object.__setattr__(self, "tapped_ids", tuple(dict.fromkeys(self.tapped_ids)))
        object.__setattr__(self, "trace", tuple(self.trace))

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "phase_label": self.phase_label,
            "hand": [_card_ref(card) for card in self.hand],
            "library": [_card_ref(card) for card in self.library],
            "battlefield": [_card_ref(card) for card in self.battlefield],
            "graveyard": [_card_ref(card) for card in self.graveyard],
            "exile": [_card_ref(card) for card in self.exile],
            "stack": [_card_ref(card) for card in self.stack],
            "mana_pool": dict(self.mana_pool),
            "land_played_this_turn": self.land_played_this_turn,
            "actions_taken": self.actions_taken,
            "target_condition": self.target_condition.to_dict() if self.target_condition is not None else None,
            "target_events": list(self.target_events),
            "unsupported_cards": list(self.unsupported_cards),
            "unsupported_actions": list(self.unsupported_actions),
            "tapped_ids": list(self.tapped_ids),
            "trace": [action.to_dict() for action in self.trace],
        }


@dataclass(frozen=True)
class SearchResult:
    status: str
    success: bool
    target_condition: SimulationTargetCondition
    search_config: SearchConfig
    final_state: SearchState
    trace: SearchTrace
    unsupported_cards: tuple[str, ...] = ()
    unsupported_actions: tuple[str, ...] = ()
    branches_evaluated: int = 0
    actions_taken: int = 0

    def __post_init__(self) -> None:
        if self.status not in {SUCCESS, FAILURE, UNSUPPORTED, INVALID_TARGET, LIMIT_EXCEEDED}:
            raise ValueError("unsupported search status")
        object.__setattr__(self, "unsupported_cards", tuple(dict.fromkeys(self.unsupported_cards)))
        object.__setattr__(self, "unsupported_actions", tuple(dict.fromkeys(self.unsupported_actions)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "success": self.success,
            "target_condition": self.target_condition.to_dict(),
            "search_config": self.search_config.to_dict(),
            "final_state": self.final_state.to_dict(),
            "trace": self.trace.to_dict(),
            "unsupported_cards": list(self.unsupported_cards),
            "unsupported_actions": list(self.unsupported_actions),
            "branches_evaluated": self.branches_evaluated,
            "actions_taken": self.actions_taken,
        }


TargetAccessResult = SearchResult


def build_initial_search_state(
    opening_hand: OpeningHand,
    target_condition: SimulationTargetCondition,
    *,
    library: Iterable[ExpandedLibraryCard] = (),
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel] | None = None,
) -> SearchState:
    manager = _manager(card_definitions)
    unsupported = _unsupported_cards((*opening_hand.cards, *tuple(library)), manager)
    return SearchState(
        turn=1,
        phase_label="main",
        hand=tuple(opening_hand.cards),
        library=tuple(library),
        mana_pool=_mana_pool(),
        target_condition=target_condition,
        unsupported_cards=unsupported,
    )


def find_target_access_line(
    opening_hand: OpeningHand,
    target_condition: SimulationTargetCondition,
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
    *,
    library: Iterable[ExpandedLibraryCard] = (),
    config: SearchConfig | None = None,
) -> TargetAccessResult:
    search_config = config or SearchConfig(max_turn=target_condition.turn)
    if target_condition.condition_type not in TARGET_CONDITION_TYPES:
        initial = build_initial_search_state(opening_hand, target_condition, library=library, card_definitions=card_definitions)
        return _result(INVALID_TARGET, False, target_condition, search_config, initial, branches=0)

    manager = _manager(card_definitions)
    initial = build_initial_search_state(
        opening_hand,
        target_condition,
        library=library,
        card_definitions=manager,
    )
    immediate = _success_if_reached(initial, search_config)
    if immediate is not None:
        return immediate

    if _target_requires_missing_overlay(initial, manager):
        return _result(
            INVALID_TARGET,
            False,
            target_condition,
            search_config,
            _with_unsupported(initial, (target_condition.target_card,), ("missing_target_behavior",)),
            branches=0,
        )

    frontier: list[SearchState] = [initial]
    visited: set[tuple[Any, ...]] = set()
    branches = 0
    last_state = initial

    while frontier:
        state = frontier.pop(0)
        last_state = state
        if state.actions_taken >= search_config.max_actions:
            return _result(LIMIT_EXCEEDED, False, target_condition, search_config, state, branches=branches)
        signature = _state_signature(state)
        if signature in visited:
            continue
        visited.add(signature)
        branches += 1
        if branches > search_config.max_branches:
            return _result(LIMIT_EXCEEDED, False, target_condition, search_config, state, branches=branches)

        next_states = _next_states(state, manager, search_config)
        if not next_states and state.unsupported_actions and not search_config.allow_unsupported_relevant:
            return _result(UNSUPPORTED, False, target_condition, search_config, state, branches=branches)
        for next_state in next_states:
            reached = _success_if_reached(next_state, search_config, branches=branches)
            if reached is not None:
                return reached
            frontier.append(next_state)

    if last_state.unsupported_actions and not search_config.allow_unsupported_relevant:
        return _result(UNSUPPORTED, False, target_condition, search_config, last_state, branches=branches)
    return _result(FAILURE, False, target_condition, search_config, last_state, branches=branches)


def is_target_accessed(state: SearchState, target_condition: SimulationTargetCondition | None = None) -> bool:
    target = target_condition or state.target_condition
    if target is None:
        return False
    target_name = _normalize(target.target_card)
    mode = target.condition_type
    in_hand = any(_matches(card, target) for card in state.hand)
    in_stack = any(_matches(card, target) for card in state.stack)
    in_battlefield = any(_matches(card, target) for card in state.battlefield)
    events = set(state.target_events)

    if mode == "access":
        return in_hand or bool(events.intersection({"draw", "find_to_hand", "find_to_top", "put_onto_battlefield", "cast"}))
    if mode == "cast":
        return "cast" in events or in_stack
    if mode == "cast_or_access":
        return in_hand or "cast" in events or bool(events.intersection({"draw", "find_to_hand", "find_to_top"}))
    if mode == "draw":
        return "draw" in events
    if mode == "find_to_hand":
        return "find_to_hand" in events
    if mode == "find_to_top":
        return "find_to_top" in events
    if mode == "put_onto_battlefield":
        return "put_onto_battlefield" in events or in_battlefield
    return any(_normalize(card.name) == target_name for card in (*state.hand, *state.stack, *state.battlefield))


def serialize_search_trace(trace: SearchTrace | Iterable[SearchAction]) -> dict[str, Any]:
    if isinstance(trace, SearchTrace):
        return trace.to_dict()
    return SearchTrace(tuple(trace)).to_dict()


def _next_states(state: SearchState, manager: CardDefinitionManager, config: SearchConfig) -> tuple[SearchState, ...]:
    states: list[SearchState] = []
    states.extend(_play_land_states(state, manager, config))
    states.extend(_tap_for_mana_states(state, manager, config))
    states.extend(_cast_spell_states(state, manager, config))
    return tuple(states)


def _play_land_states(state: SearchState, manager: CardDefinitionManager, config: SearchConfig) -> tuple[SearchState, ...]:
    if state.land_played_this_turn:
        return ()
    states: list[SearchState] = []
    for card in _sorted_cards(state.hand):
        overlay = _overlay_for_card(manager, card)
        if overlay is None or not _is_land(overlay):
            continue
        next_hand = tuple(item for item in state.hand if item.physical_id != card.physical_id)
        battlefield = (*state.battlefield, card)
        states.append(
            _advance(
                state,
                hand=next_hand,
                battlefield=battlefield,
                land_played_this_turn=True,
                action_type="play_land",
                source_card=card.name,
                source_zone="hand",
                destination_zone="battlefield",
                cards_moved=(card.name,),
                reason="land_play_available",
                config=config,
            )
        )
    return tuple(states)


def _tap_for_mana_states(state: SearchState, manager: CardDefinitionManager, config: SearchConfig) -> tuple[SearchState, ...]:
    states: list[SearchState] = []
    tapped = set(state.tapped_ids)
    for card in _sorted_cards(state.battlefield):
        if card.physical_id in tapped:
            continue
        overlay = _overlay_for_card(manager, card)
        options = _mana_options_for_card(overlay)
        for option in options:
            mana_after = _add_mana(state.mana_pool, option)
            states.append(
                _advance(
                    state,
                    mana_pool=mana_after,
                    tapped_ids=(*state.tapped_ids, card.physical_id),
                    action_type="tap_for_mana",
                    source_card=card.name,
                    source_zone="battlefield",
                    destination_zone="mana_pool",
                    reason="modeled_mana_ability",
                    config=config,
                )
            )
    return tuple(states)


def _cast_spell_states(state: SearchState, manager: CardDefinitionManager, config: SearchConfig) -> tuple[SearchState, ...]:
    states: list[SearchState] = []
    unsupported_states: list[SearchState] = []
    for card in _sorted_cards(state.hand):
        overlay = _overlay_for_card(manager, card)
        if overlay is None:
            continue
        unsupported = _unsupported_action_types(overlay)
        if unsupported:
            unsupported_states.append(_with_unsupported(state, (card.name,), unsupported))
            continue
        if _is_land(overlay) or not _can_pay(state.mana_pool, overlay.mana_cost):
            continue
        mana_after = _pay_mana(state.mana_pool, overlay.mana_cost)
        next_hand = tuple(item for item in state.hand if item.physical_id != card.physical_id)
        destination = "battlefield" if _is_permanent(overlay) else "graveyard"
        target_events = state.target_events
        if state.target_condition is not None and _matches(card, state.target_condition):
            target_events = (*target_events, "cast")
        moved_to_hand, moved_to_top, events = _resolve_cast_actions(card, overlay, state, manager)
        final_hand = (*next_hand, *moved_to_hand)
        final_library = tuple(item for item in state.library if item.physical_id not in {m.physical_id for m in moved_to_hand})
        if moved_to_top:
            final_library = (*moved_to_top, *tuple(item for item in final_library if item.physical_id not in {m.physical_id for m in moved_to_top}))
        target_events = (*target_events, *events)
        states.append(
            _advance(
                state,
                hand=final_hand,
                library=final_library,
                battlefield=(*state.battlefield, card) if destination == "battlefield" else state.battlefield,
                graveyard=(*state.graveyard, card) if destination == "graveyard" else state.graveyard,
                mana_pool=mana_after,
                target_events=target_events,
                action_type="cast_spell",
                source_card=card.name,
                source_zone="hand",
                destination_zone=destination,
                cards_moved=(card.name, *tuple(item.name for item in moved_to_hand), *tuple(item.name for item in moved_to_top)),
                reason="modeled_cast",
                config=config,
            )
        )
    return tuple(states or unsupported_states)


def _resolve_cast_actions(
    card: ExpandedLibraryCard,
    overlay: SimulationCardModel,
    state: SearchState,
    manager: CardDefinitionManager,
) -> tuple[tuple[ExpandedLibraryCard, ...], tuple[ExpandedLibraryCard, ...], tuple[str, ...]]:
    moved_to_hand: list[ExpandedLibraryCard] = []
    moved_to_top: list[ExpandedLibraryCard] = []
    events: list[str] = []
    for action in overlay.cast_actions:
        if action.action_type != "search_library" or state.target_condition is None:
            continue
        target = _first_target_in_library(state.library, state.target_condition)
        if target is None:
            continue
        destination = action.destination or "hand"
        if destination == "hand":
            moved_to_hand.append(target)
            events.append("find_to_hand")
        elif destination in {"top", "top_of_library"}:
            moved_to_top.append(target)
            events.append("find_to_top")
        else:
            events.append("unsupported_search_destination")
    return tuple(moved_to_hand), tuple(moved_to_top), tuple(events)


def _advance(state: SearchState, *, config: SearchConfig, action_type: str, **changes: Any) -> SearchState:
    mana_before = dict(state.mana_pool)
    mana_after = _mana_pool(changes.get("mana_pool", state.mana_pool))
    target_condition = state.target_condition
    probe = SearchState(
        turn=changes.get("turn", state.turn),
        phase_label=changes.get("phase_label", state.phase_label),
        hand=changes.get("hand", state.hand),
        library=changes.get("library", state.library),
        battlefield=changes.get("battlefield", state.battlefield),
        graveyard=changes.get("graveyard", state.graveyard),
        exile=changes.get("exile", state.exile),
        stack=changes.get("stack", state.stack),
        mana_pool=mana_after,
        land_played_this_turn=changes.get("land_played_this_turn", state.land_played_this_turn),
        actions_taken=state.actions_taken + 1,
        target_condition=target_condition,
        target_events=changes.get("target_events", state.target_events),
        unsupported_cards=changes.get("unsupported_cards", state.unsupported_cards),
        unsupported_actions=changes.get("unsupported_actions", state.unsupported_actions),
        tapped_ids=changes.get("tapped_ids", state.tapped_ids),
        trace=state.trace,
    )
    action = SearchAction(
        action_index=len(state.trace),
        turn=probe.turn,
        phase_label=probe.phase_label,
        action_type=action_type,
        source_card=changes.get("source_card"),
        source_zone=changes.get("source_zone"),
        destination_zone=changes.get("destination_zone"),
        mana_before=mana_before,
        mana_after=mana_after,
        cards_moved=changes.get("cards_moved", ()),
        target_status_after=target_condition.condition_type if target_condition and is_target_accessed(probe) else None,
        reason=changes.get("reason"),
        unsupported_card=changes.get("unsupported_card"),
        unsupported_action=changes.get("unsupported_action"),
    )
    return SearchState(
        turn=probe.turn,
        phase_label=probe.phase_label,
        hand=probe.hand,
        library=probe.library,
        battlefield=probe.battlefield,
        graveyard=probe.graveyard,
        exile=probe.exile,
        stack=probe.stack,
        mana_pool=probe.mana_pool,
        land_played_this_turn=probe.land_played_this_turn,
        actions_taken=probe.actions_taken,
        target_condition=probe.target_condition,
        target_events=probe.target_events,
        unsupported_cards=probe.unsupported_cards,
        unsupported_actions=probe.unsupported_actions,
        tapped_ids=probe.tapped_ids,
        trace=(*state.trace, action)[: config.trace_limit],
    )


def _success_if_reached(state: SearchState, config: SearchConfig, *, branches: int = 0) -> TargetAccessResult | None:
    if state.target_condition is not None and is_target_accessed(state):
        return _result(SUCCESS, True, state.target_condition, config, state, branches=branches)
    return None


def _result(
    status: str,
    success: bool,
    target: SimulationTargetCondition,
    config: SearchConfig,
    state: SearchState,
    *,
    branches: int,
) -> SearchResult:
    return SearchResult(
        status=status,
        success=success,
        target_condition=target,
        search_config=config,
        final_state=state,
        trace=SearchTrace(state.trace),
        unsupported_cards=state.unsupported_cards,
        unsupported_actions=state.unsupported_actions,
        branches_evaluated=branches,
        actions_taken=state.actions_taken,
    )


def _target_requires_missing_overlay(state: SearchState, manager: CardDefinitionManager) -> bool:
    target = state.target_condition
    if target is None or target.condition_type in {"access", "draw", "find_to_hand", "find_to_top"}:
        return False
    for card in (*state.hand, *state.library):
        if _matches(card, target) and _overlay_for_card(manager, card) is None:
            return True
    return False


def _with_unsupported(state: SearchState, cards: Iterable[str], actions: Iterable[str]) -> SearchState:
    return SearchState(
        turn=state.turn,
        phase_label=state.phase_label,
        hand=state.hand,
        library=state.library,
        battlefield=state.battlefield,
        graveyard=state.graveyard,
        exile=state.exile,
        stack=state.stack,
        mana_pool=state.mana_pool,
        land_played_this_turn=state.land_played_this_turn,
        actions_taken=state.actions_taken,
        target_condition=state.target_condition,
        target_events=state.target_events,
        unsupported_cards=(*state.unsupported_cards, *tuple(cards)),
        unsupported_actions=(*state.unsupported_actions, *tuple(actions)),
        tapped_ids=state.tapped_ids,
        trace=state.trace,
    )


def _manager(
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel] | None,
) -> CardDefinitionManager:
    if isinstance(card_definitions, CardDefinitionManager):
        return card_definitions
    rows = list(card_definitions or ())
    if not rows:
        return CardDefinitionManager()
    if all(isinstance(row, SimulationCardModel) for row in rows):
        return CardDefinitionManager(
            overlays_by_id={row.card_id: row for row in rows},  # type: ignore[union-attr]
            overlays_by_name={_normalize(row.name): row for row in rows},  # type: ignore[union-attr]
        )
    return CardDefinitionManager.from_overlay_rows(rows)  # type: ignore[arg-type]


def _overlay_for_card(manager: CardDefinitionManager, card: ExpandedLibraryCard) -> SimulationCardModel | None:
    if card.model_id and card.model_id in manager.overlays_by_id:
        return manager.overlays_by_id[card.model_id]
    return manager.overlays_by_name.get(_normalize(card.name))


def _unsupported_cards(cards: Iterable[ExpandedLibraryCard], manager: CardDefinitionManager) -> tuple[str, ...]:
    missing = [card.name for card in cards if _overlay_for_card(manager, card) is None]
    return tuple(dict.fromkeys(missing))


def _unsupported_action_types(overlay: SimulationCardModel) -> tuple[str, ...]:
    unsupported: list[str] = []
    for action in (*overlay.cast_actions, *overlay.hand_abilities, *overlay.static_effects, *overlay.etb_actions):
        if action.action_type not in SUPPORTED_ACTION_TYPES:
            unsupported.append(action.action_type)
        if action.metadata.get("requires_memory") or action.metadata.get("store_memory_as"):
            unsupported.append("memory_requirement")
    return tuple(dict.fromkeys(unsupported))


def _mana_options_for_card(overlay: SimulationCardModel | None) -> tuple[ManaOption, ...]:
    if overlay is None:
        return ()
    options: list[ManaOption] = list(overlay.produces)
    for action in overlay.board_abilities:
        if action.action_type == "tap_for_mana":
            options.extend(action.produces)
    return tuple(options)


def _can_pay(pool: dict[str, int], cost: ManaCost) -> bool:
    remaining = _mana_pool(pool)
    for color in MANA_COLOR_KEYS:
        required = getattr(cost, color)
        if remaining[color] < required:
            return False
        remaining[color] -= required
    return sum(remaining.values()) >= cost.Generic


def _pay_mana(pool: dict[str, int], cost: ManaCost) -> dict[str, int]:
    remaining = _mana_pool(pool)
    for color in MANA_COLOR_KEYS:
        remaining[color] -= getattr(cost, color)
    generic = cost.Generic
    for color in MANA_COLOR_KEYS:
        spend = min(generic, remaining[color])
        remaining[color] -= spend
        generic -= spend
        if generic == 0:
            break
    return remaining


def _add_mana(pool: dict[str, int], option: ManaOption) -> dict[str, int]:
    updated = _mana_pool(pool)
    for color in MANA_COLOR_KEYS:
        updated[color] += getattr(option, color)
    return updated


def _mana_pool(value: dict[str, int] | None = None) -> dict[str, int]:
    value = value or {}
    return {color: int(value.get(color, 0)) for color in MANA_COLOR_KEYS}


def _is_land(overlay: SimulationCardModel) -> bool:
    return "land" in {_normalize(item) for item in overlay.types}


def _is_permanent(overlay: SimulationCardModel) -> bool:
    types = {_normalize(item) for item in overlay.types}
    return bool(types.intersection({"artifact", "creature", "enchantment", "land", "planeswalker", "battle"}))


def _first_target_in_library(
    library: Iterable[ExpandedLibraryCard],
    target: SimulationTargetCondition,
) -> ExpandedLibraryCard | None:
    for card in library:
        if _matches(card, target):
            return card
    return None


def _matches(card: ExpandedLibraryCard, target: SimulationTargetCondition) -> bool:
    if target.target_card_id and card.model_id == target.target_card_id:
        return True
    return _normalize(card.name) == _normalize(target.target_card)


def _sorted_cards(cards: Iterable[ExpandedLibraryCard]) -> tuple[ExpandedLibraryCard, ...]:
    return tuple(sorted(cards, key=lambda card: (_normalize(card.name), card.physical_id)))


def _state_signature(state: SearchState) -> tuple[Any, ...]:
    return (
        tuple(card.physical_id for card in state.hand),
        tuple(card.physical_id for card in state.library),
        tuple(card.physical_id for card in state.battlefield),
        tuple(card.physical_id for card in state.graveyard),
        tuple(sorted(state.mana_pool.items())),
        state.land_played_this_turn,
        tuple(sorted(state.tapped_ids)),
        tuple(state.target_events),
    )


def _card_ref(card: ExpandedLibraryCard) -> dict[str, Any]:
    return {
        "name": card.name,
        "model_id": card.model_id,
        "physical_id": card.physical_id,
        "zone": card.zone,
    }


def _normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())
