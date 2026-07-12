# Outside Validation Prompt - Phase 33B Scryfall Migration Monitoring Implementation Contract

Validate Codie Phase 33B against:

```text
docs/PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CODIE_V1_CONSTITUTION.md
```

## Required Review Files

Review:

```text
docs/PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Implementation-Contract-Only Scope

Confirm Phase 33B adds only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 33B adds:

```text
production migration-monitoring code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
dependency changes
file-writing behavior
live network behavior
UI behavior
LLM behavior
recommendation behavior
```

## Confirm Future Implementation Surface

Confirm the contract limits future implementation to:

```text
codie/cards/scryfall_migration_monitoring.py
tests/test_scryfall_migration_monitoring.py
tests/fixtures/scryfall/migration_previous_snapshot.json
tests/fixtures/scryfall/migration_next_snapshot.json
tests/fixtures/scryfall/migration_unknown_fields_snapshot.json
tests/fixtures/scryfall/migration_unknown_enums_snapshot.json
tests/fixtures/scryfall/migration_breaking_snapshot.json
optional codie/cards/__init__.py exports only
```

## Confirm Public Interface

Confirm future public interface is limited to model/validation functions such as:

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

Reject if the contract authorizes persistence, activation, rollback,
downloader, repository, provider, or lookup-replacement APIs.

## Confirm Boundary Language

Confirm Phase 33B does not authorize:

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

## Required Commands

Run from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests
```

Run static scans:

```powershell
git diff --name-only HEAD~1..HEAD -- codie tests codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|analytics|recommendations|decision|evidence|openai|anthropic|google\.generativeai|langchain" docs\PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
rg -n "migration monitoring implementation|snapshot diff implementation|live Scryfall API|bulk download implementation|file writing|snapshot activation|snapshot rollback|card lookup replacement|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
```

Expected:

```text
No production/test/schema/repository/dependency drift.
Forbidden strings appear only in explicit forbidden-scope lists.
All tests pass.
```

## Return Verdict

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

If PASS or PASS WITH REVIEW NOTES, Phase 33C may begin implementation.

Do not authorize schema/repository persistence, file writing, live network
calls, provider rewrite, lookup replacement, Tagger import, UI, LLM calls,
analytics mutation, or recommendations from this Phase 33B packet.
