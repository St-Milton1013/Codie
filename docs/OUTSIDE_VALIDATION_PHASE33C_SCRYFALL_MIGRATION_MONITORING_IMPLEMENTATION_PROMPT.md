# Outside Validation Prompt - Phase 33C Scryfall Migration Monitoring Implementation

Validate Codie Phase 33C against:

```text
docs/PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
docs/PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
```

## Required Review Files

Review:

```text
docs/PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_PROMPT.md
docs/PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
codie/cards/scryfall_migration_monitoring.py
codie/cards/scryfall_bulk_snapshots.py
codie/cards/__init__.py
tests/test_scryfall_migration_monitoring.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/migration_previous_snapshot.json
tests/fixtures/scryfall/migration_next_snapshot.json
tests/fixtures/scryfall/migration_unknown_fields_snapshot.json
tests/fixtures/scryfall/migration_unknown_enums_snapshot.json
tests/fixtures/scryfall/migration_breaking_snapshot.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Implementation Scope

Confirm Phase 33C implements only:

```text
local Scryfall migration report models
local snapshot-to-snapshot comparison helpers
deterministic serialization
validation helpers
fixture-based tests
export-only updates to codie/cards/__init__.py
```

Reject if Phase 33C adds:

```text
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
analytics mutation
Scryfall Tagger import
Commander Spellbook changes
simulator behavior changes
UI work
LLM calls
recommendation generation
dependency changes
```

## Confirm Public Interface

Confirm the public interface remains limited to:

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

Reject if the implementation exposes persistence, activation, rollback,
downloader, repository, provider, or lookup-replacement APIs.

## Confirm Required Behavior

Confirm tests and implementation prove:

```text
snapshot-to-snapshot report serializes deterministically
report round-trips through dictionary-compatible JSON form
required missing Scryfall ID blocks activation
required missing card name blocks activation
duplicate Scryfall ID blocks activation
same oracle ID split across incompatible card identities blocks activation
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
no recommendation language appears in production code
```

## Required Commands

Run from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_scryfall_migration_monitoring -v
python -m unittest discover -s tests
```

Run static scans:

```powershell
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|openai|anthropic|google\.generativeai|langchain" codie\cards\scryfall_migration_monitoring.py tests\test_scryfall_migration_monitoring.py
rg -n "open\(|write_text\(|write_bytes\(|mkdir\(|touch\(|unlink\(" codie\cards\scryfall_migration_monitoring.py
rg -n "snapshot activation|snapshot rollback|card lookup replacement|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" codie\cards\scryfall_migration_monitoring.py tests\test_scryfall_migration_monitoring.py
```

Expected:

```text
No schema/repository/dependency drift.
No forbidden production imports.
No production file-writing behavior.
All focused and full tests pass.
```

## Return Verdict

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

If PASS or PASS WITH REVIEW NOTES, Phase 34A may begin contract-first.

Do not authorize schema/repository persistence, file writing, live network
calls, provider rewrite, lookup replacement, Tagger import implementation, UI,
LLM calls, analytics mutation, or recommendations from this Phase 33C packet.
