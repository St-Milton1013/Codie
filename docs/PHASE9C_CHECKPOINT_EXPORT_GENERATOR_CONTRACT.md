# Phase 9C - Checkpoint Export Generator Contract

## Objective

Generate deterministic checkpoint reports from already-built export payloads and validation metadata.

This phase turns accepted export dictionaries into a compact Markdown review packet that can be sent for outside validation.

## Scope

Allowed files:

- `codie/exports/checkpoints.py`
- `codie/exports/__init__.py`
- `tests/test_exports_checkpoints.py`
- `docs/PHASE9C_CHECKPOINT_EXPORT_GENERATOR_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes

- `ValidationSummary`
- `CheckpointExport`
- `build_checkpoint_export(...)`
- `checkpoint_markdown(...)`
- `write_checkpoint_markdown(...)`

## Inputs

- export payloads from Phase 9A helpers
- validation metadata supplied by caller
- review notes supplied by caller

## Outputs

- deterministic checkpoint dictionary
- deterministic Markdown report
- optional Markdown file via Phase 9B writer

## Schema Impact

None.

## Required Behavior

- preserve export metadata
- include validation command and result
- include test count when provided
- include commit hash when provided
- include review notes without strategic claims
- sort included exports deterministically
- write Markdown through existing writer helper
- avoid DB/provider/source access

## Failure Modes

- missing title raises `ValueError`
- missing generated timestamp raises `ValueError`
- invalid review note wording raises `ValueError`
- invalid validation status raises `ValueError`

## Tests

Required tests:

- checkpoint dictionary includes exports and validation metadata
- Markdown report is deterministic
- writer writes checkpoint Markdown
- forbidden wording is rejected
- no DB/provider imports in export package
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

- do not query DB
- do not call providers
- do not build UI
- do not add schema
- do not add strategic claim language

## Follow-Up

Recommended next packet:

```text
Phase 10A - User Deck Import / Analysis Contract
```
