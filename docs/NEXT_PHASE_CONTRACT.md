# Next Phase Contract

Recommended next task: Phase 8I - Recommendation Persistence And Rebuild Semantics

## Current Status

Phase 8G and Phase 8H are locally implemented and validated.

Phase 8H added in-memory recommendation candidate generation orchestration. It composes canonical analytics/report inputs into evidence bundles, recommendation score drafts, and audit reports without persistence.

## Files Created Or Modified In Latest Packet

- `codie/recommendations/generation.py`
- `codie/recommendations/__init__.py`
- `tests/test_recommendation_generation.py`
- `docs/PHASE8H_RECOMMENDATION_GENERATION_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes Added

- `RecommendationGenerationConfig`
- `RecommendationCandidateSource`
- `RecommendationCandidatePacket`
- `build_candidate_packet(...)`
- `generate_candidate_packets(...)`
- `candidate_sources_from_staples_report(...)`

## Schema Impact

None.

Phase 8H does not create tables, alter tables, insert recommendation runs, or insert recommendation candidates.

## Validation Command

Use the bundled Python runtime when system Python is unavailable:

```powershell
& "C:\Users\Main\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

Static checks:

```text
git diff --check
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|recommendation_runs|recommendation_candidates|execute\(|executescript\(|sqlite3" codie\recommendations
```

## Known Caveats / Review Notes

- GitHub remote is configured, but first push is still blocked on interactive GitHub HTTPS authentication.
- Phase 8H produces in-memory candidate packets only.
- Persistence is intentionally deferred to Phase 8I.

## Recommended Next Packet

Phase 8I - Recommendation Persistence And Rebuild Semantics.

## Phase 8I Objective

Persist validated recommendation candidate drafts through repository methods with deterministic rebuild semantics.

This phase must define:

- recommendation run creation
- candidate upsert or rebuild behavior
- transaction boundaries
- idempotency
- rollback behavior
- provenance JSON shape
- audit/report persistence rules

## Phase 8I Scope

Likely files:

- `codie/db/repositories/recommendations.py`
- `codie/recommendations/persistence.py`
- `tests/test_recommendation_persistence.py`
- `docs/PHASE8I_RECOMMENDATION_PERSISTENCE_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

Optional only if local code requires it:

- `codie/db/repositories/__init__.py`
- `codie/recommendations/__init__.py`

## Phase 8I Do Not Do

- Do not read provider/source tables.
- Do not call providers.
- Do not create recommendation text beyond evidence/audit outputs.
- Do not bypass repositories.
- Do not add strategic claim language.
- Do not implement UI/export surfaces.
- Do not implement simulator integration.

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
