from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    ChatAnswerBuildError,
    ChatAnswerBuilderOptions,
    ChatAnswerInput,
    ChatAnswerSection,
    ChatEvidenceNeed,
    ChatQueryPlan,
    ChatQueryPlannerOptions,
    ChatQueryRequest,
    ChatQuerySubject,
    EvidenceInputRecord,
    EvidenceRecordRef,
    SourceConflictEvidenceRef,
    SourceConflictItem,
    SourceConflictReport,
    UnsupportedCardEvidenceRef,
    UnsupportedCardQueue,
    UnsupportedCardQueueItem,
    build_chat_answer,
    build_chat_query_plan,
    chat_answer_to_dict,
)


GENERATED_AT = "2026-07-07T00:00:00+00:00"


def subject(**overrides) -> ChatQuerySubject:
    data = {
        "subject_type": "deck",
        "subject_key": "deck:1",
        "display_name": "Test Deck",
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return ChatQuerySubject(**data)


def request(**overrides) -> ChatQueryRequest:
    data = {
        "request_id": "request:answer",
        "question_text": "Summarize this deck.",
        "generated_at": GENERATED_AT,
        "subject": subject(),
        "constraints": (),
        "allowed_privacy_scopes": ("public", "local"),
        "metadata": {"channel": "test"},
    }
    data.update(overrides)
    return ChatQueryRequest(**data)


def evidence_record(**overrides) -> EvidenceInputRecord:
    data = {
        "record_id": "record:deck:1",
        "record_type": "deck_memory_summary",
        "label": "Deck memory summary",
        "summary": "Deck memory summary appears in sanitized evidence.",
        "confidence": 0.9,
        "references": (
            EvidenceRecordRef(
                source_type="deck_memory",
                source_name="Codie Deck Memory",
                observed_at=GENERATED_AT,
                source_record_id="deck:1",
            ),
        ),
        "caveats": (),
        "privacy_scope": "local",
        "metadata": {"scope": "fixture"},
    }
    data.update(overrides)
    return EvidenceInputRecord(**data)


def answer_input(plan: ChatQueryPlan, **overrides) -> ChatAnswerInput:
    data = {
        "answer_input_id": "answer-input:1",
        "plan": plan,
        "generated_at": GENERATED_AT,
        "evidence_records": (evidence_record(),),
        "context_summaries": {},
        "metadata": {"scope": "fixture"},
    }
    data.update(overrides)
    return ChatAnswerInput(**data)


def source_conflict_report() -> SourceConflictReport:
    ref = SourceConflictEvidenceRef(
        evidence_id="conflict-ref:1",
        source_type="canonical",
        source_name="Canonical Fixture",
        observed_at=GENERATED_AT,
        field_name="pilot_name",
        field_value="Different Pilot",
        source_record_id="canonical:1",
    )
    item = SourceConflictItem(
        conflict_id="conflict:1",
        conflict_type="source_disagreement",
        summary="Two sanitized sources disagree.",
        severity="warning",
        evidence_refs=(ref,),
    )
    return SourceConflictReport(
        report_id="source-conflict-report:1",
        subject_type="deck",
        subject_id="deck:1",
        generated_at=GENERATED_AT,
        conflicts=(item,),
    )


def unsupported_card_queue() -> UnsupportedCardQueue:
    ref = UnsupportedCardEvidenceRef(
        evidence_id="unsupported-ref:1",
        source_type="simulation",
        source_name="Simulation Fixture",
        observed_at=GENERATED_AT,
        card_name="Fixture Card",
        source_record_id="simulation:1",
    )
    item = UnsupportedCardQueueItem(
        item_id="unsupported:1",
        card_name="Fixture Card",
        reason="simulator_unsupported",
        severity="warning",
        evidence_refs=(ref,),
    )
    return UnsupportedCardQueue(
        queue_id="unsupported-queue:1",
        subject_type="deck",
        subject_id="deck:1",
        generated_at=GENERATED_AT,
        items=(item,),
    )


class IntelligenceAnswerBuilderTest(unittest.TestCase):
    def test_deck_summary_plan_builds_cited_answer_sections(self) -> None:
        plan = build_chat_query_plan(request())

        answer = build_chat_answer(answer_input(plan))

        self.assertEqual(answer.answer_mode, "deck_summary")
        self.assertTrue(answer.sections[0].citation_ids)
        self.assertEqual(answer.citations[0].source_type, "deck_memory")

    def test_card_evidence_plan_builds_cited_answer_sections(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Why is this card appearing in evidence?",
                subject=subject(subject_type="card", subject_key="oracle:1"),
            )
        )

        answer = build_chat_answer(
            answer_input(
                plan,
                evidence_records=(
                    evidence_record(
                        record_id="record:card:1",
                        record_type="recommendation_candidate",
                        label="Card evidence",
                    ),
                ),
            )
        )

        self.assertEqual(answer.answer_mode, "card_evidence")
        self.assertTrue(answer.citations)

    def test_commander_evidence_plan_builds_cited_answer_sections(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show commander staples for Tymna Kraum.",
                subject=subject(subject_type="partner_pair", subject_key="tymna|kraum"),
            )
        )

        answer = build_chat_answer(
            answer_input(
                plan,
                evidence_records=(
                    evidence_record(
                        record_id="record:commander:1",
                        record_type="manual_note",
                        label="Commander evidence",
                        references=(),
                    ),
                ),
                context_summaries={"frequency_pool": {"deck_count": 42}},
            )
        )

        self.assertEqual(answer.answer_mode, "commander_evidence")
        self.assertTrue(answer.sections[0].citation_ids)

    def test_comparison_plan_builds_cited_answer_sections(self) -> None:
        plan = build_chat_query_plan(request(question_text="Compare this deck against top lists."))

        answer = build_chat_answer(
            answer_input(plan, context_summaries={"frequency_pool": {"deck_count": 12}})
        )

        self.assertEqual(answer.sections[0].section_type, "comparison")

    def test_source_conflict_plan_preserves_conflict_caveats(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show source conflict for this deck.",
                subject=subject(subject_type="source_conflict", subject_key="conflict:1"),
            )
        )

        answer = build_chat_answer(
            answer_input(
                plan,
                evidence_records=(
                    evidence_record(
                        record_id="record:conflict:1",
                        record_type="source_conflict",
                        label="Source conflict",
                    ),
                ),
                source_conflict_report=source_conflict_report(),
            )
        )

        self.assertIn("source_conflict", [caveat.caveat_type for caveat in answer.caveats])

    def test_unsupported_card_plan_preserves_unsupported_card_warnings(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show unsupported cards affecting this result.",
                subject=subject(subject_type="unsupported_card", subject_key="unsupported:1"),
            )
        )

        answer = build_chat_answer(
            answer_input(
                plan,
                evidence_records=(
                    evidence_record(
                        record_id="record:unsupported:1",
                        record_type="unsupported_card",
                        label="Unsupported card",
                    ),
                ),
                unsupported_card_queue=unsupported_card_queue(),
            )
        )

        self.assertIn("unsupported_card", [caveat.caveat_type for caveat in answer.caveats])

    def test_simulation_review_plan_preserves_caveats_without_running_simulator(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="What does the simulator say about this opening hand?",
                subject=subject(subject_type="simulation_result", subject_key="simulation:1"),
            )
        )

        answer = build_chat_answer(
            answer_input(
                plan,
                evidence_records=(
                    evidence_record(
                        record_id="record:simulation:1",
                        record_type="simulation_review_summary",
                        label="Simulation review",
                        caveats=({"caveat_type": "unsupported_card", "message": "Unsupported card present.", "severity": "warning"},),
                    ),
                    evidence_record(
                        record_id="record:unsupported:1",
                        record_type="unsupported_card",
                        label="Unsupported card",
                    ),
                ),
            )
        )

        self.assertEqual(answer.answer_mode, "simulation_review")
        self.assertIn("unsupported_card", [caveat.caveat_type for caveat in answer.caveats])

    def test_unknown_plan_emits_caveated_unknown_answer(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Tell me something inscrutable.",
                subject=subject(subject_type="unknown", subject_key=None),
            )
        )

        answer = build_chat_answer(answer_input(plan, evidence_records=()))

        self.assertEqual(answer.answer_mode, "unknown")
        self.assertEqual(answer.sections[0].section_type, "unknown")
        self.assertIn("unknown_question", [caveat.caveat_type for caveat in answer.caveats])

    def test_tag_graph_context_summary_creates_citation(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show tag graph trends for draw engine and ramp.",
                subject=subject(subject_type="tag_graph", subject_key="tag-graph:1"),
            )
        )

        answer = build_chat_answer(
            answer_input(plan, evidence_records=(), context_summaries={"tag_graph": {"selected_tags": ["ramp"]}})
        )

        self.assertEqual(answer.answer_mode, "tag_graph")
        self.assertEqual(answer.citations[0].source_type, "tag_graph")

    def test_missing_required_evidence_creates_missing_evidence_entries(self) -> None:
        plan = build_chat_query_plan(request())

        answer = build_chat_answer(answer_input(plan, evidence_records=()))

        self.assertTrue(answer.missing_evidence)
        self.assertEqual(answer.sections[0].section_type, "missing_evidence")

    def test_missing_optional_evidence_creates_non_blocking_caveat(self) -> None:
        plan = build_chat_query_plan(request())
        optional_need = ChatEvidenceNeed(
            need_id="need:optional",
            need_type="manual_note",
            reason="Optional note.",
            required=False,
        )
        plan = ChatQueryPlan(
            plan_id=plan.plan_id,
            request_id=plan.request_id,
            question_class=plan.question_class,
            subject=plan.subject,
            evidence_needs=plan.evidence_needs + (optional_need,),
            constraints=plan.constraints,
            blockers=plan.blockers,
            caveats=plan.caveats,
            allowed_operations=plan.allowed_operations,
            generated_at=plan.generated_at,
            metadata=plan.metadata,
        )

        answer = build_chat_answer(answer_input(plan))

        optional = [item for item in answer.missing_evidence if item.need_id == "need:optional"][0]
        caveat = [item for item in answer.caveats if item.metadata.get("need_id") == "need:optional"][0]
        self.assertFalse(optional.required)
        self.assertEqual(caveat.severity, "info")

    def test_sections_without_citations_fail_unless_missing_or_unknown(self) -> None:
        with self.assertRaises(ChatAnswerBuildError):
            ChatAnswerSection(
                section_id="section:bad",
                section_type="summary",
                title="Bad Section",
                statements=("This section lacks support.",),
            )

    def test_plan_blockers_and_caveats_are_preserved(self) -> None:
        plan = build_chat_query_plan(
            request(allowed_privacy_scopes=("public", "sensitive")),
            options=ChatQueryPlannerOptions(default_privacy_scope="sensitive"),
        )

        answer = build_chat_answer(answer_input(plan, evidence_records=()))

        self.assertTrue(answer.blockers)
        self.assertEqual(answer.blockers[0]["blocker_type"], "privacy_scope_blocked")

    def test_private_metadata_keys_fail_cleanly(self) -> None:
        plan = build_chat_query_plan(request())
        blocked_keys = (
            "raw_input",
            "private_deck_text",
            "full_primer_body",
            "raw_" + "provider_payload",
            "provider_payload",
            "original_import_text",
        )
        for blocked_key in blocked_keys:
            with self.subTest(blocked_key=blocked_key):
                with self.assertRaises(ChatAnswerBuildError):
                    build_chat_answer(answer_input(plan, metadata={blocked_key: "secret"}))

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        plan = build_chat_query_plan(request())

        with self.assertRaises(ChatAnswerBuildError):
            build_chat_answer(answer_input(plan, metadata={"safe": [{"private-deck-text": "secret"}]}))

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        with self.assertRaises(ChatAnswerBuildError):
            ChatAnswerSection(
                section_id="section:bad",
                section_type="unknown",
                title="Bad Section",
                statements=("This card should " + "play a role.",),
            )

    def test_answer_serialization_is_deterministic(self) -> None:
        plan = build_chat_query_plan(request())

        payload = chat_answer_to_dict(build_chat_answer(answer_input(plan)))

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["sections"][0]["section_id"], "section:deck_summary:evidence")

    def test_module_has_no_forbidden_imports_raw_sql_or_file_writes(self) -> None:
        import codie.intelligence.answer_builder as answer_builder_module

        source = Path(answer_builder_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "codie." + "canonical",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "SEL" + "ECT ",
            "INS" + "ERT ",
            "UPD" + "ATE ",
            "DEL" + "ETE ",
            "exec" + "ute(",
            "execute" + "script(",
            "open(",
            "write_text(",
            "write_bytes(",
            "Path(",
            "mkdir(",
            "touch(",
            "unlink(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
