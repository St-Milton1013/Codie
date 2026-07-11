# Outside Validation Prompt - Phase 32A Scryfall Bulk Data Foundation Contract

Validate Codie Phase 32A against `CODIE_V1_CONSTITUTION.md`, the accepted
post-Phase 31 priority plan, the Codie master architecture patch, and the
accepted Phase 2 Scryfall truth contract.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
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
Phase 31R is recorded as PASS WITH REVIEW NOTES.
Phase 32A is contract-only.
Phase 32A is aligned with Priority 1: Scryfall Bulk Data Foundation.
Phase 32A does not implement bulk download.
Phase 32A does not call live Scryfall APIs.
Phase 32A does not modify existing card lookup behavior.
Phase 32A does not add schema, repositories, providers, dependencies, UI, LLM calls, file writing, or recommendations.
Phase 32A preserves existing scryfall_id/oracle_id identity rules.
Phase 32A requires fixture-first future implementation.
Phase 32A requires no live network dependency in future tests.
Phase 32A keeps migration monitoring and Tagger import as later contracts.
Phase 32B remains blocked until Phase 32A outside validation returns PASS or PASS WITH REVIEW NOTES.
```

## Commands To Run From Clean Checkout

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Static Scans

```powershell
git diff --name-only HEAD~1..HEAD -- codie tests codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|recommendations|analytics|decision|evidence|openai|anthropic|google\.generativeai|langchain" docs\PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
```

Expected:

```text
No production/test/schema/repository/dependency drift.
Forbidden strings may appear only in explicit forbidden-scope lists.
```

## Reject If

```text
Phase 32A implements Scryfall bulk snapshot code.
Phase 32A changes existing Scryfall lookup behavior.
Phase 32A adds live network behavior.
Phase 32A adds schema, repositories, dependencies, providers, UI, LLM calls, file writing, or recommendations.
Phase 32A starts migration monitoring, Tagger import, or recommendation work.
```

## Gate

```text
Phase 32B remains blocked until Phase 32A outside validation returns PASS or PASS WITH REVIEW NOTES.
```
