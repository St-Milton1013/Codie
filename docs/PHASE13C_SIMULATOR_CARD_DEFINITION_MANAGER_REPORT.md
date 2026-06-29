# Phase 13C - Simulator Card Definition Manager Contract Report

## Verdict

```text
Phase 13C Simulator Card Definition Manager Contract: PASS
```

## Objective

Define the simulator card definition manager contract before implementation.

This packet keeps Codie contract-first and prevents the probability engine from
turning into an unbounded Magic rules engine.

## Files Created

```text
docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md
docs/PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_REPORT.md
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

- Defined Phase 13D implementation scope.
- Defined allowed and forbidden dependencies.
- Defined Scryfall identity layer versus simulator behavior overlay.
- Defined relevance classifications.
- Defined unsupported relevant and unsupported irrelevant handling.
- Defined confidence levels.
- Defined required card definition manager output.
- Defined evidence and recommendation boundaries.
- Defined Phase 13D acceptance tests.

## Validation Performed

Full suite:

```text
python -m unittest discover -s tests

Ran 331 tests in 2.459s

OK (skipped=1)
```

Static checks:

```text
git diff --check
```

passed.

Strategic-language scan:

```text
rg -n "[strategic-claim blocklist]" docs\PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_CONTRACT.md docs\PHASE13C_SIMULATOR_CARD_DEFINITION_MANAGER_REPORT.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

returned only existing governance scan commands, neutral contract wording, and
the explicitly documented forbidden wording section.

Implementation leakage scan:

```text
rg -n "class CardDefinitionManager|def classify_card_relevance|data/sim_cards" codie tests
```

returned no matches.

## Boundary Notes

- No simulator behavior implementation was added.
- No behavior overlay fixture files were added.
- No schema changes were added.
- No persistence was added.
- No seeded shuffle, mulligan logic, target search, action execution, or
  Challenge Mode was added.
- No cEDHData source code or full card data was copied.

## Recommended Next Step

```text
Phase 13D - Simulator Card Definition Manager Implementation
```

Implement the contract with pure in-memory behavior overlay loading, relevance
classification, unsupported-card reporting, and focused fixture tests.
