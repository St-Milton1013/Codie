# Next Phase Contract

Recommended next task: Outside Validation - Phase 10 User Deck Workflow

## Current Status

Phase 10F is locally implemented and validated.

Phase 10F added a checkpoint report covering the Phase 10 user deck workflow from import through comparison export writing. It did not add code, providers, source table reads, recommendations, UI, schema, DB access, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `docs/CHECKPOINT_PHASE10_USER_DECK_WORKFLOW_REPORT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

None. Documentation-only checkpoint.

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
- Phase 10 should be sent for outside validation before UI or final recommendation output begins.
- No UI exists yet.

## Recommended Next Packet

Outside Validation - Phase 10 User Deck Workflow.

Send:

- `docs/CHECKPOINT_PHASE10_USER_DECK_WORKFLOW_REPORT.md`
- `docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md`
- `docs/PHASE10B_USER_DECK_ANALYSIS_INPUT_CONTRACT.md`
- `docs/PHASE10C_USER_DECK_EVIDENCE_COMPARISON_CONTRACT.md`
- `docs/PHASE10D_USER_DECK_COMPARISON_EXPORT_CONTRACT.md`
- `docs/PHASE10E_USER_DECK_COMPARISON_FILE_WRITER_CONTRACT.md`

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations before Phase 10 outside validation.

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
