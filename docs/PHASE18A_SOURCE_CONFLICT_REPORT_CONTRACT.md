# Phase 18A - Source Conflict Report Contract

## Objective

Define a pure source conflict report layer for already-sanitized evidence
records.

Source conflict reports should preserve disagreement, uncertainty, redaction,
staleness, missing evidence, and unsupported behavior as structured data before
any chat UI, LLM phrasing, persistence, or recommendation generation exists.

This is a contract packet. It adds no implementation code.

## Future Files

Future implementation should create:

```text
codie/intelligence/source_conflicts.py
tests/test_intelligence_source_conflicts.py
docs/PHASE18B_SOURCE_CONFLICT_REPORT_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

Future implementation should define:

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

## SourceConflictEvidenceRef

Required fields:

```text
evidence_id
source_type
source_name
source_record_id
source_url
observed_at
field_name
field_value
privacy_scope
metadata
```

Rules:

```text
evidence_id is required
source_type is required
source_name is required
observed_at is required
source_record_id or source_url is required
field_name is required
field_value must be JSON-compatible
privacy_scope must be valid
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## SourceConflictItem

Required fields:

```text
conflict_id
conflict_type
summary
severity
evidence_refs
resolution_status
caveats
metadata
```

Allowed `conflict_type` values:

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

Allowed `severity` values:

```text
info
warning
blocking
```

Allowed `resolution_status` values:

```text
unresolved
needs_review
resolved_externally
ignored_by_policy
```

Rules:

```text
conflict_id is required
conflict_type is required
summary is required
severity is required
at least one evidence_ref is required
blocking conflicts must be preserved
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## SourceConflictReport

Required fields:

```text
report_id
subject_type
subject_id
generated_at
conflicts
metadata
```

Rules:

```text
report_id is required
subject_type is required
subject_id is required
generated_at is required
conflicts must not be empty
conflict IDs must be unique
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## SourceConflictReportOptions

Suggested fields:

```text
include_info
include_resolved
include_sensitive
minimum_severity
```

Default behavior:

```text
include_info = true
include_resolved = false
include_sensitive = false
minimum_severity = info
```

Rules:

```text
sensitive evidence is excluded unless include_sensitive is true
resolved_externally and ignored_by_policy conflicts are excluded unless include_resolved is true
filtered conflicts must be represented by caveats when omission changes interpretation
```

## Conversion To Evidence Inputs

`source_conflict_report_to_input_records(...)` should emit
`EvidenceInputRecord` values with:

```text
record_type = source_conflict
privacy_scope = highest privacy scope among included evidence refs
references = EvidenceRecordRef values derived from evidence refs
caveats = conflict caveats plus filtered-evidence caveats
metadata = conflict type, severity, resolution status, and sanitized field names
```

The conversion must not:

```text
choose a winner
canonicalize records
generate recommendations
create strategic claims
```

## Privacy Rules

The source conflict layer must reject metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances.

Sensitive evidence refs are excluded by default. If a conflict would be changed
by exclusion, the report must retain a caveat or metadata count showing that
evidence was filtered.

## Dependency Rules

Future implementation may import:

```text
standard library
codie.intelligence.evidence_inputs
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

Future implementation should raise `SourceConflictBuildError` for:

```text
missing report_id
missing subject_id
empty conflicts
duplicate conflict_id
unsupported conflict_type
unsupported severity
unsupported resolution_status
conflict missing evidence_refs
evidence ref missing source_name
evidence ref missing observed_at
evidence ref missing both source_record_id and source_url
metadata not JSON-compatible
private/raw metadata key present
filtered report with no remaining conflicts
forbidden strategic language
```

## Required Tests For Phase 18B

```text
valid conflict report serializes deterministically
valid conflict report converts to EvidenceInputRecord values
conflict type is preserved in metadata
severity is preserved in metadata
resolution status is preserved in metadata
references map to EvidenceRecordRef values
blocking conflicts are preserved
resolved conflicts excluded by default
resolved conflicts included only with option
sensitive evidence excluded by default
sensitive evidence included only with option
filtered evidence creates caveat or count
duplicate conflict IDs fail cleanly
unsupported conflict type fails cleanly
unsupported severity fails cleanly
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
conversion emits record_type source_conflict
module has no forbidden imports
module has no raw SQL
module has no file-writing behavior
full suite passes
```

## Do Not Do In Phase 18A

```text
do not implement source conflict code
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
Phase 18B - Source Conflict Report Implementation
```
