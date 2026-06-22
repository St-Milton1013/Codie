# Phase 4E Hareruya Provider Adapter Contract

## Objective

Implement the Hareruya provider adapter as a Japanese/regional tournament and deck source. Hareruya fetches/parses only and emits provider candidate models for ingestion.

Hareruya is a regional source. Its parser must use Hareruya-specific page structure and must not reuse MTGDecks or MTGTop8 commander heuristics unless a Hareruya fixture proves the structure.

## Scope

Files to create:

- `codie/providers/hareruya/__init__.py`
- `codie/providers/hareruya/client.py`
- `codie/providers/hareruya/parser.py`
- `codie/providers/hareruya/models.py`
- `tests/fixtures/hareruya/metagame_page_202.html`
- `tests/fixtures/hareruya/deck_page_101.html`
- `tests/fixtures/hareruya/source-notes.md`
- `tests/test_provider_hareruya.py`

No schema changes are allowed in this phase.

## Public Interface

```python
class HareruyaProvider(Provider):
    def fetch_metagame_page(self, metagame_url: str) -> str: ...
    def fetch_deck_page(self, deck_url: str) -> str: ...
    def parse_metagame_page(self, html: str) -> SourceEventCandidate: ...
    def parse_deck_page(self, html: str, event_key: str) -> SourceDeckCandidate: ...
```

Naming may be adjusted if fixtures show a better source-specific split, but public methods must remain simple fetch/parse methods and must not persist data.

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

## Event Or Metagame Fields

Parse when visible:

- `provider = "hareruya"`
- `provider_event_id`
- `source_url`
- `original_source = "Hareruya"`
- `original_source_url`
- `event_name`
- `event_date`
- `format`
- `region`
- `country`
- `player_count`
- `deck_count`
- `raw_payload`

Defaults:

- `country = "JP"` when the page is explicitly Hareruya Japan.
- `region = "Japan"` unless the page exposes a more precise region.

Do not invent player/deck counts when absent.

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

Hareruya-specific commander rule:

- Prefer explicit deck page metadata.
- A first isolated card line can be a fallback commander candidate only when Hareruya metadata confirms the deck format/type is Commander.
- Do not use MTGDecks-style sideboard splitting for commander detection.

## Deck Card Fields

Parse:

- `source_deck_key`
- `raw_name`
- `quantity`
- `source_zone`
- `source_order`
- `raw_entry`

Japanese card names must be preserved as raw names if shown. Card resolution and Scryfall matching remain ingestion/canonical responsibilities, not provider responsibilities.

## Hareruya-Specific Rules

- Treat source as regional evidence.
- Preserve raw HTML.
- Preserve original source URLs.
- Do not translate or normalize Japanese names in the provider.
- Do not infer strategy/archetype.
- Skip unavailable decklists.
- Fail cleanly on unsupported page structures.

## Failure Behavior

- Network failure: `NetworkError`, retryable.
- Rate limit or temporary server throttle: `RateLimitError`, retryable.
- Missing event/deck identity: `MissingRequiredFieldError`, non-retryable.
- Malformed HTML: `ParseError`, non-retryable.
- Unsupported parsed structure: `SchemaValidationError`, non-retryable.

## Required Tests

- Valid metagame/event fixture parses `SourceEventCandidate`.
- Valid deck fixture parses `SourceDeckCandidate`.
- Deck cards parse into `SourceDeckCardCandidate`.
- Japanese/raw card names are preserved.
- Missing optional fields are allowed.
- Missing required event identity fails cleanly.
- Missing required deck identity fails cleanly.
- Malformed HTML fails cleanly.
- Hidden/unavailable decklists are skipped.
- Raw payload hash is preserved.
- Provider boundary test still passes.
- Full suite passes.

## Do Not Do

- Do not canonicalize.
- Do not calculate regional metrics yet.
- Do not calculate analytics.
- Do not translate card names.
- Do not write SQLite directly.
- Do not start primer/combo/recommendation work in this phase.
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
