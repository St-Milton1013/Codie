"""CLI wrapper for simulator review export bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from codie.probability_engine import (
    SimulationReviewExportBundle,
    write_simulation_review_export_bundle,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codie-simulation-review")
    subparsers = parser.add_subparsers(dest="command", required=True)

    export_bundle = subparsers.add_parser(
        "export-review-bundle",
        help="Write an accepted simulator review export bundle under an output root.",
    )
    export_bundle.add_argument(
        "--bundle-json",
        required=True,
        help="Path to a Phase 13Z/14A simulation review export bundle JSON.",
    )
    export_bundle.add_argument(
        "--output-root",
        required=True,
        help="Root directory where bundle files will be written.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "export-review-bundle":
        result = _export_review_bundle(args)
        print(json.dumps(result, sort_keys=True))
        return 0
    parser.error(f"Unsupported command: {args.command}")
    return 2


def _export_review_bundle(args: argparse.Namespace) -> dict[str, Any]:
    bundle = _load_bundle_json(Path(args.bundle_json))
    result = write_simulation_review_export_bundle(bundle, args.output_root)
    return result.to_dict()


def _load_bundle_json(path: Path) -> SimulationReviewExportBundle:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("bundle JSON must be an object")
    if payload.get("kind") != "simulation_review_export_bundle":
        raise ValueError("bundle JSON must be a simulation_review_export_bundle")
    files = payload.get("files")
    if not isinstance(files, list):
        raise ValueError("bundle JSON requires files list")
    return SimulationReviewExportBundle(
        bundle_id=_required_string(payload, "bundle_id"),
        summary_path=_required_string(payload, "summary_path"),
        markdown_path=_required_string(payload, "markdown_path"),
        fixture_paths=tuple(_string_list(payload.get("fixture_paths"), "fixture_paths")),
        files=tuple(_dict_list(files, "files")),
        generated_at=_required_string(payload, "generated_at"),
        exported_at=_required_string(payload, "exported_at"),
        schema_version=_required_string(payload, "schema_version"),
    )


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"bundle JSON requires {key}")
    return value


def _string_list(value: Any, key: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"bundle JSON requires {key} list")
    return value


def _dict_list(value: Any, key: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"bundle JSON requires {key} object list")
    return [dict(item) for item in value]


if __name__ == "__main__":
    raise SystemExit(main())
