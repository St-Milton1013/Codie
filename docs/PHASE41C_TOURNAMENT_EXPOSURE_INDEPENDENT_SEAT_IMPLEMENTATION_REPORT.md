# Phase 41C - Tournament Exposure Independent-Seat Implementation Report

Status: implementation complete; outside validation required

## Validation Tuple

```text
phase_id: Phase41C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Implemented Surface

```text
codie/analytics/tournament_exposure.py
tests/test_tournament_exposure.py
codie/analytics/__init__.py, exports only
```

The implementation provides the complete Phase 41B public interface for
immutable targets, population manifests, assumptions, estimates, compatible
scope comparisons, evidence-only preparation briefs, bundles, serializers,
builders, and validators.

## Implemented Behavior

```text
independent_seat is the only supported model
metagame share derives from matching / available integer counts
intermediate calculations use Fraction exact arithmetic
outputs use fixed 12-place ROUND_HALF_EVEN decimal strings
per-round encounter probability is calculated
event-wide encounter probability is calculated
expected encounter count is calculated
expected attendance remains visible and formula-neutral
partner pairs are order-normalized
scope, target, count, coverage, date, reference, and timestamp inputs are validated
sample and coverage confidence labels remain visible
local-versus-global and regional-versus-global comparisons require compatible inputs
preparation briefs remain deterministic evidence summaries
packet IDs use versioned canonical SHA-256 payloads
bundle references and duplicate IDs are validated
hand-constructed packet tampering is rejected
caller timestamps normalize to UTC
```

## Boundary

The implementation is pure and in-memory. It does not read observations,
repositories, databases, source tables, raw provider payloads, private deck
text, or live endpoints. It does not implement Swiss pairing, standings, pod
formation, repeat opponents, byes, matchup strength, placement forecasting,
recommendations, Decision Intelligence, Jin, simulation, UI, CLI, LLM calls,
network calls, or file writing.

## Phase 41B Acceptance Evidence

```text
workflow run ID: 30499567970
validated SHA: 9af972d6771177a754201ce90b7a3dd1d7bb3b09
artifact: codie-phase_ledger-validation-9af972d6771177a754201ce90b7a3dd1d7bb3b09
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

## Changed Files

```text
codie/analytics/tournament_exposure.py
codie/analytics/__init__.py
tests/test_tournament_exposure.py
docs/PHASE41C_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE41C_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE41C_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Gate

Phase 41D remains blocked until Phase 41C outside validation returns PASS or
PASS WITH REVIEW NOTES.
