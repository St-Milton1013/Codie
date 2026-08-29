from __future__ import annotations

import ast
import math
import unittest
from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

from codie.goal_engine.foundation import (
    EVIDENCE_REFERENCE_SCHEMA_VERSION,
    IDENTIFIER_SCHEMA_VERSION,
    FindingIdentifier,
    GoalEvidenceReference,
    IdeaIdentifier,
    semantic_hash,
)
from codie.goal_engine.idea_ledger import (
    FINDING_ORIGINS,
    FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION,
    HISTORY_EVENT_KINDS,
    IDEA_OCCURRENCE_SCHEMA_VERSION,
    IDEA_RECORD_SCHEMA_VERSION,
    IDEA_STATES,
    LEDGER_ENTITY_KINDS,
    LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
    LEDGER_FINDING_SCHEMA_VERSION,
    LEDGER_HISTORY_EVENT_SCHEMA_VERSION,
    LEDGER_RELATION_SCHEMA_VERSION,
    LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
    RECONSIDERATION_REQUEST_SCHEMA_VERSION,
    RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
    RELATION_TYPES,
    SENSITIVITY_VALUES,
    TRIGGER_KINDS,
    FindingsIdeaLedgerSnapshot,
    GoalEngineIdeaLedgerError,
    IdeaOccurrence,
    IdeaRecord,
    LedgerEntityReference,
    LedgerFinding,
    LedgerHistoryEvent,
    LedgerRelation,
    LedgerSnapshotReference,
    ReconsiderationRequest,
    ReconsiderationTrigger,
    build_findings_idea_ledger_snapshot,
    build_reconsideration_request,
    define_reconsideration_trigger,
    findings_idea_ledger_snapshot_from_dict,
    findings_idea_ledger_snapshot_semantic_hash,
    findings_idea_ledger_snapshot_to_dict,
    idea_occurrence_from_dict,
    idea_occurrence_to_dict,
    idea_record_from_dict,
    idea_record_semantic_hash,
    idea_record_to_dict,
    ledger_entity_reference_from_dict,
    ledger_entity_reference_to_dict,
    ledger_finding_from_dict,
    ledger_finding_semantic_hash,
    ledger_finding_to_dict,
    ledger_history_event_from_dict,
    ledger_history_event_semantic_hash,
    ledger_history_event_to_dict,
    ledger_relation_from_dict,
    ledger_relation_to_dict,
    ledger_snapshot_reference_from_dict,
    ledger_snapshot_reference_to_dict,
    reconsideration_request_from_dict,
    reconsideration_request_to_dict,
    reconsideration_trigger_from_dict,
    reconsideration_trigger_to_dict,
    record_finding,
    record_idea,
    record_occurrence,
    record_relation,
    validate_finding_origin,
    validate_history_event_kind,
    validate_idea_revision,
    validate_idea_state,
    validate_ledger_entity_kind,
    validate_ledger_snapshot_revision,
    validate_relation_type,
    validate_sensitivity,
    validate_trigger_kind,
)

T0 = "2026-08-29T00:00:00Z"
T1 = "2026-08-29T00:01:00Z"
T2 = "2026-08-29T00:02:00Z"
T3 = "2026-08-29T00:03:00Z"
T4 = "2026-08-29T00:04:00Z"
T5 = "2026-08-29T00:05:00Z"

SOURCE_PAYLOAD = {
    "schema_version": "codie.goal_engine.health_finding.v1",
    "statement": "The bounded signal is degraded.",
    "why_it_matters": "The cited behavior needs review.",
    "evidence_ref_ids": ["ev:fact"],
    "conflict_ref_ids": ["ev:conflict"],
    "confidence": 0.7,
    "disconfirmation_criteria": ["Supply a passing current observation."],
    "limitations": ["This finding is bounded to the cited signal."],
    "created_at": T0,
}
SOURCE_HASH = semantic_hash(SOURCE_PAYLOAD)


def evidence(
    ref_id: str,
    *,
    evidence_class: str = "OBJECTIVE",
    privacy_class: str = "PROJECT_INTERNAL",
    conflicts: tuple[str, ...] = (),
) -> GoalEvidenceReference:
    return GoalEvidenceReference(
        evidence_ref_id=ref_id,
        evidence_class=evidence_class,
        source_id=f"source:{ref_id}",
        source_version="v1",
        observed_at=T0,
        historical_validity="VERIFIED",
        current_applicability="CURRENT",
        review_state="REVIEWED",
        privacy_class=privacy_class,
        conflict_ref_ids=conflicts,
        schema_version=EVIDENCE_REFERENCE_SCHEMA_VERSION,
    )


def external_reference(
    entity_kind: str,
    entity_id: str,
    *,
    revision: int | None = None,
    digest: str = "a" * 64,
) -> LedgerEntityReference:
    return LedgerEntityReference(
        entity_kind=entity_kind,
        entity_id=entity_id,
        revision=revision,
        semantic_hash=digest,
        schema_version=LEDGER_ENTITY_REFERENCE_SCHEMA_VERSION,
    )


def idea_identifier(local_id: str = "idea:one") -> IdeaIdentifier:
    return IdeaIdentifier(
        entity_kind="IDEA",
        local_id=local_id,
        schema_version=IDENTIFIER_SCHEMA_VERSION,
    )


def finding_identifier(local_id: str = "finding:one") -> FindingIdentifier:
    return FindingIdentifier(
        entity_kind="FINDING",
        local_id=local_id,
        schema_version=IDENTIFIER_SCHEMA_VERSION,
    )


def idea_record(
    *,
    local_id: str = "idea:one",
    revision: int = 1,
    original_wording: str = "Keep the original user wording.",
    summary: str = "Preserve the bounded idea.",
    state: str = "UNTRIAGED",
    occurrence_ids: tuple[str, ...] = (),
    relation_ids: tuple[str, ...] = (),
    trigger_ids: tuple[str, ...] = (),
    finding_ref_ids: tuple[str, ...] = (),
    human_refs: tuple[str, ...] = (),
    policy_refs: tuple[str, ...] = (),
    updated_at: str = T1,
    supersedes: str | None = None,
    sensitivity: str = "PROJECT_INTERNAL",
    owner: str | None = None,
) -> IdeaRecord:
    return IdeaRecord(
        idea_id=idea_identifier(local_id),
        revision=revision,
        original_wording=original_wording,
        current_summary=summary,
        state=state,
        origin_ref_ids=("ev:origin",),
        finding_ref_ids=finding_ref_ids,
        relation_ids=relation_ids,
        occurrence_ids=occurrence_ids,
        trigger_ids=trigger_ids,
        human_decision_ref_ids=human_refs,
        policy_ref_ids=policy_refs,
        created_at=T1,
        updated_at=updated_at,
        sensitivity=sensitivity,
        owner_ref_id=owner,
        supersedes_idea_hash=supersedes,
        schema_version=IDEA_RECORD_SCHEMA_VERSION,
    )


