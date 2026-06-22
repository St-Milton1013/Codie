"""Read-only listing and retrieval for saved user deck analyses."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from codie.db.repositories.user import UserRepository


class SavedAnalysisReadError(ValueError):
    """Raised when a saved analysis cannot be read safely."""


@dataclass(frozen=True)
class SavedAnalysisSummary:
    saved_analysis_id: int
    user_deck_id: int | None
    deck_hash: str
    analysis_type: str
    generated_at: str
    report_path: str | None


@dataclass(frozen=True)
class SavedAnalysisDetail:
    summary: SavedAnalysisSummary
    summary_payload: dict[str, Any]


def list_saved_user_deck_analyses(
    user_repository: UserRepository,
    user_deck_id: int,
) -> tuple[SavedAnalysisSummary, ...]:
    """List saved analysis summaries for one user deck."""

    return tuple(
        _summary_from_row(row)
        for row in user_repository.list_saved_analysis_for_deck(user_deck_id)
    )


def get_saved_user_deck_analysis(
    user_repository: UserRepository,
    saved_analysis_id: int,
) -> SavedAnalysisDetail:
    """Fetch one saved analysis and parse its summary payload."""

    row = user_repository.get_saved_analysis(saved_analysis_id)
    if row is None:
        raise SavedAnalysisReadError(f"Unknown saved_analysis_id: {saved_analysis_id}")
    summary = _summary_from_row(row)
    try:
        payload = json.loads(row["summary_json"])
    except json.JSONDecodeError as exc:
        raise SavedAnalysisReadError("Saved analysis summary_json is malformed") from exc
    if not isinstance(payload, dict):
        raise SavedAnalysisReadError("Saved analysis summary_json must decode to an object")
    return SavedAnalysisDetail(summary=summary, summary_payload=payload)


def _summary_from_row(row) -> SavedAnalysisSummary:
    return SavedAnalysisSummary(
        saved_analysis_id=row["saved_analysis_id"],
        user_deck_id=row["user_deck_id"],
        deck_hash=row["deck_hash"],
        analysis_type=row["analysis_type"],
        generated_at=row["generated_at"],
        report_path=row["report_path"],
    )
