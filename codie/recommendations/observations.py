"""Pure mappers for canonical recommendation input rows."""

from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any

from .staples import StapleObservation


def _row_value(row: Any, key: str) -> Any:
    try:
        return row[key]
    except (KeyError, IndexError, TypeError):
        try:
            return getattr(row, key)
        except AttributeError as exc:
            raise ValueError(f"{key} is required") from exc


def _required_text(row: Any, key: str) -> str:
    value = _row_value(row, key)
    if value in (None, ""):
        raise ValueError(f"{key} is required")
    return str(value)


def _optional_text(row: Any, key: str) -> str | None:
    value = _row_value(row, key)
    if value in (None, ""):
        return None
    return str(value)


def _flag(row: Any, key: str) -> bool:
    return bool(_row_value(row, key) or 0)


def _color_identity(value: Any) -> tuple[str, ...]:
    if value in (None, ""):
        return ()
    try:
        decoded = json.loads(str(value))
    except json.JSONDecodeError as exc:
        raise ValueError("color_identity_json must be valid JSON") from exc
    if not isinstance(decoded, list):
        raise ValueError("color_identity_json must decode to a list")
    return tuple(str(color) for color in decoded if str(color).strip())


def staple_observations_from_canonical_rows(rows: Iterable[Any]) -> tuple[StapleObservation, ...]:
    """Convert repository rows into commander staple observations."""
    observations: list[StapleObservation] = []
    for row in rows:
        deck_id = f"event_entry:{_required_text(row, 'event_deck_entry_id')}"
        placement = _row_value(row, "placement")
        observations.append(
            StapleObservation(
                deck_id=deck_id,
                oracle_id=_required_text(row, "oracle_id"),
                scryfall_id=_required_text(row, "scryfall_id"),
                card_name=_required_text(row, "card_name"),
                quantity=int(_row_value(row, "quantity") or 1),
                type_line=_optional_text(row, "type_line"),
                color_identity=_color_identity(_row_value(row, "color_identity_json")),
                entry_weight=float(_row_value(row, "entry_weight") or 0.0),
                placement=int(placement) if placement is not None else None,
                top_cut=_flag(row, "top_cut_made") or _flag(row, "final_pod"),
                winner=_flag(row, "winner"),
                event_date=_optional_text(row, "event_date"),
                deck_url=_optional_text(row, "deck_url"),
                event_url=_optional_text(row, "event_url"),
                provider=_optional_text(row, "provider"),
                region=_optional_text(row, "region"),
                country=_optional_text(row, "country"),
            )
        )
    return tuple(observations)
