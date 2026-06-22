"""Commander signature generation.

Signatures group one commander or an unordered partner/background pair under a
stable key. They are intentionally based on normalized names until Scryfall
oracle IDs are available from the card truth layer.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable


def normalize_commander_name(name: str) -> str:
    """Normalize a commander name for stable signature sorting."""
    folded = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    lowered = folded.lower().strip()
    return re.sub(r"\s+", " ", lowered)


def commander_signature(names: Iterable[str]) -> str:
    """Return a deterministic commander signature using `|` for pairs."""
    normalized = [normalize_commander_name(name) for name in names if normalize_commander_name(name)]
    if not normalized:
        raise ValueError("At least one commander name is required")
    return "|".join(sorted(normalized))
