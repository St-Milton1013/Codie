# Next Phase Contract

Recommended next task: Phase 9A - Report/Export Surface Contract

## Current Status

Phase 8G, Phase 8H, Phase 8I, and Phase 8J are locally implemented and validated.

Phase 8J added persistent innovation snapshots. Innovation detector outputs are now stored as reproducible analytics evidence snapshots with stable run/item rows, deterministic config hashes, and atomic rebuild semantics.

## Files Created Or Modified In Latest Packet

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

## Public Functions / Classes Added

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

Adds analytics evidence tables:

- `innovation_snapshot_runs`
- `innovation_snapshot_items`

This was approved because innovation outputs are evidence artifacts requiring provenance and replayability.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|recommendation_runs|recommendation_candidates|execute\(|executescript\(|sqlite3" codie\analytics
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- Phase 8J added schema; outside review should verify the tables are appropriate before broad deployment.
- No UI exists yet.

## Recommended Next Packet

Phase 9A - Report/Export Surface Contract.

## Phase 9A Objective

Define export surfaces for the evidence and recommendation layers before building UI.

Likely outputs:

- JSON export for recommendation runs and candidates
- JSON export for innovation snapshots
- Markdown report export for outside review
- deterministic ordering and generated metadata

## Phase 9A Scope

Recommended initial scope:

- contract document only or narrow exporter implementation
- no web UI
- no live provider calls
- no new schema unless explicitly justified

## Do Not Do

- Do not build UI before export contracts are defined.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.

## Required Phase Packet Shape

Every follow-up phase packet must include:

- contract document before code
- complete implementation files
- focused tests and fixture data where relevant
- full validation command and actual output
- static architecture checks where relevant
- completion report
- updated handoff or next-phase document
- clean commit after validation passes

Use this packet order:

```text
contract -> code -> tests -> validation -> completion report -> handoff -> commit
```
