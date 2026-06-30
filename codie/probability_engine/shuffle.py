"""Deterministic library expansion and opening-hand generation."""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from typing import Any, Iterable

from .models import SimulationDeck, SimulationDeckCard


SHUFFLE_ALGORITHM_VERSION = "codie-shuffle-random-v1"


@dataclass(frozen=True)
class ExpandedLibraryCard:
    name: str
    model_id: str | None
    zone: str
    source_quantity: int
    copy_index: int
    physical_id: str

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name is required")
        if not self.zone:
            raise ValueError("zone is required")
        if self.source_quantity <= 0:
            raise ValueError("source_quantity must be positive")
        if self.copy_index <= 0:
            raise ValueError("copy_index must be positive")
        if not self.physical_id:
            raise ValueError("physical_id is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "model_id": self.model_id,
            "zone": self.zone,
            "source_quantity": self.source_quantity,
            "copy_index": self.copy_index,
            "physical_id": self.physical_id,
        }


@dataclass(frozen=True)
class ExpandedLibrary:
    deck_hash: str
    cards: tuple[ExpandedLibraryCard, ...]
    unresolved_cards: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        object.__setattr__(self, "cards", tuple(self.cards))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))

    @property
    def cards_total(self) -> int:
        return len(self.cards)

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "cards": [card.to_dict() for card in self.cards],
            "cards_total": self.cards_total,
            "unresolved_cards": list(self.unresolved_cards),
        }


@dataclass(frozen=True)
class ShuffleResult:
    deck_hash: str
    base_seed: str
    game_index: int
    derived_seed: str
    shuffle_algorithm_version: str
    shuffled_cards: tuple[ExpandedLibraryCard, ...]
    unresolved_cards: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        if not self.base_seed:
            raise ValueError("base_seed is required")
        if self.game_index < 0:
            raise ValueError("game_index cannot be negative")
        if not self.derived_seed.startswith("sha256:"):
            raise ValueError("derived_seed must be sha256-prefixed")
        if not self.shuffle_algorithm_version:
            raise ValueError("shuffle_algorithm_version is required")
        object.__setattr__(self, "shuffled_cards", tuple(self.shuffled_cards))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))

    @property
    def library_size(self) -> int:
        return len(self.shuffled_cards)

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "base_seed": self.base_seed,
            "game_index": self.game_index,
            "derived_seed": self.derived_seed,
            "shuffle_algorithm_version": self.shuffle_algorithm_version,
            "library_size": self.library_size,
            "shuffled_cards": [card.to_dict() for card in self.shuffled_cards],
            "unresolved_cards": list(self.unresolved_cards),
        }


@dataclass(frozen=True)
class OpeningHand:
    deck_hash: str
    base_seed: str
    game_index: int
    derived_seed: str
    shuffle_algorithm_version: str
    hand_size: int
    cards: tuple[ExpandedLibraryCard, ...]
    hand_id: str
    remaining_library_size: int
    unresolved_cards: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.hand_size <= 0:
            raise ValueError("hand_size must be positive")
        if len(self.cards) != self.hand_size:
            raise ValueError("hand_size must match cards")
        if not self.hand_id.startswith("sha256:"):
            raise ValueError("hand_id must be sha256-prefixed")
        if self.remaining_library_size < 0:
            raise ValueError("remaining_library_size cannot be negative")
        object.__setattr__(self, "cards", tuple(self.cards))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "base_seed": self.base_seed,
            "game_index": self.game_index,
            "derived_seed": self.derived_seed,
            "shuffle_algorithm_version": self.shuffle_algorithm_version,
            "hand_size": self.hand_size,
            "cards": [card.to_dict() for card in self.cards],
            "hand_id": self.hand_id,
            "remaining_library_size": self.remaining_library_size,
            "unresolved_cards": list(self.unresolved_cards),
        }


