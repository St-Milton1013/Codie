# Phase 15F - Deck Memory CLI Usage Documentation Report

## Status

```text
Phase 15F: COMPLETE
Validation: PASS
```

## Scope

Phase 15F adds user-facing documentation for the deck memory CLI.

Files created or modified:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Schema Impact

```text
None.
```

## Code Impact

```text
None.
```

## Guide Coverage

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

## Privacy Coverage

The guide states:

```text
raw_input contains the original imported deck text
raw_input is omitted by default
raw_input appears only when --include-raw-input is provided
raw_input should not be pasted into chats, web tools, or public reports unless intended
```

## Boundary Coverage

The guide states:

```text
user deck memory is local user data
user deck memory is not tournament evidence
the CLI does not generate recommendations
the CLI does not rank cards
the CLI does not call providers
the CLI does not call LLMs
the CLI does not run simulator logic
```

## Validation

Run:

```text
git diff --check
full test suite
strategic language scan over docs/USER_GUIDE_DECK_MEMORY_CLI.md
privacy phrase scan for --include-raw-input and raw_input warnings
```

Results:

```text
git diff --check: PASS
full test suite: Ran 526 tests in 3.223s, OK (skipped=1)
strategic language scan: no matches
privacy phrase scan: raw_input and --include-raw-input warnings present
```

## Next Packet

Recommended:

```text
Phase 15G - Deck Memory Track Checkpoint
```
