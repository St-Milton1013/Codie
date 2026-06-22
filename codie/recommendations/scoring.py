"""Deterministic recommendation candidate scoring drafts."""

from __future__ import annotations

from dataclasses import dataclass

from .evidence import EvidenceBundle
from .statistics import confidence_rating


SCORE_FORMULA = (
    "commander_lift_score + inclusion_rate_score + confidence_score + similarity_score + "
    "package_completion_score + combo_completion_score + tournament_performance_score + "
    "simulation_delta_score - generic_staple_penalty - low_sample_penalty"
)

POSITIVE_COMPONENTS = (
    "commander_lift_score",
    "inclusion_rate_score",
    "confidence_score",
    "similarity_score",
    "package_completion_score",
    "combo_completion_score",
    "tournament_performance_score",
    "simulation_delta_score",
)

PENALTY_COMPONENTS = (
    "generic_staple_penalty",
    "low_sample_penalty",
)

ALLOWED_CANDIDATE_TYPES = frozenset(
    {
        "commander_specific",
        "source_label_specific",
        "package_specific",
        "combo_completion",
        "generic_staple",
        "meta_tech",
        "budget_replacement",
        "upgrade_candidate",
        "low_evidence_card",
        "outlier_card",
    }
)


@dataclass(frozen=True)
class ScoreComponent:
    name: str
    value: float
    role: str

    def __post_init__(self) -> None:
        _require_text(self.name, "name")
        if self.role not in {"add", "subtract"}:
            raise ValueError("role must be add or subtract")
        _require_non_negative(self.value, self.name)


@dataclass(frozen=True)
class RecommendationScoreInput:
    entity_type: str
    entity_id: str
    candidate_type: str
    sample_size: int
    commander_lift_score: float = 0.0
    inclusion_rate_score: float = 0.0
    confidence_score: float | None = None
    similarity_score: float = 0.0
    package_completion_score: float = 0.0
    combo_completion_score: float = 0.0
    tournament_performance_score: float = 0.0
    simulation_delta_score: float = 0.0
    generic_staple_penalty: float = 0.0
    low_sample_penalty: float = 0.0

    def __post_init__(self) -> None:
        _require_text(self.entity_type, "entity_type")
        _require_text(self.entity_id, "entity_id")
        object.__setattr__(self, "candidate_type", normalize_candidate_type(self.candidate_type))
        if not isinstance(self.sample_size, int):
            raise TypeError("sample_size must be an integer")
        _require_non_negative(self.sample_size, "sample_size")
        for name in POSITIVE_COMPONENTS:
            value = getattr(self, name)
            if value is None:
                continue
            _require_non_negative(value, name)
        for name in PENALTY_COMPONENTS:
            _require_non_negative(getattr(self, name), name)
        for name in ("inclusion_rate_score", "similarity_score"):
            _require_unit_interval(getattr(self, name), name)
        if self.confidence_score is not None:
            _require_unit_interval(self.confidence_score, "confidence_score")


@dataclass(frozen=True)
class RecommendationScoreBreakdown:
    recommendation_score: float
    positive_total: float
    penalty_total: float
    components: tuple[ScoreComponent, ...]
    formula: str
    sample_size: int
    confidence_label: str

    def __post_init__(self) -> None:
        _require_text(self.formula, "formula")
        if not isinstance(self.sample_size, int):
            raise TypeError("sample_size must be an integer")
        _require_non_negative(self.sample_size, "sample_size")
        expected = self.positive_total - self.penalty_total
        if abs(self.recommendation_score - expected) > 1e-9:
            raise ValueError("recommendation_score must equal positive_total minus penalty_total")


@dataclass(frozen=True)
class RecommendationCandidateDraft:
    entity_type: str
    entity_id: str
    candidate_type: str
    score: RecommendationScoreBreakdown
    evidence: EvidenceBundle
    generated_at: str

    def __post_init__(self) -> None:
        _require_text(self.generated_at, "generated_at")
        _require_text(self.entity_type, "entity_type")
        _require_text(self.entity_id, "entity_id")
        object.__setattr__(self, "candidate_type", normalize_candidate_type(self.candidate_type))
        if self.evidence.entity_type != self.entity_type or self.evidence.entity_id != self.entity_id:
            raise ValueError("evidence bundle identity must match candidate identity")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _require_non_negative(value: float, field_name: str) -> None:
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative")


def _require_unit_interval(value: float, field_name: str) -> None:
    if value < 0 or value > 1:
        raise ValueError(f"{field_name} must be between 0 and 1")


def normalize_candidate_type(candidate_type: str) -> str:
    _require_text(candidate_type, "candidate_type")
    normalized = candidate_type.strip().lower().replace("-", "_")
    if normalized not in ALLOWED_CANDIDATE_TYPES:
        raise ValueError(f"unsupported candidate_type: {candidate_type}")
    return normalized


def low_sample_penalty(sample_size: int, *, threshold: int = 10, penalty: float = 0.25) -> float:
    if not isinstance(sample_size, int) or not isinstance(threshold, int):
        raise TypeError("sample_size and threshold must be integers")
    _require_non_negative(sample_size, "sample_size")
    _require_non_negative(threshold, "threshold")
    _require_non_negative(penalty, "penalty")
    if threshold == 0:
        raise ValueError("threshold must be greater than zero")
    return penalty if sample_size < threshold else 0.0


def score_recommendation_candidate(score_input: RecommendationScoreInput) -> RecommendationScoreBreakdown:
    confidence = score_input.confidence_score
    rating = confidence_rating(score_input.sample_size)
    if confidence is None:
        confidence = rating.score

    values = {
        "commander_lift_score": score_input.commander_lift_score,
        "inclusion_rate_score": score_input.inclusion_rate_score,
        "confidence_score": confidence,
        "similarity_score": score_input.similarity_score,
        "package_completion_score": score_input.package_completion_score,
        "combo_completion_score": score_input.combo_completion_score,
        "tournament_performance_score": score_input.tournament_performance_score,
        "simulation_delta_score": score_input.simulation_delta_score,
        "generic_staple_penalty": score_input.generic_staple_penalty,
        "low_sample_penalty": score_input.low_sample_penalty,
    }
    components = tuple(
        ScoreComponent(name=name, value=float(values[name]), role="add")
        for name in POSITIVE_COMPONENTS
    ) + tuple(
        ScoreComponent(name=name, value=float(values[name]), role="subtract")
        for name in PENALTY_COMPONENTS
    )
    positive_total = sum(component.value for component in components if component.role == "add")
    penalty_total = sum(component.value for component in components if component.role == "subtract")
    return RecommendationScoreBreakdown(
        recommendation_score=positive_total - penalty_total,
        positive_total=positive_total,
        penalty_total=penalty_total,
        components=components,
        formula=SCORE_FORMULA,
        sample_size=score_input.sample_size,
        confidence_label=rating.label,
    )


def build_recommendation_candidate_draft(
    *,
    score_input: RecommendationScoreInput,
    evidence: EvidenceBundle,
    generated_at: str,
) -> RecommendationCandidateDraft:
    return RecommendationCandidateDraft(
        entity_type=score_input.entity_type,
        entity_id=score_input.entity_id,
        candidate_type=score_input.candidate_type,
        score=score_recommendation_candidate(score_input),
        evidence=evidence,
        generated_at=generated_at,
    )
