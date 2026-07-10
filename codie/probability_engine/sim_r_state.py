"""Pure immutable state models for the future SIM-R engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


SIM_R_STATE_VERSION = "sim-r-state-v1"
MANA_POOL_KEYS = ("W", "U", "B", "R", "G", "C")


class SimulationStateBuildError(ValueError):
    """Raised when a SIM-R state payload violates the state contract."""


@dataclass(frozen=True)
class SimulationCardInstance:
    card_instance_id: str
    name: str
    owner: str
    controller: str
    zone: str
    zone_index: int
    scryfall_id: str | None = None
    oracle_id: str | None = None
    status_flags: tuple[str, ...] = ()
    source_card_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.card_instance_id, "card_instance_id")
        _require_text(self.name, "name")
        _require_text(self.owner, "owner")
        _require_text(self.controller, "controller")
        _require_text(self.zone, "zone")
        _require_non_negative_int(self.zone_index, "zone_index")
        if self.scryfall_id is not None:
            _require_text(self.scryfall_id, "scryfall_id")
        if self.oracle_id is not None:
            _require_text(self.oracle_id, "oracle_id")
        if self.source_card_id is not None:
            _require_text(self.source_card_id, "source_card_id")
        object.__setattr__(self, "status_flags", _string_tuple(self.status_flags, "status_flags"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_instance_id": self.card_instance_id,
            "scryfall_id": self.scryfall_id,
            "oracle_id": self.oracle_id,
            "name": self.name,
            "owner": self.owner,
            "controller": self.controller,
            "zone": self.zone,
            "zone_index": self.zone_index,
            "status_flags": list(self.status_flags),
            "source_card_id": self.source_card_id,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationCardInstance":
        _require_mapping(value, "card instance")
        return cls(
            card_instance_id=value.get("card_instance_id"),
            scryfall_id=value.get("scryfall_id"),
            oracle_id=value.get("oracle_id"),
            name=value.get("name"),
            owner=value.get("owner"),
            controller=value.get("controller"),
            zone=value.get("zone"),
            zone_index=value.get("zone_index"),
            status_flags=tuple(value.get("status_flags", ())),
            source_card_id=value.get("source_card_id"),
        )


@dataclass(frozen=True)
class SimulationZone:
    zone_name: str
    ordered: bool
    cards: tuple[SimulationCardInstance, ...] = ()
    visibility: str = "public"
    owner: str = "player"
    controller: str = "player"

    def __post_init__(self) -> None:
        _require_text(self.zone_name, "zone_name")
        _require_text(self.visibility, "visibility")
        _require_text(self.owner, "owner")
        _require_text(self.controller, "controller")
        if not isinstance(self.ordered, bool):
            raise SimulationStateBuildError("ordered must be a boolean")
        cards = tuple(self.cards)
        for index, card in enumerate(cards):
            if not isinstance(card, SimulationCardInstance):
                raise SimulationStateBuildError("zone cards must be SimulationCardInstance values")
            if card.zone != self.zone_name:
                raise SimulationStateBuildError("card zone must match containing zone")
            if self.ordered and card.zone_index != index:
                raise SimulationStateBuildError("ordered zone card indexes must match card order")
        object.__setattr__(self, "cards", cards)

    def to_dict(self) -> dict[str, Any]:
        return {
            "zone_name": self.zone_name,
            "ordered": self.ordered,
            "cards": [card.to_dict() for card in self.cards],
            "visibility": self.visibility,
            "owner": self.owner,
            "controller": self.controller,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationZone":
        _require_mapping(value, "zone")
        cards = tuple(SimulationCardInstance.from_mapping(item) for item in value.get("cards", ()))
        return cls(
            zone_name=value.get("zone_name"),
            ordered=value.get("ordered"),
            cards=cards,
            visibility=value.get("visibility", "public"),
            owner=value.get("owner", "player"),
            controller=value.get("controller", "player"),
        )


@dataclass(frozen=True)
class SimulationManaPool:
    W: int = 0
    U: int = 0
    B: int = 0
    R: int = 0
    G: int = 0
    C: int = 0
    restricted_mana: tuple[Mapping[str, Any], ...] = ()
    floating_mana_sources: tuple[str, ...] = ()
    expires_at_step: str | None = None

    def __post_init__(self) -> None:
        for key in MANA_POOL_KEYS:
            _require_non_negative_int(getattr(self, key), key)
        restricted = tuple(_immutable_mapping(item, "restricted_mana") for item in self.restricted_mana)
        object.__setattr__(self, "restricted_mana", restricted)
        object.__setattr__(self, "floating_mana_sources", _string_tuple(self.floating_mana_sources, "floating_mana_sources"))
        if self.expires_at_step is not None:
            _require_text(self.expires_at_step, "expires_at_step")

    def to_dict(self) -> dict[str, Any]:
        return {
            **{key: int(getattr(self, key)) for key in MANA_POOL_KEYS},
            "restricted_mana": [_thaw_json(item) for item in self.restricted_mana],
            "floating_mana_sources": list(self.floating_mana_sources),
            "expires_at_step": self.expires_at_step,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "SimulationManaPool":
        if value is None:
            return cls()
        _require_mapping(value, "mana pool")
        return cls(
            **{key: value.get(key, 0) for key in MANA_POOL_KEYS},
            restricted_mana=tuple(value.get("restricted_mana", ())),
            floating_mana_sources=tuple(value.get("floating_mana_sources", ())),
            expires_at_step=value.get("expires_at_step"),
        )


@dataclass(frozen=True)
class SimulationCommanderState:
    commander_instance_ids: tuple[str, ...] = ()
    commander_cast_count: Mapping[str, int] = field(default_factory=dict)
    commander_tax: Mapping[str, int] = field(default_factory=dict)
    commander_zone: Mapping[str, str] = field(default_factory=dict)
    partner_group_key: str | None = None

    def __post_init__(self) -> None:
        ids = tuple(sorted(_string_tuple(self.commander_instance_ids, "commander_instance_ids")))
        object.__setattr__(self, "commander_instance_ids", ids)
        object.__setattr__(self, "commander_cast_count", _immutable_int_mapping(self.commander_cast_count, "commander_cast_count"))
        object.__setattr__(self, "commander_tax", _immutable_int_mapping(self.commander_tax, "commander_tax"))
        object.__setattr__(self, "commander_zone", _immutable_str_mapping(self.commander_zone, "commander_zone"))
        if self.partner_group_key is not None:
            _require_text(self.partner_group_key, "partner_group_key")

    def to_dict(self) -> dict[str, Any]:
        return {
            "commander_instance_ids": list(self.commander_instance_ids),
            "commander_cast_count": dict(self.commander_cast_count),
            "commander_tax": dict(self.commander_tax),
            "commander_zone": dict(self.commander_zone),
            "partner_group_key": self.partner_group_key,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "SimulationCommanderState":
        if value is None:
            return cls()
        _require_mapping(value, "commander state")
        return cls(
            commander_instance_ids=tuple(value.get("commander_instance_ids", ())),
            commander_cast_count=dict(value.get("commander_cast_count", {})),
            commander_tax=dict(value.get("commander_tax", {})),
            commander_zone=dict(value.get("commander_zone", {})),
            partner_group_key=value.get("partner_group_key"),
        )


@dataclass(frozen=True)
class SimulationTargetProgress:
    target_condition_id: str
    target_condition_version: str
    primary_success: bool = False
    support_success: bool = False
    compound_success: bool = False
    required_components: tuple[str, ...] = ()
    satisfied_components: tuple[str, ...] = ()
    failed_components: tuple[str, ...] = ()
    interaction_readiness: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.target_condition_id, "target_condition_id")
        _require_text(self.target_condition_version, "target_condition_version")
        for field_name in ("primary_success", "support_success", "compound_success"):
            if not isinstance(getattr(self, field_name), bool):
                raise SimulationStateBuildError(f"{field_name} must be a boolean")
        object.__setattr__(self, "required_components", _string_tuple(self.required_components, "required_components"))
        object.__setattr__(self, "satisfied_components", _string_tuple(self.satisfied_components, "satisfied_components"))
        object.__setattr__(self, "failed_components", _string_tuple(self.failed_components, "failed_components"))
        object.__setattr__(self, "interaction_readiness", _immutable_mapping(self.interaction_readiness, "interaction_readiness"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_condition_id": self.target_condition_id,
            "target_condition_version": self.target_condition_version,
            "primary_success": self.primary_success,
            "support_success": self.support_success,
            "compound_success": self.compound_success,
            "required_components": list(self.required_components),
            "satisfied_components": list(self.satisfied_components),
            "failed_components": list(self.failed_components),
            "interaction_readiness": _thaw_json(self.interaction_readiness),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "SimulationTargetProgress | None":
        if value is None:
            return None
        _require_mapping(value, "target progress")
        return cls(
            target_condition_id=value.get("target_condition_id"),
            target_condition_version=value.get("target_condition_version"),
            primary_success=bool(value.get("primary_success", False)),
            support_success=bool(value.get("support_success", False)),
            compound_success=bool(value.get("compound_success", False)),
            required_components=tuple(value.get("required_components", ())),
            satisfied_components=tuple(value.get("satisfied_components", ())),
            failed_components=tuple(value.get("failed_components", ())),
            interaction_readiness=value.get("interaction_readiness", {}),
        )


@dataclass(frozen=True)
class SimulationUnsupportedBehavior:
    card_instance_id: str
    card_name: str
    behavior_key: str
    reason: str
    severity: str
    action_blocked: bool
    discovered_at_state_id: str

    def __post_init__(self) -> None:
        _require_text(self.card_instance_id, "card_instance_id")
        _require_text(self.card_name, "card_name")
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.reason, "reason")
        _require_text(self.severity, "severity")
        if not isinstance(self.action_blocked, bool):
            raise SimulationStateBuildError("action_blocked must be a boolean")
        _require_text(self.discovered_at_state_id, "discovered_at_state_id")

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_instance_id": self.card_instance_id,
            "card_name": self.card_name,
            "behavior_key": self.behavior_key,
            "reason": self.reason,
            "severity": self.severity,
            "action_blocked": self.action_blocked,
            "discovered_at_state_id": self.discovered_at_state_id,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationUnsupportedBehavior":
        _require_mapping(value, "unsupported behavior")
        return cls(
            card_instance_id=value.get("card_instance_id"),
            card_name=value.get("card_name"),
            behavior_key=value.get("behavior_key"),
            reason=value.get("reason"),
            severity=value.get("severity"),
            action_blocked=value.get("action_blocked"),
            discovered_at_state_id=value.get("discovered_at_state_id"),
        )


@dataclass(frozen=True)
class SimulationState:
    state_id: str
    simulation_id: str
    history_id: str
    turn: int
    phase: str
    step: str
    active_player: str
    priority_player: str
    zones: tuple[SimulationZone, ...]
    state_version: str = SIM_R_STATE_VERSION
    mana_pool: SimulationManaPool = field(default_factory=SimulationManaPool)
    life_total: int = 40
    land_drop_available: bool = True
    lands_played_this_turn: int = 0
    commander_state: SimulationCommanderState = field(default_factory=SimulationCommanderState)
    target_progress: SimulationTargetProgress | None = None
    unsupported_behaviors: tuple[SimulationUnsupportedBehavior, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.state_id, "state_id")
        _require_text(self.state_version, "state_version")
        if self.state_version != SIM_R_STATE_VERSION:
            raise SimulationStateBuildError("unsupported SIM-R state_version")
        _require_text(self.simulation_id, "simulation_id")
        _require_text(self.history_id, "history_id")
        _require_non_negative_int(self.turn, "turn")
        if self.turn == 0:
            raise SimulationStateBuildError("turn must be greater than zero")
        _require_text(self.phase, "phase")
        _require_text(self.step, "step")
        _require_text(self.active_player, "active_player")
        _require_text(self.priority_player, "priority_player")
        zones = tuple(self.zones)
        if not zones:
            raise SimulationStateBuildError("at least one zone is required")
        if len({zone.zone_name for zone in zones}) != len(zones):
            raise SimulationStateBuildError("zone names must be unique")
        object.__setattr__(self, "zones", zones)
        if not isinstance(self.mana_pool, SimulationManaPool):
            raise SimulationStateBuildError("mana_pool must be a SimulationManaPool")
        _require_non_negative_int(self.life_total, "life_total")
        if not isinstance(self.land_drop_available, bool):
            raise SimulationStateBuildError("land_drop_available must be a boolean")
        _require_non_negative_int(self.lands_played_this_turn, "lands_played_this_turn")
        if not isinstance(self.commander_state, SimulationCommanderState):
            raise SimulationStateBuildError("commander_state must be a SimulationCommanderState")
        if self.target_progress is not None and not isinstance(self.target_progress, SimulationTargetProgress):
            raise SimulationStateBuildError("target_progress must be a SimulationTargetProgress")
        object.__setattr__(self, "unsupported_behaviors", tuple(self.unsupported_behaviors))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_simulation_state(self)

    @property
    def hand(self) -> SimulationZone | None:
        return self.zone("hand")

    @property
    def library(self) -> SimulationZone | None:
        return self.zone("library")

    @property
    def battlefield(self) -> SimulationZone | None:
        return self.zone("battlefield")

    @property
    def graveyard(self) -> SimulationZone | None:
        return self.zone("graveyard")

    @property
    def exile(self) -> SimulationZone | None:
        return self.zone("exile")

    @property
    def command_zone(self) -> SimulationZone | None:
        return self.zone("command_zone")

    @property
    def stack(self) -> SimulationZone | None:
        return self.zone("stack")

    def zone(self, zone_name: str) -> SimulationZone | None:
        _require_text(zone_name, "zone_name")
        for zone in self.zones:
            if zone.zone_name == zone_name:
                return zone
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_id": self.state_id,
            "state_version": self.state_version,
            "simulation_id": self.simulation_id,
            "history_id": self.history_id,
            "turn": self.turn,
            "phase": self.phase,
            "step": self.step,
            "active_player": self.active_player,
            "priority_player": self.priority_player,
            "zones": [zone.to_dict() for zone in self.zones],
            "mana_pool": self.mana_pool.to_dict(),
            "life_total": self.life_total,
            "land_drop_available": self.land_drop_available,
            "lands_played_this_turn": self.lands_played_this_turn,
            "commander_state": self.commander_state.to_dict(),
            "target_progress": self.target_progress.to_dict() if self.target_progress else None,
            "unsupported_behaviors": [item.to_dict() for item in self.unsupported_behaviors],
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationState":
        _reject_trace_v1(value)
        _require_mapping(value, "simulation state")
        zones = tuple(SimulationZone.from_mapping(item) for item in value.get("zones", ()))
        unsupported = tuple(SimulationUnsupportedBehavior.from_mapping(item) for item in value.get("unsupported_behaviors", ()))
        return cls(
            state_id=value.get("state_id"),
            state_version=value.get("state_version", SIM_R_STATE_VERSION),
            simulation_id=value.get("simulation_id"),
            history_id=value.get("history_id"),
            turn=value.get("turn"),
            phase=value.get("phase"),
            step=value.get("step"),
            active_player=value.get("active_player"),
            priority_player=value.get("priority_player"),
            zones=zones,
            mana_pool=SimulationManaPool.from_mapping(value.get("mana_pool")),
            life_total=value.get("life_total", 40),
            land_drop_available=value.get("land_drop_available", True),
            lands_played_this_turn=value.get("lands_played_this_turn", 0),
            commander_state=SimulationCommanderState.from_mapping(value.get("commander_state")),
            target_progress=SimulationTargetProgress.from_mapping(value.get("target_progress")),
            unsupported_behaviors=unsupported,
            metadata=value.get("metadata", {}),
        )


def build_simulation_state(value: Mapping[str, Any]) -> SimulationState:
    return SimulationState.from_mapping(value)


def simulation_state_to_dict(state: SimulationState) -> dict[str, Any]:
    if not isinstance(state, SimulationState):
        raise SimulationStateBuildError("state must be a SimulationState")
    return state.to_dict()


def validate_simulation_state(state: SimulationState) -> None:
    if not isinstance(state, SimulationState):
        raise SimulationStateBuildError("state must be a SimulationState")
    seen: set[str] = set()
    for zone in state.zones:
        for card in zone.cards:
            if card.card_instance_id in seen:
                raise SimulationStateBuildError("card_instance_id cannot appear in more than one zone")
            seen.add(card.card_instance_id)


def _reject_trace_v1(value: Any) -> None:
    if isinstance(value, Mapping) and "actions" in value and "opening_hand" in value and "state_version" not in value:
        raise SimulationStateBuildError("Phase 13 trace v1 payload is not a SIM-R state")


def _require_mapping(value: Any, label: str) -> None:
    if not isinstance(value, Mapping):
        raise SimulationStateBuildError(f"{label} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SimulationStateBuildError(f"{field_name} is required")


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SimulationStateBuildError(f"{field_name} must be an integer")
    if value < 0:
        raise SimulationStateBuildError(f"{field_name} cannot be negative")


def _string_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if isinstance(values, str) or not isinstance(values, (tuple, list)):
        raise SimulationStateBuildError(f"{field_name} must be a list or tuple")
    result = tuple(values)
    for value in result:
        _require_text(value, field_name)
    return result


def _immutable_mapping(value: Mapping[str, Any], label: str) -> Mapping[str, Any]:
    _require_mapping(value, label)
    return MappingProxyType({str(key): _freeze_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))})


def _immutable_int_mapping(value: Mapping[str, Any], label: str) -> Mapping[str, int]:
    _require_mapping(value, label)
    payload: dict[str, int] = {}
    for key, item in sorted(value.items(), key=lambda row: str(row[0])):
        _require_text(str(key), label)
        _require_non_negative_int(item, label)
        payload[str(key)] = int(item)
    return MappingProxyType(payload)


def _immutable_str_mapping(value: Mapping[str, Any], label: str) -> Mapping[str, str]:
    _require_mapping(value, label)
    payload: dict[str, str] = {}
    for key, item in sorted(value.items(), key=lambda row: str(row[0])):
        _require_text(str(key), label)
        _require_text(item, label)
        payload[str(key)] = item
    return MappingProxyType(payload)


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise SimulationStateBuildError("state metadata must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    if isinstance(value, list):
        return [_thaw_json(item) for item in value]
    return value

