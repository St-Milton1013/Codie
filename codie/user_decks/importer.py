"""Import local user deck text for temporary analysis sessions."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

from codie.cards.lookup import CardLookup
from codie.canonical.signature import commander_signature
from codie.db.repositories.base import BaseRepository
from codie.db.repositories.user import UserRepository


_CARD_LINE_RE = re.compile(r"^\s*(?P<quantity>\d+)\s+(?P<name>.+?)\s*$")
_IGNORED_HEADERS = {"deck", "main", "mainboard", "cards"}
_COMMANDER_HEADERS = {"commander", "commanders", "partner", "partners"}
_SIDEBOARD_HEADERS = {"sideboard", "maybeboard", "considering"}


class UserDeckImportError(ValueError):
    """Raised when a user deck cannot be imported safely."""


@dataclass(frozen=True)
class ParsedUserDeckCard:
    raw_name: str
    quantity: int
    zone: str
    source_order: int
    raw_entry: str


@dataclass(frozen=True)
class ParsedUserDeck:
    deck_name: str | None
    raw_input: str
    cards: tuple[ParsedUserDeckCard, ...]


@dataclass(frozen=True)
class UserDeckImportResult:
    user_deck_id: int
    analysis_session_id: int
    deck_hash: str
    commander_hash: str | None
    card_count: int
    unresolved_names: tuple[str, ...]


def parse_user_deck_text(raw_input: str, *, deck_name: str | None = None) -> ParsedUserDeck:
    """Parse a simple quantity/name decklist into importable card rows."""

    if not raw_input or not raw_input.strip():
        raise UserDeckImportError("Deck input is empty")

    cards: list[ParsedUserDeckCard] = []
    zone = "mainboard"
    source_order = 1
    for raw_line in raw_input.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#") or line.startswith("//"):
            continue
        header = line.rstrip(":").strip().lower()
        if header in _COMMANDER_HEADERS:
            zone = "commander"
            continue
        if header in _SIDEBOARD_HEADERS:
            zone = "sideboard"
            continue
        if header in _IGNORED_HEADERS:
            zone = "mainboard"
            continue

        match = _CARD_LINE_RE.match(line)
        if match is None:
            raise UserDeckImportError(f"Malformed deck line: {line}")
        quantity = int(match.group("quantity"))
        if quantity <= 0:
            raise UserDeckImportError(f"Invalid quantity for line: {line}")
        name = match.group("name").strip()
        if not name:
            raise UserDeckImportError(f"Missing card name for line: {line}")
        cards.append(
            ParsedUserDeckCard(
                raw_name=name,
                quantity=quantity,
                zone=zone,
                source_order=source_order,
                raw_entry=line,
            )
        )
        source_order += 1

    if not cards:
        raise UserDeckImportError("Deck input contains no cards")
    return ParsedUserDeck(deck_name=deck_name, raw_input=raw_input, cards=tuple(cards))


def _stable_deck_hash(cards: tuple[ParsedUserDeckCard, ...]) -> str:
    rows = [
        {
            "name": card.raw_name.strip().lower(),
            "quantity": card.quantity,
            "zone": card.zone,
        }
        for card in sorted(cards, key=lambda item: (item.zone, item.raw_name.lower(), item.quantity))
    ]
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


class UserDeckImporter:
    """Resolve and persist a local deck as an atomic analysis-session import."""

    def __init__(self, user_repository: UserRepository, card_lookup: CardLookup) -> None:
        self.user_repository = user_repository
        self.card_lookup = card_lookup

    def import_text(
        self,
        raw_input: str,
        *,
        deck_name: str | None = None,
        source_url: str | None = None,
        session_type: str = "deck_import",
        is_temporary: bool = True,
    ) -> UserDeckImportResult:
        parsed = parse_user_deck_text(raw_input, deck_name=deck_name)
        return self.import_parsed(
            parsed,
            source_url=source_url,
            session_type=session_type,
            is_temporary=is_temporary,
        )

    def import_parsed(
        self,
        parsed: ParsedUserDeck,
        *,
        source_url: str | None = None,
        session_type: str = "deck_import",
        is_temporary: bool = True,
    ) -> UserDeckImportResult:
        resolved_rows = []
        unresolved = []
        commander_names = []
        for card in parsed.cards:
            result = self.card_lookup.resolve(card.raw_name)
            if result.card is None:
                unresolved.append(card.raw_name)
                continue
            if card.zone == "commander":
                commander_names.append(result.card["name"])
            resolved_rows.append((card, result))

        if unresolved:
            joined = ", ".join(unresolved)
            raise UserDeckImportError(f"Unresolved card(s): {joined}")

        commander_hash = commander_signature(commander_names) if commander_names else None
        deck_hash = _stable_deck_hash(parsed.cards)
        now = self.user_repository.now()
        connection = self.user_repository.connection
        with BaseRepository.transaction(connection, "user_deck_import"):
            user_deck_id = self.user_repository.create_user_deck(
                {
                    "deck_name": parsed.deck_name,
                    "source_url": source_url,
                    "deck_hash": deck_hash,
                    "commander_hash": commander_hash,
                    "raw_input": parsed.raw_input,
                    "created_at": now,
                    "updated_at": now,
                    "is_temporary": 1 if is_temporary else 0,
                }
            )
            for card, result in resolved_rows:
                self.user_repository.add_user_deck_card(
                    {
                        "user_deck_id": user_deck_id,
                        "scryfall_id": result.card["scryfall_id"],
                        "oracle_id": result.card["oracle_id"],
                        "raw_name": card.raw_name,
                        "quantity": card.quantity,
                        "zone": card.zone,
                        "resolution_status": result.status,
                    }
                )
            analysis_session_id = self.user_repository.create_analysis_session(
                {
                    "user_deck_id": user_deck_id,
                    "deck_hash": deck_hash,
                    "commander_hash": commander_hash,
                    "session_type": session_type,
                    "status": "created",
                    "started_at": now,
                    "config_json": "{}",
                }
            )

        return UserDeckImportResult(
            user_deck_id=user_deck_id,
            analysis_session_id=analysis_session_id,
            deck_hash=deck_hash,
            commander_hash=commander_hash,
            card_count=sum(card.quantity for card in parsed.cards),
            unresolved_names=tuple(unresolved),
        )
