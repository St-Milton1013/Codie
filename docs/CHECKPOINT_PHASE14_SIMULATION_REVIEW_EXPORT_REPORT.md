# Checkpoint - Phase 14 Simulation Review Export Report

## Verdict

```text
Phase 14 Simulation Review Export Track Internal Checkpoint: PASS
Status: Ready for outside validation before Phase 15
```

This is an internal checkpoint, not external proof. Phase 15 should not start
until the outside validation packet is reviewed and accepted.

## Scope Reviewed

This checkpoint covers Phase 14A through Phase 14C:

```text
Phase 14A Simulation Review Export File Writer
Phase 14B Simulation Review Export CLI
Phase 14C Simulation Review Export Usage Documentation
```

## What Exists Now

```text
codie/probability_engine/review_export_writer.py
codie/cli/simulation_review.py
docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

Related Phase 13 export builder:

```text
codie/probability_engine/review_export.py
```

## Architecture Summary

Phase 14 extends the Phase 13 simulation review export payloads with safe local
file output and a narrow CLI wrapper.

Flow:

```text
ReviewedAccuracySummary + LineReviewFixture
-> build_simulation_review_export_bundle(...)
-> SimulationReviewExportBundle.to_dict()
-> local bundle JSON file
-> python -m codie.cli.simulation_review export-review-bundle
-> write_simulation_review_export_bundle(...)
-> manifest.json + JSON/Markdown review files
```

The CLI does not build reviewed accuracy summaries, query repositories, run
simulations, call providers, or create recommendation output.

## Files Added

```text
codie/probability_engine/review_export_writer.py
codie/cli/simulation_review.py
tests/test_probability_engine_review_export_writer.py
tests/test_cli_simulation_review.py
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_CONTRACT.md
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_REPORT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_CONTRACT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_REPORT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_REPORT.md
docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

## Public API / CLI

Public Python API:

```text
SimulationReviewExportWriteResult
write_simulation_review_export_bundle(...)
```

Public CLI:

```text
python -m codie.cli.simulation_review export-review-bundle --bundle-json <path> --output-root <directory>
```

## Schema Impact

None.

Phase 14 creates no tables, migrations, repository methods, indexes, or
persistence records.

## Dependency Impact

Allowed dependencies:

```text
standard library
codie.probability_engine.review_export
codie.probability_engine
```

Forbidden dependencies remain absent:

```text
codie.db
repositories
providers
ingestion
cards
analytics
recommendations
sqlite3
requests
httpx
```

## Boundary Findings

Phase 14 preserves the intended boundaries:

```text
no schema changes
no DB reads
no repository imports
no provider imports
no analytics imports
no recommendation imports
no network clients
no simulator execution
no simulator trace mutation
no line review annotation mutation
no tournament evidence claims
```

## Safety Behaviors

The file writer:

```text
requires explicit output root
validates full bundle before writing bundle files
writes manifest.json
writes manifest.json after bundle files
writes deterministic JSON with sorted keys
writes Markdown with final newline
rejects absolute paths
rejects traversal paths
rejects Windows drive paths
rejects backslash paths
rejects duplicate relative paths
rejects unsupported content types
rejects invalid JSON payloads
rejects empty Markdown bodies
rejects output roots that point to existing files
allows repeated exports to the same output root deterministically
does not mutate bundle input
```

The CLI:

```text
requires --bundle-json
requires --output-root
rejects non-object JSON
rejects wrong bundle kind
handles missing bundle-json paths
handles malformed JSON
rejects missing required bundle fields
rejects output roots that point to existing files
delegates file writing to Phase 14A writer
prints deterministic JSON write summary
```

## Evidence / Recommendation Boundary

Simulation review exports are QA/training artifacts.

They may be used for:

```text
human review of simulator lines
regression fixture generation
unsupported-card review
reviewed accuracy summaries
simulator behavior improvement backlog
```

They must not be used as:

```text
tournament evidence
source/provider evidence
automatic recommendation truth
private deck sharing without user action
historical simulation rewrite mechanism
```

## Tests Added

```text
tests/test_probability_engine_review_export_writer.py
tests/test_cli_simulation_review.py
```

Coverage includes:

```text
writer creates manifest, JSON, Markdown, and fixture files
writer writes manifest last
writer preserves bundle ID
writer rejects unsafe paths
writer rejects duplicate paths
writer rejects unsupported content types
writer validates before writing bundle files
writer rejects output root paths that point to files
writer repeats exports to the same root deterministically
writer does not mutate bundle input
CLI writes files from bundle JSON
CLI prints bundle ID and byte count
CLI rejects non-bundle JSON
CLI rejects missing bundle path
CLI rejects malformed JSON
CLI rejects missing required fields
CLI rejects output-root file paths
CLI requires output root
import boundary checks
raw SQL / strategic language checks
```

## Validation Performed

Latest full suite:

```text
python -m unittest discover -s tests -v

Ran 503 tests in 2.970s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Boundary scans:

```text
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py codie\cli\simulation_review.py tests\test_cli_simulation_review.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\probability_engine\review_export_writer.py codie\cli\simulation_review.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py codie\cli\simulation_review.py tests\test_cli_simulation_review.py docs\USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

returned no matches.

## Known Caveats / Review Notes

- Challenge Mode has no UI yet.
- Simulator behavior coverage remains intentionally narrow.
- Unsupported-card behavior must remain visible.
- Simulation results remain QA/training metadata, not tournament evidence.
- Final recommendation output remains intentionally separate.
- The CLI accepts already-built local bundle JSON only.
- Phase 14 does not add persisted export rows or import tracking.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Outside Validation Packet

Send:

```text
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE14_SIMULATION_REVIEW_EXPORT_PROMPT.md
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

## Recommended Next Step

```text
Outside validation for Phase 14
```

Do not start Phase 15 implementation until outside validation returns PASS or
PASS WITH REVIEW NOTES.
