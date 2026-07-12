# Outside Validation Prompt - Phase 34B Scryfall Tagger Ontology Implementation Contract

Validate Codie Phase 34B against:

```text
docs/PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT.md
docs/CODIE_V1_CONSTITUTION.md
```

## Required Review Files

Review:

```text
docs/PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT.md
docs/CHECKPOINT_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_PROMPT.md
docs/PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE33C_SCRYFALL_MIGRATION_MONITORING_IMPLEMENTATION_REPORT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/CODIE_V1_CONSTITUTION.md
codie/cards/scryfall_migration_monitoring.py
tests/test_scryfall_migration_monitoring.py
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Implementation-Contract-Only Scope

Confirm Phase 34B adds only:

```text
implementation contract
checkpoint report
outside validation prompt
roadmap/status/handoff updates
```

Reject if Phase 34B adds:

```text
production Scryfall Tagger ontology code
tests for implementation code
fixtures for implementation code
schema changes
repository changes
provider changes
dependency changes
file-writing behavior
live network behavior
UI behavior
LLM behavior
analytics behavior
frequency-pool behavior
recommendation behavior
```

## Confirm Future Implementation Surface

Confirm the contract limits future implementation to:

```text
codie/cards/scryfall_tagger_ontology.py
tests/test_scryfall_tagger_ontology.py
tests/fixtures/scryfall_tagger/tagger_functional_tags.json
tests/fixtures/scryfall_tagger/tagger_artwork_tags.json
tests/fixtures/scryfall_tagger/tagger_unknown_namespace.json
tests/fixtures/scryfall_tagger/tagger_duplicate_tags.json
tests/fixtures/scryfall_tagger/tagger_aliases_deprecated_conflicts.json
optional codie/cards/__init__.py exports only
```

Reject if the contract authorizes persistence, live import, downloader,
repository, provider, analytics, charting, UI, LLM, recommendation, or
frequency-pool APIs.

## Confirm Review Note Coverage

Confirm Phase 34B explicitly includes future handling for:

```text
tag aliases
deprecated tags
replacement tags
replacement chains
conflicting namespace assignments
conflicting functional/excluded classification
manual correction conflicts
cyclic replacement chains
```

Reject if alias/deprecated-tag/conflict/replacement-chain handling is omitted
from the future implementation contract.

## Confirm Boundary Language

Confirm Phase 34B does not authorize:

```text
Scryfall Tagger ontology implementation
live Scryfall Tagger calls
Tagger scraping
schema changes
repository changes
SQLite reads or writes
provider changes
file writing
card lookup replacement
Scryfall card-truth override
canonicalization changes
analytics calculation
frequency pool calculation
Tag Graph Lab metrics
chart export
UI work
LLM calls
recommendation generation
dependency changes
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
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|analytics|recommendations|decision|evidence|openai|anthropic|google\.generativeai|langchain" docs\PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
rg -n "Scryfall Tagger ontology implementation|live Scryfall Tagger|Tagger scraping|schema changes|repository changes|file writing|analytics calculation|frequency pool calculation|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" docs\PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
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

If PASS or PASS WITH REVIEW NOTES, Phase 34C may begin implementation work.

Do not authorize schema/repository persistence, file writing, live network
calls, provider rewrite, Tagger import implementation, UI, LLM calls, analytics
mutation, frequency-pool calculation, chart export, or recommendations from
this Phase 34B packet.
