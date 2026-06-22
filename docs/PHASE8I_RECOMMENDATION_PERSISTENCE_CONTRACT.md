# Phase 8I - Recommendation Persistence And Rebuild Semantics Contract

## Objective

Persist validated in-memory recommendation candidate packets through repository methods.

This phase introduces persistence for:

- recommendation runs
- recommendation candidates
- evidence JSON
- explanation text

It must preserve deterministic rebuild semantics and rollback behavior.

## Scope

Allowed files:

- `codie/db/repositories/recommendations.py`
- `codie/db/repositories/__init__.py`
- `codie/recommendations/persistence.py`
- `codie/recommendations/__init__.py`
- `codie/recommendations/generation.py`
- `tests/test_recommendation_persistence.py`
- `docs/PHASE8I_RECOMMENDATION_PERSISTENCE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes

- `RecommendationRepository`
- `RecommendationRunSpec`
- `PersistedRecommendationRun`
- `recommendation_run_row(...)`
- `recommendation_candidate_row(...)`
- `persist_recommendation_packets(...)`

## Schema Impact

None.

This phase uses existing tables:

- `recommendation_runs`
- `recommendation_candidates`

No table creation or schema migration is allowed.

## Required Behavior

- write recommendation runs through `RecommendationRepository`
- write recommendation candidates through `RecommendationRepository`
- serialize evidence and audit data deterministically
- preserve `scryfall_id` when known
- preserve `oracle_id`
- preserve score component fields supported by the existing schema
- replace prior run/candidates for the same deterministic run key
- rollback all rows when any candidate insert fails
- avoid raw SQL outside `codie/db`

## Deterministic Rebuild Key

For Phase 8I, the rebuild key is:

```text
input_deck_hash + generated_at
```

When a run with the same key is persisted again:

- existing candidates are deleted
- existing run rows for that key are deleted
- a fresh run and candidate set is inserted atomically

Future phases may refine the key after broader user-deck workflows exist.

## Failure Modes

- missing input deck hash raises `ValueError`
- missing generated timestamp raises `ValueError`
- invalid source snapshot ID raises `ValueError`
- invalid candidate card FK rolls back the entire run
- invalid candidate packet remains rejected by upstream packet validators

## Tests

Required tests:

- run row and candidate row mappers preserve config/evidence/scores
- successful persistence writes one run and candidates
- repeated persistence replaces existing rows for the same key
- failed candidate insert rolls back run and candidates
- invalid run spec fails cleanly
- full suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks:

```text
git diff --check
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|execute\(|executescript\(|sqlite3" codie\recommendations
```

## Do Not Do

- do not read provider/source tables
- do not call providers
- do not generate unsupported strategy claims
- do not create UI/export surfaces
- do not add simulator integration
- do not add schema

## Follow-Up

Recommended next packet:

```text
Phase 8J - Innovation snapshot persistence, if needed
```

Alternative next packet:

```text
Phase 9A - report/export surface contract
```
