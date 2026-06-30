# Phase 13M - Monte Carlo Batch Runner Contract

## Purpose

Define deterministic Monte Carlo batch execution before implementation.

The batch runner will connect existing probability-engine components:

```text
deck parser / SimulationDeck
card definition manager
seeded shuffle
mulligan policy
target access search
result aggregation
```

This is a contract-only packet. It does not add batch code, persistence, schema
changes, Challenge Mode, line review, UI, or recommendation output.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md
docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md
docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md
docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md
docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md
```

## Files To Create In Phase 13N

```text
codie/probability_engine/batch.py
tests/test_probability_engine_batch.py
tests/fixtures/probability_engine/batch/batch_deck.txt
docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

```text
BatchRunConfig
BatchGameResult
BatchRunResult
BatchTraceSample
run_simulation_batch(...)
run_single_simulation_game(...)
summarize_batch_results(...)
```

Exact names may be adjusted during implementation if the completion report
documents the change and tests cover the public surface.

## Schema Impact

None.

## Dependency Impact

Allowed:

```text
codie.probability_engine.models
codie.probability_engine.card_definition_manager
codie.probability_engine.deck_parser
codie.probability_engine.shuffle
codie.probability_engine.mulligan
codie.probability_engine.search
standard library only
```

Forbidden:

```text
codie.providers
codie.db
codie.analytics
codie.recommendations
codie.ingestion
sqlite3
requests
httpx
live network calls
```

## Batch Boundary

The Monte Carlo batch runner estimates simulator outcomes. It is not advice.

It may answer:

```text
The configured simulator succeeded in N of M games.
The configured simulator reported unsupported behavior in N games.
The configured simulator found sample traces for successful games.
```

It must not answer:

```text
You should keep this deck.
You should play this card.
This card is optimal.
This deck is good or bad.
This is the correct build.
```

Batch output is reproducible simulator evidence only.

## Batch Input Requirements

Required inputs:

```text
SimulationDeck
SimulationTargetCondition
CardDefinitionManager or behavior overlay rows
base_seed
games_requested
MulliganPolicyConfig
SearchConfig
batch_version
```

Optional inputs:

```text
game_index_start
sample_successful_traces
sample_failed_traces
sample_unsupported_traces
generated_at
```

## Batch Config

Required fields:

```text
batch_version
base_seed
games_requested
game_index_start
sample_successful_traces
sample_failed_traces
sample_unsupported_traces
include_failed_trace_samples
include_unsupported_trace_samples
```

Validation rules:

```text
games_requested must be positive
game_index_start cannot be negative
trace sample counts cannot be negative
base_seed is required
batch_version is required
```

## Single-Game Workflow

Each game must follow this order:

```text
1. shuffle deck with base_seed and deterministic game_index
2. apply configured London mulligan policy
3. use kept hand after bottoming
4. preserve known remaining library order
5. run target access search against that exact hand and library
6. return per-game result with seed, game_index, mulligan_count, status, trace, and unsupported data
```

The runner must never resolve cards through Scryfall, providers, DB, or live
network calls. It consumes already-prepared simulation deck/card model data.

## Per-Game Result Output

Required fields:

```text
game_index
derived_seed
opening_hand_id
mulligan_count
kept_hand
bottomed_cards
search_status
success
actions_taken
branches_evaluated
unsupported_cards
unsupported_actions
trace
```

Allowed search statuses:

```text
success
failure
unsupported
invalid_target
limit_exceeded
```

## Batch Result Output

Required fields:

```text
deck_hash
target_condition
batch_config
mulligan_policy
search_config
games_requested
games_completed
success_count
failure_count
unsupported_count
invalid_target_count
limit_exceeded_count
success_rate
unsupported_rate
average_mulligan_count
sample_successful_traces
sample_failed_traces
sample_unsupported_traces
unsupported_cards
unsupported_actions
generated_at
```

Rates must be plain ratios from completed games:

```text
success_rate = success_count / games_completed
unsupported_rate = unsupported_count / games_completed
```

Do not add statistical confidence intervals in Phase 13N unless a separate
contract defines them.

## Trace Sampling Rules

Trace sampling must be deterministic.

Suggested default:

```text
keep the first N successful traces by game_index
keep the first N failed traces by game_index only when configured
keep the first N unsupported traces by game_index only when configured
```

Trace samples must not mutate original game results.

## Reproducibility Rules

The same inputs must produce the same batch result:

```text
deck hash
base_seed
game_index_start
games_requested
mulligan policy
search config
card definition overlays
batch version
search version
shuffle algorithm version
```

Batch output must include enough metadata to rerun the same games later.

## Unsupported Handling

Unsupported behavior must be counted explicitly.

Rules:

```text
unsupported search results increment unsupported_count
invalid target results increment invalid_target_count
limit-exceeded results increment limit_exceeded_count
unsupported cards/actions are aggregated without duplicates
unsupported behavior cannot be silently treated as failure
unsupported behavior cannot be silently treated as success
```

## Acceptance Tests For Phase 13N

Required tests:

```text
batch result is deterministic for same seed/config
game_index_start changes derived seeds
games_completed equals games_requested
success_count and success_rate are correct
failure_count is correct
unsupported_count is correct
invalid_target_count is correct
limit_exceeded_count is correct
average_mulligan_count is calculated
trace samples are deterministic and capped
unsupported cards/actions are aggregated
per-game result includes opening_hand_id and derived_seed
runner uses kept hand after mulligan bottoming
provider/db/analytics/recommendation imports are absent
strategic claim language is absent
no persistence or schema code is added
```

## Do Not Do In Phase 13M

```text
Do not implement the batch runner.
Do not add persistence.
Do not add schema changes.
Do not add Challenge Mode.
Do not add line review.
Do not add UI.
Do not add recommendation output.
Do not call providers, Scryfall, DB, or live network.
Do not copy cEDHData source code or full card catalog data.
```

## Recommended Next Step

```text
Phase 13N - Monte Carlo Batch Runner Implementation
```

Implement the deterministic batch runner described here with focused tests,
full validation, and no persistence or Challenge Mode wiring.
