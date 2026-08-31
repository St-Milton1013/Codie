# Codie Goal Engine Implementation Program v1

## Canonical Build Sequence

Status: implementation roadmap

Authority: subordinate to `docs/CODIE_V2_CONSTITUTION.md` and the ratified
`docs/GOAL_ENGINE_V1_SPEC.md`

Current execution boundary: Phase44E State Engine contract, Phase44F State
Engine implementation, and the Phase44G State Engine checkpoint / freeze are
accepted. Phase50A was accepted through merged PR #87 and Phase50B through
merged PR #88. Phase50C is accepted through merged PR #89, completing the
temporary human-priority interposition. Phase44H is accepted through merged PR
#90. Phase44I is accepted through exact-SHA artifact validation and merged PR
#91. Phase44J is accepted through exact-SHA artifact validation and merged PR
#92. Phase44K is accepted through exact-SHA artifact validation and merged PR
#93. Phase44L is accepted through exact-SHA artifact validation and merged PR
#94. Phase44M is accepted through exact-SHA artifact validation and merged PR
#95. Phase44N is accepted through exact-SHA artifact validation and merged PR
#96. Phase44O is accepted through exact-SHA artifact validation and merged PR
#97. Phase44P is accepted through merged PR #98. Phase44Q is accepted through
merged PR #99 and Phase44R through merged PR #100. Phase51A and Phase51B are
accepted validator-context infrastructure interpositions through PRs #101 and
#102. Phase44S and Phase44T are accepted through merged PRs #103 and #104.
Phase44U awaits validation. Phase51C through Phase51H are accepted
validator-gate corrections through PRs #106, #107, #109, #110, and #111.
Phase51I is accepted through merged PR #112. Phase51K is a separate structured-
disposition design contract in open PR #113. Its automatic validation is
blocked by one independently disproved architecture-model claim that a named
Phase51I record is absent from the active roadmap. Phase51L is the deliberate
documentation-record-evidence contract interposition: it does not change
Phase51K's meaning, Phase51J, or Phase44U. Phase51M is held for a two-lane
implementation-safety amendment: it replaces only Phase51L's unsafe
per-finding record-assertion attachment with a separate record-only assertion
lane, leaving all ordinary findings blocking. After that amendment is
independently validated and human-accepted, Phase51M may implement the bounded
correction and specified Phase51K-to-Phase51N handoff before PR #113 is
revalidated. Phase51N is then the structured-disposition implementation
formerly projected as Phase51L.

On 2026-08-25 the project owner approved a narrow Phase50B usability amendment
for explicit user-initiated official card-data preparation and public Moxfield
deck import. The amendment does not change the Phase44-49 sequence, evidence
authority, or human validation and merge gates.

## Completed Phase50 delivery-priority interposition

Phase44G later received artifact-backed acceptance through merged PR #86. On
2026-08-14 the human project owner approved Codie Local Working Iteration v0.1
as the next implementation packet ahead of further Goal Engine work.

The temporary sequence is:

```text
Phase50A - Local Working Iteration v0.1 contract
Phase50B - Local Working Iteration v0.1 implementation
Phase50C - Local Working Iteration v0.1 checkpoint / freeze
resume this program at Phase44H
```

Phase50A-C are accepted through merged PRs #87-#89. The original program has
resumed at Phase44H without changing the sequence or any authority gate.

This interposition changes delivery priority only. It does not renumber,
implement, validate, satisfy, promote, or weaken any Phase44-49 Goal Engine
gate. Build Graph and CCPM-inspired execution remain conditional Phase48 work.

## Operating Rule

Every implementation packet continues using Codie's existing workflow:

```text
accepted contract
-> implementation PR
-> focused tests
-> full Codie regression
-> deterministic validator
-> architecture validator
-> adversarial validator
-> aggregate result
-> repair if eligible, maximum 2 attempts
-> human merge
-> checkpoint / next packet
```

Later authority stages cannot be built early merely because their architecture
is already designed.

## Phase 44 - Goal Engine Runtime Foundation

Authority gained: none.

Phase 44 builds decision machinery required before Goal Engine may influence
actual work.

### Phase44A - Goal Engine v1 Ratification

Governance only. Accepted through PR #80.

### Phase44B - Goal Engine Foundation Implementation Contract

Defines:

```text
canonical vocabulary
Goal/Idea/Finding identifiers
authority vocabulary
policy records
Goal Contract models
lineage
safe modes
deterministic serialization
persistence boundaries
```

