# Phase 31C - SIM-R State Model Contract

Status: contract-only

## Purpose

Phase 31C defines the future SIM-R immutable state model boundary.

This phase does not implement state classes, simulator actions, behavior
modules, search, persistence, schema, CLI behavior, UI, Forge integration, or
LLM behavior generation.

The goal is to make the future state model explicit before implementation so
SIM-R can be built around deterministic, replayable, non-mutating state
transitions.

## Authorized Scope

```text
state model contract
state field definitions
zone model definitions
resource ledger relationship
state transition invariants
state hashing requirements
serialization requirements
compatibility requirements
outside validation prompt
checkpoint documentation
active roadmap/status updates
```

## Not Authorized

```text
production simulator code
state class implementation
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

## State Model Principle

SIM-R state must be immutable.

```text
Input state + action = output state + trace event
```

An action must never mutate the input state in place.

## Required Future State Fields

Future SIM-R state models must account for:

```text
state_id
state_version
simulation_id
history_id
turn
phase
step
active_player
priority_player
hand
library
battlefield
graveyard
exile
command_zone
stack
mana_pool
life_total
land_drop_available
lands_played_this_turn
commander_state
resource_ledger
target_progress
unsupported_behaviors
metadata
```

## Zone Model Requirements

Zones must preserve deterministic card identity and ordering when ordering
matters.

Required zone properties:

```text
zone_name
ordered
cards
visibility
owner
controller
```

Required card instance properties:

```text
card_instance_id
scryfall_id
oracle_id
name
owner
controller
zone
zone_index
status_flags
source_card_id
```

The same `card_instance_id` must not appear in more than one zone in the same
state.

## Commander State Requirements

Commander state must represent:

```text
commander_instance_ids
commander_cast_count
commander_tax
commander_zone
partner_group_key
```

Partner order must not affect commander identity, but card instances remain
distinct.

## Mana Pool Requirements

Mana pool state must represent:

```text
W
U
B
R
G
C
restricted_mana
floating_mana_sources
expires_at_step
```

Mana may never become negative.

Restricted mana must remain visible and may not silently pay invalid costs.

## Resource Ledger Relationship

Phase 31C does not implement the resource ledger, but state must reserve a
stable relationship to it.

Future ledger entries must be able to prove:

```text
resource consumed
source card/action
cost paid
turn/phase/step
state before
state after
```

A resource consumed by one cost may not satisfy another cost.

## Target Progress Requirements

Target progress must support future compound goals without implementing those
goals in Phase 31C:

```text
target_condition_id
target_condition_version
primary_success
support_success
compound_success
required_components
satisfied_components
failed_components
interaction_readiness
```

## Unsupported Behavior Requirements

Unsupported behavior must be explicit in state and trace context.

Required future fields:

```text
card_instance_id
card_name
behavior_key
reason
severity
action_blocked
discovered_at_state_id
```

Unsupported behavior must never be silently ignored.

## State Hash Requirements

Future state hashes must be deterministic and must include all fields that can
change future legal actions or target progress.

Hash inputs must include:

```text
turn
phase
step
hand
library position or library ordering when relevant
battlefield
graveyard
exile
command zone
stack
mana pool
life total
land-drop state
commander state
resource ledger summary
target progress
unsupported blocking behavior
```

Metadata that does not affect legal actions must not change the state hash.

## Serialization Requirements

Future state serialization must be:

```text
deterministic
versioned
JSON-compatible
round-trip safe
stable under equivalent ordering rules
explicit about hidden/visible zones
explicit about unsupported behavior
```

## Compatibility Requirements

Future implementation must not reinterpret existing Phase 13 traces as SIM-R
states.

Phase 13 traces remain historical trace v1 records. SIM-R state records and
trace v2 records must be versioned separately.

## Evidence Boundary

SIM-R state model output is simulator evidence only.

It must not become:

```text
tournament evidence
recommendation output
card ranking
deckbuilding advice
strategy claim
```

## Gate

Phase 31D is blocked until Phase 31C outside validation returns PASS or PASS
WITH REVIEW NOTES.

