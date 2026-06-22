"""Shared repository utilities."""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any


class RepositoryError(ValueError):
    """Raised when repository input violates a persistence contract."""


class BaseRepository:
    """Small repository base with parameterized SQL helpers."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    @staticmethod
    def now() -> str:
        return datetime.now(UTC).replace(microsecond=0).isoformat()

    @staticmethod
    def require(data: Mapping[str, Any], fields: Sequence[str]) -> None:
        missing = [field for field in fields if data.get(field) in (None, "")]
        if missing:
            joined = ", ".join(missing)
            raise RepositoryError(f"Missing required field(s): {joined}")

    def insert(self, table: str, data: Mapping[str, Any]) -> int:
        keys = tuple(data.keys())
        placeholders = ", ".join("?" for _ in keys)
        columns = ", ".join(keys)
        values = tuple(data[key] for key in keys)
        cursor = self.connection.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            values,
        )
        return int(cursor.lastrowid)

    def fetch_by_id(self, table: str, id_column: str, value: Any) -> sqlite3.Row | None:
        cursor = self.connection.execute(
            f"SELECT * FROM {table} WHERE {id_column} = ?",
            (value,),
        )
        return cursor.fetchone()
