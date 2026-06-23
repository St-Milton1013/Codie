# Next Phase Contract

Recommended next task: Phase 12B - User Workflow View Model Checkpoint

## Current Status

Phase 12A is locally implemented and ready for validation.

Phase 12A added pure Python user workflow view models for saved-analysis list and detail pages. It did not scaffold frontend, install npm packages, read DB tables, call providers, generate recommendations, start simulator integration, or add schema.

## Files Created Or Modified In Latest Packet

- `codie/pages/__init__.py`
- `codie/pages/user_workflow.py`
- `tests/test_pages_user_workflow.py`
- `docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `UserWorkflowSummaryCard`
- `UserWorkflowTableRow`
- `UserWorkflowPageModel`
- `saved_analysis_detail_page_model(...)`
- `saved_analysis_list_page_model(...)`

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

- GitHub remote is configured and Phase 12 planning was pushed; Phase 12A still needs commit and push after validation.
- CLI requires a local Codie database with card rows before deck import can resolve cards.
- CLI export docs recommend `--output-root` for normal usage.
- No UI exists yet.

## Recommended Next Packet

Phase 12B - User Workflow View Model Checkpoint.

Update checkpoint docs to include:

- Phase 12 planning
- Phase 12A view models
- validation output
- boundary scans
- remaining caveats before UI scaffold

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