def finding_record(
    *,
    local_id: str = "finding:one",
    source_hash: str = SOURCE_HASH,
    sensitivity: str = "PROJECT_INTERNAL",
    owner: str | None = None,
) -> LedgerFinding:
    return LedgerFinding(
        finding_id=finding_identifier(local_id),
        origin="HEALTH_FINDING",
        statement="The bounded signal is degraded.",
        why_it_matters="The cited behavior needs review.",
        source_record_ref_id="health:source",
        source_record_semantic_hash=source_hash,
        evidence_ref_ids=("ev:fact",),
        conflict_ref_ids=("ev:conflict",),
        confidence=0.7,
        disconfirmation_criteria=("Supply a passing current observation.",),
        limitations=("This finding is bounded to the cited signal.",),
        observed_at=T0,
        recorded_at=T1,
        sensitivity=sensitivity,
        owner_ref_id=owner,
        schema_version=LEDGER_FINDING_SCHEMA_VERSION,
    )


def idea_reference(idea: IdeaRecord) -> LedgerEntityReference:
    return external_reference(
        "IDEA",
        idea.idea_id.local_id,
        revision=idea.revision,
        digest=idea_record_semantic_hash(idea),
    )


def finding_reference(finding: LedgerFinding) -> LedgerEntityReference:
    return external_reference(
        "FINDING",
        finding.finding_id.local_id,
        digest=ledger_finding_semantic_hash(finding),
    )


def history_event(
    *,
    event_id: str,
    event_kind: str,
    entity: LedgerEntityReference,
    created_at: str,
    related: tuple[str, ...] = (),
    evidence_refs: tuple[str, ...] = (),
    human_refs: tuple[str, ...] = (),
    policy_refs: tuple[str, ...] = (),
    prior_hash: str | None = None,
) -> LedgerHistoryEvent:
    return LedgerHistoryEvent(
        event_id=event_id,
        event_kind=event_kind,
        entity=entity,
        related_ref_ids=related,
        evidence_ref_ids=evidence_refs,
        human_decision_ref_ids=human_refs,
        policy_ref_ids=policy_refs,
        statement=f"Recorded {event_kind} without granting authority.",
        created_at=created_at,
        prior_event_hash=prior_hash,
        schema_version=LEDGER_HISTORY_EVENT_SCHEMA_VERSION,
    )


def base_snapshot(
    *,
    evidence_values: tuple[GoalEvidenceReference, ...] | None = None,
    external_values: tuple[LedgerEntityReference, ...] | None = None,
) -> FindingsIdeaLedgerSnapshot:
    if evidence_values is None:
        evidence_values = (
            evidence("ev:origin", evidence_class="USER_INPUT"),
            evidence("ev:fact"),
            evidence("ev:conflict", evidence_class="CONFLICTING_OBJECTIVE"),
            evidence("ev:human", evidence_class="HUMAN_DECISION"),
            evidence("ev:policy", evidence_class="POLICY"),
        )
    if external_values is None:
        external_values = (
            external_reference("FINDING", "health:source", digest=SOURCE_HASH),
            external_reference("GOAL", "goal:prior", revision=1, digest="b" * 64),
        )
    return build_findings_idea_ledger_snapshot(
        snapshot_id="ledger:main",
        revision=1,
        ledger_scope_id="scope:codie",
        as_of=T1,
        findings=(),
        ideas=(),
        occurrences=(),
        relations=(),
        triggers=(),
        reconsideration_requests=(),
        history_events=(),
        evidence_snapshot=evidence_values,
        external_entity_references=external_values,
        supersedes_snapshot=None,
    )


def snapshot_with_idea() -> tuple[FindingsIdeaLedgerSnapshot, IdeaRecord, LedgerHistoryEvent]:
    snapshot = base_snapshot()
    idea = idea_record()
    event = history_event(
        event_id="event:idea:1",
        event_kind="IDEA_CAPTURED",
        entity=idea_reference(idea),
        created_at=T1,
    )
    return record_idea(snapshot, idea, event, as_of=T1), idea, event


def revise_idea(
    prior: IdeaRecord,
    *,
    updated_at: str,
    **changes,
) -> IdeaRecord:
    return replace(
        prior,
        revision=prior.revision + 1,
        updated_at=updated_at,
        supersedes_idea_hash=idea_record_semantic_hash(prior),
        **changes,
    )


def source_payload_for(finding: LedgerFinding) -> dict[str, object]:
    return {
        "schema_version": "codie.goal_engine.health_finding.v1",
        "statement": finding.statement,
        "why_it_matters": finding.why_it_matters,
        "evidence_ref_ids": list(finding.evidence_ref_ids),
        "conflict_ref_ids": list(finding.conflict_ref_ids),
        "confidence": finding.confidence,
        "disconfirmation_criteria": list(finding.disconfirmation_criteria),
        "limitations": list(finding.limitations),
        "created_at": finding.observed_at,
    }


def replace_idea_snapshot(
    snapshot: FindingsIdeaLedgerSnapshot,
    prior: IdeaRecord,
    revised: IdeaRecord,
    event: LedgerHistoryEvent,
    *,
    as_of: str,
) -> FindingsIdeaLedgerSnapshot:
    prior_ref = idea_reference(prior)
    references = snapshot.external_entity_references
    if prior_ref not in references:
        references += (prior_ref,)
    return build_findings_idea_ledger_snapshot(
        snapshot_id=snapshot.snapshot_id,
        revision=snapshot.revision + 1,
        ledger_scope_id=snapshot.ledger_scope_id,
        as_of=as_of,
        findings=snapshot.findings,
        ideas=(revised,),
        occurrences=snapshot.occurrences,
        relations=snapshot.relations,
        triggers=snapshot.triggers,
        reconsideration_requests=snapshot.reconsideration_requests,
        history_events=snapshot.history_events + (event,),
        evidence_snapshot=snapshot.evidence_snapshot,
        external_entity_references=references,
        supersedes_snapshot=LedgerSnapshotReference(
            snapshot_id=snapshot.snapshot_id,
            revision=snapshot.revision,
            semantic_hash=findings_idea_ledger_snapshot_semantic_hash(snapshot),
            schema_version=LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        ),
    )


