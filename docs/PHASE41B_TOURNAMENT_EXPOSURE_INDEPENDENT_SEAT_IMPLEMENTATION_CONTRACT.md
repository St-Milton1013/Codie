# Phase 41B - Tournament Exposure Independent-Seat Implementation Contract

Status: implementation contract only

## Validation Tuple

```text
phase_id: Phase41B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 41B authorizes a later Phase 41C implementation of the pure, in-memory,
deterministic independent-seat Tournament Exposure packet models, validators,
calculator, compatible-scope comparisons, and evidence-only preparation
briefs defined by Phase 41A.

Phase 41B is documentation-only. It does not implement code, tests, fixtures,
schema, repositories, observation ingestion, providers, Swiss pairing,
recommendations, Jin, simulator behavior, UI, LLM calls, file writing, or
network behavior.

## Governing Contracts

```text
docs/CODIE_V2_CONSTITUTION.md, Sections 13 and 37
docs/PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
```

## Phase 41C Authorized Files

Phase 41C may modify only:

```text
codie/analytics/tournament_exposure.py
tests/test_tournament_exposure.py
codie/analytics/__init__.py, exports only
```

No schema, repository, provider, fixture, dependency, workflow, CLI, UI,
simulator, recommendation, Jin, or governance implementation file is
authorized.

## Required Public Interface

Phase 41C must expose:

```text
TOURNAMENT_EXPOSURE_VERSION
INDEPENDENT_SEAT_MODEL_ID
TournamentExposureBuildError
TournamentExposureTarget
TournamentExposurePopulationManifest
TournamentExposureAssumptions
TournamentExposureEstimate
TournamentExposureComparison
TournamentExposurePreparationBrief
TournamentExposureBundle
build_tournament_exposure_estimate(...)
build_tournament_exposure_comparison(...)
build_tournament_exposure_preparation_brief(...)
build_tournament_exposure_bundle(...)
tournament_exposure_estimate_to_dict(...)
tournament_exposure_comparison_to_dict(...)
tournament_exposure_preparation_brief_to_dict(...)
tournament_exposure_bundle_to_dict(...)
validate_tournament_exposure_population_manifest(...)
validate_tournament_exposure_estimate(...)
validate_tournament_exposure_bundle(...)
```

Public value objects must be immutable. Nested collections and metadata must
use immutable JSON-compatible values. Caller-owned objects must not be
mutated.

## Target Packet

`TournamentExposureTarget` must preserve:

```text
target_type
target_id
target_version
display_label
component_ids
provenance_ref_ids
```

Allowed target types:

```text
commander
partner_pair
archetype
card
package
functional_tag
```

Partner pairs require exactly two distinct component IDs and deterministic
order normalization. Other target types reject partner-pair components unless
their accepted canonical identity contract requires components explicitly.

Target packets consume canonical IDs. They do not infer archetype, ontology,
package, combo, or card identity.

## Population Manifest Packet

`TournamentExposurePopulationManifest` must preserve:

```text
population_manifest_id
population_version
population_spec_hash
observation_unit
scope_type
scope_key
region
country
store
organizer
tournament_size_class
date_start
date_end
source_snapshot_ids
source_record_count
available_population_count
matching_population_count
excluded_record_count
deduplicated_record_count
target
deduplication_policy
deduplication_version
coverage_numerator
coverage_denominator
coverage_ratio
low_sample_threshold
low_coverage_threshold
generated_at
provenance_ref_ids
caveat_ids
```

The observation unit must be:

```text
canonical_tournament_deck_instance
```

Allowed scope types:

```text
global
region
country
store
organizer
tournament_size
```

`global` uses the stable scope key `global`. Other scope types require a
non-empty applicable scope key. Scope metadata that is not applicable remains
null rather than receiving invented values.

`coverage_ratio` and `low_coverage_threshold` use canonical decimal strings
under the declared numeric policy. Counts and dates remain their native
integer and ISO date representations.

## Population Invariants

The implementation must reject:

```text
negative counts
boolean count values
available_population_count <= 0
matching_population_count > available_population_count
excluded_record_count > source_record_count
deduplicated_record_count > source_record_count
coverage_denominator <= 0
coverage_numerator > coverage_denominator
coverage ratio outside [0, 1]
coverage ratio inconsistent with its integer numerator and denominator
date_end earlier than date_start
empty or duplicate source, provenance, or caveat references
unsupported observation units, scope types, or target types
non-finite numeric values
```

The manifest receives already-built counts and identities. Phase 41C must not
read deck records, source tables, provider payloads, private deck text,
repositories, or live endpoints to construct or verify them.

## Assumptions Packet

`TournamentExposureAssumptions` must preserve:

```text
model_id
model_version
formula_version
numeric_policy_version
expected_attendance
event_size_class
opponent_seats_per_round
round_count
approximation_label
approximation_warning
```

Required values:

```text
model_id = independent_seat
expected_attendance is a positive integer
opponent_seats_per_round is a positive integer
round_count is a positive integer
event_size_class is non-empty
```

The warning must state that the model is an independent-seat approximation
and is not a Swiss-pairing model. Expected attendance and event-size class are
visible context only and must not alter the core formulas.

Any other pairing-model identifier returns a visible unsupported-model error.

## Exact Arithmetic And Numeric Policy

Phase 41C must derive:

```text
p = matching_population_count / available_population_count
seat_opportunities_per_event = opponent_seats_per_round * round_count

per_round_encounter_probability =
    1 - (1 - p)^opponent_seats_per_round

event_wide_encounter_probability =
    1 - (1 - p)^seat_opportunities_per_event

expected_encounter_count =
    seat_opportunities_per_event * p
