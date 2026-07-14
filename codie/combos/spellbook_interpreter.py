"""Local Commander Spellbook combo interpretation models.

This module classifies already-provided Spellbook combo payloads. It does not
fetch Spellbook data, import provider code, persist records, execute simulator
logic, rank combos, or generate recommendations.
"""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping


SPELLBOOK_INTERPRETER_VERSION = "1.0"
SPELLBOOK_PROVIDER = "commander_spellbook"

OUTPUT_CLASSES = frozenset(
    {
        "infinite_mana",
        "infinite_draw",
        "infinite_damage",
        "infinite_tokens",
        "infinite_life",
        "mill",
        "storm",
        "combat",
        "lock",
        "win_condition",
        "card_advantage",
        "mana_generation",
        "board_state",
        "unknown",
    }
)

REQUIREMENT_CLASSES = frozenset(
    {
        "requires_commander",
        "requires_battlefield",
        "requires_hand",
        "requires_graveyard",
        "requires_library",
        "requires_mana",
        "requires_tap",
        "requires_untap",
        "requires_cast",
        "requires_opponent",
        "requires_specific_zone",
        "color_requirement",
        "timing_requirement",
        "once_per_turn_limit",
        "summoning_sickness_sensitive",
        "unknown_requirement",
    }
)

TARGET_COMPATIBILITY_VALUES = frozenset(
    {
        "can_satisfy_target_output_class",
        "might_satisfy_target_output_class",
        "cannot_classify_against_target",
        "unsupported_compatibility_condition",
    }
)

FORBIDDEN_STRATEGIC_LANGUAGE = (
    "should include",
    "should cut",
    "must include",
    "must cut",
    "strict upgrade",
    "auto-include",
    "recommended include",
    "recommended cut",
    "secretly optimal",
    "breaks the format",
)


class SpellbookInterpreterError(ValueError):
    """Raised when a Spellbook interpretation packet is invalid."""


@dataclass(frozen=True)
class SpellbookComboSourceRef:
    provider: str
    provider_combo_id: str
    combo_url: str | None = None
    raw_payload_hash: str | None = None


@dataclass(frozen=True)
class SpellbookComponentRef:
    card_name: str
    role: str | None = None
    required: bool = True
    scryfall_id: str | None = None
    oracle_id: str | None = None
    source_ref: str | None = None


@dataclass(frozen=True)
class SpellbookInterpretationClass:
    class_value: str
    source_text: str
    confidence: float = 1.0


@dataclass(frozen=True)
class SpellbookPrerequisite:
    prerequisite_class: str
    source_text: str
    confidence: float = 1.0


@dataclass(frozen=True)
class SpellbookOutput:
    output_class: str
    source_text: str
    confidence: float = 1.0
    win_enabling: bool = False


@dataclass(frozen=True)
class SpellbookRestriction:
    restriction_class: str
    source_text: str
    confidence: float = 1.0


@dataclass(frozen=True)
class SpellbookTargetCompatibility:
    target_output_class: str
    compatibility: str
    source_output_class: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class SpellbookUnsupportedItem:
    item_type: str
    source_text: str
    reason: str


@dataclass(frozen=True)
class SpellbookManualReviewItem:
    item_type: str
    source_text: str
    reason: str


@dataclass(frozen=True)
class SpellbookInterpreterWarning:
    warning_type: str
    message: str


@dataclass(frozen=True)
class SpellbookInterpreterOptions:
    include_manual_review_items: bool = True
    include_unsupported_items: bool = True
    target_output_classes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SpellbookComboInterpretation:
    interpreter_version: str
    provider: str
    provider_combo_id: str
    combo_url: str | None
    combo_name: str | None
    variant_ids: tuple[str, ...]
    component_refs: tuple[SpellbookComponentRef, ...]
    component_roles: tuple[SpellbookInterpretationClass, ...]
    prerequisite_classes: tuple[SpellbookPrerequisite, ...]
    output_classes: tuple[SpellbookOutput, ...]
    restriction_classes: tuple[SpellbookRestriction, ...]
    target_compatibility_items: tuple[SpellbookTargetCompatibility, ...]
    unsupported_items: tuple[SpellbookUnsupportedItem, ...]
    manual_review_items: tuple[SpellbookManualReviewItem, ...]
    source_refs: tuple[SpellbookComboSourceRef, ...]
    generated_at: str
    warnings: tuple[SpellbookInterpreterWarning, ...] = ()


