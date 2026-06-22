"""Repositories for maintainer-controlled registries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class CuratedRepository(BaseRepository):
    def create_commander_registry_entry(self, entry: Mapping[str, Any]) -> int:
        self.require(
            entry,
            ("commander_key", "commander_signature", "display_name", "source", "created_at", "updated_at"),
        )
        return self.insert("commander_registry", entry)

    def create_alias(self, alias: Mapping[str, Any]) -> int:
        self.require(
            alias,
            (
                "alias",
                "normalized_alias",
                "target_type",
                "target_name",
                "normalized_target_name",
                "source",
                "created_at",
                "updated_at",
            ),
        )
        return self.insert("alias_registry", alias)

    def get_alias(self, normalized_alias: str):
        return self.connection.execute(
            "SELECT * FROM alias_registry WHERE normalized_alias = ?",
            (normalized_alias,),
        ).fetchone()

    def create_archetype_label(self, label: Mapping[str, Any]) -> int:
        self.require(label, ("label", "normalized_label", "label_type", "source", "created_at", "updated_at"))
        return self.insert("archetype_label_registry", label)

    def upsert_combo(self, combo: Mapping[str, Any]) -> int:
        self.require(combo, ("provider", "combo_url", "created_at", "updated_at"))
        columns = (
            "provider",
            "provider_combo_id",
            "combo_url",
            "combo_name",
            "normalized_name",
            "outputs_json",
            "raw_json",
            "created_at",
            "updated_at",
        )
        values = tuple(combo.get(column) for column in columns)
        self.connection.execute(
            """
            INSERT INTO combos (
                provider, provider_combo_id, combo_url, combo_name, normalized_name,
                outputs_json, raw_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(provider, provider_combo_id) DO UPDATE SET
                combo_url = excluded.combo_url,
                combo_name = excluded.combo_name,
                normalized_name = excluded.normalized_name,
                outputs_json = excluded.outputs_json,
                raw_json = excluded.raw_json,
                updated_at = excluded.updated_at
            """,
            values,
        )
        row = self.get_combo(str(combo["provider"]), combo.get("provider_combo_id"))
        return int(row["combo_id"])

    def get_combo(self, provider: str, provider_combo_id: str | None):
        if provider_combo_id is None:
            return None
        return self.connection.execute(
            """
            SELECT * FROM combos
            WHERE provider = ? AND provider_combo_id = ?
            """,
            (provider, provider_combo_id),
        ).fetchone()

    def delete_combo_cards(self, combo_id: int) -> None:
        self.connection.execute(
            "DELETE FROM combo_cards WHERE combo_id = ?",
            (combo_id,),
        )

    def add_combo_card(self, card: Mapping[str, Any]) -> int:
        self.require(card, ("combo_id", "card_name"))
        return self.insert("combo_cards", card)

    def list_combo_cards(self, combo_id: int):
        return self.connection.execute(
            """
            SELECT * FROM combo_cards
            WHERE combo_id = ?
            ORDER BY combo_card_id
            """,
            (combo_id,),
        ).fetchall()
