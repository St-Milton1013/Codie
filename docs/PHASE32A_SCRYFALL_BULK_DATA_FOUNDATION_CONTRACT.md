# Phase 32A - Scryfall Bulk Data Foundation Contract

Status: contract only

## Purpose

Phase 32A defines the future Scryfall bulk data foundation for Codie.

Scryfall is Codie's card truth source. Existing Phase 2 functionality supports
local Scryfall parsing and lookup. The post-31 roadmap adds a stronger bulk
snapshot foundation so Codie can reduce live API dependence, improve
reproducibility, support migration monitoring, support Tagger integration, and
make future card-truth refreshes auditable.

This phase does not implement bulk download, snapshot storage, schema changes,
repository changes, provider changes, or lookup replacement.

## Accepted Dependency

Phase 32A may begin because Phase 31R outside validation returned:

```text
PASS WITH REVIEW NOTES
```

## Future Scope To Define

A future accepted implementation packet may add a local-first Scryfall bulk
snapshot foundation covering:

```text
bulk data discovery metadata
snapshot manifest models
atomic local snapshot storage
raw payload preservation
card identity normalization input contracts
offline lookup cache inputs
migration compatibility inputs
snapshot validation reports
```

## Relationship To Phase 2

Phase 2 remains accepted and authoritative for current local Scryfall truth
behavior:

```text
codie/cards/normalization.py
codie/cards/importer.py
codie/cards/lookup.py
codie/providers/scryfall/models.py
codie/providers/scryfall/bulk.py
tests/test_scryfall_truth.py
```

Phase 32A must not invalidate or rewrite Phase 2. Future work must layer bulk
snapshot management around the accepted Scryfall truth layer without changing
card identity rules:

```text
scryfall_id remains enforced card identity
oracle_id remains analytics grouping identity
raw Scryfall JSON remains preserved
Scryfall remains the card truth source
```

## Future Authorized Implementation Shape

The next implementation contract may authorize files such as:

```text
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/bulk_manifest.json
tests/fixtures/scryfall/default_cards_snapshot.json
```

If persistence is required, a later contract must explicitly define schema and
repository changes before implementation.

## Future Public Interface Candidates

The later implementation may define pure local models/functions such as:

```text
ScryfallBulkSnapshotError
ScryfallBulkFileRef
ScryfallBulkSnapshotManifest
ScryfallBulkSnapshotValidationReport
build_scryfall_bulk_snapshot_manifest(...)
validate_scryfall_bulk_snapshot_manifest(...)
scryfall_bulk_snapshot_manifest_to_dict(...)
load_scryfall_bulk_snapshot_fixture(...)
```

These are candidates, not implementation authorization in Phase 32A.

## Required Future Rules

Future implementation must:

```text
be fixture-first
avoid live network dependency in tests
preserve raw Scryfall payload metadata
record snapshot generated_at/imported_at metadata
record bulk data type such as default_cards or oracle_cards
record source URI when provided
record content hash
record card count
record schema/version metadata
validate expected object shape before import
support deterministic manifest serialization
support atomic write semantics if file writing is introduced
reject malformed JSON fixtures
reject missing required Scryfall IDs
reject missing required names
preserve oracle_id when available
preserve released_at when available
preserve legalities when available
preserve card_faces when available
preserve produced_mana when available
preserve raw JSON
```

## Not Authorized In Phase 32A

```text
bulk download implementation
live Scryfall API calls
schema changes
repository changes
SQLite reads or writes
provider rewrite
card lookup replacement
canonicalization changes
analytics changes
recommendation generation
Tagger import
migration monitoring implementation
UI work
LLM calls
file writing
dependency changes
```

## Future Implementation Boundaries

Future implementation must not:

```text
override Scryfall card truth
change scryfall_id/oracle_id semantics
modify provider ingestion behavior
produce recommendations
infer strategic value
read tournament source tables
alter canonical or analytics records
make tests depend on live network access
silently ignore malformed records
silently mutate old snapshots
```

## Dependency Rules

Allowed future dependencies:

```text
Python standard library
existing codie.cards parsing/normalization helpers when explicitly reviewed
```

Forbidden unless a later contract explicitly approves:

```text
requests
httpx
sqlite3
codie.db repositories
providers
analytics
recommendations
decision intelligence
evidence fusion
LLM SDKs
UI frameworks
```

## Required Future Tests

Future implementation must add tests proving:

```text
manifest serializes deterministically
manifest round-trips through dictionary form
snapshot hash is stable
snapshot card count is recorded
raw payload metadata is preserved
fixture loading is local-only
malformed JSON fails cleanly
missing Scryfall ID fails cleanly
missing card name fails cleanly
optional fields may be missing
card_faces are preserved when present
oracle_id is preserved when present
released_at is preserved when present
legalities are preserved when present
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears
```

## Validation For This Phase

Phase 32A must only create:

```text
contract document
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Phase 32A must run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Next Gate

After Phase 32A outside validation returns PASS or PASS WITH REVIEW NOTES, a
Phase 32B implementation contract may define the exact implementation surface.

Do not implement Scryfall bulk snapshot code until Phase 32B is accepted.
