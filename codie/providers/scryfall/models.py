"""Scryfall provider candidate models."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from codie.providers.models import normalize_provider_name


class ScryfallParseError(ValueError):
    """Raised when a Scryfall payload cannot become a card candidate."""


def _json_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _produced_mana(payload: dict[str, Any]) -> list[str] | None:
    root = payload.get("produced_mana")
    if root:
        return list(root)
    produced: set[str] = set()
    for face in payload.get("card_faces") or []:
        for mana in face.get("produced_mana") or []:
            produced.add(str(mana))
    return sorted(produced) if produced else None


def _commander_legal(payload: dict[str, Any]) -> bool:
    legalities = payload.get("legalities") or {}
    return legalities.get("commander") == "legal"


def _commander_candidate(payload: dict[str, Any]) -> bool:
    type_line = str(payload.get("type_line") or "")
    return "Legendary" in type_line and "Creature" in type_line and _commander_legal(payload)


@dataclass(frozen=True)
class ScryfallCard:
    scryfall_id: str
    oracle_id: str | None
    name: str
    normalized_name: str
    mana_cost: str | None
    mana_value: float | None
    type_line: str | None
    oracle_text: str | None
    colors_json: str | None
    color_identity_json: str | None
    legalities_json: str | None
    produced_mana_json: str | None
    keywords_json: str | None
    layout: str | None
    card_faces_json: str | None
    image_uris_json: str | None
    prices_json: str | None
    set_code: str | None
    collector_number: str | None
    rarity: str | None
    released_at: str | None
    is_reserved: int
    is_digital: int
    is_legal_commander: int
    is_commander_candidate: int
    raw_json: str
    imported_at: str

    @classmethod
    def from_payload(cls, payload: dict[str, Any], *, imported_at: str) -> "ScryfallCard":
        if not isinstance(payload, dict):
            raise ScryfallParseError("Scryfall card payload must be an object")
        missing = [field for field in ("id", "name") if not payload.get(field)]
        if missing:
            raise ScryfallParseError(f"Missing required Scryfall field(s): {', '.join(missing)}")

        produced_mana = _produced_mana(payload)
        return cls(
            scryfall_id=str(payload["id"]),
            oracle_id=payload.get("oracle_id"),
            name=str(payload["name"]),
            normalized_name=normalize_provider_name(str(payload["name"])),
            mana_cost=payload.get("mana_cost"),
            mana_value=payload.get("cmc"),
            type_line=payload.get("type_line"),
            oracle_text=payload.get("oracle_text"),
            colors_json=_json_or_none(payload.get("colors")),
            color_identity_json=_json_or_none(payload.get("color_identity")),
            legalities_json=_json_or_none(payload.get("legalities")),
            produced_mana_json=_json_or_none(produced_mana),
            keywords_json=_json_or_none(payload.get("keywords")),
            layout=payload.get("layout"),
            card_faces_json=_json_or_none(payload.get("card_faces")),
            image_uris_json=_json_or_none(payload.get("image_uris")),
            prices_json=_json_or_none(payload.get("prices")),
            set_code=payload.get("set"),
            collector_number=payload.get("collector_number"),
            rarity=payload.get("rarity"),
            released_at=payload.get("released_at"),
            is_reserved=1 if payload.get("reserved") else 0,
            is_digital=1 if payload.get("digital") else 0,
            is_legal_commander=1 if _commander_legal(payload) else 0,
            is_commander_candidate=1 if _commander_candidate(payload) else 0,
            raw_json=json.dumps(payload, sort_keys=True, separators=(",", ":")),
            imported_at=imported_at,
        )

    def to_card_row(self) -> dict[str, Any]:
        return self.__dict__.copy()
