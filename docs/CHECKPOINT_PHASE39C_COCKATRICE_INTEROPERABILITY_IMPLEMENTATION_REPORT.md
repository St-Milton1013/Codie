# Checkpoint - Phase 39C Cockatrice Interoperability Implementation

Status: internal pass pending validation

## Validation Tuple

```text
phase_id: Phase39C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Scope Summary

Phase 39C implements local, fixture-first Cockatrice interoperability packet
models, validators, XML payload parsing, and export packet builders. It remains
pure, in-memory, deterministic, file-writing-free, provider-free,
repository-free, analytics-free, recommendation-free, simulator-free,
UI-free, CLI-free, LLM-free, workflow-free, validator-free, dependency-free,
and constitution-free.

## Accepted Phase 39B Evidence

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

## Behavior Verified

```text
Phase 39B is recorded as PASS.
Phase 39B artifact evidence remains visible.
Phase 39C declares phase_id, phase_part, and gate_scope.
Phase 39C declares next_phase_id, next_phase_part, and next_gate_scope.
Cockatrice import request refs do not retain raw payload text.
Valid commander deck XML parses deterministically.
Partner commander deck XML preserves partner ordering.
Mainboard and sideboard remain distinct.
Custom zones create visible unsupported-zone records.
Malformed XML creates visible failure.
Unsafe XML with external entity or DTD declarations is rejected.
Unsupported format text creates visible failure.
Empty deck creates visible failure.
Unresolved card rows remain visible.
Duplicate card rows remain visible with caveat.
Privacy metadata is rejected recursively.
Import packets serialize deterministically.
Export packets serialize deterministically.
Dictionary round-trip preserves export packet fields.
Unknown, unavailable, unsupported, not-applicable, and zero states remain distinct.
User-local import packets are labeled not_tournament_evidence.
Unresolved export rows can be preserved with caveats.
Unresolved export rows can be rejected with visible failures.
Phase 39D remains blocked until Phase 39C returns PASS or PASS WITH REVIEW NOTES.
```

## Boundary Verified

```text
no file writing
no arbitrary file reading
no live Cockatrice process control
no network calls
no Scryfall calls
no provider imports
no card identity lookup calls
no SQLite imports
no repository imports
no analytics imports
no recommendation imports
no Decision Intelligence imports
no Evidence Fusion imports
no simulator runtime imports
no UI imports
no CLI behavior
no LLM SDK imports
no dependency changes
no workflow changes
no validator changes
no active validation scope changes
no constitution changes
```

## Validation Commands

The configured Windows venv failed to launch:

```text
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest tests.test_cockatrice_interoperability -v
Unable to create process using '"C:\Users\Main\AppData\Local\Programs\Python\Python312\python.exe" ...'
```

Validation used the bundled Python runtime:

```text
C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

Focused tests:

```text
C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest tests.test_cockatrice_interoperability -v
Ran 18 tests
OK
```

Full validation:

```text
$env:PYTHONPATH='C:\Users\Main\.venvs\codie-py312\Lib\site-packages'
C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m unittest discover -s tests -v
Ran 1092 tests
OK (skipped=1)
```

## Static Scan Expectations

Outside validation should confirm:

```text
git diff --check
git diff --name-only
git diff --name-only -- schemas codie/db codie/providers codie/analytics codie/recommendations codie/decision_intelligence codie/evidence_fusion codie/probability_engine codie/cli .github requirements.txt requirements-dev.txt docs/CODIE_ACTIVE_VALIDATION_SCOPE.json docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md
rg -n "requests|httpx|sqlite3|codie\\.db|codie\\.providers|codie\\.analytics|codie\\.recommendations|codie\\.decision_intelligence|codie\\.evidence_fusion|openai|anthropic|fastapi|flask|uvicorn" codie/cockatrice tests/test_cockatrice_interoperability.py
rg -n "recommend|should play|should cut|optimal|strict upgrade|deck health" codie/cockatrice tests/test_cockatrice_interoperability.py
```

Matches inside explicit forbidden-boundary test lists are allowed. Production
Cockatrice code must not import forbidden dependencies.

## Final Decision

```text
Phase 39C checkpoint: INTERNAL PASS
Phase 39D: BLOCKED until Phase 39C outside validation returns PASS or PASS WITH REVIEW NOTES
```
