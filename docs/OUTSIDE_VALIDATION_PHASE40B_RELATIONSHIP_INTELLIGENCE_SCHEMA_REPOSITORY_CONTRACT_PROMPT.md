# Outside Validation - Phase 40B Relationship Intelligence Schema and Repository Contract

Validate Phase 40B from a clean checkout of the exact PR head.

## Required Files

```text
docs/PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT.md
docs/CHECKPOINT_PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40B_RELATIONSHIP_INTELLIGENCE_SCHEMA_REPOSITORY_CONTRACT_PROMPT.md
docs/PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT.md
docs/CHECKPOINT_PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE40A_RELATIONSHIP_INTELLIGENCE_CORE_CONTRACT_PROMPT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

The relationship proposal may be inspected as non-authoritative context:

```text
docs/design_inputs/v2_intelligence_program/CODIE_V2_RELATIONSHIP_INTELLIGENCE_PROPOSAL.md
```

## Required Confirmation

Confirm:

```text
Phase 40A acceptance evidence is recorded exactly.
The Phase40B and Phase40C validation tuples are explicit.
Phase 40B is contract-only.
The first persistence family is narrowly bounded.
AnalyticsRepository is the sole future repository owner.
Population specifications, manifests, members, measurements, and metrics are
versioned and replayable.
Manifest membership and historical measurements are immutable.
N, nA, nB, and nAB remain persisted.
Undefined metric values remain null with visible reasons.
Directional orientation remains visible.
No opaque synergy score is authorized.
Global population persistence excludes private user data.
Assertions, theory links, confounders, strata, and graph projections remain
deferred.
Repository methods do not calculate metrics or read provider payloads.
Phase 40C remains blocked until this validation passes.
```

Reject if Phase 40B adds or authorizes:

```text
schema or repository implementation
metric calculations
provider or raw payload reads
private user data in global populations
mutable historical manifests or measurements
recommendation ranking or combined relationship scores
Jin or Tournament Exposure behavior
Evidence Fusion or Decision Intelligence output
simulator behavior
UI
LLM calls
graph database support
file writing
live network behavior
dependency changes
workflow or validator changes
active-scope changes
constitution changes
```

## Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Inspect the changed-file set and confirm it contains only the seven declared
Phase 40B documentation files.

## Allowed Verdicts

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase 40C may begin only after PASS or PASS WITH REVIEW NOTES.

