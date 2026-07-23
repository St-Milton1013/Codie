# Outside Validation - Phase 40C Relationship Intelligence Schema and Repository Implementation Contract

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE40C_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE40C_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40C_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT.md
docs/CHECKPOINT_PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT_REPORT.md
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 40C:

```text
records exact Phase 40B acceptance evidence
is implementation-contract-only
declares an explicit Phase40C to Phase40D tuple
limits Phase 40D to the named schema, repository, spec, and existing test files
defines exactly five analytics-owned tables
preserves immutable manifests and measurements
preserves raw counts and null reasons
requires foreign keys, deterministic identities, transactions, rollback, and indexes
keeps calculations and population construction outside repositories
keeps private user content outside global populations
keeps all deferred relationship concepts deferred
does not change active scope, constitutions, production, tests, schema, repositories,
dependencies, workflows, UI, providers, LLM, simulator, or network behavior
```

Run:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Allowed verdicts:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase 40D remains blocked until PASS or PASS WITH REVIEW NOTES.

