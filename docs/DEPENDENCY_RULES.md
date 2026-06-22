## 8. DEPENDENCY RULES

### 8.1 Allowed Import Direction

```text
providers → provider models/errors only
providers → no db, no repositories, no analytics

ingestion → providers
ingestion → canonical normalization helpers
ingestion → repositories

canonical → repositories
canonical → cards lookup
canonical → curated aliases
canonical → signature generation

analytics → repositories read methods
analytics → canonical read models

recommendations → repositories read methods
recommendations → analytics read models
recommendations → canonical read models

probability_engine → cards read models
probability_engine → user/source deck inputs
probability_engine → simulation_repo for persistence

pages → repositories read methods
pages → analytics read methods
pages → evidence read methods

ui → application services / repositories read methods
ui → never raw SQL
```

### 8.2 Forbidden Imports

```text
providers importing db.*
providers importing repositories.*
providers importing analytics.*
providers importing recommendations.*
ui importing sqlite3 directly
recommendations writing canonical data
curated systems mutating Scryfall card truth
old archived code importing new production code
```

### 8.3 Ownership Boundaries

| Domain | Owns | Does Not Own |
|---|---|---|
| `cards/` | Scryfall‑normalized card data, card lookup, oracle cache | Tournament records, recommendations |
| `providers/` | Fetching/parsing external source payloads | Persistence, canonicalization, analytics |
| `ingestion/` | Pipeline orchestration and persistence of source records | Source‑specific business rules outside provider contracts |
| `canonical/` | Deduplication, deck hashes, normalized canonical records, commander signatures | Raw provider payload fetching |
| `curated/` | Maintainer registries and labels | Source truth, analytics truth |
| `analytics/` | Metrics from canonical events/decks | Raw scraping, strategy claims |
| `recommendations/` | Evidence‑backed candidate generation | Strategy claims |
| `probability_engine/` | Reproducible simulation | Full MTG rules engine |
| `pages/` | Commander and card page rendering | Data ownership |
| `evidence/` | Unified presentation of evidence | Claim invention |
| `ui/` | Display and user workflow | Data ownership |

