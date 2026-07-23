# Phase 39C - Cockatrice Interoperability Implementation Report

Status: internal implementation complete

## Validation Tuple

```text
phase_id: Phase39C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Accepted Phase 39B Evidence

Phase 39B outside phase-ledger validation returned PASS.

```text
workflow run ID: 29973752107
validated SHA: 8296e473cc68dfd6dffcb5382de11d6327e5a69a
artifact: codie-phase_ledger-validation-8296e473cc68dfd6dffcb5382de11d6327e5a69a
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
unresolved findings: none
required corrections: none
```

## Scope Summary

Phase 39C implements the local, fixture-first, in-memory Cockatrice
interoperability packet surface authorized by Phase 39B.

The implementation accepts already supplied Cockatrice `.cod` XML payload text
and already supplied export card rows. It does not read arbitrary files, write
files, call live Cockatrice, call network APIs, call Scryfall, resolve card
identity, access SQLite, use repositories, calculate analytics, run simulator
logic, generate recommendations, produce deck health output, add UI or CLI
behavior, call LLMs, change dependencies, modify validators, modify workflows,
modify active validation scope, or modify either constitution.

## Files Changed

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
docs/PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Public Interface Implemented

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

## Behavior Implemented

```text
valid commander deck XML parses deterministically
partner commander deck XML preserves partner ordering
mainboard and sideboard remain distinct
custom zones create visible unsupported-zone records
malformed XML creates visible failure
unsafe XML with DTD or external entity declarations is rejected
unsupported format text creates visible failure
empty deck creates visible failure
unresolved card rows remain visible
duplicate card rows remain visible with caveat
privacy metadata is rejected recursively
import request refs do not preserve raw payload text
import packets serialize deterministically
export packets serialize deterministically
dictionary round-trip preserves all export packet fields
unknown, unavailable, unsupported, not-applicable, and zero states remain distinct
user-local import packets are labeled not_tournament_evidence
unresolved export rows can be preserved with caveats
unresolved export rows can be rejected with visible failures
```

## Boundary Preserved

```text
no file writing
no arbitrary file reading
no live Cockatrice process control
no live network calls
no Scryfall or provider calls
no card identity lookup calls
no SQLite or repository access
no analytics calculation
no frequency calculation
no recommendation generation
no deck health output
no simulator runtime behavior
no UI behavior
no CLI behavior
no LLM calls or SDK imports
no dependency changes
no workflow changes
no validator changes
no active validation scope changes
no constitution changes
```

Cockatrice user deck files remain user-local and are not tournament evidence by
default.

## Validation Notes

The configured Windows venv at
`C:\Users\Main\.venvs\codie-py312\Scripts\python.exe` failed to launch because
its launcher still points at a missing Python executable. Development
validation used the bundled runtime:

```text
C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Focused validation:

```text
C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.test_cockatrice_interoperability -v
Ran 18 tests
OK
```

Full validation results are recorded in the Phase 39C checkpoint.

## Final Governance Summary

Phase 39C implements the approved in-memory Cockatrice packet surface. Phase
39D remains blocked until Phase 39C returns PASS or PASS WITH REVIEW NOTES.
