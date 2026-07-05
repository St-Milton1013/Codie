# Phase 20A - Chat Query Planner Contract

## Objective

Define a pure chat query planner for sanitized user questions and structured
context references.

The planner should transform a question request into a deterministic
`ChatQueryPlan` that future answer builders can consume. It must not answer the
question.

This is a contract packet. It adds no implementation code.

## Future Files

Future implementation should create:

```text
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

Future implementation should define:

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

## ChatQueryRequest

Required fields:

```text
request_id
question_text
generated_at
subject
constraints
allowed_privacy_scopes
metadata
```

Rules:

```text
request_id is required
question_text is required
generated_at is required
subject may be unknown but must be explicit
constraints must be JSON-compatible
allowed_privacy_scopes must contain valid privacy scopes
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatQuerySubject

Required fields:

```text
subject_type
subject_key
display_name
metadata
```

Allowed `subject_type` values:

```text
deck
saved_deck
commander
partner_pair
card
package
simulation_result
source_conflict
unsupported_card
tag_graph
unknown
```

Rules:

```text
subject_type is required
subject_key is optional only when subject_type is unknown
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatEvidenceNeed

Required fields:

```text
need_id
need_type
reason
required
privacy_scope
record_types
filters
metadata
```

Allowed `need_type` values:

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

Rules:

```text
need_id is required
need_type is required
reason is required
privacy_scope must be valid
record_types must be deterministic
filters must be JSON-compatible
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatQueryConstraint

Required fields:

```text
constraint_id
constraint_type
value
required
metadata
```

Suggested `constraint_type` values:

```text
commander
partner_pair
deck_hash
card_name
oracle_id
scryfall_id
date_range
region
provider
placement_scope
privacy_scope
selected_tags
minimum_confidence
maximum_results
```

Rules:

```text
constraint_id is required
constraint_type is required
value must be JSON-compatible
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatQueryPlan

Required fields:

```text
plan_id
request_id
question_class
subject
evidence_needs
constraints
blockers
caveats
allowed_operations
generated_at
metadata
```

Allowed `question_class` values:

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

Allowed operations:

```text
build_evidence_graph
assemble_evidence_inputs
inspect_source_conflicts
inspect_unsupported_cards
inspect_deck_memory
inspect_saved_analysis
inspect_simulation_review
inspect_primer_metadata
inspect_innovation_signal
inspect_frequency_pool
inspect_tag_graph
return_caveated_unknown
```

Rules:

```text
plan_id is required
request_id is required
question_class is required
evidence_needs must not be empty unless question_class is unknown
required blockers must be preserved
caveats must be JSON-compatible
allowed_operations must be deterministic
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatQueryPlannerOptions

Suggested fields:

```text
default_privacy_scope
allow_sensitive
allow_local_user_data
maximum_evidence_needs
maximum_constraints
```

Default behavior:

```text
default_privacy_scope = public
allow_sensitive = false
allow_local_user_data = false
maximum_evidence_needs = 8
maximum_constraints = 12
```

## Planning Behavior

`build_chat_query_plan(...)` should:

```text
validate sanitized request shape
classify question_class using deterministic keyword/rule matching
preserve explicit subject data
preserve explicit constraints
derive evidence_needs from question_class and subject_type
filter or block privacy scopes not allowed by options
emit blockers for unavailable subject or privacy scope
emit caveats for ambiguity
serialize deterministically
```

It must not:

```text
generate final answer text
call an LLM
query a database
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

The query planner must reject metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances.

The query planner may reference local user data only through subject keys,
record IDs, privacy scopes, and caveats. It must not embed original imported
deck text.

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

Future implementation should raise `ChatQueryPlanBuildError` for:

```text
missing request_id
missing question_text
missing generated_at
unsupported subject_type
unsupported question_class
unsupported evidence need type
unsupported allowed operation
invalid privacy scope
metadata not JSON-compatible
private/raw metadata key present
too many evidence needs
too many constraints
forbidden strategic language
```

## Required Tests For Phase 20B

```text
deck summary request creates deck_summary plan
card evidence request creates card_evidence plan
commander evidence request creates commander_evidence plan
comparison request creates comparison plan
source conflict request creates source_conflict plan
unsupported card request creates unsupported_card plan
simulation review request creates simulation_review plan
tag graph request creates tag_graph plan
unknown request creates caveated unknown plan
plans serialize deterministically
explicit constraints are preserved
privacy scopes are enforced
sensitive scope blocked by default
local_user_data scope blocked by default
private metadata keys fail cleanly
nested private metadata keys fail cleanly
too many evidence needs fail cleanly
too many constraints fail cleanly
forbidden strategic language fails cleanly
module has no forbidden imports
module has no raw SQL
module has no file-writing behavior
full suite passes
```

## Do Not Do In Phase 20A

```text
do not implement query planner code
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
Phase 20B - Chat Query Planner Implementation
```
