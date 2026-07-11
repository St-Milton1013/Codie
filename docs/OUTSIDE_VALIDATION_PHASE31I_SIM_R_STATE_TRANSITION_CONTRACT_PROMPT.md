# Outside Validation Prompt - Phase 31I SIM-R State Transition Contract

Validate Codie Phase 31I against `CODIE_V1_CONSTITUTION.md`, the SIM-R
roadmap patch, and the accepted Phase 31E/31H SIM-R model implementations.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT.md
docs/CHECKPOINT_PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT_PROMPT.md
docs/PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT.md
docs/PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31I is contract-only and creates no implementation beyond docs
and roadmap/status/handoff updates.

Reject if Phase 31I implements:

```text
state transition code
action execution
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
recommendations
UI behavior
live network calls
```

## Contract Checks

Confirm the contract defines:

```text
transition principle
future transition model files
future public interface
required future transition rules
required future tests
dependency boundaries
compatibility boundaries
evidence-only boundary
Phase 31J gate
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

Phase 31J must not begin until Phase 31I returns PASS or PASS WITH REVIEW
NOTES.

