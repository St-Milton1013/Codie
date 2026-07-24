"""Pure Relationship Intelligence metric calculation over pre-counted inputs."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Sequence


RELATIONSHIP_METRIC_VERSION = "relationship-metric.v1"

_DIRECTIONALITIES = frozenset({"directed", "undirected", "bidirectional"})
_CARD_ENDPOINT_TYPES = frozenset({"card"})
_TAG_ENDPOINT_TYPES = frozenset({"functional_tag", "tag"})
_METRIC_ORDER = (
    ("support", "undirected"),
    ("directional_confidence", "A_to_B"),
    ("directional_confidence", "B_to_A"),
    ("dependence_delta", "A_to_B"),
    ("dependence_delta", "B_to_A"),
    ("lift", "undirected"),
    ("leverage", "undirected"),
    ("jaccard_similarity", "undirected"),
    ("pmi", "undirected"),
)


class RelationshipMetricBuildError(ValueError):
    """Raised when a relationship count or metric packet is invalid."""


@dataclass(frozen=True)
class RelationshipCountPacket:
    count_packet_version: str
    population_manifest_id: str
    population_manifest_version: str
    population_spec_hash: str
    source_endpoint_type: str
    source_endpoint_id: str
    target_endpoint_type: str
    target_endpoint_id: str
    directionality: str
    N: int
    nA: int
    nB: int
    nAB: int
    candidate_population_count: int
    usable_population_count: int
    unknown_or_excluded_count: int
    deduplicated_population_count: int
    matching_deck_count: int
    available_deck_count: int
    coverage_ratio: float | None
    low_sample_threshold: int
    low_coverage_threshold: float
    provenance_ref_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "provenance_ref_ids",
            _immutable_ref_ids(self.provenance_ref_ids, "provenance_ref_ids"),
        )
        object.__setattr__(
            self,
            "caveat_ids",
            _immutable_ref_ids(self.caveat_ids, "caveat_ids"),
        )
        validate_relationship_count_packet(self)


@dataclass(frozen=True)
class RelationshipMetricValue:
    metric_name: str
    metric_version: str
    orientation: str
    value: float | None
    numerator: float | int | None
    denominator: float | int | None
    undefined_reason: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.metric_name, "metric_name")
        _require_text(self.metric_version, "metric_version")
        _require_text(self.orientation, "orientation")
        if self.value is None:
            _require_text(self.undefined_reason, "undefined_reason")
        else:
            _require_finite_number(self.value, "value")
            if self.undefined_reason is not None:
                raise RelationshipMetricBuildError(
                    "defined metric values must not have undefined_reason"
                )
        for field_name, field_value in (
            ("numerator", self.numerator),
            ("denominator", self.denominator),
        ):
            if field_value is not None:
                _require_finite_number(field_value, field_name)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "metric_version": self.metric_version,
            "orientation": self.orientation,
            "value": self.value,
            "numerator": self.numerator,
            "denominator": self.denominator,
            "undefined_reason": self.undefined_reason,
        }


@dataclass(frozen=True)
class RelationshipMetricBundle:
    measurement_version: str
    metric_bundle_version: str
    population_manifest_id: str
    population_manifest_version: str
    population_spec_hash: str
    source_endpoint_type: str
    source_endpoint_id: str
    target_endpoint_type: str
    target_endpoint_id: str
    directionality: str
    N: int
    nA: int
    nB: int
    nAB: int
    observed_co_occurrence: int
    expected_co_occurrence: float
    metrics: tuple[RelationshipMetricValue, ...]
    undefined_reasons: tuple[str, ...]
    coverage_ratio: float | None
    sample_label: str
    availability_label: str
    low_sample_threshold: int
    low_coverage_threshold: float
    provenance_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    calculated_at: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "metrics", tuple(self.metrics))
        object.__setattr__(self, "undefined_reasons", tuple(self.undefined_reasons))
        object.__setattr__(
            self,
            "provenance_ref_ids",
            _immutable_ref_ids(self.provenance_ref_ids, "provenance_ref_ids"),
        )
        object.__setattr__(
            self,
            "caveat_ids",
            _immutable_ref_ids(self.caveat_ids, "caveat_ids"),
        )
        validate_relationship_metric_bundle(self)

    def to_dict(self) -> dict[str, Any]:
        return relationship_metric_bundle_to_dict(self)


def validate_relationship_count_packet(packet: RelationshipCountPacket) -> None:
    if not isinstance(packet, RelationshipCountPacket):
        raise RelationshipMetricBuildError(
            "count packet must be a RelationshipCountPacket"
        )
    for field_name in (
        "count_packet_version",
        "population_manifest_id",
        "population_manifest_version",
        "population_spec_hash",
        "source_endpoint_type",
        "source_endpoint_id",
        "target_endpoint_type",
        "target_endpoint_id",
        "directionality",
    ):
        _require_text(getattr(packet, field_name), field_name)
    if packet.directionality not in _DIRECTIONALITIES:
        raise RelationshipMetricBuildError("unsupported directionality")
    for field_name in (
        "N",
        "nA",
        "nB",
        "nAB",
        "candidate_population_count",
        "usable_population_count",
        "unknown_or_excluded_count",
        "deduplicated_population_count",
        "matching_deck_count",
        "available_deck_count",
        "low_sample_threshold",
    ):
        _require_nonnegative_integer(getattr(packet, field_name), field_name)
    if packet.N <= 0:
        raise RelationshipMetricBuildError("N must be greater than zero")
    if packet.nA > packet.N or packet.nB > packet.N:
        raise RelationshipMetricBuildError("nA and nB must not exceed N")
    if packet.nAB > packet.nA or packet.nAB > packet.nB:
        raise RelationshipMetricBuildError("nAB must not exceed nA or nB")
    if packet.matching_deck_count > packet.available_deck_count:
        raise RelationshipMetricBuildError(
            "matching_deck_count must not exceed available_deck_count"
        )
    _require_ratio(packet.low_coverage_threshold, "low_coverage_threshold")
    if packet.available_deck_count == 0:
        if packet.matching_deck_count != 0 or packet.coverage_ratio is not None:
            raise RelationshipMetricBuildError(
                "zero available_deck_count requires zero matches and unavailable coverage"
            )
    else:
        _require_ratio(packet.coverage_ratio, "coverage_ratio")
        expected_coverage = (
            packet.matching_deck_count / packet.available_deck_count
        )
        if not math.isclose(
            float(packet.coverage_ratio),
            expected_coverage,
            rel_tol=1e-12,
            abs_tol=1e-12,
        ):
            raise RelationshipMetricBuildError(
                "coverage_ratio does not match deck coverage counts"
            )
    _reject_uncontracted_card_to_tag(packet)


def build_relationship_metric_bundle(
    count_packet: RelationshipCountPacket,
    *,
    measurement_version: str,
    metric_bundle_version: str,
    calculated_at: str,
) -> RelationshipMetricBundle:
    validate_relationship_count_packet(count_packet)
    _require_text(measurement_version, "measurement_version")
    _require_text(metric_bundle_version, "metric_bundle_version")
    _require_text(calculated_at, "calculated_at")

    N = count_packet.N
    nA = count_packet.nA
    nB = count_packet.nB
    nAB = count_packet.nAB
    p_a = nA / N
    p_b = nB / N
    p_ab = nAB / N
    expected_probability = p_a * p_b
    expected_co_occurrence = (nA * nB) / N

    metrics = (
        _defined_metric("support", "undirected", p_ab, nAB, N),
        _directional_ratio_metric(
            "directional_confidence",
            "A_to_B",
            nAB,
            nA,
            "ENDPOINT_A_NOT_OBSERVED",
        ),
        _directional_ratio_metric(
            "directional_confidence",
            "B_to_A",
            nAB,
            nB,
            "ENDPOINT_B_NOT_OBSERVED",
        ),
        _dependence_delta_metric(
            "A_to_B",
            nAB,
            nA,
            p_b,
            "ENDPOINT_A_NOT_OBSERVED",
        ),
        _dependence_delta_metric(
            "B_to_A",
            nAB,
            nB,
            p_a,
            "ENDPOINT_B_NOT_OBSERVED",
        ),
        _lift_metric(p_ab, expected_probability, nA, nB),
        _defined_metric(
            "leverage",
            "undirected",
            p_ab - expected_probability,
            p_ab - expected_probability,
            1,
        ),
        _jaccard_metric(nAB, nA + nB - nAB),
        _pmi_metric(p_ab, expected_probability, nAB),
    )
    undefined_reasons = tuple(
        dict.fromkeys(
            metric.undefined_reason
            for metric in metrics
            if metric.undefined_reason is not None
        )
    )
    sample_label = (
        "low_sample"
        if count_packet.usable_population_count < count_packet.low_sample_threshold
        else "available"
    )
    availability_label = _availability_label(count_packet)

    bundle = RelationshipMetricBundle(
        measurement_version=measurement_version,
        metric_bundle_version=metric_bundle_version,
        population_manifest_id=count_packet.population_manifest_id,
        population_manifest_version=count_packet.population_manifest_version,
        population_spec_hash=count_packet.population_spec_hash,
        source_endpoint_type=count_packet.source_endpoint_type,
        source_endpoint_id=count_packet.source_endpoint_id,
        target_endpoint_type=count_packet.target_endpoint_type,
        target_endpoint_id=count_packet.target_endpoint_id,
        directionality=count_packet.directionality,
        N=N,
        nA=nA,
        nB=nB,
        nAB=nAB,
        observed_co_occurrence=nAB,
        expected_co_occurrence=expected_co_occurrence,
        metrics=metrics,
        undefined_reasons=undefined_reasons,
        coverage_ratio=count_packet.coverage_ratio,
        sample_label=sample_label,
        availability_label=availability_label,
        low_sample_threshold=count_packet.low_sample_threshold,
        low_coverage_threshold=count_packet.low_coverage_threshold,
        provenance_ref_ids=count_packet.provenance_ref_ids,
        caveat_ids=count_packet.caveat_ids,
        calculated_at=calculated_at,
    )
    validate_relationship_metric_bundle(bundle)
    return bundle


def relationship_metric_bundle_to_dict(
    bundle: RelationshipMetricBundle,
) -> dict[str, Any]:
    validate_relationship_metric_bundle(bundle)
    return {
        "measurement_version": bundle.measurement_version,
        "metric_bundle_version": bundle.metric_bundle_version,
        "population_manifest_id": bundle.population_manifest_id,
        "population_manifest_version": bundle.population_manifest_version,
        "population_spec_hash": bundle.population_spec_hash,
        "source_endpoint_type": bundle.source_endpoint_type,
        "source_endpoint_id": bundle.source_endpoint_id,
        "target_endpoint_type": bundle.target_endpoint_type,
        "target_endpoint_id": bundle.target_endpoint_id,
        "directionality": bundle.directionality,
        "N": bundle.N,
        "nA": bundle.nA,
        "nB": bundle.nB,
        "nAB": bundle.nAB,
        "observed_co_occurrence": bundle.observed_co_occurrence,
        "expected_co_occurrence": bundle.expected_co_occurrence,
        "metrics": [metric.to_dict() for metric in bundle.metrics],
        "undefined_reasons": list(bundle.undefined_reasons),
        "coverage_ratio": bundle.coverage_ratio,
        "sample_label": bundle.sample_label,
        "availability_label": bundle.availability_label,
        "low_sample_threshold": bundle.low_sample_threshold,
        "low_coverage_threshold": bundle.low_coverage_threshold,
        "provenance_ref_ids": list(bundle.provenance_ref_ids),
        "caveat_ids": list(bundle.caveat_ids),
        "calculated_at": bundle.calculated_at,
    }


def validate_relationship_metric_bundle(bundle: RelationshipMetricBundle) -> None:
    if not isinstance(bundle, RelationshipMetricBundle):
        raise RelationshipMetricBuildError(
            "metric bundle must be a RelationshipMetricBundle"
        )
    for field_name in (
        "measurement_version",
        "metric_bundle_version",
        "population_manifest_id",
        "population_manifest_version",
        "population_spec_hash",
        "source_endpoint_type",
        "source_endpoint_id",
        "target_endpoint_type",
        "target_endpoint_id",
        "directionality",
        "sample_label",
        "availability_label",
        "calculated_at",
    ):
        _require_text(getattr(bundle, field_name), field_name)
    if bundle.directionality not in _DIRECTIONALITIES:
        raise RelationshipMetricBuildError("unsupported directionality")
    for field_name in ("N", "nA", "nB", "nAB", "observed_co_occurrence"):
        _require_nonnegative_integer(getattr(bundle, field_name), field_name)
    _require_nonnegative_integer(
        bundle.low_sample_threshold,
        "low_sample_threshold",
    )
    if bundle.N <= 0:
        raise RelationshipMetricBuildError("N must be greater than zero")
    if bundle.nA > bundle.N or bundle.nB > bundle.N:
        raise RelationshipMetricBuildError("nA and nB must not exceed N")
    if bundle.nAB > bundle.nA or bundle.nAB > bundle.nB:
        raise RelationshipMetricBuildError("nAB must not exceed nA or nB")
    _require_finite_number(bundle.expected_co_occurrence, "expected_co_occurrence")
    expected_co_occurrence = (bundle.nA * bundle.nB) / bundle.N
    if not math.isclose(
        bundle.expected_co_occurrence,
        expected_co_occurrence,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise RelationshipMetricBuildError(
            "expected_co_occurrence must match N, nA, and nB"
        )
    _require_ratio(bundle.low_coverage_threshold, "low_coverage_threshold")
    if bundle.coverage_ratio is not None:
        _require_ratio(bundle.coverage_ratio, "coverage_ratio")
    if bundle.sample_label not in {"available", "low_sample"}:
        raise RelationshipMetricBuildError("unsupported sample_label")
    if bundle.availability_label not in {
        "available",
        "low_coverage",
        "insufficient_coverage",
        "unavailable",
    }:
        raise RelationshipMetricBuildError("unsupported availability_label")
    if bundle.availability_label == "unavailable":
        if bundle.coverage_ratio is not None:
            raise RelationshipMetricBuildError(
                "unavailable coverage must not have a numeric ratio"
            )
    elif bundle.coverage_ratio is None:
        raise RelationshipMetricBuildError(
            "available coverage states require a numeric ratio"
        )
    if bundle.observed_co_occurrence != bundle.nAB:
        raise RelationshipMetricBuildError(
            "observed_co_occurrence must equal nAB"
        )
    identities = tuple(
        (metric.metric_name, metric.orientation) for metric in bundle.metrics
    )
    if identities != _METRIC_ORDER:
        raise RelationshipMetricBuildError(
            "metrics must use the declared stable metric ordering"
        )
    expected_reasons = tuple(
        dict.fromkeys(
            metric.undefined_reason
            for metric in bundle.metrics
            if metric.undefined_reason is not None
        )
    )
    if bundle.undefined_reasons != expected_reasons:
        raise RelationshipMetricBuildError(
            "undefined_reasons must match visible metric reasons"
        )
    _reject_uncontracted_endpoint_pair(
        bundle.source_endpoint_type,
        bundle.target_endpoint_type,
    )


def _directional_ratio_metric(
    name: str,
    orientation: str,
    numerator: int,
    denominator: int,
    reason: str,
) -> RelationshipMetricValue:
    if denominator == 0:
        return _undefined_metric(name, orientation, reason, numerator, denominator)
    return _defined_metric(
        name,
        orientation,
        numerator / denominator,
        numerator,
        denominator,
    )


def _dependence_delta_metric(
    orientation: str,
    joint_count: int,
    endpoint_count: int,
    other_marginal: float,
    reason: str,
) -> RelationshipMetricValue:
    if endpoint_count == 0:
        return _undefined_metric(
            "dependence_delta",
            orientation,
            reason,
            joint_count,
            endpoint_count,
        )
    value = (joint_count / endpoint_count) - other_marginal
    return _defined_metric(
        "dependence_delta",
        orientation,
        value,
        value,
        1,
    )


def _lift_metric(
    observed_probability: float,
    expected_probability: float,
    nA: int,
    nB: int,
) -> RelationshipMetricValue:
    if expected_probability == 0:
        reason = (
            "ENDPOINT_A_NOT_OBSERVED" if nA == 0 else "ENDPOINT_B_NOT_OBSERVED"
        )
        return _undefined_metric(
            "lift",
            "undirected",
            reason,
            observed_probability,
            expected_probability,
        )
    return _defined_metric(
        "lift",
        "undirected",
        observed_probability / expected_probability,
        observed_probability,
        expected_probability,
    )


def _jaccard_metric(joint_count: int, union_count: int) -> RelationshipMetricValue:
    if union_count == 0:
        return _undefined_metric(
            "jaccard_similarity",
            "undirected",
            "ZERO_UNION_JACCARD_UNDEFINED",
            joint_count,
            union_count,
        )
    return _defined_metric(
        "jaccard_similarity",
        "undirected",
        joint_count / union_count,
        joint_count,
        union_count,
    )


def _pmi_metric(
    observed_probability: float,
    expected_probability: float,
    joint_count: int,
) -> RelationshipMetricValue:
    if joint_count == 0:
        return _undefined_metric(
            "pmi",
            "undirected",
            "ZERO_JOINT_PMI_UNDEFINED",
            observed_probability,
            expected_probability,
        )
    lift = observed_probability / expected_probability
    return _defined_metric("pmi", "undirected", math.log2(lift), lift, None)


def _defined_metric(
    name: str,
    orientation: str,
    value: float,
    numerator: float | int | None,
    denominator: float | int | None,
) -> RelationshipMetricValue:
    return RelationshipMetricValue(
        metric_name=name,
        metric_version=RELATIONSHIP_METRIC_VERSION,
        orientation=orientation,
        value=value,
        numerator=numerator,
        denominator=denominator,
    )


def _undefined_metric(
    name: str,
    orientation: str,
    reason: str,
    numerator: float | int | None,
    denominator: float | int | None,
) -> RelationshipMetricValue:
    return RelationshipMetricValue(
        metric_name=name,
        metric_version=RELATIONSHIP_METRIC_VERSION,
        orientation=orientation,
        value=None,
        numerator=numerator,
        denominator=denominator,
        undefined_reason=reason,
    )


def _availability_label(packet: RelationshipCountPacket) -> str:
    if packet.available_deck_count == 0:
        return "unavailable"
    if packet.matching_deck_count == 0:
        return "insufficient_coverage"
    if (
        packet.coverage_ratio is not None
        and packet.coverage_ratio < packet.low_coverage_threshold
    ):
        return "low_coverage"
    return "available"


def _reject_uncontracted_card_to_tag(packet: RelationshipCountPacket) -> None:
    _reject_uncontracted_endpoint_pair(
        packet.source_endpoint_type,
        packet.target_endpoint_type,
    )


def _reject_uncontracted_endpoint_pair(
    source_endpoint_type: str,
    target_endpoint_type: str,
) -> None:
    endpoint_types = {
        source_endpoint_type.strip().lower(),
        target_endpoint_type.strip().lower(),
    }
    if endpoint_types & _CARD_ENDPOINT_TYPES and endpoint_types & _TAG_ENDPOINT_TYPES:
        raise RelationshipMetricBuildError(
            "measured card-to-tag relationships require an accepted anti-tautology rule"
        )


def _immutable_ref_ids(
    values: Sequence[str],
    field_name: str,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise RelationshipMetricBuildError(f"{field_name} must be a sequence")
    frozen = tuple(values)
    for value in frozen:
        _require_text(value, field_name)
    if len(set(frozen)) != len(frozen):
        raise RelationshipMetricBuildError(f"{field_name} must be unique")
    return frozen


def _require_text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RelationshipMetricBuildError(f"{field_name} must be non-empty text")


def _require_nonnegative_integer(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RelationshipMetricBuildError(
            f"{field_name} must be a non-negative integer"
        )


def _require_finite_number(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RelationshipMetricBuildError(f"{field_name} must be numeric")
    if not math.isfinite(float(value)):
        raise RelationshipMetricBuildError(f"{field_name} must be finite")


def _require_ratio(value: Any, field_name: str) -> None:
    _require_finite_number(value, field_name)
    if not 0 <= float(value) <= 1:
        raise RelationshipMetricBuildError(f"{field_name} must be within [0, 1]")
