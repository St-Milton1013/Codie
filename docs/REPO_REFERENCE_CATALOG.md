# Repository Reference Catalog

Status: reference-only

## Rules

Repository references may be used for:

```text
UI inspiration
fixture ideas
edge-case discovery
parser comparison
data-shape comparison
test planning
```

They must not be copied into Codie or treated as architecture authorities.

## Magic Rules References

Official Magic documentation remains authoritative. GitHub repositories may
only support rule-shape discovery, fixture planning, parser comparison, and
simulator validation research.

Reference candidates:

```text
sethwoodworth/mtg-comprehensive-rules
dgulyas/RulesParser
pit142857/mtg-cr
machinaut/mtg-rules
MTGRuler
```

Use only for:

```text
rules parsing ideas
rule reference indexing
card interaction explanation fixtures
simulator validation test planning
chat answers about game mechanics
```

Do not use GitHub rule repositories to override official Comprehensive Rules,
official Oracle rulings, official release notes, or official format legality
announcements.

## MTG Deck Analyzer References

Reference candidates:

```text
gab-25/mtg_deck_analyzer
FPoliandri/mtg-analyzer
drmDev/MtgTrophyAnalyzer
jwhitney2209/mtg-deck-analyzer
ClaytonONeill/mtg-deck-analyzer
```

Use only for:

```text
UI inspiration
deck parsing edge cases
mana curve / color balance ideas
comparison tests
```

Suggested local reference path:

```text
reference/github/mtg_deck_analyzers/
```

## Deck Parsing Reference

Reference candidate:

```text
JasonDGates/MTG-Deck-Parser
```

Use as parser reference only. Codie's parser must remain provider-normalized
and Scryfall-backed.

## Moxfield Scraping Reference

Reference candidate:

```text
Jorazon/moxfield-scraper
Moxfield parser references
```

Use only for Moxfield URL handling, deck extraction patterns, and failure
cases.

Codie still needs its own adapter for:

```text
commander matching
partner matching
primer route detection
likes/views/comments metadata
updated metadata
frequency aggregation
staples export
```

## Scryfall Tagging / Functional Role References

Reference candidates:

```text
nathan-pham/mtg-cube-tagger
benjamin-fouilleul/mtg_ultimate_tag
```

Use only for:

```text
tag schema ideas
functional role grouping
card category modeling
deck health role summaries
```

Preferred functional classification source remains:

```text
Scryfall Tagger
```

## Commander Spellbook Backend

Reference candidate:

```text
SpaceCowMedia/commander-spellbook-backend
```

Use for:

```text
combo detection
combo component metadata
package completion logic
combo link storage
recommendation evidence
```

Do not use it as deck truth.

## MTGJSON

Reference candidates:

```text
mtgjson/mtgjson
mtgjson/mtgjson3
mtgjson/mtgjson-website
```

Use `mtgjson/mtgjson` as secondary card-data enrichment. `mtgjson3` should be
treated as archived reference material when applicable.

Scryfall remains card truth.

Good MTGJSON use cases:

```text
offline card database validation
set metadata
alternate identifiers
historical card data
bulk testing
```

## LocalSend

Reference candidates:

```text
localsend/localsend
localsend/protocol
localsend/web
```

Use for future local report delivery research. The protocol repository is the
important reference for a stable delivery contract.

## SQLite Vector Search

Reference candidates:

```text
asg017/sqlite-vec
sqliteai/sqlite-vector
```

`asg017/sqlite-vec` is especially relevant because Codie is SQLite-first.

Potential uses:

```text
semantic search over Codie reports
primer metadata retrieval
deck snapshot retrieval
card explanation retrieval
chat context retrieval
Obsidian export search
```

Vector search is retrieval support, not truth.

## Evidence Graph / Visualization

Reference candidates:

```text
Kejikus/interactive-graph
mrzahaki/dynagraph
Cytoscape / graph visualization references
```

Use for:

```text
recommendation evidence graph
card/package relationship graph
commander staples graph
co-occurrence graph
tag graph
```

V1 should use React graph components and SQLite-backed graph data. No graph
database is approved for V1.

## Obsidian / Markdown Export

Weak reference candidates:

```text
Jinius36/obsidian-cs-vault-generator
MrrKotleciq/Atlas_Generator
```

Codie should build its own Markdown exporter because it needs specific output:

```text
commander pages
deck reports
card pages
staples pages
simulation traces
evidence notes
internal wikilinks
tag pages
primer index pages
```
