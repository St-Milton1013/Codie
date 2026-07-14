# Checkpoint - Phase 36C Immutable Deck Snapshot Implementation

Status: INTERNAL PASS

This checkpoint is internal evidence only. It is not outside validation.

## Scope

Phase 36C implements the local immutable user deck snapshot packet models and
validators authorized by Phase 36B.

It remains:

```text
pure
in-memory
fixture-first
deterministic
privacy-redacted by default
repository-free
schema-free
provider-free
file-write-free
analytics-free
simulator-execution-free
LLM-free
UI-free
recommendation-free
```

## Behavior Verified

```text
valid redacted immutable snapshot builds by default
valid full-card-list snapshot requires explicit option
full-card-list snapshot includes visible privacy caveat
snapshot ID and version remain visible
deck hash remains visible
commander signature remains visible
card entries are omitted by default
card entries preserve quantities and zones when explicitly included
card entries preserve source order when explicitly included
source refs remain visible
analysis refs remain visible when supplied
analysis profile refs remain visible when supplied
privacy policy remains visible
replay metadata remains visible
raw imported text is rejected recursively
private notes are rejected recursively
raw provider payloads are rejected recursively
primer body text is rejected recursively
recursive blocked-key scans cover source refs, analysis refs, replay metadata, warnings, manual-review items, privacy metadata, and arbitrary nested metadata
deterministic serialization
dictionary-compatible JSON round-trip
input payloads are not mutated
malformed snapshot failures are clean
user snapshots do not become tournament evidence
no schema/repository/provider changes
no analytics or recommendation generation
```

## Validation

System `python` is not available on PATH.

The configured Windows venv exists but cannot launch because it points at a
missing Python install:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe
Unable to create process using '"C:\Users\Main\AppData\Local\Programs\Python\Python312\python.exe" ...'
```

Bundled runtime validation:

```text
C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.test_user_deck_immutable_snapshots -v
Ran 11 tests
OK

C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/check_schema.py
Schema bootstrap check passed.

C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest discover -s tests -v
Ran 927 tests
OK (skipped=1)

git diff --check
passed
```

## Static Scans

```text
rg -n "codie\.db|sqlite3|codie\.providers|codie\.ingestion|codie\.analytics|codie\.recommendations|codie\.evidence_fusion|codie\.decision_intelligence|requests|httpx|openai|anthropic|google\.generativeai|langchain|flask|fastapi|uvicorn|starlette" codie\user_decks\immutable_snapshots.py tests\test_user_deck_immutable_snapshots.py

Expected:
no production matches
test matches only forbidden-import assertion strings
```

```text
git diff --name-only -- codie\db codie\providers codie\analytics codie\recommendations codie\probability_engine codie\cards docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt .github

Expected:
no matches
```

```text
rg -n "should play|must include|strict upgrade|auto-include|recommended cut|recommended include|tournament evidence|commander averages|global frequency pools" codie\user_decks\immutable_snapshots.py tests\test_user_deck_immutable_snapshots.py tests\fixtures\user_deck_snapshots

Expected:
production matches only evidence-boundary text
test matches only boundary assertions
```

## Outside Validation Packet

Send:

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

## Next Gate

```text
Phase 36C outside validation: REQUIRED
```

Do not start any later phase until Phase 36C outside validation returns PASS or
PASS WITH REVIEW NOTES.
