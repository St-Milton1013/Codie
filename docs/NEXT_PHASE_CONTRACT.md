# Next Phase Contract

Recommended next task: Phase 15G - Deck Memory Track Checkpoint

## Current Status

Phase 14 has passed outside validation.

Phase 15B deck memory listing and retrieval is implemented.

Phase 15C deck memory CLI contract is complete.

Phase 15D deck memory CLI implementation is complete.

Phase 15E deck memory CLI usage documentation contract is complete.

Phase 15F deck memory CLI usage documentation is complete.

Phase 15 planning is complete:

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
codie/db/repositories/user.py
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
tests/test_user_deck_memory.py
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT_REPORT.md
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT_REPORT.md
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

## Completed Phase 15B Scope

Phase 15B added:

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

The implementation:

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

## Completed Phase 15C Scope

Phase 15C defined the contract for:

```text
Deck Memory CLI Contract
```

Required future CLI behavior:

```text
list remembered decks
show one remembered deck detail
filter by commander_hash
filter by deck_hash
include/exclude temporary decks
output JSON only by default
do not export raw_input unless explicitly requested
```

## Completed Phase 15D Scope

Phase 15D added:

```text
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
```

Commands:

```text
list-deck-memory
show-deck-memory
```

Phase 15D behavior:

```text
list remembered deck summaries as JSON
show one remembered deck detail as JSON
omit raw_input by default
include raw_input only with --include-raw-input
fail cleanly for missing database paths
fail cleanly for unknown user_deck_id
```

## Completed Phase 15E Scope

Phase 15E defined the contract for:

```text
Deck Memory CLI Usage Documentation Contract
```

Required future documentation:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

The usage guide should explain:

```text
how to list remembered decks
how to show a remembered deck
privacy warning for --include-raw-input
JSON output examples
that user deck memory is not tournament evidence
that CLI does not generate recommendations
```

## Completed Phase 15F Scope

Phase 15F added:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

Phase 15F must document:

```text
list-deck-memory usage
show-deck-memory usage
privacy warning for --include-raw-input
JSON examples using synthetic data only
failure behavior
that user deck memory is local user data
that user deck memory is not tournament evidence
that no recommendations are generated
```

## Next Checkpoint Scope

Phase 15G should create:

```text
docs/CHECKPOINT_PHASE15_DECK_MEMORY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE15_DECK_MEMORY_PROMPT.md
```

The checkpoint should cover:

```text
Phase 15 planning
Phase 15B deck memory read layer
Phase 15D deck memory CLI
Phase 15F usage documentation
privacy defaults
no schema changes
no provider/source reads
no recommendations
full test output
boundary scans
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

Static checks for Phase 15D:

```text
git diff --check
rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py
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

## Do Not Do In Phase 15C Contract

```text
do not implement CLI code until the contract is accepted
do not add schema
do not add UI
do not call LLMs
do not export private deck text by default
do not generate recommendations
```

## Do Not Do In Phase 15D

```text
do not add schema
do not add UI
do not call LLMs
do not call providers
do not read source/provider tables
do not run simulator
do not calculate analytics
do not generate recommendations
do not export private deck text by default
```

## Do Not Do In Phase 15E Contract

```text
do not implement new code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
do not tell users to upload or share raw deck text
```

## Do Not Do In Phase 15F

```text
do not add code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
do not include real private deck text in examples
do not tell users to upload or share raw deck text
```

## Do Not Do In Phase 15G

```text
do not add code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
do not weaken raw_input privacy defaults
```
