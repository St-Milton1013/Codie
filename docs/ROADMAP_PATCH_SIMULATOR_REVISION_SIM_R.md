# Roadmap Patch - Simulator Revision (SIM-R)

Status: architecture approved, implementation deferred

## Purpose

SIM-R is a future architectural revision for Codie's probability simulator.
It replaces the current target-access simulator architecture with a more
general deterministic strategic state engine while preserving all existing
simulator functionality and historical results.

This document does not authorize implementation.

## Implementation Blocker

Do not begin SIM-R implementation until all of the following are true:

```text
current implementation and validation chain is complete
current checkpoints pass
existing simulator contracts are frozen
dedicated SIM-R architecture contract exists
dedicated SIM-R outside validation returns PASS or PASS WITH REVIEW NOTES
dedicated SIM-R checkpoint plan is accepted
```

Until then, do not modify existing simulator implementation for SIM-R.

## Objective

The revised simulator should answer strategic probability questions such as:

```text
Rhystic Study by turn 2
Rhystic Study by turn 2 while preserving live interaction
Ad Nauseam with protection
commander online plus free interaction
compound package availability
```

The simulator remains a deterministic probability engine. It is not becoming a
complete Magic rules engine.

## Non-Goals

SIM-R must not build:

```text
full Magic rules engine
multiplayer AI
opponent AI
combat engine
continuous effect layer engine
complete stack engine
layer system
replacement effect engine
automatic support for every Magic card
dynamic LLM card execution
Forge runtime replacement
```

## Future Architecture

Current simulator shape:

```text
Deck -> Shuffle -> Mulligan -> Search -> Target Found -> Statistics
```

Future SIM-R shape:

```text
Deck
-> Deterministic History
-> Immutable Game State
-> Behavior Modules
-> Resource Ledger
-> Compound Target Search
-> State Hash / Pruning
-> Statistics
-> Optional Forge Validation
```

## Major Design Requirements

### Immutable Game State

Actions produce new states and never mutate previous states.

Future `SimulationState` should include:

```text
turn
phase
active_player
hand
battlefield
graveyard
exile
command_zone
library_position
mana_pool
life_total
land_drop_available
commander_state
resource_ledger
target_progress
history
```

### Resource Ledger

Every resource consumption must be explicit:

```text
cards exiled
cards discarded
cards sacrificed
cards imprinted
mana spent
life paid
land drops used
commander casts
once-per-turn resources
```

A resource may never satisfy two costs.

### Behavior Modules

Card support should be behavior-composition based, not custom simulator code
per card.

