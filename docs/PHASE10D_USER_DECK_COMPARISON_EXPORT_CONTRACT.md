# Phase 10D - User Deck Comparison Report Export

## Purpose

Export already-built user deck evidence comparisons as deterministic JSON-compatible payloads and Markdown reports.

This phase does not generate recommendations, read databases, call providers, or persist comparison rows.

## Files Created Or Modified

- `codie/exports/__init__.py`
- `codie/exports/user_deck_reports.py`
- `tests/test_exports_user_deck_reports.py`
- `docs/PHASE10D_USER_DECK_COMPARISON_EXPORT_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions

- `user_deck_comparison_export(...)`
- `user_deck_comparison_markdown(...)`

## Schema Impact

None.

## Inputs

- `UserDeckEvidenceComparison`

## Outputs

- deterministic JSON-compatible dictionary
- evidence-only Markdown report

## Boundary Rules

The export module may import user-deck comparison models.

It must not import:

- providers
- DB/repositories
- source tables
- analytics

## Evidence-Only Rules

The export must preserve comparison evidence without introducing strategic claims.

Forbidden phrasing includes:

- `should play`
- `must include`
- `correct card`
- `secretly optimal`

## Tests

Required test coverage:

- JSON-compatible payload shape
- Markdown report shape
- evidence-only language
- table escaping for pipe characters

## Do Not Do

- Do not generate final recommendations.
- Do not persist reports automatically.
- Do not read DB tables.
- Do not add schema.
- Do not build UI.
