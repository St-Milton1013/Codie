# Next Phase Contract

Recommended next task: Phase 14C - Simulation Review Export Usage Documentation

## Current Status

Phase 13 through Phase 13Z is implemented, checkpointed, and externally
accepted with review notes.

Phase 14A and 14B are implemented:

```text
Simulation Review Export File Writer
Simulation Review Export CLI
```

The simulator review export track now includes:

```text
reviewed accuracy summaries
line review regression fixtures
pure JSON/Markdown export payload builders
deterministic export bundle metadata
safe local file writer for accepted bundles
CLI wrapper for writing accepted bundle JSON files
```

## Files Created Or Modified In Latest Packet

```text
codie/cli/simulation_review.py
tests/test_cli_simulation_review.py
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_CONTRACT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_REPORT.md
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
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\cli\simulation_review.py tests\test_cli_simulation_review.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\cli\simulation_review.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\cli\simulation_review.py tests\test_cli_simulation_review.py
```

## Known Caveats / Review Notes

- Challenge Mode has no UI yet.
- Simulator behavior coverage is intentionally narrow.
- Unsupported-card behavior must remain visible.
- Simulation results remain QA/training metadata, not tournament evidence.
- Final recommendation output remains intentionally separate.
- The Phase 14B CLI accepts already-built local bundle JSON only; it does not
  query DB, build review summaries, run simulations, or call providers.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 14C - Simulation Review Export Usage Documentation
```

Document how to:

```text
build a SimulationReviewExportBundle in Python
write the bundle JSON to a local file
run python -m codie.cli.simulation_review export-review-bundle
inspect manifest.json and fixture files
share the output as local review artifacts
```

Do not add schema, DB reads, provider calls, UI, recommendations, or simulator
behavior changes in Phase 14C.
