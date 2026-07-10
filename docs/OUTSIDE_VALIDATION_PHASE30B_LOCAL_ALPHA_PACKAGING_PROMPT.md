# Outside Validation Prompt - Phase 30B Local Alpha Packaging / Usage Documentation

Validate Codie Phase 30B against:

```text
docs/PHASE30B_LOCAL_ALPHA_PACKAGING_USAGE_CONTRACT.md
docs/LOCAL_ALPHA_README.md
docs/LOCAL_ALPHA_COMMANDS.md
docs/LOCAL_ALPHA_KNOWN_CAVEATS.md
docs/LOCAL_ALPHA_VALIDATION_STEPS.md
docs/CHECKPOINT_PHASE30B_LOCAL_ALPHA_PACKAGING_REPORT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm:

```text
Phase 30A is marked PASS.
Phase 30B is documentation-only.
Local alpha README exists and is accurate.
Command guide documents only accepted CLI modules.
Command guide does not claim recommendation generation.
Command guide states local DB prerequisites where needed.
Known caveats are visible.
Deferred roadmap features remain deferred.
SIM-R remains deferred.
Strategist mode remains deferred.
No production code changes exist.
No schema changes exist.
No dependency changes exist.
No CI changes exist.
Phase 30C remains blocked until Phase 30B outside validation is accepted.
```

Run from a clean checkout:

```text
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

Run production touch check:

```text
git diff --name-only -- codie tests scripts ui .github requirements.txt requirements-dev.txt pyproject.toml docs\SCHEMA_SPEC.md codie\db
```

Expected:

```text
no production code, tests, schema, dependency, UI, scripts, or CI changes for Phase 30B
```

Reject if:

```text
Phase 30B adds runtime behavior
Phase 30B advertises unsupported commands as alpha-ready
Phase 30B claims final recommendation generation exists
Phase 30B claims SIM-R is implemented
Phase 30B hides local DB prerequisites
Phase 30B hides Hareruya/live-provider caveats
Phase 30B includes secrets or private local-only paths as required usage
```

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 30C.
