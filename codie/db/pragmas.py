"""SQLite PRAGMA setup for Codie connections."""

from __future__ import annotations

import sqlite3


def apply_pragmas(connection: sqlite3.Connection) -> None:
    """Apply deterministic, local-first SQLite settings."""
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    connection.execute("PRAGMA temp_store = MEMORY")
    connection.row_factory = sqlite3.Row


def foreign_keys_enabled(connection: sqlite3.Connection) -> bool:
    row = connection.execute("PRAGMA foreign_keys").fetchone()
    return bool(row[0])
