# Outside Validation Prompt - Phase 39B Cockatrice Interoperability Implementation Contract

You are validating Codie Phase 39B.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

## Required Verdict Context

Phase 39B is an implementation-contract-only packet. It must not implement
Cockatrice parser code, export packet builders, file writing, CLI behavior,
schema changes, repositories, provider calls, analytics, recommendations,
simulator execution, UI, LLM calls, workflow changes, validator changes,
dependency changes, active validation scope changes, or constitution changes.

Phase 39C remains blocked until Phase 39B outside validation returns PASS or
PASS WITH REVIEW NOTES.

## Required Review Files

Review:

```text
docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT.md
docs/CHECKPOINT_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE39A_COCKATRICE_INTEROPERABILITY_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_CODIE_MASTER_ARCHITECTURE.md
docs/CODIE_V2_CONSTITUTION.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CODIE_ACTIVE_VALIDATION_SCOPE.json
```

## Confirm Phase 39A Acceptance

Confirm the governance documents record Phase 39A as PASS WITH REVIEW NOTES
using:

```text
workflow run ID: 29969137239
validated SHA: bf1a966cbbf406820514ec1b2992688ed688bca1
artifact: codie-phase_ledger-validation-bf1a966cbbf406820514ec1b2992688ed688bca1
validation scope: phase_ledger
validator profile: all
deterministic: CLEAN_PASS
architecture: CLEAN_PASS
adversarial: FAIL with one INFORMATIONAL historical finding
aggregate: CLEAN_PASS
required corrections: none
```

The informational finding must remain nonblocking unless a concrete required
correction is introduced by this validation.

## Confirm Validation Tuple

Confirm Phase 39B explicitly declares:

```text
phase_id: Phase39B
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase39C
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Do not accept ambiguous next-phase scope.

## Confirm Future Implementation Boundary

Confirm Phase 39B limits future Phase 39C implementation to local,
fixture-first, in-memory Cockatrice interoperability models and validators.

These are future Phase 39C obligations, not Phase 39B completion criteria.
Do not fail Phase 39B because parser implementation, export implementation,
fixtures, or implementation tests do not exist yet. Fail Phase 39B only if the
contract authorizes that work too early, omits the required future boundary, or
leaves the future validation tuple ambiguous.

Future implementation may cover:

```text
Cockatrice .cod XML payload parsing
Cockatrice import packet models
Cockatrice export packet models
commander and partner commander handling
mainboard and sideboard handling
custom-zone preservation or unsupported-zone reporting
card-name preservation
already-supplied scryfall_id and oracle_id preservation
unresolved and unsupported card reporting
XML safety
privacy metadata rejection
deterministic serialization
dictionary round-trip behavior
fixture-first tests
```

Future implementation must remain file-writing-free unless a later safe-writer
contract authorizes writes.

## Required Rejection Conditions

Reject if Phase 39B:

```text
implements production Cockatrice parser code
implements production Cockatrice export code
adds implementation tests or fixtures
modifies codie production files
modifies tests
modifies schemas
modifies repositories
modifies providers
modifies analytics
modifies recommendation code
modifies simulator runtime
modifies UI or CLI behavior
modifies LLM behavior
modifies workflow or validator code
modifies dependencies
modifies active validation scope
modifies docs/CODIE_V1_CONSTITUTION.md
modifies docs/CODIE_V2_CONSTITUTION.md
authorizes live Cockatrice calls
authorizes live network calls
authorizes SQLite reads or writes
authorizes file writing
authorizes card identity lookup calls
authorizes recommendation generation
authorizes deck health output
authorizes treating Cockatrice user decks as tournament evidence by default
```

## Required Commands

From a clean checkout, run:

```text
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests -v
```

If the configured Python environment cannot launch, report the environment
blocker honestly and do not claim that environment passed.

## Static Scans

Run:

```text
git diff --name-only
git diff --name-only -- codie tests schemas scripts .github requirements.txt requirements-dev.txt
git diff --name-only -- docs/CODIE_ACTIVE_VALIDATION_SCOPE.json docs/CODIE_V1_CONSTITUTION.md docs/CODIE_V2_CONSTITUTION.md
rg -n "requests|httpx|sqlite3|codie\\.db|codie\\.providers|codie\\.analytics|codie\\.recommendations|codie\\.decision_intelligence|codie\\.evidence_fusion" docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
rg -n "recommend|should play|should cut|optimal|strict upgrade|deck health" docs/PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT.md docs/CHECKPOINT_PHASE39B_COCKATRICE_INTEROPERABILITY_IMPLEMENTATION_CONTRACT_REPORT.md
```

Matches inside explicit forbidden-boundary lists are allowed. Any production,
test, schema, workflow, validator, dependency, active-scope, or constitution
diff must be treated as a blocker unless explicitly authorized by a later
accepted contract.

## Required Output

Report:

```text
checkpoint document verdict
implementation contract verdict
outside validation prompt verdict
Phase 39A acceptance evidence status
Phase 39B validation tuple status
Phase 39C blocker status
required fixes, if any
review notes, if any
final decision
```
