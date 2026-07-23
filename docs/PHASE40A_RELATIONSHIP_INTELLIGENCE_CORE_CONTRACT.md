# Phase 40A - Relationship Intelligence Core Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase40A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40A defines the constitutional boundary for Relationship Intelligence,
co-occurrence, and co-dependence. It specifies typed relationship evidence,
approved deterministic pair metrics, population controls, provenance,
caveats, and future packet requirements.

Relationship Intelligence is Class 2 measured evidence. It may later project
accepted measurements into Unified Evidence, but it does not produce
recommendations, causal claims, package truth, rules truth, strategic
conclusions, or tournament predictions.

Phase 40A is documentation-only. It does not implement models, calculations,
schema, migrations, repositories, providers, analytics integration, Evidence
Fusion integration, Decision Intelligence, Jin, UI, CLI, file writing, LLM
calls, or live network behavior.

## Authority Order

The governing source is:

```text
docs/CODIE_V2_CONSTITUTION.md, Section 17
```

Supporting planning inputs are:

```text
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/design_inputs/v2_intelligence_program/README.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_RELATIONSHIP_INTELLIGENCE_PROPOSAL.md
```

The design proposal is non-authoritative. Where it differs from Constitution
V2, the constitution controls. In particular:

```text
dependence_delta A->B = P(B|A) - P(B)
dependence_delta B->A = P(A|B) - P(A)
PMI = log2(lift)
```

The proposal's alternative conditional-comparison delta and natural-log PMI
must not replace these constitutional formulas. A future separately named
metric may be proposed only through a new accepted contract.

## Evidence Boundary

Relationship Intelligence may:

```text
consume canonical identity references
consume approved immutable population manifests
measure deterministic endpoint presence
calculate approved pair metrics
preserve typed relationship evidence
emit measured-evidence packets
emit caveats, conflicts, and unsupported states
```

It may not:

```text
read raw provider payloads directly
read private user deck text directly
insert user decks into global populations
declare ontology membership
declare combo membership
declare rules interactions
declare package truth
infer causal mechanisms
rank cards or packages
generate include, cut, replacement, or deck-health output
collapse metrics into a synergy score
call an LLM
```

## Typed Relationship Model

Every future relationship edge must declare:

```text
relationship_id
relationship_type
evidence_class
source_endpoint_id
target_endpoint_id
directionality
population_manifest_id, when measured
measurement_id, when measured
authority_ref_ids, when structural
provenance_ref_ids
caveat_ids
metric_version or relationship_version
generated_at
```

Required endpoint categories include:

```text
card
functional tag
package
combo
combo output
converter
commander signature
deck snapshot reference
tournament deck instance
event
region
attributed theory claim
```

Relationship types must distinguish at least:

```text
measured co_occurrence
Tagger membership
Spellbook combo membership
rules interaction
curated package membership
theory attribution
observational event or region membership
```

Statistical co-occurrence must never be serialized as ontology, combo, rules,
package, or theory truth.

## Observation Units

The default observation unit is one canonical tournament deck instance.
Every population manifest must declare its observation unit. Alternative units
require an accepted contract and a distinct population version.

Endpoint projection must preserve:

```text
present
absent
unknown
```

Unknown must not be counted as absent. Unavailable, unsupported,
not-applicable, and zero remain distinct where the packet shape requires them.

## Required Counts

For each ordered or unordered endpoint pair `A`, `B`:

```text
N   = usable canonical population deck count
nA  = usable decks containing A
nB  = usable decks containing B
nAB = usable decks containing both A and B
```

Future packets must also disclose:

```text
candidate population count
usable population count
unknown or excluded count
deduplicated population count
observed co-occurrence
expected co-occurrence under independence
```

Counts must satisfy:

```text
0 <= nAB <= nA <= N
0 <= nAB <= nB <= N
N > 0 for calculated metrics
```

## Approved Metric Family

For a selected canonical population:

```text
P(A)   = nA / N
P(B)   = nB / N
P(A,B) = nAB / N

support = nAB / N

directional_confidence_A_to_B = nAB / nA
directional_confidence_B_to_A = nAB / nB

dependence_delta_A_to_B = (nAB / nA) - (nB / N)
dependence_delta_B_to_A = (nAB / nB) - (nA / N)

lift = (nAB / N) / ((nA / N) * (nB / N))

leverage = (nAB / N) - ((nA / N) * (nB / N))

jaccard_similarity = nAB / (nA + nB - nAB)

PMI = log2(lift)
```

Every metric must remain separately visible. No opaque combined score is
allowed.

