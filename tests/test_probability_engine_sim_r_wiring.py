import unittest
from dataclasses import FrozenInstanceError

from codie.probability_engine.sim_r_wiring import (
    COMPATIBLE,
    INCOMPATIBLE,
    SIM_R_WIRING_VERSION,
    SimulationBehaviorTransitionLink,
    SimulationBehaviorWiringResult,
    SimulationWiringBuildError,
    behavior_transition_link_to_dict,
    behavior_wiring_result_to_dict,
    build_behavior_transition_link,
    build_behavior_wiring_result,
)


def _link_payload(**overrides):
    payload = {
        "wiring_id": "wire-1",
        "wiring_version": SIM_R_WIRING_VERSION,
        "simulation_id": "sim-1",
        "pre_state_id": "state-a",
        "post_state_id": "state-b",
        "action_id": "action-1",
        "behavior_profile_id": "profile-1",
        "behavior_proposal_id": "proposal-1",
        "behavior_key": "dark-ritual",
        "behavior_category": "ManaProduction",
        "compatibility_status": COMPATIBLE,
        "transition_id": "transition-1",
        "resource_ledger_ids": ["ledger-1"],
        "requirement_ids": ["req-1"],
        "unsupported_note_ids": ["note-1"],
        "failure_reason": None,
        "caveats": ["model-derived wiring only"],
        "turn": 1,
        "priority_sequence": 0,
        "metadata": {"source": "unit"},
    }
    payload.update(overrides)
    return payload


def _result_payload(**overrides):
    payload = {
        "wiring_result_id": "wiring-result-1",
        "wiring_version": SIM_R_WIRING_VERSION,
        "simulation_id": "sim-1",
        "compatibility_status": COMPATIBLE,
        "failure_reason": None,
        "caveats": ["no execution performed"],
        "links": [_link_payload()],
        "metadata": {"generated_by": "test"},
    }
    payload.update(overrides)
    return payload


class SimulationBehaviorTransitionLinkTests(unittest.TestCase):
    def test_link_serializes_deterministically(self):
        link = build_behavior_transition_link(_link_payload())

        self.assertEqual(behavior_transition_link_to_dict(link), behavior_transition_link_to_dict(link))
        self.assertEqual(
            list(behavior_transition_link_to_dict(link).keys()),
            [
                "wiring_id",
                "wiring_version",
                "simulation_id",
                "pre_state_id",
                "post_state_id",
                "action_id",
                "behavior_profile_id",
                "behavior_proposal_id",
                "behavior_key",
                "behavior_category",
                "compatibility_status",
                "transition_id",
                "resource_ledger_ids",
                "requirement_ids",
                "unsupported_note_ids",
                "failure_reason",
                "caveats",
                "turn",
                "priority_sequence",
                "metadata",
            ],
        )

    def test_link_round_trips_through_dict(self):
        link = build_behavior_transition_link(_link_payload())
        rebuilt = build_behavior_transition_link(behavior_transition_link_to_dict(link))

        self.assertEqual(behavior_transition_link_to_dict(rebuilt), behavior_transition_link_to_dict(link))

    def test_link_is_immutable_and_does_not_mutate_input(self):
        payload = _link_payload(metadata={"nested": {"value": 1}})
        link = build_behavior_transition_link(payload)
        payload["metadata"]["nested"]["value"] = 99

        with self.assertRaises(FrozenInstanceError):
            link.wiring_id = "changed"
        self.assertEqual(behavior_transition_link_to_dict(link)["metadata"]["nested"]["value"], 1)

    def test_visibility_fields_are_preserved(self):
        link = build_behavior_transition_link(_link_payload())
        data = behavior_transition_link_to_dict(link)

        for key in (
            "wiring_id",
            "wiring_version",
            "simulation_id",
            "pre_state_id",
            "post_state_id",
            "action_id",
            "behavior_profile_id",
            "behavior_proposal_id",
            "behavior_key",
            "behavior_category",
            "transition_id",
            "resource_ledger_ids",
            "requirement_ids",
            "unsupported_note_ids",
            "compatibility_status",
            "failure_reason",
            "caveats",
        ):
            self.assertIn(key, data)

    def test_duplicate_reference_ids_fail(self):
        cases = (
            {"resource_ledger_ids": ["ledger-1", "ledger-1"]},
            {"requirement_ids": ["req-1", "req-1"]},
            {"unsupported_note_ids": ["note-1", "note-1"]},
        )
        for override in cases:
            with self.subTest(override=override):
                with self.assertRaises(SimulationWiringBuildError):
                    build_behavior_transition_link(_link_payload(**override))

    def test_negative_metadata_fails(self):
        for override in ({"turn": -1}, {"priority_sequence": -1}):
            with self.subTest(override=override):
                with self.assertRaises(SimulationWiringBuildError):
                    build_behavior_transition_link(_link_payload(**override))

    def test_compatible_link_requires_transition_and_reference(self):
        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_transition_link(_link_payload(transition_id=None))

        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_transition_link(
                _link_payload(resource_ledger_ids=[], requirement_ids=[], unsupported_note_ids=[])
            )

    def test_incompatible_link_requires_visible_reason(self):
        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_transition_link(
                _link_payload(
                    compatibility_status=INCOMPATIBLE,
                    transition_id=None,
                    resource_ledger_ids=[],
                    failure_reason=None,
                    caveats=[],
                )
            )

        link = build_behavior_transition_link(
            _link_payload(
                compatibility_status=INCOMPATIBLE,
                transition_id=None,
                resource_ledger_ids=[],
                failure_reason="behavior category mismatch",
                caveats=[],
            )
        )
        self.assertEqual(link.compatibility_status, INCOMPATIBLE)

    def test_executable_payloads_are_rejected(self):
        bad_payloads = (
            {"metadata": {"function_body": "do something"}},
            {"metadata": {"nested": {"__call__": "bad"}}},
            {"metadata": {"callable": lambda: None}},
        )
        for override in bad_payloads:
            with self.subTest(override=override):
                with self.assertRaises(SimulationWiringBuildError):
                    build_behavior_transition_link(_link_payload(**override))


