# Outside Validation Prompt - Phase 44E Goal Engine State Engine Implementation Contract

Validate Phase44E as an implementation-contract-only packet from the exact PR
head in a clean checkout.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only `PASS` or `PASS WITH REVIEW NOTES` may unblock Phase44F.

## Required Review Files

```text
docs/PHASE44E_GOAL_ENGINE_STATE_ENGINE_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE44E_GOAL_ENGINE_STATE_ENGINE_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44E_GOAL_ENGINE_STATE_ENGINE_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/PHASE44D_GOAL_ENGINE_FOUNDATION_CHECKPOINT_FREEZE_CONTRACT.md
docs/PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/GOAL_ENGINE_V1_SPEC.md
docs/CODIE_V2_CONSTITUTION.md
codie/goal_engine/foundation.py
codie/goal_engine/__init__.py
tests/test_goal_engine_foundation.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Gate Checks

Confirm:

```text
Phase44D has exact artifact-backed PASS evidence
the protected tuple is Phase44E / implementation-contract / INTERMEDIATE_PACKET
the PR does not modify docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
the packet changes only its eight authorized documentation files
the implementation-program edit is status-only
the accepted Phase44-49 sequence and capability roadmap are unchanged
Phase44F remains implementation-only and blocked
Phase44F uses INTERMEDIATE_PACKET
Codie V2 remains primary authority
Goal Engine v1 remains subordinate
Foundation v1 remains frozen
the human-governed roadmap remains active
```

## Required Architecture Checks

Confirm the contract accurately records:

```text
codie/goal_engine/foundation.py is the accepted Foundation v1 surface
no codie/goal_engine/state_engine.py currently exists
SIM-R state is separate and must not be reused as project state
the evidence graph is not a Build Graph
codie.validation is not the Independent Goal Validator
future Phase44F is isolated to one module, exports, focused tests, and report
future Phase44F adds no persistence, provider, service, queue, worker, or scheduler
```

## Required State-Model Checks

Confirm the contract defines exact immutable records for:

```text
StateProvenance
ProjectState
AuthorityState
GoalState
BuildState
ResourceState
IncidentState
HumanAttentionState
StateSnapshotReference
ProjectStateSnapshot
StateConflict
StateConflictResolution
StateReconciliationEntry
StateReconciliationResult
```

Confirm exact vocabulary distinguishes:

```text
PROJECT, AUTHORITY, GOAL, BUILD, RESOURCE, INCIDENT, HUMAN_ATTENTION
CURRENT, STALE, UNKNOWN
AVAILABLE, UNAVAILABLE, UNKNOWN
CONSISTENT, CONFLICTED, RESOLVED_CONFLICT, INCOMPLETE, UNAVAILABLE
project, Build, resource, incident, and human-attention states
DOCUMENTATION_ONLY and Stage 0 through Stage 3 authority representation
human-decision resolution from accepted-policy resolution
```

## Required Freshness And Provenance Checks

Confirm:

```text
freshness uses only caller-supplied UTC timestamps and caller-supplied as_of
the wall clock is never read
stale is distinct from unavailable
unknown is distinct from unavailable, absent, and false
facts, human decisions, and authority references remain disjoint
every evidence reference resolves to the immutable snapshot registry
raw evidence, secrets, provider payloads, prompts, and private deck text are absent
snapshot revisions preserve the immediately prior semantic hash
duplicate IDs and dangling references fail closed
```

## Required Authority Checks

Confirm:

```text
authority state is representation only and grants no permission
DOCUMENTATION_ONLY carries no capability
Stage 0 is capped at CAP-0
Stage 1 is capped at CAP-1
Stage 2 is capped at CAP-2
Stage 3 is capped at CAP-3
Stage 1 through Stage 3 require promotion references
Level 0 is never an operational capability
CAP-4, CAP-5, and Stage 4 cannot be represented as current State Engine v1 authority
safe mode cannot increase authority
conflicted, missing, stale, or unavailable authority grants no permission
promotion, restoration, downgrade execution, and kill-switch behavior are absent
```

## Required Reconciliation Checks

Confirm future Phase44F is limited to a pure function that:

```text
validates caller-supplied snapshots
groups exact domain and subject identities
classifies freshness without external reads
retains current, stale, unknown, and unavailable candidates as separate dimensions
compares canonical state semantics independently of provenance
uses only each hash-linked snapshot lineage tip as that source's current view
does not give timestamp precedence to independent snapshot IDs
compares only AVAILABLE + CURRENT candidates for current agreement
does not promote stale historical differences into current conflicts
collapses only byte-identical current state agreement
emits visible conflicts for distinct current semantic states
accepts only caller-supplied human or accepted-policy resolutions
requires accepted-policy resolutions to resolve exact version/hash references
against a caller-supplied immutable GoalPolicyRegistry
retains all conflict candidates and history after resolution
sorts deterministically
derives conflict IDs from canonical current conflict semantics without randomness
produces byte-stable serialization and hashes
```

Reject newest-wins, source-priority, provider-priority, confidence-priority,
automatic refresh, automatic conflict resolution, inferred consent, inferred
authority, repository inspection, or runtime mutation.

## Required Evidence And Scope Checks

Confirm the contract preserves:

```text
hard evidence boundaries
passing validation separately from Build acceptance and Goal success
incident containment separately from resolution
human response separately from approval and authority
local-first, private, zero-cost, standard-library-only behavior
Theory and theory-skill human review gates
external Rules and Corrections authority
Hareruya tournament-only provenance
supplemental-only Stream Deck scope with no Phase44F integration
human roadmap, merge, release, and promotion authority
health, ledger, impact, experiment, decision, corpus, validator, and shadow deferrals
Build Graph and CCPM-inspired execution only in conditional Phase48
no Stage 1 or higher authority
```

## Reject If The Packet Authorizes

```text
production implementation in Phase44E
runtime mutation or lifecycle transitions
work selection, ranking, activation, scheduling, execution, or reprioritization
automatic conflict resolution or source precedence
authority calculation, promotion, restoration, downgrade execution, or permission checks
kill-switch or safe-mode transitions
health scores, findings, ledger, impact, experiments, decisions, corpus, or shadow mode
Build Graph, task graph, GitHub Issue state, worktree dispatch, agents, or CCPM
persistence, schema, migration, repository, provider, network, model, CLI, UI, API, or service work
new dependencies or paid infrastructure
Stream Deck control, approval, notification, or mutation
Theory promotion or review bypass
Rules mutation or Correction activation
Hareruya use outside tournament provenance
validator, workflow, repair-controller, constitution, or active-scope changes
human merge, release, roadmap, or promotion bypass
```

## Required Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

## Validation Tuple

```text
phase_id: Phase44E
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44F
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Final Gate

Phase44F remains blocked until this exact Phase44E SHA receives artifact-backed
`PASS` or `PASS WITH REVIEW NOTES` and Phase44E is merged by human authority.
