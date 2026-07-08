# Roadmap Patch - Codie Architecture Revision III

Status: approved for roadmap integration

This patch supersedes earlier evidence-architecture drafts where they conflict.

## Purpose

Codie is an evidence-driven intelligence platform, not a collection of
independent analytics.

Every subsystem should answer:

```text
What evidence supports this conclusion?
```

No subsystem may invent independent reasoning.

This is a roadmap-only architecture patch. It does not authorize implementation,
schema changes, new repositories, new providers, LLM calls, UI work, file
writing, simulator behavior changes, or recommendation output until a future
contract explicitly approves the scope.

## Evidence Class Hierarchy

```text
Class 0 Authority Layer
  Class 0A Rules & Card Authority
  Class 0B Combo Authority

Class 1 Observational Data

Class 2 Measured Evidence

Primer Context Extraction

Evidence Fusion

Class 3 Decision Intelligence

Class 4 User Context

UI / Reports / Chat / Exports
```

## Class 0 - Authority Layer

Purpose:

Provide authoritative Magic knowledge.

Nothing in lower classes may contradict Class 0.

### Class 0A - Rules & Card Authority

Sources:

- Official Comprehensive Rules
- Official Oracle rulings
- Official release notes
- Official ban/restricted announcements
- Scryfall

Scryfall is promoted to Class 0 authority for Codie.

Scryfall is authoritative for:

- Oracle text
- card identity
- card names
- Oracle IDs
- Scryfall IDs
- mana cost
- color identity
- type line
- legalities
- rulings
- search syntax

Rule:

```text
Nothing inside Codie may override Scryfall card information.
```

### Class 0B - Combo Authority

Source:

```text
Commander Spellbook
```

Commander Spellbook is authoritative for:

- combo existence
- combo requirements
- combo outcomes
- combo variants

Rule:

```text
If Commander Spellbook recognizes a combo, Codie recognizes it.
No confidence score is required for combo existence.
```

## Class 1 - Observational Data

Purpose:

Store observations.

Class 1 performs no calculations, no opinions, and no reasoning.

Sources:

- TopDeck
- EDHTop16
- MTGTop8
- MTGDecks
- Hareruya
- Moxfield deck imports

Examples:

- decklists
- pilots
- placements
- tournaments
- commanders
- event metadata

Rule:

```text
Observational data is ingestion-only.
Observational data may never generate recommendations.
```

## Class 2 - Measured Evidence

Purpose:

Generate mathematical observations from Class 1.

Examples:

- inclusion rate
- frequency
- trend lines
- co-occurrence
- lift
- support
- confidence
- deck similarity
- package frequency
- simulator statistics
- card performance metrics
- commander staples statistics

Requirements:

```text
No opinions.
Fully reproducible.
Same input always produces same output.
```

## Primer Context Extraction

Purpose:

Extract useful strategic context.

Sources:

- Moxfield primers
- Moxfield deck descriptions

Outputs:

- archetype hints
- strategy summaries
- mulligan philosophy
- pilot priorities
- meta assumptions
- flex slot explanations

Rule:

```text
Primer context may explain evidence.
Primer context may never override evidence.
```

## Evidence Fusion

Purpose:

Merge:

- Authority
- Measured Evidence
- Primer Context

Output:

```text
Unified Evidence Objects
```

Rules:

```text
Every downstream system consumes Unified Evidence.
No downstream system accesses raw data directly for reasoning.
```

## Class 3 - Decision Intelligence

Purpose:

Generate conclusions.

Examples:

- recommendations
- deck health
- package detection
- commander staples
- source agreement
- recommendation confidence
- replacement engine
- evidence graph
- historical comparisons
- recommendation simulator

Rule:

```text
Decision Intelligence owns reasoning.
No other subsystem should duplicate reasoning.
```

## Class 4 - User Context

Purpose:

Personalize recommendations.

Examples:

- owned cards
- collection
- budget
- ignored cards
- testing notes
- local meta
- preferences

Rule:

```text
User Context personalizes outputs.
It never changes global evidence.
```

## Rules Layer

The Rules Layer is independent.

It is not part of Evidence Fusion.

Uses:

- chat explanations
- simulator legality validation
- card interaction explanations

Never:

- recommendations
- deck health
- confidence
- analytics

## Jin-Gitaxias Strategist Mode

Subsystem:

```text
Codie Strategist
```

Purpose:

Act as an interactive cEDH theory partner.

Jin-Gitaxias is not another recommendation engine. It is a conversational
theory engine.

Supported questions:

- archetype blending
- commander comparisons
- package design
- strategy discussions
- deck philosophy
- build direction
- thought experiments

Example:

```text
I want Rograkh / Silas built like Rograkh / Ishai.
```

