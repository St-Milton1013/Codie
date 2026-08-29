"""Pure, deterministic subsystem-health records for Goal Engine v1.

The health foundation packages caller-supplied observations for one subsystem
at a time.  It performs no discovery, persistence, provider access, scoring,
work selection, or authority transition.
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from types import MappingProxyType
from typing import Any

from .foundation import (
    IDENTIFIER_SCHEMA_VERSION,
    FindingIdentifier,
    GoalEvidenceReference,
    GoalPolicyRecord,
    finding_identifier_from_dict,
    finding_identifier_to_dict,
    goal_evidence_reference_from_dict,
    goal_evidence_reference_to_dict,
    semantic_hash,
)

HEALTH_SIGNAL_DEFINITION_SCHEMA_VERSION = (
    "codie.goal_engine.health_signal_definition.v1"
)
HEALTH_SIGNAL_OBSERVATION_SCHEMA_VERSION = (
    "codie.goal_engine.health_signal_observation.v1"
)
HEALTH_MANIFEST_SCHEMA_VERSION = "codie.goal_engine.health_manifest.v1"
HEALTH_FINDING_SCHEMA_VERSION = "codie.goal_engine.health_finding.v1"
SUBSYSTEM_HEALTH_ASSESSMENT_SCHEMA_VERSION = (
    "codie.goal_engine.subsystem_health_assessment.v1"
)
SUBSYSTEM_HEALTH_ASSESSMENT_REFERENCE_SCHEMA_VERSION = (
    "codie.goal_engine.subsystem_health_assessment_reference.v1"
)

HEALTH_DOMAINS = frozenset({"CODIE", "JIN", "THEORY_CORPUS"})
ASSESSMENT_CLASSES = frozenset({"OBJECTIVE", "SEMI_OBJECTIVE", "SUBJECTIVE"})
SIGNAL_STATUSES = frozenset(
    {"PASS", "DEGRADED", "FAIL", "UNKNOWN", "CONFLICTED", "NOT_APPLICABLE"}
)
FINDING_CLASSES = frozenset(
    {
        "DEGRADATION",
        "FAILURE",
        "EVIDENCE_GAP",
        "EVIDENCE_CONFLICT",
        "STALE_EVIDENCE",
        "PRIVACY_OR_SECURITY",
        "MANIFEST_GAP",
    }
)

HEALTH_CATEGORIES: Mapping[str, frozenset[str]] = MappingProxyType(
    {
        "CODIE": frozenset(
            {
                "TESTS",
                "VALIDATORS",
                "DATA_INTEGRITY",
                "PROVENANCE",
                "INGESTION",
                "SERVICES",
                "INVARIANTS",
                "SECURITY_PRIVACY",
                "DEPENDENCIES",
                "PERFORMANCE",
                "RELIABILITY",
                "SOURCE_HEALTH",
            }
        ),
        "JIN": frozenset(
            {
                "FACTUAL_CORRECTNESS",
                "CITATION_COVERAGE",
                "PRIVACY",
                "CORRECTION_HANDLING",
                "RETRIEVAL_QUALITY",
                "CLARITY",
                "USEFULNESS",
            }
        ),
        "THEORY_CORPUS": frozenset(
            {
                "MANIFEST_COMPLETENESS",
                "INGESTION_INTEGRITY",
                "REPRESENTATION_COVERAGE",
                "RETRIEVAL_QUALITY",
                "ATTRIBUTION_QUALITY",
                "CONTRADICTION_COVERAGE",
                "GRAPH_HEALTH",
                "DISCOVERED_GAPS",
            }
        ),
    }
)

_JIN_OBJECTIVE_CATEGORIES = frozenset(
    {"FACTUAL_CORRECTNESS", "CITATION_COVERAGE", "PRIVACY"}
)
_JIN_INTERPRETIVE_CATEGORIES = frozenset(
    {"CORRECTION_HANDLING", "RETRIEVAL_QUALITY"}
)
_JIN_SUBJECTIVE_CATEGORIES = frozenset({"CLARITY", "USEFULNESS"})
_THEORY_OBJECTIVE_CATEGORIES = frozenset(
    {
        "MANIFEST_COMPLETENESS",
        "INGESTION_INTEGRITY",
        "REPRESENTATION_COVERAGE",
        "ATTRIBUTION_QUALITY",
        "CONTRADICTION_COVERAGE",
        "GRAPH_HEALTH",
    }
)
_THEORY_INTERPRETIVE_CATEGORIES = frozenset(
    {"RETRIEVAL_QUALITY", "DISCOVERED_GAPS"}
)

_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,127}$")
_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_FIELD_NAMES = frozenset(
    {
        "action",
        "api_key",
        "automatic_action",
        "cookie",
        "credential",
        "credentials",
        "goal",
        "goal_candidate",
        "intervention",
        "model_prompt",
        "overall_status",
        "password",
        "priority",
        "private_deck_text",
        "prompt",
        "prompt_log",
        "provider_payload",
        "raw_payload",
        "recommendation",
        "score",
        "secret",
        "session",
        "session_id",
        "token",
        "weight",
    }
)


class GoalEngineHealthError(ValueError):
    """Raised when a subsystem-health value violates the Phase44H contract."""


@dataclass(frozen=True)
class HealthSignalDefinition:
    definition_id: str
    definition_version: int
    domain: str
    category: str
    assessment_class: str
    title: str
    description: str
    pass_condition: str
    degraded_condition: str
    fail_condition: str
    unknown_condition: str
    allowed_evidence_classes: tuple[str, ...]
    policy_ref_ids: tuple[str, ...]
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.definition_id, "definition_id")
        _require_positive_int(self.definition_version, "definition_version")
        validate_health_domain(self.domain)
        _validate_category(self.domain, self.category)
        validate_assessment_class(self.assessment_class)
        _validate_domain_assessment_class(
            self.domain,
            self.category,
            self.assessment_class,
        )
        for field_name in (
            "title",
            "description",
            "pass_condition",
            "degraded_condition",
            "fail_condition",
            "unknown_condition",
        ):
            _require_text(getattr(self, field_name), field_name)
        object.__setattr__(
            self,
            "allowed_evidence_classes",
            _label_tuple(
                self.allowed_evidence_classes,
                "allowed_evidence_classes",
                sort=True,
            ),
        )
        object.__setattr__(
            self,
            "policy_ref_ids",
            _id_tuple(self.policy_ref_ids, "policy_ref_ids", sort=True),
        )
        _require_schema(self.schema_version, HEALTH_SIGNAL_DEFINITION_SCHEMA_VERSION)


@dataclass(frozen=True)
class HealthSignalObservation:
    signal_id: str
    definition_id: str
    definition_version: int
    domain: str
    category: str
    subject_id: str
    status: str
    summary: str
    observed_value: str | int | float | bool | None
    measurement_unit: str | None
    confidence: float
    observed_at: str
    fresh_until: str | None
    evidence_ref_ids: tuple[str, ...]
    conflict_ref_ids: tuple[str, ...]
    limitation: str | None
    not_applicable_reason: str | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.signal_id, "signal_id")
        _require_id(self.definition_id, "definition_id")
        _require_positive_int(self.definition_version, "definition_version")
        validate_health_domain(self.domain)
        _validate_category(self.domain, self.category)
        _require_id(self.subject_id, "subject_id")
        validate_signal_status(self.status)
        _require_text(self.summary, "summary")
        _require_observed_value(self.observed_value)
        if self.measurement_unit is not None:
            _require_label(self.measurement_unit, "measurement_unit")
        object.__setattr__(
            self,
            "confidence",
            _require_ratio(self.confidence, "confidence"),
        )
        observed_at = _parse_utc_timestamp(self.observed_at, "observed_at")
        if self.fresh_until is not None:
            fresh_until = _parse_utc_timestamp(self.fresh_until, "fresh_until")
            if fresh_until < observed_at:
                raise GoalEngineHealthError(
                    "fresh_until cannot precede observed_at"
                )
        object.__setattr__(
            self,
            "evidence_ref_ids",
            _id_tuple(self.evidence_ref_ids, "evidence_ref_ids", sort=True),
        )
        object.__setattr__(
            self,
            "conflict_ref_ids",
            _id_tuple(self.conflict_ref_ids, "conflict_ref_ids", sort=True),
        )
        overlap = sorted(set(self.evidence_ref_ids) & set(self.conflict_ref_ids))
        if overlap:
            raise GoalEngineHealthError(
                "supporting and conflicting evidence must remain separate"
            )
        if self.limitation is not None:
            _require_text(self.limitation, "limitation")
        if self.not_applicable_reason is not None:
            _require_text(self.not_applicable_reason, "not_applicable_reason")
        if self.status in {"PASS", "DEGRADED", "FAIL"} and not self.evidence_ref_ids:
            raise GoalEngineHealthError(f"{self.status} requires supporting evidence")
        if self.status == "UNKNOWN" and self.limitation is None:
            raise GoalEngineHealthError("UNKNOWN requires limitation")
        if self.status == "CONFLICTED" and len(self.conflict_ref_ids) < 2:
            raise GoalEngineHealthError(
                "CONFLICTED requires at least two conflict references"
            )
        if self.status != "CONFLICTED" and self.conflict_ref_ids:
            raise GoalEngineHealthError(
                "conflict references require CONFLICTED status"
            )
        if self.status == "NOT_APPLICABLE" and self.not_applicable_reason is None:
            raise GoalEngineHealthError(
                "NOT_APPLICABLE requires not_applicable_reason"
            )
        if self.status != "NOT_APPLICABLE" and self.not_applicable_reason is not None:
            raise GoalEngineHealthError(
                "not_applicable_reason requires NOT_APPLICABLE status"
            )
        _require_schema(self.schema_version, HEALTH_SIGNAL_OBSERVATION_SCHEMA_VERSION)


@dataclass(frozen=True)
class HealthManifest:
    manifest_id: str
    revision: int
    domain: str
    subject_id: str
    scope_label: str
    definition_ids: tuple[str, ...]
    required_definition_ids: tuple[str, ...]
    optional_definition_ids: tuple[str, ...]
    scope_manifest_ref_ids: tuple[str, ...]
    supersedes_manifest_hash: str | None
    created_at: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.manifest_id, "manifest_id")
        _require_positive_int(self.revision, "revision")
        validate_health_domain(self.domain)
        _require_id(self.subject_id, "subject_id")
        _require_text(self.scope_label, "scope_label")
        for field_name in (
            "definition_ids",
            "required_definition_ids",
            "optional_definition_ids",
            "scope_manifest_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                _id_tuple(getattr(self, field_name), field_name, sort=True),
            )
        if not self.definition_ids:
            raise GoalEngineHealthError("definition_ids cannot be empty")
        required = set(self.required_definition_ids)
        optional = set(self.optional_definition_ids)
        if required & optional:
            raise GoalEngineHealthError(
                "required and optional definition IDs must be disjoint"
            )
        if required | optional != set(self.definition_ids):
            raise GoalEngineHealthError(
                "required and optional definition IDs must exactly cover definition_ids"
            )
        if self.domain == "THEORY_CORPUS" and not self.scope_manifest_ref_ids:
            raise GoalEngineHealthError(
                "THEORY_CORPUS requires a declared corpus-manifest reference"
            )
        if self.revision == 1 and self.supersedes_manifest_hash is not None:
            raise GoalEngineHealthError(
                "manifest revision 1 cannot supersede an earlier manifest"
            )
        if self.revision > 1:
            if self.supersedes_manifest_hash is None:
                raise GoalEngineHealthError(
                    "later manifest revisions require supersedes_manifest_hash"
                )
            _require_sha256(
                self.supersedes_manifest_hash,
                "supersedes_manifest_hash",
            )
        _parse_utc_timestamp(self.created_at, "created_at")
        _require_schema(self.schema_version, HEALTH_MANIFEST_SCHEMA_VERSION)


@dataclass(frozen=True)
class HealthFinding:
    finding_id: FindingIdentifier
    domain: str
    finding_class: str
    signal_ids: tuple[str, ...]
    statement: str
    why_it_matters: str
    evidence_ref_ids: tuple[str, ...]
    conflict_ref_ids: tuple[str, ...]
    confidence: float
    disconfirmation_criteria: tuple[str, ...]
    limitations: tuple[str, ...]
    created_at: str
    schema_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.finding_id, FindingIdentifier):
            raise GoalEngineHealthError(
                "finding_id must be FindingIdentifier"
            )
        validate_health_domain(self.domain)
        validate_finding_class(self.finding_class)
        object.__setattr__(
            self,
            "signal_ids",
            _id_tuple(self.signal_ids, "signal_ids", sort=True),
        )
        if not self.signal_ids:
            raise GoalEngineHealthError("HealthFinding requires signal_ids")
        _require_text(self.statement, "statement")
        _require_text(self.why_it_matters, "why_it_matters")
        object.__setattr__(
            self,
            "evidence_ref_ids",
            _id_tuple(self.evidence_ref_ids, "evidence_ref_ids", sort=True),
        )
        object.__setattr__(
            self,
            "conflict_ref_ids",
            _id_tuple(self.conflict_ref_ids, "conflict_ref_ids", sort=True),
        )
        overlap = sorted(set(self.evidence_ref_ids) & set(self.conflict_ref_ids))
        if overlap:
            raise GoalEngineHealthError(
                "finding supporting and conflicting evidence must remain separate"
            )
        object.__setattr__(
            self,
            "confidence",
            _require_ratio(self.confidence, "confidence"),
        )
        object.__setattr__(
            self,
            "disconfirmation_criteria",
            _text_tuple(
                self.disconfirmation_criteria,
                "disconfirmation_criteria",
                sort=True,
            ),
        )
        if not self.disconfirmation_criteria:
            raise GoalEngineHealthError(
                "HealthFinding requires disconfirmation criteria"
            )
        object.__setattr__(
            self,
            "limitations",
            _text_tuple(self.limitations, "limitations", sort=True),
        )
        if not self.limitations:
            raise GoalEngineHealthError("HealthFinding requires limitations")
        _parse_utc_timestamp(self.created_at, "created_at")
        _require_schema(self.schema_version, HEALTH_FINDING_SCHEMA_VERSION)


@dataclass(frozen=True)
class SubsystemHealthAssessmentReference:
    assessment_id: str
    revision: int
    domain: str
    semantic_hash: str
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.assessment_id, "assessment_id")
        _require_positive_int(self.revision, "revision")
        validate_health_domain(self.domain)
        _require_sha256(self.semantic_hash, "semantic_hash")
        _require_schema(
            self.schema_version,
            SUBSYSTEM_HEALTH_ASSESSMENT_REFERENCE_SCHEMA_VERSION,
        )


@dataclass(frozen=True)
class SubsystemHealthAssessment:
    assessment_id: str
    revision: int
    domain: str
    manifest: HealthManifest
    as_of: str
    definitions: tuple[HealthSignalDefinition, ...]
    signals: tuple[HealthSignalObservation, ...]
    findings: tuple[HealthFinding, ...]
    evidence_snapshot: tuple[GoalEvidenceReference, ...]
    required_signal_count: int
    observed_required_signal_count: int
    unknown_required_signal_count: int
    conflicted_required_signal_count: int
    supersedes_assessment: SubsystemHealthAssessmentReference | None
    schema_version: str

    def __post_init__(self) -> None:
        _require_id(self.assessment_id, "assessment_id")
        _require_positive_int(self.revision, "revision")
        validate_health_domain(self.domain)
        if not isinstance(self.manifest, HealthManifest):
            raise GoalEngineHealthError("manifest must be HealthManifest")
        _parse_utc_timestamp(self.as_of, "as_of")
        object.__setattr__(self, "definitions", _definition_tuple(self.definitions))
        object.__setattr__(self, "signals", _observation_tuple(self.signals))
        object.__setattr__(self, "findings", _finding_tuple(self.findings))
        object.__setattr__(
            self,
            "evidence_snapshot",
            _evidence_reference_tuple(self.evidence_snapshot),
        )
        for field_name in (
            "required_signal_count",
            "observed_required_signal_count",
            "unknown_required_signal_count",
            "conflicted_required_signal_count",
        ):
            _require_nonnegative_int(getattr(self, field_name), field_name)
        if self.revision == 1 and self.supersedes_assessment is not None:
            raise GoalEngineHealthError(
                "assessment revision 1 cannot supersede an earlier assessment"
            )
        if self.revision > 1:
            if not isinstance(
                self.supersedes_assessment,
                SubsystemHealthAssessmentReference,
            ):
                raise GoalEngineHealthError(
                    "later assessment revisions require supersedes_assessment"
                )
            if self.supersedes_assessment.assessment_id != self.assessment_id:
                raise GoalEngineHealthError(
                    "superseded assessment must use the same assessment_id"
                )
            if self.supersedes_assessment.domain != self.domain:
                raise GoalEngineHealthError(
                    "superseded assessment must use the same domain"
                )
            if self.supersedes_assessment.revision != self.revision - 1:
                raise GoalEngineHealthError(
                    "superseded assessment must be the immediately prior revision"
                )
        _require_schema(
            self.schema_version,
            SUBSYSTEM_HEALTH_ASSESSMENT_SCHEMA_VERSION,
        )
        validate_subsystem_health_assessment(self)


def validate_health_domain(value: str) -> str:
    return _require_allowed(value, HEALTH_DOMAINS, "health domain")


def validate_assessment_class(value: str) -> str:
    return _require_allowed(value, ASSESSMENT_CLASSES, "assessment class")


def validate_signal_status(value: str) -> str:
    return _require_allowed(value, SIGNAL_STATUSES, "signal status")


def validate_finding_class(value: str) -> str:
    return _require_allowed(value, FINDING_CLASSES, "finding class")


def validate_health_signal_definition(
    definition: HealthSignalDefinition,
) -> HealthSignalDefinition:
    _require_type(definition, HealthSignalDefinition, "definition")
    _validate_domain_assessment_class(
        definition.domain,
        definition.category,
        definition.assessment_class,
    )
    return definition


def validate_health_manifest(
    manifest: HealthManifest,
    definitions: tuple[HealthSignalDefinition, ...] | None = None,
    evidence_snapshot: tuple[GoalEvidenceReference, ...] | None = None,
    prior_manifest: HealthManifest | None = None,
) -> HealthManifest:
    _require_type(manifest, HealthManifest, "manifest")
    if definitions is not None:
        definition_values = _definition_tuple(definitions)
        definition_ids = tuple(item.definition_id for item in definition_values)
        if definition_ids != manifest.definition_ids:
            raise GoalEngineHealthError(
                "definitions must exactly match manifest definition_ids"
            )
        if any(item.domain != manifest.domain for item in definition_values):
            raise GoalEngineHealthError(
                "manifest definitions must remain in one domain"
            )
    if evidence_snapshot is not None:
        evidence_values = _evidence_reference_tuple(evidence_snapshot)
        evidence_ids = {item.evidence_ref_id for item in evidence_values}
        missing = sorted(set(manifest.scope_manifest_ref_ids) - evidence_ids)
        if missing:
            raise GoalEngineHealthError(
                f"dangling scope manifest reference: {missing[0]}"
            )
    if prior_manifest is not None:
        _require_type(prior_manifest, HealthManifest, "prior_manifest")
        if manifest.revision != prior_manifest.revision + 1:
            raise GoalEngineHealthError(
                "manifest must supersede the immediately prior revision"
            )
        if manifest.manifest_id != prior_manifest.manifest_id:
            raise GoalEngineHealthError(
                "manifest revision must retain manifest_id"
            )
        if manifest.domain != prior_manifest.domain:
            raise GoalEngineHealthError("manifest revision must retain domain")
        if manifest.subject_id != prior_manifest.subject_id:
            raise GoalEngineHealthError("manifest revision must retain subject_id")
        expected_hash = health_manifest_semantic_hash(prior_manifest)
        if manifest.supersedes_manifest_hash != expected_hash:
            raise GoalEngineHealthError(
                "supersedes_manifest_hash does not match prior manifest"
            )
    return manifest


def validate_subsystem_health_assessment(
    assessment: SubsystemHealthAssessment,
) -> SubsystemHealthAssessment:
    _require_type(assessment, SubsystemHealthAssessment, "assessment")
    if assessment.domain != assessment.manifest.domain:
        raise GoalEngineHealthError("assessment and manifest domains must match")
    validate_health_manifest(
        assessment.manifest,
        assessment.definitions,
        assessment.evidence_snapshot,
    )
    definition_by_id = {item.definition_id: item for item in assessment.definitions}
    evidence_by_id = {
        item.evidence_ref_id: item for item in assessment.evidence_snapshot
    }
    observations_by_definition: dict[str, HealthSignalObservation] = {}
    for observation in assessment.signals:
        definition = definition_by_id.get(observation.definition_id)
        if definition is None:
            raise GoalEngineHealthError(
                f"observation references unknown definition: {observation.definition_id}"
            )
        if observation.definition_id in observations_by_definition:
            raise GoalEngineHealthError(
                f"duplicate observation for definition: {observation.definition_id}"
            )
        _validate_observation_against_definition(
            observation,
            definition,
            assessment.manifest,
            evidence_by_id,
        )
        observations_by_definition[observation.definition_id] = observation
    missing_required = sorted(
        set(assessment.manifest.required_definition_ids)
        - set(observations_by_definition)
    )
    if missing_required:
        raise GoalEngineHealthError(
            f"missing required observation: {missing_required[0]}"
        )
    required_observations = tuple(
        observations_by_definition[definition_id]
        for definition_id in assessment.manifest.required_definition_ids
    )
    expected_counts = (
        len(assessment.manifest.required_definition_ids),
        len(required_observations),
        sum(item.status == "UNKNOWN" for item in required_observations),
        sum(item.status == "CONFLICTED" for item in required_observations),
    )
    actual_counts = (
        assessment.required_signal_count,
        assessment.observed_required_signal_count,
        assessment.unknown_required_signal_count,
        assessment.conflicted_required_signal_count,
    )
    if actual_counts != expected_counts:
        raise GoalEngineHealthError("assessment manifest counts do not match signals")
    signal_by_id = {item.signal_id: item for item in assessment.signals}
    semantic_findings: set[tuple[Any, ...]] = set()
    as_of_value = _parse_utc_timestamp(assessment.as_of, "as_of")
    for finding in assessment.findings:
        _validate_finding_against_signals(
            finding,
            signal_by_id,
            evidence_by_id,
            as_of_value,
        )
        key = _finding_semantic_key(finding)
        if key in semantic_findings:
            raise GoalEngineHealthError("duplicate semantic HealthFinding")
        semantic_findings.add(key)
    return assessment


def validate_subsystem_health_assessment_revision(
    assessment: SubsystemHealthAssessment,
    prior_assessment: SubsystemHealthAssessment,
) -> SubsystemHealthAssessment:
    validate_subsystem_health_assessment(assessment)
    validate_subsystem_health_assessment(prior_assessment)
    if assessment.revision != prior_assessment.revision + 1:
        raise GoalEngineHealthError(
            "assessment must supersede the immediately prior revision"
        )
    if assessment.assessment_id != prior_assessment.assessment_id:
        raise GoalEngineHealthError("assessment revision must retain assessment_id")
    if assessment.domain != prior_assessment.domain:
        raise GoalEngineHealthError("assessment revision must retain domain")
    reference = assessment.supersedes_assessment
    if reference is None:
        raise GoalEngineHealthError(
            "later assessment revision requires supersedes_assessment"
        )
    if reference.semantic_hash != subsystem_health_assessment_semantic_hash(
        prior_assessment
    ):
        raise GoalEngineHealthError(
            "supersedes_assessment semantic hash does not match prior assessment"
        )
    return assessment


def build_subsystem_health_assessment(
    *,
    assessment_id: str,
    revision: int,
    domain: str,
    manifest: HealthManifest,
    as_of: str,
    definitions: tuple[HealthSignalDefinition, ...],
    signals: tuple[HealthSignalObservation, ...],
    evidence_snapshot: tuple[GoalEvidenceReference, ...],
    policy_snapshot: tuple[GoalPolicyRecord, ...] = (),
    findings: tuple[HealthFinding, ...] = (),
    supersedes_assessment: SubsystemHealthAssessmentReference | None = None,
    prior_manifest: HealthManifest | None = None,
    prior_assessment: SubsystemHealthAssessment | None = None,
) -> SubsystemHealthAssessment:
    validate_health_domain(domain)
    as_of_value = _parse_utc_timestamp(as_of, "as_of")
    definition_values = _definition_tuple(definitions)
    signal_values = _observation_tuple(signals)
    evidence_values = _evidence_reference_tuple(evidence_snapshot)
    caller_findings = _finding_tuple(findings)
    policy_values = _policy_record_tuple(policy_snapshot)
    if manifest.domain != domain:
        raise GoalEngineHealthError("builder and manifest domains must match")
    if manifest.revision > 1 and prior_manifest is None:
        raise GoalEngineHealthError(
            "prior_manifest is required to build a later manifest revision"
        )
    validate_health_manifest(
        manifest,
        definition_values,
        evidence_values,
        prior_manifest,
    )
    _validate_policy_references(definition_values, policy_values)
    evidence_by_id = {item.evidence_ref_id: item for item in evidence_values}
    definition_by_id = {item.definition_id: item for item in definition_values}
    observations_by_definition: dict[str, HealthSignalObservation] = {}
    for observation in signal_values:
        definition = definition_by_id.get(observation.definition_id)
        if definition is None:
            raise GoalEngineHealthError(
                f"observation references unknown definition: {observation.definition_id}"
            )
        if observation.definition_id in observations_by_definition:
            raise GoalEngineHealthError(
                f"duplicate observation for definition: {observation.definition_id}"
            )
        _validate_observation_against_definition(
            observation,
            definition,
            manifest,
            evidence_by_id,
        )
        observations_by_definition[observation.definition_id] = observation
    missing_required = sorted(
        set(manifest.required_definition_ids) - set(observations_by_definition)
    )
    if missing_required:
        raise GoalEngineHealthError(
            f"missing required observation: {missing_required[0]}"
        )
    signal_by_id = {item.signal_id: item for item in signal_values}
    for finding in caller_findings:
        _validate_finding_against_signals(
            finding,
            signal_by_id,
            evidence_by_id,
            as_of_value,
        )
    generated_findings: list[HealthFinding] = []
    for observation in signal_values:
        definition = definition_by_id[observation.definition_id]
        generated_findings.extend(
            _generated_findings(
                observation,
                definition,
                as_of,
                as_of_value,
                evidence_by_id,
            )
        )
    combined_findings = _finding_tuple(tuple(generated_findings) + caller_findings)
    semantic_keys: set[tuple[Any, ...]] = set()
    for finding in combined_findings:
        key = _finding_semantic_key(finding)
        if key in semantic_keys:
            raise GoalEngineHealthError("duplicate semantic HealthFinding")
        semantic_keys.add(key)
    required_observations = tuple(
        observations_by_definition[definition_id]
        for definition_id in manifest.required_definition_ids
    )
    assessment = SubsystemHealthAssessment(
        assessment_id=assessment_id,
        revision=revision,
        domain=domain,
        manifest=manifest,
        as_of=as_of,
        definitions=definition_values,
        signals=signal_values,
        findings=combined_findings,
        evidence_snapshot=evidence_values,
        required_signal_count=len(manifest.required_definition_ids),
        observed_required_signal_count=len(required_observations),
        unknown_required_signal_count=sum(
            item.status == "UNKNOWN" for item in required_observations
        ),
        conflicted_required_signal_count=sum(
            item.status == "CONFLICTED" for item in required_observations
        ),
        supersedes_assessment=supersedes_assessment,
        schema_version=SUBSYSTEM_HEALTH_ASSESSMENT_SCHEMA_VERSION,
    )
    if prior_assessment is not None:
        validate_subsystem_health_assessment_revision(assessment, prior_assessment)
    elif revision > 1:
        raise GoalEngineHealthError(
            "prior_assessment is required to build a later assessment revision"
        )
    return assessment


def health_signal_definition_to_dict(
    definition: HealthSignalDefinition,
) -> dict[str, Any]:
    _require_type(definition, HealthSignalDefinition, "definition")
    return {
        "definition_id": definition.definition_id,
        "definition_version": definition.definition_version,
        "domain": definition.domain,
        "category": definition.category,
        "assessment_class": definition.assessment_class,
        "title": definition.title,
        "description": definition.description,
        "pass_condition": definition.pass_condition,
        "degraded_condition": definition.degraded_condition,
        "fail_condition": definition.fail_condition,
        "unknown_condition": definition.unknown_condition,
        "allowed_evidence_classes": list(definition.allowed_evidence_classes),
        "policy_ref_ids": list(definition.policy_ref_ids),
        "schema_version": definition.schema_version,
    }


def health_signal_definition_from_dict(
    payload: Mapping[str, Any],
) -> HealthSignalDefinition:
    fields = {
        "definition_id",
        "definition_version",
        "domain",
        "category",
        "assessment_class",
        "title",
        "description",
        "pass_condition",
        "degraded_condition",
        "fail_condition",
        "unknown_condition",
        "allowed_evidence_classes",
        "policy_ref_ids",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    data["allowed_evidence_classes"] = _json_tuple(
        data["allowed_evidence_classes"],
        "allowed_evidence_classes",
    )
    data["policy_ref_ids"] = _json_tuple(data["policy_ref_ids"], "policy_ref_ids")
    return HealthSignalDefinition(**data)


def health_signal_observation_to_dict(
    observation: HealthSignalObservation,
) -> dict[str, Any]:
    _require_type(observation, HealthSignalObservation, "observation")
    return {
        "signal_id": observation.signal_id,
        "definition_id": observation.definition_id,
        "definition_version": observation.definition_version,
        "domain": observation.domain,
        "category": observation.category,
        "subject_id": observation.subject_id,
        "status": observation.status,
        "summary": observation.summary,
        "observed_value": observation.observed_value,
        "measurement_unit": observation.measurement_unit,
        "confidence": observation.confidence,
        "observed_at": observation.observed_at,
        "fresh_until": observation.fresh_until,
        "evidence_ref_ids": list(observation.evidence_ref_ids),
        "conflict_ref_ids": list(observation.conflict_ref_ids),
        "limitation": observation.limitation,
        "not_applicable_reason": observation.not_applicable_reason,
        "schema_version": observation.schema_version,
    }


def health_signal_observation_from_dict(
    payload: Mapping[str, Any],
) -> HealthSignalObservation:
    fields = {
        "signal_id",
        "definition_id",
        "definition_version",
        "domain",
        "category",
        "subject_id",
        "status",
        "summary",
        "observed_value",
        "measurement_unit",
        "confidence",
        "observed_at",
        "fresh_until",
        "evidence_ref_ids",
        "conflict_ref_ids",
        "limitation",
        "not_applicable_reason",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    data["evidence_ref_ids"] = _json_tuple(
        data["evidence_ref_ids"],
        "evidence_ref_ids",
    )
    data["conflict_ref_ids"] = _json_tuple(
        data["conflict_ref_ids"],
        "conflict_ref_ids",
    )
    return HealthSignalObservation(**data)


def health_manifest_to_dict(manifest: HealthManifest) -> dict[str, Any]:
    _require_type(manifest, HealthManifest, "manifest")
    return {
        "manifest_id": manifest.manifest_id,
        "revision": manifest.revision,
        "domain": manifest.domain,
        "subject_id": manifest.subject_id,
        "scope_label": manifest.scope_label,
        "definition_ids": list(manifest.definition_ids),
        "required_definition_ids": list(manifest.required_definition_ids),
        "optional_definition_ids": list(manifest.optional_definition_ids),
        "scope_manifest_ref_ids": list(manifest.scope_manifest_ref_ids),
        "supersedes_manifest_hash": manifest.supersedes_manifest_hash,
        "created_at": manifest.created_at,
        "schema_version": manifest.schema_version,
    }


def health_manifest_from_dict(payload: Mapping[str, Any]) -> HealthManifest:
    fields = {
        "manifest_id",
        "revision",
        "domain",
        "subject_id",
        "scope_label",
        "definition_ids",
        "required_definition_ids",
        "optional_definition_ids",
        "scope_manifest_ref_ids",
        "supersedes_manifest_hash",
        "created_at",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    for field_name in (
        "definition_ids",
        "required_definition_ids",
        "optional_definition_ids",
        "scope_manifest_ref_ids",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return HealthManifest(**data)


def health_finding_to_dict(finding: HealthFinding) -> dict[str, Any]:
    _require_type(finding, HealthFinding, "finding")
    return {
        "finding_id": finding_identifier_to_dict(finding.finding_id),
        "domain": finding.domain,
        "finding_class": finding.finding_class,
        "signal_ids": list(finding.signal_ids),
        "statement": finding.statement,
        "why_it_matters": finding.why_it_matters,
        "evidence_ref_ids": list(finding.evidence_ref_ids),
        "conflict_ref_ids": list(finding.conflict_ref_ids),
        "confidence": finding.confidence,
        "disconfirmation_criteria": list(finding.disconfirmation_criteria),
        "limitations": list(finding.limitations),
        "created_at": finding.created_at,
        "schema_version": finding.schema_version,
    }


def health_finding_from_dict(payload: Mapping[str, Any]) -> HealthFinding:
    fields = {
        "finding_id",
        "domain",
        "finding_class",
        "signal_ids",
        "statement",
        "why_it_matters",
        "evidence_ref_ids",
        "conflict_ref_ids",
        "confidence",
        "disconfirmation_criteria",
        "limitations",
        "created_at",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    data["finding_id"] = finding_identifier_from_dict(
        _require_mapping(data["finding_id"], "finding_id")
    )
    for field_name in (
        "signal_ids",
        "evidence_ref_ids",
        "conflict_ref_ids",
        "disconfirmation_criteria",
        "limitations",
    ):
        data[field_name] = _json_tuple(data[field_name], field_name)
    return HealthFinding(**data)


def subsystem_health_assessment_reference_to_dict(
    reference: SubsystemHealthAssessmentReference,
) -> dict[str, Any]:
    _require_type(
        reference,
        SubsystemHealthAssessmentReference,
        "reference",
    )
    return {
        "assessment_id": reference.assessment_id,
        "revision": reference.revision,
        "domain": reference.domain,
        "semantic_hash": reference.semantic_hash,
        "schema_version": reference.schema_version,
    }


def subsystem_health_assessment_reference_from_dict(
    payload: Mapping[str, Any],
) -> SubsystemHealthAssessmentReference:
    data = _require_fields(
        payload,
        {"assessment_id", "revision", "domain", "semantic_hash", "schema_version"},
    )
    return SubsystemHealthAssessmentReference(**data)


def subsystem_health_assessment_to_dict(
    assessment: SubsystemHealthAssessment,
) -> dict[str, Any]:
    _require_type(assessment, SubsystemHealthAssessment, "assessment")
    return {
        "assessment_id": assessment.assessment_id,
        "revision": assessment.revision,
        "domain": assessment.domain,
        "manifest": health_manifest_to_dict(assessment.manifest),
        "as_of": assessment.as_of,
        "definitions": [
            health_signal_definition_to_dict(item) for item in assessment.definitions
        ],
        "signals": [
            health_signal_observation_to_dict(item) for item in assessment.signals
        ],
        "findings": [health_finding_to_dict(item) for item in assessment.findings],
        "evidence_snapshot": [
            goal_evidence_reference_to_dict(item)
            for item in assessment.evidence_snapshot
        ],
        "required_signal_count": assessment.required_signal_count,
        "observed_required_signal_count": assessment.observed_required_signal_count,
        "unknown_required_signal_count": assessment.unknown_required_signal_count,
        "conflicted_required_signal_count": assessment.conflicted_required_signal_count,
        "supersedes_assessment": (
            subsystem_health_assessment_reference_to_dict(
                assessment.supersedes_assessment
            )
            if assessment.supersedes_assessment is not None
            else None
        ),
        "schema_version": assessment.schema_version,
    }


def subsystem_health_assessment_from_dict(
    payload: Mapping[str, Any],
) -> SubsystemHealthAssessment:
    fields = {
        "assessment_id",
        "revision",
        "domain",
        "manifest",
        "as_of",
        "definitions",
        "signals",
        "findings",
        "evidence_snapshot",
        "required_signal_count",
        "observed_required_signal_count",
        "unknown_required_signal_count",
        "conflicted_required_signal_count",
        "supersedes_assessment",
        "schema_version",
    }
    data = _require_fields(payload, fields)
    data["manifest"] = health_manifest_from_dict(
        _require_mapping(data["manifest"], "manifest")
    )
    data["definitions"] = tuple(
        health_signal_definition_from_dict(_require_mapping(item, "definition"))
        for item in _json_tuple(data["definitions"], "definitions")
    )
    data["signals"] = tuple(
        health_signal_observation_from_dict(_require_mapping(item, "signal"))
        for item in _json_tuple(data["signals"], "signals")
    )
    data["findings"] = tuple(
        health_finding_from_dict(_require_mapping(item, "finding"))
        for item in _json_tuple(data["findings"], "findings")
    )
    data["evidence_snapshot"] = tuple(
        goal_evidence_reference_from_dict(_require_mapping(item, "evidence"))
        for item in _json_tuple(data["evidence_snapshot"], "evidence_snapshot")
    )
    if data["supersedes_assessment"] is not None:
        data["supersedes_assessment"] = (
            subsystem_health_assessment_reference_from_dict(
                _require_mapping(
                    data["supersedes_assessment"],
                    "supersedes_assessment",
                )
            )
        )
    return SubsystemHealthAssessment(**data)


def health_signal_definition_semantic_hash(
    definition: HealthSignalDefinition,
) -> str:
    return semantic_hash(health_signal_definition_to_dict(definition))


def health_signal_observation_semantic_hash(
    observation: HealthSignalObservation,
) -> str:
    return semantic_hash(health_signal_observation_to_dict(observation))


def health_manifest_semantic_hash(manifest: HealthManifest) -> str:
    return semantic_hash(health_manifest_to_dict(manifest))


def health_finding_semantic_hash(finding: HealthFinding) -> str:
    return semantic_hash(health_finding_to_dict(finding))


def subsystem_health_assessment_reference_semantic_hash(
    reference: SubsystemHealthAssessmentReference,
) -> str:
    return semantic_hash(subsystem_health_assessment_reference_to_dict(reference))


def subsystem_health_assessment_semantic_hash(
    assessment: SubsystemHealthAssessment,
) -> str:
    return semantic_hash(subsystem_health_assessment_to_dict(assessment))


def _validate_category(domain: str, category: str) -> str:
    validate_health_domain(domain)
    return _require_allowed(category, HEALTH_CATEGORIES[domain], "health category")


def _validate_domain_assessment_class(
    domain: str,
    category: str,
    assessment_class: str,
) -> None:
    if domain == "CODIE" and assessment_class != "OBJECTIVE":
        raise GoalEngineHealthError("CODIE signals must be OBJECTIVE in v1")
    if domain == "JIN":
        if category in _JIN_OBJECTIVE_CATEGORIES and assessment_class != "OBJECTIVE":
            raise GoalEngineHealthError(
                f"JIN {category} signals must be OBJECTIVE"
            )
        if category in _JIN_INTERPRETIVE_CATEGORIES and assessment_class not in {
            "OBJECTIVE",
            "SEMI_OBJECTIVE",
        }:
            raise GoalEngineHealthError(
                f"JIN {category} signals cannot be SUBJECTIVE"
            )
        if category in _JIN_SUBJECTIVE_CATEGORIES and assessment_class != "SUBJECTIVE":
            raise GoalEngineHealthError(
                f"JIN {category} signals must be SUBJECTIVE"
            )
    if domain == "THEORY_CORPUS":
        if category in _THEORY_OBJECTIVE_CATEGORIES and assessment_class != "OBJECTIVE":
            raise GoalEngineHealthError(
                f"THEORY_CORPUS {category} signals must be OBJECTIVE"
            )
        if category in _THEORY_INTERPRETIVE_CATEGORIES and assessment_class not in {
            "OBJECTIVE",
            "SEMI_OBJECTIVE",
        }:
            raise GoalEngineHealthError(
                f"THEORY_CORPUS {category} signals cannot be SUBJECTIVE"
            )


def _validate_observation_against_definition(
    observation: HealthSignalObservation,
    definition: HealthSignalDefinition,
    manifest: HealthManifest,
    evidence_by_id: Mapping[str, GoalEvidenceReference],
) -> None:
    if observation.domain != definition.domain or observation.domain != manifest.domain:
        raise GoalEngineHealthError("observation must remain in definition domain")
    if observation.category != definition.category:
        raise GoalEngineHealthError("observation category must match definition")
    if observation.definition_version != definition.definition_version:
        raise GoalEngineHealthError("observation definition version must match")
    if observation.subject_id != manifest.subject_id:
        raise GoalEngineHealthError("observation subject_id must match manifest")
    if observation.definition_id not in manifest.definition_ids:
        raise GoalEngineHealthError("observation definition is outside manifest")
    if (
        observation.definition_id in manifest.required_definition_ids
        and observation.status == "NOT_APPLICABLE"
    ):
        raise GoalEngineHealthError(
            "NOT_APPLICABLE cannot hide a required signal"
        )
    referenced_ids = set(observation.evidence_ref_ids) | set(
        observation.conflict_ref_ids
    )
    missing = sorted(referenced_ids - set(evidence_by_id))
    if missing:
        raise GoalEngineHealthError(f"dangling evidence reference: {missing[0]}")
    disallowed = sorted(
        evidence_ref_id
        for evidence_ref_id in referenced_ids
        if evidence_by_id[evidence_ref_id].evidence_class
        not in definition.allowed_evidence_classes
    )
    if disallowed:
        raise GoalEngineHealthError(
            f"evidence class is not allowed by definition: {disallowed[0]}"
        )


def _validate_finding_against_signals(
    finding: HealthFinding,
    signal_by_id: Mapping[str, HealthSignalObservation],
    evidence_by_id: Mapping[str, GoalEvidenceReference],
    as_of: datetime,
) -> None:
    missing_signals = sorted(set(finding.signal_ids) - set(signal_by_id))
    if missing_signals:
        raise GoalEngineHealthError(
            f"finding references unknown signal: {missing_signals[0]}"
        )
    signals = tuple(signal_by_id[item] for item in finding.signal_ids)
    if any(item.domain != finding.domain for item in signals):
        raise GoalEngineHealthError("finding and signal domains must match")
    if finding.finding_class != "STALE_EVIDENCE" and any(
        item.status in {"PASS", "NOT_APPLICABLE"} for item in signals
    ):
        raise GoalEngineHealthError(
            "finding cannot resolve from PASS or NOT_APPLICABLE signal"
        )
    if finding.finding_class == "STALE_EVIDENCE":
        if any(item.status == "NOT_APPLICABLE" for item in signals):
            raise GoalEngineHealthError(
                "STALE_EVIDENCE cannot resolve from NOT_APPLICABLE signal"
            )
        if not all(
            item.fresh_until is not None
            and as_of > _parse_utc_timestamp(item.fresh_until, "fresh_until")
            for item in signals
        ):
            raise GoalEngineHealthError(
                "STALE_EVIDENCE requires stale caller-supplied signals"
            )
    expected_statuses = {
        "DEGRADATION": {"DEGRADED"},
        "FAILURE": {"FAIL"},
        "EVIDENCE_GAP": {"UNKNOWN"},
        "EVIDENCE_CONFLICT": {"CONFLICTED"},
        "PRIVACY_OR_SECURITY": {"DEGRADED", "FAIL"},
        "MANIFEST_GAP": {"UNKNOWN"},
    }
    if finding.finding_class in expected_statuses and any(
        item.status not in expected_statuses[finding.finding_class]
        for item in signals
    ):
        raise GoalEngineHealthError(
            "finding class does not match source signal status"
        )
    allowed_evidence = set().union(*(set(item.evidence_ref_ids) for item in signals))
    allowed_conflicts = set().union(*(set(item.conflict_ref_ids) for item in signals))
    if not set(finding.evidence_ref_ids) <= allowed_evidence:
        raise GoalEngineHealthError("finding evidence exceeds source signals")
    if not set(finding.conflict_ref_ids) <= allowed_conflicts:
        raise GoalEngineHealthError(
            "finding conflict evidence exceeds source signals"
        )
    missing_evidence = sorted(
        (set(finding.evidence_ref_ids) | set(finding.conflict_ref_ids))
        - set(evidence_by_id)
    )
    if missing_evidence:
        raise GoalEngineHealthError(
            f"finding contains dangling evidence reference: {missing_evidence[0]}"
        )
    if finding.finding_class == "EVIDENCE_CONFLICT" and len(
        finding.conflict_ref_ids
    ) < 2:
        raise GoalEngineHealthError(
            "EVIDENCE_CONFLICT requires at least two conflict references"
        )
    if finding.finding_class == "EVIDENCE_CONFLICT" and set(
        finding.conflict_ref_ids
    ) != allowed_conflicts:
        raise GoalEngineHealthError(
            "EVIDENCE_CONFLICT must preserve all source conflict references"
        )
    privacy_categories = {"SECURITY_PRIVACY", "PRIVACY"}
    if finding.finding_class == "PRIVACY_OR_SECURITY" and not any(
        item.category in privacy_categories for item in signals
    ):
        raise GoalEngineHealthError(
            "PRIVACY_OR_SECURITY requires a privacy or security signal"
        )


def _validate_policy_references(
    definitions: tuple[HealthSignalDefinition, ...],
    policy_snapshot: tuple[GoalPolicyRecord, ...],
) -> None:
    policy_ids = {item.policy_id for item in policy_snapshot}
    required_ids = set().union(*(set(item.policy_ref_ids) for item in definitions))
    missing = sorted(required_ids - policy_ids)
    if missing:
        raise GoalEngineHealthError(f"dangling policy reference: {missing[0]}")


def _generated_findings(
    observation: HealthSignalObservation,
    definition: HealthSignalDefinition,
    as_of: str,
    as_of_value: datetime,
    evidence_by_id: Mapping[str, GoalEvidenceReference],
) -> tuple[HealthFinding, ...]:
    finding_classes: list[str] = []
    if observation.status == "DEGRADED":
        finding_classes.append(
            "PRIVACY_OR_SECURITY"
            if observation.category in {"SECURITY_PRIVACY", "PRIVACY"}
            else "DEGRADATION"
        )
    elif observation.status == "FAIL":
        finding_classes.append(
            "PRIVACY_OR_SECURITY"
            if observation.category in {"SECURITY_PRIVACY", "PRIVACY"}
            else "FAILURE"
        )
    elif observation.status == "UNKNOWN":
        finding_classes.append(
            "MANIFEST_GAP"
            if observation.domain == "THEORY_CORPUS"
            and observation.category == "MANIFEST_COMPLETENESS"
            else "EVIDENCE_GAP"
        )
    elif observation.status == "CONFLICTED":
        finding_classes.append("EVIDENCE_CONFLICT")
    if (
        observation.status != "NOT_APPLICABLE"
        and observation.fresh_until is not None
        and as_of_value > _parse_utc_timestamp(
        observation.fresh_until,
        "fresh_until",
        )
    ):
        finding_classes.append("STALE_EVIDENCE")
    return tuple(
        _generated_finding(
            observation,
            definition,
            finding_class,
            as_of,
            evidence_by_id,
        )
        for finding_class in finding_classes
    )


def _generated_finding(
    observation: HealthSignalObservation,
    definition: HealthSignalDefinition,
    finding_class: str,
    as_of: str,
    evidence_by_id: Mapping[str, GoalEvidenceReference],
) -> HealthFinding:
    disconfirmation: tuple[str, ...]
    identity_payload = {
        "domain": observation.domain,
        "subject_id": observation.subject_id,
        "definition": health_signal_definition_to_dict(definition),
        "signal": health_signal_observation_to_dict(observation),
        "finding_class": finding_class,
        "evidence_semantics": [
            goal_evidence_reference_to_dict(evidence_by_id[evidence_ref_id])
            for evidence_ref_id in (
                observation.evidence_ref_ids + observation.conflict_ref_ids
            )
        ],
    }
    finding_id = FindingIdentifier(
        entity_kind="FINDING",
        local_id=f"health:{semantic_hash(identity_payload)}",
        schema_version=IDENTIFIER_SCHEMA_VERSION,
    )
    if finding_class == "STALE_EVIDENCE":
        disconfirmation = (
            f"Supply current evidence with fresh_until at or after {as_of}.",
        )
        limitations = (
            "The caller-supplied signal status is preserved; only freshness is flagged.",
        )
    elif finding_class in {"EVIDENCE_GAP", "MANIFEST_GAP"}:
        disconfirmation = (definition.unknown_condition,)
        limitations = (
            observation.limitation or "The required evidence is not currently available.",
        )
    elif finding_class == "EVIDENCE_CONFLICT":
        disconfirmation = (
            "Resolve the cited conflicting evidence without discarding provenance.",
        )
        limitations = (
            observation.limitation or "The cited evidence remains conflicted.",
        )
    else:
        disconfirmation = _unique_texts(
            (definition.pass_condition, definition.degraded_condition)
            if observation.status == "FAIL"
            else (definition.pass_condition,)
        )
        limitations = (
            observation.limitation or "This finding is bounded to the cited signal evidence.",
        )
    why = {
        "DEGRADATION": "The signal does not currently meet its pass condition.",
        "FAILURE": "The signal meets its declared failure condition.",
        "EVIDENCE_GAP": "A required conclusion cannot be supported without more evidence.",
        "EVIDENCE_CONFLICT": "Incompatible evidence prevents a single factual conclusion.",
        "STALE_EVIDENCE": "Current applicability cannot be inferred from stale evidence.",
        "PRIVACY_OR_SECURITY": "The bounded privacy or security signal requires review.",
        "MANIFEST_GAP": "Corpus health is bounded by its declared manifest coverage.",
    }[finding_class]
    return HealthFinding(
        finding_id=finding_id,
        domain=observation.domain,
        finding_class=finding_class,
        signal_ids=(observation.signal_id,),
        statement=observation.summary,
        why_it_matters=why,
        evidence_ref_ids=observation.evidence_ref_ids,
        conflict_ref_ids=observation.conflict_ref_ids,
        confidence=observation.confidence,
        disconfirmation_criteria=disconfirmation,
        limitations=limitations,
        created_at=as_of,
        schema_version=HEALTH_FINDING_SCHEMA_VERSION,
    )


def _finding_semantic_key(finding: HealthFinding) -> tuple[Any, ...]:
    return (
        finding.domain,
        finding.finding_class,
        finding.signal_ids,
        finding.evidence_ref_ids,
        finding.conflict_ref_ids,
    )


def _definition_tuple(
    values: tuple[HealthSignalDefinition, ...],
) -> tuple[HealthSignalDefinition, ...]:
    return _record_tuple(
        values,
        HealthSignalDefinition,
        "definitions",
        lambda item: item.definition_id,
    )


def _observation_tuple(
    values: tuple[HealthSignalObservation, ...],
) -> tuple[HealthSignalObservation, ...]:
    return _record_tuple(
        values,
        HealthSignalObservation,
        "signals",
        lambda item: item.signal_id,
    )


def _finding_tuple(values: tuple[HealthFinding, ...]) -> tuple[HealthFinding, ...]:
    return _record_tuple(
        values,
        HealthFinding,
        "findings",
        lambda item: item.finding_id.local_id,
    )


def _evidence_reference_tuple(
    values: tuple[GoalEvidenceReference, ...],
) -> tuple[GoalEvidenceReference, ...]:
    return _record_tuple(
        values,
        GoalEvidenceReference,
        "evidence_snapshot",
        lambda item: item.evidence_ref_id,
    )


def _policy_record_tuple(
    values: tuple[GoalPolicyRecord, ...],
) -> tuple[GoalPolicyRecord, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineHealthError("policy_snapshot must be a tuple")
    for item in values:
        if not isinstance(item, GoalPolicyRecord):
            raise GoalEngineHealthError(
                "policy_snapshot must contain GoalPolicyRecord values"
            )
    ordered = tuple(sorted(values, key=lambda item: (item.policy_id, item.policy_version)))
    duplicate_ids = _duplicates([item.policy_id for item in ordered])
    if duplicate_ids:
        raise GoalEngineHealthError(
            f"policy_snapshot contains duplicate policy_id: {duplicate_ids[0]}"
        )
    return ordered


def _record_tuple(
    values: tuple[Any, ...],
    record_type: type,
    field_name: str,
    identity,
) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineHealthError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, record_type):
            raise GoalEngineHealthError(
                f"{field_name} must contain {record_type.__name__} values"
            )
    ordered = tuple(sorted(values, key=identity))
    duplicate_ids = _duplicates([identity(item) for item in ordered])
    if duplicate_ids:
        raise GoalEngineHealthError(
            f"{field_name} contains duplicate ID: {duplicate_ids[0]}"
        )
    return ordered


def _require_fields(
    payload: Mapping[str, Any],
    fields: set[str],
) -> dict[str, Any]:
    mapping = _require_mapping(payload, "payload")
    keys = set(mapping)
    forbidden = sorted(keys & _FORBIDDEN_FIELD_NAMES)
    if forbidden:
        raise GoalEngineHealthError(
            f"payload contains forbidden field: {forbidden[0]}"
        )
    missing = sorted(fields - keys)
    if missing:
        raise GoalEngineHealthError(f"payload missing required field: {missing[0]}")
    extra = sorted(keys - fields)
    if extra:
        raise GoalEngineHealthError(f"payload contains unknown field: {extra[0]}")
    return dict(mapping)


def _require_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise GoalEngineHealthError(f"{field_name} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise GoalEngineHealthError(f"{field_name} keys must be strings")
    return value


def _json_tuple(value: Any, field_name: str) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise GoalEngineHealthError(f"{field_name} must be an array")
    return tuple(value)


def _id_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineHealthError(f"{field_name} must be a tuple")
    validated = tuple(_require_id(item, field_name) for item in values)
    duplicates = _duplicates(list(validated))
    if duplicates:
        raise GoalEngineHealthError(
            f"{field_name} contains duplicate ID: {duplicates[0]}"
        )
    return tuple(sorted(validated)) if sort else validated


def _label_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineHealthError(f"{field_name} must be a tuple")
    validated = tuple(_require_label(item, field_name) for item in values)
    duplicates = _duplicates(list(validated))
    if duplicates:
        raise GoalEngineHealthError(
            f"{field_name} contains duplicate value: {duplicates[0]}"
        )
    return tuple(sorted(validated)) if sort else validated


def _text_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    sort: bool,
) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise GoalEngineHealthError(f"{field_name} must be a tuple")
    validated = tuple(_require_text(item, field_name) for item in values)
    duplicates = _duplicates(list(validated))
    if duplicates:
        raise GoalEngineHealthError(
            f"{field_name} contains duplicate value: {duplicates[0]}"
        )
    return tuple(sorted(validated)) if sort else validated


def _unique_texts(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _require_allowed(
    value: Any,
    allowed: frozenset[str],
    field_name: str,
) -> str:
    text = _require_text(value, field_name)
    if text not in allowed:
        raise GoalEngineHealthError(f"unsupported {field_name}: {text}")
    return text


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise GoalEngineHealthError(
            f"{field_name} must be non-empty text without surrounding whitespace"
        )
    if len(value) > 4096 or any(ord(character) < 32 for character in value):
        raise GoalEngineHealthError(f"{field_name} exceeds the bounded text contract")
    return value


def _require_label(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if len(text) > 128:
        raise GoalEngineHealthError(f"{field_name} is not a bounded label")
    return text


def _require_id(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _ID_PATTERN.fullmatch(text):
        raise GoalEngineHealthError(
            f"{field_name} must be a stable local identifier"
        )
    return text


def _require_positive_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise GoalEngineHealthError(f"{field_name} must be a positive integer")
    return value


def _require_nonnegative_int(value: Any, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise GoalEngineHealthError(
            f"{field_name} must be a nonnegative integer"
        )
    return value


def _require_ratio(value: Any, field_name: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise GoalEngineHealthError(f"{field_name} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < 0 or numeric > 1:
        raise GoalEngineHealthError(f"{field_name} must be finite and between 0 and 1")
    return numeric


def _require_observed_value(value: Any) -> None:
    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise GoalEngineHealthError("observed_value must be finite")
        return
    if isinstance(value, str):
        _require_label(value, "observed_value")
        return
    raise GoalEngineHealthError("observed_value must be a bounded scalar or null")


def _require_schema(value: Any, expected: str) -> str:
    text = _require_text(value, "schema_version")
    if text != expected:
        raise GoalEngineHealthError(f"schema_version must be {expected}")
    return text


def _require_sha256(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _SHA256_PATTERN.fullmatch(text):
        raise GoalEngineHealthError(
            f"{field_name} must be a lowercase SHA-256 hex digest"
        )
    return text


def _parse_utc_timestamp(value: Any, field_name: str) -> datetime:
    text = _require_text(value, field_name)
    normalized = f"{text[:-1]}+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise GoalEngineHealthError(
            f"{field_name} must be an ISO-8601 UTC timestamp"
        ) from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timedelta(0):
        raise GoalEngineHealthError(f"{field_name} must be UTC")
    return parsed


def _require_type(value: Any, expected_type: type, field_name: str) -> None:
    if not isinstance(value, expected_type):
        raise GoalEngineHealthError(
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


__all__ = [
    "ASSESSMENT_CLASSES",
    "FINDING_CLASSES",
    "HEALTH_CATEGORIES",
    "HEALTH_DOMAINS",
    "HEALTH_FINDING_SCHEMA_VERSION",
    "HEALTH_MANIFEST_SCHEMA_VERSION",
    "HEALTH_SIGNAL_DEFINITION_SCHEMA_VERSION",
    "HEALTH_SIGNAL_OBSERVATION_SCHEMA_VERSION",
    "SIGNAL_STATUSES",
    "SUBSYSTEM_HEALTH_ASSESSMENT_REFERENCE_SCHEMA_VERSION",
    "SUBSYSTEM_HEALTH_ASSESSMENT_SCHEMA_VERSION",
    "GoalEngineHealthError",
    "HealthFinding",
    "HealthManifest",
    "HealthSignalDefinition",
    "HealthSignalObservation",
    "SubsystemHealthAssessment",
    "SubsystemHealthAssessmentReference",
    "build_subsystem_health_assessment",
    "health_finding_from_dict",
    "health_finding_semantic_hash",
    "health_finding_to_dict",
    "health_manifest_from_dict",
    "health_manifest_semantic_hash",
    "health_manifest_to_dict",
    "health_signal_definition_from_dict",
    "health_signal_definition_semantic_hash",
    "health_signal_definition_to_dict",
    "health_signal_observation_from_dict",
    "health_signal_observation_semantic_hash",
    "health_signal_observation_to_dict",
    "subsystem_health_assessment_from_dict",
    "subsystem_health_assessment_reference_from_dict",
    "subsystem_health_assessment_reference_semantic_hash",
    "subsystem_health_assessment_reference_to_dict",
    "subsystem_health_assessment_semantic_hash",
    "subsystem_health_assessment_to_dict",
    "validate_assessment_class",
    "validate_finding_class",
    "validate_health_domain",
    "validate_health_manifest",
    "validate_health_signal_definition",
    "validate_signal_status",
    "validate_subsystem_health_assessment",
    "validate_subsystem_health_assessment_revision",
]
