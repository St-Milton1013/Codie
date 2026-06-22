# Phase 8B Recommendation Evidence Bundle Contract

## Objective

Create an evidence/provenance bundle model for future recommendation candidates without generating or persisting recommendations.

Phase 8B exists to carry support, attribution, metrics, and reproducibility notes. It does not decide what to recommend.

## Files Created

- `codie/recommendations/evidence.py`
- `tests/test_recommendation_evidence.py`
- `docs/PHASE8B_RECOMMENDATION_EVIDENCE_BUNDLE_CONTRACT.md`

## Files Modified

- `codie/recommendations/__init__.py`
- `tests/test_architecture_boundaries.py`

## Schema Impact

None.

Phase 8B must not write:

- recommendation run rows
- recommendation candidate rows
- canonical records
- source records

## Public API

```python
class EvidenceItem: ...
class EvidenceBundle: ...
class EvidenceStackSummary: ...

def validate_claim_text(text: str) -> str: ...
def build_evidence_bundle(entity_type: str, entity_id: str, items: Iterable[EvidenceItem], generated_at: str) -> EvidenceBundle: ...
def evidence_stack_summary(bundle: EvidenceBundle, *, cap_per_type: int = 10) -> EvidenceStackSummary: ...
```

## Required Evidence Fields

Each `EvidenceItem` includes:

- `claim_type`
- `claim_text`
- `source_type`
- `source_name`
- `source_url` or `source_record_id`
- `metric_value`
- `metric_unit`
- `sample_size`
- `confidence`
- `recency_window`
- `generated_at`
- `reproducibility_notes`

## Allowed Source Types

- tournament
- primer
- combo
- package
- simulation
- analytics
- historical
- regional
- curated

## Forbidden Claim Text

Evidence bundles must reject unsupported strategic language, including:

- "this deck is trying to"
- "the game plan is"
- "this deck should"
- "should play"
- "must include"
- "strictly better"
- "cut this"
- "always include"

## Dependencies

Allowed:

- Python standard library

Forbidden:

- providers
- ingestion
- source repositories
- raw provider/source tables
- raw SQL
- database writes

## Acceptance Tests

- evidence item requires source attribution.
- evidence item rejects unsupported strategy language.
- evidence item validates sample size and confidence.
- bundle requires at least one evidence item.
- bundle preserves source attribution and generated timestamps.
- stack summary counts evidence by source type.
- stack summary volume score is evidence volume only, not an AI score.
- no recommendation rows are created.
- recommendation package boundary test passes.

## Do Not Do

- Do not generate recommendation candidates.
- Do not rank cards.
- Do not persist recommendation runs.
- Do not read provider payloads.
- Do not read source tables.
- Do not summarize primer text.
- Do not create strategic advice.
