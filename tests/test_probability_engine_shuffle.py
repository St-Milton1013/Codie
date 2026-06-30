from __future__ import annotations

import ast
import random
import unittest
from pathlib import Path

from codie.probability_engine import (
    ExpandedLibraryCard,
    OpeningHand,
    SimulationDeckCard,
    derive_game_seed,
    draw_opening_hand,
    expand_library,
    opening_hand_id,
    parse_simulation_deck_text,
    shuffle_library,
    stable_deck_hash,
)


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "probability_engine" / "shuffle"


class ProbabilityEngineShuffleTest(unittest.TestCase):
    def _deck(self):
        payload = (FIXTURE_ROOT / "opening_hand_deck.txt").read_text(encoding="utf-8")
        parsed = parse_simulation_deck_text(
            payload,
            unresolved_names=("Sticker cards",),
            allow_partial=True,
        )
        assert parsed.deck is not None
        return parsed.deck

    def test_library_expansion_repeats_cards_by_quantity(self) -> None:
        deck_hash = stable_deck_hash((SimulationDeckCard(quantity=2, name="Sol Ring", model_id="sol_ring"),))
        parsed = parse_simulation_deck_text(
            "2 Sol Ring\n1 Rhystic Study",
            allow_partial=True,
        )
        assert parsed.deck is not None

        library = expand_library(parsed.deck)

        self.assertEqual(library.cards_total, 3)
        self.assertEqual([card.copy_index for card in library.cards if card.name == "Sol Ring"], [1, 2])
        self.assertTrue(deck_hash.startswith("sha256:"))

    def test_commanders_are_excluded_from_library(self) -> None:
        deck = self._deck()

        library = expand_library(deck)

        self.assertNotIn("Tymna the Weaver", {card.name for card in library.cards})
        self.assertNotIn("Kraum, Ludevic's Opus", {card.name for card in library.cards})

    def test_unresolved_main_deck_cards_remain_and_are_reported(self) -> None:
        deck = self._deck()

        library = expand_library(deck)
        shuffle_result = shuffle_library(deck, "seed-1")
        hand = draw_opening_hand(shuffle_result, hand_size=7)

        self.assertIn("Sticker cards", {card.name for card in library.cards})
        self.assertEqual(library.unresolved_cards, ("Sticker cards",))
        self.assertEqual(hand.unresolved_cards, ("Sticker cards",))

    def test_same_seed_and_game_index_produce_same_order(self) -> None:
        deck = self._deck()

        first = shuffle_library(deck, "seed-1", game_index=4)
        second = shuffle_library(deck, "seed-1", game_index=4)

        self.assertEqual([card.physical_id for card in first.shuffled_cards], [card.physical_id for card in second.shuffled_cards])
        self.assertEqual(first.derived_seed, second.derived_seed)

    def test_different_game_index_or_seed_can_change_order(self) -> None:
        deck = self._deck()

        base = shuffle_library(deck, "seed-1", game_index=0)
        different_index = shuffle_library(deck, "seed-1", game_index=1)
        different_seed = shuffle_library(deck, "seed-2", game_index=0)

        self.assertNotEqual([card.physical_id for card in base.shuffled_cards], [card.physical_id for card in different_index.shuffled_cards])
        self.assertNotEqual([card.physical_id for card in base.shuffled_cards], [card.physical_id for card in different_seed.shuffled_cards])

    def test_opening_hand_draws_first_seven_cards(self) -> None:
        deck = self._deck()
        shuffle_result = shuffle_library(deck, "seed-1")

        hand = draw_opening_hand(shuffle_result)

        self.assertEqual(hand.cards, shuffle_result.shuffled_cards[:7])
        self.assertEqual(hand.hand_size, 7)
        self.assertEqual(hand.remaining_library_size, shuffle_result.library_size - 7)

    def test_opening_hand_rejects_invalid_size(self) -> None:
        deck = self._deck()
        shuffle_result = shuffle_library(deck, "seed-1")

        with self.assertRaises(ValueError):
            draw_opening_hand(shuffle_result, hand_size=0)
        with self.assertRaises(ValueError):
            draw_opening_hand(shuffle_result, hand_size=shuffle_result.library_size + 1)

    def test_opening_hand_id_is_deterministic_and_order_sensitive(self) -> None:
        deck = self._deck()
        shuffle_result = shuffle_library(deck, "seed-1")
        hand = draw_opening_hand(shuffle_result)
        reordered = OpeningHand(
            deck_hash=hand.deck_hash,
            base_seed=hand.base_seed,
            game_index=hand.game_index,
            derived_seed=hand.derived_seed,
            shuffle_algorithm_version=hand.shuffle_algorithm_version,
            hand_size=hand.hand_size,
            cards=tuple(reversed(hand.cards)),
            hand_id="sha256:temporary",
            remaining_library_size=hand.remaining_library_size,
            unresolved_cards=hand.unresolved_cards,
        )

        self.assertEqual(opening_hand_id(hand), hand.hand_id)
        self.assertNotEqual(opening_hand_id(hand), opening_hand_id(reordered))

    def test_shuffle_does_not_mutate_original_deck(self) -> None:
        deck = self._deck()
        before = deck.to_dict()

        shuffle_library(deck, "seed-1")

        self.assertEqual(deck.to_dict(), before)

    def test_derive_game_seed_validates_inputs(self) -> None:
        deck = self._deck()

        self.assertTrue(derive_game_seed(deck.deck_hash, "seed-1").startswith("sha256:"))
        with self.assertRaises(ValueError):
            derive_game_seed(deck.deck_hash, "", 0)
        with self.assertRaises(ValueError):
            derive_game_seed(deck.deck_hash, "seed-1", -1)

    def test_shuffle_uses_no_global_random_seed(self) -> None:
        calls: list[object] = []
        original_seed = random.seed
        try:
            random.seed = lambda *args, **kwargs: calls.append((args, kwargs))  # type: ignore[assignment]
            shuffle_library(self._deck(), "seed-1")
        finally:
            random.seed = original_seed  # type: ignore[assignment]

        self.assertEqual(calls, [])

    def test_card_serialization_and_validation(self) -> None:
        card = ExpandedLibraryCard(
            name="Sol Ring",
            model_id="sol_ring",
            zone="main",
            source_quantity=1,
            copy_index=1,
            physical_id="sha256:test",
        )

        self.assertEqual(card.to_dict()["name"], "Sol Ring")
        with self.assertRaises(ValueError):
            ExpandedLibraryCard("", None, "main", 1, 1, "sha256:test")

    def test_shuffle_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "shuffle.py"
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

    def test_no_strategic_claim_language_in_shuffle_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "shuffle.py"
        text = path.read_text(encoding="utf-8").lower()
        forbidden = (
            "should " + "play",
            "must " + "include",
            "correct " + "card",
            "breaks " + "the format",
            "secretly " + "opti" + "mal",
            "cut " + "this",
            "you " + "should",
            "keep" + "able",
            "mull" + "igan this hand",
        )

        self.assertFalse([phrase for phrase in forbidden if phrase in text])


if __name__ == "__main__":
    unittest.main()
