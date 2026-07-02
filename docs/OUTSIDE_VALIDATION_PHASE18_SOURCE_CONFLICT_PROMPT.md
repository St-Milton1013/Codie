# Outside Validation Prompt - Phase 18 Source Conflict Report

Use this prompt with an outside reviewer before Phase 19 begins.

```text
Validate Codie Phase 18 Source Conflict Report work against CODIE_V1_CONSTITUTION.md.

Important:
- This is an outside validation request.
- Do not rely only on checkpoint prose.
- Inspect implementation files, tests, docs, and dependency boundaries.
- Run tests from a clean checkout if possible.

Return:
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 19.

Files to review:

Core contracts and reports:
- docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_CONTRACT.md
- docs/PHASE18_SOURCE_CONFLICT_REPORT_PLANNING_REPORT.md
- docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT.md
- docs/PHASE18A_SOURCE_CONFLICT_REPORT_CONTRACT_REPORT.md
- docs/PHASE18B_SOURCE_CONFLICT_REPORT_IMPLEMENTATION_REPORT.md
- docs/CHECKPOINT_PHASE18_SOURCE_CONFLICT_REPORT.md

Related Phase 17 input assembly references:
- docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
- docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
- codie/intelligence/evidence_inputs.py
- tests/test_intelligence_evidence_inputs.py

Implementation files:
- codie/intelligence/__init__.py
- codie/intelligence/source_conflicts.py

Tests:
- tests/test_intelligence_source_conflicts.py

Architecture references:
- docs/CODIE_V1_CONSTITUTION.md
- docs/DEPENDENCY_RULES.md
- docs/NEXT_PHASE_CONTRACT.md
- docs/CODEX_CONTINUITY_HANDOFF.md

Check:

1. Phase 18 planning discipline
- Confirm Phase 18 starts with source conflict reports, not chat UI.
- Confirm Phase 18 adds no LLM calls.
- Confirm Phase 18 adds no evidence graph persistence.
- Confirm Phase 18 adds no provider calls.
- Confirm Phase 18 adds no source/provider table reads.
- Confirm Phase 18 adds no simulator execution.
- Confirm Phase 18 adds no analytics calculation.
- Confirm Phase 18 adds no recommendation generation.
- Confirm Phase 18 adds no private raw_input export.

2. Schema discipline
- Confirm Phase 18 adds no schema changes.
- Confirm no tables, columns, indexes, migrations, or repository methods were added for source conflict reports.
- Confirm source conflict reports remain in-memory only.
- Confirm schema and repository files did not drift during Phase 18 unless explicitly documented as nonfunctional.

3. Public interface
- Confirm these public objects exist:
  SourceConflictBuildError
  SourceConflictEvidenceRef
  SourceConflictItem
  SourceConflictReport
  SourceConflictReportOptions
  build_source_conflict_report(...)
  source_conflict_report_to_input_records(...)
  source_conflict_report_to_dict(...)

4. Report validation behavior
- Confirm report_id is required.
- Confirm subject_id is required.
- Confirm conflicts are required.
- Confirm conflict IDs must be unique.
- Confirm conflict_type must be supported.
- Confirm severity must be supported.
- Confirm resolution_status must be supported.
- Confirm conflicts require at least one evidence_ref.
- Confirm evidence refs require source_name.
- Confirm evidence refs require observed_at.
- Confirm evidence refs require source_record_id or source_url.
- Confirm field_value must be JSON-compatible.
- Confirm metadata must be JSON-compatible.
- Confirm filtered reports with no remaining conflicts fail cleanly.
- Confirm forbidden strategic language fails cleanly.

5. Conversion behavior
- Confirm source_conflict_report_to_input_records(...) emits EvidenceInputRecord values.
- Confirm emitted records use record_type source_conflict.
- Confirm conflict type is preserved in metadata.
- Confirm severity is preserved in metadata.
- Confirm resolution status is preserved in metadata.
- Confirm references map to EvidenceRecordRef values.
- Confirm blocking conflicts are preserved.
- Confirm source conflict report conversion does not choose a winner source.
- Confirm source conflict report conversion does not canonicalize records.
- Confirm source conflict report conversion does not create recommendation candidates.

6. Filtering behavior
- Confirm resolved_externally and ignored_by_policy conflicts are excluded by default.
- Confirm resolved conflicts are included only with explicit option.
- Confirm sensitive evidence refs are excluded by default.
- Confirm sensitive evidence refs are included only with explicit option.
- Confirm filtered evidence creates caveats or counts.
- Confirm minimum_severity filters lower-severity conflicts.
- Confirm blocking conflicts remain visible.

7. Privacy
- Confirm raw_input metadata is rejected by default.
- Confirm private deck text metadata is rejected by default.
- Confirm full primer body metadata is rejected by default.
- Confirm raw provider payload metadata is rejected by default.
- Confirm tests reject private metadata keys such as:
  raw_input
  private_deck_text
  full_primer_body
  raw_provider_payload
  provider_payload
  original_import_text
- Confirm nested appearances of private metadata keys are rejected.
- Confirm private raw text is not emitted in serialized reports or EvidenceInputRecord metadata.

8. Architecture boundaries
Reject if Phase 18 code imports any of:
- codie.db
- codie.providers
- codie.analytics
- codie.recommendations.generation
- codie.recommendations.persistence
- codie.ingestion
- codie.cards
- codie.probability_engine
- codie.canonical
- requests
- httpx
- sqlite3

Confirm no raw SQL is present in:
- codie/intelligence/source_conflicts.py
- tests/test_intelligence_source_conflicts.py

Confirm no production file-writing behavior is present in:
- codie/intelligence/source_conflicts.py

9. Recommendation/evidence boundaries
Reject if Phase 18:
- generates recommendations
- ranks cards
- scores recommendation candidates
- creates recommendation candidate records
- chooses a winner source
- canonicalizes source records
- tells a user what to play or cut
- treats manual review conflicts as tournament evidence
- treats simulator output as tournament evidence
- reads source/provider payloads directly
- calls LLMs
- writes source conflicts to DB
- writes source conflicts to files

10. Tests
Run:

python -m unittest discover -s tests -v

Expected current result:

Ran 587 tests
OK (skipped=1)

Focused test:

python -m unittest tests.test_intelligence_source_conflicts -v

Expected:

Ran 21 tests
OK

Also run or equivalent-check these scans:

rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations\.generation|codie\.recommendations\.persistence|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\source_conflicts.py tests\test_intelligence_source_conflicts.py

rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\source_conflicts.py tests\test_intelligence_source_conflicts.py

rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\source_conflicts.py

rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload" codie\intelligence\source_conflicts.py tests\test_intelligence_source_conflicts.py

rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\source_conflicts.py tests\test_intelligence_source_conflicts.py docs\PHASE18B_SOURCE_CONFLICT_REPORT_IMPLEMENTATION_REPORT.md docs\CHECKPOINT_PHASE18_SOURCE_CONFLICT_REPORT.md

Expected:
no matches

Also run:

git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories

Expected:
no Phase 18 schema, repository, migration, or schema-spec changes unless explicitly documented as nonfunctional

11. Clean checkout concerns
- Confirm the test suite does not depend on local-only SQLite artifacts.
- Confirm Phase 18 docs and tests are committed.
- Confirm working tree is clean after checkout and tests.

Required final response:
- Verdict.
- Required fixes before Phase 19, if any.
- Review notes, if non-blocking.
- Whether Phase 19 may proceed.
```
