# Outside Validation Prompt - Phase 15 Deck Memory

Use this prompt with an outside reviewer before Phase 16 begins.

```text
Validate Codie Phase 15 Deck Memory work against CODIE_V1_CONSTITUTION.md.

Important:
- This is an outside validation request.
- Do not rely only on checkpoint prose.
- Inspect implementation files, tests, docs, schema, and repository boundaries.
- Run tests from a clean checkout if possible.

Return:
PASS / PASS WITH REVIEW NOTES / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 16.

Files to review:

Core contracts and reports:
- docs/PHASE15_PLANNING_CONTRACT.md
- docs/PHASE15A_DECK_MEMORY_LISTING_RETRIEVAL_CONTRACT.md
- docs/PHASE15B_DECK_MEMORY_LISTING_RETRIEVAL_IMPLEMENTATION_REPORT.md
- docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT.md
- docs/PHASE15C_DECK_MEMORY_CLI_CONTRACT_REPORT.md
- docs/PHASE15D_DECK_MEMORY_CLI_IMPLEMENTATION_REPORT.md
- docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT.md
- docs/PHASE15E_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_CONTRACT_REPORT.md
- docs/USER_GUIDE_DECK_MEMORY_CLI.md
- docs/PHASE15F_DECK_MEMORY_CLI_USAGE_DOCUMENTATION_REPORT.md
- docs/CHECKPOINT_PHASE15_DECK_MEMORY_REPORT.md

Implementation files:
- codie/db/repositories/user.py
- codie/user_decks/deck_memory.py
- codie/user_decks/__init__.py
- codie/cli/user_deck_memory.py

Tests:
- tests/test_user_deck_memory.py
- tests/test_cli_user_deck_memory.py

Schema files:
- codie/db/schema/user.sql
- docs/SCHEMA_SPEC.md

Check:

1. Schema discipline
- Confirm Phase 15 adds no schema changes.
- Confirm Phase 15 uses only existing tables:
  user_decks
  user_deck_cards
  analysis_sessions
  saved_analysis
- Confirm no new tables, columns, indexes, or migrations are required.

2. Deck memory read layer
- Confirm list_deck_memory(...) is read-only.
- Confirm get_deck_memory_detail(...) is read-only.
- Confirm list filters:
  commander_hash
  deck_hash
  include_temporary
  include_persistent
  created_at_from
  created_at_to
  limit
- Confirm include_temporary=false and include_persistent=false fails with a documented validation error.
- Confirm deterministic ordering:
  summaries by updated_at DESC, created_at DESC, user_deck_id DESC
  cards by user_deck_card_id ASC
  saved analyses by generated_at ASC, saved_analysis_id ASC
  analysis sessions by started_at ASC, analysis_session_id ASC
- Confirm unknown user_deck_id fails cleanly.

3. Repository boundary
- Confirm raw SQL for Phase 15 is only in codie/db/repositories/user.py.
- Confirm codie/user_decks/deck_memory.py does not contain raw SQL.
- Confirm user-deck memory does not read source/provider tables:
  source_events
  source_decks
  source_deck_cards
  provider_objects

4. CLI behavior
- Confirm codie/cli/user_deck_memory.py exposes:
  list-deck-memory
  show-deck-memory
- Confirm CLI outputs JSON only for successful command output.
- Confirm list-deck-memory omits raw_input.
- Confirm show-deck-memory omits raw_input by default.
- Confirm show-deck-memory includes raw_input only with --include-raw-input.
- Confirm missing database path exits cleanly and non-zero.
- Confirm unknown user_deck_id exits cleanly and non-zero.
- Confirm CLI does not create schema or mutate user deck records.

5. Privacy
- Confirm raw_input is treated as private deck text.
- Confirm usage docs warn that raw_input contains original imported deck text.
- Confirm usage docs say raw_input is omitted by default.
- Confirm usage docs say raw_input appears only with --include-raw-input.
- Confirm usage docs do not encourage uploading or sharing private raw_input.

6. Architecture boundaries
Reject if Phase 15 code imports any of:
- codie.providers
- codie.analytics
- codie.recommendations
- codie.ingestion
- codie.cards
- codie.probability_engine
- codie.canonical
- requests
- httpx
- sqlite3 directly outside the db package

7. Recommendation/evidence boundaries
Reject if Phase 15:
- treats user decks as source/provider records
- treats user decks as metagame truth
- generates recommendations
- ranks cards
- says a card should be played or cut
- calls LLMs
- calls providers
- runs simulator logic

8. Tests
Run:

python -m unittest discover -s tests -v

Expected current result:

Ran 528 tests
OK (skipped=1)

Also run or equivalent-check these scans:

rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py

rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py

rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\user_decks\deck_memory.py tests\test_user_deck_memory.py

rg -n "codie\.providers|codie\.analytics|codie\.recommendations|codie\.ingestion|codie\.cards|codie\.probability_engine|codie\.canonical|requests|httpx|sqlite3" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py

rg -n "source_events|source_decks|source_deck_cards|provider_objects" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py

rg -n "should play|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include" codie\cli\user_deck_memory.py tests\test_cli_user_deck_memory.py

rg -n "should play|should be played|should be cut|must include|correct card|breaks the format|secretly optimal|cut this|strict upgrade|auto-include|recommended cut|recommended include|tournament evidence" docs\USER_GUIDE_DECK_MEMORY_CLI.md

rg -n "raw_input|--include-raw-input|original imported deck text|omitted by default" docs\USER_GUIDE_DECK_MEMORY_CLI.md

rg -n "SELECT |INSERT |UPDATE |DELETE |execute\(|executescript\(" codie\user_decks\deck_memory.py codie\cli\user_deck_memory.py

Expected:
no matches

rg -n "create_|insert_|update_|delete_|save_|persist_|commit\(|rollback\(" codie\user_decks\deck_memory.py codie\cli\user_deck_memory.py

Expected:
no matches

9. Clean checkout concerns
- Confirm the test suite does not depend on local-only SQLite artifacts.
- Confirm Phase 15 docs and tests are committed.
- Confirm working tree is clean after checkout and tests.

Required final response:
- Verdict.
- Required fixes before Phase 16, if any.
- Review notes, if non-blocking.
- Whether Phase 16 may proceed.
```
