# Outside Validation Prompt - Phase 39C Cockatrice Interoperability Implementation

You are validating Codie Phase 39C.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

## Required Verdict Context

Phase 39C implements local, fixture-first, in-memory Cockatrice
interoperability packet models, validators, XML payload parsing, and export
packet builders.

Phase 39C must not implement file writing, arbitrary file reading, live
Cockatrice calls, network calls, Scryfall/provider calls, card identity lookup
calls, SQLite reads or writes, repositories, analytics, recommendations, deck
health output, simulator runtime behavior, UI, CLI behavior, LLM calls,
workflow changes, validator changes, dependency changes, active validation
scope changes, or constitution changes.

Phase 39D remains blocked until Phase 39C outside validation returns PASS or
PASS WITH REVIEW NOTES.

## Required Review Files

Review:

```text
docs/PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_PROMPT.md
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
docs/CHECKPOINT_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_REPORT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
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
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Confirm Phase 39B Acceptance

Confirm the governance documents record Phase 39B as PASS using:

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

## Confirm Validation Tuple

Confirm Phase 39C explicitly declares:

```text
phase_id: Phase39C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Do not accept ambiguous next-phase scope.

## Confirm Public Interface

Confirm the public interface includes:

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

## Required Behavior Checks

Confirm tests or implementation cover:

```text
valid commander deck XML parses deterministically
partner commander deck XML preserves partner ordering
mainboard and sideboard remain distinct
custom zones create visible unsupported-zone records
malformed XML creates visible failure
unsafe XML with external entity or DTD declarations is rejected
unsupported format text creates visible failure
empty deck creates visible failure
unresolved card rows remain visible
duplicate card rows remain visible with caveat
privacy metadata is rejected recursively
import request refs do not preserve raw payload text
import packets serialize deterministically
export packets serialize deterministically
dictionary round-trip preserves export packet fields
unknown/unavailable/unsupported/not-applicable/zero states remain distinct
Cockatrice user-local import packets are labeled not_tournament_evidence
unresolved export rows can be preserved with caveats
unresolved export rows can be rejected with visible failures
```

## Required Rejection Conditions

Reject if Phase 39C:

```text
writes Cockatrice files
reads arbitrary files through public parser functions
calls live Cockatrice
calls network APIs
calls Scryfall or providers
performs card identity lookup
imports sqlite3
imports codie.db or repositories
imports analytics
imports recommendations
imports Decision Intelligence
imports Evidence Fusion
imports simulator runtime
adds UI behavior
adds CLI behavior
calls LLMs or imports LLM SDKs
changes schema
changes dependencies
changes workflow or validator code
changes docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
changes docs/CODIE_V1_CONSTITUTION.md
changes docs/CODIE_V2_CONSTITUTION.md
generates recommendations
generates deck health output
treats Cockatrice user decks as tournament evidence by default
silently drops unknown zones
silently drops unresolved card rows
silently expands XML external entities
```

## Required Commands

From a clean checkout, run:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

If the configured Python environment cannot launch, report the environment
blocker honestly and do not claim that environment passed.

## Static Scans

Run:

```text
git diff --name-only
git diff --name-only -- schemas codie/db codie/providers codie/analytics codie/recommendations codie/decision_intelligence codie/evidence_fusion codie/probability_engine codie/cli .github requirements.txt requirements-dev.txt docs/CODIE_ACTIVE_VALIDATION_SCOPE.json docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md
rg -n "requests|httpx|sqlite3|codie\\.db|codie\\.providers|codie\\.analytics|codie\\.recommendations|codie\\.decision_intelligence|codie\\.evidence_fusion|openai|anthropic|fastapi|flask|uvicorn" codie/cockatrice tests/test_cockatrice_interoperability.py
rg -n "recommend|should play|should cut|optimal|strict upgrade|deck health" codie/cockatrice tests/test_cockatrice_interoperability.py
```

Matches inside explicit forbidden-boundary test lists are allowed. Production
Cockatrice code must not import forbidden dependencies.

## Required Output

Report:

```text
implementation report verdict
checkpoint document verdict
outside validation prompt verdict
Phase 39B acceptance evidence status
Phase 39C validation tuple status
Phase 39D blocker status
required fixes, if any
review notes, if any
final decision
```
