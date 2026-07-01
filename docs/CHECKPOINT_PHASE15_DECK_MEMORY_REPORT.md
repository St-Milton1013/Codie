# Checkpoint - Phase 15 Deck Memory Track

## Status

```text
Phase 15 Deck Memory Track Internal Checkpoint: PASS
Status: Ready for outside validation before Phase 16
```

This is an internal checkpoint, not external proof.

Phase 16 should not start until the outside validation packet returns:

```text
PASS
PASS WITH REVIEW NOTES
```

## Scope Reviewed

Phase 15 covered local deck memory over existing user deck records.

Included packets:

```text
docs/PHASE15_PLANNING_CONTRACT.md
docs/PHASE15A_DECK_MEMORY_LISTING_RETRIEVAL_CONTRACT.md
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT_REPORT.md
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT_REPORT.md
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

Implementation files:

```text
codie/db/repositories/user.py
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
codie/cli/user_deck_memory.py
tests/test_user_deck_memory.py
tests/test_cli_user_deck_memory.py
```

## Schema Impact

```text
None.
```

Phase 15 uses existing tables only:

```text
user_decks
user_deck_cards
analysis_sessions
saved_analysis
```

No schema migration, new table, index, or column was added.

## Phase 15B - Deck Memory Read Layer

Added:

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

Behavior verified:

```text
lists remembered user decks
filters by commander_hash
filters by deck_hash
filters temporary vs persistent records
rejects excluding both temporary and persistent records
filters by created_at window
validates limit
returns deterministic summary ordering
returns raw_input only in detail API
returns imported cards in import order
returns linked saved_analysis metadata
returns linked analysis_sessions
fails cleanly for unknown user_deck_id
```

Ordering:

```text
summaries: updated_at DESC, created_at DESC, user_deck_id DESC
cards: user_deck_card_id ASC
saved analyses: generated_at ASC, saved_analysis_id ASC
analysis sessions: started_at ASC, analysis_session_id ASC
```

## Phase 15D - Deck Memory CLI

Added:

```text
codie/cli/user_deck_memory.py
```

Commands:

```text
list-deck-memory
show-deck-memory
```

Behavior verified:

```text
outputs deterministic JSON
lists remembered deck summaries
shows one remembered deck detail
supports commander_hash filter
supports deck_hash filter
supports temporary/persistent filters
rejects excluding both temporary and persistent records
validates limit
omits raw_input by default
includes raw_input only with --include-raw-input
includes card rows in import order
includes saved analysis metadata
includes analysis sessions
fails cleanly for missing database path
fails cleanly for unknown user_deck_id
```

## Phase 15F - Usage Documentation

Added:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
```

The guide documents:

```text
purpose
privacy warning
database path requirement
list-deck-memory examples
show-deck-memory examples
raw_input behavior
filter examples
JSON output examples
failure examples
what the CLI does not do
```

Privacy documentation confirms:

```text
raw_input contains original imported deck text
raw_input is omitted by default
raw_input appears only with --include-raw-input
raw_input should not be pasted into chats, web tools, or public reports unless intended
```

## Boundary Compliance

Deck memory and deck memory CLI do not import:

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
sqlite3 directly
```

Deck memory and deck memory CLI do not:

```text
read source/provider tables
call providers
call LLMs
run simulator logic
calculate analytics
generate recommendations
create schema
mutate provider/source records
```

Repository SQL added in Phase 15 stays inside:

```text
codie/db/repositories/user.py
```

## Privacy And Evidence Rules

Phase 15 preserves these rules:

```text
user deck memory is local user data
raw_input is private deck text
raw_input is not emitted by CLI default detail output
raw_input requires explicit --include-raw-input
user decks are not source/provider records
user decks are not metagame truth
deck memory does not generate recommendation claims
```

## Validation Evidence

Focused Phase 15B tests:

```text
Ran 13 tests

OK
```

Focused Phase 15D tests:

```text
Ran 12 tests

OK
```

Latest full suite:

```text
Ran 528 tests in 3.452s

OK (skipped=1)
```

Static checks:

```text
git diff --check: PASS
deck_memory forbidden import scan: no matches
deck_memory source/provider table scan: no matches
deck_memory strategic language scan: no matches
deck memory CLI forbidden import scan: no matches
deck memory CLI source/provider table scan: no matches
deck memory CLI strategic language scan: no matches
raw SQL scan for deck_memory/CLI implementation: no matches
mutation-call scan for deck_memory/CLI implementation: no matches
usage guide strategic language scan: no matches
usage guide privacy phrase scan: raw_input and --include-raw-input warnings present
```

## Review Notes

```text
Deck memory is read-only over existing user deck records.
CLI reads existing local SQLite databases and does not create schema.
CLI raw_input output requires explicit opt-in.
No UI exists for deck memory yet.
Interactive chat/LLM features remain deferred.
```

## Internal Verdict

```text
Phase 15: PASS
Ready for outside validation before Phase 16
```
