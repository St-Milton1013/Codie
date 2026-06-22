"""External-source adapters.

Provider code fetches and parses source payloads only. It never opens SQLite
connections and never imports repositories.
"""

from .base import Provider
from .errors import (
    CanonicalizationConflict,
    CardResolutionError,
    DuplicateAmbiguityError,
    MissingRequiredFieldError,
    NetworkError,
    ParseError,
    ProviderError,
    RateLimitError,
    SchemaValidationError,
)
from .models import (
    RawPayload,
    SourceComboCandidate,
    SourceDeckCandidate,
    SourceDeckCardCandidate,
    SourceEventCandidate,
    SourcePrimerCandidate,
)

__all__ = [
    "CanonicalizationConflict",
    "CardResolutionError",
    "DuplicateAmbiguityError",
    "MissingRequiredFieldError",
    "NetworkError",
    "ParseError",
    "Provider",
    "ProviderError",
    "RateLimitError",
    "RawPayload",
    "SchemaValidationError",
    "SourceComboCandidate",
    "SourceDeckCandidate",
    "SourceDeckCardCandidate",
    "SourceEventCandidate",
    "SourcePrimerCandidate",
]
