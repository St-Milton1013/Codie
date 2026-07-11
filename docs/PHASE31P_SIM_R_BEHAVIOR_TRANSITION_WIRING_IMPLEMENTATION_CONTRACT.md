# Phase 31P - SIM-R Behavior Transition Wiring Implementation Contract

Status: implementation contract only

## Purpose

Phase 31P authorizes a future implementation packet for pure in-memory SIM-R
behavior-to-transition wiring models and validators.

Phase 31O defined the wiring boundary. Phase 31P narrows the next implementation
scope so a later packet can add transition-link and wiring-result value objects
without executing card behavior, applying behavior proposals to state, creating
resource ledgers, building transition results, running search, or integrating
with the existing Phase 13 simulator.

This phase does not implement behavior-transition wiring code.

## Accepted Dependency

Phase 31P may begin because Phase 31O outside validation returned:

```text
PASS WITH REVIEW NOTES
```

## Future Implementation Scope

A later accepted implementation packet may add only:

```text
codie/probability_engine/sim_r_wiring.py
tests/test_probability_engine_sim_r_wiring.py
```

The future implementation may update:

```text
codie/probability_engine/__init__.py
```

only to export the new public SIM-R wiring model symbols.

## Future Public Interface

The future implementation may define:

```text
SIM_R_WIRING_VERSION
SimulationWiringBuildError
SimulationBehaviorTransitionLink
SimulationBehaviorWiringResult
build_behavior_transition_link(...)
build_behavior_wiring_result(...)
behavior_transition_link_to_dict(...)
behavior_wiring_result_to_dict(...)
validate_behavior_transition_link(...)
validate_behavior_wiring_result(...)
```

## Future Model Responsibilities

The future wiring models may represent:

```text
wiring identity
wiring version
simulation ID
pre-state ID
post-state ID
action ID
behavior profile ID
behavior proposal ID
behavior key
behavior category
transition ID when already available
resource ledger IDs
requirement IDs
unsupported behavior note IDs
compatibility status
failure reason
caveats
non-executable metadata
```

The future wiring models may validate references between already-built packet
identifiers. They must not execute or apply those packets.

## Required Future Rules

The future implementation must:

```text
use immutable dataclasses or equivalent immutable value objects
avoid in-place mutation
serialize deterministically
round-trip through JSON-compatible dictionaries
require wiring_id
require wiring_version
require simulation_id
require pre_state_id
require post_state_id
require action_id
require behavior_profile_id
require behavior_proposal_id
require behavior_key
require behavior_category
preserve transition_id when already available
preserve resource ledger IDs
preserve requirement IDs
preserve unsupported behavior note IDs
preserve compatibility status
preserve failure reason when present
preserve caveats
reject executable code payloads
reject callable objects
reject LLM-authored executable behavior
remain evidence-only
```

## Required Compatibility Rules

The future implementation must reject or caveat:

```text
missing behavior profile ID
missing behavior proposal ID
missing action ID
behavior key mismatch
behavior category mismatch
successful compatibility status without required references
duplicate resource ledger IDs
duplicate requirement IDs
duplicate unsupported behavior note IDs
negative turn metadata
negative priority sequence metadata
```

## Not Authorized In Phase 31P

```text
production wiring implementation
behavior proposal application
transition result creation
card behavior execution
action execution
state mutation logic
resource ledger creation or mutation
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

## Not Authorized In The Future Implementation Packet

The future implementation packet must also avoid:

```text
executing behavior proposals
applying zone changes to SimulationState
checking legal plays against a rules engine
creating resource ledger entries
building transition results from scratch
running Monte Carlo simulation
calling existing Phase 13 simulator search
loading Scryfall or provider data
reading local SQLite data
```

Those require later contracts.

## Dependency Rules

Allowed future dependencies:

```text
standard library
codie.probability_engine.sim_r_behavior
codie.probability_engine.sim_r_transition
codie.probability_engine.sim_r_ledger
codie.probability_engine.sim_r_state
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

## Required Future Tests

The later implementation packet must add tests proving:

```text
transition link serializes deterministically
wiring result serializes deterministically
transition link round-trips through dictionary form
wiring result round-trips through dictionary form
models are immutable
input structures are not mutated by builders
wiring_id remains visible
wiring_version remains visible
simulation_id remains visible
pre_state_id remains visible
post_state_id remains visible
action_id remains visible
behavior_profile_id remains visible
behavior_proposal_id remains visible
behavior_key remains visible
behavior_category remains visible
transition_id remains visible when present
resource ledger IDs remain visible
requirement IDs remain visible
unsupported behavior note IDs remain visible
compatibility status remains visible
failure reason remains visible when present
caveats remain visible
behavior key mismatch fails or creates explicit incompatible status
behavior category mismatch fails or creates explicit incompatible status
duplicate resource ledger IDs fail validation
duplicate requirement IDs fail validation
duplicate unsupported behavior note IDs fail validation
negative turn metadata fails validation
negative priority sequence metadata fails validation
executable code payloads are rejected
callable objects are rejected
LLM-authored executable behavior is rejected
no behavior execution helper is added
no state mutation helper is added
no ledger-writing helper is added
no transition-building helper is added
no search implementation is added
no recommendation language appears
```

## Compatibility Boundary

The future implementation must not change existing:

```text
Phase 13/14 simulator behavior
Phase 31E SIM-R state behavior
Phase 31H SIM-R resource ledger behavior
Phase 31K SIM-R transition behavior
Phase 31N SIM-R behavior model behavior
```

It must remain additive and isolated until a later SIM-R runtime integration
contract explicitly allows behavior wiring to participate in simulation runs.

## Evidence Boundary

SIM-R wiring output is simulator evidence only.

It must never become tournament evidence and must never directly generate
recommendations.

## Phase 31P Scope

This Phase 31P packet may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Gate

Phase 31Q is blocked until Phase 31P outside validation returns PASS or PASS
WITH REVIEW NOTES.
