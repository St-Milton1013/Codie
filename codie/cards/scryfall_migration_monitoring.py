"""Local Scryfall snapshot migration monitoring helpers.

This module compares already-loaded local Scryfall bulk snapshot validation
reports. It does not download data, write files, access SQLite, activate
snapshots, replace card lookup behavior, or generate recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any, Mapping

from .scryfall_bulk_snapshots import ScryfallBulkSnapshotValidationReport


SCRYFALL_MIGRATION_MONITOR_VERSION = "scryfall-migration-monitor-v1"


class ScryfallMigrationMonitoringError(ValueError):
    """Raised when a Scryfall migration report cannot be represented safely."""


@dataclass(frozen=True)
class ScryfallFieldChange:
    field_name: str
    change_type: str
    old_value: Any
    new_value: Any
    scryfall_id: str | None = None
    oracle_id: str | None = None


@dataclass(frozen=True)
class ScryfallEnumChange:
    field_name: str
    enum_value: str
    scryfall_id: str
    oracle_id: str | None
    blocks_activation: bool


@dataclass(frozen=True)
class ScryfallIdentityChange:
    change_type: str
    scryfall_id: str | None
    previous_scryfall_id: str | None
    next_scryfall_id: str | None
    oracle_id: str | None
    previous_oracle_id: str | None
    next_oracle_id: str | None
    previous_name: str | None
    next_name: str | None
    blocks_activation: bool


@dataclass(frozen=True)
class ScryfallMigrationAffectedConsumer:
    consumer_key: str
    reason: str
    severity: str


@dataclass(frozen=True)
class ScryfallMigrationManualReviewItem:
    review_type: str
    severity: str
    reason: str
    scryfall_id: str | None = None
    oracle_id: str | None = None
    field_name: str | None = None
    metadata: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class ScryfallMigrationOptions:
    unknown_fields_block_activation: bool = False
    unknown_enums_block_activation: bool = False
    generated_at: str | None = None
    report_id: str | None = None


@dataclass(frozen=True)
class ScryfallMigrationReport:
    report_id: str
    monitor_version: str
    previous_snapshot_id: str
    next_snapshot_id: str
    previous_content_hash: str
    next_content_hash: str
    generated_at: str | None
    required_field_failures: tuple[str, ...]
    optional_field_changes: tuple[ScryfallFieldChange, ...]
    unknown_field_changes: tuple[ScryfallFieldChange, ...]
    unknown_enum_changes: tuple[ScryfallEnumChange, ...]
    identity_changes: tuple[ScryfallIdentityChange, ...]
    schema_breaking_conditions: tuple[str, ...]
    activation_blocked: bool
    activation_block_reasons: tuple[str, ...]
    affected_consumers: tuple[ScryfallMigrationAffectedConsumer, ...]
    manual_review_items: tuple[ScryfallMigrationManualReviewItem, ...]
    validation_errors: tuple[str, ...]
    validation_warnings: tuple[str, ...]


_REQUIRED_FIELDS = ("id", "name")
_OPTIONAL_MONITORED_FIELDS = (
    "oracle_id",
    "released_at",
    "legalities",
    "card_faces",
    "produced_mana",
    "layout",
    "type_line",
    "mana_cost",
    "color_identity",
)
_KNOWN_FIELDS = frozenset(
    {
        "id",
        "scryfall_id",
        "name",
        "oracle_id",
        "released_at",
        "legalities",
        "card_faces",
        "produced_mana",
        "layout",
        "type_line",
        "mana_cost",
        "color_identity",
        "games",
        "finishes",
        "promo_types",
        "frame_effects",
        "security_stamp",
        "border_color",
        "rarity",
    }
)
_KNOWN_ENUM_VALUES = {
    "border_color": frozenset({"black", "borderless", "gold", "silver", "white"}),
    "finishes": frozenset({"foil", "nonfoil", "etched"}),
    "frame_effects": frozenset(
        {
            "colorshifted",
            "compasslanddfc",
            "convertdfc",
            "devoid",
            "draft",
            "etched",
            "extendedart",
            "fandfc",
            "inverted",
            "legendary",
            "lesson",
            "miracle",
            "mooneldrazidfc",
            "nyxtouched",
            "originpwdfc",
            "showcase",
            "snow",
            "spree",
            "sunmoondfc",
            "tombstone",
            "upsidedowndfc",
            "waxingandwaningmoondfc",
        }
    ),
    "games": frozenset({"paper", "arena", "mtgo"}),
    "layout": frozenset(
        {
            "adventure",
            "art_series",
            "augment",
            "battle",
            "class",
            "double_faced_token",
            "emblem",
            "flip",
            "host",
            "leveler",
            "meld",
            "modal_dfc",
            "mutate",
            "normal",
            "planar",
            "prototype",
            "reversible_card",
            "saga",
            "scheme",
            "split",
            "token",
            "transform",
            "vanguard",
        }
    ),
    "legalities": frozenset({"legal", "not_legal", "banned", "restricted"}),
    "promo_types": frozenset(
        {
            "alchemy",
            "arenaleague",
            "boosterfun",
            "borderless",
            "boxset",
            "bundle",
            "buyabox",
            "datestamped",
            "draftweekend",
            "event",
            "fnm",
            "gameday",
            "giftbox",
            "intropack",
            "judgegift",
            "league",
            "mediainsert",
            "neonink",
            "openhouse",
            "planeswalkerdeck",
            "playerrewards",
            "playpromo",
            "premiereshop",
            "prerelease",
            "promopack",
            "release",
            "resale",
            "schinesealtart",
            "setpromo",
            "stamped",
            "textured",
            "themepack",
            "thick",
            "tourney",
            "wizardsplaynetwork",
        }
    ),
    "rarity": frozenset({"common", "uncommon", "rare", "mythic", "special", "bonus"}),
    "security_stamp": frozenset({"oval", "triangle", "acorn", "arena", "circle", "heart"}),
}
_AFFECTED_CONSUMERS = (
    "card_lookup",
    "canonicalization",
    "analytics",
    "simulator_card_definitions",
    "scryfall_tagger_oracle_mappings",
    "commander_spellbook_card_references",
    "user_deck_resolution",
    "report_export_surfaces",
)


def build_scryfall_migration_report(
    previous_snapshot: ScryfallBulkSnapshotValidationReport,
    next_snapshot: ScryfallBulkSnapshotValidationReport,
    *,
    options: ScryfallMigrationOptions | None = None,
) -> ScryfallMigrationReport:
    """Build a deterministic migration report for two local snapshot reports."""

    if not isinstance(previous_snapshot, ScryfallBulkSnapshotValidationReport):
        raise ScryfallMigrationMonitoringError("previous_snapshot must be a ScryfallBulkSnapshotValidationReport")
    if not isinstance(next_snapshot, ScryfallBulkSnapshotValidationReport):
        raise ScryfallMigrationMonitoringError("next_snapshot must be a ScryfallBulkSnapshotValidationReport")
    options = options or ScryfallMigrationOptions()
    if not isinstance(options, ScryfallMigrationOptions):
        raise ScryfallMigrationMonitoringError("options must be a ScryfallMigrationOptions")

    previous_cards = tuple(previous_snapshot.raw_cards)
    next_cards = tuple(next_snapshot.raw_cards)
    previous_by_id = _index_cards_by_id(previous_cards)
    next_by_id = _index_cards_by_id(next_cards)
    previous_by_oracle = _index_cards_by_oracle(previous_cards)
    next_by_oracle = _index_cards_by_oracle(next_cards)

    required_failures: list[str] = []
    breaking: list[str] = []
    block_reasons: list[str] = []
    manual_reviews: list[ScryfallMigrationManualReviewItem] = []
    validation_errors: list[str] = []
    validation_warnings: list[str] = []
    optional_changes: list[ScryfallFieldChange] = []
    unknown_field_changes: list[ScryfallFieldChange] = []
    enum_changes: list[ScryfallEnumChange] = []
    identity_changes: list[ScryfallIdentityChange] = []

    _collect_snapshot_validity(
        "previous",
        previous_snapshot,
        validation_errors,
        validation_warnings,
        breaking,
        block_reasons,
        manual_reviews,
    )
    _collect_snapshot_validity(
        "next",
        next_snapshot,
        validation_errors,
        validation_warnings,
        breaking,
        block_reasons,
        manual_reviews,
    )

    for label, cards in (("previous", previous_cards), ("next", next_cards)):
        for index, card in enumerate(cards):
            scryfall_id = _card_scryfall_id(card)
            name = _card_name(card)
            if not scryfall_id:
                message = f"{label} card[{index}] missing required Scryfall id"
                required_failures.append(message)
                _add_blocking_condition(
                    message,
                    "missing required Scryfall id",
                    breaking,
                    block_reasons,
                    manual_reviews,
                    review_type="missing_required_field",
                    severity="blocking",
                    scryfall_id=None,
                    oracle_id=_optional_text(card.get("oracle_id")),
                    field_name="id",
                )
            if not name:
                message = f"{label} card[{index}] missing required name"
                required_failures.append(message)
                _add_blocking_condition(
                    message,
                    "missing required card name",
                    breaking,
                    block_reasons,
                    manual_reviews,
                    review_type="missing_required_field",
                    severity="blocking",
                    scryfall_id=scryfall_id,
                    oracle_id=_optional_text(card.get("oracle_id")),
                    field_name="name",
                )

    duplicate_next_ids = _duplicate_ids(next_cards)
    for scryfall_id in duplicate_next_ids:
        message = f"duplicate Scryfall id in next snapshot: {scryfall_id}"
        _add_blocking_condition(
            message,
            "duplicate Scryfall ID within next snapshot",
            breaking,
            block_reasons,
            manual_reviews,
            review_type="duplicate_identity",
            severity="blocking",
            scryfall_id=scryfall_id,
        )

    for oracle_id, cards in sorted(next_by_oracle.items()):
        next_ids = sorted(scryfall_id for scryfall_id in (_card_scryfall_id(card) for card in cards) if scryfall_id)
        names = sorted(name for name in (_card_name(card) for card in cards) if name)
        if len(set(next_ids)) > 1 and len(set(names)) > 1:
            message = f"oracle_id {oracle_id} is split across incompatible card identities"
            _add_blocking_condition(
                message,
                "same oracle ID split across incompatible card identities",
                breaking,
                block_reasons,
                manual_reviews,
                review_type="oracle_id_split",
                severity="blocking",
                oracle_id=oracle_id,
                metadata={"next_scryfall_ids": next_ids, "next_names": names},
            )

    for scryfall_id in sorted(set(previous_by_id) & set(next_by_id)):
        previous_card = previous_by_id[scryfall_id]
        next_card = next_by_id[scryfall_id]
        _collect_optional_changes(scryfall_id, previous_card, next_card, optional_changes)
        _collect_identity_changes_for_matching_id(scryfall_id, previous_card, next_card, identity_changes, breaking, block_reasons, manual_reviews)

    for oracle_id in sorted(set(previous_by_oracle) & set(next_by_oracle)):
        previous_ids = {_card_scryfall_id(card) for card in previous_by_oracle[oracle_id]}
        next_ids = {_card_scryfall_id(card) for card in next_by_oracle[oracle_id]}
        if previous_ids != next_ids:
            for previous_id in sorted(previous_ids - next_ids):
                for next_id in sorted(next_ids - previous_ids):
                    previous_card = previous_by_id.get(previous_id or "")
                    next_card = next_by_id.get(next_id or "")
                    change = ScryfallIdentityChange(
                        change_type="scryfall_id_replacement",
                        scryfall_id=None,
                        previous_scryfall_id=previous_id,
                        next_scryfall_id=next_id,
                        oracle_id=oracle_id,
                        previous_oracle_id=oracle_id,
                        next_oracle_id=oracle_id,
                        previous_name=_card_name(previous_card or {}),
                        next_name=_card_name(next_card or {}),
                        blocks_activation=False,
                    )
                    identity_changes.append(change)
                    manual_reviews.append(
                        ScryfallMigrationManualReviewItem(
                            review_type="scryfall_id_replacement",
                            severity="warning",
                            reason=f"oracle_id {oracle_id} maps to changed Scryfall IDs",
                            scryfall_id=next_id,
                            oracle_id=oracle_id,
                            metadata=_freeze_json({"previous_scryfall_id": previous_id, "next_scryfall_id": next_id}),
                        )
                    )

    _collect_unknown_field_changes(previous_cards, next_cards, unknown_field_changes, options, manual_reviews, breaking, block_reasons)
    _collect_unknown_enum_changes(next_cards, enum_changes, options, manual_reviews, breaking, block_reasons)

    if _hash_changed(previous_snapshot):
        _add_blocking_condition(
            "previous snapshot validation reports hash/count mismatch",
            "hash/count mismatch in previous input snapshot",
            breaking,
            block_reasons,
            manual_reviews,
            review_type="snapshot_validation_error",
            severity="blocking",
        )
    if _hash_changed(next_snapshot):
        _add_blocking_condition(
            "next snapshot validation reports hash/count mismatch",
            "hash/count mismatch in next input snapshot",
            breaking,
            block_reasons,
            manual_reviews,
            review_type="snapshot_validation_error",
            severity="blocking",
        )

    affected_consumers = _build_affected_consumers(identity_changes, breaking, enum_changes, unknown_field_changes)
    report_id = options.report_id or _default_report_id(previous_snapshot, next_snapshot)
    report = ScryfallMigrationReport(
        report_id=report_id,
        monitor_version=SCRYFALL_MIGRATION_MONITOR_VERSION,
        previous_snapshot_id=previous_snapshot.manifest.snapshot_id,
        next_snapshot_id=next_snapshot.manifest.snapshot_id,
        previous_content_hash=previous_snapshot.manifest.content_hash,
        next_content_hash=next_snapshot.manifest.content_hash,
        generated_at=options.generated_at,
        required_field_failures=tuple(sorted(set(required_failures))),
        optional_field_changes=tuple(sorted(optional_changes, key=_field_change_sort_key)),
        unknown_field_changes=tuple(sorted(unknown_field_changes, key=_field_change_sort_key)),
        unknown_enum_changes=tuple(sorted(enum_changes, key=_enum_change_sort_key)),
        identity_changes=tuple(sorted(identity_changes, key=_identity_change_sort_key)),
        schema_breaking_conditions=tuple(sorted(set(breaking))),
        activation_blocked=bool(breaking or block_reasons),
        activation_block_reasons=tuple(sorted(set(block_reasons))),
        affected_consumers=tuple(affected_consumers),
        manual_review_items=tuple(sorted(manual_reviews, key=_manual_review_sort_key)),
        validation_errors=tuple(sorted(set(validation_errors))),
        validation_warnings=tuple(sorted(set(validation_warnings))),
    )
    return validate_scryfall_migration_report(report)


def validate_scryfall_migration_report(report: ScryfallMigrationReport) -> ScryfallMigrationReport:
    """Validate that a migration report has a coherent immutable shape."""

    if not isinstance(report, ScryfallMigrationReport):
        raise ScryfallMigrationMonitoringError("report must be a ScryfallMigrationReport")
    for field_name in (
        "report_id",
        "monitor_version",
        "previous_snapshot_id",
        "next_snapshot_id",
        "previous_content_hash",
        "next_content_hash",
    ):
        _require_text(getattr(report, field_name), field_name)
    if report.monitor_version != SCRYFALL_MIGRATION_MONITOR_VERSION:
        raise ScryfallMigrationMonitoringError("unsupported monitor_version")
    if report.activation_blocked and not report.activation_block_reasons:
        raise ScryfallMigrationMonitoringError("activation_blocked reports require activation_block_reasons")
    if report.schema_breaking_conditions and not report.activation_blocked:
        raise ScryfallMigrationMonitoringError("schema_breaking_conditions must block activation")
    _ensure_json_compatible(scryfall_migration_report_to_dict(report))
    return report


def scryfall_migration_report_to_dict(report: ScryfallMigrationReport) -> dict[str, Any]:
    """Serialize a migration report to a deterministic JSON-compatible dictionary."""

    if not isinstance(report, ScryfallMigrationReport):
        raise ScryfallMigrationMonitoringError("report must be a ScryfallMigrationReport")
    return {
        "activation_block_reasons": list(report.activation_block_reasons),
        "activation_blocked": report.activation_blocked,
        "affected_consumers": [
            {
                "consumer_key": consumer.consumer_key,
                "reason": consumer.reason,
                "severity": consumer.severity,
            }
            for consumer in report.affected_consumers
        ],
        "generated_at": report.generated_at,
        "identity_changes": [
            {
                "blocks_activation": change.blocks_activation,
                "change_type": change.change_type,
                "next_name": change.next_name,
                "next_oracle_id": change.next_oracle_id,
                "next_scryfall_id": change.next_scryfall_id,
                "oracle_id": change.oracle_id,
                "previous_name": change.previous_name,
                "previous_oracle_id": change.previous_oracle_id,
                "previous_scryfall_id": change.previous_scryfall_id,
                "scryfall_id": change.scryfall_id,
            }
            for change in report.identity_changes
        ],
        "manual_review_items": [
            {
                "field_name": item.field_name,
                "metadata": _thaw_json(item.metadata or {}),
                "oracle_id": item.oracle_id,
                "reason": item.reason,
                "review_type": item.review_type,
                "scryfall_id": item.scryfall_id,
                "severity": item.severity,
            }
            for item in report.manual_review_items
        ],
        "monitor_version": report.monitor_version,
        "next_content_hash": report.next_content_hash,
        "next_snapshot_id": report.next_snapshot_id,
        "optional_field_changes": [_field_change_to_dict(change) for change in report.optional_field_changes],
        "previous_content_hash": report.previous_content_hash,
        "previous_snapshot_id": report.previous_snapshot_id,
        "report_id": report.report_id,
        "required_field_failures": list(report.required_field_failures),
        "schema_breaking_conditions": list(report.schema_breaking_conditions),
        "unknown_enum_changes": [
            {
                "blocks_activation": change.blocks_activation,
                "enum_value": change.enum_value,
                "field_name": change.field_name,
                "oracle_id": change.oracle_id,
                "scryfall_id": change.scryfall_id,
            }
            for change in report.unknown_enum_changes
        ],
        "unknown_field_changes": [_field_change_to_dict(change) for change in report.unknown_field_changes],
        "validation_errors": list(report.validation_errors),
        "validation_warnings": list(report.validation_warnings),
    }


def _collect_snapshot_validity(
    label: str,
    snapshot: ScryfallBulkSnapshotValidationReport,
    validation_errors: list[str],
    validation_warnings: list[str],
    breaking: list[str],
    block_reasons: list[str],
    manual_reviews: list[ScryfallMigrationManualReviewItem],
) -> None:
    for error in snapshot.validation_errors:
        message = f"{label} snapshot validation error: {error}"
        validation_errors.append(message)
        if "content_hash" in error or "card_count" in error:
            _add_blocking_condition(
                message,
                f"hash/count mismatch in {label} input snapshot",
                breaking,
                block_reasons,
                manual_reviews,
                review_type="snapshot_validation_error",
                severity="blocking",
            )
    for warning in snapshot.validation_warnings:
        validation_warnings.append(f"{label} snapshot validation warning: {warning}")


def _index_cards_by_id(cards: tuple[Mapping[str, Any], ...]) -> dict[str, Mapping[str, Any]]:
    indexed: dict[str, Mapping[str, Any]] = {}
    for card in cards:
        scryfall_id = _card_scryfall_id(card)
        if scryfall_id and scryfall_id not in indexed:
            indexed[scryfall_id] = card
    return indexed


def _index_cards_by_oracle(cards: tuple[Mapping[str, Any], ...]) -> dict[str, tuple[Mapping[str, Any], ...]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for card in cards:
        oracle_id = _optional_text(card.get("oracle_id"))
        if oracle_id:
            grouped.setdefault(oracle_id, []).append(card)
    return {key: tuple(value) for key, value in grouped.items()}


def _duplicate_ids(cards: tuple[Mapping[str, Any], ...]) -> tuple[str, ...]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for card in cards:
        scryfall_id = _card_scryfall_id(card)
        if not scryfall_id:
            continue
        if scryfall_id in seen:
            duplicates.add(scryfall_id)
        seen.add(scryfall_id)
    return tuple(sorted(duplicates))


def _collect_optional_changes(
    scryfall_id: str,
    previous_card: Mapping[str, Any],
    next_card: Mapping[str, Any],
    optional_changes: list[ScryfallFieldChange],
) -> None:
    oracle_id = _optional_text(next_card.get("oracle_id")) or _optional_text(previous_card.get("oracle_id"))
    for field_name in _OPTIONAL_MONITORED_FIELDS:
        old_value = _thaw_json(previous_card.get(field_name))
        new_value = _thaw_json(next_card.get(field_name))
        if old_value != new_value:
            optional_changes.append(
                ScryfallFieldChange(
                    field_name=field_name,
                    change_type="changed",
                    old_value=old_value,
                    new_value=new_value,
                    scryfall_id=scryfall_id,
                    oracle_id=oracle_id,
                )
            )


def _collect_identity_changes_for_matching_id(
    scryfall_id: str,
    previous_card: Mapping[str, Any],
    next_card: Mapping[str, Any],
    identity_changes: list[ScryfallIdentityChange],
    breaking: list[str],
    block_reasons: list[str],
    manual_reviews: list[ScryfallMigrationManualReviewItem],
) -> None:
    previous_name = _card_name(previous_card)
    next_name = _card_name(next_card)
    previous_oracle = _optional_text(previous_card.get("oracle_id"))
    next_oracle = _optional_text(next_card.get("oracle_id"))
    if previous_name and next_name and previous_name != next_name:
        identity_changes.append(
            ScryfallIdentityChange(
                change_type="renamed_card",
                scryfall_id=scryfall_id,
                previous_scryfall_id=scryfall_id,
                next_scryfall_id=scryfall_id,
                oracle_id=next_oracle or previous_oracle,
                previous_oracle_id=previous_oracle,
                next_oracle_id=next_oracle,
                previous_name=previous_name,
                next_name=next_name,
                blocks_activation=False,
            )
        )
        manual_reviews.append(
            ScryfallMigrationManualReviewItem(
                review_type="renamed_card",
                severity="warning",
                reason=f"Scryfall id {scryfall_id} changed name",
                scryfall_id=scryfall_id,
                oracle_id=next_oracle or previous_oracle,
                metadata=_freeze_json({"previous_name": previous_name, "next_name": next_name}),
            )
        )
    if previous_oracle and next_oracle and previous_oracle != next_oracle:
        message = f"Scryfall id {scryfall_id} changed oracle_id"
        identity_changes.append(
            ScryfallIdentityChange(
                change_type="oracle_id_change",
                scryfall_id=scryfall_id,
                previous_scryfall_id=scryfall_id,
                next_scryfall_id=scryfall_id,
                oracle_id=next_oracle,
                previous_oracle_id=previous_oracle,
                next_oracle_id=next_oracle,
                previous_name=previous_name,
                next_name=next_name,
                blocks_activation=True,
            )
        )
        _add_blocking_condition(
            message,
            "same Scryfall ID mapped to conflicting oracle IDs",
            breaking,
            block_reasons,
            manual_reviews,
            review_type="oracle_id_change",
            severity="blocking",
            scryfall_id=scryfall_id,
            oracle_id=next_oracle,
            metadata={"previous_oracle_id": previous_oracle, "next_oracle_id": next_oracle},
        )


def _collect_unknown_field_changes(
    previous_cards: tuple[Mapping[str, Any], ...],
    next_cards: tuple[Mapping[str, Any], ...],
    unknown_field_changes: list[ScryfallFieldChange],
    options: ScryfallMigrationOptions,
    manual_reviews: list[ScryfallMigrationManualReviewItem],
    breaking: list[str],
    block_reasons: list[str],
) -> None:
    previous_fields = _unknown_fields(previous_cards)
    next_fields = _unknown_fields(next_cards)
    for field_name in sorted(next_fields - previous_fields):
        unknown_field_changes.append(
            ScryfallFieldChange(
                field_name=field_name,
                change_type="added_unknown_field",
                old_value=None,
                new_value="present",
            )
        )
        manual_reviews.append(
            ScryfallMigrationManualReviewItem(
                review_type="unknown_field",
                severity="warning" if not options.unknown_fields_block_activation else "blocking",
                reason=f"new unknown Scryfall field observed: {field_name}",
                field_name=field_name,
            )
        )
        if options.unknown_fields_block_activation:
            breaking.append(f"unknown field requires blocking review: {field_name}")
            block_reasons.append("unknown field policy blocks activation")
    for field_name in sorted(previous_fields - next_fields):
        unknown_field_changes.append(
            ScryfallFieldChange(
                field_name=field_name,
                change_type="removed_unknown_field",
                old_value="present",
                new_value=None,
            )
        )


def _collect_unknown_enum_changes(
    cards: tuple[Mapping[str, Any], ...],
    enum_changes: list[ScryfallEnumChange],
    options: ScryfallMigrationOptions,
    manual_reviews: list[ScryfallMigrationManualReviewItem],
    breaking: list[str],
    block_reasons: list[str],
) -> None:
    for card in cards:
        scryfall_id = _card_scryfall_id(card)
        if not scryfall_id:
            continue
        oracle_id = _optional_text(card.get("oracle_id"))
        for field_name, known_values in _KNOWN_ENUM_VALUES.items():
            for enum_value in _enum_values(card.get(field_name), field_name):
                if enum_value not in known_values:
                    blocks = options.unknown_enums_block_activation
                    enum_changes.append(
                        ScryfallEnumChange(
                            field_name=field_name,
                            enum_value=enum_value,
                            scryfall_id=scryfall_id,
                            oracle_id=oracle_id,
                            blocks_activation=blocks,
                        )
                    )
                    manual_reviews.append(
                        ScryfallMigrationManualReviewItem(
                            review_type="unknown_enum_value",
                            severity="warning" if not blocks else "blocking",
                            reason=f"unknown {field_name} enum value observed: {enum_value}",
                            scryfall_id=scryfall_id,
                            oracle_id=oracle_id,
                            field_name=field_name,
                            metadata=_freeze_json({"enum_value": enum_value}),
                        )
                    )
                    if blocks:
                        breaking.append(f"unknown {field_name} enum value requires blocking review: {enum_value}")
                        block_reasons.append("unknown enum policy blocks activation")


def _enum_values(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if field_name == "legalities" and isinstance(value, Mapping):
        return tuple(sorted(str(item) for item in value.values() if item is not None))
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(sorted(str(item) for item in value if item is not None))
    return (str(value),)


def _unknown_fields(cards: tuple[Mapping[str, Any], ...]) -> set[str]:
    fields: set[str] = set()
    for card in cards:
        fields.update(str(key) for key in card if str(key) not in _KNOWN_FIELDS)
    return fields


def _build_affected_consumers(
    identity_changes: list[ScryfallIdentityChange],
    breaking: list[str],
    enum_changes: list[ScryfallEnumChange],
    unknown_field_changes: list[ScryfallFieldChange],
) -> tuple[ScryfallMigrationAffectedConsumer, ...]:
    if not identity_changes and not breaking and not enum_changes and not unknown_field_changes:
        return ()
    severity = "blocking" if breaking else "warning"
    consumers: list[ScryfallMigrationAffectedConsumer] = []
    for consumer_key in _AFFECTED_CONSUMERS:
        consumers.append(
            ScryfallMigrationAffectedConsumer(
                consumer_key=consumer_key,
                reason="Scryfall snapshot migration report contains card identity or schema changes",
                severity=severity,
            )
        )
    return tuple(consumers)


def _add_blocking_condition(
    message: str,
    block_reason: str,
    breaking: list[str],
    block_reasons: list[str],
    manual_reviews: list[ScryfallMigrationManualReviewItem],
    *,
    review_type: str,
    severity: str,
    scryfall_id: str | None = None,
    oracle_id: str | None = None,
    field_name: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> None:
    breaking.append(message)
    block_reasons.append(block_reason)
    manual_reviews.append(
        ScryfallMigrationManualReviewItem(
            review_type=review_type,
            severity=severity,
            reason=message,
            scryfall_id=scryfall_id,
            oracle_id=oracle_id,
            field_name=field_name,
            metadata=_freeze_json(dict(metadata or {})),
        )
    )


def _hash_changed(snapshot: ScryfallBulkSnapshotValidationReport) -> bool:
    return any("content_hash" in error or "card_count" in error for error in snapshot.validation_errors)


def _card_scryfall_id(card: Mapping[str, Any]) -> str | None:
    value = card.get("id") or card.get("scryfall_id")
    return _optional_text(value)


def _card_name(card: Mapping[str, Any]) -> str | None:
    return _optional_text(card.get("name"))


def _optional_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ScryfallMigrationMonitoringError(f"{field_name} is required")


def _default_report_id(
    previous_snapshot: ScryfallBulkSnapshotValidationReport,
    next_snapshot: ScryfallBulkSnapshotValidationReport,
) -> str:
    return f"{previous_snapshot.manifest.snapshot_id}--{next_snapshot.manifest.snapshot_id}"


def _field_change_to_dict(change: ScryfallFieldChange) -> dict[str, Any]:
    return {
        "change_type": change.change_type,
        "field_name": change.field_name,
        "new_value": _thaw_json(change.new_value),
        "old_value": _thaw_json(change.old_value),
        "oracle_id": change.oracle_id,
        "scryfall_id": change.scryfall_id,
    }


def _field_change_sort_key(change: ScryfallFieldChange) -> tuple[str, str, str]:
    return (change.field_name, change.change_type, change.scryfall_id or "")


def _enum_change_sort_key(change: ScryfallEnumChange) -> tuple[str, str, str]:
    return (change.field_name, change.enum_value, change.scryfall_id)


def _identity_change_sort_key(change: ScryfallIdentityChange) -> tuple[str, str, str]:
    return (change.change_type, change.scryfall_id or "", change.oracle_id or "")


def _manual_review_sort_key(item: ScryfallMigrationManualReviewItem) -> tuple[str, str, str, str]:
    return (item.review_type, item.severity, item.scryfall_id or "", item.field_name or "")


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze_json(value[key]) for key in sorted(value)})
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze_json(item) for item in value)
    return value


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _ensure_json_compatible(value: Any) -> None:
    try:
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    except TypeError as exc:
        raise ScryfallMigrationMonitoringError("migration report must be JSON-compatible") from exc
