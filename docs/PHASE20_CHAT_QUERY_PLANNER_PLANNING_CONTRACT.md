# Phase 20 - Chat Query Planner Planning Contract

## Objective

Plan the next dependency-safe Interactive Intelligence layer after Phase 19
Unsupported Relevant Card Queue.

Phase 20 should define how Codie classifies a user question and produces a
structured, inspectable query plan before any answer builder, chat UI, LLM
phrasing, persistence, DB reads, provider calls, simulator execution, or
recommendation generation exists.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, DB reads, file
writes, analytics calculation, card behavior implementation, or recommendation
generation.

## Accepted Inputs

Phase 20 starts from these accepted foundations:

```text
Phase 16 evidence graph
Phase 17 evidence graph input assembly
Phase 18 source conflict report
Phase 19 unsupported relevant card queue
Phase 19 outside validation accepted by user
```

## Key Decision

Phase 20 should begin with:

```text
Phase 20A - Chat Query Planner Contract
```

Do not start with:

```text
chat UI
LLM calls
answer generation
evidence graph persistence
DB/repository readers
source/provider table readers
raw provider payload adapters
simulator execution
card behavior implementation
recommendation generation
deck construction instruction language
```

## Why This Lane

Codie now has structured evidence primitives:

```text
Evidence Graph
Evidence Graph Input Assembly
Source Conflict Report
Unsupported Relevant Card Queue
```

The next safe layer is a planner that maps a user question to required evidence
inputs and caveats without producing the final answer.

The planner should determine:

```text
what question class is being asked
what subject is being requested
what evidence record types are needed
what filters are requested
what privacy scopes are allowed
what blockers or caveats must be surfaced
whether an answer builder would need unavailable data
```

It should not write prose answers, call tools, query databases, call an LLM, or
produce recommendations.

## Phase 20 Direction

Build the next layer in this order:

```text
1. Chat Query Planner contract
2. Chat Query Planner implementation
3. Chat Answer Builder contract
4. Chat Answer Builder implementation
5. Optional LLM writer/auditor contract
6. UI/API contract
7. Evidence graph persistence contract, only if a real retention need exists
```

## Recommended Phase 20A Scope

Phase 20A should define a pure query planner module:

```text
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
```

The future implementation should define:

```text
ChatQueryPlanBuildError
ChatQueryRequest
ChatQuerySubject
ChatEvidenceNeed
ChatQueryConstraint
ChatQueryPlan
ChatQueryPlannerOptions
build_chat_query_plan(...)
chat_query_plan_to_dict(...)
```

## Supported Question Classes

Suggested allowed question classes:

```text
deck_summary
card_evidence
commander_evidence
comparison
source_conflict
unsupported_card
simulation_review
primer_metadata
innovation_signal
tag_graph
export_request
unknown
```

## Evidence Need Types

Suggested evidence needs:

```text
evidence_graph
evidence_input_records
deck_memory
saved_analysis
source_conflicts
unsupported_cards
simulation_review_summary
primer_metadata
combo_evidence
innovation_signal
frequency_pool
tag_graph
manual_note
```

## Planner Rules

Future implementation may:

```text
classify sanitized user intent
extract requested subject type and subject key
preserve requested filters
select evidence need types
declare required privacy scope
mark missing inputs as blockers
emit caveats for ambiguity and unavailable data
emit unsupported_card or source_conflict needs when relevant
serialize deterministically
```

Future implementation must not:

```text
answer the question
call an LLM
read or write DB records
call providers
read source/provider tables
read raw provider payloads
run simulator logic
implement card behavior
calculate analytics
generate recommendations
write files
export private raw_input
```

## Privacy Rules

Future implementation must reject request metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances.

Private user-deck context must be represented by privacy scope and references,
not by embedding original deck text.

## Dependency Rules

Phase 20A future implementation may import:

```text
standard library
codie.intelligence.evidence_inputs
```

It must not import:

```text
codie.db
codie.providers
codie.analytics
codie.recommendations.generation
codie.recommendations.persistence
codie.ingestion
codie.cards
codie.probability_engine
codie.canonical
requests
httpx
sqlite3
```

No raw SQL is allowed.

No file-writing behavior is allowed.

## Acceptance Criteria For This Planning Packet

This packet is acceptable if it:

```text
marks Phase 19 as accepted input
selects Chat Query Planner as the next dependency-safe layer
blocks chat UI and LLM calls
blocks answer generation until a separate contract exists
blocks persistence until a separate contract exists
blocks DB/provider/source reads
preserves raw_input privacy
preserves evidence/recommendation boundaries
identifies Phase 20A as the next contract
```

## Do Not Do Yet

```text
do not implement query planner code
do not add schema
do not add evidence graph persistence
do not add chat UI
do not add LLM calls
do not call providers
do not read source/provider payloads directly
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Recommended Next Packet

```text
Phase 20A - Chat Query Planner Contract
```
