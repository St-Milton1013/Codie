"""Pure immutable behavior proposal models for the future SIM-R engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


SIM_R_BEHAVIOR_VERSION = "sim-r-behavior-v1"
UNSUPPORTED_BEHAVIOR_CATEGORY = "Unsupported"
SUPPORTED_BEHAVIOR_CATEGORIES = (
    "NormalCast",
    "ManaProduction",
    "FastMana",
    "Tutor",
    "Draw",
    "CounterSpell",
    "Bounce",
    "Removal",
    "AlternativeCost",
    "CommanderCondition",
    "PitchCost",
    "PayLife",
    "ChangeZone",
    "StaticCondition",
    "TurnRestriction",
    "TargetRequirement",
    UNSUPPORTED_BEHAVIOR_CATEGORY,
)

_EXECUTABLE_KEYS = {
    "__call__",
    "callable",
    "code_payload",
    "executable_code",
    "function",
    "function_body",
}


class SimulationBehaviorBuildError(ValueError):
    """Raised when a SIM-R behavior payload violates the behavior contract."""


@dataclass(frozen=True)
class SimulationBehaviorRequirement:
    requirement_id: str
    requirement_type: str
    intent: Mapping[str, Any]
    status: str = "required"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.requirement_id, "requirement_id")
        _require_text(self.requirement_type, "requirement_type")
        _require_text(self.status, "status")
        object.__setattr__(self, "intent", _immutable_mapping(self.intent, "intent"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "requirement_type": self.requirement_type,
            "intent": _thaw_json(self.intent),
            "status": self.status,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationBehaviorRequirement":
        _require_mapping(value, "behavior requirement")
        return cls(
            requirement_id=value.get("requirement_id"),
            requirement_type=value.get("requirement_type"),
            intent=value.get("intent", {}),
            status=value.get("status", "required"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationUnsupportedBehaviorNote:
    note_id: str
    behavior_key: str
    reason: str
    affected_card_name: str | None = None
    source_card_identity: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.note_id, "note_id")
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.reason, "reason")
        if self.affected_card_name is not None:
            _require_text(self.affected_card_name, "affected_card_name")
        object.__setattr__(self, "source_card_identity", _immutable_mapping(self.source_card_identity, "source_card_identity"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "note_id": self.note_id,
            "behavior_key": self.behavior_key,
            "reason": self.reason,
            "affected_card_name": self.affected_card_name,
            "source_card_identity": _thaw_json(self.source_card_identity),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationUnsupportedBehaviorNote":
        _require_mapping(value, "unsupported behavior note")
        return cls(
            note_id=value.get("note_id"),
            behavior_key=value.get("behavior_key"),
            reason=value.get("reason"),
            affected_card_name=value.get("affected_card_name"),
            source_card_identity=value.get("source_card_identity", {}),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationBehaviorProfile:
    behavior_profile_id: str
    behavior_key: str
    behavior_category: str
    supported_action_types: tuple[str, ...]
    behavior_version: str = SIM_R_BEHAVIOR_VERSION
    source_card_identity: Mapping[str, Any] = field(default_factory=dict)
    status: str = "supported"
    confidence: float = 1.0
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.behavior_profile_id, "behavior_profile_id")
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.behavior_category, "behavior_category")
        _validate_behavior_category(self.behavior_category)
        _require_text(self.behavior_version, "behavior_version")
        if self.behavior_version != SIM_R_BEHAVIOR_VERSION:
            raise SimulationBehaviorBuildError("unsupported SIM-R behavior_version")
        object.__setattr__(self, "supported_action_types", _string_tuple(self.supported_action_types, "supported_action_types"))
        _require_text(self.status, "status")
        _require_confidence(self.confidence, "confidence")
        object.__setattr__(self, "source_card_identity", _immutable_mapping(self.source_card_identity, "source_card_identity"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_behavior_profile(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "behavior_profile_id": self.behavior_profile_id,
            "behavior_key": self.behavior_key,
            "behavior_category": self.behavior_category,
            "behavior_version": self.behavior_version,
            "supported_action_types": list(self.supported_action_types),
            "source_card_identity": _thaw_json(self.source_card_identity),
            "status": self.status,
            "confidence": self.confidence,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationBehaviorProfile":
        _require_mapping(value, "behavior profile")
        return cls(
            behavior_profile_id=value.get("behavior_profile_id"),
            behavior_key=value.get("behavior_key"),
            behavior_category=value.get("behavior_category"),
            behavior_version=value.get("behavior_version", SIM_R_BEHAVIOR_VERSION),
            supported_action_types=tuple(value.get("supported_action_types", ())),
            source_card_identity=value.get("source_card_identity", {}),
            status=value.get("status", "supported"),
            confidence=value.get("confidence", 1.0),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationBehaviorProposal:
    proposal_id: str
    behavior_profile_id: str
    behavior_key: str
    behavior_category: str
    action_id: str
    proposal_status: str
    requirements: tuple[SimulationBehaviorRequirement, ...] = ()
    required_resource_intents: tuple[Mapping[str, Any], ...] = ()
    zone_change_intents: tuple[Mapping[str, Any], ...] = ()
    target_requirements: tuple[Mapping[str, Any], ...] = ()
    timing_restrictions: tuple[Mapping[str, Any], ...] = ()
    unsupported_behavior_notes: tuple[SimulationUnsupportedBehaviorNote, ...] = ()
    behavior_version: str = SIM_R_BEHAVIOR_VERSION
    confidence: float = 1.0
    source_card_identity: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.proposal_id, "proposal_id")
        _require_text(self.behavior_profile_id, "behavior_profile_id")
        _require_text(self.behavior_key, "behavior_key")
        _require_text(self.behavior_category, "behavior_category")
        _validate_behavior_category(self.behavior_category)
        _require_text(self.action_id, "action_id")
        _require_text(self.proposal_status, "proposal_status")
        _require_text(self.behavior_version, "behavior_version")
        if self.behavior_version != SIM_R_BEHAVIOR_VERSION:
            raise SimulationBehaviorBuildError("unsupported SIM-R behavior_version")
        _require_confidence(self.confidence, "confidence")

        requirements = tuple(self.requirements)
        for requirement in requirements:
            if not isinstance(requirement, SimulationBehaviorRequirement):
                raise SimulationBehaviorBuildError("requirements must be SimulationBehaviorRequirement values")
        notes = tuple(self.unsupported_behavior_notes)
        for note in notes:
            if not isinstance(note, SimulationUnsupportedBehaviorNote):
                raise SimulationBehaviorBuildError("unsupported_behavior_notes must be SimulationUnsupportedBehaviorNote values")

        object.__setattr__(self, "requirements", requirements)
        object.__setattr__(self, "required_resource_intents", _mapping_tuple(self.required_resource_intents, "required_resource_intents"))
        object.__setattr__(self, "zone_change_intents", _mapping_tuple(self.zone_change_intents, "zone_change_intents"))
        object.__setattr__(self, "target_requirements", _mapping_tuple(self.target_requirements, "target_requirements"))
        object.__setattr__(self, "timing_restrictions", _mapping_tuple(self.timing_restrictions, "timing_restrictions"))
        object.__setattr__(self, "unsupported_behavior_notes", notes)
        object.__setattr__(self, "source_card_identity", _immutable_mapping(self.source_card_identity, "source_card_identity"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_behavior_proposal(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "behavior_profile_id": self.behavior_profile_id,
            "behavior_key": self.behavior_key,
            "behavior_category": self.behavior_category,
            "behavior_version": self.behavior_version,
            "action_id": self.action_id,
            "proposal_status": self.proposal_status,
            "requirements": [requirement.to_dict() for requirement in self.requirements],
            "required_resource_intents": [_thaw_json(item) for item in self.required_resource_intents],
            "zone_change_intents": [_thaw_json(item) for item in self.zone_change_intents],
            "target_requirements": [_thaw_json(item) for item in self.target_requirements],
            "timing_restrictions": [_thaw_json(item) for item in self.timing_restrictions],
            "unsupported_behavior_notes": [note.to_dict() for note in self.unsupported_behavior_notes],
            "confidence": self.confidence,
            "source_card_identity": _thaw_json(self.source_card_identity),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationBehaviorProposal":
        _require_mapping(value, "behavior proposal")
        return cls(
            proposal_id=value.get("proposal_id"),
            behavior_profile_id=value.get("behavior_profile_id"),
            behavior_key=value.get("behavior_key"),
            behavior_category=value.get("behavior_category"),
            behavior_version=value.get("behavior_version", SIM_R_BEHAVIOR_VERSION),
            action_id=value.get("action_id"),
            proposal_status=value.get("proposal_status"),
            requirements=tuple(SimulationBehaviorRequirement.from_mapping(item) for item in value.get("requirements", ())),
            required_resource_intents=tuple(value.get("required_resource_intents", ())),
            zone_change_intents=tuple(value.get("zone_change_intents", ())),
            target_requirements=tuple(value.get("target_requirements", ())),
            timing_restrictions=tuple(value.get("timing_restrictions", ())),
            unsupported_behavior_notes=tuple(
                SimulationUnsupportedBehaviorNote.from_mapping(item) for item in value.get("unsupported_behavior_notes", ())
            ),
            confidence=value.get("confidence", 1.0),
            source_card_identity=value.get("source_card_identity", {}),
            metadata=value.get("metadata", {}),
        )


def build_behavior_profile(value: Mapping[str, Any]) -> SimulationBehaviorProfile:
    return SimulationBehaviorProfile.from_mapping(value)


def build_behavior_proposal(value: Mapping[str, Any]) -> SimulationBehaviorProposal:
    return SimulationBehaviorProposal.from_mapping(value)


def behavior_profile_to_dict(profile: SimulationBehaviorProfile) -> dict[str, Any]:
    if not isinstance(profile, SimulationBehaviorProfile):
        raise SimulationBehaviorBuildError("profile must be a SimulationBehaviorProfile")
    return profile.to_dict()


def behavior_proposal_to_dict(proposal: SimulationBehaviorProposal) -> dict[str, Any]:
    if not isinstance(proposal, SimulationBehaviorProposal):
        raise SimulationBehaviorBuildError("proposal must be a SimulationBehaviorProposal")
    return proposal.to_dict()


def validate_behavior_profile(profile: SimulationBehaviorProfile) -> None:
    if not isinstance(profile, SimulationBehaviorProfile):
        raise SimulationBehaviorBuildError("profile must be a SimulationBehaviorProfile")
    if not profile.supported_action_types:
        raise SimulationBehaviorBuildError("supported_action_types must not be empty")
    if profile.behavior_category == UNSUPPORTED_BEHAVIOR_CATEGORY and profile.status == "supported":
        raise SimulationBehaviorBuildError("Unsupported behavior profiles cannot have supported status")


def validate_behavior_proposal(proposal: SimulationBehaviorProposal) -> None:
    if not isinstance(proposal, SimulationBehaviorProposal):
        raise SimulationBehaviorBuildError("proposal must be a SimulationBehaviorProposal")
    requirement_ids: set[str] = set()
    for requirement in proposal.requirements:
        if requirement.requirement_id in requirement_ids:
            raise SimulationBehaviorBuildError("requirement_id values must be unique")
        requirement_ids.add(requirement.requirement_id)
    note_ids: set[str] = set()
    for note in proposal.unsupported_behavior_notes:
        if note.note_id in note_ids:
            raise SimulationBehaviorBuildError("unsupported behavior note_id values must be unique")
        note_ids.add(note.note_id)
        if note.behavior_key != proposal.behavior_key:
            raise SimulationBehaviorBuildError("unsupported behavior note behavior_key must match proposal behavior_key")
    if proposal.behavior_category == UNSUPPORTED_BEHAVIOR_CATEGORY and not proposal.unsupported_behavior_notes:
        raise SimulationBehaviorBuildError("Unsupported behavior proposals require unsupported_behavior_notes")


def _validate_behavior_category(value: str) -> None:
    if value not in SUPPORTED_BEHAVIOR_CATEGORIES:
        raise SimulationBehaviorBuildError("unknown behavior_category")


def _require_mapping(value: Any, label: str) -> None:
    if not isinstance(value, Mapping):
        raise SimulationBehaviorBuildError(f"{label} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SimulationBehaviorBuildError(f"{field_name} is required")


def _require_confidence(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SimulationBehaviorBuildError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise SimulationBehaviorBuildError(f"{field_name} must be between 0 and 1")


def _string_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if isinstance(values, str) or not isinstance(values, (tuple, list)):
        raise SimulationBehaviorBuildError(f"{field_name} must be a list or tuple")
    result = tuple(values)
    for value in result:
        _require_text(value, field_name)
    return result


def _mapping_tuple(values: Any, field_name: str) -> tuple[Mapping[str, Any], ...]:
    if isinstance(values, Mapping) or not isinstance(values, (tuple, list)):
        raise SimulationBehaviorBuildError(f"{field_name} must be a list or tuple")
    return tuple(_immutable_mapping(value, field_name) for value in values)


def _immutable_mapping(value: Mapping[str, Any], label: str) -> Mapping[str, Any]:
    _require_mapping(value, label)
    _reject_executable_payload(value, label)
    return MappingProxyType({str(key): _freeze_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))})


def _reject_executable_payload(value: Any, label: str) -> None:
    if callable(value):
        raise SimulationBehaviorBuildError(f"{label} cannot contain callable values")
    if isinstance(value, Mapping):
        authored_by_llm = str(value.get("authored_by", "")).lower() == "llm"
        executable = value.get("executable") is True
        if authored_by_llm and executable:
            raise SimulationBehaviorBuildError("LLM-authored executable behavior is rejected")
        for key, item in value.items():
            key_text = str(key).lower()
            if key_text in _EXECUTABLE_KEYS:
                raise SimulationBehaviorBuildError("executable behavior payloads are rejected")
            if key_text == "llm_authored_executable" and item:
                raise SimulationBehaviorBuildError("LLM-authored executable behavior is rejected")
            if key_text == "executable" and item is True:
                raise SimulationBehaviorBuildError("executable behavior payloads are rejected")
            _reject_executable_payload(item, f"{label}.{key_text}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_executable_payload(item, f"{label}[{index}]")


def _freeze_json(value: Any) -> Any:
    _reject_executable_payload(value, "metadata")
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise SimulationBehaviorBuildError("behavior metadata must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    if isinstance(value, list):
        return [_thaw_json(item) for item in value]
    return value
