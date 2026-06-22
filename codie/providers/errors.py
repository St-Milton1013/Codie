"""Provider and ingestion error types."""

from __future__ import annotations


class ProviderError(Exception):
    """Base error with retry metadata for provider/ingestion failures."""

    retryable = False

    def __init__(self, message: str, *, retryable: bool | None = None) -> None:
        super().__init__(message)
        if retryable is not None:
            self.retryable = retryable


class NetworkError(ProviderError):
    retryable = True


class RateLimitError(ProviderError):
    retryable = True


class ParseError(ProviderError):
    retryable = False


class MissingRequiredFieldError(ProviderError):
    retryable = False


class CardResolutionError(ProviderError):
    retryable = False


class SchemaValidationError(ProviderError):
    retryable = False


class CanonicalizationConflict(ProviderError):
    retryable = False


class DuplicateAmbiguityError(ProviderError):
    retryable = False
