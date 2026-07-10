# Outside Validation Prompt - Phase 31E SIM-R State Model Implementation

Validate Codie Phase 31E against `CODIE_V1_CONSTITUTION.md`, the accepted
Phase 31C SIM-R state model contract, and the accepted Phase 31D implementation
contract.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_PROMPT.md
docs/PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT.md
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
codie/probability_engine/sim_r_state.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_state.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31E implements only isolated pure state models and does not add:

```text
simulator actions
behavior modules
search
state hashing
resource ledger execution
trace v2 execution
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
python -m unittest tests.test_probability_engine_sim_r_state -v
python -m unittest discover -s tests
git diff --check
```

## Required Static Checks

Confirm Phase 31E only changes allowed production files:

```powershell
git diff --name-only HEAD~1..HEAD -- codie
```

Expected production matches:

```text
codie/probability_engine/__init__.py
codie/probability_engine/sim_r_state.py
```

Confirm Phase 31E did not modify schema or repositories:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/db/schema codie/db/repositories docs/SCHEMA_SPEC.md
```

Expected: no matches.

Confirm Phase 31E did not add dependencies:

```powershell
git diff --name-only HEAD~1..HEAD -- requirements.txt requirements-dev.txt pyproject.toml
```

Expected: no matches.

Confirm production code has no forbidden imports:

```powershell
rg -n "codie.db|repositories|codie.providers|codie.analytics|codie.recommendations|sqlite3|requests|httpx|openai|anthropic|google.generativeai|langchain|forge" codie/probability_engine/sim_r_state.py
```

Expected: no matches.

## Required Behavior Checks

Confirm tests cover:

```text
deterministic serialization
dictionary round-trip
no action/search helpers
input builder immutability
duplicate card_instance_id rejection
negative mana rejection
restricted mana visibility
partner order normalization
zone ordering preservation
unsupported behavior visibility
target progress visibility
metadata separation
trace v1 rejection
forbidden import scan
```

## Reject If

Reject Phase 31E if:

```text
it changes existing simulator search/action behavior
it changes schema or repositories
it adds Forge runtime integration
it adds LLM executable behavior generation
it treats simulator output as tournament evidence
it allows simulator output to directly generate recommendations
it permits mutable state objects
it allows duplicate card instances across zones
it allows unsupported behavior to be silently ignored
it accepts Phase 13 trace v1 as SIM-R state
```

## Expected Result

```text
Phase 31E PASS or PASS WITH REVIEW NOTES means Phase 31F may begin contract-first.
Phase 31E PASS WITH REQUIRED FIXES means patch implementation before Phase 31F.
Phase 31E FAIL means do not proceed with later SIM-R implementation.
```

