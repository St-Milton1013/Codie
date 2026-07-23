# Active Roadmap Index

Status: active governance index

This file is the compact restart map for Codie. Detailed phase history remains in `docs/CODEX_CONTINUITY_HANDOFF.md` and `docs/NEXT_PHASE_CONTRACT.md`.

## Constitutional Authority

```text
Primary constitutional authority: docs/CODIE_V2_CONSTITUTION.md
Historical reference: docs/CODIE_V1_CONSTITUTION.md
V1 disposition: unchanged and retained
V2 status: adopted on main
```

The V2 adoption packet was governance-only. V2 is now the primary constitution.
This does not retroactively authorize runtime, schema, provider, UI, LLM,
simulator, recommendation, or export implementation without accepted contracts.

## Current Phase Gate

```text
Phase 25 Evidence Fusion: externally accepted
Phase 26A Decision Intelligence Boundary Contract: complete
Phase 26B Decision Intelligence Boundary Packet Implementation: internally complete
Phase 26 Decision Intelligence Boundary: externally accepted
Phase 27A Weight Profile / Analysis Profile Contract: complete
Phase 27B Weight Profile / Analysis Profile Packet Implementation: internally complete
Phase 27 Weight Profile / Analysis Profile: externally accepted
Phase 28A Deck Health / Recommendation Output Contract: complete
Phase 28A Deck Health / Recommendation Output Contract: accepted with review notes
Phase 28B Deck Health / Recommendation Output Packet Implementation: internally complete
Phase 28C Deck Health / Recommendation Output checkpoint: complete
Phase 28 Deck Health / Recommendation Output: externally accepted
Phase 29A CLI / Report Integration Contract: complete
Phase 29A CLI / Report Integration Contract: accepted with required fix applied
Phase 29B Report Document Implementation: internally complete
Phase 29C CLI / Safe File Writer Integration Contract: complete
Phase 29D Safe Recommendation Report File Writer: internally complete
Phase 29E Recommendation Output CLI Wrapper: externally accepted
Phase 29F CLI / Report Integration Checkpoint: externally accepted
Phase 30A Local Alpha Release Checklist: externally accepted
Phase 30B Local Alpha Packaging / Usage Documentation: externally accepted
Phase 30C Local Alpha Release Candidate Checkpoint: externally accepted
Phase 30D Local Alpha Tag / Release Notes / Handoff Finalization: externally accepted
Phase 31A SIM-R Architecture Contract: externally accepted
Phase 31B SIM-R Current Simulator Freeze: externally accepted
Phase 31C SIM-R State Model Contract: externally accepted
Phase 31D SIM-R State Model Implementation Contract: externally accepted
Phase 31E SIM-R State Model Implementation: externally accepted
Phase 31F SIM-R Resource Ledger Contract: externally accepted
Phase 31G SIM-R Resource Ledger Implementation Contract: externally accepted
Phase 31H SIM-R Resource Ledger Implementation: externally accepted
Phase 31I SIM-R State Transition Contract: externally accepted
Phase 31J SIM-R State Transition Implementation Contract: externally accepted
Phase 31K SIM-R State Transition Implementation: externally accepted
Phase 31L SIM-R Behavior Module Contract: externally accepted
Phase 31M SIM-R Behavior Module Implementation Contract: externally accepted
Phase 31N SIM-R Behavior Module Implementation: externally accepted
Phase 31O SIM-R Behavior Transition Wiring Contract: externally accepted
Phase 31P SIM-R Behavior Transition Wiring Implementation Contract: externally accepted
Phase 31Q SIM-R Behavior Transition Wiring Implementation: externally accepted
Phase 31R SIM-R Foundation Checkpoint / Freeze: externally accepted
Post-Phase 31 Deferred Implementation Priority Plan: logged
Phase 32A Scryfall Bulk Data Foundation Contract: externally accepted
Post-Phase 31 Patch Plan Cementing Audit: complete
Phase 32B Scryfall Bulk Data Foundation Implementation Contract: externally accepted
Phase 32C Scryfall Bulk Data Foundation Implementation: externally accepted
Phase 32C review-note correction: applied
Phase 33A Scryfall Migration Monitoring Contract: externally accepted
Phase 33B Scryfall Migration Monitoring Implementation Contract: externally accepted
Phase 33C Scryfall Migration Monitoring Implementation: externally accepted
Phase 34A Scryfall Tagger Functional Ontology Contract: externally accepted
Phase 34B Scryfall Tagger Ontology Implementation Contract: externally accepted
Phase 34C Scryfall Tagger Ontology Implementation: externally accepted
Phase 35A Commander Spellbook Interpreter Expansion Contract: externally accepted
Phase 35B Commander Spellbook Interpreter Implementation Contract: externally accepted
Phase 35C Commander Spellbook Interpreter Implementation: externally accepted
Phase 36A Immutable Deck Snapshot Expansion Contract: externally accepted
Phase 36B Immutable Deck Snapshot Implementation Contract: externally accepted
Phase 36C Immutable Deck Snapshot Implementation: externally accepted
Phase 37A Frequency Pools / Tag Graph Lab Contract: externally accepted with review notes
Phase 37B Frequency Pools / Tag Graph Lab Implementation Contract: accepted with review notes
Phase 37C Frequency Pool Packet Models and Validators: externally accepted
Phase 37D Tag Graph Metric Packet Models and Validators: externally accepted
Phase 37E Tag Graph Export / Report Contract: externally accepted
Phase 37 Frequency Pools / Tag Graph Lab split: externally accepted
Phase 38A Moxfield Frequency Pool Builder Contract: externally accepted
Phase 38B Moxfield Frequency Pool Builder Implementation Contract: externally accepted
Phase 38C Moxfield Frequency Pool Builder Implementation: externally accepted with review notes
Phase 38D Moxfield Frequency Pool Builder Checkpoint: externally accepted
Phase 39A Cockatrice Interoperability Contract: externally accepted with review notes
Phase 39B Cockatrice Interoperability Implementation Contract: internally complete
Current action: send Phase 39B Cockatrice Interoperability Implementation Contract to PR validation
Local alpha tag status: created locally; remote tag push not verified in this environment
```

