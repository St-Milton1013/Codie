# Phase 18 - Source Conflict Report Planning Contract

## Objective

Plan the next dependency-safe Interactive Intelligence layer after Phase 17
Evidence Graph Input Assembly.

Phase 18 should define how Codie represents conflicts between already-sanitized
evidence records before any chat UI, LLM phrasing, persistence, or
recommendation generation exists.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, DB reads, file
writes, analytics calculation, or recommendation generation.

## Accepted Inputs

Phase 18 starts from these accepted foundations:

```text
Phase 16 evidence graph
Phase 17 evidence graph input assembly
Phase 17 outside validation accepted by user
```

## Key Decision

Phase 18 should begin with:

```text
Phase 18A - Source Conflict Report Contract
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

Interactive Intelligence needs a safe way to represent disagreement.

Examples:

```text
two sanitized evidence records disagree on commander identity
one source reports a deck as public while another source has no decklist
analytics evidence and primer metadata point to different package labels
simulation review evidence has unsupported behavior caveats
local user deck memory conflicts with saved analysis metadata
```

Codie should preserve these conflicts as structured evidence, not collapse them
into confident language.

## Phase 18 Direction

Build the next layer in this order:

```text
1. Source Conflict Report contract
2. Source Conflict Report implementation
3. Unsupported Relevant Card Queue contract
4. Unsupported Relevant Card Queue implementation
5. Chat query planner contract
6. Chat answer builder contract
7. Optional LLM writer/auditor contract
8. UI/API contract
9. Evidence graph persistence contract, only if a real retention need exists
```

## Recommended Phase 18A Scope

Phase 18A should define a pure conflict report module:

```text
codie/intelligence/source_conflicts.py
tests/test_intelligence_source_conflicts.py
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
```

The future implementation should define:

```text
SourceConflictBuildError
SourceConflictEvidenceRef
SourceConflictItem
SourceConflictReport
SourceConflictReportOptions
build_source_conflict_report(...)
source_conflict_report_to_input_records(...)
source_conflict_report_to_dict(...)
```

## Data Inputs

Future implementation should accept only already-sanitized conflict inputs:

```text
EvidenceInputRecord
EvidenceInputBundle
EvidenceGraphInput
plain JSON-compatible sanitized conflict records
```

It must not accept:

```text
raw provider payloads
raw source table rows
raw_input
primer body text
unbounded LLM text
```

## Conflict Types

Suggested allowed conflict types:

```text
identity_mismatch
metadata_mismatch
source_disagreement
missing_evidence
privacy_redaction
unsupported_behavior
stale_data
manual_review_required
```

## Severity

Suggested severities:

```text
info
warning
blocking
```

Blocking conflicts must remain visible and must not be hidden by later answer
builders.

## Evidence Rules

Source conflict reports may:

```text
preserve conflict evidence references
describe what fields disagree
preserve source names and sanitized record IDs
preserve confidence and severity
emit EvidenceInputRecord values with record_type source_conflict
emit caveats for missing or redacted data
```

Source conflict reports must not:

```text
choose a winner source
overwrite raw records
canonicalize records
calculate analytics
generate recommendations
rank cards
infer strategy
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

Sensitive conflict evidence must preserve privacy scope.

## Dependency Rules

Phase 18A future implementation may import:

```text
standard library
codie.intelligence.evidence_graph
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
marks Phase 17 as accepted input
selects Source Conflict Report as the next dependency-safe layer
blocks chat UI and LLM calls
blocks persistence until a separate contract exists
blocks DB/provider/source reads
preserves raw_input privacy
preserves evidence/recommendation boundaries
identifies Phase 18A as the next contract
```

## Do Not Do Yet

```text
do not implement source conflict code
do not add schema
do not add evidence graph persistence
do not add chat UI
do not add LLM calls
do not call providers
do not read source/provider payloads directly
do not run simulator logic
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Recommended Next Packet

```text
Phase 18A - Source Conflict Report Contract
```
