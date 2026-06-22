# Next Phase Contract

Recommended next task: Phase 8J - Innovation Snapshot Persistence Decision

## Current Status

Phase 8G, Phase 8H, and Phase 8I are locally implemented and validated.

Phase 8I added recommendation persistence and rebuild semantics. Validated candidate packets can now be written through `RecommendationRepository` into existing recommendation tables with atomic replacement behavior.

## Files Created Or Modified In Latest Packet

- `codie/db/repositories/recommendations.py`
- `codie/db/repositories/__init__.py`
- `codie/recommendations/persistence.py`
- `codie/recommendations/__init__.py`
- `codie/recommendations/generation.py`
- `tests/test_recommendation_persistence.py`
- `docs/PHASE8I_RECOMMENDATION_PERSISTENCE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `RecommendationRepository`
- `RecommendationRunSpec`
- `PersistedRecommendationRun`
- `recommendation_run_row(...)`
- `recommendation_candidate_row(...)`
- `persist_recommendation_packets(...)`

## Schema Impact

None.

Phase 8I uses existing tables:

- `recommendation_runs`
- `recommendation_candidates`

No migration or schema change was introduced.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|execute\(|executescript\(|sqlite3" codie\recommendations
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- Phase 8I rebuild key is `input_deck_hash + generated_at`; future user-deck workflow may refine this.
- Phase 8J should decide whether innovation snapshots need persistence now or can remain computed on demand.

## Recommended Next Packet

Phase 8J - Innovation Snapshot Persistence Decision.

This should be a decision packet first:

- determine whether innovation outputs need persistence before exports/UI
- if yes, define schema/migration requirements explicitly
- if no, document computed-on-demand behavior and move to Phase 9A

## Alternative Next Packet

Phase 9A - Report/Export Surface Contract.

This is appropriate if innovation snapshot persistence is deferred.

## Do Not Do

- Do not add schema without an explicit migration contract.
- Do not read provider/source tables from recommendations.
- Do not call providers.
- Do not add strategic claim language.
- Do not implement UI before report/export contract is defined.
- Do not start simulator integration.

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
