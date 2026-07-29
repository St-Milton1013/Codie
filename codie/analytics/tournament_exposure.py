"""Pure independent-seat Tournament Exposure evidence packets."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from hashlib import sha256
import json
from typing import Any, Sequence


TOURNAMENT_EXPOSURE_VERSION = "tournament-exposure.independent-seat.v1"
INDEPENDENT_SEAT_MODEL_ID = "independent_seat"

_TARGET_TYPES = frozenset(
    {"commander", "partner_pair", "archetype", "card", "package", "functional_tag"}
)
_SCOPE_TYPES = frozenset(
    {"global", "region", "country", "store", "organizer", "tournament_size"}
)
_COMPARISON_TYPES = frozenset(
    {"local_versus_global", "regional_versus_global"}
)
_CONFIDENCE_LABELS = frozenset(
    {
        "SUFFICIENT",
        "LIMITED_SAMPLE",
        "LIMITED_COVERAGE",
        "LIMITED_SAMPLE_AND_COVERAGE",
    }
)
_OBSERVATION_UNIT = "canonical_tournament_deck_instance"
_DECIMAL_PLACES = 12


class TournamentExposureBuildError(ValueError):
    """Raised when a Tournament Exposure packet is invalid."""


@dataclass(frozen=True)
class TournamentExposureTarget:
    target_type: str
    target_id: str
    target_version: str
    display_label: str
    component_ids: tuple[str, ...] = ()
    provenance_ref_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        components = _refs(self.component_ids, "component_ids")
        if self.target_type == "partner_pair":
            if len(components) != 2:
                raise TournamentExposureBuildError(
                    "partner_pair requires exactly two component_ids"
                )
            components = tuple(sorted(components, key=str.casefold))
        elif components:
            raise TournamentExposureBuildError(
                "component_ids are only supported for partner_pair targets"
            )
        object.__setattr__(self, "component_ids", components)
        object.__setattr__(
            self,
            "provenance_ref_ids",
            _refs(self.provenance_ref_ids, "provenance_ref_ids"),
        )
        for name in ("target_id", "target_version", "display_label"):
            _text(getattr(self, name), name)
        if self.target_type not in _TARGET_TYPES:
            raise TournamentExposureBuildError("unsupported target_type")


@dataclass(frozen=True)
class TournamentExposurePopulationManifest:
    population_manifest_id: str
    population_version: str
    population_spec_hash: str
    observation_unit: str
    scope_type: str
    scope_key: str
    date_start: str
    date_end: str
    source_snapshot_ids: tuple[str, ...]
    source_record_count: int
    available_population_count: int
    matching_population_count: int
    excluded_record_count: int
    deduplicated_record_count: int
    target: TournamentExposureTarget
    deduplication_policy: str
    deduplication_version: str
    coverage_numerator: int
    coverage_denominator: int
    coverage_ratio: str
    low_sample_threshold: int
    low_coverage_threshold: str
    generated_at: str
    provenance_ref_ids: tuple[str, ...] = ()
    caveat_ids: tuple[str, ...] = ()
    region: str | None = None
    country: str | None = None
    store: str | None = None
    organizer: str | None = None
    tournament_size_class: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "source_snapshot_ids", _refs(self.source_snapshot_ids, "source_snapshot_ids")
        )
        object.__setattr__(
            self, "provenance_ref_ids", _refs(self.provenance_ref_ids, "provenance_ref_ids")
        )
        object.__setattr__(self, "caveat_ids", _refs(self.caveat_ids, "caveat_ids"))
        object.__setattr__(
            self,
            "coverage_ratio",
            _format_fraction(_fraction_from_decimal(self.coverage_ratio)),
        )
        object.__setattr__(
            self,
            "low_coverage_threshold",
            _format_fraction(_fraction_from_decimal(self.low_coverage_threshold)),
        )
        object.__setattr__(self, "generated_at", _timestamp(self.generated_at, "generated_at"))
        validate_tournament_exposure_population_manifest(self)


@dataclass(frozen=True)
class TournamentExposureAssumptions:
    model_id: str
    model_version: str
    formula_version: str
    numeric_policy_version: str
    expected_attendance: int
    event_size_class: str
    opponent_seats_per_round: int
    round_count: int
    approximation_label: str
    approximation_warning: str

    def __post_init__(self) -> None:
        for name in (
            "model_version",
            "formula_version",
            "numeric_policy_version",
            "event_size_class",
            "approximation_label",
            "approximation_warning",
        ):
            _text(getattr(self, name), name)
        if self.model_id != INDEPENDENT_SEAT_MODEL_ID:
            raise TournamentExposureBuildError("unsupported pairing model")
        for name in ("expected_attendance", "opponent_seats_per_round", "round_count"):
            _positive_int(getattr(self, name), name)
        warning = self.approximation_warning.casefold()
        if "independent-seat" not in warning or "not a swiss-pairing model" not in warning:
            raise TournamentExposureBuildError(
                "approximation_warning requires independent-seat and non-Swiss disclosure"
            )


@dataclass(frozen=True)
class TournamentExposureEstimate:
    exposure_id: str
    exposure_version: str
    target: TournamentExposureTarget
    population_manifest: TournamentExposurePopulationManifest
    assumptions: TournamentExposureAssumptions
    metagame_share_numerator: int
    metagame_share_denominator: int
    metagame_share: str
    seat_opportunities_per_event: int
    per_round_encounter_probability: str
    event_wide_encounter_probability: str
    expected_encounter_count: str
    sample_size: int
    coverage_ratio: str
    confidence_label: str
    provenance_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    calculated_at: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "provenance_ref_ids", _refs(self.provenance_ref_ids, "provenance_ref_ids")
        )
        object.__setattr__(self, "caveat_ids", _refs(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "calculated_at", _timestamp(self.calculated_at, "calculated_at"))
        validate_tournament_exposure_estimate(self)


@dataclass(frozen=True)
class TournamentExposureComparison:
    comparison_id: str
    comparison_version: str
    comparison_type: str
    selected_exposure_id: str
    global_exposure_id: str
    target_id: str
    selected_scope_type: str
    selected_event_wide_probability: str
    global_event_wide_probability: str
    event_wide_probability_delta: str
    selected_sample_size: int
    global_sample_size: int
    selected_coverage_ratio: str
    global_coverage_ratio: str
    provenance_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    calculated_at: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "provenance_ref_ids", _refs(self.provenance_ref_ids, "provenance_ref_ids")
        )
        object.__setattr__(self, "caveat_ids", _refs(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "calculated_at", _timestamp(self.calculated_at, "calculated_at"))
        if self.comparison_type not in _COMPARISON_TYPES:
            raise TournamentExposureBuildError("unsupported comparison_type")
        for name in (
            "comparison_id",
            "comparison_version",
            "selected_exposure_id",
            "global_exposure_id",
            "target_id",
            "selected_scope_type",
        ):
            _text(getattr(self, name), name)
        _validate_comparison(self)


@dataclass(frozen=True)
class TournamentExposurePreparationBrief:
    brief_id: str
    brief_version: str
    exposure_id: str
    comparison_ids: tuple[str, ...]
    target_label: str
    scope_label: str
    per_round_estimate: str
    event_wide_estimate: str
    comparison_deltas: tuple[str, ...]
    sample_size: int
    coverage_ratio: str
    confidence_label: str
    assumptions: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    approximation_warning: str
    generated_at: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "comparison_ids", _refs(self.comparison_ids, "comparison_ids"))
        object.__setattr__(self, "caveat_ids", _refs(self.caveat_ids, "caveat_ids"))
        object.__setattr__(
            self, "comparison_deltas", _texts(self.comparison_deltas, "comparison_deltas")
        )
        object.__setattr__(self, "assumptions", _texts(self.assumptions, "assumptions"))
        object.__setattr__(self, "generated_at", _timestamp(self.generated_at, "generated_at"))
        for name in (
            "brief_id",
            "brief_version",
            "exposure_id",
            "target_label",
            "scope_label",
            "approximation_warning",
        ):
            _text(getattr(self, name), name)
        if self.confidence_label not in _CONFIDENCE_LABELS:
            raise TournamentExposureBuildError("unsupported confidence_label")
        _validate_brief(self)


@dataclass(frozen=True)
class TournamentExposureBundle:
    bundle_id: str
    bundle_version: str
    population_manifests: tuple[TournamentExposurePopulationManifest, ...]
    estimates: tuple[TournamentExposureEstimate, ...]
    comparisons: tuple[TournamentExposureComparison, ...]
    preparation_briefs: tuple[TournamentExposurePreparationBrief, ...]
    provenance_ref_ids: tuple[str, ...]
    caveat_ids: tuple[str, ...]
    generated_at: str

    def __post_init__(self) -> None:
        for name, key in (
            ("population_manifests", lambda value: value.population_manifest_id),
            ("estimates", lambda value: value.exposure_id),
            ("comparisons", lambda value: value.comparison_id),
            ("preparation_briefs", lambda value: value.brief_id),
        ):
            object.__setattr__(self, name, tuple(sorted(getattr(self, name), key=key)))
        object.__setattr__(
            self, "provenance_ref_ids", _refs(self.provenance_ref_ids, "provenance_ref_ids")
        )
        object.__setattr__(self, "caveat_ids", _refs(self.caveat_ids, "caveat_ids"))
        object.__setattr__(self, "generated_at", _timestamp(self.generated_at, "generated_at"))
        validate_tournament_exposure_bundle(self)


def build_tournament_exposure_estimate(
    *,
    population_manifest: TournamentExposurePopulationManifest,
    assumptions: TournamentExposureAssumptions,
    calculated_at: str,
) -> TournamentExposureEstimate:
    validate_tournament_exposure_population_manifest(population_manifest)
    if not isinstance(assumptions, TournamentExposureAssumptions):
        raise TournamentExposureBuildError(
            "assumptions must be TournamentExposureAssumptions"
        )
    normalized_time = _timestamp(calculated_at, "calculated_at")
    p = Fraction(
        population_manifest.matching_population_count,
        population_manifest.available_population_count,
    )
    seats = assumptions.opponent_seats_per_round
    opportunities = seats * assumptions.round_count
    per_round = 1 - (1 - p) ** seats
    event_wide = 1 - (1 - p) ** opportunities
    expected = opportunities * p
    low_sample = (
        population_manifest.matching_population_count
        < population_manifest.low_sample_threshold
    )
    low_coverage = _fraction_from_decimal(population_manifest.coverage_ratio) < (
        _fraction_from_decimal(population_manifest.low_coverage_threshold)
    )
    label = _confidence_label(low_sample, low_coverage)
    identity = {
        **_estimate_identity_payload(
            population_manifest=population_manifest,
            assumptions=assumptions,
            calculated_at=normalized_time,
        )
    }
    return TournamentExposureEstimate(
        exposure_id=_identity("exposure", identity),
        exposure_version=TOURNAMENT_EXPOSURE_VERSION,
        target=population_manifest.target,
        population_manifest=population_manifest,
        assumptions=assumptions,
        metagame_share_numerator=p.numerator,
        metagame_share_denominator=p.denominator,
        metagame_share=_format_fraction(p),
        seat_opportunities_per_event=opportunities,
        per_round_encounter_probability=_format_fraction(per_round),
        event_wide_encounter_probability=_format_fraction(event_wide),
        expected_encounter_count=_format_fraction(expected),
        sample_size=population_manifest.available_population_count,
        coverage_ratio=population_manifest.coverage_ratio,
        confidence_label=label,
        provenance_ref_ids=population_manifest.provenance_ref_ids,
        caveat_ids=population_manifest.caveat_ids,
        calculated_at=normalized_time,
    )


def build_tournament_exposure_comparison(
    *,
    comparison_type: str,
    selected_estimate: TournamentExposureEstimate,
    global_estimate: TournamentExposureEstimate,
    calculated_at: str,
) -> TournamentExposureComparison:
    if comparison_type not in _COMPARISON_TYPES:
        raise TournamentExposureBuildError("unsupported comparison_type")
    validate_tournament_exposure_estimate(selected_estimate)
    validate_tournament_exposure_estimate(global_estimate)
    if global_estimate.population_manifest.scope_type != "global":
        raise TournamentExposureBuildError("comparison baseline must use global scope")
    required_scope = (
        {"store", "organizer"} if comparison_type == "local_versus_global" else {"region"}
    )
    if selected_estimate.population_manifest.scope_type not in required_scope:
        raise TournamentExposureBuildError("selected scope is incompatible with comparison_type")
    if _comparison_key(selected_estimate) != _comparison_key(global_estimate):
        raise TournamentExposureBuildError("exposure estimates are not comparison-compatible")
    normalized_time = _timestamp(calculated_at, "calculated_at")
    selected_value = _event_fraction(selected_estimate)
    global_value = _event_fraction(global_estimate)
    identity = {
        **_comparison_identity_payload(
            comparison_type=comparison_type,
            selected_exposure_id=selected_estimate.exposure_id,
            global_exposure_id=global_estimate.exposure_id,
            calculated_at=normalized_time,
        )
    }
    return TournamentExposureComparison(
        comparison_id=_identity("comparison", identity),
        comparison_version=TOURNAMENT_EXPOSURE_VERSION,
        comparison_type=comparison_type,
        selected_exposure_id=selected_estimate.exposure_id,
        global_exposure_id=global_estimate.exposure_id,
        target_id=selected_estimate.target.target_id,
        selected_scope_type=selected_estimate.population_manifest.scope_type,
        selected_event_wide_probability=selected_estimate.event_wide_encounter_probability,
        global_event_wide_probability=global_estimate.event_wide_encounter_probability,
        event_wide_probability_delta=_format_fraction(selected_value - global_value),
        selected_sample_size=selected_estimate.sample_size,
        global_sample_size=global_estimate.sample_size,
        selected_coverage_ratio=selected_estimate.coverage_ratio,
        global_coverage_ratio=global_estimate.coverage_ratio,
        provenance_ref_ids=tuple(
            sorted(
                set(selected_estimate.provenance_ref_ids)
                | set(global_estimate.provenance_ref_ids),
                key=str.casefold,
            )
        ),
        caveat_ids=tuple(
            sorted(
                set(selected_estimate.caveat_ids) | set(global_estimate.caveat_ids),
                key=str.casefold,
            )
        ),
        calculated_at=normalized_time,
    )


def build_tournament_exposure_preparation_brief(
    *,
    estimate: TournamentExposureEstimate,
    comparisons: Sequence[TournamentExposureComparison] = (),
    generated_at: str,
) -> TournamentExposurePreparationBrief:
    validate_tournament_exposure_estimate(estimate)
    normalized_time = _timestamp(generated_at, "generated_at")
    ordered = tuple(sorted(comparisons, key=lambda value: value.comparison_id))
    for comparison in ordered:
        if comparison.selected_exposure_id != estimate.exposure_id:
            raise TournamentExposureBuildError(
                "brief comparison does not reference the selected exposure"
            )
    identity = {
        **_brief_identity_payload(
            exposure_id=estimate.exposure_id,
            comparison_ids=tuple(item.comparison_id for item in ordered),
            generated_at=normalized_time,
        )
    }
    assumptions = (
        f"model={estimate.assumptions.model_id}",
        f"opponent_seats_per_round={estimate.assumptions.opponent_seats_per_round}",
        f"round_count={estimate.assumptions.round_count}",
        f"expected_attendance={estimate.assumptions.expected_attendance}",
        f"event_size_class={estimate.assumptions.event_size_class}",
    )
    return TournamentExposurePreparationBrief(
        brief_id=_identity("brief", identity),
        brief_version=TOURNAMENT_EXPOSURE_VERSION,
        exposure_id=estimate.exposure_id,
        comparison_ids=tuple(item.comparison_id for item in ordered),
        target_label=estimate.target.display_label,
        scope_label=estimate.population_manifest.scope_key,
        per_round_estimate=estimate.per_round_encounter_probability,
        event_wide_estimate=estimate.event_wide_encounter_probability,
        comparison_deltas=tuple(item.event_wide_probability_delta for item in ordered),
        sample_size=estimate.sample_size,
        coverage_ratio=estimate.coverage_ratio,
        confidence_label=estimate.confidence_label,
        assumptions=assumptions,
        caveat_ids=estimate.caveat_ids,
        approximation_warning=estimate.assumptions.approximation_warning,
        generated_at=normalized_time,
    )


def build_tournament_exposure_bundle(
    *,
    population_manifests: Sequence[TournamentExposurePopulationManifest],
    estimates: Sequence[TournamentExposureEstimate],
    comparisons: Sequence[TournamentExposureComparison] = (),
    preparation_briefs: Sequence[TournamentExposurePreparationBrief] = (),
    provenance_ref_ids: Sequence[str] = (),
    caveat_ids: Sequence[str] = (),
    generated_at: str,
) -> TournamentExposureBundle:
    normalized_time = _timestamp(generated_at, "generated_at")
    identity = {
        **_bundle_identity_payload(
            population_manifests=population_manifests,
            estimates=estimates,
            comparisons=comparisons,
            preparation_briefs=preparation_briefs,
            generated_at=normalized_time,
        )
    }
    return TournamentExposureBundle(
        bundle_id=_identity("bundle", identity),
        bundle_version=TOURNAMENT_EXPOSURE_VERSION,
        population_manifests=tuple(population_manifests),
        estimates=tuple(estimates),
        comparisons=tuple(comparisons),
        preparation_briefs=tuple(preparation_briefs),
        provenance_ref_ids=tuple(provenance_ref_ids),
        caveat_ids=tuple(caveat_ids),
        generated_at=normalized_time,
    )


def validate_tournament_exposure_population_manifest(
    manifest: TournamentExposurePopulationManifest,
) -> None:
    if not isinstance(manifest, TournamentExposurePopulationManifest):
        raise TournamentExposureBuildError(
            "population manifest must be TournamentExposurePopulationManifest"
        )
    for name in (
        "population_manifest_id",
        "population_version",
        "population_spec_hash",
        "scope_key",
        "deduplication_policy",
        "deduplication_version",
    ):
        _text(getattr(manifest, name), name)
    if manifest.observation_unit != _OBSERVATION_UNIT:
        raise TournamentExposureBuildError("unsupported observation_unit")
    if manifest.scope_type not in _SCOPE_TYPES:
        raise TournamentExposureBuildError("unsupported scope_type")
    if manifest.scope_type == "global" and manifest.scope_key != "global":
        raise TournamentExposureBuildError("global scope_key must be global")
    if not manifest.source_snapshot_ids:
        raise TournamentExposureBuildError("source_snapshot_ids must not be empty")
    if not isinstance(manifest.target, TournamentExposureTarget):
        raise TournamentExposureBuildError("target must be TournamentExposureTarget")
    for name in (
        "source_record_count",
        "available_population_count",
        "matching_population_count",
        "excluded_record_count",
        "deduplicated_record_count",
        "coverage_numerator",
        "coverage_denominator",
        "low_sample_threshold",
    ):
        _nonnegative_int(getattr(manifest, name), name)
    if manifest.available_population_count <= 0:
        raise TournamentExposureBuildError("available_population_count must be positive")
    if manifest.matching_population_count > manifest.available_population_count:
        raise TournamentExposureBuildError("matching count exceeds available count")
    if manifest.available_population_count > manifest.source_record_count:
        raise TournamentExposureBuildError("available count exceeds source count")
    if manifest.excluded_record_count > manifest.source_record_count:
        raise TournamentExposureBuildError("excluded count exceeds source count")
    if manifest.deduplicated_record_count > manifest.source_record_count:
        raise TournamentExposureBuildError("deduplicated count exceeds source count")
    if manifest.coverage_denominator <= 0:
        raise TournamentExposureBuildError("coverage_denominator must be positive")
    if manifest.coverage_numerator > manifest.coverage_denominator:
        raise TournamentExposureBuildError("coverage numerator exceeds denominator")
    expected_coverage = Fraction(manifest.coverage_numerator, manifest.coverage_denominator)
    if _fraction_from_decimal(manifest.coverage_ratio) != expected_coverage:
        raise TournamentExposureBuildError("coverage_ratio is inconsistent with counts")
    threshold = _fraction_from_decimal(manifest.low_coverage_threshold)
    if threshold < 0 or threshold > 1:
        raise TournamentExposureBuildError("low_coverage_threshold is outside [0, 1]")
    _date_range(manifest.date_start, manifest.date_end)


def validate_tournament_exposure_estimate(
    estimate: TournamentExposureEstimate,
) -> None:
    if not isinstance(estimate, TournamentExposureEstimate):
        raise TournamentExposureBuildError("estimate must be TournamentExposureEstimate")
    _text(estimate.exposure_id, "exposure_id")
    _text(estimate.exposure_version, "exposure_version")
    if estimate.target != estimate.population_manifest.target:
        raise TournamentExposureBuildError("estimate target does not match manifest")
    if estimate.confidence_label not in _CONFIDENCE_LABELS:
        raise TournamentExposureBuildError("unsupported confidence_label")
    if not isinstance(estimate.assumptions, TournamentExposureAssumptions):
        raise TournamentExposureBuildError(
            "estimate assumptions must be TournamentExposureAssumptions"
        )
    p = Fraction(
        estimate.population_manifest.matching_population_count,
        estimate.population_manifest.available_population_count,
    )
    if (estimate.metagame_share_numerator, estimate.metagame_share_denominator) != (
        p.numerator,
        p.denominator,
    ):
        raise TournamentExposureBuildError("metagame share fraction is inconsistent")
    if estimate.metagame_share != _format_fraction(p):
        raise TournamentExposureBuildError("metagame share decimal is inconsistent")
    if estimate.sample_size != estimate.population_manifest.available_population_count:
        raise TournamentExposureBuildError("sample_size is inconsistent")
    if estimate.coverage_ratio != estimate.population_manifest.coverage_ratio:
        raise TournamentExposureBuildError("coverage_ratio is inconsistent")
    opportunities = (
        estimate.assumptions.opponent_seats_per_round * estimate.assumptions.round_count
    )
    if estimate.seat_opportunities_per_event != opportunities:
        raise TournamentExposureBuildError("seat opportunities are inconsistent")
    expected_values = (
        ("per_round_encounter_probability", 1 - (1 - p) ** estimate.assumptions.opponent_seats_per_round),
        ("event_wide_encounter_probability", 1 - (1 - p) ** opportunities),
        ("expected_encounter_count", opportunities * p),
    )
    for field_name, exact_value in expected_values:
        if getattr(estimate, field_name) != _format_fraction(exact_value):
            raise TournamentExposureBuildError(f"{field_name} is inconsistent")
    low_sample = (
        estimate.population_manifest.matching_population_count
        < estimate.population_manifest.low_sample_threshold
    )
    low_coverage = _fraction_from_decimal(estimate.coverage_ratio) < _fraction_from_decimal(
        estimate.population_manifest.low_coverage_threshold
    )
    if estimate.confidence_label != _confidence_label(low_sample, low_coverage):
        raise TournamentExposureBuildError("confidence_label is inconsistent")
    expected_id = _identity(
        "exposure",
        _estimate_identity_payload(
            population_manifest=estimate.population_manifest,
            assumptions=estimate.assumptions,
            calculated_at=estimate.calculated_at,
        ),
    )
    if estimate.exposure_id != expected_id:
        raise TournamentExposureBuildError("exposure_id is inconsistent")


def validate_tournament_exposure_bundle(bundle: TournamentExposureBundle) -> None:
    if not isinstance(bundle, TournamentExposureBundle):
        raise TournamentExposureBuildError("bundle must be TournamentExposureBundle")
    _text(bundle.bundle_id, "bundle_id")
    _text(bundle.bundle_version, "bundle_version")
    expected_bundle_id = _identity(
        "bundle",
        _bundle_identity_payload(
            population_manifests=bundle.population_manifests,
            estimates=bundle.estimates,
            comparisons=bundle.comparisons,
            preparation_briefs=bundle.preparation_briefs,
            generated_at=bundle.generated_at,
        ),
    )
    if bundle.bundle_id != expected_bundle_id:
        raise TournamentExposureBuildError("bundle_id is inconsistent")
    manifest_ids = [value.population_manifest_id for value in bundle.population_manifests]
    exposure_ids = [value.exposure_id for value in bundle.estimates]
    comparison_ids = [value.comparison_id for value in bundle.comparisons]
    brief_ids = [value.brief_id for value in bundle.preparation_briefs]
    for name, values in (
        ("population manifest", manifest_ids),
        ("exposure", exposure_ids),
        ("comparison", comparison_ids),
        ("brief", brief_ids),
    ):
        if len(values) != len(set(values)):
            raise TournamentExposureBuildError(f"duplicate {name} ID")
    manifest_set = set(manifest_ids)
    exposure_set = set(exposure_ids)
    comparison_set = set(comparison_ids)
    for estimate in bundle.estimates:
        validate_tournament_exposure_estimate(estimate)
        if estimate.population_manifest.population_manifest_id not in manifest_set:
            raise TournamentExposureBuildError("estimate has dangling population reference")
    for comparison in bundle.comparisons:
        _validate_comparison(comparison)
        if (
            comparison.selected_exposure_id not in exposure_set
            or comparison.global_exposure_id not in exposure_set
        ):
            raise TournamentExposureBuildError("comparison has dangling exposure reference")
    for brief in bundle.preparation_briefs:
        _validate_brief(brief)
        if brief.exposure_id not in exposure_set:
            raise TournamentExposureBuildError("brief has dangling exposure reference")
        if not set(brief.comparison_ids).issubset(comparison_set):
            raise TournamentExposureBuildError("brief has dangling comparison reference")


def tournament_exposure_estimate_to_dict(
    estimate: TournamentExposureEstimate,
) -> dict[str, Any]:
    validate_tournament_exposure_estimate(estimate)
    return {
        "exposure_id": estimate.exposure_id,
        "exposure_version": estimate.exposure_version,
        "target": _target_to_dict(estimate.target),
        "population_manifest": _manifest_to_dict(estimate.population_manifest),
        "assumptions": _assumptions_to_dict(estimate.assumptions),
        "metagame_share_numerator": estimate.metagame_share_numerator,
        "metagame_share_denominator": estimate.metagame_share_denominator,
        "metagame_share": estimate.metagame_share,
        "seat_opportunities_per_event": estimate.seat_opportunities_per_event,
        "per_round_encounter_probability": estimate.per_round_encounter_probability,
        "event_wide_encounter_probability": estimate.event_wide_encounter_probability,
        "expected_encounter_count": estimate.expected_encounter_count,
        "sample_size": estimate.sample_size,
        "coverage_ratio": estimate.coverage_ratio,
        "confidence_label": estimate.confidence_label,
        "provenance_ref_ids": list(estimate.provenance_ref_ids),
        "caveat_ids": list(estimate.caveat_ids),
        "calculated_at": estimate.calculated_at,
    }


def tournament_exposure_comparison_to_dict(
    comparison: TournamentExposureComparison,
) -> dict[str, Any]:
    return {
        name: (list(value) if isinstance(value, tuple) else value)
        for name, value in comparison.__dict__.items()
    }


def tournament_exposure_preparation_brief_to_dict(
    brief: TournamentExposurePreparationBrief,
) -> dict[str, Any]:
    return {
        name: (list(value) if isinstance(value, tuple) else value)
        for name, value in brief.__dict__.items()
    }


def tournament_exposure_bundle_to_dict(
    bundle: TournamentExposureBundle,
) -> dict[str, Any]:
    validate_tournament_exposure_bundle(bundle)
    return {
        "bundle_id": bundle.bundle_id,
        "bundle_version": bundle.bundle_version,
        "population_manifests": [
            _manifest_to_dict(value) for value in bundle.population_manifests
        ],
        "estimates": [
            tournament_exposure_estimate_to_dict(value) for value in bundle.estimates
        ],
        "comparisons": [
            tournament_exposure_comparison_to_dict(value) for value in bundle.comparisons
        ],
        "preparation_briefs": [
            tournament_exposure_preparation_brief_to_dict(value)
            for value in bundle.preparation_briefs
        ],
        "provenance_ref_ids": list(bundle.provenance_ref_ids),
        "caveat_ids": list(bundle.caveat_ids),
        "generated_at": bundle.generated_at,
    }


def _manifest_to_dict(manifest: TournamentExposurePopulationManifest) -> dict[str, Any]:
    result = dict(manifest.__dict__)
    result["target"] = _target_to_dict(manifest.target)
    for name in ("source_snapshot_ids", "provenance_ref_ids", "caveat_ids"):
        result[name] = list(result[name])
    return result


def _target_to_dict(target: TournamentExposureTarget) -> dict[str, Any]:
    return {
        "target_type": target.target_type,
        "target_id": target.target_id,
        "target_version": target.target_version,
        "display_label": target.display_label,
        "component_ids": list(target.component_ids),
        "provenance_ref_ids": list(target.provenance_ref_ids),
    }


def _assumptions_to_dict(assumptions: TournamentExposureAssumptions) -> dict[str, Any]:
    return dict(assumptions.__dict__)


def _comparison_key(estimate: TournamentExposureEstimate) -> tuple[Any, ...]:
    assumptions = estimate.assumptions
    return (
        estimate.target.target_type,
        estimate.target.target_id,
        estimate.target.target_version,
        assumptions.model_id,
        assumptions.model_version,
        assumptions.formula_version,
        assumptions.numeric_policy_version,
        assumptions.opponent_seats_per_round,
        assumptions.round_count,
        estimate.population_manifest.date_start,
        estimate.population_manifest.date_end,
    )


def _estimate_identity_payload(
    *,
    population_manifest: TournamentExposurePopulationManifest,
    assumptions: TournamentExposureAssumptions,
    calculated_at: str,
) -> dict[str, Any]:
    return {
        "identity_version": TOURNAMENT_EXPOSURE_VERSION,
        "target": _target_to_dict(population_manifest.target),
        "population_manifest_id": population_manifest.population_manifest_id,
        "population_spec_hash": population_manifest.population_spec_hash,
        "assumptions": _assumptions_to_dict(assumptions),
        "calculated_at": calculated_at,
    }


def _comparison_identity_payload(
    *,
    comparison_type: str,
    selected_exposure_id: str,
    global_exposure_id: str,
    calculated_at: str,
) -> dict[str, Any]:
    return {
        "identity_version": TOURNAMENT_EXPOSURE_VERSION,
        "comparison_type": comparison_type,
        "selected_exposure_id": selected_exposure_id,
        "global_exposure_id": global_exposure_id,
        "calculated_at": calculated_at,
    }


def _brief_identity_payload(
    *,
    exposure_id: str,
    comparison_ids: Sequence[str],
    generated_at: str,
) -> dict[str, Any]:
    return {
        "identity_version": TOURNAMENT_EXPOSURE_VERSION,
        "exposure_id": exposure_id,
        "comparison_ids": sorted(comparison_ids),
        "generated_at": generated_at,
    }


def _bundle_identity_payload(
    *,
    population_manifests: Sequence[TournamentExposurePopulationManifest],
    estimates: Sequence[TournamentExposureEstimate],
    comparisons: Sequence[TournamentExposureComparison],
    preparation_briefs: Sequence[TournamentExposurePreparationBrief],
    generated_at: str,
) -> dict[str, Any]:
    return {
        "identity_version": TOURNAMENT_EXPOSURE_VERSION,
        "population_manifest_ids": sorted(
            value.population_manifest_id for value in population_manifests
        ),
        "exposure_ids": sorted(value.exposure_id for value in estimates),
        "comparison_ids": sorted(value.comparison_id for value in comparisons),
        "brief_ids": sorted(value.brief_id for value in preparation_briefs),
        "generated_at": generated_at,
    }


def _validate_comparison(comparison: TournamentExposureComparison) -> None:
    if comparison.selected_exposure_id == comparison.global_exposure_id:
        raise TournamentExposureBuildError("comparison exposure IDs must differ")
    for name in ("selected_sample_size", "global_sample_size"):
        _positive_int(getattr(comparison, name), name)
    for name in (
        "selected_event_wide_probability",
        "global_event_wide_probability",
        "selected_coverage_ratio",
        "global_coverage_ratio",
    ):
        value = _fraction_from_decimal(getattr(comparison, name))
        if value < 0 or value > 1:
            raise TournamentExposureBuildError(f"{name} is outside [0, 1]")
    delta = _fraction_from_decimal(comparison.event_wide_probability_delta)
    if delta < -1 or delta > 1:
        raise TournamentExposureBuildError(
            "event_wide_probability_delta is outside [-1, 1]"
        )
    expected_id = _identity(
        "comparison",
        _comparison_identity_payload(
            comparison_type=comparison.comparison_type,
            selected_exposure_id=comparison.selected_exposure_id,
            global_exposure_id=comparison.global_exposure_id,
            calculated_at=comparison.calculated_at,
        ),
    )
    if comparison.comparison_id != expected_id:
        raise TournamentExposureBuildError("comparison_id is inconsistent")


def _validate_brief(brief: TournamentExposurePreparationBrief) -> None:
    _positive_int(brief.sample_size, "sample_size")
    for name in ("per_round_estimate", "event_wide_estimate", "coverage_ratio"):
        value = _fraction_from_decimal(getattr(brief, name))
        if value < 0 or value > 1:
            raise TournamentExposureBuildError(f"{name} is outside [0, 1]")
    for value in brief.comparison_deltas:
        delta = _fraction_from_decimal(value)
        if delta < -1 or delta > 1:
            raise TournamentExposureBuildError(
                "comparison delta is outside [-1, 1]"
            )
    expected_id = _identity(
        "brief",
        _brief_identity_payload(
            exposure_id=brief.exposure_id,
            comparison_ids=brief.comparison_ids,
            generated_at=brief.generated_at,
        ),
    )
    if brief.brief_id != expected_id:
        raise TournamentExposureBuildError("brief_id is inconsistent")


def _event_fraction(estimate: TournamentExposureEstimate) -> Fraction:
    p = Fraction(estimate.metagame_share_numerator, estimate.metagame_share_denominator)
    return 1 - (1 - p) ** estimate.seat_opportunities_per_event


def _confidence_label(low_sample: bool, low_coverage: bool) -> str:
    if low_sample and low_coverage:
        return "LIMITED_SAMPLE_AND_COVERAGE"
    if low_sample:
        return "LIMITED_SAMPLE"
    if low_coverage:
        return "LIMITED_COVERAGE"
    return "SUFFICIENT"


def _identity(prefix: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return f"{prefix}:{sha256(canonical.encode('utf-8')).hexdigest()}"


def _format_fraction(value: Fraction) -> str:
    sign = "-" if value < 0 else ""
    numerator = abs(value.numerator)
    denominator = value.denominator
    scale = 10**_DECIMAL_PLACES
    quotient, remainder = divmod(numerator * scale, denominator)
    doubled = remainder * 2
    if doubled > denominator or (doubled == denominator and quotient % 2 == 1):
        quotient += 1
    whole, fractional = divmod(quotient, scale)
    return f"{sign}{whole}.{fractional:0{_DECIMAL_PLACES}d}"


def _fraction_from_decimal(value: str) -> Fraction:
    if not isinstance(value, str) or not value.strip():
        raise TournamentExposureBuildError("decimal value requires non-empty text")
    try:
        decimal_value = Decimal(value)
    except InvalidOperation as exc:
        raise TournamentExposureBuildError("invalid decimal value") from exc
    if not decimal_value.is_finite():
        raise TournamentExposureBuildError("decimal value must be finite")
    return Fraction(decimal_value)


def _timestamp(value: str, name: str) -> str:
    _text(value, name)
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise TournamentExposureBuildError(f"{name} must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise TournamentExposureBuildError(f"{name} requires a timezone")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def _date_range(start: str, end: str) -> None:
    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
    except (TypeError, ValueError) as exc:
        raise TournamentExposureBuildError("date range must use ISO dates") from exc
    if end_date < start_date:
        raise TournamentExposureBuildError("date_end precedes date_start")


def _refs(values: Sequence[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TournamentExposureBuildError(f"{name} must be a sequence")
    normalized = tuple(sorted((_text(value, name) for value in values), key=str.casefold))
    if len(normalized) != len(set(normalized)):
        raise TournamentExposureBuildError(f"{name} contains duplicate values")
    return normalized


def _texts(values: Sequence[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TournamentExposureBuildError(f"{name} must be a sequence")
    return tuple(_text(value, name) for value in values)


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TournamentExposureBuildError(f"{name} requires non-empty text")
    if value != value.strip():
        raise TournamentExposureBuildError(f"{name} must not contain surrounding whitespace")
    return value


def _nonnegative_int(value: Any, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TournamentExposureBuildError(f"{name} must be a nonnegative integer")


def _positive_int(value: Any, name: str) -> None:
    _nonnegative_int(value, name)
    if value <= 0:
        raise TournamentExposureBuildError(f"{name} must be positive")
