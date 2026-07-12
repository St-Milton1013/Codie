# Phase 34A - Scryfall Tagger Functional Ontology Contract

Status: contract only

## Purpose

Phase 34A defines the future Scryfall Tagger functional ontology boundary for
Codie.

Scryfall bulk snapshots and migration monitoring now provide a local,
fixture-first card-truth foundation. The next deferred priority is functional
tag ontology: stable role/tag definitions mapped to canonical card identity so
future Tag Graph Lab, frequency pools, Spellbook interpretation, and deck
comparison surfaces can reason from the same functional vocabulary.

This phase does not implement Scryfall Tagger import, tag storage, tag metrics,
graphs, UI, LLM summaries, recommendations, schema, repositories, or provider
changes.

## Accepted Dependency

Phase 34A may begin because Phase 33C outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review note carried forward:

```text
Phase 33C affected-consumer and manual-review field names differ from one
earlier prompt's exact wording, but the accepted implementation remains
report-only and no required fix was requested.
```

## Future Scope To Define

A future accepted implementation packet may add local, fixture-first functional
tag ontology models and validators covering:

```text
Tagger source capture metadata
functional tag namespaces
oracle_id mapping
scryfall_id support as provenance only
artwork/cosmetic tag exclusion
tag source provenance
tag confidence/source fields
manual correction layer input contracts
coverage reporting
unknown tag namespace reporting
duplicate tag handling
Tagger snapshot identity
```

## Source Rules

Primary tag source:

```text
Scryfall Tagger
```

Secondary future sources:

```text
Curated Functional Registry
Role Fusion Engine
User corrections
```

Scryfall Tagger data is functional ontology/reference data. It is not card
truth, deck truth, tournament truth, primer truth, combo truth, or
recommendation truth.

## Identity Rules

Future ontology implementation must preserve:

```text
scryfall_id remains enforced card identity
oracle_id remains analytics/tag grouping identity
Scryfall bulk/card truth remains authoritative for card existence and identity
Scryfall Tagger tags map to oracle_id for functional grouping
source Scryfall IDs remain visible when supplied by Tagger
```

The ontology must never override Scryfall card truth, canonical deck contents,
canonical event records, analytics records, or user deck records.

## Tag Namespace Rules

Future implementation must define tag namespaces explicitly.

Required namespace concepts:

```text
functional_role
game_action
resource
interaction
combo_role
mana_role
card_advantage
protection
stax
win_condition
```

Artwork, aesthetic, flavor, print-treatment, and image-description tags must be
excluded from functional analytics by default.

Examples of excluded categories:

```text
artwork subject
illustration style
frame treatment
artist theme
flavor-only tags
cosmetic print tags
```

## Future Functional Tag Record Shape

A later implementation may represent:

```text
tag_record_id
oracle_id
scryfall_id
tag
tag_namespace
source
confidence
source_url
source_snapshot_id
imported_at
raw_source_ref
is_functional
is_excluded
exclusion_reason
provenance
```

This is a future packet shape only. Phase 34A adds no schema or repository.

## Future Coverage Report Shape

A later implementation may represent:

```text
coverage_report_id
ontology_version
source_snapshot_id
generated_at
total_cards_seen
cards_with_functional_tags
cards_without_functional_tags
functional_tag_count
excluded_tag_count
unknown_namespace_count
duplicate_tag_count
coverage_ratio
warnings
manual_review_items
```

Coverage reporting is evidence metadata. It is not a recommendation, deck
health score, or strategic claim.

## Future Manual Correction Layer

Future implementation may accept manual correction packets as data only:

```text
add tag
remove tag
exclude tag from functional analytics
override namespace
mark tag needs review
```

Manual corrections must preserve:

```text
original source tag
correction source
correction reason
created_at
review status
```

Manual corrections must not rewrite raw Tagger source payloads or silently
delete historical tag records.

## Future Authorized Implementation Shape

A later accepted implementation contract may authorize files such as:

```text
codie/cards/scryfall_tagger_ontology.py
tests/test_scryfall_tagger_ontology.py
tests/fixtures/scryfall_tagger/tagger_functional_tags.json
tests/fixtures/scryfall_tagger/tagger_artwork_tags.json
tests/fixtures/scryfall_tagger/tagger_unknown_namespace.json
tests/fixtures/scryfall_tagger/tagger_duplicate_tags.json
```

The future implementation may update:

```text
codie/cards/__init__.py
```

only to export public ontology model symbols.

No schema, repository, provider, dependency, UI, live-network, file-writing,
analytics, recommendation, or LLM files may be changed unless a later contract
explicitly authorizes them.

## Future Public Interface Candidates

The later implementation may define pure local models/functions such as:

```text
SCRYFALL_TAGGER_ONTOLOGY_VERSION
ScryfallTaggerOntologyError
ScryfallFunctionalTag
ScryfallTaggerSourceRef
ScryfallTaggerCorrection
ScryfallTaggerCoverageReport
ScryfallTaggerOntologyOptions
build_scryfall_tagger_ontology(...)
validate_scryfall_tagger_ontology(...)
scryfall_tagger_ontology_to_dict(...)
build_scryfall_tagger_coverage_report(...)
scryfall_tagger_coverage_report_to_dict(...)
```

Do not expose persistence, live import, downloader, repository, provider,
analytics, charting, UI, LLM, or recommendation APIs in the future
implementation.

## Relationship To Tag Graph Lab

Phase 34A supports the future Tag Graph Lab by defining tag ontology
requirements only.

Future Tag Graph Lab work still requires separate contracts for:

```text
schema/repository persistence
frequency pool integration
tag metric calculation
chart/export surfaces
UI controls
LLM report summaries
```

Tag Graph Lab rules remain:

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
selected tags minimum 1 maximum 6
```

## Explicit Non-Goals

```text
No Scryfall Tagger import implementation in Phase 34A.
No live Scryfall Tagger calls.
No Tagger scraping.
No schema changes.
No repository changes.
No SQLite reads or writes.
No provider changes.
No file writing.
No card lookup replacement.
No Scryfall card-truth override.
No canonicalization changes.
No analytics calculation.
No frequency pool calculation.
No Tag Graph Lab metrics.
No chart export.
No UI work.
No LLM calls.
No recommendation generation.
No dependency changes.
```

## Dependency Rules

Allowed future dependencies:

```text
Python standard library
accepted local Scryfall bulk snapshot models
accepted local Scryfall migration monitoring report models
```

Forbidden dependencies:

```text
requests
httpx
sqlite3
codie.db
repositories
providers
ingestion
analytics
recommendations
decision intelligence
evidence fusion
LLM SDKs
UI frameworks
```

## Required Future Tests

The later implementation packet must add tests proving:

```text
functional tags map to oracle_id
scryfall_id remains visible as provenance when present
artwork/cosmetic tags are excluded by default
functional namespaces are preserved
unknown namespaces are reported
duplicate tags are deduplicated deterministically
source provenance remains visible
confidence values remain visible and bounded
manual corrections annotate without rewriting source tags
coverage ratio is calculated deterministically
low coverage creates visible warnings
raw source payloads are not mutated
malformed fixtures fail cleanly
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears
```

## Validation For This Phase

Phase 34A may create only:

```text
contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Phase 34A must run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Next Gate

After Phase 34A outside validation returns PASS or PASS WITH REVIEW NOTES, a
Phase 34B implementation-contract packet may define the exact allowed local
Scryfall Tagger ontology implementation.

Do not implement Scryfall Tagger ontology in Phase 34A.
