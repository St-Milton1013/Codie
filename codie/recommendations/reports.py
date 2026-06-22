"""Validation and source-attributed reports for candidate drafts."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .evidence import evidence_stack_summary, validate_claim_text
from .scoring import RecommendationCandidateDraft


@dataclass(frozen=True)
class CandidateAuditIssue:
    severity: str
    code: str
    message: str

    def __post_init__(self) -> None:
        if self.severity not in {"error", "warning"}:
            raise ValueError("severity must be error or warning")
        _require_text(self.code, "code")
        _require_text(self.message, "message")


@dataclass(frozen=True)
class CandidateAuditReport:
    entity_type: str
    entity_id: str
    candidate_type: str
    recommendation_score: float
    rank_eligible: bool
    evidence_count: int
    source_type_counts: dict[str, int]
    explanation_lines: tuple[str, ...]
    issues: tuple[CandidateAuditIssue, ...]
    generated_at: str
    formula: str

    @property
    def is_valid(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _format_metric(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def validate_candidate_explanation_lines(lines: Iterable[str]) -> tuple[str, ...]:
    cleaned = tuple(validate_claim_text(line) for line in lines)
    if not cleaned:
        raise ValueError("at least one explanation line is required")
    return cleaned


def candidate_explanation_lines(candidate: RecommendationCandidateDraft) -> tuple[str, ...]:
    lines = [
        f"Score {_format_metric(candidate.score.recommendation_score)} from formula: {candidate.score.formula}.",
    ]
    for item in candidate.evidence.items:
        source_ref = item.source_url or f"record {item.source_record_id}"
        formula = f" Formula: {item.formula}." if item.formula else ""
        lines.append(
            f"{item.claim_text} Source: {item.source_name} ({item.source_type}) {source_ref}. "
            f"Metric: {_format_metric(item.metric_value)} {item.metric_unit}; "
            f"sample size {item.sample_size}; confidence {_format_metric(item.confidence)}.{formula}"
        )
    return validate_candidate_explanation_lines(lines)


def build_candidate_audit_report(
    candidate: RecommendationCandidateDraft,
    *,
    generated_at: str,
    minimum_ranked_sample_size: int = 10,
) -> CandidateAuditReport:
    _require_text(generated_at, "generated_at")
    if not isinstance(minimum_ranked_sample_size, int):
        raise TypeError("minimum_ranked_sample_size must be an integer")
    if minimum_ranked_sample_size <= 0:
        raise ValueError("minimum_ranked_sample_size must be greater than zero")

    issues: list[CandidateAuditIssue] = []
    if candidate.score.sample_size < minimum_ranked_sample_size:
        issues.append(
            CandidateAuditIssue(
                severity="warning",
                code="low_sample_size",
                message="Candidate is anecdotal until the ranked sample-size threshold is met.",
            )
        )
    if candidate.evidence.entity_type != candidate.entity_type or candidate.evidence.entity_id != candidate.entity_id:
        issues.append(
            CandidateAuditIssue(
                severity="error",
                code="evidence_identity_mismatch",
                message="Evidence bundle identity does not match candidate identity.",
            )
        )

    summary = evidence_stack_summary(candidate.evidence)
    rank_eligible = not issues and candidate.score.sample_size >= minimum_ranked_sample_size
    return CandidateAuditReport(
        entity_type=candidate.entity_type,
        entity_id=candidate.entity_id,
        candidate_type=candidate.candidate_type,
        recommendation_score=candidate.score.recommendation_score,
        rank_eligible=rank_eligible,
        evidence_count=summary.total_evidence_count,
        source_type_counts=summary.source_type_counts,
        explanation_lines=candidate_explanation_lines(candidate),
        issues=tuple(issues),
        generated_at=generated_at,
        formula=candidate.score.formula,
    )
