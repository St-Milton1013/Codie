"""View models for saved user workflow analysis pages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from codie.user_decks import SavedAnalysisDetail, SavedAnalysisSummary


FORBIDDEN_PAGE_FRAGMENTS = (
    "should play",
    "must include",
    "correct card",
    "breaks the format",
    "secretly optimal",
    "cut this",
)


@dataclass(frozen=True)
class UserWorkflowSummaryCard:
    label: str
    value: str
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "value": self.value, "detail": self.detail}


@dataclass(frozen=True)
class UserWorkflowTableRow:
    cells: dict[str, Any]

    def __post_init__(self) -> None:
        for value in self.cells.values():
            _validate_value(value)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.cells)


@dataclass(frozen=True)
class UserWorkflowPageModel:
    title: str
    generated_at: str | None
    summary_cards: tuple[UserWorkflowSummaryCard, ...]
    rows: tuple[UserWorkflowTableRow, ...]
    empty_state: str | None = None

    def __post_init__(self) -> None:
        _validate_text(self.title)
        if self.empty_state is not None:
            _validate_text(self.empty_state)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "generated_at": self.generated_at,
            "summary_cards": [card.to_dict() for card in self.summary_cards],
            "rows": [row.to_dict() for row in self.rows],
            "empty_state": self.empty_state,
        }


def saved_analysis_list_page_model(
    summaries: tuple[SavedAnalysisSummary, ...],
    *,
    user_deck_id: int,
) -> UserWorkflowPageModel:
    """Build a display-ready list model for saved analyses."""

    rows = tuple(
        UserWorkflowTableRow(
            {
                "saved_analysis_id": summary.saved_analysis_id,
                "analysis_type": summary.analysis_type,
                "generated_at": summary.generated_at,
                "deck_hash": summary.deck_hash,
                "report_path": summary.report_path,
            }
        )
        for summary in summaries
    )
    return UserWorkflowPageModel(
        title="Saved Analyses",
        generated_at=summaries[-1].generated_at if summaries else None,
        summary_cards=(
            UserWorkflowSummaryCard("User deck ID", str(user_deck_id)),
            UserWorkflowSummaryCard("Saved analyses", str(len(summaries))),
        ),
        rows=rows,
        empty_state=None if rows else "No saved analyses exist for this user deck.",
    )


def saved_analysis_detail_page_model(detail: SavedAnalysisDetail) -> UserWorkflowPageModel:
    """Build a display-ready detail model for one saved analysis."""

    payload = detail.summary_payload
    rows = tuple(
        UserWorkflowTableRow(
            {
                "card_name": _validated_text(row.get("card_name", "")),
                "evidence_type": _validated_text(row.get("evidence_type", "")),
                "presence_status": _validated_text(row.get("presence_status", "")),
                "quantity_in_deck": row.get("quantity_in_deck", 0),
                "zones": tuple(row.get("zones", ())),
                "sample_size": row.get("sample_size"),
                "source_record_id": row.get("source_record_id"),
                "source_url": row.get("source_url"),
                "evidence_line": _validated_text(row.get("evidence_line", "")),
            }
        )
        for row in payload.get("rows", ())
    )
    return UserWorkflowPageModel(
        title="Saved Analysis Detail",
        generated_at=detail.summary.generated_at,
        summary_cards=(
            UserWorkflowSummaryCard("Saved analysis ID", str(detail.summary.saved_analysis_id)),
            UserWorkflowSummaryCard("Analysis type", detail.summary.analysis_type),
            UserWorkflowSummaryCard("Present evidence cards", str(payload.get("present_count", 0))),
            UserWorkflowSummaryCard("Absent evidence cards", str(payload.get("absent_count", 0))),
        ),
        rows=rows,
        empty_state=None if rows else "This saved analysis has no evidence rows.",
    )


def _validated_text(value: str) -> str:
    _validate_text(value)
    return value


def _validate_text(value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("display text is required")
    normalized = " ".join(value.lower().split())
    for fragment in FORBIDDEN_PAGE_FRAGMENTS:
        if fragment in normalized:
            raise ValueError(f"unsupported strategic display text: {fragment}")


def _validate_value(value: Any) -> None:
    if isinstance(value, str):
        _validate_text(value)
    elif isinstance(value, (tuple, list)):
        for item in value:
            _validate_value(item)
