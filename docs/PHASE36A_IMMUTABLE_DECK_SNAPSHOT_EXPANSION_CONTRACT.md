# Phase 36A - Immutable Deck Snapshot Expansion Contract

Status: contract only

## Purpose

Phase 36A defines the future immutable deck snapshot expansion boundary for
Codie.

Existing user deck import and deck memory flows preserve local user decks and
analysis sessions. The next deferred priority is a reusable immutable snapshot
packet layer that can support deck memory, user deck analysis, comparisons,
simulator challenges, local reports, future exports, and replayable evidence
without letting user decks enter commander averages or global evidence.

This phase does not implement snapshot code, schema, repositories, migrations,
file writing, CLI, UI, provider changes, analytics, simulator execution, LLM
calls, or recommendations.

## Accepted Dependency

Phase 36A may begin because Phase 35C outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review notes carried forward:

```text
win_enabling=True for infinite_mana/infinite_draw/win_condition must remain
documented as win-enabling metadata, not a claim that those outputs always win.

Future Spellbook interpreter expansion should add edge fixtures for mixed
outputs, multiple unknown requirements, optional target compatibility, and
component-role ambiguity.

GitHub CI was not available for the Phase 35C validation result.
```

## Future Scope To Define

A future accepted implementation packet may add local, deterministic immutable
deck snapshot packet models and validators covering:

```text
snapshot_id
snapshot_version
deck_hash
commander_signature
commander_names
partner_names
source_deck_ref
user_deck_ref
analysis_session_ref
analysis_profile_refs
created_at
card entries
zone preservation
quantity preservation
source ordering
redaction policy
privacy metadata
replay metadata
source provenance
validation warnings
manual-review items
deterministic serialization
dictionary round-trip
```

## Future Authorized Implementation Surface

A later accepted implementation contract may authorize only:

```text
codie/user_decks/immutable_snapshots.py
tests/test_user_deck_immutable_snapshots.py
tests/fixtures/user_deck_snapshots/user_deck_snapshot_full.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_redacted.json
tests/fixtures/user_deck_snapshots/user_deck_snapshot_invalid.json
```

The future implementation may update:

```text
codie/user_decks/__init__.py
```

only to export public immutable snapshot model symbols.

No schema, repository, provider, dependency, UI, live-network, file-writing,
analytics, recommendation, simulator-runtime, LLM, frequency-pool, charting, or
Tag Graph Lab metric files may be changed unless a later contract explicitly
authorizes that work.

## Future Public Interface

The future implementation may define:

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

Do not expose persistence, repository, provider, downloader, analytics,
recommendation, simulator execution, UI, LLM, or file-writing APIs.

## Future Identity Rules

Future implementation must preserve:

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
card name
scryfall_id when supplied
oracle_id when supplied
zone
quantity
source order
source provenance by reference
```

The snapshot layer must not override Scryfall card truth, canonical deck
contents, source deck records, user deck records, analysis session records,
analytics records, recommendation records, or raw provider/user inputs.

## Future Privacy And Redaction Rules

Future snapshots may represent local user decks, so privacy behavior must be
explicit.

Future implementation must support:

```text
redaction policy field
private notes exclusion by default
raw imported deck text exclusion by default
primer/body text exclusion
optional card-list inclusion only through explicit option
visible redaction caveats
privacy metadata
```

Future implementation must not store or expose by default:

```text
raw_input
original_import_text
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
private user notes
```

If a future option includes full card lists for local replay, the output must
label that inclusion explicitly and must not treat the snapshot as global
evidence.

## Future Evidence Boundary Rules

Immutable deck snapshots may support replay and local user workflows. They must
not become tournament evidence.

Future implementation must preserve:

```text
user decks never enter commander averages
user decks never enter frequency pools unless explicitly user-scoped
user snapshots do not alter canonical tables
user snapshots do not alter analytics tables
user snapshots do not create recommendations
snapshot packets are inputs to future analysis, not conclusions
```

## Future Replay Rules

Future replay metadata should include:

```text
analysis_profile_id
analysis_profile_version
weight_profile_id
weight_profile_version
evidence_version
decision_version
source_snapshot_ids
generated_by_phase
```

Old snapshots must remain reproducible by versioned metadata. A future snapshot
format change must not silently reinterpret older snapshot packets.

## Future Required Tests

A later implementation should include tests for:

```text
valid immutable snapshot builds
snapshot ID and version remain visible
deck hash remains visible
commander signature remains visible
card entries preserve quantities and zones
card entries preserve source order
source refs remain visible
analysis refs remain visible when supplied
privacy policy remains visible
raw imported text is rejected
private notes are rejected by default
redacted snapshot omits card list by option
explicit full snapshot includes visible privacy caveat
deterministic serialization
dictionary-compatible round-trip
input payloads are not mutated
malformed snapshot failures are clean
user snapshots do not become tournament evidence
no schema/repository/provider changes
no analytics or recommendation generation
```

## Future Dependency Rules

Future implementation may use only:

```text
Python standard library
local dataclasses / typing helpers
already accepted user deck import/listing values as input values
already accepted analysis profile/weight profile reference values as input values
```

Future implementation must not import:

```text
codie.db
codie.db.repositories
sqlite3
codie.providers
codie.ingestion
codie.analytics
codie.recommendations
codie.evidence_fusion
codie.decision_intelligence
requests
httpx
openai
anthropic
google.generativeai
langchain
flask
fastapi
uvicorn
starlette
```

## Forbidden In Phase 36A

Phase 36A must not add:

```text
production snapshot code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
SQLite reads or writes
file writing
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

## Forbidden In Future Implementation

Future implementation must not:

```text
persist snapshots
write snapshot files
read SQLite
change user_decks schema
change analysis_sessions schema
include raw imported deck text by default
include private notes by default
treat user deck snapshots as tournament evidence
insert user deck snapshots into commander averages
insert user deck snapshots into global frequency pools
generate recommendations
infer pilot intent
call live providers
call LLMs
generate play/cut/include language
```

## Outside Validation Packet

Phase 36A outside validation should review:

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

## Next Gate

```text
Phase 36B Immutable Deck Snapshot Implementation Contract: BLOCKED
```

Phase 36B may begin only after Phase 36A outside validation returns PASS or
PASS WITH REVIEW NOTES.
