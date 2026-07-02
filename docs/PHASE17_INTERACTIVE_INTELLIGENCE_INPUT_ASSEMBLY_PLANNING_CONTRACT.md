# Phase 17 - Interactive Intelligence Input Assembly Planning Contract

## Objective

Plan the next dependency-safe layer after Phase 16 Evidence Graph.

Phase 16 created the in-memory evidence graph primitives. Phase 17 should define
how future Codie read models can be converted into evidence graph inputs without
letting chat, LLMs, DB access, provider payloads, or recommendation output leak
into the intelligence layer.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, DB reads,
file writes, or recommendation generation.

## Accepted Inputs

Phase 17 starts from these accepted foundations:

```text
Phase 15 deck memory retrieval
Phase 16 evidence graph contract and implementation
Phase 16 outside validation accepted by user
```

Relevant future evidence sources already present in the project:

```text
recommendation candidate packets
innovation snapshots
combo evidence records
primer metadata records
simulation review summaries
deck memory summaries
saved analysis summaries
manual notes
```

## Key Decision

Phase 17 should begin with:

```text
Phase 17A - Evidence Graph Input Assembly Contract
```

Do not start with:

```text
chat UI
LLM calls
evidence graph persistence
source/provider table readers
raw provider payload adapters
recommendation generation
deck coaching language
```

## Why This Lane

The evidence graph is useful only if future features can feed it safely.

The next layer should define a narrow, pure conversion boundary:

```text
already-built sanitized read models
-> EvidenceGraphInput
-> build_evidence_graph(...)
```

This preserves the architecture:

```text
repositories/read models own data access
analytics/recommendation/simulator modules own their source semantics
intelligence input assembly only translates supplied sanitized objects
evidence graph remains in-memory and deterministic
```

## Phase 17 Direction

Build the Interactive Intelligence layer in this order:

```text
1. Evidence graph input assembly contract
2. Evidence graph input assembly implementation
3. Source conflict report contract
4. Unsupported relevant card queue contract
5. Deck snapshot contract, only if existing user tables prove insufficient
6. Chat query planner contract
7. Chat answer builder contract
8. Optional LLM writer/auditor contract
9. UI/API contract
10. Evidence graph persistence contract, only if a real retention need exists
```

## Recommended Phase 17A Scope

Phase 17A should define a pure input assembly module:

```text
codie/intelligence/evidence_inputs.py
tests/test_intelligence_evidence_inputs.py
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
```

The future implementation should define:

```text
EvidenceInputBuildError
EvidenceRecordRef
EvidenceInputRecord
EvidenceInputBundle
EvidenceGraphAssemblyOptions
evidence_record_from_dict(...)
validate_evidence_input_bundle(...)
build_graph_input_from_records(...)
```

The future module should accept records that are already:

```text
sanitized
JSON-compatible
privacy-scoped
citation-ready
free of raw provider payloads
free of private raw_input by default
free of primer body text
```

## Allowed Future Input Categories

Phase 17A may define categories for:

```text
recommendation_candidate
innovation_signal
combo_evidence
primer_metadata
simulation_review_summary
deck_memory_summary
saved_analysis_summary
manual_note
source_conflict
unsupported_card
```

These are input categories, not authorization to query the owning subsystems.

## Privacy Rules

The future input assembly layer must preserve Phase 16 privacy rules:

```text
raw_input rejected by default
private_deck_text rejected by default
full_primer_body rejected by default
raw_provider_payload rejected by default
provider_payload rejected by default
original_import_text rejected by default
local_user_data inputs marked local_user_data
sensitive inputs marked sensitive
privacy redactions represented as caveats
```

## Dependency Rules

Phase 17A implementation may import:

```text
standard library
codie.intelligence.evidence_graph
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

## Evidence Rules

Input assembly may:

```text
map sanitized records to evidence nodes
map supplied references to citations
preserve supplied confidence values
preserve caveats
preserve privacy scopes
emit EvidenceGraphInput
```

Input assembly must not:

```text
calculate analytics
generate recommendation candidates
rank cards
infer strategy
invent citations
turn manual notes into tournament evidence
turn simulator output into tournament evidence
read source/provider payloads
call LLMs
```

## Acceptance Criteria For This Planning Packet

This packet is acceptable if it:

```text
marks Phase 16 as accepted input
selects Evidence Graph Input Assembly as the next dependency-safe layer
blocks chat UI and LLM calls
blocks persistence until a separate contract exists
blocks DB/provider/source reads
preserves raw_input privacy
preserves evidence/recommendation boundaries
identifies Phase 17A as the next contract
```

## Do Not Do Yet

```text
do not implement evidence input assembly code
do not add schema
do not add evidence graph persistence
do not add chat UI
do not add LLM calls
do not call providers
do not read source/provider payloads directly
do not run simulator logic
do not calculate analytics
do not generate recommendations
do not export private raw_input
```

## Recommended Next Packet

```text
Phase 17A - Evidence Graph Input Assembly Contract
```
