from __future__ import annotations

import ast
import json
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import codie.goal_engine as goal_engine
from codie.goal_engine import (
    AUTHORITY_STATE_SCHEMA_VERSION,
    BUILD_STATE_SCHEMA_VERSION,
    CAPABILITY_SCHEMA_VERSION,
    EVIDENCE_REFERENCE_SCHEMA_VERSION,
    GOAL_STATE_SCHEMA_VERSION,
    HUMAN_ATTENTION_STATE_SCHEMA_VERSION,
    INCIDENT_STATE_SCHEMA_VERSION,
    POLICY_RECORD_SCHEMA_VERSION,
    POLICY_REFERENCE_SCHEMA_VERSION,
    POLICY_REGISTRY_SCHEMA_VERSION,
    PROJECT_STATE_SCHEMA_VERSION,
    PROJECT_STATE_SNAPSHOT_SCHEMA_VERSION,
    RESOURCE_STATE_SCHEMA_VERSION,
    SAFE_MODE_SCHEMA_VERSION,
    STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION,
    STATE_PROVENANCE_SCHEMA_VERSION,
    STATE_RECONCILIATION_RESULT_SCHEMA_VERSION,
    STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
    AuthorityState,
    BuildState,
    GoalCapability,
    GoalEngineStateError,
    GoalEvidenceReference,
    GoalIdentifier,
    GoalPolicyRecord,
    GoalPolicyReference,
    GoalPolicyRegistry,
    GoalSafeMode,
    GoalState,
    HumanAttentionState,
    IncidentState,
    ProjectState,
    ProjectStateSnapshot,
    ResourceState,
    StateConflictResolution,
    StateProvenance,
    StateSnapshotReference,
    authority_state_from_dict,
    authority_state_to_dict,
    build_state_from_dict,
    build_state_to_dict,
    canonical_json_bytes,
    classify_state_freshness,
    goal_policy_record_semantic_hash,
    goal_state_from_dict,
    goal_state_to_dict,
    human_attention_state_from_dict,
    human_attention_state_to_dict,
    incident_state_from_dict,
    incident_state_to_dict,
    project_state_from_dict,
    project_state_snapshot_from_dict,
    project_state_snapshot_semantic_hash,
    project_state_snapshot_to_dict,
    project_state_to_dict,
    reconcile_project_state,
    resource_state_from_dict,
    resource_state_to_dict,
    state_conflict_id,
    state_conflict_resolution_from_dict,
    state_conflict_resolution_to_dict,
    state_provenance_from_dict,
    state_provenance_to_dict,
    state_reconciliation_result_from_dict,
    state_reconciliation_result_semantic_hash,
    state_reconciliation_result_to_dict,
    state_record_comparison_semantic_hash,
    state_record_semantic_hash,
    validate_project_state_snapshot_revision,
    validate_state_conflict_resolution,
)


UTC_0 = "2026-08-08T12:00:00Z"
UTC_1 = "2026-08-08T12:30:00Z"
UTC_2 = "2026-08-08T13:00:00Z"
UTC_3 = "2026-08-08T14:00:00Z"


def evidence(reference_id: str = "evidence:state:1", *, observed_at: str = UTC_0) -> GoalEvidenceReference:
    return GoalEvidenceReference(
        evidence_ref_id=reference_id,
        evidence_class="MEASURED",
        source_id="source:local",
        source_version="v1",
        observed_at=observed_at,
        historical_validity="VALID",
        current_applicability="APPLICABLE",
        review_state="REVIEWED",
        privacy_class="PRIVATE_LOCAL",
        conflict_ref_ids=(),
        schema_version=EVIDENCE_REFERENCE_SCHEMA_VERSION,
    )


def provenance(
    provenance_id: str = "provenance:state:1",
    *,
    observed_at: str = UTC_0,
    fresh_until: str | None = UTC_2,
    availability: str = "AVAILABLE",
    evidence_ref_ids: tuple[str, ...] = ("evidence:state:1",),
    human_decision_ref_ids: tuple[str, ...] = (),
    authority_ref_ids: tuple[str, ...] = (),
) -> StateProvenance:
    return StateProvenance(
        provenance_id=provenance_id,
        observed_at=observed_at,
        fresh_until=fresh_until,
        availability=availability,
        evidence_ref_ids=evidence_ref_ids,
        human_decision_ref_ids=human_decision_ref_ids,
        authority_ref_ids=authority_ref_ids,
        schema_version=STATE_PROVENANCE_SCHEMA_VERSION,
    )


def safe_mode(mode: str = "NORMAL") -> GoalSafeMode:
    return GoalSafeMode(mode=mode, schema_version=SAFE_MODE_SCHEMA_VERSION)


def capability(capability_id: str) -> GoalCapability:
    return GoalCapability(
        capability_id=capability_id,
        capability_name=goal_engine.CAPABILITY_NAMES[capability_id],
        schema_version=CAPABILITY_SCHEMA_VERSION,
    )


