# Phase 4A TopDeck Provider Adapter Contract

## Objective

Implement the first real tournament-source adapter. TopDeck fetches/parses only and emits provider candidate models for ingestion.

## Files Created

- `codie/providers/topdeck/__init__.py`
- `codie/providers/topdeck/client.py`
- `codie/providers/topdeck/parser.py`
- `codie/providers/topdeck/models.py`
- `tests/fixtures/topdeck/*.json`
- `tests/test_provider_topdeck.py`

## Public Functions And Classes

- `TopDeckClient`
- `TopDeckProvider`
- `TopDeckProvider.fetch_event`
- `TopDeckProvider.fetch_deck`
- `TopDeckProvider.parse_event`
- `TopDeckProvider.parse_deck`

## Schema Impact

None. TopDeck emits `RawPayload`, `SourceEventCandidate`, `SourceDeckCandidate`, and `SourceDeckCardCandidate`.

## Dependencies

Uses provider base/errors/models and Python standard library HTTP utilities. Tests use injected fixture transports and do not perform live network calls.

## Test Cases

- Valid event fixture parses into `SourceEventCandidate`.
- Event fixture with missing optional fields parses.
- Missing required event field raises `ParseError`.
- Malformed event payload raises `ParseError`.
- Valid deck fixture parses into `SourceDeckCandidate`.
- Deck cards parse into `SourceDeckCardCandidate`.
- Missing required deck field raises `ParseError`.
- Fixture transport fetch/parse path works without live network.
- Network failure raises `NetworkError`.
- HTTP 429 raises `RateLimitError`.
- Ingestion preserves TopDeck raw payload JSON and hash.

## Failure Modes

- API unreachable: `NetworkError`, retryable.
- Rate limit: `RateLimitError`, retryable.
- Malformed response: `ParseError`, non-retryable.
- Missing required field: `ParseError`, non-retryable.
- Card resolution failure remains ingestion pipeline responsibility.

## Architecture Compliance

- No database, repository, cards, ingestion, analytics, recommendation, or sqlite imports in provider code.
- No canonicalization, analytics, UI, or recommendation behavior.
- No live network calls in tests.
