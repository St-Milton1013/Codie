# Phase 13E - Deck And Target Parser Contract

## Purpose

Define how simulator deck input and target settings become the Phase 13B
in-memory models:

```text
SimulationDeck
SimulationDeckCard
SimulationTargetCondition
```

This is a contract-only packet. It does not add parser code, card lookup,
seeded shuffle, opening-hand generation, mulligan logic, action execution,
target search, persistence, schema changes, or Challenge Mode.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md
docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md
docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md
```

## Files To Create In Phase 13F

```text
codie/probability_engine/deck_parser.py
tests/test_probability_engine_deck_parser.py
tests/fixtures/probability_engine/deck_parser/plaintext_deck.txt
tests/fixtures/probability_engine/deck_parser/moxfield_plaintext_deck.txt
tests/fixtures/probability_engine/deck_parser/malformed_deck.txt
docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

```text
ParsedDeckInput
ParsedTargetInput
DeckParseIssue
parse_simulation_deck_text(...)
parse_simulation_deck_rows(...)
parse_target_condition(...)
build_simulation_deck(...)
stable_deck_hash(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None.

## Dependency Impact

Allowed:

```text
codie.probability_engine.models
standard library only
```

Forbidden:

```text
codie.providers
codie.db
codie.analytics
codie.recommendations
codie.ingestion
sqlite3
requests
httpx
live network calls
```

The parser may accept already-resolved card identity rows supplied by callers,
but it must not perform live Scryfall lookup or own card resolution.

## Supported Deck Inputs

Phase 13F should support:

```text
plain text decklist rows
Moxfield-style plain text rows
explicit commander rows
main deck rows
side/considering rows only as ignored sections
already-normalized row dictionaries supplied by tests or callers
```

Supported row examples:

```text
1 Sol Ring
Sol Ring
1x Sol Ring
1 Rhystic Study
Commander
1 Tymna the Weaver
1 Kraum, Ludevic's Opus
```

Unsupported rows must produce parse issues instead of disappearing.

## Zone Rules

Allowed zones:

```text
main
command
sideboard
considering
unknown
```

Only `main` and `command` rows become simulator deck cards by default.

Rows in ignored sections must be returned as parse issues or ignored rows with
explicit reason:

```text
ignored_section
```

Do not silently include sideboard, maybeboard, considering, or primer text.

## Commander Rules

Commander rows may come from:

```text
explicit Commander section
explicit commander input parameter
already-normalized rows with zone = command
```

Partner pairs must preserve both rows and stable ordering for hashing.

Parser must not infer commanders from deck contents unless a future contract
explicitly allows it.

## Quantity Rules

Rules:

```text
missing quantity defaults to 1
quantity must be a positive integer
zero quantity is invalid
negative quantity is invalid
non-integer quantity is invalid
duplicate rows for the same name and zone are combined
```

The parser may keep original raw lines in metadata for debugging.

## Name Rules

Rules:

```text
trim whitespace
collapse repeated internal whitespace
preserve punctuation and capitalization in display name
use normalized lowercase name only for combining/hash comparison
do not perform fuzzy card correction
do not invent missing card names
```

Card identity resolution remains outside this parser unless a caller provides
resolved model IDs.

## Unresolved Cards

The parser must preserve unresolved cards explicitly in:

```text
SimulationDeck.unresolved_cards
```

Unresolved cards may include:

```text
unknown card names
malformed rows
placeholder cards
cards with missing model_id when model IDs are required by caller config
```

Unresolved cards must not be silently discarded.

## Deck Hash Rules

`stable_deck_hash(...)` must be deterministic.

Hash input should include:

```text
zone
quantity
normalized card name
model_id when present
commander rows
main deck rows
```

Hash input must exclude:

```text
raw line order when rows normalize to the same multiset
comments
ignored sections
parse issue ordering
display capitalization differences
extra whitespace
```

Partner commander order should not change the hash when the same pair is
present.

The hash string should use an explicit prefix:

```text
sha256:<hex>
```

## Target Input

Phase 13F should support explicit target fields:

```text
target_card
target_card_id
target_zone
turn
condition_type
required_support_tags
notes
```

Required:

```text
target_card
target_zone
turn
condition_type
```

Allowed target zones:

```text
hand
stack
battlefield
graveyard
exile
library
top_of_library
accessible
```

Allowed condition types:

```text
cast
cast_or_access
access
draw
find_to_hand
find_to_top
put_onto_battlefield
```

Rules:

```text
turn must be a positive integer
target card must be explicit
target zone must be explicit
condition type must be explicit
target parser must not infer strategy
```

## Parse Issues

Parse issue fields:

```text
line_number
raw_line
issue_type
message
severity
```

Allowed severities:

```text
info
warning
error
```

Issue types:

```text
ignored_blank
ignored_comment
ignored_section
malformed_row
invalid_quantity
missing_card_name
unsupported_section
unresolved_card
duplicate_combined
```

Errors should prevent building a simulation deck unless a caller explicitly
allows partial parsing.

## Required Parser Output

Parsed deck input:

```text
deck
issues
raw_input_hash
source_format
cards_total
commanders_total
unresolved_cards
ignored_rows
```

Target parser output:

```text
target_condition
issues
raw_target
```

## Evidence And Recommendation Boundaries

The parser is not a recommendation system.

Allowed wording:

```text
Deck row could not be parsed.
Card remains unresolved for simulation input.
Target condition is invalid because turn must be positive.
```

Forbidden wording:

```text
This hand is keepable.
This card is correct.
You should play this card.
You should cut this card.
This target is optimal.
```

Parser output must not enter the Evidence Stack as tournament evidence.

## Acceptance Tests For Phase 13F

```text
plain text deck parses into SimulationDeck
Moxfield-style deck parses into SimulationDeck
commander section becomes command zone rows
partner pair order does not change deck hash
duplicate rows are combined
comments and blank lines are ignored with issues
sideboard/considering sections are excluded with issues
malformed rows produce parse errors
invalid quantities produce parse errors
unresolved cards are preserved
stable deck hash ignores whitespace/capitalization/order
target condition parses valid input
target condition rejects missing target card
target condition rejects invalid turn
target condition rejects unsupported zone
target condition rejects unsupported condition type
parser does not import db/providers/analytics/recommendations
no strategic claim language appears
```

## Do Not Do In Phase 13E

- Do not implement parser code.
- Do not add card lookup.
- Do not add Scryfall calls.
- Do not add schema.
- Do not add persistence.
- Do not add seeded shuffle.
- Do not add opening-hand generation.
- Do not add mulligan logic.
- Do not add target search.
- Do not add action execution.
- Do not add Challenge Mode.
- Do not copy cEDHData source code or full card data.
