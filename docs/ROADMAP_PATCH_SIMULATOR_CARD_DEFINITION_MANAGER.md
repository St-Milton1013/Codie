# Roadmap Patch - Simulator Card Definition Manager

Date: 2026-06-29

Status: Accepted for future roadmap planning. Implementation deferred until
after the probability engine core models are in place.

## Purpose

Codie's simulator must not attempt to model every Magic card.

Codie should recognize every input card through Scryfall, but only needs
simulation behavior for cards that affect the selected target condition.

This subsystem prevents the probability engine from becoming a full Magic rules
engine.

## Core Rule

```text
Deck parser accepts all valid cards.
Simulator models only target-relevant cards.
Unsupported irrelevant cards are inert.
Unsupported relevant cards are flagged.
```

## Required Subsystem

Future module:

```text
codie/probability_engine/card_definition_manager.py
codie/probability_engine/relevance.py
```

Future data folders:

```text
data/sim_cards/
  behavior_overrides/
    mana_sources.json
    tutors.json
    rituals.json
    draw_filter.json
    static_effects.json
    lands.json
    special_cases.json
  generated/
    generated_from_scryfall.json
  review/
    pending_review.json
    unsupported_seen.json
  fixtures/
    card_definition_tests.json
```

These paths are future planning only. This patch does not add data files.

## Two-Layer Card Model

### Layer 1 - Scryfall Identity Layer

Automatically loaded from Scryfall/card lookup.

Fields:

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

Answers:

```text
What is this card?
Is it real?
What are its basic properties?
```

### Layer 2 - Simulator Behavior Overlay

Manual or semi-manual behavior model.

Answers:

```text
What can this card do inside Codie's simulator?
```

Behavior types:

```text
tap_for_mana
sacrifice_for_mana
sacrifice_to_search
add_mana
draw_cards
search_library
search_graveyard
discard_from_hand
exile_from_hand
create_token
extra_land_drop
static_effect
pregame_action
etb_action
grant_cast_permission
special_case
```

## Input Deck Workflow

```text
1. User inputs decklist.
2. Codie parses all cards.
3. Codie normalizes all card names through Scryfall-backed lookup.
4. Codie receives selected simulation target.
5. Codie classifies each card:
   - modeled_relevant
   - modeled_irrelevant
   - unsupported_relevant
   - unsupported_irrelevant
6. Codie loads behavior overlays only for relevant cards.
7. Unsupported irrelevant cards become inert.
8. Unsupported relevant cards are reported before simulation.
9. Simulation runs with confidence warnings if allowed by config.
```

## Relevance Classifier

Future function:

```python
classify_card_relevance(card, target_condition) -> RelevanceResult
```

Relevant categories:

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
wincons unrelated to target
stax pieces unless they affect casting
protection spells unless target requires protected resolution
generic value engines after target turn
```

## Unsupported Handling

Unsupported cards must never disappear.

Track:

```text
card name
oracle_id
deck_id or deck_hash
target_condition
reason unsupported
relevance classification
first_seen_at
last_seen_at
seen_count
```

Unsupported irrelevant:

```text
Treat as inert card.
Continue simulation.
Add note to report.
```

Unsupported relevant:

```text
Warn user.
Lower simulation confidence.
Allow simulation only when target validity permits.
Record missing behavior requirement.
```

## Behavior Overlay Schema

Each behavior file should contain card records keyed by normalized simulator
card ID.

Required record fields:

```text
name
behavior_version
mana_cost
types
cast_actions
board_abilities
etb_actions
hand_abilities
static_effects
pregame_action
metadata
```

Behavior overlays must be declarative. They must not contain executable copied
source code from cEDHData or any other site.

## Auto-Classification Rules

Codie may auto-create simple behavior overlays for:

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

Those go to:

```text
data/sim_cards/review/pending_review.json
```

## Required Report Output

Every simulation report must include:

```text
cards_total
cards_modeled_relevant
cards_modeled_irrelevant
cards_unsupported_relevant
cards_unsupported_irrelevant
confidence_level
unsupported_relevant_cards
unsupported_irrelevant_cards
behavior_overlay_versions
```

Confidence levels:

```text
high: all relevant cards modeled
medium: minor relevant cards unsupported
low: major relevant cards unsupported
invalid: target or required mana engine unsupported
```

## Required Tests For Future Implementation

```text
Sol Ring modeled as mana source
Chrome Mox modeled with imprint memory
Mox Diamond requires land discard
Demonic Tutor finds target to hand
Vampiric Tutor puts target on top
Rhystic Study target is recognized
unsupported irrelevant creature is inert
unsupported relevant tutor lowers confidence
unsupported target invalidates simulation
pending review records are emitted
unsupported seen records are updated
```

## Codie Design Rule

Do not copy cEDHData source code or card data into production.

Use captured files only as reference inputs to understand shape, terminology,
and behavior categories. Codie must implement an independent Python-native
simulator behavior system.

## Placement In Phase 13

Recommended order:

```text
Phase 13B - Probability Engine Core Models Implementation
Phase 13C - Simulator Card Definition Manager Contract
Phase 13D - Simulator Card Definition Manager Implementation
Phase 13E - Deck And Target Parser
Phase 13F - Opening Hand And Seeded Shuffle
```

The definition manager should land before action search. It is the gate that
decides what is modeled, inert, unsupported, or invalid for a target.
