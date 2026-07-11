# Outside Validation Prompt - Phase 31Q SIM-R Behavior Transition Wiring Implementation

Validate Codie Phase 31Q against `CODIE_V1_CONSTITUTION.md`, the SIM-R roadmap
patch, and the accepted Phase 31O/31P contracts.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31Q_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31Q_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31Q_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_PROMPT.md
docs/PHASE31P_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31P_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT.md
docs/CHECKPOINT_PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT_REPORT.md
codie/probability_engine/sim_r_wiring.py
codie/probability_engine/sim_r_behavior.py
codie/probability_engine/sim_r_transition.py
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_wiring.py
tests/test_probability_engine_sim_r_behavior.py
tests/test_probability_engine_sim_r_transition.py
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm Phase 31Q:

```text
implements only pure in-memory SIM-R behavior transition wiring value objects
uses immutable dataclasses or equivalent immutable value objects
serializes deterministically
round-trips through JSON-compatible dictionaries
does not mutate input payloads
preserves wiring IDs and wiring version
preserves simulation/pre/post state IDs
preserves action IDs
preserves behavior profile/proposal IDs
preserves behavior key/category
preserves transition ID when present
preserves resource ledger IDs
preserves requirement IDs
preserves unsupported note IDs
preserves compatibility status
preserves failure reasons and caveats
rejects duplicate resource ledger IDs
rejects duplicate requirement IDs
rejects duplicate unsupported note IDs
rejects negative turn metadata
rejects negative priority sequence metadata
rejects executable code payloads
rejects callable payloads
requires visible failure reason or caveat for incompatible links
does not execute behavior proposals
does not apply zone changes to SimulationState
does not create resource ledger records
does not create transition results
does not call Phase 13 simulator search
does not read Scryfall/provider/SQLite data
does not generate recommendations
```

## Commands To Run From Clean Checkout

```powershell
python -m unittest tests.test_probability_engine_sim_r_wiring -v
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Static Scans

```powershell
rg -n "codie\.db|repositories|sqlite3|requests|httpx|providers|ingestion|analytics|recommendations|decision|evidence" codie\probability_engine\sim_r_wiring.py tests\test_probability_engine_sim_r_wiring.py
rg -n "execute|apply|mutate|search|run_|create_ledger|build_transition_result" codie\probability_engine\sim_r_wiring.py
rg -n "forge|openai|anthropic|google\.generativeai|langchain" codie
git diff --name-only -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
```

Expected:

```text
No forbidden imports.
No runtime behavior helpers in sim_r_wiring.py.
No Forge or LLM SDK imports.
No schema/repository/dependency drift.
```

## Reject If

```text
Phase 31Q executes card behavior
Phase 31Q mutates SimulationState
Phase 31Q creates SimulationResourceLedger records
Phase 31Q creates SimulationTransitionResult records
Phase 31Q calls existing simulator search
Phase 31Q reads source/provider/Scryfall/SQLite data
Phase 31Q adds schema, repositories, dependencies, UI, live network calls, Forge, LLM SDKs, or recommendations
Phase 31Q treats simulator output as tournament evidence
```

## Gate

```text
Phase 31R remains blocked until Phase 31Q outside validation returns PASS or PASS WITH REVIEW NOTES.
```
