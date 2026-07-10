# Phase 30A Outside Validation Packet Message

Use this message when sending Phase 30A for outside validation.

```text
Validate Codie Phase 30A against the Local Alpha Release Checklist.

Phase 30A is documentation/checklist only. It must not be treated as new
feature implementation.

Review:

docs/PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_CONTRACT.md
docs/CHECKPOINT_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_PROMPT.md
docs/PRE_PHASE30_AUDIT_REPORT.md
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

Confirm:

- Phase 30A adds no production code.
- Phase 30A adds no schema, repositories, providers, UI, LLM calls, or live
  network behavior.
- Phase 30A does not implement SIM-R.
- Phase 30A does not implement strategist mode.
- Phase 30A does not implement Tag Graph Lab.
- Phase 30A does not implement Moxfield Frequency Pool Builder.
- Phase 30A does not generate recommendations.
- Active roadmap, validation status, next phase, and handoff docs agree.
- Known caveats are visible.
- Phase 30B remains blocked until Phase 30A returns PASS or PASS WITH REVIEW
  NOTES.

Run from a clean checkout:

python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check

Run status drift scans from:

docs/OUTSIDE_VALIDATION_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_PROMPT.md

Return:

PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 30B.
```

