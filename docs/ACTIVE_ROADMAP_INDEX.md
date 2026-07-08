# Active Roadmap Index

Status: active governance index

This file is the compact restart map for Codie. Detailed phase history remains in `docs/CODEX_CONTINUITY_HANDOFF.md` and `docs/NEXT_PHASE_CONTRACT.md`.

## Current Phase Gate

```text
Phase 25 Evidence Fusion: internally complete
Current action: send Phase 25 outside validation packet
Phase 26 status: blocked until Phase 25 outside validation returns PASS or PASS WITH REVIEW NOTES
```

## Next Allowed Phase

```text
Phase 26A - Decision Intelligence Boundary Contract
```

Do not start Phase 26 implementation before the Phase 25 outside validation gate is accepted.

## Release-Critical Path

```text
1. Phase 25 outside validation
2. Phase 26A Decision Intelligence Boundary Contract
3. Phase 26B Decision Intelligence MVP packet implementation
4. Phase 27A Weight Profile / Analysis Profile Contract
5. Phase 27B Weight Profile implementation
6. Phase 28A Deck Health / Recommendation Output Contract
7. Phase 28B Deck Health / Recommendation Output MVP
8. Phase 29A CLI / Report integration
9. Phase 30A Local Alpha release checklist
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
Phase 26 cannot start until Phase 25 outside validation is accepted.
```

## Phase 25 Outside Validation Packet

Send these files for the current gate:

```text
docs/CHECKPOINT_PHASE25_EVIDENCE_FUSION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE25_EVIDENCE_FUSION_PROMPT.md
docs/PHASE25A_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_CONTRACT.md
docs/PHASE25B_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_IMPLEMENTATION_REPORT.md
codie/evidence_fusion/__init__.py
codie/evidence_fusion/models.py
codie/evidence_fusion/builders.py
tests/test_evidence_fusion_models.py
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```
