"""Parse TopDeck fixture/API payloads into Codie provider candidates."""

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

PROVIDER = "topdeck"
CARD_ZONE_ALIASES = {
    "commander": "commanders",
    "commanders": "commanders",
    "main": "mainboard",
    "mainboard": "mainboard",
    "maindeck": "mainboard",
    "side": "sideboard",
    "sideboard": "sideboard",
    "maybe": "maybeboard",
    "maybeboard": "maybeboard",
    "companion": "companion",
    "companions": "companion",
}


def _required(payload: dict[str, Any], *keys: str) -> None:
    missing = [key for key in keys if payload.get(key) in (None, "", [])]
    if missing:
        raise ParseError(f"TopDeck payload missing required field(s): {', '.join(missing)}")


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


def _source_url(payload: dict[str, Any], object_type: str, object_id: str) -> str:
    return _string(payload, "source_url", "url") or f"https://topdeck.gg/{object_type}/{object_id}"


def _raw_payload(payload: dict[str, Any], object_type: str, provider_id: str, source_url: str) -> RawPayload:
    return RawPayload(
        provider=PROVIDER,
        object_type=object_type,
        provider_id=provider_id,
        source_url=source_url,
        retrieved_at=_string(payload, "retrieved_at") or "unknown",
        payload=payload,
    )


