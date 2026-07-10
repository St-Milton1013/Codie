# Outside Validation Prompt - Phase 31G SIM-R Resource Ledger Implementation Contract

Validate Codie Phase 31G against `CODIE_V1_CONSTITUTION.md`, the accepted
Phase 31F resource ledger contract, and the accepted Phase 31E state model
implementation.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
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

Confirm Phase 31G is implementation-contract-only and does not implement:

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

Confirm Phase 31G did not modify simulator runtime files:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/probability_engine codie/cli/simulation_review.py
```

Expected: no matches.

Confirm Phase 31G did not modify simulation schema or repositories:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/db/schema codie/db/repositories docs/SCHEMA_SPEC.md
```

Expected: no matches.

Confirm Phase 31G did not add dependencies:

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
future public ledger interface
future immutable ledger rules
future validation rules
future required tests
dependency boundaries
compatibility boundary
Phase 31H gate
```

## Reject If

Reject Phase 31G if:

```text
it implements resource ledger runtime behavior
it changes schema or repositories
it adds Forge runtime integration
it adds LLM executable behavior generation
it treats simulator output as tournament evidence
it allows simulator output to directly generate recommendations
it allows silent double-spending
it allows restricted mana to silently pay invalid costs
it omits failed or unsupported payment visibility requirements
it starts Phase 31H implementation before outside validation accepts Phase 31G
```

## Expected Result

```text
Phase 31G PASS or PASS WITH REVIEW NOTES means Phase 31H may begin contract-first.
Phase 31G PASS WITH REQUIRED FIXES means patch the implementation contract before Phase 31H.
Phase 31G FAIL means do not proceed with SIM-R resource ledger implementation.
```

