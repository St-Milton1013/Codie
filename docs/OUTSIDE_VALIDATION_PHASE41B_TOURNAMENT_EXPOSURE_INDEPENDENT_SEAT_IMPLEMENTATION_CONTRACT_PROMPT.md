# Outside Validation - Phase 41B Tournament Exposure Independent-Seat Implementation Contract

Validate Phase 41B from the exact merged `main` SHA.

## Required Validation Tuple

```text
phase_id: Phase41B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase41C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

## Review Files

```text
docs/PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE41B_TOURNAMENT_EXPOSURE_INDEPENDENT_SEAT_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE41A_TOURNAMENT_EXPOSURE_ANALYZER_CORE_CONTRACT_REPORT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Confirmation

Confirm that:

```text
Phase 41A acceptance evidence is accurate
Phase 41B is implementation-contract-only
Phase 41C is limited to one analytics module, one focused test file, and exports
public packets are immutable and deterministically serializable
population manifests are already-built inputs rather than observation readers
target, scope, count, date, coverage, and reference validation is explicit
independent_seat is the only supported model
exact rational intermediate arithmetic is required
output decimals use the declared 12-place ROUND_HALF_EVEN policy
packet identities use canonical versioned SHA-256 payloads
caller timestamps require a timezone and normalize to UTC
expected attendance remains visible and formula-neutral
all three constitutional formulas are exact
sample and coverage labels remain visible
comparison compatibility rules preserve both evidence sources
preparation briefs remain evidence-only
Swiss and pairing-aware behavior remains deferred
Phase 41C remains blocked
the feature packet does not modify active validation scope
neither constitution is modified
```

## Reject If

Reject the packet if it:

```text
implements production code, tests, fixtures, schema, repositories, or providers
authorizes observation ingestion or raw payload reads
uses floating point for equality or intermediate calculations
hides rounding, precision, formula, population, sample, coverage, or assumptions
silently accepts unsupported pairing models
adds Swiss, standings, pods, repeat opponents, byes, matchup, placement, or win-rate logic
allows personal or private decks into aggregate populations
creates ontology, package, combo, or archetype truth
generates deck changes or recommendations
adds simulator, Jin, UI, CLI, LLM, live-network, or file-writing behavior
changes dependencies, validators, workflows, active scope, or either constitution
starts Phase 41C implementation before Phase 41B is accepted
```

## Commands

Run from a clean checkout at the exact target SHA:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Inspect the merged diff and confirm no undeclared production, test, fixture,
schema, repository, dependency, workflow, active-scope, or constitution file
changed.

## Return

Return:

```text
validated SHA
workflow run ID
artifact name
deterministic result and findings
architecture result and findings
adversarial result and findings
aggregate result
severity totals
skipped validators
unresolved findings
errors
final governance verdict
```

Allowed final verdicts:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES unblocks Phase 41C.
