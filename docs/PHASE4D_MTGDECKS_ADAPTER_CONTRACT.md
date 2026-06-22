# Phase 4D MTGDecks Provider Adapter Contract

## Objective

Implement the MTGDecks provider adapter as a secondary tournament and deck source. MTGDecks fetches/parses only and emits provider candidate models for ingestion.

MTGDecks is mirror-risk data. It must not be treated as independent analytics evidence until Phase 5 canonicalization confirms whether each event/deck is unique or duplicated from another source.

## Scope

Files to create:

- `codie/providers/mtgdecks/__init__.py`
- `codie/providers/mtgdecks/client.py`
- `codie/providers/mtgdecks/parser.py`
- `codie/providers/mtgdecks/models.py`
- `tests/fixtures/mtgdecks/event_page_789.html`
- `tests/fixtures/mtgdecks/deck_export.txt`
- `tests/fixtures/mtgdecks/source-notes.md`
- `tests/test_provider_mtgdecks.py`

No schema changes are allowed in this phase.

## Public Interface

```python
class MTGDecksProvider(Provider):
    def fetch_event_page(self, event_url: str) -> str: ...
    def fetch_deck_page(self, deck_url: str) -> str: ...
    def parse_event_page(self, html: str) -> SourceEventCandidate: ...
    def parse_deck_page(self, html: str, event_key: str) -> SourceDeckCandidate: ...
```

The provider may expose helper methods only if they remain provider-local and do not import project persistence, analytics, canonicalization, ingestion, or card lookup code.

## Dependencies

Allowed:

- Python standard library
- `beautifulsoup4`
- `codie.providers.base`
- `codie.providers.errors`
- `codie.providers.models`

Forbidden:

- `codie.db`
- repositories
- `sqlite3`
- `codie.ingestion`
- `codie.cards`
- `codie.analytics`
- `codie.recommendations`
- `codie.canonical`

## Candidate Output

Emit only:

- `RawPayload`
- `SourceEventCandidate`
- `SourceDeckCandidate`
- `SourceDeckCardCandidate`

## Event Fields

Parse when visible:

- `provider = "mtgdecks"`
- `provider_event_id`
- `source_url`
- `original_source = "MTGDecks"`
- `original_source_url`
- `event_name`
- `event_date`
- `format`
- `region`
- `country`
- `player_count`
- `deck_count`
- `raw_payload`

Missing event identity is a structured failure.

## Deck Fields

Parse when visible:

- `provider_deck_id`
- `source_event_key`
- `source_url`
- `download_url`
- `deck_title`
- `commander_text`
- `pilot_name`
- `rank`
- `rank_label`
- `record`
- `raw_payload`

Do not infer commanders from sideboards unless the fixture proves the site explicitly labels commander sections.

## Deck Card Fields

Parse:

- `source_deck_key`
- `raw_name`
- `quantity`
- `source_zone`
- `source_order`
- `raw_entry`

Auxiliary cards, stickers, attractions, or site-specific non-deck sections must not be treated as canonical deck cards later. In this provider phase, preserve them only if the source exposes them as explicit sections and label the `source_zone` accurately.

## MTGDecks-Specific Rules

- Treat MTGDecks as mirror-risk until canonical dedupe.
- Do not calculate analytics.
- Do not mark source records as independently analytics-safe inside the provider.
- Preserve original page/export text.
- Prefer explicit event/deck IDs from URLs or page metadata.
- Skip unavailable decklists.
- Fail cleanly on malformed or unsupported parsed structures.

## Failure Behavior

- Network failure: `NetworkError`, retryable.
- Rate limit or temporary server throttle: `RateLimitError`, retryable.
- Missing event/deck identity: `MissingRequiredFieldError`, non-retryable.
- Malformed HTML/text: `ParseError`, non-retryable.
- Unsupported card/deck structure: `SchemaValidationError`, non-retryable.

## Required Tests

- Valid event fixture parses `SourceEventCandidate`.
- Valid deck fixture parses `SourceDeckCandidate`.
- Deck cards parse into `SourceDeckCardCandidate`.
- Missing optional fields are allowed.
- Missing required event identity fails cleanly.
- Missing required deck identity fails cleanly.
- Malformed HTML/text fails cleanly.
- Hidden/unavailable decklists are skipped.
- Raw payload hash is preserved.
- Provider boundary test still passes.
- Full suite passes.

## Do Not Do

- Do not canonicalize.
- Do not dedupe events/decks.
- Do not calculate analytics.
- Do not write SQLite directly.
- Do not start Hareruya in this phase.
- Do not copy third-party scraper code.

## Completion Report Requirements

Return:

- Files created
- Files modified
- Tests added
- Tests run
- Actual test output
- Static check output
- Known fixture limitations
- Recommended next step
