# Checkpoint - Phase 27 Weight Profile / Analysis Profile

## Status

```text
Phase 27 Weight Profile / Analysis Profile Internal Checkpoint: PASS
Status: Ready for outside validation before Phase 28
```

This is an internal checkpoint, not external proof. Phase 28 should not start
until outside validation returns PASS or PASS WITH REVIEW NOTES.

## Scope Covered

Phase 27 includes:

```text
Phase 27A Weight Profile / Analysis Profile Contract
Phase 27B Weight Profile / Analysis Profile Packet Implementation
```

Files created or modified:

```text
docs/PHASE27A_WEIGHT_PROFILE_ANALYSIS_PROFILE_CONTRACT.md
codie/weight_profiles/__init__.py
codie/weight_profiles/models.py
codie/weight_profiles/defaults.py
tests/test_weight_profiles.py
docs/PHASE27B_WEIGHT_PROFILE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE27_WEIGHT_PROFILE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE27_WEIGHT_PROFILE_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Behavior Verified

Tests verify:

```text
weight profile serializes deterministically
analysis profile serializes deterministically
profile IDs and versions are required
component IDs are unique within a profile
component weights are numeric and bounded
disabled components remain visible
default profiles exist
Budget Aware remains generic and does not store user-specific limits
profile version is preserved
analysis profile records weight_profile_id and weight_profile_version
analysis profile records decision_version and evidence_version
old profile version replay data remains distinguishable from new version
compatibility reports are informational only
all weight-affecting components serialize visibly
primer context component cannot replace measured metric components
simulator component remains simulator-only
caveat/conflict penalty components remain visible
private metadata is rejected
nested private metadata is rejected
unsupported strategic language is rejected
module has no forbidden imports
module has no raw SQL
module has no production file-writing behavior
module has no live LLM calls or SDK imports
module has no server framework imports
```

## Boundary Summary

Phase 27 remains:

```text
pure
in-memory
packet-only
deterministic
versioned
recommendation-output-free
DB-free
provider-free
source-table-free
LLM-call-free
simulator-execution-free
UI-free
file-write-free
```

It adds no:

```text
schema changes
DB reads or writes
repository imports
provider calls
source/provider table reads
raw provider payload reads
analytics recalculation
recommendation generation
recommendation scoring
deck health output
replacement suggestions
real LLM calls
LLM SDK imports
Jin-Gitaxias theory generation
simulator execution
UI code
HTTP server
server framework imports
network client imports
file writing
private raw_input export
```

## Validation Output

Focused tests:

```text
python -m unittest tests.test_weight_profiles -v

Ran 15 tests in 0.002s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 761 tests in 3.499s

OK (skipped=1)
```

Static scans:

```text
git diff --check: PASS
forbidden import / network / LLM SDK / server framework scan: no matches
raw SQL scan: no matches
production file-write scan: no matches
strategic-language scan: no matches
source/provider/private metadata scan: matches only blocked-key constants and rejection tests
schema/repository drift scan: no matches
```

## Required Outside Validation

Send:

```text
docs/CHECKPOINT_PHASE27_WEIGHT_PROFILE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE27_WEIGHT_PROFILE_PROMPT.md
docs/PHASE27A_WEIGHT_PROFILE_ANALYSIS_PROFILE_CONTRACT.md
docs/PHASE27B_WEIGHT_PROFILE_IMPLEMENTATION_REPORT.md
codie/weight_profiles/__init__.py
codie/weight_profiles/models.py
codie/weight_profiles/defaults.py
tests/test_weight_profiles.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```
