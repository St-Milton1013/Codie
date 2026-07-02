# Phase 17A - Evidence Graph Input Assembly Contract Report

## Status

```text
Phase 17A Contract: COMPLETE
Validation: PASS
```

## Scope

Created:

```text
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
```

## Contract Summary

Phase 17A defines a future pure input assembly layer:

```text
sanitized read-model records
-> EvidenceInputBundle
-> EvidenceGraphInput
-> build_evidence_graph(...)
```

The contract defines:

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

## Boundary Summary

The future implementation is allowed to import only:

```text
standard library
codie.intelligence.evidence_graph
```

The contract blocks:

```text
schema changes
DB reads or writes
repository imports
provider calls
source/provider table reads
raw provider payload reads
LLM calls
UI
simulator execution
analytics calculation
recommendation generation
file writing
private raw_input export
```

## Privacy Summary

The contract requires rejection of:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested metadata keys.

Sensitive records are excluded by default. Local user data may be included but
must preserve `local_user_data` privacy scope.

## Validation

Documentation-only packet.

Static validation:

```text
git diff --check: PASS
Phase 17A strategic language scan: no matches
schema/repository drift scan: no matches
```

Full suite validation:

```text
Ran 547 tests in 3.190s

OK (skipped=1)
```

No tests were added because this packet adds no executable code.

## Next Packet

```text
Phase 17B - Evidence Graph Input Assembly Implementation
```
