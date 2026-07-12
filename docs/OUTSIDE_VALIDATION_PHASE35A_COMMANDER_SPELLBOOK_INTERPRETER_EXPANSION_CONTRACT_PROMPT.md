# Outside Validation Prompt - Phase 35A Commander Spellbook Interpreter Expansion Contract

Validate Codie Phase 35A against:

```text
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
```

## Required Review Files

Review:

```text
docs/PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
docs/CHECKPOINT_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT_PROMPT.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_PROMPT.md
docs/PHASE7A_SPELLBOOK_COMBO_EVIDENCE_CONTRACT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/CODIE_V1_CONSTITUTION.md
codie/providers/spellbook/parser.py
codie/combos/sync.py
tests/test_provider_spellbook.py
tests/test_combo_sync.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Contract-Only Scope

Confirm Phase 35A adds only:

```text
contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 35A adds:

```text
production interpreter code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
dependency changes
file-writing behavior
live network behavior
simulator execution
UI behavior
LLM behavior
analytics behavior
recommendation behavior
```

## Confirm Future Implementation Surface

Confirm the contract limits future implementation to local, fixture-first
interpreter models such as:

```text
codie/combos/spellbook_interpreter.py
tests/test_spellbook_interpreter.py
tests/fixtures/spellbook_interpreter/spellbook_combo_outputs.json
tests/fixtures/spellbook_interpreter/spellbook_combo_restrictions.json
tests/fixtures/spellbook_interpreter/spellbook_combo_unknowns.json
optional codie/combos/__init__.py exports only
```

Reject if the contract authorizes persistence, live import, downloader,
repository, provider, analytics, charting, UI, LLM, recommendation, or simulator
runtime APIs.

## Confirm Interpreter Rules

Confirm the contract requires:

```text
Commander Spellbook remains combo authority
provider_combo_id remains visible
combo URL/source URL remains visible
component source refs remain visible
prerequisites are classified with explicit controlled values
outputs are classified with explicit controlled values
restrictions are classified with explicit controlled values
unknown outputs remain visible as manual-review items
unsupported requirements remain visible
infinite draw is classified without overclaiming automatic wins
infinite mana exposes compatible-sink inputs only
target compatibility does not run simulator logic
combo interpretation does not become tournament evidence
combo interpretation does not produce strategic claims
```

## Confirm Boundary Language

Confirm Phase 35A does not authorize:

```text
production interpreter code
live Commander Spellbook calls
Spellbook scraping
schema changes
repository changes
SQLite reads or writes
provider changes
file writing
analytics calculation
frequency pool calculation
Tag Graph Lab metrics
simulator execution
simulator target search integration
UI work
LLM calls
recommendation generation
dependency changes
```

Confirm future implementation is forbidden from:

```text
ranking combos
scoring combos
recommending combos
inferring deck intent
inferring pilot intent
treating combo interpretation as tournament evidence
treating simulator compatibility as tournament evidence
mutating raw Spellbook payloads
silently dropping unsupported requirements
silently converting unknown outputs to known outputs
generating play/cut/include language
```

## Required Commands

Run from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest discover -s tests
```

Run static scans:

```powershell
git diff --name-only HEAD~1..HEAD -- codie tests codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|analytics|recommendations|decision|evidence|openai|anthropic|google\.generativeai|langchain" docs\PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
rg -n "production interpreter code|live Commander Spellbook|Spellbook scraping|schema changes|repository changes|file writing|analytics calculation|frequency pool calculation|simulator execution|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE35A_COMMANDER_SPELLBOOK_INTERPRETER_EXPANSION_CONTRACT.md
```

Expected:

```text
No production/test/schema/repository/dependency drift.
Forbidden strings appear only in explicit forbidden-scope lists.
All tests pass.
```

## Return Verdict

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

If PASS or PASS WITH REVIEW NOTES, Phase 35B may begin implementation-contract
work.

Do not authorize schema/repository persistence, file writing, live network
calls, provider rewrite, Spellbook import implementation, UI, LLM calls,
analytics mutation, frequency-pool calculation, simulator runtime integration,
chart export, combo ranking, or recommendations from this Phase 35A packet.
