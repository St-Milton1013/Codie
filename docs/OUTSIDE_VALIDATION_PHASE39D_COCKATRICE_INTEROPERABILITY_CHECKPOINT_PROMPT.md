# Outside Validation Prompt - Phase 39D Cockatrice Interoperability Checkpoint

Validate Phase 39D as a checkpoint-only packet.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 40A.

## Required Review Files

```text
docs/PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_PROMPT.md
docs/PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39C_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_PROMPT.md
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
codie/cockatrice/interoperability.py
codie/cockatrice/__init__.py
tests/test_cockatrice_interoperability.py
tests/fixtures/cockatrice/
docs/CODIE_V2_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Checks

Confirm:

```text
Phase 39D is checkpoint-only
Phase 39C is recorded as artifact-backed PASS
Phase 39C run ID, SHA, and artifact match
deterministic returned CLEAN_PASS
architecture returned CLEAN_PASS
adversarial returned CLEAN_PASS
aggregate returned CLEAN_PASS
there are no findings, skipped validators, or errors
Phase 39D declares phase_id, phase_part, and gate_scope
Phase 39D declares next_phase_id, next_phase_part, and next_gate_scope
active validation scope was not modified by the PR
Phase 40A remains blocked until Phase 39D outside validation passes
```

Confirm the accepted Cockatrice implementation remains:

```text
local and fixture-first
pure and in-memory
deterministic
supplied-payload-only
supplied-row-only for export packets
file-writing-free
provider-free
repository-free
database-free
analytics-free
recommendation-free
simulator-free
CLI-free
UI-free
LLM-free
live-network-free
```

Confirm visible preservation or rejection of:

```text
partner commander order
mainboard and sideboard separation
custom or unsupported zones
malformed XML
DTD and external entity declarations
unsupported formats
empty decks
unresolved card rows
duplicate card rows
private metadata
unknown, unavailable, unsupported, not-applicable, and zero states
not_tournament_evidence labeling
```

Reject Phase 39D if it adds:

```text
production or test behavior
fixtures
schema or repositories
providers or live network calls
Cockatrice runtime integration
file writing
CLI or UI behavior
analytics or metrics
recommendations or deck-health output
simulator runtime
LLM calls
dependencies
validator or workflow changes
active validation scope changes
constitution changes
```

## Required Commands

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Inspect changed paths and confirm the packet changes only:

```text
docs/PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_CONTRACT.md
docs/CHECKPOINT_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39D_COCKATRICE_INTEROPERABILITY_CHECKPOINT_PROMPT.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Final Gate

```text
Phase 39D must merge before its protected active-scope transition.
Phase 39D must receive artifact-backed phase-ledger PASS or PASS WITH REVIEW NOTES.
Phase 40A Relationship Intelligence Core Contract remains blocked until then.
```
