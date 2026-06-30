from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path
from typing import Any

from codie.db.bootstrap import bootstrap_database
from codie.db.repositories import SimulationRepository
from codie.probability_engine import (
    BatchRunConfig,
    MulliganPolicyConfig,
    PersistedSimulationBatch,
    SearchConfig,
    SimulationTargetCondition,
    batch_result_to_repository_rows,
    deterministic_batch_id,
    parse_simulation_deck_rows,
    persist_batch_run_result,
    run_simulation_batch,
)


class FailingResultRepository(SimulationRepository):
    def create_result(self, result):
        raise RuntimeError("forced result failure")


class FailingTraceRepository(SimulationRepository):
    def create_trace(self, trace):
        raise RuntimeError("forced trace failure")


class ProbabilityEnginePersistenceTest(unittest.TestCase):
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
        self.policy = MulliganPolicyConfig(
            policy_name="test-policy",
            policy_version="v1",
            minimum_keep_size=6,
            max_mulligans=1,
            keep_rules={"allow_unresolved_cards": True},
        )
        self.batch_config = BatchRunConfig(
            base_seed="persist-seed",
            games_requested=2,
            sample_successful_traces=2,
            include_failed_trace_samples=True,
            sample_failed_traces=1,
        )
        self.batch_result = run_simulation_batch(
            self.deck,
            self.target,
            self.overlays,
            self.policy,
            SearchConfig(),
            self.batch_config,
            generated_at="2026-06-30T00:00:00Z",
        )

    def tearDown(self) -> None:
        self.connection.close()

    def test_row_mapping_preserves_seed_version_and_counts(self) -> None:
        rows = batch_result_to_repository_rows(
            self.batch_result,
            created_at="2026-06-30T00:00:00Z",
            completed_at="2026-06-30T00:00:01Z",
        )

        raw_config = json.loads(rows["batch"]["raw_config_json"])
        raw_payload = json.loads(rows["result"]["raw_payload_json"])
        self.assertEqual(raw_config["base_seed"], "persist-seed")
        self.assertEqual(raw_config["search_config"]["search_version"], "codie-target-search-v1")
        self.assertEqual(raw_payload["success_count"], self.batch_result.success_count)
        self.assertEqual(rows["result"]["win_count"], self.batch_result.success_count)

    def test_persisted_batch_creates_batch_result_and_trace_rows(self) -> None:
        persisted = persist_batch_run_result(
            self.repository,
            self.batch_result,
            created_at="2026-06-30T00:00:00Z",
            completed_at="2026-06-30T00:00:01Z",
        )

        self.assertIsInstance(persisted, PersistedSimulationBatch)
        self.assertTrue(persisted.batch_id.startswith("sha256:"))
        self.assertEqual(len(persisted.trace_ids), 2)
        self.assertEqual(self._count("simulation_batches"), 1)
        self.assertEqual(self._count("simulation_batch_results"), 1)
        self.assertEqual(self._count("simulation_traces"), 2)

    def test_unsupported_cards_and_actions_are_preserved(self) -> None:
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
        result = run_simulation_batch(
            parsed.deck,
            SimulationTargetCondition("Unsupported Ritual", "stack", 1, "cast", "unsupported_ritual"),
            [
                *self.overlays,
                {
                    "id": "unsupported_ritual",
                    "name": "Unsupported Ritual",
                    "types": ["instant"],
                    "mana_cost": {"B": 1},
                    "cast_actions": [{"type": "choose_unmodeled_mode"}],
                },
            ],
            self.policy,
            SearchConfig(),
            self.batch_config,
        )
        persisted = persist_batch_run_result(
            self.repository,
            result,
            created_at="2026-06-30T00:00:00Z",
            completed_at="2026-06-30T00:00:01Z",
        )

        row = self._fetch_result(persisted.result_id)
        payload = json.loads(row["missing_cards_json"])
        self.assertEqual(payload["unsupported_cards"], ["Unsupported Ritual"])
        self.assertEqual(payload["unsupported_actions"], ["choose_unmodeled_mode"])

    def test_deterministic_batch_id_is_stable(self) -> None:
        first = deterministic_batch_id(self.batch_result, generated_at="same")
        second = deterministic_batch_id(self.batch_result, generated_at="same")

        self.assertEqual(first, second)
        self.assertTrue(first.startswith("sha256:"))

    def test_result_failure_rolls_back_batch(self) -> None:
        failing = FailingResultRepository(self.connection)

        with self.assertRaises(RuntimeError):
            persist_batch_run_result(
                failing,
                self.batch_result,
                created_at="2026-06-30T00:00:00Z",
                completed_at="2026-06-30T00:00:01Z",
            )

        self.assertEqual(self._count("simulation_batches"), 0)
        self.assertEqual(self._count("simulation_batch_results"), 0)
        self.assertEqual(self._count("simulation_traces"), 0)

    def test_trace_failure_rolls_back_batch_and_result(self) -> None:
        failing = FailingTraceRepository(self.connection)

        with self.assertRaises(RuntimeError):
            persist_batch_run_result(
                failing,
                self.batch_result,
                created_at="2026-06-30T00:00:00Z",
                completed_at="2026-06-30T00:00:01Z",
            )

        self.assertEqual(self._count("simulation_batches"), 0)
        self.assertEqual(self._count("simulation_batch_results"), 0)
        self.assertEqual(self._count("simulation_traces"), 0)

    def test_no_evidence_or_recommendation_rows_are_written(self) -> None:
        persist_batch_run_result(
            self.repository,
            self.batch_result,
            created_at="2026-06-30T00:00:00Z",
            completed_at="2026-06-30T00:00:01Z",
        )

        self.assertEqual(self._count("evidence_counts"), 0)
        self.assertEqual(self._count("recommendation_runs"), 0)
        self.assertEqual(self._count("recommendation_candidates"), 0)

    def test_batch_runner_remains_db_free(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "batch.py"
        text = path.read_text(encoding="utf-8")

        self.assertNotIn("codie.db", text)
        self.assertNotIn("SimulationRepository", text)

    def test_persistence_module_import_boundary(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "persistence.py"
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

    def test_no_strategic_claim_language_in_persistence_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "persistence.py"
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

    def _count(self, table: str) -> int:
        return int(self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])

    def _fetch_result(self, result_id: int) -> Any:
        return self.connection.execute(
            "SELECT * FROM simulation_batch_results WHERE result_id = ?",
            (result_id,),
        ).fetchone()


if __name__ == "__main__":
    unittest.main()
