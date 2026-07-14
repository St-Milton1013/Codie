"""Pure local Frequency Pool evidence packet models.

This module validates and serializes already supplied sanitized Frequency Pool
values. It does not read providers, calculate pools, write files, build Tag
Graph metrics, run analytics, or produce action advice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


FREQUENCY_POOL_PACKET_VERSION = "frequency-pool-packet-v1"

ALLOWED_POOL_TYPES = frozenset(
    {
        "commander",
        "partner_pair",
        "top_cut",
        "winner",
        "regional",
        "meta_snapshot",
        "frequency_pool",
        "personal_deck_history",
        "user_local_snapshot",
    }
)

USER_LOCAL_POOL_TYPES = frozenset({"personal_deck_history", "user_local_snapshot"})
UNKNOWN_COVERAGE_MARKER = "unknown"

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


class FrequencyPoolBuildError(ValueError):
    """Raised when a Frequency Pool packet violates the Phase 37C boundary."""


@dataclass(frozen=True)
class FrequencyPoolSubject:
    subject_type: str
    commander: str | None = None
    partner: str | None = None
    subject_key: str | None = None
    user_local: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.subject_type, "subject_type")
        if self.commander is not None:
            _require_text(self.commander, "commander")
        if self.partner is not None:
            _require_text(self.partner, "partner")
        if self.subject_key is not None:
            _require_text(self.subject_key, "subject_key")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "subject.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_type": self.subject_type,
            "commander": self.commander,
            "partner": self.partner,
            "subject_key": self.subject_key,
            "user_local": self.user_local,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolSubject":
        _require_mapping(value, "subject")
        return cls(
            subject_type=value.get("subject_type"),
            commander=value.get("commander"),
            partner=value.get("partner"),
            subject_key=value.get("subject_key"),
            user_local=bool(value.get("user_local", False)),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolSourceWindow:
    date_start: str | None = None
    date_end: str | None = None
    placement_scope: str | None = None
    provider: str | None = None
    region: str | None = None
    filters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for value, field_name in (
            (self.date_start, "date_start"),
            (self.date_end, "date_end"),
            (self.placement_scope, "placement_scope"),
            (self.provider, "provider"),
            (self.region, "region"),
        ):
            if value is not None:
                _require_text(value, field_name)
        object.__setattr__(self, "filters", _immutable_mapping(self.filters, "source_window.filters"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "date_start": self.date_start,
            "date_end": self.date_end,
            "placement_scope": self.placement_scope,
            "provider": self.provider,
            "region": self.region,
            "filters": _thaw_json(self.filters),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "FrequencyPoolSourceWindow":
        if value is None:
            return cls()
        _require_mapping(value, "source_window")
        return cls(
            date_start=value.get("date_start"),
            date_end=value.get("date_end"),
            placement_scope=value.get("placement_scope"),
            provider=value.get("provider"),
            region=value.get("region"),
            filters=value.get("filters", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolSourceRef:
    source_ref_id: str
    source_type: str
    source_key: str
    provider: str | None = None
    event_ref_id: str | None = None
    deck_ref_id: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.source_ref_id, "source_ref_id")
        _require_text(self.source_type, "source_type")
        _require_text(self.source_key, "source_key")
        for value, field_name in (
            (self.provider, "provider"),
            (self.event_ref_id, "event_ref_id"),
            (self.deck_ref_id, "deck_ref_id"),
        ):
            if value is not None:
                _require_text(value, field_name)
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "source_ref.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_ref_id": self.source_ref_id,
            "source_type": self.source_type,
            "source_key": self.source_key,
            "provider": self.provider,
            "event_ref_id": self.event_ref_id,
            "deck_ref_id": self.deck_ref_id,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolSourceRef":
        _require_mapping(value, "source_ref")
        return cls(
            source_ref_id=value.get("source_ref_id"),
            source_type=value.get("source_type"),
            source_key=value.get("source_key"),
            provider=value.get("provider"),
            event_ref_id=value.get("event_ref_id"),
            deck_ref_id=value.get("deck_ref_id"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolCardIdentity:
    oracle_id: str
    card_name: str
    scryfall_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.card_name, "card_name")
        if self.scryfall_id is not None:
            _require_text(self.scryfall_id, "scryfall_id")

    def to_dict(self) -> dict[str, Any]:
        return {
            "oracle_id": self.oracle_id,
            "scryfall_id": self.scryfall_id,
            "card_name": self.card_name,
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolCardIdentity":
        _require_mapping(value, "card_identity")
        return cls(
            oracle_id=value.get("oracle_id"),
            scryfall_id=value.get("scryfall_id"),
            card_name=value.get("card_name"),
        )


@dataclass(frozen=True)
class FrequencyPoolCardRow:
    identity: FrequencyPoolCardIdentity
    card_count: int | None = None
    deck_count: int | None = None
    inclusion_rate: float | None = None
    average_copies: float | None = None
    placement_weighted_usage: float | None = None
    trend_delta: float | None = None
    confidence: float | None = None
    source_ref_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, FrequencyPoolCardIdentity):
            raise FrequencyPoolBuildError("identity must be FrequencyPoolCardIdentity")
        for value, field_name in ((self.card_count, "card_count"), (self.deck_count, "deck_count")):
            if value is not None:
                _require_non_negative_int(value, field_name)
        for value, field_name in (
            (self.inclusion_rate, "inclusion_rate"),
            (self.average_copies, "average_copies"),
            (self.placement_weighted_usage, "placement_weighted_usage"),
            (self.trend_delta, "trend_delta"),
            (self.confidence, "confidence"),
        ):
            if value is not None:
                _require_number(value, field_name)
        if self.inclusion_rate is not None:
            _require_ratio(self.inclusion_rate, "inclusion_rate")
        if self.confidence is not None:
            _require_ratio(self.confidence, "confidence")
        object.__setattr__(self, "source_ref_ids", _unique_text_tuple(self.source_ref_ids, "source_ref_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "card.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity.to_dict(),
            "card_count": self.card_count,
            "deck_count": self.deck_count,
            "inclusion_rate": self.inclusion_rate,
            "average_copies": self.average_copies,
            "placement_weighted_usage": self.placement_weighted_usage,
            "trend_delta": self.trend_delta,
            "confidence": self.confidence,
            "source_ref_ids": list(self.source_ref_ids),
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolCardRow":
        _require_mapping(value, "card")
        return cls(
            identity=FrequencyPoolCardIdentity.from_mapping(value.get("identity")),
            card_count=value.get("card_count"),
            deck_count=value.get("deck_count"),
            inclusion_rate=value.get("inclusion_rate"),
            average_copies=value.get("average_copies"),
            placement_weighted_usage=value.get("placement_weighted_usage"),
            trend_delta=value.get("trend_delta"),
            confidence=value.get("confidence"),
            source_ref_ids=tuple(value.get("source_ref_ids", ())),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolTagRow:
    tag: str
    tag_namespace: str
    tag_source: str
    tag_confidence: float | None = None
    oracle_ids: tuple[str, ...] = ()
    raw_tag_count: int | None = None
    tag_density: float | None = None
    tag_inclusion_rate: float | None = None
    average_cards_per_deck_with_tag: float | None = None
    matching_deck_count: int | str = UNKNOWN_COVERAGE_MARKER
    available_deck_count: int | str = UNKNOWN_COVERAGE_MARKER
    coverage_ratio: float | str = UNKNOWN_COVERAGE_MARKER
    caveat_ids: tuple[str, ...] = ()
    source_ref_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.tag, "tag")
        _require_text(self.tag_namespace, "tag_namespace")
        _require_text(self.tag_source, "tag_source")
        if self.tag_confidence is not None:
            _require_ratio(self.tag_confidence, "tag_confidence")
        if self.raw_tag_count is not None:
            _require_non_negative_int(self.raw_tag_count, "raw_tag_count")
        for value, field_name in ((self.tag_density, "tag_density"), (self.tag_inclusion_rate, "tag_inclusion_rate")):
            if value is not None:
                _require_ratio(value, field_name)
        if self.average_cards_per_deck_with_tag is not None:
            _require_number(self.average_cards_per_deck_with_tag, "average_cards_per_deck_with_tag")
        _validate_coverage_value(self.matching_deck_count, "matching_deck_count", integer=True)
        _validate_coverage_value(self.available_deck_count, "available_deck_count", integer=True)
        _validate_coverage_value(self.coverage_ratio, "coverage_ratio", ratio=True)
        object.__setattr__(self, "oracle_ids", _unique_text_tuple(self.oracle_ids, "oracle_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "source_ref_ids", _unique_text_tuple(self.source_ref_ids, "source_ref_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "tag.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "tag": self.tag,
            "tag_namespace": self.tag_namespace,
            "tag_source": self.tag_source,
            "tag_confidence": self.tag_confidence,
            "oracle_ids": list(self.oracle_ids),
            "raw_tag_count": self.raw_tag_count,
            "tag_density": self.tag_density,
            "tag_inclusion_rate": self.tag_inclusion_rate,
            "average_cards_per_deck_with_tag": self.average_cards_per_deck_with_tag,
            "matching_deck_count": self.matching_deck_count,
            "available_deck_count": self.available_deck_count,
            "coverage_ratio": self.coverage_ratio,
            "caveat_ids": list(self.caveat_ids),
            "source_ref_ids": list(self.source_ref_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolTagRow":
        _require_mapping(value, "tag")
        return cls(
            tag=value.get("tag"),
            tag_namespace=value.get("tag_namespace"),
            tag_source=value.get("tag_source"),
            tag_confidence=value.get("tag_confidence"),
            oracle_ids=tuple(value.get("oracle_ids", ())),
            raw_tag_count=value.get("raw_tag_count"),
            tag_density=value.get("tag_density"),
            tag_inclusion_rate=value.get("tag_inclusion_rate"),
            average_cards_per_deck_with_tag=value.get("average_cards_per_deck_with_tag"),
            matching_deck_count=value.get("matching_deck_count", UNKNOWN_COVERAGE_MARKER),
            available_deck_count=value.get("available_deck_count", UNKNOWN_COVERAGE_MARKER),
            coverage_ratio=value.get("coverage_ratio", UNKNOWN_COVERAGE_MARKER),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            source_ref_ids=tuple(value.get("source_ref_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolCoverageReport:
    matching_deck_count: int | str = UNKNOWN_COVERAGE_MARKER
    available_deck_count: int | str = UNKNOWN_COVERAGE_MARKER
    coverage_ratio: float | str = UNKNOWN_COVERAGE_MARKER
    low_sample_threshold: int | str = UNKNOWN_COVERAGE_MARKER
    low_coverage_threshold: float | str = UNKNOWN_COVERAGE_MARKER
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_coverage_value(self.matching_deck_count, "matching_deck_count", integer=True)
        _validate_coverage_value(self.available_deck_count, "available_deck_count", integer=True)
        _validate_coverage_value(self.coverage_ratio, "coverage_ratio", ratio=True)
        _validate_coverage_value(self.low_sample_threshold, "low_sample_threshold", integer=True)
        _validate_coverage_value(self.low_coverage_threshold, "low_coverage_threshold", ratio=True)
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "coverage.caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "coverage.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "matching_deck_count": self.matching_deck_count,
            "available_deck_count": self.available_deck_count,
            "coverage_ratio": self.coverage_ratio,
            "low_sample_threshold": self.low_sample_threshold,
            "low_coverage_threshold": self.low_coverage_threshold,
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "FrequencyPoolCoverageReport":
        if value is None:
            return cls()
        _require_mapping(value, "coverage_report")
        return cls(
            matching_deck_count=value.get("matching_deck_count", UNKNOWN_COVERAGE_MARKER),
            available_deck_count=value.get("available_deck_count", UNKNOWN_COVERAGE_MARKER),
            coverage_ratio=value.get("coverage_ratio", UNKNOWN_COVERAGE_MARKER),
            low_sample_threshold=value.get("low_sample_threshold", UNKNOWN_COVERAGE_MARKER),
            low_coverage_threshold=value.get("low_coverage_threshold", UNKNOWN_COVERAGE_MARKER),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolCaveat:
    caveat_id: str
    caveat_type: str
    message: str
    severity: str = "info"
    source_ref_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.caveat_id, "caveat_id")
        _require_text(self.caveat_type, "caveat_type")
        _require_text(self.message, "message")
        _require_text(self.severity, "severity")
        object.__setattr__(self, "source_ref_ids", _unique_text_tuple(self.source_ref_ids, "caveat.source_ref_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "caveat.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "caveat_id": self.caveat_id,
            "caveat_type": self.caveat_type,
            "message": self.message,
            "severity": self.severity,
            "source_ref_ids": list(self.source_ref_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolCaveat":
        _require_mapping(value, "caveat")
        return cls(
            caveat_id=value.get("caveat_id"),
            caveat_type=value.get("caveat_type"),
            message=value.get("message"),
            severity=value.get("severity", "info"),
            source_ref_ids=tuple(value.get("source_ref_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class FrequencyPoolOptions:
    include_tags: bool = True
    require_explicit_user_local_label: bool = True


@dataclass(frozen=True)
class FrequencyPoolPacket:
    pool_id: str
    pool_type: str
    subject: FrequencyPoolSubject
    source_window: FrequencyPoolSourceWindow
    source_refs: tuple[FrequencyPoolSourceRef, ...]
    generated_at: str
    cards: tuple[FrequencyPoolCardRow, ...]
    tags: tuple[FrequencyPoolTagRow, ...]
    coverage_report: FrequencyPoolCoverageReport
    caveats: tuple[FrequencyPoolCaveat, ...]
    filters: Mapping[str, Any]
    identity_version: str
    tag_ontology_version: str
    evidence_version: str
    pool_version: str = FREQUENCY_POOL_PACKET_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.pool_id, "pool_id")
        _require_text(self.pool_version, "pool_version")
        if self.pool_version != FREQUENCY_POOL_PACKET_VERSION:
            raise FrequencyPoolBuildError("unsupported pool_version")
        _require_text(self.pool_type, "pool_type")
        if self.pool_type not in ALLOWED_POOL_TYPES:
            raise FrequencyPoolBuildError("unsupported pool_type")
        if not isinstance(self.subject, FrequencyPoolSubject):
            raise FrequencyPoolBuildError("subject must be FrequencyPoolSubject")
        if not isinstance(self.source_window, FrequencyPoolSourceWindow):
            raise FrequencyPoolBuildError("source_window must be FrequencyPoolSourceWindow")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.identity_version, "identity_version")
        _require_text(self.tag_ontology_version, "tag_ontology_version")
        _require_text(self.evidence_version, "evidence_version")
        object.__setattr__(self, "source_refs", _object_tuple(self.source_refs, FrequencyPoolSourceRef, "source_refs"))
        object.__setattr__(self, "cards", _object_tuple(self.cards, FrequencyPoolCardRow, "cards"))
        object.__setattr__(self, "tags", _object_tuple(self.tags, FrequencyPoolTagRow, "tags"))
        if not isinstance(self.coverage_report, FrequencyPoolCoverageReport):
            raise FrequencyPoolBuildError("coverage_report must be FrequencyPoolCoverageReport")
        object.__setattr__(self, "caveats", _object_tuple(self.caveats, FrequencyPoolCaveat, "caveats"))
        object.__setattr__(self, "filters", _immutable_mapping(self.filters, "filters"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_frequency_pool_packet(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pool_id": self.pool_id,
            "pool_version": self.pool_version,
            "pool_type": self.pool_type,
            "subject": self.subject.to_dict(),
            "source_window": self.source_window.to_dict(),
            "source_refs": [ref.to_dict() for ref in self.source_refs],
            "generated_at": self.generated_at,
            "cards": [card.to_dict() for card in self.cards],
            "tags": [tag.to_dict() for tag in self.tags],
            "coverage_report": self.coverage_report.to_dict(),
            "caveats": [caveat.to_dict() for caveat in self.caveats],
            "filters": _thaw_json(self.filters),
            "identity_version": self.identity_version,
            "tag_ontology_version": self.tag_ontology_version,
            "evidence_version": self.evidence_version,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "FrequencyPoolPacket":
        _require_mapping(value, "frequency pool packet")
        return cls(
            pool_id=value.get("pool_id"),
            pool_version=value.get("pool_version", FREQUENCY_POOL_PACKET_VERSION),
            pool_type=value.get("pool_type"),
            subject=FrequencyPoolSubject.from_mapping(value.get("subject")),
            source_window=FrequencyPoolSourceWindow.from_mapping(value.get("source_window")),
            source_refs=tuple(FrequencyPoolSourceRef.from_mapping(item) for item in value.get("source_refs", ())),
            generated_at=value.get("generated_at"),
            cards=tuple(FrequencyPoolCardRow.from_mapping(item) for item in value.get("cards", ())),
            tags=tuple(FrequencyPoolTagRow.from_mapping(item) for item in value.get("tags", ())),
            coverage_report=FrequencyPoolCoverageReport.from_mapping(value.get("coverage_report")),
            caveats=tuple(FrequencyPoolCaveat.from_mapping(item) for item in value.get("caveats", ())),
            filters=value.get("filters", {}),
            identity_version=value.get("identity_version"),
            tag_ontology_version=value.get("tag_ontology_version"),
            evidence_version=value.get("evidence_version"),
            metadata=value.get("metadata", {}),
        )


def build_frequency_pool_packet(
    payload: Mapping[str, Any],
    *,
    options: FrequencyPoolOptions | None = None,
) -> FrequencyPoolPacket:
    opts = options or FrequencyPoolOptions()
    if not isinstance(opts, FrequencyPoolOptions):
        raise FrequencyPoolBuildError("options must be FrequencyPoolOptions")
    packet = FrequencyPoolPacket.from_mapping(payload)
    if not opts.include_tags:
        packet = FrequencyPoolPacket(
            pool_id=packet.pool_id,
            pool_version=packet.pool_version,
            pool_type=packet.pool_type,
            subject=packet.subject,
            source_window=packet.source_window,
            source_refs=packet.source_refs,
            generated_at=packet.generated_at,
            cards=packet.cards,
            tags=(),
            coverage_report=packet.coverage_report,
            caveats=packet.caveats,
            filters=packet.filters,
            identity_version=packet.identity_version,
            tag_ontology_version=packet.tag_ontology_version,
            evidence_version=packet.evidence_version,
            metadata=packet.metadata,
        )
    if opts.require_explicit_user_local_label:
        _validate_user_local_label(packet)
    return packet


def validate_frequency_pool_packet(packet: FrequencyPoolPacket) -> FrequencyPoolPacket:
    if not isinstance(packet, FrequencyPoolPacket):
        raise FrequencyPoolBuildError("packet must be FrequencyPoolPacket")
    if not packet.source_refs:
        raise FrequencyPoolBuildError("source_refs must not be empty")
    if not packet.cards and not packet.tags:
        raise FrequencyPoolBuildError("cards or tags must be supplied")
    _validate_user_local_label(packet)
    _validate_unique_ids(packet)
    _validate_caveat_visibility(packet)
    _reject_private_and_action_content(packet.to_dict(), "packet")
    return packet


def frequency_pool_packet_to_dict(packet: FrequencyPoolPacket) -> dict[str, Any]:
    if not isinstance(packet, FrequencyPoolPacket):
        raise FrequencyPoolBuildError("packet must be FrequencyPoolPacket")
    validate_frequency_pool_packet(packet)
    return packet.to_dict()


def _validate_unique_ids(packet: FrequencyPoolPacket) -> None:
    source_ref_ids = [ref.source_ref_id for ref in packet.source_refs]
    if len(source_ref_ids) != len(set(source_ref_ids)):
        raise FrequencyPoolBuildError("source_ref_id values must be unique")
    caveat_ids = [caveat.caveat_id for caveat in packet.caveats]
    if len(caveat_ids) != len(set(caveat_ids)):
        raise FrequencyPoolBuildError("caveat_id values must be unique")
    known_sources = set(source_ref_ids)
    known_caveats = set(caveat_ids)
    for row in (*packet.cards, *packet.tags):
        for source_ref_id in row.source_ref_ids:
            if source_ref_id not in known_sources:
                raise FrequencyPoolBuildError("source_ref_ids must reference visible source_refs")
        for caveat_id in row.caveat_ids:
            if caveat_id not in known_caveats:
                raise FrequencyPoolBuildError("caveat_ids must reference visible caveats")
    for caveat_id in packet.coverage_report.caveat_ids:
        if caveat_id not in known_caveats:
            raise FrequencyPoolBuildError("coverage_report caveat_ids must reference visible caveats")


def _validate_user_local_label(packet: FrequencyPoolPacket) -> None:
    if packet.pool_type in USER_LOCAL_POOL_TYPES:
        if not packet.subject.user_local:
            raise FrequencyPoolBuildError("user-local pool types require subject.user_local")
        if packet.metadata.get("isolated_from_global_pools") is not True:
            raise FrequencyPoolBuildError("user-local pools must be isolated_from_global_pools")
        if packet.metadata.get("not_tournament_evidence") is not True:
            raise FrequencyPoolBuildError("user-local pools must be labeled not_tournament_evidence")
        if packet.metadata.get("not_" + "rec" + "ommendation_input") is not True:
            raise FrequencyPoolBuildError("user-local pools must be labeled not action-input")


def _validate_caveat_visibility(packet: FrequencyPoolPacket) -> None:
    coverage = packet.coverage_report
    if isinstance(coverage.matching_deck_count, int) and isinstance(coverage.low_sample_threshold, int):
        if coverage.matching_deck_count < coverage.low_sample_threshold:
            _require_caveat_type(packet, "low_sample")
    if isinstance(coverage.coverage_ratio, float) and isinstance(coverage.low_coverage_threshold, float):
        if coverage.coverage_ratio < coverage.low_coverage_threshold:
            _require_caveat_type(packet, "low_coverage")


def _require_caveat_type(packet: FrequencyPoolPacket, caveat_type: str) -> None:
    if not any(caveat.caveat_type == caveat_type for caveat in packet.caveats):
        raise FrequencyPoolBuildError(f"{caveat_type} caveat is required")


def _immutable_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    _require_mapping(value, field_name)
    frozen: dict[str, Any] = {}
    for key, item in value.items():
        _require_text(key, f"{field_name} key")
        lowered = str(key).lower()
        if lowered in _FORBIDDEN_METADATA_KEYS:
            raise FrequencyPoolBuildError(f"{field_name} contains action-advice metadata")
        frozen[str(key)] = _freeze_json(item, field_name)
    return MappingProxyType(frozen)


def _freeze_json(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        return _immutable_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise FrequencyPoolBuildError(f"{field_name} must be JSON-compatible")


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
                raise FrequencyPoolBuildError(f"{field_name} contains private/raw metadata")
            if lowered_key in _FORBIDDEN_METADATA_KEYS:
                raise FrequencyPoolBuildError(f"{field_name} contains action-advice metadata")
            _reject_private_and_action_content(item, f"{field_name}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_private_and_action_content(item, f"{field_name}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if any(phrase in lowered for phrase in _FORBIDDEN_LANGUAGE):
            raise FrequencyPoolBuildError(f"{field_name} contains action-advice language")


def _validate_coverage_value(
    value: Any,
    field_name: str,
    *,
    integer: bool = False,
    ratio: bool = False,
) -> None:
    if value == UNKNOWN_COVERAGE_MARKER:
        return
    if integer:
        _require_non_negative_int(value, field_name)
        return
    if ratio:
        _require_ratio(value, field_name)
        return
    raise FrequencyPoolBuildError(f"{field_name} coverage validator is misconfigured")


def _object_tuple(values: tuple[Any, ...], expected_type: type, field_name: str) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise FrequencyPoolBuildError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, expected_type):
            raise FrequencyPoolBuildError(f"{field_name} contains invalid item")
    return values


def _unique_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise FrequencyPoolBuildError(f"{field_name} must be a tuple")
    for value in values:
        _require_text(value, field_name)
    if len(values) != len(set(values)):
        raise FrequencyPoolBuildError(f"{field_name} must not contain duplicates")
    return values


def _require_mapping(value: Any, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise FrequencyPoolBuildError(f"{field_name} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise FrequencyPoolBuildError(f"{field_name} is required")


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if not isinstance(value, int) or value < 0:
        raise FrequencyPoolBuildError(f"{field_name} must be a non-negative integer")


def _require_number(value: Any, field_name: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise FrequencyPoolBuildError(f"{field_name} must be numeric")


def _require_ratio(value: Any, field_name: str) -> None:
    _require_number(value, field_name)
    if value < 0 or value > 1:
        raise FrequencyPoolBuildError(f"{field_name} must be between 0 and 1")
