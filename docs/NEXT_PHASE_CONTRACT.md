# Next Phase Contract

Recommended next task: Phase 13U Challenge Line Review Persistence Contract

## Current Status

Phase 13T Challenge Line Review Implementation is complete.

Codie now has a pure, serializable Challenge Line Review annotation layer for
Challenge Mode simulator lines. Users can accept a simulator line or flag it as
incorrect, unrealistic, unsupported, poorly sequenced, mana-modeling related,
tutor/search related, or other QA concern.

This remains an annotation layer only. It does not rewrite simulator output,
persist review rows, modify challenge results, update analytics, or generate
recommendations.

## Files Created Or Modified In Latest Packet

```text
codie/probability_engine/line_review.py
tests/test_probability_engine_line_review.py
docs/PHASE13T_CHALLENGE_LINE_REVIEW_IMPLEMENTATION_REPORT.md
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

```text
LineReviewStatus
LineReviewReason
LineReviewAnnotation
LineReviewFixture
create_line_review_annotation(...)
reviewed_line_counts_as_success(...)
export_line_review_fixture(...)
serialize_line_review_annotation(...)
```

## Schema Impact

None.

Line review persistence is explicitly deferred.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Focused Phase 13T tests:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest tests.test_probability_engine_line_review -v
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|sqlite3|requests|httpx" codie\probability_engine\line_review.py tests\test_probability_engine_line_review.py
rg -n "line_review|LineReviewAnnotation" codie\probability_engine\batch.py codie\probability_engine\search.py codie\probability_engine\challenge_mode.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" codie\probability_engine\line_review.py tests\test_probability_engine_line_review.py
```

## Known Caveats / Review Notes

- GitHub remote is configured.
- CLI requires a local Codie database with card rows before deck import can
  resolve cards.
- UI is fixture/static-page-model backed and remains read-only.
- Local report sharing and zip export are implemented.
- Simulator persistence is implemented for batch results.
- Challenge Mode is implemented without UI.
- Challenge Line Review is implemented without persistence.
- Line review persistence, UI, reviewed-accuracy reports, and recommendation
  output are not implemented.
- cEDHData reference files remain local research inputs only; do not copy the
  JavaScript bundle or full card catalog into Codie.

## Recommended Next Packet

```text
Phase 13U - Challenge Line Review Persistence Contract
```

Define the storage contract before implementing writes:

```text
simulation_line_reviews
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

Do not add persistence until the contract clarifies repository boundaries,
transaction behavior, uniqueness/idempotency, raw-trace immutability, and
reviewed-accuracy reporting semantics.
