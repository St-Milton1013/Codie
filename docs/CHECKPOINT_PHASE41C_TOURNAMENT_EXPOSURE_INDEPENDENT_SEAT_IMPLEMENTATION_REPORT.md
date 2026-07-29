# Checkpoint - Phase 41C Tournament Exposure Independent-Seat Implementation

Status: INTERNAL PASS

## Validation Tuple

```text
phase_id: Phase41C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Behavior Verified

```text
all three constitutional formulas match hand-calculated cases
zero and one metagame-share boundaries remain valid
exact rational intermediates avoid float-dependent equality
12-place decimal serialization is deterministic
expected attendance does not alter formula outputs
target and partner-pair identities remain visible and normalized
all required target and scope types are accepted
invalid counts, dates, coverage, references, and models fail closed
sample and coverage labels remain visible
local and regional comparisons preserve their global baseline
incompatible comparisons fail visibly
preparation briefs remain evidence-only
packet objects and caller inputs remain immutable
timestamps normalize deterministically to UTC
tampered packet values and identities fail validation
bundle ordering and references are deterministic
```

## Boundaries Verified

```text
no schema, migration, repository, or SQL change
no provider, source-table, raw-payload, or private-deck read
no observation ingestion or population construction
no Swiss, standings, pod, repeat-opponent, bye, matchup, placement, or win-rate model
no recommendation or Decision Intelligence output
no Relationship Intelligence change
no Jin, simulator, UI, CLI, LLM, network, or file-writing behavior
no dependency, validator, workflow, active-scope, or constitution change
```

## Focused Validation

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_tournament_exposure -v
Ran 17 tests
OK
```

## Full Validation

```text
git diff --check
passed

C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
Schema bootstrap check passed.

C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
Ran 1178 tests
OK (skipped=1)
```

## Gate

Phase 41D remains blocked until Phase 41C outside validation returns PASS or
PASS WITH REVIEW NOTES.
