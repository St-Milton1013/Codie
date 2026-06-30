# Phase 13S - Challenge Line Review Contract

## Purpose

Define Challenge Line Review before implementation.

Challenge Line Review lets users annotate simulator-generated lines from
Challenge Mode. The user can accept a line or flag it as incorrect,
unrealistic, unsupported, poorly sequenced, or otherwise problematic.

This is a simulator QA annotation layer. It does not rewrite simulator output.

This is a contract-only packet. It does not add line review code, schema
changes, persistence, UI, regression export, recommendation output, or simulator
behavior changes.

## Source Documents

```text
docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md
docs/PHASE13Q_CHALLENGE_MODE_CONTRACT.md
docs/PHASE13R_CHALLENGE_MODE_IMPLEMENTATION_REPORT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

## Files To Create In Phase 13T

```text
codie/probability_engine/line_review.py
tests/test_probability_engine_line_review.py
docs/PHASE13T_CHALLENGE_LINE_REVIEW_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

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

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None for Phase 13T.

Line review persistence is deferred. Phase 13T should return serializable
objects only.

Potential future table:

```text
simulation_line_reviews
```

Suggested future fields:

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
action_trace_json
review_status
review_reason
review_note
affected_cards_json
affected_actions_json
created_at
```

Do not add this table in Phase 13T unless a separate migration contract is
approved.

## Dependency Impact

Allowed:

```text
codie.probability_engine.challenge_mode
standard library only
```

Optional:

```text
codie.probability_engine.search
```

Forbidden:

```text
codie.providers
codie.db
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
sqlite3
requests
httpx
live network calls
```

Line Review must not import persistence in Phase 13T. Persistence is a later
opt-in layer.

## Annotation Boundary

Line review creates an annotation over simulator output.

It must not:

```text
rewrite ChallengeResult
delete ChallengeResult
modify simulator_trace
modify historical simulation records
change target access search output
change batch results
change persisted simulation rows
```

It may:

```text
store review status
store review reason
store review note
record affected cards
record affected action types
export a regression fixture payload
exclude rejected lines from reviewed-accuracy reporting
```

## Review Statuses

Allowed statuses:

```text
accepted
incorrect
unrealistic
unsupported_card_behavior
bad_sequencing
mana_modeling_error
tutor_search_error
other
```

`accepted` means the user reviewed the line and did not flag a modeling issue.

All other statuses are veto/rejection statuses for reviewed accuracy reporting.

## Review Reasons

Suggested reason codes:

```text
line_valid
illegal_action
unsupported_card_behavior
impractical_sequence
mana_pool_error
mana_source_error
tutor_target_error
search_zone_error
missing_cost
wrong_timing
unknown_issue
```

Reason codes must remain descriptive QA metadata. They must not become
recommendation evidence or tournament evidence.

## Required Annotation Fields

Required fields:

```text
review_id
challenge_id
deck_hash
target_card
target_turn
simulator_success
simulator_status
action_trace
review_status
review_reason
review_note
affected_cards
affected_actions
created_at
```

Optional source linkage:

```text
batch_id
result_id
trace_id
```

`review_id` should be deterministic for identical annotation payloads unless a
caller-supplied ID is provided.

Use a `sha256:` prefix.

## Reviewed Accuracy Rules

Raw simulator history is immutable.

Reviewed accuracy reporting may count:

```text
accepted successful line -> reviewed success
rejected successful line -> reviewed rejected success
failed simulator result -> reviewed failure
unsupported simulator result -> reviewed unsupported
```

Rejected lines must not silently become failures in the raw simulator history.

## Regression Fixture Export

Line review may export a serializable regression fixture.

Required fixture fields:

```text
review_id
challenge_id
deck_hash
target_condition
opening_hand
simulator_status
simulator_success
action_trace
review_status
review_reason
affected_cards
affected_actions
created_at
```

Exporting a fixture must not mutate the annotation or original result.

## Evidence Boundary

Line review is QA evidence for simulator behavior.

It is not:

```text
tournament evidence
recommendation evidence
card performance evidence
deck performance evidence
```

Phase 13T must not:

```text
write evidence_counts
write analytics tables
write recommendation tables
change canonical tables
change source/provider records
```

## Acceptance Tests For Phase 13T

Required tests:

```text
user can accept a simulator line
user can veto a simulator line
veto stores status, reason, and note
affected cards are preserved
affected actions are preserved
original challenge result remains unchanged
original simulator trace remains unchanged
accepted line counts as reviewed success
rejected successful line does not count as reviewed success
unsupported line remains reviewed unsupported
reviewed rejected line can be exported as regression fixture
review annotation has deterministic ID
line review has no DB/provider/analytics/recommendation imports
challenge/search/batch modules remain line-review-free
no strategic claim language is generated
```

## Do Not Do In Phase 13S

```text
Do not implement line review.
Do not add schema changes.
Do not persist line reviews.
Do not add UI.
Do not add recommendation output.
Do not mutate ChallengeResult or simulator traces.
Do not update evidence_counts.
Do not call providers, Scryfall, DB, or network.
```

## Recommended Next Step

```text
Phase 13T - Challenge Line Review Implementation
```

Implement serializable line review annotations and regression fixture export,
with no persistence, schema changes, UI, or simulator-result mutation.
