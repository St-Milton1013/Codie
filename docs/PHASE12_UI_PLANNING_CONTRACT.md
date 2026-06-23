# Phase 12 - UI Planning Contract

## Verdict

```text
Recommended next implementation: Phase 12A - User Workflow View Models
Do not scaffold React/Vite UI yet.
```

## Purpose

Phase 12 prepares for Codie's eventual UI without letting the UI become a data owner.

The next safe step is not a frontend scaffold. It is an application/view-model layer that transforms already accepted user workflow objects into stable display-ready dictionaries. This gives the future React UI something clean to consume while preserving architecture boundaries.

## Constitution Anchors

UI technology decision:

```text
Frontend Framework: React with TypeScript
Build Tool: Vite
Styling: Tailwind CSS
UI Component Library: shadcn/ui / Radix primitives
Desktop Packaging: Electron or Tauri deferred until UI is functional
```

Dependency rules:

```text
ui -> application services / repositories read methods
ui -> never raw SQL
pages -> repositories read methods
pages -> analytics read methods
pages -> evidence read methods
```

Codie is not a deckbuilder:

```text
No drag/drop builder.
No card editing surface.
User returns to Moxfield or another deckbuilder to edit.
```

Evidence-first:

```text
Displayed evidence must include source attribution, formula/context when available, sample size, generated_at, and provenance.
```

## Decision

Proceed with:

```text
Phase 12A - User Workflow View Models
```

Defer:

- React/Vite scaffold
- Tauri/Electron packaging
- simulator UI
- final recommendation UI
- deck editing UI

## Why 12A Comes Next

Phase 10 and Phase 11 now provide:

- user deck import
- analysis input
- evidence comparison
- export and file writing
- saved analysis persistence
- saved analysis retrieval/listing
- CLI wrappers

The missing pre-UI layer is display shaping:

- summary cards
- table rows
- evidence lines
- source references
- empty/error states
- deterministic JSON-compatible payloads for a future UI

This layer can be tested without frontend tooling and without touching database ownership boundaries.

## Phase 12A Scope

Likely files:

- `codie/pages/__init__.py`
- `codie/pages/user_workflow.py`
- `tests/test_pages_user_workflow.py`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

Likely public models/functions:

- `UserWorkflowSummaryCard`
- `UserWorkflowTableRow`
- `UserWorkflowPageModel`
- `saved_analysis_detail_page_model(...)`
- `saved_analysis_list_page_model(...)`

## Schema Impact

None.

## Dependencies

Allowed:

- user deck saved-analysis retrieval models
- standard library only

Forbidden:

- providers
- source repositories/tables
- raw SQL
- DB connections
- analytics writes
- recommendations generation
- simulator
- React/Vite/frontend packages

## View Model Rules

View models must:

- be deterministic
- be JSON-compatible
- preserve evidence-only language
- preserve source IDs/URLs where available
- include generated timestamps where available
- represent empty states explicitly
- never produce strategic recommendation language

Forbidden phrases:

- `should play`
- `must include`
- `correct card`
- `breaks the format`
- `secretly optimal`
- `cut this`

## Tests Required For Phase 12A

- saved analysis detail becomes page model
- saved analysis list becomes page model
- empty saved analysis list has explicit empty state
- evidence source metadata is preserved
- generated timestamps are preserved
- forbidden strategic language is rejected or absent
- page layer boundary scan passes
- full suite passes

## Do Not Do In Phase 12A

- Do not scaffold frontend.
- Do not install npm packages.
- Do not add React/Vite/Tailwind yet.
- Do not build deck editing UI.
- Do not generate final recommendations.
- Do not call providers.
- Do not read source/provider tables.
- Do not add schema.

## Later Phase Candidates

After 12A:

- Phase 12B - User Workflow Page Export/Preview Fixture
- Phase 12C - UI Scaffold Contract
- Phase 12D - Minimal React/Vite Local UI Shell
- Phase 13 - Simulator Contract Refresh

The frontend scaffold should only start after the page/view-model layer is accepted.
