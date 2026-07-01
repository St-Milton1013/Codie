"""CLI wrapper for read-only user deck memory."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from codie.db.connection import connect
from codie.db.repositories.user import UserRepository
from codie.user_decks import (
    DeckMemoryFilters,
    DeckMemoryReadError,
    get_deck_memory_detail,
    list_deck_memory,
)


class DeckMemoryCliError(ValueError):
    """Raised when deck memory CLI inputs cannot be handled."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codie-user-deck-memory")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_memory = subparsers.add_parser("list-deck-memory", help="List remembered user decks.")
    _add_common_database_argument(list_memory)
    list_memory.add_argument("--commander-hash", help="Filter by commander hash.")
    list_memory.add_argument("--deck-hash", help="Filter by deck hash.")
    list_memory.add_argument(
        "--include-temporary",
        dest="include_temporary",
        action="store_true",
        default=True,
        help="Include temporary remembered decks. Default: enabled.",
    )
    list_memory.add_argument(
        "--exclude-temporary",
        dest="include_temporary",
        action="store_false",
        help="Exclude temporary remembered decks.",
    )
    list_memory.add_argument(
        "--include-persistent",
        dest="include_persistent",
        action="store_true",
        default=True,
        help="Include persistent remembered decks. Default: enabled.",
    )
    list_memory.add_argument(
        "--exclude-persistent",
        dest="include_persistent",
        action="store_false",
        help="Exclude persistent remembered decks.",
    )
    list_memory.add_argument("--created-at-from", help="Inclusive created_at lower bound.")
    list_memory.add_argument("--created-at-to", help="Inclusive created_at upper bound.")
    list_memory.add_argument("--limit", type=int, default=50, help="Maximum remembered decks to return.")

    show_memory = subparsers.add_parser("show-deck-memory", help="Show one remembered user deck.")
    _add_common_database_argument(show_memory)
    show_memory.add_argument("--user-deck-id", required=True, type=int, help="User deck ID to read.")
    show_memory.add_argument(
        "--include-raw-input",
        action="store_true",
        help="Include private raw deck input text in output.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list-deck-memory":
            payload = run_list_deck_memory(args)
        elif args.command == "show-deck-memory":
            payload = run_show_deck_memory(args)
        else:
            parser.error(f"Unsupported command: {args.command}")
            return 2
    except (DeckMemoryCliError, DeckMemoryReadError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(payload, sort_keys=True))
    return 0


def run_list_deck_memory(args: argparse.Namespace) -> dict[str, Any]:
    filters = DeckMemoryFilters(
        commander_hash=args.commander_hash,
        deck_hash=args.deck_hash,
        include_temporary=args.include_temporary,
        include_persistent=args.include_persistent,
        created_at_from=args.created_at_from,
        created_at_to=args.created_at_to,
        limit=args.limit,
    )
    with _user_repository(Path(args.db)) as user_repository:
        summaries = list_deck_memory(user_repository, filters)
    return {"decks": [asdict(summary) for summary in summaries]}


def run_show_deck_memory(args: argparse.Namespace) -> dict[str, Any]:
    with _user_repository(Path(args.db)) as user_repository:
        detail = get_deck_memory_detail(user_repository, args.user_deck_id)
    deck = asdict(detail)
    if not args.include_raw_input:
        deck.pop("raw_input", None)
    return {"deck": deck}


class _user_repository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.connection = None

    def __enter__(self) -> UserRepository:
        if not self.database_path.exists():
            raise DeckMemoryCliError(f"database path does not exist: {self.database_path}")
        if not self.database_path.is_file():
            raise DeckMemoryCliError(f"database path is not a file: {self.database_path}")
        try:
            self.connection = connect(self.database_path)
        except Exception as exc:  # pragma: no cover - platform-specific connection failures
            raise DeckMemoryCliError(f"database path could not be opened: {self.database_path}") from exc
        return UserRepository(self.connection)

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.connection is not None:
            self.connection.close()


def _add_common_database_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--db", required=True, help="Existing local Codie SQLite database path.")


if __name__ == "__main__":
    raise SystemExit(main())
