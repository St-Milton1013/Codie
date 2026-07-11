# Outside Validation Prompt - Phase 31N SIM-R Behavior Module Implementation

Validate Codie Phase 31N against `CODIE_V1_CONSTITUTION.md`, the SIM-R roadmap
patch, the accepted Phase 31M implementation contract, and the accepted Phase
31E/31H/31K SIM-R model implementations.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_PROMPT.md
docs/PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE31L_SIM_R_BEHAVIOR_MODULE_CONTRACT.md
codie/probability_engine/sim_r_behavior.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_behavior.py
codie/probability_engine/sim_r_transition.py
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
tests/test_probability_engine_sim_r_transition.py
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31N implements only pure in-memory behavior model value objects
and validators.

Reject if Phase 31N implements:

```text
card behavior execution
action execution
state mutation logic
resource ledger mutation
transition result creation
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

## Interface Checks

Confirm the public interface includes:

```text
SIM_R_BEHAVIOR_VERSION
SUPPORTED_BEHAVIOR_CATEGORIES
UNSUPPORTED_BEHAVIOR_CATEGORY
SimulationBehaviorBuildError
SimulationBehaviorProfile
SimulationBehaviorRequirement
SimulationBehaviorProposal
SimulationUnsupportedBehaviorNote
build_behavior_profile(...)
build_behavior_proposal(...)
behavior_profile_to_dict(...)
behavior_proposal_to_dict(...)
validate_behavior_profile(...)
validate_behavior_proposal(...)
```

## Behavior Checks

Confirm tests prove:

```text
behavior profile serializes deterministically
behavior proposal serializes deterministically
behavior profile round-trips through dictionary form
behavior proposal round-trips through dictionary form
models are immutable
input structures are not mutated by builders
behavior_profile_id remains visible
behavior_key remains visible
behavior_category remains visible
behavior_version remains visible
supported_action_types remain visible
required resource intents remain visible
zone-change intents remain visible
target requirements remain visible
timing restrictions remain visible
unsupported behavior notes remain visible
confidence/status fields remain visible
source card identity remains visible when available
unknown behavior category fails unless explicitly Unsupported
executable code payloads are rejected
callable objects are rejected
LLM-authored executable behavior is rejected
negative confidence fails
confidence above 1.0 fails
no state mutation helper is added
no action execution helper is added
no ledger-writing helper is added
no transition-building helper is added
no search implementation is added
no recommendation language appears
```

## Required Commands

From a clean checkout, run:

```powershell
python -m unittest tests.test_probability_engine_sim_r_behavior -v
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
rg -n "def apply_|def execute|def search|def write_ledger|def build_transition|recommended" codie\probability_engine\sim_r_behavior.py
```

Expected:

```text
only approved behavior model implementation files changed under codie/probability_engine/tests
no schema/repository/dependency drift
no Forge or LLM SDK imports
no runtime execution helper or recommendation language matches
```

## Gate

Phase 31O must not begin until Phase 31N returns PASS or PASS WITH REVIEW
NOTES.
