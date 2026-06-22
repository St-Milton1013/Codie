"""Parse MTGTop8 HTML payloads into Codie provider candidates."""

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

PROVIDER = "mtgtop8"
BASE_URL = "https://www.mtgtop8.com"

def _parse_html(html: str) -> BeautifulSoup:
    if not isinstance(html, str) or "<" not in html or ">" not in html:
        raise ParseError("MTGTop8 HTML payload must be an HTML string")
    soup = BeautifulSoup(html, "html.parser")
    if not soup.find(("html", "body", "main", "article", "table")):
        raise ParseError("MTGTop8 HTML payload does not contain parseable page structure")
    return soup


def _string(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value).strip()


def _int(value: Any) -> int | None:
    text = _string(value)
    if text is None:
        return None
    match = re.search(r"\d+", text.replace(",", ""))
    if not match:
        return None
    return int(match.group(0))


def _field_map(root: BeautifulSoup | Tag) -> dict[str, str]:
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


def _first_text(root: BeautifulSoup | Tag, *classes: str) -> str | None:
    for class_name in classes:
        node = root.select_one(f".{class_name}")
        if node and node.get_text(" ", strip=True):
            return node.get_text(" ", strip=True)
    return None


def _canonical_url(root: BeautifulSoup | Tag) -> str | None:
    link = root.find("link", rel=lambda value: value == "canonical" or (isinstance(value, list) and "canonical" in value))
    if isinstance(link, Tag) and link.get("href"):
        return str(link["href"])
    anchor = root.find("a", attrs={"data-source-url": True})
    if anchor:
        return str(anchor.get("data-source-url"))
    return None


def _query_value(url: str | None, key: str) -> str | None:
    if not url:
        return None
    values = parse_qs(urlparse(url).query).get(key)
    return values[0] if values else None


def _raw_payload(html: str, object_type: str, provider_id: str | None, source_url: str | None) -> RawPayload:
    return RawPayload(
        provider=PROVIDER,
        object_type=object_type,
        provider_id=provider_id,
        source_url=source_url,
        retrieved_at="unknown",
        payload=html,
    )


def _field(fields: dict[str, str], *keys: str) -> str | None:
    for key in keys:
        value = fields.get(key)
        if value not in (None, ""):
            return value
    return None


def _require(value: str | None, label: str) -> str:
    if value in (None, ""):
        raise MissingRequiredFieldError(f"MTGTop8 payload missing required field(s): {label}")
    return value


