# Phase 31R - SIM-R Foundation Checkpoint / Freeze Contract

Status: checkpoint contract only

## Purpose

Phase 31R closes the current SIM-R foundation track by freezing the implemented
pure model surfaces and documenting the boundary for future simulator work.

This phase is a checkpoint and freeze packet. It does not add simulator runtime
behavior.

## Accepted Dependency

Phase 31R may begin because Phase 31Q outside validation returned:

```text
PASS WITH REVIEW NOTES
```

## Frozen SIM-R Foundation Surfaces

The following SIM-R foundation modules are frozen as pure model layers:

```text
codie/probability_engine/sim_r_state.py
codie/probability_engine/sim_r_ledger.py
codie/probability_engine/sim_r_transition.py
codie/probability_engine/sim_r_behavior.py
codie/probability_engine/sim_r_wiring.py
```

The following tests are part of the foundation checkpoint:

```text
tests/test_probability_engine_sim_r_state.py
tests/test_probability_engine_sim_r_ledger.py
tests/test_probability_engine_sim_r_transition.py
tests/test_probability_engine_sim_r_behavior.py
tests/test_probability_engine_sim_r_wiring.py
```

## Freeze Rule

Future work must not modify these SIM-R foundation surfaces without a dedicated
contract, tests, validation report, and outside validation.

Minor documentation updates may reference these surfaces, but runtime behavior,
new execution semantics, state mutation, resource spending, transition creation,
behavior execution, and search remain contract-gated.

## Not Authorized In Phase 31R

```text
production simulator runtime changes
behavior proposal execution
behavior proposal application
state mutation logic
resource ledger creation or mutation
transition result creation from behavior proposals
card behavior execution
action execution
search implementation
state hashing implementation
trace v2 runtime implementation
paired simulation implementation
Monte Carlo simulation changes
Phase 13 simulator search calls
Scryfall/provider loading
SQLite reads or writes
schema changes
repository changes
dependency changes
Forge integration
LLM behavior generation
recommendation generation
UI work
live network calls
post-31 deferred backlog implementation
```

## Required Checkpoint Verification

Phase 31R must verify:

```text
Phase 31A through Phase 31Q are accepted or internally complete as appropriate
Phase 31Q is recorded as externally accepted
SIM-R foundation modules remain pure model layers
SIM-R foundation modules do not execute behavior or mutate state
SIM-R foundation modules do not read providers, Scryfall, SQLite, analytics, recommendations, or UI
SIM-R foundation modules do not import Forge or LLM SDKs
SIM-R foundation tests pass
schema bootstrap passes
full test suite passes
git diff --check passes
schema/repository/dependency drift scans are clean
deferred backlog remains blocked until Phase 31R outside validation is accepted
```

## Required Validation Commands

```powershell
python -m unittest tests.test_probability_engine_sim_r_state tests.test_probability_engine_sim_r_ledger tests.test_probability_engine_sim_r_transition tests.test_probability_engine_sim_r_behavior tests.test_probability_engine_sim_r_wiring -v
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Required Static Scans

```powershell
git diff --name-only -- codie\probability_engine tests
git diff --name-only -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "forge|openai|anthropic|google\.generativeai|langchain" codie
rg -n "codie\.db|repositories|sqlite3|requests|httpx|providers|ingestion|analytics|recommendations|decision|evidence" codie\probability_engine\sim_r_state.py codie\probability_engine\sim_r_ledger.py codie\probability_engine\sim_r_transition.py codie\probability_engine\sim_r_behavior.py codie\probability_engine\sim_r_wiring.py
```

Expected:

```text
Only docs/status files change in Phase 31R.
No schema/repository/dependency drift.
No Forge or LLM SDK imports.
No forbidden cross-layer imports in SIM-R foundation modules.
```

## Next Gate

After Phase 31R outside validation returns PASS or PASS WITH REVIEW NOTES, the
Post-Phase 31 Deferred Implementation Priority Plan may begin contract-first.

No deferred implementation may begin before Phase 31R outside validation is
accepted.