```

Intermediate calculations must use exact integer-ratio arithmetic. Floating
point may not determine equality, validation, or intermediate results.

Output numeric values must serialize as canonical decimal strings under:

```text
precision: 12 digits after the decimal point
rounding: ROUND_HALF_EVEN
range: probability values remain within [0, 1]
```

Trailing zero policy must be stable and documented in
`numeric_policy_version`. Rounding occurs only when the final output value is
serialized. Exact numerator and denominator values for metagame share remain
visible.

No random source, wall-clock read, platform-default decimal formatting, or
hidden mutable state may affect the result.

## Estimate Packet

`TournamentExposureEstimate` must preserve:

```text
exposure_id
exposure_version
target
population_manifest_id
population_version
population_spec_hash
model_id
model_version
formula_version
numeric_policy_version
metagame_share_numerator
metagame_share_denominator
metagame_share
expected_attendance
event_size_class
opponent_seats_per_round
round_count
seat_opportunities_per_event
per_round_encounter_probability
event_wide_encounter_probability
expected_encounter_count
matching_population_count
available_population_count
sample_size
coverage_ratio
confidence_label
assumptions
approximation_warning
provenance_ref_ids
caveat_ids
calculated_at
```

The caller supplies `calculated_at`. The module must not read the wall clock.
Caller timestamps require an ISO 8601 timezone and normalize deterministically
to UTC without changing the represented instant.

## Confidence Labels

Phase 41C must derive one visible label from the declared thresholds:

```text
SUFFICIENT
LIMITED_SAMPLE
LIMITED_COVERAGE
LIMITED_SAMPLE_AND_COVERAGE
```

`matching_population_count < low_sample_threshold` yields a sample
limitation. `coverage_ratio < low_coverage_threshold` yields a coverage
limitation. Labels do not alter formulas and are not recommendation
confidence.

## Comparison Packet

`TournamentExposureComparison` may represent:

```text
local_versus_global
regional_versus_global
```

The delta is:

```text
selected_scope_event_wide_probability - global_event_wide_probability
```

Comparison requires:

```text
equal target type, ID, and version
equal model, formula, and numeric-policy versions
equal opponent seats and round count
compatible date policy
one global baseline
selected scope matching the comparison type
```

The packet must preserve both exposure IDs, both population manifests, both
event-wide values, the signed delta, both sample and coverage values, all
assumptions, provenance, caveats, and caller-supplied calculation time.

Incompatible estimates raise a visible build error. They are not coerced or
compared approximately.

## Preparation Brief Packet

`TournamentExposurePreparationBrief` must be deterministic structured
evidence containing:

```text
brief_id
brief_version
exposure_id
comparison_ids
target label
scope label
per-round estimate
event-wide estimate
comparison deltas
sample and coverage
confidence label
assumptions
caveats
approximation warning
generated_at supplied by the caller
```

The brief must not choose cards, rank responses, prescribe deck changes,
generate matchup plans, or emit include, cut, replacement, or deck-health
language.

## Bundle And Serialization

`TournamentExposureBundle` must preserve stable ordering of:

```text
population manifests
estimates
comparisons
preparation briefs
provenance references
caveat references
```

Duplicate IDs, dangling references, mismatched targets, and inconsistent
versions must fail validation.

Dictionary serialization must be deterministic and JSON-compatible. The same
canonical packet inputs, versions, timestamps, and options must produce equal
objects and byte-stable canonical dictionaries.

## Deterministic Identity

The builders must derive exposure, comparison, brief, and bundle IDs as
versioned SHA-256 identities over canonical JSON identity payloads.

Identity payloads must expose their version and use only:

```text
canonical target identity
population manifest identity and specification hash
model, formula, and numeric-policy versions
seat, round, attendance, and event-size assumptions
referenced estimate or comparison IDs
caller-supplied timestamp
```

Presentation labels, incidental input ordering, and mutable mapping order may
not change identity. Duplicate IDs in a bundle fail visibly.

Raw provider payloads, private deck text, source HTML, primer bodies, simulator
traces, and unrestricted metadata are prohibited.

## Required Tests

Phase 41C must add focused tests for:

```text
hand-calculated p = 0, p = 1, and fractional-share formulas
per-round and event-wide probability
expected encounter count
exact rational intermediate arithmetic
12-place ROUND_HALF_EVEN output
stable trailing-zero policy
deterministic dictionary serialization
immutable value objects and immutable nested values
caller input immutability
partner-pair order normalization
all target and scope types
population count invariant rejection
boolean count rejection
coverage ratio consistency
date range validation
duplicate and empty reference rejection
unsupported pairing-model rejection
expected attendance remaining formula-neutral
sample and coverage confidence labels
local-versus-global comparison
regional-versus-global comparison
incompatible comparison rejection
evidence-only preparation brief content
provided timestamp preservation
timezone normalization
deterministic SHA-256 packet identities
no wall-clock reads
no NaN, infinity, float-dependent equality, or hidden rounding
no Swiss, standings, pod, repeat-opponent, bye, matchup, placement, or win-rate logic
no database, repository, provider, recommendation, simulator, Jin, UI, LLM,
network, or file-writing imports or behavior
```

Focused tests must run without a database and without network access.

## Forbidden Phase 41B Work

Phase 41B must not modify:

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

## Authorized Phase 41B Files

```text
docs/PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Active Scope Handling

This PR must not modify `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`. The
authorized one-file transition on `main` set the trusted base scope to
Phase41B before this packet branch was created.

## Gate

Phase 41C implementation must not begin until Phase 41B outside validation
returns PASS or PASS WITH REVIEW NOTES.