The bare field name `confidence` is prohibited in pair-detail packets.
`directional_confidence` is an association metric, not epistemic,
recommendation, or causal confidence.

## Undefined And Zero Handling

Future implementations must return visible null reasons instead of division
errors, infinities, or silent coercion.

Minimum required reasons:

```text
EMPTY_POPULATION
ENDPOINT_A_NOT_OBSERVED
ENDPOINT_B_NOT_OBSERVED
ZERO_UNION_JACCARD_UNDEFINED
ZERO_JOINT_PMI_UNDEFINED
UNKNOWN_ENDPOINT_COVERAGE
INSUFFICIENT_USABLE_POPULATION
```

No additive smoothing is allowed for the constitutional metric family.

## Population Controls

Every population result must expose:

```text
commander or exact partner-pair scope
zone scope
date range
region
store
organizer
event-size filter
placement filter
canonical and deduplicated population size
population specification version
population specification hash
source snapshot or manifest references
```

The calculation must control or visibly caveat:

```text
color identity
commander restrictions
generic-staple prevalence
repeated deck snapshots
pilot concentration
regional effects
release recency
date-aware legality
missing coverage
known combo membership
known package membership
placement selection bias
```

User decks may be compared with a population but must never become members of
commander, tournament, winner, regional, or global averages.

## Deduplication

The future population resolver must:

```text
use canonical deck-instance identity
preserve repeated-event identity
deduplicate exact duplicate records deterministically
preserve duplicate and concentration caveats
record the deduplication policy and version
avoid silently removing legitimate repeat appearances
```

## Card-To-Tag Aggregation

Core V2 includes deterministic card-to-tag aggregation. Future contracts must
distinguish:

```text
direct Tagger ontology membership
deck-level tag presence
tagged-card copy count
distinct tagged-card count
tag density
measured card-to-tag association
```

Direct ontology membership carries no support, lift, leverage, PMI, or
dependence delta by itself. A measured card-to-tag relationship requires a
population and must avoid same-card tautology through a documented
leave-one-out or equivalent rule.

## Provenance And Reproducibility

Every future measurement must preserve:

```text
measurement_id
metric_version
population_manifest_id
population_specification_hash
endpoint identities and identity versions
N, nA, nB, nAB
source snapshot references
canonical deck-instance references or reproducible manifest reference
formula identifiers
calculated_at
coverage ratio
low-sample label
caveats and confounders
```

Same canonical inputs, population specification, metric version, and options
must produce byte-stable dictionary serialization and equal numeric outputs.

## Low-Sample And Coverage Boundary

Thresholds must be explicit, versioned, and visible. A future implementation
must preserve at least:

```text
coverage_ratio
matching_deck_count
available_deck_count
low_sample_threshold
low_coverage_threshold
stability or availability label
caveat IDs
```

Low sample or coverage may reduce availability or stability. It must never be
hidden, and it must not be converted into a strategic conclusion.

## Future Packet Surfaces

Later accepted contracts may define immutable packet models for:

```text
RelationshipEndpointRef
RelationshipPopulationSpec
RelationshipPopulationManifest
RelationshipContingencyCounts
RelationshipMetricValue
RelationshipCaveat
RelationshipProvenance
RelationshipMeasurement
RelationshipMeasurementBundle
```

Names are reserved planning targets only. Phase 40A does not authorize their
implementation.

## Phase 40B Boundary

Phase 40B is the Relationship Intelligence Schema and Repository Contract. It
may specify migrations, indexes, repository methods, immutable population
manifest storage, replay identity, and rollback behavior.

Phase 40B remains contract-only unless its accepted contract explicitly says
otherwise. It must not implement metric calculations, recommendations, Jin,
Tournament Exposure, UI, or graph-database infrastructure.

## Authorized Phase 40A Files

```text
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Active Scope Handling

This PR must not modify `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`. The
protected scope remains Phase39D until this contract packet is merged. The
Phase40A transition must use the approved protected-scope governance path.

## Forbidden Work

Phase 40A must not add:

```text
production code
tests for implementation behavior
fixtures
schema or migrations
repositories or SQL
provider or source-table access
raw payload reads
metric calculations
population resolution
Evidence Fusion projection
Decision Intelligence output
Tournament Exposure
Jin or Theory Corpus behavior
UI, CLI, or file writing
LLM or live network calls
dependencies
validator or workflow changes
active validation scope changes
constitution changes
```

## Required Validation

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Phase 40B remains blocked until Phase 40A receives artifact-backed PASS or
PASS WITH REVIEW NOTES.
