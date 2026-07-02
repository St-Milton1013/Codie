# Phase 17A - Evidence Graph Input Assembly Contract

## Objective

Define a pure input assembly layer that converts already-sanitized Codie read
models into `EvidenceGraphInput` objects.

This contract prepares the path from existing evidence/read-model packets to
the Phase 16 evidence graph without adding DB access, provider access, source
payload reads, LLM calls, UI, persistence, analytics calculation, or
recommendation generation.

This is a contract packet. It adds no implementation code.

## Future Files

Future implementation should create:

```text
codie/intelligence/evidence_inputs.py
tests/test_intelligence_evidence_inputs.py
docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

Future implementation should define:

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

## EvidenceRecordRef

Required fields:

```text
source_type
source_name
source_record_id
source_url
observed_at
```

Rules:

```text
source_type must map to an allowed EvidenceCitation source_type
source_name is required
observed_at is required
source_record_id or source_url is required
raw provider payloads are forbidden
raw_input is forbidden
```

## EvidenceInputRecord

Required fields:

```text
record_id
record_type
label
summary
confidence
privacy_scope
references
caveats
metadata
```

Allowed `record_type` values:

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

Rules:

```text
record_id is required
record_type is required
label is required
summary is required
confidence must be between 0 and 1
privacy_scope must map to an allowed EvidenceNode privacy_scope
non-manual records require at least one reference
manual_note may omit references
metadata must be JSON-compatible
metadata must not contain private/raw keys
```

## EvidenceInputBundle

Required fields:

```text
bundle_id
claim_type
claim_text
subject_type
subject_id
generated_at
records
bundle_caveats
metadata
```

Rules:

```text
bundle_id is required
claim_text is required
records must not be empty
record IDs must be unique
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## EvidenceGraphAssemblyOptions

Suggested fields:

```text
graph_id
include_manual_notes
include_local_user_data
include_sensitive
minimum_confidence
```

Default behavior:

```text
include_manual_notes = true
include_local_user_data = true
include_sensitive = false
minimum_confidence = 0.0
```

Rules:

```text
sensitive records are excluded unless include_sensitive is true
local_user_data records may be included but must keep privacy_scope
filtered records must be represented by caveats when omission changes interpretation
minimum_confidence must be between 0 and 1
```

## Mapping To Evidence Graph

`build_graph_input_from_records(...)` should return an `EvidenceGraphInput`.

Mapping:

```text
bundle_id -> graph_id unless graph_id option overrides
claim_type -> claim_type
claim_text -> claim_text
subject_type -> subject_type
subject_id -> subject_id
generated_at -> generated_at
records -> EvidenceNode values
record references -> EvidenceCitation values
record caveats and bundle caveats -> EvidenceCaveat values
relationships -> no edges in MVP unless explicitly supplied by future contract
```

Initial implementation may emit no edges.

Future edge construction requires a separate contract if it needs domain-specific
relationships beyond direct record inclusion.

## Record Type To Node Type Mapping

Required mapping:

```text
recommendation_candidate -> card
innovation_signal -> innovation_signal
combo_evidence -> combo_evidence
primer_metadata -> primer_metadata
simulation_review_summary -> simulation_result
deck_memory_summary -> user_deck_memory
saved_analysis_summary -> saved_analysis
manual_note -> manual_note
source_conflict -> source_conflict
unsupported_card -> unsupported_card
```

Recommendation candidates are allowed only as already-built candidate evidence.
The input assembly layer must not generate new recommendation candidates.

## Privacy Rules

The input assembly layer must reject metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

The layer must also reject nested appearances of these keys.

Sensitive defaults:

```text
sensitive records excluded by default
local_user_data records included by default but marked local_user_data
privacy redaction caveats preserved
private raw text never emitted
```

## Dependency Rules

Future implementation may import:

```text
standard library
codie.intelligence.evidence_graph
```

Future implementation must not import:

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

## Failure Modes

Future implementation should raise `EvidenceInputBuildError` for:

```text
missing bundle_id
missing claim_text
missing subject_id
empty records
duplicate record_id
unsupported record_type
invalid confidence
invalid privacy_scope
missing reference on non-manual record
reference missing source_name
reference missing observed_at
reference missing both source_record_id and source_url
metadata not JSON-compatible
private/raw metadata key present
filtered bundle with no remaining records
forbidden strategic language
```

## Required Tests For Phase 17B

```text
valid input bundle builds EvidenceGraphInput
record type maps to expected node type
references map to citations
manual_note may omit references
non-manual record requires reference
duplicate record IDs fail cleanly
unsupported record type fails cleanly
invalid confidence fails cleanly
private metadata keys fail cleanly
nested private metadata keys fail cleanly
sensitive records excluded by default
sensitive records included only with option
local_user_data privacy scope is preserved
minimum confidence filters low-confidence records
filtered records create caveats when interpretation changes
forbidden strategic language fails cleanly
module has no forbidden imports
module has no raw SQL
module has no file-writing behavior
full suite passes
```

## Do Not Do In Phase 17A

```text
do not implement evidence input assembly code
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not run simulator logic
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Recommended Next Packet

```text
Phase 17B - Evidence Graph Input Assembly Implementation
```
