# Phase 15D - Deck Memory CLI Implementation Report

## Status

```text
Phase 15D: IMPLEMENTED
Validation: PASS
```

## Scope

Implemented the local read-only deck memory CLI defined by Phase 15C.

Files created or modified:

```text
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Schema Impact

```text
None.
```

## Public CLI Commands

Added:

```text
list-deck-memory
show-deck-memory
```

Command module:

```text
codie/cli/user_deck_memory.py
```

Callable functions:

```text
build_parser()
main(argv=None)
run_list_deck_memory(args)
run_show_deck_memory(args)
```

## Behavior

Implemented:

```text
list remembered deck summaries as deterministic JSON
filter by commander_hash
filter by deck_hash
include/exclude temporary deck records
include/exclude persistent deck records
filter by created_at window
validate limit through DeckMemoryFilters
show one remembered deck detail as deterministic JSON
include cards in import order
include saved analysis metadata
include analysis session metadata
omit raw_input by default
include raw_input only with --include-raw-input
fail cleanly for missing database paths
fail cleanly for unknown user_deck_id
```

## Privacy Rules

The CLI does not export raw deck text by default.

Private `raw_input` appears only when:

```text
--include-raw-input
```

is explicitly supplied to:

```text
show-deck-memory
```

## Boundary Compliance

The CLI uses:

```text
codie.db.connection.connect
codie.db.repositories.user.UserRepository
codie.user_decks.deck_memory
standard library argparse/json/pathlib/sys/dataclasses
```

The CLI does not import:

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

The CLI does not:

```text
create schema
mutate user records
read source/provider tables
run simulator
call LLMs
calculate analytics
generate recommendations
```

## Validation

Focused command:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest tests.test_cli_user_deck_memory -v
```

Result:

```text
Ran 11 tests in 0.176s

OK
```

Full suite command:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Result:

```text
Ran 526 tests in 3.075s

OK (skipped=1)
```

Static checks:

```text
git diff --check: PASS
forbidden CLI import scan: no matches
source/provider table scan: no matches
strategic recommendation language scan: no matches
```

## Review Notes

The CLI is intentionally local and read-only.

User deck memory remains user-local state, not tournament evidence.

Future documentation should explain that `--include-raw-input` may expose private
deck text and should be used deliberately.
