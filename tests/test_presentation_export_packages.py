from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from codie.presentation_export import (
    PresentationPackageManifestError,
    PresentationPackageManifestOptions,
    build_presentation_accessibility_state,
    build_presentation_context_ref,
    build_presentation_evidence_ref,
    build_presentation_export_intent,
    build_presentation_package_artifact_ref,
    build_presentation_package_manifest,
    build_presentation_packet,
    build_presentation_privacy_state,
    build_presentation_status_message,
    presentation_package_artifact_ref_to_dict,
    presentation_package_manifest_to_dict,
    render_presentation_packet_json,
    render_presentation_packet_markdown,
    validate_presentation_package_manifest,
    write_rendered_presentation_artifact,
)


GENERATED_AT = "2026-08-06T00:00:00+00:00"


def packet():
    return build_presentation_packet(
        packet_id="packet:package:1",
        context=build_presentation_context_ref(
            context_id="presentation:deck:package",
            context_type="deck_analysis",
            snapshot_id="snapshot:package:1",
            generated_at=GENERATED_AT,
            source_version="phase43w-fixture",
            metadata={"fixture": True},
        ),
        evidence_refs=(
            build_presentation_evidence_ref(
                evidence_ref_id="evidence:package:1",
                content_class="measured_evidence",
                source_system="hareruya",
                source_ref_type="tournament",
                source_ref_id="hareruya:event:package",
                label="Hareruya tournament evidence",
                reviewed=True,
                confidence_label="high_confidence",
                source_agreement_label="strong",
                metadata={"fixture": True},
            ),
        ),
        privacy_state=build_presentation_privacy_state(
            privacy_state_id="privacy:public",
            state="public",
            exportable=True,
            redaction_label="No redaction",
            reason="Public local fixture",
            metadata={"fixture": True},
        ),
        accessibility_state=build_presentation_accessibility_state(
            accessibility_state_id="accessibility:ready",
            keyboard_reachable=True,
            screen_reader_text="Package manifest packet is accessible.",
            focus_safe=True,
            reduced_motion_safe=True,
            non_color_text="Ready",
            metadata={"fixture": True},
        ),
        status_messages=(
            build_presentation_status_message(
                status_id="status:ready",
                status_kind="success",
                text="Ready",
                assistive_text="Ready for local package manifesting.",
                blocking=False,
                metadata={"fixture": True},
            ),
        ),
        export_intent=build_presentation_export_intent(
            intent_id="export:intent:package",
            artifact_class="evidence_summary",
            requested_format="both",
            exportable=True,
            handoff_only=True,
            safe_writer_required=True,
            metadata={"destination": "safe-writer-request"},
        ),
        stale_state="current",
        conflict_state="none",
        legality_state="legal",
        generated_at=GENERATED_AT,
        metadata={"fixture": True},
    )


def receipts():
    with tempfile.TemporaryDirectory() as root:
        json_receipt = write_rendered_presentation_artifact(
            render_presentation_packet_json(packet()),
            root,
        )
        md_receipt = write_rendered_presentation_artifact(
            render_presentation_packet_markdown(packet()),
            root,
        )
        return json_receipt, md_receipt


