# Phase 33A - Scryfall Migration Monitoring Contract

Status: contract only

## Purpose

Phase 33A defines the future Scryfall migration monitoring layer for Codie.

Scryfall bulk snapshots now have a local, fixture-first manifest foundation.
The next risk is card-truth drift between snapshots: renamed cards, changed
oracle links, replaced Scryfall IDs, enum expansion, missing required fields,
and shape changes that could corrupt card lookup, canonical identity,
analytics, simulator card behavior, Tagger mappings, and future reports.

This phase does not implement migration monitoring.

## Accepted Dependency

Phase 33A may begin because Phase 32C outside validation returned:

```text
PASS WITH REVIEW NOTES
```

The Phase 32C review-note correction was applied before this contract:

```text
fixture metadata bulk_type is used when caller does not override it
explicit bulk_type still overrides fixture metadata
manifest dictionary round-trip reconstructs file_refs and compares full serialized equality
```

## Future Scope To Define

A future accepted implementation packet may add local, fixture-first Scryfall
migration monitoring models and validators covering:

```text
snapshot-to-snapshot diff reports
required field validation
optional field drift reporting
unknown field handling
unknown enum handling
schema-breaking condition detection
renamed card detection
oracle_id continuity checks
scryfall_id replacement detection
manual review queue inputs
replay-safe migration records
snapshot activation blocking rules
affected consumer reporting
validation and rollback behavior
```

## Relationship To Phase 32

Phase 32 remains the local Scryfall bulk snapshot foundation.

Future migration monitoring must consume already-loaded local snapshot
manifests/card payloads. It must not download live Scryfall data, write active
snapshots, persist migration records, or replace card lookup unless a later
contract explicitly authorizes those behaviors.

Accepted Phase 32 surfaces:

```text
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/bulk_manifest.json
tests/fixtures/scryfall/default_cards_snapshot.json
tests/fixtures/scryfall/malformed_bulk_snapshot.json
```

Phase 2 identity rules remain unchanged:

```text
scryfall_id remains enforced card identity
oracle_id remains analytics grouping identity
raw Scryfall JSON remains preserved
Scryfall remains the card truth source
```

## Future Authorized Implementation Shape

A later accepted implementation contract may authorize files such as:

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

only to export public migration-monitoring symbols.

No schema, repository, provider, dependency, UI, or live-network files may be
changed unless a later contract explicitly authorizes them.

## Future Public Interface Candidates

The later implementation may define pure local models/functions such as:

```text
SCRYFALL_MIGRATION_MONITOR_VERSION
ScryfallMigrationMonitoringError
ScryfallFieldChange
ScryfallEnumChange
ScryfallIdentityChange
ScryfallMigrationAffectedConsumer
ScryfallMigrationRecord
ScryfallMigrationReport
ScryfallMigrationOptions
build_scryfall_migration_report(...)
validate_scryfall_migration_report(...)
scryfall_migration_report_to_dict(...)
```

These are candidates, not implementation authorization in Phase 33A.

## Required Future Model Fields

Future migration report models must preserve:

```text
report_id
monitor_version
previous_snapshot_id
next_snapshot_id
previous_content_hash
next_content_hash
generated_at
required_field_failures
optional_field_changes
unknown_fields
unknown_enums
identity_changes
schema_breaking_conditions
activation_blocked
activation_block_reasons
affected_consumers
manual_review_items
validation_errors
validation_warnings
```

Future identity-change records must preserve:

```text
change_id
change_type
previous_scryfall_id
next_scryfall_id
previous_oracle_id
next_oracle_id
previous_name
next_name
previous_released_at
next_released_at
field_deltas
requires_manual_review
blocking_severity
```

Future affected-consumer records must preserve:

```text
consumer_id
consumer_type
affected_reason
affected_identity_keys
blocking_severity
recommended_review_action
```

`recommended_review_action` is operational wording only. It must not be a deck,
card, strategy, play/cut, or recommendation-engine output.

## Required Field Rules

Future implementation must treat these card fields as required for Scryfall
truth compatibility:

```text
id or scryfall_id
name
```

Future implementation must treat these fields as optional but monitored when
present:

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

