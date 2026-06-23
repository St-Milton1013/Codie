# Checkpoint - Phase 11 User Workflow Retrieval

## Verdict

```text
Phase 11 Planning: PASS
Phase 11A Saved Analysis Retrieval And Listing: PASS
Overall: READY FOR OUTSIDE VALIDATION
```

## Scope Completed

Phase 11 chose and implemented the next safe workflow after Phase 10:

- read-only saved-analysis listing
- read-only saved-analysis detail retrieval
- stable summary/detail models
- deterministic CLI JSON output for list/show commands
- malformed saved summary failure handling
- continued evidence-only and boundary discipline

## Files Added Or Modified

Primary implementation:

- `codie/user_decks/saved_analysis_listing.py`
- `codie/user_decks/__init__.py`
- `codie/cli/user_deck.py`

Tests:

- `tests/test_user_deck_saved_analysis_listing.py`
- `tests/test_cli_user_deck.py`

Contracts:

- `docs/PHASE11_PLANNING_CONTRACT.md`
- `docs/PHASE11A_SAVED_ANALYSIS_RETRIEVAL_CONTRACT.md`

## Public API Added

- `SavedAnalysisReadError`
- `SavedAnalysisSummary`
- `SavedAnalysisDetail`
- `list_saved_user_deck_analyses(...)`
- `get_saved_user_deck_analysis(...)`

CLI commands:

- `list-saved-analyses`
- `show-saved-analysis`

## Schema Impact

None.

Existing table used:

- `saved_analysis`

## Boundary Compliance

The retrieval helper does not import:

- providers
- recommendations
- analytics
- ingestion
- source/provider tables

The CLI list/show commands do not import:

- providers
- recommendations
- analytics
- source/provider tables

## Behavior

List command:

```powershell
python -m codie.cli.user_deck list-saved-analyses `
  --db codie.sqlite `
  --user-deck-id 1
```

Show command:

```powershell
python -m codie.cli.user_deck show-saved-analysis `
  --db codie.sqlite `
  --saved-analysis-id 1
```

Both commands emit deterministic JSON.

## Failure Handling

- Unknown saved analysis IDs raise `SavedAnalysisReadError`.
- Malformed `summary_json` raises `SavedAnalysisReadError`.
- Retrieval is read-only and performs no writes.

## Validation

Focused tests:

```text
Ran 12 tests in 0.415s

OK
```

Latest full-suite validation:

```text
Ran 278 tests in 0.743s

OK
```

Static checks:

```text
git diff --check
```

passed.

User deck boundary scan:

```text
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
```

returned:

```text
user_decks: no matches
```

CLI boundary scan:

```text
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
```

returned:

```text
cli: no matches
```

## Remaining Review Notes

- No UI exists yet.
- Simulator integration remains intentionally deferred.
- Final recommendation output remains intentionally separate.
- CLI still requires a local Codie SQLite database with card rows before deck import can resolve cards.

## Recommended Next Step

Send Phase 11 for outside validation, then choose the next contract-first packet.

Likely candidates:

- UI planning contract
- simulator contract refresh
- packaging/deployment docs
- saved-analysis report polish

Do not start final recommendation output until the evidence and language gates are explicitly carried forward.
