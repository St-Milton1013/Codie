# Outside Validation Prompt - Phase 31O SIM-R Behavior Transition Wiring Contract

Validate Codie Phase 31O against `CODIE_V1_CONSTITUTION.md`, the SIM-R roadmap
patch, the accepted Phase 31N behavior module implementation, and the accepted
Phase 31E/31H/31K SIM-R model implementations.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT.md
docs/CHECKPOINT_PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT_PROMPT.md
docs/PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT.md
docs/PHASE31L_SIM_R_BEHAVIOR_MODULE_CONTRACT.md
codie/probability_engine/sim_r_behavior.py
codie/probability_engine/sim_r_transition.py
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
tests/test_probability_engine_sim_r_behavior.py
tests/test_probability_engine_sim_r_transition.py
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31O is contract-only and creates no implementation beyond docs
and roadmap/status/handoff updates.

Reject if Phase 31O implements:

```text
behavior-transition wiring code
behavior proposal application
transition result creation
card behavior execution
action execution
state mutation logic
resource ledger creation or mutation
search
state hashing
trace v2 runtime
paired simulation
schema changes
repository changes
database reads or writes
Forge integration
LLM behavior generation
recommendations
UI behavior
live network calls
```

## Contract Checks

Confirm the contract defines:

```text
accepted Phase 31N dependency
future wiring principle
future wiring files
future public interface
future model responsibilities
required future rules
future implementation exclusions
dependency boundaries
required future tests
compatibility boundary
evidence-only boundary
Phase 31P gate
```

Confirm the future implementation remains limited to:

```text
codie/probability_engine/sim_r_wiring.py
tests/test_probability_engine_sim_r_wiring.py
codie/probability_engine/__init__.py exports only, if needed
```

## Required Commands

From a clean checkout, run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

Use the bundled Python runtime if system Python is unavailable.

## Required Static Scans

Run:

```powershell
git diff --name-only HEAD~1..HEAD -- codie\probability_engine tests
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "forge|openai|anthropic|google\.generativeai|langchain" codie
```

Expected:

```text
no production simulator implementation changes
no schema/repository/dependency drift
no Forge or LLM SDK imports
```

## Gate

Phase 31P must not begin until Phase 31O returns PASS or PASS WITH REVIEW
NOTES.
