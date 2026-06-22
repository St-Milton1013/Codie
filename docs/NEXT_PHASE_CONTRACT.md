# Next Phase Contract

Recommended next task: Phase 10D - User Deck Comparison Report Export

## Current Status

Phase 10C is locally implemented and validated.

Phase 10C added an evidence-only comparison surface between imported user decks and generic card evidence candidates. It reports present/absent status, quantities, zones, source metadata, and evidence-only lines. It did not add providers, source table reads, recommendations, UI, schema, DB access, or live network dependencies.

## Files Created Or Modified In Latest Packet

- `codie/user_decks/__init__.py`
- `codie/user_decks/evidence_comparison.py`
- `tests/test_user_deck_evidence_comparison.py`
- `docs/PHASE10C_USER_DECK_EVIDENCE_COMPARISON_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `UserDeckEvidenceCandidate`
- `UserDeckEvidenceComparisonRow`
- `UserDeckEvidenceComparison`
- `compare_user_deck_to_evidence(...)`

## Schema Impact

None.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "codie\.providers|codie\.db|codie\.ingestion|source_events|source_decks|provider_objects|execute\(|executescript\(|sqlite3" codie\exports
rg -n "codie\.providers|codie\.recommendations|codie\.analytics|codie\.ingestion|source_events|source_decks|provider_objects" codie\user_decks
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- User deck evidence comparison is in-memory only and does not persist rows.
- No UI exists yet.

## Recommended Next Packet

Phase 10D - User Deck Comparison Report Export.

This should stay evidence-only and export already-built comparison objects:

- deterministic JSON-compatible comparison export
- Markdown comparison report
- no DB access
- no recommendation generation
- no strategic recommendation language

## Do Not Do

- Do not build UI before user-deck contracts are accepted.
- Do not call providers.
- Do not read source/provider tables.
- Do not add strategic claim language.
- Do not start simulator integration.
- Do not add schema without explicit migration contract.
- Do not generate final recommendations in Phase 10D.

## Required Phase Packet Shape

Every follow-up phase packet must include:

- contract document before code
- complete implementation files
- focused tests and fixture data where relevant
- full validation command and actual output
- static architecture checks where relevant
- completion report
- updated handoff or next-phase document
- clean commit after validation passes

Use this packet order:

```text
contract -> code -> tests -> validation -> completion report -> handoff -> commit
```
