# Phase 37A - Frequency Pools / Tag Graph Lab Contract

Status: contract only

## Purpose

Phase 37A defines the future boundary for Frequency Pools and Tag Graph Lab.

This phase exists because the post-31 deferred implementation priority plan
places Frequency Pools and Tag Graph Lab after immutable deck snapshots. The
goal is to define how future phases may turn accepted canonical identities,
Scryfall Tagger ontology packets, Spellbook interpretation metadata, user-local
snapshots, and measured evidence into comparison surfaces without generating
recommendations.

Phase 37A does not implement frequency pool code, tag graph code, metrics,
exports, schema, repositories, provider calls, UI, file writing, LLM calls,
simulator execution, or recommendations.

## Accepted Dependency

Phase 37A may begin because Phase 36C outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review notes carried forward:

```text
The normal Windows Python/venv environment is broken. Phase 36C passed using
Codex's bundled Python runtime, but the local Python PATH/venv should be
repaired before relying on normal local validation commands again.

Later export/report phases must preserve the Phase 36C privacy contract and
avoid reintroducing raw deck text, private notes, primer bodies, or provider
payloads downstream.
```

## Governing Inputs

Future Frequency Pool / Tag Graph work must consume only already accepted,
sanitized, canonicalized inputs.

Allowed future input classes:

```text
canonical card identities
canonical commander identities
Scryfall oracle IDs
Scryfall IDs when preserving card identity provenance
Scryfall Tagger ontology packets
curated functional tag registry packets
Role Fusion / functional role packets when separately accepted
Commander Spellbook interpretation packets
measured evidence records
commander staple / frequency observations
immutable user deck snapshots for user-local scopes only
public deck/source references through accepted repositories only when separately contracted
```

Forbidden future direct inputs:

```text
raw provider payloads
raw imported user deck text
private notes
primer body text
source/provider tables directly
live provider APIs
live Scryfall Tagger calls
live Moxfield calls
live Spellbook calls
LLM-generated tags or metrics
simulator traces as tournament evidence
recommendation outputs as metric inputs
```

## Required Future Boundaries

Future implementation contracts must preserve these rules:

```text
all card metrics use canonical card identities
functional tags map to oracle_id
Scryfall IDs remain visible where card-print provenance matters
tags preserve source provenance
low sample size is labeled
low tag coverage is labeled
coverage_ratio remains visible
matching_deck_count remains visible
available_deck_count remains visible
user decks never enter commander averages
user-local snapshot scopes are labeled as user-local
frequency pools do not generate recommendations
tag graphs do not generate strategic claims
LLMs may not create tag metrics
LLMs may not summarize single-deck reports unless separately contracted
simulator results remain simulator evidence only
```

## Future Frequency Pool Scope

Future implementation contracts may define packet models for:

```text
frequency pool subject
frequency pool source window
commander pool
partner-pair pool
winner pool
top-cut pool
regional pool
personal deck history pool
card frequency rows
functional tag frequency rows
coverage reports
low-sample caveats
source provenance
```

Future frequency pool packets must not rank cards as includes or cuts. They may
report measured presence, inclusion rate, density, trend, coverage, and caveats.

## Future Tag Graph Lab Scope

Future implementation contracts may define packet models for:

```text
selected tags, limited to one through six tags
tag count rows
tag density rows
tag inclusion rows
top card contributors per tag
tag overlap matrix rows
tag correlation rows
tag trend rows
deck vs commander average comparison rows
frequency pool tag breakdown rows
underlying numeric tables
underlying card lists
coverage caveats
source provenance
```

The default comparison may be:

```text
analyzed deck vs commander top-cut average
```

Only future UI/export contracts may decide how these packets are rendered.

## Required Future Metrics

Future implementation contracts should define deterministic calculation rules
for:

```text
raw_tag_count
tag_density
tag_inclusion_rate
average_cards_per_deck_with_tag
placement_weighted_tag_usage
top_cut_tag_frequency
winner_tag_frequency
tag_trend_delta
tag_confidence
matching_deck_count
available_deck_count
coverage_ratio
```

No metric may be calculated from raw provider payloads directly.

## Future Privacy Rules

Future implementation contracts must preserve Phase 36C privacy rules:

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

## Future Implementation Split

Recommended future sequence:

```text
Phase 37B - Frequency Pools / Tag Graph Lab Implementation Contract
Phase 37C - Frequency Pool Packet Models and Validators
Phase 37D - Tag Graph Metric Packet Models and Validators
Phase 37E - Tag Graph Export / Report Contract
```

Each future implementation phase must be separately contracted and validated.

## Forbidden In Phase 37A

Phase 37A must not add:

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
```

## Outside Validation Packet

Phase 37A outside validation should review:

```text
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
Phase 37A outside validation: REQUIRED
```

Phase 37B may begin only after Phase 37A outside validation returns PASS or
PASS WITH REVIEW NOTES.
