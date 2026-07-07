from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.intelligence import (
    ChatQueryConstraint,
    ChatQueryPlanBuildError,
    ChatQueryPlannerOptions,
    ChatQueryRequest,
    ChatQuerySubject,
    build_chat_query_plan,
    chat_query_plan_to_dict,
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


def constraint(**overrides) -> ChatQueryConstraint:
    data = {
        "constraint_id": "constraint:commander",
        "constraint_type": "commander",
        "value": "Tymna the Weaver|Kraum, Ludevic's Opus",
        "required": True,
        "metadata": {"scope": "fixture"},
    }
    data.update(overrides)
    return ChatQueryConstraint(**data)


def request(**overrides) -> ChatQueryRequest:
    data = {
        "request_id": "request:1",
        "question_text": "Summarize this deck.",
        "generated_at": GENERATED_AT,
        "subject": subject(),
        "constraints": (constraint(),),
        "allowed_privacy_scopes": ("public", "local"),
        "metadata": {"channel": "test"},
    }
    data.update(overrides)
    return ChatQueryRequest(**data)


class IntelligenceQueryPlannerTest(unittest.TestCase):
    def test_deck_summary_request_creates_deck_summary_plan(self) -> None:
        plan = build_chat_query_plan(request())

        self.assertEqual(plan.question_class, "deck_summary")
        self.assertEqual([need.need_type for need in plan.evidence_needs], ["deck_memory", "evidence_input_records"])

    def test_card_evidence_request_creates_card_evidence_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Why is this card appearing in evidence?",
                subject=subject(subject_type="card", subject_key="oracle:1"),
            )
        )

        self.assertEqual(plan.question_class, "card_evidence")
        self.assertIn("build_evidence_graph", plan.allowed_operations)

    def test_commander_evidence_request_creates_commander_evidence_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show commander staples for Tymna Kraum.",
                subject=subject(subject_type="partner_pair", subject_key="tymna|kraum"),
            )
        )

        self.assertEqual(plan.question_class, "commander_evidence")
        self.assertEqual([need.need_type for need in plan.evidence_needs], ["evidence_graph", "frequency_pool"])

    def test_comparison_request_creates_comparison_plan(self) -> None:
        plan = build_chat_query_plan(request(question_text="Compare this deck against top lists."))

        self.assertEqual(plan.question_class, "comparison")
        self.assertIn("inspect_frequency_pool", plan.allowed_operations)

    def test_source_conflict_request_creates_source_conflict_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show source conflict for this deck.",
                subject=subject(subject_type="source_conflict", subject_key="conflict:1"),
            )
        )

        self.assertEqual(plan.question_class, "source_conflict")
        self.assertEqual(plan.evidence_needs[0].need_type, "source_conflicts")

    def test_unsupported_card_request_creates_unsupported_card_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show unsupported cards affecting this result.",
                subject=subject(subject_type="unsupported_card", subject_key="unsupported:1"),
            )
        )

        self.assertEqual(plan.question_class, "unsupported_card")
        self.assertEqual(plan.evidence_needs[0].need_type, "unsupported_cards")

    def test_simulation_review_request_creates_simulation_review_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="What does the simulator say about this opening hand?",
                subject=subject(subject_type="simulation_result", subject_key="simulation:1"),
            )
        )

        self.assertEqual(plan.question_class, "simulation_review")
        self.assertIn("inspect_simulation_review", plan.allowed_operations)

    def test_tag_graph_request_creates_tag_graph_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Show tag graph trends for draw engine and ramp.",
                subject=subject(subject_type="tag_graph", subject_key="tag-graph:1"),
            )
        )

        self.assertEqual(plan.question_class, "tag_graph")
        self.assertEqual(plan.evidence_needs[0].need_type, "tag_graph")

    def test_unknown_request_creates_caveated_unknown_plan(self) -> None:
        plan = build_chat_query_plan(
            request(
                question_text="Tell me something inscrutable.",
                subject=subject(subject_type="unknown", subject_key=None),
            )
        )

        self.assertEqual(plan.question_class, "unknown")
        self.assertEqual(plan.evidence_needs, ())
        self.assertEqual(plan.allowed_operations, ("return_caveated_unknown",))
        self.assertEqual(plan.caveats[0]["caveat_type"], "unknown_question")

    def test_plans_serialize_deterministically(self) -> None:
        plan = build_chat_query_plan(
            request(
                constraints=(
                    constraint(constraint_id="constraint:b", constraint_type="region", value="NA"),
                    constraint(constraint_id="constraint:a", constraint_type="date_range", value={"days": 180}),
                )
            )
        )

        payload = chat_query_plan_to_dict(plan)

        self.assertEqual([item["constraint_id"] for item in payload["constraints"]], ["constraint:a", "constraint:b"])
        json.dumps(payload, sort_keys=True)

    def test_explicit_constraints_are_preserved(self) -> None:
        plan = build_chat_query_plan(
            request(constraints=(constraint(constraint_type="region", value="Japan"),))
        )

        self.assertEqual(plan.constraints[0].constraint_type, "region")
        self.assertEqual(plan.evidence_needs[0].filters["region"], "Japan")

    def test_subject_data_is_preserved(self) -> None:
        plan = build_chat_query_plan(
            request(
                subject=subject(
                    subject_type="partner_pair",
                    subject_key="tymna|kraum",
                    display_name="Tymna/Kraum",
                    metadata={"source": "fixture", "scope": "top_16"},
                )
            )
        )

        self.assertEqual(plan.subject.subject_type, "partner_pair")
        self.assertEqual(plan.subject.subject_key, "tymna|kraum")
        self.assertEqual(plan.subject.display_name, "Tymna/Kraum")
        self.assertEqual(plan.subject.metadata["scope"], "top_16")

    def test_question_class_derives_deterministic_evidence_needs(self) -> None:
        cases = (
            ("Summarize this deck.", ("deck_memory", "evidence_input_records")),
            ("Why is this card appearing in evidence?", ("evidence_graph", "source_conflicts")),
            ("Show commander staples for Tymna Kraum.", ("evidence_graph", "frequency_pool")),
            ("Compare this deck against top lists.", ("deck_memory", "frequency_pool")),
            ("Show source conflict for this deck.", ("source_conflicts",)),
            ("Show unsupported cards affecting this result.", ("unsupported_cards",)),
            ("What does the simulator say about this opening hand?", ("simulation_review_summary", "unsupported_cards")),
            ("Show tag graph trends for draw engine and ramp.", ("tag_graph",)),
        )
        for question_text, expected_need_types in cases:
            with self.subTest(question_text=question_text):
                plan = build_chat_query_plan(request(question_text=question_text))
                self.assertEqual(tuple(need.need_type for need in plan.evidence_needs), expected_need_types)

    def test_privacy_scopes_are_enforced(self) -> None:
        plan = build_chat_query_plan(
            request(
                allowed_privacy_scopes=("public",),
            ),
            ChatQueryPlannerOptions(default_privacy_scope="local"),
        )

        self.assertEqual(plan.caveats[0]["caveat_type"], "privacy_scope_not_allowed")

    def test_sensitive_scope_blocked_by_default(self) -> None:
        plan = build_chat_query_plan(
            request(allowed_privacy_scopes=("public", "sensitive")),
            ChatQueryPlannerOptions(default_privacy_scope="sensitive"),
        )

        self.assertEqual(plan.blockers[0]["blocker_type"], "privacy_scope_blocked")

    def test_local_user_data_scope_blocked_by_default(self) -> None:
        plan = build_chat_query_plan(
            request(allowed_privacy_scopes=("public", "local_user_data")),
            ChatQueryPlannerOptions(default_privacy_scope="local_user_data"),
        )

        self.assertEqual(plan.blockers[0]["metadata"]["privacy_scope"], "local_user_data")

    def test_private_metadata_keys_fail_cleanly(self) -> None:
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
                with self.assertRaises(ChatQueryPlanBuildError):
                    request(metadata={blocked_key: "secret"})
                with self.assertRaises(ChatQueryPlanBuildError):
                    subject(metadata={blocked_key: "secret"})
                with self.assertRaises(ChatQueryPlanBuildError):
                    constraint(metadata={blocked_key: "secret"})

    def test_nested_private_metadata_keys_fail_cleanly(self) -> None:
        with self.assertRaises(ChatQueryPlanBuildError):
            request(metadata={"safe": [{"private-deck-text": "secret"}]})

    def test_too_many_evidence_needs_fail_cleanly(self) -> None:
        with self.assertRaises(ChatQueryPlanBuildError):
            build_chat_query_plan(request(), ChatQueryPlannerOptions(maximum_evidence_needs=1))

    def test_too_many_constraints_fail_cleanly(self) -> None:
        constraints = tuple(
            constraint(constraint_id=f"constraint:{index}", constraint_type="region", value=f"region-{index}")
            for index in range(13)
        )

        with self.assertRaises(ChatQueryPlanBuildError):
            build_chat_query_plan(request(constraints=constraints))

    def test_forbidden_strategic_language_fails_cleanly(self) -> None:
        with self.assertRaises(ChatQueryPlanBuildError):
            request(question_text="This card should be " + "played.")

    def test_module_has_no_forbidden_imports_raw_sql_or_file_writes(self) -> None:
        import codie.intelligence.query_planner as query_planner_module

        source = Path(query_planner_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations.generation",
            "codie." + "recommendations.persistence",
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
