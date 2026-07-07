# Phase 21A - Chat Answer Builder Contract Report

## Status

```text
Phase 21A Chat Answer Builder Contract: COMPLETE
Recommended next task: Phase 21B - Chat Answer Builder Implementation
```

## Files Created

```text
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT.md
docs/PHASE21A_CHAT_ANSWER_BUILDER_CONTRACT_REPORT.md
```

## Contract Summary

Phase 21A defines a pure answer builder:

```text
ChatQueryPlan + already-sanitized evidence inputs -> structured cited ChatAnswer
```

The contract keeps answer building separate from retrieval, databases,
providers, LLMs, simulator execution, analytics, persistence, UI, and
recommendation generation.

## Future Public Interface

Phase 21B should implement:

```text
ChatAnswerBuildError
ChatAnswerInput
ChatAnswerSection
ChatAnswerCitation
ChatAnswerCaveat
ChatAnswerMissingEvidence
ChatAnswer
ChatAnswerBuilderOptions
build_chat_answer(...)
chat_answer_to_dict(...)
```

## Future Implementation Files

```text
codie/intelligence/answer_builder.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
```

## Boundary Rules

The future implementation may consume:

```text
ChatQueryPlan
EvidenceInputRecord
EvidenceGraph
SourceConflictReport
UnsupportedCardQueue
already-sanitized summaries
```

The future implementation must not:

```text
query SQLite
import repositories
call providers
read source/provider tables
read raw provider payloads
call LLMs
run simulator logic
implement card behavior
calculate analytics
generate recommendations
persist chat records
write files
export private raw_input
```

## Evidence Rules

Every factual section must either:

```text
include citation_ids
or include missing_evidence_ids
```

Unknown answers may omit citations only when explicitly caveated and must not
make confident factual claims.

Required evidence needs from the query plan must either be satisfied by
sanitized input or represented by `ChatAnswerMissingEvidence`.

## Privacy Rules

The contract forbids these keys anywhere in answer input or output metadata:

```text
raw_input
private_deck_text
full_primer_body
raw_provider_payload
provider_payload
original_import_text
```

including nested and punctuation-variant appearances.

## Language Rules

The contract allows evidence-descriptive language and forbids unsupported
strategy/recommendation language.

Forbidden phrases include:

```text
you should play
you should cut
must include
correct card
strict upgrade
auto-include
recommended cut
recommended include
secretly optimal
breaks the format
```

## Required Phase 21B Tests

Phase 21B must test:

```text
deck_summary plan builds cited answer sections
card_evidence plan builds cited answer sections
commander_evidence plan builds cited answer sections
comparison plan builds cited answer sections
source_conflict plan preserves conflict caveats
unsupported_card plan preserves unsupported-card warnings
simulation_review plan preserves simulator caveats without running simulator
unknown plan emits caveated unknown answer
missing required evidence creates missing_evidence entries
missing optional evidence creates non-blocking caveat
sections without citations fail unless explicitly marked as missing-evidence or unknown
plan blockers are preserved
plan caveats are preserved
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
answer serialization is deterministic
module has no forbidden imports, raw SQL, DB reads, provider calls, file writes, or LLM calls
```

## Schema Impact

```text
None.
```

Phase 21A is contract-only.

## Next Step

Proceed to:

```text
Phase 21B - Chat Answer Builder Implementation
```

Do not start chat UI, LLM writer/auditor workflows, persistence, DB retrieval,
provider calls, simulator integration, analytics, or recommendation generation
from this contract.
