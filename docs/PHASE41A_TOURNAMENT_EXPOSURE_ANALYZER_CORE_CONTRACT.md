# Phase 41A - Tournament Exposure Analyzer Core Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase41A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 41A defines the constitutional boundary for the core V2 Tournament
Exposure Analyzer. It specifies a labeled independent-seat approximation,
approved exposure formulas, source-population controls, supported scopes,
reproducibility requirements, caveats, and future packet requirements.

Tournament Exposure is measured evidence. It remains separate from
Relationship Intelligence and does not produce pairing predictions,
matchup-strength claims, tournament placement predictions, causal claims,
recommendations, or persisted decisions.

Phase 41A is documentation-only. It does not implement models, calculations,
schema, migrations, repositories, providers, population readers, Evidence
Fusion integration, Decision Intelligence, Jin, UI, CLI, file writing, LLM
calls, or live network behavior.

## Authority Order

The governing sources are:

```text
docs/CODIE_V2_CONSTITUTION.md, Section 13
docs/CODIE_V2_CONSTITUTION.md, Section 37
```

Supporting planning inputs are:

```text
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/PHASE40K_RELATIONSHIP_INTELLIGENCE_CORE_CHECKPOINT_FREEZE_CONTRACT.md
```

The constitution controls if any planning input differs from it.

## Core Approximation

The first core V2 model is an independent-seat approximation.

For:

```text
p = canonical metagame share of the selected target in the source population
s = modeled opponent seats per round
r = modeled rounds
```

the approved formulas are:

```text
per_round_encounter_probability = 1 - (1 - p)^s
event_wide_encounter_probability = 1 - (1 - p)^(s * r)
expected_encounter_count = s * r * p
```

The default Commander pod assumption may use:

```text
s = 3 opponent seats
```

The chosen value remains explicit and caller-controlled. The model may not
silently derive seat count from attendance, standings, or event format.

The event-wide formula assumes independent seat draws with replacement. It
does not model Swiss pairing, pod construction, repeat-opponent suppression,
byes, standings, matchup strength, pilot skill, or correlated deck choice.

## Required Input Packet

Every future estimate must receive or resolve:

```text
region, country, store, or organizer scope as applicable
date window
expected attendance
number of rounds
event-size class
modeled opponent seats per round
target identity and target type
canonical metagame share
matching and available population counts
sample and coverage
confidence or availability label
pairing model identifier
population manifest identity
formula and numeric-policy versions
caller-supplied timestamp
```

Expected attendance and event-size class remain visible context in the core
model. They do not silently change the independent-seat formula.

The only supported pairing-model identifier in the core track is:

```text
independent_seat
```

An omitted optional pairing model resolves visibly to `independent_seat`.
Any Swiss, standings-aware, pod-aware, or other identifier returns an
unsupported-model result rather than falling back silently.

## Input Validation

Future calculations require:

```text
0 <= p <= 1
s is a positive integer
r is a positive integer
matching population count is nonnegative
available population count is positive
matching population count does not exceed available population count
coverage ratio is within [0, 1]
```

Invalid inputs produce visible validation errors. They are not clamped,
coerced, guessed, or silently replaced.

`p = 0` and `p = 1` are valid boundary values. Missing, unknown,
unsupported, unavailable, and zero remain distinct.

The canonical metagame share is:

```text
p = matching_population_count / available_population_count
```

If a caller supplies both the counts and a precomputed share, they must agree
under the declared numeric policy. A mismatch produces a visible validation
error.

## Required Scopes

The future analyzer must support source-population filters for:

```text
global
region
country
store
organizer
tournament-size class
date range
```

It must support target identities for:

```text
commander
exact partner pair
archetype
card
package
functional tag
```

Exact partner pairs are order-normalized and remain distinct from
single-commander populations.

Tag and package targets consume already-built canonical membership or packet
identities. Tournament Exposure does not create ontology or package truth.

## Source Population Contract

Every calculation must reference an immutable, reproducible population
manifest that exposes:

```text
population_manifest_id
population_version
population_specification_hash
observation_unit
source_snapshot_ids
source_record_count
available_population_count
matching_population_count
excluded_record_count
deduplicated_record_count
date window
geographic and organizer filters
tournament-size filter
target identity and identity version
deduplication policy and version
coverage ratio
generated_at supplied by the caller
provenance references
caveat references
```

The default observation unit is one canonical tournament deck instance.
Population inputs must come from already-built canonical observation packets
or accepted repositories. The analyzer may not read raw provider payloads,
private deck text, or live provider endpoints.

## Inclusion And Exclusion Rules

Future population resolution must:

```text
use canonical tournament deck-instance identity
exclude resolved and ignored-by-policy records
exclude private and unapproved observations
deduplicate exact duplicate records deterministically
preserve legitimate repeated-event appearances
preserve excluded and deduplicated counts
preserve exclusion reasons
preserve pilot, regional, temporal, and source concentration caveats
```

Personal decks may be compared with exposure evidence. They must never enter
global, regional, country, store, organizer, or tournament-size source
populations.

## Required Outputs

Every future exposure packet must expose:

