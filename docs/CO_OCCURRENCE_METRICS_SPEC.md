# Co-occurrence Metrics Specification

Status: roadmap/specification, implementation deferred

## Purpose

Detect which cards, packages, and roles appear together across successful decks.

## Core Metrics

Future rows should include:

```text
card_a
card_b
commander_key
archetype_key
deck_count_a
deck_count_b
deck_count_both
co_occurrence_rate
lift
confidence
support
negative_association_score
sample_size
date_window
source_filter
```

## Use Cases

```text
package detection
recommendation support
cut detection
archetype identification
commander staples refinement
meta trend detection
```

## Evidence Rule

Package or gap claims may only be generated when the data supports them with
visible sample size, confidence, and source filters.

## Acceptance Tests

```text
calculates card pair support
calculates lift
calculates confidence
filters by commander
filters by date window
detects positive associations
detects weak/low-sample associations
```
