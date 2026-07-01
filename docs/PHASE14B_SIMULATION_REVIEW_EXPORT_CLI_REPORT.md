# Phase 14B - Simulation Review Export CLI Report

## Verdict

```text
Phase 14B Simulation Review Export CLI: PASS
```

## Objective

Implement a local CLI wrapper for writing accepted simulator review export
bundles.

## Files Created

```text
codie/cli/simulation_review.py
tests/test_cli_simulation_review.py
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_CONTRACT.md
docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public CLI Added

```text
python -m codie.cli.simulation_review export-review-bundle --bundle-json <path> --output-root <directory>
```

## Schema Impact

None.

## Dependency Impact

`codie.cli.simulation_review` imports:

```text
codie.probability_engine
standard library
```

It does not import DB, repositories, providers, analytics, recommendations,
ingestion, cards, SQLite, or network clients.

## Work Completed

- Added `codie-simulation-review` parser.
- Added `export-review-bundle` command.
- Added local bundle JSON loading and validation.
- Reconstructs `SimulationReviewExportBundle`.
- Delegates writing to `write_simulation_review_export_bundle(...)`.
- Prints deterministic JSON write summary.
- Added CLI tests for successful export, invalid bundle payloads, required args,
  and import boundaries.

## Validation Performed

Focused tests:

```text
python -m unittest tests.test_cli_simulation_review -v

Ran 4 tests in 0.022s

OK
```

Full suite:

```text
python -m unittest discover -s tests -v

Ran 498 tests in 2.884s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Boundary scans:

```text
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\cli\simulation_review.py tests\test_cli_simulation_review.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\cli\simulation_review.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\cli\simulation_review.py tests\test_cli_simulation_review.py
```

returned no matches.

## Boundary Notes

- No schema changes added.
- No DB reads added.
- No provider, ingestion, cards, analytics, recommendations, repository, SQLite,
  or network dependencies added.
- No simulator execution added.
- No simulator trace mutation added.
- No recommendation output added.
- No user review is treated as tournament evidence.

## Recommended Next Step

```text
Phase 14C - Simulation Review Export Usage Documentation
```

Document the local workflow for using the Phase 13Z payload builders, Phase 14A
writer, and Phase 14B CLI.
