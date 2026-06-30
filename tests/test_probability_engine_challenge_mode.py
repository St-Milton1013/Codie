from __future__ import annotations

import ast
import unittest
from pathlib import Path

from codie.probability_engine import (
    SearchConfig,
    SimulationTargetCondition,
    generate_challenge_prompt,
    parse_simulation_deck_rows,
    record_challenge_answer,
    serialize_challenge_result,
    verify_challenge_answer,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine" / "challenge_mode"


class ProbabilityEngineChallengeModeTest(unittest.TestCase):
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

    def test_challenge_hand_generation_is_deterministic_from_seed(self) -> None:
        first = self._prompt()
        second = self._prompt()

        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertTrue(first.challenge_id.startswith("sha256:"))

    def test_prompt_stores_target_opening_hand_and_library_order(self) -> None:
        prompt = self._prompt()

        self.assertEqual(prompt.config.target_condition.target_card, "Rhystic Study")
        self.assertEqual(len(prompt.opening_hand.cards), 7)
        self.assertEqual(prompt.opening_hand.remaining_library_size, len(prompt.remaining_library))
        self.assertEqual(prompt.to_dict()["remaining_library_size"], len(prompt.remaining_library))

    def test_user_answer_is_recorded(self) -> None:
        prompt = self._prompt()

        answer = record_challenge_answer(prompt, "yes", user_line_text="Island into Rhystic", answered_at="now")

        self.assertEqual(answer.challenge_id, prompt.challenge_id)
        self.assertEqual(answer.user_answer, "yes")
        self.assertEqual(answer.user_line_text, "Island into Rhystic")
        with self.assertRaises(ValueError):
            record_challenge_answer(prompt, "maybe")

    def test_verification_runs_against_exact_displayed_hand(self) -> None:
        prompt = self._prompt()
        answer = record_challenge_answer(prompt, "yes")

        result = verify_challenge_answer(prompt, answer, self.overlays, completed_at="done")

        self.assertTrue(result.simulator_success)
        self.assertEqual(result.simulator_status, "success")
        self.assertEqual(tuple(result.opening_hand), tuple(card.name for card in prompt.opening_hand.cards))
        self.assertTrue(result.user_was_correct)

    def test_unreachable_hand_returns_failure_and_no_answer_is_correct(self) -> None:
        target = SimulationTargetCondition("Missing Card", "stack", 1, "cast", "missing_card")
        prompt = generate_challenge_prompt(
            self.deck,
            target,
            self.overlays,
            base_seed="challenge-seed",
            search_config=SearchConfig(),
        )
        answer = record_challenge_answer(prompt, "no")

        result = verify_challenge_answer(prompt, answer, self.overlays)

        self.assertFalse(result.simulator_success)
        self.assertEqual(result.simulator_status, "failure")
        self.assertTrue(result.user_was_correct)

    def test_unsupported_cards_and_actions_are_reported_without_marking_correctness(self) -> None:
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
        prompt = generate_challenge_prompt(parsed.deck, target, overlays, base_seed="challenge-seed")
        answer = record_challenge_answer(prompt, "yes")

        result = verify_challenge_answer(prompt, answer, overlays)

        self.assertEqual(result.simulator_status, "unsupported")
        self.assertIn("Unsupported Ritual", result.unsupported_cards)
        self.assertIn("choose_unmodeled_mode", result.unsupported_actions)
        self.assertIsNone(result.user_was_correct)

    def test_visible_unmodeled_card_is_reported_on_prompt(self) -> None:
        prompt = generate_challenge_prompt(
            self.deck,
            self.target,
            self.overlays[:-1],
            base_seed="challenge-seed",
        )

        self.assertIn("Sol Ring", prompt.unsupported_cards)

    def test_user_answer_comparison_for_yes_no_and_unknown(self) -> None:
        prompt = self._prompt()

        yes_result = verify_challenge_answer(prompt, record_challenge_answer(prompt, "yes"), self.overlays)
        no_result = verify_challenge_answer(prompt, record_challenge_answer(prompt, "no"), self.overlays)
        unknown_result = verify_challenge_answer(prompt, record_challenge_answer(prompt, "unknown"), self.overlays)

        self.assertTrue(yes_result.user_was_correct)
        self.assertFalse(no_result.user_was_correct)
        self.assertIsNone(unknown_result.user_was_correct)

    def test_serialized_result_includes_seed_config_metadata(self) -> None:
        prompt = self._prompt()
        result = verify_challenge_answer(prompt, record_challenge_answer(prompt, "yes"), self.overlays)

        payload = serialize_challenge_result(result)

        self.assertEqual(payload["base_seed"], "challenge-seed")
        self.assertEqual(payload["game_index"], 0)
        self.assertTrue(payload["derived_seed"].startswith("sha256:"))
        self.assertEqual(payload["target_condition"]["target_card"], "Rhystic Study")

    def test_fixture_file_exists_for_challenge_packet(self) -> None:
        payload = (FIXTURE_ROOT / "challenge_deck.txt").read_text(encoding="utf-8")

        self.assertIn("Rhystic Study", payload)

    def test_challenge_mode_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "challenge_mode.py"
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

    def test_batch_search_mulligan_remain_challenge_free(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = "\n".join((root / name).read_text(encoding="utf-8") for name in ("batch.py", "search.py", "mulligan.py"))

        self.assertNotIn("challenge_mode", text)
        self.assertNotIn("ChallengePrompt", text)

    def test_no_strategic_claim_language_in_challenge_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "challenge_mode.py"
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

    def _prompt(self):
        return generate_challenge_prompt(
            self.deck,
            self.target,
            self.overlays,
            base_seed="challenge-seed",
            game_index=0,
            search_config=SearchConfig(),
            generated_at="2026-06-30T00:00:00Z",
        )


if __name__ == "__main__":
    unittest.main()
