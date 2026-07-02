# Outside Validation Prompt - Phase 19 Unsupported Relevant Card Queue

Validate Codie Phase 19 work against `CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL
```

Then list required fixes before Phase 20.

## Files To Review

Documentation:

```text
docs/PHASE19_UNSUPPORTED_RELEVANT_CARD_QUEUE_PLANNING_CONTRACT.md
docs/PHASE19_UNSUPPORTED_RELEVANT_CARD_QUEUE_PLANNING_REPORT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT.md
docs/PHASE19A_UNSUPPORTED_RELEVANT_CARD_QUEUE_CONTRACT_REPORT.md
docs/PHASE19B_UNSUPPORTED_RELEVANT_CARD_QUEUE_IMPLEMENTATION_REPORT.md
docs/CHECKPOINT_PHASE19_UNSUPPORTED_CARD_QUEUE_REPORT.md
docs/NEXT_PHASE_CONTRACT.md
docs/CODEX_CONTINUITY_HANDOFF.md
```

Implementation:

```text
codie/intelligence/unsupported_cards.py
codie/intelligence/__init__.py
tests/test_intelligence_unsupported_cards.py
```

Related context:

```text
codie/intelligence/evidence_inputs.py
codie/intelligence/evidence_graph.py
codie/intelligence/source_conflicts.py
```

## Validation Tasks

Confirm:

```text
Phase 18 outside validation is treated as accepted input.
Phase 19 planning selects Unsupported Relevant Card Queue as the next layer.
Phase 19A contract matches the implementation.
Phase 19B implements the declared public interface.
The implementation is pure and in-memory.
The implementation accepts only sanitized evidence references.
The implementation emits EvidenceInputRecord values with record_type unsupported_card.
The implementation preserves card_name, oracle_id, scryfall_id, reason, severity, and status.
The implementation preserves EvidenceRecordRef-compatible references.
Blocking items remain visible.
Resolved and ignored-by-policy items are excluded by default.
Sensitive evidence is excluded by default.
Filtered evidence creates explicit caveats, counts, or filtered-item records.
Deduplication by card identity is deterministic.
Deduplication can be disabled.
Private metadata keys are rejected, including nested keys.
Forbidden strategic language is rejected.
```

## Required Test Command

From a clean checkout, run:

```powershell
python -m unittest discover -s tests
```

Confirm:

```text
Ran 610 tests
OK (skipped=1)
```

Also run:

```powershell
python -m unittest tests.test_intelligence_unsupported_cards -v
```

Confirm:

```text
Ran 23 tests
OK
```

## Boundary Scans

Run:

```powershell
rg -n "codie\.db|codie\.providers|codie\.analytics|codie\.recommendations\.generation|codie\.recommendations\.persistence|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\intelligence\unsupported_cards.py tests\test_intelligence_unsupported_cards.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\intelligence\unsupported_cards.py tests\test_intelligence_unsupported_cards.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "open\(|write_text\(|write_bytes\(|Path\(|mkdir\(|touch\(|unlink\(" codie\intelligence\unsupported_cards.py
```

Expected:

```text
no production file-writing behavior
```

Run:

```powershell
rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\intelligence\unsupported_cards.py tests\test_intelligence_unsupported_cards.py
```

Expected:

```text
no matches
```

Run:

```powershell
rg -n "raw_provider_payload|provider_payload|original_import_text|raw_input|private_deck_text|full_primer_body" codie\intelligence\unsupported_cards.py
```

Expected:

```text
matches only blocked-key constants/rejection logic
```

Run:

```powershell
rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\intelligence\unsupported_cards.py tests\test_intelligence_unsupported_cards.py docs\PHASE19B_UNSUPPORTED_RELEVANT_CARD_QUEUE_IMPLEMENTATION_REPORT.md
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
no Phase 19 schema, repository, migration, or schema-spec changes
```

## Reject If

Reject if:

```text
unsupported_cards.py imports DB, repositories, providers, cards, analytics, recommendations, probability_engine, canonical, requests, httpx, or sqlite3
unsupported_cards.py reads source/provider tables or payloads
unsupported_cards.py writes files
unsupported_cards.py runs simulator logic
unsupported_cards.py implements card behavior
unsupported_cards.py generates recommendation or deck-construction language
unsupported_cards.py treats unsupported card queue items as tournament evidence
unsupported_cards.py persists queue items
private metadata can escape into output
filtered sensitive evidence disappears without a caveat/count/filtered-item record
blocking unsupported-card items can be silently hidden
```

## Phase 20 Gate

Phase 20 must not start unless this validation returns:

```text
PASS
PASS WITH REVIEW NOTES
```
