# Phase 14A - Simulation Review Export File Writer Contract

## Objective

Write accepted Phase 13 simulation review export bundles to local disk safely and
deterministically.

This phase adds file output for existing review export payloads only. It does
not query databases, run simulations, build review payloads, mutate simulator
records, or create recommendation output.

## Scope

Allowed files:

- `codie/probability_engine/review_export_writer.py`
- `codie/probability_engine/__init__.py`
- `tests/test_probability_engine_review_export_writer.py`
- `docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_CONTRACT.md`
- `docs/PHASE14A_SIMULATION_REVIEW_EXPORT_FILE_WRITER_REPORT.md`
- `docs/NEXT_PHASE_CONTRACT.md`
- `docs/CODEX_CONTINUITY_HANDOFF.md`

## Public Functions / Classes

- `SimulationReviewExportWriteResult`
- `write_simulation_review_export_bundle(...)`

## Inputs

- `SimulationReviewExportBundle` built by Phase 13Z
- caller-supplied `output_root`

The writer accepts already-built bundle payloads only. It must not construct
review summaries, line review fixtures, challenge results, or simulator traces.

## Outputs

- `manifest.json`
- bundle JSON payload files
- bundle Markdown files
- `SimulationReviewExportWriteResult` containing:
  - root
  - bundle_id
  - written file metadata
  - total bytes written

## Schema Impact

None.

## Dependency Impact

Allowed dependencies:

- standard library
- `codie.probability_engine.review_export`

Forbidden dependencies:

- `codie.db`
- repositories
- providers
- ingestion
- cards
- analytics
- recommendations
- network clients
- SQLite

## Required Behavior

- require a caller-supplied output root
- create parent directories under the output root
- write UTF-8 files
- serialize JSON with deterministic sorted keys and stable indentation
- ensure Markdown files end with a newline
- write a deterministic manifest for the full bundle
- enforce output-root containment
- reject absolute bundle paths
- reject path traversal
- reject Windows drive paths
- reject backslash paths
- reject duplicate relative paths
- reject unsupported content types
- reject JSON files without dictionary payloads
- reject Markdown files without non-empty body text
- validate the full bundle before writing bundle files
- not mutate the input bundle

## Failure Modes

- missing output root raises `ValueError`
- invalid relative path raises `ValueError`
- duplicate export path raises `ValueError`
- unsupported content type raises `ValueError`
- invalid JSON payload raises `ValueError`
- invalid Markdown body raises `ValueError`
- write errors propagate from the filesystem

## Tests

Required tests:

- bundle writer creates manifest, JSON, Markdown, and fixture files
- manifest preserves bundle ID
- JSON is deterministic and readable
- Markdown receives final newline
- path traversal is rejected
- absolute paths are rejected
- Windows drive and backslash paths are rejected
- duplicate paths are rejected
- unsupported content types fail cleanly
- invalid bundle validates before writing any bundle files
- writer does not mutate bundle input
- writer has no forbidden imports
- writer has no raw SQL or strategic claim language
- full test suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks:

```text
git diff --check
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx|sqlite3" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\probability_engine\review_export_writer.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\review_export_writer.py tests\test_probability_engine_review_export_writer.py
```

must return no matches.

## Do Not Do

- do not query the database
- do not import repositories
- do not call providers
- do not run simulations
- do not mutate simulator traces
- do not rewrite line review annotations
- do not add schema
- do not add CLI or UI
- do not create recommendation output
- do not treat simulation results as tournament evidence

## Follow-Up

Recommended next packet:

```text
Phase 14B - Simulation Review Export CLI Contract
```

Only after the file writer is accepted should Codie add a CLI wrapper or UI
surface for simulator review exports.
