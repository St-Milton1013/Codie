# Outside Validation Prompt - Phase 37A Frequency Pools / Tag Graph Lab Contract

Validate Codie Phase 37A against `docs/CODIE_V1_CONSTITUTION.md`, the
post-31 deferred implementation plan, accepted Phase 34/35/36 packets, and the
Phase 37A checkpoint.

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

## Review Files

```text
docs/PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT.md
docs/CHECKPOINT_PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE37A_FREQUENCY_POOLS_TAG_GRAPH_LAB_CONTRACT_PROMPT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md
docs/PATCH_EVIDENCE_INTELLIGENCE_AND_LOCAL_REPORTS.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE35C_COMMANDER_SPELLBOOK_INTERPRETER_IMPLEMENTATION_REPORT.md
docs/PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE36C_IMMUTABLE_DECK_SNAPSHOT_IMPLEMENTATION_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Required Checks

Confirm Phase 37A:

```text
is contract-only
adds no production frequency pool code
adds no production tag graph code
adds no implementation tests or fixtures
adds no schema changes
adds no repository changes
adds no provider changes
adds no SQLite reads or writes
adds no live network calls
adds no file writing
adds no CLI work
adds no UI work
adds no analytics calculation
adds no frequency pool calculation
adds no Tag Graph Lab metrics
adds no simulator execution
adds no LLM calls
adds no recommendation generation
adds no dependency changes
```

Confirm future boundary rules:

```text
future metrics must use canonical card identities
future tags must map to oracle_id
Scryfall IDs remain visible where card-print provenance matters
tag source provenance must remain visible
low sample labels are required
low tag coverage labels are required
coverage_ratio remains visible
matching_deck_count remains visible
available_deck_count remains visible
user decks never enter commander averages
user-local snapshot scopes must be labeled user-local
frequency pools must not generate recommendations
tag graphs must not generate strategic claims
LLMs may not create tag metrics
simulator output remains simulator evidence only
```

Confirm forbidden future direct inputs:

```text
raw provider payloads
raw imported user deck text
private notes
primer body text
source/provider tables directly
live provider APIs
live Scryfall Tagger calls
live Moxfield calls
live Spellbook calls
LLM-generated tags or metrics
simulator traces as tournament evidence
recommendation outputs as metric inputs
```

## Commands To Run From Clean Checkout

Because Phase 37A is documentation-only, run:

```powershell
git diff --check
```

If a Python runtime is available, also run:

```powershell
python scripts/check_schema.py
python -m unittest discover -s tests
```

If the configured Windows venv cannot launch, report that environment blocker
and rerun with a clearly identified alternative Python runtime.

## Static Scans

```powershell
git diff --name-only -- codie tests scripts ui codie\db codie\providers codie\analytics codie\recommendations codie\probability_engine codie\cards docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt .github
```

Expected:

```text
no matches
```

```powershell
rg -n "Phase 36C Immutable Deck Snapshot Implementation: INTERNAL PASS|Phase 36C outside validation|send Phase 36C outside validation|Later work is blocked until Phase 36C" docs\ACTIVE_ROADMAP_INDEX.md docs\VALIDATION_STATUS_INDEX.md docs\NEXT_PHASE_CONTRACT.md docs\CODEX_CONTINUITY_HANDOFF.md
```

Expected:

```text
no matches
```

## Reject If

Reject if Phase 37A implements frequency pools, Tag Graph Lab metrics, exports,
schema, repositories, provider calls, file writing, CLI, UI, analytics
calculation, simulator execution, LLM calls, recommendation generation, or
weakens the Phase 36C privacy boundary for user deck snapshots.

## Final Gate

No Phase 37B work may begin until Phase 37A outside validation returns PASS or
PASS WITH REVIEW NOTES.
