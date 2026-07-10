# Active Roadmap Index

Status: active governance index

This file is the compact restart map for Codie. Detailed phase history remains in `docs/CODEX_CONTINUITY_HANDOFF.md` and `docs/NEXT_PHASE_CONTRACT.md`.

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
Phase 31C SIM-R State Model Contract: internally complete
Current action: send Phase 31C outside validation packet
Local alpha tag status: created locally; remote tag push not verified in this environment
```

## Next Allowed Phase

```text
Phase 31C outside validation
```

Do not begin Phase 31D until Phase 31C outside validation returns PASS or PASS WITH REVIEW NOTES.

## Release-Critical Path

```text
1. Phase 31C outside validation
2. Phase 31D SIM-R state model implementation contract
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
Simulator Revision (SIM-R)
```

These items remain roadmap-only until a future contract explicitly authorizes implementation.

## Research / Reference-Only Items

```text
Rules reference repositories
Cytoscape / graph visualization references
sqlite-vec
LocalSend
Moxfield parser references
MTGJSON references
Forge references for SIM-R validation only
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

## Phase 31C Outside Validation Packet

Send these files for the current gate:

```text
docs/PHASE31C_SIM_R_STATE_MODEL_CONTRACT.md
docs/CHECKPOINT_PHASE31C_SIM_R_STATE_MODEL_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE31C_SIM_R_STATE_MODEL_PROMPT.md
docs/PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_CONTRACT.md
docs/CHECKPOINT_PHASE31B_SIM_R_CURRENT_SIMULATOR_FREEZE_REPORT.md
docs/PHASE31A_SIM_R_ARCHITECTURE_CONTRACT.md
docs/CHECKPOINT_PHASE31A_SIM_R_ARCHITECTURE_CONTRACT_REPORT.md
docs/ROADMAP_PATCH_SIMULATOR_REVISION_SIM_R.md
docs/PHASE13_SIMULATOR_CONTRACT_REFRESH.md
docs/CHECKPOINT_PHASE13_SIMULATOR_TRACK_REPORT.md
docs/CHECKPOINT_PHASE14_SIMULATION_REVIEW_EXPORT_REPORT.md
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
