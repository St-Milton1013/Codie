"""Card-name normalization for Scryfall-backed lookup."""

from __future__ import annotations

import re
import unicodedata


def normalize_card_name(name: str) -> str:
    """Normalize display card names into stable local lookup keys."""
    folded = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    lowered = folded.lower().strip()
    lowered = lowered.replace("//", " ")
    lowered = re.sub(r"['’]", "", lowered)
    lowered = re.sub(r"[^a-z0-9]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()
