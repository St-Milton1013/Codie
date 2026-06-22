# Phase 8D Canonical Observation Input Contract

## Objective

Create a canonical-only input layer for future recommendation and report builders.

Phase 8D does not generate recommendations. It selects already-canonical tournament deck/card observations and maps them into pure recommendation input models.

## Files Created

- `codie/recommendations/observations.py`
- `tests/test_recommendation_observation_inputs.py`
- `docs/PHASE8D_CANONICAL_OBSERVATION_INPUT_CONTRACT.md`

## Files Modified

- `codie/db/repositories/analytics.py`
- `codie/recommendations/__init__.py`

## Schema Impact

None.

Phase 8D must not write:

- recommendation runs
- recommendation candidates
- canonical records
- source records

## Public API

```python
AnalyticsRepository.list_commander_card_observation_rows(...)

def staple_observations_from_canonical_rows(rows) -> tuple[StapleObservation, ...]: ...
```

## Query Inputs

The repository method accepts:

- `commander_hash`
- `window_start_date`
- `window_end_date`
- `placement_scope`
- `include_commanders`

Supported placement scopes:

- `top_16`
- `winners`
- `all`

## Allowed Data Sources

The repository query may read:

- `event_deck_entries`
- `canonical_events`
- `canonical_decks`
- `canonical_deck_cards`
- `canonical_event_sources`
- `canonical_deck_sources`
- `cards`

The recommendation mapper may not read the database directly.

## Output Contract

The mapper emits `StapleObservation` records with:

- event entry identity as observation deck ID
- Oracle ID
- Scryfall ID
- card name
- quantity
- type line
- color identity
- entry weight
- placement
- top cut flag
- winner flag
- event date
- representative deck URL
- representative event URL
- provider
- region
- country

## Failure Modes

- Missing commander hash raises `RepositoryError`.
- Unsupported placement scope raises `RepositoryError`.
- Missing Oracle ID raises `ValueError`.
- Missing Scryfall ID raises `ValueError`.
- Missing card name raises `ValueError`.
- Invalid color identity JSON raises `ValueError`.

## Do Not Do

- Do not generate recommendation candidates.
- Do not persist recommendation runs.
- Do not compute analytics weights.
- Do not query provider payloads.
- Do not query source tables.
- Do not canonicalize.
- Do not create strategic advice.
