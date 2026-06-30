# Phase 13O - Simulator Persistence Contract

## Purpose

Define simulator persistence boundaries before implementation.

Codie already has simulator persistence tables and a repository:

```text
codie/db/schema/simulation.sql
codie/db/repositories/simulation.py
```

This contract defines how Phase 13P should persist Phase 13N batch results
through that existing DB layer without adding schema changes.

This is a contract-only packet. It does not add persistence code, schema
changes, Challenge Mode, line review, UI, or recommendation output.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md
docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md
docs/SCHEMA_SPEC.md
docs/DEPENDENCY_RULES.md
codie/db/schema/simulation.sql
codie/db/repositories/simulation.py
```

## Existing Tables

Phase 13P must use the existing tables:

```text
simulation_batches
simulation_batch_results
simulation_traces
```

## Existing Repository

Phase 13P must use:

```text
codie.db.repositories.simulation.SimulationRepository
```

Existing methods:

```text
create_batch(...)
create_result(...)
create_trace(...)
```

## Files To Create Or Modify In Phase 13P

Expected files:

```text
codie/probability_engine/persistence.py
tests/test_probability_engine_persistence.py
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

Allowed modifications:

```text
codie/db/repositories/simulation.py
codie/db/repositories/__init__.py
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Do not modify schema unless a separate migration contract is approved.

## Public Classes And Functions To Add

```text
PersistedSimulationBatch
persist_batch_run_result(...)
batch_result_to_repository_rows(...)
trace_sample_to_repository_row(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None for Phase 13P.

Use existing JSON columns for reproducibility metadata:

```text
simulation_batches.raw_config_json
simulation_batch_results.raw_payload_json
simulation_traces.final_state_json
simulation_traces.action_trace_json
```

Explicit seed/version columns may be considered later in a separate migration
packet, but Phase 13P must not add them.

## Dependency Impact

Allowed:

```text
codie.probability_engine.batch
codie.probability_engine.models
codie.db.repositories.simulation
standard library only
```

Forbidden:

```text
codie.providers
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
requests
httpx
live network calls
raw SQL outside codie/db
```

## Layer Boundary

Probability engine persistence is a thin adapter from pure batch results to the
repository layer.

Allowed direction:

```text
probability_engine.persistence -> SimulationRepository
```

Forbidden directions:

```text
db/repositories -> probability_engine
providers -> probability_engine.persistence
analytics -> probability_engine.persistence
recommendations -> probability_engine.persistence
```

The batch runner itself must remain pure. Do not make
`codie/probability_engine/batch.py` import DB or repositories.

## Persistence Workflow

Phase 13P should persist a `BatchRunResult` in this order:

```text
1. create simulation_batches row
2. create simulation_batch_results row
3. create simulation_traces rows for stored samples
4. return persisted identifiers
```

All writes for one batch must be atomic.

If result or trace persistence fails, no partial simulator batch should remain.

## Batch Row Mapping

`simulation_batches` mapping:

```text
batch_id
deck_hash
decklist_source
games_requested
games_completed
min_mulligan_keep
mulligan_mode
elapsed_ms
status
created_at
completed_at
raw_config_json
```

Required raw config metadata:

```text
batch_config
mulligan_policy
search_config
target_condition
batch_version
base_seed
game_index_start
card_model_versions if available
```

Suggested `status` values:

```text
completed
completed_with_unsupported
invalid_target
limit_exceeded
failed
```

## Result Row Mapping

`simulation_batch_results` mapping:

```text
batch_id
target_card
target_card_id
target_zone
turn
win_count
win_rate
margin_of_error
missing_cards_json
raw_payload_json
```

Phase 13P must map:

```text
win_count = success_count
win_rate = success_rate
margin_of_error = null
missing_cards_json = unsupported_cards and unsupported_actions payload
raw_payload_json = full aggregate summary
```

The raw payload must include:

```text
games_completed
success_count
failure_count
unsupported_count
invalid_target_count
limit_exceeded_count
unsupported_rate
average_mulligan_count
sample counts
generated_at
```

## Trace Row Mapping

`simulation_traces` mapping:

```text
batch_id
result_id
game_index
success
mulligan_count
opening_hand_json
final_state_json
action_trace_json
created_at
```

Phase 13P may persist trace samples only, not every game, unless configured by a
future contract.

Trace rows must preserve:

```text
game_index
search_status
success
opening hand
mulligan_count if available
action trace
unsupported cards/actions
```

## ID Rules

`batch_id` must be deterministic for the same persisted payload unless an
explicit caller-supplied ID is provided.

Suggested batch ID payload:

```text
deck_hash
target_condition
batch_config
mulligan_policy
search_config
games_completed
generated_at
```

Use a `sha256:` prefix.

## Atomicity Rules

Required:

```text
one transaction or savepoint for batch/result/trace writes
rollback on any failure
no orphan simulation_batch_results
no orphan simulation_traces
no empty simulation_batches after result failure
```

## Evidence Boundary

Simulator persistence is not tournament evidence by default.

Phase 13P must not:

```text
update evidence_counts
write analytics tables
write recommendation tables
write canonical tables
turn simulation output into card recommendations
```

Simulation evidence stack integration remains a future gated phase.

## Acceptance Tests For Phase 13P

Required tests:

```text
persisted batch creates one simulation_batches row
persisted result creates one simulation_batch_results row
trace samples create simulation_traces rows
raw_config_json includes seed/version/search/mulligan metadata
raw_payload_json includes aggregate counts and rates
unsupported cards/actions are preserved
batch persistence is atomic on result failure
batch persistence is atomic on trace failure
batch runner remains DB-free
probability_engine.persistence imports SimulationRepository but not providers/analytics/recommendations
no raw SQL appears outside codie/db
no evidence_counts or recommendations writes occur
full suite passes
```

## Do Not Do In Phase 13O

```text
Do not implement persistence.
Do not add schema changes.
Do not update evidence_counts.
Do not add Challenge Mode.
Do not add line review.
Do not add UI.
Do not add recommendation output.
Do not call providers, Scryfall, DB live backfills, or network.
```

## Recommended Next Step

```text
Phase 13P - Simulator Persistence Implementation
```

Implement the persistence adapter described here using existing simulator
tables and `SimulationRepository`, with atomicity tests and no schema changes.