### Phase44C - Goal Engine Foundation Implementation

Implement `codie/goal_engine/` foundation. No decision-making yet.

### Phase44D - Foundation Checkpoint

Freeze and validate Foundation v1.

### Phase44E - State Engine Contract

Define project/state reconciliation, freshness, provenance, conflicts,
authority state, Goal state, Build state, resources, incidents, and
human-attention state.

### Phase44F - State Engine Implementation

### Phase44G - State Engine Checkpoint

### Phase44H - Subsystem Health Foundation Contract

Keep separate:

```text
CODIE
JIN
THEORY_CORPUS
```

No universal health score. Health may produce evidence-backed signals or
findings but never Goals directly.

### Phase44I - Health Foundation Implementation

### Phase44J - Health Foundation Checkpoint

### Phase44K - Findings + Idea Ledger Runtime Contract

Implement the durable distinction:

```text
Idea != Finding != Goal
```

Include conditional ideas, recurrence, relations, immutable original wording,
reconsideration triggers, and history.

### Phase44L - Findings + Idea Ledger Implementation

### Phase44M - Ledger Checkpoint

### Phase44N - Change / Impact Engine Contract

Define:

```text
direct, indirect, and possible impact
expected untouched systems
blast radius
dependency effects
privacy, security, and cost effects
rollback analysis
required validation
historical-attempt comparison
```

### Phase44O - Change / Impact Engine Implementation

### Phase44P - Impact Engine Checkpoint

### Phase44Q - Goal Experiment Engine Contract

This defines experiment machinery only. It grants no autonomous experiment
authority.

### Phase44R - Experiment Engine Implementation

Accepted through merged PR #100 after the branch incorporated the accepted
validator-context interposition without changing the three-file Phase44R
surface. Earlier failed artifacts remain historical evidence only.

### Phase44S - Experiment Engine Checkpoint

### Phase44T - Goal Engine Read-Only Decision Core Contract

Define the first Goal Engine reasoning surface:

```text
Necessity
Evidence
Root Cause
History
Actionability
Experiment Need
Intervention
Impact
Priority
HEALTHY_IDLE
```

It may produce advisory Goal Candidates and draft Goal Contracts only.

### Phase44U - Read-Only Decision Core Implementation

### Phase44V - Read-Only Decision Core Checkpoint

### Phase44W - Goal Regression Corpus Contract

Define a fixed initial corpus of approximately 50 reviewed scenarios with
strong coverage of both `ACT` and `DO NOT ACT`.

### Phase44X - Goal Regression Corpus Implementation

### Phase44Y - Regression Corpus Checkpoint

All blocking governance scenarios must pass.

### Phase44Z - Goal Engine Pre-Authority Foundation Freeze

Required clean state:

```text
Foundation
State
Health
Ledger
Impact
Experiment Engine
Read-Only Goal Engine
Regression Corpus
```

No work-order authority exists yet.

## Phase 45 - Independent Validation + Shadow Mode

Authority gained: still none.

### Phase45A - Independent Goal Validator Contract

Blind-first reconstruction and validation.

### Phase45B - Independent Goal Validator Implementation

### Phase45C - Independent Validator Checkpoint

### Phase45D - Shadow Mode Contract

### Phase45E - Shadow Mode Implementation

Implement:

```text
frozen decision evidence
engine decision capture
independent validation
human decision capture
outcome linkage
disagreement classification
coverage tracking
```

### Phase45F - Shadow Launch Checkpoint

Human authority explicitly begins formal Stage 0 Shadow Mode.

### Operational Period

This is not another coding phase. Required minimum:

```text
30 clean calendar days
AND 25 meaningful prospective decisions
AND representative coverage
AND 0 serious Level 0 violations
```

Synthetic cases do not count. Goal Engine remains advisory only.

### Phase45G - Shadow Evaluation + Human Promotion Packet

Possible outcomes:

```text
PROMOTE_TO_STAGE_1
EXTEND_SHADOW
REVISE_AND_REPEAT
KEEP_STAGE_0
DISABLE_GOAL_ENGINE
```

Promotion is never automatic.

## Phase 46 - Stage 1 Work-Order Authority + Calibration Foundation

Phase 46 begins only after explicit human Stage 1 promotion.

### Phase46A - Stage 1 Work-Order Integration Contract

### Phase46B - Stage 1 Work-Order Implementation

