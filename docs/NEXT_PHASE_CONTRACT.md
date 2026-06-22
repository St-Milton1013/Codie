# Next Phase Contract

Recommended next task: Phase 9C - Export CLI Or Checkpoint Report Generator

## Current Status

Phase 9B is locally implemented and validated.

Phase 9B added deterministic file writers for accepted JSON-compatible export dictionaries and Markdown report strings. It did not add UI, schema, DB reads, providers, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/exports/writers.py`
- `codie/exports/__init__.py`
- `tests/test_exports_writers.py`
- `docs/PHASE9B_EXPORT_FILE_WRITER_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `ExportWriteResult`
- `write_json_export(...)`
- `write_markdown_export(...)`

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
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- Export writers are low-level helpers; no CLI exists yet.
- No UI exists yet.

## Recommended Next Packet

Phase 9C - Export CLI Or Checkpoint Report Generator.

Preferred next scope:

- generate a checkpoint Markdown report from already-built export payloads
- optionally add a tiny CLI only if it does not require packaging changes
- no DB access unless explicitly routed through repository methods and covered by contract

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
