# Phase 12A - User Workflow View Models

## Purpose

Create display-ready, JSON-compatible view models for saved user workflow analyses.

This phase prepares future UI surfaces without scaffolding React/Vite or adding frontend dependencies. It does not read databases, call providers, generate final recommendations, start simulator integration, or add schema.

## Files Created Or Modified

- `codie/pages/__init__.py`
- `codie/pages/user_workflow.py`
- `tests/test_pages_user_workflow.py`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `UserWorkflowSummaryCard`
- `UserWorkflowTableRow`
- `UserWorkflowPageModel`
- `saved_analysis_detail_page_model(...)`
- `saved_analysis_list_page_model(...)`

## Schema Impact

None.

## Inputs

- `SavedAnalysisDetail`
- tuple of `SavedAnalysisSummary`

## Outputs

JSON-compatible page model dictionaries containing:

- title
- summary cards
- rows
- empty state
- generated timestamp
- evidence/source metadata

## Boundary Rules

The page model layer may import:

- user deck saved-analysis retrieval models

It must not import:

- providers
- DB/repositories/connections
- source/provider tables
- analytics
- recommendations
- simulator
- frontend packages

## Evidence-Only Rules

View models must preserve evidence-only language and reject/avoid strategic claims.

Forbidden phrasing:

- `should play`
- `must include`
- `correct card`
- `breaks the format`
- `secretly optimal`
- `cut this`

## Tests

Required test coverage:

- saved analysis detail becomes page model
- saved analysis list becomes page model
- empty saved analysis list has explicit empty state
- evidence source metadata is preserved
- generated timestamps are preserved
- forbidden strategic language is rejected
- page boundary scan passes
- full suite passes

## Do Not Do

- Do not scaffold frontend.
- Do not install npm packages.
- Do not add React/Vite/Tailwind yet.
- Do not build deck editing UI.
- Do not generate final recommendations.
- Do not call providers.
- Do not read source/provider tables.
- Do not add schema.
