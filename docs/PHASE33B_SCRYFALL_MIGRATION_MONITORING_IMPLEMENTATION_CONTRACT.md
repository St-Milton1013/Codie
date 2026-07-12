# Phase 33B - Scryfall Migration Monitoring Implementation Contract

Status: implementation contract only

## Purpose

Phase 33B defines the exact allowed implementation shape for the future
Scryfall migration monitoring layer.

Phase 33A accepted the migration-monitoring boundary. Phase 33B narrows the
future implementation surface so a later packet can add local, fixture-first
snapshot-to-snapshot migration report models and validators without adding live
Scryfall calls, file writing, schema, repositories, provider rewrites, lookup
replacement, analytics, recommendations, UI, or LLM calls.

This phase does not implement Scryfall migration monitoring.

## Accepted Dependency

Phase 33B may begin because Phase 33A outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

## Authorized Future Implementation Scope

A later accepted implementation packet may add only:

```text
codie/cards/scryfall_migration_monitoring.py
tests/test_scryfall_migration_monitoring.py
tests/fixtures/scryfall/migration_previous_snapshot.json
tests/fixtures/scryfall/migration_next_snapshot.json
tests/fixtures/scryfall/migration_unknown_fields_snapshot.json
tests/fixtures/scryfall/migration_unknown_enums_snapshot.json
tests/fixtures/scryfall/migration_breaking_snapshot.json
```

The future implementation may update:

```text
codie/cards/__init__.py
```

only to export public Scryfall migration-monitoring model symbols.

No schema, repository, provider, dependency, UI, live-network, or file-writing
files may be changed in the implementation packet.

## Future Public Interface

The future implementation may define:

```text
SCRYFALL_MIGRATION_MONITOR_VERSION
ScryfallMigrationMonitoringError
ScryfallFieldChange
ScryfallEnumChange
ScryfallIdentityChange
ScryfallMigrationAffectedConsumer
ScryfallMigrationManualReviewItem
ScryfallMigrationReport
ScryfallMigrationOptions
build_scryfall_migration_report(...)
validate_scryfall_migration_report(...)
scryfall_migration_report_to_dict(...)
```

Do not expose persistence, activation, rollback, downloader, repository, or
provider APIs in the future implementation.

## Future Model Responsibilities

The future implementation may represent:

```text
report ID
monitor version
previous snapshot ID
next snapshot ID
previous content hash
next content hash
generated_at
required field failures
optional field changes
unknown fields
unknown enum values
identity changes
schema-breaking conditions
activation_blocked
activation_block_reasons
affected consumers
manual review items
validation errors
validation warnings
```

## Future Required Fields

The future implementation must treat these Scryfall card fields as required:

```text
id or scryfall_id
name
```

Missing either required field in a compared snapshot must produce:

```text
validation error
schema-breaking condition
activation_blocked = true
activation block reason
manual review item
```

## Future Optional Monitored Fields

The future implementation must preserve and monitor these fields when present:

```text
oracle_id
released_at
legalities
card_faces
produced_mana
layout
type_line
mana_cost
color_identity
```

Missing optional fields must not fail monitoring by default, but meaningful
changes must remain visible in warnings, field-change records, or coverage
metadata.

## Future Unknown Field Handling

The future implementation must:

```text
preserve unknown fields in raw payloads
report newly seen fields
report removed fields
distinguish additive unknown fields from breaking missing required fields
avoid blocking activation for additive unknown fields by default
allow future policy to escalate unknown fields to manual review
```

Unknown fields must not be silently ignored.

## Future Unknown Enum Handling

The future implementation must report unknown enum-like values for monitored
fields such as:

```text
layout
legalities values
games
finishes
promo_types
frame_effects
security_stamp
border_color
rarity
```

Unknown enum values should create warnings/manual-review items by default.
They should block activation only when policy marks that enum as blocking or
when the unknown value makes identity/legality interpretation unsafe.

## Future Schema-Breaking Conditions

The future implementation must mark reports as activation-blocking when any of
these occur:

```text
missing required Scryfall ID
missing required card name
duplicate Scryfall ID within the next snapshot
same Scryfall ID mapped to conflicting oracle IDs without explicit migration record
same oracle ID split across incompatible card identities without explicit migration record
hash/count mismatch in input snapshots
malformed snapshot payload
non-deterministic migration report serialization
```

## Future Snapshot Activation Blocking

The future implementation must:

```text
produce activation_blocked boolean
preserve activation_block_reasons
never silently activate a snapshot
never mutate existing active snapshots
never rewrite historical migration reports
never change card lookup behavior directly
```

Activation blocking is report metadata only. The future implementation must not
write files, update databases, replace active snapshots, or trigger rollback.

## Future Affected Consumer Reporting

The future implementation may report likely affected consumers as data only:

```text
card_lookup
canonicalization
analytics
simulator_card_definitions
scryfall_tagger_oracle_mappings
commander_spellbook_card_references
user_deck_resolution
report_export_surfaces
```

The implementation must not import, call, or mutate those consumers.

## Future Manual Review Items

The future implementation may produce manual review item packets for:

```text
renamed cards
oracle_id changes
scryfall_id replacements
unknown enum values
schema-breaking conditions
possible duplicate identities
missing optional field coverage changes
consumer-impact warnings
```

Manual review output must remain in-memory/report-only.

## Relationship To Phase 32

Future implementation may import:

```text
codie.cards.scryfall_bulk_snapshots
```

to use accepted local snapshot manifest/report models.

Future implementation must not change:

```text
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
```

unless a focused correction is separately justified.

## Required Future Rules

The future implementation must:

```text
be local-first
be fixture-first
avoid live network dependency in tests
consume local snapshot reports or local snapshot fixture payloads
avoid mutating input snapshots
preserve previous snapshot references
preserve next snapshot references
preserve content hashes
serialize migration reports deterministically
round-trip migration reports through dictionary-compatible form
fail cleanly on malformed inputs
produce visible validation errors
produce visible validation warnings
produce visible activation block reasons
produce visible manual review items
remain recommendation-free
```

## Explicit Non-Goals

```text
No migration monitoring implementation in Phase 33B.
No snapshot diff implementation in Phase 33B.
No schema changes.
No repository changes.
No SQLite reads or writes.
No provider changes.
No live Scryfall API calls.
No bulk download implementation.
No file writing.
No snapshot activation.
No snapshot rollback.
No card lookup replacement.
No canonicalization changes.
No analytics changes.
No Scryfall Tagger import.
No Commander Spellbook changes.
No simulator behavior changes.
No UI work.
No LLM calls.
No recommendation generation.
No dependency changes.
```

## Dependency Rules

Allowed future dependencies:

```text
Python standard library
codie.cards.scryfall_bulk_snapshots
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
snapshot-to-snapshot report serializes deterministically
report round-trips through dictionary-compatible form
required missing Scryfall ID blocks activation
required missing card name blocks activation
duplicate Scryfall ID blocks activation
oracle_id continuity change is visible
scryfall_id replacement is visible
renamed card detection is visible
unknown additive fields are reported but not blocking by default
unknown enum values are reported
schema-breaking conditions block activation
affected consumers are reported without importing those consumers
manual review items are produced for identity drift
previous and next snapshot hashes remain visible
input snapshots are not mutated
malformed inputs fail cleanly
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears
```

## Validation For This Phase

Phase 33B may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Phase 33B must run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Next Gate

After Phase 33B outside validation returns PASS or PASS WITH REVIEW NOTES, a
Phase 33C implementation packet may add the approved local Scryfall migration
monitoring model implementation.

Do not implement Scryfall migration monitoring in Phase 33B.
