from __future__ import annotations

import json
import unittest
from pathlib import Path

from codie.probability_engine import (
    ManaCost,
    ManaOption,
    SimulationActionModel,
    SimulationCardModel,
    SimulationConfig,
    SimulationDeck,
    SimulationDeckCard,
    SimulationResult,
    SimulationTargetCondition,
    SimulationTrace,
    SimulationTraceAction,
    SimulationUnsupportedItem,
)


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "reference" / "cedhdata_simulator" / "fixtures"


class ProbabilityEngineModelTest(unittest.TestCase):
    def test_mana_cost_is_stable_and_has_mana_value(self) -> None:
        cost = ManaCost.from_mapping({"Generic": 2, "U": 1})

        self.assertEqual(cost.mana_value, 3)
        self.assertEqual(list(cost.to_dict()), ["W", "U", "B", "R", "G", "C", "Generic"])
        self.assertEqual(cost.to_dict()["U"], 1)
        with self.assertRaises(ValueError):
            ManaCost(Generic=-1)

    def test_mana_option_serializes_restrictions(self) -> None:
        option = ManaOption(B=1, restriction="cast target", source_card_id="dark_ritual")

        self.assertEqual(option.total, 1)
        self.assertEqual(option.to_dict()["restriction"], "cast target")
        self.assertEqual(ManaOption.empty().to_dict()["restriction"], "empty")
        with self.assertRaises(ValueError):
            ManaOption()

    def test_action_model_preserves_unknown_metadata(self) -> None:
        action = SimulationActionModel.from_mapping(
            {
                "type": "tap_for_mana",
                "tap": True,
                "produces": {"C": 2},
                "requires_metalcraft": True,
            }
        )

        self.assertEqual(action.action_type, "tap_for_mana")
        self.assertEqual(action.produces[0].to_dict()["C"], 2)
        self.assertTrue(action.metadata["tap"])
        self.assertTrue(action.metadata["requires_metalcraft"])

    def test_card_model_represents_sol_ring_style_mana(self) -> None:
        card = SimulationCardModel.from_mapping(
            {
                "id": "sol_ring",
                "name": "Sol Ring",
                "types": ["artifact"],
                "mana_cost": {"Generic": 1},
                "board_abilities": [{"type": "tap_for_mana", "tap": True, "produces": {"C": 2}}],
            }
        )

        self.assertEqual(card.card_id, "sol_ring")
        self.assertEqual(card.mana_cost.mana_value, 1)
        self.assertEqual(card.board_abilities[0].action_type, "tap_for_mana")
        self.assertEqual(card.raw_reference_shape["id"], "sol_ring")

    def test_card_model_preserves_chrome_mox_memory_requirement(self) -> None:
        card = SimulationCardModel.from_mapping(
            {
                "id": "chrome_mox",
                "name": "Chrome Mox",
                "types": ["artifact"],
                "cast_actions": [
                    {
                        "type": "exile_from_hand",
                        "exclude_types": ["artifact", "land"],
                        "optional": True,
                        "store_memory_as": "imprint",
                    }
                ],
                "board_abilities": [
                    {
                        "type": "tap_for_mana",
                        "tap": True,
                        "produces": "any",
                        "requires_memory": True,
                    }
                ],
            }
        )

        self.assertEqual(card.cast_actions[0].metadata["store_memory_as"], "imprint")
        self.assertTrue(card.board_abilities[0].metadata["requires_memory"])
        self.assertEqual(len(card.board_abilities[0].produces), 5)

    def test_fetchland_style_search_action_is_declarative(self) -> None:
        card = SimulationCardModel.from_mapping(
            {
                "id": "polluted_delta",
                "name": "Polluted Delta",
                "types": ["land"],
                "board_abilities": [
                    {
                        "type": "sacrifice_to_search",
                        "sacrifice": True,
                        "search_targets": ["island", "swamp"],
                    }
                ],
            }
        )

        action = card.board_abilities[0]
        self.assertEqual(action.action_type, "sacrifice_to_search")
        self.assertEqual(action.metadata["search_targets"], ["island", "swamp"])

    def test_target_condition_and_config_validate_reproducibility(self) -> None:
        target = SimulationTargetCondition(
            target_card="Rhystic Study",
            target_card_id="rhystic_study",
            target_zone="stack",
            turn=2,
            condition_type="cast_or_access",
        )
        config = SimulationConfig(
            deck_hash="sha256:deck",
            seed="seed-1",
            games_requested=1000,
            min_mulligan_keep=3,
            mulligan_mode="policy",
            simulator_version="codie-sim-0",
            card_model_version="models-0",
            targets=(target,),
        )

        self.assertEqual(config.to_dict()["targets"][0]["target_card"], "Rhystic Study")
        with self.assertRaises(ValueError):
            SimulationTargetCondition(target_card="Rhystic Study", target_zone="stack", turn=0, condition_type="cast")
        with self.assertRaises(ValueError):
            SimulationConfig(
                deck_hash="sha256:deck",
                seed="",
                games_requested=1,
                min_mulligan_keep=1,
                mulligan_mode="policy",
                simulator_version="v",
                card_model_version="m",
                targets=(target,),
            )

    def test_deck_preserves_unresolved_cards(self) -> None:
        deck = SimulationDeck(
            deck_hash="sha256:deck",
            cards=(SimulationDeckCard(quantity=1, name="Sticker cards"),),
            commanders=(SimulationDeckCard(quantity=1, name="Tymna the Weaver", model_id="tymna_the_weaver", zone="command"),),
            unresolved_cards=("Sticker cards",),
        )

        payload = deck.to_dict()
        self.assertEqual(payload["unresolved_cards"], ["Sticker cards"])
        self.assertEqual(payload["commanders"][0]["zone"], "command")

    def test_unsupported_item_serializes_reason(self) -> None:
        item = SimulationUnsupportedItem(
            item_type="card",
            card_name="Sticker cards",
            card_id="sticker_cards",
            reason="unrecognized card treated as blank",
        )

        self.assertEqual(item.to_dict()["reason"], "unrecognized card treated as blank")
        with self.assertRaises(ValueError):
            SimulationUnsupportedItem(item_type="", reason="missing")

    def test_trace_preserves_action_order(self) -> None:
        trace = SimulationTrace(
            trace_id="trace-1",
            seed="seed-1",
            game_index=1,
            opening_hand=("Dark Ritual", "Ad Nauseam"),
            mulligan_count=0,
            success=True,
            actions=(
                SimulationTraceAction(turn=1, description="Cast Dark Ritual", card_id="dark_ritual", action_type="cast_spell"),
                SimulationTraceAction(turn=1, description="Cast Ad Nauseam", card_id="ad_nauseam", action_type="cast_spell"),
            ),
            unsupported_items=(SimulationUnsupportedItem(item_type="card", reason="none", card_name="Sticker cards"),),
        )

        payload = trace.to_dict()
        self.assertEqual([row["card_id"] for row in payload["actions"]], ["dark_ritual", "ad_nauseam"])
        self.assertEqual(payload["unsupported_items"][0]["card_name"], "Sticker cards")

    def test_result_carries_unsupported_items_and_raw_payload(self) -> None:
        target = SimulationTargetCondition("Ad Nauseam", "stack", 1, "cast_or_access", target_card_id="ad_nauseam")
        result = SimulationResult(
            target=target,
            games_completed=1000,
            win_count=2,
            win_rate=0.002,
            margin_of_error=0.0027,
            unsupported_items=(SimulationUnsupportedItem(item_type="card", reason="unknown", card_name="Sticker cards"),),
            raw_payload={"source": "reference"},
        )

        self.assertEqual(result.to_dict()["unsupported_items"][0]["card_name"], "Sticker cards")
        with self.assertRaises(ValueError):
            SimulationResult(target=target, games_completed=1, win_count=2, win_rate=2.0)

    def test_raw_cedhdata_trace_export_maps_to_core_trace_model(self) -> None:
        payload = json.loads((FIXTURE_ROOT / "rhystic-traces-ad-nauseam-2026-06-29T23-05-19-764Z.json").read_text(encoding="utf-8"))
        raw_trace = payload["traces"][0]
        trace = SimulationTrace(
            trace_id=f"cedhdata:{raw_trace['gameNum']}",
            seed=payload["run"]["startedAt"],
            game_index=raw_trace["gameNum"],
            opening_hand=tuple(raw_trace["hand"]),
            mulligan_count=0,
            success=True,
            actions=tuple(SimulationTraceAction.from_mapping(row) for row in raw_trace["trace"]),
            unsupported_items=tuple(
                SimulationUnsupportedItem(
                    item_type="card",
                    card_name=row["name"],
                    card_id=row["id"],
                    reason="missing card in reference export",
                )
                for row in payload["progress"]["missingCards"]
            ),
            created_at=payload["exportedAt"],
        )

        self.assertEqual(trace.actions[-1].description, "Cast Ad Nauseam")
        self.assertEqual(trace.actions[-1].action_type, "cast_spell")
        self.assertEqual(trace.unsupported_items[0].card_name, "Sticker cards")


if __name__ == "__main__":
    unittest.main()
