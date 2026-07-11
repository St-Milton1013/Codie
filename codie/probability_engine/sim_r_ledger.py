"""Pure immutable resource ledger models for the future SIM-R engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


SIM_R_LEDGER_VERSION = "sim-r-ledger-v1"


class SimulationLedgerBuildError(ValueError):
    """Raised when a SIM-R resource ledger payload violates the ledger contract."""


@dataclass(frozen=True)
class SimulationResourceLedgerEntry:
    ledger_entry_id: str
    resource_key: str
    resource_type: str
    resource_quantity: int | float
    action_id: str
    cost_key: str
    payment_key: str
    status: str = "consumed"
    reusable: bool = False
    restriction_metadata: Mapping[str, Any] = field(default_factory=dict)
    unsupported_metadata: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.ledger_entry_id, "ledger_entry_id")
        _require_text(self.resource_key, "resource_key")
        _require_text(self.resource_type, "resource_type")
        _require_non_negative_number(self.resource_quantity, "resource_quantity")
        _require_text(self.action_id, "action_id")
        _require_text(self.cost_key, "cost_key")
        _require_text(self.payment_key, "payment_key")
        _require_text(self.status, "status")
        if not isinstance(self.reusable, bool):
            raise SimulationLedgerBuildError("reusable must be a boolean")
        object.__setattr__(self, "restriction_metadata", _immutable_mapping(self.restriction_metadata, "restriction_metadata"))
        object.__setattr__(self, "unsupported_metadata", _immutable_mapping(self.unsupported_metadata, "unsupported_metadata"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "ledger_entry_id": self.ledger_entry_id,
            "resource_key": self.resource_key,
            "resource_type": self.resource_type,
            "resource_quantity": self.resource_quantity,
            "action_id": self.action_id,
            "cost_key": self.cost_key,
            "payment_key": self.payment_key,
            "status": self.status,
            "reusable": self.reusable,
            "restriction_metadata": _thaw_json(self.restriction_metadata),
            "unsupported_metadata": _thaw_json(self.unsupported_metadata),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationResourceLedgerEntry":
        _require_mapping(value, "resource ledger entry")
        return cls(
            ledger_entry_id=value.get("ledger_entry_id"),
            resource_key=value.get("resource_key"),
            resource_type=value.get("resource_type"),
            resource_quantity=value.get("resource_quantity"),
            action_id=value.get("action_id"),
            cost_key=value.get("cost_key"),
            payment_key=value.get("payment_key"),
            status=value.get("status", "consumed"),
            reusable=bool(value.get("reusable", False)),
            restriction_metadata=value.get("restriction_metadata", {}),
            unsupported_metadata=value.get("unsupported_metadata", {}),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationPaymentRecord:
    payment_key: str
    action_id: str
    cost_key: str
    status: str
    paid_resource_keys: tuple[str, ...] = ()
    failed_reason: str | None = None
    unsupported_reason: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.payment_key, "payment_key")
        _require_text(self.action_id, "action_id")
        _require_text(self.cost_key, "cost_key")
        _require_text(self.status, "status")
        object.__setattr__(self, "paid_resource_keys", _string_tuple(self.paid_resource_keys, "paid_resource_keys"))
        if self.failed_reason is not None:
            _require_text(self.failed_reason, "failed_reason")
        if self.unsupported_reason is not None:
            _require_text(self.unsupported_reason, "unsupported_reason")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "payment_key": self.payment_key,
            "action_id": self.action_id,
            "cost_key": self.cost_key,
            "status": self.status,
            "paid_resource_keys": list(self.paid_resource_keys),
            "failed_reason": self.failed_reason,
            "unsupported_reason": self.unsupported_reason,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationPaymentRecord":
        _require_mapping(value, "payment record")
        return cls(
            payment_key=value.get("payment_key"),
            action_id=value.get("action_id"),
            cost_key=value.get("cost_key"),
            status=value.get("status"),
            paid_resource_keys=tuple(value.get("paid_resource_keys", ())),
            failed_reason=value.get("failed_reason"),
            unsupported_reason=value.get("unsupported_reason"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class SimulationResourceLedger:
    ledger_id: str
    simulation_id: str
    pre_state_id: str
    post_state_id: str
    entries: tuple[SimulationResourceLedgerEntry, ...]
    payments: tuple[SimulationPaymentRecord, ...] = ()
    ledger_version: str = SIM_R_LEDGER_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.ledger_id, "ledger_id")
        _require_text(self.simulation_id, "simulation_id")
        _require_text(self.pre_state_id, "pre_state_id")
        _require_text(self.post_state_id, "post_state_id")
        _require_text(self.ledger_version, "ledger_version")
        if self.ledger_version != SIM_R_LEDGER_VERSION:
            raise SimulationLedgerBuildError("unsupported SIM-R ledger_version")
        entries = tuple(self.entries)
        payments = tuple(self.payments)
        for entry in entries:
            if not isinstance(entry, SimulationResourceLedgerEntry):
                raise SimulationLedgerBuildError("entries must be SimulationResourceLedgerEntry values")
        for payment in payments:
            if not isinstance(payment, SimulationPaymentRecord):
                raise SimulationLedgerBuildError("payments must be SimulationPaymentRecord values")
        object.__setattr__(self, "entries", entries)
        object.__setattr__(self, "payments", payments)
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_resource_ledger(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ledger_id": self.ledger_id,
            "ledger_version": self.ledger_version,
            "simulation_id": self.simulation_id,
            "pre_state_id": self.pre_state_id,
            "post_state_id": self.post_state_id,
            "entries": [entry.to_dict() for entry in self.entries],
            "payments": [payment.to_dict() for payment in self.payments],
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "SimulationResourceLedger":
        _require_mapping(value, "resource ledger")
        return cls(
            ledger_id=value.get("ledger_id"),
            ledger_version=value.get("ledger_version", SIM_R_LEDGER_VERSION),
            simulation_id=value.get("simulation_id"),
            pre_state_id=value.get("pre_state_id"),
            post_state_id=value.get("post_state_id"),
            entries=tuple(SimulationResourceLedgerEntry.from_mapping(item) for item in value.get("entries", ())),
            payments=tuple(SimulationPaymentRecord.from_mapping(item) for item in value.get("payments", ())),
            metadata=value.get("metadata", {}),
        )


def build_resource_ledger(value: Mapping[str, Any]) -> SimulationResourceLedger:
    return SimulationResourceLedger.from_mapping(value)


def resource_ledger_to_dict(ledger: SimulationResourceLedger) -> dict[str, Any]:
    if not isinstance(ledger, SimulationResourceLedger):
        raise SimulationLedgerBuildError("ledger must be a SimulationResourceLedger")
    return ledger.to_dict()


def validate_resource_ledger(ledger: SimulationResourceLedger) -> None:
    if not isinstance(ledger, SimulationResourceLedger):
        raise SimulationLedgerBuildError("ledger must be a SimulationResourceLedger")
    entry_ids: set[str] = set()
    consumed_resource_keys: set[str] = set()
    payment_keys: set[str] = set()

    for entry in ledger.entries:
        if entry.ledger_entry_id in entry_ids:
            raise SimulationLedgerBuildError("ledger_entry_id values must be unique")
        entry_ids.add(entry.ledger_entry_id)
        if entry.status == "consumed" and entry.resource_key in consumed_resource_keys and not entry.reusable:
            raise SimulationLedgerBuildError("resource_key cannot be consumed more than once without reusable metadata")
        if entry.status == "consumed" and not entry.reusable:
            consumed_resource_keys.add(entry.resource_key)

    for payment in ledger.payments:
        if payment.payment_key in payment_keys:
            raise SimulationLedgerBuildError("payment_key values must be unique")
        payment_keys.add(payment.payment_key)


def _require_mapping(value: Any, label: str) -> None:
    if not isinstance(value, Mapping):
        raise SimulationLedgerBuildError(f"{label} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SimulationLedgerBuildError(f"{field_name} is required")


def _require_non_negative_number(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SimulationLedgerBuildError(f"{field_name} must be a number")
    if value < 0:
        raise SimulationLedgerBuildError(f"{field_name} cannot be negative")


def _string_tuple(values: Any, field_name: str) -> tuple[str, ...]:
    if isinstance(values, str) or not isinstance(values, (tuple, list)):
        raise SimulationLedgerBuildError(f"{field_name} must be a list or tuple")
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
    raise SimulationLedgerBuildError("ledger metadata must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _thaw_json(item) for key, item in sorted(value.items(), key=lambda row: str(row[0]))}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    if isinstance(value, list):
        return [_thaw_json(item) for item in value]
    return value
