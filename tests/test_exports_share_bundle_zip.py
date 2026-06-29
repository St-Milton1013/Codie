from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from codie.cli.user_deck import main
from codie.exports import (
    build_share_bundle_zip_manifest,
    validate_share_bundle_zip_payload,
    write_share_bundle_zip,
)


GENERATED_AT = "2026-06-29T00:00:00+00:00"


class ShareBundleZipExportTest(unittest.TestCase):
    def test_valid_bundle_writes_deterministic_zip(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._write_bundle(root)
            output = root / "bundle.zip"

            result = write_share_bundle_zip(
                bundle_dir=bundle,
                output=output,
                output_root=root,
                generated_at=GENERATED_AT,
            )

            self.assertEqual(result.zip_path, str(output))
            self.assertGreater(result.bytes_written, 0)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                self.assertEqual(names, sorted(names))
                self.assertIn("index.html", names)
                self.assertIn("manifest.json", names)
                self.assertIn("print.html", names)
                self.assertIn("assets/comparison.md", names)
                self.assertIn("zip-manifest.json", names)
                for info in archive.infolist():
                    self.assertEqual(info.date_time, (1980, 1, 1, 0, 0, 0))
                zip_manifest = json.loads(archive.read("zip-manifest.json").decode("utf-8"))
            self.assertEqual(zip_manifest["generated_at"], GENERATED_AT)
            self.assertEqual(zip_manifest["entry_file"], "index.html")
            self.assertEqual(zip_manifest["file_count"], 4)
            self.assertEqual(result.file_count, 4)
            self.assertEqual(zip_manifest["rejected_files"], [])

    def test_manifest_is_deterministic_for_same_input_and_timestamp(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._write_bundle(root)

            first = build_share_bundle_zip_manifest(bundle_dir=bundle, generated_at=GENERATED_AT)
            second = validate_share_bundle_zip_payload(bundle_dir=bundle, generated_at=GENERATED_AT)

            self.assertEqual(first, second)
            self.assertEqual([row["bundle_path"] for row in first["files"]], sorted(row["bundle_path"] for row in first["files"]))

    def test_forbidden_payloads_are_rejected_and_not_zipped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._write_bundle(root)
            (bundle / "codie.sqlite").write_text("database", encoding="utf-8")
            (bundle / ".env").write_text("SECRET=1", encoding="utf-8")
            output = root / "bundle.zip"

            result = write_share_bundle_zip(
                bundle_dir=bundle,
                output=output,
                output_root=root,
                generated_at=GENERATED_AT,
            )

            rejected = {row["bundle_path"]: row["reason"] for row in result.rejected_files}
            self.assertEqual(rejected["codie.sqlite"], "forbidden_payload")
            self.assertEqual(rejected[".env"], "forbidden_payload")
            with zipfile.ZipFile(output) as archive:
                self.assertNotIn("codie.sqlite", archive.namelist())
                self.assertNotIn(".env", archive.namelist())
                manifest = json.loads(archive.read("zip-manifest.json").decode("utf-8"))
            self.assertEqual(len(manifest["rejected_files"]), 2)

    def test_symlink_is_rejected_when_platform_supports_it(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._write_bundle(root)
            target = bundle / "assets" / "comparison.md"
            link = bundle / "assets" / "linked.md"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are not available in this environment")

            manifest = build_share_bundle_zip_manifest(bundle_dir=bundle, generated_at=GENERATED_AT)

            self.assertIn({"bundle_path": "assets/linked.md", "reason": "symlink"}, manifest["rejected_files"])
            self.assertNotIn("assets/linked.md", [row["bundle_path"] for row in manifest["files"]])

    def test_missing_required_files_fail_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / "bundle"
            bundle.mkdir()
            (bundle / "index.html").write_text("<html></html>", encoding="utf-8")

            with self.assertRaises(ValueError):
                build_share_bundle_zip_manifest(bundle_dir=bundle, generated_at=GENERATED_AT)

    def test_output_root_containment_and_zip_suffix_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._write_bundle(root)

            with self.assertRaises(ValueError):
                write_share_bundle_zip(
                    bundle_dir=bundle,
                    output=root.parent / "bundle.zip",
                    output_root=root,
                    generated_at=GENERATED_AT,
                )
            with self.assertRaises(ValueError):
                write_share_bundle_zip(
                    bundle_dir=bundle,
                    output=root / "bundle.txt",
                    output_root=root,
                    generated_at=GENERATED_AT,
                )

    def test_cli_returns_zip_path_and_byte_size(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = self._write_bundle(root)
            output = root / "bundle.zip"

            stdout = StringIO()
            with redirect_stdout(stdout):
                exit_code = main(
                    [
                        "zip-share-bundle",
                        "--bundle-dir",
                        str(bundle),
                        "--output",
                        str(output),
                        "--output-root",
                        str(root),
                        "--generated-at",
                        GENERATED_AT,
                    ]
                )

            self.assertEqual(exit_code, 0)
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["zip_path"], str(output))
            self.assertGreater(payload["bytes_written"], 0)
            self.assertEqual(payload["file_count"], 4)

    def test_zip_export_module_has_no_forbidden_imports(self) -> None:
        import codie.exports.share_bundle_zip as zip_module

        source = Path(zip_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie.providers",
            "codie.db",
            "codie.analytics",
            "codie.recommendations",
            "sqlite3",
            "requests",
            "httpx",
            "discord",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)

    def _write_bundle(self, root: Path) -> Path:
        bundle = root / "bundle"
        assets = bundle / "assets"
        assets.mkdir(parents=True)
        (bundle / "index.html").write_text("<!doctype html><title>Codie</title>\n", encoding="utf-8")
        (bundle / "manifest.json").write_text('{"bundle_version":"1"}\n', encoding="utf-8")
        (bundle / "print.html").write_text("<!doctype html><title>Print</title>\n", encoding="utf-8")
        (assets / "comparison.md").write_text("# Evidence\n", encoding="utf-8")
        return bundle


if __name__ == "__main__":
    unittest.main()
