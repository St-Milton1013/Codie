# Phase 37B - Frequency Pools / Tag Graph Lab Implementation Contract

Status: implementation contract only

## Explicit Phase 37B Validation Tuple

```text
phase_id: Phase37B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
```

## Explicit Next-Phase Validation Tuple

```text
next_phase_id: Phase37C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

The active validation scope file is intentionally unchanged by this PR. This
contract declares the tuple required by the streamlined workflow; scope
advancement remains governed by accepted validation results.

## Purpose

Phase 37B converts the accepted Phase 37A Frequency Pools / Tag Graph Lab
boundary into a narrower implementation contract for the next packet.

The authorized Phase 37B deliverable is this implementation-contract packet and
the matching governance records. The packet defines the later model/validator
surface without adding `codie/`, `tests/`, fixture, schema, provider, UI,
workflow, validator, or constitution changes.

## Accepted Phase 37A Dependency Evidence

Phase 37A outside validation returned PASS WITH REVIEW NOTES.

Evidence:

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

The informational findings are nonblocking historical observations and require
no corrective action.

## Phase 37B PR Scope

This PR may contain only:

```text
Phase 37B implementation contract
Phase 37B checkpoint report
Phase 37B outside validation prompt
roadmap/status/handoff updates
```

Any runtime, schema, provider, validator, workflow, dependency, UI, export,
simulation, analytics, recommendation, or constitution change is outside this
PR.

## Implementation-Contract Packet Responsibilities

The Phase 37B implementation-contract packet is a governance packet, not a
runtime packet. Its responsibilities are:

```text
record Phase 37A acceptance evidence
declare the Phase 37B validation tuple
declare the next-phase validation tuple
define the exact future Frequency Pool model files
define the exact future Frequency Pool public interface
define future packet fields and allowed pool types
define identity, provenance, coverage, privacy, and evidence boundaries
define local fixture inventory and fixture coverage
define required tests for the later model packet
define dependency and input limits for the later model packet
define deferred work that remains outside the later model packet
define the outside-validation packet for Phase 37B
update roadmap, status, next-phase, and handoff governance records
```

The packet does not build Frequency Pool data, calculate metrics, read sources,
write files, or prepare Tag Graph visualizations. It only constrains what a
future accepted implementation packet may add.

## Authorized Future Implementation Files

After this contract is accepted, the next packet may define local, in-memory
Frequency Pool packet models and validators.

Allowed implementation files for that later packet:

```text
codie/frequency_pools/__init__.py
codie/frequency_pools/models.py
tests/test_frequency_pool_models.py
tests/fixtures/frequency_pools/frequency_pool_commander.json
tests/fixtures/frequency_pools/frequency_pool_partner_pair.json
tests/fixtures/frequency_pools/frequency_pool_user_local.json
tests/fixtures/frequency_pools/frequency_pool_invalid.json
```

The later packet remains model/validator-only. It may validate and serialize
already supplied sanitized evidence values; it may not gather data or calculate
pools from raw sources.

## Future Public Interface

The later packet may define:

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

## Future Packet Responsibilities

Future Frequency Pool packets may represent:

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

Allowed pool type values:

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

User-local pool types must be visibly labeled and isolated from commander
averages, global pools, tournament evidence, and recommendation inputs.

## Identity And Provenance

Future packets must preserve:

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

Frequency Pool packets are downstream evidence packets. They must not override
Scryfall truth, Tagger ontology truth, Spellbook interpretation packets,
immutable deck snapshots, source records, analytics records, recommendation
records, or raw provider/user inputs.

## Metric Serialization

The future packet builder may serialize already supplied measured values for:

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

The builder validates and serializes values; it does not derive them from raw
provider payloads, source tables, or live APIs.

## Tag Rows

Future tag rows may be accepted only from already accepted tag ontology packets
and sanitized measured evidence packets.

Tag row fields may include:

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

Tag rows preserve provenance and do not create, infer, or modify tags.

## Coverage And Caveats

Future packets must keep these values visible when available:

```text
matching_deck_count
available_deck_count
coverage_ratio
low_sample_threshold
low_coverage_threshold
caveats
```

Low sample and low coverage states must create visible caveats. When coverage
values are not available, the packet must still serialize explicit unknown
coverage markers for each unavailable value instead of omitting the coverage
field. The unknown marker applies independently to:

```text
matching_deck_count
available_deck_count
coverage_ratio
low_sample_threshold
low_coverage_threshold
caveats
```

## Privacy Boundary

Future packets must preserve the Phase 36C privacy boundary and must reject
private import text, private user notes, full primer bodies, and raw provider
payload metadata recursively. The later implementation should reuse the
accepted Phase 36C blocked-key policy rather than redefining or expanding the
private/raw metadata vocabulary in this packet.

## Evidence Boundary

Frequency Pool packets are evidence/reporting inputs only. They are not
recommendation outputs and do not express play, cut, include, optimality, or
pilot-intent claims.

Boundary enforcement for the later model packet:

```text
packet builders accept already-supplied sanitized values only
packet builders reject recommendation-language fields
packet builders reject ranking/scoring/include/cut metadata
packet builders preserve source_ref_ids and caveat_ids visibly
packet builders label user-local pool types visibly
packet validators reject private/raw metadata recursively
packet serializers expose metrics as evidence values only
dependency scans reject provider, database, analytics, recommendation, LLM, UI, and file-writing imports
```

If later Decision Intelligence consumes Frequency Pool packets, that connection
requires a separate accepted contract. That contract must treat the packets as
supporting evidence inputs, cite their packet IDs and source refs, preserve
their caveats, and keep recommendation reasoning inside Decision Intelligence.

## Future Fixture Requirements

Future tests must use local fixtures only:

```text
tests/fixtures/frequency_pools/frequency_pool_commander.json
tests/fixtures/frequency_pools/frequency_pool_partner_pair.json
tests/fixtures/frequency_pools/frequency_pool_user_local.json
tests/fixtures/frequency_pools/frequency_pool_invalid.json
```

Required fixture coverage:

```text
commander pool subject
partner-pair pool subject
user-local pool labeling
card identity rows
functional tag rows
source refs
coverage report values
low-sample caveat
low-coverage caveat
blocked private/raw keys
malformed packet shape
```

## Complete Future Required Tests

The later model packet should test:

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
private imported deck text is rejected recursively
private notes are rejected recursively
provider payload metadata is rejected recursively
primer body text is rejected recursively
malformed packet fixtures produce clean validation errors
provider import scan has no production matches
SQLite import scan has no production matches
analytics recalculation scan has no production matches
recommendation-language scan has no production matches
file-writing scan has no production matches
```

