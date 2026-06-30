# Phase 13I - Mulligan Policy Contract Report

## Verdict

```text
Phase 13I Mulligan Policy Contract: PASS
```

## Objective

Define London mulligan policy inputs, decision boundaries, bottoming behavior,
trace metadata, and allowed outputs before implementation begins.

This packet is contract-only.

## Files Created

```text
docs/PHASE13I_MULLIGAN_POLICY_CONTRACT.md
docs/PHASE13I_MULLIGAN_POLICY_CONTRACT_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

## Dependency Impact

None.

## Work Completed

- Defined Phase 13J implementation scope.
- Defined London mulligan simplification.
- Defined policy config fields.
- Defined keep/reject decision output.
- Defined bottoming rules.
- Defined mulligan result and step output.
- Defined seed/reproducibility rules.
- Defined unresolved-card handling.
- Defined evidence and recommendation boundaries.
- Defined Phase 13J acceptance tests.

## Validation Performed

Full suite:

```text
python -m unittest discover -s tests

Ran 369 tests in 2.602s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Implementation leakage scan:

```text
rg -n "MulliganPolicyConfig|simulate_london_mulligan|evaluate_opening_hand|MulliganResult" codie tests
```

returned no matches.

Strategic-language scan:

```text
rg -n "[strategic-claim blocklist]" docs\PHASE13I_MULLIGAN_POLICY_CONTRACT.md docs\PHASE13I_MULLIGAN_POLICY_CONTRACT_REPORT.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

returned only existing governance scan commands and the explicitly documented
forbidden wording section.

## Boundary Notes

- No mulligan code was added.
- No target search was added.
- No action execution was added.
- No Monte Carlo batch runner was added.
- No schema changes were added.
- No persistence was added.
- No Challenge Mode was added.
- No cEDHData source code or full card data was copied.

## Recommended Next Step

```text
Phase 13J - Mulligan Policy Implementation
```

Implement deterministic policy evaluation, London mulligan attempt tracking,
bottoming, and result serialization with focused reproducibility tests.
