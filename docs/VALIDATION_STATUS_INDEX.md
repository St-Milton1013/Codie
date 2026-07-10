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
Phase 28C Deck Health / Recommendation Output Checkpoint: COMPLETE
Phase 28 Deck Health / Recommendation Output: PASS
Phase 29A CLI / Report Integration Contract: COMPLETE
Phase 29A outside review: PASS WITH REQUIRED FIXES; fixes applied
Phase 29B Report Document Implementation: INTERNAL PASS
Phase 29C CLI / Safe File Writer Integration Contract: COMPLETE
Phase 29D Safe Recommendation Report File Writer: INTERNAL PASS
Phase 29E Recommendation Output CLI Wrapper: PASS WITH REVIEW NOTES
Phase 29F CLI / Report Integration Checkpoint: PASS
Phase 30A Local Alpha Release Checklist: PASS
Phase 30B Local Alpha Packaging / Usage Documentation: PASS
Phase 30C: next allowed phase
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
Phase 28B Deck Health / Recommendation Output Packet Implementation: INTERNAL PASS
Phase 28 Deck Health / Recommendation Output: PASS
Phase 29A CLI / Report Integration Contract: PASS WITH REQUIRED FIXES APPLIED
Phase 29B Report Document Implementation: INTERNAL PASS
Phase 29C CLI / Safe File Writer Integration Contract: COMPLETE; REQUIRED FIXES APPLIED
Phase 29D Safe Recommendation Report File Writer: INTERNAL PASS
Phase 29E Recommendation Output CLI Wrapper: PASS WITH REVIEW NOTES
Phase 29F CLI / Report Integration Checkpoint: PASS
Phase 30A Local Alpha Release Checklist: PASS
Phase 30B Local Alpha Packaging / Usage Documentation: PASS
```

## Latest Local Validation

```text
Phase 30B Local Alpha Packaging / Usage Documentation:
python scripts/check_schema.py
Schema bootstrap check passed.

Full suite:
python -m unittest discover -s tests
Ran 797 tests in 4.819s
OK (skipped=1)

Static check:
git diff --check
passed

Outside validation:
Phase 30B returned PASS

Production touch check:
no codie/tests/scripts/ui/schema/dependency/CI changes
```

## Current Blocker

```text
Phase 30C - Local Alpha release candidate checkpoint is the next allowed phase.
```

## Current Phase 30C Preparation Packet

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
```
