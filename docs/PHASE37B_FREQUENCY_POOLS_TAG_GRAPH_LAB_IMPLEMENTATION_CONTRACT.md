# Phase 37B - Frequency Pools / Tag Graph Lab Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase37B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase37C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

The active validation scope file is intentionally not changed by this PR. The
Phase 37B contract declares the next validation tuple, and the active scope may
advance only through the accepted governance flow.

## Purpose

Phase 37B defines the exact allowed implementation shape for future Frequency
Pool packet models and validators.

Phase 37A accepted the Frequency Pools / Tag Graph Lab boundary. Phase 37B
narrows the next implementation packet so Phase 37C can add local,
deterministic, in-memory frequency pool packet models without adding schema,
repositories, provider calls, live network behavior, analytics recalculation,
Tag Graph metric calculation, UI, exports, file writing, LLM calls, simulator
execution, or recommendations.

This phase does not implement Frequency Pool or Tag Graph Lab production code.

## Accepted Dependency

Phase 37B may begin because Phase 37A outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Phase 37A acceptance evidence:

```text
workflow run ID: 29340418728
validated SHA: 1b958d28f1d4840d56b8b1d270fc0760b41bad6a
artifact: codie-phase_ledger-validation-1b958d28f1d4840d56b8b1d270fc0760b41bad6a
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with two INFORMATIONAL findings
aggregate: CLEAN_PASS
final governance verdict: PASS WITH REVIEW NOTES
required corrections: none
```

The adversarial informational findings are nonblocking historical observations
and require no corrective action.

## Authorized Future Implementation Scope

A later accepted Phase 37C implementation packet may add only:

```text
codie/frequency_pools/__init__.py
codie/frequency_pools/models.py
tests/test_frequency_pool_models.py
tests/fixtures/frequency_pools/frequency_pool_commander.json
tests/fixtures/frequency_pools/frequency_pool_partner_pair.json
tests/fixtures/frequency_pools/frequency_pool_user_local.json
tests/fixtures/frequency_pools/frequency_pool_invalid.json
```

No schema, repository, provider, dependency, UI, live-network, file-writing,
analytics, recommendation, simulator-runtime, LLM, charting, or Tag Graph metric
files may be changed in the Phase 37C implementation packet.

## Future Public Interface

Phase 37C may define:

```text
FREQUENCY_POOL_PACKET_VERSION
FrequencyPoolBuildError
FrequencyPoolSubject
FrequencyPoolSourceWindow
FrequencyPoolSourceRef
FrequencyPoolCardIdentity
FrequencyPoolCardRow
FrequencyPoolTagRow
FrequencyPoolCoverageReport
FrequencyPoolCaveat
FrequencyPoolPacket
FrequencyPoolOptions
build_frequency_pool_packet(...)
validate_frequency_pool_packet(...)
frequency_pool_packet_to_dict(...)
```

Do not expose persistence, repository, provider, downloader, analytics
recalculation, recommendation, simulator execution, UI, CLI, LLM, charting, or
file-writing APIs.

## Future Model Responsibilities

Phase 37C may represent:

```text
pool_id
pool_version
pool_type
subject
source_window
source_refs
generated_at
cards
tags
coverage_report
caveats
filters
identity_version
tag_ontology_version
evidence_version
metadata
```

## Future Pool Types

Allowed future pool type values:

```text
commander
partner_pair
top_cut
winner
regional
meta_snapshot
frequency_pool
personal_deck_history
user_local_snapshot
```

User-local pool types must remain visibly labeled as user-local and must not
enter commander averages, global pools, tournament evidence, or recommendation
inputs.

## Future Identity Rules

Phase 37C must preserve:

```text
canonical card identity
scryfall_id when supplied
oracle_id for analytics grouping
card name
commander identity
partner identity when supplied
source deck references by ID only
source event references by ID only
source window filters
tag source provenance
identity_version
tag_ontology_version
evidence_version
```

Frequency Pool packets must never override Scryfall card truth, Tagger ontology
truth, Spellbook interpretation packets, immutable deck snapshots, source deck
records, analytics records, recommendation records, or raw provider/user inputs.

## Future Metric Fields

Phase 37C may serialize already-provided measured values for:

```text
card_count
deck_count
inclusion_rate
average_copies
placement_weighted_usage
trend_delta
confidence
matching_deck_count
available_deck_count
coverage_ratio
```

Phase 37C must not calculate metrics from raw provider payloads, source tables,
or live APIs. If a future packet builder receives numeric metrics, it may
validate and serialize them only.

## Future Tag Frequency Rows

Phase 37C may represent functional tag frequency rows only when supplied from
already accepted tag ontology packets and sanitized measured evidence packets.

