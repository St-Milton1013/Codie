"""Deterministic analytics built from canonical Codie records."""

from .foundations import AnalyticsBuildResult, AnalyticsFoundationBuilder
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
    "decklist_completeness_weight",
    "event_size_weight",
    "final_entry_weight",
    "normalize_time_window",
    "placement_weight",
    "recency_weight",
    "source_confidence_weight",
]
