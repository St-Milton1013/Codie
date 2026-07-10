"""CLI wrapper for recommendation output report files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from codie.recommendation_output import (
    RecommendationReportWriteError,
    RecommendationReportWriteOptions,
    write_recommendation_report_files,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codie-recommendation-output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render = subparsers.add_parser(
        "render",
        help="Render an already-built RecommendationOutputBundle JSON into local report files.",
    )
    render.add_argument("--bundle-json", required=True, help="Path to a RecommendationOutputBundle JSON file.")
    render.add_argument("--format", required=True, choices=("json", "markdown", "md", "both"), help="Report output format.")
    render.add_argument("--output-root", required=True, help="Existing output directory for report files.")
    render.add_argument("--basename", help="Optional deterministic output basename without extension.")
    render.add_argument("--overwrite", action="store_true", help="Allow replacing existing report files.")
    render.add_argument("--create-output-root", action="store_true", help="Create output root when it is missing.")
    render.add_argument("--no-provenance", action="store_true", help="Omit the provenance report section.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "render":
            result = _render(args)
            print(json.dumps(result, sort_keys=True))
            return 0
    except (OSError, json.JSONDecodeError, RecommendationReportWriteError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.error(f"Unsupported command: {args.command}")
    return 2


def _render(args: argparse.Namespace) -> dict[str, Any]:
    bundle = _load_bundle_json(Path(args.bundle_json))
    options = RecommendationReportWriteOptions(
        output_format=args.format,
        basename=args.basename,
        overwrite=args.overwrite,
        create_output_root=args.create_output_root,
        include_provenance_section=not args.no_provenance,
    )
    result = write_recommendation_report_files(bundle, args.output_root, options=options)
    return result.to_dict()


def _load_bundle_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("bundle JSON must be an object")
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
