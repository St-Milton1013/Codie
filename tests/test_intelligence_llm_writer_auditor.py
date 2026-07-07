from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    ChatAnswer,
    ChatAnswerBuildError,
    ChatAnswerCaveat,
    ChatAnswerCitation,
    ChatAnswerMissingEvidence,
    ChatAnswerSection,
    LLMAuditResult,
    LLMWriterAuditorBuildError,
    LLMWriterAuditorOptions,
    LLMWriterDraft,
    audit_writer_draft,
    build_writer_input_from_answer,
    llm_audit_result_to_dict,
    llm_writer_draft_to_dict,
    llm_writer_input_to_dict,
    validate_writer_draft,
)


GENERATED_AT = "2026-07-07T00:00:00+00:00"


def citation() -> ChatAnswerCitation:
    return ChatAnswerCitation(
        citation_id="citation:record:1",
        source_type="manual_note",
        source_id="record:1",
        record_type="manual_note",
        generated_at=GENERATED_AT,
        source_label="Sanitized note",
        confidence=0.9,
    )


def caveat() -> ChatAnswerCaveat:
    return ChatAnswerCaveat(
        caveat_id="caveat:low-evidence",
        caveat_type="low_evidence",
        message="Low sample caveat remains visible.",
        severity="warning",
    )


def missing_evidence() -> ChatAnswerMissingEvidence:
    return ChatAnswerMissingEvidence(
        missing_evidence_id="missing:regional",
        need_id="need:regional",
        need_type="manual_note",
        reason="Regional comparison evidence is unavailable.",
    )


def source_section(**overrides) -> ChatAnswerSection:
    data = {
        "section_id": "section:answer",
        "section_type": "summary",
        "title": "Evidence Summary",
        "statements": ("Sanitized evidence supports only the visible cited statement.",),
        "citation_ids": ("citation:record:1",),
        "caveat_ids": ("caveat:low-evidence",),
        "missing_evidence_ids": ("missing:regional",),
    }
    data.update(overrides)
    return ChatAnswerSection(**data)


