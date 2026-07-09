# Phase 29A - CLI / Report Integration Contract

## Objective

Define how already-built Deck Health / Recommendation Output packets may be
surfaced through future CLI and local report/export layers.

This is a contract packet only. It adds no implementation code, schema, DB
access, repository methods, provider calls, source-table reads, raw provider
reads, UI code, file writing, LLM calls, simulator execution, analytics
recalculation, persistence, candidate discovery, candidate ranking, candidate
scoring, deck health generation, recommendation generation, cut selection, or
addition selection.

## Accepted Inputs

Phase 29A starts after Phase 28 outside validation returned PASS.

Accepted prior layers:

```text
Phase 25 Evidence Fusion / Unified Evidence Objects
Phase 26 Decision Intelligence Boundary
Phase 27 Weight Profile / Analysis Profile
Phase 28 Deck Health / Recommendation Output
Phase 12 local report sharing/export foundations
Phase 14 safe file writer patterns
Phase 15 CLI documentation patterns
```

## Purpose

Phase 29 begins the path from internal packet objects to user-readable local
artifacts.

Future CLI/report integration may format and export existing
`RecommendationOutputBundle` payloads, but it must not create or alter the
underlying conclusions.

## Architecture Position

Future output flow:

```text
RecommendationOutputBundle
CLI / Report Integration
Local JSON / Markdown report payload
Safe file writer / share bundle / UI preview
```

CLI/report integration is a presentation and packaging boundary only.

It is not a reasoning layer.

## Allowed Future Inputs

Future Phase 29B may accept:

```text
already-built RecommendationOutputBundle object
already-built RecommendationOutputBundle dictionary
local JSON file containing a RecommendationOutputBundle payload
explicit output path or output root
explicit format option: json, markdown, or both
explicit redaction / privacy options
```

If a local JSON file is accepted, it must be treated as caller-provided packet
input and validated before rendering.

## Forbidden Future Inputs

