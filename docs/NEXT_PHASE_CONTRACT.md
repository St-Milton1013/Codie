# Next Phase Contract

Recommended next task: Phase 10C - User Deck Evidence Comparison Surface

## Current Status

Phase 10B is locally implemented and validated.

Phase 10B added a read-only analysis input builder for imported user decks. It loads user deck metadata, cards, commander hash, counts, and unresolved rows through `UserRepository`. It did not add providers, source table reads, recommendations, UI, schema, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/user_decks/__init__.py`
- `codie/user_decks/analysis_input.py`
- `codie/db/repositories/user.py`
- `tests/test_user_deck_analysis_input.py`
- `docs/PHASE10B_USER_DECK_ANALYSIS_INPUT_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `UserDeckAnalysisCard`
- `UserDeckAnalysisInput`
- `UserDeckAnalysisInputError`
- `build_user_deck_analysis_input(...)`
- `UserRepository.get_user_deck(...)`
- `UserRepository.list_user_deck_cards(...)`
- `UserRepository.get_analysis_session(...)`

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
- User deck analysis input is read-only and does not generate recommendations.
- No UI exists yet.

## Recommended Next Packet

Phase 10C - User Deck Evidence Comparison Surface.

This should stay evidence-only and compare a resolved user deck input against already-built recommendation/statistics evidence:

- identify cards already present in the user deck
- identify evidence candidates absent from the deck
- separate staple, innovation, and evidence-count signals if available
- preserve source/evidence metadata
- no strategic recommendation language yet

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations in Phase 10C.

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
