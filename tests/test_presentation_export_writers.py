from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from codie.presentation_export import (
    PresentationArtifactWriteError,
    PresentationArtifactWriteOptions,
    RenderedPresentationArtifact,
    build_presentation_accessibility_state,
    build_presentation_context_ref,
    build_presentation_evidence_ref,
    build_presentation_export_intent,
    build_presentation_packet,
    build_presentation_privacy_state,
    build_presentation_status_message,
    rendered_presentation_write_receipt_to_dict,
    render_presentation_packet_json,
    render_presentation_packet_markdown,
    write_rendered_presentation_artifact,
)


GENERATED_AT = "2026-08-06T00:00:00+00:00"


def packet(**overrides):
    data = {
        "packet_id": "packet:writer:1",
        "context": build_presentation_context_ref(
            context_id="presentation:deck:writer",
            context_type="deck_analysis",
            snapshot_id="snapshot:writer:1",
            generated_at=GENERATED_AT,
            source_version="phase43q-fixture",
            metadata={"fixture": True},
        ),
        "evidence_refs": (
            build_presentation_evidence_ref(
                evidence_ref_id="evidence:writer:1",
                content_class="measured_evidence",
                source_system="canonical",
                source_ref_type="deck_observation",
                source_ref_id="canonical:deck:writer",
                label="Canonical local evidence",
                reviewed=True,
                confidence_label="high_confidence",
                source_agreement_label="strong",
                metadata={"fixture": True},
            ),
        ),
        "privacy_state": build_presentation_privacy_state(
            privacy_state_id="privacy:public",
            state="public",
            exportable=True,
            redaction_label="No redaction",
            reason="Public local fixture",
            metadata={"fixture": True},
        ),
        "accessibility_state": build_presentation_accessibility_state(
            accessibility_state_id="accessibility:ready",
            keyboard_reachable=True,
            screen_reader_text="Writer packet is accessible.",
            focus_safe=True,
            reduced_motion_safe=True,
            non_color_text="Ready",
            metadata={"fixture": True},
        ),
        "status_messages": (
            build_presentation_status_message(
                status_id="status:ready",
                status_kind="success",
                text="Ready",
                assistive_text="Ready for local writing.",
                blocking=False,
                metadata={"fixture": True},
            ),
        ),
        "export_intent": build_presentation_export_intent(
            intent_id="export:intent:writer",
            artifact_class="evidence_summary",
            requested_format="json",
            exportable=True,
            handoff_only=True,
            safe_writer_required=True,
            metadata={"destination": "safe-writer-request"},
        ),
        "stale_state": "current",
        "conflict_state": "none",
        "legality_state": "legal",
        "generated_at": GENERATED_AT,
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_packet(**data)


class PresentationExportWriterTest(unittest.TestCase):
    def test_writes_json_artifact_and_receipt_under_local_root(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            receipt = write_rendered_presentation_artifact(
                artifact,
                root,
                options=PresentationArtifactWriteOptions(basename="presentation"),
            )

            artifact_path = Path(root) / "presentation.json"
            receipt_path = Path(root) / "presentation.receipt.json"
            self.assertEqual(artifact_path.read_bytes(), artifact.payload)
            receipt_payload = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(receipt_payload["artifact_id"], artifact.artifact_id)
            self.assertEqual(receipt_payload["payload_hash"], artifact.payload_hash)
            self.assertEqual(receipt.files[-1]["path"], "presentation.receipt.json")
            self.assertEqual(receipt.files[-1]["media_type"], "application/json")

    def test_writes_markdown_artifact_with_md_extension(self) -> None:
        artifact = render_presentation_packet_markdown(packet())
        with tempfile.TemporaryDirectory() as root:
            receipt = write_rendered_presentation_artifact(
                artifact,
                root,
                options=PresentationArtifactWriteOptions(basename="presentation-md"),
            )

            self.assertTrue((Path(root) / "presentation-md.md").exists())
            self.assertEqual(receipt.media_type, "text/markdown")

    def test_receipt_dict_is_deterministic_and_excludes_provider_authority(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            first = write_rendered_presentation_artifact(artifact, root, options=PresentationArtifactWriteOptions(basename="one"))
            second = write_rendered_presentation_artifact(artifact, root, options=PresentationArtifactWriteOptions(basename="two"))

            first_payload = rendered_presentation_write_receipt_to_dict(first)
            second_payload = rendered_presentation_write_receipt_to_dict(second)
            self.assertEqual(first_payload["artifact_id"], second_payload["artifact_id"])
            self.assertEqual(first_payload["payload_hash"], second_payload["payload_hash"])
            self.assertNotIn("provider_write", json.dumps(first_payload, sort_keys=True))
            self.assertNotIn("publish", json.dumps(first_payload, sort_keys=True))

    def test_payload_hash_and_byte_length_are_verified_before_write(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            object.__setattr__(artifact, "payload_hash", "sha256:bad")
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, root)
            self.assertEqual(list(Path(root).iterdir()), [])

        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            object.__setattr__(artifact, "byte_length", artifact.byte_length + 1)
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, root)
            self.assertEqual(list(Path(root).iterdir()), [])

    def test_unsupported_media_type_and_encoding_are_rejected(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            object.__setattr__(artifact, "media_type", "text/html")
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, root)

        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            object.__setattr__(artifact, "encoding", "utf-16")
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, root)

    def test_unsafe_basename_path_traversal_and_absolute_paths_are_rejected(self) -> None:
        artifact = render_presentation_packet_json(packet())
        for basename in ("../escape", "nested/name", "C:\\escape", "artifact.json"):
            with self.subTest(basename=basename), tempfile.TemporaryDirectory() as root:
                with self.assertRaises(PresentationArtifactWriteError):
                    write_rendered_presentation_artifact(
                        artifact,
                        root,
                        options=PresentationArtifactWriteOptions(basename=basename),
                    )
                self.assertEqual(list(Path(root).iterdir()), [])

    def test_existing_target_is_rejected_by_default_and_overwrite_is_explicit(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            write_rendered_presentation_artifact(artifact, root, options=PresentationArtifactWriteOptions(basename="presentation"))
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, root, options=PresentationArtifactWriteOptions(basename="presentation"))

            rewritten = write_rendered_presentation_artifact(
                artifact,
                root,
                options=PresentationArtifactWriteOptions(basename="presentation", overwrite=True),
            )
            self.assertTrue(rewritten.overwrite)

    def test_receipt_is_written_last(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            writes: list[str] = []

            def record_write(target: Path, payload: bytes) -> None:
                writes.append(target.name)

            with patch("codie.presentation_export.writers._atomic_write_bytes", side_effect=record_write):
                write_rendered_presentation_artifact(
                    artifact,
                    root,
                    options=PresentationArtifactWriteOptions(basename="ordered"),
                )

            self.assertEqual(writes, ["ordered.json", "ordered.receipt.json"])

    def test_output_root_creation_is_explicit(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            missing = Path(root) / "missing"
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, missing)

            receipt = write_rendered_presentation_artifact(
                artifact,
                missing,
                options=PresentationArtifactWriteOptions(create_output_root=True),
            )
            self.assertTrue((missing / receipt.files[0]["path"]).exists())

    def test_privacy_accessibility_and_boundary_labels_are_preserved_in_payload(self) -> None:
        redacted_packet = packet(
            privacy_state=build_presentation_privacy_state(
                privacy_state_id="privacy:redacted",
                state="redacted",
                exportable=False,
                redaction_label="Redacted",
                reason="User-local private text omitted",
                metadata={"fixture": True},
            ),
            export_intent=None,
        )
        artifact = render_presentation_packet_json(redacted_packet)
        with tempfile.TemporaryDirectory() as root:
            write_rendered_presentation_artifact(artifact, root, options=PresentationArtifactWriteOptions(basename="privacy"))
            payload = (Path(root) / "privacy.json").read_text(encoding="utf-8")

            self.assertIn("redacted", payload)
            self.assertIn("User-local private text omitted", payload)
            self.assertIn("Writer packet is accessible.", payload)
            self.assertIn('"export_intent":null', payload)

    def test_forbidden_provider_publish_stream_deck_and_secret_metadata_are_rejected(self) -> None:
        artifact = render_presentation_packet_json(packet())
        for key in ("provider-write-back", "publish", "sync", "stream-deck-write", "token", "url"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as root:
                with self.assertRaises(PresentationArtifactWriteError):
                    write_rendered_presentation_artifact(
                        artifact,
                        root,
                        options=PresentationArtifactWriteOptions(metadata={key: True}),
                    )

        artifact = render_presentation_packet_json(packet())
        object.__setattr__(artifact, "metadata", {"provider-write-back": True})
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(PresentationArtifactWriteError):
                write_rendered_presentation_artifact(artifact, root)

    def test_writer_module_has_no_provider_network_ui_or_model_runtime(self) -> None:
        import codie.presentation_export.writers as writers_module

        source = Path(writers_module.__file__).read_text(encoding="utf-8")
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
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source.lower())

    def test_receipt_file_hashes_match_returned_file_entries(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with tempfile.TemporaryDirectory() as root:
            receipt = write_rendered_presentation_artifact(
                artifact,
                root,
                options=PresentationArtifactWriteOptions(basename="hashes"),
            )

            for file_entry in receipt.files:
                payload = (Path(root) / file_entry["path"]).read_bytes()
                self.assertEqual(file_entry["bytes_written"], len(payload))
                self.assertEqual(file_entry["payload_hash"], "sha256:" + hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    unittest.main()
