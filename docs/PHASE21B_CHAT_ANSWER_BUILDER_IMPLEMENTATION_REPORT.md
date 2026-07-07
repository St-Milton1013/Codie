# Phase 21B - Chat Answer Builder Implementation Report

## Status

```text
Phase 21B Chat Answer Builder Implementation: COMPLETE
Recommended next task: Phase 21C - Chat Answer Builder Checkpoint
```

## Files Created Or Modified

```text
codie/intelligence/answer_builder.py
codie/intelligence/__init__.py
tests/test_intelligence_answer_builder.py
docs/PHASE21B_CHAT_ANSWER_BUILDER_IMPLEMENTATION_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Interface Implemented

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

## Implementation Summary

The implementation is a pure in-memory answer builder:

```text
ChatQueryPlan + already-sanitized evidence inputs -> structured cited ChatAnswer
```

It consumes accepted query plans and already-built sanitized evidence objects.
It does not retrieve evidence itself.

## Behavior Implemented

```text
deck_summary plans build cited answer sections
card_evidence plans build cited answer sections
commander_evidence plans build cited answer sections
comparison plans build cited answer sections
source_conflict plans preserve conflict caveats
unsupported_card plans preserve unsupported-card warnings
simulation_review plans preserve simulator caveats without running simulator
tag_graph context summaries create citations
unknown plans emit caveated unknown answers
missing required evidence creates missing_evidence entries
missing optional evidence creates non-blocking caveats
sections without citations fail unless marked as missing-evidence or unknown
plan blockers are preserved
plan caveats are preserved
private metadata keys fail cleanly
nested private metadata keys fail cleanly
forbidden strategic language fails cleanly
answer serialization is deterministic
```

## Boundary Summary

Phase 21B remains:

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
python -m unittest tests.test_intelligence_answer_builder -v

Ran 18 tests in 0.003s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 651 tests in 3.192s

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
ChatAnswer is a structured answer object, not an LLM message.
The builder does not query SQLite.
The builder does not call providers.
The builder does not run simulator logic.
The builder does not generate recommendations.
The builder does not export private deck text.
```

## Next Step

Proceed to:

```text
Phase 21C - Chat Answer Builder Checkpoint
```

The checkpoint should cover Phase 21 planning, Phase 21A contract, Phase 21B
implementation, boundary scans, test output, and outside validation prompt.
