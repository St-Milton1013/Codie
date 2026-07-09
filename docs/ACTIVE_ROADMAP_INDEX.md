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
Current action: prepare Phase 28C checkpoint and outside validation packet
Phase 29 status: blocked until Phase 28 outside validation is accepted
```

## Next Allowed Phase

```text
Phase 28C - Deck Health / Recommendation Output checkpoint and outside validation prompt
```

Do not start Phase 29 until Phase 28 outside validation is accepted.

## Release-Critical Path

```text
1. Phase 28C Deck Health / Recommendation Output checkpoint
2. Phase 28 outside validation
3. Phase 29A CLI / Report integration contract
4. Phase 29A CLI / Report integration
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
Phase 29 cannot start until Phase 28 outside validation is accepted.
```

## Phase 28C Checkpoint Packet

Prepare these files for the current gate:

```text
docs/PHASE28A_DECK_HEALTH_RECOMMENDATION_OUTPUT_CONTRACT.md
docs/PHASE28B_DECK_HEALTH_RECOMMENDATION_OUTPUT_IMPLEMENTATION_REPORT.md
codie/recommendation_output/__init__.py
codie/recommendation_output/models.py
tests/test_recommendation_output_boundary.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```
