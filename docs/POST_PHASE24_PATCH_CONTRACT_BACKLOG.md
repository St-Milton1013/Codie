# Post-Phase 24 Patch Contract Backlog

Status: planning-only

## Purpose

This document converts accepted roadmap patches into an explicit future
contract backlog.

It does not authorize implementation, schema changes, new repositories, new
providers, LLM calls, UI work, file writing, or recommendation output.

Phase 25 remains blocked until Phase 24 outside validation returns PASS or PASS
WITH REVIEW NOTES.

## Current Patch Inventory

Roadmap patches and related specs currently logged:

```text
docs/ROADMAP_PATCH_EVIDENCE_ARCHITECTURE_REMASTER.md
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/ROADMAP_PATCH_INTERACTIVE_INTELLIGENCE_LAYER.md
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/ROADMAP_PATCH_DECK_MEMORY_MOXFIELD_CONFIDENCE_NAMING.md
docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md
docs/ROADMAP_PATCH_SIMULATOR_CARD_DEFINITION_MANAGER.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/PHASE8B_ANALYTICS_INNOVATION_DETECTION_PATCH_CONTRACT.md
docs/FREQUENCY_POOL_SPEC.md
docs/COMMANDER_STAPLES_SPEC.md
docs/CO_OCCURRENCE_METRICS_SPEC.md
docs/EVIDENCE_GRAPH_SPEC.md
docs/CODIE_CHAT_SPEC.md
```

## Deferred Architecture-Approved Track

### Simulator Revision (SIM-R)

Status:

```text
architecture approved
implementation deferred
not part of the active Phase 29 chain
```

SIM-R is logged in:

```text
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
```

Do not implement SIM-R until:

```text
current implementation and validation chain is complete
current checkpoints pass
existing simulator contracts are frozen
dedicated SIM-R architecture contract exists
dedicated SIM-R outside validation returns PASS or PASS WITH REVIEW NOTES
dedicated SIM-R checkpoint plan is accepted
```

SIM-R must preserve all existing simulator behavior and historical results.
It must not turn Codie into a full Magic rules engine, Forge runtime,
opponent simulator, combat engine, or LLM-generated execution system.

## Required Contract Sequence

Codie Architecture Revision III supersedes earlier evidence-architecture
roadmap drafts where they conflict.

### 1. Evidence Fusion / Unified Evidence Objects

Recommended phase:

```text
Phase 25A
```

Why first:

Codie Architecture Revision III requires every downstream reasoning feature to
consume Unified Evidence instead of reading raw source/provider data or building
its own reasoning path.

Contract must define:

```text
unified evidence object models
Authority Layer refs
source evidence refs
canonical identity refs
measured metric refs
primer context refs
simulator statistic refs
conflict/caveat refs
confidence inputs
source agreement inputs
deterministic serialization
privacy rules
private metadata rejection
```

Must prohibit:

```text
DB reads or writes unless a repository contract exists
raw provider reads
source table reads
recommendation generation
LLM calls
UI rendering
file writing
simulator execution
analytics recalculation
Jin-Gitaxias theory generation
```

### 2. Decision Intelligence Boundary

Recommended phase:

```text
Phase 26A
```

Purpose:

Define the only subsystem allowed to produce recommendation conclusions.

Contract must enforce:

```text
no recommendations directly from raw providers
no recommendations directly from source tables
no UI-generated recommendations
no chat-generated recommendations
no export-generated recommendations
all recommendation output flows through Decision Intelligence
all recommendation output cites unified evidence objects
Jin-Gitaxias theory output cannot be persisted as recommendation evidence
```

### 3. Weight Profile / Analysis Profile

Recommended phase:

```text
Phase 26B
```

Purpose:

Make evidence weighting configurable, versioned, and reproducible.

Contract must define:

```text
profile_id
profile_name
profile_version
weight components
default profiles
generated_at
analysis_version
serialization format
compatibility rules
replay behavior for old analyses
```

Suggested profiles:

```text
Competitive Default
Tournament Heavy
Simulation Heavy
Primer Aware
Budget Aware
```

### 4. Ratio-Aware Confidence

Recommended phase:

```text
Phase 26C
```

Purpose:

Extend confidence beyond a minimum-deck-count gate.

Contract must define:

```text
eligible_deck_count
available_deck_count
matching_deck_count
coverage_ratio
date window
region scope
commander scope
low-sample caveats
ratio threshold behavior
```

### 5. Frequency Pool Builder

Recommended phase:

```text
Phase 27A
```

Purpose:

