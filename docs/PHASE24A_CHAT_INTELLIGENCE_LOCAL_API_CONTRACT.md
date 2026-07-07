# Phase 24A - Chat/Intelligence Local API Contract

## Objective

Define the boundary for a future local-only API that can expose Codie's
interactive intelligence packet layer to the local UI.

This is a contract packet. It adds no implementation code, API server, route
handler, UI code, schema, DB access, provider access, live LLM calls,
recommendation output, simulator execution, file writing, or private deck
export.

## Accepted Inputs

Phase 24A starts after Phase 23 outside validation was accepted.

Accepted prior layers:

```text
Phase 20 Chat Query Planner
Phase 21 Chat Answer Builder
Phase 22 LLM Writer/Auditor Packet Layer
Phase 23 Chat/Intelligence UI/API Boundary Packet Layer
```

## Purpose

Future local UI surfaces need a controlled local API adapter. The API must be a
thin boundary around already-approved packet builders. It must not become a
second architecture with its own retrieval, recommendation logic, provider
calls, SQL, or LLM behavior.

## Recommended Phase 24B Implementation

Phase 24B should implement local API route-spec packet models only.

Likely files:

```text
codie/intelligence/local_api.py
tests/test_intelligence_local_api.py
docs/PHASE24B_CHAT_INTELLIGENCE_LOCAL_API_IMPLEMENTATION_REPORT.md
```

Phase 24B must not start an HTTP server. It should define route descriptors,
request validators, response wrappers, and serialization helpers that a future
server can consume.

## Public Interface For Phase 24B

Future implementation should define:

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

## Route Scope

Initial route specs should describe these local-only endpoints:

```text
POST /local/chat/request
POST /local/chat/response
POST /local/chat/error
GET /local/health
```

These are route specifications, not live routes.

## LocalAPIRouteSpec

Required fields:

```text
route_id
method
path
operation
request_packet_type
response_packet_type
allowed_client_surfaces
requires_auth
local_only
privacy_scope
generated_at
metadata
```

Rules:

```text
route_id is required
method must be GET or POST
path must start with /local/
local_only must be true
requires_auth defaults false for local-only development specs
privacy_scope must be explicit
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## LocalAPIRequestEnvelope

Required fields:

```text
envelope_id
route_id
method
path
client_surface
request_packet
generated_at
metadata
```

Rules:

```text
route_id is required
method and path must match the route spec
client_surface must be allowed by the route spec
request_packet must be a ChatUIRequestPacket or serialized equivalent
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## LocalAPIResponseEnvelope

Required fields:

```text
envelope_id
route_id
status_code
response_packet
generated_at
metadata
```

Rules:

```text
status_code must be 200 for successful packet envelopes
response_packet must be a ChatUIResponsePacket or serialized equivalent
citations/caveats/missing_evidence/blockers must remain visible through the packet
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## LocalAPIErrorEnvelope

Required fields:

```text
envelope_id
route_id
status_code
error_packet
generated_at
metadata
```

Rules:

```text
status_code must be 400, 403, 404, 409, 422, or 500
error_packet must be a ChatUIErrorPacket or serialized equivalent
stack traces must not be exposed by default
metadata must be JSON-compatible
private/raw metadata keys are forbidden
```

## LocalAPIOptions

Required fields and defaults:

```text
allow_non_local_paths = false
allow_non_local_hosts = false
allow_sensitive = false
allow_local_user_data = false
maximum_payload_bytes = 262144
require_local_only_routes = true
```

Rules:

```text
allow_non_local_paths defaults false
allow_non_local_hosts defaults false
maximum_payload_bytes must be positive
require_local_only_routes defaults true
```

## Allowed Dependencies

Future implementation may import:

```text
standard library
codie.intelligence.ui_api_boundary
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
flask
fastapi
uvicorn
starlette
```

## Privacy Rules

The local API boundary must reject these keys anywhere in envelopes or
metadata:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested appearances and punctuation variants.

Private user deck text must not appear in request envelopes, response
envelopes, error envelopes, route specs, or exported fixtures.

## Local-Only Rules

Future route specs must enforce:

```text
paths begin with /local/
local_only is true
no public host binding
no remote base URL
no network client dependency
no authentication bypass language for non-local access
```

## Evidence Rules

Response envelopes must preserve the underlying `ChatUIResponsePacket`
visibility requirements:

```text
citations
caveats
missing_evidence
blockers
privacy_scope
generated_at
```

The local API boundary must not turn missing evidence into confidence.

## Forbidden Language

Packets and envelopes must reject:

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

## Required Tests For Phase 24B

Future implementation must add tests for:

```text
valid chat route spec serializes deterministically
route spec requires /local/ path
route spec rejects non-local paths by default
route spec rejects unsupported methods
request envelope validates method/path against route
request envelope rejects unsupported client_surface
response envelope preserves ChatUIResponsePacket
error envelope preserves ChatUIErrorPacket
error envelope rejects stack trace metadata
local_user_data is blocked by default
sensitive scope is blocked by default
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, server imports, network clients, file writes, or LLM SDK imports
```

## Static Scans For Phase 24B

Future implementation must pass:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\intelligence\local_api.py tests\test_intelligence_local_api.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\local_api.py tests\test_intelligence_local_api.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\local_api.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\local_api.py tests\test_intelligence_local_api.py
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\local_api.py
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\local_api.py tests\test_intelligence_local_api.py docs\PHASE24B_CHAT_INTELLIGENCE_LOCAL_API_IMPLEMENTATION_REPORT.md
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

Phase 24A authorizes no schema changes.

## UI Impact

None.

Phase 24A authorizes no React, Vite, API server, route handler, or UI
component changes.

## Do Not Do In Phase 24B

```text
do not add schema
do not add DB reads or writes
do not add repository imports
do not call providers
do not read source/provider payloads directly
do not add UI
do not add a live HTTP server
do not import Flask/FastAPI/Starlette/Uvicorn
do not call real LLM APIs
do not import LLM SDKs
do not run simulator logic
do not implement card behavior
do not calculate analytics
do not generate recommendations
do not write files
do not export private raw_input
```

## Acceptance Criteria For Phase 24A

Phase 24A is complete when:

```text
contract document exists
contract report exists
public interface is defined
route/request/response/error envelope models are defined
local-only rules are defined
privacy rules are defined
Phase 24B required tests are listed
NEXT_PHASE_CONTRACT points to Phase 24B
CODEX_CONTINUITY_HANDOFF points to Phase 24B
no implementation code was added
no schema changes were made
no API server was added
```
