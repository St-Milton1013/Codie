# Phase 6 Analytics Foundations Contract

## Objective

Build deterministic tournament analytics from canonical records only.

Phase 6 converts canonical event/deck entries into reproducible weights, card metrics, historical snapshots, regional card metrics, and evidence counts. It must not read provider/source tables directly.

## Files Created

- `codie/analytics/__init__.py`
- `codie/analytics/weights.py`
- `codie/analytics/foundations.py`
- `tests/fixtures/analytics/foundation_cases.json`
- `tests/fixtures/analytics/source-notes.md`
- `tests/test_analytics_foundations.py`

## Files Modified

- `codie/db/repositories/analytics.py`
- `codie/db/repositories/regional.py`
- `tests/test_architecture_boundaries.py`

## Schema Impact

None.

Existing tables used:

- `canonical_events`
- `canonical_decks`
- `canonical_deck_cards`
- `canonical_deck_commanders`
- `event_deck_entries`
- `card_performance_metrics`
- `historical_snapshots`
- `historical_card_metrics`
- `evidence_counts`
- `regional_card_metrics`

## Public API

```python
def event_size_weight(player_count: int | None, *, minimum_player_count: int = 16) -> float: ...
def placement_weight(placement: int | None = None, placement_label: str | None = None) -> float: ...
def recency_weight(event_date: str | None, window_end_date: str, time_window: str) -> float: ...
def source_confidence_weight(source_confidence: float | None) -> float: ...
def decklist_completeness_weight(card_count: int | None) -> float: ...

class AnalyticsFoundationBuilder:
    def build_card_metrics(self, time_window: str, window_end_date: str) -> AnalyticsBuildResult: ...
```

## Dependencies

Allowed:

- `codie.db.repositories.analytics`
- `codie.db.repositories.regional`

Forbidden:

- provider modules
- source repositories
- source tables
- raw provider payloads
- live network calls

## Failure Modes

- `AnalyticsError` for unsupported time windows.
- Ineligible events are skipped, not silently counted.
- Cards missing `oracle_id` are skipped for oracle-level metrics.
- Empty windows produce zero writes and a successful result.

## Acceptance Tests

- event size weights follow the constitution formula.
- placement weights follow exact and fallback rules.
- recency weights follow configured half-life rules.
- analytics queries read canonical tables only.
- duplicate provider/source records do not double-count after canonicalization.
- card performance metrics are generated deterministically.
- historical snapshot and card metrics are generated.
- regional card metrics are generated.
- evidence counts are aggregated.
- metrics preserve time window, window end date, timestamp, and sample size.
