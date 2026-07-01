# Next Phase Contract

Recommended next task: Phase 14B - Simulation Review Export CLI Contract

## Current Status

Phase 13 through Phase 13Z is implemented, checkpointed, and externally
accepted with review notes.

Phase 14A is implemented:

```text
Simulation Review Export File Writer
```

The simulator review export track now includes:

```text
reviewed accuracy summaries
line review regression fixtures
pure JSON/Markdown export payload builders
deterministic export bundle metadata
safe local file writer for accepted bundles
```

## Files Created Or Modified In Latest Packet

```text
codie/probability_engine/review_export_writer.py
codie/probability_engine/__init__.py
tests/test_probability_engine_review_export_writer.py
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_CONTRACT.md
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

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
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\probability_engine\review_export_writer.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py
```

## Known Caveats / Review Notes

- Challenge Mode has no UI yet.
- Simulator behavior coverage is intentionally narrow.
- Unsupported-card behavior must remain visible.
- Simulation results remain QA/training metadata, not tournament evidence.
- Final recommendation output remains intentionally separate.
- The Phase 14A writer accepts already-built bundles only; it does not query DB
  or build export payloads.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 14B - Simulation Review Export CLI Contract
```

Define a command-line wrapper for writing already-built simulator review export
bundles. Keep the CLI boundary narrow:

```text
read accepted local bundle JSON
write bundle files under explicit output root
print written file manifest
no DB reads
no providers
no simulator mutation
no recommendations
```
