# Next Phase Contract

Recommended next task: Outside Validation - Phase 10 User Deck Workflow With CLI

## Current Status

Phase 10H is locally implemented and ready for validation.

Phase 10H updated the Phase 10 checkpoint report to include the accepted CLI wrapper. It did not add code, providers, source table reads, recommendations, UI, schema, DB access, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `docs/CHECKPOINT_PHASE10_USER_DECK_WORKFLOW_REPORT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

None. Documentation-only checkpoint update.

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

- GitHub remote is configured and Phase 10F was pushed; Phase 10G/10H still need push after validation.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- No UI exists yet.

## Recommended Next Packet

Outside Validation - Phase 10 User Deck Workflow With CLI.

Send:

- `docs/CHECKPOINT_PHASE10_USER_DECK_WORKFLOW_REPORT.md`
- `docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md`
- `docs/PHASE10B_USER_DECK_ANALYSIS_INPUT_CONTRACT.md`
- `docs/PHASE10C_USER_DECK_EVIDENCE_COMPARISON_CONTRACT.md`
- `docs/PHASE10D_USER_DECK_COMPARISON_EXPORT_CONTRACT.md`
- `docs/PHASE10E_USER_DECK_COMPARISON_FILE_WRITER_CONTRACT.md`
- `docs/PHASE10G_USER_DECK_CLI_CONTRACT.md`

## Do Not Do

- Do not build UI before CLI wrapper outside validation is accepted.
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