Missing optional fields must not fail migration monitoring by default, but they
must remain visible as coverage/shape warnings when materially changed between
snapshots.

## Unknown Field Rules

Future implementation must:

```text
preserve unknown fields in raw payloads
report newly seen fields
report removed fields
distinguish additive unknown fields from breaking missing required fields
avoid failing activation for additive unknown fields by default
allow future policy to escalate unknown fields to manual review
```

Unknown fields must not be silently ignored.

## Unknown Enum Rules

Future implementation must report unknown enum-like values for monitored fields
such as:

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
They should block activation only when a future policy marks that enum as
blocking or when the unknown value makes identity/legality interpretation
unsafe.

## Schema-Breaking Conditions

Future implementation must mark migration output as activation-blocking when
any of these occur:

```text
missing required Scryfall ID
missing required card name
duplicate Scryfall ID within the next snapshot
same Scryfall ID mapped to conflicting oracle IDs without an explicit migration record
same oracle ID split across incompatible card identities without an explicit migration record
hash/count mismatch in input snapshots
malformed snapshot payload
non-deterministic migration report serialization
```

Activation-blocking means the future migration report recommends blocking
promotion of the new snapshot into any active lookup/cache path. Phase 33A does
not implement snapshot activation.

## Snapshot Activation Blocking Rules

Future implementation must:

```text
produce activation_blocked boolean
preserve activation_block_reasons
never silently activate a snapshot
never mutate existing active snapshots
never rewrite historical migration reports
never change card lookup behavior directly
```

Activation decisions remain report output only until a later persistence or
snapshot-activation contract exists.

## Affected Consumer Reporting

Future implementation must report likely affected consumers without importing
or mutating those layers:

```text
card lookup
canonicalization
analytics
simulator card definitions
Scryfall Tagger oracle mappings
Commander Spellbook card references
user deck resolution
report/export surfaces
```

Affected-consumer reporting is informational. It must not call, import, or
mutate these consumers in Phase 33 implementation.

## Manual Review Queue Inputs

Future implementation may produce manual-review item packets for:

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

Manual-review output must remain in-memory/report-only unless a later contract
authorizes persistence.

## Validation And Rollback Behavior

Future implementation must:

```text
validate previous and next snapshot manifests before comparison
fail cleanly on malformed snapshot inputs
produce deterministic reports
preserve previous snapshot references for rollback planning
preserve next snapshot references for replay
label activation-blocking conditions
avoid mutating either input snapshot
avoid deleting or rewriting any raw payloads
```

Rollback behavior in this phase means report metadata only. No file, database,
or active snapshot rollback may be implemented without a later contract.

## Not Authorized In Phase 33A

```text
migration monitoring implementation
snapshot diff implementation
schema changes
repository changes
SQLite reads or writes
provider changes
live Scryfall API calls
bulk download implementation
file writing
snapshot activation
snapshot rollback
card lookup replacement
canonicalization changes
analytics changes
Scryfall Tagger import
Commander Spellbook changes
simulator behavior changes
UI work
LLM calls
recommendation generation
dependency changes
```

## Future Implementation Boundaries

Future implementation must not:

```text
override Scryfall card truth
change scryfall_id/oracle_id semantics
mutate old snapshots
silently ignore unknown fields
silently ignore unknown enum values
silently activate snapshots
write SQLite
write files
call live network APIs
import providers
import analytics
import recommendations
generate strategic claims
```

## Dependency Rules

Allowed future dependencies:

```text
Python standard library
codie.cards.scryfall_bulk_snapshots
```

Forbidden unless a later contract explicitly approves:

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

Future implementation must add tests proving:

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
affected consumers are reported
manual review items are produced for identity drift
previous and next snapshot hashes remain visible
input snapshots are not mutated
malformed inputs fail cleanly
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears
```

## Validation For This Phase

Phase 33A must only create:

```text
contract document
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Phase 33A must run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Next Gate

After Phase 33A outside validation returns PASS or PASS WITH REVIEW NOTES, a
Phase 33B implementation contract may define the exact implementation surface.

Do not implement Scryfall migration monitoring until Phase 33B is accepted.
