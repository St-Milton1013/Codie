# Phase 40G - Relationship Intelligence Metric Calculation Implementation Report

Status: implementation complete; outside validation pending

## Validation Tuple

```text
phase_id: Phase40G
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase40H
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Implemented Scope

Phase 40G implements the pure, deterministic Relationship Intelligence metric
calculator authorized by Phase 40F:

```text
codie/analytics/relationship_metrics.py
tests/test_relationship_metrics.py
codie/analytics/__init__.py exports
```

The implementation accepts already-counted immutable packets. It does not
construct populations, query repositories, persist measurements, call
providers, generate recommendations, run simulator behavior, call LLMs, write
files, or use network access.

## Public Interface

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

## Calculations

The implementation preserves the Phase 40A formulas exactly:

```text
support
directional_confidence A_to_B and B_to_A
dependence_delta A_to_B and B_to_A
lift
leverage
jaccard_similarity
pmi using log2
```

It adds no smoothing, alternate delta, combined score, display rounding, or
hidden weighting.

## Guardrails

```text
N and count invariants fail closed.
Boolean counts fail closed.
Non-finite numeric inputs and outputs fail closed.
Coverage counts and ratio must agree.
Zero available decks use coverage_ratio null and label unavailable.
Zero endpoint denominators create visible undefined metric values.
Zero joint count makes PMI undefined without changing zero support or leverage.
Low sample and low coverage remain visible labels and do not alter formulas.
Caller-provided calculated_at is preserved; the wall clock is not read.
Direct card-to-tag measured relationships fail closed without an accepted
anti-tautology rule.
```

## Deferred Work

Phase 40G does not build canonical population manifests or count endpoint
presence. That boundary remains for a contract-first Phase 40H population
resolution track.

## Changed Files

```text
codie/analytics/relationship_metrics.py
codie/analytics/__init__.py
tests/test_relationship_metrics.py
docs/PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40G_RELATIONSHIP_INTELLIGENCE_METRIC_CALCULATION_IMPLEMENTATION_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```
