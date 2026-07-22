# Phase 39A - Cockatrice Interoperability Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase39A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 39A defines the future Cockatrice Interoperability boundary.

The future track may let Codie import and export local Cockatrice-compatible
deck files for portability and local testing. Phase 39A itself does not
implement parsers, exporters, schema, repositories, provider calls, UI, CLI,
file-writing behavior, analytics, recommendations, simulator execution, LLM
calls, workflow changes, validator changes, dependency changes, or constitution
changes.

## Accepted Phase 38D Evidence

Phase 38D outside phase-ledger validation returned CLEAN_PASS.

```text
workflow run ID: 29964132762
validated SHA: 38b3fc9d7cc812062674ae0615d7d5733c4b5401
artifact: codie-phase_ledger-validation-38b3fc9d7cc812062674ae0615d7d5733c4b5401
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
unresolved findings: none
```

## Roadmap Source

Phase 39A follows Priority 7 from
`docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md`.

The first contract must define:

```text
supported file formats
deck import/export fields
commander section handling
sideboard/zone handling
card name resolution
unsupported card reporting
privacy boundaries
```

## Phase 39A Scope

This phase may create or modify only:

```text
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
docs/CHECKPOINT_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

No production, test, fixture, schema, repository, provider, analytics,
recommendation, simulator, UI, CLI, LLM, workflow, validator, dependency,
active validation scope, export, file-writing, or constitution files are
authorized by Phase 39A.

## Future Authorized Direction

A later accepted implementation contract may authorize local, fixture-first
model and implementation planning for:

```text
Cockatrice deck file references
Cockatrice XML deck import packet models
Cockatrice deck export packet models
deck name and metadata fields
zone and section mapping
commander and partner commander handling
mainboard and sideboard handling
maybeboard or custom zone preservation
card quantity parsing
card name preservation
already-supplied card identity references
unsupported or unresolved card reporting
deterministic serialization
round-trip dictionary-compatible forms
local fixture inventory
```

Phase 39B is reserved for the implementation-contract packet. Phase 39B must
not become production implementation unless its accepted contract explicitly
narrows and authorizes that work.

## Future Supported Formats

Future contracts may support only local files or already-supplied text payloads.

Initial format targets:

```text
Cockatrice deck XML
Cockatrice-compatible .cod file content
plain text fallback only if explicitly contracted later
```

Future tests must be fixture-first and must not depend on external Cockatrice
installations, live services, network access, or user-specific local paths.

## Future Import Field Rules

Future import packets should preserve these fields when available:

```text
source_format
source_file_label
deck_name
deck_metadata
zone_name
section_name
card_name
quantity
raw_name
scryfall_id
oracle_id
unresolved
warnings
failures
unsupported_items
```

Unknown, unavailable, unsupported, not applicable, and zero states must remain
distinct. Missing information must not silently become zero or false.

## Future Export Field Rules

Future export packets may describe Cockatrice-compatible output from already
provided deck packet values. A future writer contract is required before bytes
are written to disk.

Future export models should preserve:

```text
target_format
deck_name
zone mappings
card rows
quantities
commander rows
sideboard rows
unresolved card rows
unsupported export caveats
privacy caveats
```

Phase 39A does not authorize file writing.

## Future Commander And Zone Rules

Future Cockatrice interoperability must handle Commander deck semantics
explicitly:

```text
commander section remains distinct from mainboard
partner commanders remain distinct and ordered deterministically
mainboard remains distinct from sideboard
custom zones are preserved as unsupported or explicitly mapped
unknown zones create visible warnings or failures
unknown zones must not be silently included in mainboard
unknown zones must not be silently dropped
```

## Future Card Identity Rules

Future Cockatrice work may preserve already-supplied Scryfall identity values
or already-built identity-resolution refs. It must not call Scryfall or invent
card identity.

Required behavior:

```text
preserve raw card names
preserve supplied scryfall_id when available
preserve supplied oracle_id when available
mark unresolved card rows visibly
emit unsupported card reporting when identity is missing or ambiguous
do not mutate Scryfall truth
do not change scryfall_id identity semantics
do not change oracle_id analytics grouping semantics
```

## XML Safety Rules

Future XML parsing must be local and deterministic.

Future contracts must reject or safely handle:

```text
external entities
DTD declarations
remote resource references
malformed XML
oversized payloads
unexpected root elements
unknown attributes that affect deck semantics
```

No future Cockatrice parser may fetch remote resources during tests or default
runtime.

## Privacy Boundary

Cockatrice files may contain user-local deck data. Future implementation must
preserve local-first privacy:

```text
local deck files remain local input
raw imported deck text is not exported downstream by default
private notes are rejected recursively
full primer bodies are rejected recursively
raw provider payload metadata is rejected recursively
Cockatrice user decks are not tournament evidence by default
user-local results remain visibly user-local when applicable
```

## Evidence And Recommendation Boundary

Future Cockatrice interoperability is import/export support only. It must not:

```text
generate recommendations
rank cards for inclusion
choose cuts
claim optimality
infer pilot intent
produce deck health output
treat Cockatrice user decks as commander averages
treat Cockatrice user decks as tournament evidence by default
feed Decision Intelligence without a later accepted contract
```

Reports may say a card exists in a supplied Cockatrice deck file. They may not
say the card should be played, cut, or included.

## Future Failure Codes

Future implementation should preserve explicit failure codes such as:

```text
COCKATRICE_FILE_UNAVAILABLE
COCKATRICE_XML_MALFORMED
COCKATRICE_XML_UNSAFE
COCKATRICE_UNSUPPORTED_FORMAT
COCKATRICE_UNKNOWN_ZONE
COCKATRICE_EMPTY_DECK
COCKATRICE_CARD_UNRESOLVED
COCKATRICE_DUPLICATE_CARD_ROW
COCKATRICE_EXPORT_UNSUPPORTED_CARD
COCKATRICE_PRIVACY_METADATA_REJECTED
```

Partial failures must remain visible. Failed imports must not be hidden from
coverage or result summaries.

## Future Fixture Requirements

Future tests must be fixture-first and must not depend on a live Cockatrice
installation.

Fixture inventory should include:

```text
valid commander deck XML
partner commander deck XML
mainboard and sideboard XML
custom zone XML
malformed XML
unsafe XML with external entity or DTD
unsupported file format
empty deck
unresolved card row
duplicate card row
privacy metadata failure
round-trip import/export model fixture
```

## Future Public Interface Guidance

A later implementation contract may authorize names similar to:

```text
COCKATRICE_INTEROPERABILITY_VERSION
CockatriceInteropBuildError
CockatriceDeckFileRef
CockatriceDeckCard
CockatriceDeckZone
CockatriceImportWarning
CockatriceImportFailure
CockatriceExportWarning
CockatriceExportFailure
CockatriceImportOptions
CockatriceExportOptions
CockatriceImportedDeck
CockatriceExportPacket
build_cockatrice_import_request(...)
parse_cockatrice_deck_payload(...)
build_cockatrice_export_packet(...)
validate_cockatrice_imported_deck(...)
validate_cockatrice_export_packet(...)
cockatrice_imported_deck_to_dict(...)
cockatrice_export_packet_to_dict(...)
```

These names are guidance only. Phase 39A does not add production Python files
or public symbols.

## Future Dependency Limits

Allowed future dependencies:

```text
Python standard library
existing Codie packet models explicitly authorized by a later contract
```

Forbidden dependencies unless separately contracted:

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
LLM SDKs
server frameworks
UI frameworks
file-writing helpers
live Cockatrice process control
```

## Forbidden In Phase 39A

Phase 39A must not add:

```text
production Cockatrice parser code
production Cockatrice export code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
SQLite reads or writes
provider changes
live Cockatrice calls
network calls
card identity lookup calls
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
active validation scope changes
constitution changes
```

## Outside Validation Packet

Outside validation should review:

```text
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
docs/CHECKPOINT_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

Outside validation must confirm that Phase 39A is contract-only and that Phase
39B remains blocked until Phase 39A returns PASS or PASS WITH REVIEW NOTES.

## Final Governance Summary

Phase 39A is complete when this contract, checkpoint report,
outside-validation prompt, and governance records are internally consistent and
accepted by PR validation. It does not implement Cockatrice interoperability.
