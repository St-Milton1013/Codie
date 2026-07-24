# Phase 40E - Relationship Intelligence Metric Calculation Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase40E
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40F
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40E defines the pure, deterministic calculator boundary for the
constitutional Relationship Intelligence metric family. It consumes
already-counted, canonical population inputs and emits separately visible
metric values or explicit undefined reasons.

Phase 40E is documentation-only. It does not implement calculations,
population construction, persistence, repository reads, providers, Evidence
Fusion, recommendations, Jin, Tournament Exposure, simulator behavior, UI,
LLM calls, file writing, or network behavior.

## Authority

```text
docs/CODIE_V2_CONSTITUTION.md, Section 17
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT.md
docs/PHASE40C_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_IMPLEMENTATION_CONTRACT.md
```

## Future Input Packet

The future calculator must accept an immutable count packet containing:

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

The calculator must not query a database or construct these counts.

## Count Validation

Calculable inputs must satisfy:

```text
N > 0
0 <= nAB <= nA <= N
0 <= nAB <= nB <= N
0 <= matching_deck_count <= available_deck_count
0 <= coverage_ratio <= 1
coverage_ratio equals matching_deck_count / available_deck_count when the
available count is nonzero
```

Invalid arithmetic inputs fail closed with a typed build error. Coverage or
availability states that are valid but insufficient remain visible as
caveats or undefined reasons.

## Constitutional Formulas

Phase 40F must preserve these formulas exactly:

```text
P(A) = nA / N
P(B) = nB / N
P(A,B) = nAB / N

support = nAB / N

directional_confidence A->B = nAB / nA
directional_confidence B->A = nAB / nB

dependence_delta A->B = (nAB / nA) - (nB / N)
dependence_delta B->A = (nAB / nB) - (nA / N)

lift = (nAB / N) / ((nA / N) * (nB / N))

leverage = (nAB / N) - ((nA / N) * (nB / N))

jaccard_similarity = nAB / (nA + nB - nAB)

pmi = log2(lift)
```

Natural-log PMI, smoothed PMI, conditional-comparison delta, and combined
relationship scores are prohibited.

## Output Packet

The future result must expose:

```text
measurement_version
metric_bundle_version
population_manifest_id
population_manifest_version
population_spec_hash
endpoint identities
directionality
N
nA
nB
nAB
observed_co_occurrence
expected_co_occurrence
metric values
metric versions
metric orientations
undefined reasons
coverage_ratio
sample and availability labels
provenance_ref_ids
caveat_ids
calculated_at
```

Every metric remains a separate immutable value object. The field name
`confidence` is prohibited; only `directional_confidence` is allowed.

## Orientation Rules

Symmetric values use `undirected`:

```text
support
lift
leverage
jaccard_similarity
pmi
```

Directional values emit both `A_to_B` and `B_to_A`:

```text
directional_confidence
dependence_delta
```

Endpoint ordering for undirected identity must be deterministic without
changing directional semantics.

## Undefined Reasons

At minimum:

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

Undefined metrics serialize with `value: null` and a non-empty reason. Defined
metrics serialize with no undefined reason. Infinity, NaN, silent zero
coercion, and additive smoothing are prohibited.

When `nA` is zero, A-to-B confidence and dependence delta are undefined.
When `nB` is zero, B-to-A confidence and dependence delta are undefined.
When the Jaccard union is zero, Jaccard is undefined. When `nAB` is zero, PMI
is undefined. Support and leverage may remain defined at zero when `N > 0`.

## Sample And Coverage Labels

Thresholds are inputs and must be visible. The future calculator may emit:

```text
available
low_sample
low_coverage
insufficient_coverage
unavailable
```

Labels and caveats do not alter formulas. A low-sample value must not be
silently removed or promoted to high-confidence evidence.

## Determinism

The same count packet, versions, thresholds, and timestamp input must produce:

```text
equal numeric outputs
equal undefined reasons
stable metric ordering
byte-stable dictionary serialization
```

Floating-point outputs must be finite. No hidden rounding may alter persisted
values; display rounding belongs to a later presentation contract.

## Card-To-Tag Guardrail

Direct Tagger membership is ontology truth, not a measured relationship.
Measured card-to-tag calculations require a population and a separately
accepted leave-one-out or equivalent anti-tautology rule. Phase 40F must not
invent that rule.

## Future Public Interface

Phase 40F may contract a future module:

```text
codie/analytics/relationship_metrics.py
tests/test_relationship_metrics.py
codie/analytics/__init__.py, exports only
```

Expected future names:

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

## Forbidden Phase 40E Work

Phase 40E must not modify production, tests, schema, repositories,
SCHEMA_SPEC, dependencies, workflows, active scope, or either constitution.
It must not implement formulas, persistence, population resolution,
recommendations, causal claims, Jin, Tournament Exposure, simulator, UI, LLM,
network, or file-writing behavior.

## Gate

Phase 40F must not begin until Phase 40E outside validation returns PASS or
PASS WITH REVIEW NOTES.

