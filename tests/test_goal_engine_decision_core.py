"""Contract tests for the advisory-only Read-Only Decision Core."""
import ast
import unittest
from dataclasses import replace
from pathlib import Path

from codie.goal_engine.decision_core import *

T = "2026-08-30T00:00:00Z"
def input_(problem="A bounded issue exists.", evidence=True, intervention="Investigate locally."):
    refs = (DecisionEvidenceReference("evidence:one", "a" * 64, "OBSERVATION", ("Limited evidence.",), DECISION_EVIDENCE_REFERENCE_SCHEMA_VERSION),) if evidence else ()
    return DecisionInput("decision:one", problem, refs, (), (DecisionLimitation("limitation:one", "Uncertainty remains.", DECISION_LIMITATION_SCHEMA_VERSION),), (), (), (), None, None, intervention, (), (), (), (), (), False, T, DECISION_INPUT_SCHEMA_VERSION)

class DecisionCoreTests(unittest.TestCase):
    def test_candidate_is_advisory_not_authority(self):
        result = evaluate_read_only_decision(input_())
        self.assertEqual(result.disposition, "GOAL_CANDIDATE")
        self.assertTrue(result.candidate.advisory)
        self.assertTrue(result.draft_goal_contract.advisory)
        self.assertIn("Human review", result.draft_goal_contract.approval_requirement)
        self.assertIn("no rank", result.priority)
    def test_healthy_idle_prevents_invented_work(self):
        result = evaluate_read_only_decision(input_(problem=None))
        self.assertEqual(result.disposition, "HEALTHY_IDLE")
        self.assertIsNone(result.candidate)
    def test_missing_evidence_prevents_candidate(self):
        self.assertEqual(evaluate_read_only_decision(input_(evidence=False)).disposition, "HEALTHY_IDLE")
    def test_round_trip_and_unknown_field_fail_closed(self):
        value = input_(); self.assertEqual(decision_input_from_dict(decision_input_to_dict(value)), value)
        payload = decision_input_to_dict(value); payload["unexpected"] = True
        with self.assertRaises(GoalEngineDecisionError): decision_input_from_dict(payload)
    def test_immutable_and_canonical(self):
        value = input_(); self.assertEqual(decision_input_semantic_hash(value), decision_input_semantic_hash(replace(value)))
        with self.assertRaises(Exception): value.decision_id = "other"
    def test_no_io_or_later_authority_imports(self):
        tree = ast.parse(Path("codie/goal_engine/decision_core.py").read_text(encoding="utf-8"))
        names = {node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)}
        self.assertFalse(names & {"os", "pathlib", "socket", "subprocess", "requests"})

if __name__ == "__main__": unittest.main()