class IdeaLedgerVocabularyTest(unittest.TestCase):
    def test_exact_ratified_vocabularies(self) -> None:
        self.assertEqual(
            IDEA_STATES,
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
            },
        )
        self.assertEqual(
            RELATION_TYPES,
            {"duplicate", "extension", "alternative", "contradiction", "dependency", "related"},
        )
        self.assertNotIn("new", RELATION_TYPES)
        self.assertEqual(len(FINDING_ORIGINS), 4)
        self.assertEqual(len(LEDGER_ENTITY_KINDS), 6)
        self.assertEqual(len(TRIGGER_KINDS), 7)
        self.assertEqual(len(HISTORY_EVENT_KINDS), 10)
        self.assertEqual(len(SENSITIVITY_VALUES), 5)

    def test_case_aliases_and_new_relation_fail_closed(self) -> None:
        validators = (
            (validate_idea_state, "untriaged"),
            (validate_finding_origin, "validator_finding"),
            (validate_relation_type, "new"),
            (validate_ledger_entity_kind, "RELATION"),
            (validate_trigger_kind, "AUTOMATIC"),
            (validate_history_event_kind, "GOAL_CREATED"),
            (validate_sensitivity, "PRIVATE"),
        )
        for validator, value in validators:
            with self.subTest(value=value), self.assertRaises(GoalEngineIdeaLedgerError):
                validator(value)

    def test_exact_schema_versions(self) -> None:
        self.assertEqual(LEDGER_FINDING_SCHEMA_VERSION, "codie.goal_engine.ledger_finding.v1")
        self.assertEqual(IDEA_RECORD_SCHEMA_VERSION, "codie.goal_engine.idea_record.v1")
        self.assertEqual(IDEA_OCCURRENCE_SCHEMA_VERSION, "codie.goal_engine.idea_occurrence.v1")
        self.assertEqual(LEDGER_RELATION_SCHEMA_VERSION, "codie.goal_engine.ledger_relation.v1")
        self.assertEqual(
            RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
            "codie.goal_engine.reconsideration_trigger.v1",
        )
        self.assertEqual(
            FINDINGS_IDEA_LEDGER_SNAPSHOT_SCHEMA_VERSION,
            "codie.goal_engine.findings_idea_ledger_snapshot.v1",
        )


class IdeaLedgerRecordTest(unittest.TestCase):
    def test_idea_finding_and_goal_identity_never_conflate(self) -> None:
        idea = idea_identifier("shared:id")
        finding = finding_identifier("shared:id")
        self.assertNotEqual(idea, finding)
        self.assertEqual(idea.entity_kind, "IDEA")
        self.assertEqual(finding.entity_kind, "FINDING")
        self.assertNotIn("goal_id", {item.name for item in fields(IdeaRecord)})
        self.assertNotIn("goal_id", {item.name for item in fields(LedgerFinding)})

    def test_records_are_frozen_and_use_tuples(self) -> None:
        idea = idea_record()
        with self.assertRaises(FrozenInstanceError):
            idea.state = "WATCHING"  # type: ignore[misc]
        with self.assertRaises(GoalEngineIdeaLedgerError):
            replace(idea, origin_ref_ids=["ev:origin"])  # type: ignore[arg-type]

    def test_original_wording_requires_nfc_and_is_immutable(self) -> None:
        decomposed = "Cafe\u0301"
        with self.assertRaises(GoalEngineIdeaLedgerError):
            idea_record(original_wording=decomposed)
        first = idea_record(original_wording="Café")
        revised = revise_idea(
            first,
            updated_at=T2,
            current_summary="A clearer summary.",
        )
        self.assertIs(validate_idea_revision(revised, first), revised)
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "original_wording"):
            validate_idea_revision(
                replace(revised, original_wording="Different wording."),
                first,
            )

    def test_goal_candidate_is_only_an_idea_state(self) -> None:
        idea = idea_record(
            state="GOAL_CANDIDATE",
            human_refs=("ev:human",),
        )
        payload = idea_record_to_dict(idea)
        self.assertEqual(payload["state"], "GOAL_CANDIDATE")
        self.assertNotIn("goal", payload)
        self.assertNotIn("authority", payload)

    def test_archived_conditional_requires_trigger(self) -> None:
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "requires.*trigger"):
            idea_record(
                state="ARCHIVED_CONDITIONAL",
                policy_refs=("ev:policy",),
            )

    def test_private_records_require_owner(self) -> None:
        with self.assertRaises(GoalEngineIdeaLedgerError):
            idea_record(sensitivity="USER_PRIVATE")
        private = idea_record(sensitivity="USER_PRIVATE", owner="owner:one")
        self.assertEqual(private.owner_ref_id, "owner:one")

    def test_raw_secret_material_fails_closed(self) -> None:
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "secret"):
            idea_record(original_wording="password=hunter2")

    def test_finding_requires_visible_support_limits_and_disconfirmation(self) -> None:
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "requires evidence"):
            replace(finding_record(), evidence_ref_ids=(), conflict_ref_ids=())
        with self.assertRaises(GoalEngineIdeaLedgerError):
            replace(finding_record(), limitations=())
        with self.assertRaises(GoalEngineIdeaLedgerError):
            replace(finding_record(), disconfirmation_criteria=())

    def test_finding_confidence_is_finite_bounded_evidence(self) -> None:
        for confidence in (math.nan, math.inf, -0.1, 1.1):
            with self.subTest(confidence=confidence), self.assertRaises(GoalEngineIdeaLedgerError):
                replace(finding_record(), confidence=confidence)

    def test_trigger_rules_are_declarative_and_exact(self) -> None:
        with self.assertRaises(GoalEngineIdeaLedgerError):
            ReconsiderationTrigger(
                trigger_id="trigger:bad",
                idea_id=idea_identifier(),
                trigger_kind="EVIDENCE_CHANGE",
                condition_summary="Caller reports changed evidence.",
                required_evidence_classes=(),
                recurrence_threshold=2,
                not_before=None,
                expires_at=None,
                created_at=T1,
                created_by_ref_id="actor:one",
                schema_version=RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
            )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "not_before"):
            ReconsiderationTrigger(
                trigger_id="trigger:time",
                idea_id=idea_identifier(),
                trigger_kind="TIME_WINDOW",
                condition_summary="Review in the declared time window.",
                required_evidence_classes=(),
                recurrence_threshold=None,
                not_before=None,
                expires_at=None,
                created_at=T1,
                created_by_ref_id="actor:one",
                schema_version=RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
            )


