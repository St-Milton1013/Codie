from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from codie.cli.recommendation_output import build_parser, main
from codie.recommendation_output import recommendation_output_bundle_to_dict
from tests.test_recommendation_output_reporting import report_bundle


class RecommendationOutputCliTest(unittest.TestCase):
    def _write_bundle(self, root: Path) -> Path:
        bundle_json = root / "bundle.json"
        bundle_json.write_text(json.dumps(recommendation_output_bundle_to_dict(report_bundle()), sort_keys=True), encoding="utf-8")
        return bundle_json

    def test_render_writes_files_and_prints_concise_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_json = self._write_bundle(root)
            output_root = root / "out"

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "render",
                        "--bundle-json",
                        str(bundle_json),
                        "--format",
                        "both",
                        "--output-root",
                        str(output_root),
                        "--create-output-root",
                    ]
                )

            self.assertEqual(exit_code, 0)
            result = json.loads(stdout.getvalue())
            self.assertEqual(result["source_bundle_id"], "bundle:recommendation-output:1")
            self.assertTrue((output_root / "bundle-recommendation-output-1.recommendation-report.json").exists())
            self.assertTrue((output_root / "bundle-recommendation-output-1.recommendation-report.md").exists())
            self.assertTrue((output_root / "manifest.json").exists())

    def test_parser_requires_bundle_json_format_and_output_root(self) -> None:
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args(["render", "--format", "both", "--output-root", "out"])
        with self.assertRaises(SystemExit):
            parser.parse_args(["render", "--bundle-json", "bundle.json", "--output-root", "out"])
        with self.assertRaises(SystemExit):
            parser.parse_args(["render", "--bundle-json", "bundle.json", "--format", "both"])

    def test_render_rejects_malformed_json_missing_fields_and_unsupported_format(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            malformed = root / "malformed.json"
            missing_fields = root / "missing-fields.json"
            malformed.write_text("{", encoding="utf-8")
            missing_fields.write_text(json.dumps({"bundle_id": "missing-fields"}), encoding="utf-8")

            stderr = StringIO()
            with redirect_stderr(stderr):
                malformed_code = main(
                    [
                        "render",
                        "--bundle-json",
                        str(malformed),
                        "--format",
                        "both",
                        "--output-root",
                        str(root),
                    ]
                )
            self.assertEqual(malformed_code, 1)
            self.assertNotIn("Traceback", stderr.getvalue())

            stderr = StringIO()
            with redirect_stderr(stderr):
                missing_code = main(
                    [
                        "render",
                        "--bundle-json",
                        str(missing_fields),
                        "--format",
                        "both",
                        "--output-root",
                        str(root),
                    ]
                )
            self.assertEqual(missing_code, 1)
            self.assertNotIn("Traceback", stderr.getvalue())

            with self.assertRaises(SystemExit):
                build_parser().parse_args(
                    [
                        "render",
                        "--bundle-json",
                        str(missing_fields),
                        "--format",
                        "html",
                        "--output-root",
                        str(root),
                    ]
                )

    def test_render_rejects_unsafe_output_path_and_missing_root_without_private_payloads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_json = self._write_bundle(root)
            output_file = root / "not-a-dir"
            output_file.write_text("occupied", encoding="utf-8")

            stderr = StringIO()
            with redirect_stderr(stderr):
                file_root_code = main(
                    [
                        "render",
                        "--bundle-json",
                        str(bundle_json),
                        "--format",
                        "both",
                        "--output-root",
                        str(output_file),
                    ]
            )
            self.assertEqual(file_root_code, 1)
            self.assertNotIn("Traceback", stderr.getvalue())
            self.assertNotIn("raw_" + "prov" + "ider_payload", stderr.getvalue())

            stderr = StringIO()
            with redirect_stderr(stderr):
                missing_root_code = main(
                    [
                        "render",
                        "--bundle-json",
                        str(bundle_json),
                        "--format",
                        "both",
                        "--output-root",
                        str(root / "missing"),
                    ]
                )
            self.assertEqual(missing_root_code, 1)
            self.assertIn("create_output_root=True", stderr.getvalue())

    def test_render_supports_single_format_basename_overwrite_and_no_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle_json = self._write_bundle(root)
            output_root = root / "out"
            output_root.mkdir()

            with redirect_stdout(StringIO()):
                first = main(
                    [
                        "render",
                        "--bundle-json",
                        str(bundle_json),
                        "--format",
                        "json",
                        "--output-root",
                        str(output_root),
                        "--basename",
                        "custom-report",
                        "--no-provenance",
                    ]
                )
                second = main(
                    [
                        "render",
                        "--bundle-json",
                        str(bundle_json),
                        "--format",
                        "json",
                        "--output-root",
                        str(output_root),
                        "--basename",
                        "custom-report",
                        "--overwrite",
                        "--no-provenance",
                    ]
                )

            self.assertEqual(first, 0)
            self.assertEqual(second, 0)
            payload = json.loads((output_root / "custom-report.json").read_text(encoding="utf-8"))
            self.assertNotIn("provenance", {section["section_type"] for section in payload["sections"]})
            self.assertFalse((output_root / "custom-report.md").exists())

    def test_cli_module_has_no_forbidden_imports_raw_sql_or_source_reads(self) -> None:
        import codie.cli.recommendation_output as cli_module

        source = Path(cli_module.__file__).read_text(encoding="utf-8")
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
            "raw_" + "prov" + "ider_payload",
            "private_" + "deck_text",
            "full_" + "primer_body",
            "original_" + "import_text",
            "raw_" + "input",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
