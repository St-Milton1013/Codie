from __future__ import annotations

import ast
import json
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import codie.goal_engine as goal_engine
from codie.goal_engine import (
    CAPABILITY_SCHEMA_VERSION,
    EVIDENCE_REFERENCE_SCHEMA_VERSION,
    GOAL_CONTRACT_REVISION_REFERENCE_SCHEMA_VERSION,
    GOAL_CONTRACT_SCHEMA_VERSION,
    IDENTIFIER_SCHEMA_VERSION,
    LINEAGE_EVENT_SCHEMA_VERSION,
    POLICY_RECORD_SCHEMA_VERSION,
    POLICY_REFERENCE_SCHEMA_VERSION,
    POLICY_REGISTRY_SCHEMA_VERSION,
    SAFE_MODE_SCHEMA_VERSION,
    FindingIdentifier,
    GoalCapability,
    GoalContract,
    GoalContractRevisionReference,
    GoalEngineFoundationError,
    GoalEvidenceReference,
    GoalIdentifier,
    GoalLineageEvent,
    GoalPolicyRecord,
    GoalPolicyReference,
    GoalPolicyRegistry,
    GoalSafeMode,
    IdeaIdentifier,
    canonical_json_bytes,
    finding_identifier_from_dict,
    finding_identifier_to_dict,
    goal_capability_from_dict,
    goal_capability_to_dict,
    goal_contract_from_dict,
    goal_contract_semantic_hash,
    goal_contract_to_dict,
    goal_evidence_reference_from_dict,
    goal_evidence_reference_to_dict,
    goal_identifier_from_dict,
    goal_identifier_to_dict,
    goal_lineage_event_from_dict,
    goal_lineage_event_to_dict,
    goal_policy_record_semantic_hash,
    goal_policy_registry_from_dict,
    goal_policy_registry_to_dict,
    goal_safe_mode_from_dict,
    goal_safe_mode_to_dict,
    idea_identifier_from_dict,
    idea_identifier_to_dict,
    lookup_goal_policy,
    semantic_hash,
    validate_capability_id,
    validate_goal_contract_revision,
    validate_goal_lifecycle_state,
    validate_goal_lineage_chain,
    validate_problem_classification,
    validate_risk,
    validate_rollback,
    validate_safe_mode,
    validate_size,
)


UTC_1 = "2026-08-08T12:00:00+00:00"
UTC_2 = "2026-08-08T12:01:00Z"


def evidence_reference(**overrides) -> GoalEvidenceReference:
    data = {
        "evidence_ref_id": "evidence:measured:1",
        "evidence_class": "class_2_measured_evidence",
        "source_id": "source:local:1",
        "source_version": "v1",
        "observed_at": UTC_1,
        "historical_validity": "VALID",
        "current_applicability": "APPLICABLE",
        "review_state": "REVIEWED",
        "privacy_class": "LOCAL",
        "conflict_ref_ids": ("evidence:conflict:2", "evidence:conflict:1"),
        "schema_version": EVIDENCE_REFERENCE_SCHEMA_VERSION,
    }
    data.update(overrides)
    return GoalEvidenceReference(**data)


def goal_contract(**overrides) -> GoalContract:
    data = {
        "goal_contract_id": "goal-contract:foundation:1",
        "revision": 1,
        "schema_version": GOAL_CONTRACT_SCHEMA_VERSION,
        "supersedes_revision": None,
        "originating_idea_ids": ("idea:2", "idea:1"),
        "originating_finding_ids": ("finding:1",),
        "problem_classification": "STRUCTURAL",
        "observed_problem": "The foundation contract has no runtime representation.",
        "desired_outcome": "Represent the ratified foundation deterministically.",
        "why_it_matters": "Later phases require stable authority-neutral inputs.",
        "baseline": "No codie.goal_engine package exists.",
        "expected_result": "Foundation records round-trip without semantic drift.",
        "acceptable_result": "Every required invariant has a focused test.",
        "maximum_acceptable_regressions": ("No existing test regression.",),
        "root_cause_hypothesis": "The implementation phase has not run.",
        "confidence": 0.9,
        "proposed_intervention": "Add pure immutable foundation records.",
        "credible_alternatives": ("Remain documentation-only and block Phase44D.",),
        "disconfirmation_criteria": ("A record requires runtime or provider state.",),
        "expected_affected_systems": ("codie.goal_engine",),
        "expected_unaffected_systems": ("providers", "validation"),
        "dependency_ids": ("contract:phase44b",),
        "evidence_snapshot": (evidence_reference(),),
        "privacy_implications": "Opaque local references only; no raw content.",
        "security_implications": "No secrets, network, or authority side effects.",
        "zero_cost_validation": "Run local standard-library tests.",
        "manual_burden": "Human merge remains required.",
        "operational_burden": "No runtime service is added.",
        "size": "Small",
        "risk": "Low",
        "rollback": "Easy",
        "rollback_plan": "Revert the isolated foundation package.",
        "observation_window": "Phase44D checkpoint review.",
        "if_we_do_nothing": "Phase44D remains blocked.",
        "if_we_do_this": "Later contracts receive stable value objects.",
        "historical_attempt_ids": (),
        "approval_requirements": ("Artifact-backed validation", "Human merge"),
        "created_at": UTC_1,
    }
    data.update(overrides)
    return GoalContract(**data)


