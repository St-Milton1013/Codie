# Phase 13 - Simulator Contract Refresh

## Purpose

Refresh the simulator, probability engine, Challenge Mode, and simulator review
contracts before implementation begins.

This is a contract-only packet. It does not add simulator code or schema.

## Source Documents

This refresh reconciles:

```text
docs/CODIE_V1_CONSTITUTION.md
docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md
docs/DEPENDENCY_RULES.md
codie/db/schema/simulation.sql
codie/db/repositories/simulation.py
```

## Current State

Already present:

```text
simulation_batches
simulation_batch_results
simulation_traces
SimulationRepository
```

Not yet present:

```text
codie/probability_engine/
card model registry
target condition models
opening-hand generator
London mulligan policy
action search
Monte Carlo runner
challenge mode
line review annotations
trace review exports
simulator CLI
```

## Core Boundary

The simulator is not a recommendation engine.

It may answer:

```text
Under this explicit model/config/seed, was target X reachable by turn Y?
Across this reproducible batch, what was the observed target access rate?
Which cards/actions were unsupported by the model?
What action trace did the simulator produce?
```

It must not answer:

```text
You should play this card.
This card is correct.
This line is strategically optimal.
This card breaks the format.
This simulator result is tournament evidence by itself.
```

## Dependency Rules

Allowed future dependencies:

```text
probability_engine -> cards read models
probability_engine -> user/source deck inputs
probability_engine -> simulation repository for persistence
probability_engine -> exports for trace review output
```

Forbidden future dependencies:

```text
probability_engine -> providers
probability_engine -> live network clients
probability_engine -> recommendations as an owner
probability_engine -> direct raw SQL outside repositories
probability_engine -> UI
probability_engine -> outbound delivery
```

Recommendations may later consume accepted simulation evidence only through
validated evidence/analytics surfaces, not by running the simulator directly.

## Reproducibility Rules

Every simulation batch, challenge, and trace must preserve:

```text
deck_hash
target condition
seed or deterministic seed derivation
simulator_version
card_model_version
mulligan_policy_version
complete config JSON
generated_at / created_at
unsupported cards
unsupported actions
```

No result may silently ignore unsupported cards. Unsupported cards must be
reported in the result payload and trace output.

## Existing Schema Gap

The existing `simulation_batches` table stores `raw_config_json`, but does not
have explicit columns for:

```text
seed
simulator_version
card_model_version
mulligan_policy_version
unsupported_cards_json
unsupported_actions_json
```

For the first implementation packet, these values may be stored inside
`raw_config_json` and `raw_payload_json` if the contract explicitly requires
them and tests verify they exist.

Before broad simulator usage, consider a dedicated schema migration packet for
explicit reproducibility columns and challenge/review tables.

## MVP Scope

The MVP remains a lightweight action-based target-access simulator, not a full
Magic rules engine.

MVP may model:

```text
opening hands
London mulligans
turn progression
lands and fetchlands
artifact mana
ritual mana
simple tutors
restricted mana tags
cast/access target conditions
action traces
unsupported-card disclosure
```

MVP must not attempt:

```text
full multiplayer game state
opponent interaction
complete priority/stack realism
combat
all replacement effects
all triggered abilities
full Oracle text interpretation
strategic deckbuilding advice
```

## Shared Models To Define Next

Phase 13A should define models only:

```text
SimulationTargetCondition
SimulationConfig
SimulationDeck
SimulationCardModel
SimulationResult
SimulationTrace
SimulationUnsupportedItem
SimulationAction
SimulationZone
```

These models should be plain dataclasses or typed structures with no database
or provider dependency.

## Build Order

Recommended order:

```text
Phase 13A - Probability Engine Core Models Contract/Implementation
Phase 13B - Deck And Target Parser
Phase 13C - Opening Hand And Seeded Shuffle
Phase 13D - Minimal Card Model Registry
Phase 13E - Mana And Action Trace Primitives
Phase 13F - Target Access Search MVP
Phase 13G - Monte Carlo Batch Runner
Phase 13H - Simulation Persistence Wiring
Phase 13I - Challenge Mode Contract
Phase 13J - Challenge Mode Implementation
Phase 13K - Line Review / Veto Contract
Phase 13L - Line Review / Veto Implementation
Phase 13M - Trace Review Export Contract
```

Challenge Mode must not begin before the core simulator, target model, and trace
model are implemented and tested.

## Challenge Mode Rules

Challenge Mode must:

- use the same simulator engine as the probability engine
- generate opening hands deterministically from seed/config
- run the simulator against the exact displayed hand
- store the user answer separately from simulator result
- disclose unsupported cards
- compare user answer to simulator result without strategic judgment
- preserve all traces

Challenge Mode must not:

- invent separate hand-evaluation logic
- silently ignore unsupported cards
- turn user answers into tournament evidence
- turn simulator output into recommendation text
- overwrite historical challenge records

## Line Review / Veto Rules

Line review must be an annotation layer over immutable simulator output.

Allowed statuses:

```text
accepted
incorrect
unrealistic
unsupported_card_behavior
bad_sequencing
mana_model_error
tutor_search_error
other
```

Line review must not:

- delete simulator results
- modify raw action traces
- automatically retrain strategy
- become tournament evidence
- become recommendation evidence

Reviewed rejected lines may become:

```text
regression fixtures
simulator bug reports
unsupported-card backlog items
card behavior refinement tasks
```

## Evidence Stack Gate

Simulation evidence may enter evidence counts only when:

```text
games_completed >= configured minimum
margin_of_error <= configured threshold
deck_hash is stored
seed/config are stored
simulator/card-model versions are stored
unsupported cards are disclosed
batch is reproducible
```

Until those conditions are met, simulation results remain local simulator
outputs only.

## Required Acceptance Tests For Future Implementation

Future implementation packets must include tests for:

```text
seeded shuffle determinism
opening hand determinism
target condition serialization
unsupported card disclosure
unsupported action disclosure
same hand produces same trace under same config
different seed can produce different hand
batch config is persisted
trace output contains action sequence
no recommendation language appears
simulation evidence is excluded when evidence gate fails
```

Challenge Mode future tests:

```text
challenge hand generation is deterministic from seed
target condition is stored
user answer is recorded
simulator runs against exact hand
reachable line is returned when found
failure is returned when unreachable
unsupported cards are reported
original trace remains immutable
```

Line review future tests:

```text
user can accept a simulator line
user can veto a simulator line
veto stores reason and note
original trace remains unchanged
rejected reviewed line is excluded from accepted-success accuracy
review annotations do not affect raw simulation history
```

## Do Not Do In Phase 13

- Do not add simulator code.
- Do not add schema.
- Do not add new dependencies.
- Do not run live providers.
- Do not implement Challenge Mode.
- Do not implement line review.
- Do not add final recommendation output.
- Do not let simulator output bypass evidence gates.
