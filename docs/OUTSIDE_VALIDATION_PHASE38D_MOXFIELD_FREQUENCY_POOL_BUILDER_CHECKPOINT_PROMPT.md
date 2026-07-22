# Outside Validation Prompt - Phase 38D Moxfield Frequency Pool Builder Checkpoint

You are validating Phase 38D of Codie.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 39A.

## Required Review Files

Review:

```text
docs/PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38D_MOXFIELD_FREQUENCY_POOL_BUILDER_CHECKPOINT_PROMPT.md
docs/PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_PROMPT.md
docs/PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT.md
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
codie/frequency_pools/moxfield_builder.py
codie/frequency_pools/models.py
codie/frequency_pools/__init__.py
tests/test_moxfield_frequency_pool_builder.py
tests/fixtures/moxfield_frequency_pools/
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Checks

Confirm:

```text
Phase 38D is checkpoint-only
Phase 38C is recorded as PASS WITH REVIEW NOTES
Phase 38C artifact-backed aggregate result is CLEAN_PASS
Phase 38C has no blocking findings
Phase 38C informational finding requires no correction
Phase 38D declares phase_id, phase_part, gate_scope
Phase 38D declares next_phase_id, next_phase_part, next_gate_scope
active validation scope was not modified by the PR head
Phase 39A remains blocked until Phase 38D returns PASS or PASS WITH REVIEW NOTES
```

Confirm Phase 38D does not add:

```text
production implementation code
tests for new implementation code
fixtures for new implementation code
schema changes
repository changes
SQLite reads or writes
provider changes
live Moxfield calls
Scryfall lookup calls
frequency calculation changes
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

Confirm the accepted Phase 38C implementation still preserves:

```text
local fixture-first operation
manual text export parsing only
URL extraction without network fetching
deck presence frequency by default
total copy count visibly separate from presence frequency
default commander/sideboard/maybeboard/considering/token/basic-land exclusions
visible section override settings
partial failure visibility
duplicate deck input visibility
unresolved card visibility
user-local and not-tournament-evidence labels
private/raw metadata rejection
recommendation/action-language rejection
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
git diff --name-only HEAD~1..HEAD -- codie tests schemas codie/db codie/providers codie/analytics codie/recommendations codie/decision_intelligence codie/evidence_fusion scripts .github requirements.txt requirements-dev.txt docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

The second command should report no matches.

## Reject If

Reject Phase 38D if it:

```text
implements new runtime behavior
changes Moxfield builder behavior
changes frequency pool model behavior
adds new tests or fixtures for implementation code
changes schema, repositories, providers, workflows, validators, dependencies, or constitutions
modifies docs/CODIE_ACTIVE_VALIDATION_SCOPE.json in the PR head
marks Phase 38C as clean without preserving the informational review note
treats informational findings as required corrections
starts Phase 39A before Phase 38D acceptance
claims live Moxfield fetching, exports, CLI, UI, persistence, or recommendation behavior is complete
```

## Final Decision Format

Return:

```text
Phase 38D checkpoint: PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
Phase 39A: BLOCKED or UNBLOCKED
Required fixes:
Review notes:
```
