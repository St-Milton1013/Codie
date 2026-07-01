"""Read-only deck memory listing and retrieval helpers."""

from __future__ import annotations

from dataclasses import dataclass

from codie.db.repositories.user import UserRepository


class DeckMemoryReadError(ValueError):
    """Raised when deck memory cannot be read safely."""


@dataclass(frozen=True)
class DeckMemoryFilters:
    commander_hash: str | None = None
    deck_hash: str | None = None
    include_temporary: bool = True
    include_persistent: bool = True
    created_at_from: str | None = None
    created_at_to: str | None = None
    limit: int = 50

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise DeckMemoryReadError("Deck memory limit must be at least 1")
        if not self.include_temporary and not self.include_persistent:
            raise DeckMemoryReadError("At least one deck memory visibility class must be included")
        if (
            self.created_at_from is not None
            and self.created_at_to is not None
            and self.created_at_from > self.created_at_to
        ):
            raise DeckMemoryReadError("created_at_from cannot be later than created_at_to")


@dataclass(frozen=True)
class DeckMemorySummary:
    user_deck_id: int
    deck_name: str | None
    source_url: str | None
    deck_hash: str
    commander_hash: str | None
    created_at: str
    updated_at: str
    is_temporary: bool
    card_count: int
    saved_analysis_count: int
    latest_analysis_generated_at: str | None


@dataclass(frozen=True)
class DeckMemoryCard:
    raw_name: str
    quantity: int
    zone: str | None
    scryfall_id: str | None
    oracle_id: str | None
    resolution_status: str | None


@dataclass(frozen=True)
class DeckMemoryAnalysisSummary:
    saved_analysis_id: int
    analysis_type: str
    generated_at: str
    report_path: str | None
    deck_hash: str


@dataclass(frozen=True)
class DeckMemorySessionSummary:
    analysis_session_id: int
    session_type: str
    status: str
    started_at: str
    completed_at: str | None
    deck_hash: str
    commander_hash: str | None


@dataclass(frozen=True)
class DeckMemoryDetail:
    summary: DeckMemorySummary
    raw_input: str | None
    cards: tuple[DeckMemoryCard, ...]
    analysis_sessions: tuple[DeckMemorySessionSummary, ...]
    saved_analyses: tuple[DeckMemoryAnalysisSummary, ...]


def list_deck_memory(
    user_repository: UserRepository,
    filters: DeckMemoryFilters | None = None,
) -> tuple[DeckMemorySummary, ...]:
    """List remembered user decks without reading provider or analytics tables."""

    active_filters = filters or DeckMemoryFilters()
    rows = user_repository.list_user_decks_for_memory(
        commander_hash=active_filters.commander_hash,
        deck_hash=active_filters.deck_hash,
        include_temporary=active_filters.include_temporary,
        include_persistent=active_filters.include_persistent,
        created_at_from=active_filters.created_at_from,
        created_at_to=active_filters.created_at_to,
        limit=active_filters.limit,
    )
    return tuple(_summary_from_row(row) for row in rows)


def get_deck_memory_detail(
    user_repository: UserRepository,
    user_deck_id: int,
) -> DeckMemoryDetail:
    """Return a remembered user deck with imported cards and saved analysis metadata."""

    if user_deck_id < 1:
        raise DeckMemoryReadError("user_deck_id must be at least 1")

    row = user_repository.get_user_deck_memory_row(user_deck_id)
    if row is None:
        raise DeckMemoryReadError(f"Unknown user_deck_id: {user_deck_id}")

    return DeckMemoryDetail(
        summary=_summary_from_row(row),
        raw_input=row["raw_input"],
        cards=tuple(
            _card_from_row(card_row)
            for card_row in user_repository.list_user_deck_cards(user_deck_id)
        ),
        analysis_sessions=tuple(
            _session_from_row(session_row)
            for session_row in user_repository.list_analysis_sessions_for_deck(user_deck_id)
        ),
        saved_analyses=tuple(
            _analysis_from_row(analysis_row)
            for analysis_row in user_repository.list_saved_analysis_for_deck(user_deck_id)
        ),
    )


def _summary_from_row(row) -> DeckMemorySummary:
    return DeckMemorySummary(
        user_deck_id=row["user_deck_id"],
        deck_name=row["deck_name"],
        source_url=row["source_url"],
        deck_hash=row["deck_hash"],
        commander_hash=row["commander_hash"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        is_temporary=bool(row["is_temporary"]),
        card_count=int(row["card_count"]),
        saved_analysis_count=int(row["saved_analysis_count"]),
        latest_analysis_generated_at=row["latest_analysis_generated_at"],
    )


def _card_from_row(row) -> DeckMemoryCard:
    return DeckMemoryCard(
        raw_name=row["raw_name"],
        quantity=row["quantity"],
        zone=row["zone"],
        scryfall_id=row["scryfall_id"],
        oracle_id=row["oracle_id"],
        resolution_status=row["resolution_status"],
    )


def _analysis_from_row(row) -> DeckMemoryAnalysisSummary:
    return DeckMemoryAnalysisSummary(
        saved_analysis_id=row["saved_analysis_id"],
        analysis_type=row["analysis_type"],
        generated_at=row["generated_at"],
        report_path=row["report_path"],
        deck_hash=row["deck_hash"],
    )


def _session_from_row(row) -> DeckMemorySessionSummary:
    return DeckMemorySessionSummary(
        analysis_session_id=row["analysis_session_id"],
        session_type=row["session_type"],
        status=row["status"],
        started_at=row["started_at"],
        completed_at=row["completed_at"],
        deck_hash=row["deck_hash"],
        commander_hash=row["commander_hash"],
    )
