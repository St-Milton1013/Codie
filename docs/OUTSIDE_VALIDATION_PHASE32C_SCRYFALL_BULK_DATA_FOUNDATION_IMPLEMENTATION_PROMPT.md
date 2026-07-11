# Outside Validation Prompt - Phase 32C Scryfall Bulk Data Foundation Implementation

Validate Codie Phase 32C against:

```text
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CODIE_V1_CONSTITUTION.md
```

## Required Review Files

Review:

```text
docs/PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_PROMPT.md
docs/PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT.md
docs/CHECKPOINT_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_REPORT.md
docs/OUTSIDE_VALIDATION_PHASE32B_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_CONTRACT_PROMPT.md
docs/PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT.md
docs/CHECKPOINT_PHASE32A_SCRYFALL_BULK_DATA_FOUNDATION_CONTRACT_REPORT.md
docs/POST_PHASE31_DEFERRED_IMPLEMENTATION_PRIORITY_PLAN.md
docs/POST_PHASE31_PATCH_PLAN_CEMENTING_AUDIT.md
docs/PHASE2_SCRYFALL_TRUTH_CONTRACT.md
codie/cards/scryfall_bulk_snapshots.py
codie/cards/__init__.py
tests/test_scryfall_bulk_snapshots.py
tests/fixtures/scryfall/bulk_manifest.json
tests/fixtures/scryfall/default_cards_snapshot.json
tests/fixtures/scryfall/malformed_bulk_snapshot.json
docs/ACTIVE_ROADMAP_INDEX.md
docs/VALIDATION_STATUS_INDEX.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

## Confirm Implementation Scope

Confirm Phase 32C adds only local, fixture-first Scryfall bulk snapshot manifest
models, fixture loading, deterministic serialization, and validation helpers.

Reject if Phase 32C adds:

```text
live Scryfall API calls
bulk download implementation
background refresh jobs
schema changes
repository changes
SQLite reads or writes
provider rewrite
card lookup replacement
canonicalization changes
analytics changes
migration monitoring implementation
Scryfall Tagger import
UI work
LLM calls
recommendation generation
```

## Confirm Public Interface

Confirm the public interface is limited to:

```text
SCRYFALL_BULK_SNAPSHOT_VERSION
ScryfallBulkSnapshotError
ScryfallBulkFileRef
ScryfallBulkSnapshotManifest
ScryfallBulkSnapshotValidationReport
build_scryfall_bulk_snapshot_manifest(...)
validate_scryfall_bulk_snapshot_manifest(...)
scryfall_bulk_snapshot_manifest_to_dict(...)
load_scryfall_bulk_snapshot_fixture(...)
```

`calculate_scryfall_bulk_snapshot_hash(...)` should not be required as public API
for Phase 32C because Phase 32B did not authorize it. Stable content hashing
must still be visible through manifest `content_hash`.

## Confirm Behavior

Confirm:

```text
manifest serializes deterministically
manifest round-trips through dictionary-compatible form
manifest models are frozen value objects
builder does not mutate input metadata
content hash is stable
card count is recorded
bulk data type remains visible
source URI remains visible when provided
generated_at remains visible when provided
imported_at remains visible when provided
raw metadata remains visible
fixture loading is local-only
valid fixture creates a validation report
malformed JSON fails cleanly
missing Scryfall id fails cleanly
missing card name fails cleanly
optional fields may be missing
oracle_id is preserved when available
released_at is preserved when available
legalities are preserved when available
card_faces are preserved when available
produced_mana is preserved when available
raw card payloads are preserved
hash/count mismatches remain visible in validation errors
```

## Confirm Phase 2 Identity Rules

Confirm Phase 32C does not rewrite or invalidate:

```text
codie/cards/normalization.py
codie/cards/importer.py
codie/cards/lookup.py
codie/providers/scryfall/models.py
codie/providers/scryfall/bulk.py
tests/test_scryfall_truth.py
```

Confirm:

```text
scryfall_id remains enforced card identity
oracle_id remains analytics grouping identity
raw Scryfall JSON remains preserved
Scryfall remains the card truth source
```

## Required Commands

Run from a clean checkout:

```powershell
git diff --check
python scripts/check_schema.py
python -m unittest tests.test_scryfall_bulk_snapshots -v
python -m unittest discover -s tests
```

Run static scans:

```powershell
git diff --name-only HEAD~1..HEAD -- codie\db\schema codie\db\repositories docs\SCHEMA_SPEC.md requirements.txt requirements-dev.txt pyproject.toml
rg -n "requests|httpx|sqlite3|codie\.db|repositories|providers|analytics|recommendations|decision|evidence|openai|anthropic|google\.generativeai|langchain" codie\cards\scryfall_bulk_snapshots.py tests\test_scryfall_bulk_snapshots.py
rg -n "bulk download|live Scryfall API|provider rewrite|lookup replacement|Tagger import|migration monitoring implementation|recommendation generation|should play|must include|strict upgrade|auto-include|recommended cut|recommended include" codie\cards\scryfall_bulk_snapshots.py tests\test_scryfall_bulk_snapshots.py docs\PHASE32C_SCRYFALL_BULK_DATA_FOUNDATION_IMPLEMENTATION_REPORT.md
```

Expected:

```text
No schema/repository/dependency drift.
No forbidden production imports.
Forbidden words appear only in explicit boundary/rejection lists.
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

If PASS or PASS WITH REVIEW NOTES, Phase 33A may begin contract-first.

Do not authorize Scryfall migration monitoring implementation, Scryfall Tagger
import, provider rewrite, lookup replacement, schema/repository persistence,
UI, LLM calls, live network calls, analytics mutation, or recommendations from
this Phase 32C packet.
