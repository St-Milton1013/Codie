"""Ingestion validation and pipeline orchestration."""

from .pipeline import DeckIngestionPipeline, IngestionFailure, IngestionResult
from .validation import validate_candidate

__all__ = ["DeckIngestionPipeline", "IngestionFailure", "IngestionResult", "validate_candidate"]
