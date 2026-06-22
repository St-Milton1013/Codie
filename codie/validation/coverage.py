"""Canonical coverage report helpers."""

from __future__ import annotations

from dataclasses import dataclass

from codie.db.repositories.validation import ValidationRepository


@dataclass(frozen=True)
class CanonicalCoverageReport:
    source_event_count: int
    canonical_event_count: int
    canonicalized_source_event_count: int
    pending_source_event_count: int
    unresolved_source_event_count: int
    canonical_event_source_link_count: int
    source_deck_count: int
    canonical_deck_count: int
    canonicalized_source_deck_count: int
    pending_source_deck_count: int
    unresolved_source_deck_count: int
    canonical_deck_source_link_count: int
    event_canonicalization_rate: float
    deck_canonicalization_rate: float
    event_merge_rate: float
    deck_merge_rate: float
    unresolved_deck_rate: float


def _rate(numerator: int, denominator: int) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _merge_rate(canonicalized_source_count: int, canonical_count: int) -> float:
    if canonicalized_source_count == 0:
        return 0.0
    merged_count = max(canonicalized_source_count - canonical_count, 0)
    return merged_count / canonicalized_source_count


def build_canonical_coverage_report(repository: ValidationRepository) -> CanonicalCoverageReport:
    counts = repository.canonical_coverage_counts()
    source_event_count = int(counts["source_event_count"])
    canonicalized_source_event_count = int(counts["canonicalized_source_event_count"])
    canonical_event_count = int(counts["canonical_event_count"])
    source_deck_count = int(counts["source_deck_count"])
    canonicalized_source_deck_count = int(counts["canonicalized_source_deck_count"])
    canonical_deck_count = int(counts["canonical_deck_count"])
    unresolved_source_deck_count = int(counts["unresolved_source_deck_count"])
    return CanonicalCoverageReport(
        source_event_count=source_event_count,
        canonical_event_count=canonical_event_count,
        canonicalized_source_event_count=canonicalized_source_event_count,
        pending_source_event_count=int(counts["pending_source_event_count"]),
        unresolved_source_event_count=int(counts["unresolved_source_event_count"]),
        canonical_event_source_link_count=int(counts["canonical_event_source_link_count"]),
        source_deck_count=source_deck_count,
        canonical_deck_count=canonical_deck_count,
        canonicalized_source_deck_count=canonicalized_source_deck_count,
        pending_source_deck_count=int(counts["pending_source_deck_count"]),
        unresolved_source_deck_count=unresolved_source_deck_count,
        canonical_deck_source_link_count=int(counts["canonical_deck_source_link_count"]),
        event_canonicalization_rate=_rate(canonicalized_source_event_count, source_event_count),
        deck_canonicalization_rate=_rate(canonicalized_source_deck_count, source_deck_count),
        event_merge_rate=_merge_rate(canonicalized_source_event_count, canonical_event_count),
        deck_merge_rate=_merge_rate(canonicalized_source_deck_count, canonical_deck_count),
        unresolved_deck_rate=_rate(unresolved_source_deck_count, source_deck_count),
    )
