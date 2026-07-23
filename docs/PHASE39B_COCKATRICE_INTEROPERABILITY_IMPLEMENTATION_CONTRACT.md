# Phase 39B - Cockatrice Interoperability Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase39B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 39B narrows the future Cockatrice interoperability implementation.

This phase does not implement Cockatrice parsing, export packet builders, file
writing, CLI behavior, schema changes, repositories, provider calls, analytics,
recommendations, simulator execution, UI, LLM calls, workflow changes,
validator changes, dependency changes, active validation scope changes, or
constitution changes.

Phase 39B exists only to define the exact local, fixture-first implementation
surface that a later Phase 39C packet may add.

## Accepted Phase 39A Evidence

Phase 39A outside phase-ledger validation returned PASS WITH REVIEW NOTES.

```text
workflow run ID: 29969137239
validated SHA: bf1a966cbbf406820514ec1b2992688ed688bca1
artifact: codie-phase_ledger-validation-bf1a966cbbf406820514ec1b2992688ed688bca1
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with one INFORMATIONAL historical finding
aggregate: CLEAN_PASS
required corrections: none
```

The informational finding references historical Phase 36B contract narrative
and has `required_correction: None`. It is nonblocking and does not require
repair in Phase 39B.

## Phase 39B Scope

This phase may create or modify only:

```text
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

No production, test, fixture, schema, repository, provider, analytics,
recommendation, simulator, UI, CLI, LLM, workflow, validator, dependency,
active validation scope, export writer, file-writing, or constitution files are
authorized by Phase 39B.

## Future Phase 39C File Allowlist

This section is a textual future allowlist only. Phase 39B does not create any
of these files. A validator must distinguish textual references in this
contract from actual repository changes.

A later accepted Phase 39C implementation packet may add or modify only:

```text
codie/cockatrice/__init__.py
codie/cockatrice/interoperability.py
tests/test_cockatrice_interoperability.py
tests/fixtures/cockatrice/valid_commander_deck.cod
tests/fixtures/cockatrice/partner_commander_deck.cod
tests/fixtures/cockatrice/mainboard_sideboard.cod
tests/fixtures/cockatrice/custom_zone.cod
tests/fixtures/cockatrice/malformed_xml.cod
tests/fixtures/cockatrice/unsafe_xml_external_entity.cod
tests/fixtures/cockatrice/unsupported_format.txt
tests/fixtures/cockatrice/empty_deck.cod
tests/fixtures/cockatrice/unresolved_card_row.cod
tests/fixtures/cockatrice/duplicate_card_row.cod
tests/fixtures/cockatrice/privacy_metadata_failure.cod
tests/fixtures/cockatrice/round_trip_import_export.json
```

The `codie/cockatrice/__init__.py` file may expose symbols only. It must not
execute parser logic, load files, call providers, write files, or initialize
runtime services at import time.

Any broader file set requires a later contract amendment and must not be
introduced opportunistically in Phase 39C.

Phase 39B repository changes must remain limited to docs/governance files. If
`git diff --name-only` for Phase 39B shows any path under `codie/`, `tests/`,
or `tests/fixtures/`, Phase 39B must fail. Textual future path references in
this contract are not implementation files.

## Future Public Interface

Phase 39C may implement these public symbols:

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

Phase 39C must keep the implementation pure, in-memory, deterministic,
fixture-first, and local-input-only.

## Future Import Rules

Future import parsing may accept already-supplied Cockatrice `.cod` XML text or
fixture text only. It must not read arbitrary files from disk unless a later
file-reader contract authorizes that behavior.

Future import packets must preserve:

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

## Future Export Packet Rules

Future export packets may describe Cockatrice-compatible output from already
provided deck packet values. Phase 39C must not write bytes to disk.

Future export packets must preserve:

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

Any actual file writing requires a later safe-writer contract.

## Future Commander And Zone Rules

Future implementation must preserve Commander semantics:

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

Future implementation may preserve already-supplied Scryfall identity values or
already-built identity-resolution refs. It must not call Scryfall or invent
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

## Future XML Safety Rules

Future XML parsing must be local and deterministic. It must reject or visibly
fail unsafe XML input, including:

```text
external entities
DTD declarations
remote resource references
malformed XML
oversized payloads
unexpected root elements
unknown attributes that affect deck semantics
```

Future tests must prove that unsafe XML does not trigger network access,
external entity expansion, or remote resource loading.

## Future Privacy Boundary

Cockatrice files can contain user-local deck data. Future implementation must:

```text
keep local deck payloads local
avoid exporting raw imported deck text downstream by default
reject private notes recursively
reject full primer bodies recursively
reject raw provider payload metadata recursively
label user-local results as user-local when applicable
```

Cockatrice user decks are not tournament evidence by default.

## Future Evidence And Recommendation Boundary

Future Cockatrice interoperability is import/export packet support only. It
must not:

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

Future implementation must preserve explicit failure codes such as:

```text
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

## Future Dependency Limits

Allowed dependencies:

```text
Python standard library
existing Codie packet models explicitly named by the Phase 39C contract
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
LLM SDKs
server frameworks
UI frameworks
file-writing helpers
live Cockatrice process control
```

## Future Phase 39C Test Obligations

The following obligations are not Phase 39B completion criteria. Phase 39B is
complete when the implementation contract packet is validated. These
obligations become enforceable only against the later Phase 39C implementation
packet after Phase 39B is accepted.

The later Phase 39C implementation packet must include tests proving:

```text
valid commander deck XML parses deterministically
partner commander deck XML preserves partner ordering
mainboard and sideboard remain distinct
custom zones create visible unsupported-zone records
malformed XML creates visible failure
unsafe XML with external entity or DTD is rejected
unsupported file format is rejected
empty deck creates visible failure
unresolved card rows remain visible
duplicate card rows remain visible or deterministically merged with caveats
privacy metadata is rejected recursively
import packets serialize deterministically
export packets serialize deterministically
dictionary round-trip preserves all fields
unknown/unavailable/unsupported/not-applicable/zero states remain distinct
no live network dependencies exist
no schema, repository, provider, analytics, recommendation, simulator, UI, LLM,
or file-writing imports exist
```

An outside validator must not fail Phase 39B merely because these future
implementation tests do not exist yet. Phase 39B must be rejected only if it
implements production behavior early, omits the future requirements, or leaves
the Phase 39C boundary ambiguous.

## Forbidden In Phase 39B

Phase 39B must not add actual repository files or runtime behavior for:

```text
production Cockatrice parser code
production Cockatrice export code
implementation test files under tests/
fixture files under tests/fixtures/
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

The forbidden list above applies to actual repository changes, not to textual
future allowlist entries inside this implementation contract.

## Outside Validation Packet

Outside validation should review:

```text
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_PROMPT.md
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

Outside validation must confirm that Phase 39B is implementation-contract-only
and that Phase 39C remains blocked until Phase 39B returns PASS or PASS WITH
REVIEW NOTES.

## Final Governance Summary

Phase 39B is complete when this implementation contract, checkpoint report,
outside-validation prompt, and governance records are internally consistent and
accepted by PR validation. It does not implement Cockatrice interoperability.
