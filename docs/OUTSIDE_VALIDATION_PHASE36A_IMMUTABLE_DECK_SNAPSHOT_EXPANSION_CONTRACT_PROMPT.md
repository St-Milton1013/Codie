# Outside Validation Prompt - Phase 36A Immutable Deck Snapshot Expansion Contract

Validate Codie Phase 36A against:

```text
docs/PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
```

## Required Review Files

Review:

```text
docs/PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_PROMPT.md
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/user_decks/importer.py
codie/user_decks/deck_memory.py
codie/user_decks/analysis_input.py
codie/db/schema/user.sql
codie/db/repositories/user.py
tests/test_user_deck_import.py
tests/test_user_deck_memory.py
tests/test_user_deck_analysis_input.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Contract-Only Scope

Confirm Phase 36A adds only:

```text
contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 36A adds:

```text
production snapshot code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
dependency changes
file-writing behavior
CLI behavior
UI behavior
live network behavior
simulator execution
analytics behavior
recommendation behavior
LLM behavior
```

## Confirm Future Implementation Surface

Confirm the contract limits future implementation to local, fixture-first
immutable deck snapshot packet models such as:

```text
codie/user_decks/immutable_snapshots.py
tests/test_user_deck_immutable_snapshots.py
tests/fixtures/user_deck_snapshots/user_deck_snapshot_full.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_redacted.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_invalid.json
optional codie/user_decks/__init__.py exports only
```

Reject if the contract authorizes persistence, repository writes, schema
changes, provider reads, analytics writes, recommendation output, simulator
execution, UI, LLM calls, or file writing.

## Confirm Snapshot Rules

Confirm the contract requires future implementation to preserve:

```text
snapshot_id
snapshot_version
deck_hash
commander_signature
commander names
partner names
source deck reference
user deck reference when supplied
analysis session reference when supplied
analysis profile refs when supplied
created_at
card names
scryfall_id when supplied
oracle_id when supplied
zone
quantity
source order
source provenance by reference
privacy/redaction policy
replay metadata
```

Confirm user deck snapshots:

```text
do not become tournament evidence
do not enter commander averages
do not enter global frequency pools
do not alter canonical tables
do not alter analytics tables
do not create recommendations
```

## Confirm Privacy Rules

Confirm future implementation must reject or omit by default:

```text
raw_input
original_import_text
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
private user notes
```

Confirm full card-list inclusion, if implemented later, must require explicit
option and visible privacy caveat.

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
rg -n "immutable_snapshots|production snapshot code|schema changes|repository changes|file writing|analytics calculation|frequency pool calculation|simulator execution|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
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