## Future Package Dependencies And Input Limits

Allowed implementation package dependencies:

```text
Python standard library
local dataclasses or equivalent immutable value helpers
typing helpers
```

Allowed input value categories:

```text
already accepted Scryfall identity values as input values
already accepted Scryfall Tagger ontology values as input values
already accepted immutable deck snapshot refs as input refs
already accepted measured evidence refs as input refs
already accepted caveat refs as input refs
already accepted source refs as input refs
```

Input value categories are not package dependencies and do not authorize imports
from their producing subsystems. The later implementation must remain
independent from database, provider, ingestion, analytics, recommendation,
Decision Intelligence, Evidence Fusion, HTTP, LLM, server, UI, and file-writing
dependencies.

## Complete Deferred Later Work

The following work is excluded from Phase 37B and excluded from the immediate
Phase 37C model/validator packet unless a later accepted contract explicitly
authorizes it:

```text
Tag Graph metric packet models
Tag Graph export and report surfaces
Tag Graph UI
Obsidian export
CSV / JSON / Markdown export
repository-backed Frequency Pool builders
Moxfield Frequency Pool Builder
recommendation integration
```

Validators must not require any deferred item above as a correction for Phase
37B. Requiring production implementation, Tag Graph metric packet models,
repository-backed builders, exports, UI, or recommendation integration would
contradict this implementation-contract packet.

## Phase 37B Outside Validation Packet

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

Outside validation requirements:

```text
confirm Phase 37B is implementation-contract-only
confirm Phase 37A acceptance evidence is recorded
confirm the Phase 37B validation tuple is explicit
confirm the next-phase validation tuple is explicit
confirm authorized future implementation files are complete
confirm future public interface is complete
confirm future packet responsibilities are complete
confirm future package dependencies and input limits are explicit
confirm coverage values and unknown coverage markers remain visible
confirm privacy, evidence, and recommendation boundaries remain intact
confirm fixture inventory and required tests are complete
confirm deferred later work remains deferred
confirm roadmap/status/handoff docs agree on the current gate
```

Outside validation constraints:

```text
do not treat Phase 37B as production implementation
do not require codie/ implementation files in this PR
do not require tests or fixtures in this PR
do not require active validation scope advancement in this PR
do not treat user-local pools as commander averages or tournament evidence
do not allow provider, database, analytics, recommendation, UI, LLM, or file-writing scope
do not allow Phase 37C implementation before Phase 37B acceptance
```

Expected outside validation outcomes:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 37C contract-first work.
PASS WITH REQUIRED FIXES or FAIL must leave Phase 37C blocked and identify
required corrections against this Phase 37B packet.

## Final Governance Summary

Phase 37B is complete when this implementation-contract packet, checkpoint,
outside-validation prompt, and governance records are internally consistent and
accepted by validation. The phase intentionally contains no production
Frequency Pool implementation, no Tag Graph implementation, no repository
builders, no tests or fixtures for implementation code, and no changes outside
the listed governance documents.

The next allowed work after Phase 37B acceptance is Phase 37C contract-first
work for local in-memory Frequency Pool packet models and validators only.
Phase 37C must not include deferred Tag Graph metrics, repository-backed
builders, exports, UI, provider/database access, recommendation integration, or
other deferred work unless a later accepted contract changes the scope.

## Contract Completeness Checklist

This implementation contract defines:

```text
explicit Phase 37B validation tuple
explicit next-phase validation tuple
accepted Phase 37A dependency evidence
authorized future implementation files
future public interface
future packet responsibilities
allowed pool types
identity and provenance rules
metric serialization rules
tag row rules
coverage and caveat rules
privacy boundary
evidence boundary enforcement
fixture inventory
fixture coverage requirements
required tests
future package dependencies and input limits
deferred later work
outside validation packet
```

The listed items are the complete Phase 37B contract surface for the Frequency
Pools / Tag Graph Lab implementation-contract packet.
