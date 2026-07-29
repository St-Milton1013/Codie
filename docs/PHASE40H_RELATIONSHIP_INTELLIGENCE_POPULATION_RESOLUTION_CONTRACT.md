# Phase 40H - Relationship Intelligence Population Resolution Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase40H
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40I
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Purpose

Phase 40H defines the deterministic boundary that converts an already supplied
canonical deck population into the count packet consumed by the Phase 40G
Relationship Intelligence metric calculator.

Phase 40H is documentation-only. It does not implement population resolution,
repository reads, persistence, providers, metrics, recommendations, Jin,
Tournament Exposure, simulator behavior, UI, LLM calls, file writing, or
network behavior.

## Authority

```text
docs/CODIE_V2_CONSTITUTION.md, Sections 8, 9, 10, 11, and 17
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT.md
docs/PHASE40C_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_IMPLEMENTATION_CONTRACT.md
docs/PHASE40E_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_CONTRACT.md
docs/PHASE40F_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_CONTRACT.md
codie/analytics/relationship_metrics.py
```

## Governing Principle

```text
immutable population specification
+ canonical deck-presence records
+ endpoint definitions
= immutable population manifest
+ RelationshipCountPacket
+ visible exclusions and caveats
```

The same normalized inputs, versions, and options must produce the same
manifest identity, membership order, endpoint counts, exclusions, and count
packet. No wall clock, random source, live provider, or hidden default may
change the result.

## Future Input Boundary

A later implementation contract may authorize pure, in-memory population
resolution from already supplied packets containing:

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
deck_presence_records
source_endpoint
target_endpoint
calculated_at
low_sample_threshold
low_coverage_threshold
provenance_ref_ids
caveat_ids
```

Inputs must already use canonical card identities. Raw provider payloads,
private deck text, unresolved card names, source-table rows, and live API
responses are forbidden.

## Population Manifest

The future immutable manifest must preserve:

```text
population_manifest_id
population_manifest_version
population_spec_hash
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
candidate_population_count
usable_population_count
unknown_or_excluded_count
deduplicated_population_count
member_deck_ids
excluded_deck_records
provenance_ref_ids
caveat_ids
calculated_at
```

Manifest identity must derive from normalized semantic inputs. It must not
derive from incidental input ordering, process identity, or the current time.
Member IDs, source snapshot IDs, provenance refs, and caveats must serialize in
declared stable order.

## Canonical Deck Membership

Each candidate deck must have a stable canonical deck or snapshot identity.
Population resolution must:

```text
reject missing or blank canonical deck identities
reject unresolved card identities from usable membership
deduplicate only through an explicit deterministic policy
preserve a visible record for every exclusion
preserve the count removed by deduplication
exclude private user decks from global evidence unless they are approved observations
keep sideboard-only and auxiliary objects out of normal mainboard presence counts
unless the population specification explicitly includes them
```

Duplicate resolution must use a declared stable key and tie-break rule.
Input order must never decide which duplicate survives.

## Inactive Status Policy

Resolved and ignored-by-policy records must be excluded by default through a
declared inactive-status policy. If a future option supports including either
status, the option and resulting counts must remain visible in the manifest.
No inactive item may re-enter the population through an undocumented default.

## Endpoint Presence

Endpoint presence is binary per usable deck:

```text
N = usable population deck count
nA = usable decks containing endpoint A
nB = usable decks containing endpoint B
nAB = usable decks containing both endpoints
```

Multiple copies or multiple matching cards in one deck count once for endpoint
presence. Presence records must retain the canonical identities that justified
membership without exposing raw provider payloads.

Supported endpoint types must be explicit and versioned. At minimum the
population contract anticipates:

```text
card
tag
package
commander
commander_pair
```

Unsupported endpoint types must fail closed.

## Tag Presence And Anti-Tautology

Tag presence must consume already-built canonical functional-tag assignments.
Population resolution must not call Scryfall Tagger or infer tags.

Direct card-to-tag measured relationships remain prohibited unless a later
accepted contract defines a leave-one-out or equivalent anti-tautology rule.
Phase 40H does not define or authorize that rule.

## Coverage And Exclusions

The future resolver must preserve:

```text
candidate_population_count
usable_population_count
unknown_or_excluded_count
deduplicated_population_count
matching_deck_count
available_deck_count
coverage_ratio
```

Count relationships must be validated and must not be inferred silently.
When `available_deck_count` is zero, coverage must remain visibly unavailable.
Low sample and low coverage must create visible labels or caveats and must not
change endpoint counts.

Every excluded record must preserve:

```text
deck_id or candidate identity
reason_code
source_snapshot_id when available
detail safe for serialization
```

Unknown, unavailable, unsupported, excluded, and deduplicated are distinct
states and must not be collapsed.

## Output Boundary

The future resolver may emit:

```text
RelationshipPopulationManifest
RelationshipPopulationResolution
RelationshipCountPacket
```

The emitted `RelationshipCountPacket` must match the public Phase 40G input
contract exactly. The resolver must not calculate support, confidence,
dependence delta, lift, leverage, Jaccard similarity, PMI, rankings, combined
scores, causal claims, recommendations, or deck-health conclusions.

## Privacy And Evidence Boundary

Population output is measured evidence only. It is not tournament evidence
unless its canonical inputs are approved tournament observations. It must not
contain raw provider payloads, raw primer bodies, private import text, user
notes, secrets, credentials, or unrestricted metadata.

Primer context, simulator evidence, and user context may not alter global
population membership. Private user decks may be compared with a population
but may not enter the population without approved-observation status.

## Future Validation Requirements

A later implementation contract must require tests for:

```text
deterministic manifest identity and serialization
input-order independence
immutable packets and no caller-input mutation
stable deterministic deduplication
duplicate-count visibility
default inactive-status exclusion
explicit inactive-status inclusion when supported
canonical identity enforcement
private user deck exclusion
mainboard presence counted once per deck
sideboard and auxiliary exclusion by default
card, tag, package, commander, and partner-pair endpoint presence
unsupported endpoint rejection
direct card-to-tag anti-tautology rejection
count and coverage invariants
zero available-deck coverage state
visible low-sample and low-coverage caveats
visible exclusion reasons
RelationshipCountPacket compatibility
forbidden import and boundary scans
```

Tests must be fixture-first and must not require a live network, database, or
provider.

## Forbidden Phase 40H Work

Phase 40H must not modify production code, tests, fixtures, schema,
repositories, SCHEMA_SPEC, dependencies, workflows, active scope, or either
constitution. It must not implement population resolution, repository access,
persistence, providers, metric calculation, recommendations, Jin, Tournament
Exposure, simulator behavior, UI, LLM calls, file writing, or network access.

## Gate

Phase 40I may begin only after Phase 40H outside validation returns PASS or
PASS WITH REVIEW NOTES. Phase 40I must remain an implementation contract unless
accepted governance explicitly authorizes a different packet shape.
