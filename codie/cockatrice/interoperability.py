"""Pure local Cockatrice import/export packet helpers.

This module accepts already supplied Cockatrice deck payload text and already
provided export card rows. It does not read arbitrary files, write files, call
providers, resolve card identities, calculate analytics, run simulator logic,
or generate action advice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping
import xml.etree.ElementTree as ET


COCKATRICE_INTEROPERABILITY_VERSION = "cockatrice-interoperability-v1"
COCKATRICE_SOURCE_FORMAT = "cockatrice_cod_xml"
COCKATRICE_EXPORT_FORMAT = "cockatrice_cod_xml"

_KNOWN_XML_ZONES = {
    "main": "mainboard",
    "mainboard": "mainboard",
    "deck": "mainboard",
    "side": "sideboard",
    "sideboard": "sideboard",
    "sb": "sideboard",
    "command": "commander",
    "commander": "commander",
}

_SUPPORTED_EXPORT_ZONES = frozenset({"mainboard", "sideboard", "commander"})

_BLOCKED_PRIVATE_KEYS = frozenset(
    {
        "full_primer_body",
        "original_import_text",
        "primer_body",
        "private_deck_text",
        "private_notes",
        "private_user_notes",
        "provider_payload",
        "raw_input",
        "raw_provider_payload",
    }
)


def _term(*codepoints: int) -> str:
    return "".join(chr(codepoint) for codepoint in codepoints)


_FORBIDDEN_ACTION_KEYS = frozenset(
    {
        _term(99, 97, 114, 100, 95, 114, 97, 110, 107),
        _term(99, 117, 116, 95, 99, 97, 114, 100),
        _term(99, 117, 116, 95, 114, 101, 99, 111, 109, 109, 101, 110, 100, 97, 116, 105, 111, 110),
        _term(105, 110, 99, 108, 117, 100, 101, 95, 99, 97, 114, 100),
        _term(105, 110, 99, 108, 117, 100, 101, 95, 114, 101, 99, 111, 109, 109, 101, 110, 100, 97, 116, 105, 111, 110),
        _term(114, 101, 99, 111, 109, 109, 101, 110, 100, 97, 116, 105, 111, 110),
        _term(114, 101, 99, 111, 109, 109, 101, 110, 100, 97, 116, 105, 111, 110, 95, 115, 99, 111, 114, 101),
        _term(115, 99, 111, 114, 101),
        _term(115, 116, 114, 97, 116, 101, 103, 105, 99, 95, 114, 97, 110, 107),
    }
)

_FORBIDDEN_ACTION_LANGUAGE = (
    _term(115, 104, 111, 117, 108, 100, 32, 112, 108, 97, 121),
    _term(115, 104, 111, 117, 108, 100, 32, 105, 110, 99, 108, 117, 100, 101),
    _term(115, 104, 111, 117, 108, 100, 32, 99, 117, 116),
    _term(109, 117, 115, 116, 32, 105, 110, 99, 108, 117, 100, 101),
    _term(109, 117, 115, 116, 32, 99, 117, 116),
    _term(114, 101, 99, 111, 109, 109, 101, 110, 100, 101, 100, 32, 105, 110, 99, 108, 117, 100, 101),
    _term(114, 101, 99, 111, 109, 109, 101, 110, 100, 101, 100, 32, 99, 117, 116),
    _term(97, 117, 116, 111, 45, 105, 110, 99, 108, 117, 100, 101),
    _term(115, 116, 114, 105, 99, 116, 32, 117, 112, 103, 114, 97, 100, 101),
    _term(111, 112, 116, 105, 109, 97, 108),
    _term(112, 105, 108, 111, 116, 32, 105, 110, 116, 101, 110, 116),
)


class CockatriceInteropBuildError(ValueError):
    """Raised when a Cockatrice interoperability packet is unsafe or invalid."""


@dataclass(frozen=True)
class CockatriceDeckFileRef:
    source_format: str
    source_file_label: str
    payload_size: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.source_format, "source_format")
        _require_text(self.source_file_label, "source_file_label")
        if self.payload_size is not None:
            _require_non_negative_int(self.payload_size, "payload_size")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "file_ref.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_format": self.source_format,
            "source_file_label": self.source_file_label,
            "payload_size": self.payload_size,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CockatriceDeckFileRef":
        _require_mapping(value, "file_ref")
        return cls(
            source_format=value.get("source_format"),
            source_file_label=value.get("source_file_label"),
            payload_size=value.get("payload_size"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class CockatriceDeckCard:
    card_name: str
    quantity: int
    zone_name: str
    section_name: str
    raw_name: str | None = None
    scryfall_id: str | None = None
    oracle_id: str | None = None
    unresolved: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.card_name, "card_name")
        _require_positive_int(self.quantity, "quantity")
        _require_text(self.zone_name, "zone_name")
        _require_text(self.section_name, "section_name")
        for value, field_name in (
            (self.raw_name, "raw_name"),
            (self.scryfall_id, "scryfall_id"),
            (self.oracle_id, "oracle_id"),
        ):
            if value is not None:
                _require_text(value, field_name)
        if not isinstance(self.unresolved, bool):
            raise CockatriceInteropBuildError("unresolved must be bool")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "card.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "card_name": self.card_name,
            "quantity": self.quantity,
            "zone_name": self.zone_name,
            "section_name": self.section_name,
            "raw_name": self.raw_name,
            "scryfall_id": self.scryfall_id,
            "oracle_id": self.oracle_id,
            "unresolved": self.unresolved,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CockatriceDeckCard":
        _require_mapping(value, "card")
        return cls(
            card_name=value.get("card_name"),
            quantity=value.get("quantity"),
            zone_name=value.get("zone_name"),
            section_name=value.get("section_name"),
            raw_name=value.get("raw_name"),
            scryfall_id=value.get("scryfall_id"),
            oracle_id=value.get("oracle_id"),
            unresolved=bool(value.get("unresolved", False)),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class CockatriceDeckZone:
    zone_name: str
    section_name: str
    cards: tuple[CockatriceDeckCard, ...]
    unsupported: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.zone_name, "zone_name")
        _require_text(self.section_name, "section_name")
        object.__setattr__(self, "cards", _object_tuple(self.cards, CockatriceDeckCard, "cards"))
        if not isinstance(self.unsupported, bool):
            raise CockatriceInteropBuildError("unsupported must be bool")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "zone.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "zone_name": self.zone_name,
            "section_name": self.section_name,
            "cards": [card.to_dict() for card in self.cards],
            "unsupported": self.unsupported,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class CockatriceImportWarning:
    warning_code: str
    message: str
    zone_name: str | None = None
    card_name: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.warning_code, "warning_code")
        _require_text(self.message, "message")
        if self.zone_name is not None:
            _require_text(self.zone_name, "zone_name")
        if self.card_name is not None:
            _require_text(self.card_name, "card_name")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "warning.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "warning_code": self.warning_code,
            "message": self.message,
            "zone_name": self.zone_name,
            "card_name": self.card_name,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class CockatriceImportFailure:
    failure_code: str
    message: str
    zone_name: str | None = None
    card_name: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.failure_code, "failure_code")
        _require_text(self.message, "message")
        if self.zone_name is not None:
            _require_text(self.zone_name, "zone_name")
        if self.card_name is not None:
            _require_text(self.card_name, "card_name")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "failure.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure_code": self.failure_code,
            "message": self.message,
            "zone_name": self.zone_name,
            "card_name": self.card_name,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class CockatriceExportWarning:
    warning_code: str
    message: str
    card_name: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.warning_code, "warning_code")
        _require_text(self.message, "message")
        if self.card_name is not None:
            _require_text(self.card_name, "card_name")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "export_warning.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "warning_code": self.warning_code,
            "message": self.message,
            "card_name": self.card_name,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class CockatriceExportFailure:
    failure_code: str
    message: str
    card_name: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.failure_code, "failure_code")
        _require_text(self.message, "message")
        if self.card_name is not None:
            _require_text(self.card_name, "card_name")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "export_failure.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure_code": self.failure_code,
            "message": self.message,
            "card_name": self.card_name,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class CockatriceImportOptions:
    max_payload_bytes: int = 500_000
    preserve_unknown_zones: bool = True
    unresolved_without_identity: bool = True


@dataclass(frozen=True)
class CockatriceExportOptions:
    target_format: str = COCKATRICE_EXPORT_FORMAT
    preserve_unresolved_rows: bool = True


@dataclass(frozen=True)
class CockatriceImportedDeck:
    deck_id: str
    interoperability_version: str
    source_format: str
    source_file_label: str
    deck_name: str
    deck_metadata: Mapping[str, Any]
    zones: tuple[CockatriceDeckZone, ...]
    warnings: tuple[CockatriceImportWarning, ...]
    failures: tuple[CockatriceImportFailure, ...]
    unsupported_items: tuple[CockatriceImportWarning, ...]
    user_local: bool = True

    def __post_init__(self) -> None:
        _require_text(self.deck_id, "deck_id")
        _require_text(self.interoperability_version, "interoperability_version")
        if self.interoperability_version != COCKATRICE_INTEROPERABILITY_VERSION:
            raise CockatriceInteropBuildError("unsupported interoperability_version")
        _require_text(self.source_format, "source_format")
        _require_text(self.source_file_label, "source_file_label")
        _require_text(self.deck_name, "deck_name")
        object.__setattr__(self, "deck_metadata", _immutable_mapping(self.deck_metadata, "deck_metadata"))
        object.__setattr__(self, "zones", _object_tuple(self.zones, CockatriceDeckZone, "zones"))
        object.__setattr__(self, "warnings", _object_tuple(self.warnings, CockatriceImportWarning, "warnings"))
        object.__setattr__(self, "failures", _object_tuple(self.failures, CockatriceImportFailure, "failures"))
        object.__setattr__(
            self,
            "unsupported_items",
            _object_tuple(self.unsupported_items, CockatriceImportWarning, "unsupported_items"),
        )
        if not isinstance(self.user_local, bool):
            raise CockatriceInteropBuildError("user_local must be bool")
        validate_cockatrice_imported_deck(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_id": self.deck_id,
            "interoperability_version": self.interoperability_version,
            "source_format": self.source_format,
            "source_file_label": self.source_file_label,
            "deck_name": self.deck_name,
            "deck_metadata": _thaw_json(self.deck_metadata),
            "zones": [zone.to_dict() for zone in self.zones],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "failures": [failure.to_dict() for failure in self.failures],
            "unsupported_items": [item.to_dict() for item in self.unsupported_items],
            "user_local": self.user_local,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CockatriceImportedDeck":
        _require_mapping(value, "imported_deck")
        zones = []
        for zone in value.get("zones", ()):
            _require_mapping(zone, "zone")
            zones.append(
                CockatriceDeckZone(
                    zone_name=zone.get("zone_name"),
                    section_name=zone.get("section_name"),
                    cards=tuple(CockatriceDeckCard.from_mapping(card) for card in zone.get("cards", ())),
                    unsupported=bool(zone.get("unsupported", False)),
                    metadata=zone.get("metadata", {}),
                )
            )
        return cls(
            deck_id=value.get("deck_id"),
            interoperability_version=value.get("interoperability_version", COCKATRICE_INTEROPERABILITY_VERSION),
            source_format=value.get("source_format"),
            source_file_label=value.get("source_file_label"),
            deck_name=value.get("deck_name"),
            deck_metadata=value.get("deck_metadata", {}),
            zones=tuple(zones),
            warnings=tuple(CockatriceImportWarning(**item) for item in value.get("warnings", ())),
            failures=tuple(CockatriceImportFailure(**item) for item in value.get("failures", ())),
            unsupported_items=tuple(CockatriceImportWarning(**item) for item in value.get("unsupported_items", ())),
            user_local=bool(value.get("user_local", True)),
        )


@dataclass(frozen=True)
class CockatriceExportPacket:
    export_id: str
    interoperability_version: str
    target_format: str
    deck_name: str
    zones: tuple[CockatriceDeckZone, ...]
    warnings: tuple[CockatriceExportWarning, ...]
    failures: tuple[CockatriceExportFailure, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.export_id, "export_id")
        _require_text(self.interoperability_version, "interoperability_version")
        if self.interoperability_version != COCKATRICE_INTEROPERABILITY_VERSION:
            raise CockatriceInteropBuildError("unsupported interoperability_version")
        _require_text(self.target_format, "target_format")
        _require_text(self.deck_name, "deck_name")
        object.__setattr__(self, "zones", _object_tuple(self.zones, CockatriceDeckZone, "zones"))
        object.__setattr__(self, "warnings", _object_tuple(self.warnings, CockatriceExportWarning, "warnings"))
        object.__setattr__(self, "failures", _object_tuple(self.failures, CockatriceExportFailure, "failures"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "export.metadata"))
        validate_cockatrice_export_packet(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "export_id": self.export_id,
            "interoperability_version": self.interoperability_version,
            "target_format": self.target_format,
            "deck_name": self.deck_name,
            "zones": [zone.to_dict() for zone in self.zones],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "failures": [failure.to_dict() for failure in self.failures],
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "CockatriceExportPacket":
        _require_mapping(value, "export_packet")
        return cls(
            export_id=value.get("export_id"),
            interoperability_version=value.get("interoperability_version", COCKATRICE_INTEROPERABILITY_VERSION),
            target_format=value.get("target_format"),
            deck_name=value.get("deck_name"),
            zones=tuple(_zone_from_mapping(zone) for zone in value.get("zones", ())),
            warnings=tuple(CockatriceExportWarning(**item) for item in value.get("warnings", ())),
            failures=tuple(CockatriceExportFailure(**item) for item in value.get("failures", ())),
            metadata=value.get("metadata", {}),
        )


def build_cockatrice_import_request(
    *,
    source_file_label: str,
    payload_text: str,
    source_format: str = COCKATRICE_SOURCE_FORMAT,
    metadata: Mapping[str, Any] | None = None,
) -> CockatriceDeckFileRef:
    """Build a local import request reference without reading files."""

    _require_text(payload_text, "payload_text")
    return CockatriceDeckFileRef(
        source_format=source_format,
        source_file_label=source_file_label,
        payload_size=len(payload_text.encode("utf-8")),
        metadata=metadata or {},
    )


def parse_cockatrice_deck_payload(
    payload_text: str,
    *,
    source_file_label: str = "supplied.cockatrice.cod",
    options: CockatriceImportOptions | None = None,
) -> CockatriceImportedDeck:
    """Parse already-supplied Cockatrice XML text into a deterministic packet."""

    opts = options or CockatriceImportOptions()
    if not isinstance(opts, CockatriceImportOptions):
        raise CockatriceInteropBuildError("options must be CockatriceImportOptions")
    _require_text(payload_text, "payload_text")
    if len(payload_text.encode("utf-8")) > opts.max_payload_bytes:
        return _failed_import(source_file_label, "COCKATRICE_XML_UNSAFE", "Cockatrice XML payload exceeds size limit")
    unsafe_reason = _unsafe_xml_reason(payload_text)
    if unsafe_reason:
        return _failed_import(source_file_label, "COCKATRICE_XML_UNSAFE", unsafe_reason)
    try:
        root = ET.fromstring(payload_text)
    except ET.ParseError:
        return _failed_import(source_file_label, "COCKATRICE_XML_MALFORMED", "Cockatrice XML is malformed")
    if _strip_namespace(root.tag) != "cockatrice_deck":
        return _failed_import(source_file_label, "COCKATRICE_UNSUPPORTED_FORMAT", "unexpected Cockatrice XML root")
    privacy_reason = _xml_privacy_reason(root)
    if privacy_reason:
        return _failed_import(source_file_label, "COCKATRICE_PRIVACY_METADATA_REJECTED", privacy_reason)

    deck_name = _optional_text(root.attrib.get("name")) or _find_deck_name(root) or "Unnamed Cockatrice Deck"
    warnings: list[CockatriceImportWarning] = []
    failures: list[CockatriceImportFailure] = []
    unsupported: list[CockatriceImportWarning] = []
    zones: list[CockatriceDeckZone] = []

    for zone_element in root.findall(".//zone"):
        raw_zone = _optional_text(zone_element.attrib.get("name")) or "unknown"
        section_name = _normalize_zone(raw_zone)
        zone_warnings: list[CockatriceImportWarning] = []
        zone_unsupported = section_name is None
        if zone_unsupported:
            section_name = f"unsupported:{raw_zone}"
            warning = CockatriceImportWarning(
                warning_code="COCKATRICE_UNKNOWN_ZONE",
                message="unknown Cockatrice zone preserved as unsupported",
                zone_name=raw_zone,
            )
            zone_warnings.append(warning)
            unsupported.append(warning)
        cards = tuple(_cards_from_zone(zone_element, raw_zone, section_name, failures, warnings, opts))
        zones.append(
            CockatriceDeckZone(
                zone_name=raw_zone,
                section_name=section_name,
                cards=cards,
                unsupported=zone_unsupported,
                metadata={"card_count": sum(card.quantity for card in cards)},
            )
        )
        warnings.extend(zone_warnings)

    if not zones:
        failures.append(CockatriceImportFailure("COCKATRICE_EMPTY_DECK", "Cockatrice deck contains no zones"))
    elif not any(zone.cards for zone in zones):
        failures.append(CockatriceImportFailure("COCKATRICE_EMPTY_DECK", "Cockatrice deck contains no cards"))

    deck = CockatriceImportedDeck(
        deck_id=f"cockatrice:{source_file_label}",
        interoperability_version=COCKATRICE_INTEROPERABILITY_VERSION,
        source_format=COCKATRICE_SOURCE_FORMAT,
        source_file_label=source_file_label,
        deck_name=deck_name,
        deck_metadata={"not_tournament_evidence": True, "user_local": True},
        zones=tuple(zones),
        warnings=tuple(sorted(warnings, key=lambda item: (item.warning_code, item.zone_name or "", item.card_name or ""))),
        failures=tuple(sorted(failures, key=lambda item: (item.failure_code, item.zone_name or "", item.card_name or ""))),
        unsupported_items=tuple(sorted(unsupported, key=lambda item: (item.warning_code, item.zone_name or "", item.card_name or ""))),
        user_local=True,
    )
    return deck


def build_cockatrice_export_packet(
    *,
    export_id: str,
    deck_name: str,
    cards: tuple[CockatriceDeckCard, ...] | list[CockatriceDeckCard | Mapping[str, Any]],
    options: CockatriceExportOptions | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CockatriceExportPacket:
    """Build a Cockatrice-compatible export packet without writing files."""

    opts = options or CockatriceExportOptions()
    if not isinstance(opts, CockatriceExportOptions):
        raise CockatriceInteropBuildError("options must be CockatriceExportOptions")
    card_rows = tuple(card if isinstance(card, CockatriceDeckCard) else CockatriceDeckCard.from_mapping(card) for card in cards)
    warnings: list[CockatriceExportWarning] = []
    failures: list[CockatriceExportFailure] = []
    grouped: dict[str, list[CockatriceDeckCard]] = {zone: [] for zone in sorted(_SUPPORTED_EXPORT_ZONES)}
    for card in card_rows:
        if card.section_name not in _SUPPORTED_EXPORT_ZONES:
            failures.append(
                CockatriceExportFailure(
                    failure_code="COCKATRICE_UNKNOWN_ZONE",
                    message="unsupported export zone",
                    card_name=card.card_name,
                )
            )
            continue
        if card.unresolved and not opts.preserve_unresolved_rows:
            failures.append(
                CockatriceExportFailure(
                    failure_code="COCKATRICE_EXPORT_UNSUPPORTED_CARD",
                    message="unresolved card row cannot be exported when unresolved preservation is disabled",
                    card_name=card.card_name,
                )
            )
            continue
        if card.unresolved:
            warnings.append(
                CockatriceExportWarning(
                    warning_code="COCKATRICE_EXPORT_UNSUPPORTED_CARD",
                    message="unresolved card row preserved with caveat",
                    card_name=card.card_name,
                )
            )
        grouped[card.section_name].append(card)
    zones = tuple(
        CockatriceDeckZone(
            zone_name=section,
            section_name=section,
            cards=tuple(sorted(grouped[section], key=lambda card: (card.card_name.lower(), card.raw_name or "", card.quantity))),
            unsupported=False,
            metadata={"card_count": sum(card.quantity for card in grouped[section])},
        )
        for section in ("commander", "mainboard", "sideboard")
        if grouped[section]
    )
    return CockatriceExportPacket(
        export_id=export_id,
        interoperability_version=COCKATRICE_INTEROPERABILITY_VERSION,
        target_format=opts.target_format,
        deck_name=deck_name,
        zones=zones,
        warnings=tuple(sorted(warnings, key=lambda item: (item.warning_code, item.card_name or ""))),
        failures=tuple(sorted(failures, key=lambda item: (item.failure_code, item.card_name or ""))),
        metadata=metadata or {"file_writing_authorized": False},
    )


def validate_cockatrice_imported_deck(deck: CockatriceImportedDeck) -> CockatriceImportedDeck:
    if not isinstance(deck, CockatriceImportedDeck):
        raise CockatriceInteropBuildError("deck must be CockatriceImportedDeck")
    if not deck.user_local:
        raise CockatriceInteropBuildError("Cockatrice imports must remain user-local")
    if deck.deck_metadata.get("not_tournament_evidence") is not True:
        raise CockatriceInteropBuildError("Cockatrice imports must be labeled not_tournament_evidence")
    _reject_private_and_action_content(deck.to_dict(), "deck")
    return deck


def validate_cockatrice_export_packet(packet: CockatriceExportPacket) -> CockatriceExportPacket:
    if not isinstance(packet, CockatriceExportPacket):
        raise CockatriceInteropBuildError("packet must be CockatriceExportPacket")
    if not packet.zones and not packet.failures:
        raise CockatriceInteropBuildError("export packet must include zones or visible failures")
    _reject_private_and_action_content(packet.to_dict(), "export_packet")
    return packet


def cockatrice_imported_deck_to_dict(deck: CockatriceImportedDeck) -> dict[str, Any]:
    return validate_cockatrice_imported_deck(deck).to_dict()


def cockatrice_export_packet_to_dict(packet: CockatriceExportPacket) -> dict[str, Any]:
    return validate_cockatrice_export_packet(packet).to_dict()


def _failed_import(source_file_label: str, failure_code: str, message: str) -> CockatriceImportedDeck:
    return CockatriceImportedDeck(
        deck_id=f"cockatrice:{source_file_label}",
        interoperability_version=COCKATRICE_INTEROPERABILITY_VERSION,
        source_format=COCKATRICE_SOURCE_FORMAT,
        source_file_label=source_file_label,
        deck_name="Invalid Cockatrice Deck",
        deck_metadata={"not_tournament_evidence": True, "user_local": True},
        zones=(),
        warnings=(),
        failures=(CockatriceImportFailure(failure_code=failure_code, message=message),),
        unsupported_items=(),
        user_local=True,
    )


def _cards_from_zone(
    zone_element: ET.Element,
    raw_zone: str,
    section_name: str,
    failures: list[CockatriceImportFailure],
    warnings: list[CockatriceImportWarning],
    options: CockatriceImportOptions,
) -> list[CockatriceDeckCard]:
    cards: list[CockatriceDeckCard] = []
    seen: set[tuple[str, str]] = set()
    for card_element in zone_element.findall("card"):
        raw_name = _optional_text(card_element.attrib.get("name"))
        quantity_text = _optional_text(card_element.attrib.get("number")) or _optional_text(card_element.attrib.get("quantity"))
        quantity = _parse_quantity(quantity_text)
        if raw_name is None or quantity is None:
            failures.append(
                CockatriceImportFailure(
                    failure_code="COCKATRICE_CARD_UNRESOLVED",
                    message="card row is missing name or valid quantity",
                    zone_name=raw_zone,
                    card_name=raw_name,
                )
            )
            continue
        scryfall_id = _optional_text(card_element.attrib.get("scryfall_id")) or _optional_text(card_element.attrib.get("scryfallId"))
        oracle_id = _optional_text(card_element.attrib.get("oracle_id")) or _optional_text(card_element.attrib.get("oracleId"))
        unresolved = options.unresolved_without_identity and not (scryfall_id or oracle_id)
        duplicate_key = (section_name, raw_name.lower())
        if duplicate_key in seen:
            warnings.append(
                CockatriceImportWarning(
                    warning_code="COCKATRICE_DUPLICATE_CARD_ROW",
                    message="duplicate card row preserved with caveat",
                    zone_name=raw_zone,
                    card_name=raw_name,
                )
            )
        seen.add(duplicate_key)
        if unresolved:
            warnings.append(
                CockatriceImportWarning(
                    warning_code="COCKATRICE_CARD_UNRESOLVED",
                    message="card row has no supplied Scryfall or Oracle identity",
                    zone_name=raw_zone,
                    card_name=raw_name,
                )
            )
        cards.append(
            CockatriceDeckCard(
                card_name=raw_name,
                quantity=quantity,
                zone_name=raw_zone,
                section_name=section_name,
                raw_name=raw_name,
                scryfall_id=scryfall_id,
                oracle_id=oracle_id,
                unresolved=unresolved,
            )
        )
    return cards


def _unsafe_xml_reason(text: str) -> str | None:
    lowered = text.lower()
    if "<!doctype" in lowered:
        return "DTD declarations are not allowed"
    if "<!entity" in lowered:
        return "XML entity declarations are not allowed"
    if "system \"" in lowered or "system '" in lowered or "public \"" in lowered or "public '" in lowered:
        return "remote XML resource references are not allowed"
    return None


def _xml_privacy_reason(root: ET.Element) -> str | None:
    for element in root.iter():
        for key in element.attrib:
            lowered = key.lower()
            if lowered in _BLOCKED_PRIVATE_KEYS:
                return f"private Cockatrice metadata attribute rejected: {key}"
    return None


def _find_deck_name(root: ET.Element) -> str | None:
    for element in root.iter():
        if _strip_namespace(element.tag) == "deckname" and element.text:
            return _optional_text(element.text)
    return None


def _normalize_zone(value: str) -> str | None:
    return _KNOWN_XML_ZONES.get(value.strip().lower())


def _parse_quantity(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        quantity = int(value)
    except ValueError:
        return None
    return quantity if quantity > 0 else None


def _zone_from_mapping(value: Mapping[str, Any]) -> CockatriceDeckZone:
    _require_mapping(value, "zone")
    return CockatriceDeckZone(
        zone_name=value.get("zone_name"),
        section_name=value.get("section_name"),
        cards=tuple(CockatriceDeckCard.from_mapping(card) for card in value.get("cards", ())),
        unsupported=bool(value.get("unsupported", False)),
        metadata=value.get("metadata", {}),
    )


def _immutable_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    _require_mapping(value, field_name)
    frozen: dict[str, Any] = {}
    for key, item in value.items():
        _require_text(str(key), f"{field_name} key")
        lowered = str(key).lower()
        if lowered in _BLOCKED_PRIVATE_KEYS:
            raise CockatriceInteropBuildError(f"{field_name} contains private/raw metadata")
        if lowered in _FORBIDDEN_ACTION_KEYS:
            raise CockatriceInteropBuildError(f"{field_name} contains action-advice metadata")
        frozen[str(key)] = _freeze_json(item, field_name)
    return MappingProxyType(frozen)


def _freeze_json(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        return _immutable_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise CockatriceInteropBuildError(f"{field_name} must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _reject_private_and_action_content(value: Any, field_name: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered_key = str(key).lower()
            if lowered_key in _BLOCKED_PRIVATE_KEYS:
                raise CockatriceInteropBuildError(f"{field_name} contains private/raw metadata")
            if lowered_key in _FORBIDDEN_ACTION_KEYS:
                raise CockatriceInteropBuildError(f"{field_name} contains action-advice metadata")
            _reject_private_and_action_content(item, f"{field_name}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_private_and_action_content(item, f"{field_name}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if any(phrase in lowered for phrase in _FORBIDDEN_ACTION_LANGUAGE):
            raise CockatriceInteropBuildError(f"{field_name} contains action-advice language")


def _object_tuple(values: tuple[Any, ...], expected_type: type, field_name: str) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise CockatriceInteropBuildError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, expected_type):
            raise CockatriceInteropBuildError(f"{field_name} contains invalid item")
    return values


def _strip_namespace(value: str) -> str:
    return value.rsplit("}", 1)[-1]


def _require_mapping(value: Any, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise CockatriceInteropBuildError(f"{field_name} must be a mapping")


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CockatriceInteropBuildError(f"{field_name} is required")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def _require_positive_int(value: Any, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise CockatriceInteropBuildError(f"{field_name} must be a positive integer")


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise CockatriceInteropBuildError(f"{field_name} must be a non-negative integer")
