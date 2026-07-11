# Roadmap Patch - Codie Master Architecture

Status: architecture approved / implementation deferred

This document is the consolidated architecture specification covering:

```text
Simulator Revision (SIM-R1 / SIM-R2)
Forge validation boundaries
Scryfall Bulk Data foundation
Scryfall Migration monitoring
Scryfall Tagger functional ontology
Commander Spellbook interpreter
Cockatrice interoperability
Primer ingestion
Plugin architecture
Immutable snapshots
Confidence, coverage, explainability
Smart enrichment
Conversation summaries
Testing strategy
Validation requirements
```

This roadmap patch does not authorize implementation, schema changes, new
repositories, new providers, LLM calls, UI work, file writing, simulator runtime
changes, recommendation output, or dependency changes until a future contract
explicitly approves that scope.

## Core Principles

Deterministic systems create facts.

Jin only reads and explains those facts.

Pipeline:

```text
Input
-> Canonicalization
-> Validation
-> Evidence Classification
-> Selective Enrichment
-> Graph Linking
-> Analysis
-> Confidence
-> Coverage
-> Explainability
-> Jin
-> Conversation Summary
-> Snapshot
```

## Locked Decisions

```text
1. Hybrid card behavior model.
2. LLM is read-only.
3. Immutable deck snapshots.
4. Graph contains only provable relationships.
5. Plugin architecture with validator reviewing every changed file.
6. Demand-driven enrichment with background processing.
7. Class 0 includes Scryfall, Rules, Tagger functional data, Commander Spellbook, and deterministic Codie outputs.
8. Simulator coverage targets tournament-played Commander cards.
9. Unit, integration, property, replay, golden-deck, and performance tests.
10. Conversation summaries are automatically drafted and manually saveable.
11. Confidence exposed on every result.
12. Explainability required project-wide.
13. Architecture supports all Commander through analysis profiles.
```

## Simulator

Approved:

```text
Immutable SimulationState
Resource Ledger
Behavior Modules
Compound Targets
State Hashing
Dominance Pruning
Paired Simulation
Trace v2
```

Rejected:

```text
Full rules engine
Opponent AI
Combat engine
Full Forge runtime
Z3 solver
LLM-authored behavior
```

## Combo Interpretation

```text
Parse prerequisites, steps, outputs, and restrictions.
Infinite draw = WIN.
Infinite mana requires compatible Tagger mana sink.
No combo ranking.
No deck-intent inference.
Jin interprets but never changes deterministic classifications.
```

## Scryfall Foundation

```text
Bulk data discovery
Atomic snapshots
Migration monitoring
Symbol normalization
```

## Tagger

Use:

```text
General tags
Functional card tags
Card relationships
```

Ignore:

```text
Artwork tags
```

## Validation

```text
Nothing is implemented until the active validation chain completes.
Every implementation must submit every changed file to validation.
```

## Relationship To Existing Architecture Patches

This patch consolidates and reinforces existing accepted roadmap direction in:

```text
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/ROADMAP_PATCH_EVIDENCE_ARCHITECTURE_REMASTER.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/ROADMAP_PATCH_SIMULATOR_CARD_DEFINITION_MANAGER.md
```

Where this document conflicts with an already accepted phase contract, the
accepted phase contract remains authoritative until a future contract explicitly
updates it.

## Backtracking Assessment

No completed phase requires immediate backtracking from this patch.

The patch strengthens existing principles already used throughout Codie:

```text
deterministic systems create facts
LLMs remain read-only/explanatory
simulator outputs remain evidence only
Tagger functional data remains ontology/reference data
Forge remains validation/reference only
snapshots and replayability are required for future stateful workflows
```

Future work should integrate these details contract-first rather than modifying
accepted implementation retroactively.
