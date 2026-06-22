"""JSON and Markdown export helpers for persisted Codie evidence."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from codie.recommendations.evidence import validate_claim_text


@dataclass(frozen=True)
class ExportMetadata:
    export_type: str
    generated_at: str
    schema_version: str = "1"

    def __post_init__(self) -> None:
        _require_text(self.export_type, "export_type")
        _require_text(self.generated_at, "generated_at")
        _require_text(self.schema_version, "schema_version")


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _row_value(row: Any, key: str) -> Any:
    try:
        return row[key]
    except (KeyError, IndexError, TypeError):
        try:
            return getattr(row, key)
        except AttributeError as exc:
            raise ValueError(f"{key} is required") from exc


def _optional_json(value: Any) -> Any:
    if value in (None, ""):
        return None
    return json.loads(str(value))


def _metadata(metadata: ExportMetadata) -> dict[str, str]:
    return {
        "export_type": metadata.export_type,
        "generated_at": metadata.generated_at,
        "schema_version": metadata.schema_version,
    }


def _recommendation_candidate_dict(row: Any) -> dict[str, Any]:
    return {
        "candidate_id": _row_value(row, "candidate_id"),
        "scryfall_id": _row_value(row, "scryfall_id"),
        "oracle_id": _row_value(row, "oracle_id"),
        "candidate_type": _row_value(row, "candidate_type"),
        "recommendation_score": _row_value(row, "recommendation_score"),
        "inclusion_rate": _row_value(row, "inclusion_rate"),
        "lift_score": _row_value(row, "lift_score"),
        "confidence_score": _row_value(row, "confidence_score"),
        "similarity_score": _row_value(row, "similarity_score"),
        "package_completion_score": _row_value(row, "package_completion_score"),
        "generic_staple_penalty": _row_value(row, "generic_staple_penalty"),
        "evidence": _optional_json(_row_value(row, "evidence_json")),
        "explanation_text": _row_value(row, "explanation_text"),
    }


def export_recommendation_run_json(*, run: Any, candidates: list[Any] | tuple[Any, ...], metadata: ExportMetadata) -> dict[str, Any]:
    if run is None:
        raise ValueError("run is required")
    ordered_candidates = sorted(
        (_recommendation_candidate_dict(candidate) for candidate in candidates),
        key=lambda candidate: (
            -(candidate["recommendation_score"] or 0),
            candidate["oracle_id"] or "",
            candidate["candidate_id"],
        ),
    )
    return {
        "metadata": _metadata(metadata),
        "run": {
            "recommendation_run_id": _row_value(run, "recommendation_run_id"),
            "input_deck_hash": _row_value(run, "input_deck_hash"),
            "commander_hash": _row_value(run, "commander_hash"),
            "generated_at": _row_value(run, "generated_at"),
            "config": _optional_json(_row_value(run, "config_json")),
            "source_snapshot_id": _row_value(run, "source_snapshot_id"),
            "notes": _row_value(run, "notes"),
        },
        "candidates": ordered_candidates,
    }


def _innovation_item_dict(row: Any) -> dict[str, Any]:
    return {
        "innovation_snapshot_item_id": _row_value(row, "innovation_snapshot_item_id"),
        "innovation_id": _row_value(row, "innovation_id"),
        "oracle_id": _row_value(row, "oracle_id"),
        "scryfall_id": _row_value(row, "scryfall_id"),
        "commander_signature": _row_value(row, "commander_signature"),
        "region_code": _row_value(row, "region_code"),
        "innovation_type": _row_value(row, "innovation_type"),
        "recent_window": _row_value(row, "recent_window"),
        "baseline_window": _row_value(row, "baseline_window"),
        "recent_inclusion_rate": _row_value(row, "recent_inclusion_rate"),
        "baseline_inclusion_rate": _row_value(row, "baseline_inclusion_rate"),
        "usage_delta": _row_value(row, "usage_delta"),
        "recent_topcut_count": _row_value(row, "recent_topcut_count"),
        "recent_winner_count": _row_value(row, "recent_winner_count"),
        "first_recent_seen_at": _row_value(row, "first_recent_seen_at"),
        "last_seen_before_recent_window": _row_value(row, "last_seen_before_recent_window"),
        "card_released_at": _row_value(row, "card_released_at"),
        "is_new_release": bool(_row_value(row, "is_new_release")),
        "sample_size": _row_value(row, "sample_size"),
        "confidence_score": _row_value(row, "confidence_score"),
        "source_event_ids": _optional_json(_row_value(row, "source_event_ids_json")) or [],
        "source_deck_ids": _optional_json(_row_value(row, "source_deck_ids_json")) or [],
        "generated_at": _row_value(row, "generated_at"),
    }


def export_innovation_snapshot_json(*, run: Any, items: list[Any] | tuple[Any, ...], metadata: ExportMetadata) -> dict[str, Any]:
    if run is None:
        raise ValueError("run is required")
    ordered_items = sorted(
        (_innovation_item_dict(item) for item in items),
        key=lambda item: (
            item["innovation_type"],
            item["oracle_id"],
            item["commander_signature"] or "",
            item["region_code"] or "",
            item["innovation_id"],
        ),
    )
    return {
        "metadata": _metadata(metadata),
        "snapshot": {
            "innovation_snapshot_run_id": _row_value(run, "innovation_snapshot_run_id"),
            "generated_at": _row_value(run, "generated_at"),
            "config_hash": _row_value(run, "config_hash"),
            "config": _optional_json(_row_value(run, "config_json")),
            "notes": _row_value(run, "notes"),
        },
        "items": ordered_items,
    }


def _fmt(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.4f}".rstrip("0").rstrip(".")
    return str(value)


def recommendation_run_markdown(export: dict[str, Any]) -> str:
    run = export["run"]
    candidates = export["candidates"]
    lines = [
        "# Recommendation Run Export",
        "",
        f"- Run ID: {run['recommendation_run_id']}",
        f"- Generated At: {run['generated_at']}",
        f"- Input Deck Hash: {run['input_deck_hash']}",
        f"- Candidate Count: {len(candidates)}",
        "",
        "## Candidates",
    ]
    for candidate in candidates:
        explanation = validate_claim_text(str(candidate.get("explanation_text") or "No explanation text."))
        lines.append(
            f"- `{candidate['oracle_id']}` {candidate['candidate_type']} score {_fmt(candidate['recommendation_score'])}; "
            f"confidence {_fmt(candidate['confidence_score'])}. {explanation}"
        )
    return "\n".join(lines) + "\n"


def innovation_snapshot_markdown(export: dict[str, Any]) -> str:
    snapshot = export["snapshot"]
    items = export["items"]
    lines = [
        "# Innovation Snapshot Export",
        "",
        f"- Snapshot ID: {snapshot['innovation_snapshot_run_id']}",
        f"- Generated At: {snapshot['generated_at']}",
        f"- Config Hash: {snapshot['config_hash']}",
        f"- Signal Count: {len(items)}",
        "",
        "## Signals",
    ]
    for item in items:
        line = (
            f"Card `{item['oracle_id']}` produced {item['innovation_type']} evidence in "
            f"{item['recent_window']} with sample size {item['sample_size']} and confidence {_fmt(item['confidence_score'])}."
        )
        validate_claim_text(line)
        lines.append(f"- {line}")
    return "\n".join(lines) + "\n"


def outside_review_markdown(*, title: str, exports: list[dict[str, Any]] | tuple[dict[str, Any], ...], generated_at: str) -> str:
    _require_text(title, "title")
    _require_text(generated_at, "generated_at")
    lines = [
        f"# {validate_claim_text(title)}",
        "",
        f"- Generated At: {generated_at}",
        f"- Export Count: {len(exports)}",
        "",
        "## Included Exports",
    ]
    for export in exports:
        metadata = export.get("metadata", {})
        export_type = validate_claim_text(str(metadata.get("export_type", "unknown")))
        lines.append(f"- {export_type} generated at {metadata.get('generated_at', 'n/a')}")
    return "\n".join(lines) + "\n"
