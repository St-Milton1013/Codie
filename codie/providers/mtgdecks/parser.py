"""Parse MTGDecks HTML/text payloads into Codie provider candidates."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup, Tag

from codie.providers.base import Provider
from codie.providers.errors import MissingRequiredFieldError, ParseError, SchemaValidationError
from codie.providers.models import (
    RawPayload,
    SourceDeckCandidate,
    SourceDeckCardCandidate,
    SourceEventCandidate,
)

PROVIDER = "mtgdecks"
BASE_URL = "https://mtgdecks.net"
UNAVAILABLE_MARKERS = (
    "decklist unavailable",
    "decklist not available",
    "no decklist available",
    "private decklist",
)
ZONE_ALIASES = {
    "commander": "commanders",
    "commanders": "commanders",
    "main": "mainboard",
    "maindeck": "mainboard",
    "main deck": "mainboard",
    "mainboard": "mainboard",
    "side": "sideboard",
    "sideboard": "sideboard",
    "side board": "sideboard",
    "maybeboard": "maybeboard",
    "auxiliary": "auxiliary",
    "stickers": "auxiliary",
    "attractions": "auxiliary",
}


def _string(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value).strip()


def _int(value: Any) -> int | None:
    text = _string(value)
    if text is None:
        return None
    match = re.search(r"\d+", text.replace(",", ""))
    return int(match.group(0)) if match else None


def _float(value: Any) -> float | None:
    text = _string(value)
    if text is None:
        return None
    try:
        return float(text.rstrip("%")) / 100 if text.endswith("%") else float(text)
    except ValueError as exc:
        raise ParseError("Expected numeric value") from exc


def _parse_html(payload: str) -> BeautifulSoup:
    soup = BeautifulSoup(payload, "html.parser")
    if not soup.find(("html", "body", "main", "article", "table")):
        raise ParseError("MTGDecks HTML payload does not contain parseable page structure")
    return soup


def _looks_like_html(payload: str) -> bool:
    return isinstance(payload, str) and "<" in payload and ">" in payload


def _canonical_url(root: BeautifulSoup | Tag) -> str | None:
    link = root.find("link", rel=lambda value: value == "canonical" or (isinstance(value, list) and "canonical" in value))
    if isinstance(link, Tag) and link.get("href"):
        return str(link["href"])
    anchor = root.find("a", attrs={"data-source-url": True})
    if isinstance(anchor, Tag):
        return _string(anchor.get("data-source-url"))
    return None


def _query_value(url: str | None, key: str) -> str | None:
    if not url:
        return None
    values = parse_qs(urlparse(url).query).get(key)
    return values[0] if values else None


def _path_id(url: str | None) -> str | None:
    if not url:
        return None
    match = re.search(r"(\d+)(?:/?$|[/?#])", urlparse(url).path)
    return match.group(1) if match else None


def _raw_payload(payload: str, object_type: str, provider_id: str | None, source_url: str | None) -> RawPayload:
    return RawPayload(
        provider=PROVIDER,
        object_type=object_type,
        provider_id=provider_id,
        source_url=source_url,
        retrieved_at="unknown",
        payload=payload,
    )


def _field(fields: dict[str, str], *keys: str) -> str | None:
    for key in keys:
        value = fields.get(key)
        if value not in (None, ""):
            return value
    return None


def _require(value: str | None, label: str) -> str:
    if value in (None, ""):
        raise MissingRequiredFieldError(f"MTGDecks payload missing required field(s): {label}")
    return value


def _field_map_from_html(root: BeautifulSoup | Tag) -> dict[str, str]:
    fields: dict[str, str] = {}
    for node in root.find_all(attrs={"data-field": True}):
        value = node.get("content") or node.get("value") or node.get_text(" ", strip=True)
        if value:
            fields[str(node["data-field"]).strip().lower()] = str(value).strip()
    for row in root.find_all("tr"):
        cells = row.find_all(["th", "td"], recursive=False)
        if len(cells) >= 2:
            key = cells[0].get_text(" ", strip=True).lower().rstrip(":")
            value = cells[1].get_text(" ", strip=True)
            if key and value:
                fields.setdefault(key, value)
    return fields


def _field_map_from_text(payload: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in payload.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower().replace(" ", "_")
        value = value.strip()
        if key and value and not key.startswith("["):
            fields.setdefault(key, value)
    return fields


def _first_text(root: BeautifulSoup | Tag, *classes: str) -> str | None:
    for class_name in classes:
        node = root.select_one(f".{class_name}")
        if node and node.get_text(" ", strip=True):
            return node.get_text(" ", strip=True)
    return None


class MTGDecksProvider(Provider):
    """MTGDecks adapter that fetches/parses only and emits candidate models."""

    provider_name = PROVIDER

    def __init__(self, client: Any | None = None, *, event_url: str | None = None, deck_urls: tuple[str, ...] = ()) -> None:
        self.client = client
        self.event_url = event_url
        self.deck_urls = deck_urls

    def fetch(self) -> dict[str, Any]:
        if self.client is None or self.event_url is None:
            raise ParseError("MTGDecksProvider.fetch requires a client and event_url")
        return {
            "event_page": self.fetch_event_page(self.event_url),
            "deck_pages": [self.fetch_deck_page(deck_url) for deck_url in self.deck_urls],
        }

    def parse(self, payload: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
        if not isinstance(payload, dict):
            raise ParseError("MTGDecks provider payload must be an object")
        events: list[SourceEventCandidate] = []
        decks: list[SourceDeckCandidate] = []
        event_key = ""
        event_payload = payload.get("event_page") or payload.get("event_html") or payload.get("event")
        if event_payload is not None:
            event = self.parse_event_page(event_payload)
            events.append(event)
            event_key = event.event_key or event.provider_event_id or ""
        for deck_payload in payload.get("deck_pages") or payload.get("decks") or ():
            if self._is_unavailable_decklist(deck_payload):
                continue
            decks.append(self.parse_deck_page(deck_payload, event_key))
        return {"events": tuple(events), "decks": tuple(decks)}

    def fetch_event_page(self, event_url: str) -> str:
        if self.client is None:
            raise ParseError("MTGDecksProvider.fetch_event_page requires a client")
        return self.client.fetch_event_page(event_url)

    def fetch_deck_page(self, deck_url: str) -> str:
        if self.client is None:
            raise ParseError("MTGDecksProvider.fetch_deck_page requires a client")
        return self.client.fetch_deck_page(deck_url)

    def parse_event_page(self, html: str) -> SourceEventCandidate:
        if not isinstance(html, str) or not _looks_like_html(html):
            raise ParseError("MTGDecks event payload must be HTML")
        root = _parse_html(html)
        fields = _field_map_from_html(root)
        source_url = _field(fields, "source_url", "page_url") or _canonical_url(root)
        event_id = _field(fields, "event_id", "event id") or _query_value(source_url, "event") or _query_value(source_url, "e") or _path_id(source_url)
        event_id = _require(event_id, "event_id")
        event_name = _field(fields, "event_name", "event", "name") or _first_text(root, "event-title", "event-name")
        if not event_name:
            raise ParseError("MTGDecks event page missing parseable event name")
        return SourceEventCandidate(
            provider=PROVIDER,
            provider_event_id=event_id,
            source_url=source_url or f"{BASE_URL}/events/{event_id}",
            original_source="MTGDecks",
            original_source_url=_field(fields, "original_source_url", "source") or source_url,
            event_name=event_name,
            event_date=_field(fields, "event_date", "date"),
            format=_field(fields, "format"),
            region=_field(fields, "region", "state"),
            country=_field(fields, "country"),
            store_tag=_field(fields, "store_tag", "venue", "location"),
            language=_field(fields, "language"),
            player_count=_int(_field(fields, "player_count", "players")),
            deck_count=_int(_field(fields, "deck_count", "decks")),
            raw_payload=_raw_payload(html, "event", event_id, source_url),
            event_key=event_id,
        )

    def parse_deck_page(self, payload: str, event_key: str) -> SourceDeckCandidate:
        if not isinstance(payload, str) or not payload.strip():
            raise ParseError("MTGDecks deck payload must be text or HTML")
        fields, root = self._deck_fields(payload)
        source_url = _field(fields, "source_url", "page_url") or (_canonical_url(root) if root else None)
        deck_id = _field(fields, "deck_id", "deck id") or _query_value(source_url, "deck") or _query_value(source_url, "d") or _path_id(source_url)
        deck_id = _require(deck_id, "deck_id")
        cards = tuple(self._parse_cards(payload, root, deck_id))
        if not cards and not self._is_unavailable_decklist(payload):
            raise SchemaValidationError("MTGDecks deck payload did not expose a supported decklist structure")
        commander_text = _field(fields, "commander_text", "commander")
        if commander_text is None:
            commander_text = self._commander_from_cards(cards)
        return SourceDeckCandidate(
            provider=PROVIDER,
            provider_deck_id=deck_id,
            source_event_key=event_key,
            source_url=source_url or f"{BASE_URL}/decks/{deck_id}",
            download_url=_field(fields, "download_url", "deck_url", "export_url"),
            deck_title=_field(fields, "deck_title", "deck", "name") or (_first_text(root, "deck-title", "deck-name") if root else None),
            commander_text=commander_text,
            pilot_name=_field(fields, "pilot_name", "pilot", "player"),
            rank=_int(_field(fields, "rank", "placement", "place")),
            rank_label=_field(fields, "rank_label", "placement", "place"),
            record=_field(fields, "record"),
            win_rate=_float(_field(fields, "win_rate", "winrate")),
            archetype_name=_field(fields, "archetype_name", "archetype"),
            raw_payload=_raw_payload(payload, "deck", deck_id, source_url),
            deck_key=deck_id,
            cards=cards,
        )

    def _deck_fields(self, payload: str) -> tuple[dict[str, str], BeautifulSoup | None]:
        if _looks_like_html(payload):
            root = _parse_html(payload)
            return _field_map_from_html(root), root
        if not self._looks_like_text_export(payload):
            raise ParseError("MTGDecks text payload does not contain parseable export structure")
        return _field_map_from_text(payload), None

    def _looks_like_text_export(self, payload: str) -> bool:
        text = payload.lower()
        return "deck id:" in text or "source url:" in text or "[mainboard]" in text or "[commander]" in text

    def _is_unavailable_decklist(self, payload: Any) -> bool:
        if not isinstance(payload, str):
            return True
        text = re.sub(r"\s+", " ", payload).lower()
        return any(marker in text for marker in UNAVAILABLE_MARKERS)

    def _parse_cards(self, payload: str, root: BeautifulSoup | None, deck_id: str) -> list[SourceDeckCardCandidate]:
        entries = self._card_entries_from_html(root) if root is not None else self._card_entries_from_text(payload)
        cards: list[SourceDeckCardCandidate] = []
        for entry in entries:
            name = entry["name"]
            quantity = int(entry["quantity"])
            zone = entry["zone"]
            cards.append(
                SourceDeckCardCandidate(
                    source_deck_key=deck_id,
                    raw_name=name,
                    quantity=quantity,
                    source_zone=zone,
                    source_order=len(cards) + 1,
                    raw_entry=entry["raw_entry"],
                )
            )
        return cards

    def _card_entries_from_html(self, root: BeautifulSoup | None) -> list[dict[str, Any]]:
        if root is None:
            return []
        entries: list[dict[str, Any]] = []
        for section in root.select(".deck-section[data-zone], .card-section[data-zone]"):
            zone = self._normalize_zone(str(section.get("data-zone")))
            if zone is None:
                continue
            for row in section.select(".card-row, .deck-card"):
                quantity, name = self._parse_card_text(row.get_text(" ", strip=True))
                name_node = row.select_one(".card-name, .card")
                if name_node:
                    name = name_node.get_text(" ", strip=True)
                if name is None:
                    raise SchemaValidationError("MTGDecks card row is missing a card name")
                entries.append({"name": name, "quantity": quantity, "zone": zone, "raw_entry": row.get_text(" ", strip=True)})
        return entries

    def _card_entries_from_text(self, payload: str) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        current_zone: str | None = None
        for raw_line in payload.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            section = re.match(r"^\[(.+?)\]$", line)
            if section:
                current_zone = self._normalize_zone(section.group(1))
                continue
            if current_zone is None or ":" in line:
                continue
            quantity, name = self._parse_card_text(line)
            if name is None:
                raise SchemaValidationError("MTGDecks card line is missing a card name")
            entries.append({"name": name, "quantity": quantity, "zone": current_zone, "raw_entry": raw_line})
        return entries

    def _parse_card_text(self, text: str) -> tuple[int, str | None]:
        match = re.match(r"^\s*(\d+)\s+(.+?)\s*$", text)
        if match:
            return int(match.group(1)), match.group(2).strip()
        stripped = text.strip()
        return 1, stripped or None

    def _commander_from_cards(self, cards: tuple[SourceDeckCardCandidate, ...]) -> str | None:
        commanders = [card.raw_name for card in cards if card.source_zone == "commanders"]
        return " / ".join(commanders) if commanders else None

    def _normalize_zone(self, zone: str) -> str | None:
        return ZONE_ALIASES.get(zone.lower().strip())
