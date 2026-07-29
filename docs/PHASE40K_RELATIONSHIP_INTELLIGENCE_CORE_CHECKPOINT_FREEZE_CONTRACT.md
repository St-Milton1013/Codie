# Phase 40K - Relationship Intelligence Core Checkpoint / Freeze Contract

Status: checkpoint and freeze only

## Validation Tuple

```text
phase_id: Phase40K
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41A
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 41A is reserved for the Tournament Exposure Analyzer Core Contract. It
remains blocked until Phase 40K outside validation returns PASS or PASS WITH
REVIEW NOTES.

## Purpose

Phase 40K closes the Relationship Intelligence foundation after the accepted
schema/repository, metric-calculation, and population-resolution work.

This packet freezes the accepted public surfaces and records that the core
co-occurrence and co-dependence evidence path is implemented:

```text
canonical population records
-> deterministic population manifest and RelationshipCountPacket
-> constitutional relationship metric bundle
-> optional repository persistence through the accepted repository boundary
```

Phase 40K is documentation-only. It does not implement runtime behavior,
schema, repositories, providers, recommendations, Jin, Tournament Exposure,
simulator behavior, UI, LLM calls, file writing, network behavior, or
dependencies.

## Phase 40J Acceptance Evidence

```text
workflow run ID: 30497683444
validated SHA: 8f27099334635f2a508645ccc58bd3f033321840
artifact: codie-phase_ledger-validation-8f27099334635f2a508645ccc58bd3f033321840
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
severity totals: BLOCKER 0, CRITICAL 0, HIGH 0, MEDIUM 0, LOW 0, INFORMATIONAL 0
skipped validators: none
unresolved findings: none
errors: none
final governance verdict: PASS
```

## Frozen Surfaces

The following accepted implementation surfaces remain authoritative:

```text
codie/db/schema/analytics.sql
codie/db/repositories/analytics.py
codie/analytics/relationship_metrics.py
codie/analytics/relationship_population.py
codie/analytics/__init__.py
tests/test_relationship_schema_repository.py
tests/test_relationship_metrics.py
tests/test_relationship_population.py
```

Future changes to these surfaces require a new accepted contract. Phase 40K
does not modify them.

## Frozen Evidence Rules

```text
Relationship Intelligence remains measured evidence.
No metric is causal evidence.
No opaque combined synergy score exists.
The bare field confidence is not an epistemic claim.
Every metric remains separately visible.
Unknown, unavailable, excluded, deduplicated, unsupported, and zero remain distinct.
Direct card-to-tag measurement remains blocked without an accepted anti-tautology rule.
Private user records do not enter global populations without explicit approved-observation status.
Simulator evidence does not become tournament evidence.
Population and metric calculations do not generate recommendations.
```

## Frozen Metric Family

The accepted constitutional metric family remains:

```text
support
directional_confidence A to B
directional_confidence B to A
dependence_delta A to B
dependence_delta B to A
lift
leverage
jaccard_similarity
PMI using log2(lift)
```

Undefined metric states remain explicit and unsmoothed.

## Frozen Population Rules

```text
canonical deck and snapshot identities are required
canonical_snapshot deduplication is deterministic and visible
resolved and ignored-by-policy records are excluded
private and unapproved observations are excluded
mainboard presence is the default
sideboard and auxiliary presence require explicit flags
card, tag, package, commander, and exact partner-pair endpoints are supported
exact partner pairs are order-normalized
tag and package membership consume already-built IDs
population manifests and spec hashes are deterministic
caller timestamps, provenance, caveats, sample, and coverage remain visible
```

## Backtracking Audit

No required correction or backtracking is identified for Phase 40A through
Phase 40J. All accepted outside-validation artifacts report no unresolved
blocking finding at track close.

Future additions such as anti-tautology rules, new endpoint categories,
projection into Unified Evidence, report/UI surfaces, batch population
assemblers, or new metric families require their own accepted contracts.

## Phase 41A Boundary

Phase 41A may define the Tournament Exposure Analyzer only as a contract.
It must follow Constitution V2's labeled independent-seat model and must not
silently introduce Swiss pairing, pods, standings, matchup strength, causal
claims, recommendations, or live provider behavior.

## Forbidden Phase 40K Work

Phase 40K must not modify production code, tests, fixtures, schema,
repositories, dependencies, workflows, active scope, or either constitution.
It must not implement Tournament Exposure or any other deferred program.

## Gate

Phase 41A may begin only after Phase 40K outside validation returns PASS or
PASS WITH REVIEW NOTES.