```text
exposure_id
exposure_version
target identity and target type
population_manifest_id
population_specification_hash
metagame_share
modeled_opponent_seats_per_round
modeled_round_count
per_round_encounter_probability
event_wide_encounter_probability
expected_encounter_count
source population
sample size
matching population count
available population count
coverage ratio
confidence or availability label
formula identifiers
modeling assumptions
approximation warning
provenance references
caveat references
calculated_at supplied by the caller
```

The approximation warning must state clearly that the result is an
independent-seat estimate and is not a Swiss-pairing model.

## Comparison Outputs

For compatible population manifests, the analyzer may calculate:

```text
local_versus_global_delta
regional_versus_global_delta
```

Each delta is:

```text
selected_scope_event_wide_probability - global_event_wide_probability
```

Comparison packets must preserve both source exposure IDs, both population
manifests, compatible target identity, seat count, round count, date policy,
sample size, coverage, assumptions, and caveats.

Incompatible target identities, formula versions, seat counts, round counts,
or unresolved time policies produce visible comparison errors.

## Preparation Brief Boundary

The constitution requires a preparation brief. In the core track this means a
deterministic evidence summary containing:

```text
target label
selected scope
per-round estimate
event-wide estimate
comparison deltas when available
sample and coverage
assumptions
caveats
approximation warning
```

The brief may not choose cards, rank responses, prescribe deck changes,
generate matchup plans, or produce include, cut, replacement, or deck-health
language. Decision-bearing use requires Unified Evidence and Decision
Intelligence under later accepted contracts.

## Confidence And Coverage

Thresholds are explicit, configurable, versioned, and visible.

Future packets must distinguish:

```text
calculated
low_sample
low_coverage
unavailable
unsupported
invalid
```

Low sample or coverage may lower availability or confidence. It may not be
hidden or converted into a strategic conclusion.

## Reproducibility

Same canonical inputs, population manifest, formula version, seat count,
round count, and options must produce byte-stable dictionary serialization
and equal numeric outputs.

The numeric representation, exponentiation behavior, output precision, and
rounding mode must be explicit and versioned. A future implementation may use
an exact rational input and a deterministic decimal output, but it may not
depend on platform-default formatting or silently round intermediate values.

Every future calculation must preserve:

```text
formula version
population manifest identity
population specification hash
target identity and version
input metagame share
seat and round assumptions
all output values
sample and coverage
provenance
caveats
caller-supplied timestamp
```

No wall-clock read, random source, live network call, or hidden mutable state
may influence a result.

## Explicitly Deferred Modeling

The following are not part of the core independent-seat implementation:

```text
Swiss pairing
standings-aware pod formation
repeat-opponent modeling
byes
attendance-constrained sampling without replacement
commander clustering
pilot and deck dependence
matchup strength
win rate or placement forecasting
causal inference
simulation-backed pairing prediction
```

Any such model requires a separately accepted contract, a distinct model and
formula version, explicit validation fixtures, and visible comparison with
the independent-seat baseline.

## Evidence And Recommendation Boundary

Tournament Exposure output is simulator-independent measured evidence.

It may later:

```text
project accepted exposure references into Unified Evidence
support evidence comparison
be cited by Decision Intelligence
be summarized by Jin as labeled evidence
```

It may not:

```text
become tournament outcome truth
become simulator evidence
become Relationship Intelligence
directly generate recommendations
alter canonical observations
alter global evidence through user context
claim a target will be encountered
claim a matchup is favorable or unfavorable
```

## Future Packet Surfaces

Later accepted contracts may define immutable packet models for:

```text
TournamentExposureTarget
TournamentExposurePopulationSpec
TournamentExposurePopulationManifest
TournamentExposureAssumptions
TournamentExposureEstimate
TournamentExposureComparison
TournamentExposureCaveat
TournamentExposurePreparationBrief
TournamentExposureBundle
```

These names are reserved planning targets only. Phase 41A does not authorize
their implementation.

## Phase 41B Boundary

Phase 41B is the Tournament Exposure Independent-Seat Implementation
Contract. It may authorize a later pure, in-memory implementation of packet
models, validators, deterministic formulas, comparisons, and evidence-only
preparation briefs from already-built population inputs.

Phase 41B remains contract-only. It must not implement Swiss pairing, live
provider reads, schema, repositories, population ingestion, recommendations,
Jin, UI, LLM behavior, or file writing.

## Authorized Phase 41A Files

```text
docs/PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Active Scope Handling

This PR must not modify `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json`. The
authorized one-file transition on `main` set the trusted base scope to
Phase41A before this packet branch was created.

## Forbidden Work

Phase 41A must not add:

```text
production code
tests for implementation behavior
fixtures
schema or migrations
repositories or SQL
provider or source-table access
raw payload reads
population resolution
exposure calculations
comparison calculations
Evidence Fusion projection
Decision Intelligence output
Relationship Intelligence changes
Jin or Theory Corpus behavior
Swiss or pairing-aware modeling
simulation
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

Phase 41B remains blocked until Phase 41A receives artifact-backed PASS or
PASS WITH REVIEW NOTES.
