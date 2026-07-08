# Active Roadmap Index

Status: active governance index

This file is the compact restart map for Codie. Detailed phase history remains in `docs/CODEX_CONTINUITY_HANDOFF.md` and `docs/NEXT_PHASE_CONTRACT.md`.

## Current Phase Gate

```text
Phase 25 Evidence Fusion: externally accepted
Phase 26A Decision Intelligence Boundary Contract: complete
Phase 26B Decision Intelligence Boundary Packet Implementation: internally complete
Current action: send Phase 26 outside validation packet
Phase 27 status: blocked until Phase 26 outside validation returns PASS or PASS WITH REVIEW NOTES
```

## Next Allowed Phase

```text
Phase 27A - Weight Profile / Analysis Profile Contract after Phase 26 outside validation
```

Do not start Phase 27 until the Phase 26 outside validation gate is accepted.

## Release-Critical Path

```text
1. Phase 26 outside validation
2. Phase 27A Weight Profile / Analysis Profile Contract
3. Phase 27B Weight Profile implementation
4. Phase 28A Deck Health / Recommendation Output Contract
5. Phase 28B Deck Health / Recommendation Output MVP
6. Phase 29A CLI / Report integration
7. Phase 30A Local Alpha release checklist
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
Phase 27 cannot start until Phase 26 outside validation is accepted.
```

## Phase 26 Outside Validation Packet

Send these files for the current gate:

```text
docs/CHECKPOINT_PHASE26_DECISION_INTELLIGENCE_BOUNDARY_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE26_DECISION_INTELLIGENCE_BOUNDARY_PROMPT.md
docs/PHASE26A_DECISION_INTELLIGENCE_BOUNDARY_CONTRACT.md
docs/PHASE26B_DECISION_INTELLIGENCE_BOUNDARY_IMPLEMENTATION_REPORT.md
codie/decision_intelligence/__init__.py
codie/decision_intelligence/models.py
codie/decision_intelligence/builders.py
tests/test_decision_intelligence_boundary.py
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```
