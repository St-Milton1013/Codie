"""In-memory card definition manager for simulator readiness."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .models import SimulationCardModel, SimulationDeck, SimulationDeckCard, SimulationTargetCondition
from .relevance import (
    MODELED_IRRELEVANT,
    MODELED_RELEVANT,
    TARGET_MISSING_BEHAVIOR,
    TARGET_MODELED,
    UNSUPPORTED_IRRELEVANT,
    UNSUPPORTED_RELEVANT,
    CardRelevanceResult,
    classify_card_relevance,
)


class CardDefinitionStatus:
    MODELED_RELEVANT = MODELED_RELEVANT
    MODELED_IRRELEVANT = MODELED_IRRELEVANT
    UNSUPPORTED_RELEVANT = UNSUPPORTED_RELEVANT
    UNSUPPORTED_IRRELEVANT = UNSUPPORTED_IRRELEVANT
    TARGET_MISSING_BEHAVIOR = TARGET_MISSING_BEHAVIOR
    TARGET_MODELED = TARGET_MODELED


@dataclass(frozen=True)
class UnsupportedCardRecord:
    card_name: str
    card_id: str | None
    oracle_id: str | None
    scryfall_id: str | None
    deck_hash: str
    target_condition: dict[str, Any]
    unsupported_reason: str
    relevance_classification: str
    first_seen_at: str | None = None
    last_seen_at: str | None = None
    seen_count: int = 1

    def __post_init__(self) -> None:
        if not self.card_name:
            raise ValueError("card_name is required")
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        if self.seen_count <= 0:
            raise ValueError("seen_count must be positive")
        object.__setattr__(self, "target_condition", dict(self.target_condition))

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_name": self.card_name,
            "card_id": self.card_id,
            "oracle_id": self.oracle_id,
            "scryfall_id": self.scryfall_id,
            "deck_hash": self.deck_hash,
            "target_condition": dict(self.target_condition),
            "unsupported_reason": self.unsupported_reason,
            "relevance_classification": self.relevance_classification,
            "first_seen_at": self.first_seen_at,
            "last_seen_at": self.last_seen_at,
            "seen_count": self.seen_count,
        }


@dataclass(frozen=True)
class CardDefinitionLoadResult:
    deck_hash: str
    target_condition: SimulationTargetCondition
    cards_total: int
    cards_modeled_relevant: int
    cards_modeled_irrelevant: int
    cards_unsupported_relevant: int
    cards_unsupported_irrelevant: int
    confidence_level: str
    modeled_card_ids: tuple[str, ...] = ()
    unsupported_relevant_cards: tuple[UnsupportedCardRecord, ...] = ()
    unsupported_irrelevant_cards: tuple[UnsupportedCardRecord, ...] = ()
    pending_review_cards: tuple[CardRelevanceResult, ...] = ()
    behavior_overlay_versions: tuple[str, ...] = ()
    relevance_results: tuple[CardRelevanceResult, ...] = ()
    generated_at: str | None = None

    def __post_init__(self) -> None:
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        for field_name in (
            "modeled_card_ids",
            "unsupported_relevant_cards",
            "unsupported_irrelevant_cards",
            "pending_review_cards",
            "behavior_overlay_versions",
            "relevance_results",
        ):
            object.__setattr__(self, field_name, tuple(getattr(self, field_name)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "target_condition": self.target_condition.to_dict(),
            "cards_total": self.cards_total,
            "cards_modeled_relevant": self.cards_modeled_relevant,
            "cards_modeled_irrelevant": self.cards_modeled_irrelevant,
            "cards_unsupported_relevant": self.cards_unsupported_relevant,
            "cards_unsupported_irrelevant": self.cards_unsupported_irrelevant,
            "confidence_level": self.confidence_level,
            "modeled_card_ids": list(self.modeled_card_ids),
            "unsupported_relevant_cards": [item.to_dict() for item in self.unsupported_relevant_cards],
            "unsupported_irrelevant_cards": [item.to_dict() for item in self.unsupported_irrelevant_cards],
            "pending_review_cards": [item.to_dict() for item in self.pending_review_cards],
            "behavior_overlay_versions": list(self.behavior_overlay_versions),
            "relevance_results": [item.to_dict() for item in self.relevance_results],
            "generated_at": self.generated_at,
        }


@dataclass(frozen=True)
class CardDefinitionManager:
    overlays_by_id: dict[str, SimulationCardModel] = field(default_factory=dict)
    overlays_by_name: dict[str, SimulationCardModel] = field(default_factory=dict)

    @classmethod
    def from_overlay_rows(cls, rows: Iterable[dict[str, Any]]) -> "CardDefinitionManager":
        overlays = load_behavior_overlay_rows(rows)
        return cls(
            overlays_by_id={card.card_id: card for card in overlays},
            overlays_by_name={_normalize(card.name): card for card in overlays},
        )

    def overlay_for_deck_card(self, card: SimulationDeckCard) -> SimulationCardModel | None:
        if card.model_id and card.model_id in self.overlays_by_id:
            return self.overlays_by_id[card.model_id]
        return self.overlays_by_name.get(_normalize(card.name))

    def build_load_result(
        self,
        deck: SimulationDeck,
        target_condition: SimulationTargetCondition,
        *,
        generated_at: str | None = None,
    ) -> CardDefinitionLoadResult:
        return build_card_definition_load_result(deck, target_condition, self, generated_at=generated_at)


def load_behavior_overlay_rows(rows: Iterable[dict[str, Any]]) -> tuple[SimulationCardModel, ...]:
    overlays: list[SimulationCardModel] = []
    seen_ids: set[str] = set()
    for row in rows:
        card = SimulationCardModel.from_mapping(row)
        if card.card_id in seen_ids:
            raise ValueError(f"duplicate behavior overlay card_id: {card.card_id}")
        seen_ids.add(card.card_id)
        overlays.append(card)
    return tuple(overlays)


def build_card_definition_load_result(
    deck: SimulationDeck,
    target_condition: SimulationTargetCondition,
    overlays: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
    *,
    generated_at: str | None = None,
) -> CardDefinitionLoadResult:
    manager = _manager_from_overlays(overlays)
    relevance_results: list[CardRelevanceResult] = []
    unsupported_relevant: list[UnsupportedCardRecord] = []
    unsupported_irrelevant: list[UnsupportedCardRecord] = []
    pending_review: list[CardRelevanceResult] = []
    modeled_ids: list[str] = []
    versions: list[str] = []

    deck_cards = (*deck.cards, *deck.commanders)
    for deck_card in deck_cards:
        overlay = manager.overlay_for_deck_card(deck_card)
        if overlay is None:
            payload = {"name": deck_card.name, "card_id": deck_card.model_id}
            result = classify_card_relevance(payload, target_condition, modeled=False)
        else:
            result = classify_card_relevance(overlay, target_condition, modeled=True)
            modeled_ids.append(overlay.card_id)
            if result.behavior_version:
                versions.append(result.behavior_version)

        relevance_results.append(result)
        if result.pending_review_reasons:
            pending_review.append(result)
        if result.classification in {UNSUPPORTED_RELEVANT, TARGET_MISSING_BEHAVIOR}:
            unsupported_relevant.append(_unsupported_record(deck, target_condition, result))
        elif result.classification == UNSUPPORTED_IRRELEVANT:
            unsupported_irrelevant.append(_unsupported_record(deck, target_condition, result))

    modeled_relevant_count = sum(
        1 for item in relevance_results if item.classification in {MODELED_RELEVANT, TARGET_MODELED}
    )
    modeled_irrelevant_count = sum(1 for item in relevance_results if item.classification == MODELED_IRRELEVANT)

    return CardDefinitionLoadResult(
        deck_hash=deck.deck_hash,
        target_condition=target_condition,
        cards_total=sum(card.quantity for card in deck_cards),
        cards_modeled_relevant=modeled_relevant_count,
        cards_modeled_irrelevant=modeled_irrelevant_count,
        cards_unsupported_relevant=len(unsupported_relevant),
        cards_unsupported_irrelevant=len(unsupported_irrelevant),
        confidence_level=_confidence_level(relevance_results),
        modeled_card_ids=tuple(dict.fromkeys(modeled_ids)),
        unsupported_relevant_cards=tuple(unsupported_relevant),
        unsupported_irrelevant_cards=tuple(unsupported_irrelevant),
        pending_review_cards=tuple(pending_review),
        behavior_overlay_versions=tuple(dict.fromkeys(versions)),
        relevance_results=tuple(relevance_results),
        generated_at=generated_at,
    )


def _manager_from_overlays(
    overlays: CardDefinitionManager | Iterable[dict[str, Any]] | Iterable[SimulationCardModel],
) -> CardDefinitionManager:
    if isinstance(overlays, CardDefinitionManager):
        return overlays
    rows = list(overlays)
    if not rows:
        return CardDefinitionManager()
    if all(isinstance(row, SimulationCardModel) for row in rows):
        return CardDefinitionManager(
            overlays_by_id={row.card_id: row for row in rows},  # type: ignore[union-attr]
            overlays_by_name={_normalize(row.name): row for row in rows},  # type: ignore[union-attr]
        )
    return CardDefinitionManager.from_overlay_rows(rows)  # type: ignore[arg-type]


def _unsupported_record(
    deck: SimulationDeck,
    target_condition: SimulationTargetCondition,
    result: CardRelevanceResult,
) -> UnsupportedCardRecord:
    reason = result.unsupported_reasons[0] if result.unsupported_reasons else "unsupported"
    return UnsupportedCardRecord(
        card_name=result.card_name,
        card_id=result.card_id,
        oracle_id=result.oracle_id,
        scryfall_id=result.scryfall_id,
        deck_hash=deck.deck_hash,
        target_condition=target_condition.to_dict(),
        unsupported_reason=reason,
        relevance_classification=result.classification,
    )


def _confidence_level(results: list[CardRelevanceResult]) -> str:
    if any(item.classification == TARGET_MISSING_BEHAVIOR for item in results):
        return "invalid"
    if any(item.classification == UNSUPPORTED_RELEVANT for item in results):
        return "low"
    if any(item.pending_review_reasons for item in results):
        return "medium"
    return "high"


def _normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())
