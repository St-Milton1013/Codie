# Phase 7A Commander Spellbook Combo Evidence Contract

## Objective

Sync Commander Spellbook combo evidence into Codie without creating recommendations, strategy claims, or invented combo lines.

Phase 7A is evidence-only. It stores source combo metadata, resolves known combo components to local card identities when possible, preserves raw payloads, and updates combo evidence counts.

## Files Created

- `codie/providers/spellbook/__init__.py`
- `codie/providers/spellbook/client.py`
- `codie/providers/spellbook/models.py`
- `codie/providers/spellbook/parser.py`
- `codie/combos/__init__.py`
- `codie/combos/sync.py`
- `tests/fixtures/spellbook/variants_sample.json`
- `tests/fixtures/spellbook/missing_optional.json`
- `tests/fixtures/spellbook/missing_required.json`
- `tests/fixtures/spellbook/malformed_payload.json`
- `tests/fixtures/spellbook/source-notes.md`
- `tests/test_provider_spellbook.py`
- `tests/test_combo_sync.py`

## Files Modified

- `codie/db/repositories/curated.py`
- `codie/db/repositories/source.py`
- `tests/test_architecture_boundaries.py`

## Schema Impact

None.

Existing tables used:

- `source_combos`
- `combos`
- `combo_cards`
- `evidence_counts`
- `cards`

## Public API

```python
class SpellbookProvider(Provider):
    def fetch_variants(self) -> dict: ...
    def parse_variants(self, raw: dict | list) -> tuple[SourceComboCandidate, ...]: ...

class ComboEvidenceSync:
    def sync_candidates(self, candidates: Iterable[SourceComboCandidate]) -> ComboSyncResult: ...
```

## Candidate Output

Spellbook provider emits:

- `RawPayload`
- `SourceComboCandidate`
- `SourceComboCardCandidate`

Provider output is not persisted directly by the provider.

## Dependencies

Provider allowed:

- Python standard library
- `codie.providers.base`
- `codie.providers.errors`
- `codie.providers.models`

Provider forbidden:

- `codie.db`
- repositories
- `sqlite3`
- `codie.ingestion`
- `codie.cards`
- `codie.analytics`
- `codie.recommendations`
- `codie.canonical`

Sync service allowed:

- `codie.cards.lookup`
- `codie.db.repositories.source`
- `codie.db.repositories.curated`
- `codie.db.repositories.analytics`

## Failure Modes

- Malformed top-level payload raises `ParseError`.
- Missing combo identity raises `MissingRequiredFieldError`.
- Missing component card name raises `SchemaValidationError`.
- Card resolution misses are stored as unresolved component names with null Scryfall fields; sync does not invent identities.
- Duplicate syncs upsert the same combo and do not duplicate combo card rows.

## Acceptance Tests

- valid Spellbook fixture parses combo candidates.
- combo components parse into card candidates.
- raw payload hash is preserved.
- missing optional fields are allowed.
- missing required fields fail cleanly.
- malformed payload fails cleanly.
- provider boundary test passes.
- sync persists `source_combos`.
- sync persists `combos`.
- sync persists `combo_cards`.
- sync resolves cards through local lookup when available.
- sync stores unresolved components without invented card IDs.
- sync updates `evidence_counts.combo_evidence_count`.
- sync is idempotent.

## Do Not Do

- Do not implement recommendations.
- Do not calculate combo completion for user decks yet.
- Do not infer combos from decklists.
- Do not invent combo lines.
- Do not write SQLite from provider code.
- Do not store primer body or unrelated Spellbook metadata.
