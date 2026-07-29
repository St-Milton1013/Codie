# Phase 40I - Relationship Intelligence Population Resolution Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase40I
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40J
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40I authorizes a later Phase 40J implementation of the pure, deterministic
Relationship Intelligence population resolver defined by Phase 40H.

Phase 40I is documentation-only. It does not implement population resolution,
tests, persistence, repository reads, providers, metric calculation,
recommendations, Jin, Tournament Exposure, simulator behavior, UI, LLM calls,
file writing, or network behavior.

## Governing Contracts

```text
docs/CODIE_V2_CONSTITUTION.md, Sections 8, 9, 10, 11, and 17
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/PHASE40H_RELATIONSHIP_INTELLIGENCE_POPULATION_RESOLUTION_CONTRACT.md
codie/analytics/relationship_metrics.py
```

## Phase 40J Authorized Files

Phase 40J may modify only:

```text
codie/analytics/relationship_population.py
tests/test_relationship_population.py
codie/analytics/__init__.py, exports only
```

No schema, repository, provider, fixture, dependency, workflow, CLI, UI,
simulator, recommendation, or governance implementation file is authorized.

## Required Public Interface

Phase 40J must expose:

```text
RELATIONSHIP_POPULATION_VERSION
RelationshipPopulationBuildError
RelationshipEndpoint
RelationshipDeckPresenceRecord
RelationshipPopulationSpec
RelationshipPopulationExclusion
RelationshipPopulationManifest
RelationshipPopulationResolution
build_relationship_population_resolution(...)
relationship_population_manifest_to_dict(...)
relationship_population_resolution_to_dict(...)
validate_relationship_population_spec(...)
validate_relationship_population_manifest(...)
validate_relationship_population_resolution(...)
```

Public value objects must be immutable. Collection and metadata fields must use
immutable JSON-compatible values. Caller-owned objects must not be mutated.

## Endpoint Packet

`RelationshipEndpoint` must preserve:

```text
endpoint_type
endpoint_id
canonical_identity_ids
tag_assignment_ids
package_member_ids
metadata
```

Supported endpoint types are:

```text
card
tag
package
commander
commander_pair
```

Endpoint IDs and referenced identity IDs must be non-empty. Reference
collections must reject duplicates and serialize in declared stable order.
Unsupported endpoint types must fail closed.

Tag endpoints consume already-built canonical tag assignments. The resolver
must not call Tagger or infer tag membership.

## Deck Presence Record

`RelationshipDeckPresenceRecord` must preserve:

```text
deck_id
snapshot_id
observation_status
privacy_class
commander_key
partner_key
mainboard_oracle_ids
sideboard_oracle_ids
auxiliary_oracle_ids
tag_assignment_ids
package_ids
source_snapshot_ids
provenance_ref_ids
metadata
```

Usable records must have stable deck and snapshot identities and canonical
Oracle IDs. Raw names, unresolved identities, raw provider payloads, private
deck text, primer bodies, user notes, credentials, and unrestricted metadata
are prohibited.

## Population Specification

`RelationshipPopulationSpec` must preserve:

```text
population_spec_version
population_scope_type
population_scope_key
commander_key
partner_key
time_window_start
time_window_end
region
placement_scope
source_snapshot_ids
analytics_version
deduplication_policy
inactive_status_policy
include_sideboard
include_auxiliary
low_sample_threshold
low_coverage_threshold
calculated_at
provenance_ref_ids
caveat_ids
```

Caller-provided `calculated_at` is required. Phase 40J must not read the wall
clock. Dates, versions, IDs, scope values, policies, and thresholds must be
validated. Metadata must be immutable and JSON-compatible.

## Population Policies

Phase 40J supports only declared policies:

```text
deduplication_policy: canonical_snapshot
inactive_status_policy: exclude_inactive
```

The implementation must not invent hidden defaults or alternate policies.

Canonical snapshot deduplication uses a deterministic key and stable
tie-breaker declared in code and tests. Input order must not select a survivor.
Every removed duplicate must produce a visible exclusion and increment
`deduplicated_population_count`.

Resolved and ignored-by-policy records are inactive and excluded by default.
Phase 40J does not authorize an include-inactive option. Private user records
are excluded from global evidence unless their observation status explicitly
marks them as approved observations.

## Presence Rules

Presence is binary per usable deck:

```text
N = usable_population_count
nA = usable decks containing endpoint A
nB = usable decks containing endpoint B
nAB = usable decks containing both endpoints
```

