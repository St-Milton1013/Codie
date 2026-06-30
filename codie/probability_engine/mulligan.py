"""Deterministic London mulligan policy evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .models import SimulationDeck
from .shuffle import ExpandedLibraryCard, OpeningHand, draw_opening_hand, shuffle_library


KEEP = "keep"
REJECT = "reject"
FORCED_KEEP_MINIMUM_SIZE = "forced_keep_minimum_size"
INVALID_POLICY = "invalid_policy"


@dataclass(frozen=True)
class MulliganPolicyConfig:
    policy_name: str
    policy_version: str
    minimum_keep_size: int
    max_mulligans: int
    keep_rules: dict[str, Any] = field(default_factory=dict)
    bottoming_rules: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.policy_name:
            raise ValueError("policy_name is required")
        if not self.policy_version:
            raise ValueError("policy_version is required")
        if self.minimum_keep_size <= 0 or self.minimum_keep_size > 7:
            raise ValueError("minimum_keep_size must be between 1 and 7")
        if self.max_mulligans < 0:
            raise ValueError("max_mulligans cannot be negative")
        object.__setattr__(self, "keep_rules", dict(self.keep_rules))
        object.__setattr__(self, "bottoming_rules", dict(self.bottoming_rules))

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_name": self.policy_name,
            "policy_version": self.policy_version,
            "minimum_keep_size": self.minimum_keep_size,
            "max_mulligans": self.max_mulligans,
            "keep_rules": dict(self.keep_rules),
            "bottoming_rules": dict(self.bottoming_rules),
        }


@dataclass(frozen=True)
class MulliganDecision:
    decision: str
    reason_codes: tuple[str, ...]
    hand_id: str
    hand_size: int
    land_count: int
    mana_source_count: int
    required_cards_present: bool
    unresolved_cards: tuple[str, ...]
    policy_name: str
    policy_version: str

    def __post_init__(self) -> None:
        if self.decision not in {KEEP, REJECT, FORCED_KEEP_MINIMUM_SIZE, INVALID_POLICY}:
            raise ValueError("unsupported decision")
        object.__setattr__(self, "reason_codes", tuple(self.reason_codes))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "reason_codes": list(self.reason_codes),
            "hand_id": self.hand_id,
            "hand_size": self.hand_size,
            "land_count": self.land_count,
            "mana_source_count": self.mana_source_count,
            "required_cards_present": self.required_cards_present,
            "unresolved_cards": list(self.unresolved_cards),
            "policy_name": self.policy_name,
            "policy_version": self.policy_version,
        }


@dataclass(frozen=True)
class MulliganStep:
    attempt_index: int
    game_index: int
    opening_hand: OpeningHand
    decision: MulliganDecision
    reason_codes: tuple[str, ...]
    bottomed_cards: tuple[ExpandedLibraryCard, ...] = ()
    kept_cards_after_bottom: tuple[ExpandedLibraryCard, ...] = ()

    def __post_init__(self) -> None:
        if self.attempt_index < 0:
            raise ValueError("attempt_index cannot be negative")
        if self.game_index < 0:
            raise ValueError("game_index cannot be negative")
        object.__setattr__(self, "reason_codes", tuple(self.reason_codes))
        object.__setattr__(self, "bottomed_cards", tuple(self.bottomed_cards))
        object.__setattr__(self, "kept_cards_after_bottom", tuple(self.kept_cards_after_bottom))

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_index": self.attempt_index,
            "game_index": self.game_index,
            "opening_hand": self.opening_hand.to_dict(),
            "decision": self.decision.to_dict(),
            "reason_codes": list(self.reason_codes),
            "bottomed_cards": [card.to_dict() for card in self.bottomed_cards],
            "kept_cards_after_bottom": [card.to_dict() for card in self.kept_cards_after_bottom],
        }


@dataclass(frozen=True)
class MulliganResult:
    deck_hash: str
    base_seed: str
    policy_name: str
    policy_version: str
    minimum_keep_size: int
    mulligan_count: int
    kept_hand: OpeningHand
    bottomed_cards: tuple[ExpandedLibraryCard, ...]
    steps: tuple[MulliganStep, ...]
    unresolved_cards: tuple[str, ...] = ()
    created_at: str | None = None

    def __post_init__(self) -> None:
        if self.mulligan_count < 0:
            raise ValueError("mulligan_count cannot be negative")
        object.__setattr__(self, "bottomed_cards", tuple(self.bottomed_cards))
        object.__setattr__(self, "steps", tuple(self.steps))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "base_seed": self.base_seed,
            "policy_name": self.policy_name,
            "policy_version": self.policy_version,
            "minimum_keep_size": self.minimum_keep_size,
            "mulligan_count": self.mulligan_count,
            "kept_hand": self.kept_hand.to_dict(),
            "bottomed_cards": [card.to_dict() for card in self.bottomed_cards],
            "steps": [step.to_dict() for step in self.steps],
            "unresolved_cards": list(self.unresolved_cards),
            "created_at": self.created_at,
        }


def evaluate_opening_hand(
    opening_hand: OpeningHand,
    policy: MulliganPolicyConfig,
    *,
    mulligan_count: int = 0,
) -> MulliganDecision:
    land_count = _count_matches(opening_hand.cards, policy.keep_rules, "land")
    mana_source_count = _count_matches(opening_hand.cards, policy.keep_rules, "mana_source")
    required_present = _required_cards_present(opening_hand.cards, policy.keep_rules)
    unresolved = tuple(card.name for card in opening_hand.cards if card.name in set(opening_hand.unresolved_cards))
    reason_codes: list[str] = []

    if land_count < int(policy.keep_rules.get("min_lands", 0)):
        reason_codes.append("land_count_below_minimum")
    max_lands = policy.keep_rules.get("max_lands")
    if max_lands is not None and land_count > int(max_lands):
        reason_codes.append("land_count_above_maximum")
    if not required_present:
        reason_codes.append("missing_required_card")
    if mana_source_count < int(policy.keep_rules.get("minimum_mana_sources", 0)):
        reason_codes.append("mana_sources_below_minimum")
    if unresolved and not bool(policy.keep_rules.get("allow_unresolved_cards", True)):
        reason_codes.append("unresolved_cards_disallowed")

    final_size_after_next_reject = 7 - (mulligan_count + 1)
    if reason_codes and (
        final_size_after_next_reject < policy.minimum_keep_size or mulligan_count >= policy.max_mulligans
    ):
        reason_codes.append("minimum_keep_size_reached")
        decision = FORCED_KEEP_MINIMUM_SIZE
    elif reason_codes:
        decision = REJECT
    else:
        reason_codes.append("policy_conditions_met")
        decision = KEEP

    return MulliganDecision(
        decision=decision,
        reason_codes=tuple(reason_codes),
        hand_id=opening_hand.hand_id,
        hand_size=opening_hand.hand_size,
        land_count=land_count,
        mana_source_count=mana_source_count,
        required_cards_present=required_present,
        unresolved_cards=unresolved,
        policy_name=policy.policy_name,
        policy_version=policy.policy_version,
    )


def select_bottom_cards(
    opening_hand: OpeningHand,
    policy: MulliganPolicyConfig,
    bottom_count: int,
) -> tuple[tuple[ExpandedLibraryCard, ...], tuple[ExpandedLibraryCard, ...]]:
    if bottom_count < 0:
        raise ValueError("bottom_count cannot be negative")
    if bottom_count > len(opening_hand.cards):
        raise ValueError("bottom_count cannot exceed hand size")
    if bottom_count == 0:
        return (), tuple(opening_hand.cards)

    protected_names = {_normalize(name) for name in policy.bottoming_rules.get("protected_card_names", ())}
    protected_ids = set(policy.bottoming_rules.get("protected_model_ids", ()))
    candidates = [
        card
        for card in opening_hand.cards
        if _normalize(card.name) not in protected_names and card.model_id not in protected_ids
    ]
    if len(candidates) < bottom_count:
        candidates = list(opening_hand.cards)

    selected: list[ExpandedLibraryCard] = []
    if policy.bottoming_rules.get("bottom_unresolved_first", False):
        unresolved = set(opening_hand.unresolved_cards)
        selected.extend(card for card in reversed(candidates) if card.name in unresolved)
    if policy.bottoming_rules.get("bottom_highest_name_sort_last", False):
        selected.extend(sorted(candidates, key=lambda card: (_normalize(card.name), card.physical_id), reverse=True))
    if policy.bottoming_rules.get("bottom_from_end_of_hand", True):
        selected.extend(reversed(candidates))

    selected_unique: list[ExpandedLibraryCard] = []
    seen: set[str] = set()
    for card in selected:
        if card.physical_id not in seen:
            selected_unique.append(card)
            seen.add(card.physical_id)
        if len(selected_unique) == bottom_count:
            break
    bottomed = tuple(selected_unique)
    bottomed_ids = {card.physical_id for card in bottomed}
    kept = tuple(card for card in opening_hand.cards if card.physical_id not in bottomed_ids)
    return bottomed, kept


def simulate_london_mulligan(
    deck: SimulationDeck,
    base_seed: str,
    policy: MulliganPolicyConfig,
    *,
    game_index_offset: int = 0,
    created_at: str | None = None,
) -> MulliganResult:
    steps: list[MulliganStep] = []
    attempt_index = 0
    while True:
        game_index = game_index_offset + attempt_index
        opening_hand = draw_opening_hand(shuffle_library(deck, base_seed, game_index=game_index))
        decision = evaluate_opening_hand(opening_hand, policy, mulligan_count=attempt_index)
        bottomed: tuple[ExpandedLibraryCard, ...] = ()
        kept_after_bottom: tuple[ExpandedLibraryCard, ...] = tuple(opening_hand.cards)
        should_stop = decision.decision in {KEEP, FORCED_KEEP_MINIMUM_SIZE, INVALID_POLICY}
        if should_stop:
            bottomed, kept_after_bottom = select_bottom_cards(opening_hand, policy, attempt_index)
        steps.append(
            MulliganStep(
                attempt_index=attempt_index,
                game_index=game_index,
                opening_hand=opening_hand,
                decision=decision,
                reason_codes=decision.reason_codes,
                bottomed_cards=bottomed,
                kept_cards_after_bottom=kept_after_bottom,
            )
        )
        if should_stop:
            return MulliganResult(
                deck_hash=deck.deck_hash,
                base_seed=base_seed,
                policy_name=policy.policy_name,
                policy_version=policy.policy_version,
                minimum_keep_size=policy.minimum_keep_size,
                mulligan_count=attempt_index,
                kept_hand=opening_hand,
                bottomed_cards=bottomed,
                steps=tuple(steps),
                unresolved_cards=tuple(deck.unresolved_cards),
                created_at=created_at,
            )
        attempt_index += 1


def _count_matches(cards: tuple[ExpandedLibraryCard, ...], rules: dict[str, Any], prefix: str) -> int:
    names = {_normalize(name) for name in rules.get(f"{prefix}_names", ())}
    ids = set(rules.get(f"{prefix}_model_ids", ()))
    return sum(1 for card in cards if _normalize(card.name) in names or card.model_id in ids)


def _required_cards_present(cards: tuple[ExpandedLibraryCard, ...], rules: dict[str, Any]) -> bool:
    names = {_normalize(name) for name in rules.get("required_card_names", ())}
    ids = set(rules.get("required_model_ids", ()))
    hand_names = {_normalize(card.name) for card in cards}
    hand_ids = {card.model_id for card in cards if card.model_id is not None}
    return names.issubset(hand_names) and ids.issubset(hand_ids)


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())
