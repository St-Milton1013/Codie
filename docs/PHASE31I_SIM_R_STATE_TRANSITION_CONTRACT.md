# Phase 31I - SIM-R State Transition Contract

Status: contract only

## Purpose

Phase 31I defines the future boundary for SIM-R state transitions.

The accepted SIM-R state model and resource ledger now exist as isolated value
objects. The next SIM-R layer must define how a future action may transform one
immutable state into another while preserving resource accounting and trace
evidence.

This phase does not implement state transitions.

## Transition Principle

Every future SIM-R transition must follow:

```text
input state + action intent + behavior result
= output state + resource ledger + transition trace event
```

The input state must never be mutated in place.

## Authorized Future Implementation Scope

A later accepted implementation packet may add pure in-memory transition models
and validators such as:

```text
codie/probability_engine/sim_r_transition.py
tests/test_probability_engine_sim_r_transition.py
```

The future implementation may define:

```text
SIM_R_TRANSITION_VERSION
SimulationTransitionBuildError
SimulationActionIntent
SimulationBehaviorResult
SimulationTransitionTraceEvent
SimulationTransitionResult
build_transition_result(...)
transition_result_to_dict(...)
validate_transition_result(...)
```

## Phase 31I Scope

This Phase 31I packet may create only:

```text
transition contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Not Authorized In Phase 31I

```text
production transition implementation
action implementation
behavior module implementation
search implementation
state hashing implementation
trace v2 implementation
paired simulation implementation
schema changes
repository changes
database reads or writes
Forge integration
LLM behavior generation
recommendation generation
UI work
live network calls
```

## Required Future Transition Rules

The future transition implementation must:

```text
use immutable dataclasses or equivalent immutable value objects
avoid in-place mutation
require pre_state_id
require post_state_id
require action_id
require action_type
require behavior_key
require transition_status
preserve resource ledger references
preserve unsupported behavior records
preserve failed transition reasons
preserve deterministic trace event ordering
reject transitions where pre_state_id equals post_state_id unless explicitly marked no_op
reject missing resource ledger references for resource-consuming actions
reject negative turn or priority metadata
remain evidence-only
```

## Required Future Tests

The later implementation packet must add tests proving:

```text
transition result serializes deterministically
transition result round-trips through dictionary form
transition models are immutable
input structures are not mutated by builders
pre_state_id remains visible
post_state_id remains visible
action_id remains visible
action_type remains visible
behavior_key remains visible
transition_status remains visible
resource ledger references remain visible
unsupported behavior remains visible
failed transition reason remains visible
no_op transitions are explicit
resource-consuming transitions require ledger references
no search implementation is added
no behavior module execution is added
no recommendation language appears
```

## Dependency Rules

Allowed future dependencies:

```text
standard library
codie.probability_engine.sim_r_state
codie.probability_engine.sim_r_ledger
```

Forbidden dependencies:

```text
codie.db
repositories
providers
ingestion
cards lookup
analytics
recommendations
decision intelligence
evidence fusion
sqlite3
requests
httpx
Forge runtime
LLM SDKs
UI frameworks
```

## Compatibility Boundary

The future implementation must not change existing Phase 13/14 simulator
behavior, Phase 31E SIM-R state behavior, or Phase 31H resource ledger behavior.
It must remain additive and isolated until a later SIM-R search or behavior
module contract explicitly wires transitions into a runnable engine.

## Evidence Boundary

SIM-R transition output is simulator evidence only.

It must never become tournament evidence and must never directly generate
recommendations.

## Gate

Phase 31J is blocked until Phase 31I outside validation returns PASS or PASS
WITH REVIEW NOTES.

