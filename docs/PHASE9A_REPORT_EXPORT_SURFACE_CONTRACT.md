# Phase 9A - Report/Export Surface Contract

## Objective

Create deterministic export helpers for evidence and recommendation review surfaces.

This phase does not build UI. It prepares stable JSON and Markdown outputs for:

- recommendation runs
- recommendation candidates
- innovation snapshots
- outside-review checkpoint reports

## Scope

Allowed files:

- `codie/exports/__init__.py`
- `codie/exports/reports.py`
- `tests/test_exports_reports.py`
- `docs/PHASE9A_REPORT_EXPORT_SURFACE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes

- `ExportMetadata`
- `export_recommendation_run_json(...)`
- `export_innovation_snapshot_json(...)`
- `recommendation_run_markdown(...)`
- `innovation_snapshot_markdown(...)`
- `outside_review_markdown(...)`

## Inputs

Inputs are repository rows already produced by accepted persistence layers:

- `RecommendationRepository.get_recommendation_run(...)`
- `RecommendationRepository.list_run_candidates(...)`
- `AnalyticsRepository.get_innovation_snapshot_run(...)`
- `AnalyticsRepository.list_innovation_snapshot_items(...)`

## Outputs

- deterministic JSON-compatible dictionaries
- deterministic Markdown strings

## Schema Impact

None.

## Required Behavior

- preserve run IDs and generated timestamps
- preserve config JSON/hash when present
- preserve candidate and innovation evidence JSON
- sort rows deterministically
- include source/evidence IDs already present in persisted rows
- include export metadata
- reject unsupported strategic wording
- perform no persistence
- read no provider/source tables

## Failure Modes

- missing run row raises `ValueError`
- missing export timestamp raises `ValueError`
- unsupported markdown claim text raises `ValueError`

## Tests

Required tests:

- recommendation JSON export includes run and candidates
- innovation JSON export includes snapshot and items
- Markdown export is deterministic
- forbidden strategic wording is rejected
- exports do not create DB rows
- package boundary scan remains clean
- full suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.ingestion|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
```

## Do Not Do

- do not build UI
- do not call providers
- do not read source/provider tables
- do not write DB rows
- do not add schema
- do not add strategic claim language

## Follow-Up

Recommended next packet:

```text
Phase 9B - CLI or file writer wrapper for exports
```

Only after export helpers are accepted should Codie add command-line or UI surfaces.
