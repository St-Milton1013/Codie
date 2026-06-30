# Phase 13N - Monte Carlo Batch Runner Implementation Report

## Verdict

```text
Phase 13N Monte Carlo Batch Runner Implementation: PASS
```

## Objective

Implement deterministic Monte Carlo batch execution over seeded games by
connecting shuffle, mulligan policy, and target access search.

This packet does not add persistence, schema changes, Challenge Mode, line
review, UI, or recommendation output.

## Files Created

```text
codie/probability_engine/batch.py
tests/test_probability_engine_batch.py
tests/fixtures/probability_engine/batch/batch_deck.txt
docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md
```

## Files Modified

```text
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Classes And Functions Added

```text
BatchRunConfig
BatchTraceSample
BatchGameResult
BatchRunResult
run_simulation_batch
run_single_simulation_game
summarize_batch_results
```

## Schema Impact

None.

## Dependency Impact

None.

The implementation uses only the standard library and existing probability
engine model, card definition manager, shuffle, mulligan, and search modules.

## Work Completed

- Added deterministic batch configuration.
- Added per-game batch result output.
- Added aggregate batch result output.
- Added deterministic trace sampling for success, failure, and unsupported
  results.
- Added single-game execution flow:
  shuffle, mulligan, post-bottom hand construction, target search, per-game
  result.
- Added batch aggregation for success, failure, unsupported, invalid target,
  and limit-exceeded statuses.
- Added success and unsupported rates as plain ratios.
- Added average mulligan count.
- Added unsupported card/action aggregation.
- Added public exports from `codie.probability_engine`.

## Validation Performed

Focused tests:

```text
python -m unittest tests.test_probability_engine_batch -v

Ran 15 tests in 0.044s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 413 tests in 3.260s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Boundary scan:

```text
rg -n "codie\.providers|codie\.db|codie\.analytics|codie\.recommendations|codie\.ingestion|sqlite3|requests|httpx" codie\probability_engine\batch.py tests\test_probability_engine_batch.py
```

returned no matches.

Strategic-language scan:

```text
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\batch.py tests\test_probability_engine_batch.py
```

returned no matches.

## Boundary Notes

- No persistence added.
- No schema changes added.
- No Challenge Mode added.
- No line review added.
- No UI added.
- No provider, Scryfall, DB, analytics, recommendations, or live network calls
  added.
- No cEDHData source code or full card data copied.

## Recommended Next Step

```text
Phase 13O - Simulator Persistence Contract
```

Define schema/repository boundaries for storing simulator batch results,
individual game metadata, trace samples, unsupported cards/actions, seeds, and
version metadata before adding persistence code.
