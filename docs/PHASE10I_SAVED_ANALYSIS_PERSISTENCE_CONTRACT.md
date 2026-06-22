# Phase 10I - Saved Analysis Persistence

## Purpose

Persist already-built user deck comparison summaries into the existing `saved_analysis` table.

This phase stores evidence-only analysis summaries and optional report paths. It does not generate final recommendations, call providers, read source/provider tables, add schema, or build UI.

## Files Created Or Modified

- `codie/db/repositories/user.py`
- `codie/user_decks/__init__.py`
- `codie/user_decks/saved_analysis.py`
- `tests/test_user_deck_saved_analysis.py`
- `docs/PHASE10I_SAVED_ANALYSIS_PERSISTENCE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `SavedUserDeckAnalysisResult`
- `save_user_deck_comparison_analysis(...)`
- `UserRepository.create_saved_analysis(...)`
- `UserRepository.get_saved_analysis(...)`
- `UserRepository.list_saved_analysis_for_deck(...)`

## Schema Impact

None.

Existing table used:

- `saved_analysis`

## Inputs

- `UserDeckEvidenceComparison`
- optional report path
- optional analysis type

## Persisted Fields

- `user_deck_id`
- `deck_hash`
- `analysis_type`
- `generated_at`
- `summary_json`
- `report_path`

## Summary JSON Shape

The summary includes:

- user deck identity
- deck hash
- commander hash
- present count
- absent count
- generated timestamp
- evidence-only comparison rows

Rows include:

- oracle identity
- card name
- evidence type
- present/absent status
- quantity in deck
- zones
- score
- sample size
- source metadata
- evidence line

## Boundary Rules

The saved analysis helper may import:

- `UserRepository`
- user deck evidence comparison models

It must not import:

- providers
- source repositories/tables
- analytics
- recommendations
- DB connection/bootstrap

## Evidence-Only Rules

Saved summaries must preserve evidence-only comparison language and must not introduce strategic claims.

Forbidden phrasing includes:

- `should play`
- `must include`
- `correct card`
- `breaks the format`
- `secretly optimal`

## Failure Modes

- Missing comparison object fails naturally before persistence.
- Repository required-field validation rejects incomplete rows.
- Foreign key enforcement rejects invalid `user_deck_id` values.

## Tests

Required test coverage:

- comparison summary persists to `saved_analysis`
- saved row can be fetched by ID
- saved rows can be listed for a user deck
- optional report path persists
- evidence-only language remains intact
- invalid user deck FK fails cleanly
- boundary import guard

## Do Not Do

- Do not generate final recommendations.
- Do not call providers.
- Do not read source/provider tables.
- Do not add schema.
- Do not build UI.
