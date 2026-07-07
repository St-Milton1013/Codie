# Phase 22A - LLM Writer/Auditor Boundary Contract

## Objective

Define the boundary for an optional LLM writer and separate auditor over
already-structured `ChatAnswer` payloads.

The writer/auditor layer may only work from structured `ChatAnswer` fields. It
must not retrieve data, call live LLM APIs, query SQLite, call providers, run
simulator logic, calculate analytics, generate recommendations, persist chat
records, write files, or expose private/raw input data.

This is a contract packet. It adds no implementation code.

## Future Files

Future implementation should create:

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Classes And Functions

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
llm_writer_input_to_dict(...)
llm_writer_draft_to_dict(...)
llm_audit_result_to_dict(...)
```

## LLMWriterInput

Required fields:

```text
writer_input_id
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

Rules:

```text
writer_input_id is required
answer_id is required
request_id is required
plan_id is required
answer_mode must match the source ChatAnswer
sections must be derived from ChatAnswer sections
citations must be derived from ChatAnswer citations
caveats must be derived from ChatAnswer caveats
blockers must be derived from ChatAnswer blockers
missing_evidence must be derived from ChatAnswer missing_evidence
privacy_scope must be valid
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

The writer input is a sanitized presentation packet. It is not a retrieval
request and must not contain original deck text, raw provider payloads, full
primer bodies, or raw simulator traces.

## LLMWriterDraft

Required fields:

```text
draft_id
writer_input_id
answer_id
sections
citation_ids
caveat_ids
missing_evidence_ids
generated_at
metadata
```

Rules:

```text
draft_id is required
writer_input_id is required
answer_id is required
sections must be structured render sections, not unconstrained chat logs
citation_ids must reference writer input citations
caveat_ids must reference writer input caveats
missing_evidence_ids must reference writer input missing_evidence
generated_at is required
metadata must be JSON-compatible
private/raw metadata keys are forbidden
forbidden strategic language is rejected
```

Phase 22B should use mock writer drafts only. It must not call real LLM APIs.

## LLMAuditFinding

Required fields:

```text
finding_id
finding_type
severity
message
section_id
citation_ids
metadata
```

Allowed `finding_type` values:

```text
uncited_claim
missing_citation
hidden_caveat
hidden_missing_evidence
hidden_blocker
private_data
forbidden_language
unsupported_card_treated_as_modeled
source_conflict_resolved
recommendation_language
metadata_violation
structure_violation
```

Allowed `severity` values:

```text
info
warning
blocking
```

Rules:

```text
finding_id is required
finding_type is required
severity is required
message is required
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## LLMAuditResult

Required fields:

```text
audit_id
draft_id
writer_input_id
answer_id
verdict
findings
accepted_section_ids
rejected_section_ids
generated_at
metadata
```

Allowed `verdict` values:

```text
accepted
rejected
needs_manual_review
```

Rules:

