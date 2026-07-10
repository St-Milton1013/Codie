# Phase 31G - SIM-R Resource Ledger Implementation Contract

Status: implementation contract only

## Purpose

Phase 31G defines the allowed implementation shape for the future SIM-R
resource ledger.

This phase does not implement the resource ledger. It authorizes a later
implementation packet to add pure, in-memory ledger models and validators that
satisfy the accepted Phase 31F resource ledger contract.

## Authorized Future Implementation Scope

A later accepted implementation packet may add:

```text
codie/probability_engine/sim_r_ledger.py
tests/test_probability_engine_sim_r_ledger.py
```

The future implementation may define pure data models and validators for:

```text
SIM_R_LEDGER_VERSION
SimulationLedgerBuildError
SimulationResourceLedgerEntry
SimulationPaymentRecord
SimulationResourceLedger
build_resource_ledger(...)
resource_ledger_to_dict(...)
validate_resource_ledger(...)
```

## Phase 31G Scope

This Phase 31G packet may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

## Not Authorized In Phase 31G

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

## Required Future Ledger Rules

The future implementation must:

```text
use immutable dataclasses or equivalent immutable value objects
avoid in-place mutation
serialize deterministically
round-trip through JSON-compatible dictionaries
preserve append-only ledger ordering
require ledger_entry_id uniqueness
require payment_key uniqueness within a ledger
reject duplicate consumed resource keys unless marked reusable by explicit metadata
reject negative resource quantities
preserve failed payment records
preserve unsupported payment records
preserve restricted mana metadata
preserve pre_state_id and post_state_id links
preserve action_id, cost_key, and payment_key references
remain evidence-only
```

## Required Future Tests

The later implementation packet must add tests proving:

```text
ledger serializes deterministically
ledger round-trips through dictionary form
ledger models are immutable
input structures are not mutated by builders
duplicate ledger_entry_id fails validation
duplicate payment_key fails validation
double-spent resource_key fails validation
explicit reusable resource metadata is visible
negative resource_quantity fails validation
restricted mana metadata remains visible
failed payment remains visible
unsupported payment remains visible
pre_state_id and post_state_id remain visible
action_id, cost_key, and payment_key remain visible
no state transitions are implemented
no recommendation language appears
```

## Dependency Rules

Allowed future dependencies:

```text
standard library
codie.probability_engine.sim_r_state only for version/state identifier constants if needed
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
behavior or Phase 31E SIM-R state behavior. It must be additive and isolated
until a later transition contract wires resource ledger records into SIM-R
state transitions.

## Gate

Phase 31H is blocked until Phase 31G outside validation returns PASS or PASS
WITH REVIEW NOTES.

