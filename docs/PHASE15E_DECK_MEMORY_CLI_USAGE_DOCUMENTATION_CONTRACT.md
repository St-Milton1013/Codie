# Phase 15E - Deck Memory CLI Usage Documentation Contract

## Objective

Define user-facing documentation for the Phase 15D deck memory CLI.

The documentation should make the CLI usable without adding new code, schema,
UI, provider access, simulator execution, LLM calls, analytics, or
recommendations.

This is a contract packet. It adds no implementation documentation beyond this
contract.

## Scope

Future documentation files:

```text
docs/USER_GUIDE_DECK_MEMORY_CLI.md
docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
```

Current contract files:

```text
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Documentation Sections

The future guide should include:

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

## Required Commands To Document

```text
list-deck-memory
show-deck-memory
```

## Required Privacy Warning

The guide must clearly state:

```text
raw_input contains the original imported deck text
raw_input is omitted by default
raw_input appears only when --include-raw-input is provided
do not paste raw_input into chats, web tools, or public reports unless intended
```

## Required Evidence Boundaries

The guide must state:

```text
user deck memory is local user data
user deck memory is not tournament evidence
the CLI does not generate recommendations
the CLI does not rank cards
the CLI does not call providers
the CLI does not call LLMs
the CLI does not run simulator logic
```

## Required Examples

List all remembered decks:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite
```

Filter by commander hash:

```powershell
python -m codie.cli.user_deck_memory list-deck-memory --db .\codie.sqlite --commander-hash "tymna|kraum"
```

Show one deck without raw input:

```powershell
python -m codie.cli.user_deck_memory show-deck-memory --db .\codie.sqlite --user-deck-id 1
```

Show one deck with raw input:

```powershell
python -m codie.cli.user_deck_memory show-deck-memory --db .\codie.sqlite --user-deck-id 1 --include-raw-input
```

## Output Shape Requirements

The guide should show compact examples for:

```text
list response
show response without raw_input
show response with raw_input
error response behavior
```

Examples must be synthetic and must not include real private deck text.

## Failure Documentation

The guide should explain:

```text
missing database path
unknown user_deck_id
invalid limit
both temporary and persistent decks excluded
```

## Forbidden Documentation Content

The guide must not say:

```text
this card should be played
this card should be cut
this card is correct
this deck is tournament evidence
upload your private deck text
paste private raw_input into external tools
```

## Validation For Future Phase 15F

Future implementation should run:

```text
git diff --check
full test suite
strategic language scan over docs/USER_GUIDE_DECK_MEMORY_CLI.md
privacy phrase scan confirming --include-raw-input warning exists
```

## Do Not Do In Phase 15E

```text
do not implement the usage guide yet
do not add code
do not add schema
do not add UI
do not call providers
do not call LLMs
do not generate recommendations
```

## Recommended Next Packet

```text
Phase 15F - Deck Memory CLI Usage Documentation
```
