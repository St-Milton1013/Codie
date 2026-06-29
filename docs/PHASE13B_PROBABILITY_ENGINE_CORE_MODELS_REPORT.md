# Phase 13B - Probability Engine Core Models Report

## Verdict

```text
Phase 13B Probability Engine Core Models: PASS
```

## Objective

Implement the pure in-memory probability engine model layer needed before
shuffle, mulligan, action execution, target search, or Challenge Mode work.

## Files Created

```text
codie/probability_engine/__init__.py
codie/probability_engine/models.py
tests/test_probability_engine_models.py
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Classes Added

```text
ManaCost
ManaOption
SimulationActionModel
SimulationCardModel
SimulationTargetCondition
SimulationConfig
SimulationDeckCard
SimulationDeck
SimulationUnsupportedItem
SimulationTraceAction
SimulationTrace
SimulationResult
```

## Schema Impact

None.

## Dependency Impact

None.

## Work Completed

- Added pure probability engine dataclasses.
- Added deterministic serialization helpers.
- Added validation for required fields and numeric bounds.
- Added raw reference shape preservation on card models.
- Added unsupported item model for cards/actions/effects.
- Added trace/action models compatible with the cEDHData raw trace fixture.
- Added focused tests for mana, actions, card models, target/config
  reproducibility, unresolved cards, unsupported items, traces, and results.

## Validation Performed

Focused tests:

```text
python -m unittest tests.test_probability_engine_models -v

Ran 12 tests in 0.001s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 331 tests in 2.595s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Boundary scan:

```text
rg -n "codie\.providers|codie\.db|codie\.analytics|codie\.recommendations|sqlite3|requests|httpx" codie\probability_engine
```

returned no matches.

Strategic-language scan:

```text
rg -n "[strategic-claim blocklist]" codie\probability_engine tests\test_probability_engine_models.py docs\PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
```

returned no matches.

Out-of-scope implementation scan:

```text
rg -n "shuffle|mulligan logic|target search|Challenge Mode|Monte Carlo|execute|execution" codie\probability_engine tests\test_probability_engine_models.py
```

returned no matches.

## Boundary Notes

- No simulator execution added.
- No shuffle or mulligan logic added.
- No target search added.
- No Challenge Mode added.
- No schema changes added.
- No cEDHData source code copied.

## Recommended Next Step

```text
Phase 13C - Simulator Card Definition Manager Contract
```

Purpose:

Define the behavior overlay, relevance classification, unsupported-card
reporting, and pending-review workflow before action execution begins.
