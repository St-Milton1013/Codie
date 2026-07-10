# Validation Status Index

Status: active validation index

This file is the compact validation snapshot for Codie. Detailed evidence, commands, and phase history remain in `docs/CODEX_CONTINUITY_HANDOFF.md`, `docs/NEXT_PHASE_CONTRACT.md`, and the individual checkpoint reports.

## Current Validation Gate

```text
Phase 25 Evidence Fusion: PASS
Outside validation: accepted
Phase 26 Decision Intelligence Boundary: PASS
Outside validation: accepted
Phase 27 Weight Profile / Analysis Profile: PASS
Outside validation: accepted
Phase 28A Deck Health / Recommendation Output Contract: PASS WITH REVIEW NOTES
Phase 28B Deck Health / Recommendation Output Packet Implementation: INTERNAL PASS
Phase 28C Deck Health / Recommendation Output Checkpoint: COMPLETE
Phase 28 Deck Health / Recommendation Output: PASS
Phase 29A CLI / Report Integration Contract: COMPLETE
Phase 29A outside review: PASS WITH REQUIRED FIXES; fixes applied
Phase 29B Report Document Implementation: INTERNAL PASS
Phase 29C CLI / Safe File Writer Integration Contract: COMPLETE
Phase 29D Safe Recommendation Report File Writer: INTERNAL PASS
Phase 29E Recommendation Output CLI Wrapper: PASS WITH REVIEW NOTES
Phase 29F CLI / Report Integration Checkpoint: PASS
Phase 30A Local Alpha Release Checklist: PASS
Phase 30B Local Alpha Packaging / Usage Documentation: PASS
Phase 30C Local Alpha Release Candidate Checkpoint: PASS
Phase 30D Local Alpha Tag / Release Notes / Handoff Finalization: PASS
Phase 31A SIM-R Architecture Contract: PASS WITH REVIEW NOTES
Phase 31B SIM-R Current Simulator Freeze: PASS
Phase 31C SIM-R State Model Contract: PASS WITH REVIEW NOTES
Phase 31D SIM-R State Model Implementation Contract: PASS WITH REVIEW NOTES
Phase 31E SIM-R State Model Implementation: PASS WITH REVIEW NOTES
Phase 31F SIM-R Resource Ledger Contract: PASS WITH REVIEW NOTES
Phase 31G SIM-R Resource Ledger Implementation Contract: INTERNAL PASS
Local alpha tag: created locally; remote tag push not verified in this environment
```

## Accepted Phase Summary

```text
Phase 0: PASS
Phase 1: PASS
Phase 2: PASS
Phase 3: PASS
Phase 4A TopDeck: PASS
Phase 4B EDHTop16: PASS
Phase 4C MTGTop8: PASS
Phase 4D MTGDecks: PASS
Phase 4E Hareruya: PASS WITH ACCESS CAVEAT
Phase 5 Canonicalization: PASS
Phase 6 Analytics Foundations: PASS
Phase 7A Spellbook Evidence: PASS
Phase 7B Moxfield Primer Metadata: PASS
Phase 8 Readiness / Recommendation Foundations / Innovation: PASS
Phase 9 Export Surfaces: PASS
Phase 10 User Deck Workflow: PASS WITH REVIEW NOTES
Phase 11 User Workflow Retrieval: historical checkpoint exists
Phase 12 Local UI / Report Sharing Track: COMPLETE
Phase 13 Simulator Track: PASS WITH REVIEW NOTES
Phase 14 Simulator Review Export Writer: PASS
Phase 15 Deck Memory Track: PASS
Phase 16 Evidence Graph: PASS
Phase 17 Evidence Graph Input Assembly: PASS
Phase 18 Source Conflict Report: PASS
Phase 19 Unsupported Relevant Card Queue: PASS
Phase 20 Chat Query Planner: PASS
Phase 21 Chat Answer Builder: PASS
Phase 22 LLM Writer / Auditor: PASS
Phase 23 Chat / Intelligence UI API Boundary: PASS
Phase 24 Chat / Intelligence Local API: PASS
Phase 25 Evidence Fusion: PASS
Phase 26 Decision Intelligence Boundary: PASS
Phase 27 Weight Profile / Analysis Profile: PASS
Phase 28A Deck Health / Recommendation Output Contract: PASS WITH REVIEW NOTES
Phase 28B Deck Health / Recommendation Output Packet Implementation: INTERNAL PASS
Phase 28 Deck Health / Recommendation Output: PASS
Phase 29A CLI / Report Integration Contract: PASS WITH REQUIRED FIXES APPLIED
Phase 29B Report Document Implementation: INTERNAL PASS
Phase 29C CLI / Safe File Writer Integration Contract: COMPLETE; REQUIRED FIXES APPLIED
Phase 29D Safe Recommendation Report File Writer: INTERNAL PASS
Phase 29E Recommendation Output CLI Wrapper: PASS WITH REVIEW NOTES
Phase 29F CLI / Report Integration Checkpoint: PASS
Phase 30A Local Alpha Release Checklist: PASS
Phase 30B Local Alpha Packaging / Usage Documentation: PASS
Phase 30C Local Alpha Release Candidate Checkpoint: PASS
Phase 30D Local Alpha Tag / Release Notes / Handoff Finalization: PASS
Phase 31A SIM-R Architecture Contract: PASS WITH REVIEW NOTES
Phase 31B SIM-R Current Simulator Freeze: PASS
Phase 31C SIM-R State Model Contract: PASS WITH REVIEW NOTES
Phase 31D SIM-R State Model Implementation Contract: PASS WITH REVIEW NOTES
Phase 31E SIM-R State Model Implementation: PASS WITH REVIEW NOTES
Phase 31F SIM-R Resource Ledger Contract: PASS WITH REVIEW NOTES
Phase 31G SIM-R Resource Ledger Implementation Contract: INTERNAL PASS
```

## Latest Local Validation

```text
Phase 31G SIM-R Resource Ledger Implementation Contract:
python scripts/check_schema.py
Schema bootstrap check passed.

python -m unittest discover -s tests
Ran 808 tests in 3.697s
OK (skipped=1)

git diff --check
passed

Static scans:
simulator runtime diff scan: no matches
schema/repository/dependency diff scan: no matches
production Forge / LLM SDK import scan: no matches
```

## Current Blocker

```text
Phase 31H is blocked until Phase 31G outside validation returns PASS or PASS WITH REVIEW NOTES.
```

## Current Phase 31G Outside Validation Packet

```text
docs/PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT.md
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
codie/probability_engine/sim_r_state.py
tests/test_probability_engine_sim_r_state.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```
