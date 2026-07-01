# Phase 15C - Deck Memory CLI Contract Report

## Status

```text
Phase 15C: CONTRACT COMPLETE
Implementation: DEFERRED
```

## Scope

Phase 15C defines a narrow local CLI for Phase 15B deck memory.

Contract file:

```text
docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
```

Future implementation files:

```text
codie/cli/user_deck_memory.py
tests/test_cli_user_deck_memory.py
docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
```

## Schema Impact

```text
None.
```

## Contract Decisions

The future CLI should support:

```text
list-deck-memory
show-deck-memory
```

Privacy default:

```text
raw_input is excluded by default
raw_input requires explicit --include-raw-input
```

Output default:

```text
JSON only
stdout for payloads
stderr for compact errors
non-zero exit for failures
```

## Boundary Rules

The future CLI may import:

```text
codie.db.bootstrap
codie.db.repositories.user.UserRepository
codie.user_decks.deck_memory
standard library argparse/json/pathlib
```

The future CLI must not import:

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

## Validation

Documentation-only packet.

Checks run:

```text
git diff --check
```

## Next Packet

```text
Phase 15D - Deck Memory CLI Implementation
```
