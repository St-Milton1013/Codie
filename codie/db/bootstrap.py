"""Bootstrap Codie's SQLite schema from domain SQL files."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .connection import connect

SCHEMA_DIR = Path(__file__).resolve().parent / "schema"
SCHEMA_ORDER = (
    "core.sql",
    "source.sql",
    "canonical.sql",
    "curated.sql",
    "analytics.sql",
    "regional.sql",
    "simulation.sql",
    "user.sql",
    "indexes.sql",
)


def bootstrap(connection: sqlite3.Connection) -> None:
    """Create all Codie tables and indexes on an existing connection."""
    for filename in SCHEMA_ORDER:
        path = SCHEMA_DIR / filename
        connection.executescript(path.read_text(encoding="utf-8"))


def bootstrap_database(database_path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open and bootstrap a SQLite database, returning the live connection."""
    connection = connect(database_path)
    bootstrap(connection)
    return connection
