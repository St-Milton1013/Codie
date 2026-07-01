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

    def get_user_deck(self, user_deck_id: int):
        return self.fetch_by_id("user_decks", "user_deck_id", user_deck_id)

    def get_user_deck_memory_row(self, user_deck_id: int):
        return self.connection.execute(
            """
            SELECT
                d.*,
                COALESCE(cards.card_count, 0) AS card_count,
                COALESCE(analyses.saved_analysis_count, 0) AS saved_analysis_count,
                analyses.latest_analysis_generated_at
            FROM user_decks d
            LEFT JOIN (
                SELECT user_deck_id, SUM(quantity) AS card_count
                FROM user_deck_cards
                GROUP BY user_deck_id
            ) cards ON cards.user_deck_id = d.user_deck_id
            LEFT JOIN (
                SELECT
                    user_deck_id,
                    COUNT(*) AS saved_analysis_count,
                    MAX(generated_at) AS latest_analysis_generated_at
                FROM saved_analysis
                GROUP BY user_deck_id
            ) analyses ON analyses.user_deck_id = d.user_deck_id
            WHERE d.user_deck_id = ?
            """,
            (user_deck_id,),
        ).fetchone()

    def list_user_decks_for_memory(
        self,
        *,
        commander_hash: str | None = None,
        deck_hash: str | None = None,
        include_temporary: bool = True,
        include_persistent: bool = True,
        created_at_from: str | None = None,
        created_at_to: str | None = None,
        limit: int = 50,
    ):
        where_clauses: list[str] = []
        params: list[Any] = []

        if commander_hash is not None:
            where_clauses.append("d.commander_hash = ?")
            params.append(commander_hash)
        if deck_hash is not None:
            where_clauses.append("d.deck_hash = ?")
            params.append(deck_hash)
        if not include_temporary:
            where_clauses.append("COALESCE(d.is_temporary, 0) = 0")
        if not include_persistent:
            where_clauses.append("COALESCE(d.is_temporary, 0) = 1")
        if created_at_from is not None:
            where_clauses.append("d.created_at >= ?")
            params.append(created_at_from)
        if created_at_to is not None:
            where_clauses.append("d.created_at <= ?")
            params.append(created_at_to)

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        params.append(limit)
        return self.connection.execute(
            f"""
            SELECT
                d.*,
                COALESCE(cards.card_count, 0) AS card_count,
                COALESCE(analyses.saved_analysis_count, 0) AS saved_analysis_count,
                analyses.latest_analysis_generated_at
            FROM user_decks d
            LEFT JOIN (
                SELECT user_deck_id, SUM(quantity) AS card_count
                FROM user_deck_cards
                GROUP BY user_deck_id
            ) cards ON cards.user_deck_id = d.user_deck_id
            LEFT JOIN (
                SELECT
                    user_deck_id,
                    COUNT(*) AS saved_analysis_count,
                    MAX(generated_at) AS latest_analysis_generated_at
                FROM saved_analysis
                GROUP BY user_deck_id
            ) analyses ON analyses.user_deck_id = d.user_deck_id
            {where_sql}
            ORDER BY d.updated_at DESC, d.created_at DESC, d.user_deck_id DESC
            LIMIT ?
            """,
            tuple(params),
        ).fetchall()

    def list_user_deck_cards(self, user_deck_id: int):
        return self.connection.execute(
            """
            SELECT *
            FROM user_deck_cards
            WHERE user_deck_id = ?
            ORDER BY user_deck_card_id
            """,
            (user_deck_id,),
        ).fetchall()

    def create_analysis_session(self, session: Mapping[str, Any]) -> int:
        self.require(session, ("deck_hash", "session_type", "status", "started_at"))
        return self.insert("analysis_sessions", session)

    def get_analysis_session(self, analysis_session_id: int):
        return self.fetch_by_id("analysis_sessions", "analysis_session_id", analysis_session_id)

    def list_analysis_sessions_for_deck(self, user_deck_id: int):
        return self.connection.execute(
            """
            SELECT *
            FROM analysis_sessions
            WHERE user_deck_id = ?
            ORDER BY started_at, analysis_session_id
            """,
            (user_deck_id,),
        ).fetchall()

    def create_saved_analysis(self, analysis: Mapping[str, Any]) -> int:
        self.require(analysis, ("deck_hash", "analysis_type", "generated_at", "summary_json"))
        return self.insert("saved_analysis", analysis)

    def get_saved_analysis(self, saved_analysis_id: int):
        return self.fetch_by_id("saved_analysis", "saved_analysis_id", saved_analysis_id)

    def list_saved_analysis_for_deck(self, user_deck_id: int):
        return self.connection.execute(
            """
            SELECT *
            FROM saved_analysis
            WHERE user_deck_id = ?
            ORDER BY generated_at, saved_analysis_id
            """,
            (user_deck_id,),
        ).fetchall()
