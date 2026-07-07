# Roadmap Patch - Evidence Intelligence, Frequency Pools, Local Reports, and Supporting References

Status: roadmap-only, implementation deferred

## Purpose

This patch updates Codie after removing the Stream Deck Game Tracker from
active V1 scope.

Codie remains focused on:

```text
local-first cEDH intelligence
deck analysis
tournament-backed recommendations
frequency and co-occurrence analytics
primer intelligence
simulation support
evidence graphs
exportable reports
```

This patch does not authorize schema changes, production code, provider calls,
UI work, LocalSend integration, vector search, recommendation output, or live
network dependencies. Each implementation area requires its own contract.

## Removed Scope

Remove from active Codie V1 scope:

```text
Stream Deck Game Tracker
SpellBot live-game tracking
Convoke live-game tracking
Commander tax / life / storm / treasure live UI
real-time game-state controller
replay logger from live game buttons
```

Reason:

```text
This is a separate companion app, not a deck intelligence feature.
```

It would require hardware-specific development, live game-state synchronization,
real-time multiplayer logic, custom in-game UI, and long-term maintenance
outside Codie's core purpose.

Decision:

```text
Do not include Stream Deck Game Tracker in Codie V1.
Only reconsider later as a separate app that can export logs into Codie.
```

## Accepted Active Change List

The active roadmap direction now includes:

```text
Deck Health Dashboard
Card Co-occurrence Metrics
Evidence-Based Recommendation Engine
Automatic Frequency Pool Generation
Commander Staples Database
Integrated Natural Language Chat
Evidence Graph / Explainable Analytics
Scryfall Tagger Multi-Tag Graphing
Non-MTG Core Infrastructure Improvements
LocalSend Integration for report delivery
```

## Dependency Order

Future implementation should proceed in this order:

```text
1. Canonical deck/card foundation
2. Scryfall + Tagger role mapping
3. Frequency pool generation
4. Commander staples snapshots
5. Co-occurrence metrics
6. Recommendation evidence model
7. Deck Health Dashboard
8. Evidence Graph
9. Codie Chat
10. LocalSend delivery
```

Reason:

```text
Chat and graph surfaces must not be built before the evidence exists.
```

## New Specification Files

This patch creates:

```text
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
docs/REPO_REFERENCE_CATALOG.md
docs/FEATURE_SCOPE_REMOVALS.md
docs/LOCAL_REPORT_DELIVERY.md
docs/EVIDENCE_GRAPH_SPEC.md
docs/CO_OCCURRENCE_METRICS_SPEC.md
docs/FREQUENCY_POOL_SPEC.md
docs/COMMANDER_STAPLES_SPEC.md
docs/CODIE_CHAT_SPEC.md
```

## Planned Table Candidates

Future contracts may evaluate:

```text
card_cooccurrence_metrics
tag_frequency_metrics
frequency_pool_runs
frequency_pool_cards
commander_staples_snapshots
commander_staples_cards
recommendation_evidence
evidence_graph_nodes
evidence_graph_edges
chat_sessions
chat_messages
chat_retrieval_events
export_jobs
localsend_delivery_logs
```

These are not approved schema. Any table requires a future schema contract,
repository coverage, idempotency rules, rebuild rules where derived, tests, and
outside validation.

## Strategic Summary

Codie's intended V1 identity is:

```text
canonical cEDH data
+ commander staples
+ frequency pools
+ co-occurrence intelligence
+ deck health diagnostics
+ evidence-backed recommendations
+ simulation support
+ primer intelligence
+ explainable graph UI
+ local report export
+ chat-based analysis
```

Central rule:

```text
No raw scraped source directly powers analytics.
Everything must flow through canonical records.
```

Codie is a local-first cEDH intelligence platform that explains deck structure,
evidence, gaps, and competitive context with provenance.
