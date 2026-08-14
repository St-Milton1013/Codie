# Phase50A Codie Local Working Iteration v0.1 Contract

Status: internally complete; outside validation required

Phase tuple:

```text
phase_id: Phase50A
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase50B
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## 1. Authority and priority amendment

The human project owner approved Codie Local Working Iteration v0.1 as the
next implementation packet on 2026-08-14, ahead of further Goal Engine work.
This is a deliberate delivery-priority amendment, not an inference from older
roadmap text.

The bounded interposed sequence is:

```text
Phase50A - Local Working Iteration v0.1 contract
Phase50B - Local Working Iteration v0.1 implementation
Phase50C - Local Working Iteration v0.1 checkpoint / freeze
resume Phase44H - Subsystem Health Foundation Contract
```

Existing Phase44H through Phase49 identifiers, ordering, promotion gates, and
authority rules remain unchanged. Phase50 does not grant Goal Engine authority
and does not satisfy any Phase44-49 gate.

## 2. Problem statement

Codie's current React surface is a static page-model preview. It can display
generated JSON, but it cannot initialize a workspace, import card truth, accept
a user's deck, run an evidence comparison, retrieve saved analyses, or export
results through the browser. The Python local API module defines packet
contracts only; it is not an HTTP application server.

The repository therefore contains substantial validated domain machinery but
does not yet provide one coherent local user workflow.

## 3. Required outcome

Phase50B must deliver one locally runnable, user-operated vertical slice that
allows a person to:

```text
start Codie with one documented PowerShell command
see whether the local workspace and card catalog are ready
initialize a contained local SQLite workspace
import a user-selected local Scryfall JSON card snapshot
paste or select a Commander decklist
receive explicit unresolved-card feedback without partial persistence
import a local evidence-candidate JSON packet
run and save an evidence-only deck comparison
browse remembered decks and saved analyses
inspect evidence rows with provenance and evidence type visible
download JSON and Markdown representations of a saved analysis
stop the local application without leaving a background service
```

The working iteration is successful only when the browser operates on fresh
user actions and durable local state. Replacing one fixture with another
fixture is not sufficient.

## 4. Product boundary

### 4.1 Included

```text
loopback-only local application server
same-origin local JSON API
existing React/TypeScript/Vite user interface
existing SQLite schema and repositories
existing ScryfallCard and ScryfallImporter card-truth path
existing user-deck importer and atomic resolution behavior
existing evidence-only comparison and saved-analysis paths
existing page-model and export representations where applicable
explicit first-run, loading, empty, success, and failure states
local JSON and Markdown download
PowerShell setup, launch, and stop documentation
```

### 4.2 Excluded

```text
Jin runtime or conversational strategist behavior
Theory Corpus retrieval or generation
Rules or Corrections runtime behavior
recommendation generation, ranking, cuts, additions, or deck optimization
autonomous provider backfill or scheduled network activity
Hareruya ingestion outside tournament-only evidence
simulation execution or simulator evidence promotion
Goal Engine health, ledger, decision, shadow, or authority behavior
Stream Deck control paths or required Stream Deck integration
hosted service, cloud persistence, accounts, authentication, or telemetry
LAN binding, remote access, mobile delivery, or outbound sharing automation
schema migration or a second persistence model
automatic package installation during normal application launch
```

## 5. Architecture

### 5.1 Layer ownership

```text
ui/ React application
  -> same-origin /local/* requests only
codie.local_app HTTP adapter
  -> request validation, response envelopes, containment, lifecycle
codie.local_app service layer
  -> orchestration of existing domain APIs
existing codie domain modules
  -> cards, repositories, user decks, comparisons, saved analyses, exports
existing SQLite database
  -> canonical local persistence for this slice
```

The UI must never issue SQL, import Python implementation details, parse raw
provider payloads into strategic conclusions, or own canonical state. The HTTP
adapter must not duplicate domain algorithms already present in Codie.

### 5.2 Proposed implementation locations

Phase50B may create or update only the smallest necessary set under:

```text
codie/local_app/
scripts/run-codie.ps1
scripts/setup-codie-ui.ps1
ui/src/
tests/test_local_working_iteration.py
tests/test_local_working_iteration_http.py
docs/LOCAL_WORKING_ITERATION_V0_1_USAGE.md
required current governance and checkpoint files
```

Any schema, provider-client, Goal Engine, Jin, Theory, Rules, Corrections,
simulation, recommendation, workflow, or dependency-file change requires a
separate contract amendment and outside review.

### 5.3 Runtime and dependency boundary

The local application server must use Python standard-library networking. It
may use dependencies already declared by Codie but Phase50B may not add a
runtime dependency. The browser assets remain React/TypeScript/Vite assets
built from the existing locked UI dependency set.

Setup may explicitly install declared UI development dependencies. Normal
launch must not access the network, install packages, download card data, or
modify files outside the configured workspace.

## 6. Local service contract

### 6.1 Binding and lifecycle

```text
default host: 127.0.0.1
LAN and non-loopback binding: forbidden
default port: deterministic documented value with explicit collision error
database: configured path contained beneath the workspace root
UI assets: contained build directory only
shutdown: foreground interrupt or explicit local shutdown action
```

The launcher must report the URL, database path, workspace root, process ID,
and privacy boundary without printing raw deck text or card payloads.

### 6.2 Required routes

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/local/health` | Service, database, catalog, and UI readiness only |
| `GET` | `/local/workspace` | Contained workspace summary and counts |
| `POST` | `/local/database/bootstrap` | Idempotently initialize the configured database |
| `POST` | `/local/catalog/import` | Import explicit user-selected Scryfall JSON |
| `GET` | `/local/decks` | List remembered user decks without raw input |
| `GET` | `/local/decks/{id}` | Show one remembered deck with redaction defaults |
| `POST` | `/local/decks/import` | Atomically import one pasted decklist |
| `POST` | `/local/decks/{id}/comparisons` | Run and save one evidence-only comparison |
| `GET` | `/local/decks/{id}/analyses` | List saved analyses for one deck |
| `GET` | `/local/analyses/{id}` | Retrieve one saved analysis and its evidence rows |
| `GET` | `/local/analyses/{id}/export` | Return JSON or Markdown download content |

No route may accept a remote URL for automatic fetching in v0.1. File content
must come from an explicit browser file selection or pasted user input.

### 6.3 Request and response rules

```text
JSON only for API requests and responses
explicit Content-Length and configured payload limit
structured error code, safe message, and affected field
no Python traceback in a response
no raw deck text in a response unless the user explicitly requests a local
  deck-detail view and the existing privacy boundary permits it
no raw Scryfall payload in health, workspace, or analysis responses
deterministic sorting for lists and evidence rows
HTTP 4xx for user/input errors
HTTP 5xx for bounded internal errors with redacted messages
```

## 7. Card-catalog import

The user must explicitly select a local JSON file. The service must:

```text
accept a Scryfall list payload or the accepted local snapshot object shape
validate every candidate through existing ScryfallCard parsing
import through ScryfallImporter and CoreRepository
run in one database transaction
roll back the complete import when a blocking record error occurs
return imported count, rejected count, snapshot hash, and visible warnings
never reinterpret raw card truth as tournament evidence or recommendation
```

The UI must show that Scryfall is card truth, not tournament evidence, Theory,
Rules authority, or a recommendation source.

## 8. Deck import and evidence comparison

Deck import must preserve existing atomic card resolution. Unresolved cards
must be returned by name and must not leave partial user-deck, user-deck-card,
analysis-session, or saved-analysis rows.

Evidence comparison input is an explicit local JSON packet containing typed
candidates. Each candidate must retain:

```text
oracle_id
card_name
evidence_type
score when present
sample_size when present
source_record_id when present
source_url when present
```

The service must use the existing evidence-only comparison builder and saved
analysis repository path. The UI must label every row as evidence and display
its evidence type and provenance. It must not transform absence into a cut or
inclusion recommendation.

## 9. User interface requirements

The default screen must replace the static preview with a functional local
workspace containing:

```text
service and workspace readiness
database initialization action
card-catalog import action and progress/result state
decklist text/file input and deck-name field
unresolved-card error panel
remembered-deck list
evidence-candidate file input
run comparison action
saved-analysis list
analysis detail with present/absent evidence rows
JSON and Markdown download actions
visible provenance, evidence class, privacy, and local-only notices
```

Controls must be keyboard accessible, labeled, and disabled while their action
is running. Empty states must identify the next safe action. Errors must remain
visible until dismissed or superseded by a successful retry.

No hidden action may run merely because the page loads.

## 10. Hard governance boundaries

### 10.1 Evidence classes

The implementation must preserve hard separation among:

```text
card truth
tournament evidence
community signal
simulation evidence
Theory claims
Rules authority
user corrections
recommendations
```

The working iteration may display only the class actually represented by the
source packet. It may not fuse, relabel, or promote evidence implicitly.

### 10.2 Local-first, privacy, and cost

```text
all persistence local
loopback only
no telemetry
no account
no paid API
no API key
no background network work
no secrets in repository, logs, responses, or exports
workspace-root containment for every server-side read or write
raw deck input redacted from logs and default listings
```

### 10.3 Supplemental-only integrations

Stream Deck remains supplemental-only and may not become a dependency,
authority source, required launcher, or control path. Phase50 does not add
Stream Deck behavior.

### 10.4 Theory-skill review gate

Phase50 does not implement or modify Theory, Jin, Rules, or Corrections
behavior. Any later packet that does so still requires the mandatory external
Theory/theory-skill review gate before acceptance.

### 10.5 Hareruya boundary

Hareruya remains tournament-only evidence. Phase50 may not use Hareruya for
card truth, generic deck enrichment, recommendations, Theory, Rules, or UI
demonstration data.

### 10.6 Human authority

All roadmap changes, merges, releases, phase advancement, Goal promotion, and
work-order authority remain human-gated. A clean Phase50 result cannot promote
Goal Engine authority.

## 11. Failure and safety behavior

Phase50B must fail closed for:

```text
non-loopback host requests
workspace path escape
missing or malformed Content-Length
payload over configured limit
unsupported content type
malformed JSON
invalid Scryfall records
unresolved deck cards
unknown deck or analysis identifiers
evidence candidate schema errors
unsafe export format
attempted raw traceback disclosure
attempted strategic/recommendation language promotion
```

Database mutations must be transactional. A failed request must not produce a
partial catalog import, deck, comparison, or saved analysis.

## 12. Validation requirements

Phase50B must provide focused tests for:

```text
loopback binding and remote-host rejection
workspace containment
database bootstrap idempotency
catalog import success and rollback
deck import success and unresolved-card atomicity
evidence packet validation
comparison persistence and deterministic retrieval
redaction and no-traceback errors
export content and provenance
route/method/content-type/payload-size failures
UI build
no page-load mutation or provider fetch
```

Required validation commands:

```text
python scripts/check_schema.py
python -m unittest tests.test_local_working_iteration tests.test_local_working_iteration_http -v
python -m unittest discover -s tests -p "test_*.py"
python -m ruff check codie/local_app tests/test_local_working_iteration.py tests/test_local_working_iteration_http.py
python -m mypy codie/local_app
UI TypeScript no-emit check
UI production build
git diff --check
```

Repository-wide Ruff and mypy runs must also be captured as non-regression
inventories. The Phase50B diff may introduce no new finding in a touched or new
file. Existing whole-repository findings outside the Phase50B change boundary
are inherited baseline and must not be silently repaired inside this packet.

The deterministic, architecture, adversarial, and aggregate validators must
all return `CLEAN_PASS` for the exact Phase50B SHA before merge.

## 13. Acceptance test

Outside validation must reject Phase50B unless a clean local checkout can
perform this exact end-to-end scenario without editing fixture files:

```text
1. run the documented setup once
2. start Codie with the documented launch command
3. open the reported loopback URL
4. initialize the workspace database
5. import a local Scryfall JSON snapshot
6. paste and import a resolvable Commander deck
7. import a local evidence-candidate packet
8. run and save a comparison
9. reload the page
10. retrieve the same deck and saved analysis from SQLite
11. inspect evidence type and provenance
12. download JSON and Markdown outputs
13. stop Codie
14. confirm no service remains listening and no write escaped the workspace
```

## 14. Completion and stop condition

Phase50A is complete only when this contract packet passes outside validation
and is merged by a human. Phase50B remains blocked until then.

Phase50A adds no production code, schema, API server, UI behavior, provider
behavior, dependency, workflow, Goal Engine behavior, Jin behavior, Theory
behavior, Stream Deck behavior, or runtime authority.
