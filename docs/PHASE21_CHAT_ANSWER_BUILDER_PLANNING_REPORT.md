# Phase 21 - Chat Answer Builder Planning Report

## Status

```text
Phase 21 planning: COMPLETE
Recommended next task: Phase 21A - Chat Answer Builder Contract
```

## Decision

Phase 21 should start with a contract for a pure Chat Answer Builder.

The selected lane is:

```text
ChatQueryPlan + sanitized evidence inputs -> structured cited ChatAnswer
```

This keeps Phase 21 inside the Interactive Intelligence architecture without
starting chat UI, LLM calls, persistence, database reads, provider calls,
simulator execution, analytics calculation, or recommendation generation.

## Files Created

```text
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_CONTRACT.md
docs/PHASE21_CHAT_ANSWER_BUILDER_PLANNING_REPORT.md
```

## Recommended Phase 21A Files

```text
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Future implementation files, after the contract is accepted:

```text
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
```

## Recommended Public Interface

Future implementation should define:

```text
ChatAnswerBuildError
ChatAnswerInput
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswer
ChatAnswerBuilderOptions
build_chat_answer(...)
chat_answer_to_dict(...)
```

## Guardrails Preserved

Phase 21 planning adds no:

```text
implementation code
schema changes
DB reads or writes
repository imports
provider calls
source/provider table reads
raw provider payload reads
LLM calls
UI
simulator execution
card behavior implementation
analytics calculation
recommendation generation
file writing
private raw_input export
```

## Answer Builder Boundaries

The future answer builder should:

```text
consume ChatQueryPlan values
consume already-sanitized evidence objects
produce structured answer sections
attach citations to factual sections
preserve caveats and blockers
surface missing evidence explicitly
serialize deterministically
reject private/raw metadata
reject forbidden strategic language
```

The future answer builder must not:

```text
retrieve evidence itself
query SQLite
call providers
call an LLM
run simulator logic
implement card behavior
calculate analytics
create recommendation candidates
emit deck-construction instructions
persist chat records
write export files
```

## Next Step

Proceed to:

```text
Phase 21A - Chat Answer Builder Contract
```

Phase 21A should define the contract only. Do not implement
`codie/intelligence/answer_builder.py` until the contract is written and
accepted.