def project(
    project_id: str = "project:codie",
    *,
    state_revision: int = 1,
    project_state_value: str = "ACTIVE",
    state_provenance: StateProvenance | None = None,
) -> ProjectState:
    return ProjectState(
        project_id=project_id,
        state_revision=state_revision,
        project_state=project_state_value,
        active_phase_id="Phase44F",
        active_phase_part="implementation",
        gate_scope="INTERMEDIATE_PACKET",
        provenance=state_provenance or provenance(),
        schema_version=PROJECT_STATE_SCHEMA_VERSION,
    )


def authority(
    authority_state_id: str = "authority:codie",
    *,
    state_revision: int = 1,
    authority_stage: str = "DOCUMENTATION_ONLY",
    authority_capability: GoalCapability | None = None,
    state_provenance: StateProvenance | None = None,
    promotion_ref_ids: tuple[str, ...] = (),
) -> AuthorityState:
    return AuthorityState(
        authority_state_id=authority_state_id,
        state_revision=state_revision,
        authority_stage=authority_stage,
        capability=authority_capability,
        safe_mode=safe_mode(),
        promotion_ref_ids=promotion_ref_ids,
        downgrade_ref_ids=(),
        provenance=state_provenance or provenance("provenance:authority:1"),
        schema_version=AUTHORITY_STATE_SCHEMA_VERSION,
    )


def goal(
    goal_state_id: str = "goal-state:1",
    *,
    local_id: str = "goal:1",
    state_revision: int = 1,
    lifecycle_state: str = "ACTIVE",
    blocked_by_ids: tuple[str, ...] = (),
    attention_ids: tuple[str, ...] = (),
    state_provenance: StateProvenance | None = None,
) -> GoalState:
    return GoalState(
        goal_state_id=goal_state_id,
        state_revision=state_revision,
        goal_identifier=GoalIdentifier(
            entity_kind="GOAL",
            local_id=local_id,
            schema_version=goal_engine.IDENTIFIER_SCHEMA_VERSION,
        ),
        goal_contract_id="goal-contract:1",
        goal_contract_revision=1,
        lifecycle_state=lifecycle_state,
        blocked_by_ids=blocked_by_ids,
        human_attention_request_ids=attention_ids,
        provenance=state_provenance or provenance("provenance:goal:1"),
        schema_version=GOAL_STATE_SCHEMA_VERSION,
    )


def build(
    build_id: str = "build:1",
    *,
    state_revision: int = 1,
    build_state_value: str = "IN_PROGRESS",
    attach_goal: bool = True,
    state_provenance: StateProvenance | None = None,
) -> BuildState:
    identifier = (
        GoalIdentifier(
            entity_kind="GOAL",
            local_id="goal:1",
            schema_version=goal_engine.IDENTIFIER_SCHEMA_VERSION,
        )
        if attach_goal
        else None
    )
    return BuildState(
        build_id=build_id,
        state_revision=state_revision,
        goal_identifier=identifier,
        goal_contract_id="goal-contract:1" if attach_goal else None,
        goal_contract_revision=1 if attach_goal else None,
        phase_id="Phase44F",
        phase_part="implementation",
        build_state=build_state_value,
        artifact_ref_ids=(),
        validation_ref_ids=(),
        provenance=state_provenance or provenance("provenance:build:1"),
        schema_version=BUILD_STATE_SCHEMA_VERSION,
    )


def resource(
    resource_id: str = "resource:1",
    *,
    temporary: bool = False,
    cleanup_required: bool = False,
    cleanup_ref_ids: tuple[str, ...] = (),
) -> ResourceState:
    return ResourceState(
        resource_id=resource_id,
        state_revision=1,
        resource_kind="WORKTREE",
        resource_state="AVAILABLE",
        constraint_summary="Caller reports the local resource state.",
        temporary=temporary,
        cleanup_required=cleanup_required,
        cleanup_ref_ids=cleanup_ref_ids,
        provenance=provenance("provenance:resource:1"),
        schema_version=RESOURCE_STATE_SCHEMA_VERSION,
    )


def incident(
    incident_id: str = "incident:1",
    *,
    incident_state_value: str = "OPEN",
    risk: str = "Low",
    contained_at: str | None = None,
    closed_at: str | None = None,
    attention_ids: tuple[str, ...] = (),
) -> IncidentState:
    return IncidentState(
        incident_id=incident_id,
        state_revision=1,
        incident_state=incident_state_value,
        risk=risk,
        opened_at=UTC_0,
        contained_at=contained_at,
        closed_at=closed_at,
        affected_system_ids=("system:goal-engine",),
        safe_mode=safe_mode("READ_ONLY_SAFE_MODE"),
        human_attention_request_ids=attention_ids,
        provenance=provenance("provenance:incident:1"),
        schema_version=INCIDENT_STATE_SCHEMA_VERSION,
    )


