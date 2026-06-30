# Next Phase Contract

Recommended next task: Phase 13 Checkpoint - Simulator Track Validation Packet

## Current Status

Phase 13Z Simulation Review Export Implementation is complete.

Codie now has pure JSON/Markdown export payload builders for reviewed simulator
accuracy summaries and line review fixtures. The export layer creates local
snapshot payloads and deterministic bundle metadata without querying databases,
writing files, mutating simulator rows, updating analytics, or generating
recommendations.

## Files Created Or Modified In Latest Packet

```text
codie/probability_engine/review_export.py
tests/test_probability_engine_review_export.py
docs/PHASE13Z_SIMULATION_REVIEW_EXPORT_IMPLEMENTATION_REPORT.md
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
REVIEW_EXPORT_SCHEMA_VERSION
SimulationReviewExportBundle
SimulationReviewMarkdownDocument
simulation_review_summary_to_json_payload(...)
simulation_review_summary_to_markdown(...)
line_review_fixture_to_json_payload(...)
line_review_fixture_to_markdown(...)
build_simulation_review_export_bundle(...)
```

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Focused Phase 13Z tests:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest tests.test_probability_engine_review_export -v
```

Static checks:

```text
git diff --check
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx" codie\probability_engine\review_export.py tests\test_probability_engine_review_export.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\probability_engine\review_export.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\review_export.py tests\test_probability_engine_review_export.py
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
- Simulation review export payload builders are implemented.
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13 Checkpoint - Simulator Track Validation Packet
```

Prepare a consolidated validation report and outside-check prompt covering:

```text
Phase 13A through Phase 13Z
probability engine model boundaries
card definition manager
deck/target parsing
seeded shuffle/opening hands
mulligan policy
target access search
Monte Carlo batch runner
simulator persistence
Challenge Mode
line review annotations
line review persistence
reviewed accuracy summaries
simulation review export payloads
DB/provider/analytics/recommendation boundary scans
full test output
remaining caveats
```
