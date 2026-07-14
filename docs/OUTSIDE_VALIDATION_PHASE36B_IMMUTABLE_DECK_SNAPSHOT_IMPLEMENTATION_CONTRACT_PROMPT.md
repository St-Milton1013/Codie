# Outside Validation Prompt - Phase 36B Immutable Deck Snapshot Implementation Contract

Validate Codie Phase 36B against:

```text
docs/PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
```

## Required Review Files

Review:

```text
docs/PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/user_decks/importer.py
codie/user_decks/deck_memory.py
codie/user_decks/analysis_input.py
codie/user_decks/__init__.py
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

## Confirm Implementation-Contract-Only Scope

Confirm Phase 36B adds only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 36B adds:

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

Confirm the contract limits future implementation to:

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
execution, UI, LLM calls, CLI behavior, or file writing.

## Confirm Redaction Requirements

Confirm the contract requires future implementation to:

```text
build redacted snapshots by default
omit card entries by default
require explicit include_card_entries=True for full card lists
emit visible privacy caveat for full card lists
set redaction_policy visibly
reject raw imported deck text recursively
reject private notes recursively
reject raw provider payloads recursively
reject primer body text recursively
```

Confirm blocked private/raw keys include:

```text
raw_input
original_import_text
private_deck_text
private_notes
private_user_notes
full_primer_body
primer_body
raw_provider_payload
provider_payload
```

## Confirm Snapshot Boundary

Confirm future snapshots:

```text
do not become tournament evidence
do not enter commander averages
do not enter global frequency pools
do not alter canonical tables
do not alter analytics tables
do not alter recommendation tables
do not create recommendations
do not infer pilot intent
do not generate play/cut/include language
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
rg -n "immutable_snapshots|production snapshot code|schema changes|repository changes|file writing|analytics calculation|frequency pool calculation|simulator execution|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT.md
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
