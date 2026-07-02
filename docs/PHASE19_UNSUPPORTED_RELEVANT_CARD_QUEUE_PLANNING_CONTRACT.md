# Phase 19 - Unsupported Relevant Card Queue Planning Contract

## Objective

Plan the next dependency-safe Interactive Intelligence layer after Phase 18
Source Conflict Report.

Phase 19 should define how Codie records cards, card behaviors, and evidence
items that are relevant to a user-facing explanation or simulator review but
cannot yet be fully resolved, modeled, or trusted by the current system.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, DB reads, file
writes, analytics calculation, or recommendation generation.

## Accepted Inputs

Phase 19 starts from these accepted foundations:

```text
Phase 16 evidence graph
Phase 17 evidence graph input assembly
Phase 18 source conflict report
Phase 18 outside validation accepted by user
```

## Key Decision

Phase 19 should begin with:

```text
Phase 19A - Unsupported Relevant Card Queue Contract
```

Do not start with:

```text
chat UI
LLM calls
evidence graph persistence
card behavior implementation
source/provider table readers
raw provider payload adapters
recommendation generation
deck coaching language
```

## Why This Lane

Interactive Intelligence and the simulator both need a safe way to surface
known gaps.

Examples:

```text
a simulator trace names a card whose behavior is not implemented
a user deck contains a card that failed lookup
a source conflict depends on a card identity that is unresolved
a card has rules text that is relevant but not modeled by the simulator
a local user deck analysis has a redacted or private card source
a manual review flags a card action as needing further modeling
```

Codie should preserve these gaps as structured backlog evidence, not hide them
or turn them into confident advice.

## Phase 19 Direction

Build the next layer in this order:

```text
1. Unsupported Relevant Card Queue contract
2. Unsupported Relevant Card Queue implementation
3. Chat query planner contract
4. Chat answer builder contract
5. Optional LLM writer/auditor contract
6. UI/API contract
7. Evidence graph persistence contract, only if a real retention need exists
```

## Recommended Phase 19A Scope

Phase 19A should define a pure unsupported-card queue module:

```text
codie/intelligence/unsupported_cards.py
tests/test_intelligence_unsupported_cards.py
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT_REPORT.md
```

The future implementation should define:

```text
UnsupportedCardQueueBuildError
UnsupportedCardEvidenceRef
UnsupportedCardQueueItem
UnsupportedCardQueue
UnsupportedCardQueueOptions
build_unsupported_card_queue(...)
unsupported_card_queue_to_input_records(...)
unsupported_card_queue_to_dict(...)
```

## Data Inputs

Future implementation should accept only already-sanitized records:

```text
EvidenceInputRecord
EvidenceInputBundle
SourceConflictReport-compatible sanitized records
simulator review summaries without raw trace mutation
plain JSON-compatible sanitized card-gap records
```

It must not accept:

```text
raw provider payloads
raw source table rows
raw_input
private deck text
primer body text
unbounded LLM text
```

## Queue Reasons

Suggested allowed reasons:

```text
simulator_unsupported
card_lookup_unresolved
model_gap
rules_text_gap
source_conflict
privacy_redaction
manual_review_required
```

## Status And Severity

Suggested statuses:

```text
open
in_review
resolved
ignored_by_policy
```

Suggested severities:

```text
info
warning
blocking
```

Blocking items must remain visible and must not be hidden by later answer
builders.

## Evidence Rules

Unsupported card queues may:

```text
preserve card-gap evidence references
describe what cannot be resolved or modeled
preserve source names and sanitized record IDs
preserve confidence, status, and severity
emit EvidenceInputRecord values with record_type unsupported_card
emit caveats for missing, redacted, or filtered data
```

Unsupported card queues must not:

```text
implement card behavior
run simulator logic
choose deck construction actions
overwrite raw records
canonicalize records
calculate analytics
rank cards
call LLMs
read DB/source/provider tables
```

## Privacy Rules

Future implementation must reject metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances.

Sensitive evidence must preserve privacy scope and be excluded by default unless
an explicit option includes it.

## Dependency Rules

Phase 19A future implementation may import:

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
marks Phase 18 as accepted input
selects Unsupported Relevant Card Queue as the next dependency-safe layer
blocks chat UI and LLM calls
blocks card behavior implementation until a separate contract exists
blocks persistence until a separate contract exists
blocks DB/provider/source reads
preserves raw_input privacy
preserves evidence/recommendation boundaries
identifies Phase 19A as the next contract
```

## Do Not Do Yet

```text
do not implement unsupported-card queue code
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
Phase 19A - Unsupported Relevant Card Queue Contract
```
