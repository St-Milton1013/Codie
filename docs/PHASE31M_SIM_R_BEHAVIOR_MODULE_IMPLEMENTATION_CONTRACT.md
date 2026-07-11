# Phase 31M - SIM-R Behavior Module Implementation Contract

Status: implementation contract only

## Purpose

Phase 31M authorizes a future implementation packet for pure in-memory SIM-R
behavior module data models and validators.

Phase 31L defined the behavior module boundary. Phase 31M narrows the future
implementation scope so the next packet can add behavior profiles and behavior
proposals without executing card behavior, mutating game state, writing resource
ledgers, running search, or integrating with the existing Phase 13 simulator.

This phase does not implement behavior module code.

## Accepted Dependency

Phase 31M may begin because Phase 31L outside validation returned:

```text
PASS WITH REVIEW NOTES
```

## Future Implementation Scope

A later accepted implementation packet may add only:

```text
codie/probability_engine/sim_r_behavior.py
tests/test_probability_engine_sim_r_behavior.py
```

The future implementation may update:

```text
codie/probability_engine/__init__.py
```

only to export the new public SIM-R behavior model symbols.

## Future Public Interface

The future implementation may define:

```text
SIM_R_BEHAVIOR_VERSION
SUPPORTED_BEHAVIOR_CATEGORIES
UNSUPPORTED_BEHAVIOR_CATEGORY
SimulationBehaviorBuildError
SimulationBehaviorProfile
SimulationBehaviorRequirement
SimulationBehaviorProposal
SimulationUnsupportedBehaviorNote
build_behavior_profile(...)
build_behavior_proposal(...)
behavior_profile_to_dict(...)
behavior_proposal_to_dict(...)
validate_behavior_profile(...)
validate_behavior_proposal(...)
```

## Future Model Responsibilities

The future behavior models may represent:

```text
behavior identity
behavior category
behavior version
supported action types
source card identity when available
required resource intents
zone-change intents
target requirements
timing restrictions
unsupported behavior notes
confidence/status fields
non-executable metadata
```

Behavior proposals may describe what a behavior module proposes should happen.
They must not apply that proposal to state.

## Required Future Rules

The future implementation must:

```text
use immutable dataclasses or equivalent immutable value objects
avoid in-place mutation
serialize deterministically
round-trip through JSON-compatible dictionaries
require behavior_profile_id
require behavior_key
require behavior_category
require behavior_version
require supported_action_types
preserve required resource intents
preserve zone-change intents
preserve target requirements
preserve timing restrictions
preserve unsupported behavior notes
preserve confidence/status fields
preserve source card identity when available
reject unknown behavior categories unless explicitly marked Unsupported
reject executable code payloads
reject callable objects
reject LLM-authored executable behavior
reject negative confidence values
reject confidence values above 1.0
remain evidence-only
```

## Initial Behavior Categories

The future implementation may define these values as data labels only:

```text
NormalCast
ManaProduction
FastMana
Tutor
Draw
CounterSpell
Bounce
Removal
AlternativeCost
CommanderCondition
PitchCost
PayLife
ChangeZone
StaticCondition
TurnRestriction
TargetRequirement
Unsupported
```

These labels must not execute behavior by themselves.

## Not Authorized In Phase 31M

```text
production behavior module implementation
card behavior execution
action execution
state mutation logic
resource ledger mutation
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
applying behavior proposals to SimulationState
creating resource ledger entries
building transition results
executing real Magic rules
resolving targets against a live state engine
checking legal plays against a full rules engine
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
codie.probability_engine.sim_r_state
codie.probability_engine.sim_r_transition
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
behavior profile serializes deterministically
behavior proposal serializes deterministically
behavior profile round-trips through dictionary form
behavior proposal round-trips through dictionary form
models are immutable
input structures are not mutated by builders
behavior_profile_id remains visible
behavior_key remains visible
behavior_category remains visible
behavior_version remains visible
supported_action_types remain visible
required resource intents remain visible
zone-change intents remain visible
target requirements remain visible
timing restrictions remain visible
unsupported behavior notes remain visible
confidence/status fields remain visible
source card identity remains visible when available
unknown behavior category fails unless explicitly Unsupported
executable code payloads are rejected
callable objects are rejected
LLM-authored executable behavior is rejected
negative confidence fails
confidence above 1.0 fails
no state mutation helper is added
no action execution helper is added
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
```

It must remain additive and isolated until a later SIM-R wiring contract
explicitly allows behavior proposals to feed transition packets.

## Evidence Boundary

SIM-R behavior module output is simulator evidence only.

It must never become tournament evidence and must never directly generate
recommendations.

## Phase 31M Scope

This Phase 31M packet may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Gate

Phase 31N is blocked until Phase 31M outside validation returns PASS or PASS
WITH REVIEW NOTES.
