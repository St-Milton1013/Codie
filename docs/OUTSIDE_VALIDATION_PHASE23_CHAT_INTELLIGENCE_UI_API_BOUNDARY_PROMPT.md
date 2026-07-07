# Outside Validation Prompt - Phase 23 Chat/Intelligence UI/API Boundary

Validate Codie Phase 23 work against `CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 24.

## Files To Review

Documentation:

```text
docs/PHASE23A_CHAT_INTELLIGENCE_UI_API_BOUNDARY_CONTRACT.md
docs/PHASE23A_CHAT_INTELLIGENCE_UI_API_BOUNDARY_CONTRACT_REPORT.md
docs/PHASE23B_CHAT_INTELLIGENCE_UI_API_BOUNDARY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE23_CHAT_INTELLIGENCE_UI_API_BOUNDARY_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Implementation:

```text
codie/intelligence/ui_api_boundary.py
codie/intelligence/__init__.py
tests/test_intelligence_ui_api_boundary.py
```

Related context:

```text
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
Phase 22 outside validation is treated as accepted input.
Phase 23A contract matches the implementation.
Phase 23B implements the declared public interface.
The implementation is pure and in-memory.
The implementation adds no UI code.
The implementation adds no HTTP server.
The implementation accepts only structured query/answer/writer packet objects.
Request packets are built from sanitized ChatQueryRequest values.
Response packets are built from structured ChatQueryPlan and ChatAnswer values.
Response packets preserve citations.
Response packets preserve caveats.
Response packets preserve missing_evidence.
Response packets preserve blockers.
local_user_data is blocked by default.
sensitive scope is blocked by default.
writer packets are blocked by default.
accepted audited writer packets are allowed only when explicitly enabled.
rejected writer audit results fail cleanly.
unaudited writer drafts fail cleanly by default.
error packets do not expose stack traces by default.
unknown client_surface fails cleanly.
private metadata keys are rejected, including nested keys.
forbidden strategic language is rejected.
serialization is deterministic.
The implementation does not call LLMs.
The implementation does not import LLM SDKs.
The implementation does not query SQLite or providers.
The implementation does not retrieve evidence itself.
The implementation does not generate recommendations.
```

Confirm these public objects exist:

```text
ChatUIBoundaryBuildError
ChatUIRequestPacket
ChatUIResponsePacket
ChatUIErrorPacket
ChatUIBoundaryOptions
build_chat_ui_request_packet(...)
build_chat_ui_response_packet(...)
build_chat_ui_error_packet(...)
chat_ui_request_packet_to_dict(...)
chat_ui_response_packet_to_dict(...)
chat_ui_error_packet_to_dict(...)
```

Confirm schema discipline:

```text
Phase 23 adds no schema changes.
No tables, columns, indexes, migrations, or repository methods were added for UI/API boundary packets.
UI/API boundary packets remain in-memory only.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 690 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_intelligence_ui_api_boundary -v
```

Confirm:

```text
Ran 18 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\ui_api_boundary.py
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\ui_api_boundary.py
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py docs\PHASE23B_CHAT_INTELLIGENCE_UI_API_BOUNDARY_IMPLEMENTATION_REPORT.md
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
no Phase 23 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
ui_api_boundary.py imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, sqlite3, openai, or anthropic
ui_api_boundary.py reads source/provider tables or payloads
ui_api_boundary.py writes files
ui_api_boundary.py calls LLMs
ui_api_boundary.py imports LLM SDKs
ui_api_boundary.py queries SQLite
ui_api_boundary.py retrieves evidence itself
ui_api_boundary.py runs simulator logic
ui_api_boundary.py implements card behavior
ui_api_boundary.py adds an HTTP server
ui_api_boundary.py adds UI code
ui_api_boundary.py generates recommendation or deck-construction language
ui_api_boundary.py persists request, response, or error packets
private metadata can escape into output
source conflicts are resolved instead of preserved
unsupported simulator cards are treated as modeled
hidden citations, caveats, missing_evidence, or blockers can pass response packet construction
unaudited writer drafts can pass by default
rejected writer audits can pass display construction
```

## Phase 24 Gate

Phase 24 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
