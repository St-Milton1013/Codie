# Phase 22 - LLM Writer/Auditor Planning Contract

## Objective

Plan the next dependency-safe Interactive Intelligence layer after Phase 21
Chat Answer Builder.

Phase 22 should define whether and how Codie may use an optional LLM writer and
separate LLM auditor over already-structured `ChatAnswer` payloads. The writer
may only transform structured evidence-backed answer sections into clearer
presentation text. The auditor must verify that the writer did not add claims,
recommendations, private data, or uncited facts.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, DB reads, file
writes, analytics calculation, card behavior implementation, recommendation
generation, or private-data export.

## Accepted Inputs

Phase 22 starts from these accepted foundations:

```text
Phase 20 chat query planner
Phase 21 chat answer builder
Phase 21 outside validation accepted by user
```

## Key Decision

Phase 22 should begin with:

```text
Phase 22A - LLM Writer/Auditor Boundary Contract
```

Do not start with:

```text
LLM API calls
chat UI
cloud provider wiring
prompt implementation
answer persistence
chat session persistence
DB/repository readers
source/provider table readers
raw provider payload adapters
simulator execution
card behavior implementation
analytics calculation
recommendation generation
deck construction instruction language
```

## Why This Lane

Codie now has:

```text
ChatQueryPlan
ChatAnswer
citations
caveats
missing_evidence
blockers
```

The next risk is natural-language presentation. If an LLM is eventually used,
it must be constrained to presentation over already-built evidence. It must not
become source truth, retrieval, recommendation logic, or a private-data leak.

The correct design is a two-part boundary:

```text
structured ChatAnswer -> writer draft -> auditor verdict -> accepted/rejected render text
```

The writer may improve readability. The auditor must compare draft language
against the structured `ChatAnswer` and reject unsupported additions.

## Phase 22 Direction

Build the next layer in this order:

```text
1. LLM Writer/Auditor boundary contract
2. Pure writer/auditor packet model implementation, with mock LLM outputs only
3. LLM Writer/Auditor checkpoint
4. Optional local/offline renderer contract
5. Optional real LLM provider contract, disabled by default
6. UI/API contract, only after local packet behavior is validated
```

## Recommended Phase 22A Scope

Phase 22A should define the contract for:

```text
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
```

Future implementation, after contract acceptance, should create:

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

## Future Public Interface

Future implementation should define:

```text
LLMWriterAuditorBuildError
LLMWriterInput
LLMWriterDraft
LLMAuditFinding
LLMAuditResult
LLMWriterAuditorOptions
build_writer_input_from_answer(...)
validate_writer_draft(...)
audit_writer_draft(...)
llm_writer_draft_to_dict(...)
llm_audit_result_to_dict(...)
```

## Allowed Inputs

The future layer may consume:

```text
ChatAnswer
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswerMissingEvidence
explicit user opt-in metadata
```

The future layer must not consume:

```text
raw deck text
raw provider payloads
full primer bodies
source tables
provider APIs
SQLite connections
simulator traces except summarized reviewed records
```

## Writer Rules

The future writer may:

```text
rephrase structured answer sections for readability
preserve section order
preserve citations
preserve caveats
preserve missing_evidence
preserve uncertainty language
```

The future writer must not:

```text
add new factual claims
remove caveats
hide missing evidence
hide unsupported cards
hide source conflicts
change citation meaning
generate recommendations
write deck-construction instructions
```

## Auditor Rules

The future auditor must check:

```text
every factual draft claim maps to a ChatAnswer section/citation
all caveats remain visible
all missing_evidence remains visible
all blockers remain visible
no forbidden strategic language appears
no private/raw metadata appears
no unsupported cards are treated as modeled
no source conflicts are resolved by prose
no recommendations or deck-construction instructions are added
```

The auditor result should be:

```text
accepted
rejected
needs_manual_review
```

## Privacy Rules

Phase 22A must require explicit handling for cloud LLM use:

```text
cloud LLM use is disabled by default
private user deck data is excluded by default
local_user_data requires explicit opt-in
sensitive scope is never sent by default
raw_input is never sent
private_deck_text is never sent
full_primer_body is never sent
raw_provider_payload is never sent
provider_payload is never sent
original_import_text is never sent
```

The Phase 22B implementation, if built, should use mock writer drafts only and
must not call any real LLM.

## Forbidden Language

Future writer drafts and audit-accepted output must reject:

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

## Dependency Rules

Phase 22A future implementation may import:

```text
standard library
codie.intelligence.answer_builder
codie.intelligence.query_planner
```

Phase 22A future implementation must not import:

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
openai
anthropic
```

## Recommended Tests For Phase 22B

Future implementation should test:

```text
writer input is built only from structured ChatAnswer fields
writer input preserves citations
writer input preserves caveats
writer input preserves missing_evidence
mock writer draft with supported wording is accepted
mock writer draft adding uncited claim is rejected
mock writer draft hiding caveat is rejected
mock writer draft hiding missing_evidence is rejected
mock writer draft using forbidden strategic language is rejected
private metadata keys fail cleanly
nested private metadata keys fail cleanly
cloud/provider imports are absent
no live LLM calls exist
serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM SDK imports
```

## Completion Criteria For Phase 22 Planning

Phase 22 planning is complete when:

```text
Phase 22 planning contract exists
Phase 22 planning report exists
NEXT_PHASE_CONTRACT points to Phase 22A
CODEX_CONTINUITY_HANDOFF points to Phase 22A
No implementation code was added
No schema changes were made
No LLM calls were added
```
