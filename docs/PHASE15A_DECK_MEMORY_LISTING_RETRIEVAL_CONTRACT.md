# Phase 15A - Deck Memory Listing And Retrieval Contract

## Objective

Define read-only deck memory retrieval over existing user deck records.

This phase should make previously imported/analyzed user decks discoverable by
date, deck hash, commander hash, temporary/persistent status, and saved analysis
links.

This is a contract packet. It does not add implementation code, schema, CLI,
UI, LLM calls, or recommendation output.

## Scope

Future implementation files:

```text
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
tests/test_user_deck_memory.py
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE15A_DECK_MEMORY_LISTING_RETRIEVAL_CONTRACT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Existing Tables

Use existing schema:

```text
user_decks
user_deck_cards
analysis_sessions
saved_analysis
```

No schema changes are approved by this contract.

## Public Functions And Classes

Future implementation should add:

```text
DeckMemoryReadError
DeckMemoryFilters
DeckMemorySummary
DeckMemoryCard
DeckMemoryAnalysisSummary
DeckMemorySessionSummary
DeckMemoryDetail
list_deck_memory(...)
get_deck_memory_detail(...)
```

## Inputs

`DeckMemoryFilters` should support:

```text
commander_hash
deck_hash
include_temporary
include_persistent
created_at_from
created_at_to
limit
```

`get_deck_memory_detail(...)` should accept:

```text
user_deck_id
```

## Outputs

`DeckMemorySummary` should include:

```text
user_deck_id
deck_name
source_url
deck_hash
commander_hash
created_at
updated_at
is_temporary
card_count
saved_analysis_count
latest_analysis_generated_at
```

`DeckMemoryDetail` should include:

```text
summary
raw_input
cards
analysis_sessions
saved_analyses
```

`DeckMemoryCard` should include:

```text
raw_name
quantity
zone
scryfall_id
oracle_id
resolution_status
```

`DeckMemoryAnalysisSummary` should include:

```text
saved_analysis_id
analysis_type
generated_at
report_path
deck_hash
```

`DeckMemorySessionSummary` should include:

```text
analysis_session_id
session_type
status
started_at
completed_at
deck_hash
commander_hash
```

## Ordering Rules

List ordering should be deterministic:

```text
updated_at DESC
created_at DESC
user_deck_id DESC
```

Detail card ordering should preserve import order:

```text
user_deck_card_id ASC
```

Saved analysis ordering should match existing saved-analysis behavior:

```text
generated_at ASC
saved_analysis_id ASC
```

## Boundary Rules

Deck memory may import:

```text
codie.db.repositories.user
standard library
```

Deck memory must not import:

```text
codie.providers
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
codie.probability_engine
codie.canonical
requests
httpx
sqlite3
```

Repository raw SQL, if needed, must stay in `codie.db.repositories.user`.

## Evidence Rules

Deck memory records are user-local artifacts.

Allowed wording:

```text
This user deck was imported on X.
This saved analysis is linked to user_deck_id Y.
This deck has commander_hash Z.
This deck has N saved analysis records.
```

Forbidden wording:

```text
This user deck is tournament evidence.
This proves the deck is optimal.
This card should be played.
This card is a required cut.
```

## Failure Modes

Future implementation should raise `DeckMemoryReadError` when:

```text
unknown user_deck_id is requested
filter values are invalid
limit is invalid
stored summary JSON cannot be parsed when detail includes saved analyses
```

## Required Tests For Phase 15B

```text
list deck memory returns deterministic summaries
filter by commander_hash
filter by deck_hash
include/exclude temporary decks
date filters work
limit validation works
detail returns raw_input
detail returns cards in import order
detail returns linked saved analyses
detail returns linked analysis sessions
unknown user_deck_id fails cleanly
deck memory package has no forbidden imports
deck memory does not read provider/source tables
full suite passes
```

## Do Not Do

```text
do not add schema
do not add CLI
do not add UI
do not export private deck text
do not call providers
do not read source/provider tables
do not run simulator
do not calculate recommendations
do not call LLMs
do not treat user decks as tournament evidence
```

## Follow-Up

Recommended next packet:

```text
Phase 15B - Deck Memory Listing And Retrieval Implementation
```
