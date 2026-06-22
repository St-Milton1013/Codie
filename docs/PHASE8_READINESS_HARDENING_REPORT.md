# Phase 8 Readiness Hardening Report

## Verdict

```text
Phase 8 readiness hardening: PASS
Recommendation engine work: READY WITH CI WORKFLOW ADDED
```

## Purpose

This pass closes the remaining non-blocking governance concerns raised after the Phase 7 architecture audit.

It does not implement recommendations. It adds guardrails so future recommendation work cannot quietly read the wrong inputs or treat derived evidence as authoritative truth.

## Changes

### Explicit Transaction Boundaries

Evidence syncs now run inside explicit SQLite savepoints:

- `ComboEvidenceSync.sync_candidates`
- `PrimerMetadataSync.sync_candidates`

The sync services verify that all write repositories share the same SQLite connection. If a multi-table sync fails after partial writes, the savepoint rolls all Phase 7 writes back together.

Covered failure cases:

- combo source records
- curated combo records
- combo card rows
- primer source records
- primer registry rows
- evidence count rows

### Evidence Count Rebuild Path

`AnalyticsRepository.rebuild_evidence_counts(updated_at=...)` rebuilds `evidence_counts` from durable records:

- canonical tournament deck/card records
- curated combo records
- curated combo card records
- primer registry records
- package registry/card records
- simulation batch result records

The rebuild deletes stale derived rows first, then reconstructs counts deterministically.

### Recommendation Boundary Guard

A future-facing architecture test now enforces that `codie/recommendations/` must not:

- import providers
- import ingestion
- import source repositories
- reference source/provider tables directly
- reference Moxfield or Spellbook provider implementation details directly

Allowed future recommendation inputs remain:

- canonical tables
- analytics tables
- curated registries
- evidence counts

### Canonical Coverage Metrics

Added a validation report path:

- `ValidationRepository.canonical_coverage_counts`
- `build_canonical_coverage_report`

The report exposes:

- source event count
- canonical event count
- canonicalized source event count
- pending source event count
- unresolved source event count
- event source link count
- source deck count
- canonical deck count
- canonicalized source deck count
- pending source deck count
- unresolved source deck count
- deck source link count
- canonicalization rates
- merge rates
- unresolved deck rate

This makes broad backfill health visible before recommendations depend on the dataset.

### CI Workflow

Added:

- `.github/workflows/tests.yml`

The workflow runs:

```text
python -m unittest discover -s tests -v
```

## Non-Goals

This pass does not:

- build recommendation scoring
- create recommendation rows
- read provider payloads
- canonicalize new source data
- calculate new analytics metrics
- change schema

## Phase 8 Gate

Before recommendation code is accepted, tests must continue to prove:

- recommendations never read source/provider tables directly
- recommendations never import provider adapters
- recommendation evidence comes from canonical, analytics, curated, and evidence layers only
- evidence counts can be rebuilt
- canonical coverage can be reported before broad backfill
