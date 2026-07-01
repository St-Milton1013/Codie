# Phase 16 - Interactive Intelligence Foundation Planning Contract

## Objective

Plan the first implementation track for Codie's Interactive Intelligence Layer
after Phase 15 deck memory validation.

This phase must not start with a generic chat box. The first work should build
structured, inspectable evidence artifacts that future chat, UI, and optional
LLM phrasing can consume safely.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, recommendation output, provider access, or source-table reads.

## Current Inputs

Accepted prior foundations:

```text
Phase 8 recommendation statistics, evidence, scoring, and candidate packets
Phase 10 user deck import/comparison/export
Phase 12 local UI/report sharing track
Phase 13 simulator and challenge/review track
Phase 14 simulator review export surfaces
Phase 15 deck memory and local CLI
```

Relevant roadmap patches:

```text
docs/ROADMAP_PATCH_INTERACTIVE_INTELLIGENCE_LAYER.md
docs/ROADMAP_PATCH_DECK_MEMORY_MOXFIELD_CONFIDENCE_NAMING.md
```

## Key Decision

Phase 16 should begin with:

```text
Phase 16A - Evidence Graph Contract
```

Do not start with:

```text
chat UI
LLM calls
free-form assistant answers
schema changes
recommendation output changes
```

The evidence graph is the safest foundation because it gives later chat and UI
surfaces a structured source of claims, citations, confidence, and caveats.

## Phase 16 Direction

Build a tool-first intelligence layer in this order:

```text
1. Evidence graph contract
2. Evidence graph implementation
3. Deck snapshot contract if existing user tables prove insufficient
4. Unsupported relevant card queue contract
5. Source conflict report contract
6. Primer summary contract
7. Chat query planner contract
8. Chat answer builder contract
9. UI/API contract
10. Optional LLM phrasing contract
```

## Evidence Graph Purpose

Future evidence graphs should represent structured explanations for Codie
outputs.

They should answer:

```text
what claim is being explained
which evidence nodes support it
which source records or local records are cited
what confidence/caveats apply
which unsupported cards or missing models affect interpretation
```

Evidence graphs are explanation artifacts.

They are not:

```text
source records
canonical tournament records
recommendation truth
LLM memory
private deck exports
```

## Candidate Evidence Node Types

Future contracts may include:

```text
card
commander
deck
package
tournament_stat
regional_stat
historical_stat
innovation_signal
primer_metadata
combo_evidence
simulation_result
unsupported_card
source_conflict
user_deck_memory
saved_analysis
manual_note
```

## Candidate Evidence Edge Types

Future contracts may include:

```text
supports
contradicts
qualifies
derived_from
same_card_as
same_commander_as
observed_in
linked_to
requires_caveat
```

## Initial Data Inputs

Phase 16A should prefer existing read models and repositories:

```text
canonical tables
analytics tables
recommendation candidate packets
innovation snapshots
combo evidence
primer metadata
simulation review summaries
deck memory summaries
saved analysis summaries
```

Phase 16A must not read raw provider payloads directly.

## Privacy Rules

Private user deck data must stay protected.

Rules:

```text
raw_input must not enter evidence graphs by default
raw_input requires explicit future opt-in
user deck memory nodes must be marked local_user_data
user deck memory must not become tournament evidence
private deck text must not be sent to cloud LLMs
```

## LLM Rules

Phase 16 planning does not authorize LLM usage.

Future LLM usage must follow:

```text
tools first
structured context second
LLM language last
LLM output is never source of truth
LLM output may not write DB directly
LLM output must cite supplied evidence node IDs
LLM output must preserve uncertainty and caveats
cloud LLM use must be explicit opt-in for sensitive inputs
```

## Recommendation Rules

Phase 16 must not create unsupported recommendation claims.

Allowed:

```text
describe evidence nodes
describe observed inclusion rates
describe confidence and sample size
describe missing or unsupported information
describe why an existing recommendation candidate was generated
```

Forbidden:

```text
this card should be played
this card should be cut
this card is correct
this card is optimal
LLM-generated strategic coaching
```

## Schema Impact

Phase 16 planning approves no schema changes.

Evidence graph persistence may be useful later, but it requires a separate
schema contract defining:

```text
table ownership
foreign keys
indexes
retention
privacy rules
repository methods
idempotency
derived-data rebuild path
```

Phase 16A should start in-memory unless a contract proves persistence is needed.

## Phase 16A Recommended Scope

Phase 16A should be contract-only and define:

```text
EvidenceGraph
EvidenceNode
EvidenceEdge
EvidenceCitation
EvidenceCaveat
EvidenceGraphBuildError
graph construction inputs
serialization shape
allowed node/edge types
privacy flags
confidence/caveat fields
strategic-language restrictions
tests for future implementation
```

## Required Guardrails For Phase 16A

```text
no schema changes
no DB writes
no provider calls
no source/provider table reads
no LLM calls
no UI
no simulator execution
no mutation of raw simulator traces
no recommendation generation
no private raw_input by default
```

## Acceptance Criteria For This Planning Packet

This packet is acceptable if it:

```text
marks Phase 15 as accepted input
selects evidence graph as the next dependency-safe foundation
blocks generic chat and LLM calls
blocks schema changes until a schema contract exists
preserves user deck privacy
preserves recommendation/evidence boundaries
identifies Phase 16A as the next contract
```

## Do Not Do Yet

```text
do not implement evidence graph code
do not add schema
do not add chat UI
do not add LLM calls
do not call providers
do not read source/provider payloads directly
do not run simulator logic
do not generate recommendations
do not export private raw_input
```
