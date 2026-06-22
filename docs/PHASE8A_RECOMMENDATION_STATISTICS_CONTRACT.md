# Phase 8A Recommendation Statistics Contract

## Objective

Create deterministic recommendation statistics primitives without generating recommendations.

Phase 8A builds math helpers only:

- inclusion rates
- weighted inclusion rates
- frequency summaries
- lift
- confidence score and label
- Jaccard similarity
- weighted Jaccard similarity
- generic staple detection

## Files Created

- `codie/recommendations/__init__.py`
- `codie/recommendations/statistics.py`
- `tests/test_recommendation_statistics.py`

## Files Modified

- `tests/test_architecture_boundaries.py`

## Schema Impact

None.

Phase 8A must not write:

- `recommendation_runs`
- `recommendation_candidates`

## Public API

```python
class FrequencyStats: ...
class ConfidenceRating: ...
class GenericStapleProfile: ...

def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float: ...
def safe_rate(numerator: float, denominator: float) -> float | None: ...
def inclusion_rate(included_count: float, total_count: float) -> float | None: ...
def weighted_inclusion_rate(included_weight: float, total_weight: float) -> float | None: ...
def frequency_stats(observed_count: int, total_count: int) -> FrequencyStats: ...
def lift_score(focus_rate: float | None, baseline_rate: float | None, *, cap: float = 5.0) -> float | None: ...
def confidence_rating(sample_size: int, *, low_threshold: int = 10, medium_threshold: int = 30, high_threshold: int = 100) -> ConfidenceRating: ...
def jaccard_similarity(left: Iterable[str], right: Iterable[str]) -> float: ...
def weighted_jaccard_similarity(left: Mapping[str, float], right: Mapping[str, float]) -> float: ...
def generic_staple_profile(...) -> GenericStapleProfile: ...
```

## Dependencies

Allowed:

- Python standard library

Forbidden:

- providers
- ingestion
- source repositories
- raw provider/source tables
- database writes
- recommendation persistence

## Failure Modes

- Negative counts raise `ValueError`.
- Invalid confidence thresholds raise `ValueError`.
- Negative similarity weights raise `ValueError`.
- Zero-denominator rates return `None` rather than inventing data.
- Empty Jaccard inputs return `0.0`.

## Acceptance Tests

- inclusion rates calculate correctly.
- weighted inclusion rates calculate correctly.
- zero denominators return `None`.
- lift calculates and caps deterministically.
- confidence labels follow constitution thresholds.
- Jaccard similarity works over oracle IDs.
- weighted Jaccard uses min/max weights.
- generic staple detection requires broad frequency plus low commander lift.
- unsupported/negative values fail cleanly.
- no recommendation rows are created.
- recommendation package boundary test passes.

## Do Not Do

- Do not generate recommendation candidates.
- Do not persist recommendation runs.
- Do not create strategy explanations.
- Do not read provider payloads.
- Do not read source tables.
- Do not mutate canonical data.