## Next Allowed Phase

```text
Phase 39B Cockatrice Interoperability Implementation Contract
```

Phase 38D received artifact-backed phase-ledger validation on merged `main`.
Phase 39A received artifact-backed phase-ledger validation on merged `main`.
Phase 39B is prepared as an implementation-contract-only packet. Phase 39C
remains blocked until Phase 39B returns PASS or PASS WITH REVIEW NOTES.

Phase 39A validation tuple:

```text
phase_id: Phase39A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 39A acceptance evidence:

```text
workflow run ID: 29969137239
validated SHA: bf1a966cbbf406820514ec1b2992688ed688bca1
artifact: codie-phase_ledger-validation-bf1a966cbbf406820514ec1b2992688ed688bca1
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with one INFORMATIONAL historical finding
aggregate: CLEAN_PASS
final governance verdict: PASS WITH REVIEW NOTES
required corrections: none
```

The Phase 39A informational finding references historical Phase 36B contract
narrative and has no required correction.

Phase 39B validation tuple:

```text
phase_id: Phase39B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 38A active-scope transition evidence:

```text
workflow run ID: 29928542885
validated SHA: 7f5caa161ba90f2f753da556a75f97145e0c8d9b
artifact: codie-phase_ledger-validation-7f5caa161ba90f2f753da556a75f97145e0c8d9b
aggregate: CLEAN_PASS
```

Phase 38A acceptance evidence:

```text
workflow run ID: 29935858106
validated SHA: 2bfa81dbb8c23a1b62737a8411467b602c6de1c3
artifact: codie-phase_ledger-validation-2bfa81dbb8c23a1b62737a8411467b602c6de1c3
aggregate: CLEAN_PASS
```

