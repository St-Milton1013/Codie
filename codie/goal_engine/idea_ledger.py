"""Pure, deterministic Findings + Idea Ledger records for Goal Engine v1.

The ledger preserves caller-supplied Findings, Ideas, occurrences, relations,
reconsideration requests, and append-only history.  It performs no discovery,
persistence, similarity inference, work selection, Goal creation, or authority
transition.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from .foundation import (
    FindingIdentifier,
    GoalEvidenceReference,
    IdeaIdentifier,
    finding_identifier_from_dict,
    finding_identifier_to_dict,
    goal_evidence_reference_from_dict,
    goal_evidence_reference_to_dict,
    idea_identifier_from_dict,
    idea_identifier_to_dict,
    semantic_hash,
)

LEDGER_FINDING_SCHEMA_VERSION = "codie.goal_engine.ledger_finding.v1"
IDEA_RECORD_SCHEMA_VERSION = "codie.goal_engine.idea_record.v1"
IDEA_OCCURRENCE_SCHEMA_VERSION = "codie.goal_engine.idea_occurrence.v1"
LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.ledger_entity_reference.v1"
)
LEDGER_RELATION_SCHEMA_VERSION = "codie.goal_engine.ledger_relation.v1"
RECONSIDERATION_TRIGGER_SCHEMA_VERSION = (
    "codie.goal_engine.reconsideration_trigger.v1"
)
RECONSIDERATION_REQUEST_SCHEMA_VERSION = (
    "codie.goal_engine.reconsideration_request.v1"
)
LEDGER_HISTORY_EVENT_SCHEMA_VERSION = (
    "codie.goal_engine.ledger_history_event.v1"
)
LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.ledger_snapshot_reference.v1"
)
FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION = (
    "codie.goal_engine.findings_idea_ledger_snapshot.v1"
)

IDEA_STATES = frozenset(
    {
        "UNTRIAGED",
        "NOTE",
        "CONDITIONAL",
        "WATCHING",
        "NEEDS_RESEARCH",
        "INVESTIGATION_CANDIDATE",
        "GOAL_CANDIDATE",
        "POLICY_IDEA",
        "ARCHIVED_CONDITIONAL",
    }
)
FINDING_ORIGINS = frozenset(
    {
        "HEALTH_FINDING",
        "RESEARCH_FINDING",
        "OPERATIONAL_FINDING",
        "HUMAN_REVIEW_FINDING",
    }
)
RELATION_TYPES = frozenset(
    {
        "duplicate",
        "extension",
        "alternative",
        "contradiction",
        "dependency",
        "related",
    }
)
LEDGER_ENTITY_KINDS = frozenset(
    {
        "IDEA",
        "FINDING",
        "GOAL",
        "FAILED_WORK",
        "REWIND",
        "CONDITIONAL_OPPORTUNITY",
    }
)
TRIGGER_KINDS = frozenset(
    {
        "EVIDENCE_CHANGE",
        "DEPENDENCY_CHANGE",
        "RECURRENCE_THRESHOLD",
        "CONTEXT_CHANGE",
        "POLICY_CHANGE",
        "TIME_WINDOW",
        "HUMAN_REQUEST",
    }
)
HISTORY_EVENT_KINDS = frozenset(
    {
        "FINDING_ADMITTED",
        "IDEA_CAPTURED",
        "IDEA_REVISED",
        "IDEA_CLASSIFIED",
        "OCCURRENCE_RECORDED",
        "RELATION_RECORDED",
        "TRIGGER_DEFINED",
        "RECONSIDERATION_REQUESTED",
        "GOAL_LINK_RECORDED",
        "ARCHIVED_CONDITIONAL",
    }
)
SENSITIVITY_VALUES = frozenset(
    {
        "PUBLIC_REFERENCE",
        "PROJECT_INTERNAL",
        "USER_PRIVATE",
        "DECK_PRIVATE",
        "SECRET_REFERENCE",
    }
)

_PRIVATE_SENSITIVITIES = frozenset({"USER_PRIVATE", "DECK_PRIVATE"})
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
        "raw_content",
        "raw_payload",
        "secret",
        "session",
        "session_id",
        "token",
    }
)
_SECRET_MARKERS = (
    "-----begin private key-----",
    "api_key=",
    "api-key:",
    "access_token=",
    "password=",
    "password:",
    "session_cookie=",
    "bearer ey",
)


class GoalEngineIdeaLedgerError(ValueError):
    """Raised when a Findings + Idea Ledger value violates its contract."""


@dataclass(frozen=True)
class LedgerFinding:
    finding_id: FindingIdentifier
    origin: str
    statement: str
    why_it_matters: str
    source_record_ref_id: str
    source_record_semantic_hash: str
    evidence_ref_ids: tuple[str, ...]
    conflict_ref_ids: tuple[str, ...]
    confidence: float
    disconfirmation_criteria: tuple[str, ...]
    limitations: tuple[str, ...]
    observed_at: str
    recorded_at: str
    sensitivity: str
    owner_ref_id: str | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_type(self.finding_id, FindingIdentifier, "finding_id")
        validate_finding_origin(self.origin)
        _require_safe_text(self.statement, "statement")
        _require_safe_text(self.why_it_matters, "why_it_matters")
        _require_id(self.source_record_ref_id, "source_record_ref_id")
        _require_sha256(
            self.source_record_semantic_hash,
            "source_record_semantic_hash",
        )
        evidence = _id_tuple(self.evidence_ref_ids, "evidence_ref_ids", sort=True)
        conflicts = _id_tuple(self.conflict_ref_ids, "conflict_ref_ids", sort=True)
        if not evidence and not conflicts:
            raise GoalEngineIdeaLedgerError(
                "a ledger Finding requires evidence or conflict references"
            )
        if set(evidence) & set(conflicts):
            raise GoalEngineIdeaLedgerError(
                "supporting and conflicting evidence must remain disjoint"
            )
        object.__setattr__(self, "evidence_ref_ids", evidence)
        object.__setattr__(self, "conflict_ref_ids", conflicts)
        object.__setattr__(self, "confidence", _require_ratio(self.confidence, "confidence"))
        object.__setattr__(
            self,
            "disconfirmation_criteria",
            _text_tuple(
                self.disconfirmation_criteria,
                "disconfirmation_criteria",
                require_nonempty=True,
            ),
        )
        object.__setattr__(
            self,
            "limitations",
            _text_tuple(self.limitations, "limitations", require_nonempty=True),
        )
        observed = _parse_utc_timestamp(self.observed_at, "observed_at")
        recorded = _parse_utc_timestamp(self.recorded_at, "recorded_at")
        if recorded < observed:
            raise GoalEngineIdeaLedgerError(
                "recorded_at cannot precede observed_at"
            )
        validate_sensitivity(self.sensitivity)
        _validate_owner(self.sensitivity, self.owner_ref_id)
        _require_schema(self.schema_version, LEDGER_FINDING_SCHEMA_VERSION)


@dataclass(frozen=True)
class IdeaRecord:
    idea_id: IdeaIdentifier
    revision: int
    original_wording: str
    current_summary: str
    state: str
    origin_ref_ids: tuple[str, ...]
    finding_ref_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    occurrence_ids: tuple[str, ...]
    trigger_ids: tuple[str, ...]
    human_decision_ref_ids: tuple[str, ...]
    policy_ref_ids: tuple[str, ...]
    created_at: str
    updated_at: str
    sensitivity: str
    owner_ref_id: str | None
    supersedes_idea_hash: str | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_type(self.idea_id, IdeaIdentifier, "idea_id")
        _require_positive_int(self.revision, "revision")
        _require_original_wording(self.original_wording)
        _require_safe_text(self.current_summary, "current_summary")
        validate_idea_state(self.state)
        object.__setattr__(
            self,
            "origin_ref_ids",
            _id_tuple(
                self.origin_ref_ids,
                "origin_ref_ids",
                sort=True,
                require_nonempty=True,
            ),
        )
        for field_name in (
            "finding_ref_ids",
            "relation_ids",
            "occurrence_ids",
            "trigger_ids",
            "human_decision_ref_ids",
            "policy_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        if set(self.human_decision_ref_ids) & set(self.policy_ref_ids):
            raise GoalEngineIdeaLedgerError(
                "human-decision and policy references must remain disjoint"
            )
        created = _parse_utc_timestamp(self.created_at, "created_at")
        updated = _parse_utc_timestamp(self.updated_at, "updated_at")
        if updated < created:
            raise GoalEngineIdeaLedgerError("updated_at cannot precede created_at")
        validate_sensitivity(self.sensitivity)
        _validate_owner(self.sensitivity, self.owner_ref_id)
        if self.revision == 1:
            if self.supersedes_idea_hash is not None:
                raise GoalEngineIdeaLedgerError(
                    "Idea revision 1 cannot supersede an earlier revision"
                )
        else:
            _require_sha256(self.supersedes_idea_hash, "supersedes_idea_hash")
        if self.state == "ARCHIVED_CONDITIONAL" and not self.trigger_ids:
            raise GoalEngineIdeaLedgerError(
                "ARCHIVED_CONDITIONAL requires a reconsideration trigger"
            )
        _require_schema(self.schema_version, IDEA_RECORD_SCHEMA_VERSION)


@dataclass(frozen=True)
class IdeaOccurrence:
    occurrence_id: str
    idea_id: IdeaIdentifier
    occurred_at: str
    context_summary: str
    source_ref_ids: tuple[str, ...]
    evidence_ref_ids: tuple[str, ...]
    sensitivity: str
    owner_ref_id: str | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.occurrence_id, "occurrence_id")
        _require_type(self.idea_id, IdeaIdentifier, "idea_id")
        _require_utc_timestamp(self.occurred_at, "occurred_at")
        _require_safe_text(self.context_summary, "context_summary")
        object.__setattr__(
            self,
            "source_ref_ids",
            _id_tuple(
                self.source_ref_ids,
                "source_ref_ids",
                sort=True,
                require_nonempty=True,
            ),
        )
        object.__setattr__(
            self,
            "evidence_ref_ids",
            _id_tuple(self.evidence_ref_ids, "evidence_ref_ids", sort=True),
        )
        validate_sensitivity(self.sensitivity)
        _validate_owner(self.sensitivity, self.owner_ref_id)
        _require_schema(self.schema_version, IDEA_OCCURRENCE_SCHEMA_VERSION)


@dataclass(frozen=True)
class LedgerEntityReference:
    entity_kind: str
    entity_id: str
    revision: int | None
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        validate_ledger_entity_kind(self.entity_kind)
        _require_id(self.entity_id, "entity_id")
        if self.revision is not None:
            _require_positive_int(self.revision, "revision")
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(
            self.schema_version,
            LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class LedgerRelation:
    relation_id: str
    source: LedgerEntityReference
    target: LedgerEntityReference
    relation_type: str
    basis_ref_ids: tuple[str, ...]
    confidence: float
    limitations: tuple[str, ...]
    created_at: str
    created_by_ref_id: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.relation_id, "relation_id")
        _require_type(self.source, LedgerEntityReference, "source")
        _require_type(self.target, LedgerEntityReference, "target")
        if _entity_reference_key(self.source) == _entity_reference_key(self.target):
            raise GoalEngineIdeaLedgerError(
                "relation source and target must be distinct"
            )
        validate_relation_type(self.relation_type)
        object.__setattr__(
            self,
            "basis_ref_ids",
            _id_tuple(
                self.basis_ref_ids,
                "basis_ref_ids",
                sort=True,
                require_nonempty=True,
            ),
        )
        object.__setattr__(self, "confidence", _require_ratio(self.confidence, "confidence"))
        object.__setattr__(
            self,
            "limitations",
            _text_tuple(self.limitations, "limitations", require_nonempty=True),
        )
        _require_utc_timestamp(self.created_at, "created_at")
        _require_id(self.created_by_ref_id, "created_by_ref_id")
        _require_schema(self.schema_version, LEDGER_RELATION_SCHEMA_VERSION)


@dataclass(frozen=True)
class ReconsiderationTrigger:
    trigger_id: str
    idea_id: IdeaIdentifier
    trigger_kind: str
    condition_summary: str
    required_evidence_classes: tuple[str, ...]
    recurrence_threshold: int | None
    not_before: str | None
    expires_at: str | None
    created_at: str
    created_by_ref_id: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.trigger_id, "trigger_id")
        _require_type(self.idea_id, IdeaIdentifier, "idea_id")
        validate_trigger_kind(self.trigger_kind)
        _require_safe_text(self.condition_summary, "condition_summary")
        object.__setattr__(
            self,
            "required_evidence_classes",
            _label_tuple(
                self.required_evidence_classes,
                "required_evidence_classes",
                sort=True,
            ),
        )
        if self.trigger_kind == "RECURRENCE_THRESHOLD":
            _require_positive_int(self.recurrence_threshold, "recurrence_threshold")
        elif self.recurrence_threshold is not None:
            raise GoalEngineIdeaLedgerError(
                "only RECURRENCE_THRESHOLD may use recurrence_threshold"
            )
        created = _parse_utc_timestamp(self.created_at, "created_at")
        if self.trigger_kind == "TIME_WINDOW" and self.not_before is None:
            raise GoalEngineIdeaLedgerError("TIME_WINDOW requires not_before")
        not_before = (
            _parse_utc_timestamp(self.not_before, "not_before")
            if self.not_before is not None
            else None
        )
        expires = (
            _parse_utc_timestamp(self.expires_at, "expires_at")
            if self.expires_at is not None
            else None
        )
        if expires is not None and expires < created:
            raise GoalEngineIdeaLedgerError("expires_at cannot precede created_at")
        if not_before is not None and expires is not None and expires < not_before:
            raise GoalEngineIdeaLedgerError("expires_at cannot precede not_before")
        _require_id(self.created_by_ref_id, "created_by_ref_id")
        _require_schema(
            self.schema_version,
            RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class ReconsiderationRequest:
    request_id: str
    idea_id: IdeaIdentifier
    idea_revision: int
    trigger_id: str
    as_of: str
    evidence_ref_ids: tuple[str, ...]
    occurrence_ids: tuple[str, ...]
    human_request_ref_ids: tuple[str, ...]
    limitations: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.request_id, "request_id")
        _require_type(self.idea_id, IdeaIdentifier, "idea_id")
        _require_positive_int(self.idea_revision, "idea_revision")
        _require_id(self.trigger_id, "trigger_id")
        _require_utc_timestamp(self.as_of, "as_of")
        for field_name in (
            "evidence_ref_ids",
            "occurrence_ids",
            "human_request_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        if not self.evidence_ref_ids and not self.occurrence_ids and not self.human_request_ref_ids:
            raise GoalEngineIdeaLedgerError(
                "reconsideration requires evidence, occurrences, or a human request"
            )
        object.__setattr__(
            self,
            "limitations",
            _text_tuple(self.limitations, "limitations", require_nonempty=True),
        )
        _require_schema(
            self.schema_version,
            RECONSIDERATION_REQUEST_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class LedgerHistoryEvent:
    event_id: str
    event_kind: str
    entity: LedgerEntityReference
    related_ref_ids: tuple[str, ...]
    evidence_ref_ids: tuple[str, ...]
    human_decision_ref_ids: tuple[str, ...]
    policy_ref_ids: tuple[str, ...]
    statement: str
    created_at: str
    prior_event_hash: str | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.event_id, "event_id")
        validate_history_event_kind(self.event_kind)
        _require_type(self.entity, LedgerEntityReference, "entity")
        for field_name in (
            "related_ref_ids",
            "evidence_ref_ids",
            "human_decision_ref_ids",
            "policy_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        reference_sets = (
            set(self.evidence_ref_ids),
            set(self.human_decision_ref_ids),
            set(self.policy_ref_ids),
        )
        if any(
            reference_sets[left] & reference_sets[right]
            for left, right in ((0, 1), (0, 2), (1, 2))
        ):
            raise GoalEngineIdeaLedgerError(
                "evidence, human-decision, and policy references must remain disjoint"
            )
        _require_safe_text(self.statement, "statement")
        _require_utc_timestamp(self.created_at, "created_at")
        if self.prior_event_hash is not None:
            _require_sha256(self.prior_event_hash, "prior_event_hash")
        _require_schema(self.schema_version, LEDGER_HISTORY_EVENT_SCHEMA_VERSION)


@dataclass(frozen=True)
class LedgerSnapshotReference:
    snapshot_id: str
    revision: int
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.snapshot_id, "snapshot_id")
        _require_positive_int(self.revision, "revision")
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(
            self.schema_version,
            LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class FindingsIdeaLedgerSnapshot:
    snapshot_id: str
    revision: int
    ledger_scope_id: str
    as_of: str
    findings: tuple[LedgerFinding, ...]
    ideas: tuple[IdeaRecord, ...]
    occurrences: tuple[IdeaOccurrence, ...]
    relations: tuple[LedgerRelation, ...]
    triggers: tuple[ReconsiderationTrigger, ...]
    reconsideration_requests: tuple[ReconsiderationRequest, ...]
    history_events: tuple[LedgerHistoryEvent, ...]
    evidence_snapshot: tuple[GoalEvidenceReference, ...]
    external_entity_references: tuple[LedgerEntityReference, ...]
    supersedes_snapshot: LedgerSnapshotReference | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.snapshot_id, "snapshot_id")
        _require_positive_int(self.revision, "revision")
        _require_id(self.ledger_scope_id, "ledger_scope_id")
        _require_utc_timestamp(self.as_of, "as_of")
        object.__setattr__(
            self,
            "findings",
            _record_tuple(
                self.findings,
                LedgerFinding,
                "findings",
                lambda item: item.finding_id.local_id,
            ),
        )
        object.__setattr__(
            self,
            "ideas",
            _record_tuple(
                self.ideas,
                IdeaRecord,
                "ideas",
                lambda item: item.idea_id.local_id,
            ),
        )
        object.__setattr__(
            self,
            "occurrences",
            _record_tuple(
                self.occurrences,
                IdeaOccurrence,
                "occurrences",
                lambda item: item.occurrence_id,
            ),
        )
        object.__setattr__(
            self,
            "relations",
            _record_tuple(
                self.relations,
                LedgerRelation,
                "relations",
                lambda item: item.relation_id,
            ),
        )
        object.__setattr__(
            self,
            "triggers",
            _record_tuple(
                self.triggers,
                ReconsiderationTrigger,
                "triggers",
                lambda item: item.trigger_id,
            ),
        )
        object.__setattr__(
            self,
            "reconsideration_requests",
            _record_tuple(
                self.reconsideration_requests,
                ReconsiderationRequest,
                "reconsideration_requests",
                lambda item: item.request_id,
            ),
        )
        object.__setattr__(
            self,
            "history_events",
            _record_tuple(
                self.history_events,
                LedgerHistoryEvent,
                "history_events",
                lambda item: item.event_id,
                order=lambda item: (item.created_at, item.event_id),
            ),
        )
        object.__setattr__(
            self,
            "evidence_snapshot",
            _record_tuple(
                self.evidence_snapshot,
                GoalEvidenceReference,
                "evidence_snapshot",
                lambda item: item.evidence_ref_id,
            ),
        )
        object.__setattr__(
            self,
            "external_entity_references",
            _record_tuple(
                self.external_entity_references,
                LedgerEntityReference,
                "external_entity_references",
                _entity_reference_key,
            ),
        )
        if self.revision == 1:
            if self.supersedes_snapshot is not None:
                raise GoalEngineIdeaLedgerError(
                    "ledger revision 1 cannot supersede an earlier snapshot"
                )
        elif not isinstance(self.supersedes_snapshot, LedgerSnapshotReference):
            raise GoalEngineIdeaLedgerError(
                "later ledger revisions require supersedes_snapshot"
            )
        _require_schema(
            self.schema_version,
            FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION,
        )
        validate_ledger_snapshot(self)


def validate_idea_state(value: str) -> str:
    return _require_allowed(value, IDEA_STATES, "Idea state")


def validate_finding_origin(value: str) -> str:
    return _require_allowed(value, FINDING_ORIGINS, "Finding origin")


def validate_relation_type(value: str) -> str:
    return _require_allowed(value, RELATION_TYPES, "relation type")


def validate_ledger_entity_kind(value: str) -> str:
    return _require_allowed(value, LEDGER_ENTITY_KINDS, "ledger entity kind")


def validate_trigger_kind(value: str) -> str:
    return _require_allowed(value, TRIGGER_KINDS, "trigger kind")


def validate_history_event_kind(value: str) -> str:
    return _require_allowed(value, HISTORY_EVENT_KINDS, "history event kind")


def validate_sensitivity(value: str) -> str:
    return _require_allowed(value, SENSITIVITY_VALUES, "sensitivity")


def validate_ledger_finding(finding: LedgerFinding) -> LedgerFinding:
    _require_type(finding, LedgerFinding, "finding")
    return finding


def validate_idea_record(idea: IdeaRecord) -> IdeaRecord:
    _require_type(idea, IdeaRecord, "idea")
    return idea


def validate_idea_revision(idea: IdeaRecord, prior_idea: IdeaRecord) -> IdeaRecord:
    validate_idea_record(idea)
    validate_idea_record(prior_idea)
    if idea.idea_id != prior_idea.idea_id:
        raise GoalEngineIdeaLedgerError("Idea revision must retain idea_id")
    if idea.revision != prior_idea.revision + 1:
        raise GoalEngineIdeaLedgerError(
            "Idea revision must immediately follow the prior revision"
        )
    if idea.original_wording != prior_idea.original_wording:
        raise GoalEngineIdeaLedgerError(
            "Idea original_wording is immutable across revisions"
        )
    if idea.created_at != prior_idea.created_at:
        raise GoalEngineIdeaLedgerError(
            "Idea created_at is immutable across revisions"
        )
    if idea.sensitivity != prior_idea.sensitivity:
        raise GoalEngineIdeaLedgerError(
            "Idea sensitivity is immutable across revisions"
        )
    if idea.owner_ref_id != prior_idea.owner_ref_id:
        raise GoalEngineIdeaLedgerError(
            "Idea owner_ref_id is immutable across revisions"
        )
    if _parse_utc_timestamp(idea.updated_at, "updated_at") < _parse_utc_timestamp(
        prior_idea.updated_at,
        "prior updated_at",
    ):
        raise GoalEngineIdeaLedgerError(
            "Idea updated_at cannot move backwards"
        )
    expected_hash = idea_record_semantic_hash(prior_idea)
    if idea.supersedes_idea_hash != expected_hash:
        raise GoalEngineIdeaLedgerError(
            "supersedes_idea_hash does not match the prior Idea"
        )
    return idea


def validate_ledger_snapshot(
    snapshot: FindingsIdeaLedgerSnapshot,
) -> FindingsIdeaLedgerSnapshot:
    _require_type(snapshot, FindingsIdeaLedgerSnapshot, "snapshot")
    as_of = _parse_utc_timestamp(snapshot.as_of, "as_of")
    evidence_by_id = {
        item.evidence_ref_id: item for item in snapshot.evidence_snapshot
    }
    _validate_evidence_conflicts(evidence_by_id)
    finding_by_id = {item.finding_id.local_id: item for item in snapshot.findings}
    idea_by_id = {item.idea_id.local_id: item for item in snapshot.ideas}
    occurrence_by_id = {item.occurrence_id: item for item in snapshot.occurrences}
    relation_by_id = {item.relation_id: item for item in snapshot.relations}
    trigger_by_id = {item.trigger_id: item for item in snapshot.triggers}
    entity_by_key = _snapshot_entity_references(snapshot)
    reference_counts = _reference_id_counts(snapshot, entity_by_key)

    for finding in snapshot.findings:
        _validate_finding_references(finding, evidence_by_id, entity_by_key, as_of)
    for idea in snapshot.ideas:
        _validate_idea_references(
            idea,
            finding_by_id,
            occurrence_by_id,
            relation_by_id,
            trigger_by_id,
            reference_counts,
            as_of,
        )
    for occurrence in snapshot.occurrences:
        _validate_occurrence(
            occurrence,
            idea_by_id,
            evidence_by_id,
            reference_counts,
            as_of,
        )
    for relation in snapshot.relations:
        _validate_relation(
            relation,
            entity_by_key,
            idea_by_id,
            finding_by_id,
            reference_counts,
            as_of,
        )
    for trigger in snapshot.triggers:
        _validate_trigger(trigger, idea_by_id, as_of)
    for request in snapshot.reconsideration_requests:
        _validate_reconsideration_request(
            request,
            idea_by_id,
            trigger_by_id,
            occurrence_by_id,
            evidence_by_id,
            reference_counts,
            as_of,
        )
    _validate_history(
        snapshot.history_events,
        entity_by_key,
        evidence_by_id,
        reference_counts,
        as_of,
    )
    _validate_history_coverage(snapshot)
    return snapshot


def validate_ledger_snapshot_revision(
    snapshot: FindingsIdeaLedgerSnapshot,
    prior_snapshot: FindingsIdeaLedgerSnapshot,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    validate_ledger_snapshot(prior_snapshot)
    if snapshot.snapshot_id != prior_snapshot.snapshot_id:
        raise GoalEngineIdeaLedgerError(
            "ledger revision must retain snapshot_id"
        )
    if snapshot.ledger_scope_id != prior_snapshot.ledger_scope_id:
        raise GoalEngineIdeaLedgerError(
            "ledger revision must retain ledger_scope_id"
        )
    if snapshot.revision != prior_snapshot.revision + 1:
        raise GoalEngineIdeaLedgerError(
            "ledger revision must immediately follow the prior snapshot"
        )
    if _parse_utc_timestamp(snapshot.as_of, "as_of") < _parse_utc_timestamp(
        prior_snapshot.as_of,
        "prior as_of",
    ):
        raise GoalEngineIdeaLedgerError("ledger as_of cannot move backwards")
    reference = snapshot.supersedes_snapshot
    if reference is None:
        raise GoalEngineIdeaLedgerError(
            "later ledger revision requires supersedes_snapshot"
        )
    if reference.snapshot_id != prior_snapshot.snapshot_id:
        raise GoalEngineIdeaLedgerError(
            "supersedes_snapshot must retain snapshot_id"
        )
    if reference.revision != prior_snapshot.revision:
        raise GoalEngineIdeaLedgerError(
            "supersedes_snapshot must identify the prior revision"
        )
    if reference.semantic_hash != findings_idea_ledger_snapshot_semantic_hash(
        prior_snapshot
    ):
        raise GoalEngineIdeaLedgerError(
            "supersedes_snapshot semantic hash does not match the prior snapshot"
        )
    _validate_append_only_snapshot(snapshot, prior_snapshot)
    return snapshot


def ledger_finding_to_dict(finding: LedgerFinding) -> dict[str, Any]:
    validate_ledger_finding(finding)
    return {
        "finding_id": finding_identifier_to_dict(finding.finding_id),
        "origin": finding.origin,
        "statement": finding.statement,
        "why_it_matters": finding.why_it_matters,
        "source_record_ref_id": finding.source_record_ref_id,
        "source_record_semantic_hash": finding.source_record_semantic_hash,
        "evidence_ref_ids": list(finding.evidence_ref_ids),
        "conflict_ref_ids": list(finding.conflict_ref_ids),
        "confidence": finding.confidence,
        "disconfirmation_criteria": list(finding.disconfirmation_criteria),
        "limitations": list(finding.limitations),
        "observed_at": finding.observed_at,
        "recorded_at": finding.recorded_at,
        "sensitivity": finding.sensitivity,
        "owner_ref_id": finding.owner_ref_id,
        "schema_version": finding.schema_version,
    }


def ledger_finding_from_dict(payload: Mapping[str, Any]) -> LedgerFinding:
    data = _require_fields(
        payload,
        {
            "finding_id",
            "origin",
            "statement",
            "why_it_matters",
            "source_record_ref_id",
            "source_record_semantic_hash",
            "evidence_ref_ids",
            "conflict_ref_ids",
            "confidence",
            "disconfirmation_criteria",
            "limitations",
            "observed_at",
            "recorded_at",
            "sensitivity",
            "owner_ref_id",
            "schema_version",
        },
    )
    data["finding_id"] = finding_identifier_from_dict(data["finding_id"])
    for field_name in (
        "evidence_ref_ids",
        "conflict_ref_ids",
        "disconfirmation_criteria",
        "limitations",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return LedgerFinding(**data)


def ledger_finding_semantic_hash(finding: LedgerFinding) -> str:
    return semantic_hash(ledger_finding_to_dict(finding))


def idea_record_to_dict(idea: IdeaRecord) -> dict[str, Any]:
    validate_idea_record(idea)
    return {
        "idea_id": idea_identifier_to_dict(idea.idea_id),
        "revision": idea.revision,
        "original_wording": idea.original_wording,
        "current_summary": idea.current_summary,
        "state": idea.state,
        "origin_ref_ids": list(idea.origin_ref_ids),
        "finding_ref_ids": list(idea.finding_ref_ids),
        "relation_ids": list(idea.relation_ids),
        "occurrence_ids": list(idea.occurrence_ids),
        "trigger_ids": list(idea.trigger_ids),
        "human_decision_ref_ids": list(idea.human_decision_ref_ids),
        "policy_ref_ids": list(idea.policy_ref_ids),
        "created_at": idea.created_at,
        "updated_at": idea.updated_at,
        "sensitivity": idea.sensitivity,
        "owner_ref_id": idea.owner_ref_id,
        "supersedes_idea_hash": idea.supersedes_idea_hash,
        "schema_version": idea.schema_version,
    }


def idea_record_from_dict(payload: Mapping[str, Any]) -> IdeaRecord:
    data = _require_fields(
        payload,
        {
            "idea_id",
            "revision",
            "original_wording",
            "current_summary",
            "state",
            "origin_ref_ids",
            "finding_ref_ids",
            "relation_ids",
            "occurrence_ids",
            "trigger_ids",
            "human_decision_ref_ids",
            "policy_ref_ids",
            "created_at",
            "updated_at",
            "sensitivity",
            "owner_ref_id",
            "supersedes_idea_hash",
            "schema_version",
        },
    )
    data["idea_id"] = idea_identifier_from_dict(data["idea_id"])
    for field_name in (
        "origin_ref_ids",
        "finding_ref_ids",
        "relation_ids",
        "occurrence_ids",
        "trigger_ids",
        "human_decision_ref_ids",
        "policy_ref_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return IdeaRecord(**data)


def idea_record_semantic_hash(idea: IdeaRecord) -> str:
    return semantic_hash(idea_record_to_dict(idea))


def idea_occurrence_to_dict(occurrence: IdeaOccurrence) -> dict[str, Any]:
    _require_type(occurrence, IdeaOccurrence, "occurrence")
    return {
        "occurrence_id": occurrence.occurrence_id,
        "idea_id": idea_identifier_to_dict(occurrence.idea_id),
        "occurred_at": occurrence.occurred_at,
        "context_summary": occurrence.context_summary,
        "source_ref_ids": list(occurrence.source_ref_ids),
        "evidence_ref_ids": list(occurrence.evidence_ref_ids),
        "sensitivity": occurrence.sensitivity,
        "owner_ref_id": occurrence.owner_ref_id,
        "schema_version": occurrence.schema_version,
    }


def idea_occurrence_from_dict(payload: Mapping[str, Any]) -> IdeaOccurrence:
    data = _require_fields(
        payload,
        {
            "occurrence_id",
            "idea_id",
            "occurred_at",
            "context_summary",
            "source_ref_ids",
            "evidence_ref_ids",
            "sensitivity",
            "owner_ref_id",
            "schema_version",
        },
    )
    data["idea_id"] = idea_identifier_from_dict(data["idea_id"])
    data["source_ref_ids"] = _json_tuple(data["source_ref_ids"], "source_ref_ids")
    data["evidence_ref_ids"] = _json_tuple(
        data["evidence_ref_ids"],
        "evidence_ref_ids",
    )
    return IdeaOccurrence(**data)


def idea_occurrence_semantic_hash(occurrence: IdeaOccurrence) -> str:
    return semantic_hash(idea_occurrence_to_dict(occurrence))


def ledger_entity_reference_to_dict(
    reference: LedgerEntityReference,
) -> dict[str, Any]:
    _require_type(reference, LedgerEntityReference, "reference")
    return {
        "entity_kind": reference.entity_kind,
        "entity_id": reference.entity_id,
        "revision": reference.revision,
        "semantic_hash": reference.semantic_hash,
        "schema_version": reference.schema_version,
    }


def ledger_entity_reference_from_dict(
    payload: Mapping[str, Any],
) -> LedgerEntityReference:
    data = _require_fields(
        payload,
        {"entity_kind", "entity_id", "revision", "semantic_hash", "schema_version"},
    )
    return LedgerEntityReference(**data)


def ledger_entity_reference_semantic_hash(
    reference: LedgerEntityReference,
) -> str:
    return semantic_hash(ledger_entity_reference_to_dict(reference))


def ledger_relation_to_dict(relation: LedgerRelation) -> dict[str, Any]:
    _require_type(relation, LedgerRelation, "relation")
    return {
        "relation_id": relation.relation_id,
        "source": ledger_entity_reference_to_dict(relation.source),
        "target": ledger_entity_reference_to_dict(relation.target),
        "relation_type": relation.relation_type,
        "basis_ref_ids": list(relation.basis_ref_ids),
        "confidence": relation.confidence,
        "limitations": list(relation.limitations),
        "created_at": relation.created_at,
        "created_by_ref_id": relation.created_by_ref_id,
        "schema_version": relation.schema_version,
    }


def ledger_relation_from_dict(payload: Mapping[str, Any]) -> LedgerRelation:
    data = _require_fields(
        payload,
        {
            "relation_id",
            "source",
            "target",
            "relation_type",
            "basis_ref_ids",
            "confidence",
            "limitations",
            "created_at",
            "created_by_ref_id",
            "schema_version",
        },
    )
    data["source"] = ledger_entity_reference_from_dict(data["source"])
    data["target"] = ledger_entity_reference_from_dict(data["target"])
    data["basis_ref_ids"] = _json_tuple(data["basis_ref_ids"], "basis_ref_ids")
    data["limitations"] = _json_tuple(data["limitations"], "limitations")
    return LedgerRelation(**data)


def ledger_relation_semantic_hash(relation: LedgerRelation) -> str:
    return semantic_hash(ledger_relation_to_dict(relation))


def reconsideration_trigger_to_dict(
    trigger: ReconsiderationTrigger,
) -> dict[str, Any]:
    _require_type(trigger, ReconsiderationTrigger, "trigger")
    return {
        "trigger_id": trigger.trigger_id,
        "idea_id": idea_identifier_to_dict(trigger.idea_id),
        "trigger_kind": trigger.trigger_kind,
        "condition_summary": trigger.condition_summary,
        "required_evidence_classes": list(trigger.required_evidence_classes),
        "recurrence_threshold": trigger.recurrence_threshold,
        "not_before": trigger.not_before,
        "expires_at": trigger.expires_at,
        "created_at": trigger.created_at,
        "created_by_ref_id": trigger.created_by_ref_id,
        "schema_version": trigger.schema_version,
    }


def reconsideration_trigger_from_dict(
    payload: Mapping[str, Any],
) -> ReconsiderationTrigger:
    data = _require_fields(
        payload,
        {
            "trigger_id",
            "idea_id",
            "trigger_kind",
            "condition_summary",
            "required_evidence_classes",
            "recurrence_threshold",
            "not_before",
            "expires_at",
            "created_at",
            "created_by_ref_id",
            "schema_version",
        },
    )
    data["idea_id"] = idea_identifier_from_dict(data["idea_id"])
    data["required_evidence_classes"] = _json_tuple(
        data["required_evidence_classes"],
        "required_evidence_classes",
    )
    return ReconsiderationTrigger(**data)


def reconsideration_trigger_semantic_hash(
    trigger: ReconsiderationTrigger,
) -> str:
    return semantic_hash(reconsideration_trigger_to_dict(trigger))


def reconsideration_request_to_dict(
    request: ReconsiderationRequest,
) -> dict[str, Any]:
    _require_type(request, ReconsiderationRequest, "request")
    return {
        "request_id": request.request_id,
        "idea_id": idea_identifier_to_dict(request.idea_id),
        "idea_revision": request.idea_revision,
        "trigger_id": request.trigger_id,
        "as_of": request.as_of,
        "evidence_ref_ids": list(request.evidence_ref_ids),
        "occurrence_ids": list(request.occurrence_ids),
        "human_request_ref_ids": list(request.human_request_ref_ids),
        "limitations": list(request.limitations),
        "schema_version": request.schema_version,
    }


def reconsideration_request_from_dict(
    payload: Mapping[str, Any],
) -> ReconsiderationRequest:
    data = _require_fields(
        payload,
        {
            "request_id",
            "idea_id",
            "idea_revision",
            "trigger_id",
            "as_of",
            "evidence_ref_ids",
            "occurrence_ids",
            "human_request_ref_ids",
            "limitations",
            "schema_version",
        },
    )
    data["idea_id"] = idea_identifier_from_dict(data["idea_id"])
    for field_name in (
        "evidence_ref_ids",
        "occurrence_ids",
        "human_request_ref_ids",
        "limitations",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return ReconsiderationRequest(**data)


def reconsideration_request_semantic_hash(
    request: ReconsiderationRequest,
) -> str:
    return semantic_hash(reconsideration_request_to_dict(request))


def ledger_history_event_to_dict(event: LedgerHistoryEvent) -> dict[str, Any]:
    _require_type(event, LedgerHistoryEvent, "event")
    return {
        "event_id": event.event_id,
        "event_kind": event.event_kind,
        "entity": ledger_entity_reference_to_dict(event.entity),
        "related_ref_ids": list(event.related_ref_ids),
        "evidence_ref_ids": list(event.evidence_ref_ids),
        "human_decision_ref_ids": list(event.human_decision_ref_ids),
        "policy_ref_ids": list(event.policy_ref_ids),
        "statement": event.statement,
        "created_at": event.created_at,
        "prior_event_hash": event.prior_event_hash,
        "schema_version": event.schema_version,
    }


def ledger_history_event_from_dict(
    payload: Mapping[str, Any],
) -> LedgerHistoryEvent:
    data = _require_fields(
        payload,
        {
            "event_id",
            "event_kind",
            "entity",
            "related_ref_ids",
            "evidence_ref_ids",
            "human_decision_ref_ids",
            "policy_ref_ids",
            "statement",
            "created_at",
            "prior_event_hash",
            "schema_version",
        },
    )
    data["entity"] = ledger_entity_reference_from_dict(data["entity"])
    for field_name in (
        "related_ref_ids",
        "evidence_ref_ids",
        "human_decision_ref_ids",
        "policy_ref_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return LedgerHistoryEvent(**data)


def ledger_history_event_semantic_hash(event: LedgerHistoryEvent) -> str:
    return semantic_hash(ledger_history_event_to_dict(event))


def ledger_snapshot_reference_to_dict(
    reference: LedgerSnapshotReference,
) -> dict[str, Any]:
    _require_type(reference, LedgerSnapshotReference, "reference")
    return {
        "snapshot_id": reference.snapshot_id,
        "revision": reference.revision,
        "semantic_hash": reference.semantic_hash,
        "schema_version": reference.schema_version,
    }


def ledger_snapshot_reference_from_dict(
    payload: Mapping[str, Any],
) -> LedgerSnapshotReference:
    data = _require_fields(
        payload,
        {"snapshot_id", "revision", "semantic_hash", "schema_version"},
    )
    return LedgerSnapshotReference(**data)


def ledger_snapshot_reference_semantic_hash(
    reference: LedgerSnapshotReference,
) -> str:
    return semantic_hash(ledger_snapshot_reference_to_dict(reference))


def findings_idea_ledger_snapshot_to_dict(
    snapshot: FindingsIdeaLedgerSnapshot,
) -> dict[str, Any]:
    validate_ledger_snapshot(snapshot)
    return {
        "snapshot_id": snapshot.snapshot_id,
        "revision": snapshot.revision,
        "ledger_scope_id": snapshot.ledger_scope_id,
        "as_of": snapshot.as_of,
        "findings": [ledger_finding_to_dict(item) for item in snapshot.findings],
        "ideas": [idea_record_to_dict(item) for item in snapshot.ideas],
        "occurrences": [idea_occurrence_to_dict(item) for item in snapshot.occurrences],
        "relations": [ledger_relation_to_dict(item) for item in snapshot.relations],
        "triggers": [reconsideration_trigger_to_dict(item) for item in snapshot.triggers],
        "reconsideration_requests": [
            reconsideration_request_to_dict(item)
            for item in snapshot.reconsideration_requests
        ],
        "history_events": [
            ledger_history_event_to_dict(item) for item in snapshot.history_events
        ],
        "evidence_snapshot": [
            goal_evidence_reference_to_dict(item)
            for item in snapshot.evidence_snapshot
        ],
        "external_entity_references": [
            ledger_entity_reference_to_dict(item)
            for item in snapshot.external_entity_references
        ],
        "supersedes_snapshot": (
            ledger_snapshot_reference_to_dict(snapshot.supersedes_snapshot)
            if snapshot.supersedes_snapshot is not None
            else None
        ),
        "schema_version": snapshot.schema_version,
    }


def findings_idea_ledger_snapshot_from_dict(
    payload: Mapping[str, Any],
) -> FindingsIdeaLedgerSnapshot:
    data = _require_fields(
        payload,
        {
            "snapshot_id",
            "revision",
            "ledger_scope_id",
            "as_of",
            "findings",
            "ideas",
            "occurrences",
            "relations",
            "triggers",
            "reconsideration_requests",
            "history_events",
            "evidence_snapshot",
            "external_entity_references",
            "supersedes_snapshot",
            "schema_version",
        },
    )
    data["findings"] = tuple(
        ledger_finding_from_dict(item)
        for item in _json_tuple(data["findings"], "findings")
    )
    data["ideas"] = tuple(
        idea_record_from_dict(item)
        for item in _json_tuple(data["ideas"], "ideas")
    )
    data["occurrences"] = tuple(
        idea_occurrence_from_dict(item)
        for item in _json_tuple(data["occurrences"], "occurrences")
    )
    data["relations"] = tuple(
        ledger_relation_from_dict(item)
        for item in _json_tuple(data["relations"], "relations")
    )
    data["triggers"] = tuple(
        reconsideration_trigger_from_dict(item)
        for item in _json_tuple(data["triggers"], "triggers")
    )
    data["reconsideration_requests"] = tuple(
        reconsideration_request_from_dict(item)
        for item in _json_tuple(
            data["reconsideration_requests"],
            "reconsideration_requests",
        )
    )
    data["history_events"] = tuple(
        ledger_history_event_from_dict(item)
        for item in _json_tuple(data["history_events"], "history_events")
    )
    data["evidence_snapshot"] = tuple(
        goal_evidence_reference_from_dict(item)
        for item in _json_tuple(data["evidence_snapshot"], "evidence_snapshot")
    )
    data["external_entity_references"] = tuple(
        ledger_entity_reference_from_dict(item)
        for item in _json_tuple(
            data["external_entity_references"],
            "external_entity_references",
        )
    )
    if data["supersedes_snapshot"] is not None:
        data["supersedes_snapshot"] = ledger_snapshot_reference_from_dict(
            data["supersedes_snapshot"]
        )
    return FindingsIdeaLedgerSnapshot(**data)


def findings_idea_ledger_snapshot_semantic_hash(
    snapshot: FindingsIdeaLedgerSnapshot,
) -> str:
    return semantic_hash(findings_idea_ledger_snapshot_to_dict(snapshot))


def build_findings_idea_ledger_snapshot(
    *,
    snapshot_id: str,
    revision: int,
    ledger_scope_id: str,
    as_of: str,
    findings: tuple[LedgerFinding, ...],
    ideas: tuple[IdeaRecord, ...],
    occurrences: tuple[IdeaOccurrence, ...],
    relations: tuple[LedgerRelation, ...],
    triggers: tuple[ReconsiderationTrigger, ...],
    reconsideration_requests: tuple[ReconsiderationRequest, ...],
    history_events: tuple[LedgerHistoryEvent, ...],
    evidence_snapshot: tuple[GoalEvidenceReference, ...],
    external_entity_references: tuple[LedgerEntityReference, ...],
    supersedes_snapshot: LedgerSnapshotReference | None,
    schema_version: str = FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION,
) -> FindingsIdeaLedgerSnapshot:
    return FindingsIdeaLedgerSnapshot(
        snapshot_id=snapshot_id,
        revision=revision,
        ledger_scope_id=ledger_scope_id,
        as_of=as_of,
        findings=findings,
        ideas=ideas,
        occurrences=occurrences,
        relations=relations,
        triggers=triggers,
        reconsideration_requests=reconsideration_requests,
        history_events=history_events,
        evidence_snapshot=evidence_snapshot,
        external_entity_references=external_entity_references,
        supersedes_snapshot=supersedes_snapshot,
        schema_version=schema_version,
    )


def record_idea(
    snapshot: FindingsIdeaLedgerSnapshot,
    idea: IdeaRecord,
    history_event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    validate_idea_record(idea)
    if idea.revision != 1:
        raise GoalEngineIdeaLedgerError("record_idea requires Idea revision 1")
    if idea.idea_id.local_id in {item.idea_id.local_id for item in snapshot.ideas}:
        raise GoalEngineIdeaLedgerError("record_idea cannot replace an existing Idea")
    if not idea.human_decision_ref_ids and not idea.policy_ref_ids and idea.state != "UNTRIAGED":
        raise GoalEngineIdeaLedgerError(
            "initial Idea classification requires a human-decision or policy reference"
        )
    _validate_event_for_record(history_event, "IDEA_CAPTURED", _idea_reference(idea))
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        ideas=snapshot.ideas + (idea,),
        history_events=snapshot.history_events + (history_event,),
    )


def record_finding(
    snapshot: FindingsIdeaLedgerSnapshot,
    finding: LedgerFinding,
    source_record_payload: Mapping[str, Any],
    history_event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    validate_ledger_finding(finding)
    _validate_source_record_payload(finding, source_record_payload)
    if finding.finding_id.local_id in {
        item.finding_id.local_id for item in snapshot.findings
    }:
        raise GoalEngineIdeaLedgerError(
            "record_finding cannot replace an existing Finding"
        )
    _validate_event_for_record(
        history_event,
        "FINDING_ADMITTED",
        _finding_reference(finding),
    )
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        findings=snapshot.findings + (finding,),
        history_events=snapshot.history_events + (history_event,),
    )


def record_occurrence(
    snapshot: FindingsIdeaLedgerSnapshot,
    occurrence: IdeaOccurrence,
    revised_idea: IdeaRecord,
    history_event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    if occurrence.occurrence_id in {
        item.occurrence_id for item in snapshot.occurrences
    }:
        raise GoalEngineIdeaLedgerError("duplicate occurrence_id")
    prior_idea = _current_idea(snapshot, occurrence.idea_id)
    validate_idea_revision(revised_idea, prior_idea)
    if revised_idea.state != prior_idea.state:
        raise GoalEngineIdeaLedgerError("recurrence cannot change Idea state")
    if set(revised_idea.occurrence_ids) != set(prior_idea.occurrence_ids) | {
        occurrence.occurrence_id
    }:
        raise GoalEngineIdeaLedgerError(
            "revised Idea must add exactly the recorded occurrence"
        )
    _validate_unchanged_idea_links(
        prior_idea,
        revised_idea,
        except_field="occurrence_ids",
    )
    _validate_event_for_record(
        history_event,
        "OCCURRENCE_RECORDED",
        _idea_reference(revised_idea),
        related_ref_id=occurrence.occurrence_id,
    )
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        ideas=_replace_ideas(snapshot.ideas, (revised_idea,)),
        occurrences=snapshot.occurrences + (occurrence,),
        history_events=snapshot.history_events + (history_event,),
        external_entity_references=_add_prior_idea_references(
            snapshot.external_entity_references,
            (prior_idea,),
        ),
    )


def record_relation(
    snapshot: FindingsIdeaLedgerSnapshot,
    relation: LedgerRelation,
    revised_ideas: tuple[IdeaRecord, ...],
    history_events: tuple[LedgerHistoryEvent, ...],
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    if relation.relation_id in {item.relation_id for item in snapshot.relations}:
        raise GoalEngineIdeaLedgerError("duplicate relation_id")
    expected_idea_ids = {
        reference.entity_id
        for reference in (relation.source, relation.target)
        if reference.entity_kind == "IDEA"
        and reference.entity_id in {item.idea_id.local_id for item in snapshot.ideas}
    }
    revised_by_id = {item.idea_id.local_id: item for item in revised_ideas}
    if set(revised_by_id) != expected_idea_ids:
        raise GoalEngineIdeaLedgerError(
            "revised_ideas must exactly cover current Ideas in the relation"
        )
    if not revised_by_id:
        raise GoalEngineIdeaLedgerError(
            "record_relation requires at least one current Idea endpoint"
        )
    if not isinstance(history_events, tuple):
        raise GoalEngineIdeaLedgerError("history_events must be a tuple")
    event_by_entity_id = {
        item.entity.entity_id: item for item in history_events
    }
    if len(event_by_entity_id) != len(history_events):
        raise GoalEngineIdeaLedgerError(
            "record_relation requires one distinct history event per revised Idea"
        )
    if set(event_by_entity_id) != expected_idea_ids:
        raise GoalEngineIdeaLedgerError(
            "history_events must exactly cover revised Ideas"
        )
    prior_ideas: list[IdeaRecord] = []
    for idea_id, revised_idea in revised_by_id.items():
        prior_idea = _current_idea_by_id(snapshot, idea_id)
        validate_idea_revision(revised_idea, prior_idea)
        if set(revised_idea.relation_ids) != set(prior_idea.relation_ids) | {
            relation.relation_id
        }:
            raise GoalEngineIdeaLedgerError(
                "revised Idea must add exactly the recorded relation"
            )
        _validate_unchanged_idea_links(
            prior_idea,
            revised_idea,
            except_field="relation_ids",
        )
        _validate_event_for_record(
            event_by_entity_id[idea_id],
            "RELATION_RECORDED",
            _idea_reference(revised_idea),
            related_ref_id=relation.relation_id,
        )
        endpoint = relation.source
        if endpoint.entity_kind != "IDEA" or endpoint.entity_id != idea_id:
            endpoint = relation.target
        if endpoint != _idea_reference(revised_idea):
            raise GoalEngineIdeaLedgerError(
                "relation must reference the exact revised Idea semantic hash"
            )
        prior_ideas.append(prior_idea)
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        ideas=_replace_ideas(snapshot.ideas, revised_ideas),
        relations=snapshot.relations + (relation,),
        history_events=snapshot.history_events + history_events,
        external_entity_references=_add_prior_idea_references(
            snapshot.external_entity_references,
            tuple(prior_ideas),
        ),
    )


def define_reconsideration_trigger(
    snapshot: FindingsIdeaLedgerSnapshot,
    trigger: ReconsiderationTrigger,
    revised_idea: IdeaRecord,
    history_event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    if trigger.trigger_id in {item.trigger_id for item in snapshot.triggers}:
        raise GoalEngineIdeaLedgerError("duplicate trigger_id")
    prior_idea = _current_idea(snapshot, trigger.idea_id)
    validate_idea_revision(revised_idea, prior_idea)
    if set(revised_idea.trigger_ids) != set(prior_idea.trigger_ids) | {
        trigger.trigger_id
    }:
        raise GoalEngineIdeaLedgerError(
            "revised Idea must add exactly the defined trigger"
        )
    _validate_unchanged_idea_links(
        prior_idea,
        revised_idea,
        except_field="trigger_ids",
    )
    _validate_event_for_record(
        history_event,
        "TRIGGER_DEFINED",
        _idea_reference(revised_idea),
        related_ref_id=trigger.trigger_id,
    )
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        ideas=_replace_ideas(snapshot.ideas, (revised_idea,)),
        triggers=snapshot.triggers + (trigger,),
        history_events=snapshot.history_events + (history_event,),
        external_entity_references=_add_prior_idea_references(
            snapshot.external_entity_references,
            (prior_idea,),
        ),
    )


def build_reconsideration_request(
    snapshot: FindingsIdeaLedgerSnapshot,
    request: ReconsiderationRequest,
    history_event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    if request.request_id in {
        item.request_id for item in snapshot.reconsideration_requests
    }:
        raise GoalEngineIdeaLedgerError("duplicate request_id")
    idea = _current_idea(snapshot, request.idea_id)
    if idea.state != "ARCHIVED_CONDITIONAL":
        raise GoalEngineIdeaLedgerError(
            "reconsideration requires an ARCHIVED_CONDITIONAL Idea"
        )
    _validate_event_for_record(
        history_event,
        "RECONSIDERATION_REQUESTED",
        _idea_reference(idea),
        related_ref_id=request.request_id,
    )
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        reconsideration_requests=snapshot.reconsideration_requests + (request,),
        history_events=snapshot.history_events + (history_event,),
    )


def append_ledger_history_event(
    snapshot: FindingsIdeaLedgerSnapshot,
    history_event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    validate_ledger_snapshot(snapshot)
    return _next_snapshot(
        snapshot,
        as_of=as_of,
        history_events=snapshot.history_events + (history_event,),
    )


def _validate_finding_references(
    finding: LedgerFinding,
    evidence_by_id: Mapping[str, GoalEvidenceReference],
    entity_by_key: Mapping[tuple[str, str, int | None], LedgerEntityReference],
    as_of: datetime,
) -> None:
    source_matches = [
        item
        for item in entity_by_key.values()
        if item.entity_id == finding.source_record_ref_id
        and item.semantic_hash == finding.source_record_semantic_hash
    ]
    if len(source_matches) != 1:
        raise GoalEngineIdeaLedgerError(
            "Finding source reference and semantic hash must resolve exactly once"
        )
    _require_refs(finding.evidence_ref_ids, evidence_by_id, "Finding evidence")
    _require_refs(finding.conflict_ref_ids, evidence_by_id, "Finding conflict")
    if _parse_utc_timestamp(finding.recorded_at, "recorded_at") > as_of:
        raise GoalEngineIdeaLedgerError("Finding recorded_at cannot exceed as_of")


def _validate_idea_references(
    idea: IdeaRecord,
    finding_by_id: Mapping[str, LedgerFinding],
    occurrence_by_id: Mapping[str, IdeaOccurrence],
    relation_by_id: Mapping[str, LedgerRelation],
    trigger_by_id: Mapping[str, ReconsiderationTrigger],
    reference_counts: Mapping[str, int],
    as_of: datetime,
) -> None:
    _require_exact_refs(idea.origin_ref_ids, reference_counts, "Idea origin")
    _require_refs(idea.finding_ref_ids, finding_by_id, "Idea Finding")
    _require_refs(idea.occurrence_ids, occurrence_by_id, "Idea occurrence")
    _require_refs(idea.relation_ids, relation_by_id, "Idea relation")
    _require_refs(idea.trigger_ids, trigger_by_id, "Idea trigger")
    _require_exact_refs(
        idea.human_decision_ref_ids,
        reference_counts,
        "Idea human decision",
    )
    _require_exact_refs(idea.policy_ref_ids, reference_counts, "Idea policy")
    if _parse_utc_timestamp(idea.updated_at, "updated_at") > as_of:
        raise GoalEngineIdeaLedgerError("Idea updated_at cannot exceed as_of")
    for occurrence_id in idea.occurrence_ids:
        if occurrence_by_id[occurrence_id].idea_id != idea.idea_id:
            raise GoalEngineIdeaLedgerError(
                "Idea occurrence must retain the same IdeaIdentifier"
            )
    for trigger_id in idea.trigger_ids:
        if trigger_by_id[trigger_id].idea_id != idea.idea_id:
            raise GoalEngineIdeaLedgerError(
                "Idea trigger must retain the same IdeaIdentifier"
            )
    for relation_id in idea.relation_ids:
        relation = relation_by_id[relation_id]
        endpoints = {
            (relation.source.entity_kind, relation.source.entity_id),
            (relation.target.entity_kind, relation.target.entity_id),
        }
        if ("IDEA", idea.idea_id.local_id) not in endpoints:
            raise GoalEngineIdeaLedgerError(
                "Idea relation must visibly reference that Idea"
            )


def _validate_occurrence(
    occurrence: IdeaOccurrence,
    idea_by_id: Mapping[str, IdeaRecord],
    evidence_by_id: Mapping[str, GoalEvidenceReference],
    reference_counts: Mapping[str, int],
    as_of: datetime,
) -> None:
    idea = idea_by_id.get(occurrence.idea_id.local_id)
    if idea is None or idea.idea_id != occurrence.idea_id:
        raise GoalEngineIdeaLedgerError("occurrence references unknown Idea")
    occurred = _parse_utc_timestamp(occurrence.occurred_at, "occurred_at")
    if occurred < _parse_utc_timestamp(idea.created_at, "created_at"):
        raise GoalEngineIdeaLedgerError("occurrence cannot precede Idea creation")
    if occurred > as_of:
        raise GoalEngineIdeaLedgerError("occurrence cannot exceed as_of")
    _require_exact_refs(
        occurrence.source_ref_ids,
        reference_counts,
        "occurrence source",
    )
    _require_refs(occurrence.evidence_ref_ids, evidence_by_id, "occurrence evidence")
    _validate_private_pair(
        idea.sensitivity,
        idea.owner_ref_id,
        occurrence.sensitivity,
        occurrence.owner_ref_id,
        "occurrence",
    )


def _validate_relation(
    relation: LedgerRelation,
    entity_by_key: Mapping[tuple[str, str, int | None], LedgerEntityReference],
    idea_by_id: Mapping[str, IdeaRecord],
    finding_by_id: Mapping[str, LedgerFinding],
    reference_counts: Mapping[str, int],
    as_of: datetime,
) -> None:
    for endpoint_name, endpoint in (("source", relation.source), ("target", relation.target)):
        resolved = entity_by_key.get(_entity_reference_key(endpoint))
        if resolved != endpoint:
            raise GoalEngineIdeaLedgerError(
                f"relation {endpoint_name} does not resolve to the exact entity hash"
            )
    _require_exact_refs(relation.basis_ref_ids, reference_counts, "relation basis")
    if _parse_utc_timestamp(relation.created_at, "created_at") > as_of:
        raise GoalEngineIdeaLedgerError("relation created_at cannot exceed as_of")
    source_privacy = _entity_privacy(relation.source, idea_by_id, finding_by_id)
    target_privacy = _entity_privacy(relation.target, idea_by_id, finding_by_id)
    if source_privacy is not None and target_privacy is not None:
        _validate_private_pair(*source_privacy, *target_privacy, "relation")


def _validate_trigger(
    trigger: ReconsiderationTrigger,
    idea_by_id: Mapping[str, IdeaRecord],
    as_of: datetime,
) -> None:
    idea = idea_by_id.get(trigger.idea_id.local_id)
    if idea is None or idea.idea_id != trigger.idea_id:
        raise GoalEngineIdeaLedgerError("trigger references unknown Idea")
    if trigger.trigger_id not in idea.trigger_ids:
        raise GoalEngineIdeaLedgerError("trigger must be visible on its Idea")
    if _parse_utc_timestamp(trigger.created_at, "created_at") > as_of:
        raise GoalEngineIdeaLedgerError("trigger created_at cannot exceed as_of")


def _validate_reconsideration_request(
    request: ReconsiderationRequest,
    idea_by_id: Mapping[str, IdeaRecord],
    trigger_by_id: Mapping[str, ReconsiderationTrigger],
    occurrence_by_id: Mapping[str, IdeaOccurrence],
    evidence_by_id: Mapping[str, GoalEvidenceReference],
    reference_counts: Mapping[str, int],
    as_of: datetime,
) -> None:
    idea = idea_by_id.get(request.idea_id.local_id)
    if idea is None or idea.idea_id != request.idea_id:
        raise GoalEngineIdeaLedgerError("reconsideration references unknown Idea")
    if idea.revision != request.idea_revision:
        raise GoalEngineIdeaLedgerError(
            "reconsideration must reference the current archived Idea revision"
        )
    if idea.state != "ARCHIVED_CONDITIONAL":
        raise GoalEngineIdeaLedgerError(
            "reconsideration requires an ARCHIVED_CONDITIONAL Idea"
        )
    trigger = trigger_by_id.get(request.trigger_id)
    if trigger is None or trigger.idea_id != request.idea_id:
        raise GoalEngineIdeaLedgerError(
            "reconsideration trigger does not resolve for the Idea"
        )
    _require_refs(request.evidence_ref_ids, evidence_by_id, "request evidence")
    _require_refs(request.occurrence_ids, occurrence_by_id, "request occurrence")
    _require_exact_refs(
        request.human_request_ref_ids,
        reference_counts,
        "human request",
    )
    for occurrence_id in request.occurrence_ids:
        if occurrence_by_id[occurrence_id].idea_id != request.idea_id:
            raise GoalEngineIdeaLedgerError(
                "request occurrence belongs to a different Idea"
            )
    request_time = _parse_utc_timestamp(request.as_of, "request as_of")
    if request_time > as_of:
        raise GoalEngineIdeaLedgerError("request as_of cannot exceed snapshot as_of")
    if trigger.not_before is not None and request_time < _parse_utc_timestamp(
        trigger.not_before,
        "not_before",
    ):
        raise GoalEngineIdeaLedgerError("request precedes trigger not_before")
    if trigger.expires_at is not None and request_time > _parse_utc_timestamp(
        trigger.expires_at,
        "expires_at",
    ):
        raise GoalEngineIdeaLedgerError("request follows trigger expiry")
    evidence_classes = {
        evidence_by_id[item].evidence_class for item in request.evidence_ref_ids
    }
    missing_classes = sorted(
        set(trigger.required_evidence_classes) - evidence_classes
    )
    if missing_classes:
        raise GoalEngineIdeaLedgerError(
            f"reconsideration missing evidence class: {missing_classes[0]}"
        )
    if trigger.trigger_kind == "RECURRENCE_THRESHOLD":
        if len(request.occurrence_ids) < (trigger.recurrence_threshold or 0):
            raise GoalEngineIdeaLedgerError(
                "reconsideration does not meet recurrence threshold"
            )


def _validate_history(
    events: tuple[LedgerHistoryEvent, ...],
    entity_by_key: Mapping[tuple[str, str, int | None], LedgerEntityReference],
    evidence_by_id: Mapping[str, GoalEvidenceReference],
    reference_counts: Mapping[str, int],
    as_of: datetime,
) -> None:
    prior_by_entity: dict[tuple[str, str], LedgerHistoryEvent] = {}
    for event in events:
        resolved = entity_by_key.get(_entity_reference_key(event.entity))
        if resolved != event.entity:
            raise GoalEngineIdeaLedgerError(
                "history entity does not resolve to the exact semantic hash"
            )
        _require_refs(event.evidence_ref_ids, evidence_by_id, "history evidence")
        _require_exact_refs(
            event.human_decision_ref_ids,
            reference_counts,
            "history human decision",
        )
        _require_exact_refs(event.policy_ref_ids, reference_counts, "history policy")
        for related_id in event.related_ref_ids:
            if reference_counts.get(related_id, 0) != 1:
                raise GoalEngineIdeaLedgerError(
                    "history related reference must resolve exactly once: "
                    f"{related_id}"
                )
        event_time = _parse_utc_timestamp(event.created_at, "created_at")
        if event_time > as_of:
            raise GoalEngineIdeaLedgerError("history event cannot exceed as_of")
        chain_key = (event.entity.entity_kind, event.entity.entity_id)
        prior = prior_by_entity.get(chain_key)
        if prior is None:
            if event.prior_event_hash is not None:
                raise GoalEngineIdeaLedgerError(
                    "first history event for an entity forbids prior_event_hash"
                )
        else:
            expected_hash = ledger_history_event_semantic_hash(prior)
            if event.prior_event_hash != expected_hash:
                raise GoalEngineIdeaLedgerError(
                    "history prior_event_hash does not match the immediate prior event"
                )
            if event_time < _parse_utc_timestamp(prior.created_at, "created_at"):
                raise GoalEngineIdeaLedgerError("history event time cannot move backwards")
        prior_by_entity[chain_key] = event


def _validate_history_coverage(snapshot: FindingsIdeaLedgerSnapshot) -> None:
    events = snapshot.history_events
    for finding in snapshot.findings:
        reference = _finding_reference(finding)
        if not any(
            event.event_kind == "FINDING_ADMITTED" and event.entity == reference
            for event in events
        ):
            raise GoalEngineIdeaLedgerError(
                "every ledger Finding requires a FINDING_ADMITTED history event"
            )
    for idea in snapshot.ideas:
        reference = _idea_reference(idea)
        if not any(event.entity == reference for event in events):
            raise GoalEngineIdeaLedgerError(
                "every current Idea revision requires a history event"
            )
    for event_kind, identifiers in (
        ("OCCURRENCE_RECORDED", tuple(item.occurrence_id for item in snapshot.occurrences)),
        ("RELATION_RECORDED", tuple(item.relation_id for item in snapshot.relations)),
        ("TRIGGER_DEFINED", tuple(item.trigger_id for item in snapshot.triggers)),
        (
            "RECONSIDERATION_REQUESTED",
            tuple(item.request_id for item in snapshot.reconsideration_requests),
        ),
    ):
        for identifier in identifiers:
            if not any(
                event.event_kind == event_kind
                and identifier in event.related_ref_ids
                for event in events
            ):
                raise GoalEngineIdeaLedgerError(
                    f"{identifier} requires a {event_kind} history event"
                )


def _snapshot_entity_references(
    snapshot: FindingsIdeaLedgerSnapshot,
) -> dict[tuple[str, str, int | None], LedgerEntityReference]:
    references = list(snapshot.external_entity_references)
    references.extend(_finding_reference(item) for item in snapshot.findings)
    references.extend(_idea_reference(item) for item in snapshot.ideas)
    result: dict[tuple[str, str, int | None], LedgerEntityReference] = {}
    for reference in references:
        key = _entity_reference_key(reference)
        if key in result:
            raise GoalEngineIdeaLedgerError(
                "entity reference must resolve exactly once: "
                f"{reference.entity_kind}:{reference.entity_id}:{reference.revision}"
            )
        result[key] = reference
    return result


def _reference_id_counts(
    snapshot: FindingsIdeaLedgerSnapshot,
    entity_by_key: Mapping[tuple[str, str, int | None], LedgerEntityReference],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for evidence in snapshot.evidence_snapshot:
        counts[evidence.evidence_ref_id] = counts.get(evidence.evidence_ref_id, 0) + 1
    for reference in entity_by_key.values():
        counts[reference.entity_id] = counts.get(reference.entity_id, 0) + 1
    for item_id in (
        *(item.occurrence_id for item in snapshot.occurrences),
        *(item.relation_id for item in snapshot.relations),
        *(item.trigger_id for item in snapshot.triggers),
        *(item.request_id for item in snapshot.reconsideration_requests),
        *(item.event_id for item in snapshot.history_events),
    ):
        counts[item_id] = counts.get(item_id, 0) + 1
    return counts


def _validate_evidence_conflicts(
    evidence_by_id: Mapping[str, GoalEvidenceReference],
) -> None:
    for evidence in evidence_by_id.values():
        _require_refs(
            evidence.conflict_ref_ids,
            evidence_by_id,
            "evidence conflict",
        )


def _next_snapshot(
    snapshot: FindingsIdeaLedgerSnapshot,
    *,
    as_of: str,
    findings: tuple[LedgerFinding, ...] | None = None,
    ideas: tuple[IdeaRecord, ...] | None = None,
    occurrences: tuple[IdeaOccurrence, ...] | None = None,
    relations: tuple[LedgerRelation, ...] | None = None,
    triggers: tuple[ReconsiderationTrigger, ...] | None = None,
    reconsideration_requests: tuple[ReconsiderationRequest, ...] | None = None,
    history_events: tuple[LedgerHistoryEvent, ...] | None = None,
    external_entity_references: tuple[LedgerEntityReference, ...] | None = None,
) -> FindingsIdeaLedgerSnapshot:
    next_snapshot = FindingsIdeaLedgerSnapshot(
        snapshot_id=snapshot.snapshot_id,
        revision=snapshot.revision + 1,
        ledger_scope_id=snapshot.ledger_scope_id,
        as_of=as_of,
        findings=snapshot.findings if findings is None else findings,
        ideas=snapshot.ideas if ideas is None else ideas,
        occurrences=snapshot.occurrences if occurrences is None else occurrences,
        relations=snapshot.relations if relations is None else relations,
        triggers=snapshot.triggers if triggers is None else triggers,
        reconsideration_requests=(
            snapshot.reconsideration_requests
            if reconsideration_requests is None
            else reconsideration_requests
        ),
        history_events=(
            snapshot.history_events if history_events is None else history_events
        ),
        evidence_snapshot=snapshot.evidence_snapshot,
        external_entity_references=(
            snapshot.external_entity_references
            if external_entity_references is None
            else external_entity_references
        ),
        supersedes_snapshot=LedgerSnapshotReference(
            snapshot_id=snapshot.snapshot_id,
            revision=snapshot.revision,
            semantic_hash=findings_idea_ledger_snapshot_semantic_hash(snapshot),
            schema_version=LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        ),
        schema_version=FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION,
    )
    return validate_ledger_snapshot_revision(next_snapshot, snapshot)


def _validate_append_only_snapshot(
    snapshot: FindingsIdeaLedgerSnapshot,
    prior_snapshot: FindingsIdeaLedgerSnapshot,
) -> None:
    append_only_fields = (
        "findings",
        "occurrences",
        "relations",
        "triggers",
        "reconsideration_requests",
        "history_events",
        "evidence_snapshot",
        "external_entity_references",
    )
    for field_name in append_only_fields:
        current_values = set(getattr(snapshot, field_name))
        if any(
            item not in current_values
            for item in getattr(prior_snapshot, field_name)
        ):
            raise GoalEngineIdeaLedgerError(
                f"ledger revision cannot remove or rewrite {field_name}"
            )
    current_idea_by_id = {
        item.idea_id.local_id: item for item in snapshot.ideas
    }
    external_by_key = {
        _entity_reference_key(item): item
        for item in snapshot.external_entity_references
    }
    for prior_idea in prior_snapshot.ideas:
        current_idea = current_idea_by_id.get(prior_idea.idea_id.local_id)
        if current_idea is None:
            raise GoalEngineIdeaLedgerError("ledger revision cannot remove an Idea")
        if current_idea == prior_idea:
            continue
        validate_idea_revision(current_idea, prior_idea)
        prior_reference = _idea_reference(prior_idea)
        if external_by_key.get(_entity_reference_key(prior_reference)) != prior_reference:
            raise GoalEngineIdeaLedgerError(
                "revised Idea must retain the exact prior revision reference"
            )


def _validate_source_record_payload(
    finding: LedgerFinding,
    source_record_payload: Mapping[str, Any],
) -> None:
    _reject_forbidden_mapping(source_record_payload, "source_record_payload")
    if semantic_hash(source_record_payload) != finding.source_record_semantic_hash:
        raise GoalEngineIdeaLedgerError(
            "source record payload does not match source_record_semantic_hash"
        )
    required_ceiling_fields = {
        "statement": finding.statement,
        "why_it_matters": finding.why_it_matters,
        "evidence_ref_ids": list(finding.evidence_ref_ids),
        "conflict_ref_ids": list(finding.conflict_ref_ids),
        "confidence": finding.confidence,
        "disconfirmation_criteria": list(finding.disconfirmation_criteria),
        "limitations": list(finding.limitations),
    }
    for field_name, expected in required_ceiling_fields.items():
        if source_record_payload.get(field_name) != expected:
            raise GoalEngineIdeaLedgerError(
                f"ledger Finding exceeds or rewrites source {field_name}"
            )
    source_time = source_record_payload.get(
        "observed_at",
        source_record_payload.get("created_at"),
    )
    if source_time != finding.observed_at:
        raise GoalEngineIdeaLedgerError(
            "ledger Finding must preserve source observation time"
        )


def _idea_reference(idea: IdeaRecord) -> LedgerEntityReference:
    return LedgerEntityReference(
        entity_kind="IDEA",
        entity_id=idea.idea_id.local_id,
        revision=idea.revision,
        semantic_hash=idea_record_semantic_hash(idea),
        schema_version=LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
    )


def _finding_reference(finding: LedgerFinding) -> LedgerEntityReference:
    return LedgerEntityReference(
        entity_kind="FINDING",
        entity_id=finding.finding_id.local_id,
        revision=None,
        semantic_hash=ledger_finding_semantic_hash(finding),
        schema_version=LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
    )


def _entity_reference_key(
    reference: LedgerEntityReference,
) -> tuple[str, str, int | None]:
    return reference.entity_kind, reference.entity_id, reference.revision


def _validate_event_for_record(
    event: LedgerHistoryEvent,
    event_kind: str,
    entity: LedgerEntityReference,
    *,
    related_ref_id: str | None = None,
) -> None:
    if event.event_kind != event_kind:
        raise GoalEngineIdeaLedgerError(f"history event must be {event_kind}")
    if event.entity != entity:
        raise GoalEngineIdeaLedgerError(
            "history event entity must match the exact recorded semantic hash"
        )
    if related_ref_id is not None and related_ref_id not in event.related_ref_ids:
        raise GoalEngineIdeaLedgerError(
            "history event must name the recorded child reference"
        )


def _current_idea(
    snapshot: FindingsIdeaLedgerSnapshot,
    idea_id: IdeaIdentifier,
) -> IdeaRecord:
    idea = _current_idea_by_id(snapshot, idea_id.local_id)
    if idea.idea_id != idea_id:
        raise GoalEngineIdeaLedgerError("IdeaIdentifier does not match ledger Idea")
    return idea


def _current_idea_by_id(
    snapshot: FindingsIdeaLedgerSnapshot,
    idea_id: str,
) -> IdeaRecord:
    for idea in snapshot.ideas:
        if idea.idea_id.local_id == idea_id:
            return idea
    raise GoalEngineIdeaLedgerError(f"unknown Idea: {idea_id}")


def _replace_ideas(
    ideas: tuple[IdeaRecord, ...],
    replacements: tuple[IdeaRecord, ...],
) -> tuple[IdeaRecord, ...]:
    replacement_by_id = {item.idea_id.local_id: item for item in replacements}
    if len(replacement_by_id) != len(replacements):
        raise GoalEngineIdeaLedgerError("duplicate revised Idea")
    existing_ids = {item.idea_id.local_id for item in ideas}
    missing = sorted(set(replacement_by_id) - existing_ids)
    if missing:
        raise GoalEngineIdeaLedgerError(f"cannot revise unknown Idea: {missing[0]}")
    return tuple(
        replacement_by_id.get(item.idea_id.local_id, item) for item in ideas
    )


def _add_prior_idea_references(
    references: tuple[LedgerEntityReference, ...],
    prior_ideas: tuple[IdeaRecord, ...],
) -> tuple[LedgerEntityReference, ...]:
    existing_keys = {_entity_reference_key(item) for item in references}
    additions: list[LedgerEntityReference] = []
    for idea in prior_ideas:
        reference = _idea_reference(idea)
        if _entity_reference_key(reference) not in existing_keys:
            additions.append(reference)
            existing_keys.add(_entity_reference_key(reference))
    return references + tuple(additions)


def _validate_unchanged_idea_links(
    prior: IdeaRecord,
    revised: IdeaRecord,
    *,
    except_field: str,
) -> None:
    immutable_for_operation = (
        "current_summary",
        "state",
        "origin_ref_ids",
        "finding_ref_ids",
        "relation_ids",
        "occurrence_ids",
        "trigger_ids",
        "human_decision_ref_ids",
        "policy_ref_ids",
    )
    for field_name in immutable_for_operation:
        if field_name != except_field and getattr(prior, field_name) != getattr(
            revised,
            field_name,
        ):
            raise GoalEngineIdeaLedgerError(
                f"{field_name} cannot change during this ledger operation"
            )


def _entity_privacy(
    reference: LedgerEntityReference,
    idea_by_id: Mapping[str, IdeaRecord],
    finding_by_id: Mapping[str, LedgerFinding],
) -> tuple[str, str | None] | None:
    if reference.entity_kind == "IDEA":
        idea = idea_by_id.get(reference.entity_id)
        if idea is not None and idea.revision == reference.revision:
            return idea.sensitivity, idea.owner_ref_id
    if reference.entity_kind == "FINDING":
        finding = finding_by_id.get(reference.entity_id)
        if finding is not None:
            return finding.sensitivity, finding.owner_ref_id
    return None


def _validate_private_pair(
    left_sensitivity: str,
    left_owner: str | None,
    right_sensitivity: str,
    right_owner: str | None,
    context: str,
) -> None:
    if (
        left_sensitivity in _PRIVATE_SENSITIVITIES
        or right_sensitivity in _PRIVATE_SENSITIVITIES
    ) and left_owner != right_owner:
        raise GoalEngineIdeaLedgerError(
            f"cross-owner private {context} requires a separately authorized share"
        )


def _require_refs(
    ref_ids: tuple[str, ...],
    values: Mapping[str, Any],
    context: str,
) -> None:
    missing = sorted(set(ref_ids) - set(values))
    if missing:
        raise GoalEngineIdeaLedgerError(f"dangling {context} reference: {missing[0]}")


def _require_exact_refs(
    ref_ids: tuple[str, ...],
    counts: Mapping[str, int],
    context: str,
) -> None:
    for ref_id in ref_ids:
        if counts.get(ref_id, 0) != 1:
            raise GoalEngineIdeaLedgerError(
                f"{context} reference must resolve exactly once: {ref_id}"
            )


def _require_fields(
    payload: Mapping[str, Any],
    fields: set[str],
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise GoalEngineIdeaLedgerError("payload must be an object")
    if any(not isinstance(key, str) for key in payload):
        raise GoalEngineIdeaLedgerError("payload keys must be strings")
    keys = set(payload)
    forbidden = sorted(keys & _FORBIDDEN_FIELD_NAMES)
    if forbidden:
        raise GoalEngineIdeaLedgerError(
            f"payload contains forbidden field: {forbidden[0]}"
        )
    missing = sorted(fields - keys)
    if missing:
        raise GoalEngineIdeaLedgerError(
            f"payload missing required field: {missing[0]}"
        )
    extra = sorted(keys - fields)
    if extra:
        raise GoalEngineIdeaLedgerError(
            f"payload contains unknown field: {extra[0]}"
        )
    return dict(payload)


def _reject_forbidden_mapping(value: Any, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be an object")
    for key, item in value.items():
        if not isinstance(key, str):
            raise GoalEngineIdeaLedgerError(f"{field_name} keys must be strings")
        if key.casefold() in _FORBIDDEN_FIELD_NAMES:
            raise GoalEngineIdeaLedgerError(
                f"{field_name} contains forbidden field: {key}"
            )
        if isinstance(item, Mapping):
            _reject_forbidden_mapping(item, field_name)
        elif isinstance(item, list | tuple):
            for nested in item:
                if isinstance(nested, Mapping):
                    _reject_forbidden_mapping(nested, field_name)
                elif isinstance(nested, str):
                    lowered = nested.casefold()
                    if any(marker in lowered for marker in _SECRET_MARKERS):
                        raise GoalEngineIdeaLedgerError(
                            f"{field_name} contains raw secret material"
                        )
        elif isinstance(item, str):
            lowered = item.casefold()
            if any(marker in lowered for marker in _SECRET_MARKERS):
                raise GoalEngineIdeaLedgerError(
                    f"{field_name} contains raw secret material"
                )


def _json_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be an array")
    return tuple(value)


def _record_tuple(
    values: tuple[Any, ...],
    record_type: type,
    field_name: str,
    identity,
    *,
    order=None,
) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, record_type):
            raise GoalEngineIdeaLedgerError(
                f"{field_name} must contain {record_type.__name__} values"
            )
    identities = [identity(item) for item in values]
    duplicate = _first_duplicate(identities)
    if duplicate is not None:
        raise GoalEngineIdeaLedgerError(
            f"{field_name} contains duplicate identity: {duplicate}"
        )
    sort_key = order if order is not None else identity
    return tuple(sorted(values, key=sort_key))


def _id_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
    require_nonempty: bool = False,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be a tuple")
    validated = tuple(_require_id(item, field_name) for item in values)
    if require_nonempty and not validated:
        raise GoalEngineIdeaLedgerError(f"{field_name} cannot be empty")
    duplicate = _first_duplicate(list(validated))
    if duplicate is not None:
        raise GoalEngineIdeaLedgerError(
            f"{field_name} contains duplicate ID: {duplicate}"
        )
    return tuple(sorted(validated)) if sort else validated


def _text_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    require_nonempty: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be a tuple")
    validated = tuple(_require_safe_text(item, field_name) for item in values)
    if require_nonempty and not validated:
        raise GoalEngineIdeaLedgerError(f"{field_name} cannot be empty")
    duplicate = _first_duplicate(list(validated))
    if duplicate is not None:
        raise GoalEngineIdeaLedgerError(
            f"{field_name} contains duplicate value: {duplicate}"
        )
    return validated


def _label_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be a tuple")
    validated = tuple(_require_label(item, field_name) for item in values)
    duplicate = _first_duplicate(list(validated))
    if duplicate is not None:
        raise GoalEngineIdeaLedgerError(
            f"{field_name} contains duplicate label: {duplicate}"
        )
    return tuple(sorted(validated)) if sort else validated


def _require_allowed(value: Any, allowed: frozenset[str], field_name: str) -> str:
    text = _require_label(value, field_name)
    if text not in allowed:
        raise GoalEngineIdeaLedgerError(f"unsupported {field_name}: {text}")
    return text


def _require_safe_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise GoalEngineIdeaLedgerError(
            f"{field_name} must be non-empty text without surrounding whitespace"
        )
    if "\x00" in value:
        raise GoalEngineIdeaLedgerError(f"{field_name} contains a null character")
    lowered = value.casefold()
    if any(marker in lowered for marker in _SECRET_MARKERS):
        raise GoalEngineIdeaLedgerError(f"{field_name} contains raw secret material")
    return value


def _require_original_wording(value: Any) -> str:
    if not isinstance(value, str) or not value or len(value) > 10_000:
        raise GoalEngineIdeaLedgerError(
            "original_wording must be bounded non-empty text"
        )
    if "\x00" in value:
        raise GoalEngineIdeaLedgerError("original_wording contains a null character")
    if unicodedata.normalize("NFC", value) != value:
        raise GoalEngineIdeaLedgerError(
            "original_wording must use NFC Unicode normalization"
        )
    lowered = value.casefold()
    if any(marker in lowered for marker in _SECRET_MARKERS):
        raise GoalEngineIdeaLedgerError(
            "original_wording contains raw secret material"
        )
    return value


def _require_label(value: Any, field_name: str) -> str:
    text = _require_safe_text(value, field_name)
    if len(text) > 128 or any(ord(character) < 32 for character in text):
        raise GoalEngineIdeaLedgerError(
            f"{field_name} is not a valid governance label"
        )
    return text


def _require_id(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _ID_PATTERN.fullmatch(value):
        raise GoalEngineIdeaLedgerError(
            f"{field_name} must be a stable local identifier"
        )
    return value


def _require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GoalEngineIdeaLedgerError(f"{field_name} must be a positive integer")
    return value


def _require_ratio(value: Any, field_name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be numeric")
    if not math.isfinite(value) or value < 0 or value > 1:
        raise GoalEngineIdeaLedgerError(
            f"{field_name} must be finite and between 0 and 1"
        )
    return float(value)


def _require_schema(value: Any, expected: str) -> str:
    text = _require_label(value, "schema_version")
    if text != expected:
        raise GoalEngineIdeaLedgerError(f"schema_version must be {expected}")
    return text


def _require_sha256(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not _SHA256_PATTERN.fullmatch(value):
        raise GoalEngineIdeaLedgerError(
            f"{field_name} must be a lowercase SHA-256 hex digest"
        )
    return value


def _parse_utc_timestamp(value: Any, field_name: str) -> datetime:
    text = _require_safe_text(value, field_name)
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise GoalEngineIdeaLedgerError(
            f"{field_name} must be an ISO-8601 UTC timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise GoalEngineIdeaLedgerError(f"{field_name} must be UTC")
    return parsed


def _require_utc_timestamp(value: Any, field_name: str) -> str:
    _parse_utc_timestamp(value, field_name)
    return str(value)


def _validate_owner(sensitivity: str, owner_ref_id: str | None) -> None:
    if sensitivity in _PRIVATE_SENSITIVITIES:
        _require_id(owner_ref_id, "owner_ref_id")
    elif owner_ref_id is not None:
        _require_id(owner_ref_id, "owner_ref_id")


def _require_type(value: Any, expected_type: type, field_name: str) -> None:
    if not isinstance(value, expected_type):
        raise GoalEngineIdeaLedgerError(
            f"{field_name} must be {expected_type.__name__}"
        )


def _first_duplicate(values: list[Any]) -> Any | None:
    seen: set[Any] = set()
    for value in values:
        if value in seen:
            return value
        seen.add(value)
    return None


__all__ = [
    "FINDING_ORIGINS",
    "FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION",
    "HISTORY_EVENT_KINDS",
    "IDEA_OCCURRENCE_SCHEMA_VERSION",
    "IDEA_RECORD_SCHEMA_VERSION",
    "IDEA_STATES",
    "LEDGER_ENTITY_KINDS",
    "LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION",
    "LEDGER_FINDING_SCHEMA_VERSION",
    "LEDGER_HISTORY_EVENT_SCHEMA_VERSION",
    "LEDGER_RELATION_SCHEMA_VERSION",
    "LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION",
    "RECONSIDERATION_REQUEST_SCHEMA_VERSION",
    "RECONSIDERATION_TRIGGER_SCHEMA_VERSION",
    "RELATION_TYPES",
    "SENSITIVITY_VALUES",
    "TRIGGER_KINDS",
    "FindingsIdeaLedgerSnapshot",
    "GoalEngineIdeaLedgerError",
    "IdeaOccurrence",
    "IdeaRecord",
    "LedgerEntityReference",
    "LedgerFinding",
    "LedgerHistoryEvent",
    "LedgerRelation",
    "LedgerSnapshotReference",
    "ReconsiderationRequest",
    "ReconsiderationTrigger",
    "append_ledger_history_event",
    "build_findings_idea_ledger_snapshot",
    "build_reconsideration_request",
    "define_reconsideration_trigger",
    "findings_idea_ledger_snapshot_from_dict",
    "findings_idea_ledger_snapshot_semantic_hash",
    "findings_idea_ledger_snapshot_to_dict",
    "idea_occurrence_from_dict",
    "idea_occurrence_semantic_hash",
    "idea_occurrence_to_dict",
    "idea_record_from_dict",
    "idea_record_semantic_hash",
    "idea_record_to_dict",
    "ledger_entity_reference_from_dict",
    "ledger_entity_reference_semantic_hash",
    "ledger_entity_reference_to_dict",
    "ledger_finding_from_dict",
    "ledger_finding_semantic_hash",
    "ledger_finding_to_dict",
    "ledger_history_event_from_dict",
    "ledger_history_event_semantic_hash",
    "ledger_history_event_to_dict",
    "ledger_relation_from_dict",
    "ledger_relation_semantic_hash",
    "ledger_relation_to_dict",
    "ledger_snapshot_reference_from_dict",
    "ledger_snapshot_reference_semantic_hash",
    "ledger_snapshot_reference_to_dict",
    "reconsideration_request_from_dict",
    "reconsideration_request_semantic_hash",
    "reconsideration_request_to_dict",
    "reconsideration_trigger_from_dict",
    "reconsideration_trigger_semantic_hash",
    "reconsideration_trigger_to_dict",
    "record_finding",
    "record_idea",
    "record_occurrence",
    "record_relation",
    "validate_finding_origin",
    "validate_history_event_kind",
    "validate_idea_record",
    "validate_idea_revision",
    "validate_idea_state",
    "validate_ledger_entity_kind",
    "validate_ledger_finding",
    "validate_ledger_snapshot",
    "validate_ledger_snapshot_revision",
    "validate_relation_type",
    "validate_sensitivity",
    "validate_trigger_kind",
]
