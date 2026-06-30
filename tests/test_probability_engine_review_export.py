from __future__ import annotations

import ast
import copy
import json
import unittest
from pathlib import Path

from codie.probability_engine import (
    LineReviewFixture,
    ReviewedAccuracyFilters,
    ReviewedAccuracySummary,
    ReviewReasonCount,
    ReviewStatusCount,
    SimulationReviewExportBundle,
    SimulationReviewMarkdownDocument,
    build_simulation_review_export_bundle,
    line_review_fixture_to_json_payload,
    line_review_fixture_to_markdown,
    simulation_review_summary_to_json_payload,
    simulation_review_summary_to_markdown,
)


class ProbabilityEngineReviewExportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.summary = ReviewedAccuracySummary(
            total_reviews=3,
            reviewed_success_count=2,
            accepted_success_count=1,
            rejected_success_count=1,
            reviewed_failure_count=1,
            reviewed_unsupported_count=0,
            accepted_failure_count=1,
            rejected_failure_count=0,
            status_counts=(
                ReviewStatusCount("accepted", 2),
                ReviewStatusCount("mana_modeling_error", 1),
            ),
            reason_counts=(
                ReviewReasonCount("line_valid", 2),
                ReviewReasonCount("mana_pool_error", 1),
            ),
            affected_card_counts=(("Rhystic Study", 2),),
            affected_action_counts=(("tap_for_mana", 1),),
            filters=ReviewedAccuracyFilters(deck_hash="deck-1", target_card="Rhystic Study"),
            generated_at="2026-06-30T00:00:00Z",
        )
        self.fixture = LineReviewFixture(
            review_id="sha256:" + "a" * 64,
            challenge_id="challenge-1",
            deck_hash="deck-1",
            target_condition={
                "target_card": "Rhystic Study",
                "target_zone": "stack",
                "turn": 2,
                "action": "cast",
                "target_card_id": "rhystic_study",
            },
            opening_hand=("Island", "Rhystic Study"),
            simulator_status="success",
            simulator_success=True,
            action_trace={"actions": [{"turn": 1, "action": "play_land"}]},
            review_status="accepted",
            review_reason="line_valid",
            affected_cards=("Rhystic Study",),
            affected_actions=("cast_spell",),
            created_at="2026-06-30T00:01:00Z",
        )

    def test_summary_exports_json_compatible_payload(self) -> None:
        payload = simulation_review_summary_to_json_payload(self.summary, exported_at="2026-06-30T00:02:00Z")

        encoded = json.dumps(payload, sort_keys=True)

        self.assertIn("reviewed_simulator_accuracy_summary", encoded)
        self.assertEqual(payload["summary"]["accepted_success_count"], 1)
        self.assertEqual(payload["filters"]["deck_hash"], "deck-1")

    def test_summary_exports_markdown(self) -> None:
        document = simulation_review_summary_to_markdown(self.summary, exported_at="2026-06-30T00:02:00Z")

        self.assertIsInstance(document, SimulationReviewMarkdownDocument)
        self.assertEqual(document.path, "reviewed_accuracy_summary.md")
        self.assertIn("Reviewed Simulator Accuracy Summary", document.body)
        self.assertIn("Accepted successful lines: 1", document.body)
        self.assertIn("Rejected successful lines: 1", document.body)

    def test_line_review_fixture_exports_json_compatible_payload(self) -> None:
        payload = line_review_fixture_to_json_payload(self.fixture, exported_at="2026-06-30T00:02:00Z")

        encoded = json.dumps(payload, sort_keys=True)

        self.assertIn("simulation_line_review_fixture", encoded)
        self.assertEqual(payload["review_id"], self.fixture.review_id)
        self.assertEqual(payload["challenge_id"], "challenge-1")
        self.assertEqual(payload["action_trace"], self.fixture.action_trace)

    def test_line_review_fixture_exports_markdown(self) -> None:
        document = line_review_fixture_to_markdown(self.fixture, exported_at="2026-06-30T00:02:00Z")

        self.assertEqual(document.path, "fixtures/" + "a" * 64 + ".md")
        self.assertIn("Simulation Line Review Fixture", document.body)
        self.assertIn("Review ID", document.body)
        self.assertIn("Action count: 1", document.body)

    def test_bundle_export_contains_deterministic_bundle_id_and_relative_paths(self) -> None:
        first = build_simulation_review_export_bundle(
            self.summary,
            [self.fixture],
            exported_at="2026-06-30T00:02:00Z",
        )
        second = build_simulation_review_export_bundle(
            self.summary,
            [self.fixture],
            exported_at="2026-06-30T00:02:00Z",
        )

        self.assertIsInstance(first, SimulationReviewExportBundle)
        self.assertEqual(first.bundle_id, second.bundle_id)
        self.assertTrue(first.bundle_id.startswith("sha256:"))
        for file in first.files:
            self.assertFalse(str(file["path"]).startswith("/"))
            self.assertNotIn(":\\", str(file["path"]))

    def test_bundle_payload_preserves_links_and_action_trace_copy(self) -> None:
        bundle = build_simulation_review_export_bundle(
            self.summary,
            [self.fixture],
            exported_at="2026-06-30T00:02:00Z",
        )
        payload = bundle.to_dict()
        fixture_file = next(file for file in payload["files"] if file["path"].endswith(".json") and "fixtures/" in file["path"])

        self.assertEqual(fixture_file["payload"]["review_id"], self.fixture.review_id)
        self.assertEqual(fixture_file["payload"]["challenge_id"], self.fixture.challenge_id)
        self.assertEqual(fixture_file["payload"]["action_trace"], self.fixture.action_trace)

    def test_export_does_not_mutate_summary_or_fixture(self) -> None:
        summary_before = copy.deepcopy(self.summary.to_dict())
        fixture_before = copy.deepcopy(self.fixture.to_dict())

        build_simulation_review_export_bundle(
            self.summary,
            [self.fixture],
            exported_at="2026-06-30T00:02:00Z",
        )

        self.assertEqual(self.summary.to_dict(), summary_before)
        self.assertEqual(self.fixture.to_dict(), fixture_before)

    def test_absolute_markdown_paths_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            simulation_review_summary_to_markdown(
                self.summary,
                exported_at="2026-06-30T00:02:00Z",
                path="C:\\tmp\\bad.md",
            )

    def test_review_export_import_boundary(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "review_export.py"
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
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "req" + "uests",
            "ht" + "tpx",
        }

        self.assertFalse(forbidden.intersection(imports))

    def test_no_raw_sql_or_strategic_claim_language_in_review_export_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "review_export.py"
        text = path.read_text(encoding="utf-8").lower()
        forbidden_phrases = (
            "select ",
            "insert ",
            "update ",
            "delete ",
            "should " + "play",
            "must " + "include",
            "correct " + "card",
            "breaks " + "the format",
            "secretly " + "optimal",
            "cut " + "this",
            "you " + "should",
        )

        self.assertFalse([phrase for phrase in forbidden_phrases if phrase in text])


if __name__ == "__main__":
    unittest.main()
