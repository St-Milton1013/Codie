# Phase 13Y - Simulation Review Export Contract

## Purpose

Define export surfaces for reviewed simulator accuracy summaries and simulator
line review annotations before implementation.

Phase 13X produces read-only reviewed simulator accuracy summaries. Phase 13Z
may export those summaries and selected review annotations as portable JSON and
Markdown, but exports must remain local, read-only snapshots. They must not
mutate simulator rows, import edited reviews, write analytics, generate
recommendations, or treat simulator reviews as tournament evidence.

This is a contract-only packet. It does not add export code, file writing,
schema changes, UI, CLI commands, import behavior, recommendation output,
analytics writes, or simulator behavior changes.

## Source Documents

```text
docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md
docs/PHASE13V_CHALLENGE_LINE_REVIEW_PERSISTENCE_IMPLEMENTATION_REPORT.md
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md
docs/PHASE13X_REVIEWED_SIMULATOR_ACCURACY_IMPLEMENTATION_REPORT.md
codie/probability_engine/line_review.py
codie/probability_engine/line_review_persistence.py
codie/probability_engine/reviewed_accuracy.py
```

## Files To Create Or Modify In Phase 13Z

Expected files:

```text
codie/probability_engine/review_export.py
tests/test_probability_engine_review_export.py
docs/PHASE13Z_SIMULATION_REVIEW_EXPORT_IMPLEMENTATION_REPORT.md
```

Allowed modifications:

```text
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Do not modify schema unless a separate migration contract is approved.

## Public Classes And Functions To Add

Suggested public API:

```text
SimulationReviewExportBundle
SimulationReviewMarkdownDocument
simulation_review_summary_to_json_payload(...)
simulation_review_summary_to_markdown(...)
line_review_fixture_to_json_payload(...)
line_review_fixture_to_markdown(...)
build_simulation_review_export_bundle(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None for Phase 13Z.

Export rows, export manifests, and import tracking tables are deferred.

## Dependency Impact

Allowed:

```text
codie.probability_engine.line_review
codie.probability_engine.reviewed_accuracy
standard library only
```

Forbidden:

```text
codie.providers
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
codie.db
requests
httpx
live network calls
raw SQL
```

Phase 13Z export functions should accept already-built summary/annotation
objects. They should not query the database directly.

## Export Boundary

Exports are local snapshots.

Allowed:

```text
produce JSON-compatible dictionaries
produce Markdown strings
produce deterministic bundle filenames/relative paths
include reviewed accuracy summary fields
include regression fixture payloads
include review_id, challenge_id, batch_id, result_id, trace_id when available
include action trace copies
include generated_at/exported_at metadata
```

Forbidden:

```text
write files directly
mutate simulation_line_reviews
mutate simulation_traces
mutate simulation_batch_results
import edited Markdown reviews
write analytics
write recommendations
call providers or network APIs
make strategic deckbuilding claims
```

File writing can be added later through a separate safe writer contract if
needed.

## Required JSON Payloads

Reviewed accuracy summary JSON fields:

```text
kind = reviewed_simulator_accuracy_summary
schema_version
summary
filters
generated_at
exported_at
```

Line review fixture JSON fields:

```text
kind = simulation_line_review_fixture
schema_version
review_id
challenge_id
deck_hash
target_condition
opening_hand
simulator_status
simulator_success
action_trace
review_status
review_reason
affected_cards
affected_actions
created_at
exported_at
```

Export bundle JSON fields:

```text
kind = simulation_review_export_bundle
schema_version
bundle_id
summary_path
markdown_path
fixture_paths
generated_at
exported_at
files
```

## Required Markdown Output

Summary Markdown fields:

```text
title
schema version
generated_at
exported_at
filters
total reviews
accepted successful lines
rejected successful lines
reviewed failures
reviewed unsupported
status counts
reason counts
affected card counts
affected action counts
```

Line review fixture Markdown fields:

```text
review_id
challenge_id
deck_hash
target card
target turn
simulator status
simulator success
review status
review reason
affected cards
affected actions
trace summary
```

Markdown must not include recommendation language.

## Determinism Rules

Given the same input summary, fixtures, and `exported_at`, Phase 13Z must
produce identical payloads.

Suggested deterministic IDs and paths:

```text
bundle_id = sha256 of summary payload + fixture review_ids + exported_at
summary_path = reviewed_accuracy_summary.json
markdown_path = reviewed_accuracy_summary.md
fixture path = fixtures/{review_id_without_prefix}.json
fixture markdown path = fixtures/{review_id_without_prefix}.md
```

All paths must be relative. Do not accept absolute output paths in Phase 13Z.

## Evidence-Language Rules

Allowed wording:

```text
3 successful simulator lines were accepted by review.
2 successful simulator lines were rejected by review.
1 reviewed line was marked mana_modeling_error.
4 reviewed traces affected tutor_search actions.
```

Forbidden wording:

```text
The simulator is authoritative.
The simulator made a strategic judgment.
A reviewed line proves a deckbuilding choice.
This review is tournament evidence.
The card choice is solved.
```

## Required Validation Tests For Phase 13Z

```text
summary exports JSON-compatible payload
summary exports Markdown
line review fixture exports JSON-compatible payload
line review fixture exports Markdown
bundle export contains deterministic bundle_id
bundle export contains relative paths only
same input and exported_at produce same output
payload preserves review_id/challenge_id/trace linkage
payload preserves action_trace copy
export does not mutate summary
export does not mutate fixture
export module does not import db/providers/analytics/recommendations
no raw SQL
no strategic claim language
full test suite passes
```

## Do Not Do In Phase 13Z

```text
Do not write files.
Do not build CLI.
Do not build UI.
Do not import edited reviews.
Do not add schema.
Do not generate recommendations.
Do not write analytics.
Do not treat reviews as tournament evidence.
Do not mutate simulator rows.
Do not add live network calls.
```

## Recommended Next Step

```text
Phase 13Z - Simulation Review Export Implementation
```

Implement pure JSON/Markdown export payload builders and deterministic bundle
metadata from already-built summary and fixture objects.
