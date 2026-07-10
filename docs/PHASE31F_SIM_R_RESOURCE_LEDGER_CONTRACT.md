# Phase 31F - SIM-R Resource Ledger Contract

Status: contract-only

## Purpose

Phase 31F defines the future SIM-R resource ledger boundary.

The resource ledger is the proof layer for resource consumption in future
SIM-R state transitions. It must make costs, payments, and consumed resources
explicit so a card, mana unit, land drop, life payment, discard, exile, or
other resource cannot satisfy two costs.

This phase does not implement the resource ledger.

## Authorized Scope

```text
resource ledger contract
ledger entry field definitions
resource category definitions
cost/payment relationship rules
double-spend prevention requirements
state relationship requirements
serialization requirements
future test requirements
outside validation prompt
checkpoint documentation
active roadmap/status updates
```

## Not Authorized

```text
production simulator code
resource ledger implementation
state transition implementation
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

## Ledger Principle

Every consumed resource must produce a durable ledger entry.

```text
state_before + action + cost/payment = ledger_entry + state_after
```

Ledger entries must be append-only within a transition. They may not rewrite
prior entries.

## Required Future Ledger Entry Fields

Future resource ledger entries must account for:

```text
ledger_entry_id
ledger_version
simulation_id
history_id
action_id
resource_key
resource_type
resource_quantity
source_card_instance_id
source_zone
destination_zone
cost_key
payment_key
turn
phase
step
pre_state_id
post_state_id
reversible
metadata
```

## Resource Types

Future resource ledger entries must support at least:

```text
mana
restricted_mana
life
card_in_hand
card_in_library
card_on_battlefield
card_in_graveyard
card_in_exile
commander_cast
land_drop
tap_status
once_per_turn_activation
floating_memory
```

Additional resource types require a future contract or an explicitly accepted
implementation report.

## Cost / Payment Relationship

Each payment must reference a cost.

Required future concepts:

```text
cost_key
payment_key
required_resource_type
required_quantity
paid_resource_key
paid_quantity
payment_status
```

Payment status values:

```text
paid
partial
failed
unsupported
```

Failed and unsupported payments must remain visible.

## Double-Spend Rule

The same resource instance may not satisfy two costs unless an explicit future
rule says that resource is reusable.

Examples:

```text
one mana unit pays one cost once
one discarded card pays one discard cost once
one exiled card pays one exile cost once
one land drop is consumed once
one tap activation consumes untapped status once
one life payment is recorded once per cost
```

Reusable/static resources must be represented as conditions, not consumed
resources, unless a later contract defines otherwise.

## State Relationship

Future ledger entries must link to SIM-R state records:

```text
pre_state_id
post_state_id
state_version
```

The ledger may reference state identifiers but must not mutate state records.

Phase 31F does not implement state transitions.

## Restricted Mana Rule

Restricted mana must preserve its restriction text or structured restriction
metadata through payment.

Invalid restricted-mana use must produce:

```text
payment_status = failed
reason
restriction
attempted_cost
```

Restricted mana may never silently pay an invalid cost.

## Unsupported Resource Rule

Unsupported costs or resource behaviors must produce visible unsupported
ledger entries or validation failures. They must not be ignored.

Required future unsupported fields:

```text
unsupported_reason
affected_card_instance_id
affected_action_id
affected_cost_key
blocking
```

## Serialization Requirements

Future ledger serialization must be:

```text
deterministic
versioned
JSON-compatible
round-trip safe
append-only in ordering
explicit about failed payments
explicit about unsupported payments
explicit about restricted mana
```

## Evidence Boundary

Resource ledger output is simulator evidence only.

It must not become:

```text
tournament evidence
recommendation output
card ranking
deckbuilding advice
strategy claim
```

## Future Implementation Shape

A later implementation packet may add:

```text
codie/probability_engine/sim_r_ledger.py
tests/test_probability_engine_sim_r_ledger.py
```

Only after this contract is externally accepted.

## Gate

Phase 31G is blocked until Phase 31F outside validation returns PASS or PASS
WITH REVIEW NOTES.

