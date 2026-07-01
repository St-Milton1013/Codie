# Next Phase Contract

Recommended next task: Outside validation for Phase 14 Simulation Review Export

## Current Status

Phase 13 through Phase 13Z is implemented, checkpointed, and externally
accepted with review notes.

Phase 14A through 14C are implemented and checkpointed:

```text
Simulation Review Export File Writer
Simulation Review Export CLI
Simulation Review Export Usage Documentation
```

## Files Created Or Modified In Latest Packet

```text
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE14_SIMULATION_REVIEW_EXPORT_PROMPT.md
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
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py codie\cli\simulation_review.py tests\test_cli_simulation_review.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\probability_engine\review_export_writer.py codie\cli\simulation_review.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py codie\cli\simulation_review.py tests\test_cli_simulation_review.py docs\USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

## Outside Validation Packet

Send:

```text
docs/OUTSIDE_VALIDATION_PHASE14_SIMULATION_REVIEW_EXPORT_PROMPT.md
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
```

Recommended supporting docs:

```text
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_CONTRACT.md
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_REPORT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_CONTRACT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_REPORT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_REPORT.md
docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

## Known Caveats / Review Notes

- Challenge Mode has no UI yet.
- Simulator behavior coverage is intentionally narrow.
- Unsupported-card behavior must remain visible.
- Simulation results remain QA/training metadata, not tournament evidence.
- Final recommendation output remains intentionally separate.
- The Phase 14B CLI accepts already-built local bundle JSON only.
- Phase 14 does not add persisted export rows or import tracking.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet After Validation

```text
Phase 15 Planning Contract
```

Do not start Phase 15 implementation until Phase 14 outside validation returns
PASS or PASS WITH REVIEW NOTES.
