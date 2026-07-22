"""Pure local Tag Graph metric packet models.

This module validates and serializes already supplied sanitized Tag Graph metric
values. It does not calculate metrics from raw sources, render charts, export
files, read providers, read databases, call models, or produce action advice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


TAG_GRAPH_PACKET_VERSION = "tag-graph-packet-v1"
MAX_SELECTED_TAGS = 6

ALLOWED_GRAPH_TYPES = frozenset(
    {
        "tag_count_bar",
        "tag_density_bar",
        "tag_trend_line",
        "deck_vs_commander_average",
        "top_card_contributors",
        "tag_overlap_matrix",
        "tag_correlation_scatter",
        "frequency_pool_tag_breakdown",
    }
)

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


class TagGraphBuildError(ValueError):
    """Raised when a Tag Graph packet violates the Phase 37D boundary."""


@dataclass(frozen=True)
class TagGraphSubject:
    subject_type: str
    subject_key: str
    commander: str | None = None
    partner: str | None = None
    user_local: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.subject_type, "subject_type")
        _require_text(self.subject_key, "subject_key")
        if self.commander is not None:
            _require_text(self.commander, "commander")
        if self.partner is not None:
            _require_text(self.partner, "partner")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "subject.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_type": self.subject_type,
            "subject_key": self.subject_key,
            "commander": self.commander,
            "partner": self.partner,
            "user_local": self.user_local,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphSubject":
        _require_mapping(value, "subject")
        return cls(
            subject_type=value.get("subject_type"),
            subject_key=value.get("subject_key"),
            commander=value.get("commander"),
            partner=value.get("partner"),
            user_local=bool(value.get("user_local", False)),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphComparisonRef:
    comparison_id: str
    comparison_type: str
    label: str
    frequency_pool_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.comparison_id, "comparison_id")
        _require_text(self.comparison_type, "comparison_type")
        _require_text(self.label, "label")
        object.__setattr__(
            self,
            "frequency_pool_ids",
            _unique_text_tuple(self.frequency_pool_ids, "frequency_pool_ids"),
        )
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "comparison.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "comparison_id": self.comparison_id,
            "comparison_type": self.comparison_type,
            "label": self.label,
            "frequency_pool_ids": list(self.frequency_pool_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphComparisonRef":
        _require_mapping(value, "comparison_ref")
        return cls(
            comparison_id=value.get("comparison_id"),
            comparison_type=value.get("comparison_type"),
            label=value.get("label"),
            frequency_pool_ids=tuple(value.get("frequency_pool_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphSelectedTag:
    tag: str
    tag_namespace: str
    tag_source: str
    tag_confidence: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.tag, "tag")
        _require_text(self.tag_namespace, "tag_namespace")
        _require_text(self.tag_source, "tag_source")
        if self.tag_confidence is not None:
            _require_ratio(self.tag_confidence, "tag_confidence")
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "selected_tag.metadata"))

    @property
    def tag_key(self) -> str:
        return f"{self.tag_namespace}:{self.tag}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "tag": self.tag,
            "tag_namespace": self.tag_namespace,
            "tag_source": self.tag_source,
            "tag_confidence": self.tag_confidence,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphSelectedTag":
        _require_mapping(value, "selected_tag")
        return cls(
            tag=value.get("tag"),
            tag_namespace=value.get("tag_namespace"),
            tag_source=value.get("tag_source"),
            tag_confidence=value.get("tag_confidence"),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphMetricRow:
    row_id: str
    tag: str
    scope_label: str
    raw_tag_count: int | str = UNKNOWN_COVERAGE_MARKER
    tag_density: float | str = UNKNOWN_COVERAGE_MARKER
    tag_inclusion_rate: float | str = UNKNOWN_COVERAGE_MARKER
    average_cards_per_deck_with_tag: float | str = UNKNOWN_COVERAGE_MARKER
    placement_weighted_tag_usage: float | str = UNKNOWN_COVERAGE_MARKER
    top_cut_tag_frequency: float | str = UNKNOWN_COVERAGE_MARKER
    winner_tag_frequency: float | str = UNKNOWN_COVERAGE_MARKER
    tag_trend_delta: float | str = UNKNOWN_COVERAGE_MARKER
    tag_confidence: float | str = UNKNOWN_COVERAGE_MARKER
    matching_deck_count: int | str = UNKNOWN_COVERAGE_MARKER
    available_deck_count: int | str = UNKNOWN_COVERAGE_MARKER
    coverage_ratio: float | str = UNKNOWN_COVERAGE_MARKER
    source_packet_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.row_id, "row_id")
        _require_text(self.tag, "tag")
        _require_text(self.scope_label, "scope_label")
        _validate_coverage_value(self.raw_tag_count, "raw_tag_count", integer=True)
        for value, field_name in (
            (self.tag_density, "tag_density"),
            (self.tag_inclusion_rate, "tag_inclusion_rate"),
            (self.placement_weighted_tag_usage, "placement_weighted_tag_usage"),
            (self.top_cut_tag_frequency, "top_cut_tag_frequency"),
            (self.winner_tag_frequency, "winner_tag_frequency"),
            (self.tag_confidence, "tag_confidence"),
            (self.coverage_ratio, "coverage_ratio"),
        ):
            _validate_coverage_value(value, field_name, ratio=True)
        for value, field_name in (
            (self.average_cards_per_deck_with_tag, "average_cards_per_deck_with_tag"),
            (self.tag_trend_delta, "tag_trend_delta"),
        ):
            _validate_coverage_value(value, field_name, number=True)
        _validate_coverage_value(self.matching_deck_count, "matching_deck_count", integer=True)
        _validate_coverage_value(self.available_deck_count, "available_deck_count", integer=True)
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metric_row.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "tag": self.tag,
            "scope_label": self.scope_label,
            "raw_tag_count": self.raw_tag_count,
            "tag_density": self.tag_density,
            "tag_inclusion_rate": self.tag_inclusion_rate,
            "average_cards_per_deck_with_tag": self.average_cards_per_deck_with_tag,
            "placement_weighted_tag_usage": self.placement_weighted_tag_usage,
            "top_cut_tag_frequency": self.top_cut_tag_frequency,
            "winner_tag_frequency": self.winner_tag_frequency,
            "tag_trend_delta": self.tag_trend_delta,
            "tag_confidence": self.tag_confidence,
            "matching_deck_count": self.matching_deck_count,
            "available_deck_count": self.available_deck_count,
            "coverage_ratio": self.coverage_ratio,
            "source_packet_ids": list(self.source_packet_ids),
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphMetricRow":
        _require_mapping(value, "metric_row")
        return cls(
            row_id=value.get("row_id"),
            tag=value.get("tag"),
            scope_label=value.get("scope_label"),
            raw_tag_count=value.get("raw_tag_count", UNKNOWN_COVERAGE_MARKER),
            tag_density=value.get("tag_density", UNKNOWN_COVERAGE_MARKER),
            tag_inclusion_rate=value.get("tag_inclusion_rate", UNKNOWN_COVERAGE_MARKER),
            average_cards_per_deck_with_tag=value.get(
                "average_cards_per_deck_with_tag",
                UNKNOWN_COVERAGE_MARKER,
            ),
            placement_weighted_tag_usage=value.get("placement_weighted_tag_usage", UNKNOWN_COVERAGE_MARKER),
            top_cut_tag_frequency=value.get("top_cut_tag_frequency", UNKNOWN_COVERAGE_MARKER),
            winner_tag_frequency=value.get("winner_tag_frequency", UNKNOWN_COVERAGE_MARKER),
            tag_trend_delta=value.get("tag_trend_delta", UNKNOWN_COVERAGE_MARKER),
            tag_confidence=value.get("tag_confidence", UNKNOWN_COVERAGE_MARKER),
            matching_deck_count=value.get("matching_deck_count", UNKNOWN_COVERAGE_MARKER),
            available_deck_count=value.get("available_deck_count", UNKNOWN_COVERAGE_MARKER),
            coverage_ratio=value.get("coverage_ratio", UNKNOWN_COVERAGE_MARKER),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphContributorRow:
    row_id: str
    tag: str
    oracle_id: str
    card_name: str
    contribution_count: int | str = UNKNOWN_COVERAGE_MARKER
    contribution_density: float | str = UNKNOWN_COVERAGE_MARKER
    source_packet_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.row_id, "row_id")
        _require_text(self.tag, "tag")
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.card_name, "card_name")
        _validate_coverage_value(self.contribution_count, "contribution_count", integer=True)
        _validate_coverage_value(self.contribution_density, "contribution_density", ratio=True)
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "contributor.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "tag": self.tag,
            "oracle_id": self.oracle_id,
            "card_name": self.card_name,
            "contribution_count": self.contribution_count,
            "contribution_density": self.contribution_density,
            "source_packet_ids": list(self.source_packet_ids),
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphContributorRow":
        _require_mapping(value, "contributor_row")
        return cls(
            row_id=value.get("row_id"),
            tag=value.get("tag"),
            oracle_id=value.get("oracle_id"),
            card_name=value.get("card_name"),
            contribution_count=value.get("contribution_count", UNKNOWN_COVERAGE_MARKER),
            contribution_density=value.get("contribution_density", UNKNOWN_COVERAGE_MARKER),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphOverlapRow:
    row_id: str
    tag_a: str
    tag_b: str
    overlap_count: int | str = UNKNOWN_COVERAGE_MARKER
    overlap_ratio: float | str = UNKNOWN_COVERAGE_MARKER
    source_packet_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.row_id, "row_id")
        _require_text(self.tag_a, "tag_a")
        _require_text(self.tag_b, "tag_b")
        _validate_coverage_value(self.overlap_count, "overlap_count", integer=True)
        _validate_coverage_value(self.overlap_ratio, "overlap_ratio", ratio=True)
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "overlap.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "tag_a": self.tag_a,
            "tag_b": self.tag_b,
            "overlap_count": self.overlap_count,
            "overlap_ratio": self.overlap_ratio,
            "source_packet_ids": list(self.source_packet_ids),
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphOverlapRow":
        _require_mapping(value, "overlap_row")
        return cls(
            row_id=value.get("row_id"),
            tag_a=value.get("tag_a"),
            tag_b=value.get("tag_b"),
            overlap_count=value.get("overlap_count", UNKNOWN_COVERAGE_MARKER),
            overlap_ratio=value.get("overlap_ratio", UNKNOWN_COVERAGE_MARKER),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphCorrelationRow:
    row_id: str
    tag_x: str
    tag_y: str
    correlation_value: float | str = UNKNOWN_COVERAGE_MARKER
    sample_size: int | str = UNKNOWN_COVERAGE_MARKER
    source_packet_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.row_id, "row_id")
        _require_text(self.tag_x, "tag_x")
        _require_text(self.tag_y, "tag_y")
        _validate_coverage_value(self.correlation_value, "correlation_value", bounded_number=True)
        _validate_coverage_value(self.sample_size, "sample_size", integer=True)
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "correlation.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "tag_x": self.tag_x,
            "tag_y": self.tag_y,
            "correlation_value": self.correlation_value,
            "sample_size": self.sample_size,
            "source_packet_ids": list(self.source_packet_ids),
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphCorrelationRow":
        _require_mapping(value, "correlation_row")
        return cls(
            row_id=value.get("row_id"),
            tag_x=value.get("tag_x"),
            tag_y=value.get("tag_y"),
            correlation_value=value.get("correlation_value", UNKNOWN_COVERAGE_MARKER),
            sample_size=value.get("sample_size", UNKNOWN_COVERAGE_MARKER),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphTrendRow:
    row_id: str
    tag: str
    window_start: str
    window_end: str
    value: float | str = UNKNOWN_COVERAGE_MARKER
    delta: float | str = UNKNOWN_COVERAGE_MARKER
    source_packet_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.row_id, "row_id")
        _require_text(self.tag, "tag")
        _require_text(self.window_start, "window_start")
        _require_text(self.window_end, "window_end")
        _validate_coverage_value(self.value, "value", ratio=True)
        _validate_coverage_value(self.delta, "delta", number=True)
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "caveat_ids", _unique_text_tuple(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "trend.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "row_id": self.row_id,
            "tag": self.tag,
            "window_start": self.window_start,
            "window_end": self.window_end,
            "value": self.value,
            "delta": self.delta,
            "source_packet_ids": list(self.source_packet_ids),
            "caveat_ids": list(self.caveat_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphTrendRow":
        _require_mapping(value, "trend_row")
        return cls(
            row_id=value.get("row_id"),
            tag=value.get("tag"),
            window_start=value.get("window_start"),
            window_end=value.get("window_end"),
            value=value.get("value", UNKNOWN_COVERAGE_MARKER),
            delta=value.get("delta", UNKNOWN_COVERAGE_MARKER),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            caveat_ids=tuple(value.get("caveat_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphNumericTable:
    table_id: str
    label: str
    columns: tuple[str, ...]
    rows: tuple[Mapping[str, Any], ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.table_id, "table_id")
        _require_text(self.label, "label")
        object.__setattr__(self, "columns", _unique_text_tuple(self.columns, "columns"))
        frozen_rows = tuple(_immutable_mapping(row, "numeric_table.row") for row in self.rows)
        object.__setattr__(self, "rows", frozen_rows)
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "numeric_table.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "table_id": self.table_id,
            "label": self.label,
            "columns": list(self.columns),
            "rows": [_thaw_json(row) for row in self.rows],
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphNumericTable":
        _require_mapping(value, "numeric_table")
        return cls(
            table_id=value.get("table_id"),
            label=value.get("label"),
            columns=tuple(value.get("columns", ())),
            rows=tuple(value.get("rows", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphCardList:
    list_id: str
    tag: str
    oracle_ids: tuple[str, ...]
    source_packet_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.list_id, "list_id")
        _require_text(self.tag, "tag")
        object.__setattr__(self, "oracle_ids", _unique_text_tuple(self.oracle_ids, "oracle_ids"))
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "card_list.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "list_id": self.list_id,
            "tag": self.tag,
            "oracle_ids": list(self.oracle_ids),
            "source_packet_ids": list(self.source_packet_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphCardList":
        _require_mapping(value, "card_list")
        return cls(
            list_id=value.get("list_id"),
            tag=value.get("tag"),
            oracle_ids=tuple(value.get("oracle_ids", ())),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphCaveat:
    caveat_id: str
    caveat_type: str
    message: str
    severity: str = "info"
    source_packet_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.caveat_id, "caveat_id")
        _require_text(self.caveat_type, "caveat_type")
        _require_text(self.message, "message")
        _require_text(self.severity, "severity")
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "caveat.metadata"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "caveat_id": self.caveat_id,
            "caveat_type": self.caveat_type,
            "message": self.message,
            "severity": self.severity,
            "source_packet_ids": list(self.source_packet_ids),
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphCaveat":
        _require_mapping(value, "caveat")
        return cls(
            caveat_id=value.get("caveat_id"),
            caveat_type=value.get("caveat_type"),
            message=value.get("message"),
            severity=value.get("severity", "info"),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            metadata=value.get("metadata", {}),
        )


@dataclass(frozen=True)
class TagGraphOptions:
    include_numeric_tables: bool = True
    include_card_lists: bool = True


@dataclass(frozen=True)
class TagGraphPacket:
    graph_id: str
    graph_type: str
    subject: TagGraphSubject
    selected_tags: tuple[TagGraphSelectedTag, ...]
    generated_at: str
    comparison_refs: tuple[TagGraphComparisonRef, ...]
    source_packet_ids: tuple[str, ...]
    metric_rows: tuple[TagGraphMetricRow, ...]
    contributor_rows: tuple[TagGraphContributorRow, ...]
    overlap_rows: tuple[TagGraphOverlapRow, ...]
    correlation_rows: tuple[TagGraphCorrelationRow, ...]
    trend_rows: tuple[TagGraphTrendRow, ...]
    numeric_tables: tuple[TagGraphNumericTable, ...]
    card_lists: tuple[TagGraphCardList, ...]
    caveats: tuple[TagGraphCaveat, ...]
    filters: Mapping[str, Any]
    frequency_pool_packet_version: str
    tag_ontology_version: str
    evidence_version: str
    graph_version: str = TAG_GRAPH_PACKET_VERSION
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.graph_id, "graph_id")
        _require_text(self.graph_version, "graph_version")
        if self.graph_version != TAG_GRAPH_PACKET_VERSION:
            raise TagGraphBuildError("unsupported graph_version")
        _require_text(self.graph_type, "graph_type")
        if self.graph_type not in ALLOWED_GRAPH_TYPES:
            raise TagGraphBuildError("unsupported graph_type")
        if not isinstance(self.subject, TagGraphSubject):
            raise TagGraphBuildError("subject must be TagGraphSubject")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.frequency_pool_packet_version, "frequency_pool_packet_version")
        _require_text(self.tag_ontology_version, "tag_ontology_version")
        _require_text(self.evidence_version, "evidence_version")
        object.__setattr__(self, "selected_tags", _object_tuple(self.selected_tags, TagGraphSelectedTag, "selected_tags"))
        object.__setattr__(self, "comparison_refs", _object_tuple(self.comparison_refs, TagGraphComparisonRef, "comparison_refs"))
        object.__setattr__(self, "source_packet_ids", _unique_text_tuple(self.source_packet_ids, "source_packet_ids"))
        object.__setattr__(self, "metric_rows", _object_tuple(self.metric_rows, TagGraphMetricRow, "metric_rows"))
        object.__setattr__(self, "contributor_rows", _object_tuple(self.contributor_rows, TagGraphContributorRow, "contributor_rows"))
        object.__setattr__(self, "overlap_rows", _object_tuple(self.overlap_rows, TagGraphOverlapRow, "overlap_rows"))
        object.__setattr__(self, "correlation_rows", _object_tuple(self.correlation_rows, TagGraphCorrelationRow, "correlation_rows"))
        object.__setattr__(self, "trend_rows", _object_tuple(self.trend_rows, TagGraphTrendRow, "trend_rows"))
        object.__setattr__(self, "numeric_tables", _object_tuple(self.numeric_tables, TagGraphNumericTable, "numeric_tables"))
        object.__setattr__(self, "card_lists", _object_tuple(self.card_lists, TagGraphCardList, "card_lists"))
        object.__setattr__(self, "caveats", _object_tuple(self.caveats, TagGraphCaveat, "caveats"))
        object.__setattr__(self, "filters", _immutable_mapping(self.filters, "filters"))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata, "metadata"))
        validate_tag_graph_packet(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "graph_id": self.graph_id,
            "graph_version": self.graph_version,
            "graph_type": self.graph_type,
            "subject": self.subject.to_dict(),
            "selected_tags": [tag.to_dict() for tag in self.selected_tags],
            "generated_at": self.generated_at,
            "comparison_refs": [ref.to_dict() for ref in self.comparison_refs],
            "source_packet_ids": list(self.source_packet_ids),
            "metric_rows": [row.to_dict() for row in self.metric_rows],
            "contributor_rows": [row.to_dict() for row in self.contributor_rows],
            "overlap_rows": [row.to_dict() for row in self.overlap_rows],
            "correlation_rows": [row.to_dict() for row in self.correlation_rows],
            "trend_rows": [row.to_dict() for row in self.trend_rows],
            "numeric_tables": [table.to_dict() for table in self.numeric_tables],
            "card_lists": [card_list.to_dict() for card_list in self.card_lists],
            "caveats": [caveat.to_dict() for caveat in self.caveats],
            "filters": _thaw_json(self.filters),
            "frequency_pool_packet_version": self.frequency_pool_packet_version,
            "tag_ontology_version": self.tag_ontology_version,
            "evidence_version": self.evidence_version,
            "metadata": _thaw_json(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TagGraphPacket":
        _require_mapping(value, "tag graph packet")
        return cls(
            graph_id=value.get("graph_id"),
            graph_version=value.get("graph_version", TAG_GRAPH_PACKET_VERSION),
            graph_type=value.get("graph_type"),
            subject=TagGraphSubject.from_mapping(value.get("subject")),
            selected_tags=tuple(TagGraphSelectedTag.from_mapping(item) for item in value.get("selected_tags", ())),
            generated_at=value.get("generated_at"),
            comparison_refs=tuple(TagGraphComparisonRef.from_mapping(item) for item in value.get("comparison_refs", ())),
            source_packet_ids=tuple(value.get("source_packet_ids", ())),
            metric_rows=tuple(TagGraphMetricRow.from_mapping(item) for item in value.get("metric_rows", ())),
            contributor_rows=tuple(TagGraphContributorRow.from_mapping(item) for item in value.get("contributor_rows", ())),
            overlap_rows=tuple(TagGraphOverlapRow.from_mapping(item) for item in value.get("overlap_rows", ())),
            correlation_rows=tuple(TagGraphCorrelationRow.from_mapping(item) for item in value.get("correlation_rows", ())),
            trend_rows=tuple(TagGraphTrendRow.from_mapping(item) for item in value.get("trend_rows", ())),
            numeric_tables=tuple(TagGraphNumericTable.from_mapping(item) for item in value.get("numeric_tables", ())),
            card_lists=tuple(TagGraphCardList.from_mapping(item) for item in value.get("card_lists", ())),
            caveats=tuple(TagGraphCaveat.from_mapping(item) for item in value.get("caveats", ())),
            filters=value.get("filters", {}),
            frequency_pool_packet_version=value.get("frequency_pool_packet_version"),
            tag_ontology_version=value.get("tag_ontology_version"),
            evidence_version=value.get("evidence_version"),
            metadata=value.get("metadata", {}),
        )


def build_tag_graph_packet(
    payload: Mapping[str, Any],
    *,
    options: TagGraphOptions | None = None,
) -> TagGraphPacket:
    opts = options or TagGraphOptions()
    if not isinstance(opts, TagGraphOptions):
        raise TagGraphBuildError("options must be TagGraphOptions")
    packet = TagGraphPacket.from_mapping(payload)
    if not opts.include_numeric_tables or not opts.include_card_lists:
        packet = TagGraphPacket(
            graph_id=packet.graph_id,
            graph_version=packet.graph_version,
            graph_type=packet.graph_type,
            subject=packet.subject,
            selected_tags=packet.selected_tags,
            generated_at=packet.generated_at,
            comparison_refs=packet.comparison_refs,
            source_packet_ids=packet.source_packet_ids,
            metric_rows=packet.metric_rows,
            contributor_rows=packet.contributor_rows,
            overlap_rows=packet.overlap_rows,
            correlation_rows=packet.correlation_rows,
            trend_rows=packet.trend_rows,
            numeric_tables=packet.numeric_tables if opts.include_numeric_tables else (),
            card_lists=packet.card_lists if opts.include_card_lists else (),
            caveats=packet.caveats,
            filters=packet.filters,
            frequency_pool_packet_version=packet.frequency_pool_packet_version,
            tag_ontology_version=packet.tag_ontology_version,
            evidence_version=packet.evidence_version,
            metadata=packet.metadata,
        )
    return packet


def validate_tag_graph_packet(packet: TagGraphPacket) -> TagGraphPacket:
    if not isinstance(packet, TagGraphPacket):
        raise TagGraphBuildError("packet must be TagGraphPacket")
    if not (1 <= len(packet.selected_tags) <= MAX_SELECTED_TAGS):
        raise TagGraphBuildError("selected_tags must contain one to six tags")
    if len({tag.tag_key for tag in packet.selected_tags}) != len(packet.selected_tags):
        raise TagGraphBuildError("selected_tags must not contain duplicates")
    if not packet.source_packet_ids:
        raise TagGraphBuildError("source_packet_ids must not be empty")
    if not any((packet.metric_rows, packet.contributor_rows, packet.overlap_rows, packet.correlation_rows, packet.trend_rows)):
        raise TagGraphBuildError("at least one graph metric row collection is required")
    _validate_references(packet)
    _reject_private_and_action_content(packet.to_dict(), "packet")
    return packet


def tag_graph_packet_to_dict(packet: TagGraphPacket) -> dict[str, Any]:
    if not isinstance(packet, TagGraphPacket):
        raise TagGraphBuildError("packet must be TagGraphPacket")
    validate_tag_graph_packet(packet)
    return packet.to_dict()


def _validate_references(packet: TagGraphPacket) -> None:
    source_ids = set(packet.source_packet_ids)
    caveat_ids = {caveat.caveat_id for caveat in packet.caveats}
    if len(caveat_ids) != len(packet.caveats):
        raise TagGraphBuildError("caveat_id values must be unique")
    referenced_sources: list[str] = []
    referenced_caveats: list[str] = []
    for row in (
        *packet.metric_rows,
        *packet.contributor_rows,
        *packet.overlap_rows,
        *packet.correlation_rows,
        *packet.trend_rows,
    ):
        referenced_sources.extend(row.source_packet_ids)
        referenced_caveats.extend(row.caveat_ids)
    for table in packet.numeric_tables:
        _reject_private_and_action_content(table.to_dict(), "numeric_table")
    for card_list in packet.card_lists:
        referenced_sources.extend(card_list.source_packet_ids)
    for source_id in referenced_sources:
        if source_id not in source_ids:
            raise TagGraphBuildError("source_packet_ids must reference visible source packets")
    for caveat_id in referenced_caveats:
        if caveat_id not in caveat_ids:
            raise TagGraphBuildError("caveat_ids must reference visible caveats")


def _immutable_mapping(value: Mapping[str, Any], field_name: str) -> Mapping[str, Any]:
    _require_mapping(value, field_name)
    frozen: dict[str, Any] = {}
    for key, item in value.items():
        _require_text(key, f"{field_name} key")
        lowered = str(key).lower()
        if lowered in _FORBIDDEN_METADATA_KEYS:
            raise TagGraphBuildError(f"{field_name} contains action-advice metadata")
        frozen[str(key)] = _freeze_json(item, field_name)
    return MappingProxyType(frozen)


def _freeze_json(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        return _immutable_mapping(value, field_name)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TagGraphBuildError(f"{field_name} must be JSON-compatible")


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
                raise TagGraphBuildError(f"{field_name} contains private/raw metadata")
            if lowered_key in _FORBIDDEN_METADATA_KEYS:
                raise TagGraphBuildError(f"{field_name} contains action-advice metadata")
            _reject_private_and_action_content(item, f"{field_name}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_private_and_action_content(item, f"{field_name}[{index}]")
    elif isinstance(value, str):
        lowered = value.lower()
        if any(phrase in lowered for phrase in _FORBIDDEN_LANGUAGE):
            raise TagGraphBuildError(f"{field_name} contains action-advice language")


def _validate_coverage_value(
    value: Any,
    field_name: str,
    *,
    integer: bool = False,
    ratio: bool = False,
    number: bool = False,
    bounded_number: bool = False,
) -> None:
    if value == UNKNOWN_COVERAGE_MARKER:
        return
    if integer:
        _require_non_negative_int(value, field_name)
        return
    if ratio:
        _require_ratio(value, field_name)
        return
    if bounded_number:
        _require_number(value, field_name)
        if value < -1 or value > 1:
            raise TagGraphBuildError(f"{field_name} must be between -1 and 1")
        return
    if number:
        _require_number(value, field_name)
        return
    raise TagGraphBuildError(f"{field_name} coverage validator is misconfigured")


def _object_tuple(values: tuple[Any, ...], expected_type: type, field_name: str) -> tuple[Any, ...]:
    if not isinstance(values, tuple):
        raise TagGraphBuildError(f"{field_name} must be a tuple")
    for item in values:
        if not isinstance(item, expected_type):
            raise TagGraphBuildError(f"{field_name} contains invalid item")
    return values


def _unique_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TagGraphBuildError(f"{field_name} must be a tuple")
    for value in values:
        _require_text(value, field_name)
    if len(values) != len(set(values)):
        raise TagGraphBuildError(f"{field_name} must not contain duplicates")
    return values


def _require_mapping(value: Any, field_name: str) -> None:
    if not isinstance(value, Mapping):
        raise TagGraphBuildError(f"{field_name} must be a mapping")


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise TagGraphBuildError(f"{field_name} is required")


def _require_non_negative_int(value: Any, field_name: str) -> None:
    if not isinstance(value, int) or value < 0:
        raise TagGraphBuildError(f"{field_name} must be a non-negative integer")


def _require_number(value: Any, field_name: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TagGraphBuildError(f"{field_name} must be numeric")


def _require_ratio(value: Any, field_name: str) -> None:
    _require_number(value, field_name)
    if value < 0 or value > 1:
        raise TagGraphBuildError(f"{field_name} must be between 0 and 1")