def build_spellbook_combo_interpretation(
    combo: Mapping[str, Any] | Any,
    *,
    options: SpellbookInterpreterOptions | None = None,
    generated_at: str = "1970-01-01T00:00:00Z",
) -> SpellbookComboInterpretation:
    """Build a deterministic interpretation from a local combo payload."""

    opts = options or SpellbookInterpreterOptions()
    if not isinstance(opts, SpellbookInterpreterOptions):
        raise SpellbookInterpreterError("options must be SpellbookInterpreterOptions")

    payload = _payload_from_input(combo)
    original_payload = copy.deepcopy(payload)
    try:
        if payload.get("interpreter_version") == SPELLBOOK_INTERPRETER_VERSION:
            interpretation = _interpretation_from_dict(payload)
        else:
            interpretation = _interpret_payload(payload, opts, generated_at)
        validate_spellbook_combo_interpretation(interpretation)
        return interpretation
    finally:
        if payload != original_payload:
            raise SpellbookInterpreterError("input payload was mutated")


def validate_spellbook_combo_interpretation(
    interpretation: SpellbookComboInterpretation,
) -> SpellbookComboInterpretation:
    if not isinstance(interpretation, SpellbookComboInterpretation):
        raise SpellbookInterpreterError("interpretation must be SpellbookComboInterpretation")
    _require_text(interpretation.interpreter_version, "interpreter_version")
    if interpretation.interpreter_version != SPELLBOOK_INTERPRETER_VERSION:
        raise SpellbookInterpreterError("unsupported interpreter_version")
    if interpretation.provider != SPELLBOOK_PROVIDER:
        raise SpellbookInterpreterError("provider must be commander_spellbook")
    _require_text(interpretation.provider_combo_id, "provider_combo_id")
    _require_tuple(interpretation.variant_ids, "variant_ids")
    _require_tuple(interpretation.component_refs, "component_refs")
    _require_tuple(interpretation.component_roles, "component_roles")
    _require_tuple(interpretation.prerequisite_classes, "prerequisite_classes")
    _require_tuple(interpretation.output_classes, "output_classes")
    _require_tuple(interpretation.restriction_classes, "restriction_classes")
    _require_tuple(interpretation.target_compatibility_items, "target_compatibility_items")
    _require_tuple(interpretation.unsupported_items, "unsupported_items")
    _require_tuple(interpretation.manual_review_items, "manual_review_items")
    _require_tuple(interpretation.source_refs, "source_refs")
    _require_tuple(interpretation.warnings, "warnings")
    _require_text(interpretation.generated_at, "generated_at")

    if not interpretation.component_refs:
        raise SpellbookInterpreterError("component_refs are required")
    if not interpretation.source_refs:
        raise SpellbookInterpreterError("source_refs are required")

    for item in interpretation.component_refs:
        _validate_component(item)
    for item in interpretation.component_roles:
        _validate_interpretation_class(item, "component_roles")
    for item in interpretation.prerequisite_classes:
        _validate_requirement_class(item.prerequisite_class, "prerequisite_class")
        _require_text(item.source_text, "prerequisite source_text")
        _validate_confidence(item.confidence, "prerequisite confidence")
    for item in interpretation.output_classes:
        _validate_output_class(item.output_class)
        _require_text(item.source_text, "output source_text")
        _validate_confidence(item.confidence, "output confidence")
        if not isinstance(item.win_enabling, bool):
            raise SpellbookInterpreterError("win_enabling must be bool")
    for item in interpretation.restriction_classes:
        _validate_requirement_class(item.restriction_class, "restriction_class")
        _require_text(item.source_text, "restriction source_text")
        _validate_confidence(item.confidence, "restriction confidence")
    for item in interpretation.target_compatibility_items:
        _validate_output_class(item.target_output_class)
        if item.source_output_class is not None:
            _validate_output_class(item.source_output_class)
        if item.compatibility not in TARGET_COMPATIBILITY_VALUES:
            raise SpellbookInterpreterError(f"unsupported target compatibility: {item.compatibility}")
    for item in interpretation.unsupported_items:
        _require_text(item.item_type, "unsupported item_type")
        _require_text(item.source_text, "unsupported source_text")
        _require_text(item.reason, "unsupported reason")
    for item in interpretation.manual_review_items:
        _require_text(item.item_type, "manual review item_type")
        _require_text(item.source_text, "manual review source_text")
        _require_text(item.reason, "manual review reason")
    for item in interpretation.source_refs:
        if item.provider != SPELLBOOK_PROVIDER:
            raise SpellbookInterpreterError("source_ref provider must be commander_spellbook")
        _require_text(item.provider_combo_id, "source_ref provider_combo_id")
    for item in interpretation.warnings:
        _require_text(item.warning_type, "warning_type")
        _require_text(item.message, "warning message")

    _reject_forbidden_language(_interpretation_to_dict(interpretation))
    return interpretation


