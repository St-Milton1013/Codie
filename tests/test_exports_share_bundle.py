from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codie.exports import (
    ShareBundleAsset,
    build_share_bundle_manifest,
    share_bundle_index_html,
    write_local_share_bundle,
    write_qr_png,
)


GENERATED_AT = "2026-06-28T00:00:00+00:00"


class ShareBundleExportTest(unittest.TestCase):
    def test_manifest_is_deterministic_and_qr_ready(self) -> None:
        manifest = build_share_bundle_manifest(
            title="Codie Evidence Bundle",
            generated_at=GENERATED_AT,
            assets=(ShareBundleAsset(path="comparison.md", label="Comparison"),),
        )

        self.assertEqual(manifest["bundle_version"], "1")
        self.assertEqual(manifest["entry_file"], "index.html")
        self.assertEqual(manifest["qr_ready_entry"], "index.html")
        self.assertEqual(manifest["assets"][0]["bundle_path"], "assets/comparison.md")
        self.assertIn("static", " ".join(manifest["notes"]).lower())

    def test_manifest_records_explicit_qr_target(self) -> None:
        manifest = build_share_bundle_manifest(
            title="Codie Evidence Bundle",
            generated_at=GENERATED_AT,
            assets=(ShareBundleAsset(path="comparison.md", label="Comparison"),),
            qr_target="http://127.0.0.1:4173/index.html",
            qr_asset_path="assets/bundle-entry-qr.png",
        )

        self.assertEqual(manifest["encoded_targets"], ["http://127.0.0.1:4173/index.html"])
        self.assertEqual(manifest["qr_assets"][0]["bundle_path"], "assets/bundle-entry-qr.png")
        self.assertIn("not encoded", " ".join(manifest["privacy_notes"]))

    def test_index_html_escapes_title_and_asset_labels(self) -> None:
        manifest = build_share_bundle_manifest(
            title="<Codie>",
            generated_at=GENERATED_AT,
            assets=(ShareBundleAsset(path="comparison.md", label="<Comparison>"),),
        )

        html = share_bundle_index_html(manifest)

        self.assertIn("&lt;Codie&gt;", html)
        self.assertIn("&lt;Comparison&gt;", html)
        self.assertNotIn("<Codie>", html)
        self.assertIn("No network service is required", html)

    def test_write_local_share_bundle_copies_assets_and_writes_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "comparison.md"
            report.write_text("# Evidence\n", encoding="utf-8")

            result = write_local_share_bundle(
                title="Codie Evidence Bundle",
                generated_at=GENERATED_AT,
                assets=(ShareBundleAsset(path=str(report), label="Comparison"),),
                output_dir=root / "bundle",
                output_root=root,
            )

            manifest = json.loads((root / "bundle" / "manifest.json").read_text(encoding="utf-8"))
            index = (root / "bundle" / "index.html").read_text(encoding="utf-8")
            copied = root / "bundle" / "assets" / "comparison.md"
            self.assertEqual(result.index_path, str(root / "bundle" / "index.html"))
            self.assertTrue(copied.exists())
            self.assertEqual(copied.read_text(encoding="utf-8"), "# Evidence\n")
            self.assertEqual(manifest["assets"][0]["label"], "Comparison")
            self.assertIn("Codie Evidence Bundle", index)

    def test_write_local_share_bundle_can_include_qr_asset_without_encoding_report_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "comparison.md"
            report.write_text("# Private Deck Evidence\n", encoding="utf-8")

            result = write_local_share_bundle(
                title="Codie Evidence Bundle",
                generated_at=GENERATED_AT,
                assets=(ShareBundleAsset(path=str(report), label="Comparison"),),
                output_dir=root / "bundle",
                output_root=root,
                qr_target="http://127.0.0.1:4173/index.html",
            )

            manifest = json.loads((root / "bundle" / "manifest.json").read_text(encoding="utf-8"))
            qr_asset = root / "bundle" / "assets" / "bundle-entry-qr.png"
            self.assertEqual(result.qr_asset_path, str(qr_asset))
            self.assertTrue(qr_asset.exists())
            self.assertGreater(qr_asset.stat().st_size, 100)
            self.assertEqual(manifest["encoded_targets"], ["http://127.0.0.1:4173/index.html"])
            self.assertNotIn("Private Deck Evidence", json.dumps(manifest))

    def test_write_qr_png_respects_output_root_and_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "qr.png"

            result = write_qr_png("index.html", target, output_root=root)

            self.assertEqual(result, str(target))
            self.assertTrue(target.exists())
            with self.assertRaises(ValueError):
                write_qr_png("index.html", root / "qr.svg", output_root=root)
            with self.assertRaises(ValueError):
                write_qr_png("index.html", root.parent / "qr.png", output_root=root)
            with self.assertRaises(ValueError):
                write_qr_png("", target, output_root=root)
            with self.assertRaises(ValueError):
                write_qr_png("line one\nline two", target, output_root=root)

    def test_output_root_containment_rejects_outside_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            report = root / "comparison.md"
            report.write_text("# Evidence\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                write_local_share_bundle(
                    title="Codie Evidence Bundle",
                    generated_at=GENERATED_AT,
                    assets=(ShareBundleAsset(path=str(report)),),
                    output_dir=root.parent / "outside-bundle",
                    output_root=root,
                )

    def test_invalid_inputs_fail_cleanly(self) -> None:
        with self.assertRaises(ValueError):
            ShareBundleAsset(path="")
        with self.assertRaises(ValueError):
            build_share_bundle_manifest(title="", generated_at=GENERATED_AT, assets=(ShareBundleAsset(path="a.md"),))
        with self.assertRaises(ValueError):
            build_share_bundle_manifest(title="Codie", generated_at=GENERATED_AT, assets=())


if __name__ == "__main__":
    unittest.main()
