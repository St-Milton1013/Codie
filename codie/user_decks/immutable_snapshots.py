"""Pure immutable user deck snapshot packet helpers.

Immutable deck snapshots are local replay/input packets. They do not persist
data, read databases, call providers, calculate analytics, or generate
recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


IMMUTABLE_DECK_SNAPSHOT_VERSION = "immutable-deck-snapshot-v1"

REDACTION_POLICY_REDACTED = "redacted"
REDACTION_POLICY_FULL_CARD_LIST = "full_card_list"

_BLOCKED_PRIVATE_KEYS = frozenset(
    {
        "raw_input",
        "original_import_text",
        "private_deck_text",
        "private_notes",
        "private_user_notes",
        "full_primer_body",
        "primer_body",
        "raw_provider_payload",
        "provider_payload",
    }
)

_REDACTED_PRIVACY_CAVEAT = "card entries omitted by default for user privacy"
_FULL_CARD_LIST_PRIVACY_CAVEAT = "full card list included only by explicit snapshot option"


class ImmutableDeckSnapshotError(ValueError):
    """Raised when a user deck snapshot packet cannot be represented safely."""


@dataclass(frozen=True)
class DeckSnapshotCard:
    """One optional card entry in a full-card-list snapshot."""

    name: str
    quantity: int
    zone: str
    source_order: int
    scryfall_id: str | None = None
    oracle_id: str | None = None


@dataclass(frozen=True)
class DeckSnapshotSourceRef:
    """Sanitized source reference for a user-local snapshot."""

    source_type: str
    source_id: str
    source_url: str | None = None
    metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class DeckSnapshotAnalysisRef:
    """Sanitized analysis/session reference for a user-local snapshot."""

    analysis_id: str
    analysis_type: str
    analysis_profile_id: str | None = None
    analysis_profile_version: str | None = None
    metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class DeckSnapshotPrivacyPolicy:
    """Visible redaction state and privacy caveats for a snapshot."""

    redaction_policy: str
    privacy_caveats: tuple[str, ...]


@dataclass(frozen=True)
class DeckSnapshotReplayMetadata:
    """Versioned replay metadata for reproducing a user-local analysis context."""

    analysis_profile_id: str | None = None
    analysis_profile_version: str | None = None
    weight_profile_id: str | None = None
    weight_profile_version: str | None = None
    evidence_version: str | None = None
    decision_version: str | None = None
    source_snapshot_ids: tuple[str, ...] = ()
    generated_by_phase: str | None = None
    metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class DeckSnapshotWarning:
    """Visible warning attached to a snapshot packet."""

    warning_id: str
    message: str
    severity: str
    metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ImmutableDeckSnapshotOptions:
    """Build options for immutable user deck snapshots."""

    include_card_entries: bool = False


@dataclass(frozen=True)
class ImmutableDeckSnapshot:
    """Immutable user-local deck snapshot packet."""

    snapshot_id: str
    snapshot_version: str
    snapshot_scope: str
    deck_hash: str
    commander_signature: str
    commander_names: tuple[str, ...]
    partner_names: tuple[str, ...]
    source_refs: tuple[DeckSnapshotSourceRef, ...]
    user_deck_ref: str | None
    analysis_refs: tuple[DeckSnapshotAnalysisRef, ...]
    analysis_profile_refs: tuple[str, ...]
    created_at: str
    cards: tuple[DeckSnapshotCard, ...]
    privacy_policy: DeckSnapshotPrivacyPolicy
    privacy_metadata: Mapping[str, Any]
    replay_metadata: DeckSnapshotReplayMetadata | None
    validation_warnings: tuple[DeckSnapshotWarning, ...]
    manual_review_items: tuple[Mapping[str, Any], ...]
    metadata: Mapping[str, Any]


def build_immutable_deck_snapshot(
    *,
    snapshot_id: str,
    snapshot_scope: str,
    deck_hash: str,
    commander_signature: str,
    created_at: str,
    commander_names: tuple[str, ...] | list[str] = (),
    partner_names: tuple[str, ...] | list[str] = (),
    source_refs: tuple[DeckSnapshotSourceRef, ...] | list[DeckSnapshotSourceRef] = (),
    user_deck_ref: str | None = None,
    analysis_refs: tuple[DeckSnapshotAnalysisRef, ...] | list[DeckSnapshotAnalysisRef] = (),
    analysis_profile_refs: tuple[str, ...] | list[str] = (),
    cards: tuple[DeckSnapshotCard, ...] | list[DeckSnapshotCard] = (),
    privacy_metadata: Mapping[str, Any] | None = None,
    replay_metadata: DeckSnapshotReplayMetadata | None = None,
    validation_warnings: tuple[DeckSnapshotWarning, ...] | list[DeckSnapshotWarning] = (),
    manual_review_items: tuple[Mapping[str, Any], ...] | list[Mapping[str, Any]] = (),
    metadata: Mapping[str, Any] | None = None,
    options: ImmutableDeckSnapshotOptions | None = None,
) -> ImmutableDeckSnapshot:
    """Build a deterministic immutable user deck snapshot packet."""

    _require_text(snapshot_id, "snapshot_id")
    _require_text(snapshot_scope, "snapshot_scope")
    _require_text(deck_hash, "deck_hash")
    _require_text(commander_signature, "commander_signature")
    _require_text(created_at, "created_at")
    if user_deck_ref is not None:
        _require_text(user_deck_ref, "user_deck_ref")

    resolved_options = options or ImmutableDeckSnapshotOptions()
    if not isinstance(resolved_options, ImmutableDeckSnapshotOptions):
        raise ImmutableDeckSnapshotError("options must be an ImmutableDeckSnapshotOptions value")

    frozen_cards = _freeze_cards(cards)
    redaction_policy = (
        REDACTION_POLICY_FULL_CARD_LIST if resolved_options.include_card_entries else REDACTION_POLICY_REDACTED
    )
    visible_cards = frozen_cards if resolved_options.include_card_entries else ()
    privacy_caveat = (
        _FULL_CARD_LIST_PRIVACY_CAVEAT
        if resolved_options.include_card_entries
        else _REDACTED_PRIVACY_CAVEAT
    )

    frozen_source_refs = _freeze_source_refs(source_refs)
    frozen_analysis_refs = _freeze_analysis_refs(analysis_refs)
    frozen_warnings = _freeze_warnings(validation_warnings)
    frozen_manual_review_items = _freeze_mapping_sequence(manual_review_items, "manual_review_items")
    frozen_privacy_metadata = _freeze_json(dict(privacy_metadata or {}), "privacy_metadata")
    frozen_metadata = _freeze_json(dict(metadata or {}), "metadata")
    frozen_replay_metadata = _freeze_replay_metadata(replay_metadata)

    snapshot = ImmutableDeckSnapshot(
        snapshot_id=snapshot_id,
        snapshot_version=IMMUTABLE_DECK_SNAPSHOT_VERSION,
        snapshot_scope=snapshot_scope,
        deck_hash=deck_hash,
        commander_signature=commander_signature,
        commander_names=_freeze_text_tuple(commander_names, "commander_names"),
        partner_names=_freeze_text_tuple(partner_names, "partner_names"),
        source_refs=frozen_source_refs,
        user_deck_ref=user_deck_ref,
        analysis_refs=frozen_analysis_refs,
        analysis_profile_refs=_freeze_text_tuple(analysis_profile_refs, "analysis_profile_refs"),
        created_at=created_at,
        cards=visible_cards,
        privacy_policy=DeckSnapshotPrivacyPolicy(
            redaction_policy=redaction_policy,
            privacy_caveats=(privacy_caveat,),
        ),
        privacy_metadata=frozen_privacy_metadata,
        replay_metadata=frozen_replay_metadata,
        validation_warnings=frozen_warnings,
        manual_review_items=frozen_manual_review_items,
        metadata=frozen_metadata,
    )
    validate_immutable_deck_snapshot(snapshot)
    return snapshot


def validate_immutable_deck_snapshot(snapshot: ImmutableDeckSnapshot) -> ImmutableDeckSnapshot:
    """Validate an immutable user deck snapshot packet."""

    if not isinstance(snapshot, ImmutableDeckSnapshot):
        raise ImmutableDeckSnapshotError("snapshot must be an ImmutableDeckSnapshot")
    _require_text(snapshot.snapshot_id, "snapshot_id")
    _require_text(snapshot.snapshot_version, "snapshot_version")
    _require_text(snapshot.snapshot_scope, "snapshot_scope")
    _require_text(snapshot.deck_hash, "deck_hash")
    _require_text(snapshot.commander_signature, "commander_signature")
    _require_text(snapshot.created_at, "created_at")
    if snapshot.privacy_policy.redaction_policy not in {
        REDACTION_POLICY_REDACTED,
        REDACTION_POLICY_FULL_CARD_LIST,
    }:
        raise ImmutableDeckSnapshotError("redaction_policy is invalid")
    if not snapshot.privacy_policy.privacy_caveats:
        raise ImmutableDeckSnapshotError("privacy caveat is required")
    if snapshot.privacy_policy.redaction_policy == REDACTION_POLICY_REDACTED and snapshot.cards:
        raise ImmutableDeckSnapshotError("redacted snapshots must omit card entries")
    _reject_private_keys("privacy_metadata", snapshot.privacy_metadata)
    _reject_private_keys("metadata", snapshot.metadata)
    for index, source_ref in enumerate(snapshot.source_refs):
        _reject_private_keys(f"source_refs[{index}].metadata", source_ref.metadata or {})
    for index, analysis_ref in enumerate(snapshot.analysis_refs):
        _reject_private_keys(f"analysis_refs[{index}].metadata", analysis_ref.metadata or {})
    _reject_blocked_keys_in_replay_metadata(snapshot.replay_metadata)
    for index, warning in enumerate(snapshot.validation_warnings):
        _reject_private_keys(f"validation_warnings[{index}].metadata", warning.metadata or {})
    for index, item in enumerate(snapshot.manual_review_items):
        _reject_private_keys(f"manual_review_items[{index}]", item)
    return snapshot


def immutable_deck_snapshot_to_dict(snapshot: ImmutableDeckSnapshot) -> dict[str, Any]:
    """Serialize a snapshot to a deterministic JSON-compatible dictionary."""

    validate_immutable_deck_snapshot(snapshot)
    serialized: dict[str, Any] = {
        "analysis_profile_refs": list(snapshot.analysis_profile_refs),
        "analysis_refs": [_analysis_ref_to_dict(ref) for ref in snapshot.analysis_refs],
        "commander_names": list(snapshot.commander_names),
        "commander_signature": snapshot.commander_signature,
        "created_at": snapshot.created_at,
        "deck_hash": snapshot.deck_hash,
        "manual_review_items": [_thaw_json(item) for item in snapshot.manual_review_items],
        "metadata": _thaw_json(snapshot.metadata),
        "partner_names": list(snapshot.partner_names),
        "privacy_metadata": _thaw_json(snapshot.privacy_metadata),
        "privacy_policy": {
            "privacy_caveats": list(snapshot.privacy_policy.privacy_caveats),
            "redaction_policy": snapshot.privacy_policy.redaction_policy,
        },
        "replay_metadata": _replay_metadata_to_dict(snapshot.replay_metadata),
        "snapshot_id": snapshot.snapshot_id,
        "snapshot_scope": snapshot.snapshot_scope,
        "snapshot_version": snapshot.snapshot_version,
        "source_refs": [_source_ref_to_dict(ref) for ref in snapshot.source_refs],
        "user_deck_ref": snapshot.user_deck_ref,
        "validation_warnings": [_warning_to_dict(warning) for warning in snapshot.validation_warnings],
    }
    if snapshot.privacy_policy.redaction_policy == REDACTION_POLICY_FULL_CARD_LIST:
        serialized["cards"] = [_card_to_dict(card) for card in snapshot.cards]
    return serialized


def _card_to_dict(card: DeckSnapshotCard) -> dict[str, Any]:
    return {
        "name": card.name,
        "oracle_id": card.oracle_id,
        "quantity": card.quantity,
        "scryfall_id": card.scryfall_id,
        "source_order": card.source_order,
        "zone": card.zone,
    }


def _source_ref_to_dict(source_ref: DeckSnapshotSourceRef) -> dict[str, Any]:
    return {
        "metadata": _thaw_json(source_ref.metadata or {}),
        "source_id": source_ref.source_id,
        "source_type": source_ref.source_type,
        "source_url": source_ref.source_url,
    }


def _analysis_ref_to_dict(analysis_ref: DeckSnapshotAnalysisRef) -> dict[str, Any]:
    return {
        "analysis_id": analysis_ref.analysis_id,
        "analysis_profile_id": analysis_ref.analysis_profile_id,
        "analysis_profile_version": analysis_ref.analysis_profile_version,
        "analysis_type": analysis_ref.analysis_type,
        "metadata": _thaw_json(analysis_ref.metadata or {}),
    }


def _replay_metadata_to_dict(replay_metadata: DeckSnapshotReplayMetadata | None) -> dict[str, Any] | None:
    if replay_metadata is None:
        return None
    return {
        "analysis_profile_id": replay_metadata.analysis_profile_id,
        "analysis_profile_version": replay_metadata.analysis_profile_version,
        "decision_version": replay_metadata.decision_version,
        "evidence_version": replay_metadata.evidence_version,
        "generated_by_phase": replay_metadata.generated_by_phase,
        "metadata": _thaw_json(replay_metadata.metadata or {}),
        "source_snapshot_ids": list(replay_metadata.source_snapshot_ids),
        "weight_profile_id": replay_metadata.weight_profile_id,
        "weight_profile_version": replay_metadata.weight_profile_version,
    }


def _warning_to_dict(warning: DeckSnapshotWarning) -> dict[str, Any]:
    return {
        "message": warning.message,
        "metadata": _thaw_json(warning.metadata or {}),
        "severity": warning.severity,
        "warning_id": warning.warning_id,
    }


def _freeze_cards(cards: tuple[DeckSnapshotCard, ...] | list[DeckSnapshotCard]) -> tuple[DeckSnapshotCard, ...]:
    if not isinstance(cards, (list, tuple)):
        raise ImmutableDeckSnapshotError("cards must be a list or tuple")
    frozen = []
    for index, card in enumerate(cards):
        if not isinstance(card, DeckSnapshotCard):
            raise ImmutableDeckSnapshotError(f"cards[{index}] must be a DeckSnapshotCard")
        _require_text(card.name, f"cards[{index}].name")
        _require_text(card.zone, f"cards[{index}].zone")
        if card.quantity < 1:
            raise ImmutableDeckSnapshotError(f"cards[{index}].quantity must be positive")
        if card.source_order < 0:
            raise ImmutableDeckSnapshotError(f"cards[{index}].source_order must not be negative")
        frozen.append(card)
    return tuple(sorted(frozen, key=lambda item: (item.source_order, item.name, item.zone)))


def _freeze_source_refs(
    source_refs: tuple[DeckSnapshotSourceRef, ...] | list[DeckSnapshotSourceRef],
) -> tuple[DeckSnapshotSourceRef, ...]:
    if not isinstance(source_refs, (list, tuple)):
        raise ImmutableDeckSnapshotError("source_refs must be a list or tuple")
    frozen = []
    for index, source_ref in enumerate(source_refs):
        if not isinstance(source_ref, DeckSnapshotSourceRef):
            raise ImmutableDeckSnapshotError(f"source_refs[{index}] must be a DeckSnapshotSourceRef")
        _require_text(source_ref.source_type, f"source_refs[{index}].source_type")
        _require_text(source_ref.source_id, f"source_refs[{index}].source_id")
        frozen.append(
            DeckSnapshotSourceRef(
                source_type=source_ref.source_type,
                source_id=source_ref.source_id,
                source_url=source_ref.source_url,
                metadata=_freeze_json(dict(source_ref.metadata or {}), f"source_refs[{index}].metadata"),
            )
        )
    return tuple(frozen)


def _freeze_analysis_refs(
    analysis_refs: tuple[DeckSnapshotAnalysisRef, ...] | list[DeckSnapshotAnalysisRef],
) -> tuple[DeckSnapshotAnalysisRef, ...]:
    if not isinstance(analysis_refs, (list, tuple)):
        raise ImmutableDeckSnapshotError("analysis_refs must be a list or tuple")
    frozen = []
    for index, analysis_ref in enumerate(analysis_refs):
        if not isinstance(analysis_ref, DeckSnapshotAnalysisRef):
            raise ImmutableDeckSnapshotError(f"analysis_refs[{index}] must be a DeckSnapshotAnalysisRef")
        _require_text(analysis_ref.analysis_id, f"analysis_refs[{index}].analysis_id")
        _require_text(analysis_ref.analysis_type, f"analysis_refs[{index}].analysis_type")
        frozen.append(
            DeckSnapshotAnalysisRef(
                analysis_id=analysis_ref.analysis_id,
                analysis_type=analysis_ref.analysis_type,
                analysis_profile_id=analysis_ref.analysis_profile_id,
                analysis_profile_version=analysis_ref.analysis_profile_version,
                metadata=_freeze_json(dict(analysis_ref.metadata or {}), f"analysis_refs[{index}].metadata"),
            )
        )
    return tuple(frozen)


def _freeze_warnings(
    warnings: tuple[DeckSnapshotWarning, ...] | list[DeckSnapshotWarning],
) -> tuple[DeckSnapshotWarning, ...]:
    if not isinstance(warnings, (list, tuple)):
        raise ImmutableDeckSnapshotError("validation_warnings must be a list or tuple")
    frozen = []
    for index, warning in enumerate(warnings):
        if not isinstance(warning, DeckSnapshotWarning):
            raise ImmutableDeckSnapshotError(f"validation_warnings[{index}] must be a DeckSnapshotWarning")
        _require_text(warning.warning_id, f"validation_warnings[{index}].warning_id")
        _require_text(warning.message, f"validation_warnings[{index}].message")
        _require_text(warning.severity, f"validation_warnings[{index}].severity")
        frozen.append(
            DeckSnapshotWarning(
                warning_id=warning.warning_id,
                message=warning.message,
                severity=warning.severity,
                metadata=_freeze_json(dict(warning.metadata or {}), f"validation_warnings[{index}].metadata"),
            )
        )
    return tuple(frozen)


def _freeze_mapping_sequence(
    items: tuple[Mapping[str, Any], ...] | list[Mapping[str, Any]],
    field_name: str,
) -> tuple[Mapping[str, Any], ...]:
    if not isinstance(items, (list, tuple)):
        raise ImmutableDeckSnapshotError(f"{field_name} must be a list or tuple")
    frozen = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise ImmutableDeckSnapshotError(f"{field_name}[{index}] must be an object")
        frozen.append(_freeze_json(dict(item), f"{field_name}[{index}]"))
    return tuple(frozen)


def _freeze_replay_metadata(
    replay_metadata: DeckSnapshotReplayMetadata | None,
) -> DeckSnapshotReplayMetadata | None:
    if replay_metadata is None:
        return None
    if not isinstance(replay_metadata, DeckSnapshotReplayMetadata):
        raise ImmutableDeckSnapshotError("replay_metadata must be a DeckSnapshotReplayMetadata value")
    _reject_blocked_keys_in_replay_metadata(replay_metadata)
    return DeckSnapshotReplayMetadata(
        analysis_profile_id=replay_metadata.analysis_profile_id,
        analysis_profile_version=replay_metadata.analysis_profile_version,
        weight_profile_id=replay_metadata.weight_profile_id,
        weight_profile_version=replay_metadata.weight_profile_version,
        evidence_version=replay_metadata.evidence_version,
        decision_version=replay_metadata.decision_version,
        source_snapshot_ids=tuple(replay_metadata.source_snapshot_ids),
        generated_by_phase=replay_metadata.generated_by_phase,
        metadata=_freeze_json(dict(replay_metadata.metadata or {}), "replay_metadata.metadata"),
    )


def _freeze_text_tuple(values: tuple[str, ...] | list[str], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, (list, tuple)):
        raise ImmutableDeckSnapshotError(f"{field_name} must be a list or tuple")
    frozen = []
    for index, value in enumerate(values):
        _require_text(value, f"{field_name}[{index}]")
        frozen.append(value)
    return tuple(frozen)


def _reject_blocked_keys_in_replay_metadata(replay_metadata: DeckSnapshotReplayMetadata | None) -> None:
    if replay_metadata is None:
        return
    _reject_private_keys("replay_metadata.metadata", replay_metadata.metadata or {})
    for index, source_snapshot_id in enumerate(replay_metadata.source_snapshot_ids):
        _require_text(source_snapshot_id, f"replay_metadata.source_snapshot_ids[{index}]")


def _reject_private_keys(path: str, value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            if key_text in _BLOCKED_PRIVATE_KEYS:
                raise ImmutableDeckSnapshotError(f"{path}.{key_text} contains blocked private metadata")
            _reject_private_keys(f"{path}.{key_text}", child)
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_private_keys(f"{path}[{index}]", child)


def _freeze_json(value: Any, path: str) -> Any:
    _reject_private_keys(path, value)
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(value[key], f"{path}.{key}") for key in sorted(value)})
    if isinstance(value, list):
        return tuple(_freeze_json(item, f"{path}[]") for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_json(item, f"{path}[]") for item in value)
    return value


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ImmutableDeckSnapshotError(f"{field_name} is required")