def spellbook_combo_interpretation_to_dict(
    interpretation: SpellbookComboInterpretation,
) -> dict[str, Any]:
    validated = validate_spellbook_combo_interpretation(interpretation)
    return _interpretation_to_dict(validated)


def _interpretation_to_dict(interpretation: SpellbookComboInterpretation) -> dict[str, Any]:
    validated = interpretation
    return {
        "interpreter_version": validated.interpreter_version,
        "provider": validated.provider,
        "provider_combo_id": validated.provider_combo_id,
        "combo_url": validated.combo_url,
        "combo_name": validated.combo_name,
        "variant_ids": list(validated.variant_ids),
        "component_refs": [_component_to_dict(item) for item in validated.component_refs],
        "component_roles": [_interpretation_class_to_dict(item) for item in validated.component_roles],
        "prerequisite_classes": [_prerequisite_to_dict(item) for item in validated.prerequisite_classes],
        "output_classes": [_output_to_dict(item) for item in validated.output_classes],
        "restriction_classes": [_restriction_to_dict(item) for item in validated.restriction_classes],
        "target_compatibility_items": [_compatibility_to_dict(item) for item in validated.target_compatibility_items],
        "unsupported_items": [_unsupported_to_dict(item) for item in validated.unsupported_items],
        "manual_review_items": [_manual_review_to_dict(item) for item in validated.manual_review_items],
        "source_refs": [_source_ref_to_dict(item) for item in validated.source_refs],
        "generated_at": validated.generated_at,
        "warnings": [_warning_to_dict(item) for item in validated.warnings],
    }


