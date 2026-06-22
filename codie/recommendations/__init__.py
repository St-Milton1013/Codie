"""Recommendation statistics primitives."""

from .evidence import (
    EvidenceBundle,
    EvidenceItem,
    EvidenceStackSummary,
    build_evidence_bundle,
    evidence_stack_summary,
    validate_claim_text,
)
from .observations import staple_observations_from_canonical_rows
from .statistics import (
    ConfidenceRating,
    FrequencyStats,
    GenericStapleProfile,
    clamp,
    confidence_rating,
    frequency_stats,
    generic_staple_profile,
    inclusion_rate,
    jaccard_similarity,
    lift_score,
    safe_rate,
    weighted_inclusion_rate,
    weighted_jaccard_similarity,
)
from .staples import (
    CommanderStaplesReport,
    StapleObservation,
    StapleReportRow,
    build_commander_staples_report,
)

__all__ = [
    "ConfidenceRating",
    "CommanderStaplesReport",
    "EvidenceBundle",
    "EvidenceItem",
    "EvidenceStackSummary",
    "FrequencyStats",
    "GenericStapleProfile",
    "StapleObservation",
    "StapleReportRow",
    "build_evidence_bundle",
    "build_commander_staples_report",
    "clamp",
    "confidence_rating",
    "evidence_stack_summary",
    "frequency_stats",
    "generic_staple_profile",
    "inclusion_rate",
    "jaccard_similarity",
    "lift_score",
    "safe_rate",
    "staple_observations_from_canonical_rows",
    "validate_claim_text",
    "weighted_inclusion_rate",
    "weighted_jaccard_similarity",
]
