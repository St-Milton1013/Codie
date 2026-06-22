# Phase 11A - Saved Analysis Retrieval And Listing

## Purpose

Provide read-only retrieval and listing surfaces for saved user deck analyses.

This phase makes persisted Phase 10 summaries inspectable through stable models and CLI commands. It does not generate recommendations, call providers, read source/provider tables, add schema, build UI, or start simulator integration.

## Files Created Or Modified

- `codie/user_decks/__init__.py`
- `codie/user_decks/saved_analysis_listing.py`
- `codie/cli/user_deck.py`
- `tests/test_user_deck_saved_analysis_listing.py`
- `tests/test_cli_user_deck.py`
- `docs/PHASE11A_SAVED_ANALYSIS_RETRIEVAL_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `SavedAnalysisReadError`
- `SavedAnalysisSummary`
- `SavedAnalysisDetail`
- `list_saved_user_deck_analyses(...)`
- `get_saved_user_deck_analysis(...)`

CLI commands:

- `list-saved-analyses`
- `show-saved-analysis`

## Schema Impact

None.

Existing table used:

- `saved_analysis`

## Inputs

List:

- `user_deck_id`

Detail:

- `saved_analysis_id`

## Outputs

Summary rows include:

- saved analysis ID
- user deck ID
- deck hash
- analysis type
- generated timestamp
- report path

Detail rows additionally include:

- parsed summary JSON payload

## Boundary Rules

The listing helper may import:

- `UserRepository`
- standard library JSON parsing

It must not import:

- providers
- source repositories/tables
- analytics
- recommendations
- simulator
- UI

## Failure Modes

- Unknown saved analysis ID raises `SavedAnalysisReadError`.
- Malformed `summary_json` raises `SavedAnalysisReadError`.
- CLI invalid IDs fail cleanly through exceptions in tests.
- Retrieval is read-only and performs no writes.

## Tests

Required test coverage:

- list saved analyses for a user deck
- fetch saved analysis detail by ID
- missing saved analysis fails cleanly
- malformed summary JSON fails cleanly
- CLI list command prints deterministic JSON
- CLI show command prints deterministic JSON
- boundary import guard
- full suite passes

## Do Not Do

- Do not generate final recommendations.
- Do not calculate cuts.
- Do not start UI.
- Do not start simulator integration.
- Do not call providers.
- Do not read source/provider tables.
- Do not add schema.
