"""Core in-memory models for reproducible probability simulation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MANA_COLOR_KEYS = ("W", "U", "B", "R", "G", "C")
MANA_COST_KEYS = (*MANA_COLOR_KEYS, "Generic")


@dataclass(frozen=True)
class ManaCost:
    W: int = 0
    U: int = 0
    B: int = 0
    R: int = 0
    G: int = 0
    C: int = 0
    Generic: int = 0

    def __post_init__(self) -> None:
        _require_non_negative_ints(self.to_dict(), "mana cost")

    @property
    def mana_value(self) -> int:
        return sum(self.to_dict().values())

    def to_dict(self) -> dict[str, int]:
        return {key: int(getattr(self, key)) for key in MANA_COST_KEYS}

    @classmethod
    def from_mapping(cls, value: dict[str, Any] | None) -> "ManaCost":
        if value is None:
            return cls()
        if not isinstance(value, dict):
            raise ValueError("mana cost must be a mapping")
        return cls(**{key: _int_value(value.get(key, 0), key) for key in MANA_COST_KEYS})


@dataclass(frozen=True)
class ManaOption:
    W: int = 0
    U: int = 0
    B: int = 0
    R: int = 0
    G: int = 0
    C: int = 0
    restriction: str | None = None
    source_card_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_negative_ints({key: int(getattr(self, key)) for key in MANA_COLOR_KEYS}, "mana option")
        if self.total == 0 and self.restriction != "empty":
            raise ValueError("mana option must produce mana unless marked empty")
        if self.restriction is not None:
            _require_text(self.restriction, "restriction")
        if self.source_card_id is not None:
            _require_text(self.source_card_id, "source_card_id")

    @property
    def total(self) -> int:
        return sum(int(getattr(self, key)) for key in MANA_COLOR_KEYS)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {key: int(getattr(self, key)) for key in MANA_COLOR_KEYS}
        if self.restriction is not None:
            payload["restriction"] = self.restriction
        if self.source_card_id is not None:
            payload["source_card_id"] = self.source_card_id
        return payload

    @classmethod
    def empty(cls) -> "ManaOption":
        return cls(restriction="empty")

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "ManaOption":
        if not isinstance(value, dict):
            raise ValueError("mana option must be a mapping")
        return cls(
            **{key: _int_value(value.get(key, 0), key) for key in MANA_COLOR_KEYS},
            restriction=value.get("restriction"),
            source_card_id=value.get("source_card_id"),
        )


@dataclass(frozen=True)
class SimulationActionModel:
    action_type: str
    zone: str | None = None
    cost: ManaCost | None = None
    produces: tuple[ManaOption, ...] = ()
    target_requirements: Any = None
    destination: str | None = None
    requires: tuple[str, ...] = ()
    optional: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.action_type, "action_type")
        if self.zone is not None:
            _require_text(self.zone, "zone")
        if self.destination is not None:
            _require_text(self.destination, "destination")
        object.__setattr__(self, "produces", tuple(self.produces))
        object.__setattr__(self, "requires", tuple(self.requires))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_type": self.action_type,
            "zone": self.zone,
            "cost": self.cost.to_dict() if self.cost is not None else None,
            "produces": [option.to_dict() for option in self.produces],
            "target_requirements": self.target_requirements,
            "destination": self.destination,
            "requires": list(self.requires),
            "optional": self.optional,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SimulationActionModel":
        if not isinstance(value, dict):
            raise ValueError("simulation action model must be a mapping")
        action_type = value.get("action_type", value.get("type"))
        metadata = {
            key: item
            for key, item in value.items()
            if key
            not in {
                "action_type",
                "type",
                "zone",
                "cost",
                "produces",
                "target_requirements",
                "destination",
                "requires",
                "optional",
                "metadata",
            }
        }
        metadata.update(value.get("metadata", {}))
        return cls(
            action_type=action_type,
            zone=value.get("zone"),
            cost=ManaCost.from_mapping(value.get("cost")) if value.get("cost") is not None else None,
            produces=_mana_options_from_value(value.get("produces")),
            target_requirements=value.get("target_requirements"),
            destination=value.get("destination"),
            requires=tuple(value.get("requires", ())),
            optional=bool(value.get("optional", False)),
            metadata=metadata,
        )


@dataclass(frozen=True)
class SimulationCardModel:
    card_id: str
    name: str
    types: tuple[str, ...] = ()
    colors: tuple[str, ...] = ()
    mana_cost: ManaCost = field(default_factory=ManaCost)
    land_types: tuple[str, ...] = ()
    produces: tuple[ManaOption, ...] = ()
    cast_actions: tuple[SimulationActionModel, ...] = ()
    board_abilities: tuple[SimulationActionModel, ...] = ()
    etb_actions: tuple[SimulationActionModel, ...] = ()
    hand_abilities: tuple[SimulationActionModel, ...] = ()
    static_effects: tuple[SimulationActionModel, ...] = ()
    pregame_action: SimulationActionModel | None = None
    enters_tapped: bool = False
    enters_sick: bool = False
    legendary: bool = False
    raw_reference_shape: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.card_id, "card_id")
        _require_text(self.name, "name")
        for field_name in ("types", "colors", "land_types"):
            object.__setattr__(self, field_name, tuple(getattr(self, field_name)))
        for field_name in (
            "produces",
            "cast_actions",
            "board_abilities",
            "etb_actions",
            "hand_abilities",
            "static_effects",
        ):
            object.__setattr__(self, field_name, tuple(getattr(self, field_name)))
        object.__setattr__(self, "raw_reference_shape", dict(self.raw_reference_shape))

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_id": self.card_id,
            "name": self.name,
            "types": list(self.types),
            "colors": list(self.colors),
            "mana_cost": self.mana_cost.to_dict(),
            "land_types": list(self.land_types),
            "produces": [option.to_dict() for option in self.produces],
            "cast_actions": [action.to_dict() for action in self.cast_actions],
            "board_abilities": [action.to_dict() for action in self.board_abilities],
            "etb_actions": [action.to_dict() for action in self.etb_actions],
            "hand_abilities": [action.to_dict() for action in self.hand_abilities],
            "static_effects": [action.to_dict() for action in self.static_effects],
            "pregame_action": self.pregame_action.to_dict() if self.pregame_action is not None else None,
            "enters_tapped": self.enters_tapped,
            "enters_sick": self.enters_sick,
            "legendary": self.legendary,
            "raw_reference_shape": dict(self.raw_reference_shape),
        }

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SimulationCardModel":
        if not isinstance(value, dict):
            raise ValueError("simulation card model must be a mapping")
        pregame = value.get("pregame_action")
        return cls(
            card_id=value.get("card_id", value.get("id")),
            name=value.get("name"),
            types=tuple(value.get("types", ())),
            colors=tuple(value.get("colors", ())),
            mana_cost=ManaCost.from_mapping(value.get("mana_cost")),
            land_types=tuple(value.get("land_types", ())),
            produces=_mana_options_from_value(value.get("produces")),
            cast_actions=_actions_from_value(value.get("cast_actions")),
            board_abilities=_actions_from_value(value.get("board_abilities")),
            etb_actions=_actions_from_value(value.get("etb_actions")),
            hand_abilities=_actions_from_value(value.get("hand_abilities")),
            static_effects=_actions_from_value(value.get("static_effects")),
            pregame_action=SimulationActionModel.from_mapping(pregame) if isinstance(pregame, dict) else None,
            enters_tapped=bool(value.get("enters_tapped", False)),
            enters_sick=bool(value.get("enters_sick", False)),
            legendary=bool(value.get("legendary", False)),
            raw_reference_shape=dict(value),
        )


@dataclass(frozen=True)
class SimulationTargetCondition:
    target_card: str
    target_zone: str
    turn: int
    condition_type: str
    target_card_id: str | None = None
    required_support_tags: tuple[str, ...] = ()
    notes: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.target_card, "target_card")
        _require_text(self.target_zone, "target_zone")
        _require_text(self.condition_type, "condition_type")
        if self.target_card_id is not None:
            _require_text(self.target_card_id, "target_card_id")
        if self.turn <= 0:
            raise ValueError("turn must be positive")
        object.__setattr__(self, "required_support_tags", tuple(self.required_support_tags))

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_card": self.target_card,
            "target_card_id": self.target_card_id,
            "target_zone": self.target_zone,
            "turn": self.turn,
            "condition_type": self.condition_type,
            "required_support_tags": list(self.required_support_tags),
            "notes": self.notes,
        }

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SimulationTargetCondition":
        return cls(
            target_card=value["target_card"],
            target_card_id=value.get("target_card_id"),
            target_zone=value["target_zone"],
            turn=_int_value(value["turn"], "turn"),
            condition_type=value["condition_type"],
            required_support_tags=tuple(value.get("required_support_tags", ())),
            notes=value.get("notes"),
        )


@dataclass(frozen=True)
class SimulationConfig:
    deck_hash: str
    seed: str
    games_requested: int
    min_mulligan_keep: int
    mulligan_mode: str
    simulator_version: str
    card_model_version: str
    targets: tuple[SimulationTargetCondition, ...]
    raw_config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("deck_hash", "seed", "mulligan_mode", "simulator_version", "card_model_version"):
            _require_text(getattr(self, field_name), field_name)
        if self.games_requested <= 0:
            raise ValueError("games_requested must be positive")
        if self.min_mulligan_keep <= 0:
            raise ValueError("min_mulligan_keep must be positive")
        if not self.targets:
            raise ValueError("at least one target is required")
        object.__setattr__(self, "targets", tuple(self.targets))
        object.__setattr__(self, "raw_config", dict(self.raw_config))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "seed": self.seed,
            "games_requested": self.games_requested,
            "min_mulligan_keep": self.min_mulligan_keep,
            "mulligan_mode": self.mulligan_mode,
            "simulator_version": self.simulator_version,
            "card_model_version": self.card_model_version,
            "targets": [target.to_dict() for target in self.targets],
            "raw_config": dict(self.raw_config),
        }


@dataclass(frozen=True)
class SimulationDeckCard:
    quantity: int
    name: str
    model_id: str | None = None
    zone: str = "main"

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("quantity must be positive")
        _require_text(self.name, "name")
        _require_text(self.zone, "zone")
        if self.model_id is not None:
            _require_text(self.model_id, "model_id")

    def to_dict(self) -> dict[str, Any]:
        return {"quantity": self.quantity, "name": self.name, "model_id": self.model_id, "zone": self.zone}


@dataclass(frozen=True)
class SimulationDeck:
    deck_hash: str
    cards: tuple[SimulationDeckCard, ...]
    commanders: tuple[SimulationDeckCard, ...] = ()
    source: str | None = None
    unresolved_cards: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.deck_hash, "deck_hash")
        if not self.cards and not self.commanders:
            raise ValueError("simulation deck must contain cards or commanders")
        object.__setattr__(self, "cards", tuple(self.cards))
        object.__setattr__(self, "commanders", tuple(self.commanders))
        object.__setattr__(self, "unresolved_cards", tuple(self.unresolved_cards))

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "cards": [card.to_dict() for card in self.cards],
            "commanders": [card.to_dict() for card in self.commanders],
            "source": self.source,
            "unresolved_cards": list(self.unresolved_cards),
        }


@dataclass(frozen=True)
class SimulationUnsupportedItem:
    item_type: str
    reason: str
    card_name: str | None = None
    card_id: str | None = None
    action_type: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.item_type, "item_type")
        _require_text(self.reason, "reason")
        for field_name in ("card_name", "card_id", "action_type"):
            value = getattr(self, field_name)
            if value is not None:
                _require_text(value, field_name)
        object.__setattr__(self, "details", dict(self.details))

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_type": self.item_type,
            "card_name": self.card_name,
            "card_id": self.card_id,
            "reason": self.reason,
            "action_type": self.action_type,
            "details": dict(self.details),
        }


@dataclass(frozen=True)
class SimulationTraceAction:
    turn: int
    description: str
    card_id: str | None = None
    action_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.turn <= 0:
            raise ValueError("turn must be positive")
        _require_text(self.description, "description")
        if self.card_id is not None:
            _require_text(self.card_id, "card_id")
        if self.action_type is not None:
            _require_text(self.action_type, "action_type")
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "description": self.description,
            "card_id": self.card_id,
            "action_type": self.action_type,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "SimulationTraceAction":
        metadata = {
            key: item
            for key, item in value.items()
            if key not in {"turn", "description", "cardId", "card_id", "actionType", "action_type"}
        }
        return cls(
            turn=_int_value(value["turn"], "turn"),
            description=value["description"],
            card_id=value.get("card_id", value.get("cardId")),
            action_type=value.get("action_type", value.get("actionType")),
            metadata=metadata,
        )


@dataclass(frozen=True)
class SimulationTrace:
    trace_id: str | None
    seed: str
    game_index: int
    opening_hand: tuple[str, ...]
    mulligan_count: int
    success: bool
    actions: tuple[SimulationTraceAction, ...]
    final_state: dict[str, Any] = field(default_factory=dict)
    unsupported_items: tuple[SimulationUnsupportedItem, ...] = ()
    created_at: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.seed, "seed")
        if self.trace_id is not None:
            _require_text(self.trace_id, "trace_id")
        if self.game_index < 0:
            raise ValueError("game_index cannot be negative")
        if self.mulligan_count < 0:
            raise ValueError("mulligan_count cannot be negative")
        if not self.opening_hand:
            raise ValueError("opening_hand is required")
        object.__setattr__(self, "opening_hand", tuple(self.opening_hand))
        object.__setattr__(self, "actions", tuple(self.actions))
        object.__setattr__(self, "unsupported_items", tuple(self.unsupported_items))
        object.__setattr__(self, "final_state", dict(self.final_state))

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "seed": self.seed,
            "game_index": self.game_index,
            "opening_hand": list(self.opening_hand),
            "mulligan_count": self.mulligan_count,
            "success": self.success,
            "actions": [action.to_dict() for action in self.actions],
            "final_state": dict(self.final_state),
            "unsupported_items": [item.to_dict() for item in self.unsupported_items],
            "created_at": self.created_at,
        }


@dataclass(frozen=True)
class SimulationResult:
    target: SimulationTargetCondition
    games_completed: int
    win_count: int
    win_rate: float
    margin_of_error: float | None = None
    sample_successful_traces: tuple[SimulationTrace, ...] = ()
    sample_failed_traces: tuple[SimulationTrace, ...] = ()
    unsupported_items: tuple[SimulationUnsupportedItem, ...] = ()
    raw_payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.games_completed < 0:
            raise ValueError("games_completed cannot be negative")
        if self.win_count < 0:
            raise ValueError("win_count cannot be negative")
        if self.win_count > self.games_completed:
            raise ValueError("win_count cannot exceed games_completed")
        if not 0 <= self.win_rate <= 1:
            raise ValueError("win_rate must be between 0 and 1")
        if self.margin_of_error is not None and self.margin_of_error < 0:
            raise ValueError("margin_of_error cannot be negative")
        object.__setattr__(self, "sample_successful_traces", tuple(self.sample_successful_traces))
        object.__setattr__(self, "sample_failed_traces", tuple(self.sample_failed_traces))
        object.__setattr__(self, "unsupported_items", tuple(self.unsupported_items))
        object.__setattr__(self, "raw_payload", dict(self.raw_payload))

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target.to_dict(),
            "games_completed": self.games_completed,
            "win_count": self.win_count,
            "win_rate": self.win_rate,
            "margin_of_error": self.margin_of_error,
            "sample_successful_traces": [trace.to_dict() for trace in self.sample_successful_traces],
            "sample_failed_traces": [trace.to_dict() for trace in self.sample_failed_traces],
            "unsupported_items": [item.to_dict() for item in self.unsupported_items],
            "raw_payload": dict(self.raw_payload),
        }


def _actions_from_value(value: Any) -> tuple[SimulationActionModel, ...]:
    if value is None:
        return ()
    if isinstance(value, dict):
        return (SimulationActionModel.from_mapping(value),)
    if isinstance(value, list):
        return tuple(SimulationActionModel.from_mapping(item) for item in value)
    raise ValueError("actions must be a mapping or list")


def _mana_options_from_value(value: Any) -> tuple[ManaOption, ...]:
    if value is None:
        return ()
    if value == "any":
        return tuple(ManaOption(**{color: 1}) for color in ("W", "U", "B", "R", "G"))
    if isinstance(value, dict):
        return (ManaOption.from_mapping(value),)
    if isinstance(value, list):
        return tuple(ManaOption.from_mapping(item) for item in value)
    raise ValueError("produces must be a mapping, list, or 'any'")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _int_value(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return value


def _require_non_negative_ints(values: dict[str, Any], label: str) -> None:
    for key, value in values.items():
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{label} {key} must be an integer")
        if value < 0:
            raise ValueError(f"{label} {key} cannot be negative")
