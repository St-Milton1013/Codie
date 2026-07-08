# Outside Validation Prompt - Phase 27 Weight Profile / Analysis Profile

Validate Codie Phase 27 work against `CODIE_V1_CONSTITUTION.md`, Codie
Architecture Revision III, and the Phase 27A contract.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 28.

## Files To Review

```text
docs/PHASE27A_WEIGHT_PROFILE_ANALYSIS_PROFILE_CONTRACT.md
docs/PHASE27B_WEIGHT_PROFILE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE27_WEIGHT_PROFILE_REPORT.md
codie/weight_profiles/__init__.py
codie/weight_profiles/models.py
codie/weight_profiles/defaults.py
tests/test_weight_profiles.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm:

```text
Weight profiles are in-memory configuration packets only.
Weight profiles are not evidence.
Weight profiles are not recommendations.
Weight profiles serialize deterministically.
Analysis profiles serialize deterministically.
Profile IDs and versions are required.
Component IDs are unique within a profile.
Component weights are numeric and bounded.
Disabled components remain visible.
Default profiles exist.
Budget Aware is generic only.
User-specific budget limits are not stored.
Profile versions are preserved.
Analysis profiles record weight_profile_id and weight_profile_version.
Analysis profiles record decision_version and evidence_version.
Old profile version replay data remains distinguishable from new version.
Compatibility reports are informational only.
All weight-affecting components serialize visibly.
Primer context components cannot replace measured metric components.
Simulator components remain simulator-only.
Caveat/conflict penalty components remain visible.
Private metadata is rejected.
Nested private metadata is rejected.
Unsupported strategic language is rejected.
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
python -m unittest tests.test_weight_profiles -v
```

Expected:

```text
Ran 15 tests
OK
```

Run full suite:

```powershell
python -m unittest discover -s tests
```

Expected:

```text
Ran 761 tests
OK (skipped=1)
```

## Static Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.repositories|codie\.ingestion|codie\.canonical|codie\.analytics|codie\.cards|codie\.probability_engine|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\weight_profiles tests\test_weight_profiles.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload|provider_payload|private_deck_text|full_primer_body|original_import_text" codie\weight_profiles tests\test_weight_profiles.py
```

Expected:

```text
matches only blocked-key constants and rejection tests
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\weight_profiles tests\test_weight_profiles.py
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\weight_profiles
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\weight_profiles tests\test_weight_profiles.py
git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories
```

Expected:

```text
no matches
```

## Reject If

Reject Phase 27 if:

```text
Weight profiles generate recommendations.
Weight profiles generate deck health output.
Weight profiles generate replacement suggestions.
Weight profiles are treated as evidence.
Weight profiles hide components that affect weighting.
Weight profiles store user-specific budget limits.
Primer context can replace measured metrics.
Simulator comparisons are treated as tournament evidence.
Caveat or conflict penalties can disappear silently.
Compatibility reports block replay of old analyses.
Production code imports DB, repositories, providers, ingestion, canonicalization, analytics recalculation, cards, simulator execution, UI, server frameworks, or LLM SDKs.
Production code contains raw SQL.
Production code writes files.
Schema or repository drift exists.
```

## Next Phase Gate

Phase 28 must not start until this validation returns PASS or PASS WITH REVIEW
NOTES.
