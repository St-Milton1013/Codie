# Outside Validation Prompt - Codie V2 Validator Authority and UTF-8

Validate this packet as a bounded validation-infrastructure correction.

## Required review files

```text
docs/CODIE_V2_VALIDATOR_AUTHORITY_UTF8_CONTRACT.md
docs/CHECKPOINT_CODIE_V2_VALIDATOR_AUTHORITY_UTF8_REPORT.md
codie/validation/local_gate.py
codie/validation/repair_controller.py
schemas/codie_validator_report_v1.schema.json
.github/workflows/codie-local-validation.yml
tests/test_validation_local_gate.py
tests/test_validation_repair_controller.py
```

## Required determinations

Confirm that:

1. New reports require `docs/CODIE_V2_CONSTITUTION.md` and `codie.constitution.v2`.
2. Model validators receive V2 as current constitutional context and do not receive V1 as governing context.
3. The report schema remains structurally compatible as `codie.validator.report.v1`.
4. Both V1 and V2 are protected against automated repair.
5. UTF-8 configuration applies to pull-request validation, manual validation, snapshot validation, and repair jobs.
6. Subprocess output cannot fail solely because the Windows locale cannot decode valid UTF-8 text.
7. Encoding failures are made observable through replacement characters rather than hidden by validation weakening.
8. Validator models, timeouts, severities, aggregation outcomes, cost policy, and exact-SHA controls are unchanged.
9. Neither constitution nor the active Phase 37 scope is modified or advanced.

## Reject for

- any V1 or V2 constitution text change;
- V1 remaining the authority for newly generated validation reports;
- either constitution becoming writable by automated repair;
- UTF-8 settings that apply to only some workflow paths;
- loss of validation findings, errors, exact-SHA checks, or paid-API prohibitions;
- product runtime or Phase 37 scope changes.

## Outcomes

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```
