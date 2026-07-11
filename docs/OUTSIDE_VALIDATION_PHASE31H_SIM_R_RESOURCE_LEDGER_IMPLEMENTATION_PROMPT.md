# Outside Validation Prompt - Phase 31H SIM-R Resource Ledger Implementation

Validate Codie Phase 31H against `CODIE_V1_CONSTITUTION.md`, the SIM-R
roadmap patch, and the accepted Phase 31F/31G resource ledger contracts.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_PROMPT.md
docs/PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT.md
docs/PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT.md
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
codie/probability_engine/sim_r_ledger.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_ledger.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31H implements only:

```text
pure SIM-R resource ledger value objects
resource ledger validation
deterministic serialization
focused tests
implementation report
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 31H implements:

```text
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
recommendations
UI behavior
live network calls
```

## Public Interface

Confirm the public interface exists:

```text
SIM_R_LEDGER_VERSION
SimulationLedgerBuildError
SimulationResourceLedgerEntry
SimulationPaymentRecord
SimulationResourceLedger
build_resource_ledger(...)
resource_ledger_to_dict(...)
validate_resource_ledger(...)
```

## Required Behavior Checks

Confirm:

```text
ledger serializes deterministically
ledger round-trips through dictionary form
ledger models are immutable
builders do not mutate input payloads
append-only ledger ordering is preserved
duplicate ledger_entry_id fails validation
duplicate payment_key fails validation
double-spent resource_key fails validation
explicit reusable resource metadata remains visible
negative resource_quantity fails validation
restricted mana metadata remains visible
failed payment remains visible
unsupported payment remains visible
pre_state_id and post_state_id remain visible
action_id, cost_key, and payment_key remain visible
resource ledger output remains simulator evidence only
resource ledger output does not become tournament evidence
resource ledger output does not generate recommendations
```

## Required Commands

From a clean checkout, run:

```powershell
python scripts/check_schema.py
python -m unittest tests.test_probability_engine_sim_r_ledger -v
python -m unittest discover -s tests
git diff --check
```

Use the bundled Python runtime if system Python is unavailable.

## Required Static Scans

Run:

```powershell
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|sqlite3|requests|httpx" codie\probability_engine\sim_r_ledger.py tests\test_probability_engine_sim_r_ledger.py
rg -n "forge|openai|anthropic|google\.generativeai|langchain" codie\probability_engine\sim_r_ledger.py tests\test_probability_engine_sim_r_ledger.py
rg -n "should play|must include|correct card|breaks the format|secretly optimal|strict upgrade|auto-include|recommended cut|recommended include" codie\probability_engine\sim_r_ledger.py tests\test_probability_engine_sim_r_ledger.py
```

Expected:

```text
no schema/repository/dependency drift
no forbidden production imports
no Forge or LLM SDK imports
no recommendation language
```

## Gate

Phase 31I must not begin until Phase 31H returns PASS or PASS WITH REVIEW
NOTES.

