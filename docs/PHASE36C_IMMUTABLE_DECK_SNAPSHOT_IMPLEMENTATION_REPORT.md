# Phase 36C - Immutable Deck Snapshot Implementation Report

Status: internal pass, awaiting outside validation

## Purpose

Phase 36C implements the local immutable user deck snapshot packet models and
validators authorized by Phase 36B.

The implementation is pure, in-memory, deterministic, fixture-first, and
privacy-redacted by default. It does not persist snapshots, write files, read
SQLite, import repositories, call providers, calculate analytics, run simulator
logic, call LLMs, build frequency pools, update Tag Graph Lab metrics, add UI,
or generate recommendations.

## Files Added

```text
codie/user_decks/immutable_snapshots.py
tests/test_user_deck_immutable_snapshots.py
tests/fixtures/user_deck_snapshots/user_deck_snapshot_full.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_redacted.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_invalid.json
docs/PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_PROMPT.md
```

## Files Modified

```text
codie/user_decks/__init__.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Interface

```text
IMMUTABLE_DECK_SNAPSHOT_VERSION
ImmutableDeckSnapshotError
DeckSnapshotCard
DeckSnapshotSourceRef
DeckSnapshotAnalysisRef
DeckSnapshotPrivacyPolicy
DeckSnapshotReplayMetadata
DeckSnapshotWarning
ImmutableDeckSnapshot
ImmutableDeckSnapshotOptions
build_immutable_deck_snapshot(...)
validate_immutable_deck_snapshot(...)
immutable_deck_snapshot_to_dict(...)
```

## Behavior Implemented

```text
valid redacted immutable snapshot builds by default
redacted snapshots omit card entries by default
redacted snapshots expose a visible privacy caveat
full-card-list snapshots require explicit ImmutableDeckSnapshotOptions(include_card_entries=True)
full-card-list snapshots set redaction_policy = full_card_list
full-card-list snapshots expose a visible privacy caveat
card entries preserve name, quantity, zone, source_order, scryfall_id, and oracle_id
snapshot ID, version, scope, deck hash, commander signature, and created_at remain visible
commander names and partner names remain visible
source refs remain visible
analysis refs remain visible
analysis profile refs remain visible
privacy policy remains visible
replay metadata remains visible
validation warnings remain visible
manual-review items remain visible
serialization is deterministic
dictionary-compatible serialization round-trip works through JSON
input payloads are not mutated
malformed snapshot failures are clean
```

## Privacy Guardrails

Phase 36C rejects these blocked private/raw keys recursively:

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

The recursive blocked-key coverage explicitly includes:

```text
source refs
analysis refs
replay metadata
validation warnings
manual-review items
privacy metadata
arbitrary nested input metadata
```

## Boundary Preserved

Phase 36C does not add:

```text
schema changes
repository changes
provider changes
SQLite reads or writes
file writing behavior
CLI work
UI work
analytics calculation
frequency pool calculation
Tag Graph Lab metrics
simulator execution
LLM calls
recommendation generation
dependency changes
```

User deck snapshots remain user-local replay/input packets. They are not
tournament evidence, do not enter commander averages, do not enter global
frequency pools, and do not alter canonical, analytics, recommendation, source,
provider, user deck, or analysis session records.

## Validation

System `python` is not available on PATH in this environment.

The configured Windows venv exists but cannot launch:

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

## Next Gate

```text
Phase 36C outside validation
```

No later phase should begin until Phase 36C outside validation returns PASS or
PASS WITH REVIEW NOTES.