Build commander or partner-pair card frequency pools from approved inputs.

Start with fixture/manual-input mode before live Moxfield fetching.

Contract must define:

```text
manual decklist input format
Moxfield export input format
commander signature rules
frequency row models
pool metadata
privacy handling
raw private deck text handling
Moxfield-compatible export goals
```

Must prohibit until later contracts:

```text
live Moxfield network dependency
new schema
provider writes
recommendation generation
UI chart rendering
private deck text export
```

### 6. Tag Source Import

Recommended phase:

```text
Phase 28A
```

Purpose:

Create the tag foundation before Tag Graph Lab.

Contract must define:

```text
Scryfall Tagger import mode
curated functional registry input
oracle_id mapping
scryfall_id mapping
tag namespace
tag source
tag confidence
tag provenance
user correction model
duplicate behavior
```

Must precede:

```text
tag metrics
tag graph runs
tag chart export
tag UI
tag-based LLM summaries
```

### 7. Tag Metrics / Tag Graph Lab

Recommended phase:

```text
Phase 28B+
```

Contract must define:

```text
selected tag limit
raw_tag_count
tag_density
tag_inclusion_rate
average_cards_per_deck_with_tag
placement_weighted_tag_usage
top_16_tag_frequency
winner_tag_frequency
tag_trend_delta
tag_confidence
matching_deck_count
available_deck_count
coverage_ratio
underlying card list exposure
underlying numeric table exposure
```

### 8. LLM-Assisted Naming / Alias Review

Recommended phase:

```text
Phase 29A
```

Purpose:

Use a writer/auditor pattern to propose alias or naming candidates without
letting an LLM mutate identity.

Contract must enforce:

```text
LLM writer proposes candidates only
auditor checks candidates
deterministic validator checks Scryfall and alias_registry
human or deterministic approval required before persistence
auditor rejection blocks persistence
rejected alias does not resolve future imports
no unresolved name silently accepted
```

### 9. Jin-Gitaxias Strategist Mode Boundary

Recommended phase:

```text
Post-alpha TBD
```

Purpose:

Define a future conversational theory engine without contaminating measured
evidence or recommendations.

Contract must define:

```text
retrieval planner
evidence retrieval
primary strategist model packet
evidence gate
legality validator
contradiction scanner
optional auditor model
final answer packet
safety valve fields
theory note output rules
experiment queue output rules
```

Must enforce:

```text
no writes to tournament evidence
no writes to measured evidence
no writes to confidence metrics
no writes to recommendations
no writes to staples
no writes to package statistics
all factual claims pass evidence validation
all card suggestions pass legality validation
speculation level is visible
unsupported claims removed count is visible
illegal suggestions blocked count is visible
```

### 10. Obsidian / Knowledge Vault Export

Recommended phase:

```text
Phase 31A
```

Purpose:

Extend existing export surfaces into an optional knowledge vault format.

Contract must define:

```text
output-root containment
frontmatter shape
trace export rules
stale document behavior
private data exclusion
review annotation export
no mutation of simulator history
no recommendation generation
```

## Already Covered Or Mostly Covered

These patch areas already have substantial implementation and checkpoint
coverage:

```text
Interactive intelligence primitives: Phases 16-24
Evidence graph in-memory primitives: Phase 16
Evidence input assembly: Phase 17
Source conflict report: Phase 18
Unsupported relevant card queue: Phase 19
Chat query planner: Phase 20
Chat answer builder: Phase 21
LLM writer/auditor packet layer: Phase 22
UI/API packet boundary: Phase 23
Local API packet boundary: Phase 24
Simulator card definition manager: Phase 13
Challenge mode and line review core: Phase 13
Simulation review export writer: Phase 14
Innovation detection: Phase 8
Deck memory: Phase 15
```

## Active Blocking Rule

Before final recommendation generation or action-first dashboard work:

```text
Evidence Fusion / Unified Evidence Objects must exist.
Decision Intelligence Boundary must exist.
Weight Profile / Analysis Profile must exist.
```

Do not implement recommendation output directly in:

```text
providers
source ingestion
canonicalization
analytics metric builders
chat answer builder
UI/API boundary
local API boundary
exports
simulator
primer context extraction
Jin-Gitaxias Strategist Mode
```

## Recommended Next Move

After Phase 24 outside validation is accepted:

```text
Phase 25A - Evidence Fusion / Unified Evidence Objects Contract
```

This is the lowest-risk next step because it turns Codie Architecture Revision
III into a concrete contract before any more recommendation or dashboard work.
