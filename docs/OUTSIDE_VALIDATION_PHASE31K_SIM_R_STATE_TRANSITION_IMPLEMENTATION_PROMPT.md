# Outside Validation Prompt - Phase 31K SIM-R State Transition Implementation

Validate Codie Phase 31K against `CODIE_V1_CONSTITUTION.md`, the SIM-R
roadmap patch, the accepted Phase 31J implementation contract, and the accepted
Phase 31E/31H SIM-R model implementations.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31K_SIM_R_STATE_TRANSITION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31K_SIM_R_STATE_TRANSITION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31K_SIM_R_STATE_TRANSITION_IMPLEMENTATION_PROMPT.md
docs/PHASE31J_SIM_R_STATE_TRANSITION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31J_SIM_R_STATE_TRANSITION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT.md
docs/PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
codie/probability_engine/sim_r_transition.py
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_transition.py
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31K implements only:

```text
pure SIM-R transition value objects
transition result validation
deterministic serialization
focused tests
implementation report
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 31K implements:

```text
state mutation logic
action execution
behavior module execution
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

## Public Interface

Confirm the public interface exists:

```text
SIM_R_TRANSITION_VERSION
SimulationTransitionBuildError
SimulationActionIntent
SimulationBehaviorResult
SimulationTransitionTraceEvent
SimulationTransitionResult
build_transition_result(...)
transition_result_to_dict(...)
validate_transition_result(...)
```

## Required Behavior Checks

Confirm:

```text
transition result serializes deterministically
transition result round-trips through dictionary form
transition models are immutable
builders do not mutate input payloads
transition_id remains visible
transition_version remains visible
simulation_id remains visible
pre_state_id remains visible
post_state_id remains visible
action_id remains visible
action_type remains visible
behavior_key remains visible
transition_status remains visible
resource ledger IDs remain visible
trace event IDs remain visible
unsupported behavior remains visible
failed transition reason remains visible
no_op transitions are explicit
resource-consuming successful transitions require ledger IDs
negative turn metadata fails validation
negative priority sequence metadata fails validation
trace event reference mismatches fail validation
transition packets remain simulator evidence only
transition packets do not become tournament evidence
transition packets do not generate recommendations
```

## Required Commands

From a clean checkout, run:

```powershell
python scripts/check_schema.py
python -m unittest tests.test_probability_engine_sim_r_transition -v
python -m unittest discover -s tests
git diff --check
```

Use the bundled Python runtime if system Python is unavailable.

## Required Static Scans

Run:

```powershell
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|sqlite3|requests|httpx" codie\probability_engine\sim_r_transition.py tests\test_probability_engine_sim_r_transition.py
rg -n "forge|openai|anthropic|google\.generativeai|langchain" codie\probability_engine\sim_r_transition.py tests\test_probability_engine_sim_r_transition.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|strict upgrade|auto-include|recommended cut|recommended include" codie\probability_engine\sim_r_transition.py tests\test_probability_engine_sim_r_transition.py
```

Expected:

```text
no schema/repository/dependency drift
no forbidden production imports
no Forge or LLM SDK imports
no recommendation language
```

## Gate

Phase 31L must not begin until Phase 31K returns PASS or PASS WITH REVIEW
NOTES.

