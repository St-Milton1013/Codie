"""Canonical deck hashing helpers."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any

AUXILIARY_ZONES = {"auxiliary", "stickers", "attractions"}
COMMANDER_ZONES = {"commander", "commanders"}


def _required_text(card: Mapping[str, Any], key: str) -> str:
    value = card.get(key)
    if value in (None, ""):
        raise ValueError(f"Card is missing required field: {key}")
    return str(value)


def _quantity(card: Mapping[str, Any]) -> int:
    value = card.get("quantity", 1)
    try:
        quantity = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Card quantity must be an integer") from exc
    if quantity <= 0:
        raise ValueError("Card quantity must be positive")
    return quantity


def _zone(card: Mapping[str, Any]) -> str:
    return str(card.get("source_zone") or card.get("zone") or "mainboard").lower().strip()


def canonical_card_fingerprint(cards: Iterable[Mapping[str, Any]]) -> tuple[str, ...]:
    """Return stable card fingerprints excluding auxiliary source zones."""
    aggregate: dict[tuple[str, str], int] = defaultdict(int)
    for card in cards:
        zone = _zone(card)
        if zone in AUXILIARY_ZONES:
            continue
        scryfall_id = _required_text(card, "scryfall_id")
        aggregate[(zone, scryfall_id)] += _quantity(card)
    return tuple(f"{zone}:{scryfall_id}:{quantity}" for (zone, scryfall_id), quantity in sorted(aggregate.items()))


def commander_hash(commanders: Iterable[Mapping[str, Any]]) -> str:
    """Return a deterministic commander hash from commander card identities."""
    identities = sorted({_required_text(card, "scryfall_id") for card in commanders})
    if not identities:
        raise ValueError("At least one commander card is required")
    return "|".join(identities)


def deck_hash(
    cards: Iterable[Mapping[str, Any]],
    commanders: Iterable[Mapping[str, Any]],
    *,
    format: str = "commander",
) -> str:
    """Return a stable hash for a resolved decklist and commander set."""
    payload = {
        "format": format.lower().strip(),
        "commanders": commander_hash(commanders),
        "cards": canonical_card_fingerprint(cards),
    }
    stable = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(stable.encode("utf-8")).hexdigest()
