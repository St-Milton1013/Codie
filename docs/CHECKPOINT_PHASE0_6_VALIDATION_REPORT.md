# Codie V1 Checkpoint Validation Report - Phases 0-6

## Verdict

```text
Phase 0: PASS
Phase 1: PASS
Phase 2: PASS
Phase 3: PASS
Phase 4A TopDeck: PASS
Phase 4B EDHTop16: PASS
Phase 4C MTGTop8: PASS
Phase 4D MTGDecks: PASS
Phase 4E Hareruya: PASS WITH LIVE-FETCH CAVEAT
Phase 5 Canonicalization: PASS
Phase 6 Analytics Foundations: PASS

Overall: PASS WITH REVIEW NOTES
```

The codebase is ready for outside validation before Phase 7. The remaining caveats are not test failures; they are source-access and interpretation items that should be reviewed before broad data backfill.

## Repository State

```text
Branch: main
Validated implementation commit: 569f1ab Fix Hareruya live page parsing
Tracked files: 162
Working tree at validation start: clean
```

Recent commits:

```text
569f1ab Fix Hareruya live page parsing
a1605bc Add analytics foundation metrics
51d863c Initial Codie architecture baseline
```

No Git remote is configured yet.

## Validation Commands

### Full Test Suite

Command:

```text
python -m unittest discover -s tests
```

Actual output:

```text
.........................................................................................................................
----------------------------------------------------------------------
Ran 121 tests in 0.216s

OK
```

### Architecture Boundary Tests

Command:

```text
python -m unittest tests.test_architecture_boundaries -v
```

Actual output:

```text
test_analytics_do_not_import_provider_or_source_layers ... ok
test_analytics_repository_does_not_query_source_tables ... ok
test_no_live_network_dependency_in_scryfall_layer ... ok
test_providers_do_not_import_database_or_repositories ... ok
test_sqlite_imports_stay_inside_db_package_or_tests ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.053s

OK
```

### Static Boundary Checks

Raw SQL or SQLite imports outside `codie/db`:

```text
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
```

Result:

```text
no matches
```

Forbidden provider imports:

```text
rg -n "from codie\.db|import codie\.db|import sqlite3|from .*repositories|import .*repositories|codie\.ingestion|codie\.cards|codie\.analytics|codie\.recommendations|codie\.canonical" codie\providers
```

Result:

```text
no matches
```

Analytics source/provider leakage:

```text
rg -n "codie\.providers|codie\.ingestion|codie\.db\.repositories\.source|FROM source_events|JOIN source_events|FROM source_decks|JOIN source_decks|FROM source_deck_cards|JOIN source_deck_cards|FROM provider_objects|JOIN provider_objects" codie\analytics codie\db\repositories\analytics.py
```

Result:

```text
no matches
```

Network-call hygiene outside provider clients:

```text
rg -n "urlopen\(|requests\.|httpx\.|Invoke-WebRequest|urllib\.request" tests codie --glob "!codie/providers/*/client.py" --glob "!tests/test_architecture_boundaries.py"
```

Result:

```text
no matches
```

## Phase Summary

### Phase 0 - Constitution And Reference Layout

Status: PASS

Completed:

- Constitution saved as `docs/CODIE_V1_CONSTITUTION.md`.
- Frozen dependency and ingestion docs saved.
- Reference folder tree created under `reference/`.
- Phase contracts created for implemented phases.

Important files:

- `docs/CODIE_V1_CONSTITUTION.md`
- `docs/SCHEMA_SPEC.md`
- `docs/DEPENDENCY_RULES.md`
- `docs/INGESTION_CONTRACTS.md`

### Phase 1 - Schema And Repository Foundation

Status: PASS

Completed:

- SQL schema split across domain files.
- Bootstrap loads schema files in deterministic order.
- Foreign keys enabled through connection/bootstrap helpers.
- Repository layer created for core, source, canonical, analytics, regional, curated, simulation, and user domains.
- `scryfall_id` remains enforced card identity.
- `oracle_id` remains a grouping key, not an enforced unique card identity.

Important files:

- `codie/db/schema/*.sql`
- `codie/db/bootstrap.py`
- `codie/db/connection.py`
- `codie/db/pragmas.py`
- `codie/db/repositories/*.py`
- `tests/test_schema.py`

### Phase 2 - Scryfall Truth Layer

Status: PASS

Completed:

- Local Scryfall bulk/fixture parsing.
- Card model preserves raw JSON.
- Card lookup and normalization helpers added.
- No live network dependency in Scryfall layer.
- Tests cover malformed payloads, missing fields, MDFC/card faces, commander legality, produced mana, aliases, fuzzy lookup behavior, and raw payload preservation.

Important files:

- `codie/providers/scryfall/`
- `codie/cards/`
- `tests/test_scryfall_truth.py`
- `tests/fixtures/scryfall/`

### Phase 3 - Provider Ingestion Pipeline

Status: PASS

Completed:

- Provider base class, candidate models, and structured errors.
- Ingestion validation helpers.
- Ingestion pipeline performs fetch -> parse -> validate -> resolve cards -> persist through repositories.
- Atomic ingestion behavior prevents partial deck records after card-resolution failure.
- Providers do not import repositories, DB modules, analytics, canonicalization, or cards.

Important files:

- `codie/providers/base.py`
- `codie/providers/models.py`
- `codie/providers/errors.py`
- `codie/ingestion/pipeline.py`
- `codie/ingestion/validation.py`
- `tests/test_ingestion_pipeline.py`
- `tests/test_architecture_boundaries.py`

