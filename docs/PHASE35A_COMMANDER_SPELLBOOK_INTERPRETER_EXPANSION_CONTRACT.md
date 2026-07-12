# Phase 35A - Commander Spellbook Interpreter Expansion Contract

Status: contract only

## Purpose

Phase 35A defines the future Commander Spellbook interpreter expansion boundary
for Codie.

Commander Spellbook is accepted as combo authority. Existing Phase 7A work
captures combo evidence and persists known combos. The next deferred priority is
deterministic interpretation: describing combo prerequisites, outputs,
restrictions, and simulator target compatibility from already-available
Spellbook data without ranking combos, inferring deck intent, or generating
recommendations.

This phase does not implement interpreter code, schema, repositories, provider
changes, live Spellbook calls, analytics, simulator execution, UI, LLM calls, or
recommendations.

## Accepted Dependency

Phase 35A may begin because Phase 34C outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review notes carried forward:

```text
load_scryfall_tagger_ontology_fixture(...) was listed in earlier candidate
ideas but was not required by the accepted Phase 34B interface.

Phase 34C does not import Phase 32/33 model layers because it did not need
them.

GitHub CI was not available for the Phase 34C validation result.
```

## Future Scope To Define

A future accepted implementation packet may add local, fixture-first Commander
Spellbook interpreter models and validators covering:

```text
combo identity interpretation
combo prerequisite classification
combo output classification
combo restriction classification
combo variant grouping
component role classification
target compatibility classification
infinite draw handling
infinite mana handling
compatible mana sink detection inputs
unsupported interpretation reporting
deterministic serialization
manual-review item output
```

## Source Rules

Primary combo authority:

```text
Commander Spellbook
```

Commander Spellbook combo information may establish:

```text
combo existence
combo components
combo requirements
combo outcomes
combo variants
combo source URLs
```

Commander Spellbook interpreter output is combo interpretation metadata. It is
not tournament evidence, deck intent, play-pattern proof, primer truth,
simulation proof, or recommendation output.

## Identity Rules

Future interpreter implementation must preserve:

```text
provider = commander_spellbook
provider_combo_id
combo URL/source URL
component card names
resolved scryfall_id when available
oracle_id grouping when available
raw Spellbook payload provenance
```

The interpreter must not override Scryfall card truth, canonical deck contents,
canonical event records, analytics records, user deck records, or raw Spellbook
payloads.

## Interpretation Rules

Future implementation must classify combo outputs with explicit controlled
values.

Required output concepts:

```text
infinite_mana
infinite_draw
infinite_damage
infinite_tokens
infinite_life
mill
storm
combat
lock
win_condition
card_advantage
mana_generation
board_state
unknown
```

Future implementation must classify prerequisites and restrictions with
explicit controlled values.

Required prerequisite/restriction concepts:

```text
requires_commander
requires_battlefield
requires_hand
requires_graveyard
requires_library
requires_mana
requires_tap
requires_untap
requires_cast
requires_opponent
requires_specific_zone
color_requirement
timing_requirement
once_per_turn_limit
summoning_sickness_sensitive
unknown_requirement
```

Unknown, ambiguous, or unsupported interpretation must remain visible as
manual-review metadata. It must not be silently converted into a known
classification.

## Infinite Draw And Win Treatment

Future implementation may classify:

```text
infinite draw
```

as a target-compatible win-enabling output only when the source output is
explicit and the future target context allows it.

The interpreter must not claim:

```text
infinite draw always wins
infinite mana always wins
combo is optimal
combo should be included
combo should be cut
```

## Infinite Mana And Sink Compatibility

Future implementation may expose a compatibility input that says:

```text
combo produces infinite mana of type X
target card or functional tag consumes compatible mana
```

Compatible sink detection must depend on already-built evidence/reference
packets, such as Scryfall card identity and future accepted Tagger ontology
data. It must not invent sink behavior, call an LLM, call live Scryfall Tagger,
run simulator logic, or inspect deck intent.

## Future Interpreter Record Shape

A later implementation may represent:

```text
interpreter_version
provider
provider_combo_id
combo_url
combo_name
variant_ids
component_refs
prerequisite_classes
output_classes
restriction_classes
target_compatibility
unsupported_items
manual_review_items
source_refs
generated_at
warnings
```

This is a future packet shape only. Phase 35A adds no schema or repository.

## Future Authorized Implementation Shape

A later accepted implementation contract may authorize files such as:

```text
codie/combos/spellbook_interpreter.py
tests/test_spellbook_interpreter.py
tests/fixtures/spellbook_interpreter/spellbook_combo_outputs.json
tests/fixtures/spellbook_interpreter/spellbook_combo_restrictions.json
tests/fixtures/spellbook_interpreter/spellbook_combo_unknowns.json
```

The future implementation may update:

```text
codie/combos/__init__.py
```

only to export public interpreter model symbols.

No schema, repository, provider, dependency, UI, live-network, file-writing,
analytics, recommendation, simulator-runtime, or LLM files may be changed unless
a later contract explicitly authorizes that work.

## Forbidden In Phase 35A

Phase 35A must not add:

```text
production interpreter code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
SQLite reads or writes
live Commander Spellbook calls
Spellbook scraping
file writing
analytics calculation
frequency pool calculation
Tag Graph Lab metrics
simulator execution
simulator target search integration
UI work
LLM calls
recommendation generation
dependency changes
```

## Forbidden In Future Interpreter Implementation

Future interpreter implementation must not:

```text
rank combos
score combos
recommend combos
infer deck intent
infer pilot intent
treat combo interpretation as tournament evidence
treat simulator compatibility as tournament evidence
mutate raw Spellbook payloads
silently drop unsupported requirements
silently convert unknown outputs to known outputs
call live Spellbook in tests
call Scryfall Tagger live
call LLMs
generate play/cut/include language
```

## Future Required Tests

A later implementation contract should require tests for:

```text
valid combo output classification
valid prerequisite classification
valid restriction classification
variant grouping remains deterministic
component roles preserve source refs
infinite draw is classified but not overclaimed
infinite mana records compatible-sink inputs only
unknown outputs produce manual-review items
unsupported requirements remain visible
source URLs and provider_combo_id remain visible
raw payload provenance remains untouched
deterministic serialization
no combo ranking
no recommendation language
no live network dependency
no schema/repository/provider changes
```

## Outside Validation Packet

Phase 35A outside validation should review:

```text
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_PROMPT.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_PROMPT.md
docs/PHASE7A_SPELLBOOK_COMBO_EVIDENCE_CONTRACT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/providers/spellbook/parser.py
codie/combos/sync.py
tests/test_provider_spellbook.py
tests/test_combo_sync.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Next Gate

```text
Phase 35B Commander Spellbook Interpreter Expansion Implementation Contract: BLOCKED
```

Phase 35B may begin only after Phase 35A outside validation returns PASS or
PASS WITH REVIEW NOTES.
