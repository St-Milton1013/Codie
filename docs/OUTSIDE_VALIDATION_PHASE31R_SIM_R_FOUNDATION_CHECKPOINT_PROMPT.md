# Outside Validation Prompt - Phase 31R SIM-R Foundation Checkpoint / Freeze

Validate Codie Phase 31R against `CODIE_V1_CONSTITUTION.md`, the SIM-R roadmap
patch, and the accepted Phase 31A-31Q chain.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31R_SIM_R_FOUNDATION_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE31R_SIM_R_FOUNDATION_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31R_SIM_R_FOUNDATION_CHECKPOINT_PROMPT.md
docs/PHASE31Q_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31Q_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31Q_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_PROMPT.md
docs/PHASE31P_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_CONTRACT.md
docs/PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT.md
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
codie/probability_engine/sim_r_transition.py
codie/probability_engine/sim_r_behavior.py
codie/probability_engine/sim_r_wiring.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
tests/test_probability_engine_sim_r_transition.py
tests/test_probability_engine_sim_r_behavior.py
tests/test_probability_engine_sim_r_wiring.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
```

## Required Checks

Confirm:

```text
Phase 31Q is recorded as PASS WITH REVIEW NOTES.
Phase 31R is checkpoint/freeze only.
Phase 31R adds no production simulator runtime code.
Phase 31R adds no schema, repositories, dependencies, providers, UI, LLM calls, Forge integration, live network calls, or recommendations.
SIM-R state/ledger/transition/behavior/wiring modules remain pure model layers.
SIM-R foundation modules do not execute behavior.
SIM-R foundation modules do not mutate SimulationState.
SIM-R foundation modules do not create resource ledgers at runtime.
SIM-R foundation modules do not create transition results from behavior proposals.
SIM-R foundation modules do not call Phase 13 simulator search.
SIM-R foundation modules do not read Scryfall/provider/SQLite data.
SIM-R foundation output remains simulator evidence only, not tournament evidence.
Post-31 deferred implementation backlog remains blocked until Phase 31R is accepted.
```

## Commands To Run From Clean Checkout

```powershell
python -m unittest tests.test_probability_engine_sim_r_state tests.test_probability_engine_sim_r_ledger tests.test_probability_engine_sim_r_transition tests.test_probability_engine_sim_r_behavior tests.test_probability_engine_sim_r_wiring -v
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Static Scans

```powershell
git diff --name-only HEAD~1..HEAD -- codie\probability_engine tests
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "forge|openai|anthropic|google\.generativeai|langchain" codie
rg -n "codie\.db|repositories|sqlite3|requests|httpx|providers|ingestion|analytics|recommendations|decision|evidence" codie\probability_engine\sim_r_state.py codie\probability_engine\sim_r_ledger.py codie\probability_engine\sim_r_transition.py codie\probability_engine\sim_r_behavior.py codie\probability_engine\sim_r_wiring.py
```

Expected:

```text
No production/test runtime diff for Phase 31R.
No schema/repository/dependency drift.
No Forge or LLM SDK imports.
No forbidden cross-layer imports in SIM-R foundation modules.
```

## Reject If

```text
Phase 31R modifies simulator runtime behavior.
Phase 31R starts post-31 deferred implementation backlog work.
Phase 31R adds schema, repositories, dependencies, providers, UI, live network calls, Forge, LLM SDKs, or recommendations.
Phase 31R treats simulator output as tournament evidence.
Phase 31R allows deferred implementation work before outside validation accepts the checkpoint.
```

## Gate

```text
Post-31 deferred implementation work remains blocked until Phase 31R outside validation returns PASS or PASS WITH REVIEW NOTES.
```