def _interpret_payload(
    payload: Mapping[str, Any],
    options: SpellbookInterpreterOptions,
    generated_at: str,
) -> SpellbookComboInterpretation:
    provider_combo_id = _first_text(payload, "provider_combo_id", "id", "spellbook_id", "pk")
    _require_text(provider_combo_id, "provider_combo_id")
    combo_url = _first_optional_text(payload, "combo_url", "url", "spellbook_url")
    combo_name = _first_optional_text(payload, "combo_name", "name", "title")
    variant_ids = _variant_ids(payload)
    components, component_roles, manual_items = _component_refs(payload)
    outputs, output_manual = _outputs(payload)
    prerequisites, prereq_manual = _requirements(payload, ("prerequisites", "requirements"), "prerequisite")
    restrictions, restriction_manual = _requirements(payload, ("restrictions", "limits"), "restriction")
    unsupported_items = _unsupported_items(payload)
    source_refs = (
        SpellbookComboSourceRef(
            provider=SPELLBOOK_PROVIDER,
            provider_combo_id=provider_combo_id,
            combo_url=combo_url,
            raw_payload_hash=_raw_payload_hash(payload),
        ),
    )

    all_manual = tuple(sorted(manual_items + output_manual + prereq_manual + restriction_manual, key=_manual_sort_key))
    if not options.include_manual_review_items:
        all_manual = ()
    if not options.include_unsupported_items:
        unsupported_items = ()

    return SpellbookComboInterpretation(
        interpreter_version=SPELLBOOK_INTERPRETER_VERSION,
        provider=SPELLBOOK_PROVIDER,
        provider_combo_id=provider_combo_id,
        combo_url=combo_url,
        combo_name=combo_name,
        variant_ids=variant_ids,
        component_refs=components,
        component_roles=component_roles,
        prerequisite_classes=prerequisites,
        output_classes=outputs,
        restriction_classes=restrictions,
        target_compatibility_items=_target_compatibility(outputs, options.target_output_classes),
        unsupported_items=unsupported_items,
        manual_review_items=all_manual,
        source_refs=source_refs,
        generated_at=generated_at,
        warnings=(),
    )


def _payload_from_input(combo: Mapping[str, Any] | Any) -> dict[str, Any]:
    if isinstance(combo, Mapping):
        return copy.deepcopy(dict(combo))
    payload: dict[str, Any] = {}
    for field in (
        "provider_combo_id",
        "combo_url",
        "combo_name",
        "components",
        "outputs",
        "cards",
        "raw_payload",
    ):
        if hasattr(combo, field):
            payload[field] = getattr(combo, field)
    raw_payload = payload.get("raw_payload")
    if raw_payload is not None:
        if hasattr(raw_payload, "payload"):
            payload.setdefault("raw_payload_hash", getattr(raw_payload, "payload_hash", None))
            raw_payload_value = getattr(raw_payload, "payload")
            if isinstance(raw_payload_value, Mapping):
                for key, value in raw_payload_value.items():
                    payload.setdefault(key, value)
        elif isinstance(raw_payload, Mapping):
            for key, value in raw_payload.items():
                payload.setdefault(key, value)
    return copy.deepcopy(payload)


def _variant_ids(payload: Mapping[str, Any]) -> tuple[str, ...]:
    raw = payload.get("variant_ids", payload.get("variants", ()))
    values: list[str] = []
    if isinstance(raw, str):
        values.append(raw)
    elif isinstance(raw, list | tuple):
        for item in raw:
            if isinstance(item, Mapping):
                text = _first_optional_text(item, "id", "variant_id", "pk")
            else:
                text = _optional_text(item)
            if text:
                values.append(text)
    return tuple(sorted(dict.fromkeys(values)))


def _component_refs(
    payload: Mapping[str, Any],
) -> tuple[tuple[SpellbookComponentRef, ...], tuple[SpellbookInterpretationClass, ...], tuple[SpellbookManualReviewItem, ...]]:
    raw_cards = payload.get("cards")
    if raw_cards is None:
        raw_cards = payload.get("components", ())
    components: list[SpellbookComponentRef] = []
    roles: list[SpellbookInterpretationClass] = []
    manual: list[SpellbookManualReviewItem] = []

    if isinstance(raw_cards, str):
        raw_cards = [raw_cards]
    if not isinstance(raw_cards, list | tuple):
        raise SpellbookInterpreterError("cards/components must be a list")

    for index, item in enumerate(raw_cards):
        if isinstance(item, Mapping):
            card_name = _first_text(item, "card_name", "raw_name", "name", "card")
            role = _first_optional_text(item, "role", "component_role")
            required = bool(item.get("required", True))
            scryfall_id = _first_optional_text(item, "scryfall_id", "scryfallId")
            oracle_id = _first_optional_text(item, "oracle_id", "oracleId")
            source_ref = _first_optional_text(item, "source_ref", "id")
        else:
            card_name = _require_text(_optional_text(item), "component card_name")
            role = None
            required = True
            scryfall_id = oracle_id = source_ref = None
        components.append(
            SpellbookComponentRef(
                card_name=card_name,
                role=role,
                required=required,
                scryfall_id=scryfall_id,
                oracle_id=oracle_id,
                source_ref=source_ref or f"component:{index}",
            )
        )
        if role:
            roles.append(SpellbookInterpretationClass(class_value=role, source_text=card_name, confidence=1.0))
        else:
            manual.append(
                SpellbookManualReviewItem(
                    item_type="missing_component_role",
                    source_text=card_name,
                    reason="component role was not supplied",
                )
            )

    if not components:
        raise SpellbookInterpreterError("at least one component is required")
    return tuple(components), tuple(roles), tuple(manual)


