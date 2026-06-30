# Phase 13I - Mulligan Policy Contract

## Purpose

Define London mulligan policy inputs, keep/reject boundaries, trace metadata,
and allowed policy outputs before implementation.

This is a contract-only packet. It does not add mulligan code, target search,
action execution, Monte Carlo batches, persistence, schema changes, or
Challenge Mode.

## Source Documents

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13G_SEEDED_SHUFFLE_AND_OPENING_HAND_CONTRACT.md
docs/PHASE13H_SEEDED_SHUFFLE_AND_OPENING_HAND_IMPLEMENTATION_REPORT.md
```

## Files To Create In Phase 13J

```text
codie/probability_engine/mulligan.py
tests/test_probability_engine_mulligan.py
tests/fixtures/probability_engine/mulligan/mulligan_deck.txt
docs/PHASE13J_MULLIGAN_POLICY_IMPLEMENTATION_REPORT.md
```

## Public Classes And Functions To Add

```text
MulliganPolicyConfig
MulliganDecision
MulliganStep
MulliganResult
evaluate_opening_hand(...)
select_bottom_cards(...)
simulate_london_mulligan(...)
```

Exact names may be adjusted during implementation if the report documents the
change and tests cover the public surface.

## Schema Impact

None.

## Dependency Impact

Allowed:

```text
codie.probability_engine.models
codie.probability_engine.shuffle
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

## Policy Boundary

The mulligan policy is a simulator input policy, not strategic advice.

It may answer:

```text
This configured policy kept the hand.
This configured policy rejected the hand.
This configured policy bottomed these cards.
```

It must not answer:

```text
You should keep this hand.
This hand is correct.
This is the optimal mulligan.
This hand is bad.
```

Policy decisions are reproducible simulator metadata only.

## London Mulligan Rules

Phase 13J should model a simplified London mulligan setup:

```text
draw 7 cards each attempt
if rejected, increment mulligan count and draw a new seeded hand
after keep, bottom cards equal to mulligan count
minimum keep size prevents further mulligans
final kept hand size = 7 - mulligan_count
```

The implementation must not perform game actions or target search.

## Policy Config

Required fields:

```text
policy_name
policy_version
minimum_keep_size
max_mulligans
keep_rules
bottoming_rules
```

Suggested keep rules:

```text
min_lands
max_lands
required_card_names
required_model_ids
minimum_mana_sources
allow_unresolved_cards
```

Suggested bottoming rules:

```text
bottom_unresolved_first
bottom_highest_name_sort_last
bottom_from_end_of_hand
protected_card_names
protected_model_ids
```

Rules must be explicit config data. No hidden strategic claims.

## Keep / Reject Decision Output

Decision fields:

```text
decision
reason_codes
hand_id
hand_size
land_count
mana_source_count
required_cards_present
unresolved_cards
policy_name
policy_version
```

Allowed decision values:

```text
keep
reject
forced_keep_minimum_size
invalid_policy
```

Reason codes:

```text
land_count_below_minimum
land_count_above_maximum
missing_required_card
mana_sources_below_minimum
unresolved_cards_disallowed
minimum_keep_size_reached
policy_conditions_met
```

## Bottoming Rules

When a kept 7-card hand needs to bottom N cards:

```text
N = mulligan_count
bottomed cards are deterministic
bottomed cards are returned separately
kept hand preserves original order after bottomed cards are removed
bottoming must not mutate original OpeningHand
```

If no explicit bottoming rule can decide, use a deterministic fallback:

```text
bottom cards from end of hand
```

## Mulligan Result Output

Required fields:

```text
deck_hash
base_seed
policy_name
policy_version
minimum_keep_size
mulligan_count
kept_hand
bottomed_cards
steps
unresolved_cards
created_at
```

Step fields:

```text
attempt_index
game_index
opening_hand
decision
reason_codes
bottomed_cards
kept_cards_after_bottom
```

Every rejected hand must remain in `steps`. No historical hand may be
overwritten.

## Seed And Reproducibility Rules

Mulligan attempts use the Phase 13H shuffle functions.

Rules:

```text
attempt_index maps to game_index unless caller supplies an offset
same deck + seed + policy config produces same result
different seed can produce different result
policy_version is included in output
shuffle_algorithm_version is inherited from opening hands
```

## Unsupported And Unresolved Rules

Rules:

```text
unresolved cards remain visible in decisions and results
policy config determines whether unresolved cards are allowed
unresolved cards cannot be silently ignored
unsupported behavior does not block mulligan policy
```

## Evidence And Recommendation Boundaries

Mulligan outputs are simulator setup metadata only.

Allowed wording:

```text
Configured policy kept this hand.
Configured policy rejected this hand.
Configured policy bottomed these cards.
```

Forbidden wording:

```text
You should keep this hand.
You should mulligan this hand.
This is the correct mulligan.
This hand is optimal.
This hand is bad.
```

Mulligan output must not enter the Evidence Stack as tournament evidence.

## Acceptance Tests For Phase 13J

```text
policy keeps hand when conditions are met
policy rejects hand when land count below minimum
policy rejects hand when required card missing
minimum_keep_size forces keep
bottomed cards equal mulligan count
bottoming preserves kept-card order
same seed and policy reproduce same result
different seed can produce different result
unresolved cards are reported
unresolved disallowed can reject hand
all rejected hands remain in steps
policy does not mutate original OpeningHand
mulligan module does not import db/providers/analytics/recommendations
no strategic claim language appears
```

## Do Not Do In Phase 13I

- Do not implement mulligan code.
- Do not add target search.
- Do not add action execution.
- Do not add Monte Carlo batch running.
- Do not add persistence.
- Do not add schema.
- Do not add Challenge Mode.
- Do not copy cEDHData source code or full card data.