Phase 38B active-scope transition evidence:

```text
workflow run ID: 29936045711
validated SHA: 8df261b4353c6fc9a7902112d6a742b27803093d
artifact: codie-phase_ledger-validation-8df261b4353c6fc9a7902112d6a742b27803093d
aggregate: CLEAN_PASS
```

Phase 38B acceptance evidence:

```text
workflow run ID: 29936658939
validated SHA: e132ca12598c9112d5729300c53d13a398b44f9d
artifact: codie-phase_ledger-validation-e132ca12598c9112d5729300c53d13a398b44f9d
aggregate: CLEAN_PASS
```

Phase 38C active-scope transition evidence:

```text
workflow run ID: 29936996144
validated SHA: 47756ffaa641a733f47e4ffe9720e7132590f236
artifact: codie-phase_ledger-validation-47756ffaa641a733f47e4ffe9720e7132590f236
aggregate: CLEAN_PASS
```

Phase 38C acceptance evidence:

```text
workflow run ID: 29962601660
validated SHA: bbacc28e00a0cc617f5443d834c47aba05835147
artifact: codie-phase_ledger-validation-bbacc28e00a0cc617f5443d834c47aba05835147
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with one INFORMATIONAL finding
aggregate: CLEAN_PASS
required corrections: none
```

The Phase 38C informational finding is a nonblocking historical observation
from Phase 37A and requires no corrective action.

Phase 38D acceptance evidence:

```text
workflow run ID: 29964132762
validated SHA: 38b3fc9d7cc812062674ae0615d7d5733c4b5401
artifact: codie-phase_ledger-validation-38b3fc9d7cc812062674ae0615d7d5733c4b5401
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
unresolved findings: none
```

Phase 37A acceptance evidence:

```text
workflow run ID: 29340418728
validated SHA: 1b958d28f1d4840d56b8b1d270fc0760b41bad6a
artifact: codie-phase_ledger-validation-1b958d28f1d4840d56b8b1d270fc0760b41bad6a
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with two INFORMATIONAL findings
aggregate: CLEAN_PASS
final governance verdict: PASS WITH REVIEW NOTES
required corrections: none
```

The adversarial informational findings are nonblocking historical observations
and require no corrective action.

Phase 37 final acceptance evidence:

```text
workflow run ID: 29881579352
validated SHA: 5901dc51d8bc823ce85e29894768573d0555b91a
artifact: codie-phase_ledger-validation-5901dc51d8bc823ce85e29894768573d0555b91a
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: CLEAN_PASS
aggregate: CLEAN_PASS
final governance verdict: PASS
unresolved findings: none
```

## Release-Critical Path

```text
1. Phase 37A Frequency Pools / Tag Graph Lab Contract: accepted with review notes
2. Phase 37B Frequency Pools / Tag Graph Lab Implementation Contract: accepted with review notes
3. Phase 37C Frequency Pool Packet Models and Validators: accepted
4. Phase 37D Tag Graph Metric Packet Models and Validators: accepted
5. Phase 37E Tag Graph Export / Report Contract: accepted
6. Phase 38A Moxfield Frequency Pool Builder Contract: accepted
7. Phase 38B Moxfield Frequency Pool Builder Implementation Contract: accepted
8. Phase 38C Moxfield Frequency Pool Builder Implementation: accepted with review notes
9. Phase 38D Moxfield Frequency Pool Builder Checkpoint: accepted
10. Phase 39A Cockatrice Interoperability Contract: accepted with review notes
11. Phase 39B Cockatrice Interoperability Implementation Contract: internal pass; PR validation required
12. Phase 39C: blocked
```

The post-31 patch priority order is cemented in:

```text
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
```

## Post-Alpha / Later Roadmap