def policy_record(**overrides) -> GoalPolicyRecord:
    data = {
        "policy_id": "policy:local-first",
        "policy_version": 1,
        "schema_version": POLICY_RECORD_SCHEMA_VERSION,
        "date": "2026-08-08",
        "reason": "Preserve local-first operation.",
        "rule": "Foundation records use caller-provided local data only.",
        "authority_ref_ids": ("authority:constitution:v2",),
        "affected_policy_ids": ("policy:local-first",),
        "superseded_policy_ref": None,
        "regression_case_ids": ("regression:local-first",),
    }
    data.update(overrides)
    return GoalPolicyRecord(**data)


def lineage_event(**overrides) -> GoalLineageEvent:
    data = {
        "event_id": "lineage:event:1",
        "schema_version": LINEAGE_EVENT_SCHEMA_VERSION,
        "entity_kind": "GOAL",
        "entity_id": "goal:foundation:1",
        "entity_revision": 1,
        "event_kind": "GOAL",
        "occurred_at": UTC_1,
        "actor_kind": "HUMAN",
        "summary": "Human approved the documented Goal Contract for validation.",
        "evidence_ref_ids": ("evidence:measured:1",),
        "human_decision_ref_ids": ("decision:human:1",),
        "authority_ref_ids": ("authority:merge:human",),
        "prior_event_ids": (),
        "prior_event_hashes": (),
    }
    data.update(overrides)
    return GoalLineageEvent(**data)


class GoalEngineVocabularyTest(unittest.TestCase):
    def test_exact_ratified_vocabulary_is_accepted(self) -> None:
        for value in goal_engine.GOAL_LIFECYCLE_STATES:
            self.assertEqual(validate_goal_lifecycle_state(value), value)
        for value in goal_engine.PROBLEM_CLASSIFICATIONS:
            self.assertEqual(validate_problem_classification(value), value)
        for value in goal_engine.CAPABILITY_IDS:
            self.assertEqual(validate_capability_id(value), value)
        for value in goal_engine.SIZE_VALUES:
            self.assertEqual(validate_size(value), value)
        for value in goal_engine.RISK_VALUES:
            self.assertEqual(validate_risk(value), value)
        for value in goal_engine.ROLLBACK_VALUES:
            self.assertEqual(validate_rollback(value), value)
        for value in goal_engine.SAFE_MODE_VALUES:
            self.assertEqual(validate_safe_mode(value), value)

    def test_unknown_and_case_alias_vocabulary_fails(self) -> None:
        validators = (
            (validate_goal_lifecycle_state, "healthy_idle"),
            (validate_problem_classification, "PERMANENT"),
            (validate_capability_id, "CAP-6"),
            (validate_size, "tiny"),
            (validate_risk, "Severe"),
            (validate_rollback, "Impossible"),
            (validate_safe_mode, "AUTO_RESTORE"),
        )
        for validator, value in validators:
            with self.subTest(value=value), self.assertRaises(GoalEngineFoundationError):
                validator(value)

    def test_level_zero_is_not_an_operational_capability(self) -> None:
        with self.assertRaisesRegex(GoalEngineFoundationError, "constitutional"):
            validate_capability_id("Level 0")

    def test_capability_vocabulary_mapping_is_immutable(self) -> None:
        with self.assertRaises(TypeError):
            goal_engine.CAPABILITY_NAMES["CAP-0"] = "Mutate"

    def test_capability_and_safe_mode_are_vocabulary_only(self) -> None:
        capability = GoalCapability(
            capability_id="CAP-0",
            capability_name="Observe",
            schema_version=CAPABILITY_SCHEMA_VERSION,
        )
        safe_mode = GoalSafeMode(
            mode="READ_ONLY_SAFE_MODE",
            schema_version=SAFE_MODE_SCHEMA_VERSION,
        )
        self.assertEqual(goal_capability_from_dict(goal_capability_to_dict(capability)), capability)
        self.assertEqual(goal_safe_mode_from_dict(goal_safe_mode_to_dict(safe_mode)), safe_mode)
        self.assertEqual(
            set(goal_capability_to_dict(capability)),
            {"capability_id", "capability_name", "schema_version"},
        )
        self.assertEqual(set(goal_safe_mode_to_dict(safe_mode)), {"mode", "schema_version"})
        for forbidden in ("effective_authority", "approval_state", "restore", "promote"):
            self.assertFalse(hasattr(capability, forbidden))
            self.assertFalse(hasattr(safe_mode, forbidden))


