# Phase 13W - Reviewed Simulator Accuracy Contract

## Purpose

Define reviewed simulator accuracy reporting before implementation.

Phase 13V persists Challenge Line Review annotations. Phase 13X may summarize
those annotations into QA metrics, but those metrics must remain simulator QA
metadata. They must not rewrite raw simulator history, update tournament
evidence, generate recommendations, or become strategic claims.

This is a contract-only packet. It does not add reporting code, schema changes,
UI, recommendation output, analytics writes, or simulator behavior changes.

## Source Documents

```text
docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md
docs/PHASE13S_CHALLENGE_LINE_REVIEW_CONTRACT.md
docs/PHASE13T_CHALLENGE_LINE_REVIEW_IMPLEMENTATION_REPORT.md
docs/PHASE13U_CHALLENGE_LINE_REVIEW_PERSISTENCE_CONTRACT.md
docs/PHASE13V_CHALLENGE_LINE_REVIEW_PERSISTENCE_IMPLEMENTATION_REPORT.md
codie/probability_engine/line_review.py
codie/probability_engine/line_review_persistence.py
codie/db/repositories/simulation.py
```

## Files To Create Or Modify In Phase 13X

Expected files:

```text
codie/probability_engine/reviewed_accuracy.py
tests/test_probability_engine_reviewed_accuracy.py
docs/PHASE13X_REVIEWED_SIMULATOR_ACCURACY_IMPLEMENTATION_REPORT.md
```

Allowed modifications:

```text
codie/db/repositories/simulation.py
codie/probability_engine/__init__.py
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

Do not modify schema unless a separate migration contract is approved.

## Public Classes And Functions To Add

Suggested public API:

```text
ReviewedAccuracyFilters
ReviewedAccuracySummary
ReviewStatusCount
ReviewReasonCount
build_reviewed_accuracy_summary(...)
summarize_line_review_rows(...)
```

Suggested repository method:

```text
SimulationRepository.list_line_reviews_for_accuracy(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None for Phase 13X.

Use the existing table:

```text
simulation_line_reviews
```

No derived accuracy table should be added until report needs, retention rules,
and refresh semantics are separately contracted.

## Dependency Impact

Allowed:

```text
codie.probability_engine.line_review
codie.probability_engine.line_review_persistence
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

`reviewed_accuracy.py` may consume repository rows or `LineReviewAnnotation`
objects. It must not mutate rows or write anything.

## Layer Boundary

Allowed direction:

```text
probability_engine.reviewed_accuracy -> SimulationRepository
```

Forbidden directions:

```text
probability_engine.line_review -> reviewed_accuracy
probability_engine.batch/search/challenge_mode -> reviewed_accuracy
providers -> reviewed_accuracy
analytics -> reviewed_accuracy
recommendations -> reviewed_accuracy
```

Reviewed accuracy is a simulator QA read model, not a simulator engine input.

## Filter Contract

The summary should support optional filters:

```text
deck_hash
target_card
batch_id
challenge_id
trace_id
review_status
review_reason
created_at_from
created_at_to
```

Filters must be explicit. Do not silently infer commander, strategy, archetype,
or tournament context.

## Required Output Fields

`ReviewedAccuracySummary` should include:

```text
total_reviews
reviewed_success_count
accepted_success_count
rejected_success_count
reviewed_failure_count
reviewed_unsupported_count
accepted_failure_count
rejected_failure_count
status_counts
reason_counts
affected_card_counts
affected_action_counts
filters
generated_at
```

Suggested derived rates:

```text
accepted_success_rate
rejected_success_rate
unsupported_rate
```

Rates must be null/None when the denominator is zero.

## Classification Rules

Classification must use stored review and simulator fields only:

```text
simulator_success
simulator_status
review_status
review_reason
```

Rules:

```text
accepted + simulator_success = accepted successful line
non-accepted + simulator_success = rejected successful line
simulator_status == unsupported = reviewed unsupported
not simulator_success and simulator_status != unsupported = reviewed failure
```

The report must preserve both raw simulator status and review status. A rejected
successful line is not a raw simulator failure.

## Evidence-Language Rules

Allowed wording:

```text
3 successful simulator lines were accepted by review.
2 successful simulator lines were rejected by review.
1 reviewed line was marked mana_modeling_error.
4 reviewed traces affected tutor_search actions.
```

Forbidden wording:

```text
The simulator is authoritative.
The simulator made a strategic judgment.
A reviewed line proves a deckbuilding choice.
This review is tournament evidence.
The card choice is solved.
```

Reviewed accuracy is QA evidence about simulator behavior only.

## Required Validation Tests For Phase 13X

```text
accepted successful lines count as accepted_success_count
rejected successful lines count as rejected_success_count
failed simulator lines count as reviewed_failure_count
unsupported simulator lines count as reviewed_unsupported_count
status_counts are generated
reason_counts are generated
affected_card_counts are generated
affected_action_counts are generated
rates are null when denominator is zero
filters by deck_hash
filters by target_card
filters by batch_id
filters by challenge_id
repository query uses parameterized SQL
summary does not mutate simulation_line_reviews
line_review.py remains reviewed-accuracy-free
batch/search/challenge modules remain reviewed-accuracy-free
no provider/analytics/recommendation imports
no strategic claim language
full test suite passes
```

## Do Not Do In Phase 13X

```text
Do not add schema.
Do not build UI.
Do not export Obsidian/Markdown review files yet.
Do not generate recommendations.
Do not write analytics.
Do not treat reviews as tournament evidence.
Do not mutate simulator traces.
Do not modify historical simulator records.
Do not add live network calls.
```

## Recommended Next Step

```text
Phase 13X - Reviewed Simulator Accuracy Implementation
```

Implement the read-only summary model, repository query, tests, and report
defined by this contract.
