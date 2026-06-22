"""Core card and commander repositories."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class CoreRepository(BaseRepository):
    def insert_card(self, card: Mapping[str, Any]) -> str:
        self.require(card, ("scryfall_id", "name", "normalized_name", "raw_json", "imported_at"))
        self.insert("cards", card)
        return str(card["scryfall_id"])

    def upsert_card(self, card: Mapping[str, Any]) -> str:
        self.require(card, ("scryfall_id", "name", "normalized_name", "raw_json", "imported_at"))
        columns = tuple(card.keys())
        assignments = ", ".join(f"{column} = excluded.{column}" for column in columns if column != "scryfall_id")
        placeholders = ", ".join("?" for _ in columns)
        self.connection.execute(
            f"""
            INSERT INTO cards ({", ".join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(scryfall_id) DO UPDATE SET {assignments}
            """,
            tuple(card[column] for column in columns),
        )
        return str(card["scryfall_id"])

    def get_card(self, scryfall_id: str):
        return self.fetch_by_id("cards", "scryfall_id", scryfall_id)

    def get_card_by_normalized_name(self, normalized_name: str):
        return self.connection.execute(
            "SELECT * FROM cards WHERE normalized_name = ? ORDER BY name, scryfall_id LIMIT 1",
            (normalized_name,),
        ).fetchone()

    def list_cards(self):
        return self.connection.execute(
            "SELECT * FROM cards ORDER BY normalized_name, name, scryfall_id"
        ).fetchall()

    def insert_commander(self, commander: Mapping[str, Any]) -> int:
        self.require(
            commander,
            ("scryfall_id", "canonical_name", "normalized_name", "color_identity_json", "created_at", "updated_at"),
        )
        return self.insert("commanders", commander)

    def get_commander(self, commander_id: int):
        return self.fetch_by_id("commanders", "commander_id", commander_id)