class IdeaLedgerSerializationTest(unittest.TestCase):
    def test_all_leaf_records_round_trip(self) -> None:
        idea = idea_record()
        finding = finding_record()
        occurrence = IdeaOccurrence(
            occurrence_id="occurrence:one",
            idea_id=idea.idea_id,
            occurred_at=T2,
            context_summary="The same bounded idea recurred.",
            source_ref_ids=("ev:origin",),
            evidence_ref_ids=("ev:fact",),
            sensitivity="PROJECT_INTERNAL",
            owner_ref_id=None,
            schema_version=IDEA_OCCURRENCE_SCHEMA_VERSION,
        )
        relation = LedgerRelation(
            relation_id="relation:one",
            source=idea_reference(idea),
            target=external_reference("GOAL", "goal:prior", revision=1, digest="b" * 64),
            relation_type="related",
            basis_ref_ids=("ev:fact",),
            confidence=0.4,
            limitations=("The relation is caller-supplied.",),
            created_at=T2,
            created_by_ref_id="actor:one",
            schema_version=LEDGER_RELATION_SCHEMA_VERSION,
        )
        trigger = ReconsiderationTrigger(
            trigger_id="trigger:one",
            idea_id=idea.idea_id,
            trigger_kind="HUMAN_REQUEST",
            condition_summary="A human asks for fresh review.",
            required_evidence_classes=(),
            recurrence_threshold=None,
            not_before=None,
            expires_at=None,
            created_at=T2,
            created_by_ref_id="actor:one",
            schema_version=RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
        )
        request = ReconsiderationRequest(
            request_id="request:one",
            idea_id=idea.idea_id,
            idea_revision=1,
            trigger_id=trigger.trigger_id,
            as_of=T3,
            evidence_ref_ids=(),
            occurrence_ids=(),
            human_request_ref_ids=("ev:human",),
            limitations=("A fresh Necessity Test is still required.",),
            schema_version=RECONSIDERATION_REQUEST_SCHEMA_VERSION,
        )
        event = history_event(
            event_id="event:one",
            event_kind="IDEA_CAPTURED",
            entity=idea_reference(idea),
            created_at=T1,
        )
        snapshot_ref = LedgerSnapshotReference(
            snapshot_id="ledger:main",
            revision=1,
            semantic_hash="c" * 64,
            schema_version=LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
        )
        round_trips = (
            (finding, ledger_finding_to_dict, ledger_finding_from_dict),
            (idea, idea_record_to_dict, idea_record_from_dict),
            (occurrence, idea_occurrence_to_dict, idea_occurrence_from_dict),
            (
                relation.source,
                ledger_entity_reference_to_dict,
                ledger_entity_reference_from_dict,
            ),
            (relation, ledger_relation_to_dict, ledger_relation_from_dict),
            (
                trigger,
                reconsideration_trigger_to_dict,
                reconsideration_trigger_from_dict,
            ),
            (
                request,
                reconsideration_request_to_dict,
                reconsideration_request_from_dict,
            ),
            (event, ledger_history_event_to_dict, ledger_history_event_from_dict),
            (
                snapshot_ref,
                ledger_snapshot_reference_to_dict,
                ledger_snapshot_reference_from_dict,
            ),
        )
        for value, to_dict, from_dict in round_trips:
            with self.subTest(type=type(value).__name__):
                self.assertEqual(from_dict(to_dict(value)), value)

    def test_snapshot_round_trip_and_hash_are_byte_stable(self) -> None:
        snapshot, _, _ = snapshot_with_idea()
        payload = findings_idea_ledger_snapshot_to_dict(snapshot)
        restored = findings_idea_ledger_snapshot_from_dict(payload)
        self.assertEqual(restored, snapshot)
        self.assertEqual(
            findings_idea_ledger_snapshot_semantic_hash(restored),
            findings_idea_ledger_snapshot_semantic_hash(snapshot),
        )

    def test_semantically_unordered_inputs_sort_canonically(self) -> None:
        evidence_values = (
            evidence("ev:z"),
            evidence("ev:a"),
        )
        refs = (
            external_reference("GOAL", "goal:z", revision=1, digest="f" * 64),
            external_reference("GOAL", "goal:a", revision=1, digest="e" * 64),
        )
        left = base_snapshot(evidence_values=evidence_values, external_values=refs)
        right = base_snapshot(
            evidence_values=tuple(reversed(evidence_values)),
            external_values=tuple(reversed(refs)),
        )
        self.assertEqual(left, right)
        self.assertEqual(
            findings_idea_ledger_snapshot_semantic_hash(left),
            findings_idea_ledger_snapshot_semantic_hash(right),
        )

    def test_unknown_forbidden_and_mutable_fields_fail_closed(self) -> None:
        payload = idea_record_to_dict(idea_record())
        payload["priority"] = 1
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "unknown field"):
            idea_record_from_dict(payload)
        payload = idea_record_to_dict(idea_record())
        payload["token"] = "not-allowed"
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "forbidden field"):
            idea_record_from_dict(payload)
        payload = idea_record_to_dict(idea_record())
        payload["origin_ref_ids"] = ("ev:origin",)
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "array"):
            idea_record_from_dict(payload)


