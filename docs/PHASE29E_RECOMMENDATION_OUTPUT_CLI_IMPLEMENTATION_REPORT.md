# Phase 29E - Recommendation Output CLI Implementation Report

## Status

```text
Phase 29E: INTERNAL PASS
Scope: CLI wrapper only
Phase 29F: blocked until Phase 29E outside validation returns PASS or PASS WITH REVIEW NOTES
```

## Implemented Files

```text
codie/cli/recommendation_output.py
tests/test_cli_recommendation_output.py
```

## Public CLI

```text
codie-recommendation-output render --bundle-json <path> --format json|markdown|both --output-root <path>
```

Optional flags:

```text
--basename <name>
--overwrite
--create-output-root
--no-provenance
```

## Behavior Implemented

```text
requires --bundle-json
requires --format
requires --output-root
loads local RecommendationOutputBundle JSON
validates by routing through write_recommendation_report_files(...)
supports json, markdown, md, and both formats
supports explicit basename
supports explicit overwrite
supports explicit output-root creation
supports provenance omission
prints concise JSON success result
returns nonzero for malformed JSON
returns nonzero for missing required bundle fields
returns nonzero for unsafe output paths
returns nonzero for missing output roots unless --create-output-root is used
does not print raw stack traces by default
does not print private payloads
```

## Boundaries Preserved

```text
no schema changes
no repository changes
no DB reads
no provider reads
no source table reads
no raw provider payload reads
no primer body reads
no simulator execution
no analytics recalculation
no LLM calls
no UI code
no candidate discovery
no candidate ranking
no candidate scoring
no cut selection
no addition selection
no final recommendation generation
```

The CLI imports only the recommendation output writer layer and standard
library modules.

## Tests Added

```text
test_render_writes_files_and_prints_concise_result
test_parser_requires_bundle_json_format_and_output_root
test_render_rejects_malformed_json_missing_fields_and_unsupported_format
test_render_rejects_unsafe_output_path_and_missing_root_without_private_payloads
test_render_supports_single_format_basename_overwrite_and_no_provenance
test_cli_module_has_no_forbidden_imports_raw_sql_or_source_reads
```

## Focused Validation

```text
python -m unittest tests.test_cli_recommendation_output -v
Ran 6 tests in 0.030s
OK
```

## Full Validation

```text
python -m unittest tests.test_recommendation_output_writers -v
Ran 10 tests in 0.065s
OK

python -m unittest discover -s tests
Ran 797 tests in 3.454s
OK (skipped=1)

git diff --check
passed

Phase 29E static scans:
no forbidden import matches
no source/provider table matches
no private metadata matches
no raw SQL matches
no strategic-language matches
no schema or repository drift
```

## Outside Validation Focus

Validate that Phase 29E remains CLI-wrapper-only:

```text
codie/cli/recommendation_output.py
tests/test_cli_recommendation_output.py
codie/recommendation_output/writers.py
tests/test_recommendation_output_writers.py
```

Confirm:

```text
CLI requires --bundle-json, --format, and --output-root
CLI rejects malformed JSON
CLI rejects missing required bundle fields
CLI rejects unsupported format
CLI rejects unsafe output path
CLI rejects missing output root unless --create-output-root is passed
CLI does not print private payloads
CLI does not print raw stack traces by default
CLI delegates file writing to Phase 29D writer
CLI does not recreate report semantics
CLI does not implement recommendation generation
```
