from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories import SimulationRepository
from codie.probability_engine import (
    ReviewedAccuracyFilters,
    SearchConfig,
    SimulationTargetCondition,
    build_reviewed_accuracy_summary,
    create_line_review_annotation,
    generate_challenge_prompt,
    parse_simulation_deck_rows,
    persist_line_review_annotation,
    record_challenge_answer,
    summarize_line_review_rows,
    verify_challenge_answer,
)


class ProbabilityEngineReviewedAccuracyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = bootstrap_database()
        self.repository = SimulationRepository(self.connection)
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
        self.other_target = SimulationTargetCondition("Memnite", "stack", 1, "cast", "memnite")
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

    def tearDown(self) -> None:
        self.connection.close()

    def test_classifies_accepted_rejected_failed_and_unsupported_reviews(self) -> None:
        self._seed_review_rows()

        summary = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(),
            generated_at="2026-06-30T00:10:00Z",
        )

        self.assertEqual(summary.total_reviews, 5)
        self.assertEqual(summary.reviewed_success_count, 3)
        self.assertEqual(summary.accepted_success_count, 2)
        self.assertEqual(summary.rejected_success_count, 1)
        self.assertEqual(summary.reviewed_failure_count, 1)
        self.assertEqual(summary.reviewed_unsupported_count, 1)
        self.assertEqual(summary.accepted_failure_count, 1)
        self.assertEqual(summary.rejected_failure_count, 0)

    def test_counts_status_reason_affected_cards_and_actions(self) -> None:
        self._seed_review_rows()

        payload = build_reviewed_accuracy_summary(
            self.repository,
            generated_at="2026-06-30T00:10:00Z",
        ).to_dict()

        self.assertIn({"review_status": "accepted", "count": 3}, payload["status_counts"])
        self.assertIn({"review_status": "mana_modeling_error", "count": 1}, payload["status_counts"])
        self.assertIn({"review_reason": "line_valid", "count": 3}, payload["reason_counts"])
        self.assertIn({"review_reason": "mana_pool_error", "count": 1}, payload["reason_counts"])
        self.assertIn({"value": "Rhystic Study", "count": 2}, payload["affected_card_counts"])
        self.assertIn({"value": "tap_for_mana", "count": 1}, payload["affected_action_counts"])

    def test_rates_are_generated_and_empty_rates_are_none(self) -> None:
        self._seed_review_rows()

        summary = build_reviewed_accuracy_summary(self.repository, generated_at="2026-06-30T00:10:00Z")
        empty = summarize_line_review_rows([], filters=ReviewedAccuracyFilters(), generated_at="now")

        self.assertEqual(summary.accepted_success_rate, 2 / 3)
        self.assertEqual(summary.rejected_success_rate, 1 / 3)
        self.assertEqual(summary.unsupported_rate, 0.2)
        self.assertIsNone(empty.accepted_success_rate)
        self.assertIsNone(empty.rejected_success_rate)
        self.assertIsNone(empty.unsupported_rate)

    def test_filters_by_deck_hash_target_card_batch_and_challenge(self) -> None:
        annotations = self._seed_review_rows()

        by_deck = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(deck_hash=annotations[0].deck_hash),
            generated_at="now",
        )
        by_target = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(target_card="Memnite"),
            generated_at="now",
        )
        by_batch = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(batch_id="batch-reviewed"),
            generated_at="now",
        )
        by_challenge = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(challenge_id=annotations[1].challenge_id),
            generated_at="now",
        )

        self.assertEqual(by_deck.total_reviews, 4)
        self.assertEqual(by_target.total_reviews, 1)
        self.assertEqual(by_batch.total_reviews, 1)
        self.assertEqual(by_challenge.total_reviews, 1)

    def test_filters_by_status_reason_trace_and_created_at(self) -> None:
        self._seed_review_rows()

        by_status = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(review_status="accepted"),
            generated_at="now",
        )
        by_reason = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(review_reason="mana_pool_error"),
            generated_at="now",
        )
        by_trace = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(trace_id=1),
            generated_at="now",
        )
        by_time = build_reviewed_accuracy_summary(
            self.repository,
            ReviewedAccuracyFilters(created_at_from="2026-06-30T00:03:00Z", created_at_to="2026-06-30T00:04:00Z"),
            generated_at="now",
        )

        self.assertEqual(by_status.total_reviews, 3)
        self.assertEqual(by_reason.total_reviews, 1)
        self.assertEqual(by_trace.total_reviews, 1)
        self.assertEqual(by_time.total_reviews, 2)

    def test_summary_does_not_mutate_review_rows(self) -> None:
        self._seed_review_rows()
        before = self._review_rows_json()

        build_reviewed_accuracy_summary(self.repository, generated_at="now")

        self.assertEqual(self._review_rows_json(), before)

    def test_repository_query_uses_parameterized_sql(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "db" / "repositories" / "simulation.py"
        text = path.read_text(encoding="utf-8")

        self.assertIn("list_line_reviews_for_accuracy", text)
        self.assertIn("tuple(values)", text)
        self.assertNotIn("format(", text)

    def test_line_review_and_simulator_modules_remain_reviewed_accuracy_free(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = "\n".join(
            (root / name).read_text(encoding="utf-8")
            for name in ("line_review.py", "batch.py", "search.py", "challenge_mode.py")
        )

        self.assertNotIn("reviewed_accuracy", text)
        self.assertNotIn("ReviewedAccuracySummary", text)

    def test_reviewed_accuracy_import_boundary(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "reviewed_accuracy.py"
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
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "req" + "uests",
            "ht" + "tpx",
        }

        self.assertIn("codie.db.repositories.simulation", imports)
        self.assertFalse(forbidden.intersection(imports))

    def test_no_strategic_claim_language_in_reviewed_accuracy_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "reviewed_accuracy.py"
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

    def _seed_review_rows(self):
        batch_id, _result_id, trace_id = self._create_simulation_linkage()
        success = self._challenge_result("success-seed", self.target, answer="yes")
        rejected = self._challenge_result("rejected-seed", self.target, answer="yes")
        failure = self._challenge_result(
            "failure-seed",
            SimulationTargetCondition("Missing Card", "stack", 1, "cast", "missing_card"),
            answer="no",
        )
        unsupported = self._unsupported_result()
        annotations = [
            create_line_review_annotation(
                success,
                "accepted",
                "line_valid",
                affected_cards=["Rhystic Study"],
                created_at="2026-06-30T00:01:00Z",
            ),
            create_line_review_annotation(
                rejected,
                "mana_modeling_error",
                "mana_pool_error",
                affected_cards=["Rhystic Study"],
                affected_actions=["tap_for_mana"],
                created_at="2026-06-30T00:02:00Z",
                batch_id=batch_id,
                trace_id=str(trace_id),
            ),
            create_line_review_annotation(
                failure,
                "accepted",
                "line_valid",
                affected_cards=["Missing Card"],
                created_at="2026-06-30T00:03:00Z",
            ),
            create_line_review_annotation(
                unsupported,
                "unsupported_card_behavior",
                "unsupported_card_behavior",
                affected_cards=["Unsupported Ritual"],
                affected_actions=["choose_unmodeled_mode"],
                created_at="2026-06-30T00:04:00Z",
            ),
            create_line_review_annotation(
                self._challenge_result("memnite-seed", self.other_target, answer="yes"),
                "accepted",
                "line_valid",
                affected_cards=["Memnite"],
                created_at="2026-06-30T00:05:00Z",
            ),
        ]
        for annotation in annotations[:4]:
            persist_line_review_annotation(self.repository, annotation)
        persist_line_review_annotation(self.repository, annotations[4])
        return annotations

    def _challenge_result(self, seed: str, target: SimulationTargetCondition, *, answer: str):
        prompt = generate_challenge_prompt(
            self.deck,
            target,
            self.overlays,
            base_seed=seed,
            search_config=SearchConfig(),
            generated_at="2026-06-30T00:00:00Z",
        )
        return verify_challenge_answer(
            prompt,
            record_challenge_answer(prompt, answer),
            self.overlays,
            completed_at="2026-06-30T00:00:30Z",
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
        prompt = generate_challenge_prompt(parsed.deck, target, overlays, base_seed="unsupported-seed")
        return verify_challenge_answer(prompt, record_challenge_answer(prompt, "yes"), overlays)

    def _review_rows_json(self) -> str:
        rows = self.connection.execute(
            "SELECT * FROM simulation_line_reviews ORDER BY review_id"
        ).fetchall()
        payload = [dict(row) for row in rows]
        return json.dumps(payload, sort_keys=True)

    def _create_simulation_linkage(self) -> tuple[str, int, int]:
        batch_id = self.repository.create_batch(
            {
                "batch_id": "batch-reviewed",
                "deck_hash": "deck-reviewed",
                "games_requested": 1,
                "games_completed": 1,
                "min_mulligan_keep": 7,
                "mulligan_mode": "none",
                "status": "completed",
                "created_at": "2026-06-30T00:00:00Z",
                "completed_at": "2026-06-30T00:00:01Z",
                "raw_config_json": "{}",
            }
        )
        result_id = self.repository.create_result(
            {
                "batch_id": batch_id,
                "target_card": "Rhystic Study",
                "target_zone": "stack",
                "turn": 1,
                "win_count": 1,
                "win_rate": 1.0,
                "raw_payload_json": "{}",
            }
        )
        trace_id = self.repository.create_trace(
            {
                "batch_id": batch_id,
                "result_id": result_id,
                "game_index": 0,
                "success": 1,
                "mulligan_count": 0,
                "opening_hand_json": "[]",
                "final_state_json": "{}",
                "action_trace_json": "{}",
                "created_at": "2026-06-30T00:00:02Z",
            }
        )
        return batch_id, result_id, trace_id


if __name__ == "__main__":
    unittest.main()
