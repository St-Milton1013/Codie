# Next Phase Contract

Recommended next task: Phase 13Y Simulation Review Export Contract

## Current Status

Phase 13X Reviewed Simulator Accuracy Implementation is complete.

Codie can now summarize persisted `simulation_line_reviews` into read-only QA
metrics: accepted successful lines, rejected successful lines, reviewed
failures, reviewed unsupported results, status/reason counts, affected
card/action counts, rates, filters, and generation metadata.

These summaries are simulator QA metadata only. They do not rewrite raw
simulator history, update analytics, generate recommendations, or create
tournament evidence.

## Files Created Or Modified In Latest Packet

```text
codie/probability_engine/reviewed_accuracy.py
tests/test_probability_engine_reviewed_accuracy.py
docs/PHASE13X_REVIEWED_SIMULATOR_ACCURACY_IMPLEMENTATION_REPORT.md
codie/db/repositories/simulation.py
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
ReviewedAccuracyFilters
ReviewedAccuracySummary
ReviewStatusCount
ReviewReasonCount
build_reviewed_accuracy_summary(...)
summarize_line_review_rows(...)
```

Repository method added:

```text
SimulationRepository.list_line_reviews_for_accuracy(...)
```

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Focused Phase 13X tests:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest tests.test_probability_engine_reviewed_accuracy -v
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx" codie\probability_engine\reviewed_accuracy.py tests\test_probability_engine_reviewed_accuracy.py
rg -n "reviewed_accuracy|ReviewedAccuracySummary" codie\probability_engine\line_review.py codie\probability_engine\batch.py codie\probability_engine\search.py codie\probability_engine\challenge_mode.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\reviewed_accuracy.py tests\test_probability_engine_reviewed_accuracy.py
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
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13Y - Simulation Review Export Contract
```

Define export surfaces before implementation:

```text
reviewed accuracy JSON export
reviewed accuracy Markdown export
line review regression fixture bundle
Obsidian/vault-compatible notes if selected
no mutation of simulator rows
no recommendation or tournament-evidence claims
```
