# Phase 8J - Innovation Snapshot Persistence Contract

## Objective

Persist innovation detector outputs as reproducible analytics evidence snapshots.

Innovation signals are evidence artifacts. They need stable history so Codie can answer:

- what was flagged on a specific date
- which config produced the signal
- whether a card remained an innovation over time
- which source event/deck IDs supported the signal

## Scope

Allowed files:

- `codie/db/schema/analytics.sql`
- `codie/db/repositories/analytics.py`
- `codie/analytics/innovation/snapshot_persistence.py`
- `codie/analytics/innovation/__init__.py`
- `codie/analytics/__init__.py`
- `docs/SCHEMA_SPEC.md`
- `docs/CODIE_V1_CONSTITUTION.md`
- `tests/test_analytics_innovation_snapshot_persistence.py`
- `tests/test_schema.py`
- `docs/PHASE8J_INNOVATION_SNAPSHOT_PERSISTENCE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes

- `InnovationSnapshotSpec`
- `PersistedInnovationSnapshot`
- `config_json(...)`
- `config_hash(...)`
- `innovation_snapshot_run_row(...)`
- `innovation_snapshot_item_row(...)`
- `persist_innovation_snapshot(...)`
- `AnalyticsRepository.replace_innovation_snapshot(...)`
- `AnalyticsRepository.list_innovation_snapshot_items(...)`

## Schema Impact

Adds two analytics evidence tables:

- `innovation_snapshot_runs`
- `innovation_snapshot_items`

This is an approved post-Phase-1 schema addition because innovation outputs are evidence artifacts requiring provenance and replayability.

## Required Behavior

- persist detector `InnovationSignal` outputs without changing detector behavior
- store generated timestamp, config JSON, and config hash
- store all signal fields required by the innovation model
- preserve source event/deck ID JSON
- preserve `scryfall_id` when known
- preserve `oracle_id`
- atomically replace an existing snapshot for the same `generated_at + config_hash`
- rollback run and item rows if any item insert fails
- keep recommendation tables untouched

## Failure Modes

- missing generated timestamp raises `ValueError`
- missing or empty config raises `ValueError`
- invalid `scryfall_id` foreign key rolls back the snapshot
- duplicate snapshot key replaces prior rows

## Tests

Required tests:

- schema bootstraps new tables
- run/item row mappers preserve all required fields
- snapshot persistence writes run and items
- repeated persistence replaces existing rows for same key
- failed item insert rolls back run and items
- recommendation rows are not created
- full suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks:

```text
git diff --check
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|recommendation_runs|recommendation_candidates|execute\(|executescript\(|sqlite3" codie\analytics
```

## Do Not Do

- do not create recommendation candidates from innovations
- do not read provider/source tables from detector or persistence helpers
- do not add strategic wording
- do not add UI/export surfaces
- do not start simulator integration

## Follow-Up

Recommended next packet:

```text
Phase 9A - Report/Export Surface Contract
```