def attention(
    request_id: str = "attention:1",
    *,
    attention_state_value: str = "WAITING",
    responded_at: str | None = None,
    response_ref_ids: tuple[str, ...] = (),
    blocking_goal_ids: tuple[str, ...] = (),
    blocking_build_ids: tuple[str, ...] = (),
) -> HumanAttentionState:
    return HumanAttentionState(
        request_id=request_id,
        state_revision=1,
        attention_state=attention_state_value,
        decision_question="Should the caller proceed?",
        requested_at=UTC_0,
        responded_at=responded_at,
        response_ref_ids=response_ref_ids,
        blocking_goal_ids=blocking_goal_ids,
        blocking_build_ids=blocking_build_ids,
        provenance=provenance("provenance:attention:1"),
        schema_version=HUMAN_ATTENTION_STATE_SCHEMA_VERSION,
    )


def snapshot(
    snapshot_id: str = "snapshot:source-a",
    *,
    revision: int = 1,
    supersedes_snapshot: StateSnapshotReference | None = None,
    captured_at: str = UTC_1,
    project_value: ProjectState | None = None,
    authority_value: AuthorityState | None = None,
    goals: tuple[GoalState, ...] = (),
    builds: tuple[BuildState, ...] = (),
    resources: tuple[ResourceState, ...] = (),
    incidents: tuple[IncidentState, ...] = (),
    attention_states: tuple[HumanAttentionState, ...] = (),
    evidence_values: tuple[GoalEvidenceReference, ...] = (evidence(),),
) -> ProjectStateSnapshot:
    return ProjectStateSnapshot(
        snapshot_id=snapshot_id,
        revision=revision,
        supersedes_snapshot=supersedes_snapshot,
        captured_at=captured_at,
        project_state=project_value or project(),
        authority_state=authority_value or authority(),
        goal_states=goals,
        build_states=builds,
        resource_states=resources,
        incident_states=incidents,
        human_attention_states=attention_states,
        evidence_snapshot=evidence_values,
        schema_version=PROJECT_STATE_SNAPSHOT_SCHEMA_VERSION,
    )


def policy_registry() -> GoalPolicyRegistry:
    record = GoalPolicyRecord(
        policy_id="policy:state-resolution",
        policy_version=1,
        schema_version=POLICY_RECORD_SCHEMA_VERSION,
        date="2026-08-08",
        reason="Preserve an explicitly accepted deterministic tie-break record.",
        rule="Select only the caller-named current candidate.",
        authority_ref_ids=("authority:human:1",),
        affected_policy_ids=(),
        superseded_policy_ref=None,
        regression_case_ids=(),
    )
    return GoalPolicyRegistry(
        records=(record,),
        schema_version=POLICY_REGISTRY_SCHEMA_VERSION,
    )


class StateVocabularyAndProvenanceTest(unittest.TestCase):
    def test_exact_vocabularies_accept_and_case_aliases_fail(self) -> None:
        validators = (
            (goal_engine.validate_state_domain, goal_engine.STATE_DOMAINS),
            (goal_engine.validate_state_freshness, goal_engine.STATE_FRESHNESS_VALUES),
            (goal_engine.validate_state_availability, goal_engine.STATE_AVAILABILITY_VALUES),
            (goal_engine.validate_reconciliation_status, goal_engine.RECONCILIATION_STATUS_VALUES),
            (goal_engine.validate_project_state, goal_engine.PROJECT_STATE_VALUES),
            (goal_engine.validate_authority_stage, goal_engine.AUTHORITY_STAGE_VALUES),
            (goal_engine.validate_build_state, goal_engine.BUILD_STATE_VALUES),
            (goal_engine.validate_resource_state, goal_engine.RESOURCE_STATE_VALUES),
            (goal_engine.validate_incident_state, goal_engine.INCIDENT_STATE_VALUES),
            (goal_engine.validate_human_attention_state, goal_engine.HUMAN_ATTENTION_STATE_VALUES),
        )
        for validator, values in validators:
            for value in values:
                self.assertEqual(validator(value), value)
            with self.assertRaises(GoalEngineStateError):
                validator(next(iter(values)).lower())

    def test_freshness_uses_only_caller_time(self) -> None:
        current = provenance(fresh_until=UTC_2)
        self.assertEqual(classify_state_freshness(current, UTC_1), "CURRENT")
        self.assertEqual(classify_state_freshness(current, UTC_3), "STALE")
        self.assertEqual(
            classify_state_freshness(provenance(fresh_until=None), UTC_1),
            "UNKNOWN",
        )
        with self.assertRaisesRegex(GoalEngineStateError, "precede observed"):
            classify_state_freshness(current, "2026-08-08T11:59:59Z")

    def test_provenance_keeps_reference_categories_disjoint(self) -> None:
        with self.assertRaisesRegex(GoalEngineStateError, "remain separate"):
            provenance(
                evidence_ref_ids=("reference:shared",),
                human_decision_ref_ids=("reference:shared",),
            )
        with self.assertRaises(GoalEngineStateError):
            provenance(fresh_until="2026-08-08T11:59:00Z")

    def test_provenance_round_trip_and_unknown_field_rejection(self) -> None:
        value = provenance()
        self.assertEqual(
            state_provenance_from_dict(state_provenance_to_dict(value)),
            value,
        )
        payload = state_provenance_to_dict(value)
        payload["provider_payload"] = "forbidden"
        with self.assertRaisesRegex(GoalEngineStateError, "forbidden field"):
            state_provenance_from_dict(payload)
        payload = state_provenance_to_dict(value)
        payload["schema_version"] = "codie.goal_engine.state_provenance.v2"
        with self.assertRaises(GoalEngineStateError):
            state_provenance_from_dict(payload)


