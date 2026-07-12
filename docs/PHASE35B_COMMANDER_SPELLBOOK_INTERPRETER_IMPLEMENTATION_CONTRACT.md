# Phase 35B - Commander Spellbook Interpreter Implementation Contract

Status: implementation contract only

## Purpose

Phase 35B defines the exact allowed implementation shape for the future
Commander Spellbook interpreter expansion.

Phase 35A accepted the interpreter boundary. Phase 35B narrows the future
implementation so a later packet can add local, fixture-first Spellbook
interpreter models and validators without adding live Spellbook calls, scraping,
persistence, schema, repositories, provider changes, analytics, simulator
runtime integration, UI, LLM calls, combo ranking, or recommendations.

This phase does not implement Commander Spellbook interpreter code.

## Accepted Dependency

Phase 35B may begin because Phase 35A outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review note carried forward:

```text
GitHub CI was not available for the Phase 35A validation result.
```

## Authorized Future Implementation Scope

A later accepted implementation packet may add only:

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

only to export public Commander Spellbook interpreter model symbols.

No schema, repository, provider, dependency, UI, live-network, file-writing,
analytics, recommendation, simulator-runtime, LLM, frequency-pool, charting, or
Tag Graph Lab metric files may be changed in the implementation packet.

## Future Public Interface

The future implementation may define:

```text
SPELLBOOK_INTERPRETER_VERSION
SpellbookInterpreterError
SpellbookComboSourceRef
SpellbookComponentRef
SpellbookInterpretationClass
SpellbookPrerequisite
SpellbookOutput
SpellbookRestriction
SpellbookTargetCompatibility
SpellbookUnsupportedItem
SpellbookManualReviewItem
SpellbookInterpreterWarning
SpellbookComboInterpretation
SpellbookInterpreterOptions
build_spellbook_combo_interpretation(...)
validate_spellbook_combo_interpretation(...)
spellbook_combo_interpretation_to_dict(...)
```

Do not expose persistence, live import, downloader, repository, provider,
analytics, charting, UI, LLM, recommendation, simulator execution, or
frequency-pool APIs.

## Future Model Responsibilities

The future implementation may represent:

```text
interpreter_version
provider
provider_combo_id
combo_url
combo_name
variant_ids
component_refs
component_roles
prerequisite_classes
output_classes
restriction_classes
target_compatibility_items
unsupported_items
manual_review_items
source_refs
generated_at
warnings
```

## Future Identity Rules

The future implementation must preserve:

```text
provider = commander_spellbook
provider_combo_id
combo_url
combo_name
variant_ids when supplied
component card names
component source refs
resolved scryfall_id when supplied by upstream packets
oracle_id grouping when supplied by upstream packets
raw Spellbook payload provenance by reference only
```

The interpreter must never override Scryfall card truth, canonical deck
contents, canonical event records, analytics records, user deck records, or raw
Spellbook payloads.

## Future Classification Rules

The future implementation must classify combo outputs with explicit controlled
values.

Allowed output class values:

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

Allowed prerequisite and restriction class values:

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
manual-review metadata. It must not be silently converted into a known class.

## Future Target Compatibility Rules

Future target compatibility output may describe:

```text
combo output can satisfy target output class
combo output might satisfy target output class
combo output cannot be classified against target
unsupported compatibility condition
```

Future target compatibility must be metadata only. It must not:

```text
run simulator logic
run target access search
claim tournament evidence
rank combos
recommend combo inclusion
infer deck intent
infer pilot intent
```

## Infinite Draw And Infinite Mana Rules

Infinite draw may be classified as a win-enabling output only when the source
output is explicit and the target context allows that interpretation.

Infinite mana may expose compatible-sink inputs only when the sink relationship
comes from already-built evidence/reference packets such as accepted Scryfall
identity packets or accepted Tagger ontology packets.

The future implementation must not claim:

```text
infinite draw always wins
infinite mana always wins
combo is optimal
combo should be included
combo should be cut
```

## Future Unsupported And Manual Review Rules

Future implementation must preserve visible records for:

```text
unknown output text
unknown prerequisite text
unknown restriction text
unsupported source shape
ambiguous source text
missing component role
unmapped target compatibility
unsupported sink compatibility
```

Unsupported and manual-review items must serialize deterministically and must
not be dropped from output unless an explicit option excludes them.

## Future Fixture Requirements

Future implementation tests must use local fixtures only.

Required fixture coverage:

```text
spellbook_combo_outputs.json
spellbook_combo_restrictions.json
spellbook_combo_unknowns.json
```

Fixtures should cover:

```text
explicit infinite mana output
explicit infinite draw output
finite output
unknown output
known prerequisites
known restrictions
unknown prerequisites
unknown restrictions
variant grouping
component roles
manual-review items
unsupported source shape
```

No test may depend on live Commander Spellbook, live Scryfall, live Scryfall
Tagger, or external network access.

## Future Required Tests

A later implementation should include tests for:

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
dictionary-compatible round-trip
input payloads are not mutated
malformed fixture failures are clean
no combo ranking
no recommendation language
no live network dependency
no schema/repository/provider changes
```

## Future Dependency Rules

Future implementation may use only:

```text
Python standard library
local dataclasses / typing helpers
already accepted provider candidate objects as input values
already accepted Scryfall/Tagger reference packets as optional input values
```

Future implementation must not import:

```text
codie.db
codie.db.repositories
sqlite3
codie.providers
codie.ingestion
codie.analytics
codie.recommendations
codie.evidence_fusion
codie.decision_intelligence
requests
httpx
openai
anthropic
google.generativeai
langchain
flask
fastapi
uvicorn
starlette
```

Importing `codie.providers.spellbook` is intentionally forbidden in the future
interpreter implementation. The interpreter should consume already-built local
payload dictionaries or candidate-like values passed into it; it must not fetch
or parse provider payloads itself.

## Forbidden In Phase 35B

Phase 35B must not add:

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

## Forbidden In Future Implementation

Future implementation must not:

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

## Outside Validation Packet

Phase 35B outside validation should review:

```text
docs/PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_PROMPT.md
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
Phase 35C Commander Spellbook Interpreter Implementation: BLOCKED
```

Phase 35C may begin only after Phase 35B outside validation returns PASS or
PASS WITH REVIEW NOTES.
