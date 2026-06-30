# Next Phase Contract

Recommended next task: Outside validation for Phase 13 Simulator Track

## Current Status

Phase 13 through Phase 13Z is implemented and checkpointed.

The simulator track now includes:

```text
core probability engine models
card definition manager
deck/target parser
seeded shuffle/opening hands
mulligan policy
target access search
Monte Carlo batch runner
simulator persistence
Challenge Mode
line review annotations
line review persistence
reviewed accuracy summaries
simulation review export payload builders
```

## Files Created Or Modified In Latest Packet

```text
docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE13_SIMULATOR_PROMPT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None in this checkpoint packet.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx" codie\probability_engine\review_export.py tests\test_probability_engine_review_export.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\probability_engine\review_export.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\review_export.py tests\test_probability_engine_review_export.py
```

## Outside Validation Packet

Send:

```text
docs/OUTSIDE_VALIDATION_PHASE13_SIMULATOR_PROMPT.md
docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
```

Recommended supporting docs:

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13Z_SIMULATION_REVIEW_EXPORT_IMPLEMENTATION_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Known Caveats / Review Notes

- Challenge Mode has no UI yet.
- Simulator review exports are payload builders only; no file writer yet.
- Simulator behavior coverage is intentionally narrow.
- Unsupported-card behavior must remain visible.
- Simulation results remain QA/training metadata, not tournament evidence.
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet After Validation

```text
Phase 14 Planning Contract
```

Do not start Phase 14 implementation until Phase 13 outside validation returns
PASS or PASS WITH REVIEW NOTES.