class StateRecordValidationTest(unittest.TestCase):
    def test_all_state_records_round_trip(self) -> None:
        records = (
            (project(), project_state_to_dict, project_state_from_dict),
            (authority(), authority_state_to_dict, authority_state_from_dict),
            (goal(), goal_state_to_dict, goal_state_from_dict),
            (build(), build_state_to_dict, build_state_from_dict),
            (resource(), resource_state_to_dict, resource_state_from_dict),
            (incident(), incident_state_to_dict, incident_state_from_dict),
            (attention(), human_attention_state_to_dict, human_attention_state_from_dict),
        )
        for value, serializer, parser in records:
            with self.subTest(record=type(value).__name__):
                self.assertEqual(parser(serializer(value)), value)
                with self.assertRaises(FrozenInstanceError):
                    value.state_revision = 2

    def test_mutable_repeated_fields_fail_closed(self) -> None:
        with self.assertRaisesRegex(GoalEngineStateError, "tuple"):
            goal(blocked_by_ids=[])  # type: ignore[arg-type]
        payload = goal_state_to_dict(goal())
        payload["blocked_by_ids"] = ()
        with self.assertRaisesRegex(GoalEngineStateError, "array"):
            goal_state_from_dict(payload)

    def test_goal_waiting_for_human_requires_request_reference(self) -> None:
        with self.assertRaisesRegex(GoalEngineStateError, "requires"):
            goal(lifecycle_state="WAITING_FOR_HUMAN")
        value = goal(
            lifecycle_state="WAITING_FOR_HUMAN",
            attention_ids=("attention:1",),
        )
        self.assertEqual(value.human_attention_request_ids, ("attention:1",))

    def test_build_contract_identity_is_atomic_and_completion_is_observational(self) -> None:
        complete = build(build_state_value="COMPLETE", attach_goal=False)
        self.assertEqual(complete.validation_ref_ids, ())
        with self.assertRaisesRegex(GoalEngineStateError, "present together"):
            BuildState(
                build_id="build:bad",
                state_revision=1,
                goal_identifier=None,
                goal_contract_id="goal-contract:1",
                goal_contract_revision=None,
                phase_id="Phase44F",
                phase_part="implementation",
                build_state="COMPLETE",
                artifact_ref_ids=(),
                validation_ref_ids=(),
                provenance=provenance(),
                schema_version=BUILD_STATE_SCHEMA_VERSION,
            )

    def test_authority_stage_ceilings_fail_closed(self) -> None:
        documented = authority()
        self.assertIsNone(documented.capability)
        with self.assertRaises(GoalEngineStateError):
            authority(authority_capability=capability("CAP-0"))
        stage_zero_provenance = provenance(
            "provenance:authority:stage0",
            authority_ref_ids=("authority:human:1",),
        )
        self.assertEqual(
            authority(
                authority_stage="STAGE_0_SHADOW",
                authority_capability=capability("CAP-0"),
                state_provenance=stage_zero_provenance,
            ).capability.capability_id,
            "CAP-0",
        )
        with self.assertRaises(GoalEngineStateError):
            authority(
                authority_stage="STAGE_0_SHADOW",
                authority_capability=capability("CAP-1"),
                state_provenance=stage_zero_provenance,
            )
        for forbidden_capability in ("CAP-4", "CAP-5"):
            with self.subTest(capability=forbidden_capability), self.assertRaises(
                GoalEngineStateError
            ):
                authority(
                    authority_stage="STAGE_3_BUILD_GRAPH_SUBMISSION",
                    authority_capability=capability(forbidden_capability),
                    state_provenance=stage_zero_provenance,
                    promotion_ref_ids=("promotion:human:1",),
                )
        with self.assertRaises(GoalEngineStateError):
            goal_engine.validate_authority_stage("STAGE_4_AUTONOMOUS")

    def test_stage_one_through_three_require_promotion_reference(self) -> None:
        state_provenance = provenance(
            "provenance:authority:promoted",
            authority_ref_ids=("authority:human:1",),
        )
        with self.assertRaisesRegex(GoalEngineStateError, "promotion"):
            authority(
                authority_stage="STAGE_1_WORK_ORDER",
                authority_capability=capability("CAP-1"),
                state_provenance=state_provenance,
            )

    def test_safe_mode_never_increases_capability(self) -> None:
        value = replace(authority(), safe_mode=safe_mode("FULL_AUTOMATION_HALT"))
        self.assertIsNone(value.capability)
        self.assertFalse(hasattr(value, "effective_permission"))

    def test_temporary_resource_cleanup_rules(self) -> None:
        self.assertTrue(resource(temporary=True, cleanup_required=True).cleanup_required)
        self.assertFalse(
            resource(
                temporary=True,
                cleanup_required=False,
                cleanup_ref_ids=("cleanup:evidence:1",),
            ).cleanup_required
        )
        with self.assertRaises(GoalEngineStateError):
            resource(temporary=True, cleanup_required=False)
        with self.assertRaises(GoalEngineStateError):
            resource(
                temporary=True,
                cleanup_required=True,
                cleanup_ref_ids=("cleanup:evidence:1",),
            )

    def test_incident_timestamp_and_critical_attention_rules(self) -> None:
        with self.assertRaisesRegex(GoalEngineStateError, "contained_at"):
            incident(incident_state_value="CONTAINED")
        with self.assertRaisesRegex(GoalEngineStateError, "closed_at"):
            incident(incident_state_value="RESOLVED")
        with self.assertRaisesRegex(GoalEngineStateError, "Critical"):
            incident(risk="Critical")
        value = incident(
            incident_state_value="RESOLVED",
            risk="Critical",
            contained_at=UTC_1,
            closed_at=UTC_2,
            attention_ids=("attention:1",),
        )
        self.assertEqual(value.closed_at, UTC_2)

    def test_human_response_does_not_imply_approval_or_authority(self) -> None:
        with self.assertRaises(GoalEngineStateError):
            attention(attention_state_value="RESPONDED")
        responded = attention(
            attention_state_value="RESPONDED",
            responded_at=UTC_1,
            response_ref_ids=("response:human:1",),
        )
        self.assertFalse(hasattr(responded, "approved"))
        self.assertFalse(hasattr(responded, "authority"))
        with self.assertRaises(GoalEngineStateError):
            attention(
                attention_state_value="WAITING",
                responded_at=UTC_1,
                response_ref_ids=("response:human:1",),
            )

    def test_comparison_hash_excludes_provenance_but_full_hash_preserves_it(self) -> None:
        first = goal(
            goal_state_id="goal-state:a",
            state_provenance=provenance("provenance:source:a"),
        )
        second = goal(
            goal_state_id="goal-state:b",
            state_provenance=provenance(
                "provenance:source:b",
                human_decision_ref_ids=("decision:history:1",),
            ),
        )
        self.assertEqual(
            state_record_comparison_semantic_hash(first),
            state_record_comparison_semantic_hash(second),
        )
        self.assertNotEqual(state_record_semantic_hash(first), state_record_semantic_hash(second))


