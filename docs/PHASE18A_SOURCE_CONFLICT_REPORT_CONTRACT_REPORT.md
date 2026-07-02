# Phase 18A - Source Conflict Report Contract Report

## Status

```text
Phase 18A Contract: COMPLETE
Validation: PASS
```

## Scope

Created:

```text
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
```

## Contract Summary

Phase 18A defines a future pure source conflict report layer:

```text
sanitized conflict evidence refs
-> SourceConflictReport
-> EvidenceInputRecord(record_type=source_conflict)
```

The contract defines:

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

## Boundary Summary

The future implementation is allowed to import only:

```text
standard library
codie.intelligence.evidence_inputs
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

Sensitive evidence refs are excluded by default. Blocking conflicts must remain
visible and must not be hidden by later answer builders.

## Validation

Documentation-only packet.

Static validation:

```text
git diff --check: PASS
Phase 18A strategic language scan: no matches
schema/repository drift scan: no matches
```

Full suite validation:

```text
Ran 566 tests in 3.192s

OK (skipped=1)
```

No tests were added because this packet adds no executable code.

## Next Packet

```text
Phase 18B - Source Conflict Report Implementation
```
