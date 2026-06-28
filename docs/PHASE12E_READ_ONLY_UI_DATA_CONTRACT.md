# Phase 12E - Read-Only Local UI Data Contract

## Verdict

```text
Recommended next implementation: Phase 12F - Static Page Model Export For UI
```

This contract defines how the UI can receive real saved-analysis page models
without letting frontend code own data access.

## Purpose

Move the UI from checked-in static preview fixtures toward local, user-generated
page model data while preserving Codie's architecture boundaries.

The frontend must remain a consumer of display-ready JSON page models. Python
continues to own database reads, repository usage, validation, and page-model
construction.

## Constitution Anchors

```text
UI consumes application/page models.
UI never issues raw SQL.
UI never imports or calls providers.
UI never reads source/provider tables.
UI never generates final recommendations.
User deck workflows are local user-layer artifacts, not tournament evidence.
Displayed evidence preserves source, sample size, generated_at, and provenance.
```

## Preferred Implementation Path

Phase 12F should implement static JSON export first, not a web API.

Reason:

```text
Static export keeps the UI read-only.
Static export avoids local server/security decisions.
Static export reuses existing saved-analysis retrieval and page models.
Static export is easy to validate and share.
```

Later local API work may be added under a separate contract after static export
is accepted.

## Phase 12E Scope

Files to create or modify:

```text
docs/PHASE12E_READ_ONLY_UI_DATA_CONTRACT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

No Python or frontend implementation files are changed in Phase 12E.

## Phase 12F Expected Implementation Scope

Likely files:

```text
codie/pages/export_user_workflow.py
codie/pages/__init__.py
codie/cli/user_deck.py
tests/test_pages_user_workflow_export.py
tests/test_cli_user_deck.py
docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md
docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md
```

Optional UI follow-up after 12F:

```text
ui/src/data/pageModelLoader.ts
ui/src/fixtures/generated/README.md
```

## Public API Shape

Expected Python functions:

```text
export_saved_analysis_list_page_model(...)
export_saved_analysis_detail_page_model(...)
write_page_model_json(...)
```

Expected CLI commands:

```text
export-ui-saved-analysis-list
export-ui-saved-analysis-detail
```

The exact names may change in the implementation contract, but the boundary
must remain:

```text
database/repository reads -> saved-analysis retrieval -> page model -> JSON file
```

## Data Flow

Allowed:

```text
Python reads saved_analysis through existing user workflow retrieval helpers.
Python builds Phase 12A page models.
Python writes JSON files with export writer containment rules.
UI loads JSON page model files.
UI renders the JSON.
```

Forbidden:

```text
UI reading SQLite
UI importing Python modules directly
UI calling providers
UI reading source/provider tables
UI generating recommendations
UI mutating saved_analysis
UI writing user_decks or analysis_sessions
```

## Output Requirements

Exported JSON must include:

```text
page_model_version
exported_at
source
title
generated_at
summary_cards
rows
empty_state
```

The `source` object should include:

```text
export_type
saved_analysis_id when applicable
user_deck_id when applicable
deck_hash when available
analysis_type when available
```

All exported rows must preserve evidence/source metadata already present in the
page model.

## File Safety

Static JSON export must use existing export-writer containment rules or an
equivalent output-root guard.

Required behavior:

```text
default to explicit output path
recommend --output-root for normal CLI use
reject paths outside output_root
write UTF-8 JSON
create parent directories safely
produce deterministic key ordering
```

## CLI Examples

Expected usage shape:

```powershell
python -m codie.cli.user_deck export-ui-saved-analysis-list `
  --db codie.sqlite `
  --user-deck-id 7 `
  --output outputs/ui/saved-analyses.json `
  --output-root outputs
```

```powershell
python -m codie.cli.user_deck export-ui-saved-analysis-detail `
  --db codie.sqlite `
  --saved-analysis-id 1 `
  --output outputs/ui/saved-analysis-1.json `
  --output-root outputs
```

## Test Requirements For Phase 12F

Required tests:

```text
exports saved-analysis list page model JSON
exports saved-analysis detail page model JSON
empty saved-analysis list exports explicit empty state
export includes page_model_version and exported_at
export preserves generated_at
export preserves evidence/source metadata
output_root containment rejects outside path
malformed saved summary fails cleanly
unknown saved_analysis id fails cleanly
CLI commands write deterministic JSON
CLI commands do not import providers/recommendations/analytics
UI still builds
Python full suite passes
```

Static scans:

```powershell
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\pages codie\cli
rg -n "sqlite3|source_events|source_decks|provider_objects|codie\.providers|codie\.db|codie\.recommendations|codie\.analytics" ui
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this" ui codie\pages
```

## Later Local API Option

A later local API may expose these same page models, but only under a separate
contract.

If implemented later, the API must:

```text
bind to localhost by default
be read-only for UI endpoints
return page models only
avoid exposing raw SQL or repository concepts
avoid provider calls
avoid source/provider table reads
avoid recommendation generation
document CORS behavior
document shutdown/startup behavior
```

## Schema Impact

None.

## Do Not Do

```text
Do not add schema.
Do not let UI access SQLite.
Do not start a local API in Phase 12F unless separately contracted.
Do not call providers.
Do not read source/provider tables from UI.
Do not generate final recommendations.
Do not implement simulator UI.
Do not add deck editing.
Do not upload to Moxfield.
Do not add cloud services.
```

## Completion Report Requirements For Phase 12F

The implementation report must include:

```text
files created
files modified
public functions/classes
CLI commands
schema impact
commands run
actual Python test output
actual UI build output
static scan output
export examples
known caveats
next recommended packet
```
