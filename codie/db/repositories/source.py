"""Repositories for preserved provider/source records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class SourceRepository(BaseRepository):
    def create_ingestion_run(self, run: Mapping[str, Any]) -> int:
        self.require(run, ("provider", "pipeline_name", "started_at", "status"))
        return self.insert("ingestion_runs", run)

    def update_ingestion_run(self, run_id: int, updates: Mapping[str, Any]) -> None:
        if not updates:
            return
        assignments = ", ".join(f"{column} = ?" for column in updates)
        values = tuple(updates[column] for column in updates) + (run_id,)
        self.connection.execute(
            f"UPDATE ingestion_runs SET {assignments} WHERE run_id = ?",
            values,
        )

    def get_ingestion_run(self, run_id: int):
        return self.fetch_by_id("ingestion_runs", "run_id", run_id)

    def create_provider_object(self, provider_object: Mapping[str, Any]) -> int:
        self.require(provider_object, ("provider", "object_type", "retrieved_at", "payload_hash"))
        return self.insert("provider_objects", provider_object)

    def get_provider_object(self, provider_object_id: int):
        return self.fetch_by_id("provider_objects", "provider_object_id", provider_object_id)

    def create_source_event(self, event: Mapping[str, Any]) -> int:
        self.require(event, ("provider", "imported_at"))
        return self.insert("source_events", event)

    def get_source_event(self, source_event_id: int):
        return self.fetch_by_id("source_events", "source_event_id", source_event_id)

    def list_source_events_for_canonicalization(self):
        return self.connection.execute(
            """
            SELECT * FROM source_events
            WHERE canonical_event_id IS NULL OR dedupe_status = 'pending'
            ORDER BY source_event_id
            """
        ).fetchall()

    def update_source_event(self, source_event_id: int, updates: Mapping[str, Any]) -> None:
        if not updates:
            return
        assignments = ", ".join(f"{column} = ?" for column in updates)
        values = tuple(updates[column] for column in updates) + (source_event_id,)
        self.connection.execute(
            f"UPDATE source_events SET {assignments} WHERE source_event_id = ?",
            values,
        )

    def create_source_deck(self, deck: Mapping[str, Any]) -> int:
        self.require(deck, ("provider", "imported_at"))
        return self.insert("source_decks", deck)

    def get_source_deck(self, source_deck_id: int):
        return self.fetch_by_id("source_decks", "source_deck_id", source_deck_id)

    def list_source_decks_for_canonicalization(self):
        return self.connection.execute(
            """
            SELECT * FROM source_decks
            WHERE canonical_deck_id IS NULL OR dedupe_status = 'pending'
            ORDER BY source_deck_id
            """
        ).fetchall()

    def update_source_deck(self, source_deck_id: int, updates: Mapping[str, Any]) -> None:
        if not updates:
            return
        assignments = ", ".join(f"{column} = ?" for column in updates)
        values = tuple(updates[column] for column in updates) + (source_deck_id,)
        self.connection.execute(
            f"UPDATE source_decks SET {assignments} WHERE source_deck_id = ?",
            values,
        )

    def create_source_deck_card(self, card: Mapping[str, Any]) -> int:
        self.require(card, ("source_deck_id", "raw_name", "quantity"))
        return self.insert("source_deck_cards", card)

    def list_source_deck_cards(self, source_deck_id: int):
        return self.connection.execute(
            """
            SELECT * FROM source_deck_cards
            WHERE source_deck_id = ?
            ORDER BY COALESCE(source_order, source_deck_card_id), source_deck_card_id
            """,
            (source_deck_id,),
        ).fetchall()