The strategist should explain:

- transferable ideas
- non-transferable ideas
- color identity limitations
- package differences
- strategic implications
- testing recommendations

## Jin-Gitaxias Data Access

May read:

- Authority Layer
- Observational Data
- Measured Evidence
- Primer Context

May never write back into:

- tournament evidence
- measured evidence
- confidence metrics
- recommendations
- staples
- package statistics

May write only to future approved:

- theory notes
- experiment queue
- user testing notes

This prevents theory contamination.

## Jin-Gitaxias Safety Architecture

Pipeline:

```text
Prompt
  ->
Retrieval Planner
  ->
Evidence Retrieval
  ->
Primary Strategist Model
  ->
Evidence Gate
  ->
Legality Validator
  ->
Contradiction Scanner
  ->
Optional Auditor Model
  ->
Final Answer
```

## Auditor Model

Primary model:

```text
Creates answer.
```

Auditor model:

```text
Attempts to disprove answer.
```

Checks:

- unsupported claims
- contradictory evidence
- illegal cards
- impossible interactions
- overconfidence

Only difficult theory discussions should invoke the auditor. Routine factual
questions should not.

## Safety Valves

Every Strategist answer reports:

- Evidence Level: High / Medium / Low
- Speculation Level: High / Medium / Low
- Source Coverage: Strong / Partial / Weak
- Unsupported Claims Removed count
- Illegal Suggestions Blocked count
- Confidence Ceiling Applied: Yes / No

## Confidence Ceiling

Confidence may never exceed evidence quality.

Examples:

```text
Single primer -> Low confidence
Tournament agreement -> High confidence
Conflicting evidence -> Medium confidence
```

## Legality Validation

Before output, all card suggestions must pass:

- color identity
- commander legality
- format legality
- deck construction rules

Class 0 provides explanation.

Scryfall provides validation.

## Evidence Weights

Weights become configurable and never hardcoded.

Profiles:

- Competitive Default
- Tournament Heavy
- Simulation Heavy
- Primer Aware
- Budget Aware

Profiles are versioned.

Old reports remain reproducible.

## Source Agreement

Agreement labels:

- Strong
- Mixed
- Weak

Detailed explanation appears only when expanded.

## Recommendation Confidence

Every recommendation includes:

- confidence
- impact
- evidence summary
- agreement level

## Explainability

Every recommendation supports expansion.

Collapsed:

- recommendation
- confidence
- summary

Expanded:

- evidence
- contradictions
- simulation
- weight contribution
- source references

## Card Replacement Engine

Recommendations prefer replacement framing:

```text
Replace
  ->
With
  ->
Reason
```

Reasons include:

- role overlap
- statistical improvement
- package synergy
- matchup improvement
- simulator impact

## Recommendation Simulator

Simulation should evaluate only meaningful decisions.

Examples:

- mana packages
- tutor packages
- interaction density
- draw engines
- protection
- combo packages

Avoid simulating universally accepted staples unless explicitly requested.

## User Interface Philosophy

Primary rule:

```text
Action First.
Never Trivia First.
```

Dashboard should answer:

```text
What deserves attention?
```

Suppress:

- obvious staples
- redundant confirmations
- universally accepted cards already present

Highlight:

- missing packages
- role imbalance
- simulation-impacting changes
- conflicting evidence
- confidence concerns
- actionable upgrades

## Decision Evidence Panel

Merge:

- explainability
- confidence
- agreement
- simulator
- replacement logic
- evidence weights

into one expandable panel.

This becomes the explanation hub.

## Reference Catalog

Reference repositories remain reference-only.

Rules:

- mtg-comprehensive-rules
- RulesParser
- mtg-cr
- mtg-rules

Infrastructure:

- sqlite-vec
- LocalSend

MTG:

- MTGJSON
- Commander Spellbook backend
- Moxfield parser references

Graph:

- Cytoscape references

Reference repositories never become production dependencies without validation.

## Governing Rules

1. No recommendation may originate from raw provider data.
2. Every recommendation must flow through Evidence Fusion.
3. Primer context explains; it never defines truth.
4. Jin-Gitaxias may theorize; it may never contaminate measured evidence.
5. Authority Layer overrides every lower layer.
6. Scryfall is equal in authority to official rules for card identity and legality.
7. Commander Spellbook is authoritative for combo existence.
8. Every factual claim generated by an LLM must pass evidence validation before presentation.

## Expected Outcome

This architecture transforms Codie from a statistics viewer into an
evidence-driven cEDH intelligence platform capable of:

- deterministic analytics
- explainable recommendations
- grounded theory discussions
- reproducible conclusions
- controlled speculation
- low-hallucination conversational reasoning

Future features must integrate with this architecture rather than creating
independent reasoning systems.