class SnapshotValidationTest(unittest.TestCase):
    def test_snapshot_round_trip_and_hash_stability(self) -> None:
        request = attention(blocking_goal_ids=("goal-state:1",), blocking_build_ids=("build:1",))
        value = snapshot(
            goals=(goal(attention_ids=("attention:1",)),),
            builds=(build(),),
            resources=(resource(),),
            incidents=(incident(attention_ids=("attention:1",)),),
            attention_states=(request,),
        )
        payload = project_state_snapshot_to_dict(value)
        self.assertEqual(project_state_snapshot_from_dict(payload), value)
        self.assertEqual(
            project_state_snapshot_semantic_hash(value),
            project_state_snapshot_semantic_hash(project_state_snapshot_from_dict(payload)),
        )

    def test_snapshot_rejects_unknown_evidence_and_attention_references(self) -> None:
        unknown_evidence_goal = goal(
            state_provenance=provenance(
                "provenance:unknown",
                evidence_ref_ids=("evidence:missing",),
            )
        )
        with self.assertRaisesRegex(GoalEngineStateError, "unknown evidence"):
            snapshot(goals=(unknown_evidence_goal,))
        with self.assertRaisesRegex(GoalEngineStateError, "unknown human-attention"):
            snapshot(
                goals=(
                    goal(
                        lifecycle_state="WAITING_FOR_HUMAN",
                        attention_ids=("attention:missing",),
                    ),
                )
            )

    def test_snapshot_rejects_duplicate_record_and_subject_ids(self) -> None:
        with self.assertRaisesRegex(GoalEngineStateError, "duplicate state record"):
            snapshot(goals=(goal(goal_state_id="project:codie"),))
        with self.assertRaisesRegex(GoalEngineStateError, "duplicate GOAL subject"):
            snapshot(
                goals=(
                    goal(goal_state_id="goal-state:a"),
                    goal(goal_state_id="goal-state:b"),
                )
            )

    def test_build_goal_identity_and_contract_revision_must_match(self) -> None:
        wrong_build = replace(build(), goal_contract_revision=2)
        with self.assertRaisesRegex(GoalEngineStateError, "exact Goal Contract"):
            snapshot(goals=(goal(),), builds=(wrong_build,))

    def test_snapshot_revision_preserves_hash_and_state_revision_rules(self) -> None:
        previous = snapshot(goals=(goal(),))
        reference = StateSnapshotReference(
            snapshot_id=previous.snapshot_id,
            revision=1,
            semantic_hash=project_state_snapshot_semantic_hash(previous),
            schema_version=STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        )
        current = snapshot(
            revision=2,
            supersedes_snapshot=reference,
            captured_at=UTC_2,
            goals=(goal(state_revision=2, lifecycle_state="WATCHING"),),
        )
        self.assertIs(validate_project_state_snapshot_revision(previous, current), current)
        bad = replace(current, goal_states=(goal(state_revision=1, lifecycle_state="WATCHING"),))
        with self.assertRaisesRegex(GoalEngineStateError, "state revision"):
            validate_project_state_snapshot_revision(previous, bad)
        bad_reference = replace(reference, semantic_hash="0" * 64)
        with self.assertRaisesRegex(GoalEngineStateError, "semantic hash"):
            validate_project_state_snapshot_revision(
                previous,
                replace(current, supersedes_snapshot=bad_reference),
            )


