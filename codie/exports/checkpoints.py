"""Checkpoint report generation from accepted export payloads."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from codie.recommendations.evidence import validate_claim_text

from .writers import ExportWriteResult, write_markdown_export


@dataclass(frozen=True)
class ValidationSummary:
    command: str
    status: str
    test_count: int | None = None
    commit_hash: str | None = None
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.command, "command")
        status = self.status.strip().lower()
        if status not in {"pass", "pass_with_notes", "fail", "not_run"}:
            raise ValueError("status must be pass, pass_with_notes, fail, or not_run")
        object.__setattr__(self, "status", status)
        if self.test_count is not None and self.test_count < 0:
            raise ValueError("test_count must be non-negative")
        object.__setattr__(self, "notes", tuple(validate_claim_text(note) for note in self.notes))


@dataclass(frozen=True)
class CheckpointExport:
    title: str
    generated_at: str
    validation: ValidationSummary
    exports: tuple[dict[str, Any], ...]
    review_notes: tuple[str, ...]


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")


def _export_sort_key(export: dict[str, Any]) -> tuple[str, str]:
    metadata = export.get("metadata", {})
    return (
        str(metadata.get("export_type", "")),
        str(metadata.get("generated_at", "")),
    )


def build_checkpoint_export(
    *,
    title: str,
    generated_at: str,
    validation: ValidationSummary,
    exports: tuple[dict[str, Any], ...] | list[dict[str, Any]],
    review_notes: tuple[str, ...] | list[str] = (),
) -> CheckpointExport:
    _require_text(title, "title")
    _require_text(generated_at, "generated_at")
    cleaned_notes = tuple(validate_claim_text(note) for note in review_notes)
    return CheckpointExport(
        title=validate_claim_text(title),
        generated_at=generated_at,
        validation=validation,
        exports=tuple(sorted(exports, key=_export_sort_key)),
        review_notes=cleaned_notes,
    )


def _export_summary(export: dict[str, Any]) -> str:
    metadata = export.get("metadata", {})
    export_type = str(metadata.get("export_type", "unknown"))
    generated_at = str(metadata.get("generated_at", "n/a"))
    if "candidates" in export:
        count = len(export.get("candidates", ()))
        detail = f"{count} candidate(s)"
    elif "items" in export:
        count = len(export.get("items", ()))
        detail = f"{count} innovation signal(s)"
    else:
        detail = "no row count"
    return validate_claim_text(f"{export_type} generated at {generated_at}: {detail}.")


def checkpoint_markdown(checkpoint: CheckpointExport) -> str:
    lines = [
        f"# {checkpoint.title}",
        "",
        f"- Generated At: {checkpoint.generated_at}",
        f"- Validation Status: {checkpoint.validation.status}",
        f"- Validation Command: `{checkpoint.validation.command}`",
    ]
    if checkpoint.validation.test_count is not None:
        lines.append(f"- Tests: {checkpoint.validation.test_count}")
    if checkpoint.validation.commit_hash:
        lines.append(f"- Commit: `{checkpoint.validation.commit_hash}`")
    lines.extend(["", "## Included Exports"])
    if checkpoint.exports:
        for export in checkpoint.exports:
            lines.append(f"- {_export_summary(export)}")
    else:
        lines.append("- No exports included.")

    lines.extend(["", "## Review Notes"])
    combined_notes = checkpoint.validation.notes + checkpoint.review_notes
    if combined_notes:
        for note in combined_notes:
            lines.append(f"- {validate_claim_text(note)}")
    else:
        lines.append("- No review notes.")
    return "\n".join(lines) + "\n"


def write_checkpoint_markdown(
    checkpoint: CheckpointExport,
    path: str | Path,
    *,
    output_root: str | Path | None = None,
) -> ExportWriteResult:
    return write_markdown_export(
        checkpoint_markdown(checkpoint),
        path,
        output_root=output_root,
    )
