# Phase 31J - SIM-R State Transition Implementation Contract

Status: implementation contract only

## Purpose

Phase 31J defines the allowed implementation shape for the future SIM-R state
transition model layer.

The accepted SIM-R state and resource ledger models are pure value objects. The
accepted Phase 31I contract defines the transition boundary. Phase 31J narrows
the next implementation packet so it can add transition result models and
validators without adding executable simulator behavior.

This phase does not implement state transitions.

## Authorized Future Implementation Scope

A later accepted implementation packet may add:

```text
codie/probability_engine/sim_r_transition.py
tests/test_probability_engine_sim_r_transition.py
```

The future implementation may define pure data models and validators for:

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

## Phase 31J Scope

This Phase 31J packet may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Not Authorized In Phase 31J

```text
production transition implementation
state mutation logic
action execution
behavior module execution
search implementation
state hashing implementation
trace v2 runtime implementation
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

## Required Future Transition Model Rules

The future implementation must:

```text
use immutable dataclasses or equivalent immutable value objects
avoid in-place mutation
serialize deterministically
round-trip through JSON-compatible dictionaries
require transition_id
require transition_version
require simulation_id
require pre_state_id
require post_state_id
require action_id
require action_type
require behavior_key
require transition_status
preserve resource ledger IDs
preserve trace event IDs
preserve unsupported behavior records
preserve failed transition reasons
preserve no_op status explicitly
preserve deterministic trace event ordering
reject pre_state_id equal to post_state_id unless transition_status is no_op
reject resource-consuming successful transitions without resource ledger IDs
reject negative turn metadata
reject negative priority sequence metadata
remain evidence-only
```

## Required Future Tests

The later implementation packet must add tests proving:

```text
transition result serializes deterministically
transition result round-trips through dictionary form
transition models are immutable
input structures are not mutated by builders
transition_id remains visible
transition_version remains visible
simulation_id remains visible
pre_state_id remains visible
post_state_id remains visible
action_id remains visible
action_type remains visible
behavior_key remains visible
transition_status remains visible
resource ledger IDs remain visible
trace event IDs remain visible
unsupported behavior remains visible
failed transition reason remains visible
no_op transitions are explicit
resource-consuming successful transitions require ledger IDs
negative turn metadata fails validation
negative priority sequence metadata fails validation
no state mutation helper is added
no action execution helper is added
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
It must remain additive and isolated until a later SIM-R behavior-module or
search contract explicitly wires transition packets into a runnable engine.

## Evidence Boundary

SIM-R transition packets are simulator evidence only.

They must never become tournament evidence and must never directly generate
recommendations.

## Gate

Phase 31K is blocked until Phase 31J outside validation returns PASS or PASS
WITH REVIEW NOTES.

