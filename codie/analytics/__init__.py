"""Deterministic analytics built from canonical Codie records."""

from .foundations import AnalyticsBuildResult, AnalyticsFoundationBuilder
from .innovation import (
    InnovationFilter,
    InnovationObservation,
    InnovationSignal,
    detect_innovations,
    detect_innovations_from_repository,
    innovation_observations_from_rows,
    innovation_evidence_line,
)
from .weights import (
    AnalyticsError,
    decklist_completeness_weight,
    event_size_weight,
    final_entry_weight,
    normalize_time_window,
    placement_weight,
    recency_weight,
    source_confidence_weight,
)

__all__ = [
    "AnalyticsBuildResult",
    "AnalyticsError",
    "AnalyticsFoundationBuilder",
    "InnovationFilter",
    "InnovationObservation",
    "InnovationSignal",
    "detect_innovations",
    "detect_innovations_from_repository",
    "decklist_completeness_weight",
    "event_size_weight",
    "final_entry_weight",
    "innovation_evidence_line",
    "innovation_observations_from_rows",
    "normalize_time_window",
    "placement_weight",
    "recency_weight",
    "source_confidence_weight",
]
