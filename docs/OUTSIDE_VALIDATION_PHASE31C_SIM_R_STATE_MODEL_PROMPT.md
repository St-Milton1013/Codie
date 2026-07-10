# Outside Validation Prompt - Phase 31C SIM-R State Model Contract

Validate Codie Phase 31C against `CODIE_V1_CONSTITUTION.md`, the accepted
Phase 31A SIM-R architecture contract, the accepted Phase 31B simulator freeze
contract, and the accepted Phase 13/14 simulator contracts.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
docs/CHECKPOINT_PHASE31C_SIM_R_STATE_MODEL_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31C_SIM_R_STATE_MODEL_PROMPT.md
docs/PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_CONTRACT.md
docs/CHECKPOINT_PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_REPORT.md
docs/PHASE31A_SIM_R_ARCHITECTURE_CONTRACT.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31C is contract-only and does not implement:

```text
production simulator code
state classes
actions
behavior modules
search
state hashing
resource ledger
trace v2
paired simulation
schema changes
repository changes
database reads or writes
Forge integration
LLM behavior generation
recommendation generation
UI work
live network calls
```

## Required Commands

Run from a clean checkout:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Required Static Checks

Confirm Phase 31C did not modify simulator runtime files:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/probability_engine codie/cli/simulation_review.py
```

Expected: no matches.

Confirm Phase 31C did not modify simulation schema or repositories:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/db/schema codie/db/repositories docs/SCHEMA_SPEC.md
```

Expected: no matches.

Confirm Phase 31C did not add dependencies:

```powershell
git diff --name-only HEAD~1..HEAD -- requirements.txt requirements-dev.txt pyproject.toml
```

Expected: no matches.

Confirm no production Forge or LLM SDK imports were added:

```powershell
rg -n "forge|openai|anthropic|google.generativeai|langchain" codie
```

Expected: no production integration matches.

## Validate State Contract Coverage

Confirm the contract defines:

```text
immutable state principle
required future state fields
zone model requirements
card instance requirements
commander state requirements
mana pool requirements
resource ledger relationship
target progress requirements
unsupported behavior requirements
state hash requirements
serialization requirements
trace v1 / SIM-R compatibility boundary
evidence-only boundary
```

## Reject If

Reject Phase 31C if:

```text
it implements simulator runtime behavior
it changes schema or repositories
it adds Forge runtime integration
it adds LLM executable behavior generation
it treats simulator output as tournament evidence
it allows simulator output to directly generate recommendations
it permits in-place mutation as the future state model
it allows unsupported behavior to be silently ignored
it allows historical Phase 13 traces to be silently reinterpreted as SIM-R states
it starts Phase 31D implementation before outside validation accepts Phase 31C
```

## Expected Result

```text
Phase 31C PASS or PASS WITH REVIEW NOTES means Phase 31D may begin contract-first.
Phase 31C PASS WITH REQUIRED FIXES means patch the state model contract before Phase 31D.
Phase 31C FAIL means do not proceed with SIM-R state model implementation planning.
```

