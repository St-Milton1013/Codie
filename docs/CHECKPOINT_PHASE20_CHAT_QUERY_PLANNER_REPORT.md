# Checkpoint - Phase 20 Chat Query Planner

## Status

```text
Phase 20 Chat Query Planner Internal Checkpoint: PASS
Status: Ready for outside validation before Phase 21
```

This is an internal checkpoint, not external proof. Phase 21 should not start
until outside validation returns PASS or PASS WITH REVIEW NOTES.

## Scope Covered

Phase 20 includes:

```text
Phase 20 planning
Phase 20A Chat Query Planner contract
Phase 20B Chat Query Planner implementation
```

Files created or modified:

```text
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_CONTRACT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_REPORT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE20_CHAT_QUERY_PLANNER_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE20_CHAT_QUERY_PLANNER_PROMPT.md
codie/intelligence/__init__.py
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Implementation Summary

Phase 20B implements a pure deterministic chat query planner:

```text
ChatQueryPlanBuildError
ChatQueryRequest
ChatQuerySubject
ChatEvidenceNeed
ChatQueryConstraint
ChatQueryPlan
ChatQueryPlannerOptions
build_chat_query_plan(...)
chat_query_plan_to_dict(...)
```

The planner maps sanitized user requests into structured query plans for future
answer builders. It does not answer questions.

## Behavior Verified

Tests verify:

```text
deck summary request creates deck_summary plan
card evidence request creates card_evidence plan
commander evidence request creates commander_evidence plan
comparison request creates comparison plan
source conflict request creates source_conflict plan
unsupported card request creates unsupported_card plan
simulation review request creates simulation_review plan
tag graph request creates tag_graph plan
unknown request creates caveated unknown plan
plans serialize deterministically
explicit constraints are preserved
privacy scopes are enforced
sensitive scope is blocked by default
local_user_data scope is blocked by default
private metadata keys fail cleanly
nested private metadata keys fail cleanly
too many evidence needs fail cleanly
too many constraints fail cleanly
forbidden strategic language fails cleanly
module has no forbidden imports
module has no raw SQL
module has no file-writing behavior
```

## Boundary Summary

Phase 20 remains:

```text
pure
in-memory
sanitized-input only
deterministic
privacy-aware
evidence-first
```

It adds no:

```text
schema changes
DB reads or writes
repository imports
provider calls
source/provider table reads
raw provider payload reads
LLM calls
UI
answer generation
simulator execution
card behavior implementation
analytics calculation
recommendation generation
file writing
private raw_input export
```

## Validation Output

Focused tests:

```text
python -m unittest tests.test_intelligence_query_planner -v

Ran 20 tests in 0.002s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 631 tests in 3.223s

OK (skipped=1)
```

Static scans:

```text
git diff --check: PASS
forbidden import scan: no matches
raw SQL scan: no matches
production file-write scan: no matches
source/provider table scan: no matches
private metadata production scan: matches only blocked-key constants/rejection logic
strategic-language scan: no matches
schema/repository drift scan: no matches
```

## Review Notes

```text
ChatQueryPlan is a plan, not an answer.
The planner does not call an LLM.
The planner does not retrieve data from SQLite.
The planner does not call providers.
The planner does not run simulator logic.
The planner does not generate recommendations.
The planner does not export private deck text.
```

## Required Outside Validation

Send:

```text
docs/CHECKPOINT_PHASE20_CHAT_QUERY_PLANNER_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE20_CHAT_QUERY_PLANNER_PROMPT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
codie/intelligence/__init__.py
```

## Phase 21 Gate

```text
Phase 21 is blocked until outside validation returns PASS or PASS WITH REVIEW NOTES.
```
