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
