"""MTGDecks tournament provider adapter."""

from .client import MTGDecksClient
from .parser import MTGDecksProvider

__all__ = ["MTGDecksClient", "MTGDecksProvider"]
