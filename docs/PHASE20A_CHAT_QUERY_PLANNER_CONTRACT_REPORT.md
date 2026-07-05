# Phase 20A - Chat Query Planner Contract Report

## Status

```text
Phase 20A Contract: COMPLETE
Validation: PASS
```

## Scope

Created:

```text
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT.md
docs/PHASE20A_CHAT_QUERY_PLANNER_CONTRACT_REPORT.md
```

## Contract Summary

Phase 20A defines a future pure chat query planner:

```text
sanitized question request
-> ChatQueryPlan
-> deterministic query-plan payload for future answer builders
```

The contract defines:

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

## Boundary Summary

The future implementation is allowed to import only:

```text
standard library
codie.intelligence.evidence_inputs
```

The contract blocks:

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

## Privacy Summary

The contract requires rejection of:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested metadata keys.

Local user data may be referenced only through subject keys, record IDs,
privacy scopes, and caveats.

## Validation

Documentation-only packet.

Static validation:

```text
git diff --check: PASS
Phase 20A strategic-language scan: PASS
schema/repository drift scan: PASS
```

Full suite validation:

```text
Ran 611 tests in 3.968s

OK (skipped=1)
```

No tests were added because this packet adds no executable code.

## Next Packet

```text
Phase 20B - Chat Query Planner Implementation
```
