# Outside Validation Prompt - Phase 14 Simulation Review Export

Validate Codie Phase 14 work against `CODIE_V1_CONSTITUTION.md` and the Phase
14 contracts.

Return:

```text
PASS / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 15.

## Files To Review

Checkpoint:

```text
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
```

Contracts and reports:

```text
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_CONTRACT.md
docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_REPORT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_CONTRACT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_REPORT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE14C_SIMULATION_REVIEW_EXPORT_USAGE_DOCUMENTATION_REPORT.md
docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

Implementation:

```text
codie/probability_engine/review_export.py
codie/probability_engine/review_export_writer.py
codie/probability_engine/__init__.py
codie/cli/simulation_review.py
```

Tests:

```text
tests/test_probability_engine_review_export.py
tests/test_probability_engine_review_export_writer.py
tests/test_cli_simulation_review.py
```

Architecture references:

```text
docs/CODIE_V1_CONSTITUTION.md
docs/DEPENDENCY_RULES.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Validation Tasks

### 0. Phase 13 Export Builder Dependency

Confirm Phase 14 does not weaken Phase 13 export-builder guarantees:

```text
review_export.py remains pure
review_export.py still does not write files
review_export.py still does not query DB
review_export.py still produces deterministic bundle payloads
Phase 14 writer consumes bundles but does not change bundle construction semantics
```

Reject if Phase 14 changes `review_export.py` to add file writing, DB access,
repository access, provider access, simulator execution, or nondeterministic
bundle construction.

### 1. File Writer

Confirm:

```text
write_simulation_review_export_bundle(...) exists
SimulationReviewExportWriteResult exists
writer accepts already-built SimulationReviewExportBundle only
writer writes manifest.json
writer writes JSON payload files deterministically
writer writes Markdown files with final newline
writer enforces output-root containment
writer rejects absolute paths
writer rejects traversal paths
writer rejects Windows drive paths
writer rejects backslash paths
writer rejects duplicate paths
writer rejects unsupported content types
writer rejects invalid JSON payloads
writer rejects empty Markdown bodies
writer validates full bundle before writing bundle files
writer writes manifest.json last
writer does not mutate bundle input
```

Confirm writer behavior on write failure:

```text
validates all bundle paths before writing any bundle files
does not leave a misleading manifest if later file writes fail
either writes manifest last or documents why manifest timing is safe
reports partial-write failures clearly
```

Confirm output-root behavior:

```text
output root creation behavior is documented
parent directory creation behavior is tested
output root path pointing to a file is rejected
existing output folder collision behavior is tested
repeated export to the same output root is deterministic or rejected intentionally
```

Reject if:

```text
writer queries DB
writer imports repositories
writer imports providers
writer imports analytics or recommendations
writer runs simulations
writer mutates traces or line reviews
writer accepts unsafe output paths
```

### 2. CLI

Confirm:

```text
python -m codie.cli.simulation_review export-review-bundle exists
--bundle-json is required
--output-root is required
CLI rejects non-object JSON
CLI rejects wrong bundle kind
CLI handles missing bundle-json path
CLI handles unreadable bundle-json path
CLI handles malformed JSON
CLI handles valid JSON with missing required fields
CLI handles output-root path that points to a file
CLI handles permission failure on output-root
CLI reconstructs SimulationReviewExportBundle
CLI delegates writing to write_simulation_review_export_bundle(...)
CLI prints deterministic JSON write summary
```

Reject if:

```text
CLI queries DB
CLI imports providers
CLI imports analytics or recommendations
CLI builds reviewed accuracy summaries
CLI builds line review fixtures
CLI runs simulations
CLI mutates simulator records
CLI creates recommendation output
```

### 3. Documentation

Confirm `USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md` explains:

```text
project checkout
bundled Python runtime
output folder
bundle JSON creation shape
CLI command
manifest inspection
summary inspection
fixture inspection
optional local share-bundle handoff
privacy rules
evidence boundary
troubleshooting
```

Reject if documentation implies:

```text
simulation outputs are tournament evidence
simulation exports create recommendations
unsupported cards can be ignored
private exports should be uploaded by default
cEDHData source code may be copied into Codie
```

### 4. Tests

Run from a clean checkout:

```text
python -m unittest discover -s tests -v
```

Or, if system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Confirm the expected result:

```text
Ran 503 tests
OK (skipped=1)
```

Focused tests:

```text
python -m unittest tests.test_probability_engine_review_export_writer -v
python -m unittest tests.test_cli_simulation_review -v
```

### 5. Static Boundary Checks

Run:

```text
git diff --check
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie/probability_engine/review_export_writer.py tests/test_probability_engine_review_export_writer.py codie/cli/simulation_review.py tests/test_cli_simulation_review.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie/probability_engine/review_export_writer.py codie/cli/simulation_review.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie/probability_engine/review_export_writer.py tests/test_probability_engine_review_export_writer.py codie/cli/simulation_review.py tests/test_cli_simulation_review.py docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
```

Expected:

```text
git diff --check passes
all rg scans return no matches
```

### 6. Schema And Persistence

Confirm:

```text
no schema files changed
no repository files changed
no migrations added
no export rows or import tracking tables added
no simulator persistence tables changed
```

Reject if Phase 14 added unapproved schema or repository changes.

## Final Decision

Return:

```text
PASS
```

only if:

```text
file writer is safe
CLI is narrow
documentation is evidence-safe
full test suite passes
static scans are clean
no schema drift exists
no recommendation/tournament-evidence claims were introduced
```

Return:

```text
PASS WITH REQUIRED FIXES
```

if implementation is mostly correct but needs narrow fixes.

Return:

```text
FAIL
```

if Phase 14 violates provider, DB, analytics, recommendation, simulator trace,
or evidence boundaries.
