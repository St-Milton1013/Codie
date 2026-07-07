# Phase 23A - Chat/Intelligence UI/API Boundary Contract

## Objective

Define the boundary for exposing Codie's interactive intelligence stack to a
future local UI or local API surface.

This is a contract packet. It adds no implementation code, API server, UI code,
schema, DB access, provider access, live LLM calls, recommendation output,
simulator execution, file writing, or private deck export.

## Accepted Inputs

Phase 23A starts after Phase 22 outside validation was accepted.

Accepted prior layers:

```text
Phase 16 Evidence Graph
Phase 17 Evidence Input Assembly
Phase 18 Source Conflict Report
Phase 19 Unsupported Relevant Card Queue
Phase 20 Chat Query Planner
Phase 21 Chat Answer Builder
Phase 22 LLM Writer/Auditor Packet Layer
```

## Purpose

Future UI/API surfaces need a narrow, inspectable boundary around chat and
intelligence features.

The boundary must make it impossible for a frontend or API adapter to:

```text
query SQLite directly
read source/provider tables directly
call providers
run live backfills
call real LLM APIs by default
generate recommendation claims
hide citations or caveats
export private raw_input
mutate simulator traces
```

## Recommended Phase 23B Implementation

Phase 23B should implement pure request/response packet models only.

Likely files:

```text
codie/intelligence/ui_api_boundary.py
tests/test_intelligence_ui_api_boundary.py
docs/PHASE23B_CHAT_INTELLIGENCE_UI_API_BOUNDARY_IMPLEMENTATION_REPORT.md
```

No HTTP server should be created in Phase 23B.

## Public Interface For Phase 23B

Future implementation should define:

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

## ChatUIRequestPacket

Required fields:

```text
request_packet_id
request_id
question_text
subject
constraints
allowed_privacy_scopes
requested_answer_mode
client_surface
generated_at
metadata
```

Rules:

```text
request_packet_id is required
request_id is required
question_text is required
subject must be structured
constraints must be structured
allowed_privacy_scopes must be explicit
requested_answer_mode is optional but must be supported if present
client_surface must identify local_ui, local_api, cli, or test_fixture
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

The request packet is not a database query and not an LLM prompt.

## ChatUIResponsePacket

Required fields:

```text
response_packet_id
request_packet_id
request_id
plan
answer
writer_input
writer_draft
audit_result
citations
caveats
missing_evidence
blockers
privacy_scope
generated_at
metadata
```

Rules:

```text
answer must be a structured ChatAnswer or serialized equivalent
writer_input is optional
writer_draft is optional
audit_result is optional
citations must remain visible
caveats must remain visible
missing_evidence must remain visible
blockers must remain visible
privacy_scope must be explicit
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

The response packet may include writer/auditor output only if it has passed the
Phase 22 audit rules.

## ChatUIErrorPacket

Required fields:

```text
error_packet_id
request_packet_id
request_id
error_type
message
retryable
caveats
generated_at
metadata
```

Allowed error types:

```text
validation_error
privacy_scope_blocked
unsupported_question
missing_evidence
writer_audit_rejected
internal_error
```

Rules:

```text
errors must be structured
errors must not include private raw input
errors must not expose stack traces by default
errors must preserve user-visible caveats when relevant
```

## ChatUIBoundaryOptions

Required fields and defaults:

```text
allow_local_user_data = false
allow_sensitive = false
allow_writer_draft = false
allow_unaudited_writer_draft = false
maximum_question_length = 1000
maximum_constraints = 24
require_citations_visible = true
require_caveats_visible = true
require_missing_evidence_visible = true
require_blockers_visible = true
```

Rules:

```text
allow_writer_draft defaults false
allow_unaudited_writer_draft defaults false
allow_sensitive defaults false
allow_local_user_data defaults false
maximum_question_length must be positive
maximum_constraints must be positive
```

## Allowed Dependencies

Future implementation may import:

```text
standard library
codie.intelligence.query_planner
codie.intelligence.answer_builder
codie.intelligence.llm_writer_auditor
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

## Privacy Rules

The UI/API boundary must reject these keys anywhere in packets or metadata:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances and punctuation variants.

Private user deck text must not appear in request packets, response packets,
error packets, writer packets, or exported UI fixtures.

## Evidence Rules

Response packets must preserve:

```text
citations
caveats
missing_evidence
blockers
privacy_scope
generated_at
source labels when supplied
```

The UI/API boundary must not turn missing evidence into confidence.

## Writer/Auditor Rules

If future responses include Phase 22 writer packets:

```text
writer_draft must be paired with audit_result
accepted UI display requires accepted audit_result
rejected audit_result must remain visible as an error or caveat
unaudited writer drafts are blocked by default
audit findings must not be hidden
```

## Forbidden Language

Packets must reject:

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

Tests should construct forbidden strings indirectly when possible so static
scans remain meaningful.

## Required Tests For Phase 23B

Future implementation must add tests for:

```text
valid request packet serializes deterministically
valid response packet preserves answer citations
valid response packet preserves caveats
valid response packet preserves missing_evidence
valid response packet preserves blockers
local_user_data is blocked by default
sensitive scope is blocked by default
writer draft is blocked by default
accepted audited writer draft is allowed when enabled
rejected audited writer draft fails cleanly
unaudited writer draft fails cleanly
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
error packet does not expose stack trace by default
unknown client_surface fails cleanly
serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM SDK imports
```

## Static Scans For Phase 23B

Future implementation must pass:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\ui_api_boundary.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\ui_api_boundary.py
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\ui_api_boundary.py tests\test_intelligence_ui_api_boundary.py docs\PHASE23B_CHAT_INTELLIGENCE_UI_API_BOUNDARY_IMPLEMENTATION_REPORT.md
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

## Schema Impact

None.

Phase 23A authorizes no schema changes.

## UI Impact

None.

Phase 23A authorizes no React, Vite, API server, or UI component changes.

## Do Not Do In Phase 23B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not add an HTTP server
do not call real LLM APIs
do not import LLM SDKs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Acceptance Criteria For Phase 23A

Phase 23A is complete when:

```text
contract document exists
contract report exists
public interface is defined
request/response/error packet models are defined
privacy rules are defined
writer/auditor display rules are defined
Phase 23B required tests are listed
NEXT_PHASE_CONTRACT points to Phase 23B
CODEX_CONTINUITY_HANDOFF points to Phase 23B
no implementation code was added
no schema changes were made
no UI/API server was added
```
