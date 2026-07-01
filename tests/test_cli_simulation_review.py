from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from codie.cli.simulation_review import build_parser, main
from codie.probability_engine import (
    LineReviewFixture,
    ReviewedAccuracyFilters,
    ReviewedAccuracySummary,
    ReviewReasonCount,
    ReviewStatusCount,
    build_simulation_review_export_bundle,
)


class SimulationReviewCliTest(unittest.TestCase):
    def setUp(self) -> None:
        summary = ReviewedAccuracySummary(
            total_reviews=2,
            reviewed_success_count=1,
            accepted_success_count=1,
            rejected_success_count=0,
            reviewed_failure_count=1,
            reviewed_unsupported_count=0,
            accepted_failure_count=1,
            rejected_failure_count=0,
            status_counts=(ReviewStatusCount("accepted", 2),),
            reason_counts=(ReviewReasonCount("line_valid", 2),),
            affected_card_counts=(("Rhystic Study", 1),),
            affected_action_counts=(("cast_spell", 1),),
            filters=ReviewedAccuracyFilters(deck_hash="deck-1", target_card="Rhystic Study"),
            generated_at="2026-07-01T00:00:00Z",
        )
        fixture = LineReviewFixture(
            review_id="sha256:" + "c" * 64,
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
            created_at="2026-07-01T00:01:00Z",
        )
        self.bundle = build_simulation_review_export_bundle(
            summary,
            [fixture],
            exported_at="2026-07-01T00:02:00Z",
        )

    def test_export_review_bundle_writes_files_and_prints_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_json = root / "bundle.json"
            output_root = root / "out"
            bundle_json.write_text(json.dumps(self.bundle.to_dict(), sort_keys=True), encoding="utf-8")

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "export-review-bundle",
                        "--bundle-json",
                        str(bundle_json),
                        "--output-root",
                        str(output_root),
                    ]
                )

            self.assertEqual(exit_code, 0)
            result = json.loads(stdout.getvalue())
            self.assertEqual(result["bundle_id"], self.bundle.bundle_id)
            self.assertTrue((output_root / "manifest.json").exists())
            self.assertTrue((output_root / "reviewed_accuracy_summary.json").exists())
            self.assertTrue((output_root / "reviewed_accuracy_summary.md").exists())
            self.assertTrue((output_root / "fixtures" / ("c" * 64 + ".json")).exists())
            self.assertGreater(result["bytes_written"], 0)

    def test_export_review_bundle_rejects_non_bundle_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_json = root / "not-bundle.json"
            bundle_json.write_text(json.dumps({"kind": "wrong"}), encoding="utf-8")

            with self.assertRaises(ValueError):
                main(
                    [
                        "export-review-bundle",
                        "--bundle-json",
                        str(bundle_json),
                        "--output-root",
                        str(root / "out"),
                    ]
                )

    def test_export_review_bundle_rejects_missing_bundle_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            with self.assertRaises(FileNotFoundError):
                main(
                    [
                        "export-review-bundle",
                        "--bundle-json",
                        str(root / "missing.json"),
                        "--output-root",
                        str(root / "out"),
                    ]
                )

    def test_export_review_bundle_rejects_malformed_json_and_missing_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            malformed = root / "malformed.json"
            missing_fields = root / "missing-fields.json"
            malformed.write_text("{", encoding="utf-8")
            missing_fields.write_text(json.dumps({"kind": "simulation_review_export_bundle"}), encoding="utf-8")

            with self.assertRaises(json.JSONDecodeError):
                main(
                    [
                        "export-review-bundle",
                        "--bundle-json",
                        str(malformed),
                        "--output-root",
                        str(root / "out"),
                    ]
                )
            with self.assertRaises(ValueError):
                main(
                    [
                        "export-review-bundle",
                        "--bundle-json",
                        str(missing_fields),
                        "--output-root",
                        str(root / "out"),
                    ]
                )

    def test_export_review_bundle_rejects_output_root_that_is_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_json = root / "bundle.json"
            output_file = root / "not-a-directory"
            bundle_json.write_text(json.dumps(self.bundle.to_dict(), sort_keys=True), encoding="utf-8")
            output_file.write_text("occupied", encoding="utf-8")

            with self.assertRaises(ValueError):
                main(
                    [
                        "export-review-bundle",
                        "--bundle-json",
                        str(bundle_json),
                        "--output-root",
                        str(output_file),
                    ]
                )

    def test_parser_requires_output_root(self) -> None:
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args(["export-review-bundle", "--bundle-json", "bundle.json"])

    def test_cli_module_has_no_db_provider_or_recommendation_imports(self) -> None:
        import codie.cli.simulation_review as cli_module

        source = Path(cli_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "recommendations",
            "codie." + "analytics",
            "codie." + "ingestion",
            "codie." + "cards",
            "sql" + "ite3",
            "req" + "uests",
            "ht" + "tpx",
            "source_events",
            "source_decks",
            "provider_objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
