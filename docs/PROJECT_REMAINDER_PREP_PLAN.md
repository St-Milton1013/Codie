# Codie Remaining Project Preparation Plan

Date: 2026-06-21

## Current Checkpoint

Completed and validated:

- Phase 0: Reference preservation and constitution freeze.
- Phase 1: Schema and repository foundation.
- Phase 2: Scryfall truth layer.
- Phase 3: Provider candidate contracts and ingestion pipeline.
- Phase 4A: TopDeck adapter.
- Phase 4B: EDHTop16 adapter.
- Phase 4C: MTGTop8 adapter.

Current verification baseline:

- Full test suite: 73 tests passing.
- Provider boundary tests pass.
- No schema changes after Phase 1.
- No raw SQL outside `codie/db/bootstrap.py` and `codie/db/repositories/`.
- `beautifulsoup4==4.15.0` is recorded in `requirements.txt` for HTML adapters.

## Remaining Build Sequence

### Phase 4D - MTGDecks Adapter

Objective: Add secondary tournament/deck discovery while preserving mirror-risk boundaries.

Primary risk: MTGDecks may mirror events also present in TopDeck or MTGTop8. MTGDecks source records must not independently power analytics until canonical event/deck deduplication links or separates them.

Prepared contract:

- `docs/PHASE4D_MTGDECKS_ADAPTER_CONTRACT.md`

### Phase 4E - Hareruya Adapter

Objective: Add Japanese/regional tournament and deck source coverage.

Primary risk: Hareruya commander/deck page structure differs from MTGDecks and MTGTop8. Parser logic must use Hareruya-specific metadata and must not reuse MTGDecks sideboard heuristics for commander detection.

Prepared contract:

- `docs/PHASE4E_HARERUYA_ADAPTER_CONTRACT.md`

### Phase 5 - Canonicalization And Deduplication

Do not start analytics before this phase.

Objective: Convert source records into canonical events/decks while preserving provenance links.

Required deliverables:

- `codie/canonical/canonicalizer.py`
- `codie/canonical/deck_hash.py`
- `codie/canonical/event_matcher.py`
- repository methods for canonical events, decks, cards, commanders, and source links
- `tests/fixtures/canonicalization/event_dedupe_cases.json`
- `tests/fixtures/canonicalization/deck_hash_cases.json`
- `tests/test_canonicalization.py`

Core acceptance:

- Same event across sources dedupes into one `canonical_event`.
- Similar but distinct events do not dedupe incorrectly.
- Same 99/100 decklist hashes identically across providers.
- One-card difference changes deck hash.
- Auxiliary cards do not affect canonical deck hash.
- `canonical_event_sources` and `canonical_deck_sources` retain all provider provenance.
- Analytics eligibility is checked after canonicalization, not inside providers.

### Phase 6 - Tournament Weighting And Analytics Foundations

Objective: Build deterministic metrics from canonical records only.

Required deliverables:

- tournament weighting model
- card performance metric generation
- historical snapshot generation
- regional metric generation
- evidence count aggregation

Core acceptance:

- Analytics read canonical tables only.
- Formulas are deterministic and tested.
- Every metric records input window, source scope, generated timestamp, and sample-size guardrails.
- Duplicate source records do not double count after canonicalization.

### Phase 7 - Primer, Combo, And Package Evidence

Objective: Add non-tournament evidence sources without turning them into strategy claims.

Build order:

1. Commander Spellbook combo sync.
2. Moxfield primer metadata discovery.
3. cEDH DDB classification/primer reference.
4. Manual curated package definitions.
5. Archidekt primer metadata only after primary primer workflow is stable.

Core acceptance:

- Primer body is not stored.
- Combo lines are not invented.
- Package recommendations require curated or source-backed definitions.
- Evidence counts separate tournament, primer, combo, package, and simulation evidence.

### Phase 8 - Recommendations, Simulation, Evidence, And UI

Objective: Present evidence-backed outputs after canonical and evidence layers are reliable.

