from __future__ import annotations

import ast
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from codie.probability_engine.sim_r_behavior import (
    SIM_R_BEHAVIOR_VERSION,
    UNSUPPORTED_BEHAVIOR_CATEGORY,
    SimulationBehaviorBuildError,
    build_behavior_profile,
    build_behavior_proposal,
    behavior_profile_to_dict,
    behavior_proposal_to_dict,
)


class ProbabilityEngineSimRBehaviorTest(unittest.TestCase):
    def test_behavior_profile_serializes_deterministically_and_round_trips(self) -> None:
        profile = build_behavior_profile(self._profile_payload())

        first = behavior_profile_to_dict(profile)
        second = behavior_profile_to_dict(build_behavior_profile(first))

        self.assertEqual(first, second)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["behavior_version"], SIM_R_BEHAVIOR_VERSION)

    def test_behavior_proposal_serializes_deterministically_and_round_trips(self) -> None:
        proposal = build_behavior_proposal(self._proposal_payload())

        first = behavior_proposal_to_dict(proposal)
        second = behavior_proposal_to_dict(build_behavior_proposal(first))

        self.assertEqual(first, second)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["behavior_version"], SIM_R_BEHAVIOR_VERSION)

    def test_models_are_immutable_and_builders_do_not_mutate_input(self) -> None:
        payload = self._proposal_payload()
        before = json.loads(json.dumps(payload))

        proposal = build_behavior_proposal(payload)

        self.assertEqual(payload, before)
        with self.assertRaises(FrozenInstanceError):
            proposal.proposal_id = "changed"  # type: ignore[misc]
        with self.assertRaises(TypeError):
            proposal.metadata["note"] = "changed"  # type: ignore[index]

    def test_profile_identity_fields_remain_visible(self) -> None:
        profile = behavior_profile_to_dict(build_behavior_profile(self._profile_payload()))

        self.assertEqual(profile["behavior_profile_id"], "profile-rhystic-normal-cast")
        self.assertEqual(profile["behavior_key"], "normal_cast")
        self.assertEqual(profile["behavior_category"], "NormalCast")
        self.assertEqual(profile["behavior_version"], SIM_R_BEHAVIOR_VERSION)
        self.assertEqual(profile["supported_action_types"], ["cast_spell"])
        self.assertEqual(profile["source_card_identity"]["oracle_id"], "oracle-rhystic")
        self.assertEqual(profile["status"], "supported")
        self.assertEqual(profile["confidence"], 1.0)

    def test_proposal_requirement_fields_remain_visible(self) -> None:
        proposal = behavior_proposal_to_dict(build_behavior_proposal(self._proposal_payload()))

        self.assertEqual(proposal["proposal_id"], "proposal-1")
        self.assertEqual(proposal["behavior_profile_id"], "profile-rhystic-normal-cast")
        self.assertEqual(proposal["action_id"], "action-1")
        self.assertEqual(proposal["requirements"][0]["requirement_type"], "mana_payment")
        self.assertEqual(proposal["required_resource_intents"][0]["mana"], {"C": 2, "U": 1})
        self.assertEqual(proposal["zone_change_intents"][0]["from_zone"], "hand")
        self.assertEqual(proposal["target_requirements"][0]["target_type"], "spell")
        self.assertEqual(proposal["timing_restrictions"][0]["restriction"], "main_phase")
        self.assertEqual(proposal["confidence"], 0.95)
        self.assertEqual(proposal["source_card_identity"]["scryfall_id"], "scryfall-rhystic")

    def test_unsupported_behavior_notes_remain_visible(self) -> None:
        payload = self._proposal_payload()
        payload["behavior_category"] = UNSUPPORTED_BEHAVIOR_CATEGORY
        payload["proposal_status"] = "unsupported"
        payload["unsupported_behavior_notes"] = [
            {
                "note_id": "note-1",
                "behavior_key": "normal_cast",
                "reason": "replacement effect not modeled",
                "affected_card_name": "Rhystic Study",
                "source_card_identity": {"oracle_id": "oracle-rhystic"},
            }
        ]

        proposal = behavior_proposal_to_dict(build_behavior_proposal(payload))

        self.assertEqual(proposal["unsupported_behavior_notes"][0]["reason"], "replacement effect not modeled")
        self.assertEqual(proposal["unsupported_behavior_notes"][0]["affected_card_name"], "Rhystic Study")

    def test_unknown_category_fails_unless_explicitly_unsupported(self) -> None:
        payload = self._profile_payload()
        payload["behavior_category"] = "InventedCategory"

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_profile(payload)

    def test_unsupported_profile_requires_non_supported_status(self) -> None:
        payload = self._profile_payload()
        payload["behavior_category"] = UNSUPPORTED_BEHAVIOR_CATEGORY

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_profile(payload)

        payload["status"] = "unsupported"
        profile = behavior_profile_to_dict(build_behavior_profile(payload))
        self.assertEqual(profile["behavior_category"], UNSUPPORTED_BEHAVIOR_CATEGORY)

    def test_executable_code_payloads_are_rejected(self) -> None:
        payload = self._proposal_payload()
        payload["metadata"] = {"code_payload": "def run(): pass"}

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

    def test_callable_objects_are_rejected(self) -> None:
        payload = self._proposal_payload()
        payload["metadata"] = {"callback": lambda: None}

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

    def test_llm_authored_executable_behavior_is_rejected(self) -> None:
        payload = self._proposal_payload()
        payload["metadata"] = {"authored_by": "llm", "executable": True}

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

    def test_confidence_must_be_between_zero_and_one(self) -> None:
        payload = self._proposal_payload()
        payload["confidence"] = -0.1

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

        payload["confidence"] = 1.1
        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

    def test_duplicate_requirement_and_note_ids_fail_validation(self) -> None:
        payload = self._proposal_payload()
        payload["requirements"].append(dict(payload["requirements"][0]))

        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

        payload = self._proposal_payload()
        payload["behavior_category"] = UNSUPPORTED_BEHAVIOR_CATEGORY
        payload["proposal_status"] = "unsupported"
        note = {
            "note_id": "note-1",
            "behavior_key": "normal_cast",
            "reason": "not modeled",
        }
        payload["unsupported_behavior_notes"] = [note, dict(note)]
        with self.assertRaises(SimulationBehaviorBuildError):
            build_behavior_proposal(payload)

    def test_no_runtime_execution_helpers_are_exposed(self) -> None:
        root = Path(__file__).resolve().parents[1] / "codie" / "probability_engine"
        text = (root / "sim_r_behavior.py").read_text(encoding="utf-8")

        self.assertNotIn("def apply_", text)
        self.assertNotIn("def execute", text)
        self.assertNotIn("def search", text)
        self.assertNotIn("def write_ledger", text)
        self.assertNotIn("def build_transition", text)
        self.assertNotIn("recommended", text.lower())

    def test_behavior_module_has_no_forbidden_imports(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "sim_r_behavior.py"
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

    def _profile_payload(self) -> dict:
        return {
            "behavior_profile_id": "profile-rhystic-normal-cast",
            "behavior_key": "normal_cast",
            "behavior_category": "NormalCast",
            "behavior_version": SIM_R_BEHAVIOR_VERSION,
            "supported_action_types": ["cast_spell"],
            "source_card_identity": {
                "oracle_id": "oracle-rhystic",
                "scryfall_id": "scryfall-rhystic",
                "card_name": "Rhystic Study",
            },
            "status": "supported",
            "confidence": 1.0,
            "metadata": {"evidence_only": True},
        }

    def _proposal_payload(self) -> dict:
        return {
            "proposal_id": "proposal-1",
            "behavior_profile_id": "profile-rhystic-normal-cast",
            "behavior_key": "normal_cast",
            "behavior_category": "NormalCast",
            "behavior_version": SIM_R_BEHAVIOR_VERSION,
            "action_id": "action-1",
            "proposal_status": "proposed",
            "requirements": [
                {
                    "requirement_id": "requirement-1",
                    "requirement_type": "mana_payment",
                    "intent": {"mana": {"C": 2, "U": 1}},
                    "status": "required",
                }
            ],
            "required_resource_intents": [{"resource_type": "mana", "mana": {"C": 2, "U": 1}}],
            "zone_change_intents": [{"card_instance_id": "hand-rhystic", "from_zone": "hand", "to_zone": "stack"}],
            "target_requirements": [{"target_type": "spell", "minimum_targets": 0}],
            "timing_restrictions": [{"restriction": "main_phase"}],
            "unsupported_behavior_notes": [],
            "confidence": 0.95,
            "source_card_identity": {
                "oracle_id": "oracle-rhystic",
                "scryfall_id": "scryfall-rhystic",
                "card_name": "Rhystic Study",
            },
            "metadata": {"evidence_only": True},
        }


if __name__ == "__main__":
    unittest.main()
