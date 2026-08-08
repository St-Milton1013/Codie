# Phase 44B Goal Engine Foundation Implementation Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase44B
phase_part: implementation-contract
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase44C
next_phase_part: implementation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 44B defines the exact future Phase 44C implementation boundary for the
first Goal Engine foundation package.

Future Phase 44C may add immutable, deterministic, local-only, in-memory
representations for Goal Engine vocabulary, Goal/Idea/Finding identifiers,
versioned Goal Contracts, policy records, authority vocabulary, safe-mode
vocabulary, and paper-trail lineage. It may add pure validation and canonical
serialization for those foundation records.

Phase 44B is documentation-only. It does not implement Goal Engine runtime
behavior, work selection, goal ranking, scheduling, orchestration, execution,
persistence, autonomous mutation, authority promotion, Build Graph submission,
provider access, model calls, UI, CLI, or network behavior.

## Governing Authority

Authority order is:

```text
1. docs/CODIE_V2_CONSTITUTION.md
2. docs/GOAL_ENGINE_V1_SPEC.md
3. docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
4. this Phase 44B implementation contract
5. later implementation reports and supporting documentation
```

This contract cannot weaken or reinterpret higher authority. A conflict fails
closed and returns to human review.

## Phase 44A Accepted Baseline

```text
Phase 44A pull request: 80
workflow run ID: 31241668025
validated SHA: 1c8ddc03c5d5c53dcb06298cfe6892f46594daae
merge commit: a9999a58bfc40696a94f8366f4686325004c3fcb
artifact: codie-pr-validation-1c8ddc03c5d5c53dcb06298cfe6892f46594daae
artifact ID: 9017218547
artifact digest: sha256:c79aa87d86692df1a9e7563d7403d391c31c6bc88c102f99f96db80eb01aecb5
validation scope: pr
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
severity totals: all zero
skipped validators: none
unresolved findings: none
errors: none
final governance verdict: PASS
```

Phase 44A ratified Goal Engine v1.0 as subordinate repository governance. It
did not grant runtime authority or change the human-governed roadmap takeover
rules.

## Existing Architecture Reconciliation

The repository currently has no `codie.goal_engine` package and no runtime
execution Build Graph. Existing `codie.intelligence.evidence_graph` code is an
evidence representation and must not be renamed, wrapped, or treated as the
Goal Engine Build Graph.

Existing `codie.validation` code governs repository validation and bounded
repair. It is not the future Independent Goal Validator. Phase 44C must not
import, call, alter, or claim authority over it.

The canonical implementation program places the execution Build Graph and all
CCPM-inspired dispatch work in Phase48. Phase 44C must not create an execution
graph, task dispatcher, worktree manager, or PR handoff surface.

Existing architecture commonly uses frozen dataclasses, explicit allowlists,
caller-supplied timestamps, deterministic tuple ordering, explicit validation,
and canonical `*_to_dict(...)` functions. Phase 44C should follow those local
conventions while remaining isolated from providers, repositories, database
schema, analytics, recommendations, simulator behavior, Jin, and presentation
surfaces.

## Future Phase 44C Files

Future Phase 44C may add only:

```text
codie/goal_engine/__init__.py
codie/goal_engine/foundation.py
tests/test_goal_engine_foundation.py
docs/PHASE44C_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_REPORT.md
```

No existing production module, database schema, migration, repository,
dependency declaration, workflow, validator, provider, CLI, UI, or active
validation-scope file may be changed in Phase 44C.

## Canonical Vocabulary

Phase 44C must encode the following vocabulary without aliases that blur
authority or lifecycle meaning.

Goal lifecycle states:

```text
ACTIVE
INVESTIGATING
WATCHING
HEALTHY_IDLE
WAITING_FOR_HUMAN
PAUSED_PREEMPTED
BLOCKED_PREREQUISITE
IMPLEMENTED_PENDING_OUTCOME
CLOSED_SUCCESS
CLOSED_LIMITATION
REVISE
REWIND
REINVESTIGATE
```

Problem classifications:

```text
TRANSIENT
RECURRING
STRUCTURAL
```

Operational capabilities:

```text
CAP-0 Observe
CAP-1 Investigate
CAP-2 Safe Experiment
CAP-3 Propose
CAP-4 Governed Modification
CAP-5 Release / Strategic Authority
```

The serialized capability identifiers are `CAP-0` through `CAP-5`. The term
`Level 0` remains reserved for constitutional hard constraints and must never
be used as an operational capability alias.

Size, risk, and rollback remain separate:

```text
SIZE: Tiny, Small, Medium, Large, Core
RISK: Low, Medium, High, Critical
ROLLBACK: Easy, Moderate, Hard, Not safely reversible
```

User-controlled safety modes:

