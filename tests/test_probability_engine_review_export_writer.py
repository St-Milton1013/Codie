from __future__ import annotations

import ast
import copy
import json
import tempfile
import unittest
from pathlib import Path

from codie.probability_engine import (
    LineReviewFixture,
    ReviewedAccuracyFilters,
    ReviewedAccuracySummary,
    ReviewReasonCount,
    ReviewStatusCount,
    SimulationReviewExportBundle,
    SimulationReviewExportWriteResult,
    build_simulation_review_export_bundle,
    write_simulation_review_export_bundle,
)


class ProbabilityEngineReviewExportWriterTest(unittest.TestCase):
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
            review_id="sha256:" + "b" * 64,
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
        self.bundle = build_simulation_review_export_bundle(
            self.summary,
            [self.fixture],
            exported_at="2026-06-30T00:02:00Z",
        )

    def test_writer_writes_manifest_json_markdown_and_fixture_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            result = write_simulation_review_export_bundle(self.bundle, root)

            self.assertIsInstance(result, SimulationReviewExportWriteResult)
            self.assertEqual(result.bundle_id, self.bundle.bundle_id)
            self.assertEqual(len(result.files), len(self.bundle.files) + 1)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            summary = json.loads((root / "reviewed_accuracy_summary.json").read_text(encoding="utf-8"))
            markdown = (root / "reviewed_accuracy_summary.md").read_text(encoding="utf-8")
            fixture_path = root / "fixtures" / ("b" * 64 + ".json")
            fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

            self.assertEqual(manifest["bundle_id"], self.bundle.bundle_id)
            self.assertEqual(summary["kind"], "reviewed_simulator_accuracy_summary")
            self.assertTrue(markdown.endswith("\n"))
            self.assertEqual(fixture["action_trace"], self.fixture.action_trace)
            self.assertEqual(result.bytes_written, sum(file["bytes_written"] for file in result.files))

    def test_writer_rejects_absolute_traversal_and_backslash_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for bad_path in ("../escape.json", "/tmp/escape.json", "C:\\tmp\\escape.json", "bad\\path.json"):
                bad_bundle = self._bundle_with_file_path(bad_path)
                with self.subTest(path=bad_path):
                    with self.assertRaises(ValueError):
                        write_simulation_review_export_bundle(bad_bundle, root)

    def test_writer_rejects_duplicate_paths_and_unsupported_content_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            duplicate = SimulationReviewExportBundle(
                bundle_id=self.bundle.bundle_id,
                summary_path=self.bundle.summary_path,
                markdown_path=self.bundle.markdown_path,
                fixture_paths=self.bundle.fixture_paths,
                files=(self.bundle.files[0], self.bundle.files[0]),
                generated_at=self.bundle.generated_at,
                exported_at=self.bundle.exported_at,
            )
            unsupported_file = dict(self.bundle.files[0])
            unsupported_file["path"] = "bad.bin"
            unsupported_file["content_type"] = "application/octet-stream"
            unsupported = SimulationReviewExportBundle(
                bundle_id=self.bundle.bundle_id,
                summary_path=self.bundle.summary_path,
                markdown_path=self.bundle.markdown_path,
                fixture_paths=self.bundle.fixture_paths,
                files=(unsupported_file,),
                generated_at=self.bundle.generated_at,
                exported_at=self.bundle.exported_at,
            )

            with self.assertRaises(ValueError):
                write_simulation_review_export_bundle(duplicate, root)
            with self.assertRaises(ValueError):
                write_simulation_review_export_bundle(unsupported, root)

    def test_writer_validates_before_writing_any_bundle_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            invalid_file = dict(self.bundle.files[-1])
            invalid_file["path"] = "../bad.md"
            invalid = SimulationReviewExportBundle(
                bundle_id=self.bundle.bundle_id,
                summary_path=self.bundle.summary_path,
                markdown_path=self.bundle.markdown_path,
                fixture_paths=self.bundle.fixture_paths,
                files=(*self.bundle.files[:-1], invalid_file),
                generated_at=self.bundle.generated_at,
                exported_at=self.bundle.exported_at,
            )

            with self.assertRaises(ValueError):
                write_simulation_review_export_bundle(invalid, root)

            self.assertFalse((root / "manifest.json").exists())
            self.assertFalse((root / "reviewed_accuracy_summary.json").exists())

    def test_writer_does_not_mutate_bundle(self) -> None:
        before = copy.deepcopy(self.bundle.to_dict())
        with tempfile.TemporaryDirectory() as directory:
            write_simulation_review_export_bundle(self.bundle, Path(directory))

        self.assertEqual(self.bundle.to_dict(), before)

    def test_writer_import_boundary(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "review_export_writer.py"
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

    def test_no_raw_sql_or_strategic_claim_language_in_writer_code(self) -> None:
        path = Path(__file__).resolve().parents[1] / "codie" / "probability_engine" / "review_export_writer.py"
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

    def _bundle_with_file_path(self, path: str) -> SimulationReviewExportBundle:
        file = dict(self.bundle.files[0])
        file["path"] = path
        return SimulationReviewExportBundle(
            bundle_id=self.bundle.bundle_id,
            summary_path=self.bundle.summary_path,
            markdown_path=self.bundle.markdown_path,
            fixture_paths=self.bundle.fixture_paths,
            files=(file,),
            generated_at=self.bundle.generated_at,
            exported_at=self.bundle.exported_at,
        )


if __name__ == "__main__":
    unittest.main()
