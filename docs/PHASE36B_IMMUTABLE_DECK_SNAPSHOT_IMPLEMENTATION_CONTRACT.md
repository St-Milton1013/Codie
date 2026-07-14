# Phase 36B - Immutable Deck Snapshot Implementation Contract

Status: implementation contract only

## Purpose

Phase 36B defines the exact allowed implementation shape for the future
immutable deck snapshot expansion.

Phase 36A accepted the snapshot boundary. Phase 36B narrows the future
implementation so a later packet can add local, deterministic immutable deck
snapshot packet models and validators without adding persistence, schema,
repositories, file writing, CLI, UI, provider changes, analytics, simulator
execution, LLM calls, frequency-pool work, or recommendations.

This phase does not implement immutable deck snapshot code.

## Accepted Dependency

Phase 36B may begin because Phase 36A outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review note carried forward:

```text
Phase 36B should make redaction behavior concrete: default redacted packet,
explicit full-card-list option, visible privacy caveat, and hard rejection of
raw imported text/private notes by default.

GitHub CI was not available for the Phase 36A validation result.
```

## Authorized Future Implementation Scope

A later accepted implementation packet may add only:

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
Tag Graph Lab metric files may be changed in the implementation packet.

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
recommendation, simulator execution, UI, LLM, CLI, or file-writing APIs.

## Future Model Responsibilities

The future implementation may represent:

```text
snapshot_id
snapshot_version
snapshot_scope
deck_hash
commander_signature
commander_names
partner_names
source_refs
user_deck_ref
analysis_refs
analysis_profile_refs
created_at
cards
redaction_policy
privacy_metadata
replay_metadata
validation_warnings
manual_review_items
```

## Future Redaction Rules

The default future snapshot must be redacted.

Default redacted snapshot behavior:

```text
card entries omitted by default
raw imported deck text rejected
private notes rejected
raw provider payload rejected
primer body text rejected
full card list not serialized
visible privacy caveat required
redaction_policy = redacted
```

Full-card-list behavior:

```text
requires explicit ImmutableDeckSnapshotOptions(include_card_entries=True)
sets redaction_policy = full_card_list
includes visible privacy caveat
still rejects raw imported deck text
still rejects private notes
still rejects raw provider payloads
still rejects primer body text
does not become tournament evidence
does not enter commander averages
does not enter global frequency pools
```

Any future option that tries to include raw imported deck text, private notes,
raw provider payloads, or primer body text must fail validation.

## Future Privacy Blocked Keys

Future implementation must reject these keys recursively in input metadata,
privacy metadata, replay metadata, warnings, manual-review items, and source
refs:

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

These blocked strings may appear in implementation only as blocked-key
constants, validation errors, tests, and documentation.

## Future Identity Rules

Future implementation must preserve:

```text
snapshot_id
snapshot_version
snapshot_scope
deck_hash
commander_signature
commander names
partner names
source deck reference
user deck reference when supplied
analysis session reference when supplied
analysis profile refs when supplied
created_at
card name when card entries are explicitly included
scryfall_id when supplied
oracle_id when supplied
zone when card entries are explicitly included
quantity when card entries are explicitly included
source order when card entries are explicitly included
source provenance by reference
```

The snapshot layer must never override Scryfall card truth, canonical deck
contents, source deck records, user deck records, analysis session records,
analytics records, recommendation records, or raw provider/user inputs.

## Future Evidence Boundary Rules

Future immutable deck snapshots are local replay/input packets.

They must not:

```text
be treated as tournament evidence
enter commander averages
enter global frequency pools
alter canonical tables
alter analytics tables
alter recommendation tables
create recommendations
infer pilot intent
generate play/cut/include language
```

If a future user-scoped frequency-pool or tag graph feature consumes snapshots,
that must be separately contracted and must label the scope as user-local.

## Future Replay Rules

Future replay metadata may include:

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

Replay metadata must serialize visibly and deterministically.

Old snapshots must remain distinguishable by `snapshot_version`; a future
snapshot format change must not silently reinterpret older snapshot packets.

## Future Fixture Requirements

Future implementation tests must use local fixtures only.

Required fixture coverage:

```text
user_deck_snapshot_full.json
user_deck_snapshot_redacted.json
user_deck_snapshot_invalid.json
```

Fixtures should cover:

```text
redacted snapshot without cards
full-card-list snapshot with visible privacy caveat
commander signature
deck hash
source refs
analysis refs
analysis profile refs
replay metadata
card quantities
card zones
card source order
blocked private/raw keys
malformed snapshot shape
```

No test may depend on live providers, external network access, SQLite, or file
system writes.

## Future Required Tests

A later implementation should include tests for:

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

## Forbidden In Phase 36B

Phase 36B must not add:

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
include raw imported deck text
include private notes
include raw provider payloads
include primer body text
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

Phase 36B outside validation should review:

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

## Next Gate

```text
Phase 36C Immutable Deck Snapshot Implementation: BLOCKED
```

Phase 36C may begin only after Phase 36B outside validation returns PASS or
PASS WITH REVIEW NOTES.
