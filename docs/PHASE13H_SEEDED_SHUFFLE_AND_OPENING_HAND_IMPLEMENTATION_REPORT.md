# Phase 13H - Seeded Shuffle And Opening Hand Implementation Report

## Verdict

```text
Phase 13H Seeded Shuffle And Opening Hand Implementation: PASS
```

## Objective

Implement deterministic library expansion, seeded shuffle, opening-hand drawing,
and hand identity.

This packet does not add mulligan policy, target search, action execution,
Monte Carlo batches, persistence, schema changes, or Challenge Mode.

## Files Created

```text
codie/probability_engine/shuffle.py
tests/test_probability_engine_shuffle.py
tests/fixtures/probability_engine/shuffle/opening_hand_deck.txt
docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md
```

## Files Modified

```text
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Classes And Functions Added

```text
ExpandedLibraryCard
ExpandedLibrary
OpeningHand
ShuffleResult
expand_library
derive_game_seed
shuffle_library
draw_opening_hand
opening_hand_id
```

## Schema Impact

None.

## Dependency Impact

None.

The implementation uses only the standard library and existing probability
engine models/parser outputs.

## Algorithm Note

Seed derivation:

```text
sha256:<deck_hash>|<base_seed>|<game_index>|<shuffle_algorithm_version>
```

The SHA-256 hex digest is converted to an integer and used to initialize a
local `random.Random` instance. The implementation does not call
`random.seed()` and does not mutate global random state.

## Work Completed

- Added physical library expansion by card quantity.
- Excluded command-zone rows from the library.
- Preserved unresolved main-deck cards in expanded library and hand metadata.
- Added deterministic game seed derivation.
- Added deterministic local-PRNG shuffle.
- Added opening-hand draw from the first N shuffled cards.
- Added deterministic, order-sensitive opening-hand IDs.
- Added public exports from `codie.probability_engine`.

## Validation Performed

Focused tests:

```text
python -m unittest tests.test_probability_engine_shuffle -v

Ran 14 tests in 0.006s

OK
```

Full suite:

```text
python -m unittest discover -s tests

Ran 369 tests in 2.454s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Boundary scan:

```text
rg -n "codie\.providers|codie\.db|codie\.analytics|codie\.recommendations|codie\.ingestion|sqlite3|requests|httpx" codie\probability_engine\shuffle.py
```

returned no matches.

Strategic-language scan:

```text
rg -n "[strategic-claim blocklist]" codie\probability_engine\shuffle.py tests\test_probability_engine_shuffle.py
```

returned no matches.

Out-of-scope implementation scan:

```text
rg -n "mulligan policy|target search|Challenge Mode|Monte Carlo|execute|execution|Scryfall|sqlite|provider|codie\.db|codie\.analytics|codie\.recommendations" codie\probability_engine\shuffle.py tests\test_probability_engine_shuffle.py
```

returned no matches.

## Boundary Notes

- No mulligan policy added.
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
Phase 13I - Mulligan Policy Contract
```

Define London mulligan policy inputs, keep/reject decision boundaries, trace
metadata, and allowed policy outputs before implementation.