class GoalEngineIdentifierTest(unittest.TestCase):
    def test_goal_idea_and_finding_identifiers_are_distinct(self) -> None:
        goal = GoalIdentifier("GOAL", "local:1", IDENTIFIER_SCHEMA_VERSION)
        idea = IdeaIdentifier("IDEA", "local:1", IDENTIFIER_SCHEMA_VERSION)
        finding = FindingIdentifier("FINDING", "local:1", IDENTIFIER_SCHEMA_VERSION)
        self.assertNotEqual(goal, idea)
        self.assertNotEqual(goal, finding)
        self.assertNotEqual(idea, finding)

    def test_identifiers_round_trip_with_only_identity_fields(self) -> None:
        fixtures = (
            (
                GoalIdentifier("GOAL", "goal:1", IDENTIFIER_SCHEMA_VERSION),
                goal_identifier_to_dict,
                goal_identifier_from_dict,
            ),
            (
                IdeaIdentifier("IDEA", "idea:1", IDENTIFIER_SCHEMA_VERSION),
                idea_identifier_to_dict,
                idea_identifier_from_dict,
            ),
            (
                FindingIdentifier("FINDING", "finding:1", IDENTIFIER_SCHEMA_VERSION),
                finding_identifier_to_dict,
                finding_identifier_from_dict,
            ),
        )
        for identifier, serializer, parser in fixtures:
            with self.subTest(kind=identifier.entity_kind):
                payload = serializer(identifier)
                self.assertEqual(
                    set(payload),
                    {"entity_kind", "local_id", "schema_version"},
                )
                self.assertEqual(parser(payload), identifier)

    def test_cross_kind_entity_aliases_fail(self) -> None:
        with self.assertRaises(GoalEngineFoundationError):
            GoalIdentifier("IDEA", "local:1", IDENTIFIER_SCHEMA_VERSION)

    def test_identifier_rejects_wording_and_unstable_values(self) -> None:
        for local_id in ("", " original user wording ", "contains spaces", "x" * 129):
            with self.subTest(local_id=local_id), self.assertRaises(GoalEngineFoundationError):
                GoalIdentifier("GOAL", local_id, IDENTIFIER_SCHEMA_VERSION)

    def test_identifier_is_frozen(self) -> None:
        identifier = GoalIdentifier("GOAL", "goal:1", IDENTIFIER_SCHEMA_VERSION)
        with self.assertRaises(FrozenInstanceError):
            identifier.local_id = "goal:2"


