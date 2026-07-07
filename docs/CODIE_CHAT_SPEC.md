# Codie Chat Specification

Status: roadmap/specification, implementation deferred

## Purpose

Add a Codie chat tab that lets the user interrogate Codie's local database and
reports.

This must be a grounded intelligence layer, not a generic chat box.

## Supported Question Classes

Future chat may support:

```text
why a card appears in an evidence or recommendation surface
common commander cards
deck comparison against top lists
draw engine evidence
incomplete package evidence
simulation result interpretation
deck snapshot changes
source conflict review
unsupported simulator cards that affect results
tag graph interpretation
frequency pool comparison
commander staples retrieval
```

## Architecture Direction

```text
local chat UI
retrieval from SQLite through approved read layers
optional sqlite-vec semantic retrieval layer
hard grounding against canonical records
evidence citations in answers
```

## Rules

```text
chat must not invent card stats
if Codie cannot find evidence, it must say so
LLM language is optional and must come after structured retrieval
LLM output is never source truth
private user deck text requires explicit opt-in before cloud use
```

## Current Phase Relationship

Phase 20 starts with query planning only:

```text
sanitized user question -> deterministic ChatQueryPlan
```

Chat answer building, UI, LLM writer/auditor, retrieval persistence, and
semantic search require future contracts.

## Acceptance Tests

```text
answers only from retrieved Codie evidence
shows when evidence is missing
can explain a recommendation
can summarize a deck health warning
can compare frequency pool cards
can retrieve commander staples
```
