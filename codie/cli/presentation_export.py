"""Local CLI for rendering and writing presentation/export packets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from codie.presentation_export import (
    PresentationArtifactWriteError,
    PresentationArtifactWriteOptions,
    PresentationExportPacketError,
    PresentationRenderError,
    PresentationRenderOptions,
    build_presentation_accessibility_state,
    build_presentation_context_ref,
    build_presentation_evidence_ref,
    build_presentation_export_intent,
    build_presentation_packet,
    build_presentation_privacy_state,
    build_presentation_status_message,
    rendered_presentation_write_receipt_to_dict,
    render_presentation_packet,
    write_rendered_presentation_artifact,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codie-presentation-export")
    subparsers = parser.add_subparsers(dest="command", required=True)
    render = subparsers.add_parser(
        "render",
        help="Render an already-built PresentationPacket JSON into local presentation/export files.",
    )
    render.add_argument("--packet-json", required=True, help="Path to a local PresentationPacket JSON file.")
    render.add_argument("--format", required=True, choices=("json", "markdown", "md"), help="Rendered artifact format.")
    render.add_argument("--output-root", required=True, help="Local output directory for rendered artifact files.")
    render.add_argument("--basename", help="Optional deterministic output basename without extension.")
    render.add_argument("--overwrite", action="store_true", help="Allow replacing existing local output files.")
    render.add_argument("--create-output-root", action="store_true", help="Create output root when it is missing.")
    render.add_argument("--no-metadata", action="store_true", help="Strip metadata fields from the rendered packet payload.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "render":
            result = _render(args)
            print(json.dumps(result, sort_keys=True))
            return 0
    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
        ValueError,
        PresentationArtifactWriteError,
        PresentationExportPacketError,
        PresentationRenderError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.error(f"Unsupported command: {args.command}")
    return 2


def _render(args: argparse.Namespace) -> dict[str, Any]:
    packet = _load_packet_json(Path(args.packet_json))
    render_options = PresentationRenderOptions(
        render_format=_normalize_render_format(args.format),
        include_metadata=not args.no_metadata,
    )
    write_options = PresentationArtifactWriteOptions(
        basename=args.basename,
        overwrite=args.overwrite,
        create_output_root=args.create_output_root,
    )
    artifact = render_presentation_packet(packet, render_options)
    receipt = write_rendered_presentation_artifact(artifact, args.output_root, options=write_options)
    receipt_payload = rendered_presentation_write_receipt_to_dict(receipt)
    return {
        "artifact_id": artifact.artifact_id,
        "source_packet_id": artifact.source_packet_id,
        "source_snapshot_id": artifact.source_snapshot_id,
        "render_format": artifact.render_format,
        "media_type": artifact.media_type,
        "payload_hash": artifact.payload_hash,
        "byte_length": artifact.byte_length,
        "receipt_id": receipt_payload["receipt_id"],
        "files": receipt_payload["files"],
        "writer_version": receipt_payload["writer_version"],
    }


def _load_packet_json(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("packet JSON must be an object")
    return _packet_from_dict(payload)


def _packet_from_dict(payload: dict[str, Any]):
    context_payload = _require_object(payload.get("context"), "context")
    privacy_payload = _require_object(payload.get("privacy_state"), "privacy_state")
    accessibility_payload = _require_object(payload.get("accessibility_state"), "accessibility_state")
    status_payloads = _require_list(payload.get("status_messages"), "status_messages")
    evidence_payloads = _require_list(payload.get("evidence_refs", []), "evidence_refs")
    export_intent_payload = payload.get("export_intent")
    context = build_presentation_context_ref(
        context_id=context_payload["context_id"],
        context_type=context_payload["context_type"],
        snapshot_id=context_payload["snapshot_id"],
        generated_at=context_payload["generated_at"],
        source_version=context_payload["source_version"],
        metadata=context_payload.get("metadata", {}),
    )
    privacy = build_presentation_privacy_state(
        privacy_state_id=privacy_payload["privacy_state_id"],
        state=privacy_payload["state"],
        exportable=privacy_payload["exportable"],
        redaction_label=privacy_payload["redaction_label"],
        reason=privacy_payload["reason"],
        metadata=privacy_payload.get("metadata", {}),
    )
    accessibility = build_presentation_accessibility_state(
        accessibility_state_id=accessibility_payload["accessibility_state_id"],
        keyboard_reachable=accessibility_payload["keyboard_reachable"],
        screen_reader_text=accessibility_payload["screen_reader_text"],
        focus_safe=accessibility_payload["focus_safe"],
        reduced_motion_safe=accessibility_payload["reduced_motion_safe"],
        non_color_text=accessibility_payload["non_color_text"],
        metadata=accessibility_payload.get("metadata", {}),
    )
    statuses = tuple(
        build_presentation_status_message(
            status_id=item["status_id"],
            status_kind=item["status_kind"],
            text=item["text"],
            assistive_text=item["assistive_text"],
            blocking=item["blocking"],
            metadata=item.get("metadata", {}),
        )
        for item in status_payloads
    )
    evidence_refs = tuple(
        build_presentation_evidence_ref(
            evidence_ref_id=item["evidence_ref_id"],
            content_class=item["content_class"],
            source_system=item["source_system"],
            source_ref_type=item["source_ref_type"],
            source_ref_id=item["source_ref_id"],
            label=item["label"],
            reviewed=item["reviewed"],
            confidence_label=item["confidence_label"],
            source_agreement_label=item["source_agreement_label"],
            metadata=item.get("metadata", {}),
        )
        for item in evidence_payloads
    )
    export_intent = None
    if export_intent_payload is not None:
        item = _require_object(export_intent_payload, "export_intent")
        export_intent = build_presentation_export_intent(
            intent_id=item["intent_id"],
            artifact_class=item["artifact_class"],
            requested_format=item["requested_format"],
            exportable=item["exportable"],
            handoff_only=item["handoff_only"],
            safe_writer_required=item["safe_writer_required"],
            metadata=item.get("metadata", {}),
        )
    return build_presentation_packet(
        packet_id=payload["packet_id"],
        context=context,
        evidence_refs=evidence_refs,
        privacy_state=privacy,
        accessibility_state=accessibility,
        status_messages=statuses,
        export_intent=export_intent,
        stale_state=payload.get("stale_state", "current"),
        conflict_state=payload.get("conflict_state", "none"),
        legality_state=payload.get("legality_state", "unknown"),
        generated_at=payload["generated_at"],
        metadata=payload.get("metadata", {}),
    )


def _require_object(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return value


def _normalize_render_format(value: str) -> str:
    normalized = value.lower()
    if normalized == "md":
        normalized = "markdown"
    return normalized


if __name__ == "__main__":
    raise SystemExit(main())
