from __future__ import annotations

import ast
import unittest
from pathlib import Path

from codie.probability_engine import (
    BatchRunConfig,
    BatchTraceSample,
    MulliganPolicyConfig,
    SearchConfig,
    SimulationDeckCard,
    SimulationTargetCondition,
    parse_simulation_deck_rows,
    run_simulation_batch,
    run_single_simulation_game,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine" / "batch"


class ProbabilityEngineBatchTest(unittest.TestCase):
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
            {
                "id": "unsupported_ritual",
                "name": "Unsupported Ritual",
                "types": ["instant"],
                "mana_cost": {"B": 1},
                "cast_actions": [{"type": "choose_unmodeled_mode"}],
            },
        ]
        self.policy = MulliganPolicyConfig(
            policy_name="test-policy",
            policy_version="v1",
            minimum_keep_size=6,
            max_mulligans=1,
            keep_rules={"allow_unresolved_cards": True},
            bottoming_rules={"bottom_from_end_of_hand": True},
        )
        self.batch_config = BatchRunConfig(
            base_seed="batch-seed",
            games_requested=3,
            sample_successful_traces=2,
            include_failed_trace_samples=True,
            sample_failed_traces=2,
            include_unsupported_trace_samples=True,
            sample_unsupported_traces=2,
        )
        self.target = SimulationTargetCondition("Rhystic Study", "stack", 1, "cast", "rhystic_study")

    def test_batch_result_is_deterministic_for_same_seed_and_config(self) -> None:
        first = self._run(self.target)
        second = self._run(self.target)

        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.games_completed, self.batch_config.games_requested)

    def test_game_index_start_changes_derived_seeds(self) -> None:
        base = run_single_simulation_game(
            self.deck,
            self.target,
            self.overlays,
            self.policy,
            SearchConfig(),
            self.batch_config,
            game_offset=0,
        )
        shifted = run_single_simulation_game(
            self.deck,
            self.target,
            self.overlays,
            self.policy,
            SearchConfig(),
            BatchRunConfig(base_seed="batch-seed", games_requested=1, game_index_start=10),
            game_offset=0,
        )

        self.assertNotEqual(base.derived_seed, shifted.derived_seed)
        self.assertEqual(shifted.game_index, 10)

    def test_success_count_rate_and_trace_samples_are_correct(self) -> None:
        result = self._run(self.target)

        self.assertEqual(result.success_count, 3)
        self.assertEqual(result.failure_count, 0)
        self.assertEqual(result.success_rate, 1.0)
        self.assertEqual(len(result.sample_successful_traces), 2)
        self.assertEqual([sample.game_index for sample in result.sample_successful_traces], [0, 1])

    def test_failure_count_is_correct(self) -> None:
        missing = SimulationTargetCondition("Missing Card", "stack", 1, "cast", "missing_card")

        result = self._run(missing)

        self.assertEqual(result.success_count, 0)
        self.assertEqual(result.failure_count, 3)
        self.assertEqual(len(result.sample_failed_traces), 2)

    def test_unsupported_count_and_aggregation_are_correct(self) -> None:
        target = SimulationTargetCondition("Unsupported Ritual", "stack", 1, "cast", "unsupported_ritual")

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
            target,
            self.overlays,
            self.policy,
            SearchConfig(),
            self.batch_config,
        )

        self.assertEqual(result.unsupported_count, 3)
        self.assertEqual(result.unsupported_rate, 1.0)
        self.assertEqual(result.unsupported_cards, ("Unsupported Ritual",))
        self.assertEqual(result.unsupported_actions, ("choose_unmodeled_mode",))
        self.assertEqual(len(result.sample_unsupported_traces), 2)

    def test_invalid_target_count_is_correct(self) -> None:
        target = SimulationTargetCondition("Rhystic Study", "stack", 1, "not_supported", "rhystic_study")

        result = self._run(target)

        self.assertEqual(result.invalid_target_count, 3)

    def test_limit_exceeded_count_is_correct(self) -> None:
        result = run_simulation_batch(
            self.deck,
            self.target,
            self.overlays,
            self.policy,
            SearchConfig(max_actions=1),
            self.batch_config,
        )

        self.assertEqual(result.limit_exceeded_count, 3)

    def test_per_game_result_includes_opening_hand_id_and_derived_seed(self) -> None:
        result = run_single_simulation_game(
            self.deck,
            self.target,
            self.overlays,
            self.policy,
            SearchConfig(),
            self.batch_config,
        )

        self.assertTrue(result.opening_hand_id.startswith("sha256:"))
        self.assertTrue(result.derived_seed.startswith("sha256:"))
        self.assertEqual(result.to_dict()["search_status"], "success")

    def test_runner_uses_kept_hand_after_mulligan_bottoming(self) -> None:
        policy = MulliganPolicyConfig(
            policy_name="mulligan-on-land-count",
            policy_version="v1",
            minimum_keep_size=6,
            max_mulligans=1,
            keep_rules={"min_lands": 99, "land_names": ["Island", "Plains", "Swamp"]},
            bottoming_rules={"bottom_from_end_of_hand": True},
        )

        result = run_single_simulation_game(
            self.deck,
            self.target,
            self.overlays,
            policy,
            SearchConfig(),
            self.batch_config,
        )

        self.assertEqual(result.mulligan_count, 1)
        self.assertEqual(len(result.kept_hand), 6)
        self.assertEqual(len(result.bottomed_cards), 1)

    def test_average_mulligan_count_is_calculated(self) -> None:
        result = self._run(self.target)

        self.assertEqual(result.average_mulligan_count, 0.0)

    def test_batch_config_validation(self) -> None:
        with self.assertRaises(ValueError):
            BatchRunConfig(games_requested=0)
        with self.assertRaises(ValueError):
            BatchRunConfig(base_seed="")
        with self.assertRaises(ValueError):
            BatchRunConfig(sample_successful_traces=-1)

    def test_trace_sample_validation_and_serialization(self) -> None:
        sample = BatchTraceSample(game_index=0, search_status="success", success=True, trace={"actions": []})

        self.assertEqual(sample.to_dict()["trace"], {"actions": []})
        with self.assertRaises(ValueError):
            BatchTraceSample(game_index=0, search_status="weird", success=False, trace={})

    def test_fixture_file_exists_for_batch_packet(self) -> None:
        payload = (FIXTURE_ROOT / "batch_deck.txt").read_text(encoding="utf-8")

        self.assertIn("Rhystic Study", payload)

    def test_batch_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "batch.py"
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
            "sql" + "ite3",
            "req" + "uests",
            "ht" + "tpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def test_no_strategic_claim_language_in_batch_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "batch.py"
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

    def _run(self, target: SimulationTargetCondition):
        return run_simulation_batch(
            self.deck,
            target,
            self.overlays,
            self.policy,
            SearchConfig(),
            self.batch_config,
            generated_at="2026-06-30T00:00:00Z",
        )


if __name__ == "__main__":
    unittest.main()