def answer(**overrides) -> ChatAnswer:
    data = {
        "answer_id": "answer:1",
        "request_id": "request:1",
        "plan_id": "plan:1",
        "answer_mode": "deck_summary",
        "sections": (source_section(),),
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


def draft_section(**overrides) -> ChatAnswerSection:
    data = {
        "section_id": "section:draft",
        "section_type": "summary",
        "title": "Readable Evidence Summary",
        "statements": (
            "Sanitized evidence supports only the visible cited statement.",
            "Low sample caveat remains visible.",
            "Regional comparison evidence is unavailable.",
            "Manual review required.",
        ),
        "citation_ids": ("citation:record:1",),
        "caveat_ids": ("caveat:low-evidence",),
        "missing_evidence_ids": ("missing:regional",),
    }
    data.update(overrides)
    return ChatAnswerSection(**data)


def writer_input():
    return build_writer_input_from_answer(answer())


def draft(**overrides) -> LLMWriterDraft:
    source = writer_input()
    data = {
        "draft_id": "draft:1",
        "writer_input_id": source.writer_input_id,
        "answer_id": source.answer_id,
        "sections": (draft_section(),),
        "citation_ids": ("citation:record:1",),
        "caveat_ids": ("caveat:low-evidence",),
        "missing_evidence_ids": ("missing:regional",),
        "generated_at": GENERATED_AT,
        "metadata": {"writer": "mock"},
    }
    data.update(overrides)
    return LLMWriterDraft(**data)


class IntelligenceLLMWriterAuditorTest(unittest.TestCase):
    def test_writer_input_is_built_only_from_structured_answer_fields(self) -> None:
        source_answer = answer()

        built = build_writer_input_from_answer(source_answer)

        self.assertEqual(built.answer_id, source_answer.answer_id)
        self.assertEqual(built.sections, source_answer.sections)
        self.assertEqual(built.metadata["answer_metadata"], {"source": "fixture"})

    def test_writer_input_preserves_citations_caveats_missing_evidence_and_blockers(self) -> None:
        built = writer_input()

        self.assertEqual(built.citations[0].citation_id, "citation:record:1")
        self.assertEqual(built.caveats[0].caveat_id, "caveat:low-evidence")
        self.assertEqual(built.missing_evidence[0].missing_evidence_id, "missing:regional")
        self.assertEqual(built.blockers[0]["message"], "Manual review required")

    def test_local_user_data_is_blocked_by_default(self) -> None:
        with self.assertRaises(LLMWriterAuditorBuildError):
            build_writer_input_from_answer(answer(privacy_scope="local_user_data"))

    def test_sensitive_scope_is_blocked_by_default(self) -> None:
        with self.assertRaises(LLMWriterAuditorBuildError):
            build_writer_input_from_answer(answer(privacy_scope="sensitive"))

    def test_mock_writer_draft_with_supported_wording_validates_and_audits(self) -> None:
        source = writer_input()
        output = draft()

        self.assertIs(validate_writer_draft(output, source), output)
        result = audit_writer_draft(output, source)

        self.assertEqual(result.verdict, "accepted")
        self.assertFalse(result.findings)

    def test_mock_writer_draft_adding_uncited_claim_is_rejected_by_audit(self) -> None:
        source = writer_input()
        output = draft(
            sections=(
                ChatAnswerSection(
                    section_id="section:uncited",
                    section_type="unknown",
                    title="Extra",
                    statements=("This adds a new unsupported statement.",),
                ),
            ),
            citation_ids=("citation:record:1",),
            caveat_ids=("caveat:low-evidence",),
            missing_evidence_ids=("missing:regional",),
        )

        result = audit_writer_draft(output, source)

        self.assertEqual(result.verdict, "rejected")
        self.assertIn("uncited_claim", {finding.finding_type for finding in result.findings})

    def test_mock_writer_draft_hiding_caveat_is_rejected_by_audit(self) -> None:
        result = audit_writer_draft(draft(caveat_ids=()), writer_input())

        self.assertEqual(result.verdict, "rejected")
        self.assertIn("hidden_caveat", {finding.finding_type for finding in result.findings})

    def test_mock_writer_draft_hiding_missing_evidence_is_rejected_by_audit(self) -> None:
        result = audit_writer_draft(draft(missing_evidence_ids=()), writer_input())

        self.assertEqual(result.verdict, "rejected")
        self.assertIn("hidden_missing_evidence", {finding.finding_type for finding in result.findings})

    def test_mock_writer_draft_hiding_blocker_is_rejected_by_audit(self) -> None:
        output = draft(
            sections=(
                draft_section(
                    statements=(
                        "Sanitized evidence supports only the visible cited statement.",
                        "Low sample caveat remains visible.",
                        "Regional comparison evidence is unavailable.",
                    )
                ),
            )
        )

        result = audit_writer_draft(output, writer_input())

        self.assertEqual(result.verdict, "rejected")
        self.assertIn("hidden_blocker", {finding.finding_type for finding in result.findings})

    def test_mock_writer_draft_using_forbidden_strategic_language_is_rejected(self) -> None:
        bad_phrase = "you " + "should " + "play"
        with self.assertRaises((ChatAnswerBuildError, LLMWriterAuditorBuildError)):
            draft_section(statements=(f"{bad_phrase} the card.",), missing_evidence_ids=("missing:regional",))

    def test_mock_writer_draft_treating_unsupported_card_as_modeled_is_rejected(self) -> None:
        output = draft(
            sections=(
                draft_section(
                    statements=(
                        "The unsupported card behavior is modeled by this result.",
                        "Low sample caveat remains visible.",
                        "Regional comparison evidence is unavailable.",
                        "Manual review required.",
                    )
                ),
            )
        )

        result = audit_writer_draft(output, writer_input())

        self.assertEqual(result.verdict, "rejected")
        self.assertIn("unsupported_card_treated_as_modeled", {finding.finding_type for finding in result.findings})

    def test_mock_writer_draft_resolving_source_conflict_is_rejected(self) -> None:
        output = draft(
            sections=(
                draft_section(
                    statements=(
                        "The source conflict is resolved by this draft.",
                        "Low sample caveat remains visible.",
                        "Regional comparison evidence is unavailable.",
                        "Manual review required.",
                    )
                ),
            )
        )

        result = audit_writer_draft(output, writer_input())

        self.assertEqual(result.verdict, "rejected")
        self.assertIn("source_conflict_resolved", {finding.finding_type for finding in result.findings})

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
                with self.assertRaises(LLMWriterAuditorBuildError):
                    LLMWriterDraft(
                        draft_id="draft:private",
                        writer_input_id=writer_input().writer_input_id,
                        answer_id="answer:1",
                        sections=(draft_section(),),
                        generated_at=GENERATED_AT,
                        metadata={blocked_key: "secret"},
                    )

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(LLMWriterAuditorBuildError):
            LLMWriterDraft(
                draft_id="draft:nested-private",
                writer_input_id=writer_input().writer_input_id,
                answer_id="answer:1",
                sections=(draft_section(),),
                generated_at=GENERATED_AT,
                metadata={"safe": [{"private-deck-text": "secret"}]},
            )

    def test_unknown_citation_fails_cleanly(self) -> None:
        with self.assertRaises(LLMWriterAuditorBuildError):
            validate_writer_draft(draft(citation_ids=("citation:missing",)), writer_input())

    def test_options_reject_invalid_limits(self) -> None:
        with self.assertRaises(LLMWriterAuditorBuildError):
            LLMWriterAuditorOptions(maximum_sections=0)
        with self.assertRaises(LLMWriterAuditorBuildError):
            LLMWriterAuditorOptions(maximum_draft_statements=0)

    def test_audit_result_rejects_accepted_verdict_with_blocking_finding(self) -> None:
        with self.assertRaises(LLMWriterAuditorBuildError):
            LLMAuditResult(
                audit_id="audit:bad",
                draft_id="draft:1",
                writer_input_id="writer-input:answer:1",
                answer_id="answer:1",
                verdict="accepted",
                findings=(
                    audit_writer_draft(draft(caveat_ids=()), writer_input()).findings[0],
                ),
                generated_at=GENERATED_AT,
            )

    def test_serialization_is_deterministic(self) -> None:
        source = writer_input()
        output = draft()
        result = audit_writer_draft(output, source)

        payloads = (
            llm_writer_input_to_dict(source),
            llm_writer_draft_to_dict(output),
            llm_audit_result_to_dict(result),
        )

        for payload in payloads:
            json.dumps(payload, sort_keys=True)
        self.assertEqual(payloads[0]["writer_input_id"], "writer-input:answer:1")

    def test_module_has_no_forbidden_imports_raw_sql_file_writes_or_llm_calls(self) -> None:
        import codie.intelligence.llm_writer_auditor as llm_writer_auditor_module

        source = Path(llm_writer_auditor_module.__file__).read_text(encoding="utf-8")
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
