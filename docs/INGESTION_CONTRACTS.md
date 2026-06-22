## 12. INGESTION CONTRACTS

### 12.1 Provider Output Models

Providers return candidates. They do not persist.

```text
RawPayload
SourceEventCandidate
SourceDeckCandidate
SourceDeckCardCandidate
SourcePrimerCandidate
SourceComboCandidate
```

**Minimum `SourceEventCandidate`:**
```text
provider
provider_event_id
source_url
original_source
original_source_url
event_name
event_date
format
region
country
store_tag
language
player_count
deck_count
raw_payload
```

**Minimum `SourceDeckCandidate`:**
```text
provider
provider_deck_id
source_event_key
source_url
download_url
deck_title
commander_text
pilot_name
rank
rank_label
record
win_rate
archetype_name
raw_payload
```

**Minimum `SourceDeckCardCandidate`:**
```text
source_deck_key
raw_name
quantity
source_zone
source_order
raw_entry
```

**Minimum `SourcePrimerCandidate`:**
```text
provider
primer_url
deck_url
commander_text
partner_text
deck_title
primer_title
author
updated_at
likes
views
comments
objective_metadata
raw_payload
```

### 12.2 Pipeline Flow

```text
provider.fetch()
→ provider.parse()
→ ingestion.validate_candidate()
→ cards.card_lookup.resolve()
→ source_repo.upsert_source_records()
→ canonicalizer.match_or_create()
→ canonical_repo.link_sources()
→ analytics snapshots refresh by explicit command
```

### 12.3 Failure Behavior

All failures must be captured as structured records:

```text
provider
pipeline
source_url
object_type
error_type
error_message
raw_payload_hash
occurred_at
retryable
```

**Failure classes:**
```text
NetworkError
RateLimitError
ParseError
MissingRequiredFieldError
CardResolutionError
SchemaValidationError
CanonicalizationConflict
DuplicateAmbiguityError
```

### 12.4 Canonicalization Requirements

**Event dedupe keys use:**
```text
normalized_event_name
event_date
format
country/region
player_count tolerance
source original URL
provider event ID
```

**Deck hash uses:**
```text
commander oracle IDs sorted
mainboard oracle IDs + quantities sorted
format profile
excluded auxiliary cards
normalized zones
```

**Card resolution order:**
```text
exact Scryfall name match
alias registry match
Scryfall fuzzy endpoint or local fuzzy cache
manual unresolved queue
```

