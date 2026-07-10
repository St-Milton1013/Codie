# Outside Validation Prompt - Phase 30D Local Alpha Tag / Release Notes / Handoff Finalization

Validate Codie Phase 30D against:

```text
docs/PHASE30D_LOCAL_ALPHA_TAG_RELEASE_HANDOFF_CONTRACT.md
docs/LOCAL_ALPHA_RELEASE_NOTES.md
docs/LOCAL_ALPHA_TAG_PLAN.md
docs/LOCAL_ALPHA_FINAL_HANDOFF.md
docs/CHECKPOINT_PHASE30D_LOCAL_ALPHA_TAG_RELEASE_HANDOFF_REPORT.md
docs/PHASE30C_LOCAL_ALPHA_RELEASE_CANDIDATE_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE30C_LOCAL_ALPHA_RELEASE_CANDIDATE_REPORT.md
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
Phase 30C is PASS
Phase 30D is documentation-only
release notes exist
tag plan exists
final handoff exists
recommended tag is local-alpha-0.1.0
tag creation has not been performed by Phase 30D
known caveats are visible
deferred roadmap remains deferred
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

Run production-touch check:

```text
git diff --name-only -- codie tests scripts ui .github requirements.txt requirements-dev.txt pyproject.toml docs\SCHEMA_SPEC.md codie\db
```

Expected:

```text
schema bootstrap passes
full suite passes
git diff --check passes
no production code, tests, schema, dependency, UI, scripts, or CI changes
```

Reject if:

```text
Phase 30D creates a Git tag before validation
Phase 30D changes runtime code
Phase 30D changes schema or dependencies
Phase 30D hides caveats
Phase 30D promotes deferred roadmap work
Phase 30D claims production readiness
tests fail
schema bootstrap fails
```

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before creating the local alpha tag.
