# Next Phase Contract

Recommended next task: Phase 10E - User Deck Comparison File Writer

## Current Status

Phase 10D is locally implemented and validated.

Phase 10D added deterministic export helpers for already-built user deck evidence comparisons. It emits JSON-compatible dictionaries and evidence-only Markdown reports. It did not add providers, source table reads, recommendations, UI, schema, DB access, persistence, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/exports/__init__.py`
- `codie/exports/user_deck_reports.py`
- `tests/test_exports_user_deck_reports.py`
- `docs/PHASE10D_USER_DECK_COMPARISON_EXPORT_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `user_deck_comparison_export(...)`
- `user_deck_comparison_markdown(...)`

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
- User deck comparison exports are pure transforms and do not write files.
- No UI exists yet.

## Recommended Next Packet

Phase 10E - User Deck Comparison File Writer.

This should reuse existing export writers:

- write user deck comparison JSON export
- write user deck comparison Markdown report
- deterministic paths supplied by caller
- no DB access
- no recommendation generation
- no strategic recommendation language

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations in Phase 10E.

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
