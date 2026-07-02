# Outside Validation Prompt - Phase 17 Evidence Graph Input Assembly

Use this prompt with an outside reviewer before Phase 18 begins.

```text
Validate Codie Phase 17 Evidence Graph Input Assembly work against CODIE_V1_CONSTITUTION.md.

Important:
- This is an outside validation request.
- Do not rely only on checkpoint prose.
- Inspect implementation files, tests, docs, and dependency boundaries.
- Run tests from a clean checkout if possible.

Return:
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 18.

Files to review:

Core contracts and reports:
- docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_CONTRACT.md
- docs/PHASE17_INTERACTIVE_INTELLIGENCE_INPUT_ASSEMBLY_PLANNING_REPORT.md
- docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT.md
- docs/PHASE17A_EVIDENCE_GRAPH_INPUT_ASSEMBLY_CONTRACT_REPORT.md
- docs/PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md
- docs/CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md

Related Phase 16 evidence graph references:
- docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT.md
- docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
- codie/intelligence/evidence_graph.py
- tests/test_intelligence_evidence_graph.py

Implementation files:
- codie/intelligence/__init__.py
- codie/intelligence/evidence_inputs.py

Tests:
- tests/test_intelligence_evidence_inputs.py

Architecture references:
- docs/CODIE_V1_CONSTITUTION.md
- docs/DEPENDENCY_RULES.md
- docs/NEXT_PHASE_CONTRACT.md
- docs/CODEX_CONTINUITY_HANDOFF.md

Check:

1. Phase 17 planning discipline
- Confirm Phase 17 starts with input assembly, not chat UI.
- Confirm Phase 17 adds no LLM calls.
- Confirm Phase 17 adds no evidence graph persistence.
- Confirm Phase 17 adds no provider calls.
- Confirm Phase 17 adds no source/provider table reads.
- Confirm Phase 17 adds no simulator execution.
- Confirm Phase 17 adds no analytics calculation.
- Confirm Phase 17 adds no recommendation generation.
- Confirm Phase 17 adds no private raw_input export.

2. Schema discipline
- Confirm Phase 17 adds no schema changes.
- Confirm no tables, columns, indexes, migrations, or repository methods were added for evidence input assembly.
- Confirm input assembly remains in-memory only.
- Confirm schema and repository files did not drift during Phase 17 unless explicitly documented as nonfunctional.

3. Public interface
- Confirm these public objects exist:
  EvidenceInputBuildError
  EvidenceRecordRef
  EvidenceInputRecord
  EvidenceInputBundle
  EvidenceGraphAssemblyOptions
  evidence_record_from_dict(...)
  validate_evidence_input_bundle(...)
  build_graph_input_from_records(...)

4. Input validation behavior
- Confirm bundle_id is required.
- Confirm claim_text is required.
- Confirm subject_id is required.
- Confirm records are required.
- Confirm record IDs must be unique.
- Confirm record_type must be supported.
- Confirm confidence values must be between 0 and 1.
- Confirm privacy_scope must be supported.
- Confirm non-manual records require references.
- Confirm manual_note records may omit references.
- Confirm references require source_name.
- Confirm references require observed_at.
- Confirm references require source_record_id or source_url.
- Confirm metadata must be JSON-compatible.
- Confirm filtered bundles with no remaining records fail cleanly.
- Confirm forbidden strategic language fails cleanly.

5. Mapping behavior
- Confirm record types map correctly:
  recommendation_candidate -> card
  innovation_signal -> innovation_signal
  combo_evidence -> combo_evidence
  primer_metadata -> primer_metadata
  simulation_review_summary -> simulation_result
  deck_memory_summary -> user_deck_memory
  saved_analysis_summary -> saved_analysis
  manual_note -> manual_note
  source_conflict -> source_conflict
  unsupported_card -> unsupported_card
- Confirm references map to EvidenceCitation values.
- Confirm bundle caveats map to EvidenceCaveat values.
- Confirm record caveats map to EvidenceCaveat values and link to their node.
- Confirm MVP assembly emits no edges unless a future contract adds relationship construction.
- Confirm build_graph_input_from_records(...) returns EvidenceGraphInput with edges == [] for MVP input bundles.

6. Privacy
- Confirm local_user_data records preserve privacy_scope.
- Confirm sensitive records are excluded by default.
- Confirm sensitive records are included only with explicit option.
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
- Confirm filtered records create caveats instead of disappearing silently.

7. Architecture boundaries
Reject if Phase 17 code imports any of:
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
- codie/intelligence/evidence_inputs.py
- tests/test_intelligence_evidence_inputs.py

Confirm no production file-writing behavior is present in:
- codie/intelligence/evidence_inputs.py

8. Recommendation/evidence boundaries
Recommendation_candidate records may be consumed only if they are already-built
sanitized input records. Phase 17 must not create, rank, score, or recommend
them.

Reject if Phase 17:
- generates recommendations
- ranks cards
- scores recommendation candidates
- creates recommendation candidate records
- tells a user what to play or cut
- treats manual notes as tournament evidence
- treats simulator output as tournament evidence
- reads source/provider payloads directly
- calls LLMs
- writes evidence inputs or graphs to DB
- writes evidence inputs or graphs to files

9. Tests
Run:

python -m unittest discover -s tests -v

Expected current result:

Ran 566 tests
OK (skipped=1)

Focused test:

python -m unittest tests.test_intelligence_evidence_inputs -v

Expected:

Ran 19 tests
OK

Also run or equivalent-check these scans:

rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations\.generation|codie\.recommendations\.persistence|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\evidence_inputs.py tests\test_intelligence_evidence_inputs.py

rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\evidence_inputs.py tests\test_intelligence_evidence_inputs.py

rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\evidence_inputs.py

rg -n "source_events|source_decks|source_deck_cards|provider_objects|raw_provider_payload" codie\intelligence\evidence_inputs.py tests\test_intelligence_evidence_inputs.py

rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\evidence_inputs.py tests\test_intelligence_evidence_inputs.py docs\PHASE17B_EVIDENCE_GRAPH_INPUT_ASSEMBLY_IMPLEMENTATION_REPORT.md docs\CHECKPOINT_PHASE17_INPUT_ASSEMBLY_REPORT.md

Expected:
no matches

Also run:

git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories

Expected:
no Phase 17 schema, repository, migration, or schema-spec changes unless explicitly documented as nonfunctional

10. Clean checkout concerns
- Confirm the test suite does not depend on local-only SQLite artifacts.
- Confirm Phase 17 docs and tests are committed.
- Confirm working tree is clean after checkout and tests.

Required final response:
- Verdict.
- Required fixes before Phase 18, if any.
- Review notes, if non-blocking.
- Whether Phase 18 may proceed.
```