def _outputs(payload: Mapping[str, Any]) -> tuple[tuple[SpellbookOutput, ...], tuple[SpellbookManualReviewItem, ...]]:
    raw_outputs = payload.get("outputs", ())
    if isinstance(raw_outputs, str):
        raw_outputs = [raw_outputs]
    if not isinstance(raw_outputs, list | tuple):
        raise SpellbookInterpreterError("outputs must be a list")
    outputs: list[SpellbookOutput] = []
    manual: list[SpellbookManualReviewItem] = []
    for item in raw_outputs:
        text = _source_text(item, ("text", "name", "description", "output"))
        output_class = _classify_output(text)
        win_enabling = output_class in {"win_condition", "infinite_draw", "infinite_mana"}
        outputs.append(SpellbookOutput(output_class=output_class, source_text=text, win_enabling=win_enabling))
        if output_class == "unknown":
            manual.append(
                SpellbookManualReviewItem(
                    item_type="unknown_output_text",
                    source_text=text,
                    reason="output text did not match a controlled output class",
                )
            )
    if not outputs:
        outputs.append(SpellbookOutput(output_class="unknown", source_text="missing output", confidence=0.0))
        manual.append(
            SpellbookManualReviewItem(
                item_type="unknown_output_text",
                source_text="missing output",
                reason="combo did not supply output text",
            )
        )
    return tuple(outputs), tuple(manual)


def _requirements(
    payload: Mapping[str, Any],
    field_names: tuple[str, ...],
    item_type: str,
) -> tuple[tuple[SpellbookPrerequisite | SpellbookRestriction, ...], tuple[SpellbookManualReviewItem, ...]]:
    raw_items: Any = ()
    for field_name in field_names:
        if field_name in payload:
            raw_items = payload[field_name]
            break
    if isinstance(raw_items, str):
        raw_items = [raw_items]
    if not isinstance(raw_items, list | tuple):
        raise SpellbookInterpreterError(f"{item_type} items must be a list")
    classified: list[SpellbookPrerequisite | SpellbookRestriction] = []
    manual: list[SpellbookManualReviewItem] = []
    for item in raw_items:
        text = _source_text(item, ("text", "name", "description", "requirement", "restriction"))
        class_value = _classify_requirement(text)
        if item_type == "prerequisite":
            classified.append(SpellbookPrerequisite(prerequisite_class=class_value, source_text=text))
        else:
            classified.append(SpellbookRestriction(restriction_class=class_value, source_text=text))
        if class_value == "unknown_requirement":
            manual.append(
                SpellbookManualReviewItem(
                    item_type=f"unknown_{item_type}_text",
                    source_text=text,
                    reason=f"{item_type} text did not match a controlled class",
                )
            )
    return tuple(classified), tuple(manual)


