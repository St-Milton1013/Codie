"""Pure immutable behavior-to-transition wiring models for the future SIM-R engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from .sim_r_behavior import SUPPORTED_BEHAVIOR_CATEGORIES


SIM_R_WIRING_VERSION = "sim-r-wiring-v1"
COMPATIBLE = "compatible"
INCOMPATIBLE = "incompatible"

_EXECUTABLE_KEYS = {
    "__call__",
    "callable",
    "code_payload",
    "executable_code",
    "function",
    "function_body",
    "llm_executable_behavior",
}


class SimulationWiringBuildError(ValueError):
    """Raised when a SIM-R wiring payload violates the wiring contract."""


@dataclass(frozen=True)
class SimulationBehaviorTransitionLink:
    wiring_id: str
    simulation_id: str
    pre_state_id: str
    post_state_id: str
    action_id: str
    behavior_profile_id: str
    behavior_proposal_id: str
    behavior_key: str
    behavior_category: str
    compatibility_status: str
    transition_id: str | None = None
    resource_ledger_ids: tuple[str, ...] = ()
    requirement_ids: tuple[str, ...] = ()
    unsupported_note_ids: tuple[str, ...] = ()
    failure_reason: str | None = None
    caveats: tuple[str, ...] = ()
    wiring_version: str = SIM_R_WIRING_VERSION
    turn: int | None = None
    priority_sequence: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.wiring_id, "wiring_id")
        _require_text(self.wiring_version, "wiring_version")
        if self.wiring_version != SIM_R_WIRING_VERSION:
            raise SimulationWiringBuildError("unsupported SIM-R wiring_version")
        _require_text(self.simulation_id, "simulation_id")
        _require_text(self.pre_state_id, "pre_state_id")
        _require_text(self.post_state_id, "post_state_id")
        _require_text(self.action_id, "action_id")
        _require_text(self.behavior_profile_id, "behavior_profile_id")
        _require_text(self.behavior_proposal_id, "behavior_proposal_id")
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.behavior_category, "behavior_category")
        if self.behavior_category not in SUPPORTED_BEHAVIOR_CATEGORIES:
            raise SimulationWiringBuildError("unsupported behavior_category")
        _require_text(self.compatibility_status, "compatibility_status")
        if self.transition_id is not None:
            _require_text(self.transition_id, "transition_id")
        if self.failure_reason is not None:
            _require_text(self.failure_reason, "failure_reason")
        if self.turn is not None:
            _require_non_negative_int(self.turn, "turn")
        if self.priority_sequence is not None:
            _require_non_negative_int(self.priority_sequence, "priority_sequence")
        object.__setattr__(self, "resource_ledger_ids", _unique_string_tuple(self.resource_ledger_ids, "resource_ledger_ids"))
        object.__setattr__(self, "requirement_ids", _unique_string_tuple(self.requirement_ids, "requirement_ids"))
        object.__setattr__(self, "unsupported_note_ids", _unique_string_tuple(self.unsupported_note_ids, "unsupported_note_ids"))
        object.__setattr__(self, "caveats", _string_tuple(self.caveats, "caveats"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_behavior_transition_link(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "wiring_id": self.wiring_id,
            "wiring_version": self.wiring_version,
            "simulation_id": self.simulation_id,
            "pre_state_id": self.pre_state_id,
            "post_state_id": self.post_state_id,
            "action_id": self.action_id,
            "behavior_profile_id": self.behavior_profile_id,
            "behavior_proposal_id": self.behavior_proposal_id,
            "behavior_key": self.behavior_key,
            "behavior_category": self.behavior_category,
            "compatibility_status": self.compatibility_status,
            "transition_id": self.transition_id,
            "resource_ledger_ids": list(self.resource_ledger_ids),
            "requirement_ids": list(self.requirement_ids),
            "unsupported_note_ids": list(self.unsupported_note_ids),
            "failure_reason": self.failure_reason,
            "caveats": list(self.caveats),
            "turn": self.turn,
            "priority_sequence": self.priority_sequence,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationBehaviorTransitionLink":
        _require_mapping(value, "behavior transition link")
        return cls(
            wiring_id=value.get("wiring_id"),
            wiring_version=value.get("wiring_version", SIM_R_WIRING_VERSION),
            simulation_id=value.get("simulation_id"),
            pre_state_id=value.get("pre_state_id"),
            post_state_id=value.get("post_state_id"),
            action_id=value.get("action_id"),
            behavior_profile_id=value.get("behavior_profile_id"),
            behavior_proposal_id=value.get("behavior_proposal_id"),
            behavior_key=value.get("behavior_key"),
            behavior_category=value.get("behavior_category"),
            compatibility_status=value.get("compatibility_status"),
            transition_id=value.get("transition_id"),
            resource_ledger_ids=tuple(value.get("resource_ledger_ids", ())),
            requirement_ids=tuple(value.get("requirement_ids", ())),
            unsupported_note_ids=tuple(value.get("unsupported_note_ids", ())),
            failure_reason=value.get("failure_reason"),
            caveats=tuple(value.get("caveats", ())),
            turn=value.get("turn"),
            priority_sequence=value.get("priority_sequence"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationBehaviorWiringResult:
    wiring_result_id: str
    simulation_id: str
    links: tuple[SimulationBehaviorTransitionLink, ...]
    wiring_version: str = SIM_R_WIRING_VERSION
    compatibility_status: str = COMPATIBLE
    failure_reason: str | None = None
    caveats: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.wiring_result_id, "wiring_result_id")
        _require_text(self.wiring_version, "wiring_version")
        if self.wiring_version != SIM_R_WIRING_VERSION:
            raise SimulationWiringBuildError("unsupported SIM-R wiring_version")
        _require_text(self.simulation_id, "simulation_id")
        _require_text(self.compatibility_status, "compatibility_status")
        if self.failure_reason is not None:
            _require_text(self.failure_reason, "failure_reason")
        links = tuple(self.links)
        if not links:
            raise SimulationWiringBuildError("links must contain at least one transition link")
        for link in links:
            if not isinstance(link, SimulationBehaviorTransitionLink):
                raise SimulationWiringBuildError("links must be SimulationBehaviorTransitionLink values")
        object.__setattr__(self, "links", links)
        object.__setattr__(self, "caveats", _string_tuple(self.caveats, "caveats"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_behavior_wiring_result(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "wiring_result_id": self.wiring_result_id,
            "wiring_version": self.wiring_version,
            "simulation_id": self.simulation_id,
            "compatibility_status": self.compatibility_status,
            "failure_reason": self.failure_reason,
            "caveats": list(self.caveats),
            "links": [link.to_dict() for link in self.links],
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationBehaviorWiringResult":
        _require_mapping(value, "behavior wiring result")
        return cls(
            wiring_result_id=value.get("wiring_result_id"),
            wiring_version=value.get("wiring_version", SIM_R_WIRING_VERSION),
            simulation_id=value.get("simulation_id"),
            compatibility_status=value.get("compatibility_status", COMPATIBLE),
            failure_reason=value.get("failure_reason"),
            caveats=tuple(value.get("caveats", ())),
            links=tuple(SimulationBehaviorTransitionLink.from_mapping(item) for item in value.get("links", ())),
            metadata=value.get("metadata", {}),
        )


def build_behavior_transition_link(payload: Mapping[str, Any]) -> SimulationBehaviorTransitionLink:
    return SimulationBehaviorTransitionLink.from_mapping(payload)


def build_behavior_wiring_result(payload: Mapping[str, Any]) -> SimulationBehaviorWiringResult:
    return SimulationBehaviorWiringResult.from_mapping(payload)


def behavior_transition_link_to_dict(link: SimulationBehaviorTransitionLink) -> dict[str, Any]:
    if not isinstance(link, SimulationBehaviorTransitionLink):
        raise SimulationWiringBuildError("link must be a SimulationBehaviorTransitionLink")
    return link.to_dict()


def behavior_wiring_result_to_dict(result: SimulationBehaviorWiringResult) -> dict[str, Any]:
    if not isinstance(result, SimulationBehaviorWiringResult):
        raise SimulationWiringBuildError("result must be a SimulationBehaviorWiringResult")
    return result.to_dict()


def validate_behavior_transition_link(link: SimulationBehaviorTransitionLink) -> None:
    _reject_executable_payloads(link.metadata, "metadata")
    if link.compatibility_status == COMPATIBLE:
        if not link.transition_id:
            raise SimulationWiringBuildError("compatible links require transition_id")
        if not link.requirement_ids and not link.resource_ledger_ids and not link.unsupported_note_ids:
            raise SimulationWiringBuildError("compatible links require at least one supporting reference")
    if link.compatibility_status == INCOMPATIBLE and not (link.failure_reason or link.caveats):
        raise SimulationWiringBuildError("incompatible links require failure_reason or caveats")


def validate_behavior_wiring_result(result: SimulationBehaviorWiringResult) -> None:
    _reject_executable_payloads(result.metadata, "metadata")
    seen_ids: set[str] = set()
    statuses = set()
    for link in result.links:
        if link.wiring_id in seen_ids:
            raise SimulationWiringBuildError("duplicate wiring_id in wiring result")
        seen_ids.add(link.wiring_id)
        if link.simulation_id != result.simulation_id:
            raise SimulationWiringBuildError("link simulation_id must match wiring result")
        statuses.add(link.compatibility_status)
    if result.compatibility_status == COMPATIBLE and INCOMPATIBLE in statuses:
        raise SimulationWiringBuildError("compatible wiring result cannot contain incompatible links")
    if result.compatibility_status == INCOMPATIBLE and not (result.failure_reason or result.caveats):
        raise SimulationWiringBuildError("incompatible wiring result requires failure_reason or caveats")


def _immutable_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    _require_mapping(value, field_name)
    frozen: dict[str, Any] = {}
    for key, item in value.items():
        _require_text(key, f"{field_name} key")
        if key in _EXECUTABLE_KEYS:
            raise SimulationWiringBuildError(f"{field_name} contains executable key")
        frozen[key] = _freeze_json(item, field_name)
    return MappingProxyType(frozen)


def _freeze_json(value: Any, field_name: str) -> Any:
    if callable(value):
        raise SimulationWiringBuildError(f"{field_name} contains callable value")
    if isinstance(value, Mapping):
        return _immutable_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise SimulationWiringBuildError(f"{field_name} must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _reject_executable_payloads(value: Any, field_name: str) -> None:
    if callable(value):
        raise SimulationWiringBuildError(f"{field_name} contains callable value")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in _EXECUTABLE_KEYS:
                raise SimulationWiringBuildError(f"{field_name} contains executable key")
            _reject_executable_payloads(item, field_name)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_executable_payloads(item, field_name)


def _require_mapping(value: Any, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise SimulationWiringBuildError(f"{field_name} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SimulationWiringBuildError(f"{field_name} is required")


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if not isinstance(value, int) or value < 0:
        raise SimulationWiringBuildError(f"{field_name} must be a non-negative integer")


def _string_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise SimulationWiringBuildError(f"{field_name} must be a tuple")
    for value in values:
        _require_text(value, field_name)
    return values


def _unique_string_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    string_values = _string_tuple(values, field_name)
    if len(set(string_values)) != len(string_values):
        raise SimulationWiringBuildError(f"{field_name} must not contain duplicates")
    return string_values