```text
NORMAL
READ_ONLY_SAFE_MODE
GOAL_ENGINE_DISABLED
FULL_AUTOMATION_HALT
```

`HEALTHY_IDLE` remains a successful lifecycle value, but Phase 44C does not
implement decision logic, a queue, active-goal enforcement, or work selection.
Read-only decision use of `HEALTHY_IDLE` is reserved for Phase44T-U. Canonical
one-active-mutating-goal enforcement is reserved for Phase46A-C after explicit
Stage 1 promotion.

Idea states, idea relationships, conditional reactivation, immutable original
wording, recurrence, reconsideration triggers, and durable Idea/Finding/Goal
distinction are reserved for Phase44K-M. Phase 44C implements identifiers only.

## Schema And Version Conventions

Every serialized foundation record must include a non-empty `schema_version`
with an exact namespaced value reserved by Phase 44C. The initial values must
use the `codie.goal_engine.*.v1` namespace.

Required conventions:

```text
caller-provided stable IDs
positive integer revisions starting at 1
explicit superseded ID and revision references where applicable
caller-provided UTC timestamps with no implicit clock reads
frozen dataclasses and immutable tuples
explicit enum allowlists
unknown enum values rejected
duplicate IDs rejected
deterministic ordering by stable ID and revision
canonical UTF-8 JSON semantics
sorted object keys
compact separators for hashes
SHA-256 semantic hashes where identity or lineage hashes are required
no random IDs
no environment-derived values
no hidden defaults that grant authority
```

Material semantic changes require a new schema version. Material Goal Contract
changes require a new contract revision and cannot overwrite an existing
revision. Superseded records remain historical evidence.

## Future Foundation Models

Future Phase 44C may define the following immutable record families. Exact
Python names may vary only if the implementation report maps every renamed
surface back to this contract.

### Goal evidence reference

`GoalEvidenceReference` should contain only an opaque evidence reference and
its governance labels:

```text
evidence_ref_id
evidence_class
source_id
source_version
observed_at
historical_validity
current_applicability
review_state
privacy_class
conflict_ref_ids
schema_version
```

It must not contain raw provider payloads, private deck text, credentials,
model prompts, cookies, tokens, or mutable evidence content. Goal Engine code
cannot edit incoming evidence.

### Goal Contract

`GoalContract` must include:

```text
goal_contract_id
revision
schema_version
supersedes_revision
originating_idea_ids
originating_finding_ids
problem_classification
observed_problem
desired_outcome
why_it_matters
baseline
expected_result
acceptable_result
maximum_acceptable_regressions
root_cause_hypothesis
confidence
proposed_intervention
credible_alternatives
disconfirmation_criteria
expected_affected_systems
expected_unaffected_systems
dependency_ids
evidence_snapshot
privacy_implications
security_implications
zero_cost_validation
manual_burden
operational_burden
size
risk
rollback
rollback_plan
observation_window
if_we_do_nothing
if_we_do_this
historical_attempt_ids
approval_requirements
created_at
```

`evidence_snapshot` must be a deterministic tuple of immutable
`GoalEvidenceReference` values or an equivalent immutable wrapper. Confidence
is a bounded evidence assessment, not permission.

Phase 44C must not provide an in-place Goal Contract mutation API. A material
revision must identify the prior revision, preserve its semantic hash, and add
lineage that marks earlier approval or validator references stale. Runtime Goal
state and the `WAITING_FOR_HUMAN` transition are reserved for the State Engine
and later governed integration.

### Goal, Idea, and Finding identifiers

Phase 44C may define only stable identifier value objects for the three entity
kinds:

```text
GoalIdentifier
IdeaIdentifier
FindingIdentifier
```

Each identifier must contain an exact entity kind, a caller-supplied non-empty
local ID, and its schema version. Cross-kind equality must fail. Identifiers
must serialize deterministically and must not embed user wording, finding
content, evidence, state, priority, or authority.

Phase 44C must not implement Idea records, Finding records, ledger relations,
original wording, recurrence, reconsideration triggers, health-to-finding
conversion, or Idea/Finding/Goal promotion. Those belong to Phase44H-M.

### Policy registry

`GoalPolicyRecord` must include:

```text
policy_id
policy_version
schema_version
date
reason
rule
authority_ref_ids
affected_policy_ids
superseded_policy_ref
regression_case_ids
```

`GoalPolicyRegistry` may provide deterministic validation, lookup, and
serialization over caller-supplied immutable policy records. It must retain
superseded policies as historical evidence.

Phase 44C must not provide policy execution, self-amendment, policy inference,
automatic policy adoption, repository writes, or authority changes. An
unmodeled consequential situation must fail foundation validation without
inventing policy. Later governed state handling is responsible for
`WAITING_FOR_HUMAN`.

