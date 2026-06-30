# Next Phase Contract

Recommended next task: Phase 13X Reviewed Simulator Accuracy Implementation

## Current Status

Phase 13W Reviewed Simulator Accuracy Contract is documented.

Codie now has a contract for read-only reviewed simulator accuracy summaries
over persisted `simulation_line_reviews`. These summaries are simulator QA
metadata only. They do not rewrite raw simulator history, update analytics,
generate recommendations, or create tournament evidence.

This latest packet is contract-only.

## Files Created Or Modified In Latest Packet

```text
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
None. Latest packet is contract-only.
```

## Schema Impact

None.

Phase 13X must use the existing table:

```text
simulation_line_reviews
```

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "ReviewedAccuracy|reviewed_accuracy|list_line_reviews_for_accuracy" codie tests
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md docs\PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT_REPORT.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
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
- Reviewed-accuracy reports are contracted but not implemented.
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13X - Reviewed Simulator Accuracy Implementation
```

Implement:

```text
codie/probability_engine/reviewed_accuracy.py
tests/test_probability_engine_reviewed_accuracy.py
docs/PHASE13X_REVIEWED_SIMULATOR_ACCURACY_IMPLEMENTATION_REPORT.md
```

Allowed supporting changes:

```text
codie/db/repositories/simulation.py
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Required implementation rules:

```text
read simulation_line_reviews only
do not add schema
do not mutate reviews or simulator traces
do not write analytics or recommendations
classify accepted/rejected/failed/unsupported from stored fields
return counts, rates, filters, and generated_at
preserve evidence-language restrictions
```
