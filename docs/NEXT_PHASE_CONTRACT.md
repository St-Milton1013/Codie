# Next Phase Contract

Recommended next task: Phase 13Z Simulation Review Export Implementation

## Current Status

Phase 13Y Simulation Review Export Contract is documented.

Codie now has a contract for pure JSON/Markdown export payload builders for
reviewed simulator accuracy summaries and line review fixtures. Exports remain
local read-only snapshots and do not write files, import edited reviews, mutate
simulator rows, update analytics, generate recommendations, or create
tournament evidence.

This latest packet is contract-only.

## Files Created Or Modified In Latest Packet

```text
docs/PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT.md
docs/PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
None. Latest packet is contract-only.
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
rg -n "SimulationReviewExport|review_export|simulation_review_summary_to" codie tests
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT.md docs\PHASE13Y_SIMULATION_REVIEW_EXPORT_CONTRACT_REPORT.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

## Known Caveats / Review Notes

- GitHub remote is configured.
- CLI requires a local Codie database with card rows before deck import can
  resolve cards.
- UI is fixture/static-page-model backed and remains read-only.
- Local report sharing and zip export are implemented.
- Simulator persistence is implemented for batch results.
- Challenge Mode is implemented without UI.
- Challenge Line Review annotations and persistence are implemented.
- Reviewed-accuracy summaries are implemented.
- Simulation review exports are contracted but not implemented.
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13Z - Simulation Review Export Implementation
```

Implement:

```text
codie/probability_engine/review_export.py
tests/test_probability_engine_review_export.py
docs/PHASE13Z_SIMULATION_REVIEW_EXPORT_IMPLEMENTATION_REPORT.md
```

Allowed supporting changes:

```text
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Required implementation rules:

```text
accept already-built summary/fixture objects
do not query DB
do not write files
emit JSON-compatible payloads
emit Markdown strings
produce deterministic bundle metadata
use relative paths only
preserve action trace copies
avoid recommendation or tournament-evidence language
```
