# Phase 21 - Chat Answer Builder Planning Contract

## Objective

Plan the next dependency-safe Interactive Intelligence layer after Phase 20
Chat Query Planner.

Phase 21 should define how Codie turns an accepted `ChatQueryPlan` plus
already-sanitized evidence inputs into a structured, citation-bearing answer
object. It must stay evidence-first and must not become an LLM, UI, database,
retrieval, simulator, analytics, or recommendation layer.

This is a planning packet. It adds no implementation code, schema, UI, LLM
calls, provider access, source-table reads, simulator execution, DB reads, file
writes, analytics calculation, card behavior implementation, or recommendation
generation.

## Accepted Inputs

Phase 21 starts from these accepted foundations:

```text
Phase 16 evidence graph
Phase 17 evidence graph input assembly
Phase 18 source conflict report
Phase 19 unsupported relevant card queue
Phase 20 chat query planner
Phase 20 outside validation accepted by user
```

## Key Decision

Phase 21 should begin with:

```text
Phase 21A - Chat Answer Builder Contract
```

Do not start with:

```text
chat UI
LLM calls
cloud writer/auditor workflows
answer persistence
chat session persistence
DB/repository readers
source/provider table readers
raw provider payload adapters
simulator execution
card behavior implementation
recommendation generation
deck construction instruction language
```

## Why This Lane

Codie now has a deterministic query planner:

```text
sanitized user question -> ChatQueryPlan
```

The next safe layer is a pure answer builder that consumes the plan and
already-sanitized evidence records to create a structured answer payload.

The answer builder should determine:

```text
what evidence was available
what evidence was missing
what caveats must be shown
what citations support each statement
what unsupported-card or source-conflict warnings apply
what answer sections are safe to render
```

It should not retrieve evidence, write prose through an LLM, query databases,
call tools, run simulators, or create recommendation instructions.

## Phase 21 Direction

Build the next layer in this order:

```text
1. Chat Answer Builder contract
2. Chat Answer Builder implementation
3. Chat Answer Builder checkpoint
4. Optional LLM writer/auditor contract
5. UI/API contract
6. Chat/session persistence contract, only if a real retention need exists
```

## Recommended Phase 21A Scope

Phase 21A should define a pure answer builder module:

```text
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
```

The future implementation should define:

```text
ChatAnswerBuildError
ChatAnswerInput
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswer
ChatAnswerBuilderOptions
build_chat_answer(...)
chat_answer_to_dict(...)
```

## Supported Answer Modes

Suggested allowed answer modes:

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

The answer mode should be derived from the `ChatQueryPlan.question_class`.

## Input Sources

Future implementation may consume already-built, sanitized objects such as:

```text
ChatQueryPlan
EvidenceInputRecord
EvidenceGraph
SourceConflictReport
UnsupportedCardQueue
deck memory summaries
saved analysis summaries
simulation review summaries
tag graph summaries
frequency pool summaries
```

It must not fetch or build those inputs itself.

## Output Shape

The future answer object should expose:

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

Sections should be structured and renderable, not free-form chat blobs.

## Citation Rules

Every factual answer section must cite at least one evidence item or explicitly
state that evidence is missing.

Citations should include:

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

Private/raw metadata keys are forbidden in citation metadata.

## Evidence-First Language Rules

Allowed wording should be evidence-descriptive:

```text
This card appears in 3 cited evidence records.
This commander pool shows 42 matching decks in the selected window.
The selected evidence has low coverage.
The simulator summary includes unsupported-card caveats.
No matching evidence was available for this question.
```

Forbidden wording remains:

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

## Unknown And Missing Evidence Rules

If the plan is `unknown`, the answer builder should produce a caveated unknown
answer with no confident claims.

If required evidence is missing, the answer builder should produce:

```text
missing_evidence entries
caveats
no unsupported strategic conclusion
```

## Privacy Rules

Future implementation must reject answer input metadata keys:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances.

Private user-deck context must be represented by privacy scope and references,
not by embedding original deck text.

## Dependency Rules

Phase 21A future implementation may import:

```text
standard library
codie.intelligence.query_planner
codie.intelligence.evidence_graph
codie.intelligence.evidence_inputs
codie.intelligence.source_conflicts
codie.intelligence.unsupported_cards
```

Phase 21A future implementation must not import:

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

## Recommended Tests For Phase 21B

Future implementation should test:

```text
deck_summary plan builds cited answer sections
card_evidence plan builds cited answer sections
source_conflict plan preserves conflict caveats
unsupported_card plan preserves unsupported-card warnings
unknown plan emits caveated unknown answer
missing required evidence creates missing_evidence entries
sections without citations fail unless explicitly marked as missing-evidence
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
answer serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM calls
```

## Completion Criteria For Phase 21 Planning

Phase 21 planning is complete when:

```text
Phase 21 planning contract exists
Phase 21 planning report exists
NEXT_PHASE_CONTRACT points to Phase 21A
CODEX_CONTINUITY_HANDOFF points to Phase 21A
No implementation code was added
No schema changes were made
```
