# Phase 32C - Scryfall Bulk Data Foundation Implementation Report

Status: internally complete

## Summary

Phase 32C implements the local-first, fixture-first Scryfall bulk snapshot
foundation authorized by Phase 32B.

The implementation adds deterministic manifest models and validation helpers for
local Scryfall bulk snapshot fixtures. It does not download Scryfall data, write
snapshot files, read SQLite, add schema, add repositories, rewrite providers,
replace card lookup, import Scryfall Tagger data, implement migration
monitoring, call LLMs, add UI, calculate analytics, or generate
recommendations.

## Dependency

Phase 32C may begin because Phase 32B outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

## Files Added

```text
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/bulk_manifest.json
tests/fixtures/scryfall/default_cards_snapshot.json
tests/fixtures/scryfall/malformed_bulk_snapshot.json
```

## Files Modified

```text
codie/cards/__init__.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Interface

```text
SCRYFALL_BULK_SNAPSHOT_VERSION
ScryfallBulkSnapshotError
ScryfallBulkFileRef
ScryfallBulkSnapshotManifest
ScryfallBulkSnapshotValidationReport
build_scryfall_bulk_snapshot_manifest(...)
validate_scryfall_bulk_snapshot_manifest(...)
scryfall_bulk_snapshot_manifest_to_dict(...)
load_scryfall_bulk_snapshot_fixture(...)
```

The implementation intentionally does not expose
`calculate_scryfall_bulk_snapshot_hash(...)` as public API because the accepted
Phase 32B contract did not authorize that symbol. Stable content hashing is
implemented internally and remains visible through the manifest `content_hash`
field.

## Behavior Implemented

```text
manifest serializes deterministically
manifest round-trips through dictionary-compatible form
manifest models are frozen value objects
builder does not mutate input metadata
content hash is stable
card count is recorded
bulk data type remains visible
source URI remains visible when provided
generated_at remains visible when provided
imported_at remains visible when provided
raw metadata remains visible
fixture loading is local-only
valid fixture creates a validation report
malformed JSON fails cleanly
missing Scryfall id fails cleanly
missing card name fails cleanly
optional fields may be missing
oracle_id is preserved when available
released_at is preserved when available
legalities are preserved when available
card_faces are preserved when available
produced_mana is preserved when available
raw card payloads are preserved in immutable form
hash/count mismatches remain visible in validation errors
```

## Boundaries Preserved

```text
No live Scryfall API calls.
No bulk download implementation.
No background refresh jobs.
No schema changes.
No repository changes.
No SQLite reads or writes.
No provider rewrite.
No card lookup replacement.
No canonicalization changes.
No analytics changes.
No migration monitoring implementation.
No Scryfall Tagger import.
No UI work.
No LLM calls.
No recommendation generation.
```

## Phase 2 Relationship

Phase 2 remains authoritative for current Scryfall truth behavior.

This phase does not rewrite or invalidate:

```text
codie/cards/normalization.py
codie/cards/importer.py
codie/cards/lookup.py
codie/providers/scryfall/models.py
codie/providers/scryfall/bulk.py
tests/test_scryfall_truth.py
```

Identity rules preserved:

```text
scryfall_id remains enforced card identity
oracle_id remains analytics grouping identity
raw Scryfall JSON remains preserved
Scryfall remains the card truth source
```

## Validation

Focused tests:

```text
python -m unittest tests.test_scryfall_bulk_snapshots -v
Ran 11 tests
OK
```

Phase 32C outside validation returned PASS WITH REVIEW NOTES. The follow-up
review-note correction was applied before Phase 33A:

```text
fixture metadata bulk_type is used when caller does not override it
explicit bulk_type still overrides fixture metadata
manifest dictionary round-trip reconstructs file_refs and compares full serialized equality
```

Full validation is recorded in:

```text
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
```

## Next Gate

Send Phase 32C to outside validation.

Do not begin Phase 33A or Scryfall migration monitoring until Phase 32C outside
validation returns PASS or PASS WITH REVIEW NOTES.
