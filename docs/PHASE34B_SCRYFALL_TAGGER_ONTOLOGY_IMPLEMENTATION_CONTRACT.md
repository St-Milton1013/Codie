# Phase 34B - Scryfall Tagger Ontology Implementation Contract

Status: implementation contract only

## Purpose

Phase 34B defines the exact allowed implementation shape for the future
Scryfall Tagger functional ontology layer.

Phase 34A accepted the ontology boundary. Phase 34B narrows the future
implementation so a later packet can add local, fixture-first Tagger ontology
models and validators without adding live Tagger calls, scraping, persistence,
schema, repositories, provider changes, analytics, UI, LLM calls, or
recommendations.

This phase does not implement Scryfall Tagger ontology.

## Accepted Dependency

Phase 34B may begin because Phase 34A outside validation returned:

```text
PASS WITH REVIEW NOTES
Required fixes: none
```

Review note addressed by this contract:

```text
Phase 34B explicitly includes alias, deprecated-tag, conflict, and
replacement-chain ontology handling in the future implementation scope.
```

## Authorized Future Implementation Scope

A later accepted implementation packet may add only:

```text
codie/cards/scryfall_tagger_ontology.py
tests/test_scryfall_tagger_ontology.py
tests/fixtures/scryfall_tagger/tagger_functional_tags.json
tests/fixtures/scryfall_tagger/tagger_artwork_tags.json
tests/fixtures/scryfall_tagger/tagger_unknown_namespace.json
tests/fixtures/scryfall_tagger/tagger_duplicate_tags.json
tests/fixtures/scryfall_tagger/tagger_aliases_deprecated_conflicts.json
```

The future implementation may update:

```text
codie/cards/__init__.py
```

only to export public Scryfall Tagger ontology model symbols.

No schema, repository, provider, dependency, UI, live-network, file-writing,
analytics, recommendation, LLM, frequency-pool, charting, or Tag Graph Lab
metric files may be changed in the implementation packet.

## Future Public Interface

The future implementation may define:

```text
SCRYFALL_TAGGER_ONTOLOGY_VERSION
ScryfallTaggerOntologyError
ScryfallFunctionalTag
ScryfallTaggerSourceRef
ScryfallTaggerCorrection
ScryfallTagAlias
ScryfallDeprecatedTag
ScryfallTagConflict
ScryfallTagReplacementChain
ScryfallTaggerCoverageReport
ScryfallTaggerOntology
ScryfallTaggerOntologyOptions
build_scryfall_tagger_ontology(...)
validate_scryfall_tagger_ontology(...)
scryfall_tagger_ontology_to_dict(...)
build_scryfall_tagger_coverage_report(...)
scryfall_tagger_coverage_report_to_dict(...)
```

Do not expose persistence, live import, downloader, repository, provider,
analytics, charting, UI, LLM, recommendation, or frequency-pool APIs.

## Future Model Responsibilities

The future implementation may represent:

```text
ontology ID
ontology version
source snapshot ID
source URI
generated_at
imported_at
oracle_id
scryfall_id provenance
tag
normalized tag
tag namespace
source
confidence
source URL
raw source ref
is functional
is excluded
exclusion reason
provenance
aliases
deprecated tags
replacement chains
tag conflicts
manual corrections
coverage report
validation errors
validation warnings
manual review items
```

## Future Identity Rules

The future implementation must preserve:

```text
functional tags map to oracle_id
scryfall_id remains visible as provenance when supplied
scryfall_id remains enforced card identity outside ontology grouping
oracle_id remains analytics/tag grouping identity
Scryfall remains card truth
Tagger data never overrides card/deck/tournament/primer/combo truth
```

## Future Namespace Rules

Future implementation must preserve explicit tag namespaces.

Required functional namespace concepts:

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

Unknown namespaces must be reported and may create manual review items.
Unknown namespaces must not be silently mapped to known namespaces.

## Future Exclusion Rules

Artwork, aesthetic, flavor, print-treatment, and image-description tags must be
excluded from functional analytics by default.

Exclusions must remain visible as data:

```text
is_excluded
exclusion_reason
source tag
source namespace
```

Excluded tags must not disappear from provenance records.

## Future Alias / Deprecation / Conflict Rules

The future implementation must explicitly model:

```text
tag aliases
deprecated tags
replacement tags
replacement chains
conflicting namespace assignments
conflicting functional/excluded classification
manual correction conflicts
```

Alias handling rules:

```text
aliases normalize to a canonical tag only when explicitly configured
aliases preserve original tag text
aliases preserve source provenance
alias normalization is deterministic
```

Deprecation handling rules:

```text
deprecated tags remain visible
replacement tags remain visible
replacement chains are bounded and deterministic
cyclic replacement chains fail cleanly
deprecated tags create warnings or manual review items
```

Conflict handling rules:

```text
conflicts remain visible
conflicts do not silently choose a winner
conflicts may create manual review items
conflicts do not produce recommendations
```

## Future Manual Correction Rules

Manual corrections may annotate ontology output as data only:

```text
add tag
remove tag
exclude tag from functional analytics
override namespace
mark tag needs review
add alias
mark deprecated
define replacement tag
flag conflict
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

## Future Coverage Report Rules

Coverage reports must include:

```text
total cards seen
cards with functional tags
cards without functional tags
functional tag count
excluded tag count
unknown namespace count
duplicate tag count
alias count
deprecated tag count
conflict count
manual correction count
coverage ratio
warnings
manual review items
```

Coverage reports are evidence metadata only. They are not recommendations,
deck health output, strategy output, frequency-pool output, or chart output.

## Relationship To Phase 32 / 33

Future implementation may import accepted local model layers:

```text
codie.cards.scryfall_bulk_snapshots
codie.cards.scryfall_migration_monitoring
```

Future implementation must not change:

```text
codie/cards/scryfall_bulk_snapshots.py
codie/cards/scryfall_migration_monitoring.py
tests/test_scryfall_bulk_snapshots.py
tests/test_scryfall_migration_monitoring.py
```

unless a focused correction is separately justified.

## Relationship To Tag Graph Lab

Phase 34B supports future Tag Graph Lab work by defining the local ontology
implementation surface only.

Future Tag Graph Lab work still requires separate contracts for:

```text
schema/repository persistence
frequency pool integration
tag metric calculation
chart/export surfaces
UI controls
LLM report summaries
```

## Required Future Rules

The future implementation must:

```text
be local-first
be fixture-first
avoid live network dependency in tests
consume local fixture payloads only
avoid mutating input payloads
preserve source provenance
serialize ontology reports deterministically
round-trip ontology reports through dictionary-compatible form
fail cleanly on malformed inputs
produce visible validation errors
produce visible validation warnings
produce visible manual review items
remain recommendation-free
```

## Explicit Non-Goals

```text
No Scryfall Tagger ontology implementation in Phase 34B.
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
codie.cards.scryfall_bulk_snapshots
codie.cards.scryfall_migration_monitoring
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
aliases preserve original tags and normalize deterministically
deprecated tags remain visible
replacement chains remain visible
cyclic replacement chains fail cleanly
tag conflicts remain visible and do not silently choose a winner
coverage ratio is calculated deterministically
low coverage creates visible warnings
raw source payloads are not mutated
malformed fixtures fail cleanly
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears
```

## Validation For This Phase

Phase 34B may create only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Phase 34B must run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Next Gate

After Phase 34B outside validation returns PASS or PASS WITH REVIEW NOTES, a
Phase 34C implementation packet may add the approved local Scryfall Tagger
ontology model implementation.

Do not implement Scryfall Tagger ontology in Phase 34B.
