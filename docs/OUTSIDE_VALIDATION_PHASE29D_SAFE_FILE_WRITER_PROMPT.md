# Outside Validation Prompt - Phase 29D Safe Recommendation Report File Writer

Validate Codie Phase 29D against:

```text
docs/PHASE29C_CLI_SAFE_FILE_WRITER_CONTRACT.md
docs/PHASE29D_CLI_SAFE_FILE_WRITER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29D_SAFE_FILE_WRITER_REPORT.md
CODIE_V1_CONSTITUTION.md
```

Inspect:

```text
codie/recommendation_output/writers.py
codie/recommendation_output/reporting.py
codie/recommendation_output/models.py
codie/recommendation_output/__init__.py
tests/test_recommendation_output_writers.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Run from a clean checkout:

```text
python -m unittest tests.test_recommendation_output_writers -v
python -m unittest discover -s tests
git diff --check
```

Confirm:

```text
writer accepts already-built RecommendationOutputBundle objects or validated JSON only
writer validates bundle input before rendering
writer uses Phase 29B report serializers
writer writes JSON report files
writer writes Markdown report files
writer writes both formats
writer writes UTF-8 output
writer rejects missing output_root by default
writer creates missing output_root only when create_output_root is true
writer rejects output_root paths that point to existing files
writer enforces output-root containment
writer rejects path traversal
writer rejects explicit basename path separators
writer rejects explicit basename extension override
writer rejects basename collisions with manifest.json
writer requires explicit overwrite
writer writes manifest.json last
```

Confirm JSON and Markdown output preserve:

```text
confidence
expected impact
source agreement
caveats
contradictions
speculation level
weight / analysis profile refs
decision IDs
UnifiedEvidenceObject IDs
```

Run writer-only static scans:

```text
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text|raw_input" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\recommendation_output tests\test_recommendation_output_writers.py
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\recommendation_output tests\test_recommendation_output_writers.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no forbidden import matches
no source/provider table matches
no raw SQL matches
no strategic-language matches
private metadata scan may match only blocked-key constants or rejection tests
no schema or repository drift
```

Reject if:

```text
Phase 29D implements CLI behavior
Phase 29D reads DB/repositories/providers/source tables
Phase 29D reads raw provider payloads or primer bodies
Phase 29D recalculates analytics
Phase 29D runs simulator logic
Phase 29D calls LLMs
Phase 29D discovers, ranks, scores, or generates recommendations
Phase 29D writes files outside output_root
Phase 29D creates missing output roots without create_output_root=true
Phase 29D silently overwrites files
Phase 29D writes manifest.json before report files
Phase 29D omits evidence visibility fields from JSON or Markdown output
```

Return:

```text
PASS / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 29E.