```text
SIM-R current simulator freeze / validation packet
Tag Graph Lab
Moxfield Frequency Pool Builder
Jin-Gitaxias Strategist Mode
Obsidian / Knowledge Vault
Advanced UI dashboard
Mobile-friendly local report delivery
Optional Discord / LocalSend / QR delivery integrations
Reddit RSS Community Signal Monitor
Simulator Revision (SIM-R)
Codie Master Architecture patch
Post-Phase 31 Deferred Implementation Priority Plan
```

These items remain roadmap-only until a future contract explicitly authorizes implementation.

Mobile report delivery is explicitly deferred by V2. All other V1 capabilities retain their V1 purpose, boundaries, and roadmap status unless V2 directly changes them. The standalone Natural Language Query Helper capability is folded into Jin query planning and Scryfall/Tagger translation.

The Reddit RSS Community Signal Monitor is a post-checkpoint, separately contracted discovery item. It may feed low-confidence community candidates to Jin, Theory Corpus review, research, rules, tool-evaluation, and experiment queues, but never tournament injection, measured analytics, recommendations, canonical evidence, or model training.

## Research / Reference-Only Items

```text
Rules reference repositories
Cytoscape / graph visualization references
sqlite-vec
LocalSend
Moxfield parser references
MTGJSON references
Forge references for SIM-R validation only
Cockatrice interoperability references
Scryfall bulk data and migration monitoring references
Scryfall Tagger functional ontology references
```

Reference repositories are not production dependencies unless a future contract explicitly approves that dependency.

## Deprecated Or Removed From V1

```text
Stream Deck Game Tracker
```

The Stream Deck Game Tracker is removed from active Codie V1 scope.

## Hard Gates

```text
No recommendations from raw provider data.
No recommendations directly from source tables.
No recommendations directly from primer text.
No recommendations directly from simulator output.
No feature should duplicate Decision Intelligence reasoning.
Recommendation output must flow through Evidence Fusion and Decision Intelligence.
Phase 29B report documents must not write files.
Phase 29D safe writer must not implement CLI behavior.
Phase 29E CLI wrapper must not generate recommendations.
SIM-R must not be implemented until the active validation chain completes and a dedicated SIM-R contract is accepted.
Simulator output remains evidence only and must never generate recommendations.
```

## Accepted Phase 31O Outside Validation Packet

Phase 31O was accepted with review notes using this packet:

```text
docs/PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT.md
docs/CHECKPOINT_PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT_PROMPT.md
docs/PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_PROMPT.md
docs/PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE31L_SIM_R_BEHAVIOR_MODULE_CONTRACT.md
docs/CHECKPOINT_PHASE31L_SIM_R_BEHAVIOR_MODULE_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31L_SIM_R_BEHAVIOR_MODULE_CONTRACT_PROMPT.md
docs/PHASE31K_SIM_R_STATE_TRANSITION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31K_SIM_R_STATE_TRANSITION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31K_SIM_R_STATE_TRANSITION_IMPLEMENTATION_PROMPT.md
docs/PHASE31J_SIM_R_STATE_TRANSITION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31J_SIM_R_STATE_TRANSITION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31J_SIM_R_STATE_TRANSITION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT.md
docs/CHECKPOINT_PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31I_SIM_R_STATE_TRANSITION_CONTRACT_PROMPT.md
docs/PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31H_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_PROMPT.md
docs/PHASE31G_SIM_R_RESOURCE_LEDGER_IMPLEMENTATION_CONTRACT.md
docs/PHASE31F_SIM_R_RESOURCE_LEDGER_CONTRACT.md
docs/PHASE31E_SIM_R_STATE_MODEL_IMPLEMENTATION_REPORT.md
docs/PHASE31D_SIM_R_STATE_MODEL_IMPLEMENTATION_CONTRACT.md
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
codie/probability_engine/sim_r_behavior.py
tests/test_probability_engine_sim_r_behavior.py
codie/probability_engine/sim_r_transition.py
tests/test_probability_engine_sim_r_transition.py
codie/probability_engine/sim_r_ledger.py
codie/probability_engine/__init__.py
tests/test_probability_engine_sim_r_ledger.py
codie/probability_engine/sim_r_state.py
tests/test_probability_engine_sim_r_state.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/PHASE30A_OUTSIDE_VALIDATION_PACKET_MESSAGE.md
docs/PHASE30B_LOCAL_ALPHA_PACKAGING_PLANNING_DRAFT.md
docs/LOCAL_ALPHA_USAGE_DOCUMENTATION_OUTLINE_DRAFT.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```

