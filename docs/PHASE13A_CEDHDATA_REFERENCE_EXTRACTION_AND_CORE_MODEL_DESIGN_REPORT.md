# Phase 13A - cEDHData Reference Extraction And Core Model Design Report

## Verdict

```text
Phase 13A cEDHData Reference Extraction And Core Model Design: PASS
```

## Objective

Use the user-supplied cEDHData reference files to extract architecture and data
shape lessons, then design a clean Python-native Codie probability engine model
layer.

## Files Created

```text
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Reference Files Inspected

```text
C:\Users\Main\Downloads\cedhdata_cards.json
C:\Users\Main\Downloads\cedhdata_simulator_main_bundle.js
```

The original reference source files were not copied into Codie.

## Public Functions / Classes Added

None.

## Schema Impact

None.

## Dependency Impact

None.

## Work Completed

- Inspected the cEDHData card catalog shape.
- Identified key simulator card fields and action containers.
- Identified behavior/action categories needed by Codie.
- Confirmed bundle-level architecture concepts such as deck parsing, seeded
  mulligans, winning-line search, mana payment, target access, unsupported-card
  reporting, and trace export versioning.
- Designed Codie-native Python model shapes for the next implementation packet.
- Preserved the rule that reference files are research fixtures only.

## Validation Performed

Full Python suite:

```text
Ran 319 tests in 2.482s

OK (skipped=1)
```

Whitespace validation:

```text
git diff --check
```

passed with no output.

Source-copy risk scan:

```text
rg -n "simulateMulliganForSeed|findWinningLine|playKeptHand|function |=>|const |let |var " docs\PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md docs\PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md
```

returned only three function names listed as architecture concepts. No copied
JavaScript source was added.

Reference-file scan:

```text
rg -n "cedhdata_cards\.json|cedhdata_simulator_main_bundle\.js" .gitignore docs reference codie tests
```

returned only documentation references to the local input paths. The supplied
large reference files were not copied into Codie.

Strategic-language scan:

```text
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md docs\PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md
```

returned no matches.

## Boundary Notes

- No cEDHData JavaScript was copied into Codie.
- No cEDHData JSON fixture payload was copied into Codie.
- No simulator implementation was added.
- No schema changes were added.
- No recommendation output was added.

## Recommended Next Step

```text
Phase 13B - Probability Engine Core Models Implementation
```

Purpose:

Implement the pure Python-native model layer described in Phase 13A before any
shuffle, mulligan, action search, or Monte Carlo behavior is added.
