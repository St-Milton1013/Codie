# Phase 13G - Seeded Shuffle And Opening Hand Contract

## Purpose

Define deterministic library expansion, seeded shuffle, opening-hand drawing,
hand identity, and reproducibility checks before implementation.

This is a contract-only packet. It does not add shuffle code, opening-hand
generation code, mulligan policy, target search, action execution, Monte Carlo
batches, persistence, schema changes, or Challenge Mode.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md
```

## Files To Create In Phase 13H

```text
codie/probability_engine/shuffle.py
tests/test_probability_engine_shuffle.py
tests/fixtures/probability_engine/shuffle/opening_hand_deck.txt
docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

```text
ExpandedLibraryCard
ExpandedLibrary
OpeningHand
ShuffleResult
expand_library(deck)
derive_game_seed(base_seed, game_index)
shuffle_library(deck, seed, game_index=0)
draw_opening_hand(shuffle_result, hand_size=7)
opening_hand_id(opening_hand)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None.

## Dependency Impact

Allowed:

```text
codie.probability_engine.models
codie.probability_engine.deck_parser
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

## Library Expansion Rules

`expand_library(deck)` converts a `SimulationDeck` into a deterministic sequence
of physical library cards.

Rules:

```text
main deck rows are expanded by quantity
command zone rows are excluded from library
ignored/sideboard rows are never present because parser excluded them
each physical copy gets a stable copy_index starting at 1
expanded rows include name, model_id, zone, source_quantity, copy_index
unresolved cards remain in the library if they are main deck cards
unresolved cards must be disclosed in result metadata
```

Expansion order before shuffle:

```text
normalized card name
model_id or empty string
copy_index
display name
```

This pre-shuffle order exists only for reproducibility. It must not imply
strategic ordering.

## Seed Rules

Required inputs:

```text
deck_hash
base_seed
game_index
shuffle_algorithm_version
```

Derived game seed:

```text
sha256:<deck_hash>|<base_seed>|<game_index>|<shuffle_algorithm_version>
```

The implementation may use a standard-library PRNG seeded from a SHA-256
digest, but it must document the exact conversion in the implementation report.

Rules:

```text
same deck_hash + base_seed + game_index + algorithm version produces same order
different game_index may produce different order
different base_seed may produce different order
same physical library and seed produces same opening hand
seed values are strings
game_index is a non-negative integer
```

## Shuffle Algorithm Rules

The shuffle should be:

```text
deterministic
standard-library only
stable across one Python implementation version as documented
explicitly versioned
independent from global random state
```

Recommended implementation:

```text
local random.Random(<integer derived from sha256>) instance
Fisher-Yates / Random.shuffle on local copy
```

Do not use:

```text
global random.seed
cryptographic claims
external libraries
network calls
```

## Opening Hand Rules

`draw_opening_hand(...)`:

```text
draws the first N cards from the shuffled library
defaults N to 7
requires N > 0
requires N <= library size
preserves shuffled order inside the hand
returns remaining library separately or through ShuffleResult metadata
```

Opening hand object fields:

```text
deck_hash
base_seed
game_index
derived_seed
hand_size
cards
hand_id
shuffle_algorithm_version
unresolved_cards
```

Opening hand output must not classify the hand as good, keepable, correct, or
recommended.

## Hand Identity Rules

`opening_hand_id(...)` must be deterministic.

Hash input should include:

```text
deck_hash
derived_seed
game_index
hand_size
ordered physical hand cards
shuffle_algorithm_version
```

Hash string should use:

```text
sha256:<hex>
```

The hand ID should change if card order changes.

## Unsupported And Unresolved Rules

Seeded shuffle is not card behavior modeling.

Rules:

```text
unsupported behavior does not block shuffling
unresolved cards do not block shuffling
unresolved cards are included as physical cards if present in the main deck
unresolved cards are disclosed in opening-hand metadata
no unresolved card may be silently dropped
```

## Required Output Shapes

Expanded library:

```text
deck_hash
cards
cards_total
unresolved_cards
```

Expanded card:

```text
name
model_id
zone
source_quantity
copy_index
physical_id
```

Shuffle result:

```text
deck_hash
base_seed
game_index
derived_seed
shuffle_algorithm_version
library_size
shuffled_cards
unresolved_cards
```

Opening hand:

```text
deck_hash
base_seed
game_index
derived_seed
shuffle_algorithm_version
hand_size
cards
hand_id
remaining_library_size
unresolved_cards
```

## Evidence And Recommendation Boundaries

Allowed wording:

```text
Opening hand generated from seed.
Opening hand contains unresolved cards.
The same seed and deck hash reproduce this hand.
```

Forbidden wording:

```text
This hand is keepable.
This hand is a mulligan.
This hand is correct.
You should keep this hand.
You should mulligan this hand.
```

Opening-hand output is simulator setup metadata only. It is not tournament
evidence and must not enter the Evidence Stack.

## Acceptance Tests For Phase 13H

```text
library expansion repeats cards by quantity
commanders are excluded from library
unresolved main deck cards remain in expanded library
same seed and game_index produce same shuffled order
different game_index can produce different order
different base_seed can produce different order
opening hand draws first seven shuffled cards
opening hand rejects hand_size larger than library
opening hand ID is deterministic
opening hand ID changes when ordered cards change
shuffle does not mutate original SimulationDeck
shuffle uses no global random seed
shuffle module does not import db/providers/analytics/recommendations
no strategic claim language appears
```

## Do Not Do In Phase 13G

- Do not implement shuffle code.
- Do not implement opening-hand generation code.
- Do not add mulligan logic.
- Do not add target search.
- Do not add action execution.
- Do not add Monte Carlo batch running.
- Do not add persistence.
- Do not add schema.
- Do not add Challenge Mode.
- Do not copy cEDHData source code or full card data.
