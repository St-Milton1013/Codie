# Phase 13W - Reviewed Simulator Accuracy Contract Report

## Verdict

```text
Phase 13W Reviewed Simulator Accuracy Contract: PASS
```

## Objective

Define reviewed simulator accuracy reporting before implementation.

This packet is contract-only.

## Files Created

```text
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md
docs/PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Schema Impact

None.

Phase 13X must use the existing `simulation_line_reviews` table.

## Dependency Impact

None.

The contract requires reviewed accuracy to remain read-only simulator QA
metadata, not analytics, recommendations, or tournament evidence.

## Work Completed

- Defined Phase 13X implementation scope.
- Defined reviewed accuracy filters.
- Defined required summary fields.
- Defined classification rules for accepted/rejected/failed/unsupported rows.
- Defined status, reason, affected-card, and affected-action counts.
- Defined rate behavior when denominators are zero.
- Defined evidence-language restrictions.
- Defined repository boundary and forbidden imports.
- Defined Phase 13X validation tests.

## Validation Performed

Full suite:

```text
python -m unittest discover -s tests

Ran 467 tests in 2.802s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Implementation leakage scan:

```text
rg -n "ReviewedAccuracy|reviewed_accuracy|list_line_reviews_for_accuracy" codie tests
```

returned no matches.

Strategic-language scan:

```text
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT.md docs\PHASE13W_REVIEWED_SIMULATOR_ACCURACY_CONTRACT_REPORT.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

returned only scan-command text and existing governance guardrail wording.

## Boundary Notes

- No schema changes added.
- No reporting code added.
- No repository methods added.
- No UI added.
- No recommendation output added.
- No analytics output added.
- No simulator trace mutation added.

## Recommended Next Step

```text
Phase 13X - Reviewed Simulator Accuracy Implementation
```

Implement the read-only summary model, repository query, tests, and report
defined by the Phase 13W contract.
