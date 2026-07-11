from __future__ import annotations

import ast
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from codie.probability_engine.sim_r_transition import (
    NO_OP,
    SIM_R_TRANSITION_VERSION,
    SimulationTransitionBuildError,
    build_transition_result,
    transition_result_to_dict,
)


class ProbabilityEngineSimRTransitionTest(unittest.TestCase):
    def test_transition_result_serializes_deterministically_and_round_trips(self) -> None:
        result = build_transition_result(self._transition_payload())

        first = transition_result_to_dict(result)
        second = transition_result_to_dict(build_transition_result(first))

        self.assertEqual(first, second)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["transition_version"], SIM_R_TRANSITION_VERSION)

    def test_transition_models_are_immutable_and_builder_does_not_mutate_input(self) -> None:
        payload = self._transition_payload()
        before = json.loads(json.dumps(payload))

        result = build_transition_result(payload)

        self.assertEqual(payload, before)
        with self.assertRaises(FrozenInstanceError):
            result.transition_id = "changed"  # type: ignore[misc]
        with self.assertRaises(TypeError):
            result.metadata["note"] = "changed"  # type: ignore[index]

    def test_required_identity_and_transition_fields_remain_visible(self) -> None:
        payload = transition_result_to_dict(build_transition_result(self._transition_payload()))

        self.assertEqual(payload["transition_id"], "transition-1")
        self.assertEqual(payload["transition_version"], SIM_R_TRANSITION_VERSION)
        self.assertEqual(payload["simulation_id"], "sim-1")
        self.assertEqual(payload["pre_state_id"], "state-before")
        self.assertEqual(payload["post_state_id"], "state-after")
        self.assertEqual(payload["action_intent"]["action_id"], "action-1")
        self.assertEqual(payload["action_intent"]["action_type"], "cast_spell")
        self.assertEqual(payload["action_intent"]["behavior_key"], "normal_cast")
        self.assertEqual(payload["transition_status"], "success")

    def test_resource_ledger_ids_and_trace_event_ids_remain_visible(self) -> None:
        payload = transition_result_to_dict(build_transition_result(self._transition_payload()))

        self.assertEqual(payload["resource_ledger_ids"], ["ledger-1"])
        self.assertEqual(payload["behavior_result"]["resource_ledger_ids"], ["ledger-1"])
        self.assertEqual(payload["trace_events"][0]["trace_event_id"], "trace-event-1")
        self.assertEqual(payload["trace_events"][0]["resource_ledger_ids"], ["ledger-1"])

    def test_unsupported_behavior_and_failed_reason_remain_visible(self) -> None:
        payload = self._transition_payload()
        payload["behavior_result"]["behavior_status"] = "failed"
        payload["behavior_result"]["failed_reason"] = "insufficient mana"
        payload["behavior_result"]["unsupported_behaviors"] = [{"card_name": "Unknown Card", "reason": "not modeled"}]
        payload["trace_events"][0]["transition_status"] = "failed"
        payload["trace_events"][0]["failed_reason"] = "insufficient mana"
        payload["trace_events"][0]["unsupported_behaviors"] = [{"card_name": "Unknown Card", "reason": "not modeled"}]
        payload["transition_status"] = "failed"
        payload["resource_ledger_ids"] = []
        payload["behavior_result"]["resource_ledger_ids"] = []
        payload["trace_events"][0]["resource_ledger_ids"] = []

        result = transition_result_to_dict(build_transition_result(payload))

        self.assertEqual(result["behavior_result"]["failed_reason"], "insufficient mana")
        self.assertEqual(result["trace_events"][0]["failed_reason"], "insufficient mana")
        self.assertEqual(result["behavior_result"]["unsupported_behaviors"][0]["reason"], "not modeled")
        self.assertEqual(result["trace_events"][0]["unsupported_behaviors"][0]["card_name"], "Unknown Card")

    def test_no_op_transitions_are_explicit(self) -> None:
        payload = self._transition_payload()
        payload["post_state_id"] = payload["pre_state_id"]
        payload["transition_status"] = NO_OP
        payload["resource_ledger_ids"] = []
        payload["action_intent"]["declared_cost_keys"] = []
        payload["behavior_result"]["resource_ledger_ids"] = []
        payload["trace_events"][0]["post_state_id"] = payload["pre_state_id"]
        payload["trace_events"][0]["transition_status"] = NO_OP
        payload["trace_events"][0]["resource_ledger_ids"] = []

        result = transition_result_to_dict(build_transition_result(payload))

        self.assertEqual(result["transition_status"], NO_OP)

    def test_matching_state_ids_without_no_op_fails_validation(self) -> None:
        payload = self._transition_payload()
        payload["post_state_id"] = payload["pre_state_id"]
        payload["trace_events"][0]["post_state_id"] = payload["pre_state_id"]

        with self.assertRaises(SimulationTransitionBuildError):
            build_transition_result(payload)

    def test_resource_consuming_successful_transition_requires_ledger_ids(self) -> None:
        payload = self._transition_payload()
        payload["resource_ledger_ids"] = []
        payload["behavior_result"]["resource_ledger_ids"] = []
        payload["trace_events"][0]["resource_ledger_ids"] = []

        with self.assertRaises(SimulationTransitionBuildError):
            build_transition_result(payload)

    def test_negative_turn_metadata_fails_validation(self) -> None:
        payload = self._transition_payload()
        payload["turn"] = -1

        with self.assertRaises(SimulationTransitionBuildError):
            build_transition_result(payload)

    def test_negative_priority_sequence_metadata_fails_validation(self) -> None:
        payload = self._transition_payload()
        payload["priority_sequence"] = -1

        with self.assertRaises(SimulationTransitionBuildError):
            build_transition_result(payload)

    def test_trace_event_reference_mismatch_fails_validation(self) -> None:
        payload = self._transition_payload()
        payload["trace_events"][0]["action_id"] = "different-action"

        with self.assertRaises(SimulationTransitionBuildError):
            build_transition_result(payload)

    def test_no_runtime_execution_helpers_are_exposed(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = (root / "sim_r_transition.py").read_text(encoding="utf-8")

        self.assertNotIn("def apply_", text)
        self.assertNotIn("def execute", text)
        self.assertNotIn("def search", text)
        self.assertNotIn("recommended", text.lower())

    def test_transition_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "sim_r_transition.py"
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
            ".".join(("codie", "db")),
            ".".join(("codie", "providers")),
            ".".join(("codie", "analytics")),
            ".".join(("codie", "recommendations")),
            ".".join(("codie", "ingestion")),
            "sqli" + "te3",
            "requ" + "ests",
            "ht" + "tpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def _transition_payload(self) -> dict:
        return {
            "transition_id": "transition-1",
            "simulation_id": "sim-1",
            "pre_state_id": "state-before",
            "post_state_id": "state-after",
            "action_intent": {
                "action_id": "action-1",
                "action_type": "cast_spell",
                "actor": "player",
                "behavior_key": "normal_cast",
                "source_card_instance_id": "hand-rhystic",
                "target_card_instance_ids": [],
                "declared_cost_keys": ["cost-rhystic"],
                "metadata": {"card_name": "Rhystic Study"},
            },
            "behavior_result": {
                "behavior_key": "normal_cast",
                "behavior_status": "success",
                "resource_ledger_ids": ["ledger-1"],
                "unsupported_behaviors": [],
                "metadata": {"result": "spell moved to stack"},
            },
            "transition_status": "success",
            "turn": 1,
            "priority_sequence": 3,
            "resource_ledger_ids": ["ledger-1"],
            "trace_events": [
                {
                    "trace_event_id": "trace-event-1",
                    "transition_id": "transition-1",
                    "pre_state_id": "state-before",
                    "post_state_id": "state-after",
                    "action_id": "action-1",
                    "behavior_key": "normal_cast",
                    "transition_status": "success",
                    "turn": 1,
                    "priority_sequence": 3,
                    "resource_ledger_ids": ["ledger-1"],
                    "unsupported_behaviors": [],
                    "metadata": {"line": "cast Rhystic Study"},
                }
            ],
            "metadata": {"evidence_only": True},
        }


if __name__ == "__main__":
    unittest.main()