### Authority and safe-mode vocabulary

Phase 44C may expose exact validated value objects for `CAP-0` through `CAP-5`
and the four ratified safe-mode names. These objects are vocabulary only. They
must not contain effective authority, progressive stage, approval state,
resource state, incident state, write permissions, or restoration state.

Authority state and human-attention state belong to Phase44E-G. Phase 44C may
not promote or downgrade capability, approve a stage, create human approval,
bypass a merge gate, control a kill switch, restore authority, terminate
processes, revoke permissions, modify the network, or perform containment side
effects. `CAP-5` never transfers release, constitutional, Level 0, unrestricted
strategy, or human merge authority to Goal Engine code.

### Paper-trail lineage

`GoalLineageEvent` must be append-only and must preserve:

```text
event_id
schema_version
entity_kind
entity_id
entity_revision
event_kind
occurred_at
actor_kind
summary
evidence_ref_ids
human_decision_ref_ids
authority_ref_ids
prior_event_ids
prior_event_hashes
event_hash
```

Human decisions and factual evidence must remain separate fields. Human
decisions control execution but do not rewrite fact. Later contradictory
evidence must preserve the earlier decision and add a new lineage event.

Lineage should support, without automatically advancing, the sequence:

```text
IDEA
-> RESEARCH
-> FINDING
-> GOAL
-> EXPERIMENT
-> IMPLEMENTATION
-> OBSERVATION
-> OUTCOME
```

### Deferred runtime records

Phase 44C must not implement:

```text
State Engine snapshots or reconciliation; reserved for Phase44E-G
health models or health findings; reserved for Phase44H-J
Idea/Finding ledger records or relations; reserved for Phase44K-M
impact analysis; reserved for Phase44N-P
experiment machinery; reserved for Phase44Q-S
read-only decision logic; reserved for Phase44T-V
Goal Regression Corpus records or runner; reserved for Phase44W-Y
Independent Goal Validator; reserved for Phase45A-C
shadow-mode records or operation; reserved for Phase45D-G
one-active-mutating-goal enforcement; reserved for Phase46A-C
safe experiment authority; reserved for Phase47
Build Graph or CCPM-inspired execution; reserved for Phase48
```

## Allowed Pure Interfaces

Future Phase 44C may expose:

```text
GoalEngineFoundationError
immutable foundation record constructors
explicit validate_* functions
explicit *_to_dict functions
explicit *_from_dict functions with unknown-field rejection
canonical semantic-hash helpers
explicit identifier validation
explicit Goal Contract revision validation
explicit policy-registry history validation
explicit lineage-chain validation
```

These interfaces must be pure. They may validate caller-supplied data and
return immutable values. They may not inspect the repository, current branch,
system clock, process state, environment, filesystem, database, provider,
network, model, UI, CLI, Stream Deck, or hidden application state.

## Required Deterministic Invariants

Phase 44C tests must prove:

```text
Level 0 and CAP-* vocabulary remain separate
unknown lifecycle, capability, safety, size, risk, and rollback values fail
Goal, Idea, and Finding identifiers remain distinct
identifiers contain no content, state, priority, evidence, or authority
material Goal Contract revisions identify and preserve prior revision history
material revisions invalidate stale approvals and validator results
human decision references remain separate from evidence references
policy supersession preserves historical records
unmodeled consequential situations do not invent authority
authority and safe modes remain vocabulary only
authority promotion, restoration, and downgrade behavior are not implemented
kill-switch behavior is not implemented
lineage hashes are deterministic and prior history is preserved
same canonical input produces byte-stable dictionary serialization
secret, token, credential, cookie, session, prompt-log, and raw payload fields fail
```

## Hard Evidence Boundary

Goal Engine foundation records must preserve:

```text
facts separately from human decisions
historical validity separately from current applicability
supporting evidence separately from contradicting evidence
unknown separately from absent or false
unavailable separately from unsupported
confidence separately from authority
observed problems separately from possible future risks
tests passing separately from goal outcome success
```

Missing or conflicting evidence cannot be filled, reconciled, or promoted by
the foundation. The model must preserve gaps and contradictions visibly.

## Local-First, Privacy, Cost, And Dependency Boundary

Future Phase 44C must remain:

```text
local-only
in-memory
deterministic
zero-cost
standard-library only
caller-input only
free of filesystem and database writes
free of provider and network access
free of model calls
free of telemetry and analytics emission
```

No paid software, subscription, paid API, paid model, recurring monetary cost,
or new dependency is authorized.

Goal/Idea/Finding identifiers and local evidence references must not contain or
become export, sync, publication, provider, or model context. Phase 44C does
not store original idea wording and authorizes no writer.

## Theory, Rules, Corrections, And Hareruya Boundary

