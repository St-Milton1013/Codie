# Phase 38D - Moxfield Frequency Pool Builder Checkpoint Contract

Status: checkpoint contract only

## Validation Tuple

```text
phase_id: Phase38D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39A
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 38D closes the Moxfield Frequency Pool Builder track as a checkpoint and
freeze packet. It records the accepted Phase 38C implementation evidence,
confirms the implemented builder remains local and fixture-first, and prepares
the roadmap to move to the next deferred implementation priority.

Phase 38D does not implement new Moxfield behavior, live network access,
exports, CLI, UI, schema, repositories, analytics, recommendations, simulator
runtime, LLM behavior, validators, workflows, dependencies, active validation
scope changes, or constitution changes.

## Accepted Phase 38C Evidence

Phase 38C outside phase-ledger validation returned CLEAN_PASS.

```text
workflow run ID: 29962601660
validated SHA: bbacc28e00a0cc617f5443d834c47aba05835147
artifact: codie-phase_ledger-validation-bbacc28e00a0cc617f5443d834c47aba05835147
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with one INFORMATIONAL finding
aggregate: CLEAN_PASS
unresolved blocking findings: none
```

The adversarial informational finding is a nonblocking historical observation
from Phase 37A. It requires no corrective action and must not be treated as a
Phase 38C implementation defect.

## Phase 38D Scope

This phase may create or modify only:

```text
docs/PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

No production, test, fixture, schema, repository, provider, analytics,
recommendation, simulator, UI, LLM, workflow, validator, dependency, export,
active validation scope, or constitution files are authorized by Phase 38D.

## Checkpoint Requirements

Phase 38D must verify:

```text
Phase 38A is accepted
Phase 38B is accepted
Phase 38C is accepted
Phase 38C artifact-backed aggregate result is CLEAN_PASS
Phase 38C informational findings require no correction
Moxfield builder remains local and fixture-first
Moxfield builder performs no live network calls
Moxfield builder performs no provider or repository reads
Moxfield builder performs no schema writes
Moxfield builder performs no exports, CLI, or UI work
Moxfield builder produces no recommendations
known caveats remain visible
future live Moxfield access remains separately contracted
future exports remain separately contracted
future Cockatrice work begins contract-first only
```

## Phase 38 Completion Boundary

Phase 38D may close the current Moxfield Frequency Pool Builder track only as a
local, fixture-first builder checkpoint. It does not complete every roadmap
idea from `docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md`.

Still deferred after Phase 38D unless separately contracted:

```text
live Moxfield provider adapter
Moxfield API fetching
Scryfall identity lookup during Moxfield import
Markdown export
CSV export
JSON file export
Obsidian Markdown export
CLI command
UI tab
persistence schema
repository support
Decision Intelligence consumption
recommendation output
```

## Next Roadmap Gate

After Phase 38D returns PASS or PASS WITH REVIEW NOTES, the next allowed work
is Phase 39A, expected to begin the Cockatrice Interoperability track
contract-first according to the post-Phase 31 deferred implementation priority
plan.

Phase 39A must not begin implementation until its own accepted contract
authorizes concrete files and behavior.

## Active Scope Handling

The active validation scope declaration is protected from ordinary PR-head
modification. This Phase 38D PR must not modify
`docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`.

After Phase 38D is merged and accepted, any future active-scope transition must
occur through the approved governance path for protected scope updates.

## Forbidden In Phase 38D

Phase 38D must not add:

```text
production implementation code
tests for new implementation code
fixtures for new implementation code
schema changes
repository changes
SQLite reads or writes
provider changes
live Moxfield calls
Scryfall lookup calls
frequency calculation changes
analytics recalculation
exports
file writing
CLI behavior
UI behavior
LLM calls
simulator runtime
recommendation generation
deck health output
dependency changes
validator changes
workflow changes
active validation scope changes
constitution changes
```

## Outside Validation Packet

Outside validation should review:

```text
docs/PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_PROMPT.md
docs/PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_PROMPT.md
docs/PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT.md
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
codie/frequency_pools/moxfield_builder.py
codie/frequency_pools/models.py
codie/frequency_pools/__init__.py
tests/test_moxfield_frequency_pool_builder.py
tests/fixtures/moxfield_frequency_pools/
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Outside validation must confirm that Phase 38D is checkpoint-only and that
Phase 39A remains blocked until Phase 38D returns PASS or PASS WITH REVIEW
NOTES.

## Final Governance Summary

Phase 38D is complete when this checkpoint contract, checkpoint report,
outside-validation prompt, and governance records are internally consistent
and accepted by PR validation. Phase 39A remains blocked until Phase 38D
returns PASS or PASS WITH REVIEW NOTES.
