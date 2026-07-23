# Checkpoint - Phase 39B Cockatrice Interoperability Implementation Contract

Status: internal pass

## Validation Tuple

```text
phase_id: Phase39B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Scope Summary

Phase 39B is an implementation-contract-only packet. It defines the future
Phase 39C local, fixture-first Cockatrice interoperability implementation
boundary. It does not implement Cockatrice parsing, export packet building,
file writing, CLI behavior, schema changes, repositories, provider calls,
analytics, recommendations, simulator execution, UI, LLM calls, workflow
changes, validator changes, dependency changes, active validation scope
changes, or constitution changes.

## Accepted Phase 39A Evidence

```text
workflow run ID: 29969137239
validated SHA: bf1a966cbbf406820514ec1b2992688ed688bca1
artifact: codie-phase_ledger-validation-bf1a966cbbf406820514ec1b2992688ed688bca1
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with one INFORMATIONAL historical finding
aggregate: CLEAN_PASS
final governance verdict: PASS WITH REVIEW NOTES
required corrections: none
```

The informational finding references historical Phase 36B contract narrative
and has no required correction. It is nonblocking and does not create Phase 39B
repair work.

## Files Changed

```text
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Behavior Verified

```text
Phase 39A is recorded as PASS WITH REVIEW NOTES.
Phase 39A artifact evidence remains visible.
Phase 39B declares phase_id, phase_part, and gate_scope.
Phase 39B declares next_phase_id, next_phase_part, and next_gate_scope.
Phase 39B remains implementation-contract-only.
Phase 39B does not implement Cockatrice parser code.
Phase 39B does not implement Cockatrice export code.
Phase 39B does not add actual implementation test files or fixture files.
Phase 39B does not modify production code.
Phase 39B does not modify schema or repositories.
Phase 39B does not modify providers or analytics.
Phase 39B does not generate recommendations.
Phase 39B does not add simulator runtime behavior.
Phase 39B does not add UI, CLI, LLM, workflow, validator, or dependency changes.
Phase 39B does not modify active validation scope.
Phase 39B does not modify the constitution.
Phase 39C remains blocked until Phase 39B returns PASS or PASS WITH REVIEW NOTES.
```

## Future Boundary Verified

The Phase 39B contract defines future Phase 39C requirements for:

```text
local Cockatrice .cod XML payload parsing
in-memory import packet models
in-memory export packet models
commander and partner commander handling
mainboard, sideboard, and custom-zone handling
card-name and supplied-identity preservation
unsupported and unresolved card reporting
XML safety
privacy metadata rejection
deterministic serialization
dictionary round-trip behavior
fixture-first tests
recommendation-free output
file-writing-free output
```

These are future Phase 39C obligations, not Phase 39B completion criteria.
Phase 39B remains contract-only and must not be failed because implementation
tests or production behavior do not exist yet.

The Phase 39B packet contains textual future file allowlist entries only. It
does not create `codie/`, `tests/`, or `tests/fixtures/` files.

## Validation Commands

Local validation must run before PR validation:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

If the configured venv is unavailable, the exact alternate Python executable
must be reported.

## Static Scan Expectations

Outside validation should confirm:

```text
git diff --name-only
git diff --name-only -- codie tests schemas scripts .github requirements.txt requirements-dev.txt
rg -n "requests|httpx|sqlite3|codie\\.db|codie\\.providers|codie\\.analytics|codie\\.recommendations|codie\\.decision_intelligence|codie\\.evidence_fusion" docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
rg -n "recommend|should play|should cut|optimal|strict upgrade|deck health" docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
```

Matches inside explicit forbidden-boundary lists are allowed. Production, test,
schema, dependency, workflow, validator, and constitution files must not change.

## Final Decision

```text
Phase 39B checkpoint: INTERNAL PASS
Phase 39C: BLOCKED until Phase 39B outside validation returns PASS or PASS WITH REVIEW NOTES
```
