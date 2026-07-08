# Outside Validation Prompt - Phase 25 Evidence Fusion

Validate Codie Phase 25 work against `CODIE_V1_CONSTITUTION.md` and Codie
Architecture Revision III.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 26.

## Files To Review

Documentation:

```text
docs/PHASE25A_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_CONTRACT.md
docs/PHASE25A_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_CONTRACT_REPORT.md
docs/PHASE25B_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE25_EVIDENCE_FUSION_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
docs/ROADMAP_PATCH_CODIE_ARCHITECTURE_REVISION_III.md
docs/POST_PHASE24_PATCH_CONTRACT_BACKLOG.md
```

Implementation:

```text
codie/evidence_fusion/__init__.py
codie/evidence_fusion/models.py
codie/evidence_fusion/builders.py
tests/test_evidence_fusion_models.py
```

Related context:

```text
codie/intelligence/evidence_inputs.py
codie/intelligence/evidence_graph.py
codie/intelligence/source_conflicts.py
codie/intelligence/unsupported_cards.py
codie/intelligence/query_planner.py
```

## Validation Tasks

Confirm:

```text
Phase 24 outside validation is treated as accepted input.
Phase 25A contract matches the implementation.
Phase 25B implements the declared public interface.
The implementation is pure and in-memory.
The implementation adds no schema.
The implementation adds no repositories.
The implementation reads no SQLite data.
The implementation reads no provider/source payloads.
The implementation recalculates no analytics.
The implementation generates no recommendations.
The implementation scores no recommendations.
The implementation calls no LLMs.
The implementation imports no LLM SDKs.
The implementation executes no simulator logic.
The implementation generates no Jin-Gitaxias theory answers.
The implementation writes no files.
Authority refs remain visible.
Observation refs remain visible.
Metric refs preserve sample size and coverage ratio.
Primer context refs remain explanatory only.
Simulator refs disclose unsupported-card counts.
Caveats remain visible.
Conflicts remain visible.
Source agreement remains visible.
Evidence level guardrails are enforced.
Speculation level remains visible.
Private metadata keys are rejected, including nested keys.
Strategic recommendation language is rejected.
Serialization is deterministic.
```

Confirm these public objects exist:

```text
EvidenceFusionBuildError
EvidenceAuthorityRef
EvidenceObservationRef
EvidenceMetricRef
EvidencePrimerContextRef
EvidenceSimulatorRef
EvidenceCaveat
EvidenceConflict
EvidenceSourceAgreement
UnifiedEvidenceSubject
UnifiedEvidenceObject
UnifiedEvidenceBundle
EvidenceFusionOptions
build_unified_evidence_object(...)
build_unified_evidence_bundle(...)
unified_evidence_object_to_dict(...)
unified_evidence_bundle_to_dict(...)
validate_unified_evidence_bundle(...)
```

Confirm schema discipline:

```text
Phase 25 adds no schema changes.
No tables, columns, indexes, migrations, or repository methods were added for Evidence Fusion packets.
Evidence Fusion packets remain in-memory only.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 724 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_evidence_fusion_models -v
```

Confirm:

```text
Ran 17 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic|flask|fastapi|uvicorn|starlette" codie\evidence_fusion tests\test_evidence_fusion_models.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\evidence_fusion tests\test_evidence_fusion_models.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\evidence_fusion
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\evidence_fusion tests\test_evidence_fusion_models.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\evidence_fusion
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\evidence_fusion tests\test_evidence_fusion_models.py docs\PHASE25B_EVIDENCE_FUSION_UNIFIED_EVIDENCE_OBJECTS_IMPLEMENTATION_REPORT.md docs\CHECKPOINT_PHASE25_EVIDENCE_FUSION_REPORT.md
```

Expected:

```text
no matches
```

Run:

```powershell
git diff --name-only -- codie\db\schema docs\SCHEMA_SPEC.md codie\db\repositories
```

Expected:

```text
no Phase 25 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
codie/evidence_fusion imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, sqlite3, openai, anthropic, Flask, FastAPI, Uvicorn, or Starlette
codie/evidence_fusion reads source/provider tables or payloads
codie/evidence_fusion writes files
codie/evidence_fusion calls LLMs
codie/evidence_fusion imports LLM SDKs
codie/evidence_fusion queries SQLite
codie/evidence_fusion recalculates analytics
codie/evidence_fusion runs simulator logic
codie/evidence_fusion implements card behavior
codie/evidence_fusion generates recommendation output
codie/evidence_fusion generates Jin-Gitaxias theory output
codie/evidence_fusion persists evidence objects
private metadata can escape into output
primer context overrides authority or measured evidence
simulator refs are treated as tournament evidence
conflicts are resolved instead of preserved
caveats can be hidden
speculation level can be hidden
high evidence can be emitted without metric refs
```

## Phase 26 Gate

Phase 26 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
