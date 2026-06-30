"""Read-only reviewed simulator accuracy summaries."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from codie.db.repositories.simulation import SimulationRepository


@dataclass(frozen=True)
class ReviewedAccuracyFilters:
    deck_hash: str | None = None
    target_card: str | None = None
    batch_id: str | None = None
    challenge_id: str | None = None
    trace_id: str | int | None = None
    review_status: str | None = None
    review_reason: str | None = None
    created_at_from: str | None = None
    created_at_to: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "deck_hash": self.deck_hash,
            "target_card": self.target_card,
            "batch_id": self.batch_id,
            "challenge_id": self.challenge_id,
            "trace_id": self.trace_id,
            "review_status": self.review_status,
            "review_reason": self.review_reason,
            "created_at_from": self.created_at_from,
            "created_at_to": self.created_at_to,
        }

    def active_dict(self) -> dict[str, Any]:
        return {key: value for key, value in self.to_dict().items() if value not in (None, "")}


@dataclass(frozen=True)
class ReviewStatusCount:
    review_status: str
    count: int

    def to_dict(self) -> dict[str, Any]:
        return {"review_status": self.review_status, "count": self.count}


@dataclass(frozen=True)
class ReviewReasonCount:
    review_reason: str
    count: int

    def to_dict(self) -> dict[str, Any]:
        return {"review_reason": self.review_reason, "count": self.count}


@dataclass(frozen=True)
class ReviewedAccuracySummary:
    total_reviews: int
    reviewed_success_count: int
    accepted_success_count: int
    rejected_success_count: int
    reviewed_failure_count: int
    reviewed_unsupported_count: int
    accepted_failure_count: int
    rejected_failure_count: int
    status_counts: tuple[ReviewStatusCount, ...]
    reason_counts: tuple[ReviewReasonCount, ...]
    affected_card_counts: tuple[tuple[str, int], ...]
    affected_action_counts: tuple[tuple[str, int], ...]
    filters: ReviewedAccuracyFilters
    generated_at: str

    @property
    def accepted_success_rate(self) -> float | None:
        return _rate(self.accepted_success_count, self.reviewed_success_count)

    @property
    def rejected_success_rate(self) -> float | None:
        return _rate(self.rejected_success_count, self.reviewed_success_count)

    @property
    def unsupported_rate(self) -> float | None:
        return _rate(self.reviewed_unsupported_count, self.total_reviews)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_reviews": self.total_reviews,
            "reviewed_success_count": self.reviewed_success_count,
            "accepted_success_count": self.accepted_success_count,
            "rejected_success_count": self.rejected_success_count,
            "reviewed_failure_count": self.reviewed_failure_count,
            "reviewed_unsupported_count": self.reviewed_unsupported_count,
            "accepted_failure_count": self.accepted_failure_count,
            "rejected_failure_count": self.rejected_failure_count,
            "status_counts": [item.to_dict() for item in self.status_counts],
            "reason_counts": [item.to_dict() for item in self.reason_counts],
            "affected_card_counts": [{"value": key, "count": count} for key, count in self.affected_card_counts],
            "affected_action_counts": [{"value": key, "count": count} for key, count in self.affected_action_counts],
            "accepted_success_rate": self.accepted_success_rate,
            "rejected_success_rate": self.rejected_success_rate,
            "unsupported_rate": self.unsupported_rate,
            "filters": self.filters.to_dict(),
            "generated_at": self.generated_at,
        }


def build_reviewed_accuracy_summary(
    repository: SimulationRepository,
    filters: ReviewedAccuracyFilters | None = None,
    *,
    generated_at: str | None = None,
) -> ReviewedAccuracySummary:
    active_filters = filters or ReviewedAccuracyFilters()
    rows = repository.list_line_reviews_for_accuracy(active_filters.active_dict())
    return summarize_line_review_rows(rows, filters=active_filters, generated_at=generated_at or repository.now())


def summarize_line_review_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    filters: ReviewedAccuracyFilters | None = None,
    generated_at: str,
) -> ReviewedAccuracySummary:
    row_list = list(rows)
    status_counter: Counter[str] = Counter()
    reason_counter: Counter[str] = Counter()
    affected_card_counter: Counter[str] = Counter()
    affected_action_counter: Counter[str] = Counter()
    accepted_success = 0
    rejected_success = 0
    reviewed_failure = 0
    reviewed_unsupported = 0
    accepted_failure = 0
    rejected_failure = 0

    for row in row_list:
        review_status = str(row["review_status"])
        review_reason = str(row["review_reason"])
        simulator_status = str(row["simulator_status"])
        simulator_success = bool(row["simulator_success"])
        status_counter[review_status] += 1
        reason_counter[review_reason] += 1
        affected_card_counter.update(_json_list(row["affected_cards_json"]))
        affected_action_counter.update(_json_list(row["affected_actions_json"]))
        if simulator_status == "unsupported":
            reviewed_unsupported += 1
        elif simulator_success:
            if review_status == "accepted":
                accepted_success += 1
            else:
                rejected_success += 1
        else:
            reviewed_failure += 1
            if review_status == "accepted":
                accepted_failure += 1
            else:
                rejected_failure += 1

    reviewed_success = accepted_success + rejected_success
    return ReviewedAccuracySummary(
        total_reviews=len(row_list),
        reviewed_success_count=reviewed_success,
        accepted_success_count=accepted_success,
        rejected_success_count=rejected_success,
        reviewed_failure_count=reviewed_failure,
        reviewed_unsupported_count=reviewed_unsupported,
        accepted_failure_count=accepted_failure,
        rejected_failure_count=rejected_failure,
        status_counts=_status_counts(status_counter),
        reason_counts=_reason_counts(reason_counter),
        affected_card_counts=_counter_counts(affected_card_counter),
        affected_action_counts=_counter_counts(affected_action_counter),
        filters=filters or ReviewedAccuracyFilters(),
        generated_at=generated_at,
    )


def _json_list(value: Any) -> list[str]:
    if value in (None, ""):
        return []
    return [str(item) for item in json.loads(str(value))]


def _status_counts(counter: Counter[str]) -> tuple[ReviewStatusCount, ...]:
    return tuple(ReviewStatusCount(key, count) for key, count in sorted(counter.items()))


def _reason_counts(counter: Counter[str]) -> tuple[ReviewReasonCount, ...]:
    return tuple(ReviewReasonCount(key, count) for key, count in sorted(counter.items()))


def _counter_counts(counter: Counter[str]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return numerator / denominator
