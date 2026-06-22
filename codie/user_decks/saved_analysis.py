"""Persist evidence-only user deck analysis summaries."""

from __future__ import annotations

import json
from dataclasses import dataclass

from codie.db.repositories.user import UserRepository

from .evidence_comparison import UserDeckEvidenceComparison


@dataclass(frozen=True)
class SavedUserDeckAnalysisResult:
    saved_analysis_id: int
    user_deck_id: int
    deck_hash: str
    analysis_type: str
    generated_at: str
    report_path: str | None


def save_user_deck_comparison_analysis(
    user_repository: UserRepository,
    comparison: UserDeckEvidenceComparison,
    *,
    report_path: str | None = None,
    analysis_type: str = "user_deck_evidence_comparison",
) -> SavedUserDeckAnalysisResult:
    """Persist an evidence-only user deck comparison summary."""

    if not analysis_type.strip():
        raise ValueError("analysis_type is required")
    saved_analysis_id = user_repository.create_saved_analysis(
        {
            "user_deck_id": comparison.user_deck_id,
            "deck_hash": comparison.deck_hash,
            "analysis_type": analysis_type,
            "generated_at": comparison.generated_at,
            "summary_json": _comparison_summary_json(comparison),
            "report_path": report_path,
        }
    )
    return SavedUserDeckAnalysisResult(
        saved_analysis_id=saved_analysis_id,
        user_deck_id=comparison.user_deck_id,
        deck_hash=comparison.deck_hash,
        analysis_type=analysis_type,
        generated_at=comparison.generated_at,
        report_path=report_path,
    )


def _comparison_summary_json(comparison: UserDeckEvidenceComparison) -> str:
    payload = {
        "user_deck_id": comparison.user_deck_id,
        "deck_hash": comparison.deck_hash,
        "commander_hash": comparison.commander_hash,
        "present_count": comparison.present_count,
        "absent_count": comparison.absent_count,
        "generated_at": comparison.generated_at,
        "rows": [
            {
                "oracle_id": row.oracle_id,
                "card_name": row.card_name,
                "evidence_type": row.evidence_type,
                "presence_status": row.presence_status,
                "quantity_in_deck": row.quantity_in_deck,
                "zones": list(row.zones),
                "score": row.score,
                "sample_size": row.sample_size,
                "source_record_id": row.source_record_id,
                "source_url": row.source_url,
                "evidence_line": row.evidence_line,
            }
            for row in comparison.rows
        ],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
