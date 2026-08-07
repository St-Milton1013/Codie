from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from codie.cli.presentation_export import main
from codie.presentation_export import (
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


def packet(**overrides):
    data = {
        "packet_id": "packet:cli:1",
        "context": build_presentation_context_ref(
            context_id="presentation:cli:deck",
            context_type="deck_analysis",
            snapshot_id="snapshot:cli:1",
            generated_at=GENERATED_AT,
            source_version="phase43t-fixture",
            metadata={"fixture": True},
        ),
        "evidence_refs": (
            build_presentation_evidence_ref(
                evidence_ref_id="evidence:cli:1",
                content_class="measured_evidence",
                source_system="canonical",
                source_ref_type="deck_observation",
                source_ref_id="canonical:cli:deck",
                label="Canonical CLI evidence",
                reviewed=True,
                confidence_label="high_confidence",
                source_agreement_label="strong",
                metadata={"fixture": True},
            ),
        ),
        "privacy_state": build_presentation_privacy_state(
            privacy_state_id="privacy:cli:public",
            state="public",
            exportable=True,
            redaction_label="No redaction",
            reason="Public CLI fixture",
            metadata={"fixture": True},
        ),
        "accessibility_state": build_presentation_accessibility_state(
            accessibility_state_id="accessibility:cli",
            keyboard_reachable=True,
            screen_reader_text="CLI packet is accessible.",
            focus_safe=True,
            reduced_motion_safe=True,
            non_color_text="Ready",
            metadata={"fixture": True},
        ),
        "status_messages": (
            build_presentation_status_message(
                status_id="status:cli",
                status_kind="success",
                text="Ready",
                assistive_text="Ready for CLI rendering.",
                blocking=False,
                metadata={"fixture": True},
            ),
        ),
        "export_intent": build_presentation_export_intent(
            intent_id="export:intent:cli",
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


class PresentationExportCliTest(unittest.TestCase):
    def invoke(self, argv: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                code = main(argv)
            except SystemExit as exc:
                code = int(exc.code)
        return code, stdout.getvalue(), stderr.getvalue()

    def write_packet(self, root: Path, payload: dict | None = None) -> Path:
        packet_path = root / "packet.json"
        packet_payload = payload if payload is not None else presentation_packet_to_dict(packet())
        packet_path.write_text(json.dumps(packet_payload, sort_keys=True), encoding="utf-8")
        return packet_path

    def test_json_packet_input_to_json_artifact_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = self.write_packet(root)
            output_root = root / "out"
            code, stdout, stderr = self.invoke(
                [
                    "render",
                    "--packet-json",
                    str(packet_path),
                    "--format",
                    "json",
                    "--output-root",
                    str(output_root),
                    "--basename",
                    "cli-json",
                    "--create-output-root",
                ]
            )

            self.assertEqual(code, 0, stderr)
            result = json.loads(stdout)
            self.assertEqual(result["render_format"], "json")
            self.assertTrue((output_root / "cli-json.json").exists())
            self.assertTrue((output_root / "cli-json.receipt.json").exists())
            self.assertEqual(result["source_packet_id"], "packet:cli:1")

    def test_json_packet_input_to_markdown_artifact_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = self.write_packet(root)
            output_root = root / "out"
            code, stdout, stderr = self.invoke(
                [
                    "render",
                    "--packet-json",
                    str(packet_path),
                    "--format",
                    "markdown",
                    "--output-root",
                    str(output_root),
                    "--basename",
                    "cli-md",
                    "--create-output-root",
                ]
            )

            self.assertEqual(code, 0, stderr)
            result = json.loads(stdout)
            self.assertEqual(result["media_type"], "text/markdown")
            self.assertTrue((output_root / "cli-md.md").exists())

    def test_stdout_json_is_deterministic_and_concise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = self.write_packet(root)
            first_root = root / "first"
            second_root = root / "second"
            first = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(first_root), "--basename", "same", "--create-output-root"])[1]
            second = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(second_root), "--basename", "same", "--create-output-root"])[1]

            first_payload = json.loads(first)
            second_payload = json.loads(second)
            for key in (
                "artifact_id",
                "source_packet_id",
                "source_snapshot_id",
                "render_format",
                "media_type",
                "payload_hash",
                "byte_length",
                "receipt_id",
                "writer_version",
            ):
                self.assertEqual(first_payload[key], second_payload[key])
            self.assertNotIn("packet", first_payload)
            self.assertNotIn("private", json.dumps(first_payload, sort_keys=True).lower())

    def test_missing_packet_file_malformed_json_and_wrong_shape_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            missing = root / "missing.json"
            code, _, stderr = self.invoke(["render", "--packet-json", str(missing), "--format", "json", "--output-root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("error:", stderr)

            malformed = root / "malformed.json"
            malformed.write_text("{", encoding="utf-8")
            code, _, stderr = self.invoke(["render", "--packet-json", str(malformed), "--format", "json", "--output-root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("error:", stderr)

            wrong = root / "wrong.json"
            wrong.write_text(json.dumps(["not", "object"]), encoding="utf-8")
            code, _, stderr = self.invoke(["render", "--packet-json", str(wrong), "--format", "json", "--output-root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("packet JSON must be an object", stderr)

    def test_invalid_packet_and_secret_metadata_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            invalid_payload = presentation_packet_to_dict(packet())
            invalid_payload["stale_state"] = "stale"
            invalid_packet = self.write_packet(root, invalid_payload)
            code, _, stderr = self.invoke(["render", "--packet-json", str(invalid_packet), "--format", "json", "--output-root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("stale states require stale status text", stderr)

            secret_payload = presentation_packet_to_dict(packet())
            secret_payload["metadata"] = {"token": "blocked"}
            secret_packet = root / "secret.json"
            secret_packet.write_text(json.dumps(secret_payload, sort_keys=True), encoding="utf-8")
            code, _, stderr = self.invoke(["render", "--packet-json", str(secret_packet), "--format", "json", "--output-root", str(root)])
            self.assertEqual(code, 1)
            self.assertIn("forbidden private key", stderr)

    def test_unsupported_format_unsafe_basename_existing_target_and_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = self.write_packet(root)
            output_root = root / "out"
            code, _, stderr = self.invoke(["render", "--packet-json", str(packet_path), "--format", "html", "--output-root", str(output_root)])
            self.assertEqual(code, 2)
            self.assertIn("invalid choice", stderr)

            code, _, stderr = self.invoke(
                ["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(output_root), "--basename", "../bad", "--create-output-root"]
            )
            self.assertEqual(code, 1)
            self.assertIn("basename", stderr)

            ok = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(output_root), "--basename", "same", "--create-output-root"])
            self.assertEqual(ok[0], 0, ok[2])
            code, _, stderr = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(output_root), "--basename", "same"])
            self.assertEqual(code, 1)
            self.assertIn("already exists", stderr)
            code, _, stderr = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(output_root), "--basename", "same", "--overwrite"])
            self.assertEqual(code, 0, stderr)

    def test_create_output_root_and_no_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = self.write_packet(root)
            missing_root = root / "created"
            code, _, stderr = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(missing_root), "--basename", "nope"])
            self.assertEqual(code, 1)
            self.assertIn("output_root does not exist", stderr)

            code, stdout, stderr = self.invoke(
                [
                    "render",
                    "--packet-json",
                    str(packet_path),
                    "--format",
                    "json",
                    "--output-root",
                    str(missing_root),
                    "--basename",
                    "stripped",
                    "--create-output-root",
                    "--no-metadata",
                ]
            )
            self.assertEqual(code, 0, stderr)
            self.assertTrue(json.loads(stdout))
            rendered = (missing_root / "stripped.json").read_text(encoding="utf-8")
            self.assertNotIn('"metadata"', rendered)

    def test_privacy_theory_rules_correction_hareruya_boundaries_are_preserved(self) -> None:
        refs = (
            build_presentation_evidence_ref("evidence:theory", "reviewed_theory", "theory", "claim", "theory:1", "Reviewed Theory", True, "medium", "strong"),
            build_presentation_evidence_ref("evidence:rules", "rules_authority", "rules", "rule", "rule:1", "Rule", True, "high", "strong"),
            build_presentation_evidence_ref("evidence:correction", "correction", "corrections", "correction", "correction:1", "Correction", True, "medium", "strong"),
            build_presentation_evidence_ref("evidence:hareruya", "measured_evidence", "Hareruya", "event", "hareruya:event:1", "Hareruya event", True, "medium", "strong"),
        )
        private_packet = packet(
            evidence_refs=refs,
            privacy_state=build_presentation_privacy_state("privacy:redacted", "redacted", False, "Redacted", "User-local private text omitted"),
            export_intent=None,
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet_path = self.write_packet(root, presentation_packet_to_dict(private_packet))
            output_root = root / "out"
            code, _, stderr = self.invoke(["render", "--packet-json", str(packet_path), "--format", "json", "--output-root", str(output_root), "--basename", "boundary", "--create-output-root"])
            self.assertEqual(code, 0, stderr)
            rendered = (output_root / "boundary.json").read_text(encoding="utf-8")
            self.assertIn("redacted", rendered)
            self.assertIn("reviewed_theory", rendered)
            self.assertIn("rules_authority", rendered)
            self.assertIn("correction", rendered)
            self.assertIn("Hareruya", rendered)

    def test_cli_module_has_no_provider_database_ui_model_or_simulator_imports(self) -> None:
        import codie.cli.presentation_export as cli_module

        source = Path(cli_module.__file__).read_text(encoding="utf-8").lower()
        forbidden = (
            "codie." + "db",
            "codie." + "providers",
            "codie." + "analytics",
            "codie." + "recommendations",
            "codie." + "ingestion",
            "codie." + "cards",
            "codie." + "probability_engine",
            "req" + "uests",
            "ht" + "tpx",
            "sqlite" + "3",
            "fl" + "ask",
            "fast" + "api",
            "uvi" + "corn",
            "star" + "lette",
            "open" + "ai",
            "anth" + "ropic",
            "mox" + "field",
            "arch" + "idekt",
            "scry" + "fall",
            "stream_deck",
        )
        for pattern in forbidden:
            self.assertNotIn(pattern, source)


if __name__ == "__main__":
    unittest.main()
