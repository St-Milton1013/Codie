# Outside Validation Prompt - Phase 33A Scryfall Migration Monitoring Contract

Validate Codie Phase 33A against:

```text
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
```

## Required Review Files

Review:

```text
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_PROMPT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Contract-Only Scope

Confirm Phase 33A adds only:

```text
contract document
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 33A adds:

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

## Confirm Contract Coverage

Confirm the contract defines future requirements for:

```text
required vs optional fields
unknown-field handling
unknown enum handling
schema-breaking conditions
migration report/ledger fields
snapshot activation blocking rules
affected consumer reporting
manual review queue inputs
fixture requirements
validation and rollback behavior
```

## Confirm Identity Rules

Confirm Phase 33A preserves:

```text
scryfall_id remains enforced card identity
oracle_id remains analytics grouping identity
raw Scryfall JSON remains preserved
Scryfall remains the card truth source
```

Reject if the contract authorizes changing card identity semantics, replacing
lookup behavior, mutating old snapshots, or silently activating new snapshots.

## Confirm Future Blocking Rules

Confirm the contract requires future activation-blocking conditions for:

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

## Confirm Boundary Language

Confirm Phase 33A does not authorize:

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
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|analytics|recommendations|decision|evidence|openai|anthropic|google\.generativeai|langchain" docs\PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
rg -n "migration monitoring implementation|snapshot diff implementation|live Scryfall API|bulk download implementation|file writing|snapshot activation|snapshot rollback|card lookup replacement|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
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

If PASS or PASS WITH REVIEW NOTES, Phase 33B may begin contract-first.

Do not authorize migration-monitoring implementation, schema/repository
persistence, file writing, live network calls, provider rewrite, lookup
replacement, Tagger import, UI, LLM calls, analytics mutation, or
recommendations from this Phase 33A packet.
