from __future__ import annotations

import ast
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from codie.probability_engine.sim_r_ledger import (
    SIM_R_LEDGER_VERSION,
    SimulationLedgerBuildError,
    SimulationResourceLedger,
    build_resource_ledger,
    resource_ledger_to_dict,
)


class ProbabilityEngineSimRResourceLedgerTest(unittest.TestCase):
    def test_ledger_serializes_deterministically_and_round_trips(self) -> None:
        ledger = build_resource_ledger(self._ledger_payload())

        first = resource_ledger_to_dict(ledger)
        second = resource_ledger_to_dict(build_resource_ledger(first))

        self.assertEqual(first, second)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["ledger_version"], SIM_R_LEDGER_VERSION)
        self.assertEqual(first["entries"][0]["resource_key"], "mana-u-1")

    def test_ledger_models_are_immutable_and_builder_does_not_mutate_input(self) -> None:
        payload = self._ledger_payload()
        before = json.loads(json.dumps(payload))

        ledger = build_resource_ledger(payload)

        self.assertEqual(payload, before)
        with self.assertRaises(FrozenInstanceError):
            ledger.ledger_id = "changed"  # type: ignore[misc]
        with self.assertRaises(TypeError):
            ledger.metadata["note"] = "changed"  # type: ignore[index]

    def test_duplicate_ledger_entry_id_fails_validation(self) -> None:
        payload = self._ledger_payload()
        duplicate = dict(payload["entries"][0])
        duplicate["resource_key"] = "mana-u-2"
        payload["entries"].append(duplicate)

        with self.assertRaises(SimulationLedgerBuildError):
            build_resource_ledger(payload)

    def test_duplicate_payment_key_fails_validation(self) -> None:
        payload = self._ledger_payload()
        duplicate = dict(payload["payments"][0])
        duplicate["status"] = "failed"
        payload["payments"].append(duplicate)

        with self.assertRaises(SimulationLedgerBuildError):
            build_resource_ledger(payload)

    def test_double_spent_resource_key_fails_validation(self) -> None:
        payload = self._ledger_payload()
        duplicate = dict(payload["entries"][0])
        duplicate["ledger_entry_id"] = "entry-2"
        duplicate["payment_key"] = "payment-2"
        payload["entries"].append(duplicate)

        with self.assertRaises(SimulationLedgerBuildError):
            build_resource_ledger(payload)

    def test_explicit_reusable_resource_metadata_remains_visible(self) -> None:
        payload = self._ledger_payload()
        payload["entries"][0]["reusable"] = True
        payload["entries"][0]["metadata"] = {"reusable_reason": "static replacement effect"}
        duplicate = dict(payload["entries"][0])
        duplicate["ledger_entry_id"] = "entry-2"
        duplicate["payment_key"] = "payment-2"
        payload["entries"].append(duplicate)

        ledger = build_resource_ledger(payload)
        result = resource_ledger_to_dict(ledger)

        self.assertTrue(result["entries"][0]["reusable"])
        self.assertEqual(result["entries"][0]["metadata"]["reusable_reason"], "static replacement effect")

    def test_negative_resource_quantity_fails_validation(self) -> None:
        payload = self._ledger_payload()
        payload["entries"][0]["resource_quantity"] = -1

        with self.assertRaises(SimulationLedgerBuildError):
            build_resource_ledger(payload)

    def test_restricted_mana_metadata_remains_visible(self) -> None:
        ledger = build_resource_ledger(self._ledger_payload())
        result = resource_ledger_to_dict(ledger)

        self.assertEqual(result["entries"][0]["restriction_metadata"]["restriction"], "cast enchantment")
        self.assertEqual(result["entries"][0]["restriction_metadata"]["source_card"], "Lotus Petal")

    def test_failed_and_unsupported_payments_remain_visible(self) -> None:
        payload = self._ledger_payload()
        payload["payments"].append(
            {
                "payment_key": "payment-failed",
                "action_id": "action-1",
                "cost_key": "cost-1",
                "status": "failed",
                "paid_resource_keys": [],
                "failed_reason": "insufficient mana",
                "metadata": {},
            }
        )
        payload["payments"].append(
            {
                "payment_key": "payment-unsupported",
                "action_id": "action-2",
                "cost_key": "cost-alt",
                "status": "unsupported",
                "paid_resource_keys": [],
                "unsupported_reason": "alternate cost is not modeled",
                "metadata": {"affected_card": "Force of Will"},
            }
        )
        payload["entries"].append(
            {
                "ledger_entry_id": "entry-unsupported",
                "resource_key": "alternate-cost-force",
                "resource_type": "unsupported_cost",
                "resource_quantity": 0,
                "action_id": "action-2",
                "cost_key": "cost-alt",
                "payment_key": "payment-unsupported",
                "status": "unsupported",
                "unsupported_metadata": {"reason": "alternate cost is not modeled"},
                "metadata": {},
            }
        )

        result = resource_ledger_to_dict(build_resource_ledger(payload))

        statuses = {payment["payment_key"]: payment for payment in result["payments"]}
        self.assertEqual(statuses["payment-failed"]["failed_reason"], "insufficient mana")
        self.assertEqual(statuses["payment-unsupported"]["unsupported_reason"], "alternate cost is not modeled")
        self.assertEqual(result["entries"][1]["unsupported_metadata"]["reason"], "alternate cost is not modeled")

    def test_state_action_cost_and_payment_references_remain_visible(self) -> None:
        result = resource_ledger_to_dict(build_resource_ledger(self._ledger_payload()))

        self.assertEqual(result["pre_state_id"], "state-before")
        self.assertEqual(result["post_state_id"], "state-after")
        self.assertEqual(result["entries"][0]["action_id"], "action-1")
        self.assertEqual(result["entries"][0]["cost_key"], "cost-1")
        self.assertEqual(result["entries"][0]["payment_key"], "payment-1")

    def test_no_state_transition_or_recommendation_helpers_are_exposed(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = (root / "sim_r_ledger.py").read_text(encoding="utf-8")

        self.assertNotIn("def apply_", text)
        self.assertNotIn("def transition", text)
        self.assertNotIn("def search", text)
        self.assertNotIn("recommended", text.lower())

    def test_ledger_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "sim_r_ledger.py"
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

    def _ledger_payload(self) -> dict:
        return {
            "ledger_id": "ledger-1",
            "simulation_id": "sim-1",
            "pre_state_id": "state-before",
            "post_state_id": "state-after",
            "entries": [
                {
                    "ledger_entry_id": "entry-1",
                    "resource_key": "mana-u-1",
                    "resource_type": "mana",
                    "resource_quantity": 1,
                    "action_id": "action-1",
                    "cost_key": "cost-1",
                    "payment_key": "payment-1",
                    "status": "consumed",
                    "restriction_metadata": {
                        "restriction": "cast enchantment",
                        "source_card": "Lotus Petal",
                    },
                    "unsupported_metadata": {},
                    "metadata": {"source_zone": "mana_pool"},
                }
            ],
            "payments": [
                {
                    "payment_key": "payment-1",
                    "action_id": "action-1",
                    "cost_key": "cost-1",
                    "status": "paid",
                    "paid_resource_keys": ["mana-u-1"],
                    "metadata": {"paid_for": "Rhystic Study"},
                }
            ],
            "metadata": {"note": "resource ledger evidence only"},
        }


if __name__ == "__main__":
    unittest.main()
