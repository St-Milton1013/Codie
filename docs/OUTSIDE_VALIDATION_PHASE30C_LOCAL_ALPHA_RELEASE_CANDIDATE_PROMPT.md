# Outside Validation Prompt - Phase 30C Local Alpha Release Candidate

Validate Codie Phase 30C against:

```text
docs/PHASE30C_LOCAL_ALPHA_RELEASE_CANDIDATE_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE30C_LOCAL_ALPHA_RELEASE_CANDIDATE_REPORT.md
docs/PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_CONTRACT.md
docs/CHECKPOINT_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_REPORT.md
docs/PHASE30B_LOCAL_ALPHA_PACKAGING_USAGE_CONTRACT.md
docs/CHECKPOINT_PHASE30B_LOCAL_ALPHA_PACKAGING_REPORT.md
docs/LOCAL_ALPHA_README.md
docs/LOCAL_ALPHA_COMMANDS.md
docs/LOCAL_ALPHA_KNOWN_CAVEATS.md
docs/LOCAL_ALPHA_VALIDATION_STEPS.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm:

```text
Phase 30A is PASS
Phase 30B is PASS
Phase 30C is checkpoint-only
local alpha docs are present
known caveats are visible
deferred features remain deferred
SIM-R remains deferred
strategist mode remains deferred
Tag Graph Lab remains deferred
Moxfield Frequency Pool Builder remains deferred
no production code changes exist
no schema changes exist
no dependency changes exist
no CI changes exist
no provider/live network behavior was added
no recommendation generation was added
```

Run from a clean checkout:

```text
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

Run status and production-touch scans:

```text
rg -n "Phase 30B.*INTERNAL PASS|blocked until Phase 30B|send Phase 30B outside validation|Current Phase 30B Outside Validation" docs\ACTIVE_ROADMAP_INDEX.md docs\VALIDATION_STATUS_INDEX.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
git diff --name-only -- codie tests scripts ui .github requirements.txt requirements-dev.txt pyproject.toml docs\SCHEMA_SPEC.md codie\db
```

Expected:

```text
schema bootstrap passes
full suite passes
git diff --check passes
no stale Phase 30B pending-validation matches
no production code, tests, schema, dependency, UI, scripts, or CI changes
```

Reject if:

```text
Phase 30C adds runtime behavior
Phase 30C hides caveats
Phase 30C promotes deferred roadmap work
Phase 30C claims production readiness
Phase 30C changes implementation files
Phase 30C changes schema or dependencies
tests fail
schema bootstrap fails
```

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 30D.