class IdeaLedgerSnapshotTest(unittest.TestCase):
    def test_empty_snapshot_is_valid_and_has_no_authority_output(self) -> None:
        snapshot = base_snapshot()
        payload = findings_idea_ledger_snapshot_to_dict(snapshot)
        for forbidden in ("score", "rank", "priority", "goal", "work_order", "action"):
            self.assertNotIn(forbidden, payload)

    def test_record_idea_appends_history_without_goal_creation(self) -> None:
        snapshot, idea, event = snapshot_with_idea()
        self.assertEqual(snapshot.ideas, (idea,))
        self.assertEqual(snapshot.history_events, (event,))
        self.assertEqual(snapshot.revision, 2)
        self.assertEqual(idea.state, "UNTRIAGED")
        self.assertIs(validate_ledger_snapshot_revision(snapshot, base_snapshot()), snapshot)

    def test_initial_classification_requires_explicit_reference(self) -> None:
        snapshot = base_snapshot()
        idea = idea_record(state="WATCHING")
        event = history_event(
            event_id="event:idea:watching",
            event_kind="IDEA_CAPTURED",
            entity=idea_reference(idea),
            created_at=T1,
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "classification requires"):
            record_idea(snapshot, idea, event, as_of=T1)

    def test_record_finding_preserves_exact_source_hash_and_evidence(self) -> None:
        snapshot = base_snapshot()
        finding = finding_record()
        event = history_event(
            event_id="event:finding:1",
            event_kind="FINDING_ADMITTED",
            entity=finding_reference(finding),
            created_at=T1,
            evidence_refs=("ev:fact",),
        )
        recorded = record_finding(
            snapshot,
            finding,
            SOURCE_PAYLOAD,
            event,
            as_of=T1,
        )
        self.assertEqual(recorded.findings, (finding,))
        self.assertEqual(recorded.findings[0].source_record_semantic_hash, SOURCE_HASH)
        self.assertEqual(recorded.findings[0].conflict_ref_ids, ("ev:conflict",))

    def test_finding_source_hash_mismatch_and_dangling_evidence_fail(self) -> None:
        snapshot = base_snapshot()
        finding = finding_record(source_hash="f" * 64)
        event = history_event(
            event_id="event:finding:bad",
            event_kind="FINDING_ADMITTED",
            entity=finding_reference(finding),
            created_at=T1,
        )
        with self.assertRaisesRegex(
            GoalEngineIdeaLedgerError,
            "does not match source_record_semantic_hash",
        ):
            record_finding(snapshot, finding, SOURCE_PAYLOAD, event, as_of=T1)
        bad_without_hash = replace(
            finding_record(),
            evidence_ref_ids=("ev:missing",),
        )
        bad_payload = source_payload_for(bad_without_hash)
        bad_hash = semantic_hash(bad_payload)
        bad = replace(
            bad_without_hash,
            source_record_semantic_hash=bad_hash,
        )
        bad_event = replace(event, entity=finding_reference(bad))
        bad_snapshot = base_snapshot(
            external_values=(
                external_reference("FINDING", "health:source", digest=bad_hash),
                external_reference(
                    "GOAL",
                    "goal:prior",
                    revision=1,
                    digest="b" * 64,
                ),
            )
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "dangling Finding evidence"):
            record_finding(
                bad_snapshot,
                bad,
                bad_payload,
                bad_event,
                as_of=T1,
            )

    def test_finding_admission_rejects_rewritten_source_ceiling_and_secrets(self) -> None:
        rewritten_payload = dict(SOURCE_PAYLOAD)
        rewritten_payload["statement"] = "A stronger statement than the source supports."
        rewritten_hash = semantic_hash(rewritten_payload)
        finding = replace(
            finding_record(),
            source_record_semantic_hash=rewritten_hash,
        )
        snapshot = base_snapshot(
            external_values=(
                external_reference("FINDING", "health:source", digest=rewritten_hash),
                external_reference(
                    "GOAL",
                    "goal:prior",
                    revision=1,
                    digest="b" * 64,
                ),
            )
        )
        event = history_event(
            event_id="event:finding:rewritten",
            event_kind="FINDING_ADMITTED",
            entity=finding_reference(finding),
            created_at=T1,
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "rewrites source statement"):
            record_finding(
                snapshot,
                finding,
                rewritten_payload,
                event,
                as_of=T1,
            )
        secret_payload = dict(SOURCE_PAYLOAD)
        secret_payload["metadata"] = {"token": "forbidden"}
        secret_finding = replace(
            finding_record(),
            source_record_semantic_hash=semantic_hash(secret_payload),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "forbidden field"):
            record_finding(
                base_snapshot(),
                secret_finding,
                secret_payload,
                replace(event, entity=finding_reference(secret_finding)),
                as_of=T1,
            )

    def test_duplicate_ids_and_dangling_idea_links_fail(self) -> None:
        idea = idea_record(finding_ref_ids=("finding:missing",))
        event = history_event(
            event_id="event:idea:dangling",
            event_kind="IDEA_CAPTURED",
            entity=idea_reference(idea),
            created_at=T1,
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "dangling Idea Finding"):
            record_idea(base_snapshot(), idea, event, as_of=T1)
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "duplicate identity"):
            build_findings_idea_ledger_snapshot(
                snapshot_id="ledger:bad",
                revision=1,
                ledger_scope_id="scope:bad",
                as_of=T1,
                findings=(),
                ideas=(),
                occurrences=(),
                relations=(),
                triggers=(),
                reconsideration_requests=(),
                history_events=(),
                evidence_snapshot=(evidence("ev:one"), evidence("ev:one")),
                external_entity_references=(),
                supersedes_snapshot=None,
            )

    def test_recurrence_adds_occurrence_only_and_cannot_change_state(self) -> None:
        snapshot, prior, prior_event = snapshot_with_idea()
        occurrence = IdeaOccurrence(
            occurrence_id="occurrence:one",
            idea_id=prior.idea_id,
            occurred_at=T2,
            context_summary="The same stable Idea was observed again.",
            source_ref_ids=("ev:origin",),
            evidence_ref_ids=("ev:fact",),
            sensitivity=prior.sensitivity,
            owner_ref_id=prior.owner_ref_id,
            schema_version=IDEA_OCCURRENCE_SCHEMA_VERSION,
        )
        revised = revise_idea(
            prior,
            updated_at=T2,
            occurrence_ids=(occurrence.occurrence_id,),
        )
        event = history_event(
            event_id="event:occurrence:one",
            event_kind="OCCURRENCE_RECORDED",
            entity=idea_reference(revised),
            created_at=T2,
            related=(occurrence.occurrence_id,),
            prior_hash=ledger_history_event_semantic_hash(prior_event),
        )
        recorded = record_occurrence(snapshot, occurrence, revised, event, as_of=T2)
        self.assertEqual(recorded.ideas[0].state, "UNTRIAGED")
        self.assertEqual(recorded.occurrences, (occurrence,))
        changed_state = replace(revised, state="WATCHING")
        changed_event = replace(event, entity=idea_reference(changed_state))
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "recurrence cannot change"):
            record_occurrence(snapshot, occurrence, changed_state, changed_event, as_of=T2)

    def test_occurrence_before_idea_or_cross_owner_private_fails(self) -> None:
        snapshot, prior, prior_event = snapshot_with_idea()
        occurrence = IdeaOccurrence(
            occurrence_id="occurrence:early",
            idea_id=prior.idea_id,
            occurred_at=T0,
            context_summary="An impossible early recurrence.",
            source_ref_ids=("ev:origin",),
            evidence_ref_ids=(),
            sensitivity="PROJECT_INTERNAL",
            owner_ref_id=None,
            schema_version=IDEA_OCCURRENCE_SCHEMA_VERSION,
        )
        revised = revise_idea(prior, updated_at=T2, occurrence_ids=(occurrence.occurrence_id,))
        event = history_event(
            event_id="event:occurrence:early",
            event_kind="OCCURRENCE_RECORDED",
            entity=idea_reference(revised),
            created_at=T2,
            related=(occurrence.occurrence_id,),
            prior_hash=ledger_history_event_semantic_hash(prior_event),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "precede Idea creation"):
            record_occurrence(snapshot, occurrence, revised, event, as_of=T2)

        private_idea = idea_record(
            sensitivity="USER_PRIVATE",
            owner="owner:one",
        )
        private_capture = history_event(
            event_id="event:private:idea",
            event_kind="IDEA_CAPTURED",
            entity=idea_reference(private_idea),
            created_at=T1,
        )
        private_snapshot = record_idea(
            base_snapshot(),
            private_idea,
            private_capture,
            as_of=T1,
        )
        other_owner_occurrence = replace(
            occurrence,
            occurrence_id="occurrence:other-owner",
            occurred_at=T2,
            idea_id=private_idea.idea_id,
            sensitivity="USER_PRIVATE",
            owner_ref_id="owner:two",
        )
        private_revision = revise_idea(
            private_idea,
            updated_at=T2,
            occurrence_ids=(other_owner_occurrence.occurrence_id,),
        )
        private_event = history_event(
            event_id="event:occurrence:other-owner",
            event_kind="OCCURRENCE_RECORDED",
            entity=idea_reference(private_revision),
            created_at=T2,
            related=(other_owner_occurrence.occurrence_id,),
            prior_hash=ledger_history_event_semantic_hash(private_capture),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "cross-owner private"):
            record_occurrence(
                private_snapshot,
                other_owner_occurrence,
                private_revision,
                private_event,
                as_of=T2,
            )

    def test_explicit_duplicate_relation_keeps_both_entities(self) -> None:
        snapshot, prior, prior_event = snapshot_with_idea()
        revised = revise_idea(prior, updated_at=T2, relation_ids=("relation:dup",))
        relation = LedgerRelation(
            relation_id="relation:dup",
            source=idea_reference(revised),
            target=external_reference("GOAL", "goal:prior", revision=1, digest="b" * 64),
            relation_type="duplicate",
            basis_ref_ids=("ev:fact",),
            confidence=0.6,
            limitations=("Duplicate is caller-supplied and does not merge identity.",),
            created_at=T2,
            created_by_ref_id="actor:one",
            schema_version=LEDGER_RELATION_SCHEMA_VERSION,
        )
        event = history_event(
            event_id="event:relation:dup",
            event_kind="RELATION_RECORDED",
            entity=idea_reference(revised),
            created_at=T2,
            related=(relation.relation_id,),
            prior_hash=ledger_history_event_semantic_hash(prior_event),
        )
        recorded = record_relation(snapshot, relation, (revised,), (event,), as_of=T2)
        self.assertEqual(recorded.ideas[0].idea_id, prior.idea_id)
        self.assertEqual(recorded.relations, (relation,))
        self.assertIn(relation.target, recorded.external_entity_references)

    def test_relation_is_directional_non_merging_and_requires_basis(self) -> None:
        idea = idea_record()
        target = external_reference("GOAL", "goal:prior", revision=1, digest="b" * 64)
        with self.assertRaises(GoalEngineIdeaLedgerError):
            LedgerRelation(
                relation_id="relation:no-basis",
                source=idea_reference(idea),
                target=target,
                relation_type="related",
                basis_ref_ids=(),
                confidence=0.5,
                limitations=("Caller-supplied only.",),
                created_at=T2,
                created_by_ref_id="actor:one",
                schema_version=LEDGER_RELATION_SCHEMA_VERSION,
            )
        with self.assertRaises(GoalEngineIdeaLedgerError):
            LedgerRelation(
                relation_id="relation:self",
                source=target,
                target=target,
                relation_type="related",
                basis_ref_ids=("ev:fact",),
                confidence=0.5,
                limitations=("Caller-supplied only.",),
                created_at=T2,
                created_by_ref_id="actor:one",
                schema_version=LEDGER_RELATION_SCHEMA_VERSION,
            )

    def test_history_chain_requires_exact_immediate_prior_hash(self) -> None:
        snapshot, prior, _ = snapshot_with_idea()
        revised = revise_idea(
            prior,
            updated_at=T2,
            current_summary="A revised summary.",
        )
        bad_event = history_event(
            event_id="event:idea:2",
            event_kind="IDEA_REVISED",
            entity=idea_reference(revised),
            created_at=T2,
            prior_hash="f" * 64,
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "prior_event_hash"):
            replace_idea_snapshot(snapshot, prior, revised, bad_event, as_of=T2)

    def test_history_fact_human_and_policy_refs_are_disjoint(self) -> None:
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "remain disjoint"):
            history_event(
                event_id="event:bad-refs",
                event_kind="IDEA_CAPTURED",
                entity=idea_reference(idea_record()),
                created_at=T1,
                evidence_refs=("ev:one",),
                human_refs=("ev:one",),
            )

    def test_snapshot_revision_requires_exact_prior_hash(self) -> None:
        snapshot, _, _ = snapshot_with_idea()
        self.assertIs(validate_ledger_snapshot_revision(snapshot, base_snapshot()), snapshot)
        tampered = replace(
            snapshot,
            supersedes_snapshot=replace(snapshot.supersedes_snapshot, semantic_hash="f" * 64),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "semantic hash"):
            validate_ledger_snapshot_revision(tampered, base_snapshot())

    def test_snapshot_revision_is_append_only(self) -> None:
        snapshot, _, _ = snapshot_with_idea()
        trimmed = build_findings_idea_ledger_snapshot(
            snapshot_id=snapshot.snapshot_id,
            revision=snapshot.revision + 1,
            ledger_scope_id=snapshot.ledger_scope_id,
            as_of=T2,
            findings=snapshot.findings,
            ideas=snapshot.ideas,
            occurrences=snapshot.occurrences,
            relations=snapshot.relations,
            triggers=snapshot.triggers,
            reconsideration_requests=snapshot.reconsideration_requests,
            history_events=snapshot.history_events,
            evidence_snapshot=snapshot.evidence_snapshot,
            external_entity_references=snapshot.external_entity_references[:-1],
            supersedes_snapshot=LedgerSnapshotReference(
                snapshot_id=snapshot.snapshot_id,
                revision=snapshot.revision,
                semantic_hash=findings_idea_ledger_snapshot_semantic_hash(snapshot),
                schema_version=LEDGER_SNAPSHOT_REFERENCE_SCHEMA_VERSION,
            ),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "cannot remove or rewrite"):
            validate_ledger_snapshot_revision(trimmed, snapshot)


