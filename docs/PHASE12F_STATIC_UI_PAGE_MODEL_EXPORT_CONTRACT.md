# Phase 12F - Static UI Page Model Export Contract

## Purpose

Export saved-analysis page models as deterministic JSON files for the local UI.

The UI remains read-only and does not access SQLite. Python reads saved analysis
records through existing user workflow helpers, builds Phase 12A page models,
and writes JSON using the existing export writer guardrails.

## Files Created Or Modified

```text
codie/pages/export_user_workflow.py
codie/pages/__init__.py
codie/cli/user_deck.py
tests/test_pages_user_workflow_export.py
tests/test_cli_user_deck.py
docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md
docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions

```text
page_model_export_payload(...)
write_page_model_json(...)
export_saved_analysis_list_page_model(...)
export_saved_analysis_detail_page_model(...)
```

## CLI Commands

```text
export-ui-saved-analysis-list
export-ui-saved-analysis-detail
```

## Schema Impact

None.

## Dependencies

Allowed:

```text
codie.user_decks saved-analysis retrieval helpers
codie.pages user workflow page models
codie.exports write_json_export
codie.db connection and UserRepository only inside CLI
```

Forbidden:

```text
providers
recommendations
analytics
source/provider tables
UI SQLite access
local API server
schema changes
```

## Required Output Shape

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

## Tests

Required:

```text
exports saved-analysis list page model JSON
exports saved-analysis detail page model JSON
empty saved-analysis list exports explicit empty state
export includes page_model_version and exported_at
export preserves generated_at
export preserves evidence/source metadata
output_root containment rejects outside path
CLI commands write deterministic JSON
CLI commands do not import providers/recommendations/analytics
focused tests pass
full suite passes
UI build passes
static scans pass
```
