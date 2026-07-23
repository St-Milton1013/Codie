# Checkpoint - Codie V2 Validator Authority and UTF-8

**Status:** Internal validation complete
**Verdict:** INTERNAL PASS, outside validation required

## Work completed

- Switched current validator report metadata and model review context from V1 to the official V2 constitution.
- Kept the validator report structure at schema version V1 while updating its constitutional metadata constraints.
- Protected both the historical V1 constitution and official V2 constitution from automated repair.
- Persisted UTF-8 Python behavior across all self-hosted validation and repair jobs.
- Hardened validator and repair subprocess text decoding against Windows locale-dependent failures.
- Added regression coverage for V2 authority, constitution protection, UTF-8 decoding, and workflow configuration.

## Files intentionally unchanged

```text
docs/CODIE_V1_CONSTITUTION.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
product runtime and provider modules
```

## Internal validation

```text
git diff --check: PASS
constitution preservation check: PASS - V1 and V2 unchanged
active validation-scope preservation check: PASS
schema bootstrap check: PASS
focused validation tests: PASS - 111 tests
full unit-test suite: PASS - 1,038 tests, 1 expected skip
```

The full suite used the repository-declared dependencies in the existing disposable test directory. Its package subdirectories require host-level read permission in this managed environment; the same suite passed after that read access was granted. No dependency or runtime files were changed.

Architecture and adversarial review remain required through the pull-request validation gate.

## Scope conclusion

This is a bounded validation-infrastructure correction. It does not advance Phase 37, implement a V2 capability, or alter prior phase acceptance.