Future tag rows may include:

```text
tag
tag_namespace
tag_source
tag_confidence
oracle_ids
raw_tag_count
tag_density
tag_inclusion_rate
average_cards_per_deck_with_tag
matching_deck_count
available_deck_count
coverage_ratio
caveat_ids
```

Tag rows must preserve tag provenance and must not create, infer, or modify
functional tags.

## Future Coverage And Caveat Rules

Phase 37C must keep these values visible when available:

```text
matching_deck_count
available_deck_count
coverage_ratio
low_sample_threshold
low_coverage_threshold
caveats
```

Low sample and low tag coverage conditions must create visible caveats. Missing
coverage data must remain visible as unknown coverage, not as clean coverage.

## Future Privacy Rules

Phase 37C must preserve Phase 36C privacy rules:

```text
raw imported deck text is never accepted
private notes are never accepted
primer body text is never accepted
raw provider payloads are never accepted
blocked private/raw keys are rejected recursively
full-card-list user snapshots remain user-local
user-local metrics are labeled user-local
user-local metrics do not enter commander averages
```

Blocked private/raw keys:

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

## Future Evidence Boundary Rules

Frequency Pool packets are evidence/reporting inputs only.

They must not:

```text
rank cards
score cards for inclusion
recommend cards
recommend cuts
infer pilot intent
generate play/cut/include language
claim a card is optimal
treat simulator output as tournament evidence
treat user-local snapshots as tournament evidence
mutate evidence packets
mutate source records
```

If later Decision Intelligence consumes frequency pool packets, that must be
separately contracted and must preserve the Evidence Fusion / Decision
Intelligence boundary.

## Future Fixture Requirements

Phase 37C tests must use local fixtures only.

Required fixture coverage:

```text
frequency_pool_commander.json
frequency_pool_partner_pair.json
frequency_pool_user_local.json
frequency_pool_invalid.json
```

Fixtures should cover:

```text
commander pool subject
partner-pair pool subject
top-cut or winner source window
user-local snapshot pool labeling
card identity rows
functional tag rows
source refs
coverage report
low-sample caveat
low-coverage caveat
blocked private/raw keys
malformed packet shape
```

No test may depend on live providers, external network access, SQLite, or file
system writes.

## Future Required Tests

Phase 37C should include tests for:

```text
valid commander frequency pool packet builds
valid partner-pair frequency pool packet builds
valid user-local pool packet remains labeled user-local
user-local pool does not enter commander-average fields
card identities preserve scryfall_id and oracle_id when supplied
tag rows preserve source provenance
coverage ratio remains visible
matching deck count remains visible
available deck count remains visible
low sample creates visible caveat
low coverage creates visible caveat
unknown coverage remains visible
deterministic serialization
dictionary-compatible round-trip
input payloads are not mutated
raw imported deck text is rejected recursively
private notes are rejected recursively
raw provider payloads are rejected recursively
primer body text is rejected recursively
malformed fixture failures are clean
no provider imports
no SQLite imports
no analytics recalculation
no recommendation language
no file writing
```

## Future Dependency Rules

Phase 37C may use only:

```text
Python standard library
local dataclasses / typing helpers
already accepted Scryfall identity values as input values
already accepted Scryfall Tagger ontology values as input values
already accepted immutable deck snapshot refs as input refs
already accepted measured evidence refs as input refs
```

Phase 37C must not import:

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

## Forbidden In Phase 37B

Phase 37B must not add:

```text
production frequency pool code
production tag graph code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
SQLite reads or writes
live network calls
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
validator changes
workflow changes
constitution changes
```

## Forbidden In Future Phase 37C Implementation

Phase 37C must not:

```text
calculate frequency pools from source tables
calculate tag graph metrics
read raw provider payloads
read raw imported user deck text
read private notes
read primer body text
persist frequency pools
write frequency pool files
call live providers
call live Scryfall Tagger
call live Moxfield
call LLMs
run simulator logic
generate recommendations
generate play/cut/include language
modify schema
modify repositories
```

## Deferred Later Work

These remain blocked until separate contracts:

```text
Phase 37D - Tag Graph Metric Packet Models and Validators
Phase 37E - Tag Graph Export / Report Contract
Tag Graph UI
Obsidian export
CSV / JSON / Markdown export
Frequency Pool builder over repositories
Moxfield Frequency Pool Builder
recommendation integration
```

## Outside Validation Packet

Phase 37B outside validation should review:

```text
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
docs/CHECKPOINT_PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Next Gate

```text
Phase 37C Frequency Pool Packet Models and Validators: BLOCKED
```

Phase 37C may begin only after Phase 37B outside validation returns PASS or
PASS WITH REVIEW NOTES.
