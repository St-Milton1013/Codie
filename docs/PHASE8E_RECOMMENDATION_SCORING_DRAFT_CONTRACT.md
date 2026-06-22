# Phase 8E Recommendation Scoring Draft Contract

## Objective

Create deterministic recommendation candidate scoring primitives without persistence.

Phase 8E calculates the V1 score formula from explicit inputs and attaches an evidence bundle to an in-memory candidate draft. It does not decide deck strategy, mutate data, or store outputs.

## Files Created

- `codie/recommendations/scoring.py`
- `tests/test_recommendation_scoring.py`
- `docs/PHASE8E_RECOMMENDATION_SCORING_DRAFT_CONTRACT.md`

## Files Modified

- `codie/recommendations/__init__.py`

## Schema Impact

None.

Phase 8E must not write:

- recommendation run rows
- recommendation candidate rows
- canonical records
- source records

## Public API

```python
class ScoreComponent: ...
class RecommendationScoreInput: ...
class RecommendationScoreBreakdown: ...
class RecommendationCandidateDraft: ...

def normalize_candidate_type(candidate_type: str) -> str: ...
def low_sample_penalty(sample_size: int, *, threshold: int = 10, penalty: float = 0.25) -> float: ...
def score_recommendation_candidate(score_input: RecommendationScoreInput) -> RecommendationScoreBreakdown: ...
def build_recommendation_candidate_draft(...) -> RecommendationCandidateDraft: ...
```

## Score Formula

```text
recommendation_score =
    commander_lift_score
  + inclusion_rate_score
  + confidence_score
  + similarity_score
  + package_completion_score
  + combo_completion_score
  + tournament_performance_score
  + simulation_delta_score
  - generic_staple_penalty
  - low_sample_penalty
```

## Candidate Types

Supported V1 candidate types:

- `commander_specific`
- `source_label_specific`
- `package_specific`
- `combo_completion`
- `generic_staple`
- `meta_tech`
- `budget_replacement`
- `upgrade_candidate`
- `low_evidence_card`
- `outlier_card`

Hyphenated input is normalized to snake case.

## Dependencies

Allowed:

- recommendation statistics primitives
- evidence bundle primitives
- Python standard library

Forbidden:

- providers
- ingestion
- source repositories
- raw SQL
- database writes
- strategic advice generation

## Failure Modes

- Missing entity identity raises `ValueError`.
- Unsupported candidate type raises `ValueError`.
- Negative score components raise `ValueError`.
- Unit interval score components outside `[0, 1]` raise `ValueError`.
- Evidence bundle identity mismatch raises `ValueError`.
- Sample size must be a non-negative integer.

## Do Not Do

- Do not persist scored drafts.
- Do not create recommendation rows.
- Do not read provider payloads.
- Do not query source tables.
- Do not infer strategy.
