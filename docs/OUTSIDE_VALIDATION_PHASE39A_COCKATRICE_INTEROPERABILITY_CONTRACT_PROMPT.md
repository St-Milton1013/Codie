# Outside Validation Prompt - Phase 39A Cockatrice Interoperability Contract

You are validating Phase 39A of Codie.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 39B.

## Required Review Files

Review:

```text
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
docs/CHECKPOINT_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Checks

Confirm:

```text
Phase 38D is recorded as PASS
Phase 38D artifact-backed aggregate result is CLEAN_PASS
Phase 38D has no unresolved findings
Phase 39A is contract-only
Phase 39A follows Priority 7 from the post-Phase 31 deferred plan
Phase 39A declares phase_id, phase_part, gate_scope
Phase 39A declares next_phase_id, next_phase_part, next_gate_scope
Phase 39B remains blocked until Phase 39A returns PASS or PASS WITH REVIEW NOTES
active validation scope was not modified by the PR head
```

Confirm Phase 39A defines future boundaries for:

```text
supported file formats
deck import/export fields
commander section handling
partner commander handling
sideboard and zone handling
card name preservation
already-supplied card identity refs
unsupported card reporting
XML safety
privacy boundaries
fixture-first tests
```

Confirm Phase 39A does not add:

```text
production Cockatrice parser code
production Cockatrice export code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
SQLite reads or writes
provider changes
live Cockatrice calls
network calls
card identity lookup calls
frequency calculation
analytics recalculation
exports
file writing
CLI behavior
UI behavior
LLM calls
simulator runtime
recommendation generation
deck health output
dependency changes
validator changes
workflow changes
active validation scope changes
constitution changes
```

## Required Commands

From a clean checkout, run:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Inspect the changed-file scope:

```text
git diff --name-only HEAD~1..HEAD
git diff --name-only HEAD~1..HEAD -- codie tests fixtures schemas codie/db codie/providers codie/analytics codie/recommendations codie/decision_intelligence codie/evidence_fusion scripts .github requirements.txt requirements-dev.txt docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

The second command should report no matches.

## Reject If

Reject Phase 39A if it:

```text
implements parser or exporter behavior
adds tests or fixtures for implementation code
changes production code
changes schema, repositories, providers, workflows, validators, dependencies, or constitutions
modifies docs/CODIE_ACTIVE_VALIDATION_SCOPE.json in the PR head
starts Phase 39B before Phase 39A acceptance
claims Cockatrice import/export behavior is complete
claims Cockatrice user deck files are tournament evidence by default
generates recommendation, cut, include, optimality, or deck health language
allows unsafe XML behavior without future rejection requirements
```

## Final Decision Format

Return:

```text
Phase 39A contract: PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
Phase 39B: BLOCKED or UNBLOCKED
Required fixes:
Review notes:
```
