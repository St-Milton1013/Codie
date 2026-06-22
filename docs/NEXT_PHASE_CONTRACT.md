# Next Phase Contract

Recommended next task: Phase 8G - Innovation Observation Repository Wiring

## Objective

Connect the analytics innovation detector to canonical database records through repository read methods.

This phase should turn canonical tournament/deck/card rows into `InnovationObservation` objects, then feed them into `detect_innovations`.

It must remain analytics evidence, not recommendation generation.

## Scope

Allowed files:

- `codie/db/repositories/analytics.py`
- `codie/analytics/innovation/`
- `tests/test_analytics_innovation_repository.py`
- `docs/PHASE8G_INNOVATION_REPOSITORY_WIRING_CONTRACT.md`

Optional only if needed:

- `codie/analytics/__init__.py`

## Public Functions / Classes

Expected additions:

```python
AnalyticsRepository.list_innovation_observation_rows(...)
innovation_observations_from_rows(...)
detect_innovations_from_repository(...)
```

Exact names may change if the local code suggests a better pattern, but responsibilities should remain:

- repository reads canonical/analytics data only
- mapper converts rows into `InnovationObservation`
- orchestration calls `detect_innovations`

## Allowed Reads

Repository code may read:

- `canonical_events`
- `canonical_decks`
- `canonical_deck_cards`
- `event_deck_entries`
- `cards`
- `card_performance_metrics`
- `historical_card_metrics`
- `regional_card_metrics`
- `canonical_event_sources`
- `canonical_deck_sources`

## Forbidden Reads

Do not read:

- `source_events`
- `source_decks`
- `source_deck_cards`
- `provider_objects`
- provider raw payload fields
- primer body text

## Schema Impact

None.

Do not create innovation tables yet.

Persistence, caching, and snapshot invalidation are a later explicit phase.

## Required Behavior

The repository wiring must:

- produce `InnovationObservation` records from canonical records
- include `oracle_id`
- include `scryfall_id`
- include source deck/event IDs or canonical deck/event IDs converted to stable strings
- include event date
- include commander hash/signature from canonical deck
- include region/country from canonical event
- include placement, top cut, winner flags
- include player count
- include `cards.released_at`
- support date window inputs
- support minimum event size or allow detector filters to handle it

## Tests

Required tests:

- repository rows map to `InnovationObservation`
- recent top-performing canonical rows feed detector and flag innovation
- historical common card does not flag
- new release adoption uses `cards.released_at`
- regional innovation includes region code
- commander-specific innovation includes commander hash
- source/canonical deck and event IDs are included in evidence output
- no recommendation rows are created
- boundary test still passes
- full suite passes

## Failure Modes

- Missing generated timestamp raises `ValueError`
- Missing required row identity raises `ValueError`
- Invalid date format raises `ValueError`
- Unsupported baseline window raises `ValueError`
- Empty result returns empty tuple, not failure

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static scans must remain clean:

```text
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "from codie\.db|import codie\.db|import sqlite3|from .*repositories|import .*repositories|codie\.ingestion|codie\.cards|codie\.analytics|codie\.recommendations|codie\.canonical|codie\.combos|codie\.primers|codie\.validation" codie\providers
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|recommendation_runs|recommendation_candidates|execute\(|executescript\(|sqlite3" codie\recommendations
```

## Do Not Do

- Do not generate persisted recommendation candidates.
- Do not create recommendation runs.
- Do not persist innovation rows.
- Do not add schema.
- Do not read source/provider tables directly from analytics detector code.
- Do not add strategic wording.

## Follow-Up After Phase 8G

Recommended later slices:

1. Phase 8H - recommendation candidate generation orchestration, still in memory
2. Phase 8I - recommendation persistence and rebuild semantics
3. Phase 8J - innovation snapshot persistence, if needed
4. Phase 9 - exports/UI/report surfaces

Keep each phase separately committed and validated.
