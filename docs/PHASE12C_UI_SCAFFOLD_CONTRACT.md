# Phase 12C - UI Scaffold Contract

## Verdict

```text
Recommended next implementation after outside validation: Phase 12D - Minimal React/Vite Local UI Shell
```

This contract defines the first UI scaffold. It does not authorize final
recommendation output, simulator integration, provider calls, raw SQL, or deck
editing features.

## Purpose

Create a minimal React + TypeScript + Vite frontend shell that can render static
or fixture-backed Codie page models produced by the Python application layer.

The UI must be a consumer of display-ready page models. It must not own data
retrieval, database access, source ingestion, provider access, analytics, or
recommendation generation.

## Constitution Anchors

Locked UI stack:

```text
Frontend Framework: React with TypeScript
Build Tool: Vite
Styling: Tailwind CSS
UI Component Library: shadcn/ui / Radix primitives when introduced
Desktop Packaging: Electron or Tauri deferred until UI is functional
```

Boundary rules:

```text
UI consumes page/application models.
UI never uses raw SQL.
UI never calls providers.
UI never reads source/provider tables.
UI never generates final recommendations.
UI never becomes a deckbuilder.
```

Evidence rules:

```text
Displayed evidence preserves source, sample size, generated_at, and provenance.
Displayed wording remains evidence-oriented.
Forbidden strategic claims are blocked or absent.
```

## Phase 12C Scope

Files to create or modify:

```text
docs/PHASE12C_UI_SCAFFOLD_CONTRACT.md
docs/NEXT_PHASE_CONTRACT.md
```

No frontend files are created in Phase 12C. This phase is the scaffold contract
only.

## Phase 12D Expected Implementation Scope

Likely files after this contract is accepted:

```text
ui/
ui/package.json
ui/package-lock.json
ui/index.html
ui/tsconfig.json
ui/tsconfig.node.json
ui/vite.config.ts
ui/src/main.tsx
ui/src/App.tsx
ui/src/styles.css
ui/src/types/userWorkflow.ts
ui/src/fixtures/savedAnalysisList.json
ui/src/fixtures/savedAnalysisDetail.json
ui/src/components/
ui/src/pages/
docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md
```

Package choices:

```text
react
react-dom
vite
typescript
@vitejs/plugin-react
tailwindcss only if configured completely in the same packet
```

Do not introduce shadcn/ui until the base Vite shell is stable, unless the
packet fully configures it and tests the generated components.

## Public Interface

The UI should initially consume JSON-compatible page model shapes equivalent to:

```text
UserWorkflowPageModel
UserWorkflowSummaryCard
UserWorkflowTableRow
```

Initial frontend types should mirror the Python page model fields without
inventing new data contracts.

## Data Source For First UI Shell

Allowed:

```text
checked-in non-sensitive fixture JSON generated from test page models
static mock fixture matching Phase 12A model shape
future local API endpoint after a separate backend contract
```

Forbidden:

```text
direct SQLite access from UI
source/provider table reads
provider calls
live backfills
recommendation generation
simulator calls
private user deck fixtures
```

## Required Initial Screens

Minimum Phase 12D UI shell:

```text
Saved analyses list view
Saved analysis detail view
Empty state view
Evidence/source metadata display
Generated timestamp display
```

Not required in first shell:

```text
deck import form
deck editing
final recommendations
simulation UI
provider status UI
settings/auth
mobile delivery
Moxfield upload
LLM naming review
```

## Design Requirements

The first UI should feel like a local evidence dashboard, not a landing page.

Required style direction:

```text
dense but readable information layout
clear page title and status region
summary cards for stable facts
tables or lists for saved analyses
source/provenance metadata visible near evidence
restrained color palette
mobile-responsive layout
no marketing hero
no decorative card nesting
no strategic recommendation language
```

## Test Requirements For Phase 12D

Required validation:

```text
npm install succeeds or package lock is committed from a successful install
npm run build succeeds
TypeScript compilation succeeds
fixture page renders list state
fixture page renders detail state
fixture page renders empty state
forbidden strategic phrases do not appear in UI source or fixtures
UI source contains no provider/db/sqlite imports
Python full suite still passes
git diff --check passes
```

Static scans:

```powershell
rg -n "sqlite3|source_events|source_decks|provider_objects|codie\.providers|codie\.db|codie\.recommendations|codie\.analytics" ui
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this" ui
```

Expected result:

```text
no matches
```

## Failure Modes

The UI shell must handle:

```text
empty saved analysis list
missing optional source URL
missing optional generated_at
malformed fixture shape during development
build failure due to type mismatch
```

Do not swallow malformed fixture issues silently during development.

## Schema Impact

None.

## Backend/API Impact

None in Phase 12C.

Phase 12D should use static fixtures only unless a separate local API contract is
accepted first.

## Do Not Do

```text
Do not scaffold UI before this contract is accepted.
Do not add Electron/Tauri packaging yet.
Do not add a local API server in the same packet unless separately contracted.
Do not call providers.
Do not read source/provider tables.
Do not generate final recommendations.
Do not implement simulator UI.
Do not add deck editing.
Do not add schema.
Do not upload to Moxfield.
Do not add cloud services.
```

## Completion Report Requirements For Phase 12D

The implementation report must include:

```text
files created
files modified
frontend dependencies added
commands run
actual npm build output
actual Python test output
static scan output
screens/views implemented
known caveats
next recommended packet
```