Adds canonical:

```text
one active mutating Goal
READY queue
investigation queue
WAITING_FOR_HUMAN
prerequisite handling
safe preemption
observation interference
human reprioritization
HEALTHY_IDLE
roadmap migration and fallback
```

### Phase46C - Stage 1 Activation Checkpoint

This is Takeover A. From this point Goal Engine becomes the canonical system for
determining what Codie should work on next. The existing human roadmap remains
preserved as history and fallback. Implementation still uses the existing PR
workflow.

### Phase46D - Long-Term Calibration Foundation Contract

Implement common calibration records needed from Stage 1 forward:

```text
Goal selection
priority
confidence
human gates
false Goals
missed Goals
outcomes
validator disagreement
human overrides
```

### Phase46E - Calibration Foundation Implementation

### Phase46F - Calibration Foundation Checkpoint

### Phase46G - Stage 1 Operational Review

Do not automatically proceed. Apply the Stage 2 Necessity Test:

> What meaningful recurring problem exists because Codie cannot initiate safe
> experiments itself?

`KEEP_STAGE_1` is a valid indefinite result.

## Phase 47 - Stage 2 Safe Experiment Authority

Phase 47 is conditional on Stage 2 readiness evidence and explicit human
promotion.

### Phase47A - Stage 2 Readiness Assessment

### Phase47B - Safe Autonomous Experiment Authority Contract

Initial autonomous profile:

```text
Low risk only
Tiny or Small experimental scope
local
zero-cost
no canonical writes
no production writes
no provider writes
network denied by default
secrets denied by default
bounded resources
mandatory cleanup
```

### Phase47C - Stage 2 Authority Implementation

### Phase47D - Stage 2 Activation Checkpoint

This grants only explicitly allowlisted experiment profiles.

### Phase47E - Stage 2 Operational Observation + Calibration

Measure information gain, useful and unnecessary experiments, cleanup,
resource prediction, scope drift, and human intervention.

### Phase47F - Stage 2 Review

Possible outcomes:

```text
KEEP_STAGE_2
TIGHTEN_STAGE_2
REVISE_STAGE_2
DOWNGRADE
CONSIDER_STAGE_3
```

Stage 3 requires its own Necessity Test.

## Phase 48 - Stage 3 Governed Implementation / Build Graph

Phase 48 is conditional on evidence and explicit human promotion. CCPM-inspired
execution belongs here.

### Phase48A - Stage 3 Readiness Assessment

Ask:

> What meaningful recurring problem remains because humans must initiate
> approved implementation work manually?

### Phase48B - Build Graph Core Contract

Define:

```text
ImplementationAdmissionPacket
ImplementationGraph
ImplementationTask
exact Goal/spec lineage
task dependencies
conflicts
write scopes
acceptance criteria
execution state
BuildRun state
```

### Phase48C - Build Graph Core Implementation

No agent dispatch yet.

### Phase48D - Isolated Task Execution Contract

Implement the smallest useful CCPM-inspired subset:

```text
approved Codie specification
-> bounded task decomposition
-> dependencies and conflicts
-> task-level worktree
-> machine-enforced write scope
-> coding agent
-> task validation
-> persistent execution receipt
```

Initial dispatch favors serial correctness over maximum parallelism.

### Phase48E - Isolated Task Execution Implementation

No GitHub Issue mirror is required. No shared mutable worktree is allowed.

### Phase48F - Integration + Draft PR Handoff Contract

Define integration order, conflict handling, execution-drift checks,
integration branch, draft PR construction, Goal/spec/task provenance, and
existing validator handoff.

### Phase48G - Integration + Draft PR Implementation

Absolute boundary:

```text
Build Graph may create a draft PR
Build Graph may not merge a PR
```

### Phase48H - Stage 3 Core Checkpoint + Activation

This is Takeover B. Codie may turn an approved Goal into implementation work.
Human merge remains mandatory.

## Phase 48 Optional Enhancements

These are not prerequisites for Stage 3 MVP.

### Phase48I - Bounded Parallel Dispatch Contract

Only if serial task-isolated execution proves stable and parallel work has
meaningful expected value.

### Phase48J - Bounded Parallel Dispatch Implementation / Checkpoint

Tasks may parallelize only with proven absence of dependency, write, and
mutable-resource conflicts.

### Phase48K - Optional GitHub Issue Mirror Contract

