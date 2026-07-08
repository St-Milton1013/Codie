# Validation Status Index

Status: active validation index

This file is the compact validation snapshot for Codie. Detailed evidence, commands, and phase history remain in `docs/CODEX_CONTINUITY_HANDOFF.md`, `docs/NEXT_PHASE_CONTRACT.md`, and the individual checkpoint reports.

## Current Validation Gate

```text
Phase 25 Evidence Fusion: PASS
Outside validation: accepted
Phase 26 Decision Intelligence Boundary: PASS
Outside validation: accepted
Phase 27 Weight Profile / Analysis Profile: INTERNAL PASS
Outside validation: ready to send
Phase 28: blocked until Phase 27 outside validation returns PASS or PASS WITH REVIEW NOTES
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
Phase 27 Weight Profile / Analysis Profile: INTERNAL PASS; READY FOR OUTSIDE VALIDATION
```

## Latest Local Validation

```text
Focused Phase 25 Evidence Fusion:
python -m unittest tests.test_evidence_fusion_models -v
Ran 23 tests in 0.003s
OK

Full suite:
python -m unittest discover -s tests
Ran 761 tests in 3.499s
OK (skipped=1)

Static check:
git diff --check
passed
```

## Current Blocker

```text
Phase 28A - Deck Health / Recommendation Output Contract is blocked until Phase 27 outside validation is accepted.
```

## Current Outside Validation Packet

```text
docs/CHECKPOINT_PHASE27_WEIGHT_PROFILE_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE27_WEIGHT_PROFILE_PROMPT.md
```
