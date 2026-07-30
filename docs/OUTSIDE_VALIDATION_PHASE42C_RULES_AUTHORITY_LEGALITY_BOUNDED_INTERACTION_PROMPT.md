# Outside Validation - Phase 42C Rules Authority, Legality, and Bounded Interaction

Validate the exact PR head from a clean checkout.

## Review Files

```text
docs/PHASE42C_RULES_AUTHORITY_LEGALITY_BOUNDED_INTERACTION_CONTRACT.md
docs/CHECKPOINT_PHASE42C_RULES_AUTHORITY_LEGALITY_BOUNDED_INTERACTION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE42C_RULES_AUTHORITY_LEGALITY_BOUNDED_INTERACTION_PROMPT.md
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_CONTRACT.md
docs/CODIE_V2_CONSTITUTION.md
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md
docs/design_inputs/v2_intelligence_program/README.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_RULES_LAYER_JUDGE_TRAINING_PROPOSAL.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Confirm Phase 42C:

```text
is contract-only
records exact artifact-backed Phase 42B acceptance
defines a domain-aware authority lattice rather than popularity scoring
keeps Oracle, Comprehensive Rules, official policy, rulings, Scryfall cache,
community references, user corrections, and model output in their proper scopes
requires versioned compatible authority packages and exact citations
uses the authority effective on the requested date
keeps legality LEGAL, ILLEGAL, and UNKNOWN distinct
uses categorical rules support rather than confidence percentages
preserves official conflicts and stale sources as visible blocking states
defines bounded interaction facts, issue spotting, and missing-fact behavior
limits continuous-effect support to curated deterministic capabilities
does not claim a full rules engine or arbitrary game-state execution
keeps community tools and engines non-authoritative
keeps Rules separate from strategy and recommendations
prevents Jin, Theory, corrections, models, simulator evidence, or popularity
from overriding authority
requires only SUPPORTED_VALID traces to enter clean simulator evidence later
preserves the Paradise Mantle, Springleaf Drum, copy-object, and target-turn
regression requirements
does not acquire or parse rules, implement snapshots, legality, interactions,
continuous effects, simulator validation, Jin, lessons, schema, repositories,
providers, models, prompts, UI, dependencies, workflows, active scope, or
constitution changes
records an explicit Phase42C to Phase42D validation tuple
keeps Phase 42D contract-only and blocked until Phase 42C acceptance
```

Run:

```text
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

Allowed verdicts:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Phase 42D remains blocked until PASS or PASS WITH REVIEW NOTES.