class MTGTop8Provider(Provider):
    """MTGTop8 adapter that fetches/parses only and emits candidate models."""

    provider_name = PROVIDER

    def __init__(self, client: Any | None = None, *, event_url: str | None = None, deck_urls: tuple[str, ...] = ()) -> None:
        self.client = client
        self.event_url = event_url
        self.deck_urls = deck_urls

    def fetch(self) -> dict[str, Any]:
        if self.client is None or self.event_url is None:
            raise ParseError("MTGTop8Provider.fetch requires a client and event_url")
        return {
            "event_page": self.fetch_event_page(self.event_url),
            "deck_pages": [self.fetch_deck_page(deck_url) for deck_url in self.deck_urls],
        }

    def parse(self, payload: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
        if not isinstance(payload, dict):
            raise ParseError("MTGTop8 provider payload must be an object")
        events: list[SourceEventCandidate] = []
        decks: list[SourceDeckCandidate] = []
        event_key = ""
        event_html = payload.get("event_page") or payload.get("event_html") or payload.get("event")
        if event_html is not None:
            event = self.parse_event_page(event_html)
            events.append(event)
            event_key = event.event_key or event.provider_event_id or ""
        for deck_html in payload.get("deck_pages") or payload.get("decks") or ():
            if self._is_unavailable_deck_page(deck_html):
                continue
            decks.append(self.parse_deck_page(deck_html, event_key))
        return {"events": tuple(events), "decks": tuple(decks)}

    def fetch_event_page(self, event_url: str) -> str:
        if self.client is None:
            raise ParseError("MTGTop8Provider.fetch_event_page requires a client")
        return self.client.fetch_event_page(event_url)

    def fetch_deck_page(self, deck_url: str) -> str:
        if self.client is None:
            raise ParseError("MTGTop8Provider.fetch_deck_page requires a client")
        return self.client.fetch_deck_page(deck_url)

    def parse_event_page(self, html: str) -> SourceEventCandidate:
        root = _parse_html(html)
        fields = _field_map(root)
        source_url = _field(fields, "source_url", "page_url") or _canonical_url(root)
        event_id = _field(fields, "event_id", "event id") or _query_value(source_url, "e")
        event_id = _require(event_id, "event_id")
        event_name = _field(fields, "event_name", "event", "name") or _first_text(root, "event-title", "event-name")
        if not event_name:
            raise ParseError("MTGTop8 event page missing parseable event name")
        original_source_url = _field(fields, "original_source_url", "source") or source_url
        return SourceEventCandidate(
            provider=PROVIDER,
            provider_event_id=event_id,
            source_url=source_url or f"{BASE_URL}/event?e={event_id}",
            original_source="MTGTop8",
            original_source_url=original_source_url,
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

    def parse_deck_page(self, html: str, event_key: str) -> SourceDeckCandidate:
        root = _parse_html(html)
        fields = _field_map(root)
        source_url = _field(fields, "source_url", "page_url") or _canonical_url(root)
        deck_id = _field(fields, "deck_id", "deck id") or _query_value(source_url, "d")
        deck_id = _require(deck_id, "deck_id")
        cards = tuple(self._parse_cards(root, deck_id))
        if not cards and not self._is_unavailable_deck_page(html):
            raise SchemaValidationError("MTGTop8 deck page did not expose a supported decklist structure")
        return SourceDeckCandidate(
            provider=PROVIDER,
            provider_deck_id=deck_id,
            source_event_key=event_key,
            source_url=source_url or f"{BASE_URL}/event?d={deck_id}",
            download_url=_field(fields, "download_url", "deck_url"),
            deck_title=_field(fields, "deck_title", "deck", "name") or _first_text(root, "deck-title", "deck-name"),
            commander_text=_field(fields, "commander_text", "commander"),
            pilot_name=_field(fields, "pilot_name", "pilot", "player"),
            rank=_int(_field(fields, "rank", "placement", "place")),
            rank_label=_field(fields, "rank_label", "placement", "place"),
            record=_field(fields, "record"),
            win_rate=None,
            archetype_name=_field(fields, "archetype_name", "archetype"),
            raw_payload=_raw_payload(html, "deck", deck_id, source_url),
            deck_key=deck_id,
            cards=cards,
        )

    def _is_unavailable_deck_page(self, html: Any) -> bool:
        if not isinstance(html, str):
            return True
        text = re.sub(r"\s+", " ", html).lower()
        if any(marker in text for marker in ("decklist unavailable", "decklist not available", "no decklist available")):
            return True
        try:
            root = _parse_html(html)
        except ParseError:
            return False
        fields = _field_map(root)
        has_deck_id = bool(_field(fields, "deck_id", "deck id") or _query_value(_canonical_url(root), "d"))
        return not has_deck_id and not self._card_sections(root)

    def _parse_cards(self, root: BeautifulSoup | Tag, deck_id: str) -> list[SourceDeckCardCandidate]:
        parsed: list[SourceDeckCardCandidate] = []
        for zone, rows in self._card_sections(root):
            for row in rows:
                quantity, name = self._parse_card_row(row)
                if name is None:
                    raise SchemaValidationError("MTGTop8 card row is missing a card name")
                parsed.append(
                    SourceDeckCardCandidate(
                        source_deck_key=deck_id,
                        raw_name=name,
                        quantity=quantity,
                        source_zone=zone,
                        source_order=len(parsed) + 1,
                        raw_entry=row.get_text(" ", strip=True),
                    )
                )
        return parsed

    def _card_sections(self, root: BeautifulSoup | Tag) -> list[tuple[str, list[Tag]]]:
        sections: list[tuple[str, list[Tag]]] = []
        for section in root.select(".deck-section[data-zone], .card-section[data-zone]"):
            zone = self._normalize_zone(str(section.get("data-zone")))
            if zone is None:
                continue
            rows = section.select(".card-row, .deck-card")
            if rows:
                sections.append((zone, rows))
        return sections

    def _parse_card_row(self, row: Tag) -> tuple[int, str | None]:
        quantity_node = row.select_one(".qty, .quantity, .count")
        name_node = row.select_one(".card-name, .card")
        quantity = _int(quantity_node.get_text(" ", strip=True) if quantity_node else None) or 1
        name = name_node.get_text(" ", strip=True) if name_node else None
        if name:
            return quantity, name
        match = re.match(r"^\s*(\d+)\s+(.+?)\s*$", row.get_text(" ", strip=True))
        if match:
            return int(match.group(1)), match.group(2)
        return quantity, None

    def _normalize_zone(self, zone: str) -> str | None:
        normalized = zone.lower().strip()
        aliases = {
            "main": "mainboard",
            "maindeck": "mainboard",
            "main deck": "mainboard",
            "mainboard": "mainboard",
            "side": "sideboard",
            "sideboard": "sideboard",
            "side board": "sideboard",
            "maybeboard": "maybeboard",
        }
        return aliases.get(normalized)
