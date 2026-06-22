"""Parse EDHTop16 GraphQL payloads into Codie provider candidates."""

from __future__ import annotations

from typing import Any

from codie.providers.base import Provider
from codie.providers.errors import ParseError
from codie.providers.models import (
    RawPayload,
    SourceDeckCandidate,
    SourceDeckCardCandidate,
    SourceEventCandidate,
)

PROVIDER = "edhtop16"


def _required(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if payload.get(key) in (None, "", [])]
    if missing:
        raise ParseError(f"EDHTop16 payload missing required field(s): {', '.join(missing)}")


def _string(payload: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = payload.get(key)
        if value not in (None, ""):
            return str(value)
    return None


def _int(payload: dict[str, Any], *keys: str) -> int | None:
    value = _string(payload, *keys)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ParseError(f"Expected integer for {keys[0]}") from exc


def _float(payload: dict[str, Any], *keys: str) -> float | None:
    value = _string(payload, *keys)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError as exc:
        raise ParseError(f"Expected number for {keys[0]}") from exc


def _raw_payload(payload: dict[str, Any], object_type: str, provider_id: str, source_url: str | None) -> RawPayload:
    return RawPayload(
        provider=PROVIDER,
        object_type=object_type,
        provider_id=provider_id,
        source_url=source_url,
        retrieved_at=_string(payload, "retrieved_at") or "unknown",
        payload=payload,
    )


def _connection_nodes(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if not isinstance(value, dict):
        return []
    if isinstance(value.get("nodes"), list):
        return value["nodes"]
    if isinstance(value.get("edges"), list):
        return [edge.get("node") for edge in value["edges"] if isinstance(edge, dict)]
    return []


def _source_url(payload: dict[str, Any], object_type: str, object_id: str) -> str:
    return _string(payload, "source_url", "url", "bracketUrl") or f"https://edhtop16.com/{object_type}/{object_id}"


def _name_from_nested(payload: dict[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if isinstance(value, dict):
        return _string(value, "name", "displayName", "username")
    if isinstance(value, str):
        return value
    return None


class EDHTop16Provider(Provider):
    """EDHTop16 adapter that fetches/parses only and emits candidate models."""

    provider_name = PROVIDER

    def __init__(
        self,
        client: Any | None = None,
        *,
        tournament_filters: dict[str, Any] | None = None,
        deck_ids: tuple[str, ...] = (),
    ) -> None:
        self.client = client
        self.tournament_filters = tournament_filters or {}
        self.deck_ids = deck_ids

    def fetch(self) -> dict[str, Any]:
        if self.client is None:
            raise ParseError("EDHTop16Provider.fetch requires a client")
        return {
            "tournaments": self.fetch_tournaments(self.tournament_filters),
            "decklists": [self.fetch_decklist(deck_id) for deck_id in self.deck_ids],
        }

    def parse(self, payload: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
        if not isinstance(payload, dict):
            raise ParseError("EDHTop16 provider payload must be an object")
        events: list[SourceEventCandidate] = []
        decks: list[SourceDeckCandidate] = []
        for tournament in self._tournament_payloads(payload):
            event = self.parse_tournament(tournament)
            events.append(event)
            event_key = event.event_key or event.provider_event_id or ""
            for entry in self._entry_payloads(tournament):
                if self._is_entry_without_decklist(entry):
                    continue
                decks.append(self.parse_deck(entry, event_key))
        for deck_payload in self._standalone_deck_payloads(payload):
            if self._is_entry_without_decklist(deck_payload):
                continue
            event_key = self._event_key_from_deck_payload(deck_payload)
            decks.append(self.parse_deck(deck_payload, event_key))
        return {"events": tuple(events), "decks": tuple(decks)}

    def fetch_tournaments(self, filters: dict[str, Any] | None = None) -> dict[str, Any]:
        if self.client is None:
            raise ParseError("EDHTop16Provider.fetch_tournaments requires a client")
        return self.client.fetch_tournaments(filters or {})

    def fetch_decklist(self, deck_id: str) -> dict[str, Any]:
        if self.client is None:
            raise ParseError("EDHTop16Provider.fetch_decklist requires a client")
        return self.client.fetch_decklist(deck_id)

    def parse_tournament(self, raw: dict[str, Any] | None) -> SourceEventCandidate:
        if not isinstance(raw, dict):
            raise ParseError("EDHTop16 tournament payload must be an object")
        _required(raw, "TID", "name")
        event_id = str(raw["TID"])
        source_url = _source_url(raw, "tournament", event_id)
        entries = self._entry_payloads(raw)
        return SourceEventCandidate(
            provider=PROVIDER,
            provider_event_id=event_id,
            source_url=source_url,
            original_source="EDHTop16",
            original_source_url=source_url,
            event_name=_string(raw, "name", "event_name"),
            event_date=_string(raw, "tournamentDate", "event_date", "date"),
            format=_string(raw, "format"),
            region=_string(raw, "region", "state"),
            country=_string(raw, "country"),
            store_tag=_string(raw, "store_tag", "venue"),
            language=_string(raw, "language"),
            player_count=_int(raw, "size", "player_count"),
            deck_count=len(entries) if entries else _int(raw, "deck_count", "size"),
            raw_payload=_raw_payload(raw, "event", event_id, source_url),
            event_key=event_id,
        )

    def parse_deck(self, raw: dict[str, Any] | None, event_key: str) -> SourceDeckCandidate:
        if not isinstance(raw, dict):
            raise ParseError("EDHTop16 deck payload must be an object")
        _required(raw, "id")
        deck_id = str(raw["id"])
        commander_text = self._commander_text(raw)
        if commander_text in (None, ""):
            raise ParseError("EDHTop16 payload missing required field(s): commander")
        source_url = self._deck_source_url(raw, deck_id)
        cards = tuple(self._parse_cards(raw, deck_id))
        return SourceDeckCandidate(
            provider=PROVIDER,
            provider_deck_id=deck_id,
            source_event_key=event_key,
            source_url=source_url,
            download_url=self._deck_download_url(raw),
            deck_title=_string(raw, "deck_title", "deckTitle"),
            commander_text=commander_text,
            pilot_name=_string(raw, "pilot_name", "playerName") or _name_from_nested(raw, "player"),
            rank=_int(raw, "rank", "standing", "placement"),
            rank_label=_string(raw, "rank_label") or _string(raw, "standing"),
            record=self._record(raw),
            win_rate=_float(raw, "winRate", "win_rate"),
            archetype_name=_string(raw, "archetype_name", "archetype"),
            raw_payload=_raw_payload(raw, "deck", deck_id, source_url),
            deck_key=deck_id,
            cards=cards,
        )

    def _tournament_payloads(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
        candidates: list[Any] = []
        if isinstance(data.get("tournament"), dict):
            candidates.append(data["tournament"])
        candidates.extend(_connection_nodes(data.get("tournaments")))
        nested_tournaments = payload.get("tournaments")
        if isinstance(nested_tournaments, dict) and (
            "data" in nested_tournaments or "tournament" in nested_tournaments or "TID" in nested_tournaments
        ):
            candidates.extend(self._tournament_payloads(nested_tournaments))
        else:
            candidates.extend(_connection_nodes(nested_tournaments))
        if "TID" in payload or "name" in payload:
            candidates.append(payload)
        return [candidate for candidate in candidates if isinstance(candidate, dict)]

    def _standalone_deck_payloads(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
        candidates: list[Any] = []
        if isinstance(data.get("entry"), dict):
            candidates.append(data["entry"])
        if isinstance(data.get("node"), dict):
            candidates.append(data["node"])
        candidates.extend(self._nested_deck_payloads(payload.get("decklists")))
        candidates.extend(self._nested_deck_payloads(payload.get("decks")))
        return [candidate for candidate in candidates if isinstance(candidate, dict)]

    def _nested_deck_payloads(self, value: Any) -> list[dict[str, Any]]:
        candidates: list[Any] = []
        for item in _connection_nodes(value):
            if not isinstance(item, dict):
                continue
            nested = self._standalone_deck_payloads(item)
            candidates.extend(nested or [item])
        return [candidate for candidate in candidates if isinstance(candidate, dict)]

    def _entry_payloads(self, tournament: dict[str, Any]) -> list[dict[str, Any]]:
        entries = tournament.get("entries")
        nodes = _connection_nodes(entries)
        return [entry for entry in nodes if isinstance(entry, dict)]

    def _is_entry_without_decklist(self, entry: Any) -> bool:
        if not isinstance(entry, dict):
            return True
        return (
            self._deck_download_url(entry) is None
            and not self._parse_card_entries(entry)
        )

    def _event_key_from_deck_payload(self, payload: dict[str, Any]) -> str:
        tournament = payload.get("tournament")
        if isinstance(tournament, dict):
            return _string(tournament, "TID", "event_key") or ""
        return _string(payload, "source_event_key", "event_key", "TID") or ""

    def _deck_source_url(self, raw: dict[str, Any], deck_id: str) -> str:
        return _string(raw, "source_url", "url", "deckUrl", "decklistUrl") or f"https://edhtop16.com/entry/{deck_id}"

    def _deck_download_url(self, raw: dict[str, Any]) -> str | None:
        decklist = _string(raw, "download_url", "deckUrl", "decklistUrl", "decklist")
        if decklist and decklist.startswith(("http://", "https://")):
            return decklist
        return None

    def _commander_text(self, raw: dict[str, Any]) -> str | None:
        direct = _string(raw, "commander_text", "commanderText", "commanderName")
        if direct:
            return direct
        nested = _name_from_nested(raw, "commander")
        if nested:
            return nested
        commanders = raw.get("commanders")
        if isinstance(commanders, list):
            names = [card.get("name") if isinstance(card, dict) else str(card) for card in commanders]
            names = [name for name in names if name]
            return " / ".join(names) if names else None
        return None

    def _record(self, raw: dict[str, Any]) -> str | None:
        if _string(raw, "record"):
            return _string(raw, "record")
        wins = _int(raw, "wins")
        losses = _int(raw, "losses")
        if wins is None:
            wins = (_int(raw, "winsSwiss") or 0) + (_int(raw, "winsBracket") or 0)
        if losses is None:
            losses = (_int(raw, "lossesSwiss") or 0) + (_int(raw, "lossesBracket") or 0)
        draws = _int(raw, "draws")
        if wins is None or losses is None or draws is None:
            return None
        return f"{wins}-{losses}-{draws}"

    def _parse_cards(self, raw: dict[str, Any], deck_id: str) -> list[SourceDeckCardCandidate]:
        entries = self._parse_card_entries(raw)
        cards: list[SourceDeckCardCandidate] = []
        for index, entry in enumerate(entries, start=1):
            name = _string(entry, "name", "cardName")
            if not name:
                raise ParseError("EDHTop16 deck card entry missing required field(s): name")
            quantity = _int(entry, "quantity", "count") or 1
            zone = _string(entry, "zone", "board") or "mainboard"
            cards.append(
                SourceDeckCardCandidate(
                    source_deck_key=deck_id,
                    raw_name=name,
                    quantity=quantity,
                    source_zone=zone.lower(),
                    source_order=index,
                    raw_entry=str(entry),
                )
            )
        return cards

    def _parse_card_entries(self, raw: dict[str, Any]) -> list[dict[str, Any]]:
        cards = raw.get("cards")
        if cards is None:
            cards = raw.get("maindeck")
        if cards in (None, []):
            return []
        if not isinstance(cards, list):
            raise ParseError("EDHTop16 deck cards must be a list")
        entries: list[dict[str, Any]] = []
        for card in cards:
            if isinstance(card, str):
                entries.append({"name": card, "quantity": 1, "zone": "mainboard"})
            elif isinstance(card, dict):
                entry = dict(card)
                entry.setdefault("quantity", 1)
                entry.setdefault("zone", "mainboard")
                entries.append(entry)
            else:
                raise ParseError("EDHTop16 deck card entry must be an object or string")
        return entries