## Accepted Phase 31P Outside Validation Packet

Phase 31P was accepted with review notes using this packet:

```text
docs/PHASE31P_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE31P_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31P_SIM_R_BEHAVIOR_TRANSITION_WIRING_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT.md
docs/CHECKPOINT_PHASE31O_SIM_R_BEHAVIOR_TRANSITION_WIRING_CONTRACT_REPORT.md
docs/PHASE31N_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_REPORT.md
docs/PHASE31M_SIM_R_BEHAVIOR_MODULE_IMPLEMENTATION_CONTRACT.md
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

## Accepted Phase 31Q Outside Validation Packet

Phase 31Q was accepted with review notes using this packet:

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

## Accepted Phase 31R Outside Validation Packet

Phase 31R was accepted with review notes using this packet:

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

## Accepted Phase 32A Outside Validation Packet

Phase 32A was accepted with review notes using this packet:

```text
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 32B Outside Validation Packet

Phase 32B was accepted with review notes using this packet:

```text
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 32C Outside Validation Packet

Phase 32C was accepted with review notes using this packet:

```text
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_PROMPT.md
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_REPORT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
codie/cards/scryfall_bulk_snapshots.py
codie/cards/__init__.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/bulk_manifest.json
tests/fixtures/scryfall/default_cards_snapshot.json
tests/fixtures/scryfall/malformed_bulk_snapshot.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Phase 32C Review-Note Correction

Applied before Phase 33A:

```text
fixture metadata bulk_type is used when caller does not override it
explicit bulk_type still overrides fixture metadata
manifest dictionary round-trip test reconstructs file_refs and compares full serialized equality
```

## Accepted Phase 33A Outside Validation Packet

Phase 33A was accepted with review notes using this packet:

```text
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_PROMPT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 33B Outside Validation Packet

Phase 33B was accepted with review notes using this packet:

```text
docs/PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
codie/cards/scryfall_bulk_snapshots.py
tests/test_scryfall_bulk_snapshots.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 33C Outside Validation Packet

Phase 33C was accepted with review notes using this packet:

```text
docs/PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_PROMPT.md
docs/PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE33B_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT.md
docs/CHECKPOINT_PHASE33A_SCRYFALL_MIGRATION_MONITORING_CONTRACT_REPORT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
codie/cards/scryfall_migration_monitoring.py
codie/cards/scryfall_bulk_snapshots.py
codie/cards/__init__.py
tests/test_scryfall_migration_monitoring.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/migration_previous_snapshot.json
tests/fixtures/scryfall/migration_next_snapshot.json
tests/fixtures/scryfall/migration_unknown_fields_snapshot.json
tests/fixtures/scryfall/migration_unknown_enums_snapshot.json
tests/fixtures/scryfall/migration_breaking_snapshot.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Review note:

```text
affected-consumer/manual-review field names differ from one earlier prompt's
exact wording, but no required fix was requested
```

## Accepted Phase 34A Outside Validation Packet

Phase 34A was accepted with review notes using this packet:

```text
docs/PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT.md
docs/CHECKPOINT_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_PROMPT.md
docs/PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/CODIE_V1_CONSTITUTION.md
codie/cards/scryfall_migration_monitoring.py
tests/test_scryfall_migration_monitoring.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Review note:

```text
Phase 34B should explicitly decide whether to include alias/deprecation/conflict/replacement-chain ontology handling
```

