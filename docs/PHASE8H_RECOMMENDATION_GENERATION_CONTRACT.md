# Phase 8H - Recommendation Candidate Generation Orchestration Contract

## Objective

Generate in-memory recommendation candidate packets from already computed canonical analytics inputs.

This phase composes existing recommendation primitives:

- evidence bundles
- score drafts
- candidate audit reports
- commander staples report rows

It does not persist recommendation candidates.

## Scope

Allowed files:

- `codie/recommendations/generation.py`
- `codie/recommendations/__init__.py`
- `tests/test_recommendation_generation.py`
- `docs/PHASE8H_RECOMMENDATION_GENERATION_CONTRACT.md`
- `docs/NEXT_PHASE_CONTRACT.md`

## Public Functions / Classes

- `RecommendationGenerationConfig`
- `RecommendationCandidateSource`
- `RecommendationCandidatePacket`
- `build_candidate_packet(...)`
- `generate_candidate_packets(...)`
- `candidate_sources_from_staples_report(...)`

## Inputs

Inputs must be precomputed canonical analytics or report outputs.

Allowed inputs:

- `CommanderStaplesReport`
- `StapleReportRow`
- explicit `RecommendationCandidateSource` records from canonical analytics

## Outputs

Outputs are in-memory only:

- `RecommendationCandidateDraft`
- `CandidateAuditReport`
- `RecommendationCandidatePacket`

## Schema Impact

None.

Do not write `recommendation_runs`.
Do not write `recommendation_candidates`.

## Required Behavior

- build evidence items with source attribution
- validate claim text through existing evidence rules
- build score input using existing score formula
- apply low-sample penalty
- build audit report with rank eligibility
- sort generated packets deterministically
- preserve source record IDs or URLs
- produce no strategic claims

## Failure Modes

- missing generated timestamp raises `ValueError`
- missing time window raises `ValueError`
- invalid sample threshold raises `ValueError`
- missing candidate identity raises `ValueError`
- missing evidence source reference raises `ValueError`
- invalid unit interval values raise `ValueError`

## Tests

Required tests:

- candidate packet creates draft and audit report
- generated packets sort deterministically
- low-sample candidates are marked not rank eligible
- commander staples report rows convert to candidate sources
- source record IDs are preserved
- invalid inputs fail cleanly
- no recommendation rows are created
- full suite passes

## Acceptance Criteria

```text
python -m unittest discover -s tests -v
```

must pass.

Static checks must remain clean:

```text
git diff --check
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|source_events|source_decks|source_deck_cards|source_primers|source_combos|provider_objects|Moxfield|Spellbook|moxfield|spellbook|recommendation_runs|recommendation_candidates|execute\(|executescript\(|sqlite3" codie\recommendations
```

## Do Not Do

- do not persist recommendation candidates
- do not create recommendation runs
- do not add schema
- do not read source/provider tables
- do not call providers
- do not invent strategic explanation language

## Follow-Up

Recommended next packet:

```text
Phase 8I - Recommendation persistence and rebuild semantics
```

Phase 8I must define repository write boundaries, rebuild semantics, idempotency, and rollback behavior before implementation.
