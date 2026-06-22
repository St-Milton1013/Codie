# Phase 5 Canonicalization And Deduplication Contract

## Objective

Implement canonicalization for source events and source decks after provider ingestion. Phase 5 converts source-layer records into canonical records, deduplicates equivalent events/decks across providers, and preserves all source provenance links.

Phase 5 is required before analytics, recommendations, historical snapshots, regional metrics, commander/card pages, evidence explorer, or UI work.

## Scope

Files to create:

- `codie/canonical/deck_hash.py`
- `codie/canonical/event_matcher.py`
- `codie/canonical/canonicalizer.py`
- `tests/fixtures/canonicalization/source-notes.md`
- `tests/fixtures/canonicalization/event_dedupe_cases.json`
- `tests/fixtures/canonicalization/deck_hash_cases.json`
- `tests/test_canonicalization.py`

Files to modify:

- `codie/db/repositories/canonical.py`
- `codie/db/repositories/source.py`

No schema changes are allowed unless explicitly approved with a migration plan. The existing Phase 1 canonical/source tables are sufficient for Phase 5.

## Existing Schema Surface

Canonical tables already available:

- `canonical_events`
- `canonical_event_sources`
- `canonical_decks`
- `canonical_deck_sources`
- `canonical_deck_cards`
- `canonical_deck_commanders`
- `event_deck_entries`
- `tournament_rounds`
- `match_results`

Source tables already available:

- `source_events`
- `source_decks`
- `source_deck_cards`
- `deck_auxiliary_cards`
- `provider_objects`

## Required Repository Extensions

`CanonicalRepository` currently supports inserts and links only. Add focused read/upsert helpers:

```python
class CanonicalRepository:
    def get_event_by_dedupe_key(self, dedupe_key: str): ...
    def get_deck_by_hash(self, deck_hash: str): ...
    def get_event_source_link(self, canonical_event_id: int, source_event_id: int): ...
    def get_deck_source_link(self, canonical_deck_id: int, source_deck_id: int): ...
    def update_event(self, canonical_event_id: int, updates: Mapping[str, Any]) -> None: ...
    def update_deck(self, canonical_deck_id: int, updates: Mapping[str, Any]) -> None: ...
```

`SourceRepository` currently supports inserts only. Add focused read/update helpers:

```python
class SourceRepository:
    def get_source_event(self, source_event_id: int): ...
    def get_source_deck(self, source_deck_id: int): ...
    def list_source_events_for_canonicalization(self): ...
    def list_source_decks_for_canonicalization(self): ...
    def list_source_deck_cards(self, source_deck_id: int): ...
    def update_source_event(self, source_event_id: int, updates: Mapping[str, Any]) -> None: ...
    def update_source_deck(self, source_deck_id: int, updates: Mapping[str, Any]) -> None: ...
```

All repository SQL stays inside `codie/db/repositories/`.

## Public Functions And Classes

```python
def normalize_event_name(name: str) -> str: ...
def event_dedupe_key(event: Mapping[str, Any]) -> str: ...
def event_match_confidence(left: Mapping[str, Any], right: Mapping[str, Any]) -> float: ...

def canonical_card_fingerprint(cards: Iterable[Mapping[str, Any]]) -> tuple[str, ...]: ...
def deck_hash(cards: Iterable[Mapping[str, Any]], commanders: Iterable[Mapping[str, Any]], *, format: str = "commander") -> str: ...
def commander_hash(commanders: Iterable[Mapping[str, Any]]) -> str: ...

class CanonicalizationResult: ...
class Canonicalizer:
    def canonicalize_event(self, source_event_id: int) -> CanonicalizationResult: ...
    def canonicalize_deck(self, source_deck_id: int) -> CanonicalizationResult: ...
    def canonicalize_pending(self) -> CanonicalizationResult: ...
```

## Event Canonicalization Rules

Event dedupe key inputs:

- normalized event name
- event date if available
- format if available
- country/region if available
- venue/store if available

