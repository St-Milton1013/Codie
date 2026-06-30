# Phase 13J - Mulligan Policy Implementation Report

## Verdict

```text
Phase 13J Mulligan Policy Implementation: PASS
```

## Objective

Implement deterministic London mulligan policy evaluation, attempt tracking,
bottoming, and result serialization.

This packet does not add target search, action execution, Monte Carlo batches,
persistence, schema changes, or Challenge Mode.

## Files Created

```text
codie/probability_engine/mulligan.py
tests/test_probability_engine_mulligan.py
tests/fixtures/probability_engine/mulligan/mulligan_deck.txt
docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md
```

## Files Modified

```text
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Classes And Functions Added

```text
MulliganPolicyConfig
MulliganDecision
MulliganStep
MulliganResult
evaluate_opening_hand
select_bottom_cards
simulate_london_mulligan
```

## Schema Impact

None.

## Dependency Impact

None.

The implementation uses only the standard library and existing probability
engine model/shuffle outputs.

## Work Completed

- Added explicit mulligan policy configuration.
- Added keep/reject/forced-keep decision output.
- Added land, mana-source, required-card, and unresolved-card policy checks.
- Added deterministic bottoming with unresolved-first and protected-card rules.
- Added London mulligan attempt tracking.
- Preserved rejected hand steps.
- Added result serialization with kept hand, bottomed cards, steps, unresolved
  cards, and policy metadata.
- Added public exports from `codie.probability_engine`.

## Validation Performed

Focused tests:

```text
python -m unittest tests.test_probability_engine_mulligan -v

Ran 14 tests in 0.008s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 383 tests in 2.696s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Boundary scan:

```text
rg -n "codie\.providers|codie\.db|codie\.analytics|codie\.recommendations|codie\.ingestion|sqlite3|requests|httpx" codie\probability_engine\mulligan.py
```

returned no matches.

Strategic-language scan:

```text
rg -n "[strategic-claim blocklist]" codie\probability_engine\mulligan.py tests\test_probability_engine_mulligan.py
```

returned no matches.

Out-of-scope implementation scan:

```text
rg -n "target search|Challenge Mode|Monte Carlo|execute|execution|Scryfall|sqlite|provider|codie\.db|codie\.analytics|codie\.recommendations" codie\probability_engine\mulligan.py tests\test_probability_engine_mulligan.py
```

returned no matches.

## Boundary Notes

- No target search added.
- No action execution added.
- No Monte Carlo batch runner added.
- No persistence added.
- No schema changes added.
- No Challenge Mode added.
- No live network calls added.
- No cEDHData source code or full card data copied.

## Recommended Next Step

```text
Phase 13K - Target Access Search Contract
```

Define the target access search MVP before implementing game-state exploration
or card action execution.
