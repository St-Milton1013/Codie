"""MTGTop8 tournament provider adapter."""

from .client import MTGTop8Client
from .parser import MTGTop8Provider

__all__ = ["MTGTop8Client", "MTGTop8Provider"]
