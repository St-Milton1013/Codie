"""Immutable review annotations for Challenge Mode simulator lines."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .challenge_mode import ChallengeResult


class LineReviewStatus:
    ACCEPTED = "accepted"
    INCORRECT = "incorrect"
    UNREALISTIC = "unrealistic"
    UNSUPPORTED_CARD_BEHAVIOR = "unsupported_card_behavior"
    BAD_SEQUENCING = "bad_sequencing"
    MANA_MODELING_ERROR = "mana_modeling_error"
    TUTOR_SEARCH_ERROR = "tutor_search_error"
    OTHER = "other"

    ALL = (
        ACCEPTED,
        INCORRECT,
        UNREALISTIC,
        UNSUPPORTED_CARD_BEHAVIOR,
        BAD_SEQUENCING,
        MANA_MODELING_ERROR,
        TUTOR_SEARCH_ERROR,
        OTHER,
    )
    REJECTED = (
        INCORRECT,
        UNREALISTIC,
        UNSUPPORTED_CARD_BEHAVIOR,
        BAD_SEQUENCING,
        MANA_MODELING_ERROR,
        TUTOR_SEARCH_ERROR,
        OTHER,
    )


class LineReviewReason:
    LINE_VALID = "line_valid"
    ILLEGAL_ACTION = "illegal_action"
    UNSUPPORTED_CARD_BEHAVIOR = "unsupported_card_behavior"
    IMPRACTICAL_SEQUENCE = "impractical_sequence"
    MANA_POOL_ERROR = "mana_pool_error"
    MANA_SOURCE_ERROR = "mana_source_error"
    TUTOR_TARGET_ERROR = "tutor_target_error"
    SEARCH_ZONE_ERROR = "search_zone_error"
    MISSING_COST = "missing_cost"
    WRONG_TIMING = "wrong_timing"
    UNKNOWN_ISSUE = "unknown_issue"

    ALL = (
        LINE_VALID,
        ILLEGAL_ACTION,
        UNSUPPORTED_CARD_BEHAVIOR,
        IMPRACTICAL_SEQUENCE,
        MANA_POOL_ERROR,
        MANA_SOURCE_ERROR,
        TUTOR_TARGET_ERROR,
        SEARCH_ZONE_ERROR,
        MISSING_COST,
        WRONG_TIMING,
        UNKNOWN_ISSUE,
    )


@dataclass(frozen=True)
class LineReviewAnnotation:
    review_id: str
    challenge_id: str
    deck_hash: str
    target_card: str
    target_turn: int
    simulator_success: bool
    simulator_status: str
    action_trace: dict[str, Any]
    review_status: str
    review_reason: str
    review_note: str | None
    affected_cards: tuple[str, ...]
    affected_actions: tuple[str, ...]
    created_at: str
    batch_id: str | None = None
    result_id: str | None = None
    trace_id: str | None = None

    def __post_init__(self) -> None:
        if not self.review_id or not self.review_id.startswith("sha256:"):
            raise ValueError("review_id must use sha256: prefix")
        if not self.challenge_id:
            raise ValueError("challenge_id is required")
        if not self.deck_hash:
            raise ValueError("deck_hash is required")
        if not self.target_card:
            raise ValueError("target_card is required")
        if self.target_turn <= 0:
            raise ValueError("target_turn must be positive")
        if self.review_status not in LineReviewStatus.ALL:
            raise ValueError("unknown review_status")
        if self.review_reason not in LineReviewReason.ALL:
            raise ValueError("unknown review_reason")
        if not self.created_at:
            raise ValueError("created_at is required")
        object.__setattr__(self, "action_trace", _json_clone(self.action_trace))
        object.__setattr__(self, "affected_cards", tuple(self.affected_cards))
        object.__setattr__(self, "affected_actions", tuple(self.affected_actions))

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "challenge_id": self.challenge_id,
            "deck_hash": self.deck_hash,
            "target_card": self.target_card,
            "target_turn": self.target_turn,
            "simulator_success": self.simulator_success,
            "simulator_status": self.simulator_status,
            "action_trace": _json_clone(self.action_trace),
            "review_status": self.review_status,
            "review_reason": self.review_reason,
            "review_note": self.review_note,
            "affected_cards": list(self.affected_cards),
            "affected_actions": list(self.affected_actions),
            "created_at": self.created_at,
            "batch_id": self.batch_id,
            "result_id": self.result_id,
            "trace_id": self.trace_id,
        }


@dataclass(frozen=True)
class LineReviewFixture:
    review_id: str
    challenge_id: str
    deck_hash: str
    target_condition: dict[str, Any]
    opening_hand: tuple[str, ...]
    simulator_status: str
    simulator_success: bool
    action_trace: dict[str, Any]
    review_status: str
    review_reason: str
    affected_cards: tuple[str, ...]
    affected_actions: tuple[str, ...]
    created_at: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "target_condition", _json_clone(self.target_condition))
        object.__setattr__(self, "opening_hand", tuple(self.opening_hand))
        object.__setattr__(self, "action_trace", _json_clone(self.action_trace))
        object.__setattr__(self, "affected_cards", tuple(self.affected_cards))
        object.__setattr__(self, "affected_actions", tuple(self.affected_actions))

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "challenge_id": self.challenge_id,
            "deck_hash": self.deck_hash,
            "target_condition": _json_clone(self.target_condition),
            "opening_hand": list(self.opening_hand),
            "simulator_status": self.simulator_status,
            "simulator_success": self.simulator_success,
            "action_trace": _json_clone(self.action_trace),
            "review_status": self.review_status,
            "review_reason": self.review_reason,
            "affected_cards": list(self.affected_cards),
            "affected_actions": list(self.affected_actions),
            "created_at": self.created_at,
        }


def create_line_review_annotation(
    challenge_result: ChallengeResult,
    review_status: str,
    review_reason: str,
    *,
    review_note: str | None = None,
    affected_cards: tuple[str, ...] | list[str] = (),
    affected_actions: tuple[str, ...] | list[str] = (),
    created_at: str | None = None,
    review_id: str | None = None,
    batch_id: str | None = None,
    result_id: str | None = None,
    trace_id: str | None = None,
) -> LineReviewAnnotation:
    created = created_at or challenge_result.completed_at or challenge_result.generated_at or "unknown"
    payload = {
        "challenge_id": challenge_result.challenge_id,
        "deck_hash": challenge_result.deck_hash,
        "target_card": challenge_result.target_condition.target_card,
        "target_turn": challenge_result.target_condition.turn,
        "simulator_success": challenge_result.simulator_success,
        "simulator_status": challenge_result.simulator_status,
        "action_trace": _json_clone(challenge_result.simulator_trace),
        "review_status": review_status,
        "review_reason": review_reason,
        "review_note": review_note,
        "affected_cards": list(affected_cards),
        "affected_actions": list(affected_actions),
        "created_at": created,
        "batch_id": batch_id,
        "result_id": result_id,
        "trace_id": trace_id,
    }
    return LineReviewAnnotation(
        review_id=review_id or _deterministic_review_id(payload),
        challenge_id=challenge_result.challenge_id,
        deck_hash=challenge_result.deck_hash,
        target_card=challenge_result.target_condition.target_card,
        target_turn=challenge_result.target_condition.turn,
        simulator_success=challenge_result.simulator_success,
        simulator_status=challenge_result.simulator_status,
        action_trace=payload["action_trace"],
        review_status=review_status,
        review_reason=review_reason,
        review_note=review_note,
        affected_cards=tuple(affected_cards),
        affected_actions=tuple(affected_actions),
        created_at=created,
        batch_id=batch_id,
        result_id=result_id,
        trace_id=trace_id,
    )


def reviewed_line_counts_as_success(annotation: LineReviewAnnotation) -> bool | None:
    if annotation.simulator_status == "unsupported":
        return None
    if not annotation.simulator_success:
        return False
    return annotation.review_status == LineReviewStatus.ACCEPTED


def export_line_review_fixture(
    annotation: LineReviewAnnotation,
    challenge_result: ChallengeResult,
) -> LineReviewFixture:
    if annotation.challenge_id != challenge_result.challenge_id:
        raise ValueError("annotation challenge_id does not match challenge result")
    return LineReviewFixture(
        review_id=annotation.review_id,
        challenge_id=annotation.challenge_id,
        deck_hash=annotation.deck_hash,
        target_condition=challenge_result.target_condition.to_dict(),
        opening_hand=challenge_result.opening_hand,
        simulator_status=annotation.simulator_status,
        simulator_success=annotation.simulator_success,
        action_trace=annotation.action_trace,
        review_status=annotation.review_status,
        review_reason=annotation.review_reason,
        affected_cards=annotation.affected_cards,
        affected_actions=annotation.affected_actions,
        created_at=annotation.created_at,
    )


def serialize_line_review_annotation(annotation: LineReviewAnnotation) -> dict[str, Any]:
    return annotation.to_dict()


def _deterministic_review_id(payload: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _json_clone(value: Any) -> Any:
    return json.loads(json.dumps(value, sort_keys=True))
