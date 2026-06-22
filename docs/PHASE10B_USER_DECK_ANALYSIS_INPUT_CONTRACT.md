# Phase 10B - User Deck Analysis Input Builder

## Purpose

Build a read-only, deterministic analysis input object from an imported user deck.

This phase prepares the user deck for later comparison against analytics and recommendation evidence. It does not generate recommendations or read provider/source tables.

## Files Created Or Modified

- `codie/db/repositories/user.py`
- `codie/user_decks/__init__.py`
- `codie/user_decks/analysis_input.py`
- `tests/test_user_deck_analysis_input.py`
- `docs/PHASE10B_USER_DECK_ANALYSIS_INPUT_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `UserDeckAnalysisCard`
- `UserDeckAnalysisInput`
- `UserDeckAnalysisInputError`
- `build_user_deck_analysis_input(...)`
- `UserRepository.get_user_deck(...)`
- `UserRepository.list_user_deck_cards(...)`
- `UserRepository.get_analysis_session(...)`

## Schema Impact

None.

## Inputs

- `user_deck_id`
- optional `analysis_session_id`

## Outputs

`UserDeckAnalysisInput` includes:

- user deck identity
- optional analysis session identity
- deck name
- deck hash
- commander hash
- source URL
- temporary flag
- resolved cards
- unresolved cards
- mainboard count
- commander count
- total card count

## Dependencies

- `UserRepository`

## Boundary Rules

The analysis input builder must not import:

- providers
- source repositories
- ingestion
- analytics
- recommendations

The builder reads only user-analysis tables through `UserRepository`.

## Failure Modes

- Unknown user deck raises `UserDeckAnalysisInputError`.
- Unknown analysis session raises `UserDeckAnalysisInputError`.
- Analysis session belonging to another user deck raises `UserDeckAnalysisInputError`.
- User deck with no card rows raises `UserDeckAnalysisInputError`.

## Tests

Required test coverage:

- imported deck builds analysis input
- commander/mainboard/total counts are deterministic
- unresolved rows are exposed
- unknown deck fails cleanly
- session ownership mismatch fails cleanly

## Do Not Do

- Do not generate recommendations.
- Do not read provider/source tables.
- Do not calculate analytics.
- Do not add schema.
- Do not build UI.
