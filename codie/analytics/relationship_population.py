"""Pure population resolution for Relationship Intelligence count packets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
import json
import math
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from .relationship_metrics import (
    RelationshipCountPacket,
    RelationshipMetricBuildError,
    validate_relationship_count_packet,
)


RELATIONSHIP_POPULATION_VERSION = "relationship-population.v1"

_ENDPOINT_TYPES = frozenset(
    {"card", "tag", "package", "commander", "commander_pair"}
)
_OBSERVATION_STATUSES = frozenset(
    {
        "active",
        "approved_observation",
        "resolved",
        "ignored_by_policy",
        "unapproved_observation",
    }
)
_PRIVACY_CLASSES = frozenset({"public", "private"})
_DEDUPLICATION_POLICY = "canonical_snapshot"
_INACTIVE_STATUS_POLICY = "exclude_inactive"
_PRIVATE_METADATA_KEYS = frozenset(
    {
        "api_key",
        "credential",
        "credentials",
        "deck_text",
        "import_text",
        "password",
        "pilot_notes",
        "primer_body",
        "private_notes",
        "raw_payload",
        "secret",
        "token",
        "user_notes",
    }
)
_EXCLUSION_REASONS = frozenset(
    {
        "DUPLICATE_CANONICAL_SNAPSHOT",
        "INACTIVE_RESOLVED",
        "INACTIVE_IGNORED_BY_POLICY",
        "PRIVATE_USER_RECORD",
        "UNAPPROVED_OBSERVATION",
        "MISSING_CANONICAL_DECK_ID",
        "MISSING_CANONICAL_SNAPSHOT_ID",
        "UNRESOLVED_CARD_IDENTITY",
        "UNSUPPORTED_ENDPOINT",
        "UNKNOWN_OR_EXCLUDED",
    }
)


class RelationshipPopulationBuildError(ValueError):
    """Raised when a relationship population packet is invalid."""


@dataclass(frozen=True)
class RelationshipEndpoint:
    endpoint_type: str
    endpoint_id: str
    canonical_identity_ids: tuple[str, ...] = ()
    tag_assignment_ids: tuple[str, ...] = ()
    package_member_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = MappingProxyType({})

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "canonical_identity_ids",
            tuple(
                sorted(
                    _immutable_text_tuple(
                        self.canonical_identity_ids,
                        "canonical_identity_ids",
                    ),
                    key=str.casefold,
                )
            ),
        )
        object.__setattr__(
            self,
            "tag_assignment_ids",
            tuple(
                sorted(
                    _immutable_text_tuple(
                        self.tag_assignment_ids,
                        "tag_assignment_ids",
                    ),
                    key=str.casefold,
                )
            ),
        )
        object.__setattr__(
            self,
            "package_member_ids",
            tuple(
                sorted(
                    _immutable_text_tuple(
                        self.package_member_ids,
                        "package_member_ids",
                    ),
                    key=str.casefold,
                )
            ),
        )
        object.__setattr__(
            self,
            "metadata",
            _freeze_metadata(self.metadata, "metadata"),
        )
        _validate_endpoint(self)


@dataclass(frozen=True)
class RelationshipDeckPresenceRecord:
    deck_id: str
    snapshot_id: str
    observation_status: str
    privacy_class: str
    commander_key: str | None = None
    partner_key: str | None = None
    mainboard_oracle_ids: tuple[str, ...] = ()
    sideboard_oracle_ids: tuple[str, ...] = ()
    auxiliary_oracle_ids: tuple[str, ...] = ()
    tag_assignment_ids: tuple[str, ...] = ()
    package_ids: tuple[str, ...] = ()
    source_snapshot_ids: tuple[str, ...] = ()
    provenance_ref_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = MappingProxyType({})

    def __post_init__(self) -> None:
        for field_name in (
            "mainboard_oracle_ids",
            "sideboard_oracle_ids",
            "auxiliary_oracle_ids",
            "tag_assignment_ids",
            "package_ids",
            "source_snapshot_ids",
            "provenance_ref_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                tuple(
                    sorted(
                        _immutable_text_tuple(
                            getattr(self, field_name),
                            field_name,
                        ),
                        key=str.casefold,
                    )
                ),
            )
        object.__setattr__(
            self,
            "metadata",
            _freeze_metadata(self.metadata, "metadata"),
        )
        _validate_presence_record(self)


@dataclass(frozen=True)
class RelationshipPopulationSpec:
    population_spec_version: str
    population_scope_type: str
    population_scope_key: str
    source_snapshot_ids: tuple[str, ...]
    analytics_version: str
    deduplication_policy: str
    inactive_status_policy: str
    low_sample_threshold: int
    low_coverage_threshold: float
    calculated_at: str
    commander_key: str | None = None
    partner_key: str | None = None
    time_window_start: str | None = None
    time_window_end: str | None = None
    region: str | None = None
    placement_scope: str | None = None
    include_sideboard: bool = False
    include_auxiliary: bool = False
    provenance_ref_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_snapshot_ids",
            tuple(
                sorted(
                    _immutable_text_tuple(
                        self.source_snapshot_ids,
                        "source_snapshot_ids",
                    ),
                    key=str.casefold,
                )
            ),
        )
        object.__setattr__(
            self,
            "provenance_ref_ids",
            tuple(
                sorted(
                    _immutable_text_tuple(
                        self.provenance_ref_ids,
                        "provenance_ref_ids",
                    ),
                    key=str.casefold,
                )
            ),
        )
        object.__setattr__(
            self,
            "caveat_ids",
            tuple(
                sorted(
                    _immutable_text_tuple(
                        self.caveat_ids,
                        "caveat_ids",
                    ),
                    key=str.casefold,
                )
            ),
        )
        validate_relationship_population_spec(self)


@dataclass(frozen=True)
class RelationshipPopulationExclusion:
    candidate_id: str
    deck_id: str
    snapshot_id: str
    reason_code: str
    detail: str
    source_snapshot_id: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "candidate_id",
            "deck_id",
            "snapshot_id",
            "reason_code",
            "detail",
        ):
            _require_text(getattr(self, field_name), field_name)
        if self.reason_code not in _EXCLUSION_REASONS:
            raise RelationshipPopulationBuildError(
                f"unsupported exclusion reason: {self.reason_code}"
            )
        _require_optional_text(self.source_snapshot_id, "source_snapshot_id")


@dataclass(frozen=True)
class RelationshipPopulationManifest:
    population_manifest_id: str
    population_manifest_version: str
    population_spec_hash: str
    population_scope_type: str
    population_scope_key: str
    source_snapshot_ids: tuple[str, ...]
    analytics_version: str
    deduplication_policy: str
    inactive_status_policy: str
    candidate_population_count: int
    usable_population_count: int
    unknown_or_excluded_count: int
    deduplicated_population_count: int
    member_deck_ids: tuple[str, ...]
    excluded_deck_records: tuple[RelationshipPopulationExclusion, ...]
    provenance_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    calculated_at: str
    commander_key: str | None = None
    partner_key: str | None = None
    time_window_start: str | None = None
    time_window_end: str | None = None
    region: str | None = None
    placement_scope: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "source_snapshot_ids",
            "member_deck_ids",
            "provenance_ref_ids",
            "caveat_ids",
        ):
            object.__setattr__(
                self,
                field_name,
                (
                    _immutable_text_tuple(
                        getattr(self, field_name),
                        field_name,
                        require_unique=False,
                    )
                    if field_name == "member_deck_ids"
                    else tuple(
                        sorted(
                            _immutable_text_tuple(
                                getattr(self, field_name),
                                field_name,
                            ),
                            key=str.casefold,
                        )
                    )
                ),
            )
        object.__setattr__(
            self,
            "excluded_deck_records",
            _immutable_typed_tuple(
                self.excluded_deck_records,
                RelationshipPopulationExclusion,
                "excluded_deck_records",
            ),
        )
        validate_relationship_population_manifest(self)


@dataclass(frozen=True)
class RelationshipPopulationResolution:
    resolution_version: str
    manifest: RelationshipPopulationManifest
    source_endpoint: RelationshipEndpoint
    target_endpoint: RelationshipEndpoint
    count_packet: RelationshipCountPacket
    presence_record_ids: tuple[str, ...]
    exclusions: tuple[RelationshipPopulationExclusion, ...]
    labels: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "presence_record_ids",
            _immutable_text_tuple(
                self.presence_record_ids,
                "presence_record_ids",
            ),
        )
        object.__setattr__(
            self,
            "exclusions",
            _immutable_typed_tuple(
                self.exclusions,
                RelationshipPopulationExclusion,
                "exclusions",
            ),
        )
        object.__setattr__(
            self,
            "labels",
            _immutable_text_tuple(self.labels, "labels"),
        )
        validate_relationship_population_resolution(self)


def build_relationship_population_resolution(
    population_spec: RelationshipPopulationSpec,
    deck_presence_records: Sequence[RelationshipDeckPresenceRecord],
    source_endpoint: RelationshipEndpoint,
    target_endpoint: RelationshipEndpoint,
    *,
    population_manifest_version: str = RELATIONSHIP_POPULATION_VERSION,
    count_packet_version: str = "relationship-count.v1",
    resolution_version: str = RELATIONSHIP_POPULATION_VERSION,
    directionality: str = "undirected",
) -> RelationshipPopulationResolution:
    """Resolve canonical deck observations into an existing count packet."""

    validate_relationship_population_spec(population_spec)
    _validate_endpoint(source_endpoint)
    _validate_endpoint(target_endpoint)
    _validate_endpoint_pair(source_endpoint, target_endpoint)
    _require_text(population_manifest_version, "population_manifest_version")
    _require_text(count_packet_version, "count_packet_version")
    _require_text(resolution_version, "resolution_version")
    records = _immutable_typed_tuple(
        deck_presence_records,
        RelationshipDeckPresenceRecord,
        "deck_presence_records",
    )

    candidate_population_count = len(records)
    exclusions: list[RelationshipPopulationExclusion] = []
    eligible: list[RelationshipDeckPresenceRecord] = []
    for record in records:
        exclusion = _policy_exclusion(record)
        if exclusion is None:
            eligible.append(record)
        else:
            exclusions.append(exclusion)

    survivors: list[RelationshipDeckPresenceRecord] = []
    deduplicated_population_count = 0
    grouped: dict[str, list[RelationshipDeckPresenceRecord]] = {}
    for record in eligible:
        grouped.setdefault(record.snapshot_id, []).append(record)
    for snapshot_id in sorted(grouped):
        group = sorted(grouped[snapshot_id], key=_presence_record_sort_key)
        survivors.append(group[0])
        for duplicate in group[1:]:
            exclusions.append(
                _build_exclusion(
                    duplicate,
                    "DUPLICATE_CANONICAL_SNAPSHOT",
                    "duplicate canonical snapshot removed by stable tie-breaker",
                )
            )
            deduplicated_population_count += 1

    survivors.sort(key=_presence_record_sort_key)
    exclusions.sort(key=_exclusion_sort_key)
    unknown_or_excluded_count = (
        len(exclusions) - deduplicated_population_count
    )
    usable_population_count = len(survivors)
    if usable_population_count == 0:
        raise RelationshipPopulationBuildError(
            "population must contain at least one usable deck"
        )
    if candidate_population_count != (
        usable_population_count
        + unknown_or_excluded_count
        + deduplicated_population_count
    ):
        raise RelationshipPopulationBuildError(
            "candidate population count invariant failed"
        )

    source_matches = tuple(
        _endpoint_present(record, source_endpoint, population_spec)
        for record in survivors
    )
    target_matches = tuple(
        _endpoint_present(record, target_endpoint, population_spec)
        for record in survivors
    )
    n_a = sum(source_matches)
    n_b = sum(target_matches)
    n_ab = sum(
        source_present and target_present
        for source_present, target_present in zip(
            source_matches,
            target_matches,
            strict=True,
        )
    )

    spec_payload = _population_spec_to_dict(population_spec)
    population_spec_hash = _semantic_hash(spec_payload)
    member_payloads = [
        _presence_record_to_dict(record) for record in survivors
    ]
    manifest_identity_payload = {
        "population_spec_hash": population_spec_hash,
        "source_endpoint": _endpoint_to_dict(source_endpoint),
        "target_endpoint": _endpoint_to_dict(target_endpoint),
        "members": member_payloads,
        "exclusions": [
            _exclusion_to_dict(exclusion) for exclusion in exclusions
        ],
    }
    population_manifest_id = (
        "relationship-population:"
        + _semantic_hash(manifest_identity_payload)
    )
    manifest = RelationshipPopulationManifest(
        population_manifest_id=population_manifest_id,
        population_manifest_version=population_manifest_version,
        population_spec_hash=population_spec_hash,
        population_scope_type=population_spec.population_scope_type,
        population_scope_key=population_spec.population_scope_key,
        commander_key=population_spec.commander_key,
        partner_key=population_spec.partner_key,
        time_window_start=population_spec.time_window_start,
        time_window_end=population_spec.time_window_end,
        region=population_spec.region,
        placement_scope=population_spec.placement_scope,
        source_snapshot_ids=population_spec.source_snapshot_ids,
        analytics_version=population_spec.analytics_version,
        deduplication_policy=population_spec.deduplication_policy,
        inactive_status_policy=population_spec.inactive_status_policy,
        candidate_population_count=candidate_population_count,
        usable_population_count=usable_population_count,
        unknown_or_excluded_count=unknown_or_excluded_count,
        deduplicated_population_count=deduplicated_population_count,
        member_deck_ids=tuple(record.deck_id for record in survivors),
        excluded_deck_records=tuple(exclusions),
        provenance_ref_ids=population_spec.provenance_ref_ids,
        caveat_ids=population_spec.caveat_ids,
        calculated_at=population_spec.calculated_at,
    )

    available_deck_count = usable_population_count
    matching_deck_count = sum(
        bool(record.source_snapshot_ids and record.provenance_ref_ids)
        for record in survivors
    )
    coverage_ratio = (
        matching_deck_count / available_deck_count
        if available_deck_count
        else None
    )
    try:
        count_packet = RelationshipCountPacket(
            count_packet_version=count_packet_version,
            population_manifest_id=manifest.population_manifest_id,
            population_manifest_version=manifest.population_manifest_version,
            population_spec_hash=manifest.population_spec_hash,
            source_endpoint_type=source_endpoint.endpoint_type,
            source_endpoint_id=source_endpoint.endpoint_id,
            target_endpoint_type=target_endpoint.endpoint_type,
            target_endpoint_id=target_endpoint.endpoint_id,
            directionality=directionality,
            N=usable_population_count,
            nA=n_a,
            nB=n_b,
            nAB=n_ab,
            candidate_population_count=candidate_population_count,
            usable_population_count=usable_population_count,
            unknown_or_excluded_count=unknown_or_excluded_count,
            deduplicated_population_count=deduplicated_population_count,
            matching_deck_count=matching_deck_count,
            available_deck_count=available_deck_count,
            coverage_ratio=coverage_ratio,
            low_sample_threshold=population_spec.low_sample_threshold,
            low_coverage_threshold=population_spec.low_coverage_threshold,
            provenance_ref_ids=population_spec.provenance_ref_ids,
            caveat_ids=population_spec.caveat_ids,
        )
    except RelationshipMetricBuildError as exc:
        raise RelationshipPopulationBuildError(str(exc)) from exc

    labels: list[str] = []
    if usable_population_count < population_spec.low_sample_threshold:
        labels.append("low_sample")
    if coverage_ratio is None:
        labels.append("unavailable_coverage")
    elif coverage_ratio < population_spec.low_coverage_threshold:
        labels.append("low_coverage")

    resolution = RelationshipPopulationResolution(
        resolution_version=resolution_version,
        manifest=manifest,
        source_endpoint=source_endpoint,
        target_endpoint=target_endpoint,
        count_packet=count_packet,
        presence_record_ids=tuple(
            _candidate_id(record) for record in survivors
        ),
        exclusions=tuple(exclusions),
        labels=tuple(labels),
    )
    validate_relationship_population_resolution(resolution)
    return resolution


def relationship_population_manifest_to_dict(
    manifest: RelationshipPopulationManifest,
) -> dict[str, Any]:
    validate_relationship_population_manifest(manifest)
    return {
        "population_manifest_id": manifest.population_manifest_id,
        "population_manifest_version": manifest.population_manifest_version,
        "population_spec_hash": manifest.population_spec_hash,
        "population_scope_type": manifest.population_scope_type,
        "population_scope_key": manifest.population_scope_key,
        "commander_key": manifest.commander_key,
        "partner_key": manifest.partner_key,
        "time_window_start": manifest.time_window_start,
        "time_window_end": manifest.time_window_end,
        "region": manifest.region,
        "placement_scope": manifest.placement_scope,
        "source_snapshot_ids": list(manifest.source_snapshot_ids),
        "analytics_version": manifest.analytics_version,
        "deduplication_policy": manifest.deduplication_policy,
        "inactive_status_policy": manifest.inactive_status_policy,
        "candidate_population_count": manifest.candidate_population_count,
        "usable_population_count": manifest.usable_population_count,
        "unknown_or_excluded_count": manifest.unknown_or_excluded_count,
        "deduplicated_population_count": manifest.deduplicated_population_count,
        "member_deck_ids": list(manifest.member_deck_ids),
        "excluded_deck_records": [
            _exclusion_to_dict(exclusion)
            for exclusion in manifest.excluded_deck_records
        ],
        "provenance_ref_ids": list(manifest.provenance_ref_ids),
        "caveat_ids": list(manifest.caveat_ids),
        "calculated_at": manifest.calculated_at,
    }


def relationship_population_resolution_to_dict(
    resolution: RelationshipPopulationResolution,
) -> dict[str, Any]:
    validate_relationship_population_resolution(resolution)
    return {
        "resolution_version": resolution.resolution_version,
        "manifest": relationship_population_manifest_to_dict(
            resolution.manifest
        ),
        "source_endpoint": _endpoint_to_dict(resolution.source_endpoint),
        "target_endpoint": _endpoint_to_dict(resolution.target_endpoint),
        "count_packet": _count_packet_to_dict(resolution.count_packet),
        "presence_record_ids": list(resolution.presence_record_ids),
        "exclusions": [
            _exclusion_to_dict(exclusion)
            for exclusion in resolution.exclusions
        ],
        "labels": list(resolution.labels),
    }


def validate_relationship_population_spec(
    spec: RelationshipPopulationSpec,
) -> None:
    if not isinstance(spec, RelationshipPopulationSpec):
        raise RelationshipPopulationBuildError(
            "population spec must be a RelationshipPopulationSpec"
        )
    for field_name in (
        "population_spec_version",
        "population_scope_type",
        "population_scope_key",
        "analytics_version",
        "deduplication_policy",
        "inactive_status_policy",
        "calculated_at",
    ):
        _require_text(getattr(spec, field_name), field_name)
    if spec.deduplication_policy != _DEDUPLICATION_POLICY:
        raise RelationshipPopulationBuildError(
            "unsupported deduplication_policy"
        )
    if spec.inactive_status_policy != _INACTIVE_STATUS_POLICY:
        raise RelationshipPopulationBuildError(
            "unsupported inactive_status_policy"
        )
    _require_positive_integer(
        spec.low_sample_threshold,
        "low_sample_threshold",
    )
    _require_ratio(
        spec.low_coverage_threshold,
        "low_coverage_threshold",
    )
    if not isinstance(spec.include_sideboard, bool):
        raise RelationshipPopulationBuildError(
            "include_sideboard must be boolean"
        )
    if not isinstance(spec.include_auxiliary, bool):
        raise RelationshipPopulationBuildError(
            "include_auxiliary must be boolean"
        )
    for field_name in (
        "commander_key",
        "partner_key",
        "time_window_start",
        "time_window_end",
        "region",
        "placement_scope",
    ):
        _require_optional_text(getattr(spec, field_name), field_name)
    if spec.partner_key is not None and spec.commander_key is None:
        raise RelationshipPopulationBuildError(
            "partner_key requires commander_key"
        )
    _require_iso_datetime(spec.calculated_at, "calculated_at")
    if spec.time_window_start is not None:
        _require_iso_datetime(spec.time_window_start, "time_window_start")
    if spec.time_window_end is not None:
        _require_iso_datetime(spec.time_window_end, "time_window_end")
    if spec.time_window_start and spec.time_window_end:
        if _parse_datetime(spec.time_window_start) > _parse_datetime(
            spec.time_window_end
        ):
            raise RelationshipPopulationBuildError(
                "time_window_start must not follow time_window_end"
            )


def validate_relationship_population_manifest(
    manifest: RelationshipPopulationManifest,
) -> None:
    if not isinstance(manifest, RelationshipPopulationManifest):
        raise RelationshipPopulationBuildError(
            "manifest must be a RelationshipPopulationManifest"
        )
    for field_name in (
        "population_manifest_id",
        "population_manifest_version",
        "population_spec_hash",
        "population_scope_type",
        "population_scope_key",
        "analytics_version",
        "deduplication_policy",
        "inactive_status_policy",
        "calculated_at",
    ):
        _require_text(getattr(manifest, field_name), field_name)
    if manifest.deduplication_policy != _DEDUPLICATION_POLICY:
        raise RelationshipPopulationBuildError(
            "unsupported manifest deduplication_policy"
        )
    if manifest.inactive_status_policy != _INACTIVE_STATUS_POLICY:
        raise RelationshipPopulationBuildError(
            "unsupported manifest inactive_status_policy"
        )
    for field_name in (
        "candidate_population_count",
        "usable_population_count",
        "unknown_or_excluded_count",
        "deduplicated_population_count",
    ):
        _require_nonnegative_integer(
            getattr(manifest, field_name),
            field_name,
        )
    if manifest.candidate_population_count != (
        manifest.usable_population_count
        + manifest.unknown_or_excluded_count
        + manifest.deduplicated_population_count
    ):
        raise RelationshipPopulationBuildError(
            "manifest population count invariant failed"
        )
    if len(manifest.member_deck_ids) != manifest.usable_population_count:
        raise RelationshipPopulationBuildError(
            "member_deck_ids must match usable_population_count"
        )
    if len(manifest.excluded_deck_records) != (
        manifest.unknown_or_excluded_count
        + manifest.deduplicated_population_count
    ):
        raise RelationshipPopulationBuildError(
            "excluded records must match excluded population counts"
        )
    duplicate_count = sum(
        exclusion.reason_code == "DUPLICATE_CANONICAL_SNAPSHOT"
        for exclusion in manifest.excluded_deck_records
    )
    if duplicate_count != manifest.deduplicated_population_count:
        raise RelationshipPopulationBuildError(
            "visible duplicate exclusions must match deduplicated count"
        )
    _require_iso_datetime(manifest.calculated_at, "calculated_at")


def validate_relationship_population_resolution(
    resolution: RelationshipPopulationResolution,
) -> None:
    if not isinstance(resolution, RelationshipPopulationResolution):
        raise RelationshipPopulationBuildError(
            "resolution must be a RelationshipPopulationResolution"
        )
    _require_text(resolution.resolution_version, "resolution_version")
    validate_relationship_population_manifest(resolution.manifest)
    _validate_endpoint(resolution.source_endpoint)
    _validate_endpoint(resolution.target_endpoint)
    _validate_endpoint_pair(
        resolution.source_endpoint,
        resolution.target_endpoint,
    )
    try:
        validate_relationship_count_packet(resolution.count_packet)
    except RelationshipMetricBuildError as exc:
        raise RelationshipPopulationBuildError(str(exc)) from exc
    packet = resolution.count_packet
    manifest = resolution.manifest
    if (
        packet.population_manifest_id != manifest.population_manifest_id
        or packet.population_manifest_version
        != manifest.population_manifest_version
        or packet.population_spec_hash != manifest.population_spec_hash
    ):
        raise RelationshipPopulationBuildError(
            "count packet manifest references do not match manifest"
        )
    if (
        packet.candidate_population_count
        != manifest.candidate_population_count
        or packet.usable_population_count
        != manifest.usable_population_count
        or packet.unknown_or_excluded_count
        != manifest.unknown_or_excluded_count
        or packet.deduplicated_population_count
        != manifest.deduplicated_population_count
        or packet.N != manifest.usable_population_count
    ):
        raise RelationshipPopulationBuildError(
            "count packet population totals do not match manifest"
        )
    if (
        packet.source_endpoint_type != resolution.source_endpoint.endpoint_type
        or packet.source_endpoint_id != resolution.source_endpoint.endpoint_id
        or packet.target_endpoint_type != resolution.target_endpoint.endpoint_type
        or packet.target_endpoint_id != resolution.target_endpoint.endpoint_id
    ):
        raise RelationshipPopulationBuildError(
            "count packet endpoint references do not match resolution"
        )
    if len(resolution.presence_record_ids) != manifest.usable_population_count:
        raise RelationshipPopulationBuildError(
            "presence_record_ids must match usable population"
        )
    if resolution.exclusions != manifest.excluded_deck_records:
        raise RelationshipPopulationBuildError(
            "resolution exclusions must match manifest exclusions"
        )
    expected_labels: list[str] = []
    if packet.N < packet.low_sample_threshold:
        expected_labels.append("low_sample")
    if packet.coverage_ratio is None:
        expected_labels.append("unavailable_coverage")
    elif packet.coverage_ratio < packet.low_coverage_threshold:
        expected_labels.append("low_coverage")
    if resolution.labels != tuple(expected_labels):
        raise RelationshipPopulationBuildError(
            "labels must match visible sample and coverage state"
        )


def _validate_endpoint(endpoint: RelationshipEndpoint) -> None:
    if not isinstance(endpoint, RelationshipEndpoint):
        raise RelationshipPopulationBuildError(
            "endpoint must be a RelationshipEndpoint"
        )
    _require_text(endpoint.endpoint_type, "endpoint_type")
    _require_text(endpoint.endpoint_id, "endpoint_id")
    if endpoint.endpoint_type not in _ENDPOINT_TYPES:
        raise RelationshipPopulationBuildError("unsupported endpoint_type")
    if endpoint.endpoint_type == "card":
        if not endpoint.canonical_identity_ids:
            raise RelationshipPopulationBuildError(
                "card endpoint requires canonical_identity_ids"
            )
    elif endpoint.endpoint_type == "tag":
        if not endpoint.tag_assignment_ids:
            raise RelationshipPopulationBuildError(
                "tag endpoint requires tag_assignment_ids"
            )
    elif endpoint.endpoint_type == "package":
        if not endpoint.package_member_ids:
            raise RelationshipPopulationBuildError(
                "package endpoint requires package_member_ids"
            )
    elif endpoint.endpoint_type == "commander_pair":
        if len(endpoint.canonical_identity_ids) != 2:
            raise RelationshipPopulationBuildError(
                "commander_pair requires two canonical_identity_ids"
            )
        normalized_pair_id = "+".join(endpoint.canonical_identity_ids)
        if endpoint.endpoint_id != normalized_pair_id:
            raise RelationshipPopulationBuildError(
                "commander_pair endpoint_id must use normalized pair order"
            )


def _validate_presence_record(
    record: RelationshipDeckPresenceRecord,
) -> None:
    _require_text(record.deck_id, "deck_id")
    _require_text(record.snapshot_id, "snapshot_id")
    _require_text(record.observation_status, "observation_status")
    _require_text(record.privacy_class, "privacy_class")
    if record.observation_status not in _OBSERVATION_STATUSES:
        raise RelationshipPopulationBuildError(
            "unsupported observation_status"
        )
    if record.privacy_class not in _PRIVACY_CLASSES:
        raise RelationshipPopulationBuildError("unsupported privacy_class")
    _require_optional_text(record.commander_key, "commander_key")
    _require_optional_text(record.partner_key, "partner_key")
    if record.partner_key is not None and record.commander_key is None:
        raise RelationshipPopulationBuildError(
            "partner_key requires commander_key"
        )
    for field_name in (
        "mainboard_oracle_ids",
        "sideboard_oracle_ids",
        "auxiliary_oracle_ids",
    ):
        for oracle_id in getattr(record, field_name):
            if oracle_id.casefold().startswith("unresolved:"):
                raise RelationshipPopulationBuildError(
                    "unresolved card identities are not allowed"
                )


def _validate_endpoint_pair(
    source_endpoint: RelationshipEndpoint,
    target_endpoint: RelationshipEndpoint,
) -> None:
    if (
        source_endpoint.endpoint_type == target_endpoint.endpoint_type
        and source_endpoint.endpoint_id == target_endpoint.endpoint_id
    ):
        raise RelationshipPopulationBuildError(
            "source and target endpoints must be distinct"
        )
    endpoint_types = {
        source_endpoint.endpoint_type,
        target_endpoint.endpoint_type,
    }
    if endpoint_types == {"card", "tag"}:
        raise RelationshipPopulationBuildError(
            "direct card-to-tag relationships require an accepted anti-tautology rule"
        )


def _policy_exclusion(
    record: RelationshipDeckPresenceRecord,
) -> RelationshipPopulationExclusion | None:
    if record.observation_status == "resolved":
        return _build_exclusion(
            record,
            "INACTIVE_RESOLVED",
            "resolved observation excluded by inactive-status policy",
        )
    if record.observation_status == "ignored_by_policy":
        return _build_exclusion(
            record,
            "INACTIVE_IGNORED_BY_POLICY",
            "ignored observation excluded by inactive-status policy",
        )
    if record.observation_status == "unapproved_observation":
        return _build_exclusion(
            record,
            "UNAPPROVED_OBSERVATION",
            "unapproved observation excluded from global evidence",
        )
    if (
        record.privacy_class == "private"
        and record.observation_status != "approved_observation"
    ):
        return _build_exclusion(
            record,
            "PRIVATE_USER_RECORD",
            "private user record excluded from global evidence",
        )
    return None


def _endpoint_present(
    record: RelationshipDeckPresenceRecord,
    endpoint: RelationshipEndpoint,
    spec: RelationshipPopulationSpec,
) -> bool:
    if endpoint.endpoint_type == "card":
        oracle_ids = set(record.mainboard_oracle_ids)
        if spec.include_sideboard:
            oracle_ids.update(record.sideboard_oracle_ids)
        if spec.include_auxiliary:
            oracle_ids.update(record.auxiliary_oracle_ids)
        return bool(oracle_ids.intersection(endpoint.canonical_identity_ids))
    if endpoint.endpoint_type == "tag":
        return bool(
            set(record.tag_assignment_ids).intersection(
                endpoint.tag_assignment_ids
            )
        )
    if endpoint.endpoint_type == "package":
        return bool(
            set(record.package_ids).intersection(
                endpoint.package_member_ids
            )
        )
    if endpoint.endpoint_type == "commander":
        return endpoint.endpoint_id in {
            value for value in (record.commander_key, record.partner_key) if value
        }
    expected_pair = tuple(
        sorted(endpoint.canonical_identity_ids, key=str.casefold)
    )
    if record.commander_key is None or record.partner_key is None:
        return False
    record_pair = tuple(
        sorted(
            (record.commander_key, record.partner_key),
            key=str.casefold,
        )
    )
    return record_pair == expected_pair


def _build_exclusion(
    record: RelationshipDeckPresenceRecord,
    reason_code: str,
    detail: str,
) -> RelationshipPopulationExclusion:
    return RelationshipPopulationExclusion(
        candidate_id=_candidate_id(record),
        deck_id=record.deck_id,
        snapshot_id=record.snapshot_id,
        reason_code=reason_code,
        detail=detail,
        source_snapshot_id=(
            record.source_snapshot_ids[0]
            if record.source_snapshot_ids
            else None
        ),
    )


def _candidate_id(record: RelationshipDeckPresenceRecord) -> str:
    return f"{record.deck_id}@{record.snapshot_id}"


def _presence_record_sort_key(
    record: RelationshipDeckPresenceRecord,
) -> tuple[str, str, str]:
    payload_hash = _semantic_hash(_presence_record_to_dict(record))
    return (record.snapshot_id.casefold(), record.deck_id.casefold(), payload_hash)


def _exclusion_sort_key(
    exclusion: RelationshipPopulationExclusion,
) -> tuple[str, str, str]:
    return (
        exclusion.candidate_id.casefold(),
        exclusion.reason_code,
        exclusion.detail,
    )


def _population_spec_to_dict(
    spec: RelationshipPopulationSpec,
) -> dict[str, Any]:
    return {
        "population_spec_version": spec.population_spec_version,
        "population_scope_type": spec.population_scope_type,
        "population_scope_key": spec.population_scope_key,
        "commander_key": spec.commander_key,
        "partner_key": spec.partner_key,
        "time_window_start": spec.time_window_start,
        "time_window_end": spec.time_window_end,
        "region": spec.region,
        "placement_scope": spec.placement_scope,
        "source_snapshot_ids": sorted(
            spec.source_snapshot_ids,
            key=str.casefold,
        ),
        "analytics_version": spec.analytics_version,
        "deduplication_policy": spec.deduplication_policy,
        "inactive_status_policy": spec.inactive_status_policy,
        "include_sideboard": spec.include_sideboard,
        "include_auxiliary": spec.include_auxiliary,
        "low_sample_threshold": spec.low_sample_threshold,
        "low_coverage_threshold": spec.low_coverage_threshold,
        "calculated_at": spec.calculated_at,
        "provenance_ref_ids": sorted(
            spec.provenance_ref_ids,
            key=str.casefold,
        ),
        "caveat_ids": sorted(spec.caveat_ids, key=str.casefold),
    }


def _presence_record_to_dict(
    record: RelationshipDeckPresenceRecord,
) -> dict[str, Any]:
    return {
        "deck_id": record.deck_id,
        "snapshot_id": record.snapshot_id,
        "observation_status": record.observation_status,
        "privacy_class": record.privacy_class,
        "commander_key": record.commander_key,
        "partner_key": record.partner_key,
        "mainboard_oracle_ids": sorted(
            record.mainboard_oracle_ids,
            key=str.casefold,
        ),
        "sideboard_oracle_ids": sorted(
            record.sideboard_oracle_ids,
            key=str.casefold,
        ),
        "auxiliary_oracle_ids": sorted(
            record.auxiliary_oracle_ids,
            key=str.casefold,
        ),
        "tag_assignment_ids": sorted(
            record.tag_assignment_ids,
            key=str.casefold,
        ),
        "package_ids": sorted(record.package_ids, key=str.casefold),
        "source_snapshot_ids": sorted(
            record.source_snapshot_ids,
            key=str.casefold,
        ),
        "provenance_ref_ids": sorted(
            record.provenance_ref_ids,
            key=str.casefold,
        ),
        "metadata": _thaw_json(record.metadata),
    }


def _endpoint_to_dict(endpoint: RelationshipEndpoint) -> dict[str, Any]:
    return {
        "endpoint_type": endpoint.endpoint_type,
        "endpoint_id": endpoint.endpoint_id,
        "canonical_identity_ids": list(endpoint.canonical_identity_ids),
        "tag_assignment_ids": list(endpoint.tag_assignment_ids),
        "package_member_ids": list(endpoint.package_member_ids),
        "metadata": _thaw_json(endpoint.metadata),
    }


def _exclusion_to_dict(
    exclusion: RelationshipPopulationExclusion,
) -> dict[str, Any]:
    return {
        "candidate_id": exclusion.candidate_id,
        "deck_id": exclusion.deck_id,
        "snapshot_id": exclusion.snapshot_id,
        "reason_code": exclusion.reason_code,
        "detail": exclusion.detail,
        "source_snapshot_id": exclusion.source_snapshot_id,
    }


def _count_packet_to_dict(packet: RelationshipCountPacket) -> dict[str, Any]:
    return {
        "count_packet_version": packet.count_packet_version,
        "population_manifest_id": packet.population_manifest_id,
        "population_manifest_version": packet.population_manifest_version,
        "population_spec_hash": packet.population_spec_hash,
        "source_endpoint_type": packet.source_endpoint_type,
        "source_endpoint_id": packet.source_endpoint_id,
        "target_endpoint_type": packet.target_endpoint_type,
        "target_endpoint_id": packet.target_endpoint_id,
        "directionality": packet.directionality,
        "N": packet.N,
        "nA": packet.nA,
        "nB": packet.nB,
        "nAB": packet.nAB,
        "candidate_population_count": packet.candidate_population_count,
        "usable_population_count": packet.usable_population_count,
        "unknown_or_excluded_count": packet.unknown_or_excluded_count,
        "deduplicated_population_count": packet.deduplicated_population_count,
        "matching_deck_count": packet.matching_deck_count,
        "available_deck_count": packet.available_deck_count,
        "coverage_ratio": packet.coverage_ratio,
        "low_sample_threshold": packet.low_sample_threshold,
        "low_coverage_threshold": packet.low_coverage_threshold,
        "provenance_ref_ids": list(packet.provenance_ref_ids),
        "caveat_ids": list(packet.caveat_ids),
    }


def _semantic_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _freeze_metadata(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RelationshipPopulationBuildError(
            f"{field_name} must be a mapping"
        )
    _reject_private_metadata(value, field_name)
    return _freeze_json(value, field_name)


def _freeze_json(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        frozen: dict[str, Any] = {}
        for key in sorted(value, key=lambda item: str(item)):
            if not isinstance(key, str) or not key.strip():
                raise RelationshipPopulationBuildError(
                    f"{field_name} keys must be non-empty text"
                )
            frozen[key] = _freeze_json(value[key], field_name)
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    raise RelationshipPopulationBuildError(
        f"{field_name} must contain JSON-compatible values"
    )


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(value[key]) for key in sorted(value)}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _reject_private_metadata(value: Any, field_name: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).strip().casefold()
            if normalized in _PRIVATE_METADATA_KEYS:
                raise RelationshipPopulationBuildError(
                    f"{field_name} contains prohibited private metadata"
                )
            _reject_private_metadata(item, field_name)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _reject_private_metadata(item, field_name)


def _immutable_text_tuple(
    values: Sequence[str],
    field_name: str,
    *,
    require_unique: bool = True,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise RelationshipPopulationBuildError(
            f"{field_name} must be a sequence"
        )
    frozen = tuple(values)
    for value in frozen:
        _require_text(value, field_name)
    if require_unique and len(set(frozen)) != len(frozen):
        raise RelationshipPopulationBuildError(
            f"{field_name} must be unique"
        )
    return frozen


def _immutable_typed_tuple(
    values: Sequence[Any],
    expected_type: type,
    field_name: str,
) -> tuple[Any, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise RelationshipPopulationBuildError(
            f"{field_name} must be a sequence"
        )
    frozen = tuple(values)
    if not all(isinstance(value, expected_type) for value in frozen):
        raise RelationshipPopulationBuildError(
            f"{field_name} contains an invalid item"
        )
    return frozen


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RelationshipPopulationBuildError(
            f"{field_name} must be non-empty text"
        )


def _require_optional_text(value: Any, field_name: str) -> None:
    if value is not None:
        _require_text(value, field_name)


def _require_nonnegative_integer(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RelationshipPopulationBuildError(
            f"{field_name} must be a non-negative integer"
        )


def _require_positive_integer(value: Any, field_name: str) -> None:
    _require_nonnegative_integer(value, field_name)
    if value == 0:
        raise RelationshipPopulationBuildError(
            f"{field_name} must be greater than zero"
        )


def _require_ratio(value: Any, field_name: str) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(float(value))
        or not 0 <= float(value) <= 1
    ):
        raise RelationshipPopulationBuildError(
            f"{field_name} must be within [0, 1]"
        )


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _require_iso_datetime(value: Any, field_name: str) -> None:
    _require_text(value, field_name)
    try:
        parsed = _parse_datetime(value)
    except ValueError as exc:
        raise RelationshipPopulationBuildError(
            f"{field_name} must be an ISO-8601 datetime"
        ) from exc
    if parsed.tzinfo is None:
        raise RelationshipPopulationBuildError(
            f"{field_name} must include a timezone"
        )
