"""Persistence adapter for Challenge Line Review annotations."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from codie.db.repositories.simulation import SimulationRepository

from .line_review import LineReviewAnnotation


@dataclass(frozen=True)
class PersistedLineReview:
    review_id: str
    challenge_id: str
    batch_id: str | None = None
    result_id: int | None = None
    trace_id: int | None = None

    def __post_init__(self) -> None:
        if not self.review_id:
            raise ValueError("review_id is required")
        if not self.challenge_id:
            raise ValueError("challenge_id is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "challenge_id": self.challenge_id,
            "batch_id": self.batch_id,
            "result_id": self.result_id,
            "trace_id": self.trace_id,
        }


def persist_line_review_annotation(
    repository: SimulationRepository,
    annotation: LineReviewAnnotation,
) -> PersistedLineReview:
    row = line_review_annotation_to_repository_row(annotation)
    with repository.transaction(repository.connection, "simulation_line_review"):
        review_id = repository.upsert_line_review(row)
    return PersistedLineReview(
        review_id=review_id,
        challenge_id=annotation.challenge_id,
        batch_id=annotation.batch_id,
        result_id=_optional_int(annotation.result_id),
        trace_id=_optional_int(annotation.trace_id),
    )


def line_review_annotation_to_repository_row(annotation: LineReviewAnnotation) -> dict[str, Any]:
    return {
        "review_id": annotation.review_id,
        "challenge_id": annotation.challenge_id,
        "batch_id": annotation.batch_id,
        "result_id": _optional_int(annotation.result_id),
        "trace_id": _optional_int(annotation.trace_id),
        "deck_hash": annotation.deck_hash,
        "target_card": annotation.target_card,
        "target_turn": annotation.target_turn,
        "simulator_success": 1 if annotation.simulator_success else 0,
        "simulator_status": annotation.simulator_status,
        "action_trace_json": _json(annotation.action_trace),
        "review_status": annotation.review_status,
        "review_reason": annotation.review_reason,
        "review_note": annotation.review_note,
        "affected_cards_json": _json(list(annotation.affected_cards)),
        "affected_actions_json": _json(list(annotation.affected_actions)),
        "created_at": annotation.created_at,
    }


def line_review_repository_row_to_annotation(row: Mapping[str, Any]) -> LineReviewAnnotation:
    return LineReviewAnnotation(
        review_id=str(row["review_id"]),
        challenge_id=str(row["challenge_id"]),
        deck_hash=str(row["deck_hash"]),
        target_card=str(row["target_card"]),
        target_turn=int(row["target_turn"]),
        simulator_success=bool(row["simulator_success"]),
        simulator_status=str(row["simulator_status"]),
        action_trace=json.loads(str(row["action_trace_json"])),
        review_status=str(row["review_status"]),
        review_reason=str(row["review_reason"]),
        review_note=row["review_note"],
        affected_cards=tuple(json.loads(str(row["affected_cards_json"]))),
        affected_actions=tuple(json.loads(str(row["affected_actions_json"]))),
        created_at=str(row["created_at"]),
        batch_id=row["batch_id"],
        result_id=_optional_str(row["result_id"]),
        trace_id=_optional_str(row["trace_id"]),
    )


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _optional_str(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value)
