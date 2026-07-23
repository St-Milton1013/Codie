# Codie V2 Validator Authority and UTF-8 Contract

**Status:** Bounded validation-infrastructure contract
**Date:** 2026-07-21

## Objective

Align Codie's automated validation reports and review context with the ratified V2 constitution, retain V1 as a protected historical reference, and make UTF-8 decoding persistent and deterministic on the self-hosted Windows validation runner.

## Authorized files

```text
.github/workflows/codie-local-validation.yml
codie/validation/local_gate.py
codie/validation/repair_controller.py
schemas/codie_validator_report_v1.schema.json
tests/test_validation_local_gate.py
tests/test_validation_repair_controller.py
docs/CODIE_V2_VALIDATOR_AUTHORITY_UTF8_CONTRACT.md
docs/CHECKPOINT_CODIE_V2_VALIDATOR_AUTHORITY_UTF8_REPORT.md
docs/OUTSIDE_VALIDATION_CODIE_V2_VALIDATOR_AUTHORITY_UTF8_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required behavior

- New validator reports identify `docs/CODIE_V2_CONSTITUTION.md` and `codie.constitution.v2`.
- Architecture and adversarial review context includes V2, not V1, as governing authority.
- Both V1 and V2 are protected from automated repair.
- Every job in the local-validation workflow inherits `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`.
- Validator and repair subprocess output is decoded as UTF-8 with replacement for malformed external bytes, so decoding cannot crash the gate.
- The validator report schema version remains `codie.validator.report.v1`; only its required constitutional authority metadata changes.

## Protected invariants

```text
docs/CODIE_V1_CONSTITUTION.md remains byte-for-byte unchanged
docs/CODIE_V2_CONSTITUTION.md remains byte-for-byte unchanged
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json remains unchanged
Phase 37 status and validation tuple remain unchanged
validator severities, outcomes, models, and timeouts remain unchanged
no paid API or cloud dependency is introduced
```

## Prohibited scope

```text
constitution text edits
product runtime features
provider or data-source changes
database or migration changes
Phase 37 advancement
validation weakening
repair access to either constitution
```

## Acceptance criteria

- Runtime report metadata and checked-in JSON Schema require the V2 path and version.
- V2 is present and V1 is absent from the current model review context.
- Repair path tests prove that both constitutions are protected.
- A regression test proves subprocess text output requests UTF-8 decoding.
- A workflow regression test proves the UTF-8 environment is persistent.
- Schema bootstrap, focused validator tests, full tests, and `git diff --check` pass.
- Neither constitution nor the active validation-scope file changes.
- Outside architecture and adversarial validation return no blocking findings.
