# Next Phase Contract

Recommended next task: Phase 12H Local Report Share Bundle

## Current Status

Phase 12G UI Fixture Loader / Generated Export Preview is implemented and
validated.

The UI can now load Phase 12F page-model export envelopes from static JSON
under `ui/public/page-models/`, with fixture fallback and visible source
status. Frontend code still does not access SQLite, providers, analytics, or
recommendations.

## Files Created Or Modified In Latest Packet

- `.gitignore`
- `ui/`
- `docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md`
- `docs/PHASE12E_READ_ONLY_UI_DATA_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md`
- `codie/pages/export_user_workflow.py`
- `codie/pages/__init__.py`
- `codie/cli/user_deck.py`
- `tests/test_pages_user_workflow_export.py`
- `tests/test_cli_user_deck.py`
- `ui/public/page-models/saved-analysis-list.json`
- `ui/public/page-models/saved-analysis-detail.json`
- `ui/src/data/pageModelLoader.ts`
- `ui/src/types/userWorkflow.ts`
- `ui/src/App.tsx`
- `ui/src/styles.css`
- `docs/CODEX_CONTINUITY_HANDOFF.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

Static UI export loading types/functions were added.

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
- UI loads static generated page-model JSON with fixture fallback.
- No local UI API exists yet by design.

## Recommended Next Packet

Implement Phase 12H Local Report Share Bundle.

Validation reference:

- `docs/CODEX_CONTINUITY_HANDOFF.md`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`
- `docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md`
- `docs/PHASE12C_UI_SCAFFOLD_CONTRACT.md`
- `docs/PHASE12D_MINIMAL_UI_SHELL_REPORT.md`
- `docs/PHASE12E_READ_ONLY_UI_DATA_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_CONTRACT.md`
- `docs/PHASE12F_STATIC_UI_PAGE_MODEL_EXPORT_REPORT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_CONTRACT.md`
- `docs/PHASE12G_UI_FIXTURE_LOADER_REPORT.md`

Define:

```text
Phase 12H - Local Report Share Bundle
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
- Do not make frontend fixtures private user deck data.
- Do not add hosted/mobile sharing without a separate privacy contract.

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
