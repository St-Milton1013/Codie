# Phase 17 - Interactive Intelligence Input Assembly Planning Report

## Status

```text
Phase 17 Planning: COMPLETE
Validation: PASS
```

## Decision

Phase 17 starts with:

```text
Phase 17A - Evidence Graph Input Assembly Contract
```

This follows Phase 16 without jumping directly to chat UI, LLM phrasing,
persistence, or recommendation generation.

## Scope

Created:

```text
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
```

## Rationale

The evidence graph now exists as an in-memory primitive.

The next safe layer is a pure adapter boundary:

```text
sanitized read models
-> EvidenceGraphInput
-> build_evidence_graph(...)
```

This keeps data access and domain semantics owned by their existing layers while
letting future UI/chat/report surfaces consume a consistent evidence structure.

## Guardrails Preserved

Phase 17 planning authorizes no:

```text
schema changes
DB reads or writes
repository imports
provider calls
source/provider table reads
raw provider payload reads
LLM calls
chat UI
simulator execution
analytics calculation
recommendation generation
file writing
private raw_input export
```

## Recommended Phase 17A Contract

Phase 17A should define:

```text
codie/intelligence/evidence_inputs.py
tests/test_intelligence_evidence_inputs.py
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
```

Future public interface:

```text
EvidenceInputBuildError
EvidenceRecordRef
EvidenceInputRecord
EvidenceInputBundle
EvidenceGraphAssemblyOptions
evidence_record_from_dict(...)
validate_evidence_input_bundle(...)
build_graph_input_from_records(...)
```

## Validation

Documentation-only packet.

Static validation:

```text
git diff --check: PASS
Phase 17 strategic language scan: no matches
schema/repository drift scan: no matches
```

Full suite validation:

```text
Ran 547 tests in 3.190s

OK (skipped=1)
```

No tests were added because this packet adds no executable code.

## Next Packet

```text
Phase 17A - Evidence Graph Input Assembly Contract
```
