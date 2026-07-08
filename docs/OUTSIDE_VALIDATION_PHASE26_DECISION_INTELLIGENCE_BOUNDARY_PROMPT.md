# Outside Validation Prompt - Phase 26 Decision Intelligence Boundary

Validate Codie Phase 26 work against `CODIE_V1_CONSTITUTION.md`, Codie
Architecture Revision III, and the Phase 26A contract.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 27.

## Files To Review

```text
docs/PHASE26A_DECISION_INTELLIGENCE_BOUNDARY_CONTRACT.md
docs/PHASE26B_DECISION_INTELLIGENCE_BOUNDARY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE26_DECISION_INTELLIGENCE_BOUNDARY_REPORT.md
codie/decision_intelligence/__init__.py
codie/decision_intelligence/models.py
codie/decision_intelligence/builders.py
tests/test_decision_intelligence_boundary.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm:

```text
Decision Intelligence is implemented only as in-memory packet models.
Decision packets require Unified Evidence Object input.
Decision packets expose confidence.
Decision packets expose expected impact.
Decision packets expose source agreement.
Decision packets expose evidence_object_ids.
Decision packets expose caveat_ids.
Decision packets expose speculation_level.
Decision packets preserve contradiction visibility.
Decision packets distinguish simulator evidence from tournament evidence.
Decision packets distinguish primer context from measured evidence.
Decision packets preserve authority ref IDs separately.
Decision packet bundles serialize deterministically.
Decision packet bundles reject duplicate decision IDs.
Decision packet bundles reject mismatched subjects.
Private metadata is rejected.
Nested private metadata is rejected.
Unsupported strategic language is rejected.
High confidence requires strong or mixed source agreement.
High speculation cannot pair with medium or high confidence.
No recommendation output is generated.
No deck health output is generated.
No replacement suggestions are generated.
No schema changes exist.
No repository methods are added.
No DB reads or writes exist.
No provider/source table reads exist.
No raw provider payload reads exist.
No analytics recalculation exists.
No simulator execution exists.
No LLM calls exist.
No UI code exists.
No file writing exists.
```

## Test Commands

Run from a clean checkout:

```powershell
python -m unittest tests.test_decision_intelligence_boundary -v
```

Expected:

```text
Ran 14 tests
OK
```

Run full suite:

```powershell
python -m unittest discover -s tests
```

Expected:

```text
Ran 746 tests
OK (skipped=1)
```

## Static Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
```

Expected:

```text
matches only blocked-key constants and rejection tests
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\decision_intelligence
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\decision_intelligence tests\test_decision_intelligence_boundary.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no matches
```

## Reject If

Reject Phase 26 if:

```text
Decision Intelligence reads raw providers, source tables, provider_objects, or raw payloads.
Decision Intelligence imports DB, repositories, providers, ingestion, canonicalization, analytics recalculation, cards, simulator execution, UI, server frameworks, or LLM SDKs.
Decision Intelligence emits final recommendations.
Decision Intelligence emits deck health conclusions.
Decision Intelligence emits replacement suggestions.
Decision Intelligence treats simulator refs as tournament evidence.
Decision Intelligence treats primer context as measured evidence.
Decision Intelligence lets primer context override authority or measured evidence.
Decision Intelligence lacks evidence_object_ids.
Decision Intelligence hides caveats, contradictions, source agreement, or speculation level.
Decision Intelligence persists packets or writes files.
Decision Intelligence adds schema or repository drift.
```

## Next Phase Gate

Phase 27 must not start until this validation returns PASS or PASS WITH REVIEW
NOTES.
