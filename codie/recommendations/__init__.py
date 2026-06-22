"""Recommendation statistics primitives."""

from .evidence import (
    EvidenceBundle,
    EvidenceItem,
    EvidenceStackSummary,
    build_evidence_bundle,
    evidence_stack_summary,
    validate_claim_text,
)
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

__all__ = [
    "ConfidenceRating",
    "EvidenceBundle",
    "EvidenceItem",
    "EvidenceStackSummary",
    "FrequencyStats",
    "GenericStapleProfile",
    "build_evidence_bundle",
    "clamp",
    "confidence_rating",
    "evidence_stack_summary",
    "frequency_stats",
    "generic_staple_profile",
    "inclusion_rate",
    "jaccard_similarity",
    "lift_score",
    "safe_rate",
    "validate_claim_text",
    "weighted_inclusion_rate",
    "weighted_jaccard_similarity",
]