Multiple matching identities in one deck count once. Mainboard is counted by
default. Sideboard and auxiliary identities are counted only when their
explicit specification flags are true.

Endpoint matching rules:

```text
card: canonical Oracle ID membership
tag: already-built tag-assignment membership
package: already-built package ID membership
commander: exact canonical commander key
commander_pair: exact normalized commander and partner keys
```

Exact partner-pair matching must be order-normalized and must not collapse to
a commander-only population.

Direct card-to-tag measurement must fail closed because no accepted
anti-tautology rule exists. Tag-to-tag, tag-to-package, and other endpoint
pairs still require distinct endpoint IDs.

## Exclusions

`RelationshipPopulationExclusion` must preserve:

```text
candidate_id
deck_id
snapshot_id
reason_code
detail
source_snapshot_id
```

Supported reason codes must include:

```text
DUPLICATE_CANONICAL_SNAPSHOT
INACTIVE_RESOLVED
INACTIVE_IGNORED_BY_POLICY
PRIVATE_USER_RECORD
UNAPPROVED_OBSERVATION
MISSING_CANONICAL_DECK_ID
MISSING_CANONICAL_SNAPSHOT_ID
UNRESOLVED_CARD_IDENTITY
UNSUPPORTED_ENDPOINT
UNKNOWN_OR_EXCLUDED
```

Unknown, unavailable, unsupported, inactive, private, excluded, and
deduplicated states must remain distinct.

## Manifest And Resolution

`RelationshipPopulationManifest` must preserve every field required by Phase
40H, including stable member IDs, exclusions, count totals, provenance,
caveats, policies, version, semantic spec hash, and caller timestamp.

`RelationshipPopulationResolution` must preserve:

```text
resolution_version
manifest
source_endpoint
target_endpoint
count_packet
presence_record_ids
exclusions
labels
```

Manifest identity and population spec hash must derive only from normalized
semantic inputs. Input order, process identity, current time, random values,
and object memory addresses must not affect output.

The emitted `RelationshipCountPacket` must use the Phase 40G public model and
must satisfy its validators without reconstruction of metric semantics.

## Count And Coverage Invariants

Phase 40J must validate:

```text
candidate_population_count =
    usable_population_count
    + unknown_or_excluded_count
    + deduplicated_population_count

N = usable_population_count
0 <= nAB <= nA <= N
0 <= nAB <= nB <= N
matching_deck_count <= available_deck_count
coverage_ratio = matching_deck_count / available_deck_count when denominator > 0
coverage_ratio is unavailable when available_deck_count == 0
```

Low sample and low coverage create visible labels or caveats but do not change
membership or endpoint counts.

## Forbidden Behavior

Phase 40J must not:

```text
query databases or repositories
persist manifests or measurements
read providers or raw source tables
call live APIs or Tagger
infer tags, packages, deck intent, or pilot intent
calculate support, confidence, dependence delta, lift, leverage, Jaccard, or PMI
rank or score relationships
make causal claims
generate recommendations or deck-health conclusions
call Jin, Tournament Exposure, simulator, UI, or LLM behavior
read the wall clock
write files
```

Population output remains measured evidence only. Tournament authority depends
on the authority of the already-supplied canonical observations.

## Required Phase 40J Tests

```text
deterministic manifest identity and serialization
input-order independence
immutable nested values and no caller-input mutation
stable canonical-snapshot deduplication
duplicate exclusions and counts remain visible
resolved and ignored-by-policy records are excluded
private and unapproved observations are excluded
missing deck and snapshot identities fail closed
unresolved card identity fails closed
mainboard presence counts once per deck
sideboard and auxiliary inclusion require explicit flags
card, tag, package, commander, and exact partner-pair endpoint matching
partner-pair order normalization
unsupported endpoint rejection
direct card-to-tag anti-tautology rejection
count and coverage invariant enforcement
zero available-deck coverage remains unavailable
low-sample and low-coverage labels remain visible
RelationshipCountPacket compatibility
deterministic dictionary serialization
no runtime execution helpers
forbidden import and boundary scans
```

Tests must be local and fixture-free or use inline immutable packets. They must
not require a live network, database, provider, or wall clock.

## Forbidden Phase 40I Work

Phase 40I must not modify production code, tests, fixtures, schema,
repositories, SCHEMA_SPEC, dependencies, workflows, active scope, or either
constitution. It must not implement any Phase 40J behavior.

## Gate

Phase 40J may begin only after Phase 40I outside validation returns PASS or
PASS WITH REVIEW NOTES.
