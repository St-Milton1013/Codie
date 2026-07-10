# Outside Validation Prompt - Phase 31D SIM-R State Model Implementation Contract

Validate Codie Phase 31D against `CODIE_V1_CONSTITUTION.md`, the accepted
Phase 31A SIM-R architecture contract, the accepted Phase 31B simulator freeze
contract, and the accepted Phase 31C state model contract.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
docs/CHECKPOINT_PHASE31C_SIM_R_STATE_MODEL_CONTRACT_REPORT.md
docs/PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_CONTRACT.md
docs/PHASE31A_SIM_R_ARCHITECTURE_CONTRACT.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31D is implementation-contract-only and does not implement:

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

Confirm Phase 31D did not modify simulator runtime files:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/probability_engine codie/cli/simulation_review.py
```

Expected: no matches.

Confirm Phase 31D did not modify simulation schema or repositories:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/db/schema codie/db/repositories docs/SCHEMA_SPEC.md
```

Expected: no matches.

Confirm Phase 31D did not add dependencies:

```powershell
git diff --name-only HEAD~1..HEAD -- requirements.txt requirements-dev.txt pyproject.toml
```

Expected: no matches.

Confirm no production Forge or LLM SDK imports were added:

```powershell
rg -n "forge|openai|anthropic|google.generativeai|langchain" codie
```

Expected: no production integration matches.

## Validate Contract Coverage

Confirm the contract defines:

```text
allowed future implementation files
future public model interface
future immutable model rules
future validation rules
future required tests
dependency boundaries
compatibility boundary
Phase 31E gate
```

## Reject If

Reject Phase 31D if:

```text
it implements simulator runtime behavior
it changes schema or repositories
it adds Forge runtime integration
it adds LLM executable behavior generation
it treats simulator output as tournament evidence
it allows simulator output to directly generate recommendations
it allows future mutable state models
it omits duplicate card-instance validation requirements
it omits unsupported behavior visibility requirements
it starts Phase 31E implementation before outside validation accepts Phase 31D
```

## Expected Result

```text
Phase 31D PASS or PASS WITH REVIEW NOTES means Phase 31E may begin contract-first.
Phase 31D PASS WITH REQUIRED FIXES means patch the implementation contract before Phase 31E.
Phase 31D FAIL means do not proceed with SIM-R state model implementation.
```