Build order:

1. Evidence layer and provenance bundle model.
2. Commander/card analytics pages.
3. Commander staples explorer.
4. Deck comparison.
5. Recommendation candidates.
6. Simulation engine and traces.
7. Evidence explorer and exports.
8. UI surfaces.

Core acceptance:

- Recommendation language is evidence-oriented, not strategic coaching.
- Simulation evidence appears only under the constitution thresholds.
- Every displayed metric has provenance.
- Exports do not mutate canonical data.

### Deferred Simulation And Knowledge Vault Extensions

Accepted future roadmap packet:

- `docs/ROADMAP_PATCH_SIMULATION_CHALLENGE_AND_KNOWLEDGE_VAULT.md`

Included extensions:

1. Simulation Challenge Mode.
2. Challenge Mode line review and veto annotations.
3. Simulation trace review Markdown/JSON export and annotation import.
4. Obsidian Knowledge Vault historical snapshots and internal linking.
5. Research Journals and future local retrieval support.

These items are roadmap-only. They do not authorize implementation or schema
changes. Build them only after the core Probability Simulation Engine and
immutable trace model are complete and validated. Human reviews remain QA
annotations and must not become tournament or recommendation evidence.

### Legacy Source Mining Backlog

Legacy Codie folders and archives may improve the current project only as
reference material. The useful upgrade candidates discovered so far are:

1. Deck parser edge-case fixtures from old sample decklists.
2. Commander alias candidates from old alias and nickname JSON files.
3. Provider fixture leads from old scraper attempts.
4. UI workflow ideas from the old desktop prototype.
5. Markdown, CSV, PDF, and Obsidian export formatting ideas.
6. Innovation threshold candidates from old project config.
7. Simulator and rules reference material for future probability work.

Forbidden uses:

- Do not copy old scraper code into live providers.
- Do not import old SQLite schemas or local databases as truth.
- Do not treat old staples reports or strategy text as evidence.
- Do not vendor old virtual environments, build folders, or third-party repos.
- Do not bypass the current contract, boundary, and test gates.

Any mined item must become either a fixture, a documented contract addition, or
a reviewed roadmap item before implementation.

### Deferred Mobile Report Access

Codie should eventually let the user run the program on a PC and view generated
reports on a phone.

Preferred low-priority path:

1. Generate static HTML, Markdown, or PDF reports from existing export surfaces.
2. Add a phone-readable report layout.
3. Generate a QR code for the report file or a local read-only report URL.
4. Optionally expose a read-only local network report URL.
5. Optionally send a Discord notification or message with a short summary and
   link/file, using explicit local configuration only.
6. Optionally support manual PDF-to-link service upload outside Codie when the
   user chooses to share a report that way.

Guardrails:

- Mobile access is read-only.
- The phone does not run Codie.
- No write access to SQLite is exposed.
- No cloud dependency is required for V1.
- Discord/webhook delivery is optional and must never hard-code secrets.
- External link services must not receive private deck data unless the user
  explicitly chooses that export.
- Report wording remains evidence-only.

## Persistent Quality Gate

Before each implementation phase:

- Define files created and modified.
- Define public functions/classes.
- Define schema impact.
- Define dependencies.
- Define test cases.
- Define failure modes.

Before closing each implementation phase:

- Run targeted tests.
- Run full test suite.
- Run provider boundary/static SQL checks when provider code changes.
- Confirm no schema drift unless explicitly approved.
- Return completion report with actual test output.

## Known Prep Gaps

- EDHTop16 fixtures are schema-shaped local samples, not live captures.
- MTGTop8 fixtures are local HTML samples, not live captures.
- MTGDecks and Hareruya still need captured/reference fixtures before implementation closure.
- No dependency management existed before `requirements.txt`; future third-party dependencies should be recorded there or moved to a stronger project packaging file.
- Canonicalization is now the next major architecture risk because it controls deduplication, analytics eligibility, and source provenance.