Rules:

- Same provider event imported twice links to the same canonical event.
- Same event represented by multiple providers links to one canonical event when dedupe key and confidence threshold match.
- Similar names with different dates must not dedupe.
- Similar names in different regions/countries must not dedupe unless other fields provide strong evidence.
- Missing optional fields lower confidence but do not fail if event identity is present.
- `canonical_event_sources` must preserve every source event link.
- `source_events.canonical_event_id` and `source_events.dedupe_status` must be updated after canonicalization.

Do not use provider priority as an independent event count. Provider priority may inform merge confidence only.

## Deck Canonicalization Rules

Deck hash inputs:

- resolved `scryfall_id`
- quantity
- canonical source zone
- commander set
- format profile

Rules:

- Same 99/100 decklist from different providers hashes identically.
- One-card difference changes deck hash.
- Card order does not affect deck hash.
- Mainboard/commander zones affect deck hash.
- Auxiliary cards do not affect deck hash.
- Duplicate cards aggregate quantities before hashing.
- Commanders must populate `canonical_deck_commanders`.
- Main deck and commander cards must populate `canonical_deck_cards`.
- `canonical_deck_sources` must preserve every source deck link.
- `source_decks.canonical_deck_id` and `source_decks.dedupe_status` must be updated after canonicalization.

Unresolved source cards block canonical deck creation by default. The failure must be explicit and non-silent.

## Event Deck Entries

When both a source deck and source event are canonicalized:

- create or update `event_deck_entries`
- link `canonical_event_id`
- link `canonical_deck_id`
- preserve `source_deck_id`
- preserve pilot, placement, placement label, and record text

Do not calculate tournament weights in Phase 5. `entry_weight` remains default until the tournament weighting phase.

## Source Classification Rules

- Providers remain fetch/parse only.
- Canonicalization is where source records become analytics candidates.
- MTGDecks remains mirror-risk until dedupe links or separates it.
- EDHTop16, MTGTop8, MTGDecks, and Hareruya are analytics eligible only after canonicalization.
- Moxfield/Archidekt user or primer data must not enter tournament canonicalization.

## Failure Modes

- Missing source event/deck: structured failure.
- Missing source identity: structured failure.
- Unresolved source card: structured failure.
- Invalid quantity: structured failure.
- No commander for commander-format deck: structured failure unless source explicitly lacks commander and project policy accepts deferred curation.
- FK failures must remain visible.
- Duplicate link attempts must be idempotent.

## Test Cases

Add `tests/test_canonicalization.py` with:

- event dedupe key deterministic.
- same event across TopDeck and MTGDecks dedupes.
- same event imported twice is idempotent.
- similar event name on different date does not dedupe.
- similar event name in different country does not dedupe.
- deck hash deterministic across provider order differences.
- one-card difference changes deck hash.
- auxiliary card difference does not change deck hash.
- duplicate card quantities aggregate.
- commander hash uses normalized alphabetical pipe-separated signature.
- canonical deck cards persist.
- canonical commanders persist.
- source event/deck records get canonical IDs and `dedupe_status`.
- event deck entry is created when event and deck are both canonicalized.
- unresolved source card blocks deck canonicalization.
- raw provider payloads are not modified.
- no raw SQL outside repositories.

## Validation Commands

```text
python -m unittest tests.test_canonicalization -v
python -m unittest discover -s tests -v
rg -n "execute\(|executescript\(|sqlite3" codie --glob "!codie/db/**"
```

## Do Not Do

- Do not implement analytics.
- Do not calculate tournament weights.
- Do not generate recommendations.
- Do not build UI.
- Do not let providers write canonical data.
- Do not alter Scryfall card truth.
- Do not silently canonicalize unresolved cards.

## Completion Report Requirements

Return:

- Files created
- Files modified
- Public functions/classes
- Schema impact
- Tests added
- Tests run
- Actual test output
- Static check output
- Known limitations
- Recommended next step
