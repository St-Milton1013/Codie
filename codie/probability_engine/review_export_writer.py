"""Safe file writer for simulator review export bundles."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .review_export import SimulationReviewExportBundle


@dataclass(frozen=True)
class SimulationReviewExportWriteResult:
    root: str
    bundle_id: str
    files: tuple[dict[str, Any], ...]
    bytes_written: int

    def __post_init__(self) -> None:
        if not self.root.strip():
            raise ValueError("root is required")
        if not self.bundle_id.startswith("sha256:"):
            raise ValueError("bundle_id must use sha256: prefix")
        if self.bytes_written < 0:
            raise ValueError("bytes_written must be non-negative")
        object.__setattr__(self, "files", tuple(dict(file) for file in self.files))

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "bundle_id": self.bundle_id,
            "files": [dict(file) for file in self.files],
            "bytes_written": self.bytes_written,
        }


def write_simulation_review_export_bundle(
    bundle: SimulationReviewExportBundle,
    output_root: str | Path,
) -> SimulationReviewExportWriteResult:
    """Write an already-built simulator review export bundle under output_root."""

    if str(output_root).strip() == "":
        raise ValueError("output_root is required")
    root = Path(output_root).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise ValueError("output_root must be a directory")
    writes = _prepare_bundle_writes(bundle, root)

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

    return SimulationReviewExportWriteResult(
        root=str(root),
        bundle_id=bundle.bundle_id,
        files=tuple(written),
        bytes_written=total_bytes,
    )


def _prepare_bundle_writes(
    bundle: SimulationReviewExportBundle,
    root: Path,
) -> tuple[tuple[str, Path, str, str], ...]:
    prepared: list[tuple[str, Path, str, str]] = []
    seen_paths = {"manifest.json"}

    for file in bundle.files:
        relative_path = _require_relative_path(file.get("path"))
        if relative_path in seen_paths:
            raise ValueError(f"duplicate export path: {relative_path}")
        seen_paths.add(relative_path)

        content_type = file.get("content_type")
        if content_type == "application/json":
            if not relative_path.lower().endswith(".json"):
                raise ValueError("JSON export paths must end with .json")
            if "payload" not in file or not isinstance(file["payload"], dict):
                raise ValueError("JSON export files require dictionary payload")
            text = _json_text(file["payload"])
        elif content_type == "text/markdown":
            if not relative_path.lower().endswith(".md"):
                raise ValueError("Markdown export paths must end with .md")
            body = file.get("body")
            if not isinstance(body, str) or not body.strip():
                raise ValueError("Markdown export files require non-empty body")
            text = body if body.endswith("\n") else body + "\n"
        else:
            raise ValueError("unsupported export content_type")

        prepared.append((relative_path, _resolve_relative_target(relative_path, root), content_type, text))

    prepared.append(
        (
            "manifest.json",
            _resolve_relative_target("manifest.json", root),
            "application/json",
            _json_text(bundle.to_dict()),
        )
    )
    return tuple(prepared)


def _require_relative_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("export path is required")
    if "\\" in value or ":" in value:
        raise ValueError("export paths must be portable relative paths")
    path = Path(value)
    if path.is_absolute():
        raise ValueError("export paths must be relative")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("export paths must not contain empty or traversal segments")
    return value


def _resolve_relative_target(relative_path: str, root: Path) -> Path:
    checked = _require_relative_path(relative_path)
    target = (root / checked).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("export target must stay inside output_root") from exc
    return target


def _json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def _atomic_write_text(target: Path, text: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.tmp")
    temp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temp, target)
