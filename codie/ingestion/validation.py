"""Candidate validation helpers."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any

from codie.providers.errors import MissingRequiredFieldError, SchemaValidationError


REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "RawPayload": ("provider", "object_type", "retrieved_at"),
    "SourceEventCandidate": ("provider", "raw_payload"),
    "SourceDeckCandidate": ("provider", "raw_payload"),
    "SourceDeckCardCandidate": ("source_deck_key", "raw_name", "quantity", "source_zone"),
    "SourcePrimerCandidate": ("provider", "primer_url", "objective_metadata", "raw_payload"),
    "SourceComboCandidate": ("provider", "components", "outputs", "raw_payload"),
}


def validate_candidate(candidate: Any) -> None:
    if not is_dataclass(candidate):
        raise SchemaValidationError(f"Candidate must be a dataclass: {type(candidate).__name__}")
    field_names = {field.name for field in fields(candidate)}
    required = REQUIRED_FIELDS.get(type(candidate).__name__)
    if required is None:
        raise SchemaValidationError(f"Unsupported candidate type: {type(candidate).__name__}")
    missing_from_shape = [name for name in required if name not in field_names]
    if missing_from_shape:
        raise SchemaValidationError(f"Candidate shape missing field(s): {', '.join(missing_from_shape)}")
    missing_values = [name for name in required if getattr(candidate, name) in (None, "", ())]
    if missing_values:
        raise MissingRequiredFieldError(f"Missing required field(s): {', '.join(missing_values)}")
    if hasattr(candidate, "quantity") and getattr(candidate, "quantity") < 1:
        raise SchemaValidationError("Card quantity must be at least 1")
