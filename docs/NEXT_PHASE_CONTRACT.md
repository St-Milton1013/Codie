# Next Phase Contract

Recommended next task: Phase 13W Reviewed Simulator Accuracy Contract

## Current Status

Phase 13V Challenge Line Review Persistence Implementation is complete.

Codie can now persist Challenge Line Review annotations in
`simulation_line_reviews` through `SimulationRepository` and a probability
engine persistence adapter. Persisted reviews remain annotations over immutable
simulator output; they do not rewrite simulator traces, update analytics, or
generate recommendations.

## Files Created Or Modified In Latest Packet

```text
codie/probability_engine/line_review_persistence.py
tests/test_probability_engine_line_review_persistence.py
docs/PHASE13V_CHALLENGE_LINE_REVIEW_PERSISTENCE_IMPLEMENTATION_REPORT.md
codie/db/schema/simulation.sql
codie/db/schema/indexes.sql
codie/db/repositories/simulation.py
codie/probability_engine/__init__.py
docs/SCHEMA_SPEC.md
tests/test_schema.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
PersistedLineReview
line_review_annotation_to_repository_row(...)
persist_line_review_annotation(...)
line_review_repository_row_to_annotation(...)
```

Repository methods added:

```text
SimulationRepository.upsert_line_review(...)
SimulationRepository.get_line_review(...)
SimulationRepository.list_line_reviews_for_challenge(...)
```

## Schema Impact

Added:

```text
simulation_line_reviews
idx_simulation_line_reviews_challenge_id
idx_simulation_line_reviews_deck_hash
idx_simulation_line_reviews_target_card
idx_simulation_line_reviews_trace_id
idx_simulation_line_reviews_review_status
```

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Focused Phase 13V tests:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest tests.test_probability_engine_line_review_persistence -v
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|requests|httpx" codie\probability_engine\line_review_persistence.py tests\test_probability_engine_line_review_persistence.py
rg -n "codie\.db|SimulationRepository" codie\probability_engine\line_review.py
rg -n "line_review_persistence|SimulationRepository" codie\probability_engine\batch.py codie\probability_engine\search.py codie\probability_engine\challenge_mode.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\line_review_persistence.py tests\test_probability_engine_line_review_persistence.py
```

## Known Caveats / Review Notes

- GitHub remote is configured.
- CLI requires a local Codie database with card rows before deck import can
  resolve cards.
- UI is fixture/static-page-model backed and remains read-only.
- Local report sharing and zip export are implemented.
- Simulator persistence is implemented for batch results.
- Challenge Mode is implemented without UI.
- Challenge Line Review annotations and persistence are implemented.
- Reviewed-accuracy reports remain deferred.
- Final recommendation output remains intentionally separate.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13W - Reviewed Simulator Accuracy Contract
```

Define how persisted line review annotations can be summarized without mutating
raw simulator history:

```text
accepted successful lines
rejected successful lines
reviewed failures
reviewed unsupported results
counts by review_status
counts by review_reason
optional filters by deck_hash, target_card, batch_id, challenge_id
```

Do not implement reporting until the contract defines the output shape,
repository boundaries, and evidence-language restrictions.