class PresentationExportPackageManifestTest(unittest.TestCase):
    def test_builds_manifest_from_json_and_markdown_write_receipts(self) -> None:
        json_receipt, md_receipt = receipts()
        manifest = build_presentation_package_manifest(
            (
                build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer"),
                build_presentation_package_artifact_ref(md_receipt, renderer_version="phase43n-renderer"),
            ),
            options=PresentationPackageManifestOptions(package_label="package-fixture"),
        )

        payload = presentation_package_manifest_to_dict(manifest)
        self.assertEqual(payload["package_label"], "package-fixture")
        self.assertEqual(len(payload["artifact_refs"]), 2)
        self.assertTrue(payload["aggregate_payload_hash"].startswith("sha256:"))
        self.assertEqual(
            payload["aggregate_byte_length"],
            json_receipt.byte_length + md_receipt.byte_length,
        )
        self.assertEqual(tuple(payload["source_packet_ids"]), ("packet:package:1",))

    def test_manifest_serialization_and_aggregate_hash_are_deterministic(self) -> None:
        json_receipt, md_receipt = receipts()
        json_ref = build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer")
        md_ref = build_presentation_package_artifact_ref(md_receipt, renderer_version="phase43n-renderer")

        first = build_presentation_package_manifest((json_ref, md_ref))
        second = build_presentation_package_manifest((md_ref, json_ref))

        self.assertEqual(presentation_package_manifest_to_dict(first), presentation_package_manifest_to_dict(second))
        self.assertEqual(first.aggregate_payload_hash, second.aggregate_payload_hash)
        self.assertEqual([ref.relative_path for ref in first.artifact_refs], sorted(ref.relative_path for ref in first.artifact_refs))

    def test_artifact_ref_uses_relative_local_path_and_does_not_read_files(self) -> None:
        json_receipt, _ = receipts()
        ref = build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer")
        payload = presentation_package_artifact_ref_to_dict(ref)

        self.assertEqual(payload["relative_path"], json_receipt.files[0]["path"])
        self.assertNotIn(json_receipt.root, json.dumps(payload, sort_keys=True))
        self.assertEqual(payload["payload_hash"], json_receipt.payload_hash)
        self.assertEqual(payload["byte_length"], json_receipt.byte_length)

    def test_rejects_absolute_traversal_and_unsafe_package_labels(self) -> None:
        json_receipt, _ = receipts()
        for path in ("/tmp/export.json", "../export.json", "nested\\export.json", "C:/export.json"):
            with self.subTest(path=path), self.assertRaises(PresentationPackageManifestError):
                build_presentation_package_artifact_ref(json_receipt, relative_path=path)

        for label in ("../bundle", "nested/bundle", "C:\\bundle"):
            with self.subTest(label=label), self.assertRaises(PresentationPackageManifestError):
                PresentationPackageManifestOptions(package_label=label)

    def test_rejects_duplicate_paths_and_conflicting_duplicate_artifacts(self) -> None:
        json_receipt, md_receipt = receipts()
        json_ref = build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer")
        md_ref = build_presentation_package_artifact_ref(md_receipt, renderer_version="phase43n-renderer")

        duplicate_path = build_presentation_package_artifact_ref(md_receipt, relative_path=json_ref.relative_path)
        with self.assertRaises(PresentationPackageManifestError):
            build_presentation_package_manifest((json_ref, duplicate_path))

        conflicting = build_presentation_package_artifact_ref(md_receipt, renderer_version="phase43n-renderer")
        object.__setattr__(conflicting, "artifact_id", json_ref.artifact_id)
        self.assertNotEqual(conflicting.payload_hash, json_ref.payload_hash)
        with self.assertRaises(PresentationPackageManifestError):
            build_presentation_package_manifest((json_ref, conflicting))

    def test_rejects_missing_hash_missing_byte_length_unsupported_media_and_encoding(self) -> None:
        json_receipt, _ = receipts()
        ref = build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer")
        for field_name, value in (
            ("payload_hash", ""),
            ("byte_length", -1),
            ("media_type", "text/html"),
            ("encoding", "utf-16"),
        ):
            with self.subTest(field_name=field_name), self.assertRaises(PresentationPackageManifestError):
                data = presentation_package_artifact_ref_to_dict(ref)
                data[field_name] = value
                type(ref)(**data)

    def test_rejects_recursive_secret_provider_publish_stream_deck_and_hidden_context_metadata(self) -> None:
        json_receipt, _ = receipts()
        forbidden_keys = (
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
        )
        for key in forbidden_keys:
            with self.subTest(key=key), self.assertRaises(PresentationPackageManifestError):
                build_presentation_package_artifact_ref(
                    json_receipt,
                    renderer_version="phase43n-renderer",
                    metadata={"nested": [{key: True}]},
                )

    def test_privacy_accessibility_and_boundary_summaries_are_preserved(self) -> None:
        json_receipt, _ = receipts()
        manifest = build_presentation_package_manifest(
            (build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer"),),
            options=PresentationPackageManifestOptions(
                privacy_summary=("redacted, omitted, blocked, and secret-blocked states remain explicit",),
                accessibility_summary=("screen-reader text and non-color statuses remain explicit",),
            ),
        )
        payload = json.dumps(presentation_package_manifest_to_dict(manifest), sort_keys=True)

        self.assertIn("redacted", payload)
        self.assertIn("blocked", payload)
        self.assertIn("screen-reader text", payload)
        self.assertIn("Hareruya", json.dumps(packet().evidence_refs[0].label))

    def test_validate_rejects_tampered_aggregate_values(self) -> None:
        json_receipt, _ = receipts()
        manifest = build_presentation_package_manifest(
            (build_presentation_package_artifact_ref(json_receipt, renderer_version="phase43n-renderer"),)
        )

        object.__setattr__(manifest, "aggregate_byte_length", manifest.aggregate_byte_length + 1)
        with self.assertRaises(PresentationPackageManifestError):
            validate_presentation_package_manifest(manifest)

    def test_package_module_has_no_file_read_provider_network_ui_model_or_simulator_runtime(self) -> None:
        import codie.presentation_export.packages as packages_module

        source = Path(packages_module.__file__).read_text(encoding="utf-8")
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
            ".read_text(",
            ".read_bytes(",
            ".write_text(",
            ".write_bytes(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source.lower())


if __name__ == "__main__":
    unittest.main()
