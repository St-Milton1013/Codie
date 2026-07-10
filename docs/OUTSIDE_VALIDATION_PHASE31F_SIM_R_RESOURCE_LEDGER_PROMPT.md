# Outside Validation Prompt - Phase 31F SIM-R Resource Ledger Contract

Validate Codie Phase 31F against `CODIE_V1_CONSTITUTION.md`, the accepted
SIM-R architecture/freeze/state contracts, and the accepted Phase 31E state
model implementation.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT.md
docs/CHECKPOINT_PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31F_SIM_R_RESOURCE_LEDGER_PROMPT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT.md
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
codie/probability_engine/sim_r_state.py
tests/test_probability_engine_sim_r_state.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31F is contract-only and does not implement:

```text
production simulator code
resource ledger classes
state transitions
actions
behavior modules
search
state hashing
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

Confirm Phase 31F did not modify simulator runtime files:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/probability_engine codie/cli/simulation_review.py
```

Expected: no matches.

Confirm Phase 31F did not modify simulation schema or repositories:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/db/schema codie/db/repositories docs/SCHEMA_SPEC.md
```

Expected: no matches.

Confirm Phase 31F did not add dependencies:

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
ledger principle
future ledger entry fields
resource types
cost/payment relationship
double-spend rule
state relationship
restricted mana rule
unsupported resource rule
serialization requirements
evidence-only boundary
future implementation shape
Phase 31G gate
```

## Reject If

Reject Phase 31F if:

```text
it implements resource ledger runtime behavior
it changes schema or repositories
it adds Forge runtime integration
it adds LLM executable behavior generation
it treats simulator output as tournament evidence
it allows simulator output to directly generate recommendations
it allows silent double-spending
it allows restricted mana to silently pay invalid costs
it allows unsupported resource behavior to be silently ignored
it starts Phase 31G implementation before outside validation accepts Phase 31F
```

## Expected Result

```text
Phase 31F PASS or PASS WITH REVIEW NOTES means Phase 31G may begin contract-first.
Phase 31F PASS WITH REQUIRED FIXES means patch the resource ledger contract before Phase 31G.
Phase 31F FAIL means do not proceed with SIM-R resource ledger implementation planning.
```