class IdeaLedgerReconsiderationTest(unittest.TestCase):
    def test_trigger_definition_and_reconsideration_do_not_reactivate(self) -> None:
        snapshot, prior, capture_event = snapshot_with_idea()
        trigger = ReconsiderationTrigger(
            trigger_id="trigger:human",
            idea_id=prior.idea_id,
            trigger_kind="HUMAN_REQUEST",
            condition_summary="A human requests a fresh evaluation.",
            required_evidence_classes=(),
            recurrence_threshold=None,
            not_before=None,
            expires_at=None,
            created_at=T2,
            created_by_ref_id="actor:one",
            schema_version=RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
        )
        with_trigger = revise_idea(prior, updated_at=T2, trigger_ids=(trigger.trigger_id,))
        trigger_event = history_event(
            event_id="event:trigger:human",
            event_kind="TRIGGER_DEFINED",
            entity=idea_reference(with_trigger),
            created_at=T2,
            related=(trigger.trigger_id,),
            prior_hash=ledger_history_event_semantic_hash(capture_event),
        )
        triggered = define_reconsideration_trigger(
            snapshot,
            trigger,
            with_trigger,
            trigger_event,
            as_of=T2,
        )
        archived = revise_idea(
            with_trigger,
            updated_at=T3,
            state="ARCHIVED_CONDITIONAL",
            policy_ref_ids=("ev:policy",),
        )
        archive_event = history_event(
            event_id="event:archive:one",
            event_kind="ARCHIVED_CONDITIONAL",
            entity=idea_reference(archived),
            created_at=T3,
            related=(trigger.trigger_id,),
            policy_refs=("ev:policy",),
            prior_hash=ledger_history_event_semantic_hash(trigger_event),
        )
        archived_snapshot = replace_idea_snapshot(
            triggered,
            with_trigger,
            archived,
            archive_event,
            as_of=T3,
        )
        request = ReconsiderationRequest(
            request_id="request:human",
            idea_id=archived.idea_id,
            idea_revision=archived.revision,
            trigger_id=trigger.trigger_id,
            as_of=T4,
            evidence_ref_ids=(),
            occurrence_ids=(),
            human_request_ref_ids=("ev:human",),
            limitations=("A fresh Necessity Test remains required.",),
            schema_version=RECONSIDERATION_REQUEST_SCHEMA_VERSION,
        )
        request_event = history_event(
            event_id="event:request:human",
            event_kind="RECONSIDERATION_REQUESTED",
            entity=idea_reference(archived),
            created_at=T4,
            related=(request.request_id,),
            human_refs=("ev:human",),
            prior_hash=ledger_history_event_semantic_hash(archive_event),
        )
        requested = build_reconsideration_request(
            archived_snapshot,
            request,
            request_event,
            as_of=T4,
        )
        self.assertEqual(requested.ideas[0], archived)
        self.assertEqual(requested.ideas[0].state, "ARCHIVED_CONDITIONAL")
        self.assertEqual(requested.reconsideration_requests, (request,))
        self.assertNotIn("goal", findings_idea_ledger_snapshot_to_dict(requested))

    def test_reconsideration_requires_archived_idea(self) -> None:
        snapshot, idea, prior_event = snapshot_with_idea()
        trigger = ReconsiderationTrigger(
            trigger_id="trigger:human",
            idea_id=idea.idea_id,
            trigger_kind="HUMAN_REQUEST",
            condition_summary="A human requests review.",
            required_evidence_classes=(),
            recurrence_threshold=None,
            not_before=None,
            expires_at=None,
            created_at=T2,
            created_by_ref_id="actor:one",
            schema_version=RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
        )
        revised = revise_idea(idea, updated_at=T2, trigger_ids=(trigger.trigger_id,))
        trigger_event = history_event(
            event_id="event:trigger:human",
            event_kind="TRIGGER_DEFINED",
            entity=idea_reference(revised),
            created_at=T2,
            related=(trigger.trigger_id,),
            prior_hash=ledger_history_event_semantic_hash(prior_event),
        )
        triggered = define_reconsideration_trigger(
            snapshot,
            trigger,
            revised,
            trigger_event,
            as_of=T2,
        )
        request = ReconsiderationRequest(
            request_id="request:bad",
            idea_id=revised.idea_id,
            idea_revision=revised.revision,
            trigger_id=trigger.trigger_id,
            as_of=T3,
            evidence_ref_ids=(),
            occurrence_ids=(),
            human_request_ref_ids=("ev:human",),
            limitations=("Fresh evaluation is still required.",),
            schema_version=RECONSIDERATION_REQUEST_SCHEMA_VERSION,
        )
        request_event = history_event(
            event_id="event:request:bad",
            event_kind="RECONSIDERATION_REQUESTED",
            entity=idea_reference(revised),
            created_at=T3,
            related=(request.request_id,),
            prior_hash=ledger_history_event_semantic_hash(trigger_event),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "ARCHIVED_CONDITIONAL"):
            build_reconsideration_request(
                triggered,
                request,
                request_event,
                as_of=T3,
            )

    def test_recurrence_threshold_does_not_auto_promote(self) -> None:
        snapshot, prior, capture_event = snapshot_with_idea()
        occurrence = IdeaOccurrence(
            occurrence_id="occurrence:one",
            idea_id=prior.idea_id,
            occurred_at=T2,
            context_summary="One recurrence was supplied.",
            source_ref_ids=("ev:origin",),
            evidence_ref_ids=(),
            sensitivity="PROJECT_INTERNAL",
            owner_ref_id=None,
            schema_version=IDEA_OCCURRENCE_SCHEMA_VERSION,
        )
        with_occurrence = revise_idea(
            prior,
            updated_at=T2,
            occurrence_ids=(occurrence.occurrence_id,),
        )
        occurrence_event = history_event(
            event_id="event:occurrence:one",
            event_kind="OCCURRENCE_RECORDED",
            entity=idea_reference(with_occurrence),
            created_at=T2,
            related=(occurrence.occurrence_id,),
            prior_hash=ledger_history_event_semantic_hash(capture_event),
        )
        occurred = record_occurrence(
            snapshot,
            occurrence,
            with_occurrence,
            occurrence_event,
            as_of=T2,
        )
        trigger = ReconsiderationTrigger(
            trigger_id="trigger:twice",
            idea_id=prior.idea_id,
            trigger_kind="RECURRENCE_THRESHOLD",
            condition_summary="Request review after two supplied occurrences.",
            required_evidence_classes=(),
            recurrence_threshold=2,
            not_before=None,
            expires_at=None,
            created_at=T3,
            created_by_ref_id="actor:one",
            schema_version=RECONSIDERATION_TRIGGER_SCHEMA_VERSION,
        )
        with_trigger = revise_idea(
            with_occurrence,
            updated_at=T3,
            trigger_ids=(trigger.trigger_id,),
        )
        trigger_event = history_event(
            event_id="event:trigger:twice",
            event_kind="TRIGGER_DEFINED",
            entity=idea_reference(with_trigger),
            created_at=T3,
            related=(trigger.trigger_id,),
            prior_hash=ledger_history_event_semantic_hash(occurrence_event),
        )
        triggered = define_reconsideration_trigger(
            occurred,
            trigger,
            with_trigger,
            trigger_event,
            as_of=T3,
        )
        archived = revise_idea(
            with_trigger,
            updated_at=T4,
            state="ARCHIVED_CONDITIONAL",
            policy_ref_ids=("ev:policy",),
        )
        archive_event = history_event(
            event_id="event:archive:threshold",
            event_kind="ARCHIVED_CONDITIONAL",
            entity=idea_reference(archived),
            created_at=T4,
            related=(trigger.trigger_id,),
            policy_refs=("ev:policy",),
            prior_hash=ledger_history_event_semantic_hash(trigger_event),
        )
        archived_snapshot = replace_idea_snapshot(
            triggered,
            with_trigger,
            archived,
            archive_event,
            as_of=T4,
        )
        request = ReconsiderationRequest(
            request_id="request:threshold",
            idea_id=archived.idea_id,
            idea_revision=archived.revision,
            trigger_id=trigger.trigger_id,
            as_of=T5,
            evidence_ref_ids=(),
            occurrence_ids=(occurrence.occurrence_id,),
            human_request_ref_ids=(),
            limitations=("Only one recurrence is present.",),
            schema_version=RECONSIDERATION_REQUEST_SCHEMA_VERSION,
        )
        request_event = history_event(
            event_id="event:request:threshold",
            event_kind="RECONSIDERATION_REQUESTED",
            entity=idea_reference(archived),
            created_at=T5,
            related=(request.request_id,),
            prior_hash=ledger_history_event_semantic_hash(archive_event),
        )
        with self.assertRaisesRegex(GoalEngineIdeaLedgerError, "recurrence threshold"):
            build_reconsideration_request(
                archived_snapshot,
                request,
                request_event,
                as_of=T5,
            )
        self.assertEqual(archived_snapshot.ideas[0].state, "ARCHIVED_CONDITIONAL")


