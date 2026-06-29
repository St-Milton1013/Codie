# Phase 13B - Probability Engine Core Models Contract

## Purpose

Implement pure in-memory Python-native probability engine models from Phase
13A.

This packet does not add shuffle, mulligan, search, action execution, Monte
Carlo behavior, Challenge Mode, schema changes, or recommendation integration.

## Files Created

```text
codie/probability_engine/__init__.py
codie/probability_engine/models.py
tests/test_probability_engine_models.py
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_CONTRACT.md
docs/PHASE13B_PROBABILITY_ENGINE_CORE_MODELS_REPORT.md
```

## Files Modified

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/NEXT_PHASE_CONTRACT.md
```

## Public Classes

```text
ManaCost
ManaOption
SimulationActionModel
SimulationCardModel
SimulationTargetCondition
SimulationConfig
SimulationDeckCard
SimulationDeck
SimulationUnsupportedItem
SimulationTraceAction
SimulationTrace
SimulationResult
```

## Schema Impact

None.

## Dependency Impact

None.

## Boundary Rules

The probability engine model layer must not import:

```text
codie.providers
codie.db
codie.analytics
codie.recommendations
sqlite3
requests
httpx
```

## Required Behavior

- Models are dataclasses.
- Models validate required fields.
- Mana costs use stable W/U/B/R/G/C/Generic ordering.
- Mana options preserve explicit restrictions.
- Action models preserve unknown metadata for future handlers.
- Card models preserve raw reference shape.
- Config models require seed and version fields.
- Deck models preserve unresolved cards.
- Unsupported items are explicit and serializable.
- Trace actions preserve order.
- Results carry unsupported items and raw payload metadata.

## Do Not Do

- Do not implement seeded shuffle.
- Do not implement mulligan logic.
- Do not implement mana payment.
- Do not implement target search.
- Do not implement card behavior execution.
- Do not implement Challenge Mode.
- Do not add schema.
- Do not copy cEDHData source code.
