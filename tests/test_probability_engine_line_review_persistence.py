from __future__ import annotations

import ast
import json
import sqlite3
import unittest
from pathlib import Path

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories import SimulationRepository
from codie.probability_engine import (
    LineReviewReason,
    LineReviewStatus,
    PersistedLineReview,
    SearchConfig,
    SimulationTargetCondition,
    create_line_review_annotation,
    generate_challenge_prompt,
    line_review_annotation_to_repository_row,
    line_review_repository_row_to_annotation,
    parse_simulation_deck_rows,
    persist_line_review_annotation,
    record_challenge_answer,
    verify_challenge_answer,
)


class FailingLineReviewRepository(SimulationRepository):
    def upsert_line_review(self, review):
        raise RuntimeError("forced line review failure")


class ProbabilityEngineLineReviewPersistenceTest(unittest.TestCase):
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
            base_seed="line-review-persist-seed",
            search_config=SearchConfig(),
            generated_at="2026-06-30T00:00:00Z",
        )
        result = verify_challenge_answer(
            prompt,
            record_challenge_answer(prompt, "yes"),
            self.overlays,
            completed_at="2026-06-30T00:01:00Z",
        )
        self.annotation = create_line_review_annotation(
            result,
            LineReviewStatus.MANA_MODELING_ERROR,
            LineReviewReason.MANA_POOL_ERROR,
            review_note="Review the mana pool transition.",
            affected_cards=["Island", "Rhystic Study"],
            affected_actions=["tap_for_mana", "cast_spell"],
            created_at="2026-06-30T00:02:00Z",
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_schema_contains_line_review_table_and_indexes(self) -> None:
        tables = {
            row["name"]
            for row in self.connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
        }
        indexes = {
            row["name"]
            for row in self.connection.execute("SELECT name FROM sqlite_master WHERE type = 'index'").fetchall()
        }

        self.assertIn("simulation_line_reviews", tables)
        self.assertTrue(
            {
                "idx_simulation_line_reviews_challenge_id",
                "idx_simulation_line_reviews_deck_hash",
                "idx_simulation_line_reviews_target_card",
                "idx_simulation_line_reviews_trace_id",
                "idx_simulation_line_reviews_review_status",
            }.issubset(indexes)
        )

    def test_annotation_maps_to_repository_row(self) -> None:
        row = line_review_annotation_to_repository_row(self.annotation)

        self.assertEqual(row["review_id"], self.annotation.review_id)
        self.assertEqual(row["simulator_success"], 1)
        self.assertEqual(json.loads(row["affected_cards_json"]), ["Island", "Rhystic Study"])
        self.assertEqual(json.loads(row["affected_actions_json"]), ["tap_for_mana", "cast_spell"])

    def test_repository_upserts_line_review(self) -> None:
        persisted = persist_line_review_annotation(self.repository, self.annotation)

        self.assertIsInstance(persisted, PersistedLineReview)
        self.assertEqual(persisted.review_id, self.annotation.review_id)
        self.assertEqual(self._count("simulation_line_reviews"), 1)

    def test_repeated_upsert_does_not_duplicate_row_and_updates_metadata(self) -> None:
        persist_line_review_annotation(self.repository, self.annotation)
        updated = create_line_review_annotation(
            self._challenge_result(),
            LineReviewStatus.OTHER,
            LineReviewReason.UNKNOWN_ISSUE,
            review_note="Updated note.",
            created_at="2026-06-30T00:03:00Z",
            review_id=self.annotation.review_id,
        )
        persist_line_review_annotation(self.repository, updated)

        row = self.repository.get_line_review(self.annotation.review_id)

        self.assertEqual(self._count("simulation_line_reviews"), 1)
        self.assertEqual(row["review_status"], "other")
        self.assertEqual(row["review_note"], "Updated note.")

    def test_get_line_review_returns_stored_row(self) -> None:
        persist_line_review_annotation(self.repository, self.annotation)

        row = self.repository.get_line_review(self.annotation.review_id)

        self.assertEqual(row["review_id"], self.annotation.review_id)
        self.assertEqual(row["challenge_id"], self.annotation.challenge_id)

    def test_list_line_reviews_for_challenge_filters_by_challenge_id(self) -> None:
        persist_line_review_annotation(self.repository, self.annotation)
        other = create_line_review_annotation(
            self._challenge_result(base_seed="other-challenge"),
            LineReviewStatus.ACCEPTED,
            LineReviewReason.LINE_VALID,
            created_at="2026-06-30T00:04:00Z",
        )
        persist_line_review_annotation(self.repository, other)

        rows = self.repository.list_line_reviews_for_challenge(self.annotation.challenge_id)

        self.assertEqual([row["review_id"] for row in rows], [self.annotation.review_id])

    def test_repository_row_maps_back_to_annotation_and_json_fields_round_trip(self) -> None:
        persist_line_review_annotation(self.repository, self.annotation)
        row = self.repository.get_line_review(self.annotation.review_id)

        restored = line_review_repository_row_to_annotation(row)

        self.assertEqual(restored.review_id, self.annotation.review_id)
        self.assertEqual(restored.action_trace, self.annotation.action_trace)
        self.assertEqual(restored.affected_cards, self.annotation.affected_cards)
        self.assertEqual(restored.affected_actions, self.annotation.affected_actions)

    def test_nullable_linkage_persists(self) -> None:
        persisted = persist_line_review_annotation(self.repository, self.annotation)
        row = self.repository.get_line_review(persisted.review_id)

        self.assertIsNone(row["batch_id"])
        self.assertIsNone(row["result_id"])
        self.assertIsNone(row["trace_id"])

    def test_linked_batch_result_trace_review_persists_when_referenced_rows_exist(self) -> None:
        batch_id, result_id, trace_id = self._create_simulation_linkage()
        linked = create_line_review_annotation(
            self._challenge_result(),
            LineReviewStatus.ACCEPTED,
            LineReviewReason.LINE_VALID,
            created_at="2026-06-30T00:05:00Z",
            batch_id=batch_id,
            result_id=str(result_id),
            trace_id=str(trace_id),
        )

        persisted = persist_line_review_annotation(self.repository, linked)
        row = self.repository.get_line_review(persisted.review_id)

        self.assertEqual(row["batch_id"], batch_id)
        self.assertEqual(row["result_id"], result_id)
        self.assertEqual(row["trace_id"], trace_id)

    def test_invalid_foreign_key_fails_cleanly(self) -> None:
        linked = create_line_review_annotation(
            self._challenge_result(),
            LineReviewStatus.ACCEPTED,
            LineReviewReason.LINE_VALID,
            created_at="2026-06-30T00:05:00Z",
            batch_id="missing-batch",
        )

        with self.assertRaises(sqlite3.IntegrityError):
            persist_line_review_annotation(self.repository, linked)

    def test_missing_required_fields_fail_cleanly(self) -> None:
        row = line_review_annotation_to_repository_row(self.annotation)
        row["review_id"] = ""

        with self.assertRaises(ValueError):
            self.repository.upsert_line_review(row)

    def test_rollback_leaves_no_partial_review_after_repository_failure(self) -> None:
        failing = FailingLineReviewRepository(self.connection)

        with self.assertRaises(RuntimeError):
            persist_line_review_annotation(failing, self.annotation)

        self.assertEqual(self._count("simulation_line_reviews"), 0)

    def test_persistence_does_not_mutate_existing_trace_rows(self) -> None:
        batch_id, result_id, trace_id = self._create_simulation_linkage()
        before = self._trace_payload(trace_id)
        linked = create_line_review_annotation(
            self._challenge_result(),
            LineReviewStatus.INCORRECT,
            LineReviewReason.ILLEGAL_ACTION,
            created_at="2026-06-30T00:05:00Z",
            batch_id=batch_id,
            result_id=str(result_id),
            trace_id=str(trace_id),
        )

        persist_line_review_annotation(self.repository, linked)

        self.assertEqual(self._trace_payload(trace_id), before)

    def test_line_review_model_remains_db_free(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "line_review.py"
        text = path.read_text(encoding="utf-8")

        self.assertNotIn("codie.db", text)
        self.assertNotIn("SimulationRepository", text)

    def test_batch_search_and_challenge_modules_remain_persistence_free(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = "\n".join((root / name).read_text(encoding="utf-8") for name in ("batch.py", "search.py", "challenge_mode.py"))

        self.assertNotIn("line_review_persistence", text)
        self.assertNotIn("SimulationRepository", text)

    def test_persistence_module_import_boundary(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "line_review_persistence.py"
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

    def test_no_strategic_claim_language_in_line_review_persistence_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "line_review_persistence.py"
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

    def _challenge_result(self, *, base_seed: str = "line-review-persist-seed"):
        prompt = generate_challenge_prompt(
            self.deck,
            self.target,
            self.overlays,
            base_seed=base_seed,
            search_config=SearchConfig(),
            generated_at="2026-06-30T00:00:00Z",
        )
        return verify_challenge_answer(
            prompt,
            record_challenge_answer(prompt, "yes"),
            self.overlays,
            completed_at="2026-06-30T00:01:00Z",
        )

    def _create_simulation_linkage(self) -> tuple[str, int, int]:
        batch_id = self.repository.create_batch(
            {
                "batch_id": "batch-linked",
                "deck_hash": "deck-linked",
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
                "action_trace_json": '{"original": true}',
                "created_at": "2026-06-30T00:00:02Z",
            }
        )
        return batch_id, result_id, trace_id

    def _trace_payload(self, trace_id: int) -> str:
        return str(
            self.connection.execute(
                "SELECT action_trace_json FROM simulation_traces WHERE trace_id = ?",
                (trace_id,),
            ).fetchone()["action_trace_json"]
        )

    def _count(self, table: str) -> int:
        return int(self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


if __name__ == "__main__":
    unittest.main()
