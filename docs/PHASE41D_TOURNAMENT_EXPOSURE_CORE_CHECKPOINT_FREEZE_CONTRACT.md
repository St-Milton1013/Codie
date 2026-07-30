# Phase 41D - Tournament Exposure Core Checkpoint / Freeze Contract

Status: checkpoint and freeze only

## Validation Tuple

```text
phase_id: Phase41D
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42A
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42A is reserved for the Jin / Theory / Rules / Corrections
Cross-Specification Boundary and Decision Contract. It remains blocked until
Phase 41D outside validation returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 41D closes the core Tournament Exposure track after the accepted core
contract, implementation contract, and independent-seat implementation.

This packet freezes the accepted evidence path:

```text
already-built canonical population manifest
-> immutable Tournament Exposure target and assumptions
-> exact independent-seat calculation
-> estimate, compatible-scope comparison, and preparation brief packets
-> optional downstream consumption as labeled measured evidence
```

Phase 41D is documentation-only. It does not implement runtime behavior,
schema, repositories, providers, analytics, recommendations, Jin, Theory
Corpus, Rules Layer, Correction Ledger, simulator behavior, UI, LLM calls,
file writing, network behavior, or dependencies.

## Phase 41C Acceptance Evidence

```text
workflow run ID: 30500721283
validated SHA: 0ba15f789a8f6410b376205cf500830f9c45f6ce
artifact: codie-phase_ledger-validation-0ba15f789a8f6410b376205cf500830f9c45f6ce
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
codie/analytics/tournament_exposure.py
codie/analytics/__init__.py
tests/test_tournament_exposure.py
```

Future changes to these surfaces require a new accepted contract. Phase 41D
does not modify them.

## Frozen Model Rules

```text
independent_seat is the only supported core pairing-model identifier
the model is an approximation, not a Swiss or pairing-aware model
expected attendance and event-size class remain formula-neutral context
matching and available canonical population counts determine metagame share
intermediate arithmetic remains exact
serialized numeric values remain fixed 12-place ROUND_HALF_EVEN decimals
zero, unknown, unsupported, unavailable, and invalid remain distinct
sample, coverage, assumptions, provenance, and caveats remain visible
partner pairs remain exact and order-normalized
comparisons require compatible target, model, event, and population inputs
caller-supplied timestamps and version identifiers remain visible
```

## Frozen Evidence Boundary

Tournament Exposure remains measured evidence only.

It must not:

```text
become tournament outcome truth
become matchup-strength evidence
be treated as Swiss or pod-construction modeling
claim causal effects
generate recommendations
write persisted Decision Intelligence
invent canonical population, tag, package, archetype, or combo identity
read raw provider payloads or private deck text
silently include unapproved observations
```

Jin and other future consumers may use accepted Tournament Exposure packets
only as labeled evidence references. They may not strengthen the model,
remove its approximation warning, or present it as tournament truth.

## Explicit Deferrals

The following remain deferred and unimplemented:

```text
Swiss and pairing-aware tournament exposure
pod construction and repeat-opponent suppression
byes and standings
matchup strength and pilot skill
placement forecasting
correlated deck-choice modeling
live provider or source-population assembly
Evidence Fusion projection
Decision Intelligence output
report, CLI, UI, or chat surfaces
```

Each requires a separate accepted contract. The constitution explicitly
defers Swiss and pairing-aware modeling.

## Backtracking Audit

No required correction or backtracking is identified for Phase 41A through
Phase 41C. Their accepted contracts and artifact-backed validation preserve
the V2 Tournament Exposure requirement, the measured-evidence boundary, and
the independent-seat limitation.

## Phase 42A Boundary

Phase 42A may define only the cross-specification boundary and decision
contract for the Jin, Theory, Rules, and Corrections program described in
`docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md`.

It must coordinate the future program without collapsing authority,
measurement, context, correction, model-routing, or recommendation
boundaries. It must not implement Jin, the fixed regression corpus, the Rules
Layer, model routing, the Correction Ledger, Theory Corpus ingestion, UI,
LLM calls, persistence, or recommendation output.

## Forbidden Phase 41D Work

Phase 41D must not modify production code, tests, fixtures, schema,
repositories, dependencies, workflows, active scope, or either constitution.
It must not implement Swiss exposure modeling, Phase 42A behavior, or any
other deferred program.

## Gate

Phase 42A may begin only after Phase 41D outside validation returns PASS or
PASS WITH REVIEW NOTES.