Theory references remain subject to established review gates. Unreviewed Theory
cannot become factual evidence, Goal Contract support, eligibility evidence,
authority, policy, or regression truth. Reviewed Theory remains attributed
context and cannot silently become measured evidence or rules authority.

Existing theory-skill review gates remain mandatory. Phase 44C cannot invoke,
promote, approve, replace, or bypass a theory-related skill or its human review
boundary.

Rules authority, legality, and correction state remain external inputs. Phase
44C cannot mutate Rules, activate Corrections, resolve correction conflicts, or
use Goal Engine state to override legal or evidence ceilings.

Hareruya remains tournament-only provenance. Hareruya references may identify
tournament observations, events, or deck instances. They cannot become Theory,
Rules, Corrections, curriculum authority, private user context, general factual
authority, policy, or a write target.

## Stream Deck Boundary

Stream Deck remains optional and supplemental-only. Phase 44C may not add a
Stream Deck adapter, event handler, command, confirmation path, approval path,
or mutation surface.

Any later display of Goal Engine status through Stream Deck must be read-only
and separately contracted. It cannot grant consent, select evidence, change
authority, control safety restoration, mutate a goal, retry work, override
privacy, bypass validation, or replace a primary interface.

## Build Graph And Existing Roadmap Boundary

Phase 44C does not implement a Build Graph. It may define opaque lineage and
dependency references only. It cannot submit, schedule, execute, repair, merge,
release, or close work.

The existing human-governed roadmap remains active. Goal Engine does not become
the canonical work-order manager until it completes shadow-mode requirements,
passes independent validation, and receives explicit human Stage 1 promotion.

The existing PR-only workflow, validation gates, maximum repair-attempt rules,
human merge authority, and release authority remain unchanged.

The canonical build sequence in
`docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md` remains in order:

```text
Phase44B-C-D: Foundation contract, implementation, checkpoint
Phase44E-G: State Engine
Phase44H-J: separate subsystem health
Phase44K-M: Findings + Idea Ledger runtime
Phase44N-P: Change / Impact Engine
Phase44Q-S: experiment machinery without experiment authority
Phase44T-V: read-only decision core
Phase44W-Y: Goal Regression Corpus
Phase44Z: pre-authority freeze
Phase45: Independent Goal Validator and Stage 0 Shadow Mode
Phase46: conditional Stage 1 work-order authority and calibration
Phase47: conditional Stage 2 safe experiment authority
Phase48: conditional Stage 3 Build Graph and CCPM-inspired execution
Phase49: mature governance without additional authority
Stage 4: not on the active roadmap
```

Phase 44C supplies only deterministic foundation representations. It does not
authorize or implement any later phase.

## Phase 44C Forbidden Work

Future Phase 44C must not add or modify:

```text
autonomous work selection
goal ranking or priority calculation
goal activation
scheduler, queue, worker, agent, or orchestrator
Build Graph execution or submission
runtime mutation
State Engine or project-state reconciliation
health models, health findings, or a global health score
Idea records, Finding records, ledger relations, or original idea wording
impact analysis
experiment machinery or experiment authority
read-only decision logic or Goal Candidate generation
Goal Regression Corpus records or execution
Independent Goal Validator or shadow-mode records
one-active-mutating-goal runtime enforcement
filesystem or database persistence
schema or migration
repository methods
provider or raw source access
network or egress behavior
LLM or model calls
CLI, UI, API, route, or background service
Stream Deck integration
Jin behavior
Theory ingestion, promotion, or skill review bypass
Rules mutation
Correction activation
Hareruya scope expansion
analytics or recommendation behavior
simulator behavior
presentation or export behavior
dependency or packaging changes
validator, repair controller, workflow, or constitution changes
active validation-scope edits
authority promotion or restoration
kill-switch ownership
human approval or merge bypass
release behavior
full Goal Regression Corpus execution
shadow mode
Stage 1 or higher authority
```

## Authorized Phase 44B Files

This contract packet may change only:

```text
docs/PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE44B_GOAL_ENGINE_FOUNDATION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/GOAL_ENGINE_IMPLEMENTATION_PROGRAM_V1.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Active Scope Handling

The protected active scope is established separately on `main` as:

```text
Phase44B / implementation-contract / INTERMEDIATE_PACKET
```

This PR must not modify `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`.

## Required Phase 44B Validation

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
focused changed-file and forbidden-boundary scans
```

## Gate

Phase 44C remains blocked until Phase 44B receives exact-SHA artifact-backed
`PASS` or `PASS WITH REVIEW NOTES` and is merged through human authority.
Phase 44D and every later implementation-program packet remain blocked behind
their sequential contract, implementation, checkpoint, evidence, and human
authority gates.
