# Commander Staples Specification

Status: roadmap/specification, implementation deferred

## Purpose

Provide a queryable staples system per commander or commander pair.

## Default Window

```text
last 6 months
```

## Supported Filters

```text
commander
partner commander
date range
source
top cut only
winner only
minimum deck count
minimum percentage
exclude basics
include lands
include role tags
```

## Outputs

```text
staples table
exportable CSV
exportable Markdown
Obsidian page
card role breakdown
source deck links
```

Staple rows should show:

```text
card
count
percentage
role_tags
recent_trend
top_cut_usage
winner_usage
co_occurrence_packages
```

## Guardrails

```text
depends on canonical deck records
raw provider records must not power staples directly
user decks must not enter commander averages
low sample size must be labeled
all rows need source provenance
```

## Acceptance Tests

```text
queries commander staples for a 6-month window
excludes basics when configured
returns count and percentage
links source decks
exports Markdown
exports CSV
```
