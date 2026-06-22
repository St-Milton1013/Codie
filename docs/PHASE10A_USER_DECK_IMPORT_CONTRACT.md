# Phase 10A - User Deck Import / Analysis Contract

## Purpose

Import local user deck text into Codie's existing user-analysis tables so later analysis can run against a resolved, temporary deck context.

This phase does not generate recommendations, read provider/source tables, canonicalize user decks, or add schema.

## Files Created Or Modified

- `codie/user_decks/__init__.py`
- `codie/user_decks/importer.py`
- `tests/test_user_deck_import.py`
- `docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `ParsedUserDeckCard`
- `ParsedUserDeck`
- `UserDeckImportError`
- `UserDeckImportResult`
- `parse_user_deck_text(...)`
- `UserDeckImporter.import_text(...)`
- `UserDeckImporter.import_parsed(...)`

## Accepted Input

The importer accepts simple deck text with one card per line:

```text
Commander
1 Tymna the Weaver
1 Kraum, Ludevic's Opus

Mainboard
1 Jeweled Lotus
1 Rhystic Study
```

Recognized sections:

- `commander`
- `commanders`
- `partner`
- `partners`
- `main`
- `mainboard`
- `deck`
- `cards`
- `sideboard`
- `maybeboard`
- `considering`

Card rows must use:

```text
<quantity> <card name>
```

## Schema Impact

None.

Existing tables used:

- `user_decks`
- `user_deck_cards`
- `analysis_sessions`

## Dependencies

- `codie.cards.lookup.CardLookup`
- `codie.canonical.signature.commander_signature`
- `codie.db.repositories.user.UserRepository`
- `codie.db.repositories.base.BaseRepository.transaction`

## Boundary Rules

The user deck import layer must not import:

- providers
- source repositories
- ingestion
- analytics
- recommendations

It writes only through `UserRepository`.

## Failure Modes

- Empty input raises `UserDeckImportError`.
- Malformed card rows raise `UserDeckImportError`.
- Invalid quantity raises `UserDeckImportError`.
- Unresolved card names raise `UserDeckImportError`.
- Any unresolved card aborts the full import before user rows are persisted.

## Atomicity

User deck import uses an explicit savepoint transaction.

If any failure occurs during persistence, the following must all remain absent:

- `user_decks`
- `user_deck_cards`
- `analysis_sessions`

## Tests

Required test coverage:

- section parsing
- successful deck import
- card resolution persistence
- commander signature persistence
- analysis session creation
- unresolved card rollback
- malformed input failure
- boundary import guard

## Do Not Do

- Do not generate recommendations.
- Do not read provider/source tables.
- Do not canonicalize user decks.
- Do not add schema.
- Do not store strategic claims.
