# Outside Validation Prompt - Phase 28 Deck Health / Recommendation Output

Validate Codie Phase 28 work against `CODIE_V1_CONSTITUTION.md`, Codie
Architecture Revision III, the Phase 28A contract, and the Phase 28B
implementation report.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 29.

## Files To Review

```text
docs/PHASE28A_DECK_HEALTH_RECOMMENDATION_OUTPUT_CONTRACT.md
docs/PHASE28B_DECK_HEALTH_RECOMMENDATION_OUTPUT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE28_RECOMMENDATION_OUTPUT_REPORT.md
codie/recommendation_output/__init__.py
codie/recommendation_output/models.py
tests/test_recommendation_output_boundary.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm:

```text
Phase 28A is contract-only.
Phase 28B is pure in-memory packet models and validators only.
Recommendation output packets require DecisionPacket IDs.
Recommendation output packets require UnifiedEvidenceObject IDs.
Recommendation output packets require WeightProfile ID/version.
Recommendation output packets require AnalysisProfile ID/version.
Confidence remains visible.
Expected impact remains visible.
Source agreement remains visible.
Caveats remain visible.
Contradictions remain visible.
Speculation level remains visible.
Low sample size requires visible caveats.
Low coverage requires visible caveats.
High confidence requires strong or mixed source agreement.
Medium or high confidence requires supporting refs.
High speculation cannot pair with medium or high confidence.
Recommendation candidate packets allow monitor, investigate, and no_action.
consider_include and consider_replace require at least medium confidence.
Replacement suggestions require replaced-card identity.
Replacement suggestions require candidate-card identity.
Replacement suggestions require shared role tags.
Simulator refs remain simulator evidence only.
Primer context remains explanatory only.
Package gap packets do not perform candidate generation.
Private metadata is rejected.
Nested private metadata is rejected.
Forbidden strategic language is rejected.
Serialization is deterministic.
Duplicate output IDs are rejected.
No recommendation candidate discovery exists.
No recommendation candidate ranking exists.
No recommendation candidate scoring exists.
No cut selection exists.
No addition selection exists.
No final recommendation generation exists.
No schema changes exist.
No repository methods are added.
No DB reads or writes exist.
No provider/source table reads exist.
No raw provider payload reads exist.
No raw Moxfield primer body reads exist.
No private deck import text reads exist.
No analytics recalculation exists.
No simulator execution exists.
No LLM calls exist.
No UI code exists.
No file writing exists.
```

## Test Commands

Run from a clean checkout:

```powershell
python -m unittest tests.test_recommendation_output_boundary -v
```

Expected:

```text
Ran 11 tests
OK
```

Run full suite:

```powershell
python -m unittest discover -s tests
```

Expected:

```text
Ran 772 tests
OK (skipped=1)
```

## Static Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\recommendation_output tests\test_recommendation_output_boundary.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\recommendation_output tests\test_recommendation_output_boundary.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text|raw_input" codie\recommendation_output tests\test_recommendation_output_boundary.py
```

Expected:

```text
matches only blocked-key constants and rejection tests
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\recommendation_output tests\test_recommendation_output_boundary.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\recommendation_output
rg -n "you should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|best card|strictly better" codie\recommendation_output tests\test_recommendation_output_boundary.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no matches
```

## Reject If

Reject Phase 28 if:

```text
Deck health or recommendation output reads raw provider data.
Deck health or recommendation output reads source tables.
Deck health or recommendation output reads provider_objects.
Deck health or recommendation output reads raw Moxfield primer bodies.
Deck health or recommendation output reads private deck import text.
Deck health or recommendation output calls providers.
Deck health or recommendation output queries SQLite.
Deck health or recommendation output imports repositories.
Deck health or recommendation output recalculates analytics.
Deck health or recommendation output executes simulator logic.
Deck health or recommendation output calls LLMs.
Deck health or recommendation output writes files.
Deck health or recommendation output adds schema.
Phase 28B discovers recommendation candidates.
Phase 28B ranks recommendation candidates.
Phase 28B scores recommendation candidates.
Phase 28B chooses cuts or additions.
Phase 28B generates final user-facing recommendation behavior.
Simulator refs are treated as tournament evidence.
Primer context is treated as measured evidence.
Low sample or low coverage caveats can disappear silently.
High confidence is allowed with weak source agreement.
High speculation is allowed with medium or high confidence.
Unsupported strategic language appears in production output.
```

## Next Phase Gate

Phase 29 must not start until this validation returns PASS or PASS WITH REVIEW
NOTES.
