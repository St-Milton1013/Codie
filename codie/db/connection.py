"""Connection factory for Codie's local SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .pragmas import apply_pragmas


def connect(database_path: str | Path = ":memory:") -> sqlite3.Connection:
    """Open a SQLite connection with Codie-required PRAGMAs enabled."""
    connection = sqlite3.connect(str(database_path))
    apply_pragmas(connection)
    return connection
