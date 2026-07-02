# Roadmap Patch - Tag Graph Lab

Status: roadmap-only, implementation deferred

## Purpose

Codie should eventually support graphing deck and commander data by functional
tags.

The Tag Graph Lab lets users select one to six functional tags and graph their
frequency, adoption, density, and trend across decks, commanders, time windows,
regions, tournament results, and frequency pools.

This is an evidence, comparison, and visualization feature. It is not a
strategic-claim feature.

## Tag Sources

Primary tag source:

```text
Scryfall Tagger
```

Secondary tag sources:

```text
Curated Functional Registry
Role Fusion Engine
User corrections
```

All tags must preserve source provenance.

Scryfall Tagger tags must be mapped to card `oracle_id` values.

## Supported Scopes

Future implementation should support:

```text
single analyzed deck
saved deck snapshot
commander average
exact partner-pair average
Top 16 commander pool
winner pool
regional pool
meta snapshot
frequency pool
personal deck history
```

Default comparison:

```text
Analyzed deck vs Commander Top 16 average
```

## Selected Tag Limit

Allowed selected tags:

```text
minimum: 1
maximum: 6
```

More than six selected graph categories must be rejected or require a future
explicit override. Six is the default visual clarity limit.

## Supported Graph Types

Future UI/report outputs may include:

```text
tag count bar chart
tag density bar chart
tag trend line chart
deck vs commander average comparison
top card contributors per tag
tag overlap matrix
tag correlation scatter plot
frequency pool tag breakdown
```

## Required Tag Metrics

Future metric rows should support:

```text
raw_tag_count
tag_density
tag_inclusion_rate
average_cards_per_deck_with_tag
placement_weighted_tag_usage
top_16_tag_frequency
winner_tag_frequency
tag_trend_delta
tag_confidence
matching_deck_count
available_deck_count
coverage_ratio
```

## Metric Definitions

`raw_tag_count`:

```text
number of cards in the selected deck or pool with the tag
```

`tag_density`:

```text
raw_tag_count / total deck cards counted
```

`tag_inclusion_rate`:

```text
percentage of matching decks containing at least one card with the tag
```

`average_cards_per_deck_with_tag`:

```text
average number of tagged cards among decks where the tag appears
```

`placement_weighted_tag_usage`:

```text
tag usage weighted by event size and tournament placement
```

`tag_trend_delta`:

```text
change in tag usage between selected time windows
```

`coverage_ratio`:

```text
matching decks with tag data / available matching decks
```

## Required Rules

Future implementation must follow these rules:

```text
all tag graphs are generated from canonical card identities
Scryfall Tagger tags map to oracle_id
graphs expose underlying card lists
graphs expose underlying numeric tables
tags preserve source provenance
user decks never enter commander averages
frequency pool graphs show the deck pool used
low sample and low tag coverage are labeled
tag graphs do not produce strategic claims
LLMs may summarize tag graphs only in meta/report modes, not single-deck reports
```

## Required Filters

Future implementation should support:

```text
commander
partner pair
date range
placement scope
provider
region
card type
selected tags
minimum inclusion rate
minimum deck count
include/exclude generic staples
include/exclude lands
include/exclude packages
```

## Example Query Classes

Future UI/chat/report surfaces may answer evidence-only queries such as:

```text
graph draw engine, interaction, ramp, tutors, stax, and win condition for my deck vs Tymna/Kraum Top 16 average
show tag trends for Kinnan over the last year
compare interaction density in Japan vs North America
show top cards contributing to the ramp tag in RogSi
show which tags increased in Blue Farm frequency pools over six months
```

## Frequency Pool Integration

The Tag Graph Lab must integrate with commander frequency pools.

For any selected commander or partner pair, Codie can eventually generate:

```text
Frequency Pool
-> Card frequency table
-> Tag assignment
-> Tag frequency table
-> Tag graphs
```

