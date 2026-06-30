# Next Phase Contract

Recommended next task: Phase 13V Challenge Line Review Persistence Implementation

## Current Status

Phase 13U Challenge Line Review Persistence Contract is documented.

Codie now has a contract for persisting Challenge Line Review annotations as
database rows without rewriting raw simulator traces or turning user reviews
into tournament evidence, analytics, or recommendations.

This latest packet is contract-only. It adds no schema, repository methods,
persistence adapter, UI, reports, or recommendation output.

## Files Created Or Modified In Latest Packet

```text
docs/PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT.md
docs/PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
None. Latest packet is contract-only.
```

## Schema Impact

None in Phase 13U.

Phase 13V may add:

```text
simulation_line_reviews
```

Required columns:

```text
review_id
challenge_id
batch_id
result_id
trace_id
deck_hash
target_card
target_turn
simulator_success
simulator_status
action_trace_json
review_status
review_reason
review_note
affected_cards_json
affected_actions_json
created_at
```

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "simulation_line_reviews|upsert_line_review|line_review_persistence" codie tests
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT.md docs\PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT_REPORT.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

## Known Caveats / Review Notes

- GitHub remote is configured.
- CLI requires a local Codie database with card rows before deck import can
  resolve cards.
- UI is fixture/static-page-model backed and remains read-only.
- Local report sharing and zip export are implemented.
- Simulator persistence is implemented for batch results.
- Challenge Mode is implemented without UI.
- Challenge Line Review annotations are implemented without persistence.
- Phase 13U defines line review persistence but does not implement it.
- Reviewed-accuracy reports remain deferred.
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13V - Challenge Line Review Persistence Implementation
```

Implement:

```text
codie/probability_engine/line_review_persistence.py
tests/test_probability_engine_line_review_persistence.py
docs/PHASE13V_CHALLENGE_LINE_REVIEW_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

Allowed supporting changes:

```text
codie/db/schema/simulation.sql
codie/db/repositories/simulation.py
codie/db/repositories/__init__.py
codie/probability_engine/__init__.py
docs/SCHEMA_SPEC.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Required implementation rules:

```text
review_id is primary persisted identity
upsert by review_id
repeat upsert does not duplicate rows
action_trace_json is copied from annotation
simulation_traces rows are never mutated
line_review.py remains DB-free
repository owns SQL
pure simulator modules stay persistence-free
```
