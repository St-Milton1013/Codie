# Checkpoint - Phase 17 Evidence Graph Input Assembly

## Status

```text
Phase 17 Evidence Graph Input Assembly Internal Checkpoint: PASS
Status: Ready for outside validation before Phase 18
```

This is an internal checkpoint, not external proof.

Phase 18 should not start until the outside validation packet returns:

```text
PASS
PASS WITH REVIEW NOTES
```

## Scope Reviewed

Phase 17 covered the first input assembly layer for the Interactive Intelligence
evidence graph.

Included packets:

```text
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
```

Implementation files:

```text
codie/intelligence/evidence_inputs.py
codie/intelligence/__init__.py
tests/test_intelligence_evidence_inputs.py
```

## Schema Impact

```text
None.
```

Phase 17 adds no tables, columns, indexes, migrations, repository methods, or
persistence records.

## Phase 17 Planning

Phase 17 planning selected Evidence Graph Input Assembly as the next
dependency-safe Interactive Intelligence layer after Phase 16.

Planning explicitly deferred:

```text
chat UI
LLM calls
evidence graph persistence
schema changes
DB reads or writes
provider calls
source/provider payload reads
simulator execution
analytics calculation
recommendation generation
private raw_input export
```

## Phase 17A - Input Assembly Contract

Phase 17A defined a pure conversion layer:

```text
sanitized read-model records
-> EvidenceInputBundle
-> EvidenceGraphInput
-> build_evidence_graph(...)
```

The contract required:

```text
sanitized record references
sanitized input records
sanitized input bundles
record type to node type mapping
reference to citation mapping
bundle and record caveat preservation
sensitive record filtering
local_user_data privacy preservation
private metadata rejection
no DB/provider/source reads
no LLM calls
no recommendation generation
```

## Phase 17B - Input Assembly Implementation

Phase 17B implemented:

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

Behavior verified:

```text
valid input bundle builds EvidenceGraphInput
record types map to expected EvidenceNode types
references map to EvidenceCitation values
manual_note may omit references
non-manual records require references
duplicate record IDs fail cleanly
unsupported record types fail cleanly
invalid confidence fails cleanly
private metadata keys fail cleanly
nested private metadata keys fail cleanly
sensitive records are excluded by default
sensitive records are included only with explicit option
local_user_data privacy scope is preserved
minimum confidence filters low-confidence records
filtered records create caveats when interpretation changes
filtered-empty bundles fail cleanly
bundle caveats are preserved
record caveats are preserved and linked to their nodes
forbidden strategic language fails cleanly
EvidenceGraphInput is assembled with no MVP edges
build_graph_input_from_records(...) returns edges == [] for MVP input bundles
```

## Boundary Compliance

The Phase 17 implementation does not import:

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

The Phase 17 implementation does not:

```text
read or write DB
import repositories
read source/provider tables
read raw provider payloads
call providers
call LLMs
run simulator logic
calculate analytics
generate recommendations
write files
export private raw_input
```

No raw SQL is present in the input assembly module.

## Privacy And Evidence Rules

Phase 17 preserves these rules:

```text
input assembly consumes sanitized records only
raw_input is rejected by default
private_deck_text is rejected by default
full_primer_body is rejected by default
raw_provider_payload is rejected by default
provider_payload is rejected by default
original_import_text is rejected by default
nested private metadata keys are rejected
sensitive records are excluded by default
local_user_data records preserve privacy_scope
filtered records create caveats
manual notes do not become tournament evidence
```

## Recommendation Boundary

Phase 17 does not generate recommendations.

Recommendation candidate records may be consumed only as already-built,
sanitized evidence records. The input assembly layer must not rank cards,
generate candidate records, or create play/cut/include/upgrade instructions.

## Validation Evidence

Focused Phase 17B tests:

```text
Ran 19 tests in 0.003s

OK
```

Latest full suite:

```text
Ran 566 tests in 3.185s

OK (skipped=1)
```

Static checks:

```text
git diff --check: PASS
forbidden evidence input import scan: no matches
raw SQL scan: no matches
production file-write scan: no matches
source/provider table term scan: no matches
strategic language scan: no matches
schema/repository drift scan: no matches
```

## Review Notes

```text
Input assembly is in-memory only.
Input assembly accepts sanitized records only.
No persistence exists for evidence graph inputs yet.
No chat UI exists yet.
No LLM writer/auditor workflow is implemented yet.
No final recommendation output is implemented yet.
MVP edge construction is intentionally deferred.
```

## Outside Validation Packet

Send:

```text
docs/CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE17_INPUT_ASSEMBLY_PROMPT.md
```

Recommended supporting docs:

```text
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT.md
docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
```

## Internal Verdict

```text
Phase 17: PASS
Ready for outside validation before Phase 18
```
