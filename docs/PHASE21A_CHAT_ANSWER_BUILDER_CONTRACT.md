# Phase 21A - Chat Answer Builder Contract

## Objective

Define a pure Chat Answer Builder for converting an accepted `ChatQueryPlan`
and already-sanitized evidence inputs into a deterministic, structured,
citation-bearing `ChatAnswer`.

The answer builder must be evidence-first. It must not retrieve data, call an
LLM, query SQLite, call providers, run simulator logic, calculate analytics,
generate recommendations, persist chat records, write files, or emit
deck-construction instructions.

This is a contract packet. It adds no implementation code.

## Future Files

Future implementation should create:

```text
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

Future implementation should define:

```text
ChatAnswerBuildError
ChatAnswerInput
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswerMissingEvidence
ChatAnswer
ChatAnswerBuilderOptions
build_chat_answer(...)
chat_answer_to_dict(...)
```

## ChatAnswerInput

Required fields:

```text
answer_input_id
plan
evidence_records
evidence_graph
source_conflict_report
unsupported_card_queue
context_summaries
generated_at
metadata
```

Rules:

```text
answer_input_id is required
plan must be a ChatQueryPlan
evidence_records must be already sanitized
evidence_graph is optional and must be already built
source_conflict_report is optional and must be already built
unsupported_card_queue is optional and must be already built
context_summaries must be JSON-compatible
generated_at is required
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

The answer builder may inspect these objects but must not fetch, hydrate, or
persist them.

## ChatAnswerSection

Required fields:

```text
section_id
section_type
title
statements
citation_ids
caveat_ids
missing_evidence_ids
metadata
```

Allowed `section_type` values:

```text
summary
evidence
comparison
conflict
unsupported_cards
simulation
tag_graph
missing_evidence
caveat
unknown
```

Rules:

```text
section_id is required
section_type is required
title is required
statements must be evidence-descriptive strings
factual sections must have citation_ids or missing_evidence_ids
unknown sections may omit citation_ids only when caveated
metadata must be JSON-compatible
private/raw metadata keys are forbidden
forbidden strategic language is rejected
```

Sections are renderable structures, not unconstrained chat prose.

## ChatAnswerCitation

Required fields:

```text
citation_id
source_type
source_id
source_label
source_url
record_type
confidence
generated_at
metadata
```

Allowed `source_type` values:

```text
evidence_input_record
evidence_graph_node
evidence_graph_edge
source_conflict
unsupported_card
deck_memory
saved_analysis
simulation_review
frequency_pool
tag_graph
manual_note
```

Rules:

```text
citation_id is required
source_type is required
source_id is required
record_type is required
confidence must be between 0.0 and 1.0
generated_at is required
source_url may be null
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatAnswerCaveat

Required fields:

```text
caveat_id
caveat_type
message
severity
metadata
```

Allowed `caveat_type` values:

```text
low_evidence
missing_evidence
unsupported_card
source_conflict
privacy_scope
unknown_question
unavailable_input
low_confidence
manual_review_required
```

Allowed `severity` values:

```text
info
warning
blocking
```

Rules:

```text
caveat_id is required
caveat_type is required
message is required
severity is required
metadata must be JSON-compatible
private/raw metadata keys are forbidden
forbidden strategic language is rejected
```

## ChatAnswerMissingEvidence

Required fields:

```text
missing_evidence_id
need_id
need_type
reason
required
metadata
```

Rules:

```text
missing_evidence_id is required
need_id is required
need_type is required
reason is required
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

Missing evidence is an explicit output, not a reason to invent claims.

## ChatAnswer

Required fields:

```text
answer_id
request_id
plan_id
answer_mode
sections
citations
caveats
blockers
missing_evidence
privacy_scope
generated_at
metadata
```

Allowed `answer_mode` values:

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

Rules:

