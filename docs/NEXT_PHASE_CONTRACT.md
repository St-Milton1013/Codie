# Next Phase Contract

Recommended next task: Phase 10F - User Deck Workflow Checkpoint Report

## Current Status

Phase 10E is locally implemented and validated.

Phase 10E added safe file writers for already-built user deck comparison JSON and Markdown exports. It reuses existing export writer path and content-type validation. It did not add providers, source table reads, recommendations, UI, schema, DB access, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/exports/__init__.py`
- `codie/exports/user_deck_reports.py`
- `tests/test_exports_user_deck_reports.py`
- `docs/PHASE10E_USER_DECK_COMPARISON_FILE_WRITER_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `UserDeckComparisonWriteResult`
- `write_user_deck_comparison_exports(...)`

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
- User deck comparison file writers require caller-supplied paths.
- No UI exists yet.

## Recommended Next Packet

Phase 10F - User Deck Workflow Checkpoint Report.

This should summarize Phase 10A-10E for outside validation:

- user deck import
- analysis input builder
- evidence comparison
- export surface
- file writers
- validation results
- boundaries and remaining caveats

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations in Phase 10F.

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