Only if workflow evidence shows Issues improve visibility or coordination.
GitHub Issues are mirrors, not authority or canonical state.

### Phase48L - Optional Issue Mirror Implementation

If Issue mirroring shows no real value, do not build it.

### Phase48M - Stage 3 Operational Observation Implementation

Measure decomposition quality, dependency accuracy, hidden dependencies, scope
expansion, agent performance, worktree isolation, parallelism return, integration
conflicts, first-pass validation, repair frequency, human burden, and Goal
outcomes.

### Phase48N - Stage 3 Operational Review

Possible outcomes:

```text
KEEP_STAGE_3
EXTEND_OBSERVATION
REVISE_STAGE_3
SIMPLIFY_STAGE_3
DOWNGRADE
CONSIDER_STAGE_4
```

## Phase 49 - Mature Steady-State Governance

This phase does not increase authority.

### Phase49A - Steady-State Governance Expansion Contract

Extend calibration across Goal selection, priority, confidence, validator,
experiments, Build Graph, decomposition, agents, human burden, outcomes, and
authority.

### Phase49B - Steady-State Governance Implementation

Add governance reviews, failure-history reports, authority map,
dependency/source drift monitoring, metric governance, permission-creep review,
data-retention review, and systemic-pattern detection.

### Phase49C - Mature Operating Model Checkpoint

Default mature architecture:

```text
Goal Engine controls justified attention
+ Stage 2 may run safe experiments
+ Stage 3 may dispatch approved implementation
+ Codie validators control acceptance gates
+ human controls merge
+ human controls release
+ human controls strategic and constitutional authority
```

## Stage 4

Stage 4 is not on the active roadmap. It enters investigation only if long-term
evidence demonstrates a concrete remaining problem that cannot reasonably be
solved inside Stage 3.

Default assumption:

```text
Stage 3 + human merge
is Codie's mature authority ceiling
```

## CCPM Placement

CCPM-inspired concepts are placed only at:

```text
Phase48D-E: task decomposition, dependencies, task state, worktree isolation,
agent dispatch

Phase48I-J: optional bounded parallelism

Phase48K-L: optional GitHub Issue mirroring
```

Excluded unless separately governed:

```text
CCPM as specification authority
CCPM as Goal authority
CCPM as priority authority
GitHub Issues as canonical project state
direct merge to main
issue closure as acceptance
unrestricted shared-worktree agents
mandatory Bash infrastructure
```

## Current Action

The active implementation sequence is:

```text
Phase44A ratification: accepted
-> Phase44B Foundation contract: accepted
-> Phase44C Foundation implementation: accepted
-> Phase44D Foundation checkpoint: accepted
-> Phase44E State Engine contract: accepted
-> Phase44F State Engine implementation: accepted
-> Phase44G State Engine checkpoint: accepted
-> Phase50A Local Working Iteration contract: accepted through PR #87
-> Phase50B Local Working Iteration implementation: accepted through PR #88
-> Phase50C Local Working Iteration checkpoint: accepted through PR #89
-> Phase44H Subsystem Health Foundation contract: accepted through PR #90
-> Phase44I Health Foundation implementation: accepted through PR #91
-> Phase44J Health Foundation checkpoint: accepted through PR #92
-> Phase44K Findings + Idea Ledger Runtime Contract: accepted through PR #93
-> Phase44L Findings + Idea Ledger implementation: accepted through PR #94
-> Phase44M Findings + Idea Ledger checkpoint / freeze: accepted through PR #95
-> Phase44N Change / Impact Engine contract: accepted through PR #96
-> Phase44O Change / Impact Engine implementation: accepted through PR #97
-> Phase44P Change / Impact Engine checkpoint / freeze: accepted through PR #98
-> Phase44Q Goal Experiment Engine contract: accepted through PR #99
-> Phase44R Goal Experiment Engine implementation: accepted through PR #100
-> Phase51A/Phase51B validator-context interposition: accepted through PRs #101/#102
-> Phase44S Goal Experiment Engine checkpoint / freeze: local checkpoint packet
```

Normal Codie development remains human-directed until Stage 1 earns and
receives explicit authority.

## Architecture Status

```text
Goal Engine governance architecture: DESIGN COMPLETE
Goal Engine implementation roadmap: DEFINED
CCPM-inspired execution placement: DEFINED
Stage 4: NOT PLANNED / EVIDENCE-GATED
Current runtime authority: UNCHANGED
```
