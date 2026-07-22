# Phase 38A - Moxfield Frequency Pool Builder Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase38A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase38B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 38A defines the future Moxfield Frequency Pool Builder boundary.

The future builder will allow Codie to build small, user-supplied frequency
pools from Moxfield public deck URLs and/or pasted Moxfield text exports.
Phase 38A itself does not implement parsing, fetching, provider adapters,
frequency calculation, exports, schema, repositories, UI, or recommendation
behavior.

## Accepted Dependencies

Phase 38A may begin because Phase 37 closed with artifact-backed validation:

```text
Phase 37 Frequency Pools / Tag Graph Lab split: PASS
workflow run ID: 29881579352
validated SHA: 5901dc51d8bc823ce85e29894768573d0555b91a
artifact: codie-phase_ledger-validation-5901dc51d8bc823ce85e29894768573d0555b91a
aggregate: CLEAN_PASS
unresolved findings: none
```

The active validation scope was advanced separately to Phase38A and validated:

```text
workflow run ID: 29928542885
validated SHA: 7f5caa161ba90f2f753da556a75f97145e0c8d9b
artifact: codie-phase_ledger-validation-7f5caa161ba90f2f753da556a75f97145e0c8d9b
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
```

## Phase 38A Scope

This phase may create or modify only:

```text
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/CHECKPOINT_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Future Authorized Direction

A later accepted contract may authorize local, fixture-first model and
implementation planning for:

```text
Moxfield deck input refs
Moxfield public URL ID extraction
manual text export intake contracts
deck section parsing rules
included and excluded zone options
basic land exclusion defaults
duplicate deck input detection
partial failure reporting
Scryfall identity-resolution input refs
frequency pool builder request packets
frequency pool builder result packets
frequency row input values
unresolved card reporting
local fixture inventory
```

Phase 38B is reserved for the implementation-contract packet. Phase 38B must
not become production implementation unless its accepted contract explicitly
narrows and authorizes that work.

## Future Input Modes

The future builder may support these input modes only after a later accepted
implementation contract:

```text
Moxfield public deck URLs
pasted Moxfield text exports
mixed URL and text input jobs
local fixture decks for tests
```

Manual text export support is required for private decks and for cases where
Moxfield public access changes or is unavailable.

## Moxfield Provider Boundary

Future live Moxfield access must be isolated behind a provider adapter and
must never be required for tests.

Known endpoint patterns are reference-only:

```text
GET https://api2.moxfield.com/v3/decks/all/{public_id}
GET https://api2.moxfield.com/v2/decks/all/{public_id}/export
```

They are undocumented and must not become unversioned architecture assumptions.
Any live access requires a later accepted provider contract with fixture-first
tests, failure behavior, rate/availability caveats, privacy boundaries, and no
hidden network dependency in the default test suite.

## Future Frequency Semantics

Default future metric:

```text
deck presence frequency
```

For Commander staple-style analysis, one deck contributes at most one presence
count per card by default. Total copy count may be added later only as an
explicit count mode and must not become the default.

Default sort:

```text
highest deck_count first
alphabetical within each frequency bucket
```

## Future Defaults

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

Default basic-land exclusion:

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

Future callers may override defaults only when that override remains visible
in the builder request, result, and exported frequency pool packet.

## Future Public Interface Guidance

A later implementation contract may authorize names similar to:

```text
MOXFIELD_FREQUENCY_POOL_BUILDER_VERSION
MoxfieldFrequencyPoolBuildError
MoxfieldDeckInputRef
MoxfieldDeckParseWarning
MoxfieldDeckParseFailure
MoxfieldParsedCard
MoxfieldParsedDeck
MoxfieldFrequencyPoolRequest
MoxfieldFrequencyPoolResult
build_moxfield_frequency_pool_request(...)
build_moxfield_frequency_pool_result(...)
validate_moxfield_frequency_pool_result(...)
moxfield_frequency_pool_result_to_dict(...)
```

These names are guidance only. Phase 38A does not add production Python files
or public symbols.

## Future Result Visibility

Future result packets must keep these fields visible when available:

```text
input_count
accepted_deck_count
failed_deck_count
duplicate_deck_count
partial_failure_count
included_sections
excluded_sections
exclude_basic_lands
card_name
deck_count
deck_total
frequency_percent
frequency_label
deck_ids_present
deck_names_present
deck_ids_missing
deck_names_missing
scryfall_id
oracle_id
unresolved
warnings
failures
caveats
```

Unknown, unavailable, unsupported, not applicable, and zero states must remain
distinct. Missing information must not silently become zero or false.

## Scryfall Identity Boundary

Future builder work may accept already-built Scryfall identity values or
already-built identity-resolution refs as input values. It must not override:

```text
Scryfall canonical card truth
scryfall_id identity semantics
oracle_id analytics grouping semantics
raw Scryfall payload preservation rules
Scryfall bulk snapshot versioning
Scryfall migration monitoring caveats
Scryfall Tagger ontology provenance
```

If card lookup fails, future behavior must preserve the raw card name, mark the
row unresolved, include it in the frequency pool, and surface an unresolved or
unsupported item rather than dropping it.

## Privacy Boundary

Moxfield text exports may contain private deck text. Future implementation must
preserve local-first privacy:

```text
private deck text remains local
raw imported deck text is not exported by default
private notes are not exported
full primer bodies are not exported
raw provider payloads are not exposed downstream
blocked private/raw metadata is rejected recursively
manual text input is user-local unless explicitly exported later
```

User-local Moxfield pools are observations, not tournament evidence, unless a
separate accepted source-lineage contract links a deck to a canonical
tournament record.

## Evidence And Recommendation Boundary

Future Moxfield frequency pools are evidence/reporting inputs only.

They must not:

```text
generate recommendations
rank cards for inclusion
choose cuts
claim optimality
infer pilot intent
produce deck health output
treat user deck pools as commander averages
treat Moxfield user decks as tournament evidence by default
feed Decision Intelligence without a later accepted contract
```

Future reports may say a card appears in N of M supplied decks. They may not
say the card should be played, cut, or included.

## Failure Codes

Future implementation should preserve explicit failure codes such as:

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
```

Partial failures must be reported. Failed decks must not be hidden from pool
coverage or result summaries.

## Future Fixture Requirements

Future tests must be fixture-first and must not depend on live Moxfield access.

Fixture inventory should include:

```text
successful Moxfield text export fixture
successful Moxfield URL payload fixture
mixed URL and text input fixture
private or unavailable deck failure fixture
malformed export fixture
unknown section fixture
duplicate deck input fixture
unresolved card fixture
Brigid five-deck manual frequency fixture
```

The Brigid fixture target from the roadmap patch should remain visible:

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

## Forbidden In Phase 38A

Phase 38A must not add:

```text
production Moxfield parser code
production Moxfield provider code
live Moxfield network calls
tests for implementation code
fixtures for implementation code
schema changes
repository changes
SQLite reads or writes
source table reads
raw provider payload reads
frequency calculation
analytics recalculation
Tag Graph metrics
export code
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

## Phase 38A Outside Validation Packet

Outside validation should review:

```text
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/CHECKPOINT_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_PROMPT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT.md
docs/CHECKPOINT_PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT_REPORT.md
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Outside validation must confirm that Phase 38A is contract-only and that Phase
38B remains blocked until Phase 38A returns PASS or PASS WITH REVIEW NOTES.

## Final Governance Summary

Phase 38A is complete when this contract, checkpoint, outside-validation
prompt, and governance records are internally consistent and accepted by PR
validation. It does not implement the Moxfield Frequency Pool Builder.

