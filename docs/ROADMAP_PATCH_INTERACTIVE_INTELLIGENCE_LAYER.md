# Roadmap Patch - Interactive Intelligence Layer

## Purpose

Codie should eventually include a structured chat interface inside the UI.

This chat must not be a generic LLM box. It must be a Codie intelligence layer
that routes user questions through local Codie data, evidence builders,
simulation outputs, review queues, and explicit uncertainty reporting before
language is produced.

This is a roadmap-only packet. It does not authorize implementation, schema
changes, LLM calls, recommendation output changes, primer body storage, or UI
work until a future contract explicitly approves the scope and tests the
guardrails.

## UI Placement

Future UI should add a permanent tab:

```text
Chat with Codie
```

Major tabs may also expose a right-side chat panel:

```text
Overview
Recommendations
Tournament Meta
Primers
Combos
Packages
Probability Lab
Compare
Deck Memory
Review Queue
Source Conflicts
```

## Supported Question Classes

The chat layer should eventually support questions about:

- current deck analysis
- commander evidence
- why a card appears in an evidence/recommendation surface
- missing evidence cards
- low-evidence or outlier cards
- incomplete packages
- tournament evidence
- primer summaries
- probability and simulation results
- changes between saved deck versions
- possible duplicate sources/events/decks
- unsupported simulator cards that materially affect results

Any "what to cut" or "what is missing" answer must remain evidence-first. Codie
may describe evidence, deltas, confidence, and unsupported assumptions. It must
not present unsupported strategic coaching as truth.

## Future Backend Modules

Candidate module layout:

```text
codie/intelligence/
  chat_router.py
  query_planner.py
  evidence_graph.py
  answer_builder.py
  citation_builder.py
  tool_registry.py
  context_builder.py
  safety_limits.py
```

## Future Feature Modules

Candidate feature module layout:

```text
codie/features/
  evidence_graph/
  sim_confidence/
  package_health/
  change_impact/
  deck_memory/
  unsupported_queue/
  source_conflicts/
  primer_summary/
```

## Candidate Tables

Potential tables for a future contract:

```text
chat_sessions
chat_messages
chat_context_snapshots
analysis_evidence_nodes
analysis_evidence_edges
simulation_confidence_reports
package_health_reports
deck_snapshots
deck_snapshot_cards
deck_change_reports
unsupported_relevant_cards
source_conflict_reports
primer_summaries
```

These table names are roadmap candidates only. They are not approved schema
until a schema contract defines ownership, indexes, foreign keys, retention
rules, privacy rules, and repository coverage.

## Evidence Graph

Every major Codie answer should expose evidence nodes.

Example answer structure:

```text
Claim:
This deck has Turbo Naus evidence.

Evidence:
- Ad Nauseam package detected
- Fast-mana density is high relative to selected comparison set
- Tutor density is high relative to selected comparison set
- Similar canonical tournament decks carry sourced Turbo labels
- Primer metadata contains fast Ad Nauseam claims
- Simulator shows modeled early access, with unsupported-card caveats
```

Allowed evidence node types:

```text
card
package
commander
deck
tournament_stat
primer_signal
simulation_result
source_conflict
manual_note
```

Evidence graphs are explanation artifacts. They do not replace canonical
records, source provenance, or raw simulator traces.

## Simulation Confidence Report

Every chat-visible simulation result should include:

```text
confidence_level
modeled_relevant_cards
unsupported_relevant_cards
unsupported_irrelevant_cards
invalidating_missing_models
warning_text
```

Confidence levels:

```text
high
medium
low
invalid
```

Unsupported simulator cards must not be silently ignored.

## Package Health Report

For every detected package, Codie should eventually report evidence-based
package status:

```text
complete
partial
overbuilt
under-supported
missing enabler
missing payoff
missing protection
missing tutor access
```

Package health is an evidence summary, not an unsupported instruction.

## Change Impact Simulator

Future chat may let a user propose:

```text
cut X
add Y
```

Codie may compare:

```text
package health before/after
simulation target access before/after
mana curve change
color requirement change
tournament similarity change
primer support change
recommendation score change
```

Change impact must be generated from Codie tools and local data. It must show
confidence and missing-model caveats.

## Deck Memory And Snapshots

Future analysis runs should save searchable deck snapshots containing:

```text
commander
partner commander
decklist
deck hash
source URL
date analyzed
detected archetype evidence
detected packages
recommendation/evidence surfaces
simulation results
primer links
evidence graph
unsupported card report
```

Snapshots should be retrievable from chat, for example:

```text
How did my Heliod list change since last week?
```

Private user deck snapshots must not be sent to cloud LLMs or third-party
services unless the user explicitly opts in through a future contract.

## Unsupported Relevant Card Queue

When unsupported simulator-relevant cards appear, Codie should eventually record:

```text
card
oracle_id
deck
commander
why relevant
missing behavior type
priority
decks affected
first_seen
last_seen
```

This queue should drive future simulator expansion and regression tests. It
must not hide unsupported cards from users.

## Source Conflict Detector

Codie should eventually flag possible duplicate or conflicting records across:

```text
TopDeck
EDHTop16
MTGTop8
MTGDecks
Hareruya
```

Conflicts may include:

```text
same event, different source
same deck, different source
same player/date/commander overlap
player count conflicts
placement conflicts
decklist differences
```

Analytics must continue to use only canonical deduped records. Source conflict
reports are review aids, not direct analytics inputs.

## Primer Summarization

Codie may eventually summarize primers, but must not store full primer text
permanently.

Allowed stored fields:

```text
primer URL
deck URL
commander
partner
author
section headings
summary
archetype claims
mulligan guidance summary
combo/package mentions
card role notes
last checked date
quality score
```

Forbidden stored fields:

```text
full copied primer body
long quoted sections
full strategy guide text
```

Primer summaries must keep source attribution and must not become tournament
evidence.

## Chat Answer Rule

Chat answers must use Codie tools first, LLM language second.

Required order:

```text
user question
identify needed data
query Codie database/tools
build evidence graph
produce answer
show uncertainty/confidence
```

Forbidden order:

```text
user question
LLM guesses from memory
```

## LLM Guardrails

If an LLM is used for answer phrasing, it must:

- receive structured Codie context rather than raw unrestricted project memory
- cite supplied evidence node IDs or citations
- preserve uncertainty and unsupported-card warnings
- avoid strategic claims that exceed the evidence
- avoid storing or replaying private deck text without explicit consent
- remain disabled or local-only when sensitive inputs are not approved for
  cloud processing

LLM output is never a source of truth.

## Acceptance Criteria For Future Implementation

This roadmap patch can be considered implemented only when Codie can:

1. Chat about the currently loaded deck.
2. Explain answers with evidence nodes.
3. Show simulation confidence.
4. Report package health.
5. Compare proposed card swaps.
6. Save and retrieve deck snapshots.
7. Maintain unsupported relevant card queue.
8. Detect source conflicts before analytics.
9. Summarize primers without storing full primer bodies.
10. Answer "why?" questions using structured Codie data.

## Phase Placement

Recommended future placement:

```text
Phase 15+ after simulator export/CLI surfaces and deck snapshot persistence are stable
```

Do not start this before contract-first decomposition into smaller packets.

Suggested split:

1. Evidence graph contract.
2. Deck snapshot contract.
3. Unsupported relevant card queue contract.
4. Source conflict report contract.
5. Primer summary contract.
6. Chat query planner contract.
7. Chat answer builder contract.
8. UI/API contract.

## Do Not Do Yet

- do not add chat UI
- do not add schema
- do not add LLM calls
- do not store primer bodies
- do not create recommendation claims from chat
- do not let chat read provider payloads directly
- do not let chat mutate simulator traces
- do not let chat bypass canonical analytics boundaries