class GoalEvidenceAndContractTest(unittest.TestCase):
    def test_evidence_reference_preserves_hard_evidence_labels(self) -> None:
        reference = evidence_reference()
        payload = goal_evidence_reference_to_dict(reference)
        self.assertEqual(payload["historical_validity"], "VALID")
        self.assertEqual(payload["current_applicability"], "APPLICABLE")
        self.assertEqual(payload["review_state"], "REVIEWED")
        self.assertEqual(
            payload["conflict_ref_ids"],
            ["evidence:conflict:1", "evidence:conflict:2"],
        )
        self.assertEqual(goal_evidence_reference_from_dict(payload), reference)

    def test_evidence_reference_rejects_non_utc_and_duplicate_conflicts(self) -> None:
        with self.assertRaises(GoalEngineFoundationError):
            evidence_reference(observed_at="2026-08-08T12:00:00-05:00")
        with self.assertRaises(GoalEngineFoundationError):
            evidence_reference(conflict_ref_ids=("evidence:1", "evidence:1"))

    def test_goal_contract_round_trip_and_deterministic_identifier_order(self) -> None:
        contract = goal_contract()
        payload = goal_contract_to_dict(contract)
        self.assertEqual(payload["originating_idea_ids"], ["idea:1", "idea:2"])
        self.assertEqual(payload["expected_unaffected_systems"], ["providers", "validation"])
        self.assertEqual(goal_contract_from_dict(payload), contract)
        self.assertEqual(
            canonical_json_bytes(payload),
            canonical_json_bytes(goal_contract_to_dict(contract)),
        )

    def test_goal_contract_confidence_is_evidence_not_authority(self) -> None:
        payload = goal_contract_to_dict(goal_contract(confidence=1.0))
        self.assertEqual(payload["confidence"], 1.0)
        self.assertNotIn("authority", payload)
        self.assertNotIn("approved", payload)
        with self.assertRaises(GoalEngineFoundationError):
            goal_contract(confidence=1.01)

    def test_goal_contract_requires_origins_evidence_alternative_and_disconfirmation(self) -> None:
        invalid = (
            {"originating_idea_ids": (), "originating_finding_ids": ()},
            {"evidence_snapshot": ()},
            {"credible_alternatives": ()},
            {"disconfirmation_criteria": ()},
        )
        for override in invalid:
            with self.subTest(override=override), self.assertRaises(GoalEngineFoundationError):
                goal_contract(**override)

    def test_goal_contract_rejects_unknown_schema_and_runtime_state_field(self) -> None:
        payload = goal_contract_to_dict(goal_contract())
        payload["schema_version"] = "codie.goal_engine.goal_contract.v2"
        with self.assertRaises(GoalEngineFoundationError):
            goal_contract_from_dict(payload)
        payload = goal_contract_to_dict(goal_contract())
        payload["state"] = "ACTIVE"
        with self.assertRaisesRegex(GoalEngineFoundationError, "unknown field"):
            goal_contract_from_dict(payload)

    def test_material_revision_preserves_hash_and_stale_references(self) -> None:
        previous = goal_contract()
        reference = GoalContractRevisionReference(
            goal_contract_id=previous.goal_contract_id,
            revision=previous.revision,
            semantic_hash=goal_contract_semantic_hash(previous),
            stale_approval_ref_ids=("approval:phase44c:1",),
            stale_validator_ref_ids=("validator:phase44c:1",),
            schema_version=GOAL_CONTRACT_REVISION_REFERENCE_SCHEMA_VERSION,
        )
        current = replace(
            previous,
            revision=2,
            supersedes_revision=reference,
            desired_outcome="Represent the revised foundation deterministically.",
            created_at=UTC_2,
        )
        self.assertIs(validate_goal_contract_revision(previous, current), current)
        payload = goal_contract_to_dict(current)["supersedes_revision"]
        self.assertEqual(payload["semantic_hash"], goal_contract_semantic_hash(previous))
        self.assertEqual(payload["stale_approval_ref_ids"], ["approval:phase44c:1"])
        self.assertEqual(payload["stale_validator_ref_ids"], ["validator:phase44c:1"])

    def test_revision_rejects_missing_or_incorrect_history(self) -> None:
        previous = goal_contract()
        with self.assertRaises(GoalEngineFoundationError):
            replace(previous, revision=2)
        bad_reference = GoalContractRevisionReference(
            goal_contract_id=previous.goal_contract_id,
            revision=1,
            semantic_hash="0" * 64,
            stale_approval_ref_ids=(),
            stale_validator_ref_ids=(),
            schema_version=GOAL_CONTRACT_REVISION_REFERENCE_SCHEMA_VERSION,
        )
        current = replace(previous, revision=2, supersedes_revision=bad_reference)
        with self.assertRaisesRegex(GoalEngineFoundationError, "semantic hash"):
            validate_goal_contract_revision(previous, current)