Initial behavior categories:

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
```

### Compound Targets

Future target conditions should support:

```text
ALL
ANY
AT_LEAST_N
PRIMARY_PLUS_SUPPORT
```

Expected result fields include:

```text
primary_success
support_success
compound_success
shield_down
interaction_live
interaction_reason
unsupported_behavior_count
behavior_support_level
search_completeness
```

### Post-Line Evaluation

The simulator must evaluate whether support remains live after an exact line,
not merely whether the support card could be cast from the opening hand.

### State Hashing

Future search should include deterministic state hashing and transposition
caching over:

```text
hand
battlefield
graveyard
mana
life
commander state
resource ledger
target progress
```

### Paired Simulation

Deck comparisons must support identical random histories for Deck A and Deck B.
This is required for meaningful change-impact reports.

### Trace Version 2

Existing traces remain supported. New traces should include:

```text
pre_state_hash
post_state_hash
resources_consumed
behavior_module
interaction_readiness
unsupported_behavior
pruning_reason
```

## Card Support Redesign

SIM-R stops prioritizing manual card implementations and moves toward behavior
profiles.

Future support pipeline:

```text
Card
-> Scryfall
-> Tagger
-> Quick Scan
-> Behavior Match
-> Existing Module
-> Supported
```

If no existing behavior applies:

```text
Forge Parser
-> Behavior Draft
-> Validation
-> Support Profile
```

### Tagger Quick Scan

Promote cards for simulator support only if they are simulator-relevant:

```text
interaction
tutor
fast mana
draw engine
combo piece
alternative cost
commander interaction
high cEDH frequency
explicit user request
```

All cards may exist in the database, but simulator support should focus on
cards observed in Codie datasets, active decks, active simulations,
recommendation candidates, frequency pools, or explicit user requests.

## Forge Integration

Forge is a research and validation source only. It is not the simulator.

Allowed Forge uses:

```text
behavior discovery
alternative cost discovery
condition discovery
validation fixtures
optional sampled validation
```

Forbidden Forge uses:

```text
Monte Carlo
deck search
statistics
recommendation generation
game AI
```

Initial supported Forge tokens:

```text
Name
ManaCost
Types
AlternativeCost
Cost
IsPresent
ValidCard
ValidPlayer
TargetType
ValidTgts
Counter
Draw
Mana
ChangeZone
```

Unknown tokens must never be guessed. They become unsupported behavior and
manual review items.

## Confidence Inputs

Future simulator confidence should include:

```text
Forge agreement
human review agreement
unsupported behavior rate
partial mapping rate
search completeness
```

## Deferred Items

```text
Z3 resource solver
dynamic programming mulligans
full Forge validation mode
full Magic rules engine
```

If a resource solver is ever added, it may only assist resource assignment. It
must not become the primary simulator.

Current mulligan behavior remains until a separate future contract replaces it.

## LLM Rules

LLMs must never generate executable simulator behavior.

LLMs may:

```text
summarize
propose mappings
explain unsupported mechanics
identify likely behavior
```

LLM output must flow through validation and manual approval before it can inform
a behavior module.

## Future Schema Concepts

Future SIM-R contracts may define versioned storage for:

```text
SimulationState
ResourceLedger
BehaviorModule
CardBehaviorProfile
CompoundTargetCondition
InteractionProfile
BehaviorSupportStatus
```

No schema change is authorized by this roadmap patch.

## Testing Requirements

All existing simulator tests must be retained.

Future SIM-R test groups:

```text
property tests
immutable state tests
resource ledger tests
paired comparison tests
behavior module tests
Forge fixture tests
trace v2 compatibility tests
unsupported behavior tests
deterministic replay tests
```

Required invariants:

```text
card cannot exist twice
consumed card cannot be reused
mana never negative
same seed produces same history and result
immutable states remain unchanged
commander conditions are enforced
alternative costs are validated
unsupported behavior is disclosed
```

## Planned SIM-R Phase Order

```text
SIM-R0 - Freeze current simulator contracts and generate validation packet
SIM-R1 - Strategic State Engine
SIM-R2 - Forge Assisted Validation
SIM-R3 - Freeze simulator redesign checkpoint
```

SIM-R1 includes:

```text
immutable state
behavior modules
resource ledger
compound targets
state hashing
trace v2
paired simulation
property tests
```

SIM-R2 includes:

```text
Forge sparse checkout or reference capture
Forge index
restricted parser
Forge AST
Codie IR
validation fixtures
sample validation
simulator confidence report
```

## Backward Compatibility

SIM-R must preserve:

```text
existing deck parser
existing batch runner
existing persistence
existing challenge mode
existing line review
existing review export
existing CLI
existing simulation database
existing trace reader
existing deterministic replay
```

All new schemas and trace formats must be versioned. Historical simulation
results must never be silently reinterpreted.

## Dependency Constraints

The simulator remains isolated.

SIM-R must not depend on:

```text
Recommendation Engine
Evidence Fusion
Tournament Analytics
Decision Intelligence
Jin-Gitaxias
```

The simulator produces evidence. It never produces recommendations.

## Stop Line

After SIM-R2, do not proceed into:

```text
full Forge runtime
full Magic rules engine
opponent simulation
combat engine
continuous effect engine
layer system
LLM generated execution
```

Future simulator work beyond SIM-R2 requires a new approved architectural
proposal demonstrating a user-facing capability that cannot be achieved by the
SIM-R2 architecture.
