"""Static JSON exports for user workflow page models."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from codie.exports import ExportWriteResult, write_json_export
from codie.user_decks import (
    get_saved_user_deck_analysis,
    list_saved_user_deck_analyses,
)

from .user_workflow import (
    UserWorkflowPageModel,
    saved_analysis_detail_page_model,
    saved_analysis_list_page_model,
)


PAGE_MODEL_VERSION = "1"


def page_model_export_payload(
    page_model: UserWorkflowPageModel,
    *,
    exported_at: str,
    source: dict[str, Any],
) -> dict[str, Any]:
    """Wrap a UI page model with export metadata."""

    if not isinstance(exported_at, str) or not exported_at.strip():
        raise ValueError("exported_at is required")
    if not isinstance(source, dict) or not source:
        raise ValueError("source is required")
    payload = page_model.to_dict()
    return {
        "page_model_version": PAGE_MODEL_VERSION,
        "exported_at": exported_at,
        "source": dict(source),
        **payload,
    }


def write_page_model_json(
    payload: dict[str, Any],
    path: str | Path,
    *,
    output_root: str | Path | None = None,
) -> ExportWriteResult:
    """Write a page-model payload using the standard JSON export guardrails."""

    return write_json_export(payload, path, output_root=output_root)


def export_saved_analysis_list_page_model(
    user_repository,
    user_deck_id: int,
    *,
    path: str | Path,
    exported_at: str,
    output_root: str | Path | None = None,
) -> ExportWriteResult:
    """Export the saved-analysis list page model for one user deck."""

    summaries = list_saved_user_deck_analyses(user_repository, user_deck_id)
    page_model = saved_analysis_list_page_model(summaries, user_deck_id=user_deck_id)
    payload = page_model_export_payload(
        page_model,
        exported_at=exported_at,
        source={
            "export_type": "saved_analysis_list",
            "user_deck_id": user_deck_id,
        },
    )
    return write_page_model_json(payload, path, output_root=output_root)


def export_saved_analysis_detail_page_model(
    user_repository,
    saved_analysis_id: int,
    *,
    path: str | Path,
    exported_at: str,
    output_root: str | Path | None = None,
) -> ExportWriteResult:
    """Export one saved-analysis detail page model."""

    detail = get_saved_user_deck_analysis(user_repository, saved_analysis_id)
    page_model = saved_analysis_detail_page_model(detail)
    payload = page_model_export_payload(
        page_model,
        exported_at=exported_at,
        source={
            "export_type": "saved_analysis_detail",
            "saved_analysis_id": saved_analysis_id,
            "user_deck_id": detail.summary.user_deck_id,
            "deck_hash": detail.summary.deck_hash,
            "analysis_type": detail.summary.analysis_type,
        },
    )
    return write_page_model_json(payload, path, output_root=output_root)
