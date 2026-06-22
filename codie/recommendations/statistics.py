"""Pure recommendation statistics helpers.

These helpers do not generate recommendation candidates or explanations. They
exist so later recommendation phases can compose deterministic, tested math.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class FrequencyStats:
    observed_count: int
    total_count: int
    frequency: float | None


@dataclass(frozen=True)
class ConfidenceRating:
    sample_size: int
    score: float
    label: str


@dataclass(frozen=True)
class GenericStapleProfile:
    is_generic_staple: bool
    penalty: float
    reasons: tuple[str, ...]


def _require_non_negative(value: float, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return max(minimum, min(maximum, value))


def safe_rate(numerator: float, denominator: float) -> float | None:
    _require_non_negative(numerator, "numerator")
    _require_non_negative(denominator, "denominator")
    if denominator == 0:
        return None
    return numerator / denominator


def inclusion_rate(included_count: float, total_count: float) -> float | None:
    return safe_rate(included_count, total_count)


def weighted_inclusion_rate(included_weight: float, total_weight: float) -> float | None:
    return safe_rate(included_weight, total_weight)


def frequency_stats(observed_count: int, total_count: int) -> FrequencyStats:
    if not isinstance(observed_count, int) or not isinstance(total_count, int):
        raise TypeError("frequency counts must be integers")
    _require_non_negative(observed_count, "observed_count")
    _require_non_negative(total_count, "total_count")
    if observed_count > total_count:
        raise ValueError("observed_count cannot exceed total_count")
    return FrequencyStats(
        observed_count=observed_count,
        total_count=total_count,
        frequency=safe_rate(observed_count, total_count),
    )


def lift_score(focus_rate: float | None, baseline_rate: float | None, *, cap: float = 5.0) -> float | None:
    _require_non_negative(cap, "cap")
    if cap == 0:
        raise ValueError("cap must be greater than zero")
    if focus_rate is None or baseline_rate is None:
        return None
    _require_non_negative(focus_rate, "focus_rate")
    _require_non_negative(baseline_rate, "baseline_rate")
    if baseline_rate == 0:
        return None
    return min(focus_rate / baseline_rate, cap)


def confidence_rating(
    sample_size: int,
    *,
    low_threshold: int = 10,
    medium_threshold: int = 30,
    high_threshold: int = 100,
) -> ConfidenceRating:
    if not all(isinstance(value, int) for value in (sample_size, low_threshold, medium_threshold, high_threshold)):
        raise TypeError("confidence thresholds and sample size must be integers")
    _require_non_negative(sample_size, "sample_size")
    _require_non_negative(low_threshold, "low_threshold")
    _require_non_negative(medium_threshold, "medium_threshold")
    _require_non_negative(high_threshold, "high_threshold")
    if not low_threshold < medium_threshold < high_threshold:
        raise ValueError("confidence thresholds must be strictly increasing")
    if sample_size < low_threshold:
        label = "insufficient"
    elif sample_size < medium_threshold:
        label = "low"
    elif sample_size < high_threshold:
        label = "medium"
    else:
        label = "high"
    return ConfidenceRating(
        sample_size=sample_size,
        score=clamp(sample_size / high_threshold),
        label=label,
    )


def _normalized_set(values: Iterable[str]) -> set[str]:
    return {str(value).strip() for value in values if str(value).strip()}


def jaccard_similarity(left: Iterable[str], right: Iterable[str]) -> float:
    left_set = _normalized_set(left)
    right_set = _normalized_set(right)
    union = left_set | right_set
    if not union:
        return 0.0
    return len(left_set & right_set) / len(union)


def _clean_weights(values: Mapping[str, float]) -> dict[str, float]:
    weights: dict[str, float] = {}
    for key, value in values.items():
        name = str(key).strip()
        if not name:
            continue
        weight = float(value)
        _require_non_negative(weight, f"weight for {name}")
        if weight > 0:
            weights[name] = weight
    return weights


def weighted_jaccard_similarity(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    left_weights = _clean_weights(left)
    right_weights = _clean_weights(right)
    keys = set(left_weights) | set(right_weights)
    if not keys:
        return 0.0
    numerator = sum(min(left_weights.get(key, 0.0), right_weights.get(key, 0.0)) for key in keys)
    denominator = sum(max(left_weights.get(key, 0.0), right_weights.get(key, 0.0)) for key in keys)
    return numerator / denominator if denominator else 0.0


def generic_staple_profile(
    *,
    global_inclusion_rate: float | None,
    commander_lift: float | None,
    color_identity_baseline_rate: float | None,
    commander_frequency: int,
    broad_commander_threshold: int = 8,
    high_inclusion_threshold: float = 0.40,
    low_lift_threshold: float = 1.15,
    high_color_baseline_threshold: float = 0.30,
    penalty: float = 0.25,
) -> GenericStapleProfile:
    _require_non_negative(commander_frequency, "commander_frequency")
    _require_non_negative(broad_commander_threshold, "broad_commander_threshold")
    _require_non_negative(high_inclusion_threshold, "high_inclusion_threshold")
    _require_non_negative(low_lift_threshold, "low_lift_threshold")
    _require_non_negative(high_color_baseline_threshold, "high_color_baseline_threshold")
    _require_non_negative(penalty, "penalty")

    reasons: list[str] = []
    if global_inclusion_rate is not None:
        _require_non_negative(global_inclusion_rate, "global_inclusion_rate")
        if global_inclusion_rate >= high_inclusion_threshold:
            reasons.append("high_global_inclusion")
    if commander_lift is not None:
        _require_non_negative(commander_lift, "commander_lift")
        if commander_lift <= low_lift_threshold:
            reasons.append("low_commander_lift")
    if color_identity_baseline_rate is not None:
        _require_non_negative(color_identity_baseline_rate, "color_identity_baseline_rate")
        if color_identity_baseline_rate >= high_color_baseline_threshold:
            reasons.append("high_color_identity_baseline")
    if commander_frequency >= broad_commander_threshold:
        reasons.append("broad_commander_frequency")

    required_reasons = {
        "high_global_inclusion",
        "low_commander_lift",
        "high_color_identity_baseline",
        "broad_commander_frequency",
    }
    is_generic = required_reasons.issubset(reasons)
    return GenericStapleProfile(
        is_generic_staple=is_generic,
        penalty=penalty if is_generic else 0.0,
        reasons=tuple(reasons),
    )
