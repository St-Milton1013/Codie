# Outside Validation Prompt - Phase 32B Scryfall Bulk Data Foundation Implementation Contract

Validate Codie Phase 32B against `CODIE_V1_CONSTITUTION.md`, the accepted
Phase 32A contract, the post-Phase 31 priority plan, and the accepted Phase 2
Scryfall truth contract.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm:

```text
Phase 32A is recorded as PASS WITH REVIEW NOTES.
Phase 32B is implementation-contract-only.
Phase 32B defines the exact future implementation surface.
Phase 32B does not add production code, tests, fixtures, schema, repositories, providers, dependencies, live network calls, UI, LLM calls, file writing, or recommendations.
Phase 32B preserves existing Scryfall identity rules.
Phase 32B keeps implementation fixture-first and local-only.
Phase 32B keeps Phase 32C blocked until outside validation passes.
```

## Commands To Run From Clean Checkout

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Static Scans

```powershell
git diff --name-only HEAD~1..HEAD -- codie tests tests\fixtures codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|recommendations|analytics|decision|evidence|openai|anthropic|google\.generativeai|langchain" docs\PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
```

Expected:

```text
No production/test/fixture/schema/repository/dependency drift.
Forbidden strings may appear only in explicit forbidden-scope lists.
```

## Reject If

```text
Phase 32B implements Scryfall bulk snapshot code.
Phase 32B adds fixtures or tests before the implementation packet.
Phase 32B changes existing Scryfall lookup behavior.
Phase 32B adds live network behavior.
Phase 32B adds schema, repositories, dependencies, providers, UI, LLM calls, file writing, or recommendations.
Phase 32B starts migration monitoring, Tagger import, or recommendation work.
```

## Gate

```text
Phase 32C remains blocked until Phase 32B outside validation returns PASS or PASS WITH REVIEW NOTES.
```