class GoalPolicyRegistryTest(unittest.TestCase):
    def test_registry_preserves_superseded_policy_history(self) -> None:
        first = policy_record()
        reference = GoalPolicyReference(
            policy_id=first.policy_id,
            policy_version=first.policy_version,
            semantic_hash=goal_policy_record_semantic_hash(first),
            schema_version=POLICY_REFERENCE_SCHEMA_VERSION,
        )
        second = policy_record(
            policy_version=2,
            date="2026-08-09",
            reason="Clarify that model calls remain outside the foundation.",
            rule="Foundation records are local, caller-input-only, and model-free.",
            superseded_policy_ref=reference,
        )
        registry = GoalPolicyRegistry(
            records=(second, first),
            schema_version=POLICY_REGISTRY_SCHEMA_VERSION,
        )
        self.assertEqual([item.policy_version for item in registry.records], [1, 2])
        self.assertEqual(lookup_goal_policy(registry, first.policy_id), second)
        self.assertEqual(lookup_goal_policy(registry, first.policy_id, 1), first)
        self.assertEqual(
            goal_policy_registry_from_dict(goal_policy_registry_to_dict(registry)),
            registry,
        )

    def test_registry_rejects_missing_or_tampered_history(self) -> None:
        first = policy_record()
        bad_reference = GoalPolicyReference(
            policy_id=first.policy_id,
            policy_version=1,
            semantic_hash="0" * 64,
            schema_version=POLICY_REFERENCE_SCHEMA_VERSION,
        )
        second = policy_record(policy_version=2, superseded_policy_ref=bad_reference)
        with self.assertRaisesRegex(GoalEngineFoundationError, "semantic hash"):
            GoalPolicyRegistry(
                records=(first, second),
                schema_version=POLICY_REGISTRY_SCHEMA_VERSION,
            )

    def test_registry_rejects_duplicate_and_unknown_affected_policy(self) -> None:
        first = policy_record()
        with self.assertRaises(GoalEngineFoundationError):
            GoalPolicyRegistry(
                records=(first, first),
                schema_version=POLICY_REGISTRY_SCHEMA_VERSION,
            )
        unknown = policy_record(affected_policy_ids=("policy:missing",))
        with self.assertRaisesRegex(GoalEngineFoundationError, "unknown policy"):
            GoalPolicyRegistry(
                records=(unknown,),
                schema_version=POLICY_REGISTRY_SCHEMA_VERSION,
            )

    def test_registry_fails_closed_without_policy_invention(self) -> None:
        registry = GoalPolicyRegistry(
            records=(policy_record(),),
            schema_version=POLICY_REGISTRY_SCHEMA_VERSION,
        )
        with self.assertRaisesRegex(GoalEngineFoundationError, "unknown policy_id"):
            lookup_goal_policy(registry, "policy:unmodeled-situation")
        for forbidden in ("execute", "adopt", "amend", "write"):
            self.assertFalse(hasattr(registry, forbidden))