def expand_library(deck: SimulationDeck) -> ExpandedLibrary:
    expanded: list[ExpandedLibraryCard] = []
    for card in _sorted_deck_cards(deck.cards):
        for copy_index in range(1, card.quantity + 1):
            expanded.append(
                ExpandedLibraryCard(
                    name=card.name,
                    model_id=card.model_id,
                    zone=card.zone,
                    source_quantity=card.quantity,
                    copy_index=copy_index,
                    physical_id=_physical_id(deck.deck_hash, card, copy_index),
                )
            )
    return ExpandedLibrary(
        deck_hash=deck.deck_hash,
        cards=tuple(expanded),
        unresolved_cards=tuple(deck.unresolved_cards),
    )


def derive_game_seed(
    deck_hash: str,
    base_seed: str,
    game_index: int = 0,
    *,
    shuffle_algorithm_version: str = SHUFFLE_ALGORITHM_VERSION,
) -> str:
    if not deck_hash:
        raise ValueError("deck_hash is required")
    if not isinstance(base_seed, str) or not base_seed:
        raise ValueError("base_seed is required")
    if isinstance(game_index, bool) or not isinstance(game_index, int) or game_index < 0:
        raise ValueError("game_index must be a non-negative integer")
    payload = f"{deck_hash}|{base_seed}|{game_index}|{shuffle_algorithm_version}"
    return _sha256_text(payload)


def shuffle_library(
    deck: SimulationDeck,
    seed: str,
    *,
    game_index: int = 0,
    shuffle_algorithm_version: str = SHUFFLE_ALGORITHM_VERSION,
) -> ShuffleResult:
    library = expand_library(deck)
    derived_seed = derive_game_seed(
        deck.deck_hash,
        seed,
        game_index,
        shuffle_algorithm_version=shuffle_algorithm_version,
    )
    seed_int = int(derived_seed.removeprefix("sha256:"), 16)
    shuffled = list(library.cards)
    random.Random(seed_int).shuffle(shuffled)
    return ShuffleResult(
        deck_hash=deck.deck_hash,
        base_seed=seed,
        game_index=game_index,
        derived_seed=derived_seed,
        shuffle_algorithm_version=shuffle_algorithm_version,
        shuffled_cards=tuple(shuffled),
        unresolved_cards=library.unresolved_cards,
    )


def draw_opening_hand(shuffle_result: ShuffleResult, hand_size: int = 7) -> OpeningHand:
    if isinstance(hand_size, bool) or not isinstance(hand_size, int) or hand_size <= 0:
        raise ValueError("hand_size must be a positive integer")
    if hand_size > shuffle_result.library_size:
        raise ValueError("hand_size cannot exceed library size")
    cards = tuple(shuffle_result.shuffled_cards[:hand_size])
    hand = OpeningHand(
        deck_hash=shuffle_result.deck_hash,
        base_seed=shuffle_result.base_seed,
        game_index=shuffle_result.game_index,
        derived_seed=shuffle_result.derived_seed,
        shuffle_algorithm_version=shuffle_result.shuffle_algorithm_version,
        hand_size=hand_size,
        cards=cards,
        hand_id="sha256:pending",
        remaining_library_size=shuffle_result.library_size - hand_size,
        unresolved_cards=shuffle_result.unresolved_cards,
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


def opening_hand_id(opening_hand: OpeningHand) -> str:
    payload = {
        "deck_hash": opening_hand.deck_hash,
        "derived_seed": opening_hand.derived_seed,
        "game_index": opening_hand.game_index,
        "hand_size": opening_hand.hand_size,
        "shuffle_algorithm_version": opening_hand.shuffle_algorithm_version,
        "cards": [card.to_dict() for card in opening_hand.cards],
    }
    return _sha256_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def _sorted_deck_cards(cards: Iterable[SimulationDeckCard]) -> list[SimulationDeckCard]:
    return sorted(cards, key=lambda card: (_normalize(card.name), card.model_id or "", card.zone))


def _physical_id(deck_hash: str, card: SimulationDeckCard, copy_index: int) -> str:
    payload = {
        "deck_hash": deck_hash,
        "zone": card.zone,
        "name": _normalize(card.name),
        "model_id": card.model_id,
        "source_quantity": card.quantity,
        "copy_index": copy_index,
    }
    return _sha256_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def _sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())