```text
audit_id is required
draft_id is required
writer_input_id is required
answer_id is required
blocking findings require rejected verdict
warning findings require rejected or needs_manual_review verdict unless explicitly non-blocking
accepted verdict requires no blocking or warning findings
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## LLMWriterAuditorOptions

Required fields and defaults:

```text
allow_cloud_llm = false
allow_local_user_data = false
allow_sensitive = false
maximum_sections = 8
maximum_draft_statements = 24
require_all_citations_visible = true
require_all_caveats_visible = true
require_all_missing_evidence_visible = true
require_all_blockers_visible = true
```

Rules:

```text
maximum_sections must be at least 1
maximum_draft_statements must be at least 1
allow_cloud_llm must default false
allow_sensitive must default false
```

## build_writer_input_from_answer(...)

Future signature:

```python
def build_writer_input_from_answer(
    answer: ChatAnswer,
    options: LLMWriterAuditorOptions | None = None,
) -> LLMWriterInput: ...
```

Responsibilities:

```text
validate source ChatAnswer
copy only structured answer fields
preserve citations
preserve caveats
preserve missing_evidence
preserve blockers
preserve privacy_scope
reject sensitive scope unless explicitly allowed
reject local_user_data scope unless explicitly allowed
reject private/raw metadata
serialize deterministically
```

Forbidden behavior:

```text
do not call LLM APIs
do not query SQLite
do not import repositories
do not call providers
do not read source/provider tables
do not read raw provider payloads
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not persist writer inputs
do not export private raw_input
```

## validate_writer_draft(...)

Future signature:

```python
def validate_writer_draft(
    draft: LLMWriterDraft,
    writer_input: LLMWriterInput,
    options: LLMWriterAuditorOptions | None = None,
) -> LLMWriterDraft: ...
```

Responsibilities:

```text
validate draft structure
confirm cited IDs exist in writer input
confirm caveat IDs exist in writer input
confirm missing_evidence IDs exist in writer input
reject private/raw metadata
reject forbidden strategic language
reject excessive section or statement counts
```

Validation is structural. It does not accept the draft as faithful; that is the
auditor's job.

## audit_writer_draft(...)

Future signature:

```python
def audit_writer_draft(
    draft: LLMWriterDraft,
    writer_input: LLMWriterInput,
    options: LLMWriterAuditorOptions | None = None,
) -> LLMAuditResult: ...
```

Responsibilities:

```text
verify citations remain visible
verify caveats remain visible
verify missing_evidence remains visible
verify blockers remain visible
reject uncited factual additions
reject hidden caveats
reject hidden missing evidence
reject hidden blockers
reject private/raw metadata
reject forbidden strategic language
reject treating unsupported cards as modeled
reject resolving source conflicts in prose
reject recommendation or deck-construction language
```

The audit result is an annotation over the draft. It must not mutate the source
`ChatAnswer`, writer input, or draft.

## Serialization Functions

Future signatures:

```python
def llm_writer_input_to_dict(writer_input: LLMWriterInput) -> dict[str, object]: ...
def llm_writer_draft_to_dict(draft: LLMWriterDraft) -> dict[str, object]: ...
def llm_audit_result_to_dict(result: LLMAuditResult) -> dict[str, object]: ...
```

Rules:

```text
output must be JSON-compatible
ordering must be deterministic
private/raw metadata keys must not appear
citations must remain visible
caveats must remain visible
missing_evidence must remain visible
blockers must remain visible
```

## Writer Rules

The future writer may:

```text
rephrase structured answer sections for readability
preserve section order
preserve citations
preserve caveats
preserve missing_evidence
preserve blockers
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

The future auditor must reject or flag:

```text
uncited factual additions
missing citation visibility
hidden caveats
hidden missing_evidence
hidden blockers
private/raw metadata
forbidden strategic language
unsupported cards treated as modeled
source conflicts resolved by prose
recommendation or deck-construction language
structure violations
```

## Privacy Rules

Cloud LLM use must remain disabled by default.

The future implementation must reject these keys anywhere in writer input,
drafts, audit findings, audit results, or metadata:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances and common punctuation variants.

The writer/auditor layer must not embed original deck text, primer body text,
raw provider payloads, or raw simulator traces.

## Forbidden Language

Writer drafts and accepted audit results must reject:

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

## Dependency Rules

Future implementation may import:

```text
standard library
codie.intelligence.answer_builder
codie.intelligence.query_planner
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
openai
anthropic
```

## Required Tests For Phase 22B

Future implementation must add tests for:

```text
writer input is built only from structured ChatAnswer fields
writer input preserves citations
writer input preserves caveats
writer input preserves missing_evidence
writer input preserves blockers
local_user_data is blocked by default
sensitive scope is blocked by default
mock writer draft with supported wording validates
mock writer draft adding uncited claim is rejected by audit
mock writer draft hiding caveat is rejected by audit
mock writer draft hiding missing_evidence is rejected by audit
mock writer draft hiding blocker is rejected by audit
mock writer draft using forbidden strategic language is rejected
mock writer draft treating unsupported card as modeled is rejected
mock writer draft resolving source conflict is rejected
private metadata keys fail cleanly
nested private metadata keys fail cleanly
cloud/provider imports are absent
no live LLM calls exist
serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM SDK imports
```

## Static Scans For Phase 22B

Future implementation must pass:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\llm_writer_auditor.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\llm_writer_auditor.py
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py docs\PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
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

## Do Not Do In Phase 22B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not call real LLM APIs
do not import LLM SDKs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Acceptance Criteria For Phase 22A

Phase 22A is complete when:

```text
contract document exists
contract report exists
public interface is defined
input/draft/audit models are defined
writer rules are defined
auditor rules are defined
privacy and forbidden-language rules are defined
Phase 22B required tests are listed
NEXT_PHASE_CONTRACT points to Phase 22B
CODEX_CONTINUITY_HANDOFF points to Phase 22B
no implementation code was added
no schema changes were made
no LLM calls were added
```
