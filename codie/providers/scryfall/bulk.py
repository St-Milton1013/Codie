"""Read local Scryfall bulk-data fixtures or cache files."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ScryfallCard, ScryfallParseError


def load_bulk_cards(path: str | Path, *, imported_at: str) -> list[ScryfallCard]:
    """Load a local Scryfall bulk file.

    Both official-style JSON arrays and newline-delimited JSON fixtures are
    accepted so tests and cache refreshes can use compact files.
    """
    bulk_path = Path(path)
    text = bulk_path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
        payloads = parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        payloads = []
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payloads.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ScryfallParseError(f"Invalid JSON on line {line_number}: {exc.msg}") from exc
    return [ScryfallCard.from_payload(payload, imported_at=imported_at) for payload in payloads]
