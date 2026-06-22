# Phase 7B Moxfield Primer Metadata Contract

## Objective

Discover and persist Moxfield primer metadata without storing primer bodies, copying strategy text, generating recommendations, or making tournament claims.

Phase 7B is primer evidence only. It stores objective metadata, links back to source pages, preserves sanitized raw metadata, and updates primer evidence counts.

## Files Created

- `codie/providers/moxfield/__init__.py`
- `codie/providers/moxfield/client.py`
- `codie/providers/moxfield/models.py`
- `codie/providers/moxfield/parser.py`
- `codie/primers/__init__.py`
- `codie/primers/sync.py`
- `tests/fixtures/moxfield/deck_with_primer.json`
- `tests/fixtures/moxfield/deck_without_primer.json`
- `tests/fixtures/moxfield/missing_required.json`
- `tests/fixtures/moxfield/malformed_payload.json`
- `tests/fixtures/moxfield/source-notes.md`
- `tests/test_provider_moxfield.py`
- `tests/test_primer_sync.py`

## Files Modified

- `codie/db/repositories/source.py`
- `codie/db/repositories/curated.py`
- `codie/providers/models.py`
- `tests/test_architecture_boundaries.py`

## Schema Impact

None.

Existing tables used:

- `source_primers`
- `primer_registry`
- `evidence_counts`

## Public API

```python
class MoxfieldProvider(Provider):
    def fetch_deck(self, deck_id: str) -> dict: ...
    def parse_deck(self, raw: dict) -> SourcePrimerCandidate: ...

class PrimerMetadataSync:
    def sync_candidates(self, candidates: Iterable[PrimerCandidate]) -> PrimerSyncResult: ...

def score_primer_candidate(candidate: PrimerCandidate, *, generated_at: str) -> PrimerRankingScore: ...
```

## Provider Output

Moxfield provider emits:

- `RawPayload`
- `SourcePrimerCandidate`

Provider output is not persisted directly by the provider.

## Allowed Metadata

- Primer URL
- Deck URL
- author
- commander/partner text
- deck title
- primer title
- updated timestamps
- likes/views/comments
- tags
- bracket
- route/content presence booleans
- table-of-contents presence
- heading count
- section names
- external link count
- video count
- image count
- content length estimate
- objective quality score
- sanitized raw metadata JSON

## Forbidden Storage

- full primer body
- copied long primer sections
- strategy text
- mulligan guide text
- combo explanations copied from primer
- card-by-card strategic explanations copied from primer

## Dependencies

Provider allowed:

- Python standard library
- `codie.providers.base`
- `codie.providers.errors`
- `codie.providers.models`

Provider forbidden:

- `codie.db`
- repositories
- `sqlite3`
- `codie.ingestion`
- `codie.cards`
- `codie.analytics`
- `codie.recommendations`
- `codie.canonical`

Sync service allowed:

- `codie.db.repositories.source`
- `codie.db.repositories.curated`
- `codie.db.repositories.analytics`

## Failure Modes

- malformed payload raises `ParseError`.
- missing deck URL and deck identity raises `MissingRequiredFieldError`.
- missing primer route produces a candidate with `has_primer_route = 0`; sync may skip registry insertion but may store source metadata.
- body-like fields are stripped from raw metadata before persistence.
- repeated syncs upsert `primer_registry` by `primer_url`.
- primer registry commander keys use canonical alphabetical pipe-separated commander signatures.
- primer score output includes score, component breakdown, and generated_at for reproducibility.

## Acceptance Tests

- valid Moxfield fixture parses `SourcePrimerCandidate`.
- raw metadata is sanitized and does not include primer body text.
- missing optional fields are allowed.
- missing required deck identity fails cleanly.
- malformed payload fails cleanly.
- source primer metadata persists.
- primer registry upsert persists objective metadata.
- repeated syncs update the existing `primer_registry` row instead of creating duplicates.
- partner pairs match exactly, are order-insensitive, and do not collapse into single-commander records.
- evidence counts update primer evidence only.
- sync does not create recommendations, packages, or analytics metrics.
- provider boundary test passes.
- full suite passes.

## Do Not Do

- Do not store primer body.
- Do not summarize primer text.
- Do not infer strategy or archetype.
- Do not generate recommendations.
- Do not use Moxfield as tournament truth.
- Do not write SQLite from provider code.
