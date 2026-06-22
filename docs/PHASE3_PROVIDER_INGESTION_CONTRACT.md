# Phase 3 Provider Contracts And Source Ingestion Contract

## Objective

Implement provider output models, provider base interface, structured provider errors, candidate validation, and a deck ingestion pipeline that runs `fetch -> parse -> validate -> resolve cards -> persist source records`.

## Files Created

- `codie/providers/models.py`
- `codie/providers/base.py`
- `codie/providers/errors.py`
- `codie/ingestion/__init__.py`
- `codie/ingestion/validation.py`
- `codie/ingestion/pipeline.py`
- `tests/test_ingestion_pipeline.py`

## Files Modified

- `codie/db/repositories/source.py`

## Public Functions And Classes

- `Provider`
- `RawPayload`
- `SourceEventCandidate`
- `SourceDeckCandidate`
- `SourceDeckCardCandidate`
- `SourcePrimerCandidate`
- `SourceComboCandidate`
- `ProviderError`
- `NetworkError`
- `RateLimitError`
- `ParseError`
- `MissingRequiredFieldError`
- `CardResolutionError`
- `SchemaValidationError`
- `CanonicalizationConflict`
- `DuplicateAmbiguityError`
- `validate_candidate`
- `DeckIngestionPipeline`
- `IngestionFailure`
- `IngestionResult`
- `SourceRepository.update_ingestion_run`
- `SourceRepository.get_ingestion_run`

## Schema Impact

None. Phase 3 uses existing Phase 1 tables: `ingestion_runs`, `provider_objects`, `source_events`, `source_decks`, and `source_deck_cards`.

## Dependencies

Python standard library, provider candidate models, `SourceRepository`, and `CardLookup`.

## Test Cases

- Mock provider successful parse and persistence.
- Mock provider malformed parse failure.
- Missing required field validation.
- Card resolution failure.
- Ingestion run logging.
- Raw payload hash preservation.
- Provider isolation from SQLite/repositories remains enforced.

## Failure Modes

Structured failures capture provider, pipeline, source URL, object type, error type, message, raw payload hash, occurrence timestamp, and retryability.

## Architecture Compliance

- Providers fetch and parse only.
- Providers do not import database, repositories, ingestion pipeline, or analytics.
- Persistence is orchestration-owned and repository-mediated.
- No canonicalization, analytics refresh, recommendations, or UI behavior is implemented in Phase 3.
