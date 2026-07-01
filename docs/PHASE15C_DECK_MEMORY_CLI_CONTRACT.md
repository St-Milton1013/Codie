# Phase 15C - Deck Memory CLI Contract

## Objective

Define a narrow command-line interface for reading remembered user decks created
by Phase 15B.

The CLI should make local deck memory usable from the terminal without adding
new schema, UI, LLM calls, simulator execution, provider reads, source-table
reads, analytics writes, or recommendation output.

This is a contract packet. It adds no implementation code.

## Scope

Future implementation files:

```text
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Dependencies

The CLI may use:

```text
codie.db.bootstrap
codie.db.repositories.user.UserRepository
codie.user_decks.deck_memory
standard library argparse/json/pathlib
```

The CLI must not import:

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

SQLite access must happen through existing bootstrap/repository paths.

## Public CLI Commands

Future implementation should add a local CLI module with these commands:

```text
list-deck-memory
show-deck-memory
```

The command surface should be callable by tests without installing a console
script.

Suggested callable functions:

```text
build_parser()
main(argv=None)
run_list_deck_memory(args)
run_show_deck_memory(args)
```

## Common Inputs

Both commands should require:

```text
--db PATH
```

`--db` points to the local Codie SQLite database.

The CLI must not create or mutate the database. It should fail cleanly if the
database path is missing or unreadable.

## list-deck-memory

Required behavior:

```text
list remembered user deck summaries
output deterministic JSON to stdout
do not include raw_input
do not include full card list
do not include saved analysis summary_json
```

Supported filters:

```text
--commander-hash TEXT
--deck-hash TEXT
--include-temporary / --exclude-temporary
--include-persistent / --exclude-persistent
--created-at-from TEXT
--created-at-to TEXT
--limit INTEGER
```

Default behavior:

```text
include temporary decks
include persistent decks
limit 50
JSON output only
```

Output shape:

```json
{
  "decks": [
    {
      "user_deck_id": 1,
      "deck_name": "Example",
      "source_url": "https://example.test/deck",
      "deck_hash": "deck-hash",
      "commander_hash": "commander-hash",
      "created_at": "2026-07-01T00:00:00+00:00",
      "updated_at": "2026-07-01T00:00:00+00:00",
      "is_temporary": false,
      "card_count": 100,
      "saved_analysis_count": 2,
      "latest_analysis_generated_at": "2026-07-01T01:00:00+00:00"
    }
  ]
}
```

## show-deck-memory

Required behavior:

```text
show one remembered user deck detail
output deterministic JSON to stdout
include imported card rows
include linked analysis sessions
include linked saved analysis metadata
exclude raw_input by default
```

Required input:

```text
--user-deck-id INTEGER
```

Optional input:

```text
--include-raw-input
```

Privacy rule:

```text
raw_input must be omitted unless --include-raw-input is explicitly provided
```

Output shape without raw input:

```json
{
  "deck": {
    "summary": {},
    "cards": [],
    "analysis_sessions": [],
    "saved_analyses": []
  }
}
```

Output shape with raw input:

```json
{
  "deck": {
    "summary": {},
    "raw_input": "1 Card Name",
    "cards": [],
    "analysis_sessions": [],
    "saved_analyses": []
  }
}
```

## Serialization Rules

CLI output must be:

```text
JSON only
UTF-8 safe
deterministically sorted where dictionaries are produced
newline-terminated
free of strategic recommendation language
```

The CLI should not print human prose except for argparse usage/errors.

## Failure Modes

The CLI should fail non-zero and print a compact error to stderr when:

```text
--db is missing
database path does not exist
database path is unreadable
user_deck_id is unknown
limit is invalid
both temporary and persistent deck records are excluded
created_at_from is later than created_at_to
JSON serialization fails
```

Unknown deck-memory read failures should map from:

```text
DeckMemoryReadError
```

## Privacy And Evidence Rules

Deck memory records are user-local artifacts.

Allowed wording in future docs/tests:

```text
remembered user deck
linked saved analysis
imported card row
analysis session metadata
```

Forbidden behavior:

```text
do not treat user decks as tournament evidence
do not generate recommendations
do not say a card should be played or cut
do not upload private deck text
do not export raw_input by default
do not read source/provider tables
```

## Required Tests For Future Phase 15D

```text
list command prints deterministic JSON summaries
list command omits raw_input
list filters by commander_hash
list filters by deck_hash
list include/exclude temporary flags work
list validates limit
show command prints deck detail
show command omits raw_input by default
show command includes raw_input only with explicit flag
show command includes card rows in import order
show command includes saved analysis metadata
show command includes analysis sessions
unknown user_deck_id exits cleanly
missing database path exits cleanly
CLI module has no forbidden imports
CLI output contains no recommendation language
full suite passes
```

## Do Not Do In Phase 15C

```text
do not implement CLI code
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

## Recommended Next Packet

```text
Phase 15D - Deck Memory CLI Implementation
```
