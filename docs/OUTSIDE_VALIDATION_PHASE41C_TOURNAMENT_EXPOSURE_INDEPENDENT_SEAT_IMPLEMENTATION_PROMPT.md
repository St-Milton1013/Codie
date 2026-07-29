# Outside Validation - Phase 41C Tournament Exposure Independent-Seat Implementation

Validate Phase 41C from the exact merged `main` SHA.

## Validation Tuple

```text
phase_id: Phase41C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Review Files

```text
docs/PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT.md
docs/PHASE41C_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE41C_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_REPORT.md
codie/analytics/tournament_exposure.py
codie/analytics/__init__.py
tests/test_tournament_exposure.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
docs/CODIE_V2_CONSTITUTION.md
```

## Confirm

Confirm the implementation:

```text
matches the Phase 41B public interface and file boundary
uses immutable packets and deterministic serialization
derives shares and formulas from exact integer-ratio arithmetic
uses the declared fixed 12-place ROUND_HALF_EVEN output policy
supports all constitutional target and population scopes
normalizes exact partner pairs
preserves population, sample, coverage, assumptions, provenance, and caveats
keeps expected attendance formula-neutral
rejects unsupported pairing models
builds only compatible local and regional comparisons
keeps preparation briefs evidence-only
derives and validates canonical SHA-256 packet identities
rejects malformed and hand-tampered packets
has no undeclared storage, provider, recommendation, model, UI, or network coupling
keeps Phase 41D blocked
does not modify active scope or either constitution in the feature packet
```

## Reject If

Reject if it introduces float-dependent intermediate math, hidden rounding,
Swiss or pairing-aware behavior, observation ingestion, database/provider
access, personal-deck aggregation, recommendation language, Jin, simulator,
UI, CLI, LLM, network, file-writing, dependency, validator, workflow,
active-scope, or constitution changes.

## Commands

```text
python -m unittest tests.test_tournament_exposure -v
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Return the exact SHA, run ID, artifact, three validator results and findings,
aggregate, severity totals, skips, unresolved findings, errors, and final
governance verdict. Only PASS or PASS WITH REVIEW NOTES unblocks Phase 41D.
