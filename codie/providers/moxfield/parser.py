"""Parse Moxfield deck metadata into primer candidates."""

from __future__ import annotations

import re
from typing import Any

from codie.providers.base import Provider
from codie.providers.errors import MissingRequiredFieldError, ParseError
from codie.providers.models import RawPayload, SourcePrimerCandidate

from .models import PROVIDER

BASE_URL = "https://moxfield.com"
BODY_KEYS = {
    "body",
    "content",
    "primer",
    "primer_body",
    "primerbody",
    "description",
    "markdown",
    "html",
    "text",
    "sections",
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


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return False


def _nested(payload: dict[str, Any], *keys: str) -> Any:
    value: Any = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _name(value: Any) -> str | None:
    if isinstance(value, str):
        return _string(value)
    if isinstance(value, dict):
        return _string(value.get("name") or value.get("cardName") or value.get("displayName"))
    return None


def _names(value: Any) -> list[str]:
    if isinstance(value, list):
        return [name for item in value if (name := _name(item))]
    if isinstance(value, dict):
        return [name for item in value.values() if (name := _name(item))]
    if isinstance(value, str):
        return [value]
    return []


def _deck_id(payload: dict[str, Any]) -> str | None:
    return _string(payload.get("publicId") or payload.get("public_id") or payload.get("id") or payload.get("deck_id"))


def _deck_url(payload: dict[str, Any], deck_id: str | None) -> str | None:
    value = _string(payload.get("publicUrl") or payload.get("deck_url") or payload.get("url"))
    if value:
        return value if value.startswith("http") else f"{BASE_URL}{value}"
    return f"{BASE_URL}/decks/{deck_id}" if deck_id else None


def _primer_url(payload: dict[str, Any], deck_url: str | None) -> str | None:
    value = _string(payload.get("primerUrl") or payload.get("primer_url") or _nested(payload, "primerMetadata", "primerUrl"))
    if value:
        return value if value.startswith("http") else f"{BASE_URL}{value}"
    if deck_url and _has_primer_route(payload):
        return f"{deck_url.rstrip('/')}/primer"
    return None


def _author(payload: dict[str, Any]) -> tuple[str | None, str | None]:
    author = payload.get("author") or payload.get("createdByUser") or payload.get("user") or {}
    if isinstance(author, dict):
        name = _string(author.get("userName") or author.get("username") or author.get("displayName") or author.get("name"))
        url = _string(author.get("profileUrl") or author.get("url"))
        if url and not url.startswith("http"):
            url = f"{BASE_URL}{url}"
        return name, url
    return _string(author), None


def _tags(payload: dict[str, Any]) -> list[str]:
    tags = payload.get("tags") or payload.get("hubs") or []
    if isinstance(tags, list):
        values = []
        for tag in tags:
            if isinstance(tag, dict):
                text = _string(tag.get("name") or tag.get("title") or tag.get("tag"))
            else:
                text = _string(tag)
            if text:
                values.append(text)
        return values
    return []


def _has_primer_route(payload: dict[str, Any]) -> bool:
    return _bool(
        payload.get("hasPrimer")
        or payload.get("has_primer")
        or payload.get("primerContentPresent")
        or _nested(payload, "primerMetadata", "hasPrimer")
        or _nested(payload, "primerMetadata", "routeExists")
    )


def _strip_body(value: Any) -> Any:
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            normalized_key = re.sub(r"[^a-z0-9]+", "_", str(key).lower()).strip("_")
            if normalized_key in BODY_KEYS:
                continue
            clean[key] = _strip_body(item)
        return clean
    if isinstance(value, list):
        return [_strip_body(item) for item in value]
    return value


def _raw_payload(payload: dict[str, Any], primer_url: str | None, deck_id: str | None) -> RawPayload:
    return RawPayload(
        provider=PROVIDER,
        object_type="primer",
        provider_id=deck_id,
        source_url=primer_url,
        retrieved_at="unknown",
        payload=_strip_body(payload),
    )


class MoxfieldProvider(Provider):
    """Moxfield adapter that fetches/parses only and emits primer candidates."""

    provider_name = PROVIDER

    def __init__(self, client: Any | None = None, deck_id: str | None = None) -> None:
        self.client = client
        self.deck_id = deck_id

    def fetch(self) -> dict[str, Any]:
        if self.deck_id is None:
            raise ParseError("MoxfieldProvider.fetch requires deck_id")
        return self.fetch_deck(self.deck_id)

    def parse(self, payload: dict[str, Any]) -> dict[str, tuple[Any, ...]]:
        return {"primers": (self.parse_deck(payload),)}

    def fetch_deck(self, deck_id: str) -> dict[str, Any]:
        if self.client is None:
            raise ParseError("MoxfieldProvider.fetch_deck requires a client")
        return self.client.fetch_deck(deck_id)

    def parse_deck(self, raw: dict[str, Any]) -> SourcePrimerCandidate:
        if not isinstance(raw, dict):
            raise ParseError("Moxfield deck payload must be an object")
        deck_id = _deck_id(raw)
        deck_url = _deck_url(raw, deck_id)
        if not deck_url:
            raise MissingRequiredFieldError("Moxfield deck missing required field(s): deck_url")
        primer_url = _primer_url(raw, deck_url)
        commanders = _names(raw.get("commanders") or raw.get("mainboardCommander"))
        partners = _names(raw.get("partners") or raw.get("companions") or raw.get("partner"))
        author, author_url = _author(raw)
        tags = _tags(raw)
        primer_metadata = raw.get("primerMetadata") if isinstance(raw.get("primerMetadata"), dict) else {}
        objective_metadata = {
            "source_tags": tags,
            "bracket": _string(raw.get("bracket") or raw.get("format")),
            "has_primer_route": 1 if primer_url else 0,
            "primer_content_present": 1 if _has_primer_route(raw) else 0,
            "primer_toc_present": 1 if _bool(primer_metadata.get("tocPresent")) else 0,
            "primer_heading_count": _int(primer_metadata.get("headingCount")) or 0,
            "primer_section_names": primer_metadata.get("sectionNames") if isinstance(primer_metadata.get("sectionNames"), list) else [],
            "primer_external_link_count": _int(primer_metadata.get("externalLinkCount")) or 0,
            "primer_video_count": _int(primer_metadata.get("videoCount")) or 0,
            "primer_image_count": _int(primer_metadata.get("imageCount")) or 0,
            "content_length_estimate": _int(primer_metadata.get("contentLengthEstimate")),
            "cedh_title_signal": 1 if "cedh" in f"{raw.get('name', '')} {raw.get('title', '')}".lower() else 0,
            "cedh_tag_signal": 1 if any("cedh" in tag.lower() for tag in tags) else 0,
            "competitive_tag_signal": 1 if any("competitive" in tag.lower() for tag in tags) else 0,
            "tournament_title_signal": 1 if "tournament" in f"{raw.get('name', '')} {raw.get('title', '')}".lower() else 0,
        }
        return SourcePrimerCandidate(
            provider=PROVIDER,
            primer_url=primer_url or deck_url,
            deck_url=deck_url,
            commander_text=" / ".join(commanders) if commanders else None,
            partner_text=" / ".join(partners) if partners else None,
            deck_title=_string(raw.get("name") or raw.get("title")),
            primer_title=_string(raw.get("primerTitle") or primer_metadata.get("title") or raw.get("name")),
            author=author,
            updated_at=_string(raw.get("updatedAt") or raw.get("lastUpdatedAt") or primer_metadata.get("updatedAt")),
            likes=_int(raw.get("likeCount") or raw.get("likes")),
            views=_int(raw.get("viewCount") or raw.get("views")),
            comments=_int(raw.get("commentCount") or raw.get("comments")),
            objective_metadata=objective_metadata,
            raw_payload=_raw_payload(raw, primer_url or deck_url, deck_id),
            author_url=author_url,
        )
