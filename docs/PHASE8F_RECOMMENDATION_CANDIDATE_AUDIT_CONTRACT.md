# Phase 8F Recommendation Candidate Audit Contract

## Objective

Create validation and reporting primitives for scored recommendation candidate drafts.

Phase 8F explains why a candidate draft exists, confirms source attribution, checks ranked eligibility, and rejects unsupported explanation language. It does not persist outputs or turn evidence into strategic coaching.

## Files Created

- `codie/recommendations/reports.py`
- `tests/test_recommendation_candidate_audit.py`
- `docs/PHASE8F_RECOMMENDATION_CANDIDATE_AUDIT_CONTRACT.md`

## Files Modified

- `codie/recommendations/__init__.py`

## Schema Impact

None.

Phase 8F must not write:

- recommendation run rows
- recommendation candidate rows
- canonical records
- source records

## Public API

```python
class CandidateAuditIssue: ...
class CandidateAuditReport: ...

def validate_candidate_explanation_lines(lines) -> tuple[str, ...]: ...
def candidate_explanation_lines(candidate) -> tuple[str, ...]: ...
def build_candidate_audit_report(candidate, *, generated_at: str, minimum_ranked_sample_size: int = 10) -> CandidateAuditReport: ...
```

## Required Report Fields

- entity type
- entity ID
- candidate type
- score
- rank eligibility
- evidence count
- source type counts
- explanation lines
- validation issues
- generated timestamp
- score formula

## Validation Rules

- Every explanation line passes the evidence claim text validator.
- Every explanation line must preserve source attribution.
- Low sample size produces a warning and makes the draft not rank eligible.
- Evidence identity mismatch is an error.
- Report score comes from the scored draft formula.

## Allowed Explanation Style

```text
Card appears in 73% of comparable canonical decks.
Card has lift 2.1 for this commander compared to color baseline.
Source: canonical tournament analytics.
Metric: 0.73 inclusion; sample size 41; confidence 0.68.
```

## Forbidden Explanation Style

```text
This deck should play this card.
This card is required.
Cut this card.
This is strictly better.
```

## Do Not Do

- Do not persist reports.
- Do not create strategic advice.
- Do not summarize primer body text.
- Do not read provider payloads.
- Do not query source tables.
- Do not generate UI.