class SimulationBehaviorWiringResultTests(unittest.TestCase):
    def test_result_serializes_and_round_trips(self):
        result = build_behavior_wiring_result(_result_payload())
        rebuilt = build_behavior_wiring_result(behavior_wiring_result_to_dict(result))

        self.assertEqual(behavior_wiring_result_to_dict(rebuilt), behavior_wiring_result_to_dict(result))

    def test_result_is_immutable_and_does_not_mutate_input(self):
        payload = _result_payload(metadata={"nested": {"value": 1}})
        result = build_behavior_wiring_result(payload)
        payload["metadata"]["nested"]["value"] = 99

        with self.assertRaises(FrozenInstanceError):
            result.wiring_result_id = "changed"
        self.assertEqual(behavior_wiring_result_to_dict(result)["metadata"]["nested"]["value"], 1)

    def test_result_rejects_duplicate_link_ids(self):
        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_wiring_result(_result_payload(links=[_link_payload(), _link_payload()]))

    def test_result_requires_matching_simulation_id(self):
        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_wiring_result(_result_payload(links=[_link_payload(simulation_id="other")]))

    def test_compatible_result_rejects_incompatible_links(self):
        incompatible_link = _link_payload(
            compatibility_status=INCOMPATIBLE,
            transition_id=None,
            failure_reason="behavior key mismatch",
        )
        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_wiring_result(_result_payload(links=[incompatible_link]))

    def test_incompatible_result_requires_visible_reason(self):
        incompatible_link = _link_payload(
            compatibility_status=INCOMPATIBLE,
            transition_id=None,
            failure_reason="behavior key mismatch",
        )
        with self.assertRaises(SimulationWiringBuildError):
            build_behavior_wiring_result(
                _result_payload(
                    compatibility_status=INCOMPATIBLE,
                    failure_reason=None,
                    caveats=[],
                    links=[incompatible_link],
                )
            )

    def test_no_runtime_helpers_are_exposed(self):
        import codie.probability_engine.sim_r_wiring as wiring

        forbidden = (
            "execute",
            "apply",
            "mutate",
            "search",
            "run",
            "create_ledger",
            "build_transition_result",
        )
        for name in dir(wiring):
            lowered = name.lower()
            self.assertFalse(any(term in lowered for term in forbidden), name)


if __name__ == "__main__":
    unittest.main()
