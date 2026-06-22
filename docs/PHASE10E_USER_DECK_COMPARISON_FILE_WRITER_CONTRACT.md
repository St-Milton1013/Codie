# Phase 10E - User Deck Comparison File Writer

## Purpose

Write already-built user deck comparison exports to caller-supplied JSON and Markdown paths.

This phase reuses the existing export writer safety rules and does not add database access, provider access, recommendation generation, or schema.

## Files Created Or Modified

- `codie/exports/__init__.py`
- `codie/exports/user_deck_reports.py`
- `tests/test_exports_user_deck_reports.py`
- `docs/PHASE10E_USER_DECK_COMPARISON_FILE_WRITER_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions And Classes

- `UserDeckComparisonWriteResult`
- `write_user_deck_comparison_exports(...)`

## Schema Impact

None.

## Inputs

- `UserDeckEvidenceComparison`
- caller-supplied JSON path
- caller-supplied Markdown path
- optional output root

## Outputs

- JSON `ExportWriteResult`
- Markdown `ExportWriteResult`

## Safety Rules

- JSON path must end in `.json`.
- Markdown path must end in `.md`.
- If `output_root` is provided, both paths must stay inside it.
- Parent directories may be created by the existing writer.

## Tests

Required test coverage:

- writes JSON and Markdown files
- output content is readable
- output root containment is enforced

## Do Not Do

- Do not generate final recommendations.
- Do not read DB tables.
- Do not call providers.
- Do not add schema.
- Do not build UI.
