# Phase 13Q - Challenge Mode Contract

## Purpose

Define Challenge Mode before implementation.

Challenge Mode is an interactive training layer tied to the existing
probability engine. It generates an exact opening hand from a selected deck and
target condition, records the user's prediction, runs the existing target access
search against that exact hand, and compares the user's answer to the simulator
result.

This is not a recommendation system.

This is a contract-only packet. It does not add Challenge Mode code, schema
changes, line review, UI, recommendation output, or new simulator logic.

## Source Documents

```text
docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md
docs/PHASE13K_TARGET_ACCESS_SEARCH_CONTRACT.md
docs/PHASE13L_TARGET_ACCESS_SEARCH_MVP_IMPLEMENTATION_REPORT.md
docs/PHASE13M_MONTE_CARLO_BATCH_RUNNER_CONTRACT.md
docs/PHASE13N_MONTE_CARLO_BATCH_RUNNER_IMPLEMENTATION_REPORT.md
docs/PHASE13O_SIMULATOR_PERSISTENCE_CONTRACT.md
docs/PHASE13P_SIMULATOR_PERSISTENCE_IMPLEMENTATION_REPORT.md
```

## Files To Create In Phase 13R

```text
codie/probability_engine/challenge_mode.py
tests/test_probability_engine_challenge_mode.py
tests/fixtures/probability_engine/challenge_mode/challenge_deck.txt
docs/PHASE13R_CHALLENGE_MODE_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

```text
ChallengeConfig
ChallengePrompt
ChallengeAnswer
ChallengeResult
generate_challenge_prompt(...)
record_challenge_answer(...)
verify_challenge_answer(...)
serialize_challenge_result(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None for Phase 13R.

Challenge persistence tables are deferred. Phase 13R should return serializable
objects only.

Potential future table:

```text
simulation_challenges
```

Suggested future fields:

```text
challenge_id
deck_hash
target_card
target_zone
target_turn
opening_hand_json
seed
user_answer
user_line_text
simulator_success
simulator_line_json
unsupported_cards_json
generated_at
completed_at
```

Do not add this table in Phase 13R unless a separate migration contract is
approved.

## Dependency Impact

Allowed:

```text
codie.probability_engine.models
codie.probability_engine.shuffle
codie.probability_engine.search
codie.probability_engine.card_definition_manager
standard library only
```

Optional, if needed only for input convenience:

```text
codie.probability_engine.deck_parser
```

Forbidden:

```text
codie.providers
codie.db
codie.analytics
codie.recommendations
codie.ingestion
codie.cards
sqlite3
requests
httpx
live network calls
```

Challenge Mode must not import simulator persistence in Phase 13R. Persistence
is a later opt-in layer.

## Challenge Boundary

Challenge Mode may answer:

```text
The user predicted success.
The simulator result was success.
The user's answer matched the simulator result.
The simulator could not model these cards/actions.
```

Challenge Mode must not answer:

```text
You should keep this hand.
You should play this card.
This line is optimal.
This card is correct.
This deck is good or bad.
```

The output compares a user prediction to a simulator result. It is not strategic
advice.

## Challenge Config

Required fields:

```text
challenge_version
deck_hash
base_seed
game_index
target_condition
search_config
hand_size
```

Optional fields:

```text
prompt_id
generated_at
```

Validation rules:

```text
challenge_version is required
deck_hash is required
base_seed is required
game_index cannot be negative
hand_size must be positive
target_condition is required
```

## Prompt Generation

Challenge prompt generation must:

```text
shuffle the selected deck using base_seed and game_index
draw the configured opening hand
store opening hand exactly as displayed
store remaining library order for verification
store target condition
store seed/config metadata
report unsupported cards visible in hand when card definitions are provided
```

Prompt generation must not:

```text
evaluate whether the hand is strong
run recommendations
invent a separate hand evaluator
change the hand after displaying it
```

## User Answer

Allowed answer values:

```text
yes
no
unknown
```

Optional user line:

```text
user_line_text
```

User line text is stored as user-provided text. Phase 13R must not parse it into
strategic claims or treat it as evidence.

## Verification Workflow

Verification must:

```text
use the exact opening hand from the challenge prompt
use the exact remaining library order from the challenge prompt
run find_target_access_line(...)
return simulator status
return simulator success/failure
return action trace when available
return unsupported cards/actions
compare user answer to simulator success
```

The simulator result is the target access search result for that exact prompt,
not a new shuffled game.

## Result Output

Required fields:

```text
challenge_id
challenge_version
deck_hash
target_condition
opening_hand
remaining_library_size
base_seed
game_index
derived_seed
user_answer
user_line_text
simulator_status
simulator_success
simulator_trace
unsupported_cards
unsupported_actions
user_was_correct
generated_at
completed_at
```

## Unsupported Handling

Unsupported behavior must be explicit:

```text
unsupported cards are returned by name
unsupported actions are returned by type
unsupported cards cannot be silently ignored
unsupported simulator status makes user_was_correct null unless answer was unknown
```

Allowed `user_was_correct` values:

```text
true
false
null
```

If simulator status is `unsupported` or `invalid_target`, the result should not
pretend the user was right or wrong about a model the simulator cannot validate.

## Reproducibility Rules

The same inputs must produce the same prompt and verification result:

```text
deck_hash
deck contents
base_seed
game_index
shuffle algorithm version
target_condition
search_config
card definition overlays
challenge_version
```

Challenge output must include enough seed/config metadata to recreate the exact
hand.

## Acceptance Tests For Phase 13R

Required tests:

```text
challenge hand generation is deterministic from seed
challenge prompt stores target condition
challenge prompt stores opening hand and remaining library order
user answer is recorded
verification runs target search against exact displayed hand
reachable line returns simulator success and trace
unreachable hand returns simulator failure
unsupported cards/actions are reported
unsupported result does not mark user right or wrong
user answer comparison works for yes and no
serialized result includes seed/config metadata
challenge mode has no DB/provider/analytics/recommendation imports
batch/search/mulligan modules remain Challenge Mode-free
no strategic claim language is generated
```

## Do Not Do In Phase 13Q

```text
Do not implement Challenge Mode.
Do not add schema changes.
Do not persist challenge records.
Do not add line review or veto.
Do not add UI.
Do not add recommendation output.
Do not add a separate hand evaluator.
Do not call providers, Scryfall, DB, or network.
```

## Recommended Next Step

```text
Phase 13R - Challenge Mode Implementation
```

Implement serializable Challenge Mode prompt/answer/verification models using
the existing shuffle and target access search layers, with no persistence or UI.