This allows evidence-only answers about:

```text
which functional roles are most represented in successful versions of a commander
which tags differ between a user deck and a commander pool
which tags trend upward in top finishes
which cards are driving a tag increase
```

## Suggested Module Placement

Future implementation may use:

```text
codie/tag_graphs/tag_graph_models.py
codie/tag_graphs/tag_metric_calculator.py
codie/tag_graphs/tag_frequency_pool.py
codie/tag_graphs/tag_comparison.py
codie/tag_graphs/tag_trend.py
codie/tag_graphs/tag_chart_export.py
codie/tag_graphs/tag_graph_service.py
```

## Possible Future Schema

Future schema may include:

```sql
CREATE TABLE card_functional_tags (
    card_tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    oracle_id TEXT NOT NULL,
    scryfall_id TEXT,
    tag TEXT NOT NULL,
    tag_namespace TEXT NOT NULL,
    source TEXT NOT NULL,
    confidence REAL DEFAULT 1.0,
    source_url TEXT,
    imported_at TEXT NOT NULL,
    UNIQUE(oracle_id, tag, tag_namespace, source)
);

CREATE TABLE tag_graph_runs (
    tag_graph_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope_type TEXT NOT NULL,
    scope_key TEXT NOT NULL,
    commander_key TEXT,
    partner_key TEXT,
    selected_tags_json TEXT NOT NULL,
    filters_json TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    analytics_version TEXT NOT NULL,
    source_snapshot_id TEXT,
    data_json TEXT NOT NULL
);
```

Schema is not approved by this roadmap patch. Any persistence requires a
separate schema contract with repositories, indexes, idempotency, rebuild
rules, provenance, and migration review.

## Recommended First UI

Future UI concept:

```text
Tag Graph Lab
```

Recommended flow:

```text
1. Select deck or commander
2. Select comparison baseline
3. Select up to six tags
4. Select time window
5. Generate graph
6. Expand each tag into contributing cards
7. Export to Obsidian, Markdown, CSV, or JSON
```

Recommended first visual:

```text
grouped bar chart: analyzed deck vs commander Top 16 average
```

Example tags:

```text
Draw Engine
Interaction
Ramp
Tutors
Stax
Win Condition
```

Example output shape:

```text
Draw Engine       My Deck 8     Commander Avg 6.4
Interaction       My Deck 16    Commander Avg 21.2
Ramp              My Deck 13    Commander Avg 12.7
Tutors            My Deck 7     Commander Avg 6.9
Stax              My Deck 3     Commander Avg 4.8
Win Condition     My Deck 5     Commander Avg 5.1
```

## Relationship To Existing Roadmap Items

Tag Graph Lab combines:

```text
Scryfall Tagger
Commander Staples / Frequency Pools
Commander Baseline Comparison Graphs
Evidence Graph / Interactive Intelligence surfaces
```

Functional tags describe what cards do. Card types describe card type lines.
Codie should prioritize functional tag graphs when the user is asking about
roles, density, adoption, and trend.

## Future Acceptance Tests

Future implementation should include tests for:

```text
one to six selected tags accepted
zero selected tags rejected
more than six selected tags rejected
tags map to oracle_id
tag source provenance preserved
user deck excluded from commander averages
frequency pool exposes deck pool used
low sample caveat emitted
low coverage caveat emitted
underlying card list exported
underlying numeric table exported
placement-weighted usage calculated deterministically
trend delta calculated deterministically
coverage ratio calculated deterministically
strategic claim language rejected
```

## Non-Goals

```text
do not implement this during Phase 19 outside-validation gating
do not add schema from this roadmap patch
do not add UI from this roadmap patch
do not call live Scryfall Tagger without a provider/import contract
do not let user decks enter commander averages
do not treat tag graphs as recommendation output
do not generate strategic claims
do not let LLM summaries appear in single-deck reports
do not hide low sample or low tag coverage
```
