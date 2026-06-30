from __future__ import annotations

import ast
import unittest
from pathlib import Path

from codie.probability_engine import (
    ExpandedLibraryCard,
    OpeningHand,
    SearchConfig,
    SimulationTargetCondition,
    build_initial_search_state,
    find_target_access_line,
    is_target_accessed,
    load_behavior_overlay_rows,
    serialize_search_trace,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine"


class ProbabilityEngineSearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.overlays = [
            {
                "id": "island",
                "name": "Island",
                "types": ["land"],
                "board_abilities": [{"type": "tap_for_mana", "produces": {"U": 1}}],
            },
            {
                "id": "rhystic_study",
                "name": "Rhystic Study",
                "types": ["enchantment"],
                "mana_cost": {"U": 1},
            },
            {
                "id": "demonic_tutor",
                "name": "Demonic Tutor",
                "types": ["sorcery"],
                "mana_cost": {"B": 1, "Generic": 1},
                "cast_actions": [{"type": "search_library", "destination": "hand"}],
            },
            {
                "id": "unsupported_ritual",
                "name": "Unsupported Ritual",
                "types": ["instant"],
                "mana_cost": {"B": 1},
                "cast_actions": [{"type": "choose_unmodeled_mode"}],
            },
        ]
        self.target = SimulationTargetCondition(
            target_card="Rhystic Study",
            target_card_id="rhystic_study",
            target_zone="stack",
            turn=1,
            condition_type="cast",
        )

    def test_target_already_in_opening_hand_succeeds_for_access(self) -> None:
        hand = self._hand([self._card("Rhystic Study", "rhystic_study", 1)])
        target = SimulationTargetCondition("Rhystic Study", "accessible", 1, "access", "rhystic_study")

        result = find_target_access_line(hand, target, self.overlays)

        self.assertTrue(result.success)
        self.assertEqual(result.status, "success")
        self.assertEqual(result.actions_taken, 0)

    def test_target_cast_line_uses_modeled_mana_and_trace(self) -> None:
        hand = self._hand([
            self._card("Island", "island", 1),
            self._card("Rhystic Study", "rhystic_study", 2),
        ])

        result = find_target_access_line(hand, self.target, self.overlays)

        self.assertTrue(result.success)
        self.assertEqual(result.status, "success")
        self.assertEqual([action.action_type for action in result.trace.actions], ["play_land", "tap_for_mana", "cast_spell"])
        self.assertEqual(result.trace.actions[-1].source_card, "Rhystic Study")
        self.assertEqual(result.trace.actions[-1].target_status_after, "cast")

    def test_unavailable_target_fails_cleanly(self) -> None:
        hand = self._hand([self._card("Island", "island", 1)])

        result = find_target_access_line(hand, self.target, self.overlays)

        self.assertFalse(result.success)
        self.assertEqual(result.status, "failure")

    def test_unsupported_relevant_action_returns_unsupported(self) -> None:
        hand = self._hand([
            self._card("Unsupported Ritual", "unsupported_ritual", 1),
        ])
        target = SimulationTargetCondition("Unsupported Ritual", "stack", 1, "cast", "unsupported_ritual")

        result = find_target_access_line(hand, target, self.overlays)

        self.assertFalse(result.success)
        self.assertEqual(result.status, "unsupported")
        self.assertIn("Unsupported Ritual", result.unsupported_cards)
        self.assertIn("choose_unmodeled_mode", result.unsupported_actions)

    def test_unsupported_irrelevant_card_is_reported_without_blocking_success(self) -> None:
        hand = self._hand([
            self._card("Island", "island", 1),
            self._card("Rhystic Study", "rhystic_study", 2),
            self._card("Sticker cards", None, 3),
        ])

        result = find_target_access_line(hand, self.target, self.overlays)

        self.assertTrue(result.success)
        self.assertIn("Sticker cards", result.unsupported_cards)

    def test_max_actions_stops_search(self) -> None:
        hand = self._hand([
            self._card("Island", "island", 1),
            self._card("Rhystic Study", "rhystic_study", 2),
        ])

        result = find_target_access_line(hand, self.target, self.overlays, config=SearchConfig(max_actions=1))

        self.assertFalse(result.success)
        self.assertEqual(result.status, "limit_exceeded")

    def test_max_branches_stops_search(self) -> None:
        hand = self._hand([
            self._card("Island", "island", 1),
            self._card("Rhystic Study", "rhystic_study", 2),
        ])

        result = find_target_access_line(hand, self.target, self.overlays, config=SearchConfig(max_branches=1))

        self.assertFalse(result.success)
        self.assertEqual(result.status, "limit_exceeded")

    def test_deterministic_tie_breakers_produce_same_trace(self) -> None:
        hand = self._hand([
            self._card("Rhystic Study", "rhystic_study", 2),
            self._card("Island", "island", 1),
        ])

        first = find_target_access_line(hand, self.target, self.overlays)
        second = find_target_access_line(hand, self.target, self.overlays)

        self.assertEqual(first.trace.to_dict(), second.trace.to_dict())

    def test_search_library_action_can_find_target_to_hand(self) -> None:
        overlays = [
            {
                "id": "black_lotus",
                "name": "Black Lotus",
                "types": ["artifact"],
                "mana_cost": {},
                "board_abilities": [{"type": "tap_for_mana", "produces": {"B": 3}}],
            },
            *self.overlays,
        ]
        hand = self._hand([
            self._card("Black Lotus", "black_lotus", 1),
            self._card("Demonic Tutor", "demonic_tutor", 2),
        ])
        library = (self._card("Rhystic Study", "rhystic_study", 3),)
        target = SimulationTargetCondition("Rhystic Study", "hand", 1, "find_to_hand", "rhystic_study")

        result = find_target_access_line(hand, target, overlays, library=library)

        self.assertTrue(result.success)
        self.assertIn("find_to_hand", result.final_state.target_events)

    def test_build_initial_state_and_serialization(self) -> None:
        hand = self._hand([self._card("Rhystic Study", "rhystic_study", 1)])

        state = build_initial_search_state(hand, self.target, card_definitions=self.overlays)

        self.assertFalse(is_target_accessed(state, self.target))
        self.assertEqual(state.to_dict()["hand"][0]["name"], "Rhystic Study")
        self.assertEqual(serialize_search_trace(()), {"actions": []})

    def test_config_validation(self) -> None:
        with self.assertRaises(ValueError):
            SearchConfig(max_actions=0)

    def test_search_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "search.py"
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

    def test_no_strategic_claim_language_in_search_code(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = (root / "search.py").read_text(encoding="utf-8").lower()
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

    def test_fixture_file_exists_for_search_packet(self) -> None:
        payload = (FIXTURE_ROOT / "search" / "target_access_deck.txt").read_text(encoding="utf-8")

        self.assertIn("Rhystic Study", payload)

    def test_overlay_rows_load_for_search_fixtures(self) -> None:
        loaded = load_behavior_overlay_rows(self.overlays)

        self.assertEqual({card.card_id for card in loaded}, {"island", "rhystic_study", "demonic_tutor", "unsupported_ritual"})

    def _hand(self, cards: list[ExpandedLibraryCard]) -> OpeningHand:
        return OpeningHand(
            deck_hash="sha256:deck",
            base_seed="seed",
            game_index=0,
            derived_seed="sha256:" + "1" * 64,
            shuffle_algorithm_version="test",
            hand_size=len(cards),
            cards=tuple(cards),
            hand_id="sha256:" + "2" * 64,
            remaining_library_size=0,
        )

    def _card(self, name: str, model_id: str | None, index: int) -> ExpandedLibraryCard:
        return ExpandedLibraryCard(
            name=name,
            model_id=model_id,
            zone="main",
            source_quantity=1,
            copy_index=1,
            physical_id=f"sha256:{index:064d}",
        )


if __name__ == "__main__":
    unittest.main()
