"""Relevance classification for simulator card definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .models import SimulationActionModel, SimulationCardModel, SimulationTargetCondition


MODELED_RELEVANT = "modeled_relevant"
MODELED_IRRELEVANT = "modeled_irrelevant"
UNSUPPORTED_RELEVANT = "unsupported_relevant"
UNSUPPORTED_IRRELEVANT = "unsupported_irrelevant"
TARGET_MISSING_BEHAVIOR = "target_missing_behavior"
TARGET_MODELED = "target_modeled"

RELEVANT_ACTION_TYPES = {
    "add_mana",
    "add_mana_any",
    "draw_cards",
    "exile_from_hand_for_mana",
    "extra_land_drop",
    "grant_cast_permission",
    "mana_production_modifier",
    "sacrifice_for_mana",
    "sacrifice_to_search",
    "search_graveyard",
    "search_library",
    "tap_for_mana",
}

PENDING_REVIEW_ACTION_METADATA = {
    "conditional_mana",
    "conditional_target_requirements",
    "exclude_ids",
    "exclude_types",
    "requires_legendary",
    "requires_memory",
    "requires_metalcraft",
    "search_targets",
    "spend_restriction",
    "store_memory_as",
}

TUTOR_NAME_MARKERS = ("tutor", "wish", "transmute")
MANA_NAME_MARKERS = ("mox", "lotus", "ritual", "sol ring", "mana vault", "mana crypt", "petal")
DRAW_FILTER_NAME_MARKERS = ("brainstorm", "ponder", "preordain", "wheel", "study", "remora")


@dataclass(frozen=True)
class CardRelevanceResult:
    card_name: str
    card_id: str | None
    oracle_id: str | None
    scryfall_id: str | None
    classification: str
    relevance_reasons: tuple[str, ...] = ()
    unsupported_reasons: tuple[str, ...] = ()
    behavior_version: str | None = None
    confidence_impact: str = "none"
    pending_review_reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.card_name:
            raise ValueError("card_name is required")
        object.__setattr__(self, "relevance_reasons", tuple(self.relevance_reasons))
        object.__setattr__(self, "unsupported_reasons", tuple(self.unsupported_reasons))
        object.__setattr__(self, "pending_review_reasons", tuple(self.pending_review_reasons))

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_name": self.card_name,
            "card_id": self.card_id,
            "oracle_id": self.oracle_id,
            "scryfall_id": self.scryfall_id,
            "classification": self.classification,
            "relevance_reasons": list(self.relevance_reasons),
            "unsupported_reasons": list(self.unsupported_reasons),
            "behavior_version": self.behavior_version,
            "confidence_impact": self.confidence_impact,
            "pending_review_reasons": list(self.pending_review_reasons),
        }


def classify_card_relevance(
    card: SimulationCardModel | dict[str, Any],
    target_condition: SimulationTargetCondition,
    *,
    modeled: bool | None = None,
) -> CardRelevanceResult:
    card_model = _card_model_from_value(card) if modeled is not False else None
    payload = card_model.raw_reference_shape if card_model is not None else dict(card)
    name = str(payload.get("name", card_model.name if card_model else "")).strip()
    card_id = payload.get("card_id", payload.get("id", card_model.card_id if card_model else None))
    oracle_id = payload.get("oracle_id")
    scryfall_id = payload.get("scryfall_id")
    behavior_version = payload.get("behavior_version")
    is_modeled = card_model is not None if modeled is None else bool(modeled)

    target_match = _matches_target(name, card_id, target_condition)
    reasons = _relevance_reasons(card_model, payload, target_condition)
    pending = _pending_review_reasons(card_model) if card_model is not None else ()

    if target_match and is_modeled:
        classification = TARGET_MODELED
        confidence_impact = "none"
        reasons = _append_unique(reasons, "target_card")
    elif target_match:
        classification = TARGET_MISSING_BEHAVIOR
        confidence_impact = "invalid"
        reasons = _append_unique(reasons, "target_card")
    elif reasons and is_modeled:
        classification = MODELED_RELEVANT
        confidence_impact = "review" if pending else "none"
    elif reasons:
        classification = UNSUPPORTED_RELEVANT
        confidence_impact = "low"
    elif is_modeled:
        classification = MODELED_IRRELEVANT
        confidence_impact = "none"
    else:
        classification = UNSUPPORTED_IRRELEVANT
        confidence_impact = "note"

    unsupported = ()
    if classification in {UNSUPPORTED_RELEVANT, UNSUPPORTED_IRRELEVANT, TARGET_MISSING_BEHAVIOR}:
        unsupported = ("missing_behavior_overlay",)

    return CardRelevanceResult(
        card_name=name,
        card_id=card_id,
        oracle_id=oracle_id,
        scryfall_id=scryfall_id,
        classification=classification,
        relevance_reasons=reasons,
        unsupported_reasons=unsupported,
        behavior_version=behavior_version,
        confidence_impact=confidence_impact,
        pending_review_reasons=pending,
    )


def _card_model_from_value(card: SimulationCardModel | dict[str, Any]) -> SimulationCardModel:
    if isinstance(card, SimulationCardModel):
        return card
    return SimulationCardModel.from_mapping(card)


def _matches_target(name: str, card_id: str | None, target_condition: SimulationTargetCondition) -> bool:
    normalized_name = _normalize(name)
    return normalized_name == _normalize(target_condition.target_card) or (
        card_id is not None and card_id == target_condition.target_card_id
    )


def _relevance_reasons(
    card: SimulationCardModel | None,
    payload: dict[str, Any],
    target_condition: SimulationTargetCondition,
) -> tuple[str, ...]:
    reasons: list[str] = []
    name = str(payload.get("name", "")).lower()
    type_text = " ".join(str(item).lower() for item in payload.get("types", ()))
    type_text = f"{type_text} {str(payload.get('type_line', '')).lower()}"

    if "land" in type_text:
        reasons.append("land")
    if card is not None and card.produces:
        reasons.append("produces_mana")
    if payload.get("produced_mana"):
        reasons.append("produces_mana")
    if any(marker in name for marker in MANA_NAME_MARKERS):
        reasons.append("mana_name_marker")
    if any(marker in name for marker in TUTOR_NAME_MARKERS):
        reasons.append("tutor_name_marker")
    if target_condition.turn > 0 and any(marker in name for marker in DRAW_FILTER_NAME_MARKERS):
        reasons.append("draw_filter_name_marker")

    if card is not None:
        for action in _all_actions(card):
            if action.produces:
                reasons.append("produces_mana")
            if action.action_type in RELEVANT_ACTION_TYPES:
                reasons.append(action.action_type)

    return tuple(dict.fromkeys(reasons))


def _pending_review_reasons(card: SimulationCardModel) -> tuple[str, ...]:
    reasons: list[str] = []
    for action in _all_actions(card):
        for key in sorted(PENDING_REVIEW_ACTION_METADATA):
            if key in action.metadata:
                reasons.append(key)
        if action.requires:
            reasons.extend(f"requires:{item}" for item in action.requires)
    return tuple(dict.fromkeys(reasons))


def _all_actions(card: SimulationCardModel) -> tuple[SimulationActionModel, ...]:
    actions: list[SimulationActionModel] = []
    actions.extend(card.cast_actions)
    actions.extend(card.board_abilities)
    actions.extend(card.etb_actions)
    actions.extend(card.hand_abilities)
    actions.extend(card.static_effects)
    if card.pregame_action is not None:
        actions.append(card.pregame_action)
    return tuple(actions)


def _append_unique(values: tuple[str, ...], item: str) -> tuple[str, ...]:
    if item in values:
        return values
    return (*values, item)


def _normalize(value: str) -> str:
    return " ".join(value.lower().strip().split())
