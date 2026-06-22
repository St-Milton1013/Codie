# Phase 2 Scryfall Truth Layer Contract

## Objective

Create the local Scryfall truth layer used to populate and resolve cards before any provider ingestion, canonicalization, analytics, recommendations, or UI work.

## Files Created

- `codie/cards/normalization.py`
- `codie/cards/importer.py`
- `codie/cards/lookup.py`
- `codie/providers/scryfall/models.py`
- `codie/providers/scryfall/bulk.py`
- `tests/fixtures/scryfall/bulk_cards.json`
- `tests/fixtures/scryfall/malformed.json`
- `tests/test_scryfall_truth.py`

## Public Functions And Classes

- `normalize_card_name`
- `ScryfallImporter`
- `CardLookup`
- `LookupResult`
- `ScryfallCard`
- `ScryfallParseError`
- `load_bulk_cards`

## Schema Impact

No schema changes. Phase 2 writes to the existing `cards` table through `CoreRepository.upsert_card`.

## Dependencies

Python standard library only. The implementation is local-first and accepts local Scryfall bulk/cache files. Live Scryfall download is intentionally outside this contract.

## Test Cases

- Loads local Scryfall bulk fixture.
- Resolves exact card names.
- Resolves injected aliases, registry-backed aliases, and local fuzzy names.
- Stores `scryfall_id` and `oracle_id`.
- Preserves raw Scryfall JSON.
- Handles MDFC/card faces.
- Extracts commander legality and commander-candidate flag.
- Extracts produced mana from root or faces.
- Fails cleanly on malformed JSON and missing required fields.

## Failure Modes

- Invalid JSON raises `ScryfallParseError`.
- Missing `id` or `name` raises `ScryfallParseError`.
- Empty lookup queries return unresolved results.
- No local match returns unresolved results with the best local fuzzy score.
- Missing optional Scryfall fields are accepted.

## Architecture Compliance

- Scryfall provider code parses only and does not import repositories or open SQLite connections.
- Persistence routes through the `cards` layer and `CoreRepository`.
- Scryfall remains the only implemented card-truth source.
- No tournament analytics, recommendations, strategy inference, or UI behavior is introduced.
