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
Current action: send Phase 27 outside validation packet
Phase 28 status: blocked until Phase 27 outside validation returns PASS or PASS WITH REVIEW NOTES
```

## Next Allowed Phase

```text
Phase 28A - Deck Health / Recommendation Output Contract after Phase 27 outside validation
```

Do not start Phase 28 until the Phase 27 outside validation gate is accepted.

## Release-Critical Path

```text
1. Phase 27 outside validation
2. Phase 28A Deck Health / Recommendation Output Contract
3. Phase 28B Deck Health / Recommendation Output MVP
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
Phase 28 cannot start until Phase 27 outside validation is accepted.
```

## Phase 27 Outside Validation Packet

Send these files for the current gate:

```text
docs/CHECKPOINT_PHASE27_WEIGHT_PROFILE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE27_WEIGHT_PROFILE_PROMPT.md
docs/PHASE27A_WEIGHT_PROFILE_ANALYSIS_PROFILE_CONTRACT.md
docs/PHASE27B_WEIGHT_PROFILE_IMPLEMENTATION_REPORT.md
codie/weight_profiles/__init__.py
codie/weight_profiles/models.py
codie/weight_profiles/defaults.py
tests/test_weight_profiles.py
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```
