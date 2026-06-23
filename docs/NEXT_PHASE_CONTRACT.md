# Next Phase Contract

Recommended next task: Outside Validation - Phase 12 UI Preparation

## Current Status

Phase 12B is locally implemented and ready for validation.

Phase 12B added a checkpoint report for UI preparation and user workflow view models. It did not add code, providers, DB access, recommendations, UI scaffold, schema, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md`
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
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
```

## Known Caveats / Review Notes

- GitHub remote is configured and Phase 12A still needs push after checkpoint validation.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- No UI exists yet.

## Recommended Next Packet

Outside Validation - Phase 12 UI Preparation.

Send:

- `docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md`
- `docs/PHASE12_UI_PLANNING_CONTRACT.md`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`

Keep final recommendation generation separate until the Phase 8/10 boundaries are explicitly carried forward.

## Do Not Do

- Do not scaffold UI before view models are accepted.
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
