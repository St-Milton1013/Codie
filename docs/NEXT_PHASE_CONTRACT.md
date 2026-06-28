# Next Phase Contract

Recommended next task: Phase 12E Read-Only Local UI Data Contract

## Current Status

Phase 12D Minimal React/Vite Local UI Shell is implemented and ready for validation.

The UI scaffold under `ui/` renders fixture-backed saved-analysis list, detail,
and empty-state views while preserving the rule that UI consumes page models and
does not own data access.

## Files Created Or Modified In Latest Packet

- `.gitignore`
- `ui/`
- `docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md`
- `docs/CODEX_CONTINUITY_HANDOFF.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

None in Python. Frontend TypeScript interfaces were added under `ui/src/types/`.

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Frontend validation:

```powershell
cd ui
npm install
npm run build
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
rg -n "sqlite3|source_events|source_decks|provider_objects|codie\.providers|codie\.db|codie\.recommendations|codie\.analytics" ui
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this" ui
```

## Known Caveats / Review Notes

- GitHub remote is configured and Phase 12B was pushed.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- UI is fixture-backed only.
- No local UI API exists yet.

## Recommended Next Packet

Draft Phase 12E Read-Only Local UI Data Contract.

Validation reference:

- `docs/CODEX_CONTINUITY_HANDOFF.md`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`
- `docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md`
- `docs/PHASE12C_UI_SCAFFOLD_CONTRACT.md`
- `docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md`

Define:

```text
Phase 12E - Read-Only Local UI Data Contract
```

Keep final recommendation generation separate until the Phase 8/10 boundaries are explicitly carried forward.

## Do Not Do

- Do not scaffold UI before view models are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations before updated Phase 10 outside validation.
- Do not let UI access SQLite directly.
- Do not add a local API server without a contract.

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
