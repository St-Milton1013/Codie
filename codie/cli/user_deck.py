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
from codie.exports import (
    user_deck_comparison_export,
    user_deck_comparison_markdown,
    write_user_deck_comparison_exports,
)
from codie.user_decks import (
    UserDeckEvidenceCandidate,
    UserDeckImporter,
    build_user_deck_analysis_input,
    compare_user_deck_to_evidence,
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
