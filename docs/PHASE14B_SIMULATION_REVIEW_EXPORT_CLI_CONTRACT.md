# Phase 14B - Simulation Review Export CLI Contract

## Objective

Add a command-line wrapper for writing already-built simulator review export
bundles to disk.

The CLI is a thin local wrapper over Phase 14A. It reads an accepted bundle JSON
file, reconstructs the bundle model, writes files under an explicit output
root, and prints the write manifest as deterministic JSON.

## Scope

Allowed files:

- `codie/cli/simulation_review.py`
- `tests/test_cli_simulation_review.py`
- `docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_CONTRACT.md`
- `docs/PHASE14B_SIMULATION_REVIEW_EXPORT_CLI_REPORT.md`
- `docs/NEXT_PHASE_CONTRACT.md`
- `docs/CODEX_CONTINUITY_HANDOFF.md`

## Public CLI

```text
codie-simulation-review export-review-bundle
  --bundle-json <path>
  --output-root <directory>
```

The module entry point is:

```text
python -m codie.cli.simulation_review export-review-bundle ...
```

## Inputs

- local JSON file produced from `SimulationReviewExportBundle.to_dict()`
- explicit output root

## Outputs

- simulator review export files written under output root
- JSON summary printed to stdout with:
  - root
  - bundle_id
  - files
  - bytes_written

## Schema Impact

None.

## Dependencies

Allowed:

- standard library
- `codie.probability_engine`

Forbidden:

- `codie.db`
- repositories
- providers
- ingestion
- cards
- analytics
- recommendations
- SQLite
- network clients

## Required Behavior

- require `--bundle-json`
- require `--output-root`
- reject non-object JSON
- reject non-`simulation_review_export_bundle` payloads
- reject missing required bundle fields
- reject missing `files` list
- reconstruct `SimulationReviewExportBundle`
- delegate all file writing to `write_simulation_review_export_bundle(...)`
- print deterministic JSON to stdout
- do not query DB
- do not call providers
- do not run simulations
- do not mutate simulator traces
- do not create recommendation output

## Failure Modes

- argparse exits for missing required CLI args
- malformed JSON propagates `json.JSONDecodeError`
- wrong bundle kind raises `ValueError`
- missing required bundle fields raise `ValueError`
- file writer validation failures propagate from Phase 14A writer

## Tests

Required tests:

- CLI writes manifest, summary JSON, summary Markdown, and fixture files
- CLI prints bundle ID and byte count
- non-bundle JSON fails cleanly
- parser requires output root
- CLI module has no forbidden imports
- full suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks:

```text
git diff --check
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\cli\simulation_review.py tests\test_cli_simulation_review.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\cli\simulation_review.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\cli\simulation_review.py tests\test_cli_simulation_review.py
```

must return no matches.

## Do Not Do

- do not add schema
- do not add DB reads
- do not add provider calls
- do not run or mutate simulations
- do not build review summaries in the CLI
- do not build line review fixtures in the CLI
- do not add UI
- do not create recommendation claims

## Follow-Up

Recommended next packet:

```text
Phase 14C - Simulation Review Export Usage Documentation
```

Document the local workflow for generating, writing, and sharing simulator
review export bundles without adding new behavior.