def _unsupported_items(payload: Mapping[str, Any]) -> tuple[SpellbookUnsupportedItem, ...]:
    raw_items = payload.get("unsupported_items", payload.get("unsupported", ()))
    if isinstance(raw_items, str):
        raw_items = [raw_items]
    if not isinstance(raw_items, list | tuple):
        raise SpellbookInterpreterError("unsupported_items must be a list")
    items: list[SpellbookUnsupportedItem] = []
    for item in raw_items:
        if isinstance(item, Mapping):
            item_type = _first_optional_text(item, "item_type", "type") or "unsupported_source_shape"
            source_text = _source_text(item, ("source_text", "text", "description", "name"))
            reason = _first_optional_text(item, "reason") or "unsupported Spellbook interpretation input"
        else:
            item_type = "unsupported_source_shape"
            source_text = _require_text(_optional_text(item), "unsupported source_text")
            reason = "unsupported Spellbook interpretation input"
        items.append(SpellbookUnsupportedItem(item_type=item_type, source_text=source_text, reason=reason))
    return tuple(sorted(items, key=lambda item: (item.item_type, item.source_text, item.reason)))


def _target_compatibility(
    outputs: tuple[SpellbookOutput, ...],
    target_output_classes: tuple[str, ...],
) -> tuple[SpellbookTargetCompatibility, ...]:
    items: list[SpellbookTargetCompatibility] = []
    for target in target_output_classes:
        _validate_output_class(target)
        matching = [item for item in outputs if item.output_class == target]
        unknown = [item for item in outputs if item.output_class == "unknown"]
        if matching:
            items.append(
                SpellbookTargetCompatibility(
                    target_output_class=target,
                    compatibility="can_satisfy_target_output_class",
                    source_output_class=target,
                    reason="source output class matches target output class",
                )
            )
        elif unknown:
            items.append(
                SpellbookTargetCompatibility(
                    target_output_class=target,
                    compatibility="cannot_classify_against_target",
                    source_output_class="unknown",
                    reason="source output includes unknown output text",
                )
            )
        else:
            items.append(
                SpellbookTargetCompatibility(
                    target_output_class=target,
                    compatibility="unsupported_compatibility_condition",
                    source_output_class=None,
                    reason="no matching output class was present",
                )
            )
    return tuple(items)


def _classify_output(text: str) -> str:
    normalized = _normalize(text)
    rules = (
        ("infinite_mana", ("infinite mana", "unbounded mana")),
        ("infinite_draw", ("draw your deck", "draws your deck", "draw your library", "infinite draw")),
        ("infinite_damage", ("infinite damage", "unbounded damage", "deals damage repeatedly")),
        ("infinite_tokens", ("infinite tokens", "unbounded tokens")),
        ("infinite_life", ("infinite life", "gain infinite life", "unbounded life")),
        ("mill", ("mill", "mills")),
        ("storm", ("storm",)),
        ("combat", ("combat", "attack")),
        ("lock", ("lock", "prevents opponents", "opponents can't")),
        ("win_condition", ("win the game", "wins the game", "win condition")),
        ("card_advantage", ("draw cards", "card advantage")),
        ("mana_generation", ("add mana", "adds mana", "produce mana", "produces mana")),
        ("board_state", ("battlefield", "board state")),
    )
    for output_class, needles in rules:
        if any(needle in normalized for needle in needles):
            return output_class
    return "unknown"


def _classify_requirement(text: str) -> str:
    normalized = _normalize(text)
    rules = (
        ("requires_commander", ("commander",)),
        ("requires_battlefield", ("battlefield", "in play")),
        ("requires_hand", ("hand",)),
        ("requires_graveyard", ("graveyard",)),
        ("requires_library", ("library",)),
        ("requires_mana", ("mana",)),
        ("requires_tap", ("tap", "tapped")),
        ("requires_untap", ("untap", "untapped")),
        ("requires_cast", ("cast",)),
        ("requires_opponent", ("opponent",)),
        ("requires_specific_zone", ("zone", "exile")),
        ("color_requirement", ("color", "blue", "black", "red", "green", "white")),
        ("timing_requirement", ("timing", "instant speed", "sorcery speed")),
        ("once_per_turn_limit", ("once per turn",)),
        ("summoning_sickness_sensitive", ("summoning sickness",)),
    )
    for requirement_class, needles in rules:
        if any(needle in normalized for needle in needles):
            return requirement_class
    return "unknown_requirement"


