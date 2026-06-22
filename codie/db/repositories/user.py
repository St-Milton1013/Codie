"""Repositories for local user analysis records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .base import BaseRepository


class UserRepository(BaseRepository):
    def create_user_deck(self, deck: Mapping[str, Any]) -> int:
        self.require(deck, ("deck_hash", "created_at", "updated_at"))
        return self.insert("user_decks", deck)

    def add_user_deck_card(self, card: Mapping[str, Any]) -> int:
        self.require(card, ("user_deck_id", "raw_name", "quantity"))
        return self.insert("user_deck_cards", card)

    def create_analysis_session(self, session: Mapping[str, Any]) -> int:
        self.require(session, ("deck_hash", "session_type", "status", "started_at"))
        return self.insert("analysis_sessions", session)
