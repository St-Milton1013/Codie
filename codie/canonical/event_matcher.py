"""Canonical event matching helpers."""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Mapping
from difflib import SequenceMatcher
from typing import Any


def _text(value: Any) -> str:
    return str(value or "").strip()


def _value(event: Mapping[str, Any], key: str) -> Any:
    try:
        return event[key]
    except (KeyError, IndexError):
        return None


def normalize_event_name(name: str) -> str:
    """Normalize event names for deterministic dedupe keys."""
    folded = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    lowered = folded.lower().replace("&", " and ")
    lowered = re.sub(r"\bcedh\b", "cedh", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def normalize_format(value: Any) -> str:
    text = _text(value).lower()
    if text in {"edh", "cedh", "commander"}:
        return "commander"
    return text


def event_dedupe_key(event: Mapping[str, Any]) -> str:
    """Return a deterministic conservative event dedupe key."""
    event_name = normalize_event_name(_text(_value(event, "event_name")))
    event_date = _text(_value(event, "event_date"))
    event_format = normalize_format(_value(event, "format"))
    country = _text(_value(event, "source_country") or _value(event, "country")).upper()
    region = _text(_value(event, "source_region") or _value(event, "region")).lower()
    venue = normalize_event_name(_text(_value(event, "source_store_tag") or _value(event, "store_tag")))
    return "|".join((event_name, event_date, event_format, country, region, venue))


def event_match_confidence(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    """Return a simple deterministic confidence score for two source events."""
    if event_dedupe_key(left) == event_dedupe_key(right):
        return 1.0
    left_name = normalize_event_name(_text(_value(left, "event_name")))
    right_name = normalize_event_name(_text(_value(right, "event_name")))
    if not left_name or not right_name:
        return 0.0
    return SequenceMatcher(None, left_name, right_name).ratio()
