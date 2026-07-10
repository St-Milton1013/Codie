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
Phase 30B Local Alpha Packaging / Usage Documentation: internally complete
Current action: send Phase 30B outside validation packet
Phase 30C status: blocked until Phase 30B outside validation is accepted
```

## Next Allowed Phase

```text
Phase 30C - Local Alpha release candidate checkpoint after Phase 30B outside validation
```

Do not start Phase 30C until Phase 30B outside validation returns PASS or PASS WITH REVIEW NOTES.

## Release-Critical Path

```text
1. Phase 30B outside validation
2. Phase 30C Local Alpha release candidate checkpoint
```

## Post-Alpha / Later Roadmap

```text
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

## Phase 30B Outside Validation Packet

Send these files for the current gate:

```text
docs/PHASE30B_LOCAL_ALPHA_PACKAGING_USAGE_CONTRACT.md
docs/LOCAL_ALPHA_README.md
docs/LOCAL_ALPHA_COMMANDS.md
docs/LOCAL_ALPHA_KNOWN_CAVEATS.md
docs/LOCAL_ALPHA_VALIDATION_STEPS.md
docs/CHECKPOINT_PHASE30B_LOCAL_ALPHA_PACKAGING_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE30B_LOCAL_ALPHA_PACKAGING_PROMPT.md
docs/PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_CONTRACT.md
docs/CHECKPOINT_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE30A_LOCAL_ALPHA_RELEASE_CHECKLIST_PROMPT.md
docs/CHECKPOINT_PHASE29F_CLI_REPORT_INTEGRATION_REPORT.md
docs/PRE_PHASE30_AUDIT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE29F_CLI_REPORT_INTEGRATION_PROMPT.md
docs/PHASE29E_RECOMMENDATION_OUTPUT_CLI_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29E_RECOMMENDATION_OUTPUT_CLI_REPORT.md
docs/PHASE29D_CLI_SAFE_FILE_WRITER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE29D_SAFE_FILE_WRITER_REPORT.md
docs/PHASE29C_CLI_SAFE_FILE_WRITER_CONTRACT.md
codie/cli/recommendation_output.py
codie/recommendation_output/writers.py
codie/recommendation_output/reporting.py
tests/test_cli_recommendation_output.py
tests/test_recommendation_output_writers.py
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
