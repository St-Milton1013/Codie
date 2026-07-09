# Phase 29C - CLI / Safe File Writer Integration Contract

## Objective

Define the future CLI and safe local file-writing boundary for recommendation
report documents.

This is a contract packet only. It adds no implementation code, schema, DB
access, repository methods, provider calls, source-table reads, raw provider
reads, UI code, LLM calls, simulator execution, analytics recalculation,
persistence, candidate discovery, candidate ranking, candidate scoring, deck
health generation, recommendation generation, cut selection, or addition
selection.

## Accepted Inputs

Phase 29C starts after Phase 29B Report Document Implementation is internally
complete and Phase 29A's conditional CLI/file-writing validation fix has been
applied.

Accepted prior layers:

```text
Phase 28 Deck Health / Recommendation Output
Phase 29A CLI / Report Integration Contract
Phase 29B Report Document Implementation
Phase 9 Export Surfaces
Phase 12 Local Report Sharing Track
Phase 14 Safe File Writer patterns
```

## Purpose

Phase 29C decides how future CLI users can render and write local report files
from already-built `RecommendationOutputBundle` JSON.

CLI and file writing are presentation/export concerns only.

They must not become reasoning, candidate discovery, recommendation generation,
data loading, or repository access layers.

## Architecture Position

Future output flow:

```text
RecommendationOutputBundle JSON
validate bundle input
build RecommendationReportDocument
render JSON and/or Markdown report payload
safe file writer
local filesystem output
```

## Allowed Future Inputs

Future implementation may accept:

```text
local JSON file containing a RecommendationOutputBundle payload
explicit output root
explicit output format: json, markdown, or both
optional explicit output basename
optional overwrite flag
optional provenance-section flag
```

The local JSON input is caller-provided packet data. It must be validated before
rendering.

## Forbidden Future Inputs

Future CLI/file writer must not read:

```text
raw provider payloads
provider_objects
source_events
source_decks
source_deck_cards
raw Moxfield primer bodies
private deck import text
raw simulator traces
live provider APIs
live Scryfall
live Moxfield
SQLite
repositories
LLM output as evidence
```

## Required Future Public Interface

Future implementation should define:

```text
RecommendationReportWriteError
RecommendationReportWriteResult
RecommendationReportWriteOptions
write_recommendation_report_files(...)
```

Future CLI should define a command equivalent to:

```text
codie-recommendation-output render --bundle-json <path> --format json|markdown|both --output-root <path>
```

Optional flags may include:

```text
--basename <name>
--overwrite
--no-provenance
```

Names may change only if the implementation report documents the mapping.

## Safe File Writing Rules

Future file writing must:

```text
require output_root
resolve output_root to an absolute path
reject output roots that point to files
create missing output root directories only when explicitly requested by implementation contract
enforce output-root containment for all written files
write UTF-8
allow only .json and .md report files
use deterministic file names or explicit user-provided file names
reject path traversal
reject unsupported extensions
reject partial writes appearing complete
avoid overwriting existing files unless overwrite is explicit
return written file paths
return format metadata
return source bundle ID
```

If a manifest is implemented, it must be written last.

## CLI Behavior Rules

Future CLI must:

```text
require --bundle-json
require --format
require --output-root for file writes
validate bundle input before rendering
fail with nonzero status for malformed JSON
fail with nonzero status for missing required bundle fields
fail with nonzero status for unsupported format
fail with nonzero status for unsafe output path
fail with nonzero status for output-root pointing to a file
fail with nonzero status for write permission failures
avoid printing private payloads
avoid printing raw stack traces by default
print concise success output with written paths
```

## Output Naming Rules

Default deterministic filenames should be based on the source bundle ID:

```text
<safe_bundle_id>.recommendation-report.json
<safe_bundle_id>.recommendation-report.md
manifest.json, if implemented
```

Unsafe filename characters must be normalized or rejected. Filename
normalization must be deterministic.

