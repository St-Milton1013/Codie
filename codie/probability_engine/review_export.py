"""Pure export payload builders for simulator review summaries."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from .line_review import LineReviewFixture
from .reviewed_accuracy import ReviewedAccuracySummary


REVIEW_EXPORT_SCHEMA_VERSION = "codie-simulation-review-export-v1"


@dataclass(frozen=True)
class SimulationReviewMarkdownDocument:
    path: str
    title: str
    body: str

    def __post_init__(self) -> None:
        if not self.path or _is_absolute_path(self.path):
            raise ValueError("path must be relative")
        if not self.title:
            raise ValueError("title is required")

    def to_dict(self) -> dict[str, Any]:
        return {"path": self.path, "title": self.title, "body": self.body}


@dataclass(frozen=True)
class SimulationReviewExportBundle:
    bundle_id: str
    summary_path: str
    markdown_path: str
    fixture_paths: tuple[str, ...]
    files: tuple[dict[str, Any], ...]
    generated_at: str
    exported_at: str
    schema_version: str = REVIEW_EXPORT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not self.bundle_id or not self.bundle_id.startswith("sha256:"):
            raise ValueError("bundle_id must use sha256: prefix")
        paths = (self.summary_path, self.markdown_path, *self.fixture_paths)
        for path in paths:
            if not path or _is_absolute_path(path):
                raise ValueError("bundle paths must be relative")
        object.__setattr__(self, "fixture_paths", tuple(self.fixture_paths))
        object.__setattr__(self, "files", tuple(dict(file) for file in self.files))

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "simulation_review_export_bundle",
            "schema_version": self.schema_version,
            "bundle_id": self.bundle_id,
            "summary_path": self.summary_path,
            "markdown_path": self.markdown_path,
            "fixture_paths": list(self.fixture_paths),
            "generated_at": self.generated_at,
            "exported_at": self.exported_at,
            "files": [dict(file) for file in self.files],
        }


def simulation_review_summary_to_json_payload(
    summary: ReviewedAccuracySummary,
    *,
    exported_at: str,
) -> dict[str, Any]:
    payload = summary.to_dict()
    return {
        "kind": "reviewed_simulator_accuracy_summary",
        "schema_version": REVIEW_EXPORT_SCHEMA_VERSION,
        "summary": payload,
        "filters": payload["filters"],
        "generated_at": summary.generated_at,
        "exported_at": exported_at,
    }


def simulation_review_summary_to_markdown(
    summary: ReviewedAccuracySummary,
    *,
    exported_at: str,
    path: str = "reviewed_accuracy_summary.md",
) -> SimulationReviewMarkdownDocument:
    payload = summary.to_dict()
    lines = [
        "# Reviewed Simulator Accuracy Summary",
        "",
        f"- Schema version: `{REVIEW_EXPORT_SCHEMA_VERSION}`",
        f"- Generated at: `{summary.generated_at}`",
        f"- Exported at: `{exported_at}`",
        "",
        "## Filters",
        *_markdown_key_values(payload["filters"]),
        "",
        "## Counts",
        f"- Total reviews: {summary.total_reviews}",
        f"- Accepted successful lines: {summary.accepted_success_count}",
        f"- Rejected successful lines: {summary.rejected_success_count}",
        f"- Reviewed failures: {summary.reviewed_failure_count}",
        f"- Reviewed unsupported: {summary.reviewed_unsupported_count}",
        f"- Accepted success rate: {_rate_text(summary.accepted_success_rate)}",
        f"- Rejected success rate: {_rate_text(summary.rejected_success_rate)}",
        f"- Unsupported rate: {_rate_text(summary.unsupported_rate)}",
        "",
        "## Status Counts",
        *_markdown_count_lines(payload["status_counts"], "review_status"),
        "",
        "## Reason Counts",
        *_markdown_count_lines(payload["reason_counts"], "review_reason"),
        "",
        "## Affected Cards",
        *_markdown_count_lines(payload["affected_card_counts"], "value"),
        "",
        "## Affected Actions",
        *_markdown_count_lines(payload["affected_action_counts"], "value"),
        "",
    ]
    return SimulationReviewMarkdownDocument(
        path=path,
        title="Reviewed Simulator Accuracy Summary",
        body="\n".join(lines),
    )


def line_review_fixture_to_json_payload(
    fixture: LineReviewFixture,
    *,
    exported_at: str,
) -> dict[str, Any]:
    payload = fixture.to_dict()
    return {
        "kind": "simulation_line_review_fixture",
        "schema_version": REVIEW_EXPORT_SCHEMA_VERSION,
        **payload,
        "exported_at": exported_at,
    }


def line_review_fixture_to_markdown(
    fixture: LineReviewFixture,
    *,
    exported_at: str,
    path: str | None = None,
) -> SimulationReviewMarkdownDocument:
    payload = fixture.to_dict()
    target = payload["target_condition"]
    actions = payload["action_trace"].get("actions", [])
    body = "\n".join(
        [
            "# Simulation Line Review Fixture",
            "",
            f"- Schema version: `{REVIEW_EXPORT_SCHEMA_VERSION}`",
            f"- Review ID: `{fixture.review_id}`",
            f"- Challenge ID: `{fixture.challenge_id}`",
            f"- Deck hash: `{fixture.deck_hash}`",
            f"- Target card: `{target.get('target_card')}`",
            f"- Target turn: {target.get('turn')}",
            f"- Simulator status: `{fixture.simulator_status}`",
            f"- Simulator success: {fixture.simulator_success}",
            f"- Review status: `{fixture.review_status}`",
            f"- Review reason: `{fixture.review_reason}`",
            f"- Created at: `{fixture.created_at}`",
            f"- Exported at: `{exported_at}`",
            "",
            "## Affected Cards",
            *_markdown_values(fixture.affected_cards),
            "",
            "## Affected Actions",
            *_markdown_values(fixture.affected_actions),
            "",
            "## Trace Summary",
            f"- Action count: {len(actions)}",
            f"- Opening hand size: {len(fixture.opening_hand)}",
            "",
        ]
    )
    return SimulationReviewMarkdownDocument(
        path=path or _fixture_markdown_path(fixture.review_id),
        title="Simulation Line Review Fixture",
        body=body,
    )


def build_simulation_review_export_bundle(
    summary: ReviewedAccuracySummary,
    fixtures: tuple[LineReviewFixture, ...] | list[LineReviewFixture],
    *,
    exported_at: str,
) -> SimulationReviewExportBundle:
    fixture_tuple = tuple(fixtures)
    summary_payload = simulation_review_summary_to_json_payload(summary, exported_at=exported_at)
    summary_markdown = simulation_review_summary_to_markdown(summary, exported_at=exported_at)
    files: list[dict[str, Any]] = [
        {"path": "reviewed_accuracy_summary.json", "content_type": "application/json", "payload": summary_payload},
        {"path": summary_markdown.path, "content_type": "text/markdown", "body": summary_markdown.body},
    ]
    fixture_paths = []
    for fixture in fixture_tuple:
        json_path = _fixture_json_path(fixture.review_id)
        markdown_doc = line_review_fixture_to_markdown(fixture, exported_at=exported_at)
        fixture_paths.extend((json_path, markdown_doc.path))
        files.append(
            {
                "path": json_path,
                "content_type": "application/json",
                "payload": line_review_fixture_to_json_payload(fixture, exported_at=exported_at),
            }
        )
        files.append({"path": markdown_doc.path, "content_type": "text/markdown", "body": markdown_doc.body})
    bundle_payload = {
        "summary": summary_payload,
        "fixture_review_ids": [fixture.review_id for fixture in fixture_tuple],
        "fixture_paths": fixture_paths,
        "exported_at": exported_at,
    }
    return SimulationReviewExportBundle(
        bundle_id=_sha256_id(bundle_payload),
        summary_path="reviewed_accuracy_summary.json",
        markdown_path=summary_markdown.path,
        fixture_paths=tuple(fixture_paths),
        files=tuple(files),
        generated_at=summary.generated_at,
        exported_at=exported_at,
    )


def _fixture_json_path(review_id: str) -> str:
    return f"fixtures/{_path_id(review_id)}.json"


def _fixture_markdown_path(review_id: str) -> str:
    return f"fixtures/{_path_id(review_id)}.md"


def _path_id(value: str) -> str:
    return value.replace("sha256:", "")


def _sha256_id(payload: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(_json(payload).encode("utf-8")).hexdigest()


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _is_absolute_path(path: str) -> bool:
    return path.startswith("/") or path.startswith("\\") or (len(path) > 2 and path[1:3] == ":\\")


def _rate_text(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def _markdown_key_values(values: dict[str, Any]) -> list[str]:
    lines = [f"- {key}: `{value}`" for key, value in sorted(values.items()) if value not in (None, "")]
    return lines or ["- None"]


def _markdown_count_lines(items: list[dict[str, Any]], key: str) -> list[str]:
    return [f"- `{item[key]}`: {item['count']}" for item in items] or ["- None"]


def _markdown_values(values: tuple[str, ...]) -> list[str]:
    return [f"- `{value}`" for value in values] or ["- None"]
