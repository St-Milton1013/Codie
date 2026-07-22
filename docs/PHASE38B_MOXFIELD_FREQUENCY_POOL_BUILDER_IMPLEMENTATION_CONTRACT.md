# Phase 38B - Moxfield Frequency Pool Builder Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase38B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase38C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 38B converts the accepted Phase 38A Moxfield Frequency Pool Builder
boundary into a concrete implementation contract for the next packet.

Phase 38B itself does not implement parser, provider, builder, export, schema,
repository, UI, CLI, LLM, simulator, analytics, recommendation, or file-writing
behavior. It defines the future Phase 38C files, interfaces, fixture inventory,
tests, and boundaries.

## Accepted Phase 38A Evidence

Phase 38A outside phase-ledger validation returned CLEAN_PASS.

```text
workflow run ID: 29935858106
validated SHA: 2bfa81dbb8c23a1b62737a8411467b602c6de1c3
artifact: codie-phase_ledger-validation-2bfa81dbb8c23a1b62737a8411467b602c6de1c3
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
unresolved findings: none
```

The active validation scope was advanced separately to Phase38B and validated:

```text
workflow run ID: 29936045711
validated SHA: 8df261b4353c6fc9a7902112d6a742b27803093d
artifact: codie-phase_ledger-validation-8df261b4353c6fc9a7902112d6a742b27803093d
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
```

## Phase 38B Scope

This phase may create or modify only:

