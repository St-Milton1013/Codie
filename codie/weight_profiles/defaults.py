"""Default Weight Profile packets."""

from __future__ import annotations

from codie.weight_profiles.models import WeightComponent, build_weight_profile


GENERATED_AT = "2026-07-08T00:00:00+00:00"
ANALYSIS_VERSION = "phase27b-weight-profile"


def build_default_weight_profiles():
    """Return deterministic default weight profiles."""

    return (
        _profile("competitive-default", "Competitive Default", "Balanced competitive evidence profile."),
        _profile(
            "tournament-heavy",
            "Tournament Heavy",
            "Places extra emphasis on tournament performance.",
            tournament_weight=1.45,
        ),
        _profile(
            "simulation-heavy",
            "Simulation Heavy",
            "Places extra emphasis on simulator comparisons.",
            simulator_weight=1.25,
        ),
        _profile(
            "primer-aware",
            "Primer Aware",
            "Allows primer context as explanatory context.",
            primer_weight=0.35,
        ),
        _profile(
            "budget-aware",
            "Budget Aware",
            "Generic price-sensitivity weighting; user-specific budget limits require a future user context overlay.",
            user_weight=0.25,
        ),
    )


def _profile(
    profile_id: str,
    label: str,
    description: str,
    tournament_weight: float = 1.0,
    simulator_weight: float = 0.5,
    primer_weight: float = 0.2,
    user_weight: float = 0.0,
):
    components = (
        WeightComponent(
            component_id="authority",
            component_name="Authority References",
            component_type="authority",
            weight=1.0,
            enabled=True,
            minimum_threshold=None,
            maximum_threshold=None,
            applies_to_decision_types=("all",),
            description="Authority facts remain visible and cannot be overridden.",
            metadata={"visible": True},
        ),
        WeightComponent(
            component_id="measured-metric",
            component_name="Measured Metrics",
            component_type="measured_metric",
            weight=1.0,
            enabled=True,
            minimum_threshold=0.0,
            maximum_threshold=1.0,
            applies_to_decision_types=("all",),
            description="Measured evidence is the primary weighted signal.",
            metadata={"visible": True},
        ),
        WeightComponent(
            component_id="source-agreement",
            component_name="Source Agreement",
            component_type="source_agreement",
            weight=1.0,
            enabled=True,
            minimum_threshold=0.0,
            maximum_threshold=1.0,
            applies_to_decision_types=("all",),
            description="Source agreement affects confidence.",
            metadata={"visible": True},
        ),
        WeightComponent(
            component_id="tournament-performance",
            component_name="Tournament Performance",
            component_type="tournament_performance",
            weight=tournament_weight,
            enabled=True,
            minimum_threshold=0.0,
            maximum_threshold=1.0,
            applies_to_decision_types=("all",),
            description="Tournament performance remains measured evidence.",
            metadata={"visible": True},
        ),
        WeightComponent(
            component_id="simulator-comparison",
            component_name="Simulator Comparison",
            component_type="simulator_comparison",
            weight=simulator_weight,
            enabled=True,
            minimum_threshold=0.0,
            maximum_threshold=1.0,
            applies_to_decision_types=("all",),
            description="Simulator comparisons remain simulator evidence only.",
            metadata={"simulator_only": True, "visible": True},
        ),
        WeightComponent(
            component_id="primer-context",
            component_name="Primer Context",
            component_type="primer_context",
            weight=primer_weight,
            enabled=True,
            minimum_threshold=None,
            maximum_threshold=None,
            applies_to_decision_types=("all",),
            description="Primer context is explanatory and cannot override measured evidence.",
            metadata={"explanatory_only": True, "visible": True},
        ),
        WeightComponent(
            component_id="user-context",
            component_name="User Context",
            component_type="user_context",
            weight=user_weight,
            enabled=user_weight > 0,
            minimum_threshold=None,
            maximum_threshold=None,
            applies_to_decision_types=("all",),
            description="Generic user-context sensitivity; user-specific overlays require a future contract.",
            metadata={"generic_only": True, "visible": True},
        ),
        WeightComponent(
            component_id="caveat-penalty",
            component_name="Caveat Penalty",
            component_type="caveat_penalty",
            weight=-0.5,
            enabled=True,
            minimum_threshold=None,
            maximum_threshold=None,
            applies_to_decision_types=("all",),
            description="Caveat penalties remain visible.",
            metadata={"visible": True},
        ),
        WeightComponent(
            component_id="conflict-penalty",
            component_name="Conflict Penalty",
            component_type="conflict_penalty",
            weight=-0.75,
            enabled=True,
            minimum_threshold=None,
            maximum_threshold=None,
            applies_to_decision_types=("all",),
            description="Conflict penalties remain visible.",
            metadata={"visible": True},
        ),
    )
    return build_weight_profile(
        profile_id=profile_id,
        profile_name=profile_id,
        profile_version="1.0.0",
        profile_label=label,
        profile_description=description,
        components=components,
        normalization_rule="none",
        minimum_confidence=0.25,
        minimum_coverage_ratio=0.1,
        minimum_sample_size=1,
        generated_at=GENERATED_AT,
        analysis_version=ANALYSIS_VERSION,
        metadata={"default_profile": True},
    )
