"""Deterministic in-memory renderers for presentation/export packets."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .packets import PresentationPacket, presentation_packet_to_dict, validate_presentation_packet


RENDER_FORMATS = frozenset({"json", "markdown"})
MEDIA_TYPES = {
    "json": "application/json",
    "markdown": "text/markdown",
}
FORBIDDEN_RENDER_KEYS = frozenset(
    {
        "path",
        "file_path",
        "output_path",
        "overwrite",
        "receipt",
        "provider_write",
        "provider_write_back",
        "publish",
        "sync",
        "upload",
        "api",
        "route",
        "safe_writer",
    }
)


class PresentationRenderError(ValueError):
    """Raised when a presentation packet cannot be rendered safely."""


@dataclass(frozen=True)
class PresentationRenderOptions:
    render_format: str = "json"
    include_metadata: bool = True
    renderer_version: str = "phase43n-renderer"

    def __post_init__(self) -> None:
        object.__setattr__(self, "render_format", _normalize_format(self.render_format))
        if not isinstance(self.include_metadata, bool):
            raise PresentationRenderError("include_metadata must be a bool")
        _require_text(self.renderer_version, "renderer_version")


@dataclass(frozen=True)
class RenderedPresentationArtifact:
    artifact_id: str
    artifact_class: str
    render_format: str
    media_type: str
    encoding: str
    payload: bytes
    payload_hash: str
    byte_length: int
    source_packet_id: str
    source_snapshot_id: str
    renderer_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.artifact_id, "artifact_id")
        _require_text(self.artifact_class, "artifact_class")
        object.__setattr__(self, "render_format", _normalize_format(self.render_format))
        _require_text(self.media_type, "media_type")
        if self.encoding != "utf-8":
            raise PresentationRenderError("encoding must be utf-8")
        if not isinstance(self.payload, bytes):
            raise PresentationRenderError("payload must be bytes")
        expected_hash = _sha256(self.payload)
        if self.payload_hash != expected_hash:
            raise PresentationRenderError("payload_hash must match payload bytes")
        if self.byte_length != len(self.payload):
            raise PresentationRenderError("byte_length must match payload bytes")
        _require_text(self.source_packet_id, "source_packet_id")
        _require_text(self.source_snapshot_id, "source_snapshot_id")
        _require_text(self.renderer_version, "renderer_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


def render_presentation_packet(packet: PresentationPacket, options: PresentationRenderOptions | None = None) -> RenderedPresentationArtifact:
    resolved = options or PresentationRenderOptions()
    if resolved.render_format == "json":
        return render_presentation_packet_json(packet, resolved)
    if resolved.render_format == "markdown":
        return render_presentation_packet_markdown(packet, resolved)
    raise PresentationRenderError(f"unsupported render_format: {resolved.render_format}")


def render_presentation_packet_json(
    packet: PresentationPacket,
    options: PresentationRenderOptions | None = None,
) -> RenderedPresentationArtifact:
    resolved = options or PresentationRenderOptions(render_format="json")
    resolved = PresentationRenderOptions(render_format="json", include_metadata=resolved.include_metadata, renderer_version=resolved.renderer_version)
    payload_dict = _render_payload_dict(packet, resolved)
    payload = (json.dumps(payload_dict, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    return _artifact(packet, resolved, payload)


def render_presentation_packet_markdown(
    packet: PresentationPacket,
    options: PresentationRenderOptions | None = None,
) -> RenderedPresentationArtifact:
    resolved = options or PresentationRenderOptions(render_format="markdown")
    resolved = PresentationRenderOptions(render_format="markdown", include_metadata=resolved.include_metadata, renderer_version=resolved.renderer_version)
    data = _render_payload_dict(packet, resolved)
    lines = [
        f"# Presentation Packet {data['packet']['packet_id']}",
        "",
        "## Context",
        f"- context_id: {data['packet']['context']['context_id']}",
        f"- snapshot_id: {data['packet']['context']['snapshot_id']}",
        f"- generated_at: {data['packet']['generated_at']}",
        "",
        "## Privacy",
        f"- state: {data['packet']['privacy_state']['state']}",
        f"- redaction_label: {data['packet']['privacy_state']['redaction_label']}",
        f"- reason: {data['packet']['privacy_state']['reason']}",
        "",
        "## Accessibility",
        f"- screen_reader_text: {data['packet']['accessibility_state']['screen_reader_text']}",
        f"- non_color_text: {data['packet']['accessibility_state']['non_color_text']}",
        "",
        "## Status",
    ]
    for item in data["packet"]["status_messages"]:
        lines.append(f"- {item['status_kind']}: {item['text']} / {item['assistive_text']}")
    lines.extend(["", "## Evidence"])
    for item in data["packet"]["evidence_refs"]:
        lines.append(
            "- "
            + f"{item['evidence_ref_id']} | {item['content_class']} | confidence={item['confidence_label']} | "
            + f"source_agreement={item['source_agreement_label']} | source={item['source_system']}:{item['source_ref_type']}"
        )
    lines.extend(
        [
            "",
            "## Render",
            f"- render_format: {data['render_format']}",
            f"- renderer_version: {data['renderer_version']}",
            "- output_authority: inert_payload_only",
            "",
        ]
    )
    payload = "\n".join(lines).encode("utf-8")
    return _artifact(packet, resolved, payload)


def rendered_presentation_artifact_to_dict(artifact: RenderedPresentationArtifact) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "artifact_id": artifact.artifact_id,
            "artifact_class": artifact.artifact_class,
            "render_format": artifact.render_format,
            "media_type": artifact.media_type,
            "encoding": artifact.encoding,
            "payload_hash": artifact.payload_hash,
            "byte_length": artifact.byte_length,
            "source_packet_id": artifact.source_packet_id,
            "source_snapshot_id": artifact.source_snapshot_id,
            "renderer_version": artifact.renderer_version,
            "metadata": artifact.metadata,
        }
    )


def _render_payload_dict(packet: PresentationPacket, options: PresentationRenderOptions) -> dict[str, Any]:
    try:
        validated = validate_presentation_packet(packet)
        packet_dict = presentation_packet_to_dict(validated)
    except Exception as exc:  # noqa: BLE001 - normalize packet-layer failures at renderer boundary.
        raise PresentationRenderError(f"invalid presentation packet: {exc}") from exc
    _reject_render_authority(packet_dict)
    if not options.include_metadata:
        packet_dict = _strip_metadata(packet_dict)
    return _sorted_json_object(
        {
            "packet": packet_dict,
            "render_format": options.render_format,
            "renderer_version": options.renderer_version,
            "output_authority": "inert_payload_only",
        }
    )


def _artifact(packet: PresentationPacket, options: PresentationRenderOptions, payload: bytes) -> RenderedPresentationArtifact:
    packet_dict = presentation_packet_to_dict(packet)
    artifact_class = "presentation_" + options.render_format
    artifact_id = f"render:{options.render_format}:{packet.packet_id}:{packet.context.snapshot_id}"
    return RenderedPresentationArtifact(
        artifact_id=artifact_id,
        artifact_class=artifact_class,
        render_format=options.render_format,
        media_type=MEDIA_TYPES[options.render_format],
        encoding="utf-8",
        payload=payload,
        payload_hash=_sha256(payload),
        byte_length=len(payload),
        source_packet_id=packet.packet_id,
        source_snapshot_id=packet.context.snapshot_id,
        renderer_version=options.renderer_version,
        metadata={"context_type": packet_dict["context"]["context_type"], "output_authority": "inert_payload_only"},
    )


def _strip_metadata(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _strip_metadata(child) for key, child in value.items() if key != "metadata"}
    if isinstance(value, list):
        return [_strip_metadata(child) for child in value]
    return value


def _reject_render_authority(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if _normalize_key(key) in FORBIDDEN_RENDER_KEYS:
                raise PresentationRenderError(f"render payload contains forbidden authority key: {key}")
            _reject_render_authority(child)
    elif isinstance(value, list):
        for child in value:
            _reject_render_authority(child)


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise PresentationRenderError("metadata must be an object")
    _reject_render_authority(metadata)
    return _sorted_json_object(metadata)


def _normalize_format(value: str) -> str:
    text = _require_text(value, "render_format").lower()
    if text not in RENDER_FORMATS:
        raise PresentationRenderError(f"unsupported render_format: {value}")
    return text


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationRenderError(f"{field_name} is required")
    return value.strip()


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
