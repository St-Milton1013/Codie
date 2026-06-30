"""Serializable Challenge Mode prompt and verification models."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable

from .card_definition_manager import CardDefinitionManager
from .models import SimulationCardModel, SimulationDeck, SimulationTargetCondition
from .search import SearchConfig, SearchResult, find_target_access_line
from .shuffle import ExpandedLibraryCard, OpeningHand, draw_opening_hand, shuffle_library


CHALLENGE_VERSION = "codie-challenge-mode-v1"
ANSWER_YES = "yes"
ANSWER_NO = "no"
ANSWER_UNKNOWN = "unknown"
ANSWER_VALUES = {ANSWER_YES, ANSWER_NO, ANSWER_UNKNOWN}


@dataclass(frozen=True)
class ChallengeConfig:
    challenge_version: str
    deck_hash: str
    base_seed: str
    game_index: int
    target_condition: SimulationTargetCondition
    search_config: SearchConfig
    hand_size: int = 7
    prompt_id: str | None = None
    generated_at: str | None = None

    def __post_init__(self) -> None:
        if not self.challenge_version:
            raise ValueError("challenge_version is required")
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        if not self.base_seed:
            raise ValueError("base_seed is required")
        if self.game_index < 0:
            raise ValueError("game_index cannot be negative")
        if self.hand_size <= 0:
            raise ValueError("hand_size must be positive")
        if self.prompt_id is not None and not self.prompt_id:
            raise ValueError("prompt_id cannot be blank")

    def to_dict(self) -> dict[str, Any]:
        return {
            "challenge_version": self.challenge_version,
            "deck_hash": self.deck_hash,
            "base_seed": self.base_seed,
            "game_index": self.game_index,
            "target_condition": self.target_condition.to_dict(),
            "search_config": self.search_config.to_dict(),
            "hand_size": self.hand_size,
            "prompt_id": self.prompt_id,
            "generated_at": self.generated_at,
        }


@dataclass(frozen=True)
class ChallengePrompt:
    challenge_id: str
    config: ChallengeConfig
    opening_hand: OpeningHand
    remaining_library: tuple[ExpandedLibraryCard, ...]
    unsupported_cards: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.challenge_id:
            raise ValueError("challenge_id is required")
        object.__setattr__(self, "remaining_library", tuple(self.remaining_library))
        object.__setattr__(self, "unsupported_cards", tuple(dict.fromkeys(self.unsupported_cards)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "challenge_id": self.challenge_id,
            "config": self.config.to_dict(),
            "opening_hand": self.opening_hand.to_dict(),
            "remaining_library": [card.to_dict() for card in self.remaining_library],
            "remaining_library_size": len(self.remaining_library),
            "unsupported_cards": list(self.unsupported_cards),
        }


@dataclass(frozen=True)
class ChallengeAnswer:
    challenge_id: str
    user_answer: str
    user_line_text: str | None = None
    answered_at: str | None = None

    def __post_init__(self) -> None:
        if not self.challenge_id:
            raise ValueError("challenge_id is required")
        if self.user_answer not in ANSWER_VALUES:
            raise ValueError("user_answer must be yes, no, or unknown")

    def to_dict(self) -> dict[str, Any]:
        return {
            "challenge_id": self.challenge_id,
            "user_answer": self.user_answer,
            "user_line_text": self.user_line_text,
            "answered_at": self.answered_at,
        }


@dataclass(frozen=True)
class ChallengeResult:
    challenge_id: str
    challenge_version: str
    deck_hash: str
    target_condition: SimulationTargetCondition
    opening_hand: tuple[str, ...]
    remaining_library_size: int
    base_seed: str
    game_index: int
    derived_seed: str
    user_answer: str
    user_line_text: str | None
    simulator_status: str
    simulator_success: bool
    simulator_trace: dict[str, Any]
    unsupported_cards: tuple[str, ...]
    unsupported_actions: tuple[str, ...]
    user_was_correct: bool | None
    generated_at: str | None = None
    completed_at: str | None = None

    def __post_init__(self) -> None:
        if not self.challenge_id:
            raise ValueError("challenge_id is required")
        if not self.challenge_version:
            raise ValueError("challenge_version is required")
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        object.__setattr__(self, "opening_hand", tuple(self.opening_hand))
        object.__setattr__(self, "simulator_trace", dict(self.simulator_trace))
        object.__setattr__(self, "unsupported_cards", tuple(dict.fromkeys(self.unsupported_cards)))
        object.__setattr__(self, "unsupported_actions", tuple(dict.fromkeys(self.unsupported_actions)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "challenge_id": self.challenge_id,
            "challenge_version": self.challenge_version,
            "deck_hash": self.deck_hash,
            "target_condition": self.target_condition.to_dict(),
            "opening_hand": list(self.opening_hand),
            "remaining_library_size": self.remaining_library_size,
            "base_seed": self.base_seed,
            "game_index": self.game_index,
            "derived_seed": self.derived_seed,
            "user_answer": self.user_answer,
            "user_line_text": self.user_line_text,
            "simulator_status": self.simulator_status,
            "simulator_success": self.simulator_success,
            "simulator_trace": dict(self.simulator_trace),
            "unsupported_cards": list(self.unsupported_cards),
            "unsupported_actions": list(self.unsupported_actions),
            "user_was_correct": self.user_was_correct,
            "generated_at": self.generated_at,
            "completed_at": self.completed_at,
        }


def generate_challenge_prompt(
    deck: SimulationDeck,
    target_condition: SimulationTargetCondition,
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel] | None,
    *,
    base_seed: str,
    game_index: int = 0,
    search_config: SearchConfig | None = None,
    hand_size: int = 7,
    challenge_version: str = CHALLENGE_VERSION,
    generated_at: str | None = None,
) -> ChallengePrompt:
    config = ChallengeConfig(
        challenge_version=challenge_version,
        deck_hash=deck.deck_hash,
        base_seed=base_seed,
        game_index=game_index,
        target_condition=target_condition,
        search_config=search_config or SearchConfig(max_turn=target_condition.turn),
        hand_size=hand_size,
        generated_at=generated_at,
    )
    shuffle_result = shuffle_library(deck, base_seed, game_index=game_index)
    opening_hand = draw_opening_hand(shuffle_result, hand_size=hand_size)
    remaining_library = tuple(shuffle_result.shuffled_cards[hand_size:])
    unsupported = _unsupported_visible_cards(opening_hand.cards, card_definitions)
    prompt = ChallengePrompt(
        challenge_id="sha256:pending",
        config=config,
        opening_hand=opening_hand,
        remaining_library=remaining_library,
        unsupported_cards=unsupported,
    )
    challenge_id = config.prompt_id or _challenge_id(prompt)
    return ChallengePrompt(
        challenge_id=challenge_id,
        config=config,
        opening_hand=opening_hand,
        remaining_library=remaining_library,
        unsupported_cards=unsupported,
    )


def record_challenge_answer(
    prompt: ChallengePrompt,
    user_answer: str,
    *,
    user_line_text: str | None = None,
    answered_at: str | None = None,
) -> ChallengeAnswer:
    return ChallengeAnswer(
        challenge_id=prompt.challenge_id,
        user_answer=user_answer,
        user_line_text=user_line_text,
        answered_at=answered_at,
    )


def verify_challenge_answer(
    prompt: ChallengePrompt,
    answer: ChallengeAnswer,
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
    *,
    completed_at: str | None = None,
) -> ChallengeResult:
    if answer.challenge_id != prompt.challenge_id:
        raise ValueError("answer challenge_id does not match prompt")
    search_result = find_target_access_line(
        prompt.opening_hand,
        prompt.config.target_condition,
        card_definitions,
        library=prompt.remaining_library,
        config=prompt.config.search_config,
    )
    return _challenge_result(prompt, answer, search_result, completed_at=completed_at)


def serialize_challenge_result(result: ChallengeResult) -> dict[str, Any]:
    return result.to_dict()


def _challenge_result(
    prompt: ChallengePrompt,
    answer: ChallengeAnswer,
    search_result: SearchResult,
    *,
    completed_at: str | None,
) -> ChallengeResult:
    unsupported_cards = (*prompt.unsupported_cards, *search_result.unsupported_cards)
    user_was_correct = _user_was_correct(answer.user_answer, search_result)
    return ChallengeResult(
        challenge_id=prompt.challenge_id,
        challenge_version=prompt.config.challenge_version,
        deck_hash=prompt.config.deck_hash,
        target_condition=prompt.config.target_condition,
        opening_hand=tuple(card.name for card in prompt.opening_hand.cards),
        remaining_library_size=len(prompt.remaining_library),
        base_seed=prompt.config.base_seed,
        game_index=prompt.config.game_index,
        derived_seed=prompt.opening_hand.derived_seed,
        user_answer=answer.user_answer,
        user_line_text=answer.user_line_text,
        simulator_status=search_result.status,
        simulator_success=search_result.success,
        simulator_trace=search_result.trace.to_dict(),
        unsupported_cards=unsupported_cards,
        unsupported_actions=search_result.unsupported_actions,
        user_was_correct=user_was_correct,
        generated_at=prompt.config.generated_at,
        completed_at=completed_at or answer.answered_at,
    )


def _user_was_correct(user_answer: str, search_result: SearchResult) -> bool | None:
    if user_answer == ANSWER_UNKNOWN or search_result.status in {"unsupported", "invalid_target"}:
        return None
    if user_answer == ANSWER_YES:
        return bool(search_result.success)
    if user_answer == ANSWER_NO:
        return not bool(search_result.success)
    return None


def _unsupported_visible_cards(
    cards: Iterable[ExpandedLibraryCard],
    card_definitions: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel] | None,
) -> tuple[str, ...]:
    manager = _manager(card_definitions)
    missing = []
    for card in cards:
        if card.model_id and card.model_id in manager.overlays_by_id:
            continue
        if _normalize(card.name) in manager.overlays_by_name:
            continue
        missing.append(card.name)
    return tuple(dict.fromkeys(missing))


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


def _challenge_id(prompt: ChallengePrompt) -> str:
    payload = {
        "config": prompt.config.to_dict(),
        "opening_hand": prompt.opening_hand.to_dict(),
        "remaining_library": [card.to_dict() for card in prompt.remaining_library],
    }
    return "sha256:" + hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())
