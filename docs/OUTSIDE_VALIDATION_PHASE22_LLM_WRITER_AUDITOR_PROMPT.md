# Outside Validation Prompt - Phase 22 LLM Writer/Auditor

Validate Codie Phase 22 work against `CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 23.

## Files To Review

Documentation:

```text
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_CONTRACT.md
docs/PHASE22_LLM_WRITER_AUDITOR_PLANNING_REPORT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT.md
docs/PHASE22A_LLM_WRITER_AUDITOR_CONTRACT_REPORT.md
docs/PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE22_LLM_WRITER_AUDITOR_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Implementation:

```text
codie/intelligence/llm_writer_auditor.py
codie/intelligence/__init__.py
tests/test_intelligence_llm_writer_auditor.py
```

Related context:

```text
codie/intelligence/answer_builder.py
codie/intelligence/query_planner.py
codie/intelligence/evidence_graph.py
codie/intelligence/evidence_inputs.py
codie/intelligence/source_conflicts.py
codie/intelligence/unsupported_cards.py
```

## Validation Tasks

Confirm:

```text
Phase 21 outside validation is treated as accepted input.
Phase 22 planning selects LLM writer/auditor boundary as the next layer.
Phase 22A contract matches the implementation.
Phase 22B implements the declared public interface.
The implementation is pure and in-memory.
The implementation accepts only structured ChatAnswer values as source input.
The implementation builds writer input only from structured ChatAnswer fields.
The implementation preserves citations.
The implementation preserves caveats.
The implementation preserves missing_evidence.
The implementation preserves blockers.
The implementation rejects local_user_data scope by default.
The implementation rejects sensitive scope by default.
The implementation validates draft citation/caveat/missing-evidence IDs.
The implementation rejects hidden caveats.
The implementation rejects hidden missing_evidence.
The implementation rejects hidden blockers.
The implementation rejects uncited draft claims.
The implementation rejects unsupported cards treated as modeled.
The implementation rejects source conflicts resolved in prose.
The implementation rejects forbidden strategic language.
The implementation rejects private metadata keys, including nested keys.
The implementation serializes deterministically.
The implementation does not call LLMs.
The implementation does not import LLM SDKs.
The implementation does not query SQLite or providers.
The implementation does not retrieve evidence itself.
The implementation does not generate recommendations.
```

Confirm these public objects exist:

```text
LLMWriterAuditorBuildError
LLMWriterInput
LLMWriterDraft
LLMAuditFinding
LLMAuditResult
LLMWriterAuditorOptions
build_writer_input_from_answer(...)
validate_writer_draft(...)
audit_writer_draft(...)
llm_writer_input_to_dict(...)
llm_writer_draft_to_dict(...)
llm_audit_result_to_dict(...)
```

Confirm schema discipline:

```text
Phase 22 adds no schema changes.
No tables, columns, indexes, migrations, or repository methods were added for writer/auditor packets.
Writer/auditor packets remain in-memory only.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 672 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_intelligence_llm_writer_auditor -v
```

Confirm:

```text
Ran 21 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3|openai|anthropic" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\llm_writer_auditor.py
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\llm_writer_auditor.py
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\llm_writer_auditor.py tests\test_intelligence_llm_writer_auditor.py docs\PHASE22B_LLM_WRITER_AUDITOR_IMPLEMENTATION_REPORT.md
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
no Phase 22 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
llm_writer_auditor.py imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, sqlite3, openai, or anthropic
llm_writer_auditor.py reads source/provider tables or payloads
llm_writer_auditor.py writes files
llm_writer_auditor.py calls LLMs
llm_writer_auditor.py imports LLM SDKs
llm_writer_auditor.py queries SQLite
llm_writer_auditor.py retrieves evidence itself
llm_writer_auditor.py runs simulator logic
llm_writer_auditor.py implements card behavior
llm_writer_auditor.py generates unconstrained final prose outside the structured draft model
llm_writer_auditor.py invents facts not backed by citations or missing_evidence
llm_writer_auditor.py generates recommendation or deck-construction language
llm_writer_auditor.py persists writer inputs, drafts, or audit results
private metadata can escape into output
source conflicts are resolved instead of preserved as caveats/findings
unsupported simulator cards are treated as modeled
hidden caveats, hidden missing_evidence, or hidden blockers can pass accepted audit
```

## Phase 23 Gate

Phase 23 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
