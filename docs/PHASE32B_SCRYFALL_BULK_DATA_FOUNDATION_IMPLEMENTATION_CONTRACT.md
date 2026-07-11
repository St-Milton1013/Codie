# Phase 32B - Scryfall Bulk Data Foundation Implementation Contract

Status: implementation contract only

## Purpose

Phase 32B defines the exact allowed implementation shape for the future
Scryfall bulk data foundation.

Phase 32A accepted the contract boundary. Phase 32B narrows the implementation
surface so a later packet can add fixture-first, local-only Scryfall bulk
snapshot manifest models and validation helpers without adding live Scryfall
download behavior, schema, repositories, provider rewrites, lookup replacement,
analytics, recommendations, UI, or LLM calls.

This phase does not implement Scryfall bulk snapshot code.

## Accepted Dependency

Phase 32B may begin because Phase 32A outside validation returned:

```text
PASS WITH REVIEW NOTES
```

## Authorized Future Implementation Scope

A later accepted implementation packet may add only:

```text
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/bulk_manifest.json
tests/fixtures/scryfall/default_cards_snapshot.json
tests/fixtures/scryfall/malformed_bulk_snapshot.json
```

The future implementation may update:

```text
codie/cards/__init__.py
```

only to export the new local Scryfall bulk snapshot model symbols.

## Future Public Interface

The future implementation may define:

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

## Future Model Responsibilities

The future models may represent:

```text
snapshot ID
snapshot version
bulk data type
source URI
source filename
content hash
card count
generated_at
imported_at
raw metadata
fixture path
validation status
validation errors
validation warnings
```

## Required Future Rules

The future implementation must:

```text
be local-first
be fixture-first
avoid live network dependency in tests
serialize manifests deterministically
round-trip manifests through dictionary form
preserve raw metadata
record content hash
record card count
record bulk data type
record source URI when provided
record generated_at and imported_at when provided
validate fixture shape before reporting success
reject malformed JSON
reject missing Scryfall id
reject missing card name
preserve oracle_id when available
preserve released_at when available
preserve legalities when available
preserve card_faces when available
preserve produced_mana when available
avoid mutating fixture input structures
remain recommendation-free
```

## Explicit Non-Goals

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

## Dependency Rules

Allowed future dependencies:

```text
Python standard library
existing codie.cards normalization helpers, only if explicitly imported and reviewed
```

Forbidden dependencies:

```text
requests
httpx
sqlite3
codie.db
repositories
providers
ingestion
analytics
recommendations
decision intelligence
evidence fusion
LLM SDKs
UI frameworks
```

## Required Future Tests

The later implementation packet must add tests proving:

```text
manifest serializes deterministically
manifest round-trips through dictionary form
manifest models are immutable or treated as immutable value objects
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
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears
```

## Validation For This Phase

Phase 32B may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Phase 32B must run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Next Gate

After Phase 32B outside validation returns PASS or PASS WITH REVIEW NOTES, a
Phase 32C implementation packet may add the approved local Scryfall bulk
snapshot model implementation.

Do not implement Scryfall bulk snapshot code in Phase 32B.
