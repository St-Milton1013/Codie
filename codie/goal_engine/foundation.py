"""Pure, deterministic Goal Engine foundation records.

This module contains vocabulary and immutable in-memory representations only.
It intentionally has no persistence, provider, model, runtime-state, or
decision-making integration.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from types import MappingProxyType
from typing import Any


IDENTIFIER_SCHEMA_VERSION = "codie.goal_engine.identifier.v1"
CAPABILITY_SCHEMA_VERSION = "codie.goal_engine.capability.v1"
SAFE_MODE_SCHEMA_VERSION = "codie.goal_engine.safe_mode.v1"
EVIDENCE_REFERENCE_SCHEMA_VERSION = "codie.goal_engine.evidence_reference.v1"
GOAL_CONTRACT_REVISION_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.goal_contract_revision_reference.v1"
)
GOAL_CONTRACT_SCHEMA_VERSION = "codie.goal_engine.goal_contract.v1"
POLICY_REFERENCE_SCHEMA_VERSION = "codie.goal_engine.policy_reference.v1"
POLICY_RECORD_SCHEMA_VERSION = "codie.goal_engine.policy_record.v1"
POLICY_REGISTRY_SCHEMA_VERSION = "codie.goal_engine.policy_registry.v1"
LINEAGE_EVENT_SCHEMA_VERSION = "codie.goal_engine.lineage_event.v1"

GOAL_LIFECYCLE_STATES = frozenset(
    {
        "ACTIVE",
        "INVESTIGATING",
        "WATCHING",
        "HEALTHY_IDLE",
        "WAITING_FOR_HUMAN",
        "PAUSED_PREEMPTED",
        "BLOCKED_PREREQUISITE",
        "IMPLEMENTED_PENDING_OUTCOME",
        "CLOSED_SUCCESS",
        "CLOSED_LIMITATION",
        "REVISE",
        "REWIND",
        "REINVESTIGATE",
    }
)
PROBLEM_CLASSIFICATIONS = frozenset({"TRANSIENT", "RECURRING", "STRUCTURAL"})
CAPABILITY_NAMES: Mapping[str, str] = MappingProxyType(
    {
        "CAP-0": "Observe",
        "CAP-1": "Investigate",
        "CAP-2": "Safe Experiment",
        "CAP-3": "Propose",
        "CAP-4": "Governed Modification",
        "CAP-5": "Release / Strategic Authority",
    }
)
CAPABILITY_IDS = frozenset(CAPABILITY_NAMES)
SIZE_VALUES = frozenset({"Tiny", "Small", "Medium", "Large", "Core"})
RISK_VALUES = frozenset({"Low", "Medium", "High", "Critical"})
ROLLBACK_VALUES = frozenset({"Easy", "Moderate", "Hard", "Not safely reversible"})
SAFE_MODE_VALUES = frozenset(
    {
        "NORMAL",
        "READ_ONLY_SAFE_MODE",
        "GOAL_ENGINE_DISABLED",
        "FULL_AUTOMATION_HALT",
    }
)
LINEAGE_ENTITY_KINDS = frozenset({"GOAL", "IDEA", "FINDING", "POLICY"})
LINEAGE_EVENT_KINDS = frozenset(
    {
        "IDEA",
        "RESEARCH",
        "FINDING",
        "GOAL",
        "EXPERIMENT",
        "IMPLEMENTATION",
        "OBSERVATION",
        "OUTCOME",
        "CONTRACT_REVISED",
        "POLICY_RECORDED",
        "HUMAN_DECISION_RECORDED",
        "EVIDENCE_RECORDED",
        "CONTRADICTORY_EVIDENCE_RECORDED",
    }
)

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


class GoalEngineFoundationError(ValueError):
    """Raised when a Goal Engine foundation value violates its contract."""


@dataclass(frozen=True)
class GoalIdentifier:
    entity_kind: str
    local_id: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_exact(self.entity_kind, "GOAL", "entity_kind")
        _require_id(self.local_id, "local_id")
        _require_schema(self.schema_version, IDENTIFIER_SCHEMA_VERSION)


@dataclass(frozen=True)
class IdeaIdentifier:
    entity_kind: str
    local_id: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_exact(self.entity_kind, "IDEA", "entity_kind")
        _require_id(self.local_id, "local_id")
        _require_schema(self.schema_version, IDENTIFIER_SCHEMA_VERSION)


@dataclass(frozen=True)
class FindingIdentifier:
    entity_kind: str
    local_id: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_exact(self.entity_kind, "FINDING", "entity_kind")
        _require_id(self.local_id, "local_id")
        _require_schema(self.schema_version, IDENTIFIER_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalCapability:
    capability_id: str
    capability_name: str
    schema_version: str

    def __post_init__(self) -> None:
        capability_id = validate_capability_id(self.capability_id)
        _require_exact(
            self.capability_name,
            CAPABILITY_NAMES[capability_id],
            "capability_name",
        )
        _require_schema(self.schema_version, CAPABILITY_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalSafeMode:
    mode: str
    schema_version: str

    def __post_init__(self) -> None:
        validate_safe_mode(self.mode)
        _require_schema(self.schema_version, SAFE_MODE_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalEvidenceReference:
    evidence_ref_id: str
    evidence_class: str
    source_id: str
    source_version: str
    observed_at: str
    historical_validity: str
    current_applicability: str
    review_state: str
    privacy_class: str
    conflict_ref_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.evidence_ref_id, "evidence_ref_id")
        _require_label(self.evidence_class, "evidence_class")
        _require_id(self.source_id, "source_id")
        _require_label(self.source_version, "source_version")
        _require_utc_timestamp(self.observed_at, "observed_at")
        _require_label(self.historical_validity, "historical_validity")
        _require_label(self.current_applicability, "current_applicability")
        _require_label(self.review_state, "review_state")
        _require_label(self.privacy_class, "privacy_class")
        object.__setattr__(
            self,
            "conflict_ref_ids",
            _id_tuple(self.conflict_ref_ids, "conflict_ref_ids", sort=True),
        )
        if self.evidence_ref_id in self.conflict_ref_ids:
            raise GoalEngineFoundationError(
                "evidence_ref_id cannot conflict with itself"
            )
        _require_schema(self.schema_version, EVIDENCE_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalContractRevisionReference:
    goal_contract_id: str
    revision: int
    semantic_hash: str
    stale_approval_ref_ids: tuple[str, ...]
    stale_validator_ref_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.goal_contract_id, "goal_contract_id")
        _require_positive_int(self.revision, "revision")
        _require_sha256(self.semantic_hash, "semantic_hash")
        object.__setattr__(
            self,
            "stale_approval_ref_ids",
            _id_tuple(
                self.stale_approval_ref_ids,
                "stale_approval_ref_ids",
                sort=True,
            ),
        )
        object.__setattr__(
            self,
            "stale_validator_ref_ids",
            _id_tuple(
                self.stale_validator_ref_ids,
                "stale_validator_ref_ids",
                sort=True,
            ),
        )
        _require_schema(
            self.schema_version,
            GOAL_CONTRACT_REVISION_REFERENCE_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class GoalContract:
    goal_contract_id: str
    revision: int
    schema_version: str
    supersedes_revision: GoalContractRevisionReference | None
    originating_idea_ids: tuple[str, ...]
    originating_finding_ids: tuple[str, ...]
    problem_classification: str
    observed_problem: str
    desired_outcome: str
    why_it_matters: str
    baseline: str
    expected_result: str
    acceptable_result: str
    maximum_acceptable_regressions: tuple[str, ...]
    root_cause_hypothesis: str
    confidence: float
    proposed_intervention: str
    credible_alternatives: tuple[str, ...]
    disconfirmation_criteria: tuple[str, ...]
    expected_affected_systems: tuple[str, ...]
    expected_unaffected_systems: tuple[str, ...]
    dependency_ids: tuple[str, ...]
    evidence_snapshot: tuple[GoalEvidenceReference, ...]
    privacy_implications: str
    security_implications: str
    zero_cost_validation: str
    manual_burden: str
    operational_burden: str
    size: str
    risk: str
    rollback: str
    rollback_plan: str
    observation_window: str
    if_we_do_nothing: str
    if_we_do_this: str
    historical_attempt_ids: tuple[str, ...]
    approval_requirements: tuple[str, ...]
    created_at: str

    def __post_init__(self) -> None:
        _require_id(self.goal_contract_id, "goal_contract_id")
        _require_positive_int(self.revision, "revision")
        _require_schema(self.schema_version, GOAL_CONTRACT_SCHEMA_VERSION)
        _validate_supersedes_revision(self)
        object.__setattr__(
            self,
            "originating_idea_ids",
            _id_tuple(self.originating_idea_ids, "originating_idea_ids", sort=True),
        )
        object.__setattr__(
            self,
            "originating_finding_ids",
            _id_tuple(
                self.originating_finding_ids,
                "originating_finding_ids",
                sort=True,
            ),
        )
        if not self.originating_idea_ids and not self.originating_finding_ids:
            raise GoalEngineFoundationError(
                "GoalContract requires an originating Idea or Finding identifier"
            )
        validate_problem_classification(self.problem_classification)
        for field_name in (
            "observed_problem",
            "desired_outcome",
            "why_it_matters",
            "baseline",
            "expected_result",
            "acceptable_result",
            "root_cause_hypothesis",
            "proposed_intervention",
            "privacy_implications",
            "security_implications",
            "zero_cost_validation",
            "manual_burden",
            "operational_burden",
            "rollback_plan",
            "observation_window",
            "if_we_do_nothing",
            "if_we_do_this",
        ):
            _require_text(getattr(self, field_name), field_name)
        object.__setattr__(self, "confidence", _require_ratio(self.confidence, "confidence"))
        object.__setattr__(
            self,
            "maximum_acceptable_regressions",
            _text_tuple(
                self.maximum_acceptable_regressions,
                "maximum_acceptable_regressions",
            ),
        )
        object.__setattr__(
            self,
            "credible_alternatives",
            _text_tuple(self.credible_alternatives, "credible_alternatives"),
        )
        if not self.credible_alternatives:
            raise GoalEngineFoundationError(
                "GoalContract requires a documented credible alternative"
            )
        object.__setattr__(
            self,
            "disconfirmation_criteria",
            _text_tuple(self.disconfirmation_criteria, "disconfirmation_criteria"),
        )
        if not self.disconfirmation_criteria:
            raise GoalEngineFoundationError(
                "GoalContract requires disconfirmation criteria"
            )
        for field_name in (
            "expected_affected_systems",
            "expected_unaffected_systems",
            "approval_requirements",
        ):
            object.__setattr__(
                self,
                field_name,
                _text_tuple(getattr(self, field_name), field_name),
            )
        for field_name in ("dependency_ids", "historical_attempt_ids"):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        object.__setattr__(
            self,
            "evidence_snapshot",
            _evidence_reference_tuple(self.evidence_snapshot),
        )
        if not self.evidence_snapshot:
            raise GoalEngineFoundationError(
                "GoalContract requires an immutable evidence_snapshot"
            )
        validate_size(self.size)
        validate_risk(self.risk)
        validate_rollback(self.rollback)
        _require_utc_timestamp(self.created_at, "created_at")


@dataclass(frozen=True)
class GoalPolicyReference:
    policy_id: str
    policy_version: int
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.policy_id, "policy_id")
        _require_positive_int(self.policy_version, "policy_version")
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(self.schema_version, POLICY_REFERENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class GoalPolicyRecord:
    policy_id: str
    policy_version: int
    schema_version: str
    date: str
    reason: str
    rule: str
    authority_ref_ids: tuple[str, ...]
    affected_policy_ids: tuple[str, ...]
    superseded_policy_ref: GoalPolicyReference | None
    regression_case_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_id(self.policy_id, "policy_id")
        _require_positive_int(self.policy_version, "policy_version")
        _require_schema(self.schema_version, POLICY_RECORD_SCHEMA_VERSION)
        _require_date(self.date, "date")
        _require_text(self.reason, "reason")
        _require_text(self.rule, "rule")
        for field_name in (
            "authority_ref_ids",
            "affected_policy_ids",
            "regression_case_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        if self.policy_version == 1 and self.superseded_policy_ref is not None:
            raise GoalEngineFoundationError(
                "policy version 1 cannot supersede an earlier policy version"
            )
        if self.policy_version > 1:
            if not isinstance(self.superseded_policy_ref, GoalPolicyReference):
                raise GoalEngineFoundationError(
                    "later policy versions require superseded_policy_ref"
                )
            if self.superseded_policy_ref.policy_id != self.policy_id:
                raise GoalEngineFoundationError(
                    "superseded policy must use the same policy_id"
                )
            if self.superseded_policy_ref.policy_version != self.policy_version - 1:
                raise GoalEngineFoundationError(
                    "superseded policy must be the immediately prior version"
                )


@dataclass(frozen=True)
class GoalPolicyRegistry:
    records: tuple[GoalPolicyRecord, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_schema(self.schema_version, POLICY_REGISTRY_SCHEMA_VERSION)
        if not isinstance(self.records, tuple):
            raise GoalEngineFoundationError("records must be a tuple")
        for record in self.records:
            if not isinstance(record, GoalPolicyRecord):
                raise GoalEngineFoundationError(
                    "records must contain GoalPolicyRecord values"
                )
        if not self.records:
            raise GoalEngineFoundationError("GoalPolicyRegistry requires records")
        object.__setattr__(
            self,
            "records",
            tuple(sorted(self.records, key=lambda item: (item.policy_id, item.policy_version))),
        )
        validate_goal_policy_registry(self)


@dataclass(frozen=True)
class GoalLineageEvent:
    event_id: str
    schema_version: str
    entity_kind: str
    entity_id: str
    entity_revision: int
    event_kind: str
    occurred_at: str
    actor_kind: str
    summary: str
    evidence_ref_ids: tuple[str, ...]
    human_decision_ref_ids: tuple[str, ...]
    authority_ref_ids: tuple[str, ...]
    prior_event_ids: tuple[str, ...]
    prior_event_hashes: tuple[str, ...]
    event_hash: str = ""

    def __post_init__(self) -> None:
        _require_id(self.event_id, "event_id")
        _require_schema(self.schema_version, LINEAGE_EVENT_SCHEMA_VERSION)
        _require_allowed(self.entity_kind, LINEAGE_ENTITY_KINDS, "entity_kind")
        _require_id(self.entity_id, "entity_id")
        _require_positive_int(self.entity_revision, "entity_revision")
        _require_allowed(self.event_kind, LINEAGE_EVENT_KINDS, "event_kind")
        _require_utc_timestamp(self.occurred_at, "occurred_at")
        _require_label(self.actor_kind, "actor_kind")
        _require_text(self.summary, "summary")
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
        conflated_refs = sorted(
            set(self.evidence_ref_ids) & set(self.human_decision_ref_ids)
        )
        if conflated_refs:
            raise GoalEngineFoundationError(
                "evidence and human decision references must remain separate"
            )
        prior_ids, prior_hashes = _prior_event_tuples(
            self.prior_event_ids,
            self.prior_event_hashes,
        )
        object.__setattr__(self, "prior_event_ids", prior_ids)
        object.__setattr__(self, "prior_event_hashes", prior_hashes)
        expected_hash = _lineage_event_expected_hash(self)
        if self.event_hash:
            _require_sha256(self.event_hash, "event_hash")
            if self.event_hash != expected_hash:
                raise GoalEngineFoundationError("event_hash does not match event semantics")
        else:
            object.__setattr__(self, "event_hash", expected_hash)


def validate_goal_lifecycle_state(value: str) -> str:
    return _require_allowed(value, GOAL_LIFECYCLE_STATES, "goal_lifecycle_state")


def validate_problem_classification(value: str) -> str:
    return _require_allowed(value, PROBLEM_CLASSIFICATIONS, "problem_classification")


def validate_capability_id(value: str) -> str:
    if value == "Level 0":
        raise GoalEngineFoundationError(
            "Level 0 is constitutional vocabulary, not a capability identifier"
        )
    return _require_allowed(value, CAPABILITY_IDS, "capability_id")


def validate_size(value: str) -> str:
    return _require_allowed(value, SIZE_VALUES, "size")


def validate_risk(value: str) -> str:
    return _require_allowed(value, RISK_VALUES, "risk")


def validate_rollback(value: str) -> str:
    return _require_allowed(value, ROLLBACK_VALUES, "rollback")


def validate_safe_mode(value: str) -> str:
    return _require_allowed(value, SAFE_MODE_VALUES, "safe_mode")


def goal_identifier_to_dict(identifier: GoalIdentifier) -> dict[str, Any]:
    _require_type(identifier, GoalIdentifier, "identifier")
    return _identifier_to_dict(identifier)


def goal_identifier_from_dict(payload: Mapping[str, Any]) -> GoalIdentifier:
    data = _require_fields(payload, {"entity_kind", "local_id", "schema_version"})
    return GoalIdentifier(**data)


def idea_identifier_to_dict(identifier: IdeaIdentifier) -> dict[str, Any]:
    _require_type(identifier, IdeaIdentifier, "identifier")
    return _identifier_to_dict(identifier)


def idea_identifier_from_dict(payload: Mapping[str, Any]) -> IdeaIdentifier:
    data = _require_fields(payload, {"entity_kind", "local_id", "schema_version"})
    return IdeaIdentifier(**data)


def finding_identifier_to_dict(identifier: FindingIdentifier) -> dict[str, Any]:
    _require_type(identifier, FindingIdentifier, "identifier")
    return _identifier_to_dict(identifier)


def finding_identifier_from_dict(payload: Mapping[str, Any]) -> FindingIdentifier:
    data = _require_fields(payload, {"entity_kind", "local_id", "schema_version"})
    return FindingIdentifier(**data)


def goal_capability_to_dict(capability: GoalCapability) -> dict[str, Any]:
    _require_type(capability, GoalCapability, "capability")
    return {
        "capability_id": capability.capability_id,
        "capability_name": capability.capability_name,
        "schema_version": capability.schema_version,
    }


def goal_capability_from_dict(payload: Mapping[str, Any]) -> GoalCapability:
    data = _require_fields(
        payload,
        {"capability_id", "capability_name", "schema_version"},
    )
    return GoalCapability(**data)


def goal_safe_mode_to_dict(safe_mode: GoalSafeMode) -> dict[str, Any]:
    _require_type(safe_mode, GoalSafeMode, "safe_mode")
    return {"mode": safe_mode.mode, "schema_version": safe_mode.schema_version}


def goal_safe_mode_from_dict(payload: Mapping[str, Any]) -> GoalSafeMode:
    data = _require_fields(payload, {"mode", "schema_version"})
    return GoalSafeMode(**data)


def goal_evidence_reference_to_dict(reference: GoalEvidenceReference) -> dict[str, Any]:
    _require_type(reference, GoalEvidenceReference, "reference")
    return {
        "evidence_ref_id": reference.evidence_ref_id,
        "evidence_class": reference.evidence_class,
        "source_id": reference.source_id,
        "source_version": reference.source_version,
        "observed_at": reference.observed_at,
        "historical_validity": reference.historical_validity,
        "current_applicability": reference.current_applicability,
        "review_state": reference.review_state,
        "privacy_class": reference.privacy_class,
        "conflict_ref_ids": list(reference.conflict_ref_ids),
        "schema_version": reference.schema_version,
    }


def goal_evidence_reference_from_dict(
    payload: Mapping[str, Any],
) -> GoalEvidenceReference:
    fields = {
        "evidence_ref_id",
        "evidence_class",
        "source_id",
        "source_version",
        "observed_at",
        "historical_validity",
        "current_applicability",
        "review_state",
        "privacy_class",
        "conflict_ref_ids",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    data["conflict_ref_ids"] = _json_tuple(data["conflict_ref_ids"], "conflict_ref_ids")
    return GoalEvidenceReference(**data)


def goal_contract_revision_reference_to_dict(
    reference: GoalContractRevisionReference,
) -> dict[str, Any]:
    _require_type(reference, GoalContractRevisionReference, "reference")
    return {
        "goal_contract_id": reference.goal_contract_id,
        "revision": reference.revision,
        "semantic_hash": reference.semantic_hash,
        "stale_approval_ref_ids": list(reference.stale_approval_ref_ids),
        "stale_validator_ref_ids": list(reference.stale_validator_ref_ids),
        "schema_version": reference.schema_version,
    }


def goal_contract_revision_reference_from_dict(
    payload: Mapping[str, Any],
) -> GoalContractRevisionReference:
    fields = {
        "goal_contract_id",
        "revision",
        "semantic_hash",
        "stale_approval_ref_ids",
        "stale_validator_ref_ids",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    for field_name in ("stale_approval_ref_ids", "stale_validator_ref_ids"):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return GoalContractRevisionReference(**data)


def goal_contract_to_dict(contract: GoalContract) -> dict[str, Any]:
    _require_type(contract, GoalContract, "contract")
    return {
        "goal_contract_id": contract.goal_contract_id,
        "revision": contract.revision,
        "schema_version": contract.schema_version,
        "supersedes_revision": (
            goal_contract_revision_reference_to_dict(contract.supersedes_revision)
            if contract.supersedes_revision is not None
            else None
        ),
        "originating_idea_ids": list(contract.originating_idea_ids),
        "originating_finding_ids": list(contract.originating_finding_ids),
        "problem_classification": contract.problem_classification,
        "observed_problem": contract.observed_problem,
        "desired_outcome": contract.desired_outcome,
        "why_it_matters": contract.why_it_matters,
        "baseline": contract.baseline,
        "expected_result": contract.expected_result,
        "acceptable_result": contract.acceptable_result,
        "maximum_acceptable_regressions": list(
            contract.maximum_acceptable_regressions
        ),
        "root_cause_hypothesis": contract.root_cause_hypothesis,
        "confidence": contract.confidence,
        "proposed_intervention": contract.proposed_intervention,
        "credible_alternatives": list(contract.credible_alternatives),
        "disconfirmation_criteria": list(contract.disconfirmation_criteria),
        "expected_affected_systems": list(contract.expected_affected_systems),
        "expected_unaffected_systems": list(contract.expected_unaffected_systems),
        "dependency_ids": list(contract.dependency_ids),
        "evidence_snapshot": [
            goal_evidence_reference_to_dict(item) for item in contract.evidence_snapshot
        ],
        "privacy_implications": contract.privacy_implications,
        "security_implications": contract.security_implications,
        "zero_cost_validation": contract.zero_cost_validation,
        "manual_burden": contract.manual_burden,
        "operational_burden": contract.operational_burden,
        "size": contract.size,
        "risk": contract.risk,
        "rollback": contract.rollback,
        "rollback_plan": contract.rollback_plan,
        "observation_window": contract.observation_window,
        "if_we_do_nothing": contract.if_we_do_nothing,
        "if_we_do_this": contract.if_we_do_this,
        "historical_attempt_ids": list(contract.historical_attempt_ids),
        "approval_requirements": list(contract.approval_requirements),
        "created_at": contract.created_at,
    }


def goal_contract_from_dict(payload: Mapping[str, Any]) -> GoalContract:
    fields = {
        "goal_contract_id",
        "revision",
        "schema_version",
        "supersedes_revision",
        "originating_idea_ids",
        "originating_finding_ids",
        "problem_classification",
        "observed_problem",
        "desired_outcome",
        "why_it_matters",
        "baseline",
        "expected_result",
        "acceptable_result",
        "maximum_acceptable_regressions",
        "root_cause_hypothesis",
        "confidence",
        "proposed_intervention",
        "credible_alternatives",
        "disconfirmation_criteria",
        "expected_affected_systems",
        "expected_unaffected_systems",
        "dependency_ids",
        "evidence_snapshot",
        "privacy_implications",
        "security_implications",
        "zero_cost_validation",
        "manual_burden",
        "operational_burden",
        "size",
        "risk",
        "rollback",
        "rollback_plan",
        "observation_window",
        "if_we_do_nothing",
        "if_we_do_this",
        "historical_attempt_ids",
        "approval_requirements",
        "created_at",
    }
    data = _require_fields(payload, fields)
    supersedes = data["supersedes_revision"]
    if supersedes is not None:
        data["supersedes_revision"] = goal_contract_revision_reference_from_dict(
            _require_mapping(supersedes, "supersedes_revision")
        )
    for field_name in (
        "originating_idea_ids",
        "originating_finding_ids",
        "maximum_acceptable_regressions",
        "credible_alternatives",
        "disconfirmation_criteria",
        "expected_affected_systems",
        "expected_unaffected_systems",
        "dependency_ids",
        "historical_attempt_ids",
        "approval_requirements",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    evidence_payloads = _json_tuple(data["evidence_snapshot"], "evidence_snapshot")
    data["evidence_snapshot"] = tuple(
        goal_evidence_reference_from_dict(_require_mapping(item, "evidence_snapshot"))
        for item in evidence_payloads
    )
    return GoalContract(**data)


def goal_contract_semantic_hash(contract: GoalContract) -> str:
    return semantic_hash(goal_contract_to_dict(contract))


def validate_goal_contract_revision(
    previous: GoalContract,
    current: GoalContract,
) -> GoalContract:
    _require_type(previous, GoalContract, "previous")
    _require_type(current, GoalContract, "current")
    if previous.goal_contract_id != current.goal_contract_id:
        raise GoalEngineFoundationError(
            "Goal Contract revisions must use the same goal_contract_id"
        )
    if current.revision != previous.revision + 1:
        raise GoalEngineFoundationError(
            "Goal Contract revisions must advance by exactly one revision"
        )
    reference = current.supersedes_revision
    if reference is None:
        raise GoalEngineFoundationError("current revision lacks supersedes_revision")
    if reference.revision != previous.revision:
        raise GoalEngineFoundationError("supersedes_revision revision mismatch")
    if reference.semantic_hash != goal_contract_semantic_hash(previous):
        raise GoalEngineFoundationError(
            "supersedes_revision must preserve the prior semantic hash"
        )
    return current


def goal_policy_reference_to_dict(reference: GoalPolicyReference) -> dict[str, Any]:
    _require_type(reference, GoalPolicyReference, "reference")
    return {
        "policy_id": reference.policy_id,
        "policy_version": reference.policy_version,
        "semantic_hash": reference.semantic_hash,
        "schema_version": reference.schema_version,
    }


def goal_policy_reference_from_dict(
    payload: Mapping[str, Any],
) -> GoalPolicyReference:
    data = _require_fields(
        payload,
        {"policy_id", "policy_version", "semantic_hash", "schema_version"},
    )
    return GoalPolicyReference(**data)


def goal_policy_record_to_dict(record: GoalPolicyRecord) -> dict[str, Any]:
    _require_type(record, GoalPolicyRecord, "record")
    return {
        "policy_id": record.policy_id,
        "policy_version": record.policy_version,
        "schema_version": record.schema_version,
        "date": record.date,
        "reason": record.reason,
        "rule": record.rule,
        "authority_ref_ids": list(record.authority_ref_ids),
        "affected_policy_ids": list(record.affected_policy_ids),
        "superseded_policy_ref": (
            goal_policy_reference_to_dict(record.superseded_policy_ref)
            if record.superseded_policy_ref is not None
            else None
        ),
        "regression_case_ids": list(record.regression_case_ids),
    }


def goal_policy_record_from_dict(payload: Mapping[str, Any]) -> GoalPolicyRecord:
    fields = {
        "policy_id",
        "policy_version",
        "schema_version",
        "date",
        "reason",
        "rule",
        "authority_ref_ids",
        "affected_policy_ids",
        "superseded_policy_ref",
        "regression_case_ids",
    }
    data = _require_fields(payload, fields)
    for field_name in (
        "authority_ref_ids",
        "affected_policy_ids",
        "regression_case_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    superseded = data["superseded_policy_ref"]
    if superseded is not None:
        data["superseded_policy_ref"] = goal_policy_reference_from_dict(
            _require_mapping(superseded, "superseded_policy_ref")
        )
    return GoalPolicyRecord(**data)


def goal_policy_record_semantic_hash(record: GoalPolicyRecord) -> str:
    return semantic_hash(goal_policy_record_to_dict(record))


def goal_policy_registry_to_dict(registry: GoalPolicyRegistry) -> dict[str, Any]:
    validate_goal_policy_registry(registry)
    return {
        "records": [goal_policy_record_to_dict(item) for item in registry.records],
        "schema_version": registry.schema_version,
    }


def goal_policy_registry_from_dict(
    payload: Mapping[str, Any],
) -> GoalPolicyRegistry:
    data = _require_fields(payload, {"records", "schema_version"})
    records = _json_tuple(data["records"], "records")
    data["records"] = tuple(
        goal_policy_record_from_dict(_require_mapping(item, "records"))
        for item in records
    )
    return GoalPolicyRegistry(**data)


def validate_goal_policy_registry(registry: GoalPolicyRegistry) -> GoalPolicyRegistry:
    _require_type(registry, GoalPolicyRegistry, "registry")
    keys = [(item.policy_id, item.policy_version) for item in registry.records]
    duplicates = _duplicates(keys)
    if duplicates:
        policy_id, version = duplicates[0]
        raise GoalEngineFoundationError(
            f"duplicate policy record: {policy_id} version {version}"
        )
    by_key = {
        (item.policy_id, item.policy_version): item for item in registry.records
    }
    known_policy_ids = {item.policy_id for item in registry.records}
    for record in registry.records:
        unknown_affected = sorted(set(record.affected_policy_ids) - known_policy_ids)
        if unknown_affected:
            raise GoalEngineFoundationError(
                f"affected_policy_ids references unknown policy: {unknown_affected[0]}"
            )
        if record.policy_version == 1:
            continue
        reference = record.superseded_policy_ref
        if reference is None:
            raise GoalEngineFoundationError("policy history reference is required")
        prior = by_key.get((reference.policy_id, reference.policy_version))
        if prior is None:
            raise GoalEngineFoundationError(
                "superseded policy record is missing from registry history"
            )
        if reference.semantic_hash != goal_policy_record_semantic_hash(prior):
            raise GoalEngineFoundationError(
                "superseded policy semantic hash does not match history"
            )
    return registry


def lookup_goal_policy(
    registry: GoalPolicyRegistry,
    policy_id: str,
    policy_version: int | None = None,
) -> GoalPolicyRecord:
    validate_goal_policy_registry(registry)
    _require_id(policy_id, "policy_id")
    matches = [item for item in registry.records if item.policy_id == policy_id]
    if not matches:
        raise GoalEngineFoundationError(f"unknown policy_id: {policy_id}")
    if policy_version is None:
        return max(matches, key=lambda item: item.policy_version)
    _require_positive_int(policy_version, "policy_version")
    for item in matches:
        if item.policy_version == policy_version:
            return item
    raise GoalEngineFoundationError(
        f"unknown policy version: {policy_id} version {policy_version}"
    )


def goal_lineage_event_to_dict(event: GoalLineageEvent) -> dict[str, Any]:
    _require_type(event, GoalLineageEvent, "event")
    if event.event_hash != _lineage_event_expected_hash(event):
        raise GoalEngineFoundationError("event_hash does not match event semantics")
    return _lineage_event_dict(event, include_hash=True)


def goal_lineage_event_from_dict(payload: Mapping[str, Any]) -> GoalLineageEvent:
    fields = {
        "event_id",
        "schema_version",
        "entity_kind",
        "entity_id",
        "entity_revision",
        "event_kind",
        "occurred_at",
        "actor_kind",
        "summary",
        "evidence_ref_ids",
        "human_decision_ref_ids",
        "authority_ref_ids",
        "prior_event_ids",
        "prior_event_hashes",
        "event_hash",
    }
    data = _require_fields(payload, fields)
    for field_name in (
        "evidence_ref_ids",
        "human_decision_ref_ids",
        "authority_ref_ids",
        "prior_event_ids",
        "prior_event_hashes",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    if not data["event_hash"]:
        raise GoalEngineFoundationError("event_hash is required in serialized lineage")
    return GoalLineageEvent(**data)


def validate_goal_lineage_chain(
    events: tuple[GoalLineageEvent, ...],
) -> tuple[GoalLineageEvent, ...]:
    if not isinstance(events, tuple):
        raise GoalEngineFoundationError("events must be a tuple")
    event_ids: list[str] = []
    seen: dict[str, GoalLineageEvent] = {}
    previous_timestamp: datetime | None = None
    for event in events:
        _require_type(event, GoalLineageEvent, "event")
        if event.event_hash != _lineage_event_expected_hash(event):
            raise GoalEngineFoundationError("lineage contains an invalid event_hash")
        event_ids.append(event.event_id)
        current_timestamp = _parse_utc_timestamp(event.occurred_at, "occurred_at")
        if previous_timestamp is not None and current_timestamp < previous_timestamp:
            raise GoalEngineFoundationError(
                "lineage events must be supplied in append-only time order"
            )
        previous_timestamp = current_timestamp
        for prior_id, prior_hash in zip(
            event.prior_event_ids,
            event.prior_event_hashes,
            strict=True,
        ):
            prior = seen.get(prior_id)
            if prior is None:
                raise GoalEngineFoundationError(
                    f"prior event must already exist in lineage: {prior_id}"
                )
            if prior.event_hash != prior_hash:
                raise GoalEngineFoundationError(
                    f"prior event hash mismatch: {prior_id}"
                )
        seen[event.event_id] = event
    duplicates = _duplicates(event_ids)
    if duplicates:
        raise GoalEngineFoundationError(f"duplicate event_id: {duplicates[0]}")
    return events


def canonical_json_bytes(payload: Mapping[str, Any]) -> bytes:
    mapping = _require_mapping(payload, "payload")
    try:
        serialized = json.dumps(
            mapping,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise GoalEngineFoundationError(
            "payload must contain only canonical JSON values"
        ) from exc
    return serialized.encode("utf-8")


def semantic_hash(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def _identifier_to_dict(
    identifier: GoalIdentifier | IdeaIdentifier | FindingIdentifier,
) -> dict[str, Any]:
    return {
        "entity_kind": identifier.entity_kind,
        "local_id": identifier.local_id,
        "schema_version": identifier.schema_version,
    }


def _validate_supersedes_revision(contract: GoalContract) -> None:
    reference = contract.supersedes_revision
    if contract.revision == 1:
        if reference is not None:
            raise GoalEngineFoundationError(
                "Goal Contract revision 1 cannot supersede an earlier revision"
            )
        return
    if not isinstance(reference, GoalContractRevisionReference):
        raise GoalEngineFoundationError(
            "later Goal Contract revisions require supersedes_revision"
        )
    if reference.goal_contract_id != contract.goal_contract_id:
        raise GoalEngineFoundationError(
            "supersedes_revision must use the same goal_contract_id"
        )
    if reference.revision != contract.revision - 1:
        raise GoalEngineFoundationError(
            "supersedes_revision must identify the immediately prior revision"
        )


def _evidence_reference_tuple(
    values: tuple[GoalEvidenceReference, ...],
) -> tuple[GoalEvidenceReference, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineFoundationError("evidence_snapshot must be a tuple")
    for item in values:
        if not isinstance(item, GoalEvidenceReference):
            raise GoalEngineFoundationError(
                "evidence_snapshot must contain GoalEvidenceReference values"
            )
    sorted_values = tuple(sorted(values, key=lambda item: item.evidence_ref_id))
    duplicates = _duplicates([item.evidence_ref_id for item in sorted_values])
    if duplicates:
        raise GoalEngineFoundationError(
            f"duplicate evidence_ref_id: {duplicates[0]}"
        )
    return sorted_values


def _lineage_event_expected_hash(event: GoalLineageEvent) -> str:
    return semantic_hash(_lineage_event_dict(event, include_hash=False))


def _lineage_event_dict(
    event: GoalLineageEvent,
    *,
    include_hash: bool,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "event_id": event.event_id,
        "schema_version": event.schema_version,
        "entity_kind": event.entity_kind,
        "entity_id": event.entity_id,
        "entity_revision": event.entity_revision,
        "event_kind": event.event_kind,
        "occurred_at": event.occurred_at,
        "actor_kind": event.actor_kind,
        "summary": event.summary,
        "evidence_ref_ids": list(event.evidence_ref_ids),
        "human_decision_ref_ids": list(event.human_decision_ref_ids),
        "authority_ref_ids": list(event.authority_ref_ids),
        "prior_event_ids": list(event.prior_event_ids),
        "prior_event_hashes": list(event.prior_event_hashes),
    }
    if include_hash:
        payload["event_hash"] = event.event_hash
    return payload


def _prior_event_tuples(
    event_ids: tuple[str, ...],
    event_hashes: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(event_ids, tuple) or not isinstance(event_hashes, tuple):
        raise GoalEngineFoundationError(
            "prior_event_ids and prior_event_hashes must be tuples"
        )
    if len(event_ids) != len(event_hashes):
        raise GoalEngineFoundationError(
            "prior_event_ids and prior_event_hashes must have equal length"
        )
    pairs: list[tuple[str, str]] = []
    for event_id, event_hash in zip(event_ids, event_hashes, strict=True):
        _require_id(event_id, "prior_event_ids")
        _require_sha256(event_hash, "prior_event_hashes")
        pairs.append((event_id, event_hash))
    duplicate_ids = _duplicates([item[0] for item in pairs])
    if duplicate_ids:
        raise GoalEngineFoundationError(
            f"duplicate prior event ID: {duplicate_ids[0]}"
        )
    pairs.sort(key=lambda item: item[0])
    return tuple(item[0] for item in pairs), tuple(item[1] for item in pairs)


def _require_fields(
    payload: Mapping[str, Any],
    fields: set[str],
) -> dict[str, Any]:
    mapping = _require_mapping(payload, "payload")
    keys = set(mapping)
    forbidden = sorted(keys & _FORBIDDEN_FIELD_NAMES)
    if forbidden:
        raise GoalEngineFoundationError(
            f"payload contains forbidden field: {forbidden[0]}"
        )
    missing = sorted(fields - keys)
    if missing:
        raise GoalEngineFoundationError(f"payload missing required field: {missing[0]}")
    extra = sorted(keys - fields)
    if extra:
        raise GoalEngineFoundationError(f"payload contains unknown field: {extra[0]}")
    return dict(mapping)


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GoalEngineFoundationError(f"{field_name} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise GoalEngineFoundationError(f"{field_name} keys must be strings")
    return value


def _json_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise GoalEngineFoundationError(f"{field_name} must be an array")
    return tuple(value)


def _id_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineFoundationError(f"{field_name} must be a tuple")
    validated = tuple(_require_id(item, field_name) for item in values)
    duplicates = _duplicates(list(validated))
    if duplicates:
        raise GoalEngineFoundationError(
            f"{field_name} contains duplicate ID: {duplicates[0]}"
        )
    return tuple(sorted(validated)) if sort else validated


def _text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineFoundationError(f"{field_name} must be a tuple")
    validated = tuple(_require_text(item, field_name) for item in values)
    duplicates = _duplicates(list(validated))
    if duplicates:
        raise GoalEngineFoundationError(
            f"{field_name} contains duplicate value: {duplicates[0]}"
        )
    return validated


def _require_allowed(value: Any, allowed: frozenset[str], field_name: str) -> str:
    text = _require_text(value, field_name)
    if text not in allowed:
        raise GoalEngineFoundationError(f"unsupported {field_name}: {text}")
    return text


def _require_exact(value: Any, expected: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    if text != expected:
        raise GoalEngineFoundationError(f"{field_name} must be {expected}")
    return text


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise GoalEngineFoundationError(
            f"{field_name} must be non-empty text without surrounding whitespace"
        )
    return value


def _require_label(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if len(text) > 128 or any(ord(character) < 32 for character in text):
        raise GoalEngineFoundationError(f"{field_name} is not a valid governance label")
    return text


def _require_id(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _ID_PATTERN.fullmatch(text):
        raise GoalEngineFoundationError(
            f"{field_name} must be a stable local identifier"
        )
    return text


def _require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GoalEngineFoundationError(f"{field_name} must be a positive integer")
    return value


def _require_ratio(value: Any, field_name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise GoalEngineFoundationError(f"{field_name} must be numeric")
    if value < 0 or value > 1:
        raise GoalEngineFoundationError(f"{field_name} must be between 0 and 1")
    return float(value)


def _require_schema(value: Any, expected: str) -> str:
    return _require_exact(value, expected, "schema_version")


def _require_sha256(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _SHA256_PATTERN.fullmatch(text):
        raise GoalEngineFoundationError(
            f"{field_name} must be a lowercase SHA-256 hex digest"
        )
    return text


def _require_date(value: Any, field_name: str) -> date:
    text = _require_text(value, field_name)
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise GoalEngineFoundationError(f"{field_name} must be an ISO date") from exc
    if parsed.isoformat() != text:
        raise GoalEngineFoundationError(f"{field_name} must use YYYY-MM-DD")
    return parsed


def _parse_utc_timestamp(value: Any, field_name: str) -> datetime:
    text = _require_text(value, field_name)
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise GoalEngineFoundationError(
            f"{field_name} must be an ISO-8601 UTC timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise GoalEngineFoundationError(f"{field_name} must be UTC")
    return parsed


def _require_utc_timestamp(value: Any, field_name: str) -> str:
    _parse_utc_timestamp(value, field_name)
    return str(value)


def _require_type(value: Any, expected_type: type, field_name: str) -> None:
    if not isinstance(value, expected_type):
        raise GoalEngineFoundationError(
            f"{field_name} must be {expected_type.__name__}"
        )


def _duplicates(values: list[Any]) -> list[Any]:
    seen: set[Any] = set()
    duplicates: list[Any] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return duplicates
