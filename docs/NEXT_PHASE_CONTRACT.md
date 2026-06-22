# Next Phase Contract

Recommended next task: Phase 10H - CLI Checkpoint Update

## Current Status

Phase 10G is locally implemented and ready for validation.

Phase 10G added a small command-line wrapper for the accepted Phase 10 user deck workflow. It can bootstrap a SQLite database, import a deck text file, compare against optional evidence JSON, and write JSON/Markdown comparison exports. It did not add providers, source table reads, recommendations, UI, schema, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/cli/__init__.py`
- `codie/cli/user_deck.py`
- `tests/test_cli_user_deck.py`
- `docs/PHASE10G_USER_DECK_CLI_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `build_parser(...)`
- `main(...)`

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

- GitHub remote is configured and Phase 10F was pushed; Phase 10G still needs commit and push after validation.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- No UI exists yet.

## Recommended Next Packet

Phase 10H - CLI Checkpoint Update.

After Phase 10G validates, update:

- `docs/CHECKPOINT_PHASE10_USER_DECK_WORKFLOW_REPORT.md`

to include:

- CLI commands
- CLI validation results
- Phase 10G contract reference
- remaining caveats

## Do Not Do

- Do not build UI before CLI wrapper validation is accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations before updated Phase 10 validation.

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
