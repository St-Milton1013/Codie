# Phase 40C - Relationship Intelligence Schema and Repository Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase40C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40C authorizes a later Phase 40D implementation of the narrow,
analytics-owned Relationship Intelligence persistence family accepted in
Phase 40B. Phase 40C itself is documentation-only and does not modify schema,
repositories, tests, production code, dependencies, workflows, or active
validation scope.

## Governing Contracts

```text
docs/CODIE_V2_CONSTITUTION.md, Section 17
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT.md
```

## Phase 40D Authorized Files

Phase 40D may modify only:

```text
codie/db/schema/analytics.sql
codie/db/schema/indexes.sql
codie/db/repositories/analytics.py
docs/SCHEMA_SPEC.md
tests/test_schema.py
tests/test_repositories.py
codie/db/repositories/__init__.py, only if an existing export requires change
```

Phase 40D must not add a new repository owner or a separate migration
framework. It must use the existing schema bootstrap and `AnalyticsRepository`
patterns.

## Required Tables

Phase 40D must add exactly:

```text
relationship_population_specs
relationship_population_manifests
relationship_population_members
relationship_measurements
relationship_measurement_metrics
```

No assertion, theory-link, stratum, confounder, graph-projection, user-local,
provider, recommendation, or combined-score table is authorized.

## Required Column Families

`relationship_population_specs` must persist:

```text
population_spec_id
population_spec_version
population_spec_hash
observation_unit
scope_type
scope_key
zone_scope
window_start_date
window_end_date
region
store
organizer
minimum_event_size
placement_filter
deduplication_policy
concentration_policy
spec_json
created_at
```

`relationship_population_manifests` must persist:

```text
population_manifest_id
population_manifest_version
population_manifest_hash
population_spec_id
population_spec_version
population_spec_hash
source_snapshot_refs_json
candidate_population_count
usable_population_count
unknown_or_excluded_count
deduplicated_population_count
generated_at
```

`relationship_population_members` must persist:

```text
population_member_id
population_manifest_id
member_sequence
observation_unit_type
observation_unit_id
canonical_deck_id
canonical_event_id
inclusion_status
exclusion_reason
deduplication_key
concentration_group_key
```

`relationship_measurements` must persist:

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
provenance_refs_json
caveat_refs_json
generated_at
```

`relationship_measurement_metrics` must persist:

```text
relationship_measurement_metric_id
relationship_measurement_id
metric_name
metric_version
orientation
metric_value
numerator
denominator
undefined_reason
```

SQLite names may use the listed casing for `N`, `nA`, `nB`, and `nAB`, or a
documented lowercase equivalent, but repository outputs and SCHEMA_SPEC must
preserve the Phase 40A meanings unambiguously.

## Constraints

Phase 40D must enforce:

```text
non-empty version and hash identities
unique population specification hash plus version
unique population manifest hash plus version
unique manifest member sequence per manifest
unique observation unit identity per manifest
unique measurement hash plus version
unique metric name, version, and orientation per measurement
foreign keys from manifests to specifications
foreign keys from members to manifests
foreign keys from measurements to manifests
foreign keys from metrics to measurements
optional canonical deck and event foreign keys for applicable members
non-negative population and raw pair counts
0 <= nAB <= nA <= N
0 <= nAB <= nB <= N
null metric_value requires non-empty undefined_reason
non-null metric_value requires null undefined_reason
```

The implementation may use repository validation where a SQLite `CHECK`
cannot express a cross-field or JSON rule cleanly. Tests must prove the
boundary regardless of enforcement location.

## Deterministic JSON

The following fields must contain canonical JSON arrays or objects:

```text
spec_json
source_snapshot_refs_json
provenance_refs_json
caveat_refs_json
```

Repository writes must serialize them deterministically and reads must decode
them without losing order or identity. Raw provider payloads and private user
content are prohibited.

## Repository Interface

Phase 40D may add these methods to `AnalyticsRepository`, using local naming
conventions where equivalent:

```text
insert_relationship_population_spec(...)
get_relationship_population_spec(...)
insert_relationship_population_manifest(...)
get_relationship_population_manifest(...)
list_relationship_population_members(...)
insert_relationship_measurement(...)
get_relationship_measurement(...)
list_relationship_measurements(...)
list_relationship_measurement_metrics(...)
```

Manifest insertion must include members in one transaction. Measurement
insertion must include metrics in one transaction.

The repository must:

```text
return stable ordering
verify exact content before treating a duplicate immutable identity as idempotent
reject conflicting duplicate identities
roll back parent and children together
never update or delete historical manifests or measurements through the public interface
```

The repository must not:

```text
calculate metrics
construct populations
query source or provider tables
read private user deck content
rank or score relationships
generate recommendations
call Evidence Fusion, Decision Intelligence, Jin, simulator, UI, LLM, or network code
write files
```

## Indexes

Required indexes must cover:

```text
specification hash and version
manifest hash and version
manifest specification identity
manifest member sequence
measurement hash and version
measurement manifest identity
measurement endpoint pair plus relationship type
metric measurement identity plus name and orientation
generated-at audit retrieval
```

## Required Tests

Phase 40D must add focused tests for:

```text
schema bootstrap and SCHEMA_SPEC parity
all five tables and required indexes
foreign-key enforcement
deterministic JSON persistence
specification idempotency and conflict rejection
atomic manifest plus member insertion
atomic measurement plus metric insertion
rollback after child failure
stable member and metric ordering
raw N, nA, nB, and nAB round trip
count invariant rejection
nullable metric and undefined-reason rules
directional orientation preservation
immutable historical identity behavior
global-population private-data rejection
no source/provider table reads
no metric calculation or recommendation behavior
```

## Forbidden Phase 40C Work

Phase 40C must not modify:

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

## Gate

Phase 40D implementation must not begin until Phase 40C outside validation
returns PASS or PASS WITH REVIEW NOTES.

