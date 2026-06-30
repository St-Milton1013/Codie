# Phase 13P - Simulator Persistence Implementation Report

## Verdict

```text
Phase 13P Simulator Persistence Implementation: PASS
```

## Objective

Implement a persistence adapter for Phase 13N batch results using existing
simulator tables and `SimulationRepository`.

This packet does not add schema changes, evidence stack writes, analytics
writes, recommendation output, Challenge Mode, line review, or UI.

## Files Created

```text
codie/probability_engine/persistence.py
tests/test_probability_engine_persistence.py
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

## Files Modified

```text
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Classes And Functions Added

```text
PersistedSimulationBatch
persist_batch_run_result
batch_result_to_repository_rows
trace_sample_to_repository_row
deterministic_batch_id
```

## Schema Impact

None.

The implementation uses existing tables:

```text
simulation_batches
simulation_batch_results
simulation_traces
```

## Dependency Impact

`codie.probability_engine.persistence` imports:

```text
codie.db.repositories.simulation.SimulationRepository
```

The pure simulator modules remain DB-free.

## Work Completed

- Added deterministic batch ID generation.
- Added batch/result/trace row mapping.
- Preserved seed, batch config, search config, mulligan policy, target, and
  version metadata in existing JSON fields.
- Persisted batch, aggregate result, and trace sample rows through
  `SimulationRepository`.
- Added savepoint atomicity around batch/result/trace writes.
- Added rollback coverage for result persistence failure.
- Added rollback coverage for trace persistence failure.
- Verified no evidence_counts, analytics, or recommendation rows are written.
- Exported persistence adapter functions from `codie.probability_engine`.

## Validation Performed

Focused tests:

```text
python -m unittest tests.test_probability_engine_persistence -v

Ran 10 tests in 0.055s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 423 tests in 2.541s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Forbidden dependency scan:

```text
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx" codie\probability_engine\persistence.py tests\test_probability_engine_persistence.py
```

returned no matches.

Pure simulator DB boundary scan:

```text
rg -n "codie\.db|SimulationRepository" codie\probability_engine\batch.py codie\probability_engine\search.py codie\probability_engine\mulligan.py
```

returned no matches.

Strategic-language scan:

```text
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\persistence.py tests\test_probability_engine_persistence.py
```

returned no matches.

## Boundary Notes

- No schema changes added.
- No evidence_counts writes added.
- No analytics writes added.
- No recommendation writes added.
- No Challenge Mode added.
- No line review added.
- No UI added.
- No provider, Scryfall, or live network calls added.

## Recommended Next Step

```text
Phase 13Q - Challenge Mode Contract
```

Define generated challenge hands, exact-hand simulator verification, unsupported
card disclosure, stored seeds/config, and no-recommendation boundaries before
implementing Challenge Mode.
