# Outside Validation Prompt - Phase 36C Immutable Deck Snapshot Implementation

Validate Codie Phase 36C against `docs/CODIE_V1_CONSTITUTION.md`, the Phase
36A/36B contracts, and the implementation checkpoint.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

## Review Files

```text
docs/PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_PROMPT.md
docs/PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
codie/user_decks/immutable_snapshots.py
codie/user_decks/__init__.py
tests/test_user_deck_immutable_snapshots.py
tests/fixtures/user_deck_snapshots/user_deck_snapshot_full.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_redacted.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_invalid.json
codie/user_decks/importer.py
codie/user_decks/deck_memory.py
codie/user_decks/analysis_input.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm Phase 36C:

```text
implements only local immutable user deck snapshot models and validators
uses local fixtures only
defaults to redacted snapshots
omits card entries by default
requires explicit option for full-card-list snapshots
sets redaction_policy = full_card_list only for explicit full-card-list snapshots
preserves visible privacy caveats
preserves snapshot ID, snapshot version, scope, deck hash, commander signature, commander names, partner names, and created_at
preserves card names, quantities, zones, source order, scryfall_id, and oracle_id when card entries are explicitly included
preserves source refs
preserves analysis refs
preserves analysis profile refs
preserves replay metadata
preserves validation warnings
preserves manual-review items
serializes deterministically
round-trips through JSON-compatible dictionary form
does not mutate input payloads
fails cleanly for malformed snapshots
```

Confirm privacy behavior:

```text
raw imported text is rejected recursively
private notes are rejected recursively
raw provider payloads are rejected recursively
primer body text is rejected recursively
blocked-key rejection covers source refs, analysis refs, replay metadata, validation warnings, manual-review items, privacy metadata, and arbitrary nested metadata
```

Confirm Phase 36C does not:

```text
persist snapshots
write snapshot files
read SQLite
change user_decks schema
change analysis_sessions schema
import repositories
import providers
call live providers
call LLMs
run simulator logic
calculate analytics
calculate frequency pools
add Tag Graph Lab metrics
add UI behavior
generate recommendations
infer pilot intent
treat user deck snapshots as tournament evidence
insert user deck snapshots into commander averages
insert user deck snapshots into global frequency pools
generate play/cut/include language
```

## Commands To Run From Clean Checkout

Use an available project Python. If using the configured Windows venv, run:

```powershell
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_user_deck_immutable_snapshots -v
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
git diff --check
```

If the configured venv cannot launch, report that environment blocker and rerun
with a clearly identified alternative Python runtime.

## Static Scans

```powershell
rg -n "codie\.db|sqlite3|codie\.providers|codie\.ingestion|codie\.analytics|codie\.recommendations|codie\.evidence_fusion|codie\.decision_intelligence|requests|httpx|openai|anthropic|google\.generativeai|langchain|flask|fastapi|uvicorn|starlette" codie\user_decks\immutable_snapshots.py tests\test_user_deck_immutable_snapshots.py
```

Expected:

```text
no production matches
test matches only forbidden-import assertion strings
```

```powershell
git diff --name-only -- codie\db codie\providers codie\analytics codie\recommendations codie\probability_engine codie\cards docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt .github
```

Expected:

```text
no matches
```

```powershell
rg -n "should play|must include|strict upgrade|auto-include|recommended cut|recommended include" codie\user_decks\immutable_snapshots.py tests\test_user_deck_immutable_snapshots.py tests\fixtures\user_deck_snapshots
```

Expected:

```text
no production recommendation-language matches
```

## Reject If

Reject if Phase 36C persists snapshots, writes files, reads SQLite, imports
repositories or providers, changes schema, calls live providers, calls LLMs,
runs simulator logic, calculates analytics/frequency pools, adds UI behavior,
generates recommendations, includes raw/private deck text, includes raw provider
payloads, includes primer body text, treats user deck snapshots as tournament
evidence, or includes full card lists without explicit option and visible
privacy caveat.

## Final Gate

No later phase may begin until Phase 36C outside validation returns PASS or PASS
WITH REVIEW NOTES.
