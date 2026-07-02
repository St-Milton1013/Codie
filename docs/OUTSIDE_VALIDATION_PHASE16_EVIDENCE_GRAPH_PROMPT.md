# Outside Validation Prompt - Phase 16 Evidence Graph

Use this prompt with an outside reviewer before Phase 17 begins.

```text
Validate Codie Phase 16 Evidence Graph work against CODIE_V1_CONSTITUTION.md.

Important:
- This is an outside validation request.
- Do not rely only on checkpoint prose.
- Inspect implementation files, tests, docs, and dependency boundaries.
- Run tests from a clean checkout if possible.

Return:
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 17.

Files to review:

Core contracts and reports:
- docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_CONTRACT.md
- docs/PHASE16_INTERACTIVE_INTELLIGENCE_PLANNING_REPORT.md
- docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT.md
- docs/PHASE16A_EVIDENCE_GRAPH_CONTRACT_REPORT.md
- docs/PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md
- docs/CHECKPOINT_PHASE16_EVIDENCE_GRAPH_REPORT.md
- docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md

Implementation files:
- codie/intelligence/__init__.py
- codie/intelligence/evidence_graph.py

Tests:
- tests/test_intelligence_evidence_graph.py

Architecture references:
- docs/CODIE_V1_CONSTITUTION.md
- docs/DEPENDENCY_RULES.md
- docs/NEXT_PHASE_CONTRACT.md
- docs/CODEX_CONTINUITY_HANDOFF.md

Check:

1. Phase 16 planning discipline
- Confirm Phase 16 starts with evidence graph, not chat UI.
- Confirm Phase 16 adds no LLM calls.
- Confirm Phase 16 adds no provider calls.
- Confirm Phase 16 adds no source/provider table reads.
- Confirm Phase 16 adds no simulator execution.
- Confirm Phase 16 adds no recommendation generation.
- Confirm Phase 16 adds no private raw_input export.

2. Schema discipline
- Confirm Phase 16 adds no schema changes.
- Confirm no tables, columns, indexes, migrations, or repository methods were added for evidence graphs.
- Confirm evidence graph remains in-memory only.
- Confirm schema and repository files did not drift during Phase 16 unless explicitly documented as nonfunctional.

3. Public interface
- Confirm these public objects exist:
  EvidenceGraphBuildError
  EvidenceCitation
  EvidenceCaveat
  EvidenceNode
  EvidenceEdge
  EvidenceGraph
  EvidenceGraphInput
  build_evidence_graph(...)
  validate_evidence_graph(...)
  evidence_graph_to_dict(...)

4. Graph validation behavior
- Confirm graph_id is required.
- Confirm claim_text is required.
- Confirm strategic-language validation applies to claim_text, node summaries, edge summaries, and caveat messages.
- Confirm nodes are required.
- Confirm node IDs are unique.
- Confirm edge IDs are unique.
- Confirm edge references must point to existing nodes.
- Confirm caveat references must point to existing nodes.
- Confirm confidence values must be between 0 and 1.
- Confirm metadata must be JSON-compatible.
- Confirm unsupported node, edge, source, and caveat types fail cleanly.
- Confirm manual_note nodes may omit citations.
- Confirm non-manual nodes require citations.
- Confirm citations require either source_record_id or source_url.
- Confirm blocking caveats are preserved in serialized output.

5. Determinism
- Confirm evidence_graph_to_dict(...) output is deterministic.
- Confirm nodes sort by node_id.
- Confirm edges sort by edge_id.
- Confirm caveats sort by caveat_id.
- Confirm citations sort by citation_id.
- Confirm repeated serialization of the same graph is stable.

6. Privacy
- Confirm local_user_data nodes preserve privacy_scope.
- Confirm sensitive nodes preserve privacy_scope.
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
- Confirm evidence graph serialization does not expose private raw_input.
- Confirm privacy redactions and blocking caveats are not hidden.

7. Architecture boundaries
Reject if Phase 16 code imports any of:
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
- codie/intelligence/evidence_graph.py
- tests/test_intelligence_evidence_graph.py

Confirm no production file-writing behavior is present in:
- codie/intelligence/evidence_graph.py

8. Recommendation/evidence boundaries
Reject if Phase 16:
- generates recommendations
- ranks cards
- tells a user what to play or cut
- treats manual notes as tournament evidence
- treats simulator output as tournament evidence
- reads source/provider payloads directly
- calls LLMs
- writes evidence graphs to DB
- writes evidence graphs to files

9. Moxfield Frequency Pool Builder roadmap patch
- Confirm docs/ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md is roadmap-only.
- Confirm it does not implement provider code.
- Confirm it does not authorize live Moxfield fetching yet.
- Confirm it does not authorize schema changes yet.
- Confirm it does not authorize UI work yet.
- Confirm it does not authorize recommendation output.

10. Tests
Run:

python -m unittest discover -s tests -v

Expected current result:

Ran 547 tests
OK (skipped=1)

Focused test:

python -m unittest tests.test_intelligence_evidence_graph -v

Expected:

Ran 19 tests
OK

Also run or equivalent-check these scans:

rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations\.generation|codie\.recommendations\.persistence|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\evidence_graph.py tests\test_intelligence_evidence_graph.py

rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\evidence_graph.py tests\test_intelligence_evidence_graph.py

rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\evidence_graph.py

rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\evidence_graph.py tests\test_intelligence_evidence_graph.py docs\PHASE16B_EVIDENCE_GRAPH_IMPLEMENTATION_REPORT.md docs\CHECKPOINT_PHASE16_EVIDENCE_GRAPH_REPORT.md docs\ROADMAP_PATCH_MOXFIELD_FREQUENCY_POOL_BUILDER.md

Expected:
no matches for production file-writing behavior in codie\intelligence\evidence_graph.py
otherwise no matches

Also run:

git diff --name-only -- codie/db/schema docs/SCHEMA_SPEC.md codie/db/repositories

Expected:
no Phase 16 schema, repository, migration, or schema-spec changes unless explicitly documented as nonfunctional

11. Clean checkout concerns
- Confirm the test suite does not depend on local-only SQLite artifacts.
- Confirm Phase 16 docs and tests are committed.
- Confirm working tree is clean after checkout and tests.

Required final response:
- Verdict.
- Required fixes before Phase 17, if any.
- Review notes, if non-blocking.
- Whether Phase 17 may proceed.
```
