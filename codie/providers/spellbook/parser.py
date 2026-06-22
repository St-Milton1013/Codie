"""Parse Commander Spellbook payloads into provider candidates."""

from __future__ import annotations

from typing import Any

from codie.providers.base import Provider
from codie.providers.errors import MissingRequiredFieldError, ParseError, SchemaValidationError
from codie.providers.models import RawPayload, SourceComboCandidate, SourceComboCardCandidate

from .models import PROVIDER

BASE_URL = "https://commanderspellbook.com"


def _string(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value).strip()


def _list_payload(raw: dict[str, Any] | list[Any]) -> list[Any]:
    if isinstance(raw, list):
        return raw
    if not isinstance(raw, dict):
        raise ParseError("Commander Spellbook payload must be an object or array")
    for key in ("results", "variants", "data"):
        value = raw.get(key)
        if isinstance(value, list):
            return value
    if any(key in raw for key in ("id", "pk", "slug", "uses", "requires", "cards")):
        return [raw]
    raise ParseError("Commander Spellbook payload does not contain variants")


def _raw_payload(payload: Any, provider_id: str | None, source_url: str | None) -> RawPayload:
    return RawPayload(
        provider=PROVIDER,
        object_type="combo",
        provider_id=provider_id,
        source_url=source_url,
        retrieved_at="unknown",
        payload=payload,
    )


def _combo_id(payload: dict[str, Any]) -> str | None:
    return _string(
        payload.get("id")
        or payload.get("pk")
        or payload.get("variant_id")
        or payload.get("spellbook_id")
        or payload.get("slug")
    )


def _combo_name(payload: dict[str, Any]) -> str | None:
    return _string(payload.get("name") or payload.get("name_oracle") or payload.get("title") or payload.get("description"))


def _combo_url(payload: dict[str, Any], provider_combo_id: str | None) -> str | None:
    url = _string(payload.get("url") or payload.get("uri") or payload.get("spellbook_url"))
    if url:
        return url if url.startswith("http") else f"{BASE_URL}{url}"
    slug = _string(payload.get("slug"))
    if slug:
        return f"{BASE_URL}/combo/{slug}/"
    if provider_combo_id:
        return f"{BASE_URL}/combo/{provider_combo_id}/"
    return None


def _card_name(entry: Any) -> str | None:
    if isinstance(entry, str):
        return _string(entry)
    if not isinstance(entry, dict):
        return None
    value = entry.get("name") or entry.get("card_name") or entry.get("oracle") or entry.get("name_oracle")
    if isinstance(value, dict):
        value = value.get("name") or value.get("oracle")
    card = entry.get("card")
    if value is None and isinstance(card, dict):
        value = card.get("name") or card.get("oracle") or card.get("name_oracle")
    return _string(value)


def _card_role(entry: Any, default: str | None) -> str | None:
    if isinstance(entry, dict):
        return _string(entry.get("role") or entry.get("zone") or entry.get("component_role") or default)
    return default


def _card_required(entry: Any) -> bool:
    if isinstance(entry, dict) and "required" in entry:
        return bool(entry["required"])
    return True


def _component_entries(payload: dict[str, Any]) -> list[tuple[Any, str | None]]:
    entries: list[tuple[Any, str | None]] = []
    for key, role in (("uses", "uses"), ("requires", "requires"), ("cards", "component"), ("components", "component")):
        value = payload.get(key)
        if isinstance(value, list):
            entries.extend((entry, role) for entry in value)
    return entries


def _outputs(payload: dict[str, Any]) -> tuple[str, ...]:
    values: list[str] = []
    for key in ("produces", "outputs", "results"):
        value = payload.get(key)
        if isinstance(value, list):
            for entry in value:
                if isinstance(entry, dict):
                    text = _string(entry.get("name") or entry.get("description") or entry.get("output"))
                else:
                    text = _string(entry)
                if text:
                    values.append(text)
        elif isinstance(value, str):
            values.append(value)
    return tuple(values)


class SpellbookProvider(Provider):
    """Commander Spellbook adapter that fetches/parses only."""

    provider_name = PROVIDER

    def __init__(self, client: Any | None = None) -> None:
        self.client = client

    def fetch(self) -> dict[str, Any] | list[Any]:
        return self.fetch_variants()

    def parse(self, payload: dict[str, Any] | list[Any]) -> dict[str, tuple[Any, ...]]:
        return {"combos": self.parse_variants(payload)}

    def fetch_variants(self) -> dict[str, Any] | list[Any]:
        if self.client is None:
            raise ParseError("SpellbookProvider.fetch_variants requires a client")
        return self.client.fetch_variants()

    def parse_variants(self, raw: dict[str, Any] | list[Any]) -> tuple[SourceComboCandidate, ...]:
        combos: list[SourceComboCandidate] = []
        for entry in _list_payload(raw):
            if not isinstance(entry, dict):
                raise SchemaValidationError("Commander Spellbook variant entry must be an object")
            combos.append(self._parse_combo(entry))
        return tuple(combos)

    def _parse_combo(self, raw: dict[str, Any]) -> SourceComboCandidate:
        provider_combo_id = _combo_id(raw)
        if not provider_combo_id:
            raise MissingRequiredFieldError("Commander Spellbook combo missing required field(s): id")
        combo_url = _combo_url(raw, provider_combo_id)
        if not combo_url:
            raise MissingRequiredFieldError("Commander Spellbook combo missing required field(s): combo_url")
        combo_name = _combo_name(raw)
        cards = []
        for entry, role in _component_entries(raw):
            name = _card_name(entry)
            if not name:
                raise SchemaValidationError("Commander Spellbook combo component is missing a card name")
            cards.append(
                SourceComboCardCandidate(
                    raw_name=name,
                    role=_card_role(entry, role),
                    required=_card_required(entry),
                    raw_entry=entry,
                )
            )
        if not cards:
            raise SchemaValidationError("Commander Spellbook combo has no component cards")
        components = tuple(card.raw_name for card in cards)
        return SourceComboCandidate(
            provider=PROVIDER,
            provider_combo_id=provider_combo_id,
            combo_url=combo_url,
            combo_name=combo_name,
            components=components,
            outputs=_outputs(raw),
            raw_payload=_raw_payload(raw, provider_combo_id, combo_url),
            cards=tuple(cards),
        )
