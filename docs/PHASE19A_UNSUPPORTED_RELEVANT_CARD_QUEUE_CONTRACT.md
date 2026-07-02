# Phase 19A - Unsupported Relevant Card Queue Contract

## Objective

Define a pure unsupported relevant card queue layer for already-sanitized
evidence records.

The queue should preserve unresolved cards, unsupported simulator behaviors,
modeling gaps, rules-text gaps, privacy redactions, source-conflict card gaps,
and manual-review needs as structured data before any chat UI, LLM phrasing,
persistence, card behavior implementation, or recommendation generation exists.

This is a contract packet. It adds no implementation code.

## Future Files

Future implementation should create:

```text
codie/intelligence/unsupported_cards.py
tests/test_intelligence_unsupported_cards.py
docs/PHASE19B_UNSUPPORTED_RELEVANT_CARD_QUEUE_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

Future implementation should define:

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

## UnsupportedCardEvidenceRef

Required fields:

```text
evidence_id
source_type
source_name
source_record_id
source_url
observed_at
card_name
oracle_id
scryfall_id
context
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
card_name is required
oracle_id and scryfall_id are optional
context must be JSON-compatible
privacy_scope must be valid
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## UnsupportedCardQueueItem

Required fields:

```text
item_id
card_name
oracle_id
scryfall_id
reason
severity
status
evidence_refs
first_seen_at
last_seen_at
caveats
metadata
```

Allowed `reason` values:

```text
simulator_unsupported
card_lookup_unresolved
model_gap
rules_text_gap
source_conflict
privacy_redaction
manual_review_required
```

Allowed `severity` values:

```text
info
warning
blocking
```

Allowed `status` values:

```text
open
in_review
resolved
ignored_by_policy
```

Rules:

```text
item_id is required
card_name is required
reason is required
severity is required
status is required
at least one evidence_ref is required
blocking items must be preserved
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## UnsupportedCardQueue

Required fields:

```text
queue_id
subject_type
subject_id
generated_at
items
metadata
```

Rules:

```text
queue_id is required
subject_type is required
subject_id is required
generated_at is required
items must not be empty
item IDs must be unique
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## UnsupportedCardQueueOptions

Suggested fields:

```text
include_resolved
include_sensitive
minimum_severity
deduplicate_by
```

Default behavior:

```text
include_resolved = false
include_sensitive = false
minimum_severity = info
deduplicate_by = card_identity
```

Rules:

```text
sensitive evidence is excluded unless include_sensitive is true
resolved and ignored_by_policy items are excluded unless include_resolved is true
filtered items must be represented by caveats when omission changes interpretation
deduplication must be deterministic
```

## Conversion To Evidence Inputs

`unsupported_card_queue_to_input_records(...)` should emit
`EvidenceInputRecord` values with:

```text
record_type = unsupported_card
privacy_scope = highest privacy scope among included evidence refs
references = EvidenceRecordRef values derived from evidence refs
caveats = item caveats plus filtered-evidence caveats
metadata = reason, severity, status, card identity fields, and sanitized context
```

The conversion must not:

```text
implement card behavior
run simulator logic
choose deck construction actions
canonicalize records
generate recommendations
create strategic claims
```

## Privacy Rules

The unsupported card queue layer must reject metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances.

Sensitive evidence refs are excluded by default. If an item would be changed by
exclusion, the queue must retain a caveat or metadata count showing that
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

Future implementation should raise `UnsupportedCardQueueBuildError` for:

```text
missing queue_id
missing subject_id
empty items
duplicate item_id
unsupported reason
unsupported severity
unsupported status
item missing evidence_refs
evidence ref missing card_name
evidence ref missing source_name
evidence ref missing observed_at
evidence ref missing both source_record_id and source_url
metadata not JSON-compatible
private/raw metadata key present
filtered queue with no remaining items
forbidden strategic language
```

## Required Tests For Phase 19B

```text
valid queue serializes deterministically
valid queue converts to EvidenceInputRecord values
reason is preserved in metadata
severity is preserved in metadata
status is preserved in metadata
card identity fields are preserved in metadata
references map to EvidenceRecordRef values
blocking items are preserved
resolved items excluded by default
resolved items included only with option
sensitive evidence excluded by default
sensitive evidence included only with option
filtered evidence creates caveat or count
duplicate item IDs fail cleanly
unsupported reason fails cleanly
unsupported severity fails cleanly
unsupported status fails cleanly
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
conversion emits record_type unsupported_card
module has no forbidden imports
module has no raw SQL
module has no file-writing behavior
full suite passes
```

## Do Not Do In Phase 19A

```text
do not implement unsupported-card queue code
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call LLMs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Recommended Next Packet

```text
Phase 19B - Unsupported Relevant Card Queue Implementation
```
