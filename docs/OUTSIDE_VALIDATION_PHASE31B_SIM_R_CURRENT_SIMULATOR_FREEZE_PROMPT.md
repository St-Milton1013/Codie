# Outside Validation Prompt - Phase 31B SIM-R Current Simulator Freeze

Validate Codie Phase 31B against `CODIE_V1_CONSTITUTION.md`, the accepted
Phase 31A SIM-R architecture contract, and the accepted Phase 13/14 simulator
contracts.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

## Files To Review

```text
docs/PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_CONTRACT.md
docs/CHECKPOINT_PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_PROMPT.md
docs/PHASE31A_SIM_R_ARCHITECTURE_CONTRACT.md
docs/CHECKPOINT_PHASE31A_SIM_R_ARCHITECTURE_CONTRACT_REPORT.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
docs/USER_GUIDE_SIMULATION_REVIEW_EXPORTS.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Scope

Confirm Phase 31B is a freeze/checkpoint packet only and does not implement:

```text
production simulator changes
schema changes
repository changes
database reads or writes
Forge integration
Forge dependency installation
behavior module implementation
state engine implementation
resource ledger implementation
compound target implementation
trace v2 implementation
paired simulation implementation
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

Confirm Phase 31B did not modify simulator runtime files:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/probability_engine codie/cli/simulation_review.py
```

Expected: no matches.

Confirm Phase 31B did not modify simulation schema or repositories:

```powershell
git diff --name-only HEAD~1..HEAD -- codie/db/schema codie/db/repositories docs/SCHEMA_SPEC.md
```

Expected: no matches.

Confirm Phase 31B did not add dependencies:

```powershell
git diff --name-only HEAD~1..HEAD -- requirements.txt requirements-dev.txt pyproject.toml
```

Expected: no matches.

Confirm no production Forge or LLM SDK imports were added:

```powershell
rg -n "forge|openai|anthropic|google.generativeai|langchain" codie
```

Expected: no production integration matches.

## Validate Freeze Coverage

Confirm the freeze contract names:

```text
current simulator runtime modules
simulation schema/repository surfaces
fixtures and reference captures
existing behavior guarantees
required regression test groups
future compatibility/versioning rule
future rejection conditions
```

## Reject If

Reject Phase 31B if:

```text
it changes simulator runtime behavior
it changes schema or repositories
it adds Forge runtime integration
it adds LLM executable behavior generation
it treats simulator output as tournament evidence
it allows simulator output to directly generate recommendations
it weakens existing Phase 13/14 simulator contracts
it starts Phase 31C implementation before outside validation accepts Phase 31B
```

## Expected Result

```text
Phase 31B PASS or PASS WITH REVIEW NOTES means Phase 31C may begin contract-first.
Phase 31B PASS WITH REQUIRED FIXES means patch the freeze packet before Phase 31C.
Phase 31B FAIL means do not proceed with SIM-R implementation planning.
```

