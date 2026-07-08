"""In-memory weight profile packets for future Decision Intelligence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


ALLOWED_COMPONENT_TYPES = frozenset(
    {
        "authority",
        "measured_metric",
        "source_agreement",
        "coverage",
        "sample_size",
        "tournament_performance",
        "regional_signal",
        "historical_signal",
        "innovation_signal",
        "simulator_comparison",
        "primer_context",
        "user_context",
        "caveat_penalty",
        "conflict_penalty",
        "unsupported_card_penalty",
        "speculation_penalty",
    }
)

ALLOWED_DECISION_TYPES = frozenset(
    {
        "evidence_summary",
        "deck_health_input",
        "replacement_input",
        "package_input",
        "dashboard_input",
        "candidate_signal",
        "all",
    }
)

ALLOWED_NORMALIZATION_RULES = frozenset({"none", "sum_to_one", "max_abs_one"})
ALLOWED_ANALYSIS_SCOPES = frozenset(
    {
        "deck_analysis",
        "commander_profile",
        "card_profile",
        "package_profile",
        "dashboard_context",
        "report_context",
    }
)

FORBIDDEN_METADATA_KEYS = frozenset(
    {
        "raw_input",
        "private_deck_text",
        "full_primer_body",
        "raw_" + "provider_payload",
        "provider_payload",
        "original_import_text",
    }
)

STACK_TRACE_KEYS = frozenset({"traceback", "stack", "stack_trace", "exception_trace"})

FORBIDDEN_TEXT_FRAGMENTS = (
    "should " + "play",
    "should be " + "played",
    "should be " + "cut",
    "must " + "include",
    "correct " + "card",
    "breaks the " + "format",
    "secretly " + "optimal",
    "cut " + "this",
    "strict " + "upgrade",
    "auto-" + "include",
    "recommended " + "cut",
    "recommended " + "include",
)


class WeightProfileBuildError(ValueError):
    """Raised when weight profile packets cannot be built safely."""


@dataclass(frozen=True)
class WeightComponent:
    component_id: str
    component_name: str
    component_type: str
    weight: float
    enabled: bool
    minimum_threshold: float | None
    maximum_threshold: float | None
    applies_to_decision_types: tuple[str, ...]
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.component_id, "component_id")
        object.__setattr__(self, "component_name", _validate_text(self.component_name, "component_name"))
        object.__setattr__(
            self,
            "component_type",
            _normalize_allowed(self.component_type, ALLOWED_COMPONENT_TYPES, "component_type"),
        )
        _validate_bounded_number(self.weight, "weight", -10.0, 10.0)
        if not isinstance(self.enabled, bool):
            raise WeightProfileBuildError("enabled must be a bool")
        for field_name in ("minimum_threshold", "maximum_threshold"):
            value = getattr(self, field_name)
            if value is not None:
                _validate_bounded_number(value, field_name, -10.0, 10.0)
        if (
            self.minimum_threshold is not None
            and self.maximum_threshold is not None
            and self.minimum_threshold > self.maximum_threshold
        ):
            raise WeightProfileBuildError("minimum_threshold cannot exceed maximum_threshold")
        object.__setattr__(
            self,
            "applies_to_decision_types",
            tuple(
                sorted(
                    _normalize_allowed(item, ALLOWED_DECISION_TYPES, "applies_to_decision_types")
                    for item in self.applies_to_decision_types
                )
            ),
        )
        if not self.applies_to_decision_types:
            raise WeightProfileBuildError("applies_to_decision_types is required")
        object.__setattr__(self, "description", _validate_text(self.description, "description"))
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class WeightProfile:
    profile_id: str
    profile_name: str
    profile_version: str
    profile_label: str
    profile_description: str
    components: tuple[WeightComponent, ...]
    normalization_rule: str
    minimum_confidence: float
    minimum_coverage_ratio: float
    minimum_sample_size: int
    generated_at: str
    analysis_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.profile_id, "profile_id")
        _require_text(self.profile_name, "profile_name")
        _require_text(self.profile_version, "profile_version")
        object.__setattr__(self, "profile_label", _validate_text(self.profile_label, "profile_label"))
        object.__setattr__(self, "profile_description", _validate_text(self.profile_description, "profile_description"))
        object.__setattr__(self, "components", _sort_components(self.components))
        _require_unique([item.component_id for item in self.components], "component_id")
        object.__setattr__(
            self,
            "normalization_rule",
            _normalize_allowed(self.normalization_rule, ALLOWED_NORMALIZATION_RULES, "normalization_rule"),
        )
        _validate_ratio(self.minimum_confidence, "minimum_confidence")
        _validate_ratio(self.minimum_coverage_ratio, "minimum_coverage_ratio")
        _validate_non_negative_int(self.minimum_sample_size, "minimum_sample_size")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.analysis_version, "analysis_version")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))
        _validate_weight_profile_boundaries(self)


@dataclass(frozen=True)
class AnalysisProfile:
    analysis_profile_id: str
    analysis_profile_name: str
    analysis_profile_version: str
    weight_profile_id: str
    weight_profile_version: str
    decision_version: str
    evidence_version: str
    analysis_scope: str
    default_filters: dict[str, Any]
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.analysis_profile_id, "analysis_profile_id")
        _require_text(self.analysis_profile_name, "analysis_profile_name")
        _require_text(self.analysis_profile_version, "analysis_profile_version")
        _require_text(self.weight_profile_id, "weight_profile_id")
        _require_text(self.weight_profile_version, "weight_profile_version")
        _require_text(self.decision_version, "decision_version")
        _require_text(self.evidence_version, "evidence_version")
        object.__setattr__(
            self,
            "analysis_scope",
            _normalize_allowed(self.analysis_scope, ALLOWED_ANALYSIS_SCOPES, "analysis_scope"),
        )
        object.__setattr__(self, "default_filters", _validate_metadata(self.default_filters))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


@dataclass(frozen=True)
class WeightProfileCompatibilityReport:
    base_profile_id: str
    base_profile_version: str
    candidate_profile_id: str
    candidate_profile_version: str
    compatible: bool
    informational_only: bool
    changed_component_ids: tuple[str, ...]
    added_component_ids: tuple[str, ...]
    removed_component_ids: tuple[str, ...]
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.base_profile_id, "base_profile_id")
        _require_text(self.base_profile_version, "base_profile_version")
        _require_text(self.candidate_profile_id, "candidate_profile_id")
        _require_text(self.candidate_profile_version, "candidate_profile_version")
        if not isinstance(self.compatible, bool):
            raise WeightProfileBuildError("compatible must be a bool")
        if not isinstance(self.informational_only, bool):
            raise WeightProfileBuildError("informational_only must be a bool")
        for field_name in ("changed_component_ids", "added_component_ids", "removed_component_ids"):
            object.__setattr__(self, field_name, _sorted_text_tuple(getattr(self, field_name), field_name))
        _require_text(self.generated_at, "generated_at")
        object.__setattr__(self, "metadata", _validate_metadata(self.metadata))


def build_weight_profile(
    profile_id: str,
    profile_name: str,
    profile_version: str,
    profile_label: str,
    profile_description: str,
    components: tuple[WeightComponent, ...],
    normalization_rule: str,
    minimum_confidence: float,
    minimum_coverage_ratio: float,
    minimum_sample_size: int,
    generated_at: str,
    analysis_version: str,
    metadata: dict[str, Any] | None = None,
) -> WeightProfile:
    """Build one deterministic in-memory weight profile packet."""

    return WeightProfile(
        profile_id=profile_id,
        profile_name=profile_name,
        profile_version=profile_version,
        profile_label=profile_label,
        profile_description=profile_description,
        components=components,
        normalization_rule=normalization_rule,
        minimum_confidence=minimum_confidence,
        minimum_coverage_ratio=minimum_coverage_ratio,
        minimum_sample_size=minimum_sample_size,
        generated_at=generated_at,
        analysis_version=analysis_version,
        metadata=metadata or {},
    )


def build_analysis_profile(
    analysis_profile_id: str,
    analysis_profile_name: str,
    analysis_profile_version: str,
    weight_profile_id: str,
    weight_profile_version: str,
    decision_version: str,
    evidence_version: str,
    analysis_scope: str,
    default_filters: dict[str, Any],
    generated_at: str,
    metadata: dict[str, Any] | None = None,
) -> AnalysisProfile:
    """Build one deterministic in-memory analysis profile packet."""

    return AnalysisProfile(
        analysis_profile_id=analysis_profile_id,
        analysis_profile_name=analysis_profile_name,
        analysis_profile_version=analysis_profile_version,
        weight_profile_id=weight_profile_id,
        weight_profile_version=weight_profile_version,
        decision_version=decision_version,
        evidence_version=evidence_version,
        analysis_scope=analysis_scope,
        default_filters=default_filters,
        generated_at=generated_at,
        metadata=metadata or {},
    )


def validate_weight_profile(profile: WeightProfile) -> WeightProfile:
    """Validate one weight profile packet."""

    if not isinstance(profile, WeightProfile):
        raise WeightProfileBuildError("profile must be a WeightProfile")
    return profile


def validate_analysis_profile(profile: AnalysisProfile) -> AnalysisProfile:
    """Validate one analysis profile packet."""

    if not isinstance(profile, AnalysisProfile):
        raise WeightProfileBuildError("profile must be an AnalysisProfile")
    return profile


def compare_weight_profile_versions(
    base: WeightProfile,
    candidate: WeightProfile,
    generated_at: str,
    metadata: dict[str, Any] | None = None,
) -> WeightProfileCompatibilityReport:
    """Compare profiles without blocking replay of either version."""

    base_components = {item.component_id: item for item in base.components}
    candidate_components = {item.component_id: item for item in candidate.components}
    changed = [
        component_id
        for component_id in sorted(base_components.keys() & candidate_components.keys())
        if weight_component_to_dict(base_components[component_id])
        != weight_component_to_dict(candidate_components[component_id])
    ]
    added = sorted(candidate_components.keys() - base_components.keys())
    removed = sorted(base_components.keys() - candidate_components.keys())
    return WeightProfileCompatibilityReport(
        base_profile_id=base.profile_id,
        base_profile_version=base.profile_version,
        candidate_profile_id=candidate.profile_id,
        candidate_profile_version=candidate.profile_version,
        compatible=not changed and not added and not removed,
        informational_only=True,
        changed_component_ids=tuple(changed),
        added_component_ids=tuple(added),
        removed_component_ids=tuple(removed),
        generated_at=generated_at,
        metadata=metadata or {},
    )


def weight_component_to_dict(component: WeightComponent) -> dict[str, Any]:
    return {
        "component_id": component.component_id,
        "component_name": component.component_name,
        "component_type": component.component_type,
        "weight": component.weight,
        "enabled": component.enabled,
        "minimum_threshold": component.minimum_threshold,
        "maximum_threshold": component.maximum_threshold,
        "applies_to_decision_types": list(component.applies_to_decision_types),
        "description": component.description,
        "metadata": _sorted_json_object(component.metadata),
    }


def weight_profile_to_dict(profile: WeightProfile) -> dict[str, Any]:
    """Serialize one weight profile deterministically."""

    validated = validate_weight_profile(profile)
    return {
        "profile_id": validated.profile_id,
        "profile_name": validated.profile_name,
        "profile_version": validated.profile_version,
        "profile_label": validated.profile_label,
        "profile_description": validated.profile_description,
        "components": [weight_component_to_dict(item) for item in validated.components],
        "normalization_rule": validated.normalization_rule,
        "minimum_confidence": validated.minimum_confidence,
        "minimum_coverage_ratio": validated.minimum_coverage_ratio,
        "minimum_sample_size": validated.minimum_sample_size,
        "generated_at": validated.generated_at,
        "analysis_version": validated.analysis_version,
        "metadata": _sorted_json_object(validated.metadata),
    }


def analysis_profile_to_dict(profile: AnalysisProfile) -> dict[str, Any]:
    """Serialize one analysis profile deterministically."""

    validated = validate_analysis_profile(profile)
    return {
        "analysis_profile_id": validated.analysis_profile_id,
        "analysis_profile_name": validated.analysis_profile_name,
        "analysis_profile_version": validated.analysis_profile_version,
        "weight_profile_id": validated.weight_profile_id,
        "weight_profile_version": validated.weight_profile_version,
        "decision_version": validated.decision_version,
        "evidence_version": validated.evidence_version,
        "analysis_scope": validated.analysis_scope,
        "default_filters": _sorted_json_object(validated.default_filters),
        "generated_at": validated.generated_at,
        "metadata": _sorted_json_object(validated.metadata),
    }


def compatibility_report_to_dict(report: WeightProfileCompatibilityReport) -> dict[str, Any]:
    """Serialize one compatibility report deterministically."""

    return {
        "base_profile_id": report.base_profile_id,
        "base_profile_version": report.base_profile_version,
        "candidate_profile_id": report.candidate_profile_id,
        "candidate_profile_version": report.candidate_profile_version,
        "compatible": report.compatible,
        "informational_only": report.informational_only,
        "changed_component_ids": list(report.changed_component_ids),
        "added_component_ids": list(report.added_component_ids),
        "removed_component_ids": list(report.removed_component_ids),
        "generated_at": report.generated_at,
        "metadata": _sorted_json_object(report.metadata),
    }


def _validate_weight_profile_boundaries(profile: WeightProfile) -> None:
    component_types = {item.component_type for item in profile.components if item.enabled}
    if "measured_metric" not in component_types:
        raise WeightProfileBuildError("enabled measured_metric component is required")
    if "simulator_comparison" in component_types:
        for item in profile.components:
            if item.component_type == "simulator_comparison" and "simulator_only" not in item.metadata:
                raise WeightProfileBuildError("simulator_comparison components must be marked simulator_only")
    for item in profile.components:
        if item.component_type in {"caveat_penalty", "conflict_penalty"} and not item.enabled:
            raise WeightProfileBuildError("caveat/conflict penalty components must remain visible and enabled")


def _sort_components(items: tuple[WeightComponent, ...]) -> tuple[WeightComponent, ...]:
    if not items:
        raise WeightProfileBuildError("components are required")
    for item in items:
        if not isinstance(item, WeightComponent):
            raise WeightProfileBuildError("components must contain WeightComponent")
    return tuple(sorted(items, key=lambda item: item.component_id))


def _require_unique(values: list[str], field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise WeightProfileBuildError(f"duplicate {field_name}: {value}")
        seen.add(value)


def _sorted_text_tuple(items: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(items, tuple):
        raise WeightProfileBuildError(f"{field_name} must be a tuple")
    return tuple(sorted(_require_text(item, field_name) for item in items))


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WeightProfileBuildError(f"{field_name} is required")
    return value.strip()


def _normalize_allowed(value: str, allowed: frozenset[str], field_name: str) -> str:
    normalized = _require_text(value, field_name).lower()
    if normalized not in allowed:
        raise WeightProfileBuildError(f"unsupported {field_name}: {value}")
    return normalized


def _validate_bounded_number(value: float, field_name: str, minimum: float, maximum: float) -> None:
    if not isinstance(value, int | float):
        raise WeightProfileBuildError(f"{field_name} must be numeric")
    if value < minimum or value > maximum:
        raise WeightProfileBuildError(f"{field_name} must be between {minimum} and {maximum}")


def _validate_ratio(value: float, field_name: str) -> None:
    _validate_bounded_number(value, field_name, 0.0, 1.0)


def _validate_non_negative_int(value: int, field_name: str) -> None:
    if not isinstance(value, int) or value < 0:
        raise WeightProfileBuildError(f"{field_name} must be a non-negative integer")


def _validate_text(value: str, field_name: str) -> str:
    text = _require_text(value, field_name)
    normalized = " ".join(text.lower().split())
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment in normalized:
            raise WeightProfileBuildError(f"forbidden strategic language in {field_name}")
    return text


def _validate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise WeightProfileBuildError("metadata must be an object")
    return _sorted_json_object(_validate_json_value(metadata, "metadata"))


def _validate_json_value(value: Any, path: str) -> Any:
    if isinstance(value, dict):
        validated: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str) or not key.strip():
                raise WeightProfileBuildError(f"{path} contains invalid key")
            normalized_key = _normalize_metadata_key(key)
            if normalized_key in FORBIDDEN_METADATA_KEYS:
                raise WeightProfileBuildError(f"{path} contains forbidden metadata key: {key}")
            if normalized_key in STACK_TRACE_KEYS:
                raise WeightProfileBuildError(f"{path} contains forbidden stack trace key: {key}")
            validated[key] = _validate_json_value(child, f"{path}.{key}")
        return validated
    if isinstance(value, (list, tuple)):
        return [_validate_json_value(child, f"{path}[]") for child in value]
    if isinstance(value, str):
        return _validate_text(value, path)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise WeightProfileBuildError(f"{path} must be JSON-compatible")


def _normalize_metadata_key(key: str) -> str:
    return key.strip().lower().replace("-", "_").replace(" ", "_")


def _sorted_json_object(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, sort_keys=True))
