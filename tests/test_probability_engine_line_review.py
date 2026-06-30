from __future__ import annotations

import ast
import copy
import unittest
from pathlib import Path

from codie.probability_engine import (
    LineReviewReason,
    LineReviewStatus,
    SearchConfig,
    SimulationTargetCondition,
    create_line_review_annotation,
    export_line_review_fixture,
    generate_challenge_prompt,
    parse_simulation_deck_rows,
    record_challenge_answer,
    reviewed_line_counts_as_success,
    serialize_line_review_annotation,
    verify_challenge_answer,
)


class ProbabilityEngineLineReviewTest(unittest.TestCase):
    def setUp(self) -> None:
        parsed = parse_simulation_deck_rows(
            [
                {"quantity": 1, "name": "Island", "zone": "main", "model_id": "island"},
                {"quantity": 1, "name": "Rhystic Study", "zone": "main", "model_id": "rhystic_study"},
                {"quantity": 1, "name": "Memnite", "zone": "main", "model_id": "memnite"},
                {"quantity": 1, "name": "Ornithopter", "zone": "main", "model_id": "ornithopter"},
                {"quantity": 1, "name": "Sol Ring", "zone": "main", "model_id": "sol_ring"},
                {"quantity": 1, "name": "Plains", "zone": "main", "model_id": "plains"},
                {"quantity": 1, "name": "Swamp", "zone": "main", "model_id": "swamp"},
            ],
            allow_partial=True,
        )
        assert parsed.deck is not None
        self.deck = parsed.deck
        self.target = SimulationTargetCondition("Rhystic Study", "stack", 1, "cast", "rhystic_study")
        self.overlays = [
            {
                "id": "island",
                "name": "Island",
                "types": ["land"],
                "board_abilities": [{"type": "tap_for_mana", "produces": {"U": 1}}],
            },
            {
                "id": "plains",
                "name": "Plains",
                "types": ["land"],
                "board_abilities": [{"type": "tap_for_mana", "produces": {"W": 1}}],
            },
            {
                "id": "swamp",
                "name": "Swamp",
                "types": ["land"],
                "board_abilities": [{"type": "tap_for_mana", "produces": {"B": 1}}],
            },
            {"id": "rhystic_study", "name": "Rhystic Study", "types": ["enchantment"], "mana_cost": {"U": 1}},
            {"id": "memnite", "name": "Memnite", "types": ["artifact", "creature"], "mana_cost": {}},
            {"id": "ornithopter", "name": "Ornithopter", "types": ["artifact", "creature"], "mana_cost": {}},
            {"id": "sol_ring", "name": "Sol Ring", "types": ["artifact"], "mana_cost": {"Generic": 1}},
        ]
        prompt = generate_challenge_prompt(
            self.deck,
            self.target,
            self.overlays,
            base_seed="line-review-seed",
            search_config=SearchConfig(),
            generated_at="2026-06-30T00:00:00Z",
        )
        answer = record_challenge_answer(prompt, "yes", user_line_text="Island into Rhystic")
        self.result = verify_challenge_answer(prompt, answer, self.overlays, completed_at="2026-06-30T00:01:00Z")

    def test_user_can_accept_simulator_line(self) -> None:
        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.ACCEPTED,
            LineReviewReason.LINE_VALID,
            created_at="2026-06-30T00:02:00Z",
        )

        self.assertEqual(annotation.review_status, "accepted")
        self.assertEqual(annotation.review_reason, "line_valid")
        self.assertTrue(annotation.review_id.startswith("sha256:"))
        self.assertTrue(reviewed_line_counts_as_success(annotation))

    def test_user_can_veto_simulator_line_with_reason_note_and_affected_objects(self) -> None:
        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.MANA_MODELING_ERROR,
            LineReviewReason.MANA_POOL_ERROR,
            review_note="Mana pool should not retain that color through this action.",
            affected_cards=["Island", "Rhystic Study"],
            affected_actions=["tap_for_mana", "cast_spell"],
            created_at="2026-06-30T00:02:00Z",
        )

        self.assertEqual(annotation.review_status, "mana_modeling_error")
        self.assertEqual(annotation.review_note, "Mana pool should not retain that color through this action.")
        self.assertEqual(annotation.affected_cards, ("Island", "Rhystic Study"))
        self.assertEqual(annotation.affected_actions, ("tap_for_mana", "cast_spell"))
        self.assertFalse(reviewed_line_counts_as_success(annotation))

    def test_annotation_serializes_optional_source_linkage(self) -> None:
        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.BAD_SEQUENCING,
            LineReviewReason.WRONG_TIMING,
            created_at="2026-06-30T00:02:00Z",
            batch_id="batch-1",
            result_id="result-2",
            trace_id="trace-3",
        )

        payload = serialize_line_review_annotation(annotation)

        self.assertEqual(payload["batch_id"], "batch-1")
        self.assertEqual(payload["result_id"], "result-2")
        self.assertEqual(payload["trace_id"], "trace-3")

    def test_original_challenge_result_and_trace_are_unchanged(self) -> None:
        before_result = self.result.to_dict()
        before_trace = copy.deepcopy(self.result.simulator_trace)

        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.UNREALISTIC,
            LineReviewReason.IMPRACTICAL_SEQUENCE,
            created_at="2026-06-30T00:02:00Z",
        )
        annotation.action_trace["actions"] = []

        self.assertEqual(self.result.to_dict(), before_result)
        self.assertEqual(self.result.simulator_trace, before_trace)

    def test_rejected_successful_line_does_not_count_as_reviewed_success(self) -> None:
        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.INCORRECT,
            LineReviewReason.ILLEGAL_ACTION,
            created_at="2026-06-30T00:02:00Z",
        )

        self.assertFalse(reviewed_line_counts_as_success(annotation))
        self.assertTrue(self.result.simulator_success)

    def test_failed_simulator_result_counts_as_reviewed_failure(self) -> None:
        failure_result = self._failure_result()
        annotation = create_line_review_annotation(
            failure_result,
            LineReviewStatus.ACCEPTED,
            LineReviewReason.LINE_VALID,
            created_at="2026-06-30T00:02:00Z",
        )

        self.assertFalse(failure_result.simulator_success)
        self.assertFalse(reviewed_line_counts_as_success(annotation))

    def test_unsupported_line_remains_reviewed_unsupported(self) -> None:
        unsupported_result = self._unsupported_result()
        annotation = create_line_review_annotation(
            unsupported_result,
            LineReviewStatus.UNSUPPORTED_CARD_BEHAVIOR,
            LineReviewReason.UNSUPPORTED_CARD_BEHAVIOR,
            affected_cards=["Unsupported Ritual"],
            affected_actions=["choose_unmodeled_mode"],
            created_at="2026-06-30T00:02:00Z",
        )

        self.assertEqual(unsupported_result.simulator_status, "unsupported")
        self.assertIsNone(reviewed_line_counts_as_success(annotation))

    def test_rejected_line_exports_regression_fixture_without_mutation(self) -> None:
        before_result = self.result.to_dict()
        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.TUTOR_SEARCH_ERROR,
            LineReviewReason.SEARCH_ZONE_ERROR,
            affected_cards=["Rhystic Study"],
            affected_actions=["search_library"],
            created_at="2026-06-30T00:02:00Z",
        )

        fixture = export_line_review_fixture(annotation, self.result)
        payload = fixture.to_dict()

        self.assertEqual(payload["review_id"], annotation.review_id)
        self.assertEqual(payload["target_condition"]["target_card"], "Rhystic Study")
        self.assertEqual(payload["review_status"], "tutor_search_error")
        self.assertEqual(payload["affected_actions"], ["search_library"])
        self.assertEqual(self.result.to_dict(), before_result)

    def test_export_rejects_mismatched_challenge_result(self) -> None:
        annotation = create_line_review_annotation(
            self.result,
            LineReviewStatus.ACCEPTED,
            LineReviewReason.LINE_VALID,
            created_at="2026-06-30T00:02:00Z",
        )

        with self.assertRaises(ValueError):
            export_line_review_fixture(annotation, self._failure_result())

    def test_annotation_id_is_deterministic_for_identical_payload(self) -> None:
        first = create_line_review_annotation(
            self.result,
            LineReviewStatus.OTHER,
            LineReviewReason.UNKNOWN_ISSUE,
            review_note="Needs review.",
            created_at="2026-06-30T00:02:00Z",
        )
        second = create_line_review_annotation(
            self.result,
            LineReviewStatus.OTHER,
            LineReviewReason.UNKNOWN_ISSUE,
            review_note="Needs review.",
            created_at="2026-06-30T00:02:00Z",
        )

        self.assertEqual(first.review_id, second.review_id)

    def test_invalid_review_status_and_reason_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            create_line_review_annotation(self.result, "bad", LineReviewReason.LINE_VALID)
        with self.assertRaises(ValueError):
            create_line_review_annotation(self.result, LineReviewStatus.ACCEPTED, "bad")

    def test_line_review_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "line_review.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports = [
            alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        ]
        imports.extend(
            node.module
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module is not None
        )
        forbidden = {
            "codie." + "providers",
            "codie." + "db",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "sql" + "ite3",
            "req" + "uests",
            "ht" + "tpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def test_challenge_search_and_batch_modules_remain_line_review_free(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = "\n".join((root / name).read_text(encoding="utf-8") for name in ("batch.py", "search.py", "challenge_mode.py"))

        self.assertNotIn("line_review", text)
        self.assertNotIn("LineReviewAnnotation", text)

    def test_no_strategic_claim_language_in_line_review_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "line_review.py"
        text = path.read_text(encoding="utf-8").lower()
        forbidden = (
            "should " + "play",
            "must " + "include",
            "correct " + "card",
            "breaks " + "the format",
            "secretly " + "optimal",
            "cut " + "this",
            "you " + "should",
        )

        self.assertFalse([phrase for phrase in forbidden if phrase in text])

    def _failure_result(self):
        target = SimulationTargetCondition("Missing Card", "stack", 1, "cast", "missing_card")
        prompt = generate_challenge_prompt(
            self.deck,
            target,
            self.overlays,
            base_seed="line-review-failure-seed",
            search_config=SearchConfig(),
            generated_at="2026-06-30T00:00:00Z",
        )
        return verify_challenge_answer(
            prompt,
            record_challenge_answer(prompt, "no"),
            self.overlays,
            completed_at="2026-06-30T00:01:00Z",
        )

    def _unsupported_result(self):
        parsed = parse_simulation_deck_rows(
            [
                {"quantity": 1, "name": "Island", "zone": "main", "model_id": "island"},
                {"quantity": 1, "name": "Rhystic Study", "zone": "main", "model_id": "rhystic_study"},
                {"quantity": 1, "name": "Memnite", "zone": "main", "model_id": "memnite"},
                {"quantity": 1, "name": "Ornithopter", "zone": "main", "model_id": "ornithopter"},
                {"quantity": 1, "name": "Sol Ring", "zone": "main", "model_id": "sol_ring"},
                {"quantity": 1, "name": "Plains", "zone": "main", "model_id": "plains"},
                {"quantity": 1, "name": "Unsupported Ritual", "zone": "main", "model_id": "unsupported_ritual"},
            ],
            allow_partial=True,
        )
        assert parsed.deck is not None
        overlays = [
            *self.overlays,
            {
                "id": "unsupported_ritual",
                "name": "Unsupported Ritual",
                "types": ["instant"],
                "mana_cost": {"B": 1},
                "cast_actions": [{"type": "choose_unmodeled_mode"}],
            },
        ]
        target = SimulationTargetCondition("Unsupported Ritual", "stack", 1, "cast", "unsupported_ritual")
        prompt = generate_challenge_prompt(
            parsed.deck,
            target,
            overlays,
            base_seed="line-review-unsupported-seed",
            generated_at="2026-06-30T00:00:00Z",
        )
        return verify_challenge_answer(
            prompt,
            record_challenge_answer(prompt, "yes"),
            overlays,
            completed_at="2026-06-30T00:01:00Z",
        )


if __name__ == "__main__":
    unittest.main()
