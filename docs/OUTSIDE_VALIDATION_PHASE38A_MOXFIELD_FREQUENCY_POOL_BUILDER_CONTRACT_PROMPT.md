# Outside Validation Prompt - Phase 38A Moxfield Frequency Pool Builder Contract

Validate Phase 38A as a contract-only packet.

## Required Verdict Options

Return exactly one:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 38B.

## Review Packet

Review:

```text
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/CHECKPOINT_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_PROMPT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT.md
docs/CHECKPOINT_PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT_REPORT.md
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Required Checks

Confirm:

```text
Phase 38A is contract-only
Phase 38A validation tuple is explicit
next-phase validation tuple is explicit
active scope is Phase38A / outside-validation / INTERMEDIATE_PACKET
Phase 37 final PASS evidence is recorded
Phase 38B remains blocked
future Moxfield URL support is contract-gated
future manual text export support is preserved
future live Moxfield access is provider-contract-gated
future tests are fixture-first
deck presence frequency is the future default
total copy count is not the future default
partial failures remain visible
duplicate deck inputs remain visible
unresolved cards remain visible
unknown/unavailable/unsupported/not applicable/zero remain distinct
Scryfall identity semantics remain unchanged
private deck text remains local by default
Moxfield user decks are not tournament evidence by default
frequency pools do not generate recommendations
Phase 38A does not authorize implementation code
roadmap/status/handoff files agree on the current gate
```

## Reject If

Reject if Phase 38A:

```text
implements production Moxfield parser code
implements production Moxfield provider code
adds live Moxfield network calls
adds tests or fixtures for implementation code
adds schema changes
adds repository changes
adds SQLite reads or writes
reads source tables
reads raw provider payloads
calculates frequency pools
recalculates analytics
adds Tag Graph metrics
adds export code
writes files
adds CLI behavior
adds UI behavior
calls LLMs
changes simulator runtime
generates recommendations
generates deck health output
changes dependencies
changes validators
changes workflows
changes either constitution file
treats Moxfield user decks as tournament evidence by default
hides partial failures or unresolved cards
collapses unknown/unavailable/unsupported/not applicable into zero or false
starts Phase 38B before Phase 38A acceptance
```

## Required Local Commands

Rerun from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

Also inspect changed paths:

```powershell
git diff --name-only HEAD~1..HEAD
git diff --name-only HEAD~1..HEAD -- codie tests fixtures schemas scripts .github requirements.txt requirements-dev.txt docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md
```

The second diff command should return no production, test, fixture, schema,
script, workflow, dependency, or constitution changes.

## Expected Finding Treatment

Blocking findings:

```text
BLOCKER
CRITICAL
HIGH
```

Nonblocking review notes:

```text
MEDIUM
LOW
INFORMATIONAL
```

For this INTERMEDIATE_PACKET gate, MEDIUM/LOW/INFORMATIONAL findings may remain
review notes unless the finding includes a concrete required correction or
contradicts the contract.

## Final Response Template

```text
Verdict: PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Phase 38A contract: ...
Checkpoint: ...
Outside validation prompt: ...
Current gate: ...
Phase 38B: BLOCKED or UNBLOCKED

Required fixes:
- ...

Review notes:
- ...

Validation:
- git diff --check: ...
- schema check: ...
- full tests: ...

Final decision:
...
```

