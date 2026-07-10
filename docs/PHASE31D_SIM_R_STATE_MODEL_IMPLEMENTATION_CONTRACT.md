# Phase 31D - SIM-R State Model Implementation Contract

Status: implementation contract only

## Purpose

Phase 31D defines the allowed implementation shape for the future SIM-R state
model.

This phase does not implement the state model. It authorizes a later
implementation packet to add pure, in-memory Python state models that satisfy
the Phase 31C immutable state contract.

## Authorized Future Implementation Scope

A later accepted implementation packet may add:

```text
codie/probability_engine/sim_r_state.py
tests/test_probability_engine_sim_r_state.py
```

The future implementation may define pure data models and validators for:

```text
SimulationState
SimulationZone
SimulationCardInstance
SimulationManaPool
SimulationCommanderState
SimulationTargetProgress
SimulationUnsupportedBehavior
SimulationStateBuildError
build_simulation_state(...)
simulation_state_to_dict(...)
validate_simulation_state(...)
```

## Phase 31D Scope

This Phase 31D packet may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Not Authorized In Phase 31D

```text
production simulator code
state model implementation
state transition implementation
action implementation
behavior module implementation
search implementation
state hashing implementation
resource ledger implementation
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

## Required Future Model Rules

The future implementation must:

```text
use immutable dataclasses or equivalent immutable value objects
avoid in-place mutation
serialize deterministically
round-trip through JSON-compatible dictionaries
preserve explicit zone ordering when ordering matters
prevent duplicate card_instance_id across zones
prevent negative mana
preserve restricted mana metadata
preserve commander partner identity without depending on partner order
preserve unsupported behavior records
preserve target progress records
avoid interpreting Phase 13 trace v1 records as SIM-R state records
remain evidence-only
```

## Required Future Tests

The later implementation packet must add tests proving:

```text
state serializes deterministically
state round-trips through dictionary form
actions are not implemented in the state model packet
input structures are not mutated by builders
duplicate card_instance_id across zones fails validation
negative mana fails validation
restricted mana remains visible
commander partner identity is order-independent where applicable
zone ordering is preserved
unsupported behavior remains visible
target progress remains visible
metadata that does not affect legality remains separate from state identity
Phase 13 trace v1 is not accepted as a SIM-R state
no recommendation language appears
```

## Dependency Rules

Allowed future dependencies:

```text
standard library
codie.probability_engine models only when needed for shared primitive types
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
behavior or tests. It must be additive and isolated until a later transition
contract wires SIM-R state into action search.

## Gate

Phase 31E is blocked until Phase 31D outside validation returns PASS or PASS
WITH REVIEW NOTES.

