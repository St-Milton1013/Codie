from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    ChatAnswer,
    ChatAnswerCaveat,
    ChatAnswerCitation,
    ChatAnswerMissingEvidence,
    ChatAnswerSection,
    ChatEvidenceNeed,
    ChatQueryPlan,
    ChatQueryRequest,
    ChatQuerySubject,
    ChatUIBoundaryBuildError,
    ChatUIBoundaryOptions,
    ChatUIErrorPacket,
    ChatUIRequestPacket,
    audit_writer_draft,
    build_chat_ui_error_packet,
    build_chat_ui_request_packet,
    build_chat_ui_response_packet,
    build_writer_input_from_answer,
    chat_ui_error_packet_to_dict,
    chat_ui_request_packet_to_dict,
    chat_ui_response_packet_to_dict,
)
from codie.intelligence.llm_writer_auditor import LLMWriterDraft


GENERATED_AT = "2026-07-07T00:00:00+00:00"


def subject() -> ChatQuerySubject:
    return ChatQuerySubject(
        subject_type="deck",
        subject_key="deck:fixture",
        display_name="Fixture Deck",
        metadata={"source": "fixture"},
    )


def request(**overrides) -> ChatQueryRequest:
    data = {
        "request_id": "request:ui",
        "question_text": "Summarize this deck.",
        "generated_at": GENERATED_AT,
        "subject": subject(),
        "constraints": (),
        "allowed_privacy_scopes": ("public",),
        "metadata": {"channel": "test"},
    }
    data.update(overrides)
    return ChatQueryRequest(**data)


