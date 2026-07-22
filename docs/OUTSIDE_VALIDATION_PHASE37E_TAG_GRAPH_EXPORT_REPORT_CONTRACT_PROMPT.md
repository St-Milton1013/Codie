# Outside Validation Prompt - Phase 37E Tag Graph Export / Report Contract

You are validating Phase 37E as a contract-only packet.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 38A.

## Review Files

Review:

```text
docs/PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT.md
docs/CHECKPOINT_PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT_PROMPT.md
docs/PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37D_TAG_GRAPH_METRIC_MODELS_IMPLEMENTATION_REPORT.md
docs/PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE37C_FREQUENCY_POOL_MODELS_IMPLEMENTATION_REPORT.md
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm:

```text
Phase 37E is contract-only
Phase 37E does not implement export/report code
Phase 37E does not add chart rendering
Phase 37E does not add UI or CLI work
Phase 37E does not add file writing
Phase 37E does not add schema or repository changes
Phase 37E does not add provider/source reads
Phase 37E does not add analytics or metric calculation
Phase 37E does not add recommendation output
Phase 37E does not add LLM calls
Phase 37E does not alter validators or workflows
Phase 37E does not modify the constitution
Phase 37E declares phase_id, phase_part, and gate_scope
Phase 37E declares next_phase_id, next_phase_part, and next_gate_scope
future export/report work consumes already-built TagGraphPacket objects
future exports preserve underlying numeric tables
future exports preserve underlying card lists
future exports preserve source provenance
future exports preserve caveats and coverage labels
future exports preserve user-local labels
future exports reject private/raw metadata
future exports reject strategic/action-advice language
roadmap/status/handoff docs agree on the Phase 37E gate
```

## Static Diff Checks

Run:

```powershell
git diff --name-only origin/main...HEAD
```

Confirm the Phase 37E commit changes only governance/contract documents unless
it is bundled with already validated Phase 37C/37D PR implementation changes.

Run:

```powershell
git diff --name-only -- .github scripts codie tests schemas requirements.txt requirements-dev.txt pyproject.toml
```

For a standalone Phase 37E contract commit, expected result is no matches. If
Phase 37E is bundled in the existing Phase 37C/37D PR branch, confirm all
non-document changes belong to the already validated Phase 37C/37D model
packets.

## Required Commands

Run:

```powershell
git diff --check
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe scripts/check_schema.py
C:\Users\Main\.venvs\codie-py312\Scripts\python.exe -m unittest discover -s tests -v
```

## Reject If

Reject if Phase 37E:

```text
implements export/report code
implements file writing
implements chart rendering
implements UI or CLI behavior
changes schema or repositories
reads providers or source tables
recalculates analytics or metrics
generates recommendations
uses LLM calls
changes validators or workflows
modifies docs/CODIE_V1_CONSTITUTION.md
hides underlying numeric tables
hides underlying card lists
hides caveats or source provenance
allows private/raw metadata export
allows strategic/action-advice language
leaves the validation tuple ambiguous
marks Phase 37E externally accepted before validation
starts Phase 38A before Phase 37E validation
```
