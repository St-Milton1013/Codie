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
Current action: review Phase 27A, then proceed to Phase 27B if accepted
Phase 27 status: Phase 27B blocked until Phase 27A is reviewed
```

## Next Allowed Phase

```text
Phase 27B - Weight Profile / Analysis Profile Packet Implementation after Phase 27A review
```

Do not start Phase 27B implementation until the Phase 27A contract is complete and reviewed.

## Release-Critical Path

```text
1. Phase 27A Weight Profile / Analysis Profile Contract
2. Phase 27B Weight Profile implementation
3. Phase 28A Deck Health / Recommendation Output Contract
4. Phase 28B Deck Health / Recommendation Output MVP
5. Phase 29A CLI / Report integration
6. Phase 30A Local Alpha release checklist
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
Phase 27B cannot start until Phase 27A is complete and reviewed.
```

## Current Phase 27A Packet

Current contract file:

```text
docs/PHASE27A_WEIGHT_PROFILE_ANALYSIS_PROFILE_CONTRACT.md
```
