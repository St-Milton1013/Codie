from __future__ import annotations

import ast
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from codie.probability_engine import (
    SIM_R_STATE_VERSION,
    SimulationCardInstance,
    SimulationCommanderState,
    SimulationManaPool,
    SimulationState,
    SimulationStateBuildError,
    SimulationTargetProgress,
    SimulationUnsupportedBehavior,
    SimulationZone,
    build_simulation_state,
    simulation_state_to_dict,
)


class ProbabilityEngineSimRStateTest(unittest.TestCase):
    def test_state_serializes_deterministically_and_round_trips(self) -> None:
        state = build_simulation_state(self._state_payload())

        first = simulation_state_to_dict(state)
        second = simulation_state_to_dict(build_simulation_state(first))

        self.assertEqual(first, second)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["state_version"], SIM_R_STATE_VERSION)
        self.assertEqual(first["zones"][0]["cards"][0]["name"], "Rhystic Study")

    def test_state_model_is_immutable_and_builder_does_not_mutate_input(self) -> None:
        payload = self._state_payload()
        before = json.loads(json.dumps(payload))

        state = build_simulation_state(payload)

        self.assertEqual(payload, before)
        with self.assertRaises(FrozenInstanceError):
            state.turn = 2  # type: ignore[misc]
        with self.assertRaises(TypeError):
            state.metadata["note"] = "changed"  # type: ignore[index]

    def test_duplicate_card_instance_across_zones_fails_validation(self) -> None:
        payload = self._state_payload()
        duplicate = dict(payload["zones"][0]["cards"][0])
        duplicate["zone"] = "battlefield"
        duplicate["zone_index"] = 0
        payload["zones"].append(
            {
                "zone_name": "battlefield",
                "ordered": False,
                "visibility": "public",
                "owner": "player",
                "controller": "player",
                "cards": [duplicate],
            }
        )

        with self.assertRaises(SimulationStateBuildError):
            build_simulation_state(payload)

    def test_negative_mana_fails_and_restricted_mana_remains_visible(self) -> None:
        payload = self._state_payload()
        payload["mana_pool"]["restricted_mana"] = [{"amount": 1, "restriction": "cast enchantment", "source": "lotus_petal"}]

        state = build_simulation_state(payload)

        self.assertEqual(state.to_dict()["mana_pool"]["restricted_mana"][0]["restriction"], "cast enchantment")
        payload["mana_pool"]["U"] = -1
        with self.assertRaises(SimulationStateBuildError):
            build_simulation_state(payload)

    def test_commander_partner_identity_is_order_independent(self) -> None:
        first = SimulationCommanderState(
            commander_instance_ids=("kraum", "tymna"),
            commander_cast_count={"tymna": 1, "kraum": 0},
            commander_tax={"tymna": 2, "kraum": 0},
            commander_zone={"tymna": "command_zone", "kraum": "command_zone"},
            partner_group_key="kraum|tymna",
        )
        second = SimulationCommanderState(
            commander_instance_ids=("tymna", "kraum"),
            commander_cast_count={"kraum": 0, "tymna": 1},
            commander_tax={"kraum": 0, "tymna": 2},
            commander_zone={"kraum": "command_zone", "tymna": "command_zone"},
            partner_group_key="kraum|tymna",
        )

        self.assertEqual(first.to_dict(), second.to_dict())

    def test_zone_ordering_is_preserved(self) -> None:
        state = build_simulation_state(self._state_payload())

        self.assertEqual([card["name"] for card in state.library.to_dict()["cards"]], ["Island", "Mystic Remora"])

    def test_unsupported_behavior_and_target_progress_remain_visible(self) -> None:
        state = build_simulation_state(self._state_payload())
        payload = state.to_dict()

        self.assertEqual(payload["target_progress"]["target_condition_id"], "target-rhystic")
        self.assertEqual(payload["unsupported_behaviors"][0]["card_name"], "Sticker cards")
        self.assertTrue(payload["unsupported_behaviors"][0]["action_blocked"])

    def test_metadata_is_separate_from_core_state_fields(self) -> None:
        state = build_simulation_state(self._state_payload())
        payload = state.to_dict()

        self.assertEqual(payload["metadata"]["note"], "non-legality annotation")
        self.assertNotIn("note", payload["zones"][0]["cards"][0])

    def test_phase13_trace_v1_is_not_accepted_as_sim_r_state(self) -> None:
        trace_v1 = {
            "trace_id": "trace-1",
            "seed": "seed-1",
            "opening_hand": ["Island", "Rhystic Study"],
            "actions": [],
        }

        with self.assertRaises(SimulationStateBuildError):
            build_simulation_state(trace_v1)

    def test_no_action_or_search_helpers_are_exposed_by_state_module(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = (root / "sim_r_state.py").read_text(encoding="utf-8")

        self.assertNotIn("def apply_", text)
        self.assertNotIn("def search", text)
        self.assertNotIn("recommended", text.lower())

    def test_state_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "sim_r_state.py"
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
            "codie.db",
            "codie.providers",
            "codie.analytics",
            "codie.recommendations",
            "codie.ingestion",
            "sqlite3",
            "requests",
            "httpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def _state_payload(self) -> dict:
        return {
            "state_id": "state-1",
            "simulation_id": "sim-1",
            "history_id": "history-1",
            "turn": 1,
            "phase": "main",
            "step": "precombat_main",
            "active_player": "player",
            "priority_player": "player",
            "zones": [
                {
                    "zone_name": "hand",
                    "ordered": True,
                    "visibility": "private",
                    "owner": "player",
                    "controller": "player",
                    "cards": [
                        {
                            "card_instance_id": "hand-1",
                            "scryfall_id": "scryfall-rhystic",
                            "oracle_id": "oracle-rhystic",
                            "name": "Rhystic Study",
                            "owner": "player",
                            "controller": "player",
                            "zone": "hand",
                            "zone_index": 0,
                            "status_flags": ["castable"],
                            "source_card_id": "rhystic_study",
                        }
                    ],
                },
                {
                    "zone_name": "library",
                    "ordered": True,
                    "visibility": "hidden",
                    "owner": "player",
                    "controller": "player",
                    "cards": [
                        {
                            "card_instance_id": "library-1",
                            "scryfall_id": "scryfall-island",
                            "oracle_id": "oracle-island",
                            "name": "Island",
                            "owner": "player",
                            "controller": "player",
                            "zone": "library",
                            "zone_index": 0,
                            "status_flags": [],
                            "source_card_id": "island",
                        },
                        {
                            "card_instance_id": "library-2",
                            "scryfall_id": "scryfall-remora",
                            "oracle_id": "oracle-remora",
                            "name": "Mystic Remora",
                            "owner": "player",
                            "controller": "player",
                            "zone": "library",
                            "zone_index": 1,
                            "status_flags": [],
                            "source_card_id": "mystic_remora",
                        },
                    ],
                },
            ],
            "mana_pool": {
                "W": 0,
                "U": 1,
                "B": 0,
                "R": 0,
                "G": 0,
                "C": 0,
                "restricted_mana": [],
                "floating_mana_sources": ["tropical_island"],
                "expires_at_step": "end_of_step",
            },
            "life_total": 40,
            "land_drop_available": False,
            "lands_played_this_turn": 1,
            "commander_state": {
                "commander_instance_ids": ["tymna", "kraum"],
                "commander_cast_count": {"tymna": 0, "kraum": 0},
                "commander_tax": {"tymna": 0, "kraum": 0},
                "commander_zone": {"tymna": "command_zone", "kraum": "command_zone"},
                "partner_group_key": "kraum|tymna",
            },
            "target_progress": {
                "target_condition_id": "target-rhystic",
                "target_condition_version": "target-v1",
                "primary_success": False,
                "support_success": True,
                "compound_success": False,
                "required_components": ["cast_rhystic", "hold_interaction"],
                "satisfied_components": ["hold_interaction"],
                "failed_components": [],
                "interaction_readiness": {"force_of_will": True},
            },
            "unsupported_behaviors": [
                {
                    "card_instance_id": "unknown-1",
                    "card_name": "Sticker cards",
                    "behavior_key": "unrecognized_card",
                    "reason": "card behavior is not modeled",
                    "severity": "blocking",
                    "action_blocked": True,
                    "discovered_at_state_id": "state-1",
                }
            ],
            "metadata": {"note": "non-legality annotation"},
        }


if __name__ == "__main__":
    unittest.main()