class GoalLineageTest(unittest.TestCase):
    def test_lineage_hash_is_deterministic_and_decisions_remain_separate(self) -> None:
        first = lineage_event()
        same = lineage_event()
        self.assertEqual(first.event_hash, same.event_hash)
        payload = goal_lineage_event_to_dict(first)
        self.assertEqual(payload["evidence_ref_ids"], ["evidence:measured:1"])
        self.assertEqual(payload["human_decision_ref_ids"], ["decision:human:1"])
        self.assertNotEqual(payload["evidence_ref_ids"], payload["human_decision_ref_ids"])
        self.assertEqual(goal_lineage_event_from_dict(payload), first)

    def test_lineage_chain_preserves_prior_event_hash(self) -> None:
        first = lineage_event()
        second = lineage_event(
            event_id="lineage:event:2",
            entity_revision=2,
            event_kind="CONTRACT_REVISED",
            occurred_at=UTC_2,
            summary="A material revision preserved the earlier event.",
            prior_event_ids=(first.event_id,),
            prior_event_hashes=(first.event_hash,),
        )
        self.assertEqual(validate_goal_lineage_chain((first, second)), (first, second))

    def test_lineage_rejects_tamper_future_reference_and_time_reversal(self) -> None:
        first = lineage_event()
        payload = goal_lineage_event_to_dict(first)
        payload["summary"] = "Tampered summary."
        with self.assertRaisesRegex(GoalEngineFoundationError, "event_hash"):
            goal_lineage_event_from_dict(payload)
        future = lineage_event(
            event_id="lineage:event:2",
            occurred_at=UTC_2,
            prior_event_ids=("lineage:event:future",),
            prior_event_hashes=("0" * 64,),
        )
        with self.assertRaisesRegex(GoalEngineFoundationError, "already exist"):
            validate_goal_lineage_chain((first, future))
        earlier = lineage_event(
            event_id="lineage:event:earlier",
            occurred_at="2026-08-08T11:59:00Z",
        )
        with self.assertRaisesRegex(GoalEngineFoundationError, "time order"):
            validate_goal_lineage_chain((first, earlier))

    def test_lineage_rejects_unknown_event_kind_and_misaligned_prior_hashes(self) -> None:
        with self.assertRaises(GoalEngineFoundationError):
            lineage_event(event_kind="AUTO_PROMOTED")
        with self.assertRaises(GoalEngineFoundationError):
            lineage_event(prior_event_ids=("lineage:event:0",), prior_event_hashes=())

    def test_lineage_rejects_conflated_evidence_and_human_decision_refs(self) -> None:
        with self.assertRaisesRegex(GoalEngineFoundationError, "remain separate"):
            lineage_event(
                evidence_ref_ids=("reference:shared:1",),
                human_decision_ref_ids=("reference:shared:1",),
            )


class GoalFoundationBoundaryTest(unittest.TestCase):
    def test_canonical_json_is_compact_sorted_utf8_and_hash_stable(self) -> None:
        left = {"z": "café", "a": [2, 1]}
        right = {"a": [2, 1], "z": "café"}
        encoded = canonical_json_bytes(left)
        self.assertEqual(encoded, b'{"a":[2,1],"z":"caf\xc3\xa9"}')
        self.assertEqual(encoded, canonical_json_bytes(right))
        self.assertEqual(semantic_hash(left), semantic_hash(right))
        with self.assertRaises(GoalEngineFoundationError):
            canonical_json_bytes({"value": float("nan")})

    def test_serialized_records_reject_unknown_secret_and_raw_fields(self) -> None:
        base = goal_identifier_to_dict(
            GoalIdentifier("GOAL", "goal:1", IDENTIFIER_SCHEMA_VERSION)
        )
        for field_name in (
            "secret",
            "token",
            "credential",
            "cookie",
            "session",
            "prompt_log",
            "raw_payload",
            "provider_payload",
            "private_deck_text",
        ):
            payload = dict(base)
            payload[field_name] = "forbidden"
            with self.subTest(field_name=field_name), self.assertRaises(
                GoalEngineFoundationError
            ):
                goal_identifier_from_dict(payload)

    def test_foundation_uses_only_standard_library_imports(self) -> None:
        source_path = Path(goal_engine.foundation.__file__)
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
            if isinstance(node, ast.ImportFrom) and node.module != "__future__"
        )
        self.assertEqual(
            imported_roots,
            {
                "collections",
                "dataclasses",
                "datetime",
                "hashlib",
                "json",
                "re",
                "types",
                "typing",
            },
        )

    def test_public_surface_has_no_runtime_authority_or_later_phase_types(self) -> None:
        forbidden_fragments = (
            "activate",
            "agent",
            "build_graph",
            "decision_core",
            "execute",
            "experiment",
            "finding_record",
            "idea_record",
            "kill_switch",
            "persist",
            "promote",
            "queue",
            "restore_authority",
            "scheduler",
            "shadow",
            "state_engine",
            "stream_deck",
        )
        exported = "\n".join(goal_engine.__all__).lower()
        for fragment in forbidden_fragments:
            self.assertNotIn(fragment, exported)

    def test_contract_records_are_frozen_and_contain_no_mutable_collections(self) -> None:
        contract = goal_contract()
        with self.assertRaises(FrozenInstanceError):
            contract.risk = "Critical"
        payload = goal_contract_to_dict(contract)
        json.dumps(payload, sort_keys=True, ensure_ascii=False)
        self.assertIsInstance(contract.evidence_snapshot, tuple)
        self.assertIsInstance(contract.approval_requirements, tuple)


if __name__ == "__main__":
    unittest.main()
