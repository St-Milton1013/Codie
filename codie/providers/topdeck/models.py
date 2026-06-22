"""TopDeck response helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TopDeckCardEntry:
    name: str
    quantity: int
    zone: str
    raw: Any
