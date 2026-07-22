# Checkpoint - Phase 37D Tag Graph Metric Packet Models

Status: local implementation prepared; validation required

This checkpoint records the Phase 37D local implementation state. It does not
mark Phase 37D externally complete.

```text
Phase 37C: PR-validated and used as the basis for continued Phase 37 work
Phase 37D: implementation prepared
Phase 37D outside validation: required
Phase 37E: blocked until Phase 37D returns PASS or PASS WITH REVIEW NOTES
```

## Scope Verified

```text
model/validator-only implementation
local fixtures only
no chart rendering
no export surfaces
no UI work
no repository-backed builders
no provider reads
no source table reads
no live network calls
no schema changes
no dependency changes
no LLM calls
no simulator runtime
no analytics recalculation
no action advice
no file writing
```

## Behavior Verified

```text
deterministic serialization
dictionary round-trip
immutable packet values
input payload immutability
graph type validation
selected tag count validation
duplicate selected tag rejection
tag provenance visibility
source_packet_ids visibility
caveat_ids visibility
numeric table visibility
card list visibility
metric row visibility
trend row visibility
overlap row visibility
correlation row visibility
contributor row visibility
explicit unknown markers
recursive private/raw metadata rejection
action-advice metadata rejection
action-advice language rejection
```

## Local Validation

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
Schema bootstrap check passed.

C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_tag_graph_models -v
Ran 13 tests
OK

C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
Ran 1060 tests
OK (skipped=1)

git diff --check
passed
```

## Validation Gate

Phase 37D must be validated before Phase 37E starts.

```text
phase_id: Phase37D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase37E
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```
