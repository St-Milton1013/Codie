# Checkpoint Phase 7 Architecture Audit

## Verdict

```text
Phase 7A Commander Spellbook Combo Evidence Sync: PASS
Phase 7B Moxfield Primer Metadata Sync: PASS
Overall Phase 7 evidence foundation: PASS WITH REVIEW NOTES
```

## Scope

This checkpoint covers the Phase 7 evidence-only layer before recommendation, historical snapshot expansion, or user-facing evidence aggregation work begins.

Included:

- Commander Spellbook combo evidence sync
- Moxfield primer metadata discovery
- Provider boundary enforcement
- Source and curated repository paths
- Evidence count updates
- Commander signature usage for primer matching
- Evidence-only raw metadata compliance

Excluded:

- Recommendation engine
- Strategic card claims
- Primer text summarization
- Historical snapshot generation beyond already-validated Phase 6 foundations
- UI surfaces

## Schema Coverage

Validated existing schema use:

- `source_combos`
- `combos`
- `combo_cards`
- `source_primers`
- `primer_registry`
- `evidence_counts`

No Phase 7B schema changes were introduced.

`primer_registry.primer_url` remains the duplicate boundary for primer records and is enforced with `UNIQUE(primer_url)`.

## Repository Coverage

Phase 7 writes through repositories only:

- `SourceRepository.create_source_combo`
- `SourceRepository.get_source_combo`
- `SourceRepository.create_source_primer`
- `SourceRepository.get_source_primer`
- `CuratedRepository.upsert_combo`
- `CuratedRepository.get_combo`
- `CuratedRepository.add_combo_card`
- `CuratedRepository.list_combo_cards`
- `CuratedRepository.upsert_primer`
- `CuratedRepository.get_primer`
- `AnalyticsRepository.upsert_evidence_count`

Repeated primer syncs update the existing `primer_registry` row instead of creating duplicates.

## Provider Boundaries

Provider packages remain fetch/parse only.

Static boundary checks verify providers do not import:

- `codie.db`
- repositories
- `sqlite3`
- `codie.ingestion`
- `codie.cards`
- `codie.analytics`
- `codie.recommendations`
- `codie.canonical`
- `codie.combos`
- `codie.primers`

Primer sync also does not import providers or recommendations.

## Source Classification

Phase 7A and 7B are evidence sources only.

Commander Spellbook:

- Adds combo evidence.
- Resolves local card identities when available.
- Keeps unresolved combo card evidence without inventing card identity.
- Does not create recommendations or packages.

Moxfield:

- Adds primer metadata evidence.
- Does not create tournament truth.
- Does not create recommendations or packages.
- Does not summarize or store primer body text.

## Commander Signature Usage

Primer registry commander matching now uses the canonical commander signature helper:

```text
single commander:
tymna the weaver

partner pair:
kraum, ludevic's opus|tymna the weaver
```

Validated behavior:

- Exact partner pair match is preserved.
- Reversed partner order produces the same key.
- Single commander does not match partner pair.
- Explicit commander plus partner fields produce the same pair key.

## Evidence-Only Compliance

Moxfield raw metadata is sanitized before persistence.

Validated forbidden content is absent from:

- `source_primers.raw_metadata_json`
- `primer_registry.raw_metadata_json`

Forbidden content includes:

- full primer body
- mulligan guide text
- strategy text
- copied description body

## Ranking Reproducibility

Primer scoring is objective metadata only.

`score_primer_candidate` returns:

- `score`
- `component_breakdown`
- `generated_at`

The persisted `primer_quality_score` is derived from that deterministic score output.

## Tests

Required Phase 7 audit tests now cover:

- primer URL de-duplication
- repeated sync metadata update
- evidence-only storage scan
- exact partner pair matching
- reversed pair order
- single commander mismatch
- missing partner mismatch
- minimal Moxfield metadata drift
- score component breakdown
- provider and sync boundary checks

## Review Notes

Non-blocking notes remain:

- Hareruya WAF challenge handling is retryable, but broad backfill may need a separate access strategy.
- No Git remote is configured yet.
- No CI workflow is configured yet.
- Event dedupe should continue to be watched during broad backfill.

## Phase 8 Gate

Before recommendation work starts, Phase 8 must continue to enforce:

- canonical tables as analytics input
- evidence-only source attribution
- no direct provider reads from analytics
- no strategic claims without supporting evidence
- no primer body storage or summarization
