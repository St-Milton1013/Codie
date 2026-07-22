# Outside Validation Prompt - Phase 38C Moxfield Frequency Pool Builder Implementation

Validate Phase 38C as a bounded implementation packet.

## Required Verdict Options

Return exactly one:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Only PASS or PASS WITH REVIEW NOTES may unblock Phase 38D.

## Review Packet

Review:

```text
docs/PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38C_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_PROMPT.md
docs/PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE38B_MOXFIELD_FREQUENCY_POOL_BUILDER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE38A_MOXFIELD_FREQUENCY_POOL_BUILDER_CONTRACT.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
codie/frequency_pools/moxfield_builder.py
codie/frequency_pools/models.py
codie/frequency_pools/__init__.py
tests/test_moxfield_frequency_pool_builder.py
tests/fixtures/moxfield_frequency_pools/
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
Phase 38B acceptance evidence is recorded
Phase 38C validation tuple is explicit
next-phase validation tuple is explicit
active scope is Phase38C / outside-validation / INTERMEDIATE_PACKET
Phase 38D remains blocked
implementation files match the Phase 38B authorization
public interface matches the Phase 38B contract
implementation is local and fixture-first
URL inputs are identifiers only and do not fetch
URL inputs without local payload fail visibly
local text export parsing works
default included/excluded sections are enforced
basic lands are excluded by default
override settings remain visible
deck presence frequency is the default
total copy count is visible but not the default frequency basis
duplicate cards within a deck do not inflate deck presence
duplicate deck inputs fail before contributing frequency
partial failures remain visible
unresolved cards and raw names remain visible
output builds FrequencyPoolPacket-compatible packets
user-local and not-tournament-evidence labels remain visible
serialization is deterministic
dictionary-compatible round-trip behavior is tested
input payloads are not mutated
private/raw metadata is rejected recursively
recommendation/action language is rejected
Brigid five-deck bucket shape is reproduced with synthetic fixture data
roadmap/status/handoff files agree on the current gate
```

## Reject If

Reject if Phase 38C:

```text
fetches Moxfield URLs
calls live Moxfield APIs
calls live Scryfall lookup
changes providers
changes schema
changes repositories
reads or writes SQLite
recalculates analytics
writes files
adds CLI behavior
adds UI behavior
calls LLMs
changes simulator runtime
generates recommendations
generates deck health output
treats user-local Moxfield decks as tournament evidence
hides partial failures
hides unresolved card rows
silently drops unknown sections
uses total copy count as default frequency basis
changes validators
changes workflows
changes dependencies
changes either constitution file
changes docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
starts Phase 38D before Phase 38C acceptance
```

## Required Local Commands

Rerun from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_moxfield_frequency_pool_builder -v
python -m unittest discover -s tests -v
```

Also inspect changed paths:

```powershell
git diff --name-only HEAD~1..HEAD
git diff --name-only HEAD~1..HEAD -- schemas codie/db codie/providers codie/analytics codie/recommendations codie/decision_intelligence codie/evidence_fusion scripts .github requirements.txt requirements-dev.txt docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

The second diff command should return no schema, repository, provider,
analytics, recommendation, Decision Intelligence, Evidence Fusion, script,
workflow, dependency, constitution, or active-scope changes.

## Final Response Template

```text
Verdict: PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Phase 38C implementation: ...
Checkpoint: ...
Outside validation prompt: ...
Current gate: ...
Phase 38D: BLOCKED or UNBLOCKED

Required fixes:
- ...

Review notes:
- ...

Validation:
- git diff --check: ...
- schema check: ...
- focused tests: ...
- full tests: ...

Final decision:
...
```