def _interpretation_from_dict(payload: Mapping[str, Any]) -> SpellbookComboInterpretation:
    return SpellbookComboInterpretation(
        interpreter_version=_first_text(payload, "interpreter_version"),
        provider=_first_text(payload, "provider"),
        provider_combo_id=_first_text(payload, "provider_combo_id"),
        combo_url=_first_optional_text(payload, "combo_url"),
        combo_name=_first_optional_text(payload, "combo_name"),
        variant_ids=tuple(_require_string_list(payload.get("variant_ids"), "variant_ids")),
        component_refs=tuple(SpellbookComponentRef(**item) for item in _require_list(payload.get("component_refs"), "component_refs")),
        component_roles=tuple(
            SpellbookInterpretationClass(**item) for item in _require_list(payload.get("component_roles"), "component_roles")
        ),
        prerequisite_classes=tuple(
            SpellbookPrerequisite(**item) for item in _require_list(payload.get("prerequisite_classes"), "prerequisite_classes")
        ),
        output_classes=tuple(SpellbookOutput(**item) for item in _require_list(payload.get("output_classes"), "output_classes")),
        restriction_classes=tuple(
            SpellbookRestriction(**item) for item in _require_list(payload.get("restriction_classes"), "restriction_classes")
        ),
        target_compatibility_items=tuple(
            SpellbookTargetCompatibility(**item)
            for item in _require_list(payload.get("target_compatibility_items"), "target_compatibility_items")
        ),
        unsupported_items=tuple(
            SpellbookUnsupportedItem(**item) for item in _require_list(payload.get("unsupported_items"), "unsupported_items")
        ),
        manual_review_items=tuple(
            SpellbookManualReviewItem(**item) for item in _require_list(payload.get("manual_review_items"), "manual_review_items")
        ),
        source_refs=tuple(SpellbookComboSourceRef(**item) for item in _require_list(payload.get("source_refs"), "source_refs")),
        generated_at=_first_text(payload, "generated_at"),
        warnings=tuple(SpellbookInterpreterWarning(**item) for item in _require_list(payload.get("warnings"), "warnings")),
    )


def _component_to_dict(item: SpellbookComponentRef) -> dict[str, Any]:
    return {
        "card_name": item.card_name,
        "role": item.role,
        "required": item.required,
        "scryfall_id": item.scryfall_id,
        "oracle_id": item.oracle_id,
        "source_ref": item.source_ref,
    }


def _interpretation_class_to_dict(item: SpellbookInterpretationClass) -> dict[str, Any]:
    return {"class_value": item.class_value, "source_text": item.source_text, "confidence": item.confidence}


def _prerequisite_to_dict(item: SpellbookPrerequisite) -> dict[str, Any]:
    return {"prerequisite_class": item.prerequisite_class, "source_text": item.source_text, "confidence": item.confidence}


def _output_to_dict(item: SpellbookOutput) -> dict[str, Any]:
    return {
        "output_class": item.output_class,
        "source_text": item.source_text,
        "confidence": item.confidence,
        "win_enabling": item.win_enabling,
    }


def _restriction_to_dict(item: SpellbookRestriction) -> dict[str, Any]:
    return {"restriction_class": item.restriction_class, "source_text": item.source_text, "confidence": item.confidence}


def _compatibility_to_dict(item: SpellbookTargetCompatibility) -> dict[str, Any]:
    return {
        "target_output_class": item.target_output_class,
        "compatibility": item.compatibility,
        "source_output_class": item.source_output_class,
        "reason": item.reason,
    }


def _unsupported_to_dict(item: SpellbookUnsupportedItem) -> dict[str, Any]:
    return {"item_type": item.item_type, "source_text": item.source_text, "reason": item.reason}


def _manual_review_to_dict(item: SpellbookManualReviewItem) -> dict[str, Any]:
    return {"item_type": item.item_type, "source_text": item.source_text, "reason": item.reason}