Explicit basenames must be normalized deterministically, must not contain path
separators, and must not override the allowed `.json` / `.md` extension rules.

## Report Payload Rules

The writer must use:

```text
build_recommendation_report_document(...)
recommendation_report_document_to_dict(...)
recommendation_report_document_to_markdown(...)
```

It must not recreate report semantics independently.

JSON output must preserve the structured report document.

Markdown output must be generated from the report document serializer.

## Privacy Rules

CLI and file writer output must not expose:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
raw simulator trace
stack traces
```

Blocked keys must be rejected recursively before file writing.

## Forbidden Behavior

Future implementation must not:

```text
discover recommendation candidates
rank recommendation candidates
score recommendation candidates
choose cuts
choose additions
generate deck health findings
generate final recommendations
read DB tables
import repositories
call providers
read source/provider tables
read raw provider payloads
read primer bodies
run simulator logic
call LLMs
start a server
add UI
calculate analytics
persist to SQLite
```

## Forbidden Wording

Future CLI/report output must reject unsupported strategic claims such as:

```text
you should play
should be played
should be cut
must include
correct card
strict upgrade
auto-include
recommended cut
recommended include
secretly optimal
breaks the format
best card
strictly better
```

## Phase 29D Recommended Implementation Scope

If Phase 29C is accepted, Phase 29D should implement:

```text
codie/recommendation_output/writers.py
codie/cli/recommendation_output.py
tests/test_recommendation_output_writers.py
tests/test_cli_recommendation_output.py
docs/PHASE29D_CLI_SAFE_FILE_WRITER_IMPLEMENTATION_REPORT.md
```

If implementation becomes too large, split CLI and writer:

```text
Phase 29D - Safe file writer
Phase 29E - CLI wrapper
Phase 29F - Checkpoint
```

## Required Phase 29D / 29E Tests

If Phase 29D implements only the safe file writer, tests should prove:

```text
writer requires RecommendationOutputBundle JSON input
writer validates bundle before rendering
writer writes JSON report
writer writes Markdown report
writer writes both formats
JSON output preserves structured report document
Markdown output includes evidence visibility fields
output_root containment is enforced
path traversal is rejected
unsupported file extension is rejected
output roots pointing to files are rejected
overwrite is explicit
UTF-8 output is used
manifest writes last, if manifest exists
```

If Phase 29E implements the CLI wrapper, also test:

```text
CLI requires --bundle-json
CLI requires --format
CLI requires --output-root
CLI rejects malformed JSON
CLI rejects missing required bundle fields
CLI rejects unsupported format
CLI rejects unsafe output path
CLI does not print private payloads
CLI does not print raw stack traces by default
```

## Required Static Scans

If Phase 29D implements only the safe file writer, scan:

```text
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text|raw_input" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\recommendation_output tests\test_recommendation_output_writers.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

If Phase 29E implements the CLI wrapper, also scan:

```text
codie\cli
tests\test_cli_recommendation_output.py
```

Do not require `codie\cli` or `tests\test_cli_recommendation_output.py` to
exist when Phase 29D is writer-only.

Expected:

```text
no production matches, except blocked-key constants and rejection tests where explicitly documented
no schema or repository drift
```

## Do Not Do In Phase 29C

```text
do not implement CLI code
do not implement file writing
do not add schema
do not add repositories
do not read DB tables
do not read source/provider tables
do not read raw provider payloads
do not read primer bodies
do not run simulator logic
do not call LLMs
do not add UI
do not calculate analytics
do not discover candidates
do not rank candidates
do not score candidates
do not choose cuts
do not choose additions
do not generate final recommendations
```

## Acceptance Criteria

Phase 29C is accepted when:

```text
contract exists
active roadmap index points to Phase 29D after Phase 29C review
validation index records Phase 29C as contract complete
handoff records Phase 29C status and next gate
git diff --check passes
full test suite passes
```
