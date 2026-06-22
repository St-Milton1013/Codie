"""In-memory recommendation candidate generation orchestration."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .evidence import EvidenceItem, build_evidence_bundle
from .reports import CandidateAuditReport, build_candidate_audit_report
from .scoring import (
    RecommendationCandidateDraft,
    RecommendationScoreInput,
    build_recommendation_candidate_draft,
    low_sample_penalty,
)
from .staples import CommanderStaplesReport, StapleReportRow


@dataclass(frozen=True)
class RecommendationGenerationConfig:
    generated_at: str
    time_window: str
    minimum_sample_size: int = 10
    candidate_type: str = "commander_specific"
    entity_type: str = "card"

    def __post_init__(self) -> None:
        _require_text(self.generated_at, "generated_at")
        _require_text(self.time_window, "time_window")
        _require_text(self.candidate_type, "candidate_type")
        _require_text(self.entity_type, "entity_type")
        if not isinstance(self.minimum_sample_size, int):
            raise TypeError("minimum_sample_size must be an integer")
        if self.minimum_sample_size <= 0:
            raise ValueError("minimum_sample_size must be greater than zero")


@dataclass(frozen=True)
class RecommendationCandidateSource:
    oracle_id: str
    card_name: str
    sample_size: int
    inclusion_rate: float | None
    commander_lift: float | None = None
    similarity_score: float = 0.0
    tournament_performance_score: float = 0.0
    generic_staple_penalty: float = 0.0
    scryfall_id: str | None = None
    source_record_id: str | None = None
    source_url: str | None = None
    source_name: str = "canonical recommendation analytics"
    source_type: str = "analytics"
    metric_unit: str = "inclusion"
    formula: str = "included comparable decks / total comparable decks"

    def __post_init__(self) -> None:
        _require_text(self.oracle_id, "oracle_id")
        _require_text(self.card_name, "card_name")
        _require_text(self.source_name, "source_name")
        _require_text(self.source_type, "source_type")
        _require_text(self.metric_unit, "metric_unit")
        _require_text(self.formula, "formula")
        if not isinstance(self.sample_size, int):
            raise TypeError("sample_size must be an integer")
        if self.sample_size < 0:
            raise ValueError("sample_size must be non-negative")
        for name in (
            "inclusion_rate",
            "commander_lift",
            "similarity_score",
            "tournament_performance_score",
            "generic_staple_penalty",
        ):
            value = getattr(self, name)
            if value is None:
                continue
            if value < 0:
                raise ValueError(f"{name} must be non-negative")
        for name in ("inclusion_rate", "similarity_score"):
            value = getattr(self, name)
            if value is not None and value > 1:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.source_url in (None, "") and self.source_record_id in (None, ""):
            raise ValueError("source_url or source_record_id is required")


@dataclass(frozen=True)
class RecommendationCandidatePacket:
    candidate: RecommendationCandidateDraft
    audit: CandidateAuditReport


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _score_from_rate(value: float | None) -> float:
    return 0.0 if value is None else float(value)


def _claim_text(source: RecommendationCandidateSource, config: RecommendationGenerationConfig) -> str:
    rate = "unknown" if source.inclusion_rate is None else f"{source.inclusion_rate:.1%}"
    return (
        f"{source.card_name} appeared in {rate} of comparable canonical decks "
        f"in the {config.time_window} window."
    )


def build_candidate_packet(
    *,
    source: RecommendationCandidateSource,
    config: RecommendationGenerationConfig,
) -> RecommendationCandidatePacket:
    """Build one in-memory recommendation candidate and audit report."""
    metric_value = _score_from_rate(source.inclusion_rate)
    evidence_item = EvidenceItem(
        claim_type="canonical_inclusion",
        claim_text=_claim_text(source, config),
        source_type=source.source_type,
        source_name=source.source_name,
        source_url=source.source_url,
        source_record_id=source.source_record_id,
        metric_value=metric_value,
        metric_unit=source.metric_unit,
        sample_size=source.sample_size,
        confidence=min(1.0, source.sample_size / 100),
        recency_window=config.time_window,
        generated_at=config.generated_at,
        reproducibility_notes="Generated from canonical recommendation input records only.",
        formula=source.formula,
    )
    evidence = build_evidence_bundle(
        entity_type=config.entity_type,
        entity_id=source.oracle_id,
        items=(evidence_item,),
        generated_at=config.generated_at,
    )
    score_input = RecommendationScoreInput(
        entity_type=config.entity_type,
        entity_id=source.oracle_id,
        candidate_type=config.candidate_type,
        sample_size=source.sample_size,
        commander_lift_score=_score_from_rate(source.commander_lift),
        inclusion_rate_score=metric_value,
        similarity_score=source.similarity_score,
        tournament_performance_score=source.tournament_performance_score,
        generic_staple_penalty=source.generic_staple_penalty,
        low_sample_penalty=low_sample_penalty(source.sample_size, threshold=config.minimum_sample_size),
    )
    candidate = build_recommendation_candidate_draft(
        score_input=score_input,
        evidence=evidence,
        generated_at=config.generated_at,
    )
    return RecommendationCandidatePacket(
        candidate=candidate,
        audit=build_candidate_audit_report(
            candidate,
            generated_at=config.generated_at,
            minimum_ranked_sample_size=config.minimum_sample_size,
        ),
    )


def generate_candidate_packets(
    *,
    sources: Iterable[RecommendationCandidateSource],
    config: RecommendationGenerationConfig,
) -> tuple[RecommendationCandidatePacket, ...]:
    packets = tuple(build_candidate_packet(source=source, config=config) for source in sources)
    return tuple(
        sorted(
            packets,
            key=lambda packet: (
                not packet.audit.rank_eligible,
                -packet.candidate.score.recommendation_score,
                packet.candidate.entity_id,
            ),
        )
    )


def candidate_sources_from_staples_report(
    report: CommanderStaplesReport,
    *,
    source_name: str = "commander staples report",
) -> tuple[RecommendationCandidateSource, ...]:
    """Convert a commander staples report into candidate-generation sources."""
    return tuple(
        _source_from_staple_row(row, report=report, source_name=source_name)
        for row in report.rows
    )


def _source_from_staple_row(
    row: StapleReportRow,
    *,
    report: CommanderStaplesReport,
    source_name: str,
) -> RecommendationCandidateSource:
    source_record_id = (
        f"commander_staples:{report.commander_signature}:"
        f"{report.time_window}:{row.oracle_id}"
    )
    return RecommendationCandidateSource(
        oracle_id=row.oracle_id,
        scryfall_id=row.scryfall_id,
        card_name=row.card_name,
        sample_size=row.total_matching_decks,
        inclusion_rate=row.inclusion_percentage,
        tournament_performance_score=_tournament_performance_score(row),
        source_record_id=source_record_id,
        source_name=source_name,
        formula="matching decks containing card / total matching commander decks",
    )


def _tournament_performance_score(row: StapleReportRow) -> float:
    if row.matching_deck_count <= 0:
        return 0.0
    topcut_rate = row.top16_count / row.matching_deck_count
    winner_bonus = min(0.25, row.winner_count * 0.05)
    return min(1.0, topcut_rate + winner_bonus)
