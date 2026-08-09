"""Pure, deterministic Goal Engine project-state reconciliation.

This module accepts immutable caller-supplied observations.  It performs no
I/O, discovery, mutation, permission calculation, work selection, or state
transition.  Freshness is always classified against an explicit caller time.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, TypeAlias

from .foundation import (
    GoalCapability,
    GoalEngineFoundationError,
    GoalEvidenceReference,
    GoalIdentifier,
    GoalPolicyReference,
    GoalPolicyRegistry,
    GoalSafeMode,
    goal_capability_from_dict,
    goal_capability_to_dict,
    goal_evidence_reference_from_dict,
    goal_evidence_reference_to_dict,
    goal_identifier_from_dict,
    goal_identifier_to_dict,
    goal_policy_record_semantic_hash,
    goal_policy_reference_from_dict,
    goal_policy_reference_to_dict,
    goal_safe_mode_from_dict,
    goal_safe_mode_to_dict,
    lookup_goal_policy,
    semantic_hash,
    validate_goal_lifecycle_state,
    validate_risk,
)


STATE_PROVENANCE_SCHEMA_VERSION = "codie.goal_engine.state_provenance.v1"
PROJECT_STATE_SCHEMA_VERSION = "codie.goal_engine.project_state.v1"
AUTHORITY_STATE_SCHEMA_VERSION = "codie.goal_engine.authority_state.v1"
GOAL_STATE_SCHEMA_VERSION = "codie.goal_engine.goal_state.v1"
BUILD_STATE_SCHEMA_VERSION = "codie.goal_engine.build_state.v1"
RESOURCE_STATE_SCHEMA_VERSION = "codie.goal_engine.resource_state.v1"
INCIDENT_STATE_SCHEMA_VERSION = "codie.goal_engine.incident_state.v1"
HUMAN_ATTENTION_STATE_SCHEMA_VERSION = "codie.goal_engine.human_attention_state.v1"
STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.state_snapshot_reference.v1"
)
PROJECT_STATE_SNAPSHOT_SCHEMA_VERSION = (
    "codie.goal_engine.project_state_snapshot.v1"
)
STATE_CONFLICT_SCHEMA_VERSION = "codie.goal_engine.state_conflict.v1"
STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION = (
    "codie.goal_engine.state_conflict_resolution.v1"
)
STATE_RECONCILIATION_ENTRY_SCHEMA_VERSION = (
    "codie.goal_engine.state_reconciliation_entry.v1"
)
STATE_RECONCILIATION_RESULT_SCHEMA_VERSION = (
    "codie.goal_engine.state_reconciliation_result.v1"
)

STATE_DOMAINS = frozenset(
    {"PROJECT", "AUTHORITY", "GOAL", "BUILD", "RESOURCE", "INCIDENT", "HUMAN_ATTENTION"}
)
STATE_FRESHNESS_VALUES = frozenset({"CURRENT", "STALE", "UNKNOWN"})
STATE_AVAILABILITY_VALUES = frozenset({"AVAILABLE", "UNAVAILABLE", "UNKNOWN"})
RECONCILIATION_STATUS_VALUES = frozenset(
    {"CONSISTENT", "CONFLICTED", "RESOLVED_CONFLICT", "INCOMPLETE", "UNAVAILABLE"}
)
PROJECT_STATE_VALUES = frozenset(
    {"ACTIVE", "WAITING_FOR_HUMAN", "PAUSED", "BLOCKED", "VALIDATING", "CLOSED", "UNKNOWN"}
)
AUTHORITY_STAGE_VALUES = frozenset(
    {
        "DOCUMENTATION_ONLY",
        "STAGE_0_SHADOW",
        "STAGE_1_WORK_ORDER",
        "STAGE_2_SAFE_EXPERIMENT",
        "STAGE_3_BUILD_GRAPH_SUBMISSION",
    }
)
BUILD_STATE_VALUES = frozenset(
    {"NOT_STARTED", "IN_PROGRESS", "PAUSED", "BLOCKED", "VALIDATING", "COMPLETE", "FAILED", "UNKNOWN"}
)
RESOURCE_STATE_VALUES = frozenset({"AVAILABLE", "CONSTRAINED", "UNAVAILABLE", "UNKNOWN"})
INCIDENT_STATE_VALUES = frozenset(
    {"OPEN", "CONTAINED", "WAITING_FOR_HUMAN", "RESOLVED", "CLOSED_WITH_LIMITATION"}
)
HUMAN_ATTENTION_STATE_VALUES = frozenset(
    {"REQUESTED", "WAITING", "RESPONDED", "WITHDRAWN", "SUPERSEDED"}
)
CONFLICT_RESOLUTION_KINDS = frozenset({"HUMAN_DECISION", "ACCEPTED_POLICY"})

_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_FIELD_NAMES = frozenset(
    {
        "api_key",
        "cookie",
        "credential",
        "credentials",
        "model_prompt",
        "password",
        "private_deck_text",
        "prompt",
        "prompt_log",
        "provider_payload",
        "raw_payload",
        "secret",
        "session",
        "session_id",
        "token",
    }
)


class GoalEngineStateError(ValueError):
    """Raised when caller-supplied Goal Engine state fails closed."""


@dataclass(frozen=True)
class StateProvenance:
    provenance_id: str
    observed_at: str
    fresh_until: str | None
    availability: str
    evidence_ref_ids: tuple[str, ...]
    human_decision_ref_ids: tuple[str, ...]
    authority_ref_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.provenance_id, "provenance_id")
        observed = _parse_utc_timestamp(self.observed_at, "observed_at")
        if self.fresh_until is not None:
            fresh_until = _parse_utc_timestamp(self.fresh_until, "fresh_until")
            if fresh_until < observed:
                raise GoalEngineStateError("fresh_until cannot precede observed_at")
        validate_state_availability(self.availability)
        for field_name in (
            "evidence_ref_ids",
            "human_decision_ref_ids",
            "authority_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        _require_disjoint_reference_sets(
            self.evidence_ref_ids,
            self.human_decision_ref_ids,
            self.authority_ref_ids,
        )
        _require_schema(self.schema_version, STATE_PROVENANCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ProjectState:
    project_id: str
    state_revision: int
    project_state: str
    active_phase_id: str
    active_phase_part: str
    gate_scope: str
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.project_id, "project_id")
        _require_positive_int(self.state_revision, "state_revision")
        validate_project_state(self.project_state)
        _require_label(self.active_phase_id, "active_phase_id")
        _require_label(self.active_phase_part, "active_phase_part")
        _require_label(self.gate_scope, "gate_scope")
        _require_type(self.provenance, StateProvenance, "provenance")
        _require_schema(self.schema_version, PROJECT_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class AuthorityState:
    authority_state_id: str
    state_revision: int
    authority_stage: str
    capability: GoalCapability | None
    safe_mode: GoalSafeMode
    promotion_ref_ids: tuple[str, ...]
    downgrade_ref_ids: tuple[str, ...]
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.authority_state_id, "authority_state_id")
        _require_positive_int(self.state_revision, "state_revision")
        validate_authority_stage(self.authority_stage)
        if self.capability is not None:
            _require_type(self.capability, GoalCapability, "capability")
        _require_type(self.safe_mode, GoalSafeMode, "safe_mode")
        for field_name in ("promotion_ref_ids", "downgrade_ref_ids"):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        _require_type(self.provenance, StateProvenance, "provenance")
        _validate_authority_representation(self)
        _require_schema(self.schema_version, AUTHORITY_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalState:
    goal_state_id: str
    state_revision: int
    goal_identifier: GoalIdentifier
    goal_contract_id: str
    goal_contract_revision: int
    lifecycle_state: str
    blocked_by_ids: tuple[str, ...]
    human_attention_request_ids: tuple[str, ...]
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.goal_state_id, "goal_state_id")
        _require_positive_int(self.state_revision, "state_revision")
        _require_type(self.goal_identifier, GoalIdentifier, "goal_identifier")
        _require_id(self.goal_contract_id, "goal_contract_id")
        _require_positive_int(self.goal_contract_revision, "goal_contract_revision")
        _foundation_validate(validate_goal_lifecycle_state, self.lifecycle_state)
        for field_name in ("blocked_by_ids", "human_attention_request_ids"):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        if self.lifecycle_state == "WAITING_FOR_HUMAN" and not self.human_attention_request_ids:
            raise GoalEngineStateError(
                "WAITING_FOR_HUMAN requires a human-attention request reference"
            )
        _require_type(self.provenance, StateProvenance, "provenance")
        _require_schema(self.schema_version, GOAL_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class BuildState:
    build_id: str
    state_revision: int
    goal_identifier: GoalIdentifier | None
    goal_contract_id: str | None
    goal_contract_revision: int | None
    phase_id: str
    phase_part: str
    build_state: str
    artifact_ref_ids: tuple[str, ...]
    validation_ref_ids: tuple[str, ...]
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.build_id, "build_id")
        _require_positive_int(self.state_revision, "state_revision")
        if self.goal_identifier is not None:
            _require_type(self.goal_identifier, GoalIdentifier, "goal_identifier")
        contract_fields_present = self.goal_contract_id is not None or self.goal_contract_revision is not None
        if contract_fields_present:
            if self.goal_contract_id is None or self.goal_contract_revision is None:
                raise GoalEngineStateError(
                    "goal_contract_id and goal_contract_revision must be present together"
                )
            _require_id(self.goal_contract_id, "goal_contract_id")
            _require_positive_int(self.goal_contract_revision, "goal_contract_revision")
        if self.goal_identifier is not None and not contract_fields_present:
            raise GoalEngineStateError(
                "an attached goal_identifier requires Goal Contract identity and revision"
            )
        _require_label(self.phase_id, "phase_id")
        _require_label(self.phase_part, "phase_part")
        validate_build_state(self.build_state)
        for field_name in ("artifact_ref_ids", "validation_ref_ids"):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        overlap = sorted(set(self.artifact_ref_ids) & set(self.validation_ref_ids))
        if overlap:
            raise GoalEngineStateError(
                "artifact and validation references must remain separate"
            )
        _require_type(self.provenance, StateProvenance, "provenance")
        _require_schema(self.schema_version, BUILD_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ResourceState:
    resource_id: str
    state_revision: int
    resource_kind: str
    resource_state: str
    constraint_summary: str
    temporary: bool
    cleanup_required: bool
    cleanup_ref_ids: tuple[str, ...]
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.resource_id, "resource_id")
        _require_positive_int(self.state_revision, "state_revision")
        _require_label(self.resource_kind, "resource_kind")
        validate_resource_state(self.resource_state)
        _require_text(self.constraint_summary, "constraint_summary")
        _require_bool(self.temporary, "temporary")
        _require_bool(self.cleanup_required, "cleanup_required")
        object.__setattr__(
            self,
            "cleanup_ref_ids",
            _id_tuple(self.cleanup_ref_ids, "cleanup_ref_ids", sort=True),
        )
        if self.cleanup_ref_ids and self.cleanup_required:
            raise GoalEngineStateError(
                "cleanup references require cleanup_required to be false"
            )
        if self.temporary and not self.cleanup_required and not self.cleanup_ref_ids:
            raise GoalEngineStateError(
                "a temporary resource requires cleanup evidence or cleanup_required"
            )
        _require_type(self.provenance, StateProvenance, "provenance")
        _require_schema(self.schema_version, RESOURCE_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class IncidentState:
    incident_id: str
    state_revision: int
    incident_state: str
    risk: str
    opened_at: str
    contained_at: str | None
    closed_at: str | None
    affected_system_ids: tuple[str, ...]
    safe_mode: GoalSafeMode
    human_attention_request_ids: tuple[str, ...]
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.incident_id, "incident_id")
        _require_positive_int(self.state_revision, "state_revision")
        validate_incident_state(self.incident_state)
        _foundation_validate(validate_risk, self.risk)
        opened = _parse_utc_timestamp(self.opened_at, "opened_at")
        contained = (
            _parse_utc_timestamp(self.contained_at, "contained_at")
            if self.contained_at is not None
            else None
        )
        closed = (
            _parse_utc_timestamp(self.closed_at, "closed_at")
            if self.closed_at is not None
            else None
        )
        if contained is not None and contained < opened:
            raise GoalEngineStateError("contained_at cannot precede opened_at")
        if closed is not None and closed < opened:
            raise GoalEngineStateError("closed_at cannot precede opened_at")
        if contained is not None and closed is not None and closed < contained:
            raise GoalEngineStateError("closed_at cannot precede contained_at")
        if self.incident_state == "CONTAINED" and contained is None:
            raise GoalEngineStateError("CONTAINED requires contained_at")
        if self.incident_state in {"RESOLVED", "CLOSED_WITH_LIMITATION"} and closed is None:
            raise GoalEngineStateError(f"{self.incident_state} requires closed_at")
        object.__setattr__(
            self,
            "affected_system_ids",
            _id_tuple(self.affected_system_ids, "affected_system_ids", sort=True),
        )
        _require_type(self.safe_mode, GoalSafeMode, "safe_mode")
        object.__setattr__(
            self,
            "human_attention_request_ids",
            _id_tuple(
                self.human_attention_request_ids,
                "human_attention_request_ids",
                sort=True,
            ),
        )
        if self.risk == "Critical" and not self.human_attention_request_ids:
            raise GoalEngineStateError(
                "Critical incidents require a human-attention request reference"
            )
        _require_type(self.provenance, StateProvenance, "provenance")
        _require_schema(self.schema_version, INCIDENT_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class HumanAttentionState:
    request_id: str
    state_revision: int
    attention_state: str
    decision_question: str
    requested_at: str
    responded_at: str | None
    response_ref_ids: tuple[str, ...]
    blocking_goal_ids: tuple[str, ...]
    blocking_build_ids: tuple[str, ...]
    provenance: StateProvenance
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.request_id, "request_id")
        _require_positive_int(self.state_revision, "state_revision")
        validate_human_attention_state(self.attention_state)
        _require_text(self.decision_question, "decision_question")
        requested = _parse_utc_timestamp(self.requested_at, "requested_at")
        responded = (
            _parse_utc_timestamp(self.responded_at, "responded_at")
            if self.responded_at is not None
            else None
        )
        if responded is not None and responded < requested:
            raise GoalEngineStateError("responded_at cannot precede requested_at")
        for field_name in (
            "response_ref_ids",
            "blocking_goal_ids",
            "blocking_build_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        if self.attention_state == "RESPONDED":
            if responded is None or not self.response_ref_ids:
                raise GoalEngineStateError(
                    "RESPONDED requires responded_at and a response reference"
                )
        elif responded is not None or self.response_ref_ids:
            raise GoalEngineStateError(
                "non-responded attention state cannot carry response data"
            )
        _require_type(self.provenance, StateProvenance, "provenance")
        _require_schema(self.schema_version, HUMAN_ATTENTION_STATE_SCHEMA_VERSION)


@dataclass(frozen=True)
class StateSnapshotReference:
    snapshot_id: str
    revision: int
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.snapshot_id, "snapshot_id")
        _require_positive_int(self.revision, "revision")
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(self.schema_version, STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class ProjectStateSnapshot:
    snapshot_id: str
    revision: int
    supersedes_snapshot: StateSnapshotReference | None
    captured_at: str
    project_state: ProjectState
    authority_state: AuthorityState
    goal_states: tuple[GoalState, ...]
    build_states: tuple[BuildState, ...]
    resource_states: tuple[ResourceState, ...]
    incident_states: tuple[IncidentState, ...]
    human_attention_states: tuple[HumanAttentionState, ...]
    evidence_snapshot: tuple[GoalEvidenceReference, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.snapshot_id, "snapshot_id")
        _require_positive_int(self.revision, "revision")
        if self.revision == 1:
            if self.supersedes_snapshot is not None:
                raise GoalEngineStateError(
                    "snapshot revision 1 cannot supersede an earlier snapshot"
                )
        else:
            _require_type(
                self.supersedes_snapshot,
                StateSnapshotReference,
                "supersedes_snapshot",
            )
            if self.supersedes_snapshot.snapshot_id != self.snapshot_id:
                raise GoalEngineStateError(
                    "superseded snapshot must use the same snapshot_id"
                )
            if self.supersedes_snapshot.revision != self.revision - 1:
                raise GoalEngineStateError(
                    "superseded snapshot must be the immediately prior revision"
                )
        _parse_utc_timestamp(self.captured_at, "captured_at")
        _require_type(self.project_state, ProjectState, "project_state")
        _require_type(self.authority_state, AuthorityState, "authority_state")
        for field_name, expected_type, key in (
            ("goal_states", GoalState, lambda item: item.goal_state_id),
            ("build_states", BuildState, lambda item: item.build_id),
            ("resource_states", ResourceState, lambda item: item.resource_id),
            ("incident_states", IncidentState, lambda item: item.incident_id),
            ("human_attention_states", HumanAttentionState, lambda item: item.request_id),
        ):
            values = _typed_tuple(getattr(self, field_name), expected_type, field_name)
            object.__setattr__(self, field_name, tuple(sorted(values, key=key)))
        evidence = _typed_tuple(
            self.evidence_snapshot,
            GoalEvidenceReference,
            "evidence_snapshot",
        )
        object.__setattr__(
            self,
            "evidence_snapshot",
            tuple(sorted(evidence, key=lambda item: item.evidence_ref_id)),
        )
        _require_schema(self.schema_version, PROJECT_STATE_SNAPSHOT_SCHEMA_VERSION)
        validate_project_state_snapshot(self)


@dataclass(frozen=True)
class StateConflict:
    conflict_id: str
    domain: str
    subject_id: str
    candidate_record_ids: tuple[str, ...]
    candidate_semantic_hashes: tuple[str, ...]
    detected_at: str
    evidence_ref_ids: tuple[str, ...]
    human_decision_ref_ids: tuple[str, ...]
    authority_ref_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.conflict_id, "conflict_id")
        validate_state_domain(self.domain)
        _require_id(self.subject_id, "subject_id")
        ids, hashes = _candidate_pairs(
            self.candidate_record_ids,
            self.candidate_semantic_hashes,
            require_distinct_hashes=True,
        )
        object.__setattr__(self, "candidate_record_ids", ids)
        object.__setattr__(self, "candidate_semantic_hashes", hashes)
        _parse_utc_timestamp(self.detected_at, "detected_at")
        for field_name in (
            "evidence_ref_ids",
            "human_decision_ref_ids",
            "authority_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        _require_disjoint_reference_sets(
            self.evidence_ref_ids,
            self.human_decision_ref_ids,
            self.authority_ref_ids,
        )
        expected_id = state_conflict_id(
            self.domain,
            self.subject_id,
            self.candidate_semantic_hashes,
        )
        if self.conflict_id != expected_id:
            raise GoalEngineStateError("conflict_id does not match conflict semantics")
        _require_schema(self.schema_version, STATE_CONFLICT_SCHEMA_VERSION)


@dataclass(frozen=True)
class StateConflictResolution:
    resolution_id: str
    conflict_id: str
    selected_record_id: str
    resolution_kind: str
    resolved_at: str
    human_decision_ref_ids: tuple[str, ...]
    policy_refs: tuple[GoalPolicyReference, ...]
    authority_ref_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.resolution_id, "resolution_id")
        _require_id(self.conflict_id, "conflict_id")
        _require_id(self.selected_record_id, "selected_record_id")
        _require_allowed(
            self.resolution_kind,
            CONFLICT_RESOLUTION_KINDS,
            "resolution_kind",
        )
        _parse_utc_timestamp(self.resolved_at, "resolved_at")
        object.__setattr__(
            self,
            "human_decision_ref_ids",
            _id_tuple(
                self.human_decision_ref_ids,
                "human_decision_ref_ids",
                sort=True,
            ),
        )
        policies = _typed_tuple(self.policy_refs, GoalPolicyReference, "policy_refs")
        policies = tuple(
            sorted(
                policies,
                key=lambda item: (item.policy_id, item.policy_version, item.semantic_hash),
            )
        )
        if _duplicates([(item.policy_id, item.policy_version) for item in policies]):
            raise GoalEngineStateError("policy_refs contains a duplicate policy version")
        object.__setattr__(self, "policy_refs", policies)
        object.__setattr__(
            self,
            "authority_ref_ids",
            _id_tuple(self.authority_ref_ids, "authority_ref_ids", sort=True),
        )
        if set(self.human_decision_ref_ids) & set(self.authority_ref_ids):
            raise GoalEngineStateError(
                "human-decision and authority references must remain separate"
            )
        if not self.authority_ref_ids:
            raise GoalEngineStateError(
                "conflict resolution requires an authority reference"
            )
        if self.resolution_kind == "HUMAN_DECISION":
            if not self.human_decision_ref_ids or self.policy_refs:
                raise GoalEngineStateError(
                    "HUMAN_DECISION requires human-decision refs and no policy refs"
                )
        elif self.human_decision_ref_ids or not self.policy_refs:
            raise GoalEngineStateError(
                "ACCEPTED_POLICY requires policy refs and no human-decision refs"
            )
        _require_schema(
            self.schema_version,
            STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class StateReconciliationEntry:
    domain: str
    subject_id: str
    reconciliation_status: str
    candidate_record_ids: tuple[str, ...]
    candidate_semantic_hashes: tuple[str, ...]
    current_record_ids: tuple[str, ...]
    stale_record_ids: tuple[str, ...]
    unavailable_record_ids: tuple[str, ...]
    unknown_freshness_record_ids: tuple[str, ...]
    unknown_availability_record_ids: tuple[str, ...]
    conflict_id: str | None
    resolution_id: str | None
    schema_version: str

    def __post_init__(self) -> None:
        validate_state_domain(self.domain)
        _require_id(self.subject_id, "subject_id")
        validate_reconciliation_status(self.reconciliation_status)
        ids, hashes = _candidate_pairs(
            self.candidate_record_ids,
            self.candidate_semantic_hashes,
            require_distinct_hashes=False,
        )
        object.__setattr__(self, "candidate_record_ids", ids)
        object.__setattr__(self, "candidate_semantic_hashes", hashes)
        for field_name in (
            "current_record_ids",
            "stale_record_ids",
            "unavailable_record_ids",
            "unknown_freshness_record_ids",
            "unknown_availability_record_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        candidates = set(self.candidate_record_ids)
        freshness_sets = (
            set(self.current_record_ids),
            set(self.stale_record_ids),
            set(self.unknown_freshness_record_ids),
        )
        if any(left & right for index, left in enumerate(freshness_sets) for right in freshness_sets[index + 1 :]):
            raise GoalEngineStateError("freshness buckets must remain disjoint")
        if set().union(*freshness_sets) != candidates:
            raise GoalEngineStateError("freshness buckets must partition candidates")
        unavailable = set(self.unavailable_record_ids)
        unknown_availability = set(self.unknown_availability_record_ids)
        if unavailable & unknown_availability:
            raise GoalEngineStateError("availability overlays must remain disjoint")
        if not unavailable <= candidates or not unknown_availability <= candidates:
            raise GoalEngineStateError("availability overlays must reference candidates")
        if self.conflict_id is not None:
            _require_id(self.conflict_id, "conflict_id")
        if self.resolution_id is not None:
            _require_id(self.resolution_id, "resolution_id")
        if self.reconciliation_status == "CONFLICTED":
            if self.conflict_id is None or self.resolution_id is not None:
                raise GoalEngineStateError(
                    "CONFLICTED requires conflict_id and no resolution_id"
                )
        elif self.reconciliation_status == "RESOLVED_CONFLICT":
            if self.conflict_id is None or self.resolution_id is None:
                raise GoalEngineStateError(
                    "RESOLVED_CONFLICT requires conflict_id and resolution_id"
                )
        elif self.conflict_id is not None or self.resolution_id is not None:
            raise GoalEngineStateError(
                "non-conflict status cannot carry conflict or resolution IDs"
            )
        available_ids = candidates - unavailable - unknown_availability
        usable_current_ids = set(self.current_record_ids) & available_ids
        usable_current_hashes = {
            digest
            for record_id, digest in zip(
                self.candidate_record_ids,
                self.candidate_semantic_hashes,
                strict=True,
            )
            if record_id in usable_current_ids
        }
        if len(usable_current_hashes) > 1:
            if self.reconciliation_status not in {"CONFLICTED", "RESOLVED_CONFLICT"}:
                raise GoalEngineStateError(
                    "distinct usable current semantics require a conflict status"
                )
        elif usable_current_ids:
            if self.reconciliation_status != "CONSISTENT":
                raise GoalEngineStateError(
                    "one exact usable current semantic state must be CONSISTENT"
                )
        elif available_ids:
            if self.reconciliation_status != "INCOMPLETE":
                raise GoalEngineStateError(
                    "available historical or unknown-freshness state must be INCOMPLETE"
                )
        elif unavailable:
            if self.reconciliation_status != "UNAVAILABLE":
                raise GoalEngineStateError(
                    "explicit unavailability without a usable observation must be UNAVAILABLE"
                )
        elif self.reconciliation_status != "INCOMPLETE":
            raise GoalEngineStateError(
                "unknown availability without a usable observation must be INCOMPLETE"
            )
        _require_schema(
            self.schema_version,
            STATE_RECONCILIATION_ENTRY_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class StateReconciliationResult:
    reconciliation_id: str
    as_of: str
    input_snapshot_refs: tuple[StateSnapshotReference, ...]
    entries: tuple[StateReconciliationEntry, ...]
    conflicts: tuple[StateConflict, ...]
    resolutions: tuple[StateConflictResolution, ...]
    aggregate_status: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.reconciliation_id, "reconciliation_id")
        _parse_utc_timestamp(self.as_of, "as_of")
        refs = _typed_tuple(
            self.input_snapshot_refs,
            StateSnapshotReference,
            "input_snapshot_refs",
        )
        entries = _typed_tuple(self.entries, StateReconciliationEntry, "entries")
        conflicts = _typed_tuple(self.conflicts, StateConflict, "conflicts")
        resolutions = _typed_tuple(
            self.resolutions,
            StateConflictResolution,
            "resolutions",
        )
        object.__setattr__(
            self,
            "input_snapshot_refs",
            tuple(sorted(refs, key=lambda item: (item.snapshot_id, item.revision))),
        )
        object.__setattr__(
            self,
            "entries",
            tuple(sorted(entries, key=lambda item: (item.domain, item.subject_id))),
        )
        object.__setattr__(
            self,
            "conflicts",
            tuple(sorted(conflicts, key=lambda item: item.conflict_id)),
        )
        object.__setattr__(
            self,
            "resolutions",
            tuple(sorted(resolutions, key=lambda item: item.resolution_id)),
        )
        validate_reconciliation_status(self.aggregate_status)
        _require_schema(
            self.schema_version,
            STATE_RECONCILIATION_RESULT_SCHEMA_VERSION,
        )
        _validate_reconciliation_result(self)


StateRecord: TypeAlias = (
    ProjectState
    | AuthorityState
    | GoalState
    | BuildState
    | ResourceState
    | IncidentState
    | HumanAttentionState
)


def validate_state_domain(value: str) -> str:
    return _require_allowed(value, STATE_DOMAINS, "state_domain")


def validate_state_freshness(value: str) -> str:
    return _require_allowed(value, STATE_FRESHNESS_VALUES, "state_freshness")


def validate_state_availability(value: str) -> str:
    return _require_allowed(value, STATE_AVAILABILITY_VALUES, "state_availability")


def validate_reconciliation_status(value: str) -> str:
    return _require_allowed(
        value,
        RECONCILIATION_STATUS_VALUES,
        "reconciliation_status",
    )


def validate_project_state(value: str) -> str:
    return _require_allowed(value, PROJECT_STATE_VALUES, "project_state")


def validate_authority_stage(value: str) -> str:
    return _require_allowed(value, AUTHORITY_STAGE_VALUES, "authority_stage")


def validate_build_state(value: str) -> str:
    return _require_allowed(value, BUILD_STATE_VALUES, "build_state")


def validate_resource_state(value: str) -> str:
    return _require_allowed(value, RESOURCE_STATE_VALUES, "resource_state")


def validate_incident_state(value: str) -> str:
    return _require_allowed(value, INCIDENT_STATE_VALUES, "incident_state")


def validate_human_attention_state(value: str) -> str:
    return _require_allowed(
        value,
        HUMAN_ATTENTION_STATE_VALUES,
        "human_attention_state",
    )


def classify_state_freshness(provenance: StateProvenance, as_of: str) -> str:
    _require_type(provenance, StateProvenance, "provenance")
    as_of_time = _parse_utc_timestamp(as_of, "as_of")
    observed = _parse_utc_timestamp(provenance.observed_at, "observed_at")
    if as_of_time < observed:
        raise GoalEngineStateError("as_of cannot precede observed_at")
    if provenance.fresh_until is None:
        return "UNKNOWN"
    fresh_until = _parse_utc_timestamp(provenance.fresh_until, "fresh_until")
    return "CURRENT" if as_of_time <= fresh_until else "STALE"


def state_provenance_to_dict(value: StateProvenance) -> dict[str, Any]:
    _require_type(value, StateProvenance, "value")
    return {
        "provenance_id": value.provenance_id,
        "observed_at": value.observed_at,
        "fresh_until": value.fresh_until,
        "availability": value.availability,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "human_decision_ref_ids": list(value.human_decision_ref_ids),
        "authority_ref_ids": list(value.authority_ref_ids),
        "schema_version": value.schema_version,
    }


def state_provenance_from_dict(payload: Mapping[str, Any]) -> StateProvenance:
    data = _require_fields(
        payload,
        {
            "provenance_id",
            "observed_at",
            "fresh_until",
            "availability",
            "evidence_ref_ids",
            "human_decision_ref_ids",
            "authority_ref_ids",
            "schema_version",
        },
    )
    for field_name in (
        "evidence_ref_ids",
        "human_decision_ref_ids",
        "authority_ref_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return StateProvenance(**data)


def project_state_to_dict(value: ProjectState) -> dict[str, Any]:
    _require_type(value, ProjectState, "value")
    return {
        "project_id": value.project_id,
        "state_revision": value.state_revision,
        "project_state": value.project_state,
        "active_phase_id": value.active_phase_id,
        "active_phase_part": value.active_phase_part,
        "gate_scope": value.gate_scope,
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def project_state_from_dict(payload: Mapping[str, Any]) -> ProjectState:
    data = _require_fields(
        payload,
        {
            "project_id",
            "state_revision",
            "project_state",
            "active_phase_id",
            "active_phase_part",
            "gate_scope",
            "provenance",
            "schema_version",
        },
    )
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return ProjectState(**data)


def authority_state_to_dict(value: AuthorityState) -> dict[str, Any]:
    _require_type(value, AuthorityState, "value")
    return {
        "authority_state_id": value.authority_state_id,
        "state_revision": value.state_revision,
        "authority_stage": value.authority_stage,
        "capability": (
            goal_capability_to_dict(value.capability)
            if value.capability is not None
            else None
        ),
        "safe_mode": goal_safe_mode_to_dict(value.safe_mode),
        "promotion_ref_ids": list(value.promotion_ref_ids),
        "downgrade_ref_ids": list(value.downgrade_ref_ids),
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def authority_state_from_dict(payload: Mapping[str, Any]) -> AuthorityState:
    data = _require_fields(
        payload,
        {
            "authority_state_id",
            "state_revision",
            "authority_stage",
            "capability",
            "safe_mode",
            "promotion_ref_ids",
            "downgrade_ref_ids",
            "provenance",
            "schema_version",
        },
    )
    if data["capability"] is not None:
        data["capability"] = _foundation_parse(
            goal_capability_from_dict,
            _require_mapping(data["capability"], "capability"),
        )
    data["safe_mode"] = _foundation_parse(
        goal_safe_mode_from_dict,
        _require_mapping(data["safe_mode"], "safe_mode"),
    )
    for field_name in ("promotion_ref_ids", "downgrade_ref_ids"):
        data[field_name] = _json_tuple(data[field_name], field_name)
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return AuthorityState(**data)


def goal_state_to_dict(value: GoalState) -> dict[str, Any]:
    _require_type(value, GoalState, "value")
    return {
        "goal_state_id": value.goal_state_id,
        "state_revision": value.state_revision,
        "goal_identifier": goal_identifier_to_dict(value.goal_identifier),
        "goal_contract_id": value.goal_contract_id,
        "goal_contract_revision": value.goal_contract_revision,
        "lifecycle_state": value.lifecycle_state,
        "blocked_by_ids": list(value.blocked_by_ids),
        "human_attention_request_ids": list(value.human_attention_request_ids),
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def goal_state_from_dict(payload: Mapping[str, Any]) -> GoalState:
    data = _require_fields(
        payload,
        {
            "goal_state_id",
            "state_revision",
            "goal_identifier",
            "goal_contract_id",
            "goal_contract_revision",
            "lifecycle_state",
            "blocked_by_ids",
            "human_attention_request_ids",
            "provenance",
            "schema_version",
        },
    )
    data["goal_identifier"] = _foundation_parse(
        goal_identifier_from_dict,
        _require_mapping(data["goal_identifier"], "goal_identifier"),
    )
    for field_name in ("blocked_by_ids", "human_attention_request_ids"):
        data[field_name] = _json_tuple(data[field_name], field_name)
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return GoalState(**data)


def build_state_to_dict(value: BuildState) -> dict[str, Any]:
    _require_type(value, BuildState, "value")
    return {
        "build_id": value.build_id,
        "state_revision": value.state_revision,
        "goal_identifier": (
            goal_identifier_to_dict(value.goal_identifier)
            if value.goal_identifier is not None
            else None
        ),
        "goal_contract_id": value.goal_contract_id,
        "goal_contract_revision": value.goal_contract_revision,
        "phase_id": value.phase_id,
        "phase_part": value.phase_part,
        "build_state": value.build_state,
        "artifact_ref_ids": list(value.artifact_ref_ids),
        "validation_ref_ids": list(value.validation_ref_ids),
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def build_state_from_dict(payload: Mapping[str, Any]) -> BuildState:
    data = _require_fields(
        payload,
        {
            "build_id",
            "state_revision",
            "goal_identifier",
            "goal_contract_id",
            "goal_contract_revision",
            "phase_id",
            "phase_part",
            "build_state",
            "artifact_ref_ids",
            "validation_ref_ids",
            "provenance",
            "schema_version",
        },
    )
    if data["goal_identifier"] is not None:
        data["goal_identifier"] = _foundation_parse(
            goal_identifier_from_dict,
            _require_mapping(data["goal_identifier"], "goal_identifier"),
        )
    for field_name in ("artifact_ref_ids", "validation_ref_ids"):
        data[field_name] = _json_tuple(data[field_name], field_name)
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return BuildState(**data)


def resource_state_to_dict(value: ResourceState) -> dict[str, Any]:
    _require_type(value, ResourceState, "value")
    return {
        "resource_id": value.resource_id,
        "state_revision": value.state_revision,
        "resource_kind": value.resource_kind,
        "resource_state": value.resource_state,
        "constraint_summary": value.constraint_summary,
        "temporary": value.temporary,
        "cleanup_required": value.cleanup_required,
        "cleanup_ref_ids": list(value.cleanup_ref_ids),
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def resource_state_from_dict(payload: Mapping[str, Any]) -> ResourceState:
    data = _require_fields(
        payload,
        {
            "resource_id",
            "state_revision",
            "resource_kind",
            "resource_state",
            "constraint_summary",
            "temporary",
            "cleanup_required",
            "cleanup_ref_ids",
            "provenance",
            "schema_version",
        },
    )
    data["cleanup_ref_ids"] = _json_tuple(data["cleanup_ref_ids"], "cleanup_ref_ids")
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return ResourceState(**data)


def incident_state_to_dict(value: IncidentState) -> dict[str, Any]:
    _require_type(value, IncidentState, "value")
    return {
        "incident_id": value.incident_id,
        "state_revision": value.state_revision,
        "incident_state": value.incident_state,
        "risk": value.risk,
        "opened_at": value.opened_at,
        "contained_at": value.contained_at,
        "closed_at": value.closed_at,
        "affected_system_ids": list(value.affected_system_ids),
        "safe_mode": goal_safe_mode_to_dict(value.safe_mode),
        "human_attention_request_ids": list(value.human_attention_request_ids),
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def incident_state_from_dict(payload: Mapping[str, Any]) -> IncidentState:
    data = _require_fields(
        payload,
        {
            "incident_id",
            "state_revision",
            "incident_state",
            "risk",
            "opened_at",
            "contained_at",
            "closed_at",
            "affected_system_ids",
            "safe_mode",
            "human_attention_request_ids",
            "provenance",
            "schema_version",
        },
    )
    for field_name in ("affected_system_ids", "human_attention_request_ids"):
        data[field_name] = _json_tuple(data[field_name], field_name)
    data["safe_mode"] = _foundation_parse(
        goal_safe_mode_from_dict,
        _require_mapping(data["safe_mode"], "safe_mode"),
    )
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return IncidentState(**data)


def human_attention_state_to_dict(value: HumanAttentionState) -> dict[str, Any]:
    _require_type(value, HumanAttentionState, "value")
    return {
        "request_id": value.request_id,
        "state_revision": value.state_revision,
        "attention_state": value.attention_state,
        "decision_question": value.decision_question,
        "requested_at": value.requested_at,
        "responded_at": value.responded_at,
        "response_ref_ids": list(value.response_ref_ids),
        "blocking_goal_ids": list(value.blocking_goal_ids),
        "blocking_build_ids": list(value.blocking_build_ids),
        "provenance": state_provenance_to_dict(value.provenance),
        "schema_version": value.schema_version,
    }


def human_attention_state_from_dict(
    payload: Mapping[str, Any],
) -> HumanAttentionState:
    data = _require_fields(
        payload,
        {
            "request_id",
            "state_revision",
            "attention_state",
            "decision_question",
            "requested_at",
            "responded_at",
            "response_ref_ids",
            "blocking_goal_ids",
            "blocking_build_ids",
            "provenance",
            "schema_version",
        },
    )
    for field_name in (
        "response_ref_ids",
        "blocking_goal_ids",
        "blocking_build_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    data["provenance"] = state_provenance_from_dict(
        _require_mapping(data["provenance"], "provenance")
    )
    return HumanAttentionState(**data)


def state_snapshot_reference_to_dict(
    value: StateSnapshotReference,
) -> dict[str, Any]:
    _require_type(value, StateSnapshotReference, "value")
    return {
        "snapshot_id": value.snapshot_id,
        "revision": value.revision,
        "semantic_hash": value.semantic_hash,
        "schema_version": value.schema_version,
    }


def state_snapshot_reference_from_dict(
    payload: Mapping[str, Any],
) -> StateSnapshotReference:
    return StateSnapshotReference(
        **_require_fields(
            payload,
            {"snapshot_id", "revision", "semantic_hash", "schema_version"},
        )
    )


def project_state_snapshot_to_dict(
    value: ProjectStateSnapshot,
) -> dict[str, Any]:
    _require_type(value, ProjectStateSnapshot, "value")
    return {
        "snapshot_id": value.snapshot_id,
        "revision": value.revision,
        "supersedes_snapshot": (
            state_snapshot_reference_to_dict(value.supersedes_snapshot)
            if value.supersedes_snapshot is not None
            else None
        ),
        "captured_at": value.captured_at,
        "project_state": project_state_to_dict(value.project_state),
        "authority_state": authority_state_to_dict(value.authority_state),
        "goal_states": [goal_state_to_dict(item) for item in value.goal_states],
        "build_states": [build_state_to_dict(item) for item in value.build_states],
        "resource_states": [
            resource_state_to_dict(item) for item in value.resource_states
        ],
        "incident_states": [
            incident_state_to_dict(item) for item in value.incident_states
        ],
        "human_attention_states": [
            human_attention_state_to_dict(item)
            for item in value.human_attention_states
        ],
        "evidence_snapshot": [
            goal_evidence_reference_to_dict(item) for item in value.evidence_snapshot
        ],
        "schema_version": value.schema_version,
    }


def project_state_snapshot_from_dict(
    payload: Mapping[str, Any],
) -> ProjectStateSnapshot:
    data = _require_fields(
        payload,
        {
            "snapshot_id",
            "revision",
            "supersedes_snapshot",
            "captured_at",
            "project_state",
            "authority_state",
            "goal_states",
            "build_states",
            "resource_states",
            "incident_states",
            "human_attention_states",
            "evidence_snapshot",
            "schema_version",
        },
    )
    if data["supersedes_snapshot"] is not None:
        data["supersedes_snapshot"] = state_snapshot_reference_from_dict(
            _require_mapping(data["supersedes_snapshot"], "supersedes_snapshot")
        )
    data["project_state"] = project_state_from_dict(
        _require_mapping(data["project_state"], "project_state")
    )
    data["authority_state"] = authority_state_from_dict(
        _require_mapping(data["authority_state"], "authority_state")
    )
    parsers = {
        "goal_states": goal_state_from_dict,
        "build_states": build_state_from_dict,
        "resource_states": resource_state_from_dict,
        "incident_states": incident_state_from_dict,
        "human_attention_states": human_attention_state_from_dict,
        "evidence_snapshot": lambda item: _foundation_parse(
            goal_evidence_reference_from_dict,
            item,
        ),
    }
    for field_name, parser in parsers.items():
        values = _json_tuple(data[field_name], field_name)
        data[field_name] = tuple(
            parser(_require_mapping(item, field_name)) for item in values
        )
    return ProjectStateSnapshot(**data)


def state_conflict_to_dict(value: StateConflict) -> dict[str, Any]:
    _require_type(value, StateConflict, "value")
    return {
        "conflict_id": value.conflict_id,
        "domain": value.domain,
        "subject_id": value.subject_id,
        "candidate_record_ids": list(value.candidate_record_ids),
        "candidate_semantic_hashes": list(value.candidate_semantic_hashes),
        "detected_at": value.detected_at,
        "evidence_ref_ids": list(value.evidence_ref_ids),
        "human_decision_ref_ids": list(value.human_decision_ref_ids),
        "authority_ref_ids": list(value.authority_ref_ids),
        "schema_version": value.schema_version,
    }


def state_conflict_from_dict(payload: Mapping[str, Any]) -> StateConflict:
    data = _require_fields(
        payload,
        {
            "conflict_id",
            "domain",
            "subject_id",
            "candidate_record_ids",
            "candidate_semantic_hashes",
            "detected_at",
            "evidence_ref_ids",
            "human_decision_ref_ids",
            "authority_ref_ids",
            "schema_version",
        },
    )
    for field_name in (
        "candidate_record_ids",
        "candidate_semantic_hashes",
        "evidence_ref_ids",
        "human_decision_ref_ids",
        "authority_ref_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return StateConflict(**data)


def state_conflict_resolution_to_dict(
    value: StateConflictResolution,
) -> dict[str, Any]:
    _require_type(value, StateConflictResolution, "value")
    return {
        "resolution_id": value.resolution_id,
        "conflict_id": value.conflict_id,
        "selected_record_id": value.selected_record_id,
        "resolution_kind": value.resolution_kind,
        "resolved_at": value.resolved_at,
        "human_decision_ref_ids": list(value.human_decision_ref_ids),
        "policy_refs": [
            goal_policy_reference_to_dict(item) for item in value.policy_refs
        ],
        "authority_ref_ids": list(value.authority_ref_ids),
        "schema_version": value.schema_version,
    }


def state_conflict_resolution_from_dict(
    payload: Mapping[str, Any],
) -> StateConflictResolution:
    data = _require_fields(
        payload,
        {
            "resolution_id",
            "conflict_id",
            "selected_record_id",
            "resolution_kind",
            "resolved_at",
            "human_decision_ref_ids",
            "policy_refs",
            "authority_ref_ids",
            "schema_version",
        },
    )
    for field_name in ("human_decision_ref_ids", "authority_ref_ids"):
        data[field_name] = _json_tuple(data[field_name], field_name)
    policy_values = _json_tuple(data["policy_refs"], "policy_refs")
    data["policy_refs"] = tuple(
        _foundation_parse(
            goal_policy_reference_from_dict,
            _require_mapping(item, "policy_refs"),
        )
        for item in policy_values
    )
    return StateConflictResolution(**data)


def state_reconciliation_entry_to_dict(
    value: StateReconciliationEntry,
) -> dict[str, Any]:
    _require_type(value, StateReconciliationEntry, "value")
    return {
        "domain": value.domain,
        "subject_id": value.subject_id,
        "reconciliation_status": value.reconciliation_status,
        "candidate_record_ids": list(value.candidate_record_ids),
        "candidate_semantic_hashes": list(value.candidate_semantic_hashes),
        "current_record_ids": list(value.current_record_ids),
        "stale_record_ids": list(value.stale_record_ids),
        "unavailable_record_ids": list(value.unavailable_record_ids),
        "unknown_freshness_record_ids": list(value.unknown_freshness_record_ids),
        "unknown_availability_record_ids": list(
            value.unknown_availability_record_ids
        ),
        "conflict_id": value.conflict_id,
        "resolution_id": value.resolution_id,
        "schema_version": value.schema_version,
    }


def state_reconciliation_entry_from_dict(
    payload: Mapping[str, Any],
) -> StateReconciliationEntry:
    data = _require_fields(
        payload,
        {
            "domain",
            "subject_id",
            "reconciliation_status",
            "candidate_record_ids",
            "candidate_semantic_hashes",
            "current_record_ids",
            "stale_record_ids",
            "unavailable_record_ids",
            "unknown_freshness_record_ids",
            "unknown_availability_record_ids",
            "conflict_id",
            "resolution_id",
            "schema_version",
        },
    )
    for field_name in (
        "candidate_record_ids",
        "candidate_semantic_hashes",
        "current_record_ids",
        "stale_record_ids",
        "unavailable_record_ids",
        "unknown_freshness_record_ids",
        "unknown_availability_record_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return StateReconciliationEntry(**data)


def state_reconciliation_result_to_dict(
    value: StateReconciliationResult,
) -> dict[str, Any]:
    _require_type(value, StateReconciliationResult, "value")
    return {
        "reconciliation_id": value.reconciliation_id,
        "as_of": value.as_of,
        "input_snapshot_refs": [
            state_snapshot_reference_to_dict(item)
            for item in value.input_snapshot_refs
        ],
        "entries": [state_reconciliation_entry_to_dict(item) for item in value.entries],
        "conflicts": [state_conflict_to_dict(item) for item in value.conflicts],
        "resolutions": [
            state_conflict_resolution_to_dict(item) for item in value.resolutions
        ],
        "aggregate_status": value.aggregate_status,
        "schema_version": value.schema_version,
    }


def state_reconciliation_result_from_dict(
    payload: Mapping[str, Any],
) -> StateReconciliationResult:
    data = _require_fields(
        payload,
        {
            "reconciliation_id",
            "as_of",
            "input_snapshot_refs",
            "entries",
            "conflicts",
            "resolutions",
            "aggregate_status",
            "schema_version",
        },
    )
    parsers = {
        "input_snapshot_refs": state_snapshot_reference_from_dict,
        "entries": state_reconciliation_entry_from_dict,
        "conflicts": state_conflict_from_dict,
        "resolutions": state_conflict_resolution_from_dict,
    }
    for field_name, parser in parsers.items():
        values = _json_tuple(data[field_name], field_name)
        data[field_name] = tuple(
            parser(_require_mapping(item, field_name)) for item in values
        )
    return StateReconciliationResult(**data)


def state_record_to_dict(value: StateRecord) -> dict[str, Any]:
    serializers = (
        (ProjectState, project_state_to_dict),
        (AuthorityState, authority_state_to_dict),
        (GoalState, goal_state_to_dict),
        (BuildState, build_state_to_dict),
        (ResourceState, resource_state_to_dict),
        (IncidentState, incident_state_to_dict),
        (HumanAttentionState, human_attention_state_to_dict),
    )
    for expected_type, serializer in serializers:
        if isinstance(value, expected_type):
            return serializer(value)
    raise GoalEngineStateError("value must be a State Engine state record")


def state_record_comparison_to_dict(value: StateRecord) -> dict[str, Any]:
    """Return explicit current-state semantics without record metadata/provenance."""

    if isinstance(value, ProjectState):
        return {
            "project_state": value.project_state,
            "active_phase_id": value.active_phase_id,
            "active_phase_part": value.active_phase_part,
            "gate_scope": value.gate_scope,
            "schema_version": value.schema_version,
        }
    if isinstance(value, AuthorityState):
        return {
            "authority_stage": value.authority_stage,
            "capability": (
                goal_capability_to_dict(value.capability)
                if value.capability is not None
                else None
            ),
            "safe_mode": goal_safe_mode_to_dict(value.safe_mode),
            "promotion_ref_ids": list(value.promotion_ref_ids),
            "downgrade_ref_ids": list(value.downgrade_ref_ids),
            "schema_version": value.schema_version,
        }
    if isinstance(value, GoalState):
        return {
            "goal_identifier": goal_identifier_to_dict(value.goal_identifier),
            "goal_contract_id": value.goal_contract_id,
            "goal_contract_revision": value.goal_contract_revision,
            "lifecycle_state": value.lifecycle_state,
            "blocked_by_ids": list(value.blocked_by_ids),
            "human_attention_request_ids": list(value.human_attention_request_ids),
            "schema_version": value.schema_version,
        }
    if isinstance(value, BuildState):
        return {
            "goal_identifier": (
                goal_identifier_to_dict(value.goal_identifier)
                if value.goal_identifier is not None
                else None
            ),
            "goal_contract_id": value.goal_contract_id,
            "goal_contract_revision": value.goal_contract_revision,
            "phase_id": value.phase_id,
            "phase_part": value.phase_part,
            "build_state": value.build_state,
            "artifact_ref_ids": list(value.artifact_ref_ids),
            "validation_ref_ids": list(value.validation_ref_ids),
            "schema_version": value.schema_version,
        }
    if isinstance(value, ResourceState):
        return {
            "resource_kind": value.resource_kind,
            "resource_state": value.resource_state,
            "constraint_summary": value.constraint_summary,
            "temporary": value.temporary,
            "cleanup_required": value.cleanup_required,
            "cleanup_ref_ids": list(value.cleanup_ref_ids),
            "schema_version": value.schema_version,
        }
    if isinstance(value, IncidentState):
        return {
            "incident_state": value.incident_state,
            "risk": value.risk,
            "opened_at": value.opened_at,
            "contained_at": value.contained_at,
            "closed_at": value.closed_at,
            "affected_system_ids": list(value.affected_system_ids),
            "safe_mode": goal_safe_mode_to_dict(value.safe_mode),
            "human_attention_request_ids": list(value.human_attention_request_ids),
            "schema_version": value.schema_version,
        }
    if isinstance(value, HumanAttentionState):
        return {
            "attention_state": value.attention_state,
            "decision_question": value.decision_question,
            "requested_at": value.requested_at,
            "responded_at": value.responded_at,
            "response_ref_ids": list(value.response_ref_ids),
            "blocking_goal_ids": list(value.blocking_goal_ids),
            "blocking_build_ids": list(value.blocking_build_ids),
            "schema_version": value.schema_version,
        }
    raise GoalEngineStateError("value must be a State Engine state record")


def state_provenance_semantic_hash(value: StateProvenance) -> str:
    return semantic_hash(state_provenance_to_dict(value))


def project_state_semantic_hash(value: ProjectState) -> str:
    return semantic_hash(project_state_to_dict(value))


def authority_state_semantic_hash(value: AuthorityState) -> str:
    return semantic_hash(authority_state_to_dict(value))


def goal_state_semantic_hash(value: GoalState) -> str:
    return semantic_hash(goal_state_to_dict(value))


def build_state_semantic_hash(value: BuildState) -> str:
    return semantic_hash(build_state_to_dict(value))


def resource_state_semantic_hash(value: ResourceState) -> str:
    return semantic_hash(resource_state_to_dict(value))


def incident_state_semantic_hash(value: IncidentState) -> str:
    return semantic_hash(incident_state_to_dict(value))


def human_attention_state_semantic_hash(value: HumanAttentionState) -> str:
    return semantic_hash(human_attention_state_to_dict(value))


def state_snapshot_reference_semantic_hash(value: StateSnapshotReference) -> str:
    return semantic_hash(state_snapshot_reference_to_dict(value))


def project_state_snapshot_semantic_hash(value: ProjectStateSnapshot) -> str:
    return semantic_hash(project_state_snapshot_to_dict(value))


def state_conflict_semantic_hash(value: StateConflict) -> str:
    return semantic_hash(state_conflict_to_dict(value))


def state_conflict_resolution_semantic_hash(value: StateConflictResolution) -> str:
    return semantic_hash(state_conflict_resolution_to_dict(value))


def state_reconciliation_entry_semantic_hash(value: StateReconciliationEntry) -> str:
    return semantic_hash(state_reconciliation_entry_to_dict(value))


def state_reconciliation_result_semantic_hash(value: StateReconciliationResult) -> str:
    return semantic_hash(state_reconciliation_result_to_dict(value))


def state_record_semantic_hash(value: StateRecord) -> str:
    return semantic_hash(state_record_to_dict(value))


def state_record_comparison_semantic_hash(value: StateRecord) -> str:
    return semantic_hash(state_record_comparison_to_dict(value))


def validate_project_state_snapshot(
    snapshot: ProjectStateSnapshot,
) -> ProjectStateSnapshot:
    _require_type(snapshot, ProjectStateSnapshot, "snapshot")
    collections = _snapshot_collections(snapshot)
    record_ids = [_record_id(record) for _, records in collections for record in records]
    duplicate_record_ids = _duplicates(record_ids)
    if duplicate_record_ids:
        raise GoalEngineStateError(
            f"duplicate state record ID: {duplicate_record_ids[0]}"
        )
    for domain, records in collections:
        duplicate_subjects = _duplicates([_subject_id(domain, item) for item in records])
        if duplicate_subjects:
            raise GoalEngineStateError(
                f"duplicate {domain} subject ID: {duplicate_subjects[0]}"
            )
    evidence_ids = [item.evidence_ref_id for item in snapshot.evidence_snapshot]
    duplicate_evidence = _duplicates(evidence_ids)
    if duplicate_evidence:
        raise GoalEngineStateError(
            f"duplicate evidence_ref_id: {duplicate_evidence[0]}"
        )
    known_evidence = set(evidence_ids)
    for _, records in collections:
        for record in records:
            unknown = sorted(set(record.provenance.evidence_ref_ids) - known_evidence)
            if unknown:
                raise GoalEngineStateError(
                    f"provenance references unknown evidence: {unknown[0]}"
                )
    request_ids = {item.request_id for item in snapshot.human_attention_states}
    for goal in snapshot.goal_states:
        unknown = sorted(set(goal.human_attention_request_ids) - request_ids)
        if unknown:
            raise GoalEngineStateError(
                f"Goal references unknown human-attention request: {unknown[0]}"
            )
    for incident in snapshot.incident_states:
        unknown = sorted(set(incident.human_attention_request_ids) - request_ids)
        if unknown:
            raise GoalEngineStateError(
                f"incident references unknown human-attention request: {unknown[0]}"
            )
    goal_state_ids = {item.goal_state_id for item in snapshot.goal_states}
    build_ids = {item.build_id for item in snapshot.build_states}
    for request in snapshot.human_attention_states:
        unknown_goals = sorted(set(request.blocking_goal_ids) - goal_state_ids)
        if unknown_goals:
            raise GoalEngineStateError(
                f"human-attention request references unknown Goal state: {unknown_goals[0]}"
            )
        unknown_builds = sorted(set(request.blocking_build_ids) - build_ids)
        if unknown_builds:
            raise GoalEngineStateError(
                f"human-attention request references unknown Build: {unknown_builds[0]}"
            )
    goals_by_identifier = {
        (item.goal_identifier.entity_kind, item.goal_identifier.local_id): item
        for item in snapshot.goal_states
    }
    for build in snapshot.build_states:
        if build.goal_identifier is None:
            continue
        goal = goals_by_identifier.get(
            (build.goal_identifier.entity_kind, build.goal_identifier.local_id)
        )
        if goal is None:
            raise GoalEngineStateError(
                "Build goal_identifier does not resolve within the snapshot"
            )
        if (
            build.goal_contract_id != goal.goal_contract_id
            or build.goal_contract_revision != goal.goal_contract_revision
        ):
            raise GoalEngineStateError(
                "Build and Goal must preserve exact Goal Contract identity and revision"
            )
    return snapshot


def validate_project_state_snapshot_revision(
    previous: ProjectStateSnapshot,
    current: ProjectStateSnapshot,
) -> ProjectStateSnapshot:
    validate_project_state_snapshot(previous)
    validate_project_state_snapshot(current)
    if current.snapshot_id != previous.snapshot_id:
        raise GoalEngineStateError("snapshot revisions must use the same snapshot_id")
    if current.revision != previous.revision + 1:
        raise GoalEngineStateError("snapshot revisions must advance by exactly one")
    reference = current.supersedes_snapshot
    if reference is None:
        raise GoalEngineStateError("current snapshot lacks supersedes_snapshot")
    if reference.revision != previous.revision:
        raise GoalEngineStateError("supersedes_snapshot revision mismatch")
    if reference.semantic_hash != project_state_snapshot_semantic_hash(previous):
        raise GoalEngineStateError(
            "supersedes_snapshot must preserve the prior semantic hash"
        )
    if _parse_utc_timestamp(current.captured_at, "captured_at") < _parse_utc_timestamp(
        previous.captured_at,
        "captured_at",
    ):
        raise GoalEngineStateError("snapshot capture time cannot move backward")
    previous_records = {
        _record_id(record): (domain, record)
        for domain, records in _snapshot_collections(previous)
        for record in records
    }
    for domain, records in _snapshot_collections(current):
        for record in records:
            record_id = _record_id(record)
            prior = previous_records.get(record_id)
            if prior is None:
                if record.state_revision != 1:
                    raise GoalEngineStateError(
                        f"new state record must begin at revision 1: {record_id}"
                    )
                continue
            prior_domain, prior_record = prior
            if prior_domain != domain or _subject_id(prior_domain, prior_record) != _subject_id(domain, record):
                raise GoalEngineStateError(
                    f"state record identity changed under record ID: {record_id}"
                )
            prior_semantics = _record_revision_comparison_to_dict(prior_record)
            current_semantics = _record_revision_comparison_to_dict(record)
            expected_revision = (
                prior_record.state_revision
                if prior_semantics == current_semantics
                else prior_record.state_revision + 1
            )
            if record.state_revision != expected_revision:
                raise GoalEngineStateError(
                    f"invalid state revision for record: {record_id}"
                )
    return current


def validate_state_conflict_resolution(
    resolution: StateConflictResolution,
    conflict: StateConflict,
    accepted_policy_registry: GoalPolicyRegistry | None = None,
) -> StateConflictResolution:
    _require_type(resolution, StateConflictResolution, "resolution")
    _require_type(conflict, StateConflict, "conflict")
    if accepted_policy_registry is not None:
        _require_type(
            accepted_policy_registry,
            GoalPolicyRegistry,
            "accepted_policy_registry",
        )
    if resolution.conflict_id != conflict.conflict_id:
        raise GoalEngineStateError("resolution references the wrong conflict")
    if resolution.selected_record_id not in conflict.candidate_record_ids:
        raise GoalEngineStateError(
            "resolution must select an exact usable current conflict candidate"
        )
    if conflict.candidate_record_ids.count(resolution.selected_record_id) != 1:
        raise GoalEngineStateError(
            "resolution cannot select an ambiguous candidate record ID"
        )
    if resolution.resolution_kind == "ACCEPTED_POLICY":
        if accepted_policy_registry is None:
            raise GoalEngineStateError(
                "ACCEPTED_POLICY requires an accepted GoalPolicyRegistry"
            )
        for reference in resolution.policy_refs:
            try:
                record = lookup_goal_policy(
                    accepted_policy_registry,
                    reference.policy_id,
                    reference.policy_version,
                )
            except GoalEngineFoundationError as exc:
                raise GoalEngineStateError(str(exc)) from exc
            if reference.semantic_hash != goal_policy_record_semantic_hash(record):
                raise GoalEngineStateError(
                    "policy reference semantic hash does not match accepted history"
                )
    return resolution


def state_conflict_id(
    domain: str,
    subject_id: str,
    candidate_semantic_hashes: tuple[str, ...],
) -> str:
    validate_state_domain(domain)
    _require_id(subject_id, "subject_id")
    if not isinstance(candidate_semantic_hashes, tuple):
        raise GoalEngineStateError("candidate_semantic_hashes must be a tuple")
    hashes = tuple(sorted({_require_sha256(item, "candidate_semantic_hashes") for item in candidate_semantic_hashes}))
    if len(hashes) < 2:
        raise GoalEngineStateError(
            "state conflict requires at least two distinct candidate semantic hashes"
        )
    digest = semantic_hash(
        {
            "domain": domain,
            "subject_id": subject_id,
            "candidate_semantic_hashes": list(hashes),
        }
    )
    return f"state-conflict:{digest}"


def reconcile_project_state(
    reconciliation_id: str,
    snapshots: tuple[ProjectStateSnapshot, ...],
    as_of: str,
    conflict_resolutions: tuple[StateConflictResolution, ...] = (),
    accepted_policy_registry: GoalPolicyRegistry | None = None,
) -> StateReconciliationResult:
    _require_id(reconciliation_id, "reconciliation_id")
    as_of_time = _parse_utc_timestamp(as_of, "as_of")
    snapshots = _typed_tuple(snapshots, ProjectStateSnapshot, "snapshots")
    if not snapshots:
        raise GoalEngineStateError("reconciliation requires at least one snapshot")
    conflict_resolutions = _typed_tuple(
        conflict_resolutions,
        StateConflictResolution,
        "conflict_resolutions",
    )
    if accepted_policy_registry is not None:
        _require_type(
            accepted_policy_registry,
            GoalPolicyRegistry,
            "accepted_policy_registry",
        )
    duplicate_snapshots = _duplicates(
        [(item.snapshot_id, item.revision) for item in snapshots]
    )
    if duplicate_snapshots:
        snapshot_id, revision = duplicate_snapshots[0]
        raise GoalEngineStateError(
            f"duplicate snapshot input: {snapshot_id} revision {revision}"
        )
    lineages: dict[str, list[ProjectStateSnapshot]] = {}
    for snapshot in snapshots:
        validate_project_state_snapshot(snapshot)
        lineages.setdefault(snapshot.snapshot_id, []).append(snapshot)
    tips: list[ProjectStateSnapshot] = []
    for snapshot_id in sorted(lineages):
        lineage = sorted(lineages[snapshot_id], key=lambda item: item.revision)
        if lineage[0].revision != 1:
            raise GoalEngineStateError(
                f"snapshot lineage must include revision 1: {snapshot_id}"
            )
        for previous, current in zip(lineage, lineage[1:], strict=False):
            validate_project_state_snapshot_revision(previous, current)
        tips.append(lineage[-1])
    grouped: dict[tuple[str, str], list[StateRecord]] = {}
    for snapshot in tips:
        for domain, records in _snapshot_collections(snapshot):
            for record in records:
                grouped.setdefault((domain, _subject_id(domain, record)), []).append(record)
    supplied_by_conflict: dict[str, StateConflictResolution] = {}
    seen_resolution_ids: set[str] = set()
    for resolution in conflict_resolutions:
        if resolution.resolution_id in seen_resolution_ids:
            raise GoalEngineStateError(
                f"duplicate resolution_id: {resolution.resolution_id}"
            )
        seen_resolution_ids.add(resolution.resolution_id)
        if resolution.conflict_id in supplied_by_conflict:
            raise GoalEngineStateError(
                f"multiple resolutions for conflict: {resolution.conflict_id}"
            )
        if _parse_utc_timestamp(resolution.resolved_at, "resolved_at") > as_of_time:
            raise GoalEngineStateError("future conflict resolution cannot apply as_of")
        supplied_by_conflict[resolution.conflict_id] = resolution
    entries: list[StateReconciliationEntry] = []
    conflicts: list[StateConflict] = []
    accepted_resolutions: list[StateConflictResolution] = []
    for (domain, subject_id), records in sorted(grouped.items()):
        candidates: list[tuple[StateRecord, str, str, str]] = []
        for record in records:
            freshness = classify_state_freshness(record.provenance, as_of)
            candidates.append(
                (
                    record,
                    state_record_comparison_semantic_hash(record),
                    freshness,
                    record.provenance.availability,
                )
            )
        candidates.sort(key=lambda item: (_record_id(item[0]), item[1]))
        collapsed_candidates: list[tuple[StateRecord, str, str, str]] = []
        observations_by_pair: dict[tuple[str, str], tuple[str, str]] = {}
        dimensions_by_id: dict[str, tuple[str, str]] = {}
        for item in candidates:
            record_id = _record_id(item[0])
            pair = (record_id, item[1])
            dimensions = (item[2], item[3])
            prior_dimensions = observations_by_pair.get(pair)
            if prior_dimensions is not None:
                if prior_dimensions != dimensions:
                    raise GoalEngineStateError(
                        "the same candidate identity and semantics cannot carry "
                        "different freshness or availability classifications"
                    )
                continue
            id_dimensions = dimensions_by_id.get(record_id)
            if id_dimensions is not None and id_dimensions != dimensions:
                raise GoalEngineStateError(
                    "ambiguous candidate record ID spans freshness or availability buckets"
                )
            observations_by_pair[pair] = dimensions
            dimensions_by_id[record_id] = dimensions
            collapsed_candidates.append(item)
        candidates = collapsed_candidates
        candidate_ids = tuple(_record_id(item[0]) for item in candidates)
        candidate_hashes = tuple(item[1] for item in candidates)
        current_ids = tuple(
            _record_id(item[0]) for item in candidates if item[2] == "CURRENT"
        )
        stale_ids = tuple(
            _record_id(item[0]) for item in candidates if item[2] == "STALE"
        )
        unknown_freshness_ids = tuple(
            _record_id(item[0]) for item in candidates if item[2] == "UNKNOWN"
        )
        unavailable_ids = tuple(
            _record_id(item[0]) for item in candidates if item[3] == "UNAVAILABLE"
        )
        unknown_availability_ids = tuple(
            _record_id(item[0]) for item in candidates if item[3] == "UNKNOWN"
        )
        usable_current = [
            item for item in candidates if item[2] == "CURRENT" and item[3] == "AVAILABLE"
        ]
        usable_hashes = {item[1] for item in usable_current}
        conflict: StateConflict | None = None
        resolution: StateConflictResolution | None = None
        if len(usable_hashes) > 1:
            usable_records = [item[0] for item in usable_current]
            evidence_refs = tuple(
                sorted(
                    {
                        reference
                        for record in usable_records
                        for reference in record.provenance.evidence_ref_ids
                    }
                )
            )
            human_refs = tuple(
                sorted(
                    {
                        reference
                        for record in usable_records
                        for reference in record.provenance.human_decision_ref_ids
                    }
                )
            )
            authority_refs = tuple(
                sorted(
                    {
                        reference
                        for record in usable_records
                        for reference in record.provenance.authority_ref_ids
                    }
                )
            )
            conflict_id = state_conflict_id(domain, subject_id, tuple(usable_hashes))
            conflict = StateConflict(
                conflict_id=conflict_id,
                domain=domain,
                subject_id=subject_id,
                candidate_record_ids=tuple(_record_id(item[0]) for item in usable_current),
                candidate_semantic_hashes=tuple(item[1] for item in usable_current),
                detected_at=as_of,
                evidence_ref_ids=evidence_refs,
                human_decision_ref_ids=human_refs,
                authority_ref_ids=authority_refs,
                schema_version=STATE_CONFLICT_SCHEMA_VERSION,
            )
            resolution = supplied_by_conflict.pop(conflict_id, None)
            if resolution is not None:
                validate_state_conflict_resolution(
                    resolution,
                    conflict,
                    accepted_policy_registry,
                )
                status = "RESOLVED_CONFLICT"
                accepted_resolutions.append(resolution)
            else:
                status = "CONFLICTED"
            conflicts.append(conflict)
        elif usable_current:
            status = "CONSISTENT"
        elif any(item[3] == "AVAILABLE" for item in candidates):
            status = "INCOMPLETE"
        elif any(item[3] == "UNAVAILABLE" for item in candidates):
            status = "UNAVAILABLE"
        else:
            status = "INCOMPLETE"
        entries.append(
            StateReconciliationEntry(
                domain=domain,
                subject_id=subject_id,
                reconciliation_status=status,
                candidate_record_ids=candidate_ids,
                candidate_semantic_hashes=candidate_hashes,
                current_record_ids=current_ids,
                stale_record_ids=stale_ids,
                unavailable_record_ids=unavailable_ids,
                unknown_freshness_record_ids=unknown_freshness_ids,
                unknown_availability_record_ids=unknown_availability_ids,
                conflict_id=conflict.conflict_id if conflict is not None else None,
                resolution_id=resolution.resolution_id if resolution is not None else None,
                schema_version=STATE_RECONCILIATION_ENTRY_SCHEMA_VERSION,
            )
        )
    if supplied_by_conflict:
        unknown_conflict = sorted(supplied_by_conflict)[0]
        raise GoalEngineStateError(
            f"resolution references no current conflict: {unknown_conflict}"
        )
    aggregate_status = _aggregate_status(tuple(entries))
    input_refs = tuple(
        StateSnapshotReference(
            snapshot_id=item.snapshot_id,
            revision=item.revision,
            semantic_hash=project_state_snapshot_semantic_hash(item),
            schema_version=STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        )
        for item in snapshots
    )
    return StateReconciliationResult(
        reconciliation_id=reconciliation_id,
        as_of=as_of,
        input_snapshot_refs=input_refs,
        entries=tuple(entries),
        conflicts=tuple(conflicts),
        resolutions=tuple(accepted_resolutions),
        aggregate_status=aggregate_status,
        schema_version=STATE_RECONCILIATION_RESULT_SCHEMA_VERSION,
    )


def _validate_authority_representation(value: AuthorityState) -> None:
    capability_id = value.capability.capability_id if value.capability is not None else None
    ceilings = {
        "DOCUMENTATION_ONLY": (None,),
        "STAGE_0_SHADOW": ("CAP-0",),
        "STAGE_1_WORK_ORDER": ("CAP-0", "CAP-1"),
        "STAGE_2_SAFE_EXPERIMENT": ("CAP-0", "CAP-1", "CAP-2"),
        "STAGE_3_BUILD_GRAPH_SUBMISSION": ("CAP-0", "CAP-1", "CAP-2", "CAP-3"),
    }
    if capability_id not in ceilings[value.authority_stage]:
        raise GoalEngineStateError(
            "capability exceeds or violates the represented authority-stage ceiling"
        )
    if value.authority_stage != "DOCUMENTATION_ONLY" and not value.provenance.authority_ref_ids:
        raise GoalEngineStateError(
            "represented authority beyond documentation requires authority references"
        )
    if value.authority_stage in {
        "STAGE_1_WORK_ORDER",
        "STAGE_2_SAFE_EXPERIMENT",
        "STAGE_3_BUILD_GRAPH_SUBMISSION",
    } and not value.promotion_ref_ids:
        raise GoalEngineStateError(
            "Stage 1 through Stage 3 representation requires a promotion reference"
        )


def _snapshot_collections(
    snapshot: ProjectStateSnapshot,
) -> tuple[tuple[str, tuple[StateRecord, ...]], ...]:
    return (
        ("PROJECT", (snapshot.project_state,)),
        ("AUTHORITY", (snapshot.authority_state,)),
        ("GOAL", snapshot.goal_states),
        ("BUILD", snapshot.build_states),
        ("RESOURCE", snapshot.resource_states),
        ("INCIDENT", snapshot.incident_states),
        ("HUMAN_ATTENTION", snapshot.human_attention_states),
    )


def _record_id(value: StateRecord) -> str:
    if isinstance(value, ProjectState):
        return value.project_id
    if isinstance(value, AuthorityState):
        return value.authority_state_id
    if isinstance(value, GoalState):
        return value.goal_state_id
    if isinstance(value, BuildState):
        return value.build_id
    if isinstance(value, ResourceState):
        return value.resource_id
    if isinstance(value, IncidentState):
        return value.incident_id
    if isinstance(value, HumanAttentionState):
        return value.request_id
    raise GoalEngineStateError("value must be a State Engine state record")


def _subject_id(domain: str, value: StateRecord) -> str:
    if domain == "GOAL" and isinstance(value, GoalState):
        return value.goal_identifier.local_id
    return _record_id(value)


def _record_revision_comparison_to_dict(value: StateRecord) -> dict[str, Any]:
    payload = state_record_to_dict(value)
    payload.pop("state_revision")
    return payload


def _validate_reconciliation_result(value: StateReconciliationResult) -> None:
    duplicate_refs = _duplicates(
        [(item.snapshot_id, item.revision) for item in value.input_snapshot_refs]
    )
    if duplicate_refs:
        raise GoalEngineStateError("duplicate input snapshot reference")
    entry_keys = [(item.domain, item.subject_id) for item in value.entries]
    if _duplicates(entry_keys):
        raise GoalEngineStateError("duplicate reconciliation entry")
    conflicts = {item.conflict_id: item for item in value.conflicts}
    if len(conflicts) != len(value.conflicts):
        raise GoalEngineStateError("duplicate conflict_id")
    resolutions = {item.resolution_id: item for item in value.resolutions}
    if len(resolutions) != len(value.resolutions):
        raise GoalEngineStateError("duplicate resolution_id")
    conflict_ids_from_entries = {
        item.conflict_id for item in value.entries if item.conflict_id is not None
    }
    if conflict_ids_from_entries != set(conflicts):
        raise GoalEngineStateError("entries and conflicts must align exactly")
    resolution_ids_from_entries = {
        item.resolution_id for item in value.entries if item.resolution_id is not None
    }
    if resolution_ids_from_entries != set(resolutions):
        raise GoalEngineStateError("entries and resolutions must align exactly")
    for resolution in value.resolutions:
        conflict = conflicts.get(resolution.conflict_id)
        if conflict is None:
            raise GoalEngineStateError("resolution references unknown conflict")
        if resolution.selected_record_id not in conflict.candidate_record_ids:
            raise GoalEngineStateError("resolution selects a non-candidate record")
        if conflict.candidate_record_ids.count(resolution.selected_record_id) != 1:
            raise GoalEngineStateError("resolution selects an ambiguous candidate record")
        if _parse_utc_timestamp(resolution.resolved_at, "resolved_at") > _parse_utc_timestamp(
            value.as_of,
            "as_of",
        ):
            raise GoalEngineStateError("future conflict resolution cannot apply as_of")
    for conflict in value.conflicts:
        if conflict.detected_at != value.as_of:
            raise GoalEngineStateError("conflict detected_at must equal reconciliation as_of")
    expected = _aggregate_status(value.entries)
    if value.aggregate_status != expected:
        raise GoalEngineStateError("aggregate_status violates exact precedence")


def _aggregate_status(entries: tuple[StateReconciliationEntry, ...]) -> str:
    statuses = {item.reconciliation_status for item in entries}
    if "CONFLICTED" in statuses:
        return "CONFLICTED"
    if "RESOLVED_CONFLICT" in statuses:
        return "RESOLVED_CONFLICT"
    if "INCOMPLETE" in statuses:
        return "INCOMPLETE"
    if "UNAVAILABLE" in statuses:
        return "UNAVAILABLE"
    return "CONSISTENT"


def _candidate_pairs(
    record_ids: tuple[str, ...],
    semantic_hashes: tuple[str, ...],
    *,
    require_distinct_hashes: bool,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(record_ids, tuple) or not isinstance(semantic_hashes, tuple):
        raise GoalEngineStateError("candidate IDs and hashes must be tuples")
    if len(record_ids) != len(semantic_hashes) or not record_ids:
        raise GoalEngineStateError(
            "candidate IDs and hashes must be non-empty and aligned"
        )
    pairs = [
        (_require_id(record_id, "candidate_record_ids"), _require_sha256(digest, "candidate_semantic_hashes"))
        for record_id, digest in zip(record_ids, semantic_hashes, strict=True)
    ]
    duplicate_pairs = _duplicates(pairs)
    if duplicate_pairs:
        raise GoalEngineStateError(
            "candidate IDs and hashes cannot repeat an identical pair"
        )
    pairs.sort()
    if require_distinct_hashes and len({item[1] for item in pairs}) < 2:
        raise GoalEngineStateError(
            "state conflict requires at least two distinct candidate semantic hashes"
        )
    return tuple(item[0] for item in pairs), tuple(item[1] for item in pairs)


def _require_disjoint_reference_sets(*groups: tuple[str, ...]) -> None:
    for index, left in enumerate(groups):
        for right in groups[index + 1 :]:
            overlap = sorted(set(left) & set(right))
            if overlap:
                raise GoalEngineStateError(
                    "evidence, human-decision, and authority references must remain separate"
                )


def _require_fields(
    payload: Mapping[str, Any],
    fields: set[str],
) -> dict[str, Any]:
    mapping = _require_mapping(payload, "payload")
    keys = set(mapping)
    forbidden = sorted(keys & _FORBIDDEN_FIELD_NAMES)
    if forbidden:
        raise GoalEngineStateError(
            f"payload contains forbidden field: {forbidden[0]}"
        )
    missing = sorted(fields - keys)
    if missing:
        raise GoalEngineStateError(f"payload missing required field: {missing[0]}")
    extra = sorted(keys - fields)
    if extra:
        raise GoalEngineStateError(f"payload contains unknown field: {extra[0]}")
    return dict(mapping)


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GoalEngineStateError(f"{field_name} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise GoalEngineStateError(f"{field_name} keys must be strings")
    return value


def _json_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise GoalEngineStateError(f"{field_name} must be an array")
    return tuple(value)


def _typed_tuple(
    values: tuple[Any, ...],
    expected_type: type,
    field_name: str,
) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineStateError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, expected_type):
            raise GoalEngineStateError(
                f"{field_name} must contain {expected_type.__name__} values"
            )
    return values


def _id_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineStateError(f"{field_name} must be a tuple")
    validated = tuple(_require_id(item, field_name) for item in values)
    duplicates = _duplicates(list(validated))
    if duplicates:
        raise GoalEngineStateError(
            f"{field_name} contains duplicate ID: {duplicates[0]}"
        )
    return tuple(sorted(validated)) if sort else validated


def _require_allowed(value: Any, allowed: frozenset[str], field_name: str) -> str:
    text = _require_text(value, field_name)
    if text not in allowed:
        raise GoalEngineStateError(f"unsupported {field_name}: {text}")
    return text


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise GoalEngineStateError(
            f"{field_name} must be non-empty text without surrounding whitespace"
        )
    return value


def _require_label(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if len(text) > 128 or any(ord(character) < 32 for character in text):
        raise GoalEngineStateError(f"{field_name} is not a valid governance label")
    return text


def _require_id(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _ID_PATTERN.fullmatch(text):
        raise GoalEngineStateError(f"{field_name} must be a stable local identifier")
    return text


def _require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GoalEngineStateError(f"{field_name} must be a positive integer")
    return value


def _require_bool(value: Any, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise GoalEngineStateError(f"{field_name} must be a boolean")
    return value


def _require_schema(value: Any, expected: str) -> str:
    text = _require_text(value, "schema_version")
    if text != expected:
        raise GoalEngineStateError(f"schema_version must be {expected}")
    return text


def _require_sha256(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _SHA256_PATTERN.fullmatch(text):
        raise GoalEngineStateError(
            f"{field_name} must be a lowercase SHA-256 hex digest"
        )
    return text


def _parse_utc_timestamp(value: Any, field_name: str) -> datetime:
    text = _require_text(value, field_name)
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise GoalEngineStateError(
            f"{field_name} must be an ISO-8601 UTC timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise GoalEngineStateError(f"{field_name} must be UTC")
    return parsed


def _require_type(value: Any, expected_type: type, field_name: str) -> None:
    if not isinstance(value, expected_type):
        raise GoalEngineStateError(
            f"{field_name} must be {expected_type.__name__}"
        )


def _foundation_validate(function: Any, value: Any) -> Any:
    try:
        return function(value)
    except GoalEngineFoundationError as exc:
        raise GoalEngineStateError(str(exc)) from exc


def _foundation_parse(function: Any, payload: Mapping[str, Any]) -> Any:
    try:
        return function(payload)
    except GoalEngineFoundationError as exc:
        raise GoalEngineStateError(str(exc)) from exc


def _duplicates(values: list[Any]) -> list[Any]:
    seen: set[Any] = set()
    duplicates: list[Any] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates


__all__ = [
    "AUTHORITY_STAGE_VALUES",
    "AUTHORITY_STATE_SCHEMA_VERSION",
    "BUILD_STATE_SCHEMA_VERSION",
    "BUILD_STATE_VALUES",
    "CONFLICT_RESOLUTION_KINDS",
    "GOAL_STATE_SCHEMA_VERSION",
    "HUMAN_ATTENTION_STATE_SCHEMA_VERSION",
    "HUMAN_ATTENTION_STATE_VALUES",
    "INCIDENT_STATE_SCHEMA_VERSION",
    "INCIDENT_STATE_VALUES",
    "PROJECT_STATE_SCHEMA_VERSION",
    "PROJECT_STATE_SNAPSHOT_SCHEMA_VERSION",
    "PROJECT_STATE_VALUES",
    "RECONCILIATION_STATUS_VALUES",
    "RESOURCE_STATE_SCHEMA_VERSION",
    "RESOURCE_STATE_VALUES",
    "STATE_AVAILABILITY_VALUES",
    "STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION",
    "STATE_CONFLICT_SCHEMA_VERSION",
    "STATE_DOMAINS",
    "STATE_FRESHNESS_VALUES",
    "STATE_PROVENANCE_SCHEMA_VERSION",
    "STATE_RECONCILIATION_ENTRY_SCHEMA_VERSION",
    "STATE_RECONCILIATION_RESULT_SCHEMA_VERSION",
    "STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION",
    "AuthorityState",
    "BuildState",
    "GoalEngineStateError",
    "GoalState",
    "HumanAttentionState",
    "IncidentState",
    "ProjectState",
    "ProjectStateSnapshot",
    "ResourceState",
    "StateConflict",
    "StateConflictResolution",
    "StateProvenance",
    "StateReconciliationEntry",
    "StateReconciliationResult",
    "StateSnapshotReference",
    "authority_state_from_dict",
    "authority_state_semantic_hash",
    "authority_state_to_dict",
    "build_state_from_dict",
    "build_state_semantic_hash",
    "build_state_to_dict",
    "classify_state_freshness",
    "goal_state_from_dict",
    "goal_state_semantic_hash",
    "goal_state_to_dict",
    "human_attention_state_from_dict",
    "human_attention_state_semantic_hash",
    "human_attention_state_to_dict",
    "incident_state_from_dict",
    "incident_state_semantic_hash",
    "incident_state_to_dict",
    "project_state_from_dict",
    "project_state_semantic_hash",
    "project_state_snapshot_from_dict",
    "project_state_snapshot_semantic_hash",
    "project_state_snapshot_to_dict",
    "project_state_to_dict",
    "reconcile_project_state",
    "resource_state_from_dict",
    "resource_state_semantic_hash",
    "resource_state_to_dict",
    "state_conflict_from_dict",
    "state_conflict_id",
    "state_conflict_resolution_from_dict",
    "state_conflict_resolution_semantic_hash",
    "state_conflict_resolution_to_dict",
    "state_conflict_semantic_hash",
    "state_conflict_to_dict",
    "state_provenance_from_dict",
    "state_provenance_semantic_hash",
    "state_provenance_to_dict",
    "state_reconciliation_entry_from_dict",
    "state_reconciliation_entry_semantic_hash",
    "state_reconciliation_entry_to_dict",
    "state_reconciliation_result_from_dict",
    "state_reconciliation_result_semantic_hash",
    "state_reconciliation_result_to_dict",
    "state_record_comparison_semantic_hash",
    "state_record_comparison_to_dict",
    "state_record_semantic_hash",
    "state_record_to_dict",
    "state_snapshot_reference_from_dict",
    "state_snapshot_reference_semantic_hash",
    "state_snapshot_reference_to_dict",
    "validate_authority_stage",
    "validate_build_state",
    "validate_human_attention_state",
    "validate_incident_state",
    "validate_project_state",
    "validate_project_state_snapshot",
    "validate_project_state_snapshot_revision",
    "validate_reconciliation_status",
    "validate_resource_state",
    "validate_state_availability",
    "validate_state_conflict_resolution",
    "validate_state_domain",
    "validate_state_freshness",
]
