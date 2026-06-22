"""Build read-only analysis input objects for imported user decks."""

from __future__ import annotations

from dataclasses import dataclass

from codie.db.repositories.user import UserRepository


class UserDeckAnalysisInputError(ValueError):
    """Raised when a user deck analysis input cannot be built."""


@dataclass(frozen=True)
class UserDeckAnalysisCard:
    raw_name: str
    quantity: int
    zone: str
    scryfall_id: str | None
    oracle_id: str | None
    resolution_status: str | None


@dataclass(frozen=True)
class UserDeckAnalysisInput:
    user_deck_id: int
    analysis_session_id: int | None
    deck_name: str | None
    deck_hash: str
    commander_hash: str | None
    source_url: str | None
    is_temporary: bool
    cards: tuple[UserDeckAnalysisCard, ...]
    unresolved_cards: tuple[UserDeckAnalysisCard, ...]
    mainboard_count: int
    commander_count: int
    total_card_count: int


def build_user_deck_analysis_input(
    user_repository: UserRepository,
    user_deck_id: int,
    *,
    analysis_session_id: int | None = None,
) -> UserDeckAnalysisInput:
    """Load an imported user deck into a deterministic analysis input object."""

    deck = user_repository.get_user_deck(user_deck_id)
    if deck is None:
        raise UserDeckAnalysisInputError(f"Unknown user_deck_id: {user_deck_id}")

    if analysis_session_id is not None:
        session = user_repository.get_analysis_session(analysis_session_id)
        if session is None:
            raise UserDeckAnalysisInputError(f"Unknown analysis_session_id: {analysis_session_id}")
        if session["user_deck_id"] != user_deck_id:
            raise UserDeckAnalysisInputError("Analysis session does not belong to user deck")

    cards = tuple(
        UserDeckAnalysisCard(
            raw_name=row["raw_name"],
            quantity=row["quantity"],
            zone=row["zone"] or "mainboard",
            scryfall_id=row["scryfall_id"],
            oracle_id=row["oracle_id"],
            resolution_status=row["resolution_status"],
        )
        for row in user_repository.list_user_deck_cards(user_deck_id)
    )
    if not cards:
        raise UserDeckAnalysisInputError("User deck has no card rows")

    unresolved = tuple(card for card in cards if not card.scryfall_id or not card.oracle_id)
    mainboard_count = sum(card.quantity for card in cards if card.zone == "mainboard")
    commander_count = sum(card.quantity for card in cards if card.zone == "commander")
    total_card_count = sum(card.quantity for card in cards)
    return UserDeckAnalysisInput(
        user_deck_id=user_deck_id,
        analysis_session_id=analysis_session_id,
        deck_name=deck["deck_name"],
        deck_hash=deck["deck_hash"],
        commander_hash=deck["commander_hash"],
        source_url=deck["source_url"],
        is_temporary=bool(deck["is_temporary"]),
        cards=cards,
        unresolved_cards=unresolved,
        mainboard_count=mainboard_count,
        commander_count=commander_count,
        total_card_count=total_card_count,
    )
