"""Pure immutable transition result models for the future SIM-R engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


SIM_R_TRANSITION_VERSION = "sim-r-transition-v1"
NO_OP = "no_op"
SUCCESS = "success"


class SimulationTransitionBuildError(ValueError):
    """Raised when a SIM-R transition payload violates the transition contract."""


@dataclass(frozen=True)
class SimulationActionIntent:
    action_id: str
    action_type: str
    actor: str
    behavior_key: str
    source_card_instance_id: str | None = None
    target_card_instance_ids: tuple[str, ...] = ()
    declared_cost_keys: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.action_id, "action_id")
        _require_text(self.action_type, "action_type")
        _require_text(self.actor, "actor")
        _require_text(self.behavior_key, "behavior_key")
        if self.source_card_instance_id is not None:
            _require_text(self.source_card_instance_id, "source_card_instance_id")
        object.__setattr__(self, "target_card_instance_ids", _string_tuple(self.target_card_instance_ids, "target_card_instance_ids"))
        object.__setattr__(self, "declared_cost_keys", _string_tuple(self.declared_cost_keys, "declared_cost_keys"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "actor": self.actor,
            "behavior_key": self.behavior_key,
            "source_card_instance_id": self.source_card_instance_id,
            "target_card_instance_ids": list(self.target_card_instance_ids),
            "declared_cost_keys": list(self.declared_cost_keys),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationActionIntent":
        _require_mapping(value, "action intent")
        return cls(
            action_id=value.get("action_id"),
            action_type=value.get("action_type"),
            actor=value.get("actor"),
            behavior_key=value.get("behavior_key"),
            source_card_instance_id=value.get("source_card_instance_id"),
            target_card_instance_ids=tuple(value.get("target_card_instance_ids", ())),
            declared_cost_keys=tuple(value.get("declared_cost_keys", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationBehaviorResult:
    behavior_key: str
    behavior_status: str
    resource_ledger_ids: tuple[str, ...] = ()
    unsupported_behaviors: tuple[Mapping[str, Any], ...] = ()
    failed_reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.behavior_status, "behavior_status")
        object.__setattr__(self, "resource_ledger_ids", _string_tuple(self.resource_ledger_ids, "resource_ledger_ids"))
        object.__setattr__(
            self,
            "unsupported_behaviors",
            tuple(_immutable_mapping(item, "unsupported_behaviors") for item in self.unsupported_behaviors),
        )
        if self.failed_reason is not None:
            _require_text(self.failed_reason, "failed_reason")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "behavior_key": self.behavior_key,
            "behavior_status": self.behavior_status,
            "resource_ledger_ids": list(self.resource_ledger_ids),
            "unsupported_behaviors": [_thaw_json(item) for item in self.unsupported_behaviors],
            "failed_reason": self.failed_reason,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationBehaviorResult":
        _require_mapping(value, "behavior result")
        return cls(
            behavior_key=value.get("behavior_key"),
            behavior_status=value.get("behavior_status"),
            resource_ledger_ids=tuple(value.get("resource_ledger_ids", ())),
            unsupported_behaviors=tuple(value.get("unsupported_behaviors", ())),
            failed_reason=value.get("failed_reason"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationTransitionTraceEvent:
    trace_event_id: str
    transition_id: str
    pre_state_id: str
    post_state_id: str
    action_id: str
    behavior_key: str
    transition_status: str
    turn: int
    priority_sequence: int
    resource_ledger_ids: tuple[str, ...] = ()
    unsupported_behaviors: tuple[Mapping[str, Any], ...] = ()
    failed_reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.trace_event_id, "trace_event_id")
        _require_text(self.transition_id, "transition_id")
        _require_text(self.pre_state_id, "pre_state_id")
        _require_text(self.post_state_id, "post_state_id")
        _require_text(self.action_id, "action_id")
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.transition_status, "transition_status")
        _require_non_negative_int(self.turn, "turn")
        _require_non_negative_int(self.priority_sequence, "priority_sequence")
        object.__setattr__(self, "resource_ledger_ids", _string_tuple(self.resource_ledger_ids, "resource_ledger_ids"))
        object.__setattr__(
            self,
            "unsupported_behaviors",
            tuple(_immutable_mapping(item, "unsupported_behaviors") for item in self.unsupported_behaviors),
        )
        if self.failed_reason is not None:
            _require_text(self.failed_reason, "failed_reason")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_event_id": self.trace_event_id,
            "transition_id": self.transition_id,
            "pre_state_id": self.pre_state_id,
            "post_state_id": self.post_state_id,
            "action_id": self.action_id,
            "behavior_key": self.behavior_key,
            "transition_status": self.transition_status,
            "turn": self.turn,
            "priority_sequence": self.priority_sequence,
            "resource_ledger_ids": list(self.resource_ledger_ids),
            "unsupported_behaviors": [_thaw_json(item) for item in self.unsupported_behaviors],
            "failed_reason": self.failed_reason,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationTransitionTraceEvent":
        _require_mapping(value, "transition trace event")
        return cls(
            trace_event_id=value.get("trace_event_id"),
            transition_id=value.get("transition_id"),
            pre_state_id=value.get("pre_state_id"),
            post_state_id=value.get("post_state_id"),
            action_id=value.get("action_id"),
            behavior_key=value.get("behavior_key"),
            transition_status=value.get("transition_status"),
            turn=value.get("turn"),
            priority_sequence=value.get("priority_sequence"),
            resource_ledger_ids=tuple(value.get("resource_ledger_ids", ())),
            unsupported_behaviors=tuple(value.get("unsupported_behaviors", ())),
            failed_reason=value.get("failed_reason"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationTransitionResult:
    transition_id: str
    simulation_id: str
    pre_state_id: str
    post_state_id: str
    action_intent: SimulationActionIntent
    behavior_result: SimulationBehaviorResult
    transition_status: str
    turn: int
    priority_sequence: int
    resource_ledger_ids: tuple[str, ...] = ()
    trace_events: tuple[SimulationTransitionTraceEvent, ...] = ()
    transition_version: str = SIM_R_TRANSITION_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.transition_id, "transition_id")
        _require_text(self.transition_version, "transition_version")
        if self.transition_version != SIM_R_TRANSITION_VERSION:
            raise SimulationTransitionBuildError("unsupported SIM-R transition_version")
        _require_text(self.simulation_id, "simulation_id")
        _require_text(self.pre_state_id, "pre_state_id")
        _require_text(self.post_state_id, "post_state_id")
        if not isinstance(self.action_intent, SimulationActionIntent):
            raise SimulationTransitionBuildError("action_intent must be a SimulationActionIntent")
        if not isinstance(self.behavior_result, SimulationBehaviorResult):
            raise SimulationTransitionBuildError("behavior_result must be a SimulationBehaviorResult")
        _require_text(self.transition_status, "transition_status")
        _require_non_negative_int(self.turn, "turn")
        _require_non_negative_int(self.priority_sequence, "priority_sequence")
        object.__setattr__(self, "resource_ledger_ids", _string_tuple(self.resource_ledger_ids, "resource_ledger_ids"))
        trace_events = tuple(self.trace_events)
        for trace_event in trace_events:
            if not isinstance(trace_event, SimulationTransitionTraceEvent):
                raise SimulationTransitionBuildError("trace_events must be SimulationTransitionTraceEvent values")
        object.__setattr__(self, "trace_events", trace_events)
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_transition_result(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "transition_id": self.transition_id,
            "transition_version": self.transition_version,
            "simulation_id": self.simulation_id,
            "pre_state_id": self.pre_state_id,
            "post_state_id": self.post_state_id,
            "action_intent": self.action_intent.to_dict(),
            "behavior_result": self.behavior_result.to_dict(),
            "transition_status": self.transition_status,
            "turn": self.turn,
            "priority_sequence": self.priority_sequence,
            "resource_ledger_ids": list(self.resource_ledger_ids),
            "trace_events": [trace_event.to_dict() for trace_event in self.trace_events],
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationTransitionResult":
        _require_mapping(value, "transition result")
        return cls(
            transition_id=value.get("transition_id"),
            transition_version=value.get("transition_version", SIM_R_TRANSITION_VERSION),
            simulation_id=value.get("simulation_id"),
            pre_state_id=value.get("pre_state_id"),
            post_state_id=value.get("post_state_id"),
            action_intent=SimulationActionIntent.from_mapping(value.get("action_intent", {})),
            behavior_result=SimulationBehaviorResult.from_mapping(value.get("behavior_result", {})),
            transition_status=value.get("transition_status"),
            turn=value.get("turn"),
            priority_sequence=value.get("priority_sequence"),
            resource_ledger_ids=tuple(value.get("resource_ledger_ids", ())),
            trace_events=tuple(SimulationTransitionTraceEvent.from_mapping(item) for item in value.get("trace_events", ())),
            metadata=value.get("metadata", {}),
        )


def build_transition_result(value: Mapping[str, Any]) -> SimulationTransitionResult:
    return SimulationTransitionResult.from_mapping(value)


def transition_result_to_dict(result: SimulationTransitionResult) -> dict[str, Any]:
    if not isinstance(result, SimulationTransitionResult):
        raise SimulationTransitionBuildError("result must be a SimulationTransitionResult")
    return result.to_dict()


def validate_transition_result(result: SimulationTransitionResult) -> None:
    if not isinstance(result, SimulationTransitionResult):
        raise SimulationTransitionBuildError("result must be a SimulationTransitionResult")
    if result.pre_state_id == result.post_state_id and result.transition_status != NO_OP:
        raise SimulationTransitionBuildError("matching pre_state_id and post_state_id requires no_op transition_status")
    if result.transition_status == SUCCESS and result.action_intent.declared_cost_keys and not result.resource_ledger_ids:
        raise SimulationTransitionBuildError("resource-consuming successful transitions require resource_ledger_ids")
    for trace_event in result.trace_events:
        if trace_event.transition_id != result.transition_id:
            raise SimulationTransitionBuildError("trace_event transition_id must match result transition_id")
        if trace_event.pre_state_id != result.pre_state_id:
            raise SimulationTransitionBuildError("trace_event pre_state_id must match result pre_state_id")
        if trace_event.post_state_id != result.post_state_id:
            raise SimulationTransitionBuildError("trace_event post_state_id must match result post_state_id")
        if trace_event.action_id != result.action_intent.action_id:
            raise SimulationTransitionBuildError("trace_event action_id must match action_intent action_id")


def _require_mapping(value: Any, label: str) -> None:
    if not isinstance(value, Mapping):
        raise SimulationTransitionBuildError(f"{label} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SimulationTransitionBuildError(f"{field_name} is required")


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise SimulationTransitionBuildError(f"{field_name} must be an integer")
    if value < 0:
        raise SimulationTransitionBuildError(f"{field_name} cannot be negative")


def _string_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if isinstance(values, str) or not isinstance(values, (tuple, list)):
        raise SimulationTransitionBuildError(f"{field_name} must be a list or tuple")
    result = tuple(values)
    for value in result:
        _require_text(value, field_name)
    return result


def _immutable_mapping(value: Mapping[str, Any], label: str) -> Mapping[str, Any]:
    _require_mapping(value, label)
    return MappingProxyType({str(key): _freeze_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))})


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise SimulationTransitionBuildError("transition metadata must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    if isinstance(value, list):
        return [_thaw_json(item) for item in value]
    return value
