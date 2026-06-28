# Outside Validation Prompt - Phase 11 And Phase 12

Use this prompt to validate Codie Phase 11 and Phase 12 before any React/Vite UI scaffold begins.

## Files To Review

```text
docs/CODEX_CONTINUITY_HANDOFF.md
docs/CHECKPOINT_PHASE11_USER_WORKFLOW_RETRIEVAL_REPORT.md
docs/PHASE11_PLANNING_CONTRACT.md
docs/PHASE11A_SAVED_ANALYSIS_RETRIEVAL_CONTRACT.md
docs/CHECKPOINT_PHASE12_UI_PREP_REPORT.md
docs/PHASE12_UI_PLANNING_CONTRACT.md
docs/PHASE12A_USER_WORKFLOW_VIEW_MODELS_CONTRACT.md
```

Primary implementation files:

```text
codie/user_decks/saved_analysis_listing.py
codie/cli/user_deck.py
codie/pages/user_workflow.py
tests/test_user_deck_saved_analysis_listing.py
tests/test_cli_user_deck.py
tests/test_pages_user_workflow.py
```

## Validation Request

Validate Phase 11 and Phase 12 against `docs/CODIE_V1_CONSTITUTION.md`.

Return:

```text
PASS
PASS WITH REVIEW NOTES
PASS WITH REQUIRED FIXES
FAIL
```

Then list required fixes before Phase 12C.

## Phase 11 Checks

Confirm:

```text
saved-analysis listing is read-only
saved-analysis detail retrieval is read-only
retrieval uses existing saved_analysis records only
no schema changes were introduced
malformed summary_json fails cleanly
unknown saved_analysis id fails cleanly
CLI list/show commands emit deterministic JSON
CLI list/show commands do not generate recommendations
```

Reject if:

```text
retrieval writes to DB
retrieval imports providers
retrieval imports recommendations
retrieval imports analytics
retrieval reads source/provider tables
retrieval mutates saved summaries
CLI emits strategic recommendation language
```

## Phase 12 Checks

Confirm:

```text
page/view-model layer is pure transformation only
page/view-model layer does not open DB connections
page/view-model layer does not import repositories
page/view-model layer does not import providers
page/view-model layer does not import analytics
page/view-model layer does not import recommendations
page/view-model layer preserves evidence/source metadata
page/view-model layer preserves generated timestamps
empty states are explicit
forbidden strategic language is rejected or absent
no React/Vite/Tailwind scaffold was created
no npm packages were added
no schema changes were introduced
```

Reject if:

```text
codie/pages imports db/repositories/providers/analytics/recommendations
view models own data retrieval
view models read source/provider tables
view models generate final recommendation language
view models omit provenance/source metadata
frontend scaffold exists before acceptance
```

## Boundary Scans To Confirm

Expected clean scans:

```powershell
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
rg -n "codie\.providers|codie\.db|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects|sqlite3" codie\pages
```

## Test Evidence To Confirm

Reported latest validation:

```text
Phase 11 focused tests: Ran 12 tests - OK
Phase 12 focused tests: Ran 5 tests - OK
Latest full suite: Ran 283 tests - OK
git diff --check: passed
```

If running locally, use:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
git diff --check
```

## Architecture Gate Before Phase 12C

Phase 12C may proceed only if:

```text
Phase 11 saved-analysis retrieval is accepted
Phase 12 view-model boundary is accepted
UI remains a consumer of page/application models
UI does not own data access
UI does not use raw SQL
UI does not call providers
UI does not generate final recommendations
```

Recommended next packet if accepted:

```text
Phase 12C - UI Scaffold Contract
```

Do not start:

```text
final recommendation output
simulator implementation
provider live backfills
schema changes
deck editing UI
```