## Accepted Phase 34B Outside Validation Packet

Phase 34B was accepted with review notes using this packet:

```text
docs/PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT.md
docs/CHECKPOINT_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_PROMPT.md
docs/PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/CODIE_V1_CONSTITUTION.md
codie/cards/scryfall_migration_monitoring.py
tests/test_scryfall_migration_monitoring.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 34C Outside Validation Packet

Phase 34C was accepted with review notes using this packet:

```text
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_PROMPT.md
docs/PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT.md
docs/CHECKPOINT_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_REPORT.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/CODIE_V1_CONSTITUTION.md
codie/cards/scryfall_tagger_ontology.py
codie/cards/__init__.py
tests/test_scryfall_tagger_ontology.py
tests/fixtures/scryfall_tagger/tagger_functional_tags.json
tests/fixtures/scryfall_tagger/tagger_artwork_tags.json
tests/fixtures/scryfall_tagger/tagger_unknown_namespace.json
tests/fixtures/scryfall_tagger/tagger_duplicate_tags.json
tests/fixtures/scryfall_tagger/tagger_aliases_deprecated_conflicts.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 35A Outside Validation Packet

Phase 35A was accepted with review notes using this packet:

```text
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_PROMPT.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_PROMPT.md
docs/PHASE7A_SPELLBOOK_COMBO_EVIDENCE_CONTRACT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/providers/spellbook/parser.py
codie/combos/sync.py
tests/test_provider_spellbook.py
tests/test_combo_sync.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 35B Outside Validation Packet

Phase 35B was accepted with review notes using this packet:

```text
docs/PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_PROMPT.md
docs/PHASE7A_SPELLBOOK_COMBO_EVIDENCE_CONTRACT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/providers/spellbook/parser.py
codie/combos/sync.py
tests/test_provider_spellbook.py
tests/test_combo_sync.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 35C Outside Validation Packet

Phase 35C was accepted with review notes using this packet:

```text
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_PROMPT.md
docs/PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/PHASE7A_SPELLBOOK_COMBO_EVIDENCE_CONTRACT.md
docs/CODIE_V1_CONSTITUTION.md
codie/combos/spellbook_interpreter.py
codie/combos/__init__.py
tests/test_spellbook_interpreter.py
tests/fixtures/spellbook_interpreter/spellbook_combo_outputs.json
tests/fixtures/spellbook_interpreter/spellbook_combo_restrictions.json
tests/fixtures/spellbook_interpreter/spellbook_combo_unknowns.json
codie/providers/spellbook/parser.py
codie/combos/sync.py
tests/test_provider_spellbook.py
tests/test_combo_sync.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Accepted Phase 36A Outside Validation Packet

Phase 36A was accepted with review notes using this packet:

```text
docs/PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_PROMPT.md
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/user_decks/importer.py
codie/user_decks/deck_memory.py
codie/user_decks/analysis_input.py
codie/db/schema/user.sql
codie/db/repositories/user.py
tests/test_user_deck_import.py
tests/test_user_deck_memory.py
tests/test_user_deck_analysis_input.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Phase 36A outside validation review notes to carry forward:

```text
Phase 36B / 36C must make redaction behavior concrete:
- default redacted snapshot packet
- explicit full-card-list option
- visible privacy caveat on full-card-list snapshots
- hard rejection of raw imported text and private notes by default

GitHub CI was not available for the Phase 36A validation result.
```

## Current Phase 36B Outside Validation Packet

Send these files for the current gate:

```text
docs/PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36B_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE36A_IMMUTABLE_DECK_SNAPSHOT_EXPANSION_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/user_decks/importer.py
codie/user_decks/deck_memory.py
codie/user_decks/analysis_input.py
codie/user_decks/__init__.py
codie/db/schema/user.sql
codie/db/repositories/user.py
tests/test_user_deck_import.py
tests/test_user_deck_memory.py
tests/test_user_deck_analysis_input.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```
