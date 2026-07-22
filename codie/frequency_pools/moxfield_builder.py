"""Local Moxfield export parser for Frequency Pool packet construction.

The builder accepts already supplied local text or local payload values. URL
inputs are identifiers only; this module does not fetch decks or call provider
APIs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import re
from types import MappingProxyType
from typing import Any, Mapping

from codie.frequency_pools.models import (
    FrequencyPoolBuildError,
    FrequencyPoolCardIdentity,
    FrequencyPoolCardRow,
    FrequencyPoolCaveat,
    FrequencyPoolCoverageReport,
    FrequencyPoolPacket,
    FrequencyPoolSourceRef,
    FrequencyPoolSourceWindow,
    FrequencyPoolSubject,
    build_frequency_pool_packet,
    frequency_pool_packet_to_dict,
    validate_frequency_pool_packet,
)


MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION = "moxfield-frequency-pool-builder-v1"

RECOGNIZED_SECTIONS = frozenset(
    {
        "commander",
        "commanders",
        "mainboard",
        "sideboard",
        "maybeboard",
        "considering",
        "tokens",
    }
)
DEFAULT_INCLUDED_SECTIONS = ("mainboard",)
DEFAULT_EXCLUDED_SECTIONS = (
    "commander",
    "sideboard",
    "maybeboard",
    "considering",
    "tokens",
    "attractions",
    "stickers",
    "planes",
    "schemes",
)
DEFAULT_BASIC_LANDS = frozenset(
    {
        "Plains",
        "Island",
        "Swamp",
        "Mountain",
        "Forest",
        "Wastes",
        "Snow-Covered Plains",
        "Snow-Covered Island",
        "Snow-Covered Swamp",
        "Snow-Covered Mountain",
        "Snow-Covered Forest",
    }
)
SUPPORTED_FAILURE_CODES = frozenset(
    {
        "MOXFIELD_FETCH_BLOCKED",
        "MOXFIELD_PRIVATE_DECK",
        "MOXFIELD_DECK_NOT_FOUND",
        "MOXFIELD_API_SCHEMA_CHANGED",
        "CARD_UNRESOLVED",
        "SECTION_UNKNOWN",
        "DUPLICATE_DECK_INPUT",
        "EMPTY_DECKLIST",
        "UNSUPPORTED_EXPORT_FORMAT",
        "URL_PAYLOAD_UNAVAILABLE",
    }
)

_MOXFIELD_PUBLIC_ID_PATTERNS = (
    re.compile(r"^https?://(?:www\.)?moxfield\.com/decks/([A-Za-z0-9_-]+)(?:[/?#].*)?$"),
    re.compile(r"^moxfield:([A-Za-z0-9_-]+)$"),
)
_CARD_LINE_RE = re.compile(r"^\s*(?P<count>\d+)\s+(?P<name>.+?)\s*$")
_SET_SUFFIX_RE = re.compile(r"\s+\([A-Z0-9]{2,8}\)\s+\d+[A-Za-z]?\s*$")
_COLLECTOR_SUFFIX_RE = re.compile(r"\s+\[[^\]]+\]\s*$")
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
_FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "card_rank",
        "cut_card",
        "cut_" + "rec" + "ommendation",
        "include_card",
        "include_" + "rec" + "ommendation",
        "rec" + "ommendation",
        "rec" + "ommendation_score",
        "score",
        "strategic_rank",
    }
)
_FORBIDDEN_LANGUAGE = (
    "should " + "play",
    "should " + "include",
    "should " + "cut",
    "must " + "include",
    "must " + "cut",
    "rec" + "ommended include",
    "rec" + "ommended cut",
    "auto" + "-include",
    "strict " + "upgrade",
    "optimal",
    "pilot " + "intent",
)


class MoxfieldFrequencyPoolBuildError(FrequencyPoolBuildError):
    """Raised when local Moxfield frequency-pool input is invalid."""


@dataclass(frozen=True)
class MoxfieldDeckInputRef:
    input_ref_id: str
    input_type: str
    source_key: str
    export_text: str | None = None
    payload: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.input_ref_id, "input_ref_id")
        _require_text(self.input_type, "input_type")
        _require_text(self.source_key, "source_key")
        if self.input_type not in {"url", "deck_id", "text_export", "fixture_payload"}:
            raise MoxfieldFrequencyPoolBuildError("unsupported input_type")
        if self.export_text is not None and not isinstance(self.export_text, str):
            raise MoxfieldFrequencyPoolBuildError("export_text must be text")
        object.__setattr__(self, "payload", _immutable_json_mapping(self.payload, "payload"))
        object.__setattr__(self, "metadata", _immutable_json_mapping(self.metadata, "metadata"))

    def to_dict(self, *, include_export_text: bool = False) -> dict[str, Any]:
        data = {
            "input_ref_id": self.input_ref_id,
            "input_type": self.input_type,
            "source_key": self.source_key,
            "payload": _thaw_json(self.payload),
            "metadata": _thaw_json(self.metadata),
        }
        if include_export_text:
            data["export_text"] = self.export_text
        else:
            data["has_export_text"] = self.export_text is not None
        return data


@dataclass(frozen=True)
class MoxfieldDeckCard:
    raw_name: str
    card_name: str
    count: int
    section: str
    scryfall_id: str | None = None
    oracle_id: str | None = None
    unresolved: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.raw_name, "raw_name")
        _require_text(self.card_name, "card_name")
        _require_non_negative_int(self.count, "count")
        if self.count <= 0:
            raise MoxfieldFrequencyPoolBuildError("count must be positive")
        _require_text(self.section, "section")
        if self.scryfall_id is not None:
            _require_text(self.scryfall_id, "scryfall_id")
        if self.oracle_id is not None:
            _require_text(self.oracle_id, "oracle_id")
        object.__setattr__(self, "metadata", _immutable_json_mapping(self.metadata, "card.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_name": self.raw_name,
            "card_name": self.card_name,
            "count": self.count,
            "section": self.section,
            "scryfall_id": self.scryfall_id,
            "oracle_id": self.oracle_id,
            "unresolved": self.unresolved,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class MoxfieldDeckParseWarning:
    warning_code: str
    message: str
    input_ref_id: str
    section: str | None = None
    raw_value: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.warning_code, "warning_code")
        _require_text(self.message, "message")
        _require_text(self.input_ref_id, "input_ref_id")
        if self.section is not None:
            _require_text(self.section, "section")
        if self.raw_value is not None:
            _require_text(self.raw_value, "raw_value")

    def to_dict(self) -> dict[str, Any]:
        return {
            "warning_code": self.warning_code,
            "message": self.message,
            "input_ref_id": self.input_ref_id,
            "section": self.section,
            "raw_value": self.raw_value,
        }


@dataclass(frozen=True)
class MoxfieldDeckParseFailure:
    failure_code: str
    message: str
    input_ref_id: str
    section: str | None = None
    raw_value: str | None = None

    def __post_init__(self) -> None:
        if self.failure_code not in SUPPORTED_FAILURE_CODES:
            raise MoxfieldFrequencyPoolBuildError("unsupported failure_code")
        _require_text(self.message, "message")
        _require_text(self.input_ref_id, "input_ref_id")
        if self.section is not None:
            _require_text(self.section, "section")
        if self.raw_value is not None:
            _require_text(self.raw_value, "raw_value")

    def to_dict(self) -> dict[str, Any]:
        return {
            "failure_code": self.failure_code,
            "message": self.message,
            "input_ref_id": self.input_ref_id,
            "section": self.section,
            "raw_value": self.raw_value,
        }


@dataclass(frozen=True)
class MoxfieldParsedDeck:
    input_ref: MoxfieldDeckInputRef
    public_id: str | None
    cards: tuple[MoxfieldDeckCard, ...]
    warnings: tuple[MoxfieldDeckParseWarning, ...] = ()
    failures: tuple[MoxfieldDeckParseFailure, ...] = ()
    accepted: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.input_ref, MoxfieldDeckInputRef):
            raise MoxfieldFrequencyPoolBuildError("input_ref must be MoxfieldDeckInputRef")
        if self.public_id is not None:
            _require_text(self.public_id, "public_id")
        object.__setattr__(self, "cards", _object_tuple(self.cards, MoxfieldDeckCard, "cards"))
        object.__setattr__(self, "warnings", _object_tuple(self.warnings, MoxfieldDeckParseWarning, "warnings"))
        object.__setattr__(self, "failures", _object_tuple(self.failures, MoxfieldDeckParseFailure, "failures"))
        object.__setattr__(self, "metadata", _immutable_json_mapping(self.metadata, "parsed_deck.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_ref": self.input_ref.to_dict(),
            "public_id": self.public_id,
            "cards": [card.to_dict() for card in self.cards],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "failures": [failure.to_dict() for failure in self.failures],
            "accepted": self.accepted,
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class MoxfieldFrequencyPoolBuilderOptions:
    included_sections: tuple[str, ...] = DEFAULT_INCLUDED_SECTIONS
    excluded_sections: tuple[str, ...] = DEFAULT_EXCLUDED_SECTIONS
    exclude_basic_lands: bool = True
    deck_presence_frequency: bool = True
    user_local: bool = True
    generated_at: str = "1970-01-01T00:00:00Z"
    identity_version: str = "supplied-moxfield-identity-v1"
    tag_ontology_version: str = "not-applied"
    evidence_version: str = MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "included_sections", _normalized_section_tuple(self.included_sections, "included_sections"))
        object.__setattr__(self, "excluded_sections", _normalized_section_tuple(self.excluded_sections, "excluded_sections"))
        for value, field_name in (
            (self.generated_at, "generated_at"),
            (self.identity_version, "identity_version"),
            (self.tag_ontology_version, "tag_ontology_version"),
            (self.evidence_version, "evidence_version"),
        ):
            _require_text(value, field_name)
        if not self.deck_presence_frequency:
            raise MoxfieldFrequencyPoolBuildError("deck presence frequency is required by default")

    def to_dict(self) -> dict[str, Any]:
        return {
            "included_sections": list(self.included_sections),
            "excluded_sections": list(self.excluded_sections),
            "exclude_basic_lands": self.exclude_basic_lands,
            "deck_presence_frequency": self.deck_presence_frequency,
            "user_local": self.user_local,
            "generated_at": self.generated_at,
            "identity_version": self.identity_version,
            "tag_ontology_version": self.tag_ontology_version,
            "evidence_version": self.evidence_version,
        }


@dataclass(frozen=True)
class MoxfieldFrequencyPoolBuildRequest:
    request_id: str
    subject_key: str
    inputs: tuple[MoxfieldDeckInputRef, ...]
    options: MoxfieldFrequencyPoolBuilderOptions = field(default_factory=MoxfieldFrequencyPoolBuilderOptions)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.request_id, "request_id")
        _require_text(self.subject_key, "subject_key")
        object.__setattr__(self, "inputs", _object_tuple(self.inputs, MoxfieldDeckInputRef, "inputs"))
        if not self.inputs:
            raise MoxfieldFrequencyPoolBuildError("inputs must not be empty")
        if not isinstance(self.options, MoxfieldFrequencyPoolBuilderOptions):
            raise MoxfieldFrequencyPoolBuildError("options must be MoxfieldFrequencyPoolBuilderOptions")
        object.__setattr__(self, "metadata", _immutable_json_mapping(self.metadata, "request.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "subject_key": self.subject_key,
            "inputs": [input_ref.to_dict() for input_ref in self.inputs],
            "options": self.options.to_dict(),
            "metadata": _thaw_json(self.metadata),
        }


@dataclass(frozen=True)
class MoxfieldFrequencyPoolBuildResult:
    request: MoxfieldFrequencyPoolBuildRequest
    parsed_decks: tuple[MoxfieldParsedDeck, ...]
    frequency_pool: FrequencyPoolPacket
    input_count: int
    accepted_deck_count: int
    failed_deck_count: int
    duplicate_deck_count: int
    partial_failure_count: int
    warnings: tuple[MoxfieldDeckParseWarning, ...]
    failures: tuple[MoxfieldDeckParseFailure, ...]
    unresolved_cards: tuple[MoxfieldDeckCard, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.request, MoxfieldFrequencyPoolBuildRequest):
            raise MoxfieldFrequencyPoolBuildError("request must be MoxfieldFrequencyPoolBuildRequest")
        object.__setattr__(self, "parsed_decks", _object_tuple(self.parsed_decks, MoxfieldParsedDeck, "parsed_decks"))
        if not isinstance(self.frequency_pool, FrequencyPoolPacket):
            raise MoxfieldFrequencyPoolBuildError("frequency_pool must be FrequencyPoolPacket")
        for value, field_name in (
            (self.input_count, "input_count"),
            (self.accepted_deck_count, "accepted_deck_count"),
            (self.failed_deck_count, "failed_deck_count"),
            (self.duplicate_deck_count, "duplicate_deck_count"),
            (self.partial_failure_count, "partial_failure_count"),
        ):
            _require_non_negative_int(value, field_name)
        object.__setattr__(self, "warnings", _object_tuple(self.warnings, MoxfieldDeckParseWarning, "warnings"))
        object.__setattr__(self, "failures", _object_tuple(self.failures, MoxfieldDeckParseFailure, "failures"))
        object.__setattr__(self, "unresolved_cards", _object_tuple(self.unresolved_cards, MoxfieldDeckCard, "unresolved_cards"))
        object.__setattr__(self, "metadata", _immutable_json_mapping(self.metadata, "result.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "builder_version": MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION,
            "request": self.request.to_dict(),
            "parsed_decks": [deck.to_dict() for deck in self.parsed_decks],
            "frequency_pool": frequency_pool_packet_to_dict(self.frequency_pool),
            "input_count": self.input_count,
            "accepted_deck_count": self.accepted_deck_count,
            "failed_deck_count": self.failed_deck_count,
            "duplicate_deck_count": self.duplicate_deck_count,
            "partial_failure_count": self.partial_failure_count,
            "warnings": [warning.to_dict() for warning in self.warnings],
            "failures": [failure.to_dict() for failure in self.failures],
            "unresolved_cards": [card.to_dict() for card in self.unresolved_cards],
            "metadata": _thaw_json(self.metadata),
        }


def extract_moxfield_public_id(value: str) -> str:
    _require_text(value, "moxfield URL")
    stripped = value.strip()
    for pattern in _MOXFIELD_PUBLIC_ID_PATTERNS:
        match = pattern.match(stripped)
        if match:
            return match.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{8,}", stripped):
        return stripped
    raise MoxfieldFrequencyPoolBuildError("unsupported Moxfield URL or deck ID")


def parse_moxfield_export_text(
    export_text: str,
    *,
    input_ref: MoxfieldDeckInputRef,
    options: MoxfieldFrequencyPoolBuilderOptions | None = None,
) -> MoxfieldParsedDeck:
    opts = options or MoxfieldFrequencyPoolBuilderOptions()
    if not isinstance(input_ref, MoxfieldDeckInputRef):
        raise MoxfieldFrequencyPoolBuildError("input_ref must be MoxfieldDeckInputRef")
    if not isinstance(export_text, str) or not export_text.strip():
        failure = MoxfieldDeckParseFailure("EMPTY_DECKLIST", "Empty Moxfield export.", input_ref.input_ref_id)
        return MoxfieldParsedDeck(input_ref=input_ref, public_id=_public_id_or_none(input_ref), cards=(), failures=(failure,), accepted=False)

    cards: list[MoxfieldDeckCard] = []
    warnings: list[MoxfieldDeckParseWarning] = []
    failures: list[MoxfieldDeckParseFailure] = []
    current_section: str | None = None
    saw_section = False
    identity_map = _identity_map_from_payload(input_ref.payload)

    for raw_line in export_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized_header = _normalize_section(line)
        if normalized_header is not None:
            saw_section = True
            current_section = normalized_header
            if normalized_header not in RECOGNIZED_SECTIONS:
                warnings.append(
                    MoxfieldDeckParseWarning(
                        "SECTION_UNKNOWN",
                        "Unknown Moxfield export section.",
                        input_ref.input_ref_id,
                        section=normalized_header,
                        raw_value=line,
                    )
                )
            continue
        if current_section is None:
            warnings.append(
                MoxfieldDeckParseWarning(
                    "UNSUPPORTED_EXPORT_FORMAT",
                    "Card line appeared before a section header.",
                    input_ref.input_ref_id,
                    raw_value=line,
                )
            )
            continue
        match = _CARD_LINE_RE.match(line)
        if not match:
            warnings.append(
                MoxfieldDeckParseWarning(
                    "UNSUPPORTED_EXPORT_FORMAT",
                    "Could not parse Moxfield card line.",
                    input_ref.input_ref_id,
                    section=current_section,
                    raw_value=line,
                )
            )
            continue
        count = int(match.group("count"))
        raw_name = _clean_card_name(match.group("name"))
        card_name = _display_name(raw_name)
        supplied_identity = identity_map.get(_identity_key(card_name), {})
        oracle_id = _optional_text(supplied_identity.get("oracle_id"))
        scryfall_id = _optional_text(supplied_identity.get("scryfall_id"))
        unresolved = oracle_id is None
        card = MoxfieldDeckCard(
            raw_name=raw_name,
            card_name=card_name,
            count=count,
            section=current_section,
            oracle_id=oracle_id,
            scryfall_id=scryfall_id,
            unresolved=unresolved,
            metadata={"identity_source": "supplied" if oracle_id else "unresolved"},
        )
        cards.append(card)
        if unresolved:
            failures.append(
                MoxfieldDeckParseFailure(
                    "CARD_UNRESOLVED",
                    "Card identity was not supplied.",
                    input_ref.input_ref_id,
                    section=current_section,
                    raw_value=raw_name,
                )
            )
    if not saw_section:
        failures.append(MoxfieldDeckParseFailure("UNSUPPORTED_EXPORT_FORMAT", "No recognized export sections were found.", input_ref.input_ref_id))
    included_cards = tuple(card for card in cards if _include_card(card, opts))
    accepted = bool(included_cards) and not any(f.failure_code in {"EMPTY_DECKLIST", "UNSUPPORTED_EXPORT_FORMAT"} for f in failures)
    return MoxfieldParsedDeck(
        input_ref=input_ref,
        public_id=_public_id_or_none(input_ref),
        cards=included_cards,
        warnings=tuple(warnings),
        failures=tuple(failures),
        accepted=accepted,
        metadata={
            "included_sections": list(opts.included_sections),
            "excluded_sections": list(opts.excluded_sections),
            "exclude_basic_lands": opts.exclude_basic_lands,
        },
    )


def build_moxfield_frequency_pool_request(
    *,
    request_id: str,
    subject_key: str,
    inputs: tuple[MoxfieldDeckInputRef, ...],
    options: MoxfieldFrequencyPoolBuilderOptions | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> MoxfieldFrequencyPoolBuildRequest:
    return MoxfieldFrequencyPoolBuildRequest(
        request_id=request_id,
        subject_key=subject_key,
        inputs=inputs,
        options=options or MoxfieldFrequencyPoolBuilderOptions(),
        metadata=metadata or {},
    )


def build_moxfield_frequency_pool_from_parsed_decks(
    request: MoxfieldFrequencyPoolBuildRequest,
    parsed_decks: tuple[MoxfieldParsedDeck, ...],
) -> FrequencyPoolPacket:
    if not isinstance(request, MoxfieldFrequencyPoolBuildRequest):
        raise MoxfieldFrequencyPoolBuildError("request must be MoxfieldFrequencyPoolBuildRequest")
    parsed = _object_tuple(parsed_decks, MoxfieldParsedDeck, "parsed_decks")
    accepted = tuple(deck for deck in parsed if deck.accepted and deck.cards)
    source_refs = [
        FrequencyPoolSourceRef(
            source_ref_id=_source_ref_id(deck.input_ref.input_ref_id),
            source_type="moxfield_local_export",
            source_key=deck.public_id or deck.input_ref.source_key,
            provider="moxfield",
            deck_ref_id=deck.public_id,
            metadata={"user_local": True, "not_tournament_evidence": True},
        )
        for deck in accepted
    ]
    rows = _build_card_rows(accepted)
    caveats = _build_caveats(parsed)
    coverage_caveat_ids = tuple(caveat.caveat_id for caveat in caveats if caveat.caveat_type in {"partial_failure", "unresolved_cards"})
    payload = {
        "pool_id": f"moxfield-frequency-pool-{_stable_digest(request.request_id + request.subject_key)[:12]}",
        "pool_type": "user_local_snapshot",
        "subject": {
            "subject_type": "moxfield_frequency_pool",
            "subject_key": request.subject_key,
            "user_local": request.options.user_local,
            "metadata": {"source": "moxfield_local_exports"},
        },
        "source_window": FrequencyPoolSourceWindow(filters={"source": "local_moxfield_exports"}).to_dict(),
        "source_refs": [ref.to_dict() for ref in source_refs],
        "generated_at": request.options.generated_at,
        "cards": [row.to_dict() for row in rows],
        "tags": [],
        "coverage_report": FrequencyPoolCoverageReport(
            matching_deck_count=len(accepted),
            available_deck_count=len(parsed),
            coverage_ratio=(len(accepted) / len(parsed)) if parsed else 0.0,
            low_sample_threshold=1,
            low_coverage_threshold=0.0,
            caveat_ids=coverage_caveat_ids,
            metadata={"accepted_deck_count": len(accepted), "input_count": len(parsed)},
        ).to_dict(),
        "caveats": [caveat.to_dict() for caveat in caveats],
        "filters": {
            "included_sections": list(request.options.included_sections),
            "excluded_sections": list(request.options.excluded_sections),
            "exclude_basic_lands": request.options.exclude_basic_lands,
            "deck_presence_frequency": request.options.deck_presence_frequency,
        },
        "identity_version": request.options.identity_version,
        "tag_ontology_version": request.options.tag_ontology_version,
        "evidence_version": request.options.evidence_version,
        "metadata": {
            "builder_version": MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION,
            "user_local": True,
            "isolated_from_global_pools": True,
            "not_tournament_evidence": True,
            "not_" + "rec" + "ommendation_input": True,
            "frequency_basis": "deck_presence",
        },
    }
    return build_frequency_pool_packet(payload)


def build_moxfield_frequency_pool_result(
    request: MoxfieldFrequencyPoolBuildRequest,
    parsed_decks: tuple[MoxfieldParsedDeck, ...] | None = None,
) -> MoxfieldFrequencyPoolBuildResult:
    if not isinstance(request, MoxfieldFrequencyPoolBuildRequest):
        raise MoxfieldFrequencyPoolBuildError("request must be MoxfieldFrequencyPoolBuildRequest")
    duplicates = _duplicate_input_ids(request.inputs)
    if parsed_decks is None:
        parsed = tuple(
            _duplicate_failure_deck(input_ref) if input_ref.input_ref_id in duplicates else _parse_input_ref(input_ref, request.options)
            for input_ref in request.inputs
        )
    else:
        parsed = parsed_decks
    parsed = _object_tuple(parsed, MoxfieldParsedDeck, "parsed_decks")
    packet = build_moxfield_frequency_pool_from_parsed_decks(request, parsed)
    warnings = tuple(warning for deck in parsed for warning in deck.warnings)
    failures = tuple(failure for deck in parsed for failure in deck.failures)
    unresolved = tuple(card for deck in parsed for card in deck.cards if card.unresolved)
    accepted_count = sum(1 for deck in parsed if deck.accepted and deck.cards)
    failed_count = sum(1 for deck in parsed if not deck.accepted)
    partial_count = sum(1 for deck in parsed if deck.accepted and deck.failures)
    result = MoxfieldFrequencyPoolBuildResult(
        request=request,
        parsed_decks=parsed,
        frequency_pool=packet,
        input_count=len(request.inputs),
        accepted_deck_count=accepted_count,
        failed_deck_count=failed_count,
        duplicate_deck_count=len(duplicates),
        partial_failure_count=partial_count,
        warnings=warnings,
        failures=failures,
        unresolved_cards=unresolved,
        metadata={
            "included_sections": list(request.options.included_sections),
            "excluded_sections": list(request.options.excluded_sections),
            "exclude_basic_lands": request.options.exclude_basic_lands,
            "deck_presence_frequency": request.options.deck_presence_frequency,
            "user_local": True,
            "not_tournament_evidence": True,
        },
    )
    return validate_moxfield_frequency_pool_result(result)


def validate_moxfield_frequency_pool_result(result: MoxfieldFrequencyPoolBuildResult) -> MoxfieldFrequencyPoolBuildResult:
    if not isinstance(result, MoxfieldFrequencyPoolBuildResult):
        raise MoxfieldFrequencyPoolBuildError("result must be MoxfieldFrequencyPoolBuildResult")
    validate_frequency_pool_packet(result.frequency_pool)
    _reject_private_and_action_content(result.to_dict(), "result")
    return result


def moxfield_frequency_pool_result_to_dict(result: MoxfieldFrequencyPoolBuildResult) -> dict[str, Any]:
    validate_moxfield_frequency_pool_result(result)
    return result.to_dict()


def _parse_input_ref(input_ref: MoxfieldDeckInputRef, options: MoxfieldFrequencyPoolBuilderOptions) -> MoxfieldParsedDeck:
    if input_ref.input_type == "url" and input_ref.export_text is None:
        failure = MoxfieldDeckParseFailure("URL_PAYLOAD_UNAVAILABLE", "URL inputs require supplied local payload.", input_ref.input_ref_id)
        return MoxfieldParsedDeck(input_ref=input_ref, public_id=_public_id_or_none(input_ref), cards=(), failures=(failure,), accepted=False)
    if input_ref.payload.get("failure_code"):
        failure = MoxfieldDeckParseFailure(str(input_ref.payload["failure_code"]), str(input_ref.payload.get("message", "Moxfield payload failure.")), input_ref.input_ref_id)
        return MoxfieldParsedDeck(input_ref=input_ref, public_id=_public_id_or_none(input_ref), cards=(), failures=(failure,), accepted=False)
    if input_ref.export_text is None:
        failure = MoxfieldDeckParseFailure("EMPTY_DECKLIST", "Input does not include local export text.", input_ref.input_ref_id)
        return MoxfieldParsedDeck(input_ref=input_ref, public_id=_public_id_or_none(input_ref), cards=(), failures=(failure,), accepted=False)
    return parse_moxfield_export_text(input_ref.export_text, input_ref=input_ref, options=options)


def _duplicate_failure_deck(input_ref: MoxfieldDeckInputRef) -> MoxfieldParsedDeck:
    failure = MoxfieldDeckParseFailure(
        "DUPLICATE_DECK_INPUT",
        "Duplicate Moxfield deck input.",
        input_ref.input_ref_id,
        raw_value=input_ref.source_key,
    )
    return MoxfieldParsedDeck(
        input_ref=input_ref,
        public_id=_public_id_or_none(input_ref),
        cards=(),
        failures=(failure,),
        accepted=False,
    )


def _build_card_rows(parsed_decks: tuple[MoxfieldParsedDeck, ...]) -> tuple[FrequencyPoolCardRow, ...]:
    deck_total = len(parsed_decks)
    card_sources: dict[str, set[str]] = {}
    card_identity: dict[str, MoxfieldDeckCard] = {}
    total_copies: dict[str, int] = {}
    for deck in parsed_decks:
        seen_in_deck: set[str] = set()
        for card in deck.cards:
            key = card.oracle_id or f"unresolved:{_identity_key(card.card_name)}"
            card_identity.setdefault(key, card)
            total_copies[key] = total_copies.get(key, 0) + card.count
            if key in seen_in_deck:
                continue
            seen_in_deck.add(key)
            card_sources.setdefault(key, set()).add(_source_ref_id(deck.input_ref.input_ref_id))
    rows: list[FrequencyPoolCardRow] = []
    for key, source_ids in card_sources.items():
        card = card_identity[key]
        deck_count = len(source_ids)
        oracle_id = card.oracle_id or f"unresolved:{_stable_digest(card.card_name)[:12]}"
        metadata: dict[str, Any] = {
            "raw_name": card.raw_name,
            "unresolved": card.unresolved,
            "deck_presence_count": deck_count,
            "total_copy_count": total_copies[key],
            "frequency_basis": "deck_presence",
            "frequency_label": f"{deck_count}/{deck_total}",
        }
        rows.append(
            FrequencyPoolCardRow(
                identity=FrequencyPoolCardIdentity(
                    oracle_id=oracle_id,
                    scryfall_id=card.scryfall_id,
                    card_name=card.card_name,
                ),
                card_count=total_copies[key],
                deck_count=deck_count,
                inclusion_rate=(deck_count / deck_total) if deck_total else 0.0,
                average_copies=total_copies[key] / deck_count,
                confidence=0.0 if card.unresolved else 1.0,
                source_ref_ids=tuple(sorted(source_ids)),
                caveat_ids=("cav-unresolved-cards",) if card.unresolved else (),
                metadata=metadata,
            )
        )
    rows.sort(key=lambda row: (-(row.deck_count or 0), row.identity.card_name.lower()))
    return tuple(rows)


def _build_caveats(parsed_decks: tuple[MoxfieldParsedDeck, ...]) -> tuple[FrequencyPoolCaveat, ...]:
    caveats: list[FrequencyPoolCaveat] = []
    failures = tuple(failure for deck in parsed_decks for failure in deck.failures)
    if failures:
        caveats.append(
            FrequencyPoolCaveat(
                caveat_id="cav-partial-failures",
                caveat_type="partial_failure",
                message="One or more local Moxfield inputs produced visible failures.",
                severity="warning",
                metadata={"failure_count": len(failures)},
            )
        )
    unresolved_count = sum(1 for deck in parsed_decks for card in deck.cards if card.unresolved)
    if unresolved_count:
        caveats.append(
            FrequencyPoolCaveat(
                caveat_id="cav-unresolved-cards",
                caveat_type="unresolved_cards",
                message="One or more cards lacked supplied canonical identity.",
                severity="warning",
                metadata={"unresolved_card_count": unresolved_count},
            )
        )
    return tuple(caveats)


def _identity_map_from_payload(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    identities = payload.get("card_identities", {})
    if not isinstance(identities, Mapping):
        raise MoxfieldFrequencyPoolBuildError("card_identities must be a mapping")
    return {_identity_key(str(name)): identity for name, identity in identities.items() if isinstance(identity, Mapping)}


def _include_card(card: MoxfieldDeckCard, options: MoxfieldFrequencyPoolBuilderOptions) -> bool:
    section = _canonical_section(card.section)
    if section not in options.included_sections:
        return False
    if section in options.excluded_sections:
        return False
    if options.exclude_basic_lands and card.card_name in DEFAULT_BASIC_LANDS:
        return False
    return True


def _normalize_section(value: str) -> str | None:
    cleaned = value.strip().strip(":").lower().replace(" ", "_")
    if cleaned in RECOGNIZED_SECTIONS or cleaned in DEFAULT_EXCLUDED_SECTIONS:
        return cleaned
    if value.isupper() and not _CARD_LINE_RE.match(value):
        return cleaned
    return None


def _canonical_section(section: str) -> str:
    return "commander" if section == "commanders" else section


def _clean_card_name(value: str) -> str:
    cleaned = value.strip()
    cleaned = _SET_SUFFIX_RE.sub("", cleaned)
    cleaned = _COLLECTOR_SUFFIX_RE.sub("", cleaned)
    return cleaned.strip()


def _display_name(value: str) -> str:
    return " ".join(value.split())


def _identity_key(value: str) -> str:
    return " ".join(value.lower().split())


def _duplicate_input_ids(inputs: tuple[MoxfieldDeckInputRef, ...]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for input_ref in inputs:
        key = _public_id_or_none(input_ref) or input_ref.source_key
        if key in seen:
            duplicates.add(input_ref.input_ref_id)
        seen.add(key)
    return duplicates


def _public_id_or_none(input_ref: MoxfieldDeckInputRef) -> str | None:
    try:
        return extract_moxfield_public_id(input_ref.source_key)
    except MoxfieldFrequencyPoolBuildError:
        return None


def _source_ref_id(input_ref_id: str) -> str:
    return f"moxfield:{input_ref_id}"


def _stable_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _normalized_section_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} must be a tuple")
    normalized = tuple(_canonical_section(value.strip().lower()) for value in values if isinstance(value, str) and value.strip())
    if len(normalized) != len(set(normalized)):
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} must not contain duplicates")
    if not normalized:
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} must not be empty")
    return normalized


def _immutable_json_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} must be a mapping")
    frozen: dict[str, Any] = {}
    for key, item in value.items():
        _require_text(key, f"{field_name} key")
        lowered = str(key).lower()
        if lowered in _BLOCKED_PRIVATE_KEYS:
            raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains private/raw metadata")
        if lowered in _FORBIDDEN_METADATA_KEYS:
            raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains action metadata")
        frozen[str(key)] = _freeze_json(item, field_name)
    return MappingProxyType(frozen)


def _freeze_json(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        return _immutable_json_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, str):
        lowered = value.lower()
        if any(phrase in lowered for phrase in _FORBIDDEN_LANGUAGE):
            raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains action language")
        return value
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    raise MoxfieldFrequencyPoolBuildError(f"{field_name} must be JSON-compatible")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _reject_private_and_action_content(value: Any, field_name: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            lowered_key = str(key).lower()
            if lowered_key in _BLOCKED_PRIVATE_KEYS:
                raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains private/raw metadata")
            if lowered_key in _FORBIDDEN_METADATA_KEYS:
                raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains action metadata")
            _reject_private_and_action_content(item, f"{field_name}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_private_and_action_content(item, f"{field_name}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if any(phrase in lowered for phrase in _FORBIDDEN_LANGUAGE):
            raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains action language")


def _object_tuple(values: tuple[Any, ...], expected_type: type, field_name: str) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, expected_type):
            raise MoxfieldFrequencyPoolBuildError(f"{field_name} contains invalid item")
    return values


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} is required")


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    _require_text(value, "optional text")
    return value


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise MoxfieldFrequencyPoolBuildError(f"{field_name} must be a non-negative integer")
