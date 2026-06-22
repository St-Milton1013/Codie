"""Base provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    """Fetch and parse provider payloads without persistence."""

    provider_name: str

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch raw provider payload material."""

    @abstractmethod
    def parse(self, payload: Any):
        """Parse raw payload material into provider candidate models."""
