# Outside Validation Prompt - Phase 30A Local Alpha Release Checklist

Validate Codie Phase 30A against:

```text
docs/CODIE_V1_CONSTITUTION.md
docs/PRE_PHASE30_AUDIT_REPORT.md
docs/PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_CONTRACT.md
docs/CHECKPOINT_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_REPORT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
.github/workflows/tests.yml
scripts/check_schema.py
pyproject.toml
requirements.txt
requirements-dev.txt
```

Confirm:

```text
Phase 30A is checklist/documentation only
Phase 30A does not add production code
Phase 30A does not add schema
Phase 30A does not add repositories
Phase 30A does not add providers
Phase 30A does not add live network behavior
Phase 30A does not add UI
Phase 30A does not add LLM calls
Phase 30A does not implement SIM-R
Phase 30A does not implement strategist mode
Phase 30A does not implement Tag Graph Lab
Phase 30A does not implement Moxfield Frequency Pool Builder
Phase 30A does not generate recommendations
active roadmap, validation status, next phase, and handoff docs agree
known caveats are visible
next packet is Phase 30B local alpha packaging/docs unless separately contracted
```

Run from a clean checkout:

```text
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

Run status drift scans:

```text
rg -n "Phase 29F.*INTERNAL PASS|blocked until Phase 29F|review Phase 29F|Phase 30A.*blocked|Current Phase 29F Review Packet|Do not start Phase 30A" docs\ACTIVE_ROADMAP_INDEX.md docs\VALIDATION_STATUS_INDEX.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md docs\PRE_PHASE30_AUDIT_REPORT.md docs\PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_CONTRACT.md docs\CHECKPOINT_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_REPORT.md
rg -n "Phase 30A" docs\POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```

Expected:

```text
no stale Phase 29F / Phase 30A gate matches
no post-alpha patch backlog item still claiming Phase 30A
schema bootstrap passes
full suite passes
git diff --check passes
```

Reject if:

```text
Phase 30A implements new behavior instead of a release checklist
Phase 30A promotes roadmap-only patches into implementation
SIM-R is implemented or authorized without a dedicated contract
strategist mode is implemented or authorized without a dedicated contract
active status docs disagree about the current phase
known caveats are hidden
tests fail
schema bootstrap fails
```

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 30B.
