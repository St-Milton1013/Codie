# Phase 12G - UI Fixture Loader / Generated Export Preview Contract

## Purpose

Let the local React/Vite UI load deterministic page-model export JSON files
created by Python, while preserving the Phase 12 boundary that the frontend is a
read-only static preview.

## Scope

```text
ui/src/
ui/public/page-models/
docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md
docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Files Created Or Modified

```text
ui/public/page-models/saved-analysis-list.json
ui/public/page-models/saved-analysis-detail.json
ui/src/data/pageModelLoader.ts
ui/src/types/userWorkflow.ts
ui/src/App.tsx
ui/src/styles.css
docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md
docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Types

```text
PageModelExport
PageModelLoadResult
loadPageModelExport(...)
validatePageModelExport(...)
```

## Schema Impact

None.

## Dependencies

- React state/effect hooks.
- Browser `fetch(...)` for static JSON only.
- Existing `UserWorkflowPageModel` UI type.
- Existing Phase 12F export wrapper shape.

## Runtime Rules

- The UI may load only static JSON files served by Vite/public hosting.
- The UI must not access SQLite.
- The UI must not call Codie Python modules.
- The UI must not call providers, recommendations, analytics, or source tables.
- The UI must fall back to checked-in fixture models if static export loading
  fails.
- The UI must disclose whether the displayed model came from generated export
  JSON or fallback fixture data.

## Supported URLs

Default static export paths:

```text
/page-models/saved-analysis-list.json
/page-models/saved-analysis-detail.json
```

Optional query parameters for local preview:

```text
?listModel=/page-models/saved-analysis-list.json
?detailModel=/page-models/saved-analysis-detail.json
```

## Required Tests / Validation

```text
npm run build
python -m unittest discover -s tests
git diff --check
rg boundary scans over ui/
forbidden recommendation-language scan over ui/
```

## Failure Modes

- Missing static export file: show fallback fixture data and loader status.
- Invalid export envelope: show fallback fixture data and loader status.
- Invalid page model shape: show fallback fixture data and loader status.

## Do Not Do

- Do not add a local API server.
- Do not let UI read SQLite.
- Do not import Codie backend modules into UI.
- Do not add strategic recommendation language.
- Do not persist UI state to Codie tables.
