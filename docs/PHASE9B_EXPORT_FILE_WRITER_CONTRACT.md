# Phase 9B - Export File Writer Contract

## Objective

Write accepted JSON-compatible export dictionaries and Markdown report strings to disk deterministically.

This phase adds file output only. It does not query databases, call providers, or build UI.

## Scope

Allowed files:

- `codie/exports/writers.py`
- `codie/exports/__init__.py`
- `tests/test_exports_writers.py`
- `docs/PHASE9B_EXPORT_FILE_WRITER_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes

- `ExportWriteResult`
- `write_json_export(...)`
- `write_markdown_export(...)`

## Inputs

- JSON-compatible dictionaries produced by Phase 9A helpers
- Markdown strings produced by Phase 9A helpers
- target file path
- optional output root for path containment

## Outputs

- UTF-8 JSON files with deterministic key ordering
- UTF-8 Markdown files
- `ExportWriteResult` with path, byte count, and content type

## Schema Impact

None.

## Required Behavior

- create parent directories when needed
- write UTF-8 files
- serialize JSON with sorted keys and stable indentation
- require `.json` for JSON exports
- require `.md` for Markdown exports
- reject writes outside the optional output root
- return deterministic metadata about the written file

## Failure Modes

- missing target path raises `ValueError`
- unsupported suffix raises `ValueError`
- path outside output root raises `ValueError`
- empty Markdown raises `ValueError`

## Tests

Required tests:

- JSON writer creates deterministic file
- Markdown writer creates deterministic file
- nested parent directories are created
- output root containment rejects outside paths
- unsupported suffixes fail cleanly
- writers do not import DB/providers
- full suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
```

## Do Not Do

- do not query the database
- do not call providers
- do not build UI
- do not add schema
- do not add strategic claim language

## Follow-Up

Recommended next packet:

```text
Phase 9C - Export CLI wrapper or checkpoint report generator
```