Phase 29A and future Phase 29B must not read:

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
SQLite without a future repository contract
LLM output as evidence
```

## Required Future Public Interface

Future implementation should define:

```text
RecommendationReportBuildError
RecommendationReportOptions
RecommendationReportSection
RecommendationReportDocument
build_recommendation_report_document(...)
recommendation_report_document_to_dict(...)
recommendation_report_document_to_markdown(...)
validate_recommendation_report_document(...)
```

Future CLI implementation should define a command equivalent to:

```text
codie-recommendation-output render --bundle-json <path> --format json|markdown|both --output-root <path>
```

Names may change only if the implementation report documents the mapping.

## Report Document Required Fields

Every report document must expose:

```text
report_id
source_bundle_id
bundle_type
subject
generated_at
report_version
output_version
sections
caveat_count
contradiction_count
metadata
```

Each section must expose:

```text
section_id
section_type
title
summary
source_output_ids
decision_ids
evidence_object_ids
weight_profile_refs
analysis_profile_refs
confidence
expected_impact
source_agreement
caveats
contradictions
speculation_level
body_lines
metadata
```

## Allowed Section Types

```text
deck_health
recommendation_candidate
replacement_suggestion
package_gap
evidence_explanation
caveats
contradictions
provenance
```

## Required Presentation Rules

Future reports must:

```text
keep confidence visible
keep expected impact visible
keep source agreement visible
keep caveats visible
keep contradictions visible
keep speculation level visible
keep weight profile ID/version visible
keep analysis profile ID/version visible
keep decision IDs visible
keep UnifiedEvidenceObject IDs visible
label monitor / investigate / no_action as non-action outputs
label simulator-derived material as model-derived and not tournament evidence
label primer context as explanatory only
label low sample size visibly
label low coverage visibly
```

## Formatting Rules

Markdown output should be evidence-first and action-aware:

```text
title
subject
summary
deck health findings
candidate packets
replacement suggestion packets
package gaps
evidence explanations
caveats
contradictions
provenance / versions
```

JSON output should preserve the structured report document, not a lossy text
summary.

Markdown tables must escape pipes in user-visible fields.

## Safe File Writing Rules

If Phase 29B writes files, it must use the established safe writer pattern:

```text
output_root containment required for user-facing writes
reject output roots that point to files
create missing output root directories only when explicitly requested
write UTF-8
allow only .json and .md report files
write deterministic file names or explicit user-provided file names
avoid partial success looking complete
```

If a manifest is added, it must be written last.

## CLI Rules

Future CLI must:

```text
require bundle input
validate bundle input before rendering
require explicit output format
recommend or require output_root for file writes
return nonzero status for malformed bundle input
return nonzero status for unsupported format
return nonzero status for unsafe output path
avoid printing private payloads
avoid printing raw stack traces by default
```

## Forbidden Wording

Future report and CLI output must reject unsupported strategic claims such as:

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

Allowed wording remains evidence-first:

```text
Codie found evidence supporting review of this packet.
This candidate is marked monitor.
This output has low coverage and should be treated as a review item.
Simulator comparison is model-derived and not tournament evidence.
Primer context is explanatory only.
```

## Privacy Rules

Reports must not expose:

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

Blocked keys must be rejected recursively.

## Phase 29B Recommended Implementation Scope

If Phase 29A is accepted, Phase 29B should implement only:

```text
codie/recommendation_output/reporting.py
tests/test_recommendation_output_reporting.py
docs/PHASE29B_CLI_REPORT_INTEGRATION_IMPLEMENTATION_REPORT.md
```

CLI and file writing may be split into Phase 29C if the implementation becomes
large.

If CLI is included in Phase 29B, expected files are:

```text
codie/cli/recommendation_output.py
tests/test_cli_recommendation_output.py
```

## Required Phase 29B Tests

Future tests should prove:

```text
report document requires RecommendationOutputBundle input
report document serializes deterministically
markdown output includes confidence
markdown output includes expected impact
markdown output includes source agreement
markdown output includes caveats
markdown output includes contradictions
markdown output includes speculation level
markdown output includes weight profile versions
markdown output includes analysis profile versions
markdown output includes decision IDs
markdown output includes UnifiedEvidenceObject IDs
monitor / investigate / no_action are labeled as non-action outputs
simulator material is labeled model-derived and not tournament evidence
primer context is labeled explanatory only
private metadata is rejected recursively
forbidden strategic language is rejected
markdown table pipes are escaped
malformed bundle input fails cleanly
```

If file writing is implemented:

```text
output_root containment is enforced
unsafe output paths are rejected
unsupported file extensions are rejected
output roots pointing to files are rejected
JSON and Markdown writes are UTF-8
manifest writes last if manifest exists
```

## Required Static Scans

Reporting-only Phase 29B implementation should run:

```text
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\recommendation_output tests\test_recommendation_output_reporting.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\recommendation_output tests\test_recommendation_output_reporting.py
rg -n "raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text|raw_input" codie\recommendation_output tests\test_recommendation_output_reporting.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\recommendation_output tests\test_recommendation_output_reporting.py
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\recommendation_output tests\test_recommendation_output_reporting.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no production matches, except blocked-key constants and rejection tests where explicitly documented
no schema or repository drift
```

If CLI is implemented in Phase 29B or a later Phase 29 packet, also scan:

```text
codie\cli
tests\test_cli_recommendation_output.py
```

If file writing is deferred, do not require file-writing behavior tests yet.

If file writing is implemented in Phase 29B or a later Phase 29 packet, add
tests for:

```text
output_root containment
unsafe output path rejection
unsupported extension rejection
output-root-is-file rejection
UTF-8 JSON and Markdown writes
manifest-last behavior, if a manifest exists
```

## Do Not Do In Phase 29A

```text
do not implement CLI code
do not implement report code
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

Phase 29A is accepted when:

```text
contract exists
Phase 28 outside validation is recorded as PASS
active roadmap index points to Phase 29B after Phase 29A review
validation index records Phase 29A as contract complete
handoff records Phase 29A status and next gate
git diff --check passes
full test suite passes
```
