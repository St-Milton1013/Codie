from __future__ import annotations

import hashlib
import json
import unittest

from codie.presentation_export import (
    PresentationRenderError,
    PresentationRenderOptions,
    RenderedPresentationArtifact,
    build_presentation_accessibility_state,
    build_presentation_context_ref,
    build_presentation_evidence_ref,
    build_presentation_export_intent,
    build_presentation_packet,
    build_presentation_privacy_state,
    build_presentation_status_message,
    render_presentation_packet,
    render_presentation_packet_json,
    render_presentation_packet_markdown,
    rendered_presentation_artifact_to_dict,
)


GENERATED_AT = "2026-08-06T00:00:00+00:00"


def context(**overrides):
    data = {
        "context_id": "presentation:deck:1",
        "context_type": "deck_analysis",
        "snapshot_id": "snapshot:accepted:1",
        "generated_at": GENERATED_AT,
        "source_version": "phase43n-fixture",
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_context_ref(**data)


def evidence(**overrides):
    data = {
        "evidence_ref_id": "evidence:metric:1",
        "content_class": "measured_evidence",
        "source_system": "canonical",
        "source_ref_type": "deck_observation",
        "source_ref_id": "canonical:deck:1",
        "label": "Canonical tournament observation",
        "reviewed": True,
        "confidence_label": "high_confidence",
        "source_agreement_label": "strong",
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_evidence_ref(**data)


def privacy(**overrides):
    data = {
        "privacy_state_id": "privacy:public",
        "state": "public",
        "exportable": True,
        "redaction_label": "No redaction",
        "reason": "Public fixture evidence",
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_privacy_state(**data)


def accessibility(**overrides):
    data = {
        "accessibility_state_id": "accessibility:ready",
        "keyboard_reachable": True,
        "screen_reader_text": "Packet ready with public evidence.",
        "focus_safe": True,
        "reduced_motion_safe": True,
        "non_color_text": "Ready",
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_accessibility_state(**data)


def status(**overrides):
    data = {
        "status_id": "status:success",
        "status_kind": "success",
        "text": "Ready",
        "assistive_text": "Ready for review.",
        "blocking": False,
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_status_message(**data)


def export_intent(**overrides):
    data = {
        "intent_id": "export:intent:1",
        "artifact_class": "evidence_summary",
        "requested_format": "json",
        "exportable": True,
        "handoff_only": True,
        "safe_writer_required": True,
        "metadata": {"destination": "safe-writer-request"},
    }
    data.update(overrides)
    return build_presentation_export_intent(**data)


def packet(**overrides):
    data = {
        "packet_id": "packet:1",
        "context": context(),
        "evidence_refs": (evidence(),),
        "privacy_state": privacy(),
        "accessibility_state": accessibility(),
        "status_messages": (status(),),
        "export_intent": export_intent(),
        "stale_state": "current",
        "conflict_state": "none",
        "legality_state": "legal",
        "generated_at": GENERATED_AT,
        "metadata": {"fixture": True},
    }
    data.update(overrides)
    return build_presentation_packet(**data)


class PresentationExportRendererTest(unittest.TestCase):
    def test_json_rendering_is_deterministic_utf8_bytes(self) -> None:
        first = render_presentation_packet_json(packet())
        second = render_presentation_packet_json(packet())

        self.assertEqual(first.payload, second.payload)
        self.assertEqual(first.media_type, "application/json")
        self.assertEqual(first.encoding, "utf-8")
        json.loads(first.payload.decode("utf-8"))

    def test_markdown_rendering_is_deterministic_utf8_bytes(self) -> None:
        first = render_presentation_packet_markdown(packet())
        second = render_presentation_packet_markdown(packet())

        self.assertEqual(first.payload, second.payload)
        self.assertEqual(first.media_type, "text/markdown")
        text = first.payload.decode("utf-8")
        self.assertIn("# Presentation Packet packet:1", text)
        self.assertIn("screen_reader_text: Packet ready with public evidence.", text)

    def test_hash_and_byte_length_are_derived_from_payload(self) -> None:
        artifact = render_presentation_packet_json(packet())

        self.assertEqual(artifact.byte_length, len(artifact.payload))
        self.assertEqual(artifact.payload_hash, "sha256:" + hashlib.sha256(artifact.payload).hexdigest())

    def test_artifact_dict_excludes_payload_and_write_authority(self) -> None:
        payload = rendered_presentation_artifact_to_dict(render_presentation_packet_json(packet()))

        self.assertNotIn("payload", payload)
        self.assertNotIn("path", json.dumps(payload, sort_keys=True).lower())
        self.assertEqual(payload["metadata"]["output_authority"], "inert_payload_only")

    def test_redacted_omitted_and_blocked_states_remain_explicit(self) -> None:
        for state_name in ("redacted", "omitted", "blocked"):
            item = privacy(state=state_name, exportable=False, redaction_label=f"{state_name} label", reason=f"{state_name} reason")
            artifact = render_presentation_packet_markdown(packet(privacy_state=item, export_intent=None))
            text = artifact.payload.decode("utf-8")
            self.assertIn(f"state: {state_name}", text)
            self.assertIn(f"reason: {state_name} reason", text)

    def test_secret_token_credential_rejection_remains_enforced(self) -> None:
        with self.assertRaises(Exception):
            context(metadata={"nested": {"token": "blocked"}})

    def test_accessibility_status_text_appears_in_json_and_markdown(self) -> None:
        json_text = render_presentation_packet_json(packet()).payload.decode("utf-8")
        markdown_text = render_presentation_packet_markdown(packet()).payload.decode("utf-8")

        self.assertIn("Packet ready with public evidence.", json_text)
        self.assertIn("Ready for review.", json_text)
        self.assertIn("Packet ready with public evidence.", markdown_text)
        self.assertIn("Ready for review.", markdown_text)

    def test_content_class_confidence_and_source_agreement_are_preserved(self) -> None:
        artifact = render_presentation_packet_json(packet())
        data = json.loads(artifact.payload.decode("utf-8"))
        ref = data["packet"]["evidence_refs"][0]

        self.assertEqual(ref["content_class"], "measured_evidence")
        self.assertEqual(ref["confidence_label"], "high_confidence")
        self.assertEqual(ref["source_agreement_label"], "strong")

    def test_theory_rules_correction_hareruya_boundaries_are_rendered_as_labels(self) -> None:
        refs = (
            evidence(evidence_ref_id="evidence:theory", content_class="reviewed_theory", source_system="theory", reviewed=True),
            evidence(evidence_ref_id="evidence:rules", content_class="rules_authority", source_system="rules"),
            evidence(evidence_ref_id="evidence:correction", content_class="correction", source_system="corrections"),
            evidence(evidence_ref_id="evidence:hareruya", source_system="Hareruya", source_ref_type="event", source_ref_id="hareruya:event:1"),
        )
        text = render_presentation_packet_markdown(packet(evidence_refs=refs)).payload.decode("utf-8")

        self.assertIn("reviewed_theory", text)
        self.assertIn("rules_authority", text)
        self.assertIn("correction", text)
        self.assertIn("source=Hareruya:event", text)

    def test_stream_deck_and_provider_write_authority_is_rejected_before_rendering(self) -> None:
        for key in ("stream-deck-confirm", "provider-write-back", "publish", "sync", "api", "path", "receipt"):
            with self.subTest(key=key):
                with self.assertRaises(Exception):
                    export_intent(metadata={key: True})

    def test_invalid_packet_fails_deterministically(self) -> None:
        with self.assertRaises(Exception):
            packet(stale_state="stale")

    def test_render_presentation_packet_dispatches_by_format(self) -> None:
        json_artifact = render_presentation_packet(packet(), PresentationRenderOptions(render_format="json"))
        markdown_artifact = render_presentation_packet(packet(), PresentationRenderOptions(render_format="markdown"))

        self.assertEqual(json_artifact.render_format, "json")
        self.assertEqual(markdown_artifact.render_format, "markdown")

    def test_artifact_validation_rejects_tampered_hash_or_length(self) -> None:
        artifact = render_presentation_packet_json(packet())
        with self.assertRaises(PresentationRenderError):
            RenderedPresentationArtifact(
                artifact_id=artifact.artifact_id,
                artifact_class=artifact.artifact_class,
                render_format=artifact.render_format,
                media_type=artifact.media_type,
                encoding=artifact.encoding,
                payload=artifact.payload,
                payload_hash="sha256:bad",
                byte_length=artifact.byte_length,
                source_packet_id=artifact.source_packet_id,
                source_snapshot_id=artifact.source_snapshot_id,
                renderer_version=artifact.renderer_version,
            )
        with self.assertRaises(PresentationRenderError):
            RenderedPresentationArtifact(
                artifact_id=artifact.artifact_id,
                artifact_class=artifact.artifact_class,
                render_format=artifact.render_format,
                media_type=artifact.media_type,
                encoding=artifact.encoding,
                payload=artifact.payload,
                payload_hash=artifact.payload_hash,
                byte_length=artifact.byte_length + 1,
                source_packet_id=artifact.source_packet_id,
                source_snapshot_id=artifact.source_snapshot_id,
                renderer_version=artifact.renderer_version,
            )

    def test_renderer_module_has_no_io_provider_network_or_ui_runtime(self) -> None:
        import codie.presentation_export.renderers as renderers_module

        with open(renderers_module.__file__, encoding="utf-8") as source_file:
            source = source_file.read()
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
            "open(",
            "write_text(",
            "write_bytes(",
            "mkdir(",
            "touch(",
            "unlink(",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
