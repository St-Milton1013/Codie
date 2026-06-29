# Phase 13C - Simulator Card Definition Manager Contract

## Purpose

Define the simulator card definition manager before Codie implements card
behavior loading, relevance classification, unsupported-card reporting, or
action execution.

This is a contract-only packet. It does not add simulator behavior code, data
files, schema changes, seeded shuffle, mulligan logic, search, or Challenge
Mode.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/ROADMAP_PATCH_SIMULATOR_CARD_DEFINITION_MANAGER.md
```

## Files To Create In Phase 13D

```text
codie/probability_engine/card_definition_manager.py
codie/probability_engine/relevance.py
tests/test_probability_engine_card_definition_manager.py
tests/fixtures/probability_engine/card_definitions/simple_behavior_overlays.json
tests/fixtures/probability_engine/card_definitions/pending_review_seed.json
docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md
```

Optional later data paths:

```text
data/sim_cards/behavior_overrides/
data/sim_cards/generated/
data/sim_cards/review/
data/sim_cards/fixtures/
```

Do not add long-lived data files until the implementation packet explicitly
needs them.

## Public Classes And Functions To Add

```text
CardRelevanceResult
CardDefinitionStatus
UnsupportedCardRecord
CardDefinitionLoadResult
CardDefinitionManager
classify_card_relevance(card, target_condition)
load_behavior_overlay_rows(rows)
build_card_definition_load_result(deck, target_condition, overlays)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None in Phase 13C.

Phase 13D should also avoid schema changes. Unsupported seen records and
pending-review records may be returned as in-memory data or written to local
fixture/report files only if a separate persistence contract approves it.

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

The manager may accept Scryfall/card identity data as plain mappings or model
objects supplied by callers. It must not perform live lookup or own card
resolution.

## Core Rules

```text
Deck parsing accepts all valid cards.
Simulator behavior is loaded only for target-relevant cards.
Unsupported irrelevant cards are inert but reported.
Unsupported relevant cards are reported and lower/invalidates confidence.
Unsupported cards are never silently ignored.
Behavior overlays are declarative data, not executable copied code.
```

## Card Definition Layers

### Scryfall Identity Layer

Supplied by existing card lookup or test fixtures.

Required identity fields when available:

```text
name
oracle_id
scryfall_id
mana_cost
mana_value
colors
color_identity
type_line
oracle_text
legalities
produced_mana
```

This layer answers what the card is. It does not define simulator behavior by
itself, except for safe auto-classification candidates described below.

### Simulator Behavior Overlay

Declarative overlay data defining what the card can do inside Codie's limited
simulator.

Required overlay fields:

```text
card_id
name
behavior_version
types
cast_actions
board_abilities
etb_actions
hand_abilities
static_effects
pregame_action
metadata
```

Overlay rows must deserialize into the Phase 13B model layer. Unknown behavior
fields must be preserved as metadata and surfaced as unsupported if they are
target-relevant.

## Relevance Classifications

Allowed classification values:

```text
modeled_relevant
modeled_irrelevant
unsupported_relevant
unsupported_irrelevant
target_missing_behavior
target_modeled
```

Required result fields:

```text
card_name
card_id
oracle_id
scryfall_id
classification
relevance_reasons
unsupported_reasons
behavior_version
confidence_impact
```

## Relevance Categories

Relevant when applicable to the selected target:

```text
target card itself
lands
mana rocks
mana dorks
rituals
free mana
tutors that can find target
draw/filter spells before target turn
extra land drop effects
cost reducers
cards that grant cast permission
cards that create usable mana tokens
static effects that affect mana/casting
```

Usually irrelevant:

```text
counterspells
removal
combat creatures
win conditions unrelated to target
stax pieces unless they affect casting
protection spells unless target requires protected resolution
generic value engines after target turn
```

Irrelevant does not mean hidden. The manager must still report unsupported
irrelevant cards in summary output.

## Safe Auto-Model Candidates

The implementation may auto-classify simple cases for future modeling:

```text
basic lands
dual lands with basic land types
untapped lands with explicit produced_mana
simple mana rocks
simple mana dorks
simple draw-one spells
simple rituals
```

Do not auto-model:

```text
modal cards
replacement effects
copy effects
timing permission cards
conditional tutors
storm cards
graveyard recursion
cost reducers
cards with complex opponent interaction
cards with hidden/random information
cards with nontrivial static effects
```

These must become pending-review or unsupported records.

## Unsupported Reporting

Unsupported record fields:

```text
card_name
card_id
oracle_id
scryfall_id
deck_hash
target_condition
unsupported_reason
relevance_classification
first_seen_at
last_seen_at
seen_count
```

For in-memory Phase 13D tests, timestamps may be deterministic fixture values.

Unsupported irrelevant:

```text
treat as inert card
continue simulation preparation
include in unsupported summary
do not silently discard
```

Unsupported relevant:

```text
report before simulation
lower confidence or mark invalid
include missing behavior requirement
do not silently continue as if modeled
```

## Confidence Levels

Allowed confidence levels:

```text
high
medium
low
invalid
```

Rules:

```text
high: all relevant cards modeled
medium: only minor relevant cards unsupported
low: major relevant cards unsupported but target may still be testable
invalid: target or required mana/search engine unsupported
```

The manager should compute confidence from classification counts and reasons,
not from strategic claims.

## Required Manager Output

Card definition load result:

```text
deck_hash
target_condition
cards_total
cards_modeled_relevant
cards_modeled_irrelevant
cards_unsupported_relevant
cards_unsupported_irrelevant
confidence_level
modeled_card_ids
unsupported_relevant_cards
unsupported_irrelevant_cards
pending_review_cards
behavior_overlay_versions
generated_at
```

## Evidence And Recommendation Boundaries

The card definition manager is not a recommendation system.

Allowed wording:

```text
Card has no simulator behavior overlay for the selected target.
Card is treated as inert for this target.
Target cannot be simulated because required behavior is unsupported.
```

Forbidden wording:

```text
This card is correct.
This card is secretly optimal.
You should play this card.
You should cut this card.
This card breaks the format.
```

Definition-manager output must not enter the Evidence Stack as tournament
evidence. It is simulator readiness metadata only.

## Acceptance Tests For Phase 13D

```text
Sol Ring modeled as relevant mana source
Chrome Mox reports imprint memory requirement
Mox Diamond reports land discard requirement
Demonic Tutor classified as relevant for target search
Vampiric Tutor classified as relevant topdeck tutor
Rhystic Study target is recognized as target card
unsupported irrelevant creature is inert and reported
unsupported relevant tutor lowers confidence
unsupported target makes result invalid
pending-review records are emitted for complex cards
overlay versions are included in load result
unknown overlay fields are preserved as metadata
manager does not import db/providers/analytics/recommendations
no strategic claim language appears
```

## Do Not Do In Phase 13C

- Do not implement the manager.
- Do not add behavior overlay data files.
- Do not add schema.
- Do not add persistence.
- Do not add seeded shuffle.
- Do not add mulligan logic.
- Do not add target search.
- Do not add action execution.
- Do not add Challenge Mode.
- Do not copy cEDHData source code or full card data.
