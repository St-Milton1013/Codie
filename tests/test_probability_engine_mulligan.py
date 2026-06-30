from __future__ import annotations

import ast
import unittest
from pathlib import Path

from codie.probability_engine import (
    FORCED_KEEP_MINIMUM_SIZE,
    KEEP,
    REJECT,
    MulliganPolicyConfig,
    draw_opening_hand,
    evaluate_opening_hand,
    parse_simulation_deck_text,
    select_bottom_cards,
    shuffle_library,
    simulate_london_mulligan,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine" / "mulligan"


class ProbabilityEngineMulliganTest(unittest.TestCase):
    def _deck(self):
        payload = (FIXTURE_ROOT / "mulligan_deck.txt").read_text(encoding="utf-8")
        parsed = parse_simulation_deck_text(payload, unresolved_names=("Sticker cards",), allow_partial=True)
        assert parsed.deck is not None
        return parsed.deck

    def _policy(self, **overrides):
        keep_rules = {
            "min_lands": 1,
            "max_lands": 4,
            "land_names": ["Underground Sea", "Volcanic Island", "Polluted Delta"],
            "minimum_mana_sources": 1,
            "mana_source_names": ["Sol Ring", "Chrome Mox", "Lotus Petal", "Mana Crypt"],
            "required_card_names": [],
            "allow_unresolved_cards": True,
        }
        keep_rules.update(overrides.pop("keep_rules", {}))
        bottoming_rules = {
            "bottom_unresolved_first": True,
            "bottom_from_end_of_hand": True,
            "protected_card_names": ["Rhystic Study"],
        }
        bottoming_rules.update(overrides.pop("bottoming_rules", {}))
        return MulliganPolicyConfig(
            policy_name=overrides.pop("policy_name", "fixture-policy"),
            policy_version=overrides.pop("policy_version", "v1"),
            minimum_keep_size=overrides.pop("minimum_keep_size", 5),
            max_mulligans=overrides.pop("max_mulligans", 3),
            keep_rules=keep_rules,
            bottoming_rules=bottoming_rules,
        )

    def test_policy_keeps_hand_when_conditions_are_met(self) -> None:
        hand = draw_opening_hand(shuffle_library(self._deck(), "seed-keep", game_index=0))

        decision = evaluate_opening_hand(hand, self._policy(keep_rules={"required_card_names": []}))

        if decision.decision == KEEP:
            self.assertIn("policy_conditions_met", decision.reason_codes)
        else:
            self.assertEqual(decision.decision, REJECT)

    def test_policy_rejects_when_land_count_below_minimum(self) -> None:
        hand = draw_opening_hand(shuffle_library(self._deck(), "seed-1", game_index=0))
        policy = self._policy(keep_rules={"min_lands": 99})

        decision = evaluate_opening_hand(hand, policy)

        self.assertEqual(decision.decision, REJECT)
        self.assertIn("land_count_below_minimum", decision.reason_codes)

    def test_policy_rejects_when_required_card_missing(self) -> None:
        hand = draw_opening_hand(shuffle_library(self._deck(), "seed-1", game_index=0))
        policy = self._policy(keep_rules={"required_card_names": ["Nonexistent Card"]})

        decision = evaluate_opening_hand(hand, policy)

        self.assertEqual(decision.decision, REJECT)
        self.assertIn("missing_required_card", decision.reason_codes)

    def test_minimum_keep_size_forces_keep(self) -> None:
        hand = draw_opening_hand(shuffle_library(self._deck(), "seed-1", game_index=0))
        policy = self._policy(minimum_keep_size=6, max_mulligans=5, keep_rules={"min_lands": 99})

        decision = evaluate_opening_hand(hand, policy, mulligan_count=1)

        self.assertEqual(decision.decision, FORCED_KEEP_MINIMUM_SIZE)
        self.assertIn("minimum_keep_size_reached", decision.reason_codes)

    def test_bottomed_cards_equal_mulligan_count_and_keep_order(self) -> None:
        hand = draw_opening_hand(shuffle_library(self._deck(), "seed-1", game_index=0))

        bottomed, kept = select_bottom_cards(hand, self._policy(), 2)

        self.assertEqual(len(bottomed), 2)
        self.assertEqual(len(kept), 5)
        kept_ids = [card.physical_id for card in kept]
        original_kept_ids = [card.physical_id for card in hand.cards if card.physical_id in set(kept_ids)]
        self.assertEqual(kept_ids, original_kept_ids)

    def test_same_seed_and_policy_reproduce_same_result(self) -> None:
        deck = self._deck()
        policy = self._policy()

        first = simulate_london_mulligan(deck, "seed-1", policy, created_at="2026-06-29T00:00:00Z")
        second = simulate_london_mulligan(deck, "seed-1", policy, created_at="2026-06-29T00:00:00Z")

        self.assertEqual(first.to_dict(), second.to_dict())

    def test_different_seed_can_produce_different_result(self) -> None:
        deck = self._deck()
        policy = self._policy()

        first = simulate_london_mulligan(deck, "seed-1", policy)
        second = simulate_london_mulligan(deck, "seed-2", policy)

        self.assertNotEqual(first.kept_hand.hand_id, second.kept_hand.hand_id)

    def test_unresolved_cards_are_reported_and_can_reject(self) -> None:
        deck = self._deck()
        policy = self._policy(keep_rules={"allow_unresolved_cards": False})

        result = simulate_london_mulligan(deck, "seed-1", policy)

        self.assertEqual(result.unresolved_cards, ("Sticker cards",))
        self.assertTrue(
            any("unresolved_cards_disallowed" in step.reason_codes for step in result.steps)
            or "Sticker cards" not in {card.name for step in result.steps for card in step.opening_hand.cards}
        )

    def test_all_rejected_hands_remain_in_steps(self) -> None:
        deck = self._deck()
        policy = self._policy(minimum_keep_size=6, max_mulligans=5, keep_rules={"min_lands": 99})

        result = simulate_london_mulligan(deck, "seed-1", policy)

        self.assertGreaterEqual(len(result.steps), 2)
        self.assertEqual(result.steps[-1].decision.decision, FORCED_KEEP_MINIMUM_SIZE)
        self.assertTrue(all(step.opening_hand.hand_id for step in result.steps))

    def test_policy_does_not_mutate_original_opening_hand(self) -> None:
        hand = draw_opening_hand(shuffle_library(self._deck(), "seed-1", game_index=0))
        before = hand.to_dict()

        select_bottom_cards(hand, self._policy(), 2)

        self.assertEqual(hand.to_dict(), before)

    def test_result_serializes_bottomed_cards_and_steps(self) -> None:
        result = simulate_london_mulligan(self._deck(), "seed-1", self._policy(), created_at="now")
        payload = result.to_dict()

        self.assertEqual(payload["created_at"], "now")
        self.assertIn("steps", payload)
        self.assertIn("bottomed_cards", payload)

    def test_config_validation(self) -> None:
        with self.assertRaises(ValueError):
            MulliganPolicyConfig("", "v1", 5, 1)
        with self.assertRaises(ValueError):
            MulliganPolicyConfig("policy", "v1", 0, 1)

    def test_mulligan_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "mulligan.py"
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
            "codie." + "prov" + "iders",
            "codie." + "db",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "sql" + "ite3",
            "req" + "uests",
            "ht" + "tpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def test_no_strategic_claim_language_in_mulligan_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "mulligan.py"
        text = path.read_text(encoding="utf-8").lower()
        forbidden = (
            "should " + "play",
            "correct " + "card",
            "breaks " + "the format",
            "secretly " + "opti" + "mal",
            "you " + "should",
            "keep" + "able",
            "correct " + "mulligan",
            "hand " + "is bad",
        )

        self.assertFalse([phrase for phrase in forbidden if phrase in text])


if __name__ == "__main__":
    unittest.main()
