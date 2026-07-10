# Outside Validation Prompt - Phase 29E Recommendation Output CLI

Validate Codie Phase 29E against:

```text
docs/PHASE29C_CLI_SAFE_FILE_WRITER_CONTRACT.md
docs/PHASE29D_CLI_SAFE_FILE_WRITER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29D_SAFE_FILE_WRITER_REPORT.md
docs/PHASE29E_RECOMMENDATION_OUTPUT_CLI_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29E_RECOMMENDATION_OUTPUT_CLI_REPORT.md
CODIE_V1_CONSTITUTION.md
```

Inspect:

```text
codie/cli/recommendation_output.py
codie/recommendation_output/writers.py
codie/recommendation_output/reporting.py
tests/test_cli_recommendation_output.py
tests/test_recommendation_output_writers.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Run from a clean checkout:

```text
python -m unittest tests.test_cli_recommendation_output -v
python -m unittest tests.test_recommendation_output_writers -v
python -m unittest discover -s tests
git diff --check
```

Confirm:

```text
CLI requires --bundle-json
CLI requires --format
CLI requires --output-root
CLI rejects malformed JSON
CLI rejects missing required bundle fields
CLI rejects unsupported format
CLI rejects unsafe output paths
CLI rejects missing output roots unless --create-output-root is passed
CLI avoids private payload output
CLI avoids raw stack traces by default
CLI delegates report rendering/writing to Phase 29D writer
CLI does not recreate report semantics
CLI does not generate recommendation output
```

Run static scans against the Phase 29E CLI module and tests:

```text
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\cli\recommendation_output.py tests\test_cli_recommendation_output.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\cli\recommendation_output.py tests\test_cli_recommendation_output.py
rg -n "raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text|raw_input" codie\cli\recommendation_output.py tests\test_cli_recommendation_output.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\cli\recommendation_output.py tests\test_cli_recommendation_output.py
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\cli\recommendation_output.py tests\test_cli_recommendation_output.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no forbidden import matches
no source/provider table matches
no raw SQL matches
no strategic-language matches
no schema or repository drift
```

Reject if:

```text
Phase 29E imports DB/repositories/providers/source layers
Phase 29E reads raw provider payloads or primer bodies
Phase 29E recalculates analytics
Phase 29E runs simulator logic
Phase 29E calls LLMs
Phase 29E discovers, ranks, scores, or generates recommendations
Phase 29E prints private payloads
Phase 29E prints raw stack traces by default
Phase 29E bypasses the Phase 29D safe writer
```

Return:

```text
PASS / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 29F.
