from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codie.presentation_export import (
    PresentationPackageArtifactRef,
    PresentationPackageManifestError,
    PresentationPackageWriteError,
    PresentationPackageWriteOptions,
    build_presentation_package_artifact_ref,
    build_presentation_package_manifest,
    presentation_package_manifest_to_dict,
    presentation_package_write_receipt_to_dict,
    write_presentation_package_manifest,
)
from tests.test_presentation_export_packages import receipts


def manifest():
    json_receipt, md_receipt = receipts()
    return build_presentation_package_manifest(
        (
            build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer"),
            build_presentation_package_artifact_ref(md_receipt, renderer_version="phase43n-renderer"),
        )
    )


class PresentationPackageWriterTest(unittest.TestCase):
    def test_writes_manifest_json_and_receipt_under_local_root(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            receipt = write_presentation_package_manifest(
                package_manifest,
                root,
                options=PresentationPackageWriteOptions(manifest_basename="presentation-package"),
            )

            manifest_path = Path(root) / "presentation-package.package-manifest.json"
            receipt_path = Path(root) / "presentation-package.package-receipt.json"
            self.assertTrue(manifest_path.exists())
            self.assertTrue(receipt_path.exists())
            self.assertEqual(json.loads(manifest_path.read_text(encoding="utf-8")), presentation_package_manifest_to_dict(package_manifest))
            receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt_payload["manifest_id"], package_manifest.manifest_id)
            self.assertEqual(receipt_payload["manifest_version"], package_manifest.manifest_version)
            self.assertEqual(receipt_payload["package_label"], package_manifest.package_label)
            self.assertEqual(receipt.files[-1]["path"], "presentation-package.package-receipt.json")

    def test_manifest_and_receipt_serialization_are_deterministic(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            first = write_presentation_package_manifest(
                package_manifest,
                root,
                options=PresentationPackageWriteOptions(manifest_basename="first"),
            )
            second = write_presentation_package_manifest(
                package_manifest,
                root,
                options=PresentationPackageWriteOptions(manifest_basename="second"),
            )

            first_manifest = (Path(root) / "first.package-manifest.json").read_bytes()
            second_manifest = (Path(root) / "second.package-manifest.json").read_bytes()
            self.assertEqual(first_manifest, second_manifest)
            first_payload = presentation_package_write_receipt_to_dict(first)
            second_payload = presentation_package_write_receipt_to_dict(second)
            self.assertEqual(first_payload["receipt_id"], second_payload["receipt_id"])
            self.assertEqual(first_payload["manifest_payload_hash"], second_payload["manifest_payload_hash"])
            self.assertEqual(first_payload["manifest_byte_length"], second_payload["manifest_byte_length"])

    def test_manifest_validation_hash_and_byte_totals_happen_before_write(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            object.__setattr__(package_manifest, "aggregate_byte_length", package_manifest.aggregate_byte_length + 1)
            with self.assertRaises(PresentationPackageWriteError):
                write_presentation_package_manifest(package_manifest, root)
            self.assertEqual(list(Path(root).iterdir()), [])

        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            object.__setattr__(package_manifest, "aggregate_payload_hash", "sha256:" + "0" * 64)
            with self.assertRaises(PresentationPackageWriteError):
                write_presentation_package_manifest(package_manifest, root)
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_unsafe_basename_absolute_filename_and_traversal_are_rejected(self) -> None:
        package_manifest = manifest()
        for basename in ("../escape", "nested/name", "C:\\escape", "manifest.json"):
            with self.subTest(basename=basename), tempfile.TemporaryDirectory() as root:
                with self.assertRaises(PresentationPackageWriteError):
                    write_presentation_package_manifest(
                        package_manifest,
                        root,
                        options=PresentationPackageWriteOptions(manifest_basename=basename),
                    )
                self.assertEqual(list(Path(root).iterdir()), [])

    def test_existing_targets_are_rejected_by_default_and_overwrite_is_explicit(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            write_presentation_package_manifest(
                package_manifest,
                root,
                options=PresentationPackageWriteOptions(manifest_basename="package"),
            )
            with self.assertRaises(PresentationPackageWriteError):
                write_presentation_package_manifest(
                    package_manifest,
                    root,
                    options=PresentationPackageWriteOptions(manifest_basename="package"),
                )

            rewritten = write_presentation_package_manifest(
                package_manifest,
                root,
                options=PresentationPackageWriteOptions(manifest_basename="package", overwrite=True),
            )
            self.assertTrue(rewritten.overwrite)

    def test_receipt_is_written_last(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            writes: list[str] = []

            def record_write(target: Path, payload: bytes) -> None:
                writes.append(target.name)

            with patch("codie.presentation_export.package_writers._atomic_write_bytes", side_effect=record_write):
                write_presentation_package_manifest(
                    package_manifest,
                    root,
                    options=PresentationPackageWriteOptions(manifest_basename="ordered"),
                )

            self.assertEqual(writes, ["ordered.package-manifest.json", "ordered.package-receipt.json"])

    def test_output_root_creation_is_explicit(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            missing = Path(root) / "missing"
            with self.assertRaises(PresentationPackageWriteError):
                write_presentation_package_manifest(package_manifest, missing)

            receipt = write_presentation_package_manifest(
                package_manifest,
                missing,
                options=PresentationPackageWriteOptions(create_output_root=True),
            )
            self.assertTrue((missing / receipt.files[0]["path"]).exists())

    def test_no_artifact_file_reads_copying_package_directory_or_zip_creation(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            write_presentation_package_manifest(
                package_manifest,
                root,
                options=PresentationPackageWriteOptions(manifest_basename="no-copy"),
            )
            names = sorted(item.name for item in Path(root).iterdir())
            self.assertEqual(names, ["no-copy.package-manifest.json", "no-copy.package-receipt.json"])
            self.assertFalse(any(path.suffix == ".zip" for path in Path(root).iterdir()))

    def test_forbidden_metadata_and_boundary_states_are_preserved_or_rejected(self) -> None:
        package_manifest = manifest()
        for key in (
            "token",
            "provider-write-back",
            "publish",
            "sync",
            "upload",
            "stream-deck-consent",
            "model-prompt",
            "raw-input",
            "database",
            "repository",
            "url",
        ):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as root:
                with self.assertRaises(PresentationPackageWriteError):
                    write_presentation_package_manifest(
                        package_manifest,
                        root,
                        options=PresentationPackageWriteOptions(metadata={"nested": [{key: True}]}),
                    )

        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            write_presentation_package_manifest(package_manifest, root, options=PresentationPackageWriteOptions(manifest_basename="boundaries"))
            payload = (Path(root) / "boundaries.package-manifest.json").read_text(encoding="utf-8")
            self.assertIn("privacy states preserved", payload)
            self.assertIn("accessibility states preserved", payload)

    def test_writer_does_not_mutate_manifest_input(self) -> None:
        package_manifest = manifest()
        before = presentation_package_manifest_to_dict(package_manifest)
        with tempfile.TemporaryDirectory() as root:
            write_presentation_package_manifest(package_manifest, root)
        self.assertEqual(before, presentation_package_manifest_to_dict(package_manifest))

    def test_receipt_file_hashes_match_returned_file_entries(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            receipt = write_presentation_package_manifest(package_manifest, root)
            for file_entry in receipt.files:
                payload = (Path(root) / file_entry["path"]).read_bytes()
                self.assertEqual(file_entry["bytes_written"], len(payload))
                self.assertEqual(file_entry["payload_hash"], "sha256:" + hashlib.sha256(payload).hexdigest())

    def test_writer_module_has_no_provider_network_ui_database_or_model_runtime(self) -> None:
        import codie.presentation_export.package_writers as package_writers_module

        source = Path(package_writers_module.__file__).read_text(encoding="utf-8")
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "codie." + "canonical",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "open" + "ai",
            "anth" + "ropic",
            "fl" + "ask",
            "fast" + "api",
            "uvi" + "corn",
            "star" + "lette",
            "mox" + "field",
            "arch" + "idekt",
            "scry" + "fall",
            "zip" + "file",
            ".read_text(",
            ".read_bytes(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source.lower())

    def test_invalid_receipt_entries_are_rejected(self) -> None:
        package_manifest = manifest()
        with tempfile.TemporaryDirectory() as root:
            receipt = write_presentation_package_manifest(package_manifest, root)
            data = presentation_package_write_receipt_to_dict(receipt)
            data["files"] = ({"path": "../escape.json", "media_type": "application/json", "bytes_written": 1, "payload_hash": "sha256:" + "0" * 64},)
            with self.assertRaises(PresentationPackageWriteError):
                type(receipt)(**data)

    def test_manifest_model_still_rejects_package_scope_mutation(self) -> None:
        package_manifest = manifest()
        data = presentation_package_manifest_to_dict(package_manifest)
        data["artifact_refs"][0]["relative_path"] = "package-directory/artifact.zip"
        with self.assertRaises(PresentationPackageManifestError):
            PresentationPackageArtifactRef(**data["artifact_refs"][0])


if __name__ == "__main__":
    unittest.main()