class ReconciliationTest(unittest.TestCase):
    def source_snapshot(
        self,
        source: str,
        lifecycle_state: str,
        *,
        freshness_until: str | None = UTC_2,
        availability: str = "AVAILABLE",
        captured_at: str = UTC_1,
    ) -> ProjectStateSnapshot:
        reference_id = f"evidence:{source}"
        source_evidence = evidence(reference_id)
        source_provenance = provenance(
            f"provenance:{source}",
            fresh_until=freshness_until,
            availability=availability,
            evidence_ref_ids=(reference_id,),
        )
        return snapshot(
            snapshot_id=f"snapshot:{source}",
            captured_at=captured_at,
            project_value=project(
                project_id=f"project:{source}",
                state_provenance=source_provenance,
            ),
            authority_value=authority(
                authority_state_id=f"authority:{source}",
                state_provenance=source_provenance,
            ),
            goals=(
                goal(
                    goal_state_id=f"goal-state:{source}",
                    lifecycle_state=lifecycle_state,
                    state_provenance=source_provenance,
                ),
            ),
            evidence_values=(source_evidence,),
        )

    def goal_entry(self, result: goal_engine.StateReconciliationResult):
        return next(item for item in result.entries if item.domain == "GOAL")

    def test_exact_agreement_is_consistent_despite_provenance_difference(self) -> None:
        result = reconcile_project_state(
            "reconciliation:agreement",
            (self.source_snapshot("a", "ACTIVE"), self.source_snapshot("b", "ACTIVE")),
            UTC_1,
        )
        entry = self.goal_entry(result)
        self.assertEqual(entry.reconciliation_status, "CONSISTENT")
        self.assertEqual(result.aggregate_status, "CONSISTENT")
        self.assertEqual(len(set(entry.candidate_semantic_hashes)), 1)

    def test_state_difference_creates_visible_deterministic_conflict(self) -> None:
        left = self.source_snapshot("a", "ACTIVE", captured_at=UTC_0)
        right = self.source_snapshot("b", "WATCHING", captured_at=UTC_2)
        result = reconcile_project_state(
            "reconciliation:conflict",
            (right, left),
            UTC_1,
        )
        entry = self.goal_entry(result)
        self.assertEqual(entry.reconciliation_status, "CONFLICTED")
        self.assertEqual(result.aggregate_status, "CONFLICTED")
        self.assertEqual(len(result.conflicts), 1)
        conflict = result.conflicts[0]
        self.assertEqual(conflict.detected_at, UTC_1)
        self.assertEqual(
            conflict.conflict_id,
            state_conflict_id("GOAL", "goal:1", conflict.candidate_semantic_hashes),
        )

    def test_stale_difference_is_retained_without_becoming_conflict(self) -> None:
        current = self.source_snapshot("current", "ACTIVE")
        stale = self.source_snapshot(
            "stale",
            "WATCHING",
            freshness_until="2026-08-08T12:15:00Z",
        )
        result = reconcile_project_state(
            "reconciliation:stale",
            (stale, current),
            UTC_1,
        )
        entry = self.goal_entry(result)
        self.assertEqual(entry.reconciliation_status, "CONSISTENT")
        self.assertEqual(entry.stale_record_ids, ("goal-state:stale",))
        self.assertEqual(result.conflicts, ())

    def test_unknown_and_unavailable_remain_distinct(self) -> None:
        unknown = reconcile_project_state(
            "reconciliation:unknown",
            (self.source_snapshot("unknown", "ACTIVE", freshness_until=None),),
            UTC_1,
        )
        unknown_entry = self.goal_entry(unknown)
        self.assertEqual(unknown_entry.reconciliation_status, "INCOMPLETE")
        self.assertEqual(unknown_entry.unknown_freshness_record_ids, ("goal-state:unknown",))
        unavailable = reconcile_project_state(
            "reconciliation:unavailable",
            (self.source_snapshot("offline", "ACTIVE", availability="UNAVAILABLE"),),
            UTC_1,
        )
        unavailable_entry = self.goal_entry(unavailable)
        self.assertEqual(unavailable_entry.reconciliation_status, "UNAVAILABLE")
        self.assertEqual(unavailable_entry.current_record_ids, ("goal-state:offline",))
        self.assertEqual(unavailable_entry.unavailable_record_ids, ("goal-state:offline",))

    def test_caller_human_resolution_retains_conflict_history(self) -> None:
        left = self.source_snapshot("a", "ACTIVE")
        right = self.source_snapshot("b", "WATCHING")
        left_goal = left.goal_states[0]
        right_goal = right.goal_states[0]
        conflict_id = state_conflict_id(
            "GOAL",
            "goal:1",
            (
                state_record_comparison_semantic_hash(left_goal),
                state_record_comparison_semantic_hash(right_goal),
            ),
        )
        resolution = StateConflictResolution(
            resolution_id="resolution:human:1",
            conflict_id=conflict_id,
            selected_record_id=left_goal.goal_state_id,
            resolution_kind="HUMAN_DECISION",
            resolved_at=UTC_1,
            human_decision_ref_ids=("decision:human:1",),
            policy_refs=(),
            authority_ref_ids=("authority:human:1",),
            schema_version=STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION,
        )
        result = reconcile_project_state(
            "reconciliation:resolved",
            (left, right),
            UTC_1,
            (resolution,),
        )
        self.assertEqual(self.goal_entry(result).reconciliation_status, "RESOLVED_CONFLICT")
        self.assertEqual(result.aggregate_status, "RESOLVED_CONFLICT")
        self.assertEqual(len(result.conflicts), 1)
        self.assertEqual(result.resolutions, (resolution,))

    def test_accepted_policy_resolution_requires_exact_registry_history(self) -> None:
        left = self.source_snapshot("a", "ACTIVE")
        right = self.source_snapshot("b", "WATCHING")
        hashes = tuple(
            state_record_comparison_semantic_hash(item)
            for item in (left.goal_states[0], right.goal_states[0])
        )
        conflict_id = state_conflict_id("GOAL", "goal:1", hashes)
        registry = policy_registry()
        record = registry.records[0]
        reference = GoalPolicyReference(
            policy_id=record.policy_id,
            policy_version=record.policy_version,
            semantic_hash=goal_policy_record_semantic_hash(record),
            schema_version=POLICY_REFERENCE_SCHEMA_VERSION,
        )
        resolution = StateConflictResolution(
            resolution_id="resolution:policy:1",
            conflict_id=conflict_id,
            selected_record_id=right.goal_states[0].goal_state_id,
            resolution_kind="ACCEPTED_POLICY",
            resolved_at=UTC_1,
            human_decision_ref_ids=(),
            policy_refs=(reference,),
            authority_ref_ids=("authority:human:1",),
            schema_version=STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION,
        )
        result = reconcile_project_state(
            "reconciliation:policy",
            (left, right),
            UTC_1,
            (resolution,),
            registry,
        )
        self.assertEqual(result.aggregate_status, "RESOLVED_CONFLICT")
        with self.assertRaisesRegex(GoalEngineStateError, "Registry"):
            reconcile_project_state(
                "reconciliation:no-registry",
                (left, right),
                UTC_1,
                (resolution,),
            )
        bad_reference = replace(reference, semantic_hash="0" * 64)
        bad_resolution = replace(resolution, policy_refs=(bad_reference,))
        with self.assertRaisesRegex(GoalEngineStateError, "semantic hash"):
            reconcile_project_state(
                "reconciliation:bad-policy",
                (left, right),
                UTC_1,
                (bad_resolution,),
                registry,
            )

    def test_resolution_validation_rejects_non_candidate(self) -> None:
        left = self.source_snapshot("a", "ACTIVE")
        right = self.source_snapshot("b", "WATCHING")
        initial = reconcile_project_state(
            "reconciliation:initial",
            (left, right),
            UTC_1,
        )
        conflict = initial.conflicts[0]
        resolution = StateConflictResolution(
            resolution_id="resolution:bad",
            conflict_id=conflict.conflict_id,
            selected_record_id="goal-state:missing",
            resolution_kind="HUMAN_DECISION",
            resolved_at=UTC_1,
            human_decision_ref_ids=("decision:human:1",),
            policy_refs=(),
            authority_ref_ids=("authority:human:1",),
            schema_version=STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION,
        )
        with self.assertRaisesRegex(GoalEngineStateError, "exact usable current"):
            validate_state_conflict_resolution(resolution, conflict)

    def test_lineage_tip_replaces_prior_revision_as_current_source_view(self) -> None:
        prior = self.source_snapshot("lineage", "ACTIVE")
        reference = StateSnapshotReference(
            snapshot_id=prior.snapshot_id,
            revision=1,
            semantic_hash=project_state_snapshot_semantic_hash(prior),
            schema_version=STATE_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        )
        tip = replace(
            prior,
            revision=2,
            supersedes_snapshot=reference,
            captured_at=UTC_2,
            goal_states=(replace(prior.goal_states[0], state_revision=2, lifecycle_state="WATCHING"),),
        )
        peer = self.source_snapshot("peer", "WATCHING")
        result = reconcile_project_state(
            "reconciliation:lineage-tip",
            (tip, peer, prior),
            UTC_1,
        )
        self.assertEqual(self.goal_entry(result).reconciliation_status, "CONSISTENT")
        self.assertEqual(len(result.input_snapshot_refs), 3)

    def test_same_input_is_byte_and_hash_stable_regardless_input_order(self) -> None:
        left = self.source_snapshot("a", "ACTIVE")
        right = self.source_snapshot("b", "ACTIVE")
        first = reconcile_project_state(
            "reconciliation:stable",
            (left, right),
            UTC_1,
        )
        second = reconcile_project_state(
            "reconciliation:stable",
            (right, left),
            UTC_1,
        )
        first_payload = state_reconciliation_result_to_dict(first)
        second_payload = state_reconciliation_result_to_dict(second)
        self.assertEqual(canonical_json_bytes(first_payload), canonical_json_bytes(second_payload))
        self.assertEqual(
            state_reconciliation_result_semantic_hash(first),
            state_reconciliation_result_semantic_hash(second),
        )
        self.assertEqual(state_reconciliation_result_from_dict(first_payload), first)


