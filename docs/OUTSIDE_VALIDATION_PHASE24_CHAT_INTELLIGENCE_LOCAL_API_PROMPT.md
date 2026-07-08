# Outside Validation Prompt - Phase 24 Chat/Intelligence Local API

Validate Codie Phase 24 work against `CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 25.

## Files To Review

Documentation:

```text
docs/PHASE24A_CHAT_INTELLIGENCE_LOCAL_API_CONTRACT.md
docs/PHASE24A_CHAT_INTELLIGENCE_LOCAL_API_CONTRACT_REPORT.md
docs/PHASE24B_CHAT_INTELLIGENCE_LOCAL_API_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE24_CHAT_INTELLIGENCE_LOCAL_API_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Implementation:

```text
codie/intelligence/local_api.py
codie/intelligence/__init__.py
tests/test_intelligence_local_api.py
```

Related context:

```text
codie/intelligence/ui_api_boundary.py
codie/intelligence/query_planner.py
codie/intelligence/answer_builder.py
codie/intelligence/llm_writer_auditor.py
codie/intelligence/evidence_inputs.py
codie/intelligence/evidence_graph.py
codie/intelligence/source_conflicts.py
codie/intelligence/unsupported_cards.py
```

## Validation Tasks

Confirm:

```text
Phase 23 outside validation is treated as accepted input.
Phase 24A contract matches the implementation.
Phase 24B implements the declared public interface.
The implementation is pure and in-memory.
The implementation adds route specs only, not live routes.
The implementation adds no UI code.
The implementation adds no HTTP server.
The implementation imports no server framework.
The implementation imports no network client.
The implementation accepts only structured Phase 23 ChatUI packet objects.
Route specs are local-only.
Route specs reject remote URLs and non-local paths.
Route specs reject unsupported methods.
Request envelopes preserve route method and path.
Request envelopes enforce allowed client surfaces.
Response envelopes preserve citations.
Response envelopes preserve caveats.
Response envelopes preserve missing_evidence.
Response envelopes preserve blockers.
Error envelopes preserve structured error packet details.
Error envelopes reject stack traces by default.
local_user_data is blocked by default.
sensitive scope is blocked by default.
private metadata keys are rejected, including nested keys.
forbidden strategic language is rejected.
payload size limits are enforced.
serialization is deterministic.
The implementation does not call LLMs.
The implementation does not import LLM SDKs.
The implementation does not query SQLite or providers.
The implementation does not retrieve evidence itself.
The implementation does not generate recommendations.
```

Confirm these public objects exist:

```text
LocalAPIContractError
LocalAPIRouteSpec
LocalAPIRequestEnvelope
LocalAPIResponseEnvelope
LocalAPIErrorEnvelope
LocalAPIOptions
build_chat_route_spec(...)
build_local_api_request_envelope(...)
build_local_api_response_envelope(...)
build_local_api_error_envelope(...)
local_api_route_spec_to_dict(...)
local_api_request_envelope_to_dict(...)
local_api_response_envelope_to_dict(...)
local_api_error_envelope_to_dict(...)
```

Confirm schema discipline:

```text
Phase 24 adds no schema changes.
No tables, columns, indexes, migrations, or repository methods were added for local API packets.
Local API route and envelope packets remain in-memory only.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 707 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_intelligence_local_api -v
```

Confirm:

```text
Ran 17 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\intelligence\local_api.py tests\test_intelligence_local_api.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\local_api.py tests\test_intelligence_local_api.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\local_api.py
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\local_api.py tests\test_intelligence_local_api.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\local_api.py
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\local_api.py tests\test_intelligence_local_api.py docs\PHASE24B_CHAT_INTELLIGENCE_LOCAL_API_IMPLEMENTATION_REPORT.md docs\CHECKPOINT_PHASE24_CHAT_INTELLIGENCE_LOCAL_API_REPORT.md
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
no Phase 24 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
local_api.py imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, sqlite3, openai, anthropic, Flask, FastAPI, Uvicorn, or Starlette
local_api.py reads source/provider tables or payloads
local_api.py writes files
local_api.py calls LLMs
local_api.py imports LLM SDKs
local_api.py queries SQLite
local_api.py retrieves evidence itself
local_api.py runs simulator logic
local_api.py implements card behavior
local_api.py starts an HTTP server
local_api.py registers live routes
local_api.py opens network sockets
local_api.py adds UI code
local_api.py generates recommendation or deck-construction language
local_api.py persists request, response, or error envelopes
private metadata can escape into output
remote URL paths are accepted by default
non-local route specs are accepted by default
source conflicts are resolved instead of preserved
unsupported simulator cards are treated as modeled
hidden citations, caveats, missing_evidence, or blockers can pass response envelope construction
```

## Phase 25 Gate

Phase 25 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
