# Phase 40B - Relationship Intelligence Schema and Repository Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase40B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40B defines the future SQLite schema and repository boundary for
Relationship Intelligence measured evidence. It narrows persistence to
immutable population specifications, population manifests, manifest members,
relationship measurements, and separately visible metric values.

This phase is documentation-only. It does not add schema, migrations,
repositories, calculations, providers, recommendations, Evidence Fusion
integration, Jin behavior, Tournament Exposure analysis, UI, LLM calls, graph
database support, file writing, or live network behavior.

## Authority

The governing authority is:

```text
docs/CODIE_V2_CONSTITUTION.md, Section 17
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
```

The following proposal is non-authoritative design input:

```text
docs/design_inputs/v2_intelligence_program/CODIE_V2_RELATIONSHIP_INTELLIGENCE_PROPOSAL.md
```

When the proposal differs from Constitution V2 or Phase 40A, the accepted
authority controls.

## Future Authorized Files

After Phase 40B outside validation passes, Phase 40C may define an
implementation contract limited to:

```text
codie/db/schema/analytics.sql
codie/db/schema/indexes.sql
codie/db/repositories/analytics.py
docs/SCHEMA_SPEC.md
tests/test_schema.py
tests/test_repositories.py
```

If the existing test ownership differs at implementation time, Phase 40C must
name the exact existing test files rather than creating duplicate repository
test ownership.

No other files are authorized by this contract.

## First Persistence Family

The first schema implementation must be limited to these logical tables:

```text
relationship_population_specs
relationship_population_manifests
relationship_population_members
relationship_measurements
relationship_measurement_metrics
```

The `AnalyticsRepository` remains the sole repository owner for this table
family. A second relationship repository or provider-facing persistence path
is prohibited.

The following proposal concepts remain deferred:

```text
relationship assertions
assertion-source links
measurement strata
confounder records
theory links
graph database projections
```

They require later accepted contracts and must not be smuggled into the first
migration as nullable future-proofing columns.

## Population Specification Contract

Each population specification must preserve:

```text
population_spec_id
population_spec_version
population_spec_hash
observation_unit
commander or exact partner-pair scope
zone scope
date range
region
store
organizer
event-size filter
placement filter
deduplication policy
concentration policy
created_at
```

The canonical JSON used to calculate `population_spec_hash` must serialize
deterministically. Identical specifications must produce the same hash.
Changed filters or policies must produce a new version and hash.

## Immutable Population Manifest Contract

Each manifest must preserve:

```text
population_manifest_id
population_manifest_version
population_manifest_hash
population_spec_id
population_spec_version
population_spec_hash
source_snapshot_refs
candidate_population_count
usable_population_count
unknown_or_excluded_count
deduplicated_population_count
generated_at
```

Each manifest member must preserve:

```text
population_manifest_id
member_sequence
observation_unit_type
observation_unit_id
canonical_deck_id, when applicable
canonical_event_id, when applicable
inclusion_status
exclusion_reason, when excluded
deduplication_key
concentration_group_key, when applicable
```

Manifest membership and order are immutable after insertion. Rebuilding a
population creates a new manifest identity; it never mutates historical
membership.

Global manifests may contain canonical tournament observations only. Private
user decks, imported deck text, private notes, and personal snapshots must not
enter global population tables. User-local comparison persistence requires a
separate privacy contract.

## Measurement Contract

Each relationship measurement must preserve:

```text
relationship_measurement_id
relationship_measurement_version
relationship_measurement_hash
relationship_type
source_endpoint_type
source_endpoint_id
target_endpoint_type
target_endpoint_id
directionality
population_manifest_id
population_manifest_version
N
nA
nB
nAB
candidate_population_count
usable_population_count
unknown_or_excluded_count
deduplicated_population_count
observed_co_occurrence
expected_co_occurrence
metric_bundle_version
provenance_refs
caveat_refs
generated_at
```

The persisted raw counts are authoritative inputs for replay. Metrics must not
be persisted without their counts and immutable population manifest identity.
Endpoint ordering must be deterministic for undirected relationships.
Directional measurements must preserve their declared source and target.

