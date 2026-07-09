from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codie.recommendation_output import (
    RecommendationReportWriteError,
    RecommendationReportWriteOptions,
    recommendation_output_bundle_to_dict,
    write_recommendation_report_files,
)
from tests.test_recommendation_output_reporting import report_bundle


class RecommendationOutputWritersTest(unittest.TestCase):
    def test_writer_requires_recommendation_output_bundle_json_input(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(RecommendationReportWriteError):
                write_recommendation_report_files({"bundle_id": "missing-fields"}, root)
            with self.assertRaises(RecommendationReportWriteError):
                write_recommendation_report_files(["not", "an", "object"], root)  # type: ignore[arg-type]

    def test_writer_writes_json_markdown_and_manifest_last(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = recommendation_output_bundle_to_dict(report_bundle())

            result = write_recommendation_report_files(bundle, root)
            payload = result.to_dict()
            paths = [file["path"] for file in payload["files"]]

            self.assertEqual(paths[-1], "manifest.json")
            self.assertIn("bundle-recommendation-output-1.recommendation-report.json", paths)
            self.assertIn("bundle-recommendation-output-1.recommendation-report.md", paths)
            report_json = json.loads((root / "bundle-recommendation-output-1.recommendation-report.json").read_text(encoding="utf-8"))
            report_markdown = (root / "bundle-recommendation-output-1.recommendation-report.md").read_text(encoding="utf-8")
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(report_json["source_bundle_id"], "bundle:recommendation-output:1")
            self.assertIn("Confidence", report_markdown)
            self.assertIn("Expected impact", report_markdown)
            self.assertIn("UnifiedEvidenceObject IDs", report_markdown)
            self.assertIn("Contradictions", report_markdown)
            self.assertEqual(manifest["source_bundle_id"], "bundle:recommendation-output:1")
            self.assertEqual(manifest["files"][0]["path"], "bundle-recommendation-output-1.recommendation-report.json")

    def test_writer_can_write_single_formats(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = recommendation_output_bundle_to_dict(report_bundle())

            json_result = write_recommendation_report_files(
                bundle,
                root / "json",
                options=RecommendationReportWriteOptions(output_format="json"),
            )
            markdown_result = write_recommendation_report_files(
                bundle,
                root / "markdown",
                options=RecommendationReportWriteOptions(output_format="markdown"),
            )

            self.assertEqual([file["content_type"] for file in json_result.files], ["application/json", "application/json"])
            self.assertEqual([file["content_type"] for file in markdown_result.files], ["text/markdown", "application/json"])
            self.assertFalse((root / "json" / "bundle-recommendation-output-1.recommendation-report.md").exists())
            self.assertFalse((root / "markdown" / "bundle-recommendation-output-1.recommendation-report.json").exists())

    def test_output_root_containment_and_file_root_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            occupied = root / "occupied"
            occupied.write_text("already here", encoding="utf-8")
            bundle = recommendation_output_bundle_to_dict(report_bundle())

            with self.assertRaises(RecommendationReportWriteError):
                write_recommendation_report_files(bundle, occupied)

    def test_path_traversal_and_extension_override_are_rejected(self) -> None:
        with self.assertRaises(RecommendationReportWriteError):
            RecommendationReportWriteOptions(basename="../escape")
        with self.assertRaises(RecommendationReportWriteError):
            RecommendationReportWriteOptions(basename="nested/report")
        with self.assertRaises(RecommendationReportWriteError):
            RecommendationReportWriteOptions(basename="report.json")
        with self.assertRaises(RecommendationReportWriteError):
            RecommendationReportWriteOptions(output_format="html")

    def test_basename_cannot_collide_with_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = recommendation_output_bundle_to_dict(report_bundle())

            with self.assertRaises(RecommendationReportWriteError):
                write_recommendation_report_files(
                    bundle,
                    root,
                    options=RecommendationReportWriteOptions(output_format="json", basename="manifest"),
                )

    def test_overwrite_is_explicit_and_repeated_export_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = recommendation_output_bundle_to_dict(report_bundle())

            first = write_recommendation_report_files(bundle, root)
            first_manifest = (root / "manifest.json").read_text(encoding="utf-8")
            with self.assertRaises(RecommendationReportWriteError):
                write_recommendation_report_files(bundle, root)
            second = write_recommendation_report_files(
                bundle,
                root,
                options=RecommendationReportWriteOptions(overwrite=True),
            )
            second_manifest = (root / "manifest.json").read_text(encoding="utf-8")

            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual([file["path"] for file in first.files], [file["path"] for file in second.files])

    def test_utf8_output_preserves_unicode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = recommendation_output_bundle_to_dict(report_bundle())
            bundle["subject"]["display_name"] = "Tymna / Kraum - 東京"

            write_recommendation_report_files(bundle, root)
            markdown = (root / "bundle-recommendation-output-1.recommendation-report.md").read_text(encoding="utf-8")

            self.assertIn("東京", markdown)

    def test_module_has_no_forbidden_imports_raw_sql_provider_reads_or_cli_scope(self) -> None:
        import codie.recommendation_output.writers as writers_module

        source = Path(writers_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "repositories",
            "codie." + "ingestion",
            "codie." + "canonical",
            "codie." + "analytics",
            "codie." + "cards",
            "codie." + "probability_engine",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "open" + "ai",
            "anth" + "ropic",
            "fl" + "ask",
            "fast" + "api",
            "uvi" + "corn",
            "star" + "lette",
            "SEL" + "ECT ",
            "INS" + "ERT ",
            "UPD" + "ATE ",
            "DEL" + "ETE ",
            "exec" + "ute(",
            "execute" + "script(",
            "source_" + "events",
            "source_" + "decks",
            "source_" + "deck_cards",
            "provider_" + "objects",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
