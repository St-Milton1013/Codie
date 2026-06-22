# Next Phase Contract

Recommended next task: Phase 10B - User Deck Analysis Input Builder

## Current Status

Phase 10A is locally implemented and validated.

Phase 10A added local user deck text parsing, card resolution, atomic persistence into user-analysis tables, and analysis-session creation. It did not add providers, source table reads, recommendations, UI, schema, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/user_decks/__init__.py`
- `codie/user_decks/importer.py`
- `tests/test_user_deck_import.py`
- `docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `ParsedUserDeckCard`
- `ParsedUserDeck`
- `UserDeckImportError`
- `UserDeckImportResult`
- `parse_user_deck_text(...)`
- `UserDeckImporter.import_text(...)`
- `UserDeckImporter.import_parsed(...)`

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- User deck import currently supports simple quantity/name text input and section headers.
- No UI exists yet.

## Recommended Next Packet

Phase 10B - User Deck Analysis Input Builder.

This should stay read-only and build the resolved user-deck view needed by later analysis:

- load one imported user deck through `UserRepository`
- return deck metadata, commander hash, and resolved cards
- expose unresolved/partial states if future import modes allow them
- prepare an input object for later recommendation/statistics comparison
- no recommendation generation yet

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate recommendations in Phase 10B.

## Required Phase Packet Shape

Every follow-up phase packet must include:

- contract document before code
- complete implementation files
- focused tests and fixture data where relevant
- full validation command and actual output
- static architecture checks where relevant
- completion report
- updated handoff or next-phase document
- clean commit after validation passes

Use this packet order:

```text
contract -> code -> tests -> validation -> completion report -> handoff -> commit
```
