from __future__ import annotations

import json
import unittest

from codie.presentation_export import (
    PresentationExportPacketError,
    build_presentation_accessibility_state,
    build_presentation_context_ref,
    build_presentation_evidence_ref,
    build_presentation_export_intent,
    build_presentation_packet,
    build_presentation_privacy_state,
    build_presentation_status_message,
    presentation_packet_to_dict,
)


GENERATED_AT = "2026-08-06T00:00:00+00:00"


def context(**overrides):
    data = {
        "context_id": "presentation:deck:1",
        "context_type": "deck_analysis",
        "snapshot_id": "snapshot:accepted:1",
        "generated_at": GENERATED_AT,
        "source_version": "phase43k-fixture",
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
        "metadata": {"window": "fixture"},
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
        "metadata": {"class": "fixture"},
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
        "metadata": {"z": 1, "a": 2},
    }
    data.update(overrides)
    return build_presentation_packet(**data)


class PresentationExportPacketTest(unittest.TestCase):
    def test_packet_serializes_deterministically(self) -> None:
        payload = presentation_packet_to_dict(packet())

        json.dumps(payload, sort_keys=True)
        self.assertEqual(payload["packet_id"], "packet:1")
        self.assertEqual(list(payload["metadata"].keys()), ["a", "z"])

    def test_recursive_secret_token_credential_keys_are_rejected(self) -> None:
        for key in ("secret", "token", "credential", "api-key", "provider cookie"):
            with self.subTest(key=key):
                with self.assertRaises(PresentationExportPacketError):
                    context(metadata={"nested": [{key: "blocked"}]})

    def test_private_local_only_state_cannot_be_exportable(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            privacy(state="local_only", exportable=True)

    def test_export_intent_cannot_override_privacy_state(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            packet(privacy_state=privacy(state="redacted", exportable=False), export_intent=export_intent(exportable=True))

    def test_redacted_omitted_and_blocked_states_are_explicit(self) -> None:
        for state_name in ("redacted", "omitted", "blocked"):
            item = privacy(state=state_name, exportable=False, redaction_label=f"{state_name} label", reason=f"{state_name} reason")
            payload = presentation_packet_to_dict(packet(privacy_state=item, export_intent=None))
            self.assertEqual(payload["privacy_state"]["state"], state_name)
            self.assertIn(state_name, payload["privacy_state"]["reason"])

    def test_content_classes_remain_separate(self) -> None:
        refs = (
            evidence(evidence_ref_id="evidence:measured", content_class="measured_evidence"),
            evidence(evidence_ref_id="evidence:rules", content_class="rules_authority", source_system="rules"),
            evidence(evidence_ref_id="evidence:correction", content_class="correction", source_system="corrections"),
            evidence(evidence_ref_id="evidence:theory", content_class="reviewed_theory", source_system="theory", reviewed=True),
        )
        payload = presentation_packet_to_dict(packet(evidence_refs=refs))

        self.assertEqual(
            [item["content_class"] for item in payload["evidence_refs"]],
            ["correction", "measured_evidence", "rules_authority", "reviewed_theory"],
        )

    def test_confidence_and_source_agreement_cannot_collapse(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            packet(evidence_refs=(evidence(confidence_label="strong", source_agreement_label="strong"),))

    def test_unreviewed_theory_is_rejected(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            packet(evidence_refs=(evidence(content_class="unreviewed_theory", source_system="theory", reviewed=False),))

    def test_reviewed_theory_requires_reviewed_flag(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            evidence(content_class="reviewed_theory", source_system="theory", reviewed=False)

    def test_hareruya_remains_tournament_only(self) -> None:
        good = evidence(source_system="Hareruya", source_ref_type="tournament", source_ref_id="hareruya:event:1")
        payload = presentation_packet_to_dict(packet(evidence_refs=(good,)))
        self.assertEqual(payload["evidence_refs"][0]["source_system"], "Hareruya")

        with self.assertRaises(PresentationExportPacketError):
            evidence(source_system="Hareruya", source_ref_type="theory", source_ref_id="hareruya:theory:1")

    def test_stream_deck_authority_is_rejected(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            export_intent(metadata={"stream-deck-confirm": True})

    def test_writer_renderer_path_provider_publish_and_api_authority_are_rejected(self) -> None:
        for key in ("path", "overwrite", "receipt", "renderer", "writer", "provider-write-back", "sync", "publish", "route", "api"):
            with self.subTest(key=key):
                with self.assertRaises(PresentationExportPacketError):
                    export_intent(metadata={key: True})

    def test_accessibility_text_state_is_required(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            accessibility(screen_reader_text="")
        with self.assertRaises(PresentationExportPacketError):
            accessibility(non_color_text="")
        with self.assertRaises(PresentationExportPacketError):
            accessibility(keyboard_reachable=False)

    def test_stale_conflict_and_legality_states_require_status_text(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            packet(stale_state="stale")
        with self.assertRaises(PresentationExportPacketError):
            packet(conflict_state="visible")
        with self.assertRaises(PresentationExportPacketError):
            packet(legality_state="unsupported")

        stale_payload = presentation_packet_to_dict(packet(stale_state="stale", status_messages=(status(status_kind="stale"),)))
        self.assertEqual(stale_payload["stale_state"], "stale")

    def test_export_intent_remains_inert_safe_writer_handoff(self) -> None:
        with self.assertRaises(PresentationExportPacketError):
            export_intent(exportable=True, handoff_only=False)
        with self.assertRaises(PresentationExportPacketError):
            export_intent(exportable=True, safe_writer_required=False)

    def test_module_has_no_forbidden_imports_io_provider_network_or_ui_runtime(self) -> None:
        import codie.presentation_export.packets as packets_module

        with open(packets_module.__file__, encoding="utf-8") as source_file:
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