class StateEngineBoundaryTest(unittest.TestCase):
    def test_serialized_result_rejects_unknown_and_raw_fields(self) -> None:
        result = reconcile_project_state(
            "reconciliation:mapping",
            (snapshot(),),
            UTC_1,
        )
        payload = state_reconciliation_result_to_dict(result)
        payload["raw_payload"] = {}
        with self.assertRaisesRegex(GoalEngineStateError, "forbidden field"):
            state_reconciliation_result_from_dict(payload)
        payload = state_reconciliation_result_to_dict(result)
        payload["automatic_permission"] = True
        with self.assertRaisesRegex(GoalEngineStateError, "unknown field"):
            state_reconciliation_result_from_dict(payload)

    def test_resolution_round_trip_preserves_decision_as_reference_only(self) -> None:
        resolution = StateConflictResolution(
            resolution_id="resolution:roundtrip",
            conflict_id=f"state-conflict:{'0' * 64}",
            selected_record_id="goal-state:1",
            resolution_kind="HUMAN_DECISION",
            resolved_at=UTC_1,
            human_decision_ref_ids=("decision:human:1",),
            policy_refs=(),
            authority_ref_ids=("authority:human:1",),
            schema_version=STATE_CONFLICT_RESOLUTION_SCHEMA_VERSION,
        )
        self.assertEqual(
            state_conflict_resolution_from_dict(
                state_conflict_resolution_to_dict(resolution)
            ),
            resolution,
        )
        self.assertFalse(hasattr(resolution, "decision_body"))

    def test_module_uses_no_runtime_or_external_integration_imports(self) -> None:
        source_path = Path(goal_engine.state_engine.__file__)
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported_roots = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        imported_roots.update(
            node.module.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module not in {None, "__future__", "foundation"}
        )
        self.assertEqual(imported_roots, {"collections", "dataclasses", "datetime", "re", "typing"})
        forbidden_imports = {
            "asyncio",
            "http",
            "os",
            "pathlib",
            "random",
            "requests",
            "socket",
            "sqlite3",
            "subprocess",
            "time",
            "urllib",
            "uuid",
        }
        self.assertFalse(imported_roots & forbidden_imports)

    def test_public_records_have_no_mutation_or_later_phase_methods(self) -> None:
        exported = "\n".join(goal_engine.__all__).lower()
        for forbidden in (
            "activate_goal",
            "build_graph_executor",
            "ccpm",
            "health_score",
            "persist",
            "promote_authority",
            "provider",
            "scheduler",
            "stream_deck",
        ):
            self.assertNotIn(forbidden, exported)
        result = reconcile_project_state(
            "reconciliation:no-mutation",
            (snapshot(),),
            UTC_1,
        )
        json.dumps(state_reconciliation_result_to_dict(result), sort_keys=True)
        for forbidden in ("execute", "mutate", "save", "promote", "resolve_automatically"):
            self.assertFalse(hasattr(result, forbidden))


if __name__ == "__main__":
    unittest.main()
