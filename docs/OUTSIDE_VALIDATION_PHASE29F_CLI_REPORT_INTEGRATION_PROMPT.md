# Outside Validation Prompt - Phase 29F CLI / Report Integration

Validate Codie Phase 29F against:

```text
docs/PHASE29B_CLI_REPORT_INTEGRATION_IMPLEMENTATION_REPORT.md
docs/PHASE29C_CLI_SAFE_FILE_WRITER_CONTRACT.md
docs/PHASE29D_CLI_SAFE_FILE_WRITER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29D_SAFE_FILE_WRITER_REPORT.md
docs/PHASE29E_RECOMMENDATION_OUTPUT_CLI_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29E_RECOMMENDATION_OUTPUT_CLI_REPORT.md
docs/CHECKPOINT_PHASE29F_CLI_REPORT_INTEGRATION_REPORT.md
CODIE_V1_CONSTITUTION.md
```

Inspect:

```text
codie/recommendation_output/reporting.py
codie/recommendation_output/writers.py
codie/cli/recommendation_output.py
tests/test_recommendation_output_reporting.py
tests/test_recommendation_output_writers.py
tests/test_cli_recommendation_output.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Run from a clean checkout:

```text
python -m unittest tests.test_recommendation_output_reporting -v
python -m unittest tests.test_recommendation_output_writers -v
python -m unittest tests.test_cli_recommendation_output -v
python -m unittest discover -s tests
git diff --check
```

Confirm the full chain:

```text
RecommendationOutputBundle JSON
-> report document serializer
-> safe writer
-> CLI wrapper
-> local JSON / Markdown / manifest files
```

Confirm:

```text
reporting stays in-memory and file-write-free
writer stays writer-only and CLI-free
CLI stays wrapper-only
CLI delegates to the Phase 29D writer
writer uses Phase 29B report serializers
JSON and Markdown preserve evidence visibility fields
manifest.json is written last
output-root containment is enforced
missing output roots require --create-output-root
overwrites require --overwrite
CLI avoids private payload output
CLI avoids raw stack traces by default
```

Run static scans:

```text
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\recommendation_output codie\cli\recommendation_output.py tests\test_recommendation_output_reporting.py tests\test_recommendation_output_writers.py tests\test_cli_recommendation_output.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\recommendation_output codie\cli\recommendation_output.py tests\test_recommendation_output_reporting.py tests\test_recommendation_output_writers.py tests\test_cli_recommendation_output.py
rg -n "raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text|raw_input" codie\recommendation_output codie\cli\recommendation_output.py tests\test_recommendation_output_reporting.py tests\test_recommendation_output_writers.py tests\test_cli_recommendation_output.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\recommendation_output codie\cli\recommendation_output.py tests\test_recommendation_output_reporting.py tests\test_recommendation_output_writers.py tests\test_cli_recommendation_output.py
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\recommendation_output codie\cli\recommendation_output.py tests\test_recommendation_output_reporting.py tests\test_recommendation_output_writers.py tests\test_cli_recommendation_output.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no forbidden production imports
no source/provider table access
no raw SQL
no strategic-language output
private metadata strings only in blocked-key constants or rejection tests
no schema or repository drift
```

Reject if:

```text
Phase 29F adds new behavior instead of checkpointing the existing chain
reporting writes files
writer implements CLI behavior
CLI bypasses the writer
CLI/report/writer reads DB/repositories/providers/source tables
CLI/report/writer reads raw provider payloads or primer bodies
CLI/report/writer recalculates analytics
CLI/report/writer runs simulator logic
CLI/report/writer calls LLMs
CLI/report/writer discovers, ranks, scores, or generates recommendations
CLI/report/writer prints private payloads
CLI/report/writer prints raw stack traces by default
```

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 30A.