```text
answer_id is required
request_id must match the plan request_id
plan_id must match the plan plan_id
answer_mode must equal the plan question_class
sections must be deterministic
citations must be deterministic
caveats must include plan caveats when relevant
blockers must include plan blockers when relevant
missing_evidence must be explicit when required evidence is unavailable
privacy_scope must be valid
generated_at is required
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## ChatAnswerBuilderOptions

Required fields and defaults:

```text
maximum_sections = 8
maximum_citations = 24
maximum_statements_per_section = 8
require_citations_for_factual_sections = true
allow_unknown_without_evidence = true
```

Rules:

```text
maximum_sections must be at least 1
maximum_citations must be at least 1
maximum_statements_per_section must be at least 1
```

## build_chat_answer(...)

Future signature:

```python
def build_chat_answer(
    answer_input: ChatAnswerInput,
    options: ChatAnswerBuilderOptions | None = None,
) -> ChatAnswer: ...
```

Responsibilities:

```text
validate the input object
copy plan blockers into answer blockers
copy relevant plan caveats into answer caveats
derive answer_mode from plan.question_class
build sections from already-sanitized evidence inputs
attach citations to factual sections
emit missing_evidence for unavailable required evidence needs
emit caveated unknown answers for unknown plans
reject forbidden strategic language
serialize deterministically
```

Forbidden behavior:

```text
do not query SQLite
do not import repositories
do not call providers
do not read source/provider tables
do not read raw provider payloads
do not call LLMs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not persist answers
do not export private raw_input
```

## chat_answer_to_dict(...)

Future signature:

```python
def chat_answer_to_dict(answer: ChatAnswer) -> dict[str, object]: ...
```

Rules:

```text
output must be JSON-compatible
ordering must be deterministic
private/raw metadata keys must not appear
citations must remain visible
caveats must remain visible
missing_evidence must remain visible
```

## Evidence And Citation Rules

Every factual section must either:

```text
include at least one citation_id
or include at least one missing_evidence_id
```

The builder must fail cleanly if a factual section has neither.

Unknown answers may contain a caveated unknown section without citations, but
must not make confident factual claims.

## Missing Evidence Rules

For every required `ChatEvidenceNeed` in the plan, the future implementation
must either:

```text
use matching sanitized evidence
or emit a ChatAnswerMissingEvidence record
```

Missing required evidence should add a caveat.

Missing optional evidence may add an info caveat but should not block the
answer.

## Source Conflict And Unsupported Card Rules

When available in the input, source conflicts and unsupported-card queues must
remain visible as caveats or sections.

The answer builder must not:

```text
choose a winner between conflicting sources
resolve source conflicts
treat unsupported simulator cards as modeled
treat user review annotations as tournament evidence
```

## Evidence-First Language Rules

Allowed answer language is descriptive:

```text
This card appears in 3 cited evidence records.
This commander pool has 42 matching decks in the selected window.
The selected evidence has low coverage.
The simulator summary includes unsupported-card caveats.
No matching evidence was available for this question.
```

Forbidden answer language:

```text
you should play
you should cut
must include
correct card
strict upgrade
auto-include
recommended cut
recommended include
secretly optimal
breaks the format
```

Future tests should avoid literal forbidden phrases in production code. If
tests need rejection fixtures, they should construct the strings indirectly so
static scans remain meaningful.

## Privacy Rules

Future implementation must reject these keys anywhere in input metadata,
section metadata, citation metadata, caveat metadata, missing-evidence metadata,
or answer metadata:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances and common punctuation variants.

The answer builder must not embed original deck text, primer body text, raw
provider payloads, or raw simulator traces.

## Dependency Rules

Future implementation may import:

```text
standard library
codie.intelligence.query_planner
codie.intelligence.evidence_graph
codie.intelligence.evidence_inputs
codie.intelligence.source_conflicts
codie.intelligence.unsupported_cards
```

Future implementation must not import:

```text
codie.db
codie.providers
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
codie.probability_engine
codie.canonical
requests
httpx
sqlite3
```

## Required Tests For Phase 21B

Future implementation must add tests for:

```text
deck_summary plan builds cited answer sections
card_evidence plan builds cited answer sections
commander_evidence plan builds cited answer sections
comparison plan builds cited answer sections
source_conflict plan preserves conflict caveats
unsupported_card plan preserves unsupported-card warnings
simulation_review plan preserves simulator caveats without running simulator
unknown plan emits caveated unknown answer
missing required evidence creates missing_evidence entries
missing optional evidence creates non-blocking caveat
sections without citations fail unless explicitly marked as missing-evidence or unknown
plan blockers are preserved
plan caveats are preserved
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
answer serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM calls
```

## Static Scans For Phase 21B

Future implementation must pass:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\answer_builder.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\answer_builder.py
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py docs\PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
git diff --name-only -- codie\db\schema docs\SCHEMA_SPEC.md codie\db\repositories
```

Expected:

```text
no forbidden imports
no raw SQL
no production file writing
no source/provider table reads
private metadata scan matches only blocked-key constants/rejection logic
strategic-language scan has no production matches
no schema, repository, migration, or schema-spec drift
```

## Do Not Do In Phase 21B

```text
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

## Acceptance Criteria For Phase 21A

Phase 21A is complete when:

```text
contract document exists
contract report exists
public interface is defined
input/output models are defined
citation rules are defined
missing-evidence behavior is defined
privacy and forbidden-language rules are defined
Phase 21B required tests are listed
NEXT_PHASE_CONTRACT points to Phase 21B
CODEX_CONTINUITY_HANDOFF points to Phase 21B
no implementation code was added
no schema changes were made
```
