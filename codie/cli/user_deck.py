"""CLI wrapper for local user deck import and evidence comparison exports."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from codie.cards.lookup import CardLookup
from codie.db.bootstrap import bootstrap_database
from codie.db.connection import connect
from codie.db.repositories.core import CoreRepository
from codie.db.repositories.user import UserRepository
from codie.delivery import LocalPreviewConfig, LocalPreviewServer
from codie.exports import (
    ShareBundleAsset,
    user_deck_comparison_export,
    user_deck_comparison_markdown,
    write_local_share_bundle,
    write_share_bundle_zip,
    write_user_deck_comparison_exports,
)
from codie.pages import (
    export_saved_analysis_detail_page_model,
    export_saved_analysis_list_page_model,
)
from codie.user_decks import (
    UserDeckEvidenceCandidate,
    UserDeckImporter,
    build_user_deck_analysis_input,
    compare_user_deck_to_evidence,
    get_saved_user_deck_analysis,
    list_saved_user_deck_analyses,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codie-user-deck")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_db = subparsers.add_parser("init-db", help="Bootstrap a Codie SQLite database.")
    init_db.add_argument("--db", required=True, help="SQLite database path to create or bootstrap.")

    import_deck = subparsers.add_parser("import-user-deck", help="Import and optionally compare a user deck.")
    import_deck.add_argument("--db", required=True, help="Existing Codie SQLite database path.")
    import_deck.add_argument("--deck-file", required=True, help="Text file containing a quantity/name decklist.")
    import_deck.add_argument("--deck-name", help="Optional display name for the imported deck.")
    import_deck.add_argument("--source-url", help="Optional user-supplied deck URL.")
    import_deck.add_argument("--evidence-json", help="Optional JSON file containing evidence candidates.")
    import_deck.add_argument("--json-out", help="Optional path for JSON comparison export.")
    import_deck.add_argument("--markdown-out", help="Optional path for Markdown comparison export.")
    import_deck.add_argument("--output-root", help="Optional root directory that output paths must stay inside.")
    import_deck.add_argument(
        "--generated-at",
        default="1970-01-01T00:00:00+00:00",
        help="Timestamp to stamp comparison outputs with.",
    )

    list_saved = subparsers.add_parser("list-saved-analyses", help="List saved analyses for a user deck.")
    list_saved.add_argument("--db", required=True, help="Existing Codie SQLite database path.")
    list_saved.add_argument("--user-deck-id", required=True, type=int, help="User deck ID to list analyses for.")

    show_saved = subparsers.add_parser("show-saved-analysis", help="Show one saved analysis detail.")
    show_saved.add_argument("--db", required=True, help="Existing Codie SQLite database path.")
    show_saved.add_argument("--saved-analysis-id", required=True, type=int, help="Saved analysis ID to show.")

    export_ui_list = subparsers.add_parser(
        "export-ui-saved-analysis-list",
        help="Export saved-analysis list page model JSON for the UI.",
    )
    export_ui_list.add_argument("--db", required=True, help="Existing Codie SQLite database path.")
    export_ui_list.add_argument("--user-deck-id", required=True, type=int, help="User deck ID to export.")
    export_ui_list.add_argument("--output", required=True, help="JSON output path.")
    export_ui_list.add_argument("--output-root", help="Optional root directory that output path must stay inside.")
    export_ui_list.add_argument(
        "--exported-at",
        default="1970-01-01T00:00:00+00:00",
        help="Timestamp to stamp the UI page model export with.",
    )

    export_ui_detail = subparsers.add_parser(
        "export-ui-saved-analysis-detail",
        help="Export saved-analysis detail page model JSON for the UI.",
    )
    export_ui_detail.add_argument("--db", required=True, help="Existing Codie SQLite database path.")
    export_ui_detail.add_argument("--saved-analysis-id", required=True, type=int, help="Saved analysis ID to export.")
    export_ui_detail.add_argument("--output", required=True, help="JSON output path.")
    export_ui_detail.add_argument("--output-root", help="Optional root directory that output path must stay inside.")
    export_ui_detail.add_argument(
        "--exported-at",
        default="1970-01-01T00:00:00+00:00",
        help="Timestamp to stamp the UI page model export with.",
    )

    share_bundle = subparsers.add_parser(
        "build-share-bundle",
        help="Build a static local report bundle from existing export files.",
    )
    share_bundle.add_argument("--title", required=True, help="Display title for the bundle.")
    share_bundle.add_argument("--generated-at", required=True, help="Timestamp to stamp the bundle with.")
    share_bundle.add_argument("--asset", action="append", required=True, help="Report/export file to include.")
    share_bundle.add_argument(
        "--asset-label",
        action="append",
        help="Optional label for an asset. Labels are applied in asset order.",
    )
    share_bundle.add_argument("--output-dir", required=True, help="Bundle output directory.")
    share_bundle.add_argument("--output-root", help="Optional root directory that output path must stay inside.")
    share_bundle.add_argument(
        "--qr-target",
        help="Optional explicit path or URL to encode as a local QR PNG in the bundle.",
    )
    share_bundle.add_argument(
        "--no-print-entry",
        action="store_true",
        help="Do not write the print-friendly HTML entry.",
    )

    serve_bundle = subparsers.add_parser(
        "serve-share-bundle",
        help="Serve one local share bundle directory until interrupted.",
    )
    serve_bundle.add_argument("--bundle-dir", required=True, help="Share bundle directory containing index.html.")
    serve_bundle.add_argument("--host", default="127.0.0.1", help="Host to bind. Default: 127.0.0.1.")
    serve_bundle.add_argument("--port", type=int, default=0, help="Port to bind. Default: 0 picks an available port.")
    serve_bundle.add_argument(
        "--allow-lan",
        action="store_true",
        help="Required when binding a LAN-visible host such as 0.0.0.0.",
    )

    zip_bundle = subparsers.add_parser(
        "zip-share-bundle",
        help="Package a static local report bundle into a deterministic zip file.",
    )
    zip_bundle.add_argument("--bundle-dir", required=True, help="Share bundle directory containing index.html.")
    zip_bundle.add_argument("--output", required=True, help="Zip output path.")
    zip_bundle.add_argument("--output-root", help="Optional root directory that output path must stay inside.")
    zip_bundle.add_argument(
        "--generated-at",
        required=True,
        help="Timestamp to stamp the zip manifest with.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init-db":
        _init_db(Path(args.db))
        return 0
    if args.command == "import-user-deck":
        summary = _import_user_deck(args)
        print(json.dumps(summary, sort_keys=True))
        return 0
    if args.command == "list-saved-analyses":
        summary = _list_saved_analyses(args)
        print(json.dumps(summary, sort_keys=True))
        return 0
    if args.command == "show-saved-analysis":
        detail = _show_saved_analysis(args)
        print(json.dumps(detail, sort_keys=True))
        return 0
    if args.command == "export-ui-saved-analysis-list":
        result = _export_ui_saved_analysis_list(args)
        print(json.dumps(result, sort_keys=True))
        return 0
    if args.command == "export-ui-saved-analysis-detail":
        result = _export_ui_saved_analysis_detail(args)
        print(json.dumps(result, sort_keys=True))
        return 0
    if args.command == "build-share-bundle":
        result = _build_share_bundle(args)
        print(json.dumps(result, sort_keys=True))
        return 0
    if args.command == "serve-share-bundle":
        return _serve_share_bundle(args)
    if args.command == "zip-share-bundle":
        result = _zip_share_bundle(args)
        print(json.dumps(result, sort_keys=True))
        return 0
    parser.error(f"Unsupported command: {args.command}")
    return 2


def _init_db(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = bootstrap_database(path)
    connection.commit()
    connection.close()


def _import_user_deck(args: argparse.Namespace) -> dict[str, Any]:
    deck_text = Path(args.deck_file).read_text(encoding="utf-8")
    connection = connect(args.db)
    try:
        user_repository = UserRepository(connection)
        importer = UserDeckImporter(user_repository, CardLookup(CoreRepository(connection)))
        imported = importer.import_text(
            deck_text,
            deck_name=args.deck_name,
            source_url=args.source_url,
        )
        analysis_input = build_user_deck_analysis_input(
            user_repository,
            imported.user_deck_id,
            analysis_session_id=imported.analysis_session_id,
        )
        candidates = _load_evidence_candidates(Path(args.evidence_json)) if args.evidence_json else ()
        comparison = compare_user_deck_to_evidence(
            analysis_input,
            candidates,
            generated_at=args.generated_at,
        )

        summary: dict[str, Any] = {
            "user_deck_id": imported.user_deck_id,
            "analysis_session_id": imported.analysis_session_id,
            "deck_hash": imported.deck_hash,
            "commander_hash": imported.commander_hash,
            "card_count": imported.card_count,
            "present_count": comparison.present_count,
            "absent_count": comparison.absent_count,
        }
        if args.json_out or args.markdown_out:
            if not args.json_out or not args.markdown_out:
                raise ValueError("--json-out and --markdown-out must be supplied together")
            result = write_user_deck_comparison_exports(
                comparison,
                json_path=args.json_out,
                markdown_path=args.markdown_out,
                output_root=args.output_root,
            )
            summary["json_export_path"] = result.json.path
            summary["markdown_export_path"] = result.markdown.path
        else:
            summary["comparison"] = user_deck_comparison_export(comparison)
            summary["comparison_markdown"] = user_deck_comparison_markdown(comparison)
        connection.commit()
        return summary
    finally:
        connection.close()


def _load_evidence_candidates(path: Path) -> tuple[UserDeckEvidenceCandidate, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload["candidates"] if isinstance(payload, dict) and "candidates" in payload else payload
    if not isinstance(rows, list):
        raise ValueError("evidence JSON must be a list or an object with a candidates list")
    return tuple(_candidate_from_mapping(row) for row in rows)


def _list_saved_analyses(args: argparse.Namespace) -> dict[str, Any]:
    connection = connect(args.db)
    try:
        user_repository = UserRepository(connection)
        rows = list_saved_user_deck_analyses(user_repository, args.user_deck_id)
        return {
            "user_deck_id": args.user_deck_id,
            "saved_analyses": [_summary_to_dict(row) for row in rows],
        }
    finally:
        connection.close()


def _show_saved_analysis(args: argparse.Namespace) -> dict[str, Any]:
    connection = connect(args.db)
    try:
        user_repository = UserRepository(connection)
        detail = get_saved_user_deck_analysis(user_repository, args.saved_analysis_id)
        return {
            "summary": _summary_to_dict(detail.summary),
            "summary_payload": detail.summary_payload,
        }
    finally:
        connection.close()


def _export_ui_saved_analysis_list(args: argparse.Namespace) -> dict[str, Any]:
    connection = connect(args.db)
    try:
        user_repository = UserRepository(connection)
        result = export_saved_analysis_list_page_model(
            user_repository,
            args.user_deck_id,
            path=args.output,
            output_root=args.output_root,
            exported_at=args.exported_at,
        )
        return _write_result_to_dict(result)
    finally:
        connection.close()


def _export_ui_saved_analysis_detail(args: argparse.Namespace) -> dict[str, Any]:
    connection = connect(args.db)
    try:
        user_repository = UserRepository(connection)
        result = export_saved_analysis_detail_page_model(
            user_repository,
            args.saved_analysis_id,
            path=args.output,
            output_root=args.output_root,
            exported_at=args.exported_at,
        )
        return _write_result_to_dict(result)
    finally:
        connection.close()


def _write_result_to_dict(result) -> dict[str, Any]:
    return {
        "path": result.path,
        "bytes_written": result.bytes_written,
        "content_type": result.content_type,
    }


def _build_share_bundle(args: argparse.Namespace) -> dict[str, Any]:
    labels = args.asset_label or []
    if len(labels) > len(args.asset):
        raise ValueError("--asset-label cannot be supplied more times than --asset")
    assets = tuple(
        ShareBundleAsset(path=asset_path, label=labels[index] if index < len(labels) else None)
        for index, asset_path in enumerate(args.asset)
    )
    result = write_local_share_bundle(
        title=args.title,
        generated_at=args.generated_at,
        assets=assets,
        output_dir=args.output_dir,
        output_root=args.output_root,
        qr_target=args.qr_target,
        include_print_entry=not args.no_print_entry,
    )
    return {
        "output_dir": result.output_dir,
        "index_path": result.index_path,
        "print_path": result.print_path,
        "manifest_path": result.manifest_path,
        "asset_paths": list(result.asset_paths),
        "qr_asset_path": result.qr_asset_path,
    }


def _serve_share_bundle(args: argparse.Namespace) -> int:
    config = LocalPreviewConfig(
        bundle_dir=args.bundle_dir,
        host=args.host,
        port=args.port,
        allow_lan=args.allow_lan,
    )
    server = LocalPreviewServer(config)
    try:
        print(
            json.dumps(
                {
                    "bundle_dir": str(server.root),
                    "host": server.host,
                    "port": server.port,
                    "url": server.url,
                    "privacy_warning": "Serving this bundle exposes its files to clients that can reach the bound host and port.",
                },
                sort_keys=True,
            ),
            flush=True,
        )
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.close()
    return 0


def _zip_share_bundle(args: argparse.Namespace) -> dict[str, Any]:
    result = write_share_bundle_zip(
        bundle_dir=args.bundle_dir,
        output=args.output,
        output_root=args.output_root,
        generated_at=args.generated_at,
    )
    return {
        "zip_path": result.zip_path,
        "bytes_written": result.bytes_written,
        "file_count": result.file_count,
        "total_bytes": result.total_bytes,
        "rejected_files": list(result.rejected_files),
    }


def _summary_to_dict(summary) -> dict[str, Any]:
    return {
        "saved_analysis_id": summary.saved_analysis_id,
        "user_deck_id": summary.user_deck_id,
        "deck_hash": summary.deck_hash,
        "analysis_type": summary.analysis_type,
        "generated_at": summary.generated_at,
        "report_path": summary.report_path,
    }


def _candidate_from_mapping(row: Any) -> UserDeckEvidenceCandidate:
    if not isinstance(row, dict):
        raise ValueError("each evidence candidate must be an object")
    return UserDeckEvidenceCandidate(
        oracle_id=row["oracle_id"],
        card_name=row["card_name"],
        evidence_type=row["evidence_type"],
        score=row.get("score"),
        sample_size=row.get("sample_size"),
        source_record_id=row.get("source_record_id"),
        source_url=row.get("source_url"),
    )


if __name__ == "__main__":
    raise SystemExit(main())
