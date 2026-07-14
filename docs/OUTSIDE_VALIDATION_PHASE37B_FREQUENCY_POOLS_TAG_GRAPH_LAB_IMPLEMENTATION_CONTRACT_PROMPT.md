# Outside Validation Prompt - Phase 37B Frequency Pools / Tag Graph Lab Implementation Contract

Validate Codie Phase 37B against:

```text
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
```

## Required Review Files

Review:

```text
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
docs/CHECKPOINT_PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Validation Tuple

Confirm the Phase 37B contract explicitly declares:

```text
phase_id: Phase37B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase37C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Reject if the Phase 37B or next-phase validation tuple is missing, ambiguous,
or inconsistent across the contract/checkpoint/status documents.

Confirm `docs/CODIE_ACTIVE_VALIDATION_SCOPE.json` was not modified by this PR.

## Confirm Implementation-Contract-Only Scope

Confirm Phase 37B adds only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 37B adds:

```text
production frequency pool code
production tag graph code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
dependency changes
file-writing behavior
CLI behavior
UI behavior
live network behavior
simulator execution
analytics behavior
recommendation behavior
LLM behavior
validator changes
workflow changes
constitution changes
```

## Confirm Future Implementation Surface

Confirm the contract limits future Phase 37C implementation to:

```text
codie/frequency_pools/__init__.py
codie/frequency_pools/models.py
tests/test_frequency_pool_models.py
tests/fixtures/frequency_pools/frequency_pool_commander.json
tests/fixtures/frequency_pools/frequency_pool_partner_pair.json
tests/fixtures/frequency_pools/frequency_pool_user_local.json
tests/fixtures/frequency_pools/frequency_pool_invalid.json
```

Reject if the contract authorizes schema changes, repository reads/writes,
provider reads, live network calls, analytics recalculation, recommendation
output, simulator execution, UI, LLM calls, CLI behavior, or file writing.

## Confirm Contract Completeness

Confirm the Phase 37B contract includes all of these review points:

```text
explicit Phase 37B validation tuple
explicit next-phase validation tuple
accepted Phase 37A dependency evidence
authorized future implementation files
future public interface
future packet responsibilities
allowed pool types
identity and provenance rules
metric serialization rules
tag row rules
coverage and caveat rules
privacy boundary
evidence boundary enforcement
fixture inventory
fixture coverage requirements
required tests
future package dependencies and input limits
deferred later work
outside validation packet
```

Reject only if a required review point is missing or contradicts
`CODIE_V1_CONSTITUTION.md`.

## Confirm Frequency Pool Boundaries

Confirm future Frequency Pool packet models must:

```text
use canonical card identities
preserve scryfall_id when supplied
preserve oracle_id grouping when supplied
preserve tag provenance
preserve source refs by ID only
keep matching_deck_count visible
keep available_deck_count visible
keep coverage_ratio visible
keep low_sample_threshold visible or explicitly unknown
keep low_coverage_threshold visible or explicitly unknown
keep caveats visible or explicitly unknown
label low sample caveats
label low coverage caveats
label user-local pool scopes
keep user-local pools out of commander averages
keep user-local pools out of tournament evidence
```

## Confirm Privacy Requirements

Confirm the future implementation must preserve the accepted Phase 36C
blocked-key policy and reject private import text, private notes, primer body
text, and raw provider payload metadata recursively. This prompt intentionally
does not redefine the private/raw key vocabulary.

## Confirm Evidence And Recommendation Boundaries

Confirm future Frequency Pool packets:

```text
do not rank cards
do not score cards for inclusion
do not recommend cards
do not recommend cuts
do not infer pilot intent
do not generate play/cut/include language
do not claim a card is optimal
do not treat simulator output as tournament evidence
do not treat user-local snapshots as tournament evidence
do not mutate evidence packets
do not mutate source records
```

## Required Commands

Run from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests
```

Run static scans:

```powershell
git diff --name-only HEAD~1..HEAD -- codie tests scripts ui codie\db codie\providers codie\analytics codie\recommendations codie\probability_engine codie\cards docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml .github
rg -n "production frequency pool code|production tag graph code|schema changes|repository changes|file writing|analytics calculation|frequency pool calculation|Tag Graph Lab metrics|simulator execution|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md docs\CHECKPOINT_PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT_REPORT.md
git diff --name-only HEAD~1..HEAD -- docs\CODIE_V1_CONSTITUTION.md docs\CODIE_ACTIVE_VALIDATION_SCOPE.json .github codie\validation scripts\codie_validation_gate.py scripts\codie_repair_controller.py
```

Expected:

```text
No production/test/schema/repository/dependency drift.
No constitution, active-scope, validator, or workflow changes.
Forbidden strings appear only in explicit forbidden-scope lists.
All tests pass.
```

## Return Verdict

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```
