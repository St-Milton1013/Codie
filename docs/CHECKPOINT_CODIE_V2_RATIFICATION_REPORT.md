# Checkpoint — Codie V2 Constitution Ratification

**Status:** Internal governance checkpoint
**Verdict:** INTERNAL PASS, outside validation required

## Work completed

- Added the ratified V2 constitution candidate.
- Preserved V1 unchanged as historical reference.
- Added the formal V1/V2 change log.
- Added compatibility and ratification contracts.
- Reconciled the constitution with explicit user decisions and the Codie/Jin handoff.
- Kept Phase 37 and runtime implementation outside the packet.

## Design decisions

- V2 becomes authoritative on merge, not merely when a branch exists.
- Relationship Intelligence is a typed, metric-only evidence subsystem.
- All V1 capabilities carry forward except the folded standalone query helper and deferred mobile report delivery.
- Core capabilities and implementation sequence remain separate: constitutional inclusion does not bypass contracts.

## Files intentionally unchanged

```text
docs/CODIE_V1_CONSTITUTION.md
codie/
tests/
schemas/
.github/workflows/
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Internal validation

```text
git diff --check: PASS
V1 content comparison against origin/main: PASS (unchanged)
Markdown heading, stale-draft-language, and encoding scans: PASS
schema bootstrap check: PASS
full unit-test suite: PASS — 1,033 tests, 1 expected skip
```

The full suite used the repository-declared `requirements.txt` dependencies in a disposable test directory because the configured project virtual environment points to a removed local Python installation. No dependency or runtime files were changed by this packet.

Architecture and adversarial review remain required through the outside/PR validation gate.

## Next step

Send the adoption packet through pull-request validation. Only accepted validation and merge make V2 the official repository constitution.
