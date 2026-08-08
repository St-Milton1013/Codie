# Outside Validation Prompt - Phase 44B Goal Engine Foundation Implementation Contract

Validate Phase 44B as an implementation-contract-only packet.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only `PASS` or `PASS WITH REVIEW NOTES` may unblock Phase 44C.

## Required Review Files

```text
docs/PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/GOAL_ENGINE_V1_SPEC.md
docs/GOAL_ENGINE_V1_RATIFICATION_REPORT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Gate Checks

Confirm:

```text
Phase 44A is recorded with exact artifact-backed PASS evidence
Phase 44B uses implementation-contract scope
the protected active tuple is Phase44B / implementation-contract / INTERMEDIATE_PACKET
the PR does not modify docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
the packet changes only its eight authorized documentation files
Phase 44C remains blocked
Phase 44C is implementation-only and uses INTERMEDIATE_PACKET
the Codie V2 Constitution remains primary authority
Goal Engine v1.0 remains subordinate governance
the canonical Phase44-49 implementation program remains subordinate and sequential
the existing human-governed roadmap remains active
```

## Required Architecture Checks

Confirm the contract accurately records that:

```text
no codie.goal_engine package currently exists
no runtime execution Build Graph currently exists
codie.intelligence.evidence_graph is not the Goal Engine Build Graph
codie.validation is not the Independent Goal Validator
future Phase 44C uses a new isolated codie/goal_engine/foundation.py module
future Phase 44C is pure, local-only, in-memory, deterministic, and standard-library only
future Phase 44C does not modify existing production modules
future Phase 44C does not add schema, migrations, repositories, dependencies, workflows, or validators
```

## Required Foundation Checks

Confirm the contract defines:

```text
exact lifecycle vocabulary including HEALTHY_IDLE and WAITING_FOR_HUMAN
Level 0 reserved for constitutional hard constraints
CAP-0 through CAP-5 operational capability vocabulary
separate SIZE, RISK, and ROLLBACK values
NORMAL, READ_ONLY_SAFE_MODE, GOAL_ENGINE_DISABLED, and FULL_AUTOMATION_HALT
namespaced v1 schema/version conventions
positive immutable revisions
caller-provided IDs and timestamps
canonical deterministic serialization and semantic hashes
Goal evidence references without mutable or raw evidence content
all ratified minimum Goal Contract fields
distinct content-free Goal, Idea, and Finding identifiers
read-only historical Policy Registry records
authority and safe-mode vocabulary without authority or safety state
append-only paper-trail lineage
separation of human decisions from facts
explicit no-persistence boundaries
```

Confirm these invariants remain explicit:

```text
HEALTHY_IDLE and WAITING_FOR_HUMAN remain vocabulary only in Phase 44C
Goal, Idea, and Finding identifiers remain distinct and contain no record content
material Goal Contract revisions preserve history and invalidate stale approvals
unmodeled consequential situations do not invent authority
authority promotion, restoration, and downgrade behavior are not implemented
safe modes do not grant kill-switch control or runtime behavior
State Engine, health, ledger, impact, experiment, decision, corpus, and authority work remain deferred
same canonical input produces byte-stable serialization
```

## Required Evidence And Scope Checks

Confirm the contract preserves:

```text
hard evidence boundaries
facts separately from human decisions
history separately from current applicability
supporting evidence separately from contradictions
unknown separately from absent or false
confidence separately from authority
tests passing separately from outcome success
local-first behavior
zero-cost operation
privacy and secret rejection
supplemental-only Stream Deck support
Theory review gates
theory-skill review gates
Rules authority and Correction boundaries
Hareruya tournament-only provenance
provider write-back prohibition
no autonomous work selection
no runtime mutation
no Build Graph execution
no Stage 1 or higher authority
human merge and release authority
the canonical Phase44-49 implementation sequence remains in order
CCPM-inspired execution remains exclusively in Phase48
```

## Reject If The Packet Authorizes

```text
production implementation in Phase 44B
autonomous selection, ranking, activation, scheduling, or execution
goal, policy, authority, evidence, or safety-state mutation
database or filesystem persistence
schema, migration, repository, provider, network, model, CLI, UI, API, or service work
new dependencies or paid infrastructure
Stream Deck control or approval behavior
Theory promotion or review bypass
Rules mutation or Correction activation
Hareruya use outside tournament provenance
validator, workflow, constitution, or repair-controller changes
active-scope modification by the PR
authority promotion, kill-switch ownership, merge bypass, or release behavior
State Engine, health runtime, Idea/Finding ledger, impact engine, experiment engine,
read-only decision core, Goal Regression Corpus, Independent Goal Validator,
shadow mode, Stage 1 promotion, Stage 2 authority, or Stage 3 Build Graph work
CCPM-inspired execution outside Phase48
```

## Required Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

## Validation Tuple

```text
phase_id: Phase44B
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44C
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Final Gate

Phase 44C remains blocked until this exact Phase 44B SHA receives
artifact-backed `PASS` or `PASS WITH REVIEW NOTES` and Phase 44B is merged by
human authority.
