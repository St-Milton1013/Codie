# Phase 15 - Deck Memory And Interactive Intelligence Planning Contract

## Objective

Plan the next project track after Phase 14.

Phase 15 begins the foundation for user-facing memory and future interactive
intelligence. It must not start with chat UI or LLM calls. The first useful
step is making saved user deck artifacts easier to retrieve, filter, and compare
using existing user tables.

## Current Inputs

Accepted prior work:

```text
Phase 10 user deck import/comparison/export
Phase 11 saved analysis retrieval
Phase 12 local report sharing/UI prep
Phase 13 simulator track
Phase 14 simulator review export surfaces
```

Relevant roadmap patches:

```text
docs/ROADMAP_PATCH_DECK_MEMORY_MOXFIELD_CONFIDENCE_NAMING.md
docs/ROADMAP_PATCH_INTERACTIVE_INTELLIGENCE_LAYER.md
```

## Key Decision

Phase 15 should not implement generic chat first.

The Interactive Intelligence Layer requires stable deck snapshots, evidence
retrieval, unsupported-card visibility, and source-conflict review surfaces
before a chat router can safely answer questions.

Recommended first implementation:

```text
Phase 15A - Deck Memory Listing And Retrieval Contract
```

## Existing Tables To Use First

Use existing tables before adding schema:

```text
user_decks
user_deck_cards
analysis_sessions
saved_analysis
```

These already provide:

```text
deck_name
source_url
deck_hash
commander_hash
raw_input
created_at
updated_at
is_temporary
resolved user deck card rows
analysis session metadata
saved analysis summaries
```

## Phase 15A Recommended Scope

Build read-only deck memory models and helpers over existing user-deck records.

Allowed scope:

```text
list saved/imported user decks
filter by commander_hash
filter by deck_hash
filter temporary vs persistent deck records
show deck memory detail
include linked saved_analysis summaries
include linked analysis_sessions
include resolved card rows
include raw_input only in detail view
```

CLI can be added after helper contract is accepted:

```text
list-user-decks
show-user-deck-memory
```

## Required Guardrails

Deck memory records are user-local artifacts.

They are not:

```text
tournament evidence
source/provider records
canonical tournament decks
recommendation truth
primer evidence
public exports
```

Private user deck text must not be exported, uploaded, or sent to an LLM without
explicit user action and a future contract.

## Dependency Rules

Deck memory helper may import:

```text
codie.db.repositories.user
standard library
```

It must not import:

```text
providers
source repositories
analytics
recommendations
simulator/probability engine
canonicalization
ingestion
LLM clients
network clients
```

## Schema Impact

Phase 15A should have no schema impact unless implementation proves an explicit
gap.

Potential future schema, not approved yet:

```text
user_deck_snapshots
user_deck_snapshot_cards
```

Do not add those tables in Phase 15A unless a separate schema contract is
approved.

## Suggested Phase Split

```text
Phase 15A - Deck Memory Listing And Retrieval Contract
Phase 15B - Deck Memory Listing And Retrieval Implementation
Phase 15C - Deck Memory CLI Contract
Phase 15D - Deck Memory CLI Implementation
Phase 15E - Deck Version Difference Contract
Phase 15F - Deck Version Difference Implementation
Phase 15G - Unsupported Relevant Card Queue Contract
Phase 15H - Source Conflict Report Contract
Phase 15I - Phase 15 Checkpoint
```

Only after these foundations are accepted should Codie start:

```text
evidence graph
chat query planner
chat answer builder
chat UI/API
LLM phrasing layer
```

## Acceptance Criteria For Phase 15 Planning

This planning packet is acceptable if:

```text
it selects deck memory as the next dependency-safe foundation
it uses existing user tables first
it blocks chat UI and LLM calls for now
it preserves evidence-only boundaries
it forbids user deck memory from becoming tournament evidence
it identifies Phase 15A as the next contract
```

## Do Not Do Yet

```text
do not add schema
do not add chat UI
do not add LLM calls
do not export private deck text
do not calculate recommendations
do not read provider/source tables
do not mutate canonical analytics
do not treat user decks as tournament evidence
```
