# Roadmap Patch - Moxfield Frequency Pool Builder

Status: roadmap-only, implementation deferred

## Purpose

Codie should eventually build a frequency pool from multiple submitted Moxfield
deck links or deck text exports.

The feature should show how often each card appears across a submitted deck
group, using deck presence by default rather than total copy count.

Useful applications:

```text
commander staple analysis
small-sample deck comparison
new commander scouting
top-deck cluster analysis
package detection
manual validation against tournament lists
exportable commander-specific staples lists
```

## Core Workflow

Given multiple deck inputs, Codie should:

```text
extract Moxfield public IDs when URLs are supplied
fetch or import each decklist
parse deck sections
normalize card names
optionally resolve through Scryfall
exclude configured zones and basics by default
count deck presence by default
group cards by frequency
export Markdown, CSV, JSON, and Obsidian-ready Markdown
report partial failures explicitly
```

## Input Modes

Future implementation should support:

```text
Moxfield URLs
plain text Moxfield exports
mixed URL and text input jobs
```

Manual text export support is required because private decks or Moxfield access
changes may block direct fetches.

## Moxfield Fetch Guardrails

Moxfield fetches must be isolated behind a provider adapter.

Known endpoint patterns may be useful:

```text
GET https://api2.moxfield.com/v3/decks/all/{public_id}
GET https://api2.moxfield.com/v2/decks/all/{public_id}/export
```

These are undocumented and must not become core architecture assumptions.

Required behavior:

```text
fixture-first tests
manual paste/export fallback
partial-result error reporting
no hard dependency on live Moxfield access
no hidden skipping of failed decks
```

## Suggested Provider Models

Future contracts may define:

```text
ParsedDeck
DeckCard
```

Suggested `ParsedDeck` fields:

```text
source
source_url
source_id
deck_name
commander_names
mainboard
sideboard
considering
maybeboard
tokens
raw_text
fetched_at
warnings
```

Suggested `DeckCard` fields:

```text
name
quantity
section
raw_line
scryfall_id
oracle_id
```

## Parsing Rules

Recognized section headers:

```text
COMMANDER
COMMANDERS
MAINBOARD
SIDEBOARD
MAYBEBOARD
CONSIDERING
TOKENS
```

Default included section:

```text
mainboard
```

Default excluded sections:

```text
commander
sideboard
maybeboard
considering
tokens
attractions
stickers
planes
schemes
```

Basic lands should be excluded by default:

```text
Plains
Island
Swamp
Mountain
Forest
Wastes
Snow-Covered Plains
Snow-Covered Island
Snow-Covered Swamp
Snow-Covered Mountain
Snow-Covered Forest
```

Users should be able to override these defaults in a future contract.

## Frequency Semantics

Default metric:

```text
deck presence frequency
```

Example:

```text
Sol Ring appears in 4 of 5 decks = 4/5
```

Total copies may be supported later as an explicit count mode, but must not be
the default for Commander staple analysis.

## Required Output Fields

Future frequency rows should support:

```text
card_name
deck_count
deck_total
frequency_label
frequency_percent
deck_ids_present
deck_names_present
deck_ids_missing
deck_names_missing
is_basic_land
included_sections
excluded_reason
scryfall_id
oracle_id
```

Default sort:

```text
highest deck count first
alphabetical within each frequency bucket
```

## Scryfall Normalization

Scryfall remains the source of truth for:

```text
canonical card name
oracle_id
scryfall_id
type line
color identity
mana value
legality
layout
basic land detection
```

If lookup fails:

```text
keep raw name
mark unresolved
include in frequency pool
add to unresolved or unsupported card queue
```

## Future Exports

Future export surfaces:

```text
Markdown
CSV
JSON
Obsidian Markdown
```

CSV columns should include at least:

```text
card_name
deck_count
deck_total
frequency_percent
frequency_label
present_in
missing_from
unresolved
```

## Future UI/CLI

Future UI tab:

```text
Frequency Pool
```

Future CLI concept:

```powershell
python -m codie frequency-pool --source moxfield --urls urls.txt --exclude-basics --mainboard-only --out exports/frequency_pool.md
```

UI and CLI are not approved by this roadmap patch.

## Possible Future Schema

Future persistence may use:

```text
frequency_pool_runs
frequency_pool_run_decks
frequency_pool_cards
```

Schema is not approved by this roadmap patch. Any persistence requires a
separate schema contract with repositories, indexes, idempotency, and rebuild
rules.

## Fixture Target

Future tests should reproduce the five-deck Brigid manual result:

```text
49 cards at 5/5
27 cards at 4/5
17 cards at 3/5
22 cards at 2/5
37 cards at 1/5
```

Known default exclusions:

```text
Brigid, Clachan's Heart
Forest
Plains
sideboard-only Deafening Silence
sideboard-only Walking Ballista
```

## Failure Codes

Future implementation should report:

```text
MOXFIELD_FETCH_BLOCKED
MOXFIELD_PRIVATE_DECK
MOXFIELD_DECK_NOT_FOUND
MOXFIELD_API_SCHEMA_CHANGED
CARD_UNRESOLVED
SECTION_UNKNOWN
DUPLICATE_DECK_INPUT
EMPTY_DECKLIST
```

## Risks

Main risks:

```text
Moxfield API instability
counting the wrong zones
fake precision from small sample pools
card name drift
duplicate deck inputs
private deck exposure
```

Mitigations:

```text
provider isolation
fixture-first tests
manual export fallback
visible run settings
deck presence default
Scryfall normalization
explicit unresolved warnings
duplicate input warnings
```

## Done Criteria

The future feature is complete only when Codie can:

```text
accept five or more Moxfield links or text exports
fetch or import decklists
produce grouped frequency pools
exclude commanders, sideboards, and basics by default
export Markdown, CSV, JSON, and Obsidian Markdown
show failed deck imports instead of hiding them
reproduce the Brigid five-deck fixture result
optionally persist runs after a schema contract is accepted
```

## Non-Goals

```text
do not implement this in Phase 16B
do not add schema from this roadmap patch
do not add UI from this roadmap patch
do not add live Moxfield network dependency without a provider contract
do not treat Moxfield frequency pools as tournament evidence
do not generate strategic recommendation claims
do not expose private deck text without explicit user action
```
