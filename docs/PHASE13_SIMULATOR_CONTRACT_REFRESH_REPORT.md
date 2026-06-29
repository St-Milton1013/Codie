# Phase 13 - Simulator Contract Refresh Report

## Verdict

```text
Phase 13 Simulator Contract Refresh: PASS
```

## Objective

Refresh the probability engine, Challenge Mode, and simulator review contracts
before implementation begins.

## Files Created

```text
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Functions / Classes Added

None.

## Schema Impact

None.

## Dependency Impact

None.

## Work Completed

- Reconciled constitution simulator requirements with the accepted Challenge
  Mode roadmap patch.
- Identified current simulation persistence tables and repository support.
- Flagged reproducibility fields that are currently implicit in JSON payloads
  rather than explicit schema columns.
- Defined simulator boundary rules.
- Defined reproducibility requirements.
- Defined MVP scope and non-goals.
- Defined Challenge Mode rules.
- Defined line review/veto annotation rules.
- Defined simulation Evidence Stack gate conditions.
- Defined recommended build order for Phase 13A onward.

## Required Review Notes

The existing schema can persist initial simulator configs through
`raw_config_json` and result details through `raw_payload_json`, but explicit
columns for seed/version/unsupported-item metadata should be considered before
broad simulator usage.

Challenge Mode and line review require future schema contracts before
implementation.

## Validation Performed

Full Python suite:

```text
Ran 319 tests in 2.547s

OK (skipped=1)
```

Whitespace validation:

```text
git diff --check
```

passed with no output.

Strategic-language scan:

```text
rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|you should" docs\PHASE13_SIMULATOR_CONTRACT_REFRESH.md docs\PHASE13_SIMULATOR_CONTRACT_REFRESH_REPORT.md
```

returned only the contract's explicit forbidden-answer examples and future test
requirement wording. A narrowed scan over the report, next-phase document, and
handoff found only existing scan-command text.

Implementation-wording scan:

```text
rg -n "simulator code added|schema changes added|dependencies added|Challenge Mode implementation added|line review implementation added" docs\PHASE13_SIMULATOR_CONTRACT_REFRESH.md docs\PHASE13_SIMULATOR_CONTRACT_REFRESH_REPORT.md
```

returned only explicit "not added" boundary notes.

## Boundary Notes

- No simulator code added.
- No schema changes added.
- No dependencies added.
- No recommendation output added.
- No Challenge Mode implementation added.
- No line review implementation added.

## Recommended Next Step

```text
Phase 13A - Probability Engine Core Models
```

Purpose:

Define and implement the pure in-memory models for target conditions, configs,
decks, card models, unsupported items, results, and traces before any search or
Monte Carlo behavior is added.
