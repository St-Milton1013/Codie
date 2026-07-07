# Outside Validation Prompt - Phase 20 Chat Query Planner

Validate Codie Phase 20 work against `CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 21.

## Files To Review

Documentation:

```text
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_CONTRACT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_REPORT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE20_CHAT_QUERY_PLANNER_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Implementation:

```text
codie/intelligence/query_planner.py
codie/intelligence/__init__.py
tests/test_intelligence_query_planner.py
```

Related context:

```text
codie/intelligence/evidence_graph.py
codie/intelligence/evidence_inputs.py
codie/intelligence/source_conflicts.py
codie/intelligence/unsupported_cards.py
```

## Validation Tasks

Confirm:

```text
Phase 19 outside validation is treated as accepted input.
Phase 20 planning selects Chat Query Planner as the next layer.
Phase 20A contract matches the implementation.
Phase 20B implements the declared public interface.
The implementation is pure and in-memory.
The implementation accepts only sanitized user requests and structured context references.
The implementation emits deterministic ChatQueryPlan values.
The implementation does not answer questions.
The implementation does not call LLMs.
The implementation does not query SQLite or providers.
The implementation does not generate recommendations.
The implementation preserves subject and constraint data.
The implementation derives evidence needs from question class.
The implementation blocks sensitive scope by default.
The implementation blocks local_user_data scope by default.
The implementation emits caveats for unsupported/unknown questions.
Private metadata keys are rejected, including nested keys.
Forbidden strategic language is rejected.
```

Confirm these public objects exist:

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

Confirm schema discipline:

```text
Phase 20 adds no schema changes.
No tables, columns, indexes, migrations, or repository methods were added for chat query planning.
Chat query plans remain in-memory only.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 631 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_intelligence_query_planner -v
```

Confirm:

```text
Ran 20 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations\.generation|codie\.recommendations\.persistence|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\query_planner.py tests\test_intelligence_query_planner.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\query_planner.py tests\test_intelligence_query_planner.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\query_planner.py
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\query_planner.py tests\test_intelligence_query_planner.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\query_planner.py
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\query_planner.py tests\test_intelligence_query_planner.py docs\PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
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
no Phase 20 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
query_planner.py imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, or sqlite3
query_planner.py reads source/provider tables or payloads
query_planner.py writes files
query_planner.py calls LLMs
query_planner.py generates final answer text
query_planner.py runs simulator logic
query_planner.py implements card behavior
query_planner.py generates recommendation or deck-construction language
query_planner.py persists chat plans
private metadata can escape into output
sensitive or local_user_data scope can be used without explicit option
unknown questions produce confident answers instead of caveated unknown plans
```

## Phase 21 Gate

Phase 21 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
