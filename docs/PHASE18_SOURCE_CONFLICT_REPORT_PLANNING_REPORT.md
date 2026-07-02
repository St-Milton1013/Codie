# Phase 18 - Source Conflict Report Planning Report

## Status

```text
Phase 18 Planning: COMPLETE
Validation: PASS
```

## Decision

Phase 18 starts with:

```text
Phase 18A - Source Conflict Report Contract
```

This follows Phase 17 without jumping directly to chat UI, LLM phrasing,
persistence, or recommendation generation.

## Scope

Created:

```text
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_CONTRACT.md
docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_REPORT.md
```

## Rationale

Codie needs a structured way to preserve disagreement between sanitized evidence
records.

Source conflict reports should let future UI/chat/report surfaces show conflict,
uncertainty, missing data, stale data, privacy redactions, and unsupported
behavior without choosing a winner source or inventing strategic conclusions.

## Guardrails Preserved

Phase 18 planning authorizes no:

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

## Recommended Phase 18A Contract

Phase 18A should define:

```text
codie/intelligence/source_conflicts.py
tests/test_intelligence_source_conflicts.py
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
```

Future public interface:

```text
SourceConflictBuildError
SourceConflictEvidenceRef
SourceConflictItem
SourceConflictReport
SourceConflictReportOptions
build_source_conflict_report(...)
source_conflict_report_to_input_records(...)
source_conflict_report_to_dict(...)
```

## Validation

Documentation-only packet.

Static validation:

```text
git diff --check: PASS
Phase 18 strategic language scan: no matches
schema/repository drift scan: no matches
```

Full suite validation:

```text
Ran 566 tests in 3.192s

OK (skipped=1)
```

No tests were added because this packet adds no executable code.

## Next Packet

```text
Phase 18A - Source Conflict Report Contract
```
