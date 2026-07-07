# Outside Validation Prompt - Phase 21 Chat Answer Builder

Validate Codie Phase 21 work against `CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 22.

## Files To Review

Documentation:

```text
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_CONTRACT.md
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_REPORT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE21_CHAT_ANSWER_BUILDER_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Implementation:

```text
codie/intelligence/answer_builder.py
codie/intelligence/__init__.py
tests/test_intelligence_answer_builder.py
```

Related context:

```text
codie/intelligence/query_planner.py
codie/intelligence/evidence_graph.py
codie/intelligence/evidence_inputs.py
codie/intelligence/source_conflicts.py
codie/intelligence/unsupported_cards.py
```

## Validation Tasks

Confirm:

```text
Phase 20 outside validation is treated as accepted input.
Phase 21 planning selects Chat Answer Builder as the next layer.
Phase 21A contract matches the implementation.
Phase 21B implements the declared public interface.
The implementation is pure and in-memory.
The implementation accepts only ChatQueryPlan values and already-sanitized evidence inputs.
The implementation emits deterministic ChatAnswer values.
The implementation does not retrieve evidence itself.
The implementation does not call LLMs.
The implementation does not query SQLite or providers.
The implementation does not generate recommendations.
The implementation preserves plan blockers and caveats.
The implementation requires citations or missing_evidence for factual sections.
Structured ChatAnswer sections are allowed only when backed by citations, missing_evidence, or caveated unknown status.
The implementation emits missing_evidence for unavailable required evidence.
The implementation creates non-blocking caveats for unavailable optional evidence.
The implementation preserves source-conflict caveats.
The implementation preserves unsupported-card caveats.
The implementation preserves simulator caveats without running simulator logic.
The implementation emits caveated unknown answers for unknown plans.
Private metadata keys are rejected, including nested keys.
Forbidden strategic language is rejected.
```

Confirm these public objects exist:

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

Confirm schema discipline:

```text
Phase 21 adds no schema changes.
No tables, columns, indexes, migrations, or repository methods were added for chat answer building.
Chat answers remain in-memory only.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 651 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_intelligence_answer_builder -v
```

Confirm:

```text
Ran 18 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\answer_builder.py
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\answer_builder.py
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\answer_builder.py tests\test_intelligence_answer_builder.py docs\PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
```

Expected:

```text
no matches
```

Run:

```powershell
git diff --name-only -- codie\db\schema docs\SCHEMA_SPEC.md codie\db\repositories
```

Expected:

```text
no Phase 21 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
answer_builder.py imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, or sqlite3
answer_builder.py reads source/provider tables or payloads
answer_builder.py writes files
answer_builder.py calls LLMs
answer_builder.py queries SQLite
answer_builder.py retrieves evidence itself
answer_builder.py runs simulator logic
answer_builder.py implements card behavior
answer_builder.py generates unconstrained final prose outside the structured ChatAnswer model
answer_builder.py invents facts not backed by citations or missing_evidence
answer_builder.py generates recommendation or deck-construction language
answer_builder.py persists chat answers
factual sections can be emitted without citations or missing_evidence
private metadata can escape into output
source conflicts are resolved instead of preserved as caveats
unsupported simulator cards are treated as modeled
unknown questions produce confident answers instead of caveated unknown answers
```

## Phase 22 Gate

Phase 22 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
