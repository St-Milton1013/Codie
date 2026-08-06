"""Pure in-memory presentation/export packets."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


CONTENT_CLASSES = frozenset(
    {
        "measured_evidence",
        "reviewed_theory",
        "unreviewed_theory",
        "rules_authority",
        "correction",
        "user_context",
        "simulation",
        "recommendation",
        "example",
        "unknown",
    }
)

PRIVACY_STATES = frozenset({"public", "local_only", "redacted", "omitted", "blocked", "unavailable", "secret_blocked"})
STATUS_KINDS = frozenset({"success", "warning", "blocking", "redacted", "omitted", "stale", "conflict", "legality", "unsupported"})
STALE_STATES = frozenset({"current", "stale", "unknown"})
CONFLICT_STATES = frozenset({"none", "visible", "blocking", "unknown"})
LEGALITY_STATES = frozenset({"legal", "illegal", "unsupported", "unknown"})
SOURCE_AGREEMENT_STATES = frozenset({"strong", "mixed", "weak", "unknown"})
EXPORT_FORMATS = frozenset({"json", "markdown", "both"})
EXPORT_CLASSES = frozenset({"read_model", "evidence_summary", "decision_packet", "knowledge_vault", "review_bundle"})
HARERUYA_ALLOWED_REF_TYPES = frozenset({"tournament", "event", "deck", "deck_observation"})
FORBIDDEN_AUTHORITY_KEYS = frozenset(
    {
        "path",
        "file_path",
        "output_path",
        "root",
        "overwrite",
        "receipt",
        "writer",
        "renderer",
        "provider_write",
        "provider_write_back",
        "sync",
        "publish",
        "upload",
        "route",
        "api",
        "stream_deck_confirm",
        "stream_deck_consent",
        "stream_deck_write",
        "stream_deck_retry",
    }
)
SECRET_KEYS = frozenset(
    {
        "secret",
        "token",
        "credential",
        "password",
        "api_key",
        "cookie",
        "session",
        "provider_cookie",
        "trace",
        "prompt",
        "chain_of_thought",
        "raw_input",
        "private_deck_text",
        "private_note",
    }
)


class PresentationExportPacketError(ValueError):
    """Raised when presentation/export packets violate their safety contract."""


@dataclass(frozen=True)
class PresentationExportPacketOptions:
    allow_local_export: bool = False
    allow_unreviewed_theory: bool = False
    packet_version: str = "phase43k-packet-model"

    def __post_init__(self) -> None:
        if not isinstance(self.allow_local_export, bool):
            raise PresentationExportPacketError("allow_local_export must be a bool")
        if not isinstance(self.allow_unreviewed_theory, bool):
            raise PresentationExportPacketError("allow_unreviewed_theory must be a bool")
        _require_text(self.packet_version, "packet_version")


@dataclass(frozen=True)
class PresentationContextRef:
    context_id: str
    context_type: str
    snapshot_id: str
    generated_at: str
    source_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.context_id, "context_id")
        _require_text(self.context_type, "context_type")
        _require_text(self.snapshot_id, "snapshot_id")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.source_version, "source_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationEvidenceRef:
    evidence_ref_id: str
    content_class: str
    source_system: str
    source_ref_type: str
    source_ref_id: str
    label: str
    reviewed: bool
    confidence_label: str
    source_agreement_label: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.evidence_ref_id, "evidence_ref_id")
        object.__setattr__(self, "content_class", _normalize_allowed(self.content_class, CONTENT_CLASSES, "content_class"))
        _require_text(self.source_system, "source_system")
        _require_text(self.source_ref_type, "source_ref_type")
        _require_text(self.source_ref_id, "source_ref_id")
        _require_text(self.label, "label")
        if not isinstance(self.reviewed, bool):
            raise PresentationExportPacketError("reviewed must be a bool")
        _require_text(self.confidence_label, "confidence_label")
        object.__setattr__(
            self,
            "source_agreement_label",
            _normalize_allowed(self.source_agreement_label, SOURCE_AGREEMENT_STATES, "source_agreement_label"),
        )
        if self.content_class == "reviewed_theory" and not self.reviewed:
            raise PresentationExportPacketError("reviewed Theory requires reviewed=true")
        if self.content_class == "unreviewed_theory" and self.reviewed:
            raise PresentationExportPacketError("unreviewed Theory cannot be marked reviewed")
        if self.source_system.lower() == "hareruya" and self.source_ref_type.lower() not in HARERUYA_ALLOWED_REF_TYPES:
            raise PresentationExportPacketError("Hareruya references must remain tournament/event/deck provenance")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationPrivacyState:
    privacy_state_id: str
    state: str
    exportable: bool
    redaction_label: str
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.privacy_state_id, "privacy_state_id")
        object.__setattr__(self, "state", _normalize_allowed(self.state, PRIVACY_STATES, "state"))
        if not isinstance(self.exportable, bool):
            raise PresentationExportPacketError("exportable must be a bool")
        _require_text(self.redaction_label, "redaction_label")
        _require_text(self.reason, "reason")
        if self.state != "public" and self.exportable:
            raise PresentationExportPacketError("non-public privacy states are not exportable by default")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationAccessibilityState:
    accessibility_state_id: str
    keyboard_reachable: bool
    screen_reader_text: str
    focus_safe: bool
    reduced_motion_safe: bool
    non_color_text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.accessibility_state_id, "accessibility_state_id")
        for field_name in ("keyboard_reachable", "focus_safe", "reduced_motion_safe"):
            if not isinstance(getattr(self, field_name), bool):
                raise PresentationExportPacketError(f"{field_name} must be a bool")
        _require_text(self.screen_reader_text, "screen_reader_text")
        _require_text(self.non_color_text, "non_color_text")
        if not self.keyboard_reachable or not self.focus_safe:
            raise PresentationExportPacketError("accessibility states must be keyboard reachable and focus safe")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationStatusMessage:
    status_id: str
    status_kind: str
    text: str
    assistive_text: str
    blocking: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.status_id, "status_id")
        object.__setattr__(self, "status_kind", _normalize_allowed(self.status_kind, STATUS_KINDS, "status_kind"))
        _require_text(self.text, "text")
        _require_text(self.assistive_text, "assistive_text")
        if not isinstance(self.blocking, bool):
            raise PresentationExportPacketError("blocking must be a bool")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationExportIntent:
    intent_id: str
    artifact_class: str
    requested_format: str
    exportable: bool
    handoff_only: bool
    safe_writer_required: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.intent_id, "intent_id")
        object.__setattr__(self, "artifact_class", _normalize_allowed(self.artifact_class, EXPORT_CLASSES, "artifact_class"))
        object.__setattr__(self, "requested_format", _normalize_allowed(self.requested_format, EXPORT_FORMATS, "requested_format"))
        for field_name in ("exportable", "handoff_only", "safe_writer_required"):
            if not isinstance(getattr(self, field_name), bool):
                raise PresentationExportPacketError(f"{field_name} must be a bool")
        if self.exportable and (not self.handoff_only or not self.safe_writer_required):
            raise PresentationExportPacketError("export intent must remain inert handoff metadata requiring the safe writer")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class PresentationPacket:
    packet_id: str
    context: PresentationContextRef
    evidence_refs: tuple[PresentationEvidenceRef, ...]
    privacy_state: PresentationPrivacyState
    accessibility_state: PresentationAccessibilityState
    status_messages: tuple[PresentationStatusMessage, ...]
    export_intent: PresentationExportIntent | None
    stale_state: str
    conflict_state: str
    legality_state: str
    generated_at: str
    packet_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.packet_id, "packet_id")
        if not isinstance(self.context, PresentationContextRef):
            raise PresentationExportPacketError("context must be a PresentationContextRef")
        object.__setattr__(self, "evidence_refs", _sort_tuple(self.evidence_refs, "evidence_ref_id", PresentationEvidenceRef))
        if not isinstance(self.privacy_state, PresentationPrivacyState):
            raise PresentationExportPacketError("privacy_state must be a PresentationPrivacyState")
        if not isinstance(self.accessibility_state, PresentationAccessibilityState):
            raise PresentationExportPacketError("accessibility_state must be a PresentationAccessibilityState")
        object.__setattr__(self, "status_messages", _sort_tuple(self.status_messages, "status_id", PresentationStatusMessage))
        if self.export_intent is not None and not isinstance(self.export_intent, PresentationExportIntent):
            raise PresentationExportPacketError("export_intent must be a PresentationExportIntent")
        object.__setattr__(self, "stale_state", _normalize_allowed(self.stale_state, STALE_STATES, "stale_state"))
        object.__setattr__(self, "conflict_state", _normalize_allowed(self.conflict_state, CONFLICT_STATES, "conflict_state"))
        object.__setattr__(self, "legality_state", _normalize_allowed(self.legality_state, LEGALITY_STATES, "legality_state"))
        _require_text(self.generated_at, "generated_at")
        _require_text(self.packet_version, "packet_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        validate_presentation_packet(self)


def build_presentation_context_ref(
    context_id: str,
    context_type: str,
    snapshot_id: str,
    generated_at: str,
    source_version: str,
    metadata: dict[str, Any] | None = None,
) -> PresentationContextRef:
    return PresentationContextRef(context_id, context_type, snapshot_id, generated_at, source_version, metadata or {})


def build_presentation_evidence_ref(
    evidence_ref_id: str,
    content_class: str,
    source_system: str,
    source_ref_type: str,
    source_ref_id: str,
    label: str,
    reviewed: bool,
    confidence_label: str,
    source_agreement_label: str,
    metadata: dict[str, Any] | None = None,
) -> PresentationEvidenceRef:
    return PresentationEvidenceRef(
        evidence_ref_id,
        content_class,
        source_system,
        source_ref_type,
        source_ref_id,
        label,
        reviewed,
        confidence_label,
        source_agreement_label,
        metadata or {},
    )


def build_presentation_privacy_state(
    privacy_state_id: str,
    state: str,
    exportable: bool,
    redaction_label: str,
    reason: str,
    metadata: dict[str, Any] | None = None,
) -> PresentationPrivacyState:
    return PresentationPrivacyState(privacy_state_id, state, exportable, redaction_label, reason, metadata or {})


def build_presentation_accessibility_state(
    accessibility_state_id: str,
    keyboard_reachable: bool,
    screen_reader_text: str,
    focus_safe: bool,
    reduced_motion_safe: bool,
    non_color_text: str,
    metadata: dict[str, Any] | None = None,
) -> PresentationAccessibilityState:
    return PresentationAccessibilityState(
        accessibility_state_id,
        keyboard_reachable,
        screen_reader_text,
        focus_safe,
        reduced_motion_safe,
        non_color_text,
        metadata or {},
    )


def build_presentation_status_message(
    status_id: str,
    status_kind: str,
    text: str,
    assistive_text: str,
    blocking: bool,
    metadata: dict[str, Any] | None = None,
) -> PresentationStatusMessage:
    return PresentationStatusMessage(status_id, status_kind, text, assistive_text, blocking, metadata or {})


def build_presentation_export_intent(
    intent_id: str,
    artifact_class: str,
    requested_format: str,
    exportable: bool,
    handoff_only: bool,
    safe_writer_required: bool,
    metadata: dict[str, Any] | None = None,
) -> PresentationExportIntent:
    return PresentationExportIntent(intent_id, artifact_class, requested_format, exportable, handoff_only, safe_writer_required, metadata or {})


def build_presentation_packet(
    packet_id: str,
    context: PresentationContextRef,
    privacy_state: PresentationPrivacyState,
    accessibility_state: PresentationAccessibilityState,
    status_messages: tuple[PresentationStatusMessage, ...],
    generated_at: str,
    evidence_refs: tuple[PresentationEvidenceRef, ...] = (),
    export_intent: PresentationExportIntent | None = None,
    stale_state: str = "current",
    conflict_state: str = "none",
    legality_state: str = "unknown",
    metadata: dict[str, Any] | None = None,
    options: PresentationExportPacketOptions | None = None,
) -> PresentationPacket:
    resolved_options = options or PresentationExportPacketOptions()
    return PresentationPacket(
        packet_id=packet_id,
        context=context,
        evidence_refs=evidence_refs,
        privacy_state=privacy_state,
        accessibility_state=accessibility_state,
        status_messages=status_messages,
        export_intent=export_intent,
        stale_state=stale_state,
        conflict_state=conflict_state,
        legality_state=legality_state,
        generated_at=generated_at,
        packet_version=resolved_options.packet_version,
        metadata=metadata or {},
    )


def validate_presentation_packet(packet: PresentationPacket) -> PresentationPacket:
    if not packet.context.context_id or not packet.context.snapshot_id:
        raise PresentationExportPacketError("packet requires stable context and snapshot identity")
    if packet.export_intent is not None and not packet.privacy_state.exportable and packet.export_intent.exportable:
        raise PresentationExportPacketError("export intent cannot override privacy_state")
    if packet.export_intent is not None and packet.export_intent.metadata:
        _reject_authority_smuggling(packet.export_intent.metadata)
    if packet.conflict_state != "none" and not any(message.status_kind == "conflict" for message in packet.status_messages):
        raise PresentationExportPacketError("conflict states require conflict status text")
    if packet.stale_state == "stale" and not any(message.status_kind == "stale" for message in packet.status_messages):
        raise PresentationExportPacketError("stale states require stale status text")
    if packet.legality_state in {"illegal", "unsupported"} and not any(message.status_kind in {"legality", "unsupported"} for message in packet.status_messages):
        raise PresentationExportPacketError("legality or unsupported states require status text")
    for ref in packet.evidence_refs:
        if ref.content_class == "unreviewed_theory":
            raise PresentationExportPacketError("unreviewed Theory cannot enter presentation packets")
        if ref.confidence_label == ref.source_agreement_label:
            raise PresentationExportPacketError("confidence and source agreement must remain separate labels")
    return packet


def presentation_context_ref_to_dict(item: PresentationContextRef) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "context_id": item.context_id,
            "context_type": item.context_type,
            "snapshot_id": item.snapshot_id,
            "generated_at": item.generated_at,
            "source_version": item.source_version,
            "metadata": item.metadata,
        }
    )


def presentation_evidence_ref_to_dict(item: PresentationEvidenceRef) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "evidence_ref_id": item.evidence_ref_id,
            "content_class": item.content_class,
            "source_system": item.source_system,
            "source_ref_type": item.source_ref_type,
            "source_ref_id": item.source_ref_id,
            "label": item.label,
            "reviewed": item.reviewed,
            "confidence_label": item.confidence_label,
            "source_agreement_label": item.source_agreement_label,
            "metadata": item.metadata,
        }
    )


def presentation_privacy_state_to_dict(item: PresentationPrivacyState) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "privacy_state_id": item.privacy_state_id,
            "state": item.state,
            "exportable": item.exportable,
            "redaction_label": item.redaction_label,
            "reason": item.reason,
            "metadata": item.metadata,
        }
    )


def presentation_accessibility_state_to_dict(item: PresentationAccessibilityState) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "accessibility_state_id": item.accessibility_state_id,
            "keyboard_reachable": item.keyboard_reachable,
            "screen_reader_text": item.screen_reader_text,
            "focus_safe": item.focus_safe,
            "reduced_motion_safe": item.reduced_motion_safe,
            "non_color_text": item.non_color_text,
            "metadata": item.metadata,
        }
    )


def presentation_status_message_to_dict(item: PresentationStatusMessage) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "status_id": item.status_id,
            "status_kind": item.status_kind,
            "text": item.text,
            "assistive_text": item.assistive_text,
            "blocking": item.blocking,
            "metadata": item.metadata,
        }
    )


def presentation_export_intent_to_dict(item: PresentationExportIntent) -> dict[str, Any]:
    return _sorted_json_object(
        {
            "intent_id": item.intent_id,
            "artifact_class": item.artifact_class,
            "requested_format": item.requested_format,
            "exportable": item.exportable,
            "handoff_only": item.handoff_only,
            "safe_writer_required": item.safe_writer_required,
            "metadata": item.metadata,
        }
    )


def presentation_packet_to_dict(packet: PresentationPacket) -> dict[str, Any]:
    validated = validate_presentation_packet(packet)
    return _sorted_json_object(
        {
            "packet_id": validated.packet_id,
            "context": presentation_context_ref_to_dict(validated.context),
            "evidence_refs": [presentation_evidence_ref_to_dict(item) for item in validated.evidence_refs],
            "privacy_state": presentation_privacy_state_to_dict(validated.privacy_state),
            "accessibility_state": presentation_accessibility_state_to_dict(validated.accessibility_state),
            "status_messages": [presentation_status_message_to_dict(item) for item in validated.status_messages],
            "export_intent": presentation_export_intent_to_dict(validated.export_intent) if validated.export_intent else None,
            "stale_state": validated.stale_state,
            "conflict_state": validated.conflict_state,
            "legality_state": validated.legality_state,
            "generated_at": validated.generated_at,
            "packet_version": validated.packet_version,
            "metadata": validated.metadata,
        }
    )


def _sort_tuple(values: tuple[Any, ...], id_field: str, expected_type: type) -> tuple[Any, ...]:
    for value in values:
        if not isinstance(value, expected_type):
            raise PresentationExportPacketError(f"{id_field} collection contains invalid item")
    return tuple(sorted(values, key=lambda item: getattr(item, id_field)))


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    text = _require_text(value, field_name).lower().replace("-", "_").replace(" ", "_")
    if text not in allowed:
        raise PresentationExportPacketError(f"unsupported {field_name}: {value}")
    return text


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PresentationExportPacketError(f"{field_name} is required")
    return value.strip()


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise PresentationExportPacketError("metadata must be an object")
    validated = _validate_json_value(metadata, "metadata")
    _reject_authority_smuggling(validated)
    return _sorted_json_object(validated)


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise PresentationExportPacketError(f"{path} contains invalid key")
            normalized_key = _normalize_key(key)
            if normalized_key in SECRET_KEYS:
                raise PresentationExportPacketError(f"{path} contains forbidden private key: {key}")
            result[key] = _validate_json_value(child, f"{path}.{key}")
        return result
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _require_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise PresentationExportPacketError(f"{path} must be JSON-compatible")


def _reject_authority_smuggling(metadata: dict[str, Any]) -> None:
    for key, value in metadata.items():
        normalized_key = _normalize_key(key)
        if normalized_key in FORBIDDEN_AUTHORITY_KEYS:
            raise PresentationExportPacketError(f"metadata contains forbidden authority key: {key}")
        if isinstance(value, dict):
            _reject_authority_smuggling(value)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _reject_authority_smuggling(item)


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
