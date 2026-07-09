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
Current action: review Phase 29A contract packet
Phase 29B status: blocked until Phase 29A review is accepted
```

## Next Allowed Phase

```text
Phase 29B - CLI / Report integration implementation after Phase 29A review
```

Do not start Phase 29B until Phase 29A is accepted.

## Release-Critical Path

```text
1. Phase 29A CLI / Report integration contract review
2. Phase 29B Report document implementation
3. Phase 29C CLI / safe file writer integration
4. Phase 29D CLI / Report integration checkpoint
5. Phase 30A Local Alpha release checklist
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
Phase 29B cannot start until Phase 29A is accepted.
```

## Phase 29A Contract Packet

Review these files for the current gate:

```text
docs/PHASE29A_CLI_REPORT_INTEGRATION_CONTRACT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```
