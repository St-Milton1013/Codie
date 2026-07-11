# Phase 31L - SIM-R Behavior Module Contract

Status: contract only

## Purpose

Phase 31L defines the future boundary for SIM-R behavior modules.

The accepted SIM-R state, ledger, and transition packets now define how future
simulation evidence can represent state, resource accounting, and transition
results. The next layer must define how future card/action behavior modules may
produce behavior results without turning Codie into a full Magic rules engine.

This phase does not implement behavior modules.

## Behavior Module Principle

Every future behavior module must be a narrow deterministic component:

```text
state snapshot + action intent + behavior profile
= behavior result proposal + required resource intents + unsupported behavior notes
```

Behavior modules must not mutate state directly.

Behavior modules must not write ledgers directly. They may propose resource
requirements that a later transition/resource layer validates.

## Authorized Future Implementation Scope

A later accepted implementation packet may add pure in-memory behavior module
models and validators such as:

```text
codie/probability_engine/sim_r_behavior.py
tests/test_probability_engine_sim_r_behavior.py
```

The future implementation may define:

```text
SIM_R_BEHAVIOR_VERSION
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

## Phase 31L Scope

This Phase 31L packet may create only:

```text
behavior module contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Not Authorized In Phase 31L

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

## Required Future Behavior Module Rules

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
reject unknown behavior categories unless explicitly marked unsupported
reject executable code payloads
reject LLM-authored executable behavior
remain evidence-only
```

## Initial Behavior Categories

The future implementation may define these categories as data labels only:

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
unknown behavior category fails unless explicitly unsupported
executable code payloads are rejected
LLM-authored executable behavior is rejected
no state mutation helper is added
no action execution helper is added
no search implementation is added
no recommendation language appears
```

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

## Forge And LLM Boundary

Forge may remain reference material for future human-reviewed behavior discovery.

LLMs may never generate executable behavior modules.

Any future LLM-assisted behavior proposal must remain non-executable, marked as
unapproved, and require explicit validation before becoming a supported profile.

## Compatibility Boundary

The future implementation must not change existing Phase 13/14 simulator
behavior, Phase 31E SIM-R state behavior, Phase 31H resource ledger behavior, or
Phase 31K transition behavior.

It must remain additive and isolated until a later SIM-R transition wiring
contract explicitly allows behavior proposals to feed transition packets.

## Evidence Boundary

SIM-R behavior module output is simulator evidence only.

It must never become tournament evidence and must never directly generate
recommendations.

## Gate

Phase 31M is blocked until Phase 31L outside validation returns PASS or PASS
WITH REVIEW NOTES.

