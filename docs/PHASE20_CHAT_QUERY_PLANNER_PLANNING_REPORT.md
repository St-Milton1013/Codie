# Phase 20 - Chat Query Planner Planning Report

## Status

```text
Phase 20 Planning: COMPLETE
Validation: PASS
```

## Scope

Created:

```text
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_CONTRACT.md
docs/PHASE20_CHAT_QUERY_PLANNER_PLANNING_REPORT.md
```

## Planning Decision

Phase 20 starts with:

```text
Phase 20A - Chat Query Planner Contract
```

This is the next dependency-safe Interactive Intelligence layer after the
Unsupported Relevant Card Queue.

## Why This Is Next

Codie now has structured evidence primitives and review surfaces:

```text
Evidence Graph
Evidence Graph Input Assembly
Source Conflict Report
Unsupported Relevant Card Queue
```

The next safe layer is a planner that classifies a user question and produces a
structured plan for future answer builders.

It must not produce the answer itself.

## Boundary Summary

Phase 20 planning blocks:

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

Documentation-only packet.

Static validation:

```text
git diff --check: PASS
Phase 20 planning strategic-language scan: PASS
schema/repository drift scan: PASS
```

Full suite validation:

```text
Ran 611 tests in 3.968s

OK (skipped=1)
```

## Next Packet

```text
Phase 20A - Chat Query Planner Contract
```
