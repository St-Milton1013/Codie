"""EDHTop16 response helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class EDHTop16CardEntry:
    name: str
    quantity: int
    zone: str
    raw: Any
