# Phase 13K - Target Access Search Contract

## Purpose

Define the first deterministic target access search before implementation.

This is a contract-only packet. It does not add search code, action execution,
Monte Carlo batches, persistence, schema changes, Challenge Mode, line review,
or recommendation output.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13D_SIMULATOR_CARD_DEFINITION_MANAGER_IMPLEMENTATION_REPORT.md
docs/PHASE13F_DECK_AND_TARGET_PARSER_IMPLEMENTATION_REPORT.md
docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md
docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md
```

## Files To Create In Phase 13L

```text
codie/probability_engine/search.py
tests/test_probability_engine_search.py
tests/fixtures/probability_engine/search/target_access_deck.txt
docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

```text
SearchConfig
SearchState
SearchAction
SearchTrace
SearchResult
TargetAccessResult
build_initial_search_state(...)
find_target_access_line(...)
is_target_accessed(...)
serialize_search_trace(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None.

## Dependency Impact

Allowed:

```text
codie.probability_engine.models
codie.probability_engine.card_definition_manager
codie.probability_engine.deck_parser
codie.probability_engine.shuffle
codie.probability_engine.mulligan
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

## Search Boundary

The target access search is a simulator mechanic, not advice.

It may answer:

```text
The configured simulator found a line to the target.
The configured simulator did not find a line within limits.
The configured simulator could not model required behavior.
```

It must not answer:

```text
You should keep this hand.
You should play this card.
This line is optimal.
This is the correct line.
This card is good or bad.
```

Search output is reproducible simulator evidence only.

## MVP Search Scope

Phase 13L should implement a small deterministic search that can answer whether
a target condition is reached from an exact hand and library state.

The MVP must support:

```text
single-game initial state
known opening hand
known library order
configured target condition
configured maximum turn
configured maximum actions
configured maximum branches
deterministic action ordering
compact serializable trace output
unsupported-card and unsupported-action reporting
```

The MVP must not support:

```text
opponent interaction
priority passes beyond compact cast/resolve traces
hidden information inference
probabilistic branches
heuristic strategic evaluation
deck recommendations
Monte Carlo batches
persistence
Challenge Mode
line review
```

## Search State

Required state fields:

```text
turn
phase_label
hand
library
battlefield
graveyard
exile
stack
mana_pool
land_played_this_turn
actions_taken
target_condition
unsupported_cards
unsupported_actions
```

Mana pool should support:

```text
W
U
B
R
G
C
generic_available
```

The implementation may keep generic spending metadata simple, but it must be
deterministic and serializable.

## Allowed Action Categories

Phase 13L may execute only actions explicitly supported by card behavior
overlays or core land rules.

Allowed action categories:

```text
play_land
tap_for_mana
sacrifice_for_mana
cast_spell
resolve_spell
draw_cards
search_library
move_to_hand
put_on_top
put_onto_battlefield
add_mana
unsupported_marker
```

Unknown card behavior must not be invented. If a line requires an unsupported
card behavior, the result must report it rather than silently ignoring it.

## Target Conditions

Supported target condition modes:

```text
access
cast
cast_or_access
draw
find_to_hand
find_to_top
put_onto_battlefield
```

Definitions:

```text
access
  The target card is reachable in hand, has been drawn, or has been found by a
  modeled search action.

cast
  The target card has been cast or placed onto the stack by a modeled action.

cast_or_access
  Either access or cast condition is satisfied.

draw
  The target card was drawn from library into hand by a modeled draw action.

find_to_hand
  The target card was moved from library or another modeled zone into hand by a
  modeled search or tutor action.

find_to_top
  The target card was placed on top of library by a modeled action.

put_onto_battlefield
  The target card was moved onto the battlefield by a modeled action.
```

Target matching must use normalized card names and model identifiers already
provided by the probability engine parsing/model layer.

## Search Config

Required fields:

```text
search_version
max_turn
max_actions
max_branches
trace_limit
stop_at_first_success
allow_unsupported_relevant
deterministic_tie_breakers
```

Defaults should prefer bounded, reproducible behavior:

```text
stop_at_first_success = true
allow_unsupported_relevant = false
deterministic_tie_breakers = true
```

## Termination Rules

Search terminates when:

```text
target condition is reached
max_turn is exceeded
max_actions is exceeded
max_branches is exceeded
no legal modeled actions remain
required target/card behavior is unsupported and unsupported behavior is disallowed
```

Allowed result statuses:

```text
success
failure
unsupported
invalid_target
limit_exceeded
```

## Trace Output

Every successful line and reported failure path must be serializable.

Trace action fields:

```text
action_index
turn
phase_label
action_type
source_card
source_zone
destination_zone
mana_before
mana_after
cards_moved
target_status_after
reason
unsupported_card
unsupported_action
```

Trace output should be compact. It must preserve enough information to replay
the simulator claim in tests and future Challenge Mode review.

## Unsupported Behavior Handling

Rules:

```text
unsupported cards are reported by name
unsupported relevant behaviors are reported by action type
unsupported behavior is never silently ignored
unsupported irrelevant cards may remain inert
unsupported relevant behavior returns unsupported unless config explicitly allows continuing
```

If a card is in hand but not needed for the discovered line, the result may
include it in passive unsupported cards without failing the search. If the only
known path requires that unsupported card, the result must be unsupported.

## Determinism Rules

The same inputs must produce the same result:

```text
deck hash
opening hand
library order
target condition
card definition overlays
search config
search version
```

Action ordering must be stable. Suggested ordering:

```text
play land
mana abilities
free mana actions
draw/search actions
cast target
other castable supported spells
```

Within an action category, sort by:

```text
zone order
card normalized name
original card order
action type
```

## Acceptance Tests For Phase 13L

Required tests:

```text
target already in opening hand succeeds for access
target cast line succeeds when modeled mana source and target cost are available
unavailable target fails cleanly
unsupported relevant action returns unsupported
unsupported irrelevant card is reported without blocking an unrelated success
max_actions stops search
max_branches stops search
deterministic tie breakers produce the same trace for the same input
trace includes ordered action records
result serialization includes unsupported cards and unsupported actions
provider/db/analytics/recommendation imports are absent
strategic claim language is absent
```

## Do Not Do In Phase 13K

```text
Do not implement search.
Do not implement action execution.
Do not implement Monte Carlo batches.
Do not add persistence.
Do not add schema changes.
Do not add Challenge Mode.
Do not add line review.
Do not copy cEDHData source code or card catalog data.
Do not generate recommendations or strategic claims.
```

## Recommended Next Step

```text
Phase 13L - Target Access Search MVP Implementation
```

Implement the bounded deterministic search described here, with focused tests
and no simulator persistence or Challenge Mode wiring.
