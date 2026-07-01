# Phase 15E - Deck Memory CLI Usage Documentation Contract Report

## Status

```text
Phase 15E: CONTRACT COMPLETE
Implementation: DEFERRED
```

## Scope

Phase 15E defines the documentation requirements for the Phase 15D deck memory
CLI.

Contract file:

```text
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
```

Future documentation files:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

## Schema Impact

```text
None.
```

## Contract Decisions

The future guide must document:

```text
list-deck-memory
show-deck-memory
database path requirements
filters
JSON output shapes
failure behavior
privacy behavior for raw_input
```

The guide must make clear:

```text
raw_input is omitted by default
raw_input appears only with --include-raw-input
user deck memory is local user data
user deck memory is not tournament evidence
the CLI does not generate recommendations
```

## Validation

Documentation-only contract packet.

Checks to run:

```text
git diff --check
full test suite
```

## Next Packet

```text
Phase 15F - Deck Memory CLI Usage Documentation
```
