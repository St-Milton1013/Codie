# Phase 20B - Chat Query Planner Implementation Report

## Status

```text
Phase 20B Implementation: COMPLETE
Validation: PASS
```

## Scope

Created:

```text
codie/intelligence/query_planner.py
tests/test_intelligence_query_planner.py
docs/PHASE20B_CHAT_QUERY_PLANNER_IMPLEMENTATION_REPORT.md
```

Modified:

```text
codie/intelligence/__init__.py
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Interface Implemented

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

## Behavior Implemented

Phase 20B implements a pure deterministic query planner for sanitized user
questions.

The planner:

```text
classifies supported question classes
preserves explicit subjects
preserves explicit constraints
derives evidence needs from question class
derives allowed operations from evidence needs
blocks sensitive scope by default
blocks local_user_data scope by default
emits caveats when requested privacy scope is not allowed
emits caveated unknown plans for unsupported questions
serializes deterministically
rejects private metadata keys, including nested keys
rejects forbidden strategic phrasing
```

## Boundary Summary

Phase 20B remains:

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

## Validation

Focused tests:

```text
Ran 22 tests in 0.003s

OK
```

Full suite:

```text
Ran 633 tests in 3.293s

OK (skipped=1)
```

Static scans:

```text
git diff --check: PASS
forbidden import scan: no matches
raw SQL scan: no matches
production file-write scan: no matches
strategic-language scan: no matches
schema/repository drift scan: no matches
```
