# Next Phase Contract

Recommended next task: Phase 9B - Export File Writer / CLI Wrapper

## Current Status

Phase 9A is locally implemented and validated.

Phase 9A added deterministic JSON-compatible and Markdown export helpers for recommendation runs and innovation snapshots. It did not add UI, schema, providers, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/exports/__init__.py`
- `codie/exports/reports.py`
- `tests/test_exports_reports.py`
- `docs/PHASE9A_REPORT_EXPORT_SURFACE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `ExportMetadata`
- `export_recommendation_run_json(...)`
- `export_innovation_snapshot_json(...)`
- `recommendation_run_markdown(...)`
- `innovation_snapshot_markdown(...)`
- `outside_review_markdown(...)`

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
rg -n "codie\.providers|codie\.ingestion|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- Export helpers are pure in-memory transforms; no file writer or CLI exists yet.
- No UI exists yet.

## Recommended Next Packet

Phase 9B - Export File Writer / CLI Wrapper.

## Phase 9B Objective

Add a thin, deterministic wrapper that writes accepted export dictionaries/Markdown strings to disk.

Likely outputs:

- JSON file writer
- Markdown file writer
- safe path handling
- optional small CLI entry point if project structure supports it

## Do Not Do

- Do not build UI.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not add schema.
- Do not start simulator integration.

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