### Phase 4 - Provider Adapters

Status: PASS

Implemented adapters:

- TopDeck
- EDHTop16
- MTGTop8
- MTGDecks
- Hareruya

Completed:

- Adapters fetch/parse only.
- Adapters emit candidate models only.
- Raw payloads are preserved.
- Tests use fixtures and injected transports.
- No live network dependency in tests.
- Provider boundary tests pass.

Important files:

- `codie/providers/topdeck/`
- `codie/providers/edhtop16/`
- `codie/providers/mtgtop8/`
- `codie/providers/mtgdecks/`
- `codie/providers/hareruya/`
- `tests/test_provider_*.py`
- `tests/fixtures/*/`

Hareruya update:

- Added sanitized live-shape fixture for `https://www.hareruyamtg.com/en/deck/7/metagame/`.
- Added sanitized live-shape fixture for `https://www.hareruyamtg.com/en/deck/100000/show/`.
- Parser now supports current Hareruya `deckSearch-*` metagame/decklist structures.
- Hareruya `202` AWS WAF challenge is mapped to retryable `RateLimitError`.

Review note:

- Live `deck/result` pages may return an AWS WAF challenge to simple HTTP clients. The adapter handles this cleanly as retryable, but broad Hareruya backfill may require a capture strategy that respects site access constraints.

### Phase 5 - Canonicalization

Status: PASS

Completed:

- Event dedupe keys.
- Deck hash generation.
- Commander hash generation with alphabetical pipe-separated signatures.
- Source event/deck records link to canonical records.
- Canonical event/deck source provenance preserved.
- `event_deck_entries` generated when both event and deck are canonicalized.
- Unresolved source cards block canonical deck creation explicitly.
- Canonicalization is idempotent.
- Raw provider payloads are not modified.

Important files:

- `codie/canonical/event_matcher.py`
- `codie/canonical/deck_hash.py`
- `codie/canonical/canonicalizer.py`
- `tests/test_canonicalization.py`
- `tests/fixtures/canonicalization/`

Review note:

- Canonicalization currently uses conservative deterministic event keys. Outside review should check whether the chosen event key fields are too strict for real-world duplicated events.

### Phase 6 - Analytics Foundations

Status: PASS

Completed:

- Deterministic tournament weighting functions:
  - event size
  - placement
  - recency
  - source confidence
  - decklist completeness
  - final entry weight
- Analytics builder reads canonical records only.
- Duplicate mirror/source records are collapsed before card metric aggregation.
- Card performance metrics generated.
- Historical snapshots and historical card metrics generated.
- Regional card metrics generated.
- Evidence counts updated.
- Entry weights persisted to `event_deck_entries.entry_weight`.

Important files:

- `codie/analytics/weights.py`
- `codie/analytics/foundations.py`
- `codie/db/repositories/analytics.py`
- `codie/db/repositories/regional.py`
- `tests/test_analytics_foundations.py`
- `tests/fixtures/analytics/`

Review note:

- The implementation follows the written constitution formula:

```text
event_size_weight = clamp(log2(player_count) / log2(128), 0.25, 1.50)
```

The constitution's nearby prose examples appear inconsistent with that formula for 16/32/64-player events. Outside review should decide whether the formula or examples should be amended.

## Known Caveats

```text
No Git remote is configured.
No CI workflow is configured yet.
No Phase 7 evidence-source implementation yet.
Hareruya deck/result live pages may WAF-challenge basic clients.
Phase 6 follows the written event-size formula despite inconsistent prose examples.
TopDeck API key is not committed; local probe scripts remain ignored under work/.
```

## Outside Reviewer Prompt

```text
Validate Codie V1 Phase 0-6 work against docs/CODIE_V1_CONSTITUTION.md.

Validated implementation commit:
569f1ab Fix Hareruya live page parsing

If this checkpoint report has been committed after validation, treat that later commit as report-only unless it includes code changes.

Run:
python -m unittest discover -s tests
python -m unittest tests.test_architecture_boundaries -v

Also check:
1. Providers do not import codie.db, repositories, sqlite3, ingestion, cards, analytics, recommendations, or canonical.
2. Providers fetch/parse only and emit candidate models only.
3. Raw payload preservation exists for provider and Scryfall records.
4. Scryfall identity uses scryfall_id as enforced card identity.
5. oracle_id is used as analytics grouping key, not unique card identity.
6. Ingestion is atomic and does not leave partial deck records after resolution failure.
7. Canonicalization reads source records and writes canonical records through repositories.
8. Canonicalization preserves source provenance links and does not modify raw provider payloads.
9. Duplicate source/provider deck records do not double count in Phase 6 analytics.
10. Analytics reads canonical tables only, not source/provider tables.
11. Hareruya live-shape fixtures match current Hareruya DOM assumptions.
12. Hareruya WAF challenge handling is acceptable for retryable live-fetch failure.
13. Phase 6 event-size weighting should follow either the written formula or prose examples; flag any required constitution correction.

Return:
PASS / PASS WITH REQUIRED FIXES / FAIL

Then list required fixes before Phase 7.
```

## Recommended Next Step

Do outside validation now. If accepted, start Phase 7A: Commander Spellbook combo evidence sync.

Phase 7A should remain evidence-only:

- no recommendations
- no analytics claims from combo data
- no provider DB writes
- raw payload preservation
- Scryfall/card identity resolution through existing card layer
- evidence count updates only after validated persistence
