# Phase 13A - cEDHData Reference Extraction And Core Model Design

## Purpose

Extract architecture and model-shape lessons from the supplied cEDHData
reference files without copying cEDHData source code into Codie.

This is a design-only packet. It does not add simulator code, copied source,
fixture payloads, dependencies, or schema.

## Supplied Reference Files

The user supplied local reference files:

```text
C:\Users\Main\Downloads\cedhdata_cards.json
C:\Users\Main\Downloads\cedhdata_simulator_main_bundle.js
```

These files were inspected locally only. Their source contents were not copied
into Codie.

## Extraction Boundary

Allowed:

- derive high-level architecture
- derive field-shape categories
- derive behavior categories
- derive target/search/trace concepts
- design Codie-native Python models
- record counts and observed key names

Forbidden:

- copy bundled JavaScript into Codie
- port functions line-by-line
- preserve minified source snippets
- treat cEDHData output as Codie evidence
- add simulator implementation before Codie contracts are ready

## Card Catalog Shape Observed

The supplied card catalog is a JSON object containing:

```text
cards: list
```

Observed scale:

```text
34760 card records
```

Common card fields:

```text
id
name
types
colors
mana_cost
land_types
produces
cast_actions
board_abilities
etb_actions
hand_abilities
static_effects
pregame_action
enters_tapped
enters_sick
legendary
```

Mana cost shape:

```text
{
  "W": count,
  "U": count,
  "B": count,
  "R": count,
  "G": count,
  "C": count,
  "Generic": count
}
```

Mana production shape:

```text
produces: list of mana option objects
produces: "any" for any-color sources in some records
produces_options: list of restricted/special options
```

## Behavior Categories Observed

Observed action containers:

```text
cast_actions
board_abilities
etb_actions
hand_abilities
static_effects
pregame_action
```

Observed action types include:

```text
tap_for_mana
sacrifice_for_mana
sacrifice_to_search
search_library
search_graveyard
draw_cards
create_token
add_mana
add_mana_any
discard_from_hand
discard_random
return_to_hand
untap_board
extra_land_drop
exile_from_hand_to_play
exile_from_hand_for_mana
grant_cast_permission
mana_production_modifier
modify_card
add_static_effect
grant_board_ability
```

Observed action fields include:

```text
type
tap
sacrifice
produces
produces_options
mana
conditional_mana
target_requirements
conditional_target_requirements
search_targets
destination
count
amount
token_id
requires
requires_not_sick
requires_memory
requires_metalcraft
requires_legendary
require_type
exclude_types
exclude_ids
optional
activation_cost
spend_restriction
store_memory_as
source_zone
duration
```

## Bundle Architecture Concepts Observed

The supplied JavaScript bundle includes simulator concepts matching the
constitution:

```text
parseDecklist
simulateMulliganForSeed
findWinningLine
playKeptHand
seeded shuffle / seed mixing
mana options
payment choice
target access detection
tutor target detection
unsupported-card reporting
recent trace buffering
trace export versioning
raw trace buffer limit
worker-style batch progress
```

This confirms Codie should use a declarative catalog plus pure engine modules,
not a one-off hypergeometric calculator.

## Codie-Native Design

Codie should implement its own Python-native model layer under:

```text
codie/probability_engine/
```

Recommended files for the next implementation packet:

```text
codie/probability_engine/__init__.py
codie/probability_engine/models.py
tests/test_probability_engine_models.py
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
```

No copied JavaScript should appear in these files.

## Core Python Models

### ManaCost

Purpose:
Represent spell costs and payment requirements.

Fields:

```text
W
U
B
R
G
C
Generic
```

Rules:

- values are non-negative integers
- mana value is the sum of all fields
- serialization uses stable key order

### ManaOption

Purpose:
Represent one produced mana option.

Fields:

```text
W
U
B
R
G
C
restriction
source_card_id
```

Rules:

- at least one mana amount must be positive unless used as an empty marker
- restrictions must be explicit, not hidden in prose

### SimulationActionModel

Purpose:
Represent declarative card behavior without executable source-code copying.

Fields:

```text
action_type
zone
cost
produces
target_requirements
destination
requires
optional
metadata
```

Rules:

- unknown action types remain unsupported
- metadata is preserved for future handlers
- action model does not execute itself

### SimulationCardModel

Purpose:
Represent a card known to the simulator.

Fields:

```text
card_id
name
types
colors
mana_cost
land_types
produces
cast_actions
board_abilities
etb_actions
hand_abilities
static_effects
pregame_action
enters_tapped
enters_sick
legendary
raw_reference_shape
```

Rules:

- Codie card identity still resolves through Scryfall where persistence matters
- simulator `card_id` is a local model id, not database identity
- unsupported fields must be preserved in `raw_reference_shape`

### SimulationTargetCondition

Purpose:
Represent a target access question.

Fields:

```text
target_card
target_card_id
target_zone
turn
condition_type
required_support_tags
notes
```

Rules:

- target turn must be positive
- target zone must be explicit
- condition type must be explicit

### SimulationConfig

Purpose:
Represent reproducible simulation settings.

Fields:

```text
deck_hash
seed
games_requested
min_mulligan_keep
mulligan_mode
simulator_version
card_model_version
targets
raw_config
```

Rules:

- seed is required
- versions are required before persistence
- targets are non-empty

### SimulationDeck

Purpose:
Represent simulator input deck state.

Fields:

```text
deck_hash
cards
commanders
source
unresolved_cards
```

Rules:

- cards are quantity/name/model-id rows
- unresolved cards are explicit
- no unresolved card may be silently discarded

### SimulationUnsupportedItem

Purpose:
Represent unsupported cards/actions/effects.

Fields:

```text
item_type
card_name
card_id
reason
action_type
details
```

Rules:

- must be serializable
- must appear in result output and trace output

### SimulationTrace

Purpose:
Represent immutable simulator trace output.

Fields:

```text
trace_id
seed
game_index
opening_hand
mulligan_count
success
actions
final_state
unsupported_items
created_at
```

Rules:

- action order is preserved
- trace is immutable once persisted
- user review annotations are separate

### SimulationResult

Purpose:
Represent target-level output.

Fields:

```text
target
games_completed
win_count
win_rate
margin_of_error
sample_successful_traces
sample_failed_traces
unsupported_items
raw_payload
```

Rules:

- no strategic recommendation language
- no Evidence Stack promotion unless the Phase 13 gate is satisfied

## Implementation Strategy

The clean Codie implementation should:

1. Define pure dataclasses first.
2. Add deterministic `to_dict()`/`from_mapping()` helpers.
3. Validate required fields and enum values.
4. Preserve unknown reference fields as metadata.
5. Add card catalog loading only after model tests pass.
6. Add seeded shuffle only after deck/target models are stable.
7. Add action execution only after mana/action primitives are stable.

## Reference-Informed Test Cases

Future model tests should cover:

```text
ManaCost mana value
ManaOption serialization
SimulationActionModel unknown action preservation
SimulationCardModel for Sol Ring-style tap mana
SimulationCardModel for Chrome Mox-style memory requirement
SimulationCardModel for fetchland-style search action
SimulationTargetCondition validation
SimulationConfig requires seed and versions
SimulationDeck preserves unresolved cards
SimulationUnsupportedItem serializes reason
SimulationTrace preserves action order
SimulationResult carries unsupported items
```

## Do Not Implement Yet

- seeded shuffle
- mulligan logic
- mana payment search
- target access search
- Monte Carlo runner
- Challenge Mode
- line review/veto
- trace review export
- schema migration
- recommendation integration
