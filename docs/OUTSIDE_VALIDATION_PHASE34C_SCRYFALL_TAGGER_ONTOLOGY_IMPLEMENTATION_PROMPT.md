# Outside Validation Prompt - Phase 34C Scryfall Tagger Ontology Implementation

Validate Codie Phase 34C against:

```text
docs/PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
```

## Required Review Files

Review:

```text
docs/PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE34C_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_PROMPT.md
docs/PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE34B_SCRYFALL_TAGGER_ONTOLOGY_IMPLEMENTATION_CONTRACT_REPORT.md
docs/PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT.md
docs/CHECKPOINT_PHASE34A_SCRYFALL_TAGGER_FUNCTIONAL_ONTOLOGY_CONTRACT_REPORT.md
docs/ROADMAP_PATCH_TAG_GRAPH_LAB.md
docs/CODIE_V1_CONSTITUTION.md
codie/cards/scryfall_tagger_ontology.py
codie/cards/__init__.py
tests/test_scryfall_tagger_ontology.py
tests/fixtures/scryfall_tagger/tagger_functional_tags.json
tests/fixtures/scryfall_tagger/tagger_artwork_tags.json
tests/fixtures/scryfall_tagger/tagger_unknown_namespace.json
tests/fixtures/scryfall_tagger/tagger_duplicate_tags.json
tests/fixtures/scryfall_tagger/tagger_aliases_deprecated_conflicts.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Implementation Scope

Confirm Phase 34C implements only:

```text
local Scryfall Tagger ontology models
local fixture-based ontology builders
deterministic serialization
coverage report helpers
validation helpers
fixture-based tests
export-only updates to codie/cards/__init__.py
```

Reject if Phase 34C adds:

```text
schema changes
repository changes
SQLite reads or writes
provider changes
live Scryfall Tagger calls
Tagger scraping
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

## Confirm Required Behavior

Confirm tests and implementation prove:

```text
functional tags map to oracle_id
scryfall_id remains visible as provenance when present
artwork/cosmetic tags are excluded by default
functional namespaces are preserved
unknown namespaces are reported
duplicate tags are deduplicated deterministically
source provenance remains visible
confidence values remain visible and bounded
manual corrections annotate without rewriting source tags
aliases preserve original tags and normalize deterministically
deprecated tags remain visible
replacement chains remain visible
cyclic replacement chains fail cleanly
tag conflicts remain visible and do not silently choose a winner
coverage ratio is calculated deterministically
low coverage creates visible warnings
raw source payloads are not mutated
malformed fixtures fail cleanly
no live network calls occur in tests
no SQLite access occurs
no recommendation language appears in production code
```

## Required Commands

Run from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_scryfall_tagger_ontology -v
python -m unittest discover -s tests
```

Run static scans:

```powershell
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|openai|anthropic|google\.generativeai|langchain" codie\cards\scryfall_tagger_ontology.py tests\test_scryfall_tagger_ontology.py
rg -n "open\(|write_text\(|write_bytes\(|mkdir\(|touch\(|unlink\(" codie\cards\scryfall_tagger_ontology.py
rg -n "live Scryfall Tagger|Tagger scraping|card lookup replacement|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" codie\cards\scryfall_tagger_ontology.py tests\test_scryfall_tagger_ontology.py
```

Expected:

```text
No schema/repository/dependency drift.
No forbidden production imports.
No production file-writing behavior.
All focused and full tests pass.
```

## Return Verdict

Return one of:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

If PASS or PASS WITH REVIEW NOTES, Phase 35A may begin contract-first.

Do not authorize schema/repository persistence, file writing, live network
calls, provider rewrite, Tagger scraping, UI, LLM calls, analytics mutation,
frequency-pool calculation, chart export, or recommendations from this Phase
34C packet.