def plan(**overrides) -> ChatQueryPlan:
    data = {
        "plan_id": "plan:ui",
        "request_id": "request:ui",
        "question_class": "deck_summary",
        "subject": subject(),
        "evidence_needs": (
            ChatEvidenceNeed(
                need_id="need:deck",
                need_type="deck_memory",
                reason="Deck memory summary is needed.",
            ),
        ),
        "constraints": (),
        "blockers": (),
        "caveats": (),
        "allowed_operations": ("inspect_deck_memory",),
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return ChatQueryPlan(**data)


def citation() -> ChatAnswerCitation:
    return ChatAnswerCitation(
        citation_id="citation:deck",
        source_type="deck_memory",
        source_id="deck:fixture",
        record_type="deck_memory_summary",
        generated_at=GENERATED_AT,
        source_label="Deck memory summary",
        confidence=0.9,
    )


def caveat() -> ChatAnswerCaveat:
    return ChatAnswerCaveat(
        caveat_id="caveat:sample",
        caveat_type="low_evidence",
        message="Low sample caveat remains visible.",
        severity="warning",
    )


def missing_evidence() -> ChatAnswerMissingEvidence:
    return ChatAnswerMissingEvidence(
        missing_evidence_id="missing:regional",
        need_id="need:regional",
        need_type="manual_note",
        reason="Regional evidence is unavailable.",
    )


def answer_section(**overrides) -> ChatAnswerSection:
    data = {
        "section_id": "section:answer",
        "section_type": "summary",
        "title": "Evidence Summary",
        "statements": ("Sanitized evidence supports this summary.",),
        "citation_ids": ("citation:deck",),
        "caveat_ids": ("caveat:sample",),
        "missing_evidence_ids": ("missing:regional",),
    }
    data.update(overrides)
    return ChatAnswerSection(**data)


def answer(**overrides) -> ChatAnswer:
    data = {
        "answer_id": "answer:ui",
        "request_id": "request:ui",
        "plan_id": "plan:ui",
        "answer_mode": "deck_summary",
        "sections": (answer_section(),),
        "citations": (citation(),),
        "caveats": (caveat(),),
        "blockers": ({"message": "Manual review required"},),
        "missing_evidence": (missing_evidence(),),
        "privacy_scope": "public",
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return ChatAnswer(**data)


def request_packet(**overrides) -> ChatUIRequestPacket:
    data = {
        "request_packet_id": "chat-ui-request:request:ui",
        "request_id": "request:ui",
        "question_text": "Summarize this deck.",
        "subject": subject(),
        "constraints": (),
        "allowed_privacy_scopes": ("public",),
        "requested_answer_mode": "deck_summary",
        "client_surface": "test_fixture",
        "generated_at": GENERATED_AT,
        "metadata": {"source": "fixture"},
    }
    data.update(overrides)
    return ChatUIRequestPacket(**data)


def accepted_writer_packets():
    source_answer = answer()
    writer_input = build_writer_input_from_answer(source_answer)
    writer_draft = LLMWriterDraft(
        draft_id="draft:ui",
        writer_input_id=writer_input.writer_input_id,
        answer_id=source_answer.answer_id,
        sections=(
            ChatAnswerSection(
                section_id="section:draft",
                section_type="summary",
                title="Readable Summary",
                statements=(
                    "Sanitized evidence supports this summary.",
                    "Low sample caveat remains visible.",
                    "Regional evidence is unavailable.",
                    "Manual review required.",
                ),
                citation_ids=("citation:deck",),
                caveat_ids=("caveat:sample",),
                missing_evidence_ids=("missing:regional",),
            ),
        ),
        citation_ids=("citation:deck",),
        caveat_ids=("caveat:sample",),
        missing_evidence_ids=("missing:regional",),
        generated_at=GENERATED_AT,
    )
    return writer_input, writer_draft, audit_writer_draft(writer_draft, writer_input)


class IntelligenceUIAPIBoundaryTest(unittest.TestCase):
    def test_valid_request_packet_serializes_deterministically(self) -> None:
        packet = build_chat_ui_request_packet(request(), "test_fixture", "deck_summary")

        payload = chat_ui_request_packet_to_dict(packet)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["client_surface"], "test_fixture")
        self.assertEqual(payload["requested_answer_mode"], "deck_summary")

    def test_valid_response_packet_preserves_answer_citations(self) -> None:
        packet = build_chat_ui_response_packet(request_packet(), plan(), answer())

        self.assertEqual(packet.citations[0].citation_id, "citation:deck")

    def test_valid_response_packet_preserves_caveats_missing_evidence_and_blockers(self) -> None:
        packet = build_chat_ui_response_packet(request_packet(), plan(), answer())

        self.assertEqual(packet.caveats[0].caveat_id, "caveat:sample")
        self.assertEqual(packet.missing_evidence[0].missing_evidence_id, "missing:regional")
        self.assertEqual(packet.blockers[0]["message"], "Manual review required")

    def test_local_user_data_is_blocked_by_default(self) -> None:
        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_request_packet(request(allowed_privacy_scopes=("local_user_data",)), "test_fixture")

    def test_sensitive_scope_is_blocked_by_default(self) -> None:
        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_response_packet(request_packet(), plan(), answer(privacy_scope="sensitive"))

    def test_writer_draft_is_blocked_by_default(self) -> None:
        writer_input, writer_draft, audit_result = accepted_writer_packets()

        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_response_packet(request_packet(), plan(), answer(), writer_input, writer_draft, audit_result)

    def test_accepted_audited_writer_draft_is_allowed_when_enabled(self) -> None:
        writer_input, writer_draft, audit_result = accepted_writer_packets()

        packet = build_chat_ui_response_packet(
            request_packet(),
            plan(),
            answer(),
            writer_input,
            writer_draft,
            audit_result,
            options=ChatUIBoundaryOptions(allow_writer_draft=True),
        )

        self.assertEqual(packet.audit_result.verdict, "accepted")

    def test_rejected_audited_writer_draft_fails_cleanly(self) -> None:
        writer_input, writer_draft, _ = accepted_writer_packets()
        rejected = audit_writer_draft(
            LLMWriterDraft(
                draft_id="draft:bad",
                writer_input_id=writer_input.writer_input_id,
                answer_id=writer_input.answer_id,
                sections=writer_draft.sections,
                citation_ids=("citation:deck",),
                caveat_ids=(),
                missing_evidence_ids=("missing:regional",),
                generated_at=GENERATED_AT,
            ),
            writer_input,
        )

        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_response_packet(
                request_packet(),
                plan(),
                answer(),
                writer_input,
                writer_draft,
                rejected,
                options=ChatUIBoundaryOptions(allow_writer_draft=True),
            )

    def test_unaudited_writer_draft_fails_cleanly(self) -> None:
        writer_input, writer_draft, _ = accepted_writer_packets()

        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_response_packet(
                request_packet(),
                plan(),
                answer(),
                writer_input,
                writer_draft,
                None,
                options=ChatUIBoundaryOptions(allow_writer_draft=True),
            )

    def test_private_metadata_keys_fail_cleanly(self) -> None:
        blocked_keys = (
            "raw_" + "input",
            "private_" + "deck_text",
            "full_" + "primer_body",
            "raw_" + "provider_payload",
            "provider_" + "payload",
            "original_" + "import_text",
        )
        for blocked_key in blocked_keys:
            with self.subTest(blocked_key=blocked_key):
                with self.assertRaises(ChatUIBoundaryBuildError):
                    request_packet(metadata={blocked_key: "secret"})

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(ChatUIBoundaryBuildError):
            request_packet(metadata={"safe": [{"private-deck-text": "secret"}]})

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        bad_phrase = "you " + "should " + "play"

        with self.assertRaises(ChatUIBoundaryBuildError):
            ChatUIErrorPacket(
                error_packet_id="error:bad",
                request_packet_id="packet:1",
                request_id="request:ui",
                error_type="validation_error",
                message=f"{bad_phrase} this card.",
                retryable=False,
                generated_at=GENERATED_AT,
            )

    def test_error_packet_does_not_expose_stack_trace_by_default(self) -> None:
        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_error_packet(
                request_packet(),
                "internal_error",
                "Internal error.",
                metadata={"stack-trace": "secret"},
            )

    def test_unknown_client_surface_fails_cleanly(self) -> None:
        with self.assertRaises(ChatUIBoundaryBuildError):
            build_chat_ui_request_packet(request(), "browser")

    def test_response_serialization_is_deterministic(self) -> None:
        packet = build_chat_ui_response_packet(request_packet(), plan(), answer())

        payload = chat_ui_response_packet_to_dict(packet)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["answer"]["answer_id"], "answer:ui")

    def test_error_serialization_is_deterministic(self) -> None:
        packet = build_chat_ui_error_packet(request_packet(), "missing_evidence", "Evidence unavailable.")

        payload = chat_ui_error_packet_to_dict(packet)

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["error_type"], "missing_evidence")

    def test_options_reject_invalid_limits(self) -> None:
        with self.assertRaises(ChatUIBoundaryBuildError):
            ChatUIBoundaryOptions(maximum_question_length=0)
        with self.assertRaises(ChatUIBoundaryBuildError):
            ChatUIBoundaryOptions(maximum_constraints=0)

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_or_llm_calls(self) -> None:
        import codie.intelligence.ui_api_boundary as ui_api_boundary_module

        source = Path(ui_api_boundary_module.__file__).read_text(encoding="utf-8")
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
            "open" + "ai",
            "anth" + "ropic",
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
