"""File writers for accepted Codie export artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ExportWriteResult:
    path: str
    bytes_written: int
    content_type: str

    def __post_init__(self) -> None:
        if not self.path.strip():
            raise ValueError("path is required")
        if self.bytes_written < 0:
            raise ValueError("bytes_written must be non-negative")
        if self.content_type not in {"application/json", "text/markdown"}:
            raise ValueError("unsupported content_type")


def _resolve_target(path: str | Path, *, output_root: str | Path | None) -> Path:
    target = Path(path)
    if str(target).strip() == "":
        raise ValueError("path is required")
    resolved_target = target.expanduser().resolve()
    if output_root is not None:
        resolved_root = Path(output_root).expanduser().resolve()
        try:
            resolved_target.relative_to(resolved_root)
        except ValueError as exc:
            raise ValueError("target path must stay inside output_root") from exc
    return resolved_target


def _write_text(path: Path, text: str, content_type: str) -> ExportWriteResult:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return ExportWriteResult(
        path=str(path),
        bytes_written=len(text.encode("utf-8")),
        content_type=content_type,
    )


def write_json_export(
    payload: dict[str, Any],
    path: str | Path,
    *,
    output_root: str | Path | None = None,
) -> ExportWriteResult:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")
    target = _resolve_target(path, output_root=output_root)
    if target.suffix.lower() != ".json":
        raise ValueError("JSON export path must end with .json")
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    return _write_text(target, text, "application/json")


def write_markdown_export(
    markdown: str,
    path: str | Path,
    *,
    output_root: str | Path | None = None,
) -> ExportWriteResult:
    if not isinstance(markdown, str) or not markdown.strip():
        raise ValueError("markdown is required")
    target = _resolve_target(path, output_root=output_root)
    if target.suffix.lower() != ".md":
        raise ValueError("Markdown export path must end with .md")
    text = markdown if markdown.endswith("\n") else markdown + "\n"
    return _write_text(target, text, "text/markdown")
