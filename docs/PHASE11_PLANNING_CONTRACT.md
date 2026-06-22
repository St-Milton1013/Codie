# Phase 11 - Planning Contract

## Verdict

```text
Recommended next implementation: Phase 11A - Saved Analysis Retrieval And Listing
Do not start UI, simulator integration, or final recommendation output yet.
```

## Purpose

Phase 11 begins the transition from local user-deck workflow primitives into user-facing workflows. The safest next step is to make saved analyses retrievable and listable through repository-backed, evidence-only surfaces.

This keeps Codie useful while preserving the Phase 8 and Phase 10 boundaries:

- no provider calls
- no source/provider table reads
- no final recommendation output
- no strategic claim language
- no UI yet
- no simulator integration yet
- no schema changes

## Decision

Proceed with:

```text
Phase 11A - Saved Analysis Retrieval And Listing
```

Defer:

- UI planning until saved analysis retrieval has a stable API.
- Simulator integration until simulator contracts are refreshed against current Phase 8/10 evidence rules.
- Final recommendation output until recommendation language and user-deck comparison boundaries are explicitly revalidated.

## Why 11A Comes Next

Phase 10 can now:

- import user deck text
- resolve cards
- create analysis sessions
- compare against evidence candidates
- export reports
- save evidence-only summaries
- run through a CLI

The missing operational piece is retrieval:

- list saved analyses for a user deck
- fetch saved analysis details
- expose summary JSON in a stable model
- avoid direct SQL outside the repository
- allow CLI users to inspect prior saved reports

This is lower risk than UI or simulator work and makes existing functionality easier to validate.

## Phase 11A Scope

Files likely to create or modify:

- `codie/user_decks/saved_analysis_listing.py`
- `codie/cli/user_deck.py`
- `tests/test_user_deck_saved_analysis_listing.py`
- `tests/test_cli_user_deck.py`
- `docs/PHASE11A_SAVED_ANALYSIS_RETRIEVAL_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

Public functions/classes likely needed:

- `SavedAnalysisSummary`
- `SavedAnalysisDetail`
- `list_saved_user_deck_analyses(...)`
- `get_saved_user_deck_analysis(...)`

Possible CLI commands:

```text
list-saved-analyses
show-saved-analysis
```

## Schema Impact

None expected.

Use existing table:

- `saved_analysis`

## Dependencies

Allowed:

- `UserRepository`
- `saved_analysis` summary models
- standard library JSON parsing
- existing CLI parser

Forbidden:

- providers
- source repositories/tables
- analytics
- recommendations
- simulator
- UI
- raw SQL outside `codie/db/repositories`

## Required Tests

Phase 11A should test:

- list saved analyses for a deck
- fetch saved analysis detail by ID
- missing saved analysis fails cleanly
- malformed summary JSON fails cleanly
- CLI list command prints deterministic JSON
- CLI show command prints deterministic JSON
- boundary scans remain clean
- full test suite passes

## Failure Modes

Required failure behavior:

- unknown saved analysis ID raises a structured user-deck error
- malformed `summary_json` raises a structured user-deck error
- CLI invalid IDs return nonzero or raise cleanly in tests
- no partial writes because retrieval is read-only

## Do Not Do In Phase 11A

- Do not generate final recommendations.
- Do not calculate cuts.
- Do not start UI.
- Do not start simulator integration.
- Do not call providers.
- Do not read source/provider tables.
- Do not add schema.

## Later Phase Candidates

After Phase 11A:

- Phase 11B - Saved Analysis CLI Report Listing Polish
- Phase 11C - User Workflow Checkpoint
- Phase 12 - UI Planning Contract
- Phase 13 - Simulator Contract Refresh

Final recommendation output should remain separate until the recommendation language and evidence-stack gates are reviewed again.