Measurements are append-only. Recalculation under changed inputs, formulas,
or versions creates a new measurement identity.

## Metric Value Contract

Each metric row must preserve:

```text
relationship_measurement_id
metric_name
metric_version
orientation
metric_value, nullable
numerator, when applicable
denominator, when applicable
undefined_reason, when metric_value is null
```

Required names are limited to the Phase 40A metric family:

```text
support
directional_confidence
dependence_delta
lift
leverage
jaccard_similarity
pmi
```

The schema must not contain an opaque combined synergy score. The bare metric
name `confidence` is prohibited. Undefined values must remain null with a
visible Phase 40A reason; they must not become zero, infinity, or smoothed
values.

## Foreign Keys And Identity

Future schema must:

```text
enable SQLite foreign keys in tests
link manifest members to canonical deck and event rows when those IDs apply
link measurements to immutable manifests
link metric rows to measurements
enforce deterministic uniqueness for specification, manifest, measurement,
and metric identities
reject dangling references
```

Generic endpoint IDs may not all be foreign-keyed to one table because the
accepted endpoint types span cards, tags, packages, combos, outputs, events,
and attributed claims. The repository must validate endpoint type and
non-empty canonical identity, while later endpoint-specific contracts may add
stronger references.

## Repository Contract

Future repository methods may only:

```text
insert and retrieve population specifications
insert a manifest and its members transactionally
retrieve manifests and ordered members
insert a measurement and its metrics transactionally
retrieve measurements by identity
list measurements by endpoint pair, population manifest, and version
verify replay identities and immutable hashes
```

Repository methods must not:

```text
calculate relationship metrics
build populations from provider or source tables
read raw provider payloads
read private user deck content
upsert or mutate historical manifests or measurements
rank relationships
generate recommendations
call an LLM
run simulator behavior
write files
```

Duplicate insertion of the same immutable identity may return the existing
record only after exact content equality is verified. Conflicting content for
an existing identity must fail closed.

## Transaction And Rollback Rules

Manifest plus member insertion and measurement plus metric insertion must be
atomic. Any failed child insert must roll back the whole transaction.

The future migration must be additive, preserve schema bootstrap parity, and
include rollback instructions in dependency-reverse order. Runtime rollback
must not rewrite historical rows. A failed new measurement leaves prior
measurements untouched.

## Index Requirements

Phase 40C must define indexes supporting:

```text
population specification hash and version lookup
population manifest hash and specification lookup
ordered manifest member retrieval
measurement identity and manifest lookup
endpoint-pair and relationship-type lookup
metric lookup by measurement and metric name
generated-at and version audit lookup
```

Indexes must support retrieval only. They must not encode recommendation
ranking or a combined relationship score.

## Required Future Tests

Phase 40C must require tests for:

```text
schema bootstrap and SCHEMA_SPEC parity
foreign-key enforcement
deterministic specification, manifest, and measurement identity
manifest and measurement immutability
ordered member replay
raw N, nA, nB, and nAB preservation
nullable metric values with visible undefined reasons
directional orientation preservation
transaction rollback on child failure
conflicting duplicate identity rejection
global population privacy rejection
repository retrieval ordering
no provider, recommendation, simulator, LLM, UI, or file-writing coupling
```

## Phase 40B Forbidden Work

Phase 40B must not modify:

```text
codie/
tests/
ui/
scripts/
schemas/
codie/db/schema/
codie/db/repositories/
docs/SCHEMA_SPEC.md
requirements.txt
requirements-dev.txt
pyproject.toml
.github/workflows/
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
docs/CODIE_V1_CONSTITUTION.md
docs/CODIE_V2_CONSTITUTION.md
```

Phase 40B must not implement schema, repository methods, calculations,
providers, recommendations, Jin, Tournament Exposure, UI, graph database
support, LLM calls, simulator behavior, or live network access.

## Acceptance Gate

Phase 40C must not begin until Phase 40B outside validation returns PASS or
PASS WITH REVIEW NOTES.

