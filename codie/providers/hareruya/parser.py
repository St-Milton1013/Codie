"""Parse Hareruya HTML payloads into Codie provider candidates."""

from __future__ import annotations

import re
from html import unescape
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

PROVIDER = "hareruya"
BASE_URL = "https://www.hareruyamtg.com"
UNAVAILABLE_MARKERS = (
    "decklist unavailable",
    "decklist not available",
    "no decklist available",
    "デッキリストは非公開",
)
ZONE_ALIASES = {
    "commander": "commanders",
    "commanders": "commanders",
    "統率者": "commanders",
    "main": "mainboard",
    "maindeck": "mainboard",
    "main deck": "mainboard",
    "mainboard": "mainboard",
    "メイン": "mainboard",
    "side": "sideboard",
    "sideboard": "sideboard",
    "side board": "sideboard",
    "サイドボード": "sideboard",
    "maybeboard": "maybeboard",
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


def _parse_html(payload: str) -> BeautifulSoup:
    if not isinstance(payload, str) or "<" not in payload or ">" not in payload:
        raise ParseError("Hareruya payload must be HTML")
    soup = BeautifulSoup(payload, "html.parser")
    if not soup.find(("html", "body", "main", "article", "table")):
        raise ParseError("Hareruya HTML payload does not contain parseable page structure")
    return soup


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
        raise MissingRequiredFieldError(f"Hareruya payload missing required field(s): {label}")
    return value


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
    for row in root.select(".deckSearch-deckList__information__flex__list"):
        header = row.select_one(".deckSearch-deckList__information__list__header")
        body = row.select_one(".deckSearch-deckList__information__list__body")
        key = header.get_text(" ", strip=True).lower().rstrip(":") if header else ""
        value = body.get_text(" ", strip=True) if body else ""
        if key and value:
            fields.setdefault(key, value)
    return fields


def _first_text(root: BeautifulSoup | Tag, *classes: str) -> str | None:
    for class_name in classes:
        node = root.select_one(f".{class_name}")
        if node and node.get_text(" ", strip=True):
            return node.get_text(" ", strip=True)
    return None


def _select_text(root: BeautifulSoup | Tag, *selectors: str) -> str | None:
    for selector in selectors:
        node = root.select_one(selector)
        if node and node.get_text(" ", strip=True):
            return node.get_text(" ", strip=True)
    return None


def _strip_card_brackets(value: str) -> str:
    text = unescape(value).strip()
    if text.startswith("《") and text.endswith("》"):
        return text[1:-1].strip()
    return text


def _headline_format(headline: str | None) -> str | None:
    if not headline:
        return None
    match = re.match(r"^\s*([A-Za-z ]+?)\s+Meta\s+Game", headline)
    return match.group(1).strip() if match else None


def _live_metagame_deck_count(root: BeautifulSoup | Tag) -> int | None:
    total = 0
    found = False
    for node in root.select(".deckSearch-metaList__list__item__count"):
        count = _int(node.get_text(" ", strip=True))
        if count is not None:
            total += count
            found = True
    return total if found else None


def _download_url(root: BeautifulSoup | Tag, fields: dict[str, str]) -> str | None:
    explicit = _field(fields, "download_url", "deck_url")
    if explicit:
        return explicit
    link = root.find("a", title=lambda value: isinstance(value, str) and "download" in value.lower())
    if isinstance(link, Tag) and link.get("href"):
        href = str(link["href"])
        return href if href.startswith("http") else f"{BASE_URL}{href}"
    return None


class HareruyaProvider(Provider):
    """Hareruya adapter that fetches/parses only and emits candidate models."""

    provider_name = PROVIDER

    def __init__(
        self,
        client: Any | None = None,
        *,
        metagame_url: str | None = None,
        deck_urls: tuple[str, ...] = (),
    ) -> None:
        self.client = client
        self.metagame_url = metagame_url
        self.deck_urls = deck_urls

    def fetch(self) -> dict[str, Any]:
        if self.client is None or self.metagame_url is None:
            raise ParseError("HareruyaProvider.fetch requires a client and metagame_url")
        return {
            "metagame_page": self.fetch_metagame_page(self.metagame_url),
            "deck_pages": [self.fetch_deck_page(deck_url) for deck_url in self.deck_urls],
        }

    def parse(self, payload: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
        if not isinstance(payload, dict):
            raise ParseError("Hareruya provider payload must be an object")
        events: list[SourceEventCandidate] = []
        decks: list[SourceDeckCandidate] = []
        event_key = ""
        event_payload = payload.get("metagame_page") or payload.get("event_page") or payload.get("event")
        if event_payload is not None:
            event = self.parse_metagame_page(event_payload)
            events.append(event)
            event_key = event.event_key or event.provider_event_id or ""
        for deck_payload in payload.get("deck_pages") or payload.get("decks") or ():
            if self._is_unavailable_decklist(deck_payload):
                continue
            decks.append(self.parse_deck_page(deck_payload, event_key))
        return {"events": tuple(events), "decks": tuple(decks)}

    def fetch_metagame_page(self, metagame_url: str) -> str:
        if self.client is None:
            raise ParseError("HareruyaProvider.fetch_metagame_page requires a client")
        return self.client.fetch_metagame_page(metagame_url)

    def fetch_deck_page(self, deck_url: str) -> str:
        if self.client is None:
            raise ParseError("HareruyaProvider.fetch_deck_page requires a client")
        return self.client.fetch_deck_page(deck_url)

    def parse_metagame_page(self, html: str) -> SourceEventCandidate:
        root = _parse_html(html)
        fields = _field_map(root)
        source_url = _field(fields, "source_url", "page_url") or _canonical_url(root)
        event_id = _field(fields, "event_id", "metagame_id", "event id") or _query_value(source_url, "event") or _query_value(source_url, "id") or _path_id(source_url)
        event_id = _require(event_id, "event_id")
        headline = _select_text(root, "h1.common-headline--deckSearch")
        event_name = _field(fields, "event_name", "metagame_name", "event", "name") or _first_text(root, "event-title", "metagame-title", "event-name") or headline
        if not event_name:
            raise ParseError("Hareruya metagame page missing parseable event name")
        country = _field(fields, "country") or "JP"
        region = _field(fields, "region", "state") or "Japan"
        deck_count = _int(_field(fields, "deck_count", "decks"))
        if deck_count is None:
            deck_count = _live_metagame_deck_count(root)
        return SourceEventCandidate(
            provider=PROVIDER,
            provider_event_id=event_id,
            source_url=source_url or f"{BASE_URL}/en/deck/{event_id}/metagame/",
            original_source="Hareruya",
            original_source_url=_field(fields, "original_source_url", "source") or source_url,
            event_name=event_name,
            event_date=_field(fields, "event_date", "date"),
            format=_field(fields, "format") or _headline_format(headline),
            region=region,
            country=country,
            store_tag=_field(fields, "store_tag", "venue", "location"),
            language=_field(fields, "language"),
            player_count=_int(_field(fields, "player_count", "players")),
            deck_count=deck_count,
            raw_payload=_raw_payload(html, "event", event_id, source_url),
            event_key=event_id,
        )

    def parse_deck_page(self, html: str, event_key: str) -> SourceDeckCandidate:
        root = _parse_html(html)
        fields = _field_map(root)
        source_url = _field(fields, "source_url", "page_url") or _canonical_url(root)
        deck_id = _field(fields, "deck_id", "deck id") or _query_value(source_url, "deck") or _query_value(source_url, "id") or _path_id(source_url)
        deck_id = _require(deck_id, "deck_id")
        cards = tuple(self._parse_cards(root, deck_id))
        if not cards and not self._is_unavailable_decklist(html):
            raise SchemaValidationError("Hareruya deck page did not expose a supported decklist structure")
        commander_text = _field(fields, "commander_text", "commander")
        if commander_text is None:
            commander_text = self._fallback_commander_from_first_card(fields, cards)
        return SourceDeckCandidate(
            provider=PROVIDER,
            provider_deck_id=deck_id,
            source_event_key=event_key,
            source_url=source_url or f"{BASE_URL}/en/deck/{deck_id}/show/",
            download_url=_download_url(root, fields),
            deck_title=_field(fields, "deck_title", "deck", "name", "archetype") or _first_text(root, "deck-title", "deck-name") or _select_text(root, "h1.common-headline--deckSearch-deck_List"),
            commander_text=commander_text,
            pilot_name=_field(fields, "pilot_name", "pilot", "player"),
            rank=_int(_field(fields, "rank", "placement", "place", "score")),
            rank_label=_field(fields, "rank_label", "placement", "place", "score"),
            record=_field(fields, "record"),
            win_rate=None,
            archetype_name=_field(fields, "archetype_name", "archetype"),
            raw_payload=_raw_payload(html, "deck", deck_id, source_url),
            deck_key=deck_id,
            cards=cards,
        )

    def _is_unavailable_decklist(self, payload: Any) -> bool:
        if not isinstance(payload, str):
            return True
        text = re.sub(r"\s+", " ", payload).lower()
        return any(marker.lower() in text for marker in UNAVAILABLE_MARKERS)

    def _parse_cards(self, root: BeautifulSoup | Tag, deck_id: str) -> list[SourceDeckCardCandidate]:
        entries: list[SourceDeckCardCandidate] = []
        for section in root.select(".deck-section[data-zone], .card-section[data-zone]"):
            zone = self._normalize_zone(str(section.get("data-zone")))
            if zone is None:
                continue
            for row in section.select(".card-row, .deck-card"):
                quantity, name = self._parse_card_row(row)
                if name is None:
                    raise SchemaValidationError("Hareruya card row is missing a card name")
                entries.append(
                    SourceDeckCardCandidate(
                        source_deck_key=deck_id,
                        raw_name=name,
                        quantity=quantity,
                        source_zone=zone,
                        source_order=len(entries) + 1,
                        raw_entry=row.get_text(" ", strip=True),
                    )
                )
        for section in root.select(".deckSearch-deckList__deckList__container__text"):
            zone = self._normalize_live_section_zone(section)
            if zone is None:
                continue
            for row in section.find_all("div", recursive=False):
                if row.select_one(".deckSearch-deckList__deckList__totalNumber"):
                    continue
                card_link = row.select_one("a.popup_product")
                if card_link is None:
                    continue
                quantity, name = self._parse_live_card_row(row, card_link)
                if name is None:
                    raise SchemaValidationError("Hareruya card row is missing a card name")
                entries.append(
                    SourceDeckCardCandidate(
                        source_deck_key=deck_id,
                        raw_name=name,
                        quantity=quantity,
                        source_zone=zone,
                        source_order=len(entries) + 1,
                        raw_entry=row.get_text(" ", strip=True),
                    )
                )
        return entries

    def _parse_card_row(self, row: Tag) -> tuple[int, str | None]:
        quantity_node = row.select_one(".qty, .quantity, .count")
        name_node = row.select_one(".card-name, .card")
        quantity = _int(quantity_node.get_text(" ", strip=True) if quantity_node else None) or 1
        name = name_node.get_text(" ", strip=True) if name_node else None
        if name:
            return quantity, name
        match = re.match(r"^\s*(\d+)\s+(.+?)\s*$", row.get_text(" ", strip=True))
        if match:
            return int(match.group(1)), match.group(2).strip()
        return quantity, None

    def _fallback_commander_from_first_card(
        self,
        fields: dict[str, str],
        cards: tuple[SourceDeckCardCandidate, ...],
    ) -> str | None:
        deck_type = (_field(fields, "deck_type", "format") or "").lower()
        if "commander" not in deck_type and "edh" not in deck_type:
            return None
        commander_cards = [card.raw_name for card in cards if card.source_zone == "commanders"]
        if commander_cards:
            return " / ".join(commander_cards)
        return cards[0].raw_name if cards else None

    def _normalize_zone(self, zone: str) -> str | None:
        return ZONE_ALIASES.get(zone.lower().strip())

    def _parse_live_card_row(self, row: Tag, card_link: Tag) -> tuple[int, str | None]:
        quantity_node = row.find("span", recursive=False)
        quantity = _int(quantity_node.get_text(" ", strip=True) if quantity_node else None) or 1
        name = _strip_card_brackets(card_link.get_text(" ", strip=True))
        return quantity, name or None

    def _normalize_live_section_zone(self, section: Tag) -> str | None:
        classes = " ".join(str(value) for value in section.get("class", ())).lower()
        text = section.get_text(" ", strip=True).lower()
        if "sideboard" in classes or text.startswith("sideboard"):
            return "sideboard"
        if "commander" in classes or text.startswith("commander"):
            return "commanders"
        if "container__text--" in classes:
            return "mainboard"
        return None
