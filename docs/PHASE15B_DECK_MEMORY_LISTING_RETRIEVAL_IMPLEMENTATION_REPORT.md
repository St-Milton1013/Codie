# Phase 15B - Deck Memory Listing And Retrieval Implementation Report

## Status

```text
Phase 15B: IMPLEMENTED
Validation: PASS
```

## Scope

Phase 15B added a read-only deck memory layer over existing user-deck tables.

Implemented files:

```text
codie/db/repositories/user.py
codie/user_decks/deck_memory.py
codie/user_decks/__init__.py
tests/test_user_deck_memory.py
docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Schema Impact

```text
None.
```

Phase 15B uses only existing tables:

```text
user_decks
user_deck_cards
analysis_sessions
saved_analysis
```

## Public Interface

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

## Behavior

Implemented:

```text
list remembered user decks
filter by commander_hash
filter by deck_hash
filter temporary vs persistent deck records
filter by created_at window
limit result count
return deterministic summary ordering
return raw_input only in detail view
return imported card rows in import order
return linked saved_analysis summaries
return linked analysis_sessions
raise DeckMemoryReadError for unknown user_deck_id
```

Ordering rules:

```text
list summaries:
updated_at DESC, created_at DESC, user_deck_id DESC

detail cards:
user_deck_card_id ASC

saved analyses:
generated_at ASC, saved_analysis_id ASC

analysis sessions:
started_at ASC, analysis_session_id ASC
```

## Boundary Compliance

Deck memory:

```text
imports codie.db.repositories.user only
does not import providers
does not import analytics
does not import recommendations
does not import ingestion
does not import cards
does not import probability_engine
does not import canonical
does not import requests/httpx
does not import sqlite3
does not read source/provider tables
does not run simulator
does not calculate recommendations
does not export private deck text
```

Raw SQL was added only to:

```text
codie/db/repositories/user.py
```

## Validation

Focused test command:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest tests.test_user_deck_memory -v
```

Result:

```text
Ran 12 tests in 0.040s

OK
```

Full suite command:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Result:

```text
Ran 515 tests in 2.920s

OK (skipped=1)
```

Static checks:

```text
git diff --check: PASS
forbidden deck_memory import scan: no matches
source/provider table scan: no matches
strategic recommendation language scan: no matches
```

## Review Notes

Phase 15B is intentionally local and read-only.

User deck memory is not tournament evidence and must not be used as source truth.

Future CLI/UI/export work must require a separate contract before private deck text is written or shared.
