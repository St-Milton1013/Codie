# Outside Validation Prompt - Phase 35C Commander Spellbook Interpreter Implementation

Validate Codie Phase 35C against `docs/CODIE_V1_CONSTITUTION.md`, the Phase
35A/35B contracts, and the implementation checkpoint.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

## Review Files

```text
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_PROMPT.md
docs/PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35B_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/PHASE7A_SPELLBOOK_COMBO_EVIDENCE_CONTRACT.md
docs/CODIE_V1_CONSTITUTION.md
codie/combos/spellbook_interpreter.py
codie/combos/__init__.py
tests/test_spellbook_interpreter.py
tests/fixtures/spellbook_interpreter/spellbook_combo_outputs.json
tests/fixtures/spellbook_interpreter/spellbook_combo_restrictions.json
tests/fixtures/spellbook_interpreter/spellbook_combo_unknowns.json
codie/providers/spellbook/parser.py
codie/combos/sync.py
tests/test_provider_spellbook.py
tests/test_combo_sync.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm Phase 35C:

```text
implements only local Spellbook interpreter models and validators
uses local fixtures only
does not import codie.providers or codie.providers.spellbook
does not call live Commander Spellbook
does not scrape Spellbook
does not change schema
does not change repositories
does not read or write SQLite
does not calculate analytics
does not calculate frequency pools
does not add charting or Tag Graph Lab metrics
does not execute simulator logic
does not integrate simulator target search
does not call LLMs
does not add UI behavior
does not add file-writing behavior
does not rank, score, or recommend combos
does not infer deck intent or pilot intent
does not treat combo interpretation as tournament evidence
does not mutate raw Spellbook payloads
does not silently drop unsupported requirements
does not silently convert unknown outputs to known outputs
```

Confirm implementation behavior:

```text
provider_combo_id remains visible
combo_url remains visible
combo_name remains visible
variant_ids remain visible and deterministic
component refs remain visible
component roles remain visible
source refs remain visible
raw payload provenance is referenced only by source ref/hash
output classes use controlled values
prerequisite classes use controlled values
restriction classes use controlled values
target compatibility is metadata-only
unknown outputs create manual-review records
unknown prerequisites create manual-review records
unknown restrictions create manual-review records
unsupported items remain visible
manual-review and unsupported item hiding requires explicit options
serialization is deterministic
dictionary round-trip works
input payloads are not mutated
malformed payload failures are clean
recommendation language is rejected
```

## Commands To Run From Clean Checkout

```powershell
python -m unittest tests.test_spellbook_interpreter -v
python scripts/check_schema.py
python -m unittest discover -s tests
git diff --check
```

## Static Scans

```powershell
rg -n "codie\.db|sqlite3|codie\.providers|codie\.ingestion|codie\.analytics|codie\.recommendations|codie\.evidence_fusion|codie\.decision_intelligence|requests|httpx|openai|anthropic|google\.generativeai|langchain|flask|fastapi|uvicorn|starlette" codie\combos\spellbook_interpreter.py tests\test_spellbook_interpreter.py
```

Expected:

```text
no production matches
test matches only forbidden-import assertion strings
```

```powershell
git diff --name-only -- codie\db codie\providers codie\analytics codie\recommendations codie\probability_engine codie\cards docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt .github
```

Expected:

```text
no matches
```

```powershell
rg -n "should include|should cut|must include|must cut|strict upgrade|auto-include|recommended include|recommended cut|secretly optimal|breaks the format|score combos|rank combos|recommend combos" codie\combos\spellbook_interpreter.py tests\test_spellbook_interpreter.py tests\fixtures\spellbook_interpreter
```

Expected:

```text
production matches only blocked phrase constants or explicit boundary comments
test matches only rejection coverage
```

## Reject If

Reject if Phase 35C imports provider code, performs live network work, adds
schema/repository/provider changes, executes simulator logic, calculates
analytics/frequency pools, ranks/scores/recommends combos, hides unknown or
unsupported interpretation by default, mutates raw Spellbook payloads, or
generates play/cut/include language.

## Final Gate

No later phase may begin until Phase 35C outside validation returns PASS or PASS
WITH REVIEW NOTES.
