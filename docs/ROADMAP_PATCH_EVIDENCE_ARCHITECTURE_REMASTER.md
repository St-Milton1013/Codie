# Roadmap Patch - Evidence Architecture Remaster

Version: Architecture Revision 2

## Purpose

This patch restructures how Codie reasons.

Previous roadmap versions focused on adding more analytics. This revision
changes the future architecture so every reasoning feature consumes a common
body of evidence instead of implementing independent reasoning.

Objectives:

- eliminate duplicated logic
- improve explainability
- increase confidence
- simplify future feature development
- make every conclusion reproducible

This is a roadmap-only architecture patch. It does not authorize implementation,
schema changes, new providers, new repositories, recommendation output, LLM
calls, UI changes, or simulator behavior changes until a future contract
explicitly approves them.

## Architectural Principle

No feature should reason independently.

Every feature should consume the same evidence.

Future architecture:

```text
Class 0 Rules & Standards
Independent Reference Layer

Class 1 Canonical Truth
  ->
Class 2 Observational Data
  ->
Class 3 Measured Evidence
  ->
Primer Context Extraction
  ->
Evidence Fusion
  ->
Class 4 Decision Intelligence
  ->
Class 5 User Context
  ->
UI / Reports / Chat / Exports
```

## Class 0 - Rules & Standards

Purpose:

Provide authoritative references explaining how Magic functions.

Class 0 does not participate in recommendations. It exists only for:

- rule explanations
- card interaction explanations
- simulator validation
- chat answers about game mechanics

Primary truth sources:

- Official Comprehensive Rules
- Official Oracle rulings
- Official release notes
- Official format legality announcements

Reference repositories:

- sethwoodworth/mtg-comprehensive-rules
- dgulyas/RulesParser
- pit142857/mtg-cr
- machinaut/mtg-rules
- MTGRuler

Rules:

```text
GitHub repositories never override official documentation.
Simulator behavior may reference Class 0.
Recommendations may not use Class 0 as recommendation evidence.
```

## Class 1 - Canonical Truth

Purpose:

Store objective game information.

Sources:

```text
Scryfall
Commander Spellbook
```

Scryfall provides:

- Oracle text
- card identity
- type line
- mana cost
- color identity
- legalities
- IDs
- rulings linkage

Commander Spellbook provides:

- combo existence
- combo requirements
- combo outcomes
- combo variants

Rule:

```text
Commander Spellbook combo information is treated as canonical truth.
If Spellbook lists a combo, Codie accepts it as fact.
No confidence calculation is required for combo existence.
```

## Class 2 - Observational Data

Purpose:

Capture real-world observations.

Class 2 performs no calculations and no reasoning. It records what happened.

Sources:

- TopDeck
- EDHTop16
- MTGTop8
- MTGDecks
- Hareruya
- Moxfield deck imports

Examples:

- tournament placement
- pilot
- commander
- deck contents
- event date
- match record

Rule:

```text
Observational data never produces recommendations directly.
```

## Class 3 - Measured Evidence

Purpose:

Generate mathematical observations from Class 2.

Class 3 produces no opinions and no interpretation.

Outputs:

- frequency
- inclusion rate
- win rate
- top-cut percentage
- card performance metrics
- trend lines
- co-occurrence
- lift
- support
- confidence
- similarity
- simulator statistics
- package frequency

Rule:

```text
All calculations must be reproducible.
Same input data must always produce the same output.
```

## Primer Context Extraction

This replaces the previously proposed interpretive layer.

Purpose:

Extract useful strategic context without treating it as objective truth.

Sources:

- Moxfield primers
- Moxfield deck descriptions

Outputs:

- archetype hints
- mulligan philosophy
- strategy summaries
- flex slot explanations
- pilot priorities
- meta assumptions

Rules:

```text
Primer context may explain evidence.
Primer context may never override objective evidence.
Primer context is context, not truth.
```

Example:

```text
Objective evidence:
Deck contains twelve interaction spells.

Primer context:
This list intentionally increases interaction because the expected meta is control-heavy.

Interpretation:
The primer explains the observation. It does not create it.
```

## Evidence Fusion

Purpose:

Merge objective evidence with contextual signals.

Inputs:

```text
Class 1 Canonical Truth
Class 3 Measured Evidence
Primer Context
```

