# Checkpoint - Phase 10 User Deck Workflow

## Verdict

```text
Phase 10A: PASS
Phase 10B: PASS
Phase 10C: PASS
Phase 10D: PASS
Phase 10E: PASS
Phase 10G: PASS
Phase 10I: PASS
Overall: READY FOR OUTSIDE VALIDATION
```

## Scope Completed

Phase 10 added the local user-deck workflow needed before user-facing analysis:

- import user deck text
- resolve cards through local Scryfall-backed lookup
- persist user deck rows atomically
- create analysis sessions
- build read-only analysis input objects
- compare deck contents against generic evidence candidates
- export comparison data as JSON-compatible dictionaries
- export comparison reports as Markdown
- write comparison exports to caller-supplied files
- run the accepted workflow through a repeatable CLI wrapper
- persist already-built evidence-only comparison summaries to `saved_analysis`

## Files Added Or Modified

Primary implementation:

- `codie/user_decks/__init__.py`
- `codie/user_decks/importer.py`
- `codie/user_decks/analysis_input.py`
- `codie/user_decks/evidence_comparison.py`
- `codie/db/repositories/user.py`
- `codie/exports/user_deck_reports.py`
- `codie/exports/__init__.py`
- `codie/cli/__init__.py`
- `codie/cli/user_deck.py`
- `codie/user_decks/saved_analysis.py`

Tests:

- `tests/test_user_deck_import.py`
- `tests/test_user_deck_analysis_input.py`
- `tests/test_user_deck_evidence_comparison.py`
- `tests/test_exports_user_deck_reports.py`
- `tests/test_cli_user_deck.py`
- `tests/test_user_deck_saved_analysis.py`

Contracts:

- `docs/PHASE10A_USER_DECK_IMPORT_CONTRACT.md`
- `docs/PHASE10B_USER_DECK_ANALYSIS_INPUT_CONTRACT.md`
- `docs/PHASE10C_USER_DECK_EVIDENCE_COMPARISON_CONTRACT.md`
- `docs/PHASE10D_USER_DECK_COMPARISON_EXPORT_CONTRACT.md`
- `docs/PHASE10E_USER_DECK_COMPARISON_FILE_WRITER_CONTRACT.md`
- `docs/PHASE10G_USER_DECK_CLI_CONTRACT.md`
- `docs/PHASE10I_SAVED_ANALYSIS_PERSISTENCE_CONTRACT.md`

## Public API Added

User deck import:

- `ParsedUserDeckCard`
- `ParsedUserDeck`
- `UserDeckImportError`
- `UserDeckImportResult`
- `parse_user_deck_text(...)`
- `UserDeckImporter.import_text(...)`
- `UserDeckImporter.import_parsed(...)`

Analysis input:

- `UserDeckAnalysisCard`
- `UserDeckAnalysisInput`
- `UserDeckAnalysisInputError`
- `build_user_deck_analysis_input(...)`

Evidence comparison:

- `UserDeckEvidenceCandidate`
- `UserDeckEvidenceComparisonRow`
- `UserDeckEvidenceComparison`
- `compare_user_deck_to_evidence(...)`

Exports:

- `user_deck_comparison_export(...)`
- `user_deck_comparison_markdown(...)`
- `UserDeckComparisonWriteResult`
- `write_user_deck_comparison_exports(...)`

Repository read methods:

- `UserRepository.get_user_deck(...)`
- `UserRepository.list_user_deck_cards(...)`
- `UserRepository.get_analysis_session(...)`

CLI:

- `codie.cli.user_deck.build_parser(...)`
- `codie.cli.user_deck.main(...)`

Saved analysis:

- `SavedUserDeckAnalysisResult`
- `save_user_deck_comparison_analysis(...)`
- `UserRepository.create_saved_analysis(...)`
- `UserRepository.get_saved_analysis(...)`
- `UserRepository.list_saved_analysis_for_deck(...)`

## Schema Impact

None.

Existing tables used:

- `user_decks`
- `user_deck_cards`
- `analysis_sessions`
- `saved_analysis`

## Boundary Compliance

The user deck core does not import:

- providers
- recommendations
- analytics
- ingestion
- source/provider tables

The export layer does not import:

- providers
- DB/repositories
- ingestion
- source/provider tables
- SQLite

The CLI layer does not import:

- providers
- recommendations
- analytics
- source/provider tables

## Atomicity

User deck import uses an explicit savepoint transaction.

Validation proves unresolved card imports leave no partial rows in:

- `user_decks`
- `user_deck_cards`
- `analysis_sessions`

## Evidence-Only Compliance

Phase 10 does not generate final recommendations.

Allowed comparison wording:

```text
Mystic Remora is absent in the imported user deck; evidence type commander_staple; sample size 42.
```

Forbidden recommendation language is rejected or absent from exports:

- `should play`
- `must include`
- `correct card`
- `breaks the format`
- `secretly optimal`

## Validation

Focused tests were run for each packet.

Latest full-suite validation:

```text
Ran 271 tests in 0.691s

OK
```

Static checks:

```text
git diff --check
```

passed.

Export boundary scan:

```text
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
```

returned:

```text
no matches
```

CLI boundary scan:

```text
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|source_events|source_decks|provider_objects" codie\cli
```

returned:

```text
no matches
```

User deck boundary scan:

```text
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
```

returned:

```text
no matches
```

## Remaining Review Notes

- GitHub remote is configured and the earlier Phase 10F checkpoint was pushed. Phase 10G should be pushed after this checkpoint update commit.
- No UI exists yet.
- Phase 10 comparison is evidence-only and does not persist comparison rows.
- CLI requires a local Codie SQLite database with card rows before deck import can resolve cards.
- Saved analysis persistence stores summaries, not final recommendations.
- Final recommendation generation remains intentionally separate.

## Recommended Next Step

Run outside validation on Phase 10, then proceed to the next contract-first packet.

Likely next candidates:

- UI planning
- simulator integration planning
- broader Phase 10 outside validation with CLI and saved-analysis persistence

Do not start final recommendation output until outside validation accepts the user-deck workflow boundaries.
