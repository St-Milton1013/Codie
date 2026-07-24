# Phase 40F - Relationship Intelligence Metric Calculation Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase40F
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40G
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40F authorizes a later Phase 40G implementation of the pure,
deterministic Relationship Intelligence metric calculator defined by Phase
40E. Phase 40F is documentation-only. It does not implement calculator code,
tests, persistence, population construction, providers, recommendations, Jin,
Tournament Exposure, simulator behavior, UI, LLM calls, file writing, or
network behavior.

## Governing Contracts

```text
docs/CODIE_V2_CONSTITUTION.md, Section 17
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/PHASE40E_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_CONTRACT.md
```

## Phase 40G Authorized Files

Phase 40G may modify only:

```text
codie/analytics/relationship_metrics.py
tests/test_relationship_metrics.py
codie/analytics/__init__.py, exports only
```

No schema, repository, provider, fixture, dependency, workflow, CLI, UI,
simulator, recommendation, or governance implementation file is authorized.

## Required Public Interface

Phase 40G must expose:

```text
RELATIONSHIP_METRIC_VERSION
RelationshipMetricBuildError
RelationshipCountPacket
RelationshipMetricValue
RelationshipMetricBundle
build_relationship_metric_bundle(...)
relationship_metric_bundle_to_dict(...)
validate_relationship_count_packet(...)
validate_relationship_metric_bundle(...)
```

The public value objects must be immutable. Collection and metadata fields
must use immutable JSON-compatible values. Caller-owned input objects must
not be mutated.

## Input Packet

`RelationshipCountPacket` must preserve:

```text
count_packet_version
population_manifest_id
population_manifest_version
population_spec_hash
source_endpoint_type
source_endpoint_id
target_endpoint_type
target_endpoint_id
directionality
N
nA
nB
nAB
candidate_population_count
usable_population_count
unknown_or_excluded_count
deduplicated_population_count
matching_deck_count
available_deck_count
coverage_ratio
low_sample_threshold
low_coverage_threshold
provenance_ref_ids
caveat_ids
```

Count fields must be integers and must reject booleans. Ratios and thresholds
must be finite numeric values. IDs, versions, hashes, endpoint types, and
endpoint IDs must be non-empty strings. Reference IDs must be non-empty,
unique strings with stable ordering.

## Input Invariants

The builder must reject:

```text
N <= 0
negative counts
nA > N
nB > N
nAB > nA
nAB > nB
matching_deck_count > available_deck_count
coverage_ratio outside [0, 1]
coverage_ratio inconsistent with matching_deck_count / available_deck_count
when available_deck_count is nonzero
non-finite numeric inputs
duplicate reference IDs
unsupported directionality
```

When `available_deck_count` is zero, the packet must use a visible unavailable
coverage state rather than inventing a ratio from a zero denominator.

## Exact Calculations

Phase 40G must calculate:

```text
P(A) = nA / N
P(B) = nB / N
P(A,B) = nAB / N

support = nAB / N

directional_confidence A_to_B = nAB / nA
directional_confidence B_to_A = nAB / nB

dependence_delta A_to_B = (nAB / nA) - (nB / N)
dependence_delta B_to_A = (nAB / nB) - (nA / N)

lift = (nAB / N) / ((nA / N) * (nB / N))

leverage = (nAB / N) - ((nA / N) * (nB / N))

jaccard_similarity = nAB / (nA + nB - nAB)

pmi = log2(lift)
```

No smoothing, natural-log PMI, alternate dependence delta, hidden weighting,
display rounding, or combined relationship score is authorized.

## Metric Value Shape

Each `RelationshipMetricValue` must preserve:

```text
metric_name
metric_version
orientation
value
numerator
denominator
undefined_reason
```

Symmetric metrics use `undirected`:

```text
support
lift
leverage
jaccard_similarity
pmi
```

Directional metrics emit both `A_to_B` and `B_to_A`:

```text
directional_confidence
dependence_delta
```

The field name `confidence` is prohibited. Metric ordering must be a declared,
stable order rather than incidental dictionary ordering.

## Undefined Values

Undefined metrics must serialize with `value: null` and exactly one non-empty
reason. Defined metrics must use a finite numeric value and no undefined
reason.

Supported reasons include:

```text
EMPTY_POPULATION
ENDPOINT_A_NOT_OBSERVED
ENDPOINT_B_NOT_OBSERVED
ZERO_UNION_JACCARD_UNDEFINED
ZERO_JOINT_PMI_UNDEFINED
UNKNOWN_ENDPOINT_COVERAGE
INSUFFICIENT_USABLE_POPULATION
LOW_SAMPLE_SIZE
LOW_COVERAGE
```

Phase 40G must preserve these behaviors:

```text
nA == 0 makes A_to_B directional metrics undefined
nB == 0 makes B_to_A directional metrics undefined
nA + nB - nAB == 0 makes Jaccard undefined
nAB == 0 makes PMI undefined
support and leverage remain defined at zero when N > 0
NaN and infinity are never serialized
undefined values are never silently coerced to zero
```

Low-sample and low-coverage states remain visible labels or caveats and do not
alter the constitutional formulas.

## Output Bundle

`RelationshipMetricBundle` must preserve:

```text
measurement_version
metric_bundle_version
population_manifest_id
population_manifest_version
population_spec_hash
source_endpoint_type
source_endpoint_id
target_endpoint_type
target_endpoint_id
directionality
N
nA
nB
nAB
observed_co_occurrence
expected_co_occurrence
metrics
undefined_reasons
coverage_ratio
sample_label
availability_label
provenance_ref_ids
caveat_ids
calculated_at
```

`observed_co_occurrence` is `nAB`. `expected_co_occurrence` is
`(nA * nB) / N`. The caller must supply `calculated_at`; the calculator must
not read the wall clock.

## Identity And Serialization

Endpoint identities must remain visible in their supplied directional order.
An internal canonical pair may be used only for stable undirected identity and
must not reverse directional outputs.

Dictionary serialization must be deterministic and JSON-compatible. The same
packet, versions, thresholds, and timestamp must produce equal bundles and
byte-stable canonical JSON dictionaries. No raw provider payload or private
user content may be accepted as metadata.

## Card-To-Tag Guardrail

Phase 40G must not calculate direct card-to-Tagger membership as a measured
relationship. No leave-one-out or anti-tautology method is authorized by this
contract. Such inputs must fail closed or remain explicitly unsupported.

## Required Tests

Phase 40G must add focused tests for:

```text
all constitutional formulas using hand-calculated fixtures
both directional orientations
stable metric ordering
deterministic dictionary serialization
immutable value objects and immutable nested values
caller input immutability
count invariant rejection
boolean count rejection
finite numeric validation
coverage ratio consistency
duplicate reference rejection
zero endpoint undefined behavior
zero-union Jaccard behavior
zero-joint PMI behavior
zero support and leverage remaining defined
no NaN or infinity serialization
sample and coverage label visibility
threshold visibility
provided timestamp preservation
no wall-clock reads
no smoothing, rounding, alternate formulas, or combined score
card-to-tag anti-tautology rejection
no database, repository, provider, recommendation, simulator, UI, LLM,
network, or file-writing imports or behavior
```

Focused tests must run without a database and without network access.

## Forbidden Phase 40F Work

Phase 40F must not modify:

```text
codie/
tests/
ui/
scripts/
schemas/
codie/db/
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

Phase 40G implementation must not begin until Phase 40F outside validation
returns PASS or PASS WITH REVIEW NOTES.
