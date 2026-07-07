# Frequency Pool Specification

Status: roadmap/specification, implementation deferred

## Purpose

Generate frequency pools from deck groups, especially Moxfield links and text
exports.

## Inputs

Future implementation should support:

```text
list of Moxfield deck URLs
plain text Moxfield exports
optional commander key
optional date window
optional archetype label
optional source label
```

## Outputs

Future frequency rows should include:

```text
card_name
deck_count
deck_total
percentage
role_tags
type_line
mana_value
color_identity
scryfall_id
oracle_id
sample_deck_count
source_deck_urls
```

Export formats:

```text
CSV
Markdown
JSON
Obsidian note
PDF later
```

## Required Behavior

```text
normalize all cards through Scryfall
deduplicate repeated deck URLs
detect commanders separately from mainboard
ignore basic lands when requested
preserve deck source URLs
report failed imports
```

## Guardrails

```text
Scryfall remains card identity truth
Moxfield access must be isolated behind a provider/import contract
manual text export fallback is required
frequency pools are not tournament evidence unless sourced from canonical tournament records
private deck text must not be exported without explicit user action
```

## Acceptance Tests

```text
imports 5 Moxfield URLs
deduplicates repeated URLs
normalizes all card names
separates commanders from mainboard
calculates card counts
calculates percentages
exports CSV
exports Markdown
reports failed URLs
```
