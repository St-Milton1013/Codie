# Next Phase Contract

Recommended next task: Phase 15B - Deck Memory Listing And Retrieval Implementation

## Current Status

Phase 14 has passed outside validation.

Phase 15 planning is complete:

```text
docs/PHASE15_PLANNING_CONTRACT.md
docs/PHASE15A_DECK_MEMORY_LISTING_RETRIEVAL_CONTRACT.md
```

## Phase 15 Direction

Start with deck memory over existing user tables before building chat or LLM
features.

Use existing tables first:

```text
user_decks
user_deck_cards
analysis_sessions
saved_analysis
```

Do not add schema in Phase 15B.

## Files Created Or Modified In Latest Packet

```text
docs/PHASE15_PLANNING_CONTRACT.md
docs/PHASE15A_DECK_MEMORY_LISTING_RETRIEVAL_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

## Next Implementation Scope

Phase 15B should add:

```text
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
tests/test_user_deck_memory.py
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
```

## Required Behavior

Implement:

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

The implementation must:

```text
list saved/imported user decks
filter by commander_hash
filter by deck_hash
filter temporary vs persistent deck records
show deck memory detail
include linked saved_analysis summaries
include linked analysis_sessions
include resolved card rows
include raw_input only in detail view
```

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks for Phase 15B:

```text
git diff --check
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py
```

## Known Caveats / Review Notes

- Deck memory is user-local only.
- User decks are not tournament evidence.
- User deck memory must not read source/provider tables.
- Chat UI and LLM features remain deferred.
- Private deck text must not be exported or uploaded without explicit user
  action and a future contract.

## Do Not Do In Phase 15B

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