class IdeaLedgerBoundaryTest(unittest.TestCase):
    def test_module_imports_only_standard_library_and_foundation(self) -> None:
        module_path = Path(__file__).parents[1] / "codie" / "goal_engine" / "idea_ledger.py"
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        imported_roots: set[str] = set()
        relative_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    relative_modules.add(node.module or "")
                elif node.module:
                    imported_roots.add(node.module.split(".")[0])
        self.assertLessEqual(
            imported_roots,
            {"__future__", "math", "re", "unicodedata", "collections", "dataclasses", "datetime", "typing"},
        )
        self.assertEqual(relative_modules, {"foundation"})

    def test_public_surface_contains_no_runtime_or_authority_methods(self) -> None:
        forbidden_fragments = (
            "persist",
            "save",
            "load",
            "fetch",
            "search",
            "similar",
            "embed",
            "rank",
            "prioritize",
            "schedule",
            "activate",
            "execute",
            "approve",
            "promote",
            "merge_idea",
            "create_goal",
            "stream_deck",
        )
        public_methods = set(dir(FindingsIdeaLedgerSnapshot))
        public_methods.update(dir(IdeaRecord))
        for name in public_methods:
            self.assertFalse(any(fragment in name.lower() for fragment in forbidden_fragments), name)

    def test_records_expose_no_score_rank_priority_or_action_fields(self) -> None:
        forbidden = {"score", "rank", "priority", "action", "work_order", "goal_contract"}
        for record_type in (
            LedgerFinding,
            IdeaRecord,
            IdeaOccurrence,
            LedgerRelation,
            ReconsiderationTrigger,
            ReconsiderationRequest,
            LedgerHistoryEvent,
            FindingsIdeaLedgerSnapshot,
        ):
            names = {item.name for item in fields(record_type)}
            self.assertTrue(names.isdisjoint(forbidden), record_type.__name__)


if __name__ == "__main__":
    unittest.main()