Output:

```text
Unified evidence objects
```

Rule:

```text
Every downstream feature consumes unified evidence objects.
No feature accesses raw evidence directly for reasoning.
```

## Class 4 - Decision Intelligence

Purpose:

Generate conclusions.

Outputs:

- recommendations
- deck health
- replacement suggestions
- commander staples
- package detection
- recommendation confidence
- source agreement
- explainability
- evidence graph
- simulator comparisons
- historical comparisons

Rule:

```text
Decision Intelligence owns reasoning.
No other subsystem should duplicate reasoning logic.
```

## Class 5 - User Context

Purpose:

Personalize decisions.

Examples:

- owned cards
- budget
- local meta
- testing notes
- ignored cards
- collection
- preferences

Rule:

```text
User Context personalizes outputs.
It never changes global evidence.
```

## Evidence Weight Tuning

Weights become configurable, never hardcoded.

Future implementation should store versioned analysis profiles.

Example profiles:

- Tournament Focus
- Simulation Focus
- Primer Aware
- Budget Aware
- Competitive Default

Requirement:

```text
Weight profiles must be versioned.
Old analyses must remain reproducible.
```

## Recommendation Confidence

Every future recommendation receives:

- confidence
- expected impact
- source agreement
- evidence summary

Rule:

```text
Recommendations without sufficient evidence should not be generated.
```

## Source Agreement

Codie should measure agreement between evidence sources.

Labels:

- Strong
- Mixed
- Weak

Detailed breakdown should appear only when expanded.

## Explainability

Every recommendation must support an expandable explanation.

Collapsed view:

- recommendation
- confidence
- summary

Expanded view:

- evidence
- supporting metrics
- contradictions
- simulation
- weight contribution
- source references

## Card Replacement Knowledge

Recommendations should prefer replacements over isolated additions.

Example:

```text
Replace Card A with Card B.

Reason:
- same functional role
- higher performance
- better package support
- improved matchup profile
```

## Recommendation Simulator

Simulation should run only for meaningful changes.

Examples:

- mana changes
- tutor changes
- package completion
- draw engine changes
- protection packages
- fast mana changes

Avoid simulations for universally accepted staples unless explicitly requested.

## User Interface Philosophy

Primary principle:

```text
Action First.
Not Information First.
```

The dashboard should answer:

```text
What needs my attention?
```

Not:

```text
What facts already exist?
```

## Dashboard Priorities

Default dashboard:

- highest-value upgrades
- missing packages
- role imbalance
- deck health warnings
- simulation-impacting changes
- conflicting evidence
- confidence concerns
- meta shifts

Suppress:

- obvious staples
- redundant confirmations
- universally accepted inclusions already present
- low-value informational clutter

## Decision Evidence Panel

Instead of multiple dashboard widgets, merge these into one expandable panel:

- confidence
- agreement
- simulation
- explainability
- replacement logic
- evidence weights

This becomes the primary explanation interface.

## Rules For Surfacing Information

Do not surface:

```text
Sol Ring is good.
```

Do surface:

```text
Sol Ring is absent.
This omission significantly impacts opening acceleration.
Recent tournament lists differ from this build.
```

Only present information that enables a decision.

## GitHub Reference Catalog Additions

Add to the reference catalog:

Rules:

- mtg-comprehensive-rules
- RulesParser
- mtg-cr
- mtg-rules

Infrastructure:

- sqlite-vec
- LocalSend

MTG:

- Commander Spellbook backend
- MTGJSON
- Moxfield parser references

Graph UI:

- Cytoscape / graph visualization references

These repositories are references only. They are not production dependencies.

## Governing Rule

No Codie subsystem may produce recommendations directly from raw provider data.

Every recommendation must flow through:

```text
Canonical Truth
  ->
Measured Evidence
  ->
Evidence Fusion
  ->
Decision Intelligence
```

This rule is mandatory for all future development.

## Expected Benefits

- single reasoning engine
- reproducible recommendations
- easier debugging
- explainable outputs
- simpler future feature development
- cleaner architecture
- reduced duplicated logic
- consistent confidence scoring
- scalable evidence model
- action-focused user interface

This architecture establishes Codie as an evidence-driven intelligence platform
rather than a collection of independent analytical tools.