def _source_ref_to_dict(item: SpellbookComboSourceRef) -> dict[str, Any]:
    return {
        "provider": item.provider,
        "provider_combo_id": item.provider_combo_id,
        "combo_url": item.combo_url,
        "raw_payload_hash": item.raw_payload_hash,
    }


def _warning_to_dict(item: SpellbookInterpreterWarning) -> dict[str, Any]:
    return {"warning_type": item.warning_type, "message": item.message}


def _source_text(item: Any, field_names: tuple[str, ...]) -> str:
    if isinstance(item, Mapping):
        text = _first_optional_text(item, *field_names)
    else:
        text = _optional_text(item)
    return _require_text(text, "source_text")


def _first_text(payload: Mapping[str, Any], *field_names: str) -> str:
    return _require_text(_first_optional_text(payload, *field_names), field_names[0])


def _first_optional_text(payload: Mapping[str, Any], *field_names: str) -> str | None:
    for field_name in field_names:
        if field_name in payload:
            text = _optional_text(payload[field_name])
            if text:
                return text
    return None


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int):
        return str(value)
    return None


def _require_text(value: str | None, field_name: str) -> str:
    if value is None or not isinstance(value, str) or not value.strip():
        raise SpellbookInterpreterError(f"{field_name} is required")
    return value.strip()


def _require_tuple(value: Any, field_name: str) -> None:
    if not isinstance(value, tuple):
        raise SpellbookInterpreterError(f"{field_name} must be a tuple")


def _require_list(value: Any, field_name: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise SpellbookInterpreterError(f"{field_name} must be a list")
    if not all(isinstance(item, dict) for item in value):
        raise SpellbookInterpreterError(f"{field_name} must contain objects")
    return value


def _require_string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise SpellbookInterpreterError(f"{field_name} must be a list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise SpellbookInterpreterError(f"{field_name} must contain strings")
    return value


def _validate_component(item: SpellbookComponentRef) -> None:
    if not isinstance(item, SpellbookComponentRef):
        raise SpellbookInterpreterError("component_refs must contain SpellbookComponentRef")
    _require_text(item.card_name, "component card_name")
    if not isinstance(item.required, bool):
        raise SpellbookInterpreterError("component required must be bool")


def _validate_interpretation_class(item: SpellbookInterpretationClass, field_name: str) -> None:
    if not isinstance(item, SpellbookInterpretationClass):
        raise SpellbookInterpreterError(f"{field_name} must contain SpellbookInterpretationClass")
    _require_text(item.class_value, "class_value")
    _require_text(item.source_text, "source_text")
    _validate_confidence(item.confidence, "confidence")


def _validate_output_class(value: str) -> None:
    if value not in OUTPUT_CLASSES:
        raise SpellbookInterpreterError(f"unsupported output class: {value}")


def _validate_requirement_class(value: str, field_name: str) -> None:
    if value not in REQUIREMENT_CLASSES:
        raise SpellbookInterpreterError(f"unsupported {field_name}: {value}")


def _validate_confidence(value: float, field_name: str) -> None:
    if not isinstance(value, int | float):
        raise SpellbookInterpreterError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise SpellbookInterpreterError(f"{field_name} must be between 0 and 1")


def _raw_payload_hash(payload: Mapping[str, Any]) -> str | None:
    value = _first_optional_text(payload, "raw_payload_hash", "payload_hash")
    if value:
        return value
    raw_payload = payload.get("raw_payload")
    if isinstance(raw_payload, Mapping):
        return _first_optional_text(raw_payload, "payload_hash")
    return None


def _manual_sort_key(item: SpellbookManualReviewItem) -> tuple[str, str, str]:
    return (item.item_type, item.source_text, item.reason)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _reject_forbidden_language(value: Any) -> None:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False).lower()
    for phrase in FORBIDDEN_STRATEGIC_LANGUAGE:
        if phrase in text:
            raise SpellbookInterpreterError("forbidden recommendation language")
