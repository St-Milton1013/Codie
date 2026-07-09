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
Phase 28C: checkpoint pending
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
Phase 28B Deck Health / Recommendation Output Packet Implementation: INTERNAL PASS; CHECKPOINT PENDING
```

## Latest Local Validation

```text
Focused Phase 28B Recommendation Output:
python -m unittest tests.test_recommendation_output_boundary -v
Ran 11 tests in 0.005s
OK

Full suite:
python -m unittest discover -s tests
Ran 772 tests in 5.357s
OK (skipped=1)

Static check:
git diff --check
passed
```

## Current Blocker

```text
Phase 29 is blocked until Phase 28 checkpoint and outside validation are accepted.
```

## Current Phase 28C Checkpoint Packet

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
```