```text
docs/PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Authorized Future Phase 38C Files

After Phase 38B is accepted, Phase 38C may implement only:

```text
codie/frequency_pools/moxfield_builder.py
tests/test_moxfield_frequency_pool_builder.py
tests/fixtures/moxfield_frequency_pools/brigid_export_1.txt
tests/fixtures/moxfield_frequency_pools/brigid_export_2.txt
tests/fixtures/moxfield_frequency_pools/brigid_export_3.txt
tests/fixtures/moxfield_frequency_pools/brigid_export_4.txt
tests/fixtures/moxfield_frequency_pools/brigid_export_5.txt
tests/fixtures/moxfield_frequency_pools/moxfield_url_payload.json
tests/fixtures/moxfield_frequency_pools/moxfield_private_deck_failure.json
tests/fixtures/moxfield_frequency_pools/moxfield_malformed_export.txt
tests/fixtures/moxfield_frequency_pools/moxfield_unknown_section.txt
tests/fixtures/moxfield_frequency_pools/moxfield_unresolved_card.txt
tests/fixtures/moxfield_frequency_pools/moxfield_duplicate_inputs.json
```

Optional export-only change:

```text
codie/frequency_pools/__init__.py
```

No other production, test, fixture, schema, repository, provider, UI, workflow,
validator, dependency, or constitution files are authorized by Phase 38C unless
a later accepted contract narrows and approves that work.

## Future Public Interface

Phase 38C may define:

```text
MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION
MoxfieldFrequencyPoolBuildError
MoxfieldDeckInputRef
MoxfieldDeckCard
MoxfieldParsedDeck
MoxfieldDeckParseWarning
MoxfieldDeckParseFailure
MoxfieldFrequencyPoolBuilderOptions
MoxfieldFrequencyPoolBuildRequest
MoxfieldFrequencyPoolBuildResult
extract_moxfield_public_id(...)
parse_moxfield_export_text(...)
build_moxfield_frequency_pool_request(...)
build_moxfield_frequency_pool_result(...)
build_moxfield_frequency_pool_from_parsed_decks(...)
validate_moxfield_frequency_pool_result(...)
moxfield_frequency_pool_result_to_dict(...)
```

The future implementation must remain local, deterministic, and fixture-first.
It may parse supplied text fixtures and already-supplied local payload values.
It may not fetch live Moxfield URLs or call Moxfield APIs.

## Future Input Rules

Future request packets may represent:

```text
public Moxfield URL refs
public Moxfield deck IDs extracted from URLs
manual Moxfield text export refs
fixture payload refs
mixed URL and text jobs
```

URL refs in Phase 38C are identifiers only. They do not authorize network
fetching. A URL input without a supplied local payload must produce an explicit
failure or unavailable state.

## Future Parsing Rules

Phase 38C may parse local Moxfield-style export text with recognized sections:

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

Unknown sections must create visible warnings or failures. They must not be
silently included or silently dropped.

## Future Frequency Rules

Phase 38C may build a `FrequencyPoolPacket` from parsed decks using deck
presence by default:

```text
one deck contributes at most one presence count per card
deck_count is the number of accepted decks containing the card
deck_total is the accepted deck count for the pool
frequency_percent is deck_count / deck_total
frequency_label is deck_count/deck_total
```

Total copy count must not be the default. If represented, it must be visibly
separate from deck presence.

Default sort:

```text
highest deck_count first
alphabetical within each deck_count bucket
```

## Future Basic Land Defaults

Basic lands must be excluded by default:

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

Override options may exist only if the result records the chosen setting
visibly.

## Future Identity Rules

Phase 38C may preserve already-supplied Scryfall identity values, including:

```text
card_name
scryfall_id
oracle_id
unresolved marker
raw_name
```

It must not call Scryfall, mutate Scryfall truth, or invent card identity. If a
card cannot be resolved from supplied identity values, the future result must
preserve the raw name and mark the row unresolved.

## Future Failure Visibility

Future results must preserve:

```text
input_count
accepted_deck_count
failed_deck_count
duplicate_deck_count
partial_failure_count
warnings
failures
unresolved_cards
included_sections
excluded_sections
exclude_basic_lands
```

Supported failure codes:

```text
MOXFIELD_FETCH_BLOCKED
MOXFIELD_PRIVATE_DECK
MOXFIELD_DECK_NOT_FOUND
MOXFIELD_API_SCHEMA_CHANGED
CARD_UNRESOLVED
SECTION_UNKNOWN
DUPLICATE_DECK_INPUT
EMPTY_DECKLIST
UNSUPPORTED_EXPORT_FORMAT
URL_PAYLOAD_UNAVAILABLE
```

Partial failures and rejected inputs must not be hidden.

## Future Privacy Boundary

Phase 38C must preserve local-first privacy:

```text
manual export text remains local input
raw imported deck text is not exported downstream by default
private notes are rejected recursively
full primer bodies are rejected recursively
raw provider payload metadata is rejected recursively
Moxfield user decks are not tournament evidence by default
user-local results remain visibly user-local when applicable
```

The future implementation should reuse the existing Frequency Pool private/raw
metadata rejection policy where possible instead of redefining the vocabulary.

## Future Evidence Boundary

Phase 38C may produce local evidence/reporting packets only. It must not:

```text
generate recommendations
rank cards for inclusion
choose cuts
claim optimality
infer pilot intent
produce deck health output
treat Moxfield user decks as commander averages
treat Moxfield user decks as tournament evidence by default
feed Decision Intelligence
```

Decision Intelligence consumption requires a later accepted contract.

## Future Brigid Fixture Target

The Phase 38C fixture suite should reproduce the roadmap target:

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

If fixture data must be synthetic due licensing or privacy, the test fixture
must preserve the same frequency bucket shape and document that card names are
synthetic.

## Future Required Tests

Phase 38C must test:

```text
extracts public Moxfield IDs from supported URL shapes
rejects malformed Moxfield URLs cleanly
parses local Moxfield export sections
includes mainboard by default
excludes commanders by default
excludes sideboard by default
excludes maybeboard by default
excludes considering by default
excludes tokens by default
excludes basic lands by default
records section override settings visibly
uses deck presence frequency by default
does not use total copy count as default
deduplicates repeated card names within one deck for presence counting
detects duplicate deck inputs
preserves partial failures
preserves unresolved card rows
preserves raw names for unresolved rows
builds FrequencyPoolPacket-compatible output
keeps user-local and not-tournament-evidence labels visible
produces deterministic serialization
round-trips through dictionary-compatible form
does not mutate input payloads
rejects private deck text in downstream metadata
rejects private notes recursively
rejects raw provider payload metadata recursively
rejects recommendation/action language
has no live network imports or calls
has no provider, database, repository, analytics, UI, LLM, simulator, or file-writing imports
reproduces the Brigid five-deck frequency bucket fixture
```

## Future Dependency Limits

Allowed dependencies:

```text
Python standard library
codie.frequency_pools.models
```

Allowed import from `codie.frequency_pools.models`:

```text
FrequencyPoolBuildError
FrequencyPoolSubject
FrequencyPoolSourceWindow
FrequencyPoolSourceRef
FrequencyPoolCardIdentity
FrequencyPoolCardRow
FrequencyPoolCoverageReport
FrequencyPoolCaveat
FrequencyPoolPacket
FrequencyPoolOptions
build_frequency_pool_packet
frequency_pool_packet_to_dict
validate_frequency_pool_packet
```

Forbidden dependencies:

```text
requests
httpx
urllib network use
sqlite3
codie.db
codie.providers
codie.analytics
codie.recommendations
codie.decision_intelligence
codie.evidence_fusion
codie.scryfall live lookup
LLM SDKs
server frameworks
UI frameworks
file-writing helpers
```

## Forbidden In Phase 38B

Phase 38B must not add:

```text
production implementation code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
SQLite reads or writes
provider changes
live Moxfield calls
Scryfall lookup calls
frequency calculation
analytics recalculation
exports
file writing
CLI behavior
UI behavior
LLM calls
simulator runtime
recommendation generation
deck health output
dependency changes
validator changes
workflow changes
constitution changes
```

## Phase 38B Outside Validation Packet

Outside validation should review:

```text
docs/PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/CHECKPOINT_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_REPORT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT.md
codie/frequency_pools/models.py
codie/frequency_pools/__init__.py
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Final Governance Summary

Phase 38B is complete when this implementation contract, checkpoint, outside
validation prompt, and governance records are internally consistent and
accepted by PR validation. Phase 38C remains blocked until Phase 38B returns
PASS or PASS WITH REVIEW NOTES.

