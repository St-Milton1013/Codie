# Next Phase Contract

Recommended next task: Phase 11B - Saved Analysis Retrieval Checkpoint

## Current Status

Phase 11A is locally implemented and ready for validation.

Phase 11A added read-only saved-analysis listing/detail models plus CLI commands for deterministic JSON output. It completes the local user-deck workflow loop before UI, simulator integration, or final recommendation output.

## Files Created Or Modified In Latest Packet

- `codie/user_decks/__init__.py`
- `codie/user_decks/saved_analysis_listing.py`
- `codie/cli/user_deck.py`
- `tests/test_user_deck_saved_analysis_listing.py`
- `tests/test_cli_user_deck.py`
- `docs/PHASE11A_SAVED_ANALYSIS_RETRIEVAL_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `SavedAnalysisReadError`
- `SavedAnalysisSummary`
- `SavedAnalysisDetail`
- `list_saved_user_deck_analyses(...)`
- `get_saved_user_deck_analysis(...)`

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
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
```

## Known Caveats / Review Notes

- GitHub remote is configured and Phase 11 planning was pushed; Phase 11A still needs commit and push after validation.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- No UI exists yet.

## Recommended Next Packet

Phase 11B - Saved Analysis Retrieval Checkpoint.

Update checkpoint docs to include:

- saved-analysis retrieval/listing
- CLI list/show commands
- latest validation output
- Phase 11A contract reference
- remaining caveats

Keep final recommendation generation separate until the Phase 8/10 boundaries are explicitly carried forward.

## Do Not Do

- Do not build UI before saved-analysis retrieval/listing is accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations before updated Phase 10 outside validation.

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