class TopDeckProvider(Provider):
    """TopDeck adapter that fetches/parses only and emits candidate models."""

    provider_name = PROVIDER

    def __init__(self, client: Any | None = None, *, event_id: str | None = None, deck_ids: tuple[str, ...] = ()) -> None:
        self.client = client
        self.event_id = event_id
        self.deck_ids = deck_ids

    def fetch(self) -> dict[str, Any]:
        if self.client is None or self.event_id is None:
            raise ParseError("TopDeckProvider.fetch requires a client and event_id")
        return {
            "event": self.fetch_event(self.event_id),
            "decks": [self.fetch_deck(deck_id) for deck_id in self.deck_ids],
        }

    def parse(self, payload: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
        if not isinstance(payload, dict):
            raise ParseError("TopDeck provider payload must be an object")
        event_payload = payload.get("event") or payload
        event = self.parse_event(event_payload)
        deck_payloads = payload.get("decks")
        if deck_payloads is None and "standings" in event_payload:
            deck_payloads = event_payload.get("standings") or ()
        decks = []
        for deck_payload in deck_payloads or ():
            if self._is_standing_without_deck(deck_payload):
                continue
            decks.extend(self.parse_deck(deck_payload, event.event_key or event.provider_event_id or ""))
        return {"events": (event,), "decks": tuple(decks)}

    def fetch_event(self, event_id: str) -> dict[str, Any]:
        if self.client is None:
            raise ParseError("TopDeckProvider.fetch_event requires a client")
        return self.client.fetch_event(event_id)

    def fetch_deck(self, deck_id: str) -> dict[str, Any]:
        if self.client is None:
            raise ParseError("TopDeckProvider.fetch_deck requires a client")
        return self.client.fetch_deck(deck_id)

    def parse_event(self, raw: dict[str, Any] | None) -> SourceEventCandidate:
        if not isinstance(raw, dict):
            raise ParseError("TopDeck event payload must be an object")
        data = raw.get("data") if isinstance(raw.get("data"), dict) else raw
        location = data.get("location") if isinstance(data.get("location"), dict) else {}
        event_data = data.get("eventData") if isinstance(data.get("eventData"), dict) else {}
        if "tid" in data or "name" in data:
            _required(data, "tid", "name")
        elif "TID" in data or "tournamentName" in data:
            _required(data, "TID", "tournamentName")
        else:
            _required(data, "event_id", "event_name")
        event_id = str(_string(data, "tid", "TID", "event_id"))
        source_url = _source_url(raw, "event", event_id)
        standings = raw.get("standings") if isinstance(raw.get("standings"), list) else data.get("standings")
        deck_count = len(standings) if isinstance(standings, list) else _int(data, "deck_count", "decks_count")
        return SourceEventCandidate(
            provider=PROVIDER,
            provider_event_id=event_id,
            source_url=source_url,
            original_source=_string(raw, "original_source") or "TopDeck",
            original_source_url=_string(raw, "original_source_url") or source_url,
            event_name=_string(data, "event_name", "name", "tournamentName"),
            event_date=_string(data, "event_date", "date", "startDate"),
            format=_string(data, "format"),
            region=_string(data, "region", "state") or _string(location, "state") or _string(event_data, "state"),
            country=_string(data, "country") or _string(location, "country"),
            store_tag=_string(data, "store_tag", "venue") or _string(location, "name") or _string(event_data, "address"),
            language=_string(data, "language"),
            player_count=_int(data, "player_count", "players", "participantCount"),
            deck_count=deck_count,
            raw_payload=_raw_payload(raw, "event", event_id, source_url),
            event_key=event_id,
        )

    def parse_deck(self, raw: dict[str, Any] | None, event_key: str) -> list[SourceDeckCandidate]:
        if not isinstance(raw, dict):
            raise ParseError("TopDeck deck payload must be an object")
        deck_payloads = raw.get("decks") if isinstance(raw.get("decks"), list) else [raw]
        return [self._parse_one_deck(deck, event_key) for deck in deck_payloads]

    def _parse_one_deck(self, raw: dict[str, Any], event_key: str) -> SourceDeckCandidate:
        if not isinstance(raw, dict):
            raise ParseError("TopDeck deck entry must be an object")
        _required(raw, "deck_id", "commander_text") if "deck_id" in raw or "commander_text" in raw else _required(raw, "id", "deckObj")
        deck_id = str(_string(raw, "deck_id", "id"))
        source_url = _source_url(raw, "deck", deck_id)
        cards = tuple(self._parse_cards(raw, deck_id))
        commander_text = _string(raw, "commander_text", "commander") or self._commander_text_from_cards(cards)
        return SourceDeckCandidate(
            provider=PROVIDER,
            provider_deck_id=deck_id,
            source_event_key=event_key,
            source_url=source_url,
            download_url=_string(raw, "download_url", "decklist_url"),
            deck_title=_string(raw, "deck_title"),
            commander_text=commander_text,
            pilot_name=_string(raw, "pilot_name", "player", "name"),
            rank=_int(raw, "rank", "placement", "standing"),
            rank_label=_string(raw, "rank_label", "placement_label") or _string(raw, "standing"),
            record=_string(raw, "record"),
            win_rate=_float(raw, "win_rate", "winRate", "successRate"),
            archetype_name=_string(raw, "archetype_name", "archetype"),
            raw_payload=_raw_payload(raw, "deck", deck_id, source_url),
            deck_key=deck_id,
            cards=cards,
        )

    def _parse_cards(self, raw: dict[str, Any], deck_id: str) -> list[SourceDeckCardCandidate]:
        entries = raw.get("cards")
        if entries is None and isinstance(raw.get("deckObj"), dict):
            entries = self._entries_from_deck_obj(raw["deckObj"])
        if entries in (None, []):
            raise ParseError("TopDeck deck payload missing required field(s): cards")
        if not isinstance(entries, list):
            raise ParseError("TopDeck deck cards must be a list")
        cards = []
        for index, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                raise ParseError("TopDeck deck card entry must be an object")
            _required(entry, "name")
            quantity = _int(entry, "quantity", "count") or 1
            zone = self._normalize_card_zone(_string(entry, "zone", "board")) or "mainboard"
            cards.append(
                SourceDeckCardCandidate(
                    source_deck_key=deck_id,
                    raw_name=str(entry["name"]),
                    quantity=quantity,
                    source_zone=zone,
                    source_order=index,
                    raw_entry=str(entry),
                )
            )
        return cards

    def _is_standing_without_deck(self, payload: Any) -> bool:
        if not isinstance(payload, dict):
            return False
        if payload.get("cards") not in (None, []):
            return False
        deck_obj = payload.get("deckObj")
        if not isinstance(deck_obj, dict):
            return True
        return not self._entries_from_deck_obj(deck_obj)

    def _entries_from_deck_obj(self, deck_obj: dict[str, Any]) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        for zone, cards in deck_obj.items():
            normalized_zone = self._normalize_card_zone(str(zone))
            if normalized_zone is None:
                continue
            if isinstance(cards, dict):
                for name, value in cards.items():
                    if isinstance(value, dict):
                        quantity = value.get("quantity") or value.get("count") or 1
                    else:
                        quantity = value
                    entries.append({"name": name, "quantity": quantity or 1, "zone": normalized_zone})
            elif isinstance(cards, list):
                for card in cards:
                    if isinstance(card, dict):
                        entry = dict(card)
                        entry["zone"] = normalized_zone
                        entries.append(entry)
        return entries

    def _commander_text_from_cards(self, cards: tuple[SourceDeckCardCandidate, ...]) -> str | None:
        commanders = [card.raw_name for card in cards if card.source_zone.lower() == "commanders"]
        return " / ".join(commanders) if commanders else None

    def _normalize_card_zone(self, zone: str | None) -> str | None:
        if zone is None:
            return None
        return CARD_ZONE_ALIASES.get(zone.lower().strip())
