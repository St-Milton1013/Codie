# Phase 10C - User Deck Evidence Comparison Surface

## Purpose

Compare an imported user deck analysis input against generic evidence candidates and report whether each candidate card is already present or absent.

This phase is evidence-only. It does not generate final recommendations, rank deck changes, or use strategic claim language.

## Files Created Or Modified

- `codie/user_decks/__init__.py`
- `codie/user_decks/evidence_comparison.py`
- `tests/test_user_deck_evidence_comparison.py`
- `docs/PHASE10C_USER_DECK_EVIDENCE_COMPARISON_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `UserDeckEvidenceCandidate`
- `UserDeckEvidenceComparisonRow`
- `UserDeckEvidenceComparison`
- `compare_user_deck_to_evidence(...)`

## Schema Impact

None.

## Inputs

- `UserDeckAnalysisInput`
- tuple of `UserDeckEvidenceCandidate`
- `generated_at`

## Outputs

`UserDeckEvidenceComparison` includes:

- user deck identity
- deck hash
- commander hash
- comparison rows
- present count
- absent count
- generated timestamp

Each row includes:

- oracle identity
- card name
- evidence type
- present/absent status
- quantity in deck
- zones in deck
- optional score
- optional sample size
- source metadata
- evidence-only line

## Boundary Rules

The comparison module does not import:

- providers
- DB/repositories
- source tables
- analytics
- recommendations

It operates on already-built in-memory inputs only.

## Evidence-Only Language

Allowed:

- `Mystic Remora is absent in the imported user deck; evidence type commander_staple; sample size 42.`

Forbidden:

- `should play`
- `must include`
- `correct card`
- `breaks the format`
- `secretly optimal`

## Tests

Required test coverage:

- present/absent comparison
- quantity and zone reporting
- candidate score validation
- strategic claim language rejection
- missing generated timestamp failure
- boundary import guard

## Do Not Do

- Do not generate final recommendations.
- Do not calculate deck cuts.
- Do not read provider/source tables.
- Do not persist comparison rows yet.
- Do not add schema.
- Do not build UI.
