"""Repositories for canonical analytics records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class CanonicalRepository(BaseRepository):
    def get_event(self, canonical_event_id: int):
        return self.fetch_by_id("canonical_events", "canonical_event_id", canonical_event_id)

    def get_event_by_dedupe_key(self, dedupe_key: str):
        return self.connection.execute(
            "SELECT * FROM canonical_events WHERE dedupe_key = ?",
            (dedupe_key,),
        ).fetchone()

    def create_event(self, event: Mapping[str, Any]) -> int:
        self.require(event, ("event_name", "normalized_event_name", "dedupe_key", "created_at", "updated_at"))
        return self.insert("canonical_events", event)

    def update_event(self, canonical_event_id: int, updates: Mapping[str, Any]) -> None:
        if not updates:
            return
        assignments = ", ".join(f"{column} = ?" for column in updates)
        values = tuple(updates[column] for column in updates) + (canonical_event_id,)
        self.connection.execute(
            f"UPDATE canonical_events SET {assignments} WHERE canonical_event_id = ?",
            values,
        )

    def get_deck(self, canonical_deck_id: int):
        return self.fetch_by_id("canonical_decks", "canonical_deck_id", canonical_deck_id)

    def get_deck_by_hash(self, deck_hash: str):
        return self.connection.execute(
            "SELECT * FROM canonical_decks WHERE deck_hash = ?",
            (deck_hash,),
        ).fetchone()

    def create_deck(self, deck: Mapping[str, Any]) -> int:
        self.require(deck, ("deck_hash", "commander_hash", "card_count", "commander_count", "created_at", "updated_at"))
        return self.insert("canonical_decks", deck)

    def update_deck(self, canonical_deck_id: int, updates: Mapping[str, Any]) -> None:
        if not updates:
            return
        assignments = ", ".join(f"{column} = ?" for column in updates)
        values = tuple(updates[column] for column in updates) + (canonical_deck_id,)
        self.connection.execute(
            f"UPDATE canonical_decks SET {assignments} WHERE canonical_deck_id = ?",
            values,
        )

    def get_event_source_link(self, canonical_event_id: int, source_event_id: int):
        return self.connection.execute(
            """
            SELECT * FROM canonical_event_sources
            WHERE canonical_event_id = ? AND source_event_id = ?
            """,
            (canonical_event_id, source_event_id),
        ).fetchone()

    def link_event_source(self, link: Mapping[str, Any]) -> int:
        self.require(link, ("canonical_event_id", "source_event_id", "provider", "created_at"))
        return self.insert("canonical_event_sources", link)

    def get_deck_source_link(self, canonical_deck_id: int, source_deck_id: int):
        return self.connection.execute(
            """
            SELECT * FROM canonical_deck_sources
            WHERE canonical_deck_id = ? AND source_deck_id = ?
            """,
            (canonical_deck_id, source_deck_id),
        ).fetchone()

    def link_deck_source(self, link: Mapping[str, Any]) -> int:
        self.require(link, ("canonical_deck_id", "source_deck_id", "provider", "created_at"))
        return self.insert("canonical_deck_sources", link)

    def get_deck_card(self, canonical_deck_id: int, scryfall_id: str, zone: str):
        return self.connection.execute(
            """
            SELECT * FROM canonical_deck_cards
            WHERE canonical_deck_id = ? AND scryfall_id = ? AND zone = ?
            """,
            (canonical_deck_id, scryfall_id, zone),
        ).fetchone()

    def add_deck_card(self, card: Mapping[str, Any]) -> int:
        self.require(card, ("canonical_deck_id", "scryfall_id"))
        return self.insert("canonical_deck_cards", card)

    def get_deck_commander(self, canonical_deck_id: int, scryfall_id: str):
        return self.connection.execute(
            """
            SELECT * FROM canonical_deck_commanders
            WHERE canonical_deck_id = ? AND scryfall_id = ?
            """,
            (canonical_deck_id, scryfall_id),
        ).fetchone()

    def add_deck_commander(self, commander: Mapping[str, Any]) -> int:
        self.require(commander, ("canonical_deck_id", "scryfall_id"))
        return self.insert("canonical_deck_commanders", commander)

    def get_event_deck_entry(self, canonical_event_id: int, canonical_deck_id: int, source_deck_id: int | None):
        if source_deck_id is None:
            return self.connection.execute(
                """
                SELECT * FROM event_deck_entries
                WHERE canonical_event_id = ? AND canonical_deck_id = ? AND source_deck_id IS NULL
                """,
                (canonical_event_id, canonical_deck_id),
            ).fetchone()
        return self.connection.execute(
            """
            SELECT * FROM event_deck_entries
            WHERE canonical_event_id = ? AND canonical_deck_id = ? AND source_deck_id = ?
            """,
            (canonical_event_id, canonical_deck_id, source_deck_id),
        ).fetchone()

    def create_event_deck_entry(self, entry: Mapping[str, Any]) -> int:
        self.require(entry, ("canonical_event_id", "canonical_deck_id", "created_at"))
        return self.insert("event_deck_entries", entry)
