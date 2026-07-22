# Outside Validation Prompt - Phase 38B Moxfield Frequency Pool Builder Implementation Contract

Validate Phase 38B as an implementation-contract-only packet.

## Required Verdict Options

Return exactly one:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 38C.

## Review Packet

Review:

```text
docs/PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/CHECKPOINT_PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT_REPORT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PHASE37B_FREQUENCY_POOLS_TAG_GRAPH_LAB_IMPLEMENTATION_CONTRACT.md
docs/PHASE37E_TAG_GRAPH_EXPORT_REPORT_CONTRACT.md
codie/frequency_pools/models.py
codie/frequency_pools/__init__.py
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
Phase 38A acceptance evidence is recorded
Phase 38B is implementation-contract-only
Phase 38B validation tuple is explicit
next-phase validation tuple is explicit
active scope is Phase38B / outside-validation / INTERMEDIATE_PACKET
Phase 38C remains blocked
future files are limited and complete
future public interface is explicit
future tests are fixture-first
future URL inputs do not authorize live fetching
future manual text export parsing is authorized
deck presence frequency is the future default
total copy count is not the future default
basic lands are excluded by default
section inclusion and exclusion defaults are explicit
partial failures remain visible
duplicate inputs remain visible
unresolved cards remain visible
Moxfield user decks are not tournament evidence by default
future output may build FrequencyPoolPacket-compatible values
future output does not generate recommendations
Phase 38B does not add implementation code
roadmap/status/handoff files agree on the current gate
```

## Reject If

Reject if Phase 38B:

```text
implements production code
adds implementation tests
adds implementation fixtures
adds schema changes
adds repository changes
adds provider changes
adds live Moxfield calls
adds Scryfall lookup calls
calculates frequency pools
recalculates analytics
adds exports
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
changes docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
treats Moxfield user decks as tournament evidence by default
hides partial failures or unresolved cards
starts Phase 38C before Phase 38B acceptance
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
git diff --name-only HEAD~1..HEAD -- codie tests fixtures schemas scripts .github requirements.txt requirements-dev.txt docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

The second diff command should return no production, test, fixture, schema,
script, workflow, dependency, constitution, or active-scope changes.

## Final Response Template

```text
Verdict: PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Phase 38B contract: ...
Checkpoint: ...
Outside validation prompt: ...
Current gate: ...
Phase 38C: BLOCKED or UNBLOCKED

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

