# Phase 31A - SIM-R Architecture Contract

Status: contract-only

## Purpose

Phase 31A defines the architecture boundary for Simulator Revision (SIM-R).
It does not authorize runtime implementation.

SIM-R is a future deterministic strategic state engine for Codie's probability
simulator. It must preserve existing simulator behavior, historical results,
review exports, challenge mode, persistence, and deterministic replay while
opening a contract path toward immutable states, resource ledgers, behavior
modules, compound targets, trace v2, and paired simulations.

## Authorized Scope

```text
architecture contract
boundary definition
phase order definition
validation packet definition
compatibility requirements
non-goal confirmation
outside validation prompt
checkpoint documentation
```

## Not Authorized

```text
production simulator changes
schema changes
repository changes
database reads or writes
Forge integration
Forge dependency installation
behavior module implementation
state engine implementation
resource solver implementation
compound target implementation
trace v2 implementation
paired simulation implementation
LLM behavior generation
recommendation generation
UI work
live network calls
```

## Existing Simulator Freeze

The current simulator track remains authoritative until a later SIM-R
implementation phase is separately contracted and validated.

Frozen existing surfaces:

```text
codie/probability_engine/deck_parser.py
codie/probability_engine/shuffle.py
codie/probability_engine/mulligan.py
codie/probability_engine/search.py
codie/probability_engine/batch.py
codie/probability_engine/challenge_mode.py
codie/probability_engine/line_review.py
codie/probability_engine/review_export.py
codie/probability_engine/review_export_writer.py
codie/probability_engine/persistence.py
codie/probability_engine/reviewed_accuracy.py
codie/probability_engine/card_definition_manager.py
```

Phase 31A must not modify these files.

## SIM-R Target Architecture

Future SIM-R phases may define:

```text
immutable simulation state
deterministic history
resource ledger
behavior module registry
card behavior profiles
compound target conditions
post-line interaction readiness
state hash and pruning model
trace v2 records
paired simulation histories
unsupported behavior reporting
simulator confidence signals
```

## Core Invariants

Future implementation must preserve these invariants:

```text
same seed and config produce same result
same input ordering produces deterministic output ordering
actions produce new states and do not mutate prior states
resources consumed by one cost cannot satisfy another cost
cards cannot exist in two zones at the same time
mana cannot become negative
unsupported behavior is visible and never silently ignored
simulator output remains evidence only
simulator output never becomes tournament evidence
simulator output never directly generates recommendations
historical traces are never silently reinterpreted
```

## Behavior Module Boundary

Future behavior modules may describe reusable card behavior categories such as:

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

Phase 31A does not implement any behavior module.

## Forge Boundary

Forge may be used only as a future reference and validation source. It must not
become Codie's simulator runtime.

Allowed future Forge uses:

```text
behavior discovery
alternative cost discovery
condition discovery
validation fixtures
optional sampled validation
```

Forbidden Forge uses:

```text
Monte Carlo execution
deck search
statistics generation
recommendation generation
game AI
runtime replacement
```

## LLM Boundary

LLMs must never generate executable simulator behavior.

LLMs may only help future review workflows by:

```text
summarizing unsupported mechanics
proposing behavior mappings for human review
explaining why behavior is unsupported
drafting documentation
```

Any LLM-proposed mapping must remain non-executable until manually reviewed,
validated, and converted through a later approved contract.

## Phase Order

```text
Phase 31A - SIM-R architecture contract
Phase 31B - SIM-R current simulator freeze / validation packet
Phase 31C - SIM-R state model contract
Phase 31D - SIM-R state model implementation
Phase 31E - SIM-R resource ledger contract
Phase 31F - SIM-R behavior module contract
Phase 31G - SIM-R compound target / trace v2 contract
```

Later phase names may change, but implementation must remain contract-first.

## Validation Requirements

Outside validation must confirm:

```text
Phase 31A is contract-only
existing simulator files were not modified
no schema/repository changes were introduced
no Forge dependency or runtime integration was added
no LLM SDK or live LLM call was added
no recommendation output was added
no UI behavior was added
SIM-R remains evidence-only
existing Phase 13 and Phase 14 simulator contracts remain authoritative
the next phase remains blocked until outside validation accepts Phase 31A
```

