# Phase 13U - Challenge Line Review Persistence Contract

## Purpose

Define persistence for Challenge Line Review annotations before implementation.

Phase 13T added pure serializable line review objects. Phase 13V may persist
those annotations, but persistence must remain an annotation layer over immutable
simulator output. It must not rewrite Challenge Mode results, simulator traces,
batch results, analytics, or recommendation outputs.

This is a contract-only packet. It does not add schema changes, persistence
code, UI, reviewed-accuracy reports, recommendation output, or simulator
behavior changes.

## Source Documents

```text
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md
docs/PHASE13T_CHALLENGE_LINE_REVIEW_IMPLEMENTATION_REPORT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
docs/SCHEMA_SPEC.md
docs/DEPENDENCY_RULES.md
codie/probability_engine/line_review.py
codie/db/repositories/simulation.py
codie/db/schema/simulation.sql
```

## Files To Create Or Modify In Phase 13V

Expected files:

```text
codie/probability_engine/line_review_persistence.py
tests/test_probability_engine_line_review_persistence.py
docs/PHASE13V_CHALLENGE_LINE_REVIEW_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

Allowed modifications:

```text
codie/db/schema/simulation.sql
codie/db/repositories/simulation.py
codie/db/repositories/__init__.py
codie/probability_engine/__init__.py
docs/SCHEMA_SPEC.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Do not modify providers, analytics, recommendations, ingestion, cards, user
deck workflow, or UI.

## Public Classes And Functions To Add

Suggested public API:

```text
PersistedLineReview
line_review_annotation_to_repository_row(...)
persist_line_review_annotation(...)
line_review_repository_row_to_annotation(...)
```

Repository methods to add:

```text
SimulationRepository.upsert_line_review(...)
SimulationRepository.get_line_review(...)
SimulationRepository.list_line_reviews_for_challenge(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact For Phase 13V

Phase 13V may add one table:

```text
simulation_line_reviews
```

Required columns:

```text
review_id TEXT PRIMARY KEY
challenge_id TEXT NOT NULL
batch_id TEXT
result_id INTEGER
trace_id INTEGER
deck_hash TEXT NOT NULL
target_card TEXT NOT NULL
target_turn INTEGER NOT NULL
simulator_success INTEGER NOT NULL
simulator_status TEXT NOT NULL
action_trace_json TEXT NOT NULL
review_status TEXT NOT NULL
review_reason TEXT NOT NULL
review_note TEXT
affected_cards_json TEXT NOT NULL
affected_actions_json TEXT NOT NULL
created_at TEXT NOT NULL
```

Required indexes:

```text
idx_simulation_line_reviews_challenge_id
idx_simulation_line_reviews_deck_hash
idx_simulation_line_reviews_target_card
idx_simulation_line_reviews_trace_id
idx_simulation_line_reviews_review_status
```

Recommended foreign keys when referenced rows exist:

```text
FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id)
FOREIGN KEY(result_id) REFERENCES simulation_batch_results(result_id)
FOREIGN KEY(trace_id) REFERENCES simulation_traces(trace_id)
```

Foreign keys must allow `NULL` because Challenge Mode can produce reviewable
results before batch persistence exists.

## Dependency Impact

Allowed:

```text
codie.probability_engine.line_review
codie.probability_engine.challenge_mode
codie.db.repositories.simulation
standard library only
```

Forbidden:

```text
codie.providers
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
requests
httpx
live network calls
raw SQL outside codie/db
```

`codie/probability_engine/line_review.py` must remain DB-free. Add persistence
in a separate adapter module.

## Layer Boundary

Allowed direction:

```text
probability_engine.line_review_persistence -> SimulationRepository
```

Forbidden directions:

```text
probability_engine.line_review -> db/repositories
db/repositories -> probability_engine
providers -> probability_engine.line_review_persistence
analytics -> probability_engine.line_review_persistence
recommendations -> probability_engine.line_review_persistence
```

The review annotation model remains pure. The repository owns SQL. The
persistence adapter maps between the two.

## Persistence Workflow

Phase 13V should persist one `LineReviewAnnotation` in this order:

```text
1. convert annotation to repository row
2. upsert row by review_id
3. return persisted review_id and linkage fields
```

The write must be atomic even if only one table is touched. Use the existing
repository transaction/savepoint pattern.

## Idempotency And Uniqueness

`review_id` is the authoritative persisted identity.

Repeated persistence of the same annotation must:

```text
update the existing row
not create duplicates
preserve review_id
```

Different annotations for the same challenge, trace, or batch may coexist when
they have different `review_id` values. This supports multiple human reviews or
new review notes without rewriting old annotations.

## Raw Trace Immutability

Persistence must copy the annotation's `action_trace` into
`action_trace_json`.

It must not:

```text
update simulation_traces.action_trace_json
update simulation_batch_results.raw_payload_json
update simulation_batches.raw_config_json
update ChallengeResult
delete simulator traces
delete batch results
```

Line review rows are annotations over simulator output, not replacements for
simulator output.

## Reviewed Accuracy Semantics

Persistence may store enough data for later reviewed-accuracy reports, but Phase
13V must not implement reporting unless separately contracted.

Stored rows must preserve:

```text
simulator_success
simulator_status
review_status
review_reason
```

Later reviewed-accuracy code may interpret:

```text
accepted + simulator_success = reviewed success
rejected + simulator_success = reviewed rejected success
unsupported simulator_status = reviewed unsupported
failed simulator_success = reviewed failure
```

Raw simulator success/failure history must remain unchanged.

## Required Validation Tests For Phase 13V

```text
schema contains simulation_line_reviews
schema contains required indexes
repository upserts line review
repeated upsert does not duplicate row
get_line_review returns stored row
list_line_reviews_for_challenge filters by challenge_id
JSON fields round trip
annotation maps to repository row
repository row maps back to annotation
foreign keys allow nullable linkage
linked batch/result/trace review persists when referenced rows exist
invalid missing required fields fail cleanly
rollback leaves no partial review row after repository failure
line_review.py remains DB-free
batch/search/challenge modules remain line-review-persistence-free
no provider/analytics/recommendation imports
no strategic claim language
full test suite passes
```

## Do Not Do In Phase 13V

```text
Do not build UI.
Do not build reviewed-accuracy reports.
Do not generate recommendations.
Do not write analytics.
Do not treat user review as tournament evidence.
Do not mutate simulator traces.
Do not modify historical simulator records.
Do not add live network calls.
```

## Recommended Next Step

```text
Phase 13V - Challenge Line Review Persistence Implementation
```

Implement the table, repository methods, persistence adapter, tests, and report
defined by this contract.
