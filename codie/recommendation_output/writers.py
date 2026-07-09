"""Safe file writer for recommendation output report documents."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .models import RecommendationOutputBuildError, RecommendationOutputBundle, recommendation_output_bundle_to_dict
from .reporting import (
    RecommendationReportOptions,
    build_recommendation_report_document,
    recommendation_report_document_to_dict,
    recommendation_report_document_to_markdown,
)


ALLOWED_REPORT_FORMATS = frozenset({"json", "markdown", "both"})
WRITER_VERSION = "phase29d-safe-file-writer"


class RecommendationReportWriteError(ValueError):
    """Raised when recommendation report files cannot be written safely."""


@dataclass(frozen=True)
class RecommendationReportWriteOptions:
    output_format: str = "both"
    basename: str | None = None
    overwrite: bool = False
    include_provenance_section: bool = True
    writer_version: str = WRITER_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "output_format", _normalize_format(self.output_format))
        if not isinstance(self.overwrite, bool):
            raise RecommendationReportWriteError("overwrite must be a bool")
        if not isinstance(self.include_provenance_section, bool):
            raise RecommendationReportWriteError("include_provenance_section must be a bool")
        _require_text(self.writer_version, "writer_version")
        if self.basename is not None:
            object.__setattr__(self, "basename", _safe_explicit_basename(self.basename))


@dataclass(frozen=True)
class RecommendationReportWriteResult:
    root: str
    source_bundle_id: str
    report_id: str
    files: tuple[dict[str, Any], ...]
    bytes_written: int
    writer_version: str = WRITER_VERSION

    def __post_init__(self) -> None:
        _require_text(self.root, "root")
        _require_text(self.source_bundle_id, "source_bundle_id")
        _require_text(self.report_id, "report_id")
        _require_text(self.writer_version, "writer_version")
        if not isinstance(self.bytes_written, int) or self.bytes_written < 0:
            raise RecommendationReportWriteError("bytes_written must be a non-negative integer")
        object.__setattr__(self, "files", tuple(dict(file) for file in self.files))

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "source_bundle_id": self.source_bundle_id,
            "report_id": self.report_id,
            "files": [dict(file) for file in self.files],
            "bytes_written": self.bytes_written,
            "writer_version": self.writer_version,
        }


def write_recommendation_report_files(
    bundle: RecommendationOutputBundle | dict[str, Any],
    output_root: str | Path,
    *,
    options: RecommendationReportWriteOptions | None = None,
    report_id: str | None = None,
    generated_at: str | None = None,
) -> RecommendationReportWriteResult:
    """Write an already-built recommendation output bundle under output_root."""

    resolved_options = options or RecommendationReportWriteOptions()
    root = _resolve_output_root(output_root)
    bundle_payload = _bundle_payload(bundle)
    resolved_report_id = _require_text(report_id or f"report:{bundle_payload['bundle_id']}", "report_id")
    resolved_generated_at = _require_text(generated_at or bundle_payload["generated_at"], "generated_at")
    document = build_recommendation_report_document(
        bundle_payload,
        report_id=resolved_report_id,
        generated_at=resolved_generated_at,
        options=RecommendationReportOptions(include_provenance_section=resolved_options.include_provenance_section),
    )
    report_payload = recommendation_report_document_to_dict(document)
    report_markdown = recommendation_report_document_to_markdown(document)
    base_name = resolved_options.basename or f"{_safe_filename_stem(bundle_payload['bundle_id'])}.recommendation-report"
    writes = _prepare_report_writes(report_payload, report_markdown, base_name, root, resolved_options)

    written: list[dict[str, Any]] = []
    total_bytes = 0
    for relative_path, target, content_type, text in writes:
        _atomic_write_text(target, text)
        byte_count = len(text.encode("utf-8"))
        total_bytes += byte_count
        written.append(
            {
                "path": relative_path,
                "absolute_path": str(target),
                "content_type": content_type,
                "bytes_written": byte_count,
            }
        )

    return RecommendationReportWriteResult(
        root=str(root),
        source_bundle_id=bundle_payload["bundle_id"],
        report_id=resolved_report_id,
        files=tuple(written),
        bytes_written=total_bytes,
        writer_version=resolved_options.writer_version,
    )


def _prepare_report_writes(
    report_payload: dict[str, Any],
    report_markdown: str,
    base_name: str,
    root: Path,
    options: RecommendationReportWriteOptions,
) -> tuple[tuple[str, Path, str, str], ...]:
    prepared: list[tuple[str, Path, str, str]] = []
    if options.output_format in {"json", "both"}:
        prepared.append(
            _prepared_write(
                f"{base_name}.json",
                "application/json",
                _json_text(report_payload),
                root,
                overwrite=options.overwrite,
            )
        )
    if options.output_format in {"markdown", "both"}:
        prepared.append(
            _prepared_write(
                f"{base_name}.md",
                "text/markdown",
                report_markdown,
                root,
                overwrite=options.overwrite,
            )
        )
    file_manifest = [
        {"path": relative_path, "content_type": content_type, "bytes": len(text.encode("utf-8"))}
        for relative_path, _, content_type, text in prepared
    ]
    manifest = {
        "manifest_version": "phase29d-recommendation-report-writer",
        "writer_version": options.writer_version,
        "source_bundle_id": report_payload["source_bundle_id"],
        "report_id": report_payload["report_id"],
        "generated_at": report_payload["generated_at"],
        "files": file_manifest,
    }
    prepared.append(
        _prepared_write(
            "manifest.json",
            "application/json",
            _json_text(manifest),
            root,
            overwrite=options.overwrite,
        )
    )
    _reject_duplicate_paths(prepared)
    return tuple(prepared)


def _prepared_write(
    relative_path: str,
    content_type: str,
    text: str,
    root: Path,
    *,
    overwrite: bool,
) -> tuple[str, Path, str, str]:
    target = _resolve_relative_target(relative_path, root)
    if target.exists() and not overwrite:
        raise RecommendationReportWriteError("output file already exists; pass overwrite=True to replace it")
    return relative_path, target, content_type, text


def _reject_duplicate_paths(prepared: list[tuple[str, Path, str, str]]) -> None:
    seen: set[str] = set()
    for relative_path, _, _, _ in prepared:
        if relative_path in seen:
            raise RecommendationReportWriteError(f"duplicate output path: {relative_path}")
        seen.add(relative_path)


def _bundle_payload(bundle: RecommendationOutputBundle | dict[str, Any]) -> dict[str, Any]:
    if isinstance(bundle, RecommendationOutputBundle):
        return recommendation_output_bundle_to_dict(bundle)
    if not isinstance(bundle, dict):
        raise RecommendationReportWriteError("bundle must be a RecommendationOutputBundle or JSON object")
    try:
        build_recommendation_report_document(bundle, report_id="report:validation", generated_at=bundle["generated_at"])
    except (KeyError, RecommendationOutputBuildError) as exc:
        raise RecommendationReportWriteError(f"invalid RecommendationOutputBundle JSON input: {exc}") from exc
    return bundle


def _resolve_output_root(output_root: str | Path) -> Path:
    if str(output_root).strip() == "":
        raise RecommendationReportWriteError("output_root is required")
    root = Path(output_root).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise RecommendationReportWriteError("output_root must be a directory")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _resolve_relative_target(relative_path: str, root: Path) -> Path:
    checked = _require_relative_path(relative_path)
    target = (root / checked).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise RecommendationReportWriteError("output target must stay inside output_root") from exc
    return target


def _require_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecommendationReportWriteError("output path is required")
    if "\\" in value or ":" in value:
        raise RecommendationReportWriteError("output paths must be portable relative paths")
    path = Path(value)
    if path.is_absolute():
        raise RecommendationReportWriteError("output paths must be relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise RecommendationReportWriteError("output paths must not contain empty or traversal segments")
    suffix = path.suffix.lower()
    if suffix not in {".json", ".md"}:
        raise RecommendationReportWriteError("output paths must end with .json or .md")
    return value


def _safe_explicit_basename(value: str) -> str:
    text = _require_text(value, "basename")
    if "\\" in text or "/" in text or ":" in text:
        raise RecommendationReportWriteError("basename must not contain path separators or drive markers")
    if text.lower().endswith((".json", ".md")):
        raise RecommendationReportWriteError("basename must not include a file extension")
    return _safe_filename_stem(text)


def _safe_filename_stem(value: str) -> str:
    text = _require_text(value, "filename")
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip(".-")
    if not safe:
        raise RecommendationReportWriteError("filename cannot be normalized safely")
    return safe


def _normalize_format(value: str) -> str:
    normalized = _require_text(value, "output_format").lower()
    if normalized == "md":
        normalized = "markdown"
    if normalized not in ALLOWED_REPORT_FORMATS:
        raise RecommendationReportWriteError(f"unsupported output_format: {value}")
    return normalized


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecommendationReportWriteError(f"{field_name} is required")
    return value.strip()


def _json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def _atomic_write_text(target: Path, text: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.tmp")
    temp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temp, target)
