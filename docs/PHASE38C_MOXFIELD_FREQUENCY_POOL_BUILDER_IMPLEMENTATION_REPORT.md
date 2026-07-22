# Phase 38C - Moxfield Frequency Pool Builder Implementation Report

Status: implementation packet prepared

## Validation Tuple

```text
phase_id: Phase38C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase38D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 38C implements the accepted Phase 38B contract for a local, fixture-first
Moxfield Frequency Pool Builder.

The implementation parses already supplied Moxfield-style text exports and
already supplied local fixture payloads into Frequency Pool packet-compatible
output. It does not fetch Moxfield URLs, call Moxfield APIs, call Scryfall,
rewrite providers, read or write SQLite, write files, add CLI or UI behavior,
run analytics, run simulator logic, call LLMs, or generate recommendations.

## Accepted Phase 38B Evidence

Phase 38B outside phase-ledger validation returned CLEAN_PASS.

```text
workflow run ID: 29936658939
validated SHA: e132ca12598c9112d5729300c53d13a398b44f9d
artifact: codie-phase_ledger-validation-e132ca12598c9112d5729300c53d13a398b44f9d
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
unresolved findings: none
```

The active validation scope was advanced separately to Phase38C and validated:

```text
workflow run ID: 29936996144
validated SHA: 47756ffaa641a733f47e4ffe9720e7132590f236
artifact: codie-phase_ledger-validation-47756ffaa641a733f47e4ffe9720e7132590f236
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
```

## Changed Files

```text
codie/frequency_pools/moxfield_builder.py
codie/frequency_pools/__init__.py
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
docs/PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Interface Implemented

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

## Behavior Implemented

```text
extracts public Moxfield IDs from supported URL shapes
rejects malformed Moxfield URLs cleanly
parses local Moxfield-style export sections
includes mainboard by default
excludes commander sections by default
excludes sideboard, maybeboard, considering, and tokens by default
excludes basic lands by default
records section override settings visibly
uses deck presence frequency by default
keeps total copy count visibly separate from deck presence
deduplicates repeated card names within one deck for presence counting
detects duplicate deck inputs before they contribute frequency
preserves partial failures
preserves unresolved card rows
preserves raw names for unresolved rows
builds FrequencyPoolPacket-compatible output
keeps user-local and not-tournament-evidence labels visible
produces deterministic serialization
round-trips through dictionary-compatible form
does not mutate input payloads
rejects private deck text and private notes recursively
rejects raw provider payload metadata recursively
rejects recommendation/action language
reproduces the Brigid five-deck frequency bucket fixture shape
```

The Brigid fixture target is synthetic to avoid copying private or licensed
deck contents, but it preserves the contracted bucket shape:

```text
49 cards at 5/5
27 cards at 4/5
17 cards at 3/5
22 cards at 2/5
37 cards at 1/5
```

## Boundary Preserved

Phase 38C does not add:

```text
live Moxfield calls
Moxfield provider adapter changes
Scryfall lookup calls
schema changes
repository changes
SQLite reads or writes
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

## Validation

To be run before PR submission:

```text
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_moxfield_frequency_pool_builder -v
python -m unittest discover -s tests -v
```

## Final Governance Summary

Phase 38C is complete when the implementation report, checkpoint,
outside-validation prompt, implementation files, tests, fixtures, and
governance records are accepted by PR validation. Phase 38D remains blocked
until Phase 38C receives PASS or PASS WITH REVIEW NOTES.

