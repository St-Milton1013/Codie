# Phase 22 - LLM Writer/Auditor Planning Report

## Status

```text
Phase 22 planning: COMPLETE
Recommended next task: Phase 22A - LLM Writer/Auditor Boundary Contract
```

## Decision

Phase 22 should start with a contract for an optional LLM Writer/Auditor
boundary.

The selected lane is:

```text
structured ChatAnswer -> writer draft -> auditor verdict -> accepted/rejected render text
```

This keeps Phase 22 inside the Interactive Intelligence architecture without
starting real LLM calls, chat UI, cloud provider wiring, persistence, database
reads, provider calls, simulator execution, analytics calculation, or
recommendation generation.

## Files Created

```text
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_CONTRACT.md
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_REPORT.md
```

## Recommended Phase 22A Files

```text
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Future implementation files, after contract acceptance:

```text
codie/intelligence/llm_writer_auditor.py
tests/test_intelligence_llm_writer_auditor.py
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
```

## Recommended Public Interface

Future implementation should define:

```text
LLMWriterAuditorBuildError
LLMWriterInput
LLMWriterDraft
LLMAuditFinding
LLMAuditResult
LLMWriterAuditorOptions
build_writer_input_from_answer(...)
validate_writer_draft(...)
audit_writer_draft(...)
llm_writer_draft_to_dict(...)
llm_audit_result_to_dict(...)
```

## Guardrails Preserved

Phase 22 planning adds no:

```text
implementation code
schema changes
DB reads or writes
repository imports
provider calls
source/provider table reads
raw provider payload reads
LLM calls
LLM SDK imports
UI
simulator execution
card behavior implementation
analytics calculation
recommendation generation
file writing
private raw_input export
```

## Boundary Rules

Future writer/auditor work should:

```text
consume structured ChatAnswer values only
preserve citations
preserve caveats
preserve missing_evidence
preserve blockers
reject uncited added claims
reject hidden caveats
reject hidden missing evidence
reject forbidden strategic language
reject private/raw metadata
```

Future writer/auditor work must not:

```text
retrieve evidence itself
query SQLite
call providers
call real LLM APIs in Phase 22B
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
Phase 22A - LLM Writer/Auditor Boundary Contract
```

Phase 22A should define the contract only. Do not implement
`codie/intelligence/llm_writer_auditor.py` until the contract is written and
accepted.
