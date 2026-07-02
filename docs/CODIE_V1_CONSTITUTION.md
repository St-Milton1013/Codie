# CODIE V1 CONSTITUTION — DEFINITIVE MASTER ARCHITECTURE, GOVERNANCE, ROADMAP, AND HANDOFF

**Version:** 1.2 Final Constitution with Implementation Quality Gate  
**Date:** 2026-06-20  
**Status:** Implementation Ready – Roadmap Freeze  
**Replaces:** Every previous roadmap, governance file, architecture note, patch, status document, and handoff document.

---

## TABLE OF CONTENTS

1. Executive Summary
2. Product Identity
3. Governance Rules
4. Source Classification Matrix
5. Approved Source Catalog
6. GitHub Reference Catalog
7. Package Structure
8. Dependency Rules
9. Four‑Layer Data Architecture
10. Database Specification
11. Commander Signature Definition
12. Ingestion Contracts
13. Tournament Weighting Model
14. Card Performance Metrics Layer
15. Historical Snapshot System
16. Evidence Count Aggregation Layer
17. Recommendation Engine
18. Probability Simulation Engine
19. Primer Discovery & Indexing
20. Combo & Package Intelligence
21. Commander Intelligence Pages
22. Card Intelligence Pages
23. Commander Staples Explorer
24. Deck Comparison System
25. Evidence Explorer
26. Unified Evidence Layer
27. Evidence Stack UI Concept
28. Natural Language Query Helper
29. Export & Obsidian Integration
30. UI Technology Decision
31. Fixture Catalog
32. Acceptance Test Matrix
33. Implementation Quality Gate
34. Build Order
35. Immediate Next Tasks
36. AI Handoff Instructions
37. Conflict Resolution Log
38. Unresolved Items

---

## 1. EXECUTIVE SUMMARY

### 1.1 What Codie Is

Codie is a **local‑first competitive Commander, cEDH, evidence and intelligence platform**. It is designed for 1 to 3 trusted users, not public SaaS, not enterprise cosplay, and not another deckbuilder wearing analytics glasses.

Codie exists beside Moxfield, Archidekt, TopDeck, EDHTop16, MTGTop8, MTGDecks, Hareruya, Commander Spellbook, cEDH Decklist Database, Scryfall, and other public resources. Its job is to pull evidence from those sources, preserve the raw source material, normalize it, deduplicate it, calculate reproducible metrics, and present the results in one local system.

**Codie must not become an AI strategy oracle.** That path leads straight to confident nonsense, which software already produces without the extra branding effort.

### 1.2 Locked Product Identity

```text
Codie = Tournament Intelligence
      + Evidence Recommendation Engine
      + Source Recommendation Engine
      + Simulation Engine
      + Primer Discovery
      + Combo Intelligence
      + Package Intelligence
      + Card Performance Analytics
      + Historical Meta Intelligence
      + Unified Evidence Layer
      + Commander Intelligence Pages
      + Card Intelligence Pages
      + Evidence Stack Visualization
      + Evidence Explorer
      + Deck Comparison
```

### 1.3 Questions Codie Answers

```text
What evidence exists?
Where did it come from?
How strong is it?
How recent is it?
How reproducible is it?
What source links support it?
What does the simulator show under explicit assumptions?
What cards, packages, primers, and combos are linked by evidence?
What is this commander's meta share?
What cards are growing or declining in usage?
How much evidence supports this card or commander?
What is the provenance of this metric?
```

### 1.4 Questions Codie Does NOT Answer

```text
What does this deck "mean"?
What is the correct strategy?
What is the pilot supposed to do?
What archetype did the AI hallucinate after seeing three blue cards?
```

The user interprets. Codie brings receipts.

---

## 2. PRODUCT IDENTITY

### 2.1 Codie Is

Codie is a local‑first cEDH evidence platform that:

1. Imports decklists from text, Moxfield, TopDeck, EDHTop16, MTGTop8, MTGDecks, Hareruya, and future approved sources.
2. Normalizes every card through Scryfall.
3. Preserves raw source payloads.
4. Deduplicates tournament events and deck instances across providers.
5. Separates source records from canonical analytics records.
6. Tracks tournament evidence, regional evidence, historical evidence, and card‑performance evidence.
7. Discovers primers and stores only metadata and source links.
8. Detects known combos and combo completion from Commander Spellbook.
9. Detects packages only from explicit package definitions.
10. Produces evidence‑backed recommendation candidates.
11. Runs reproducible probability simulations with action traces.
12. Supports a two‑screen workflow:

```text
Screen 1: Moxfield / Archidekt / active deck editor
Screen 2: Codie evidence dashboard
```

### 2.2 Codie Is Not

```text
A visual deckbuilder
A deck hosting platform
A collection manager
A card marketplace
A price‑alert system
A social deck network
A full Magic rules engine
A casual EDH recommender
A Reddit or Discord opinion scraper
An AI strategy coach
A primer replacement
An archetype guesser
A public SaaS product
```

### 2.3 Main User Workflow

1. User enters deck text or URL.
2. Codie imports the deck into a temporary user‑analysis context unless the deck came from an approved source ingestion pipeline.
3. Codie normalizes cards via Scryfall.
4. Codie shows source evidence:

```text
Commander evidence
Tournament evidence
Card inclusion evidence
Card performance evidence
Primer links
Combo evidence
Package evidence
Simulation results
Historical meta context
Regional meta context
Potential recommendation candidates
Potential low‑evidence/outlier cards
Evidence Stack visualization
Evidence Explorer details
Deck comparison options
```

5. User returns to Moxfield or another deckbuilder to edit. Codie does not edit the deck for them.

---

## 3. GOVERNANCE RULES

These rules override implementation convenience.

### Rule 1 — Zero Cost Requirement

Codie must remain 100% free.

**Forbidden unless explicitly reapproved:**
```text
Paid APIs
Paid SaaS
Paid datasets
Subscriptions
Commercial SDKs
Cloud services requiring payment
Premium analytics services
Pay‑per‑run scraper services
```

**Preferred:**
```text
Local SQLite
Local file storage
Open‑source libraries
Self‑hosted tools
Free public APIs
Free public datasets
Free browser/manual capture when no stable API exists
```

If a feature cannot work without payment, it is rejected unless there is no plausible free alternative and the roadmap explicitly records the exception.

### Rule 2 — No Partial Implementations

No code should be returned as:

```text
Pseudocode
Skeleton files
Placeholder functions
TODO‑only files
Half modules
Undefined imports
"finish this yourself" sections
```

Code is complete only when:

```text
Feature implemented
Code compiles
Imports resolved
Integration points identified
Known errors addressed
File placement specified
Validation performed
Failure behavior documented
```

### Rule 3 — Completion Reports

Every completed task must end with a report containing:

```text
Task Name
Objective
Files Created
Files Modified
Work Completed
Design Decisions
Validation Performed
Issues Found
Recommended Next Step
Roadmap Impact
```

### Rule 4 — AI Responsibility Model

**ChatGPT** — Primary role: project organization and architecture hub.

Responsibilities:
```text
Roadmap maintenance
Architecture planning
Project organization
Source classification
Research synthesis
Handoff generation
Prioritization
Dependency tracking
Conflict resolution
Implementation sequencing
```

**Claude** — Primary role: architecture validation and continuity checking.

Responsibilities:
```text
Architecture validation
Conflict detection
Consistency checking
Dependency analysis
Roadmap verification
Handoff review
Scope‑drift detection
```

**DeepSeek** — Primary role: implementation and refactor engine.

Responsibilities:
```text
Complete file generation
Database implementation
Parser implementation
Provider adapters
Refactors
Testing support
Bug fixing
Performance cleanup
```

DeepSeek implements locked contracts. Does not design schema semantics from vibes.

### Rule 5 — Roadmap First

No major implementation begins before:

```text
Requirement documented
Roadmap placement exists
Dependencies identified
Data flow understood
Acceptance tests defined
Schema impact understood
Failure behavior specified
```

### Rule 6 — Source Preservation

All research must be preserved under `reference/`.

**Required reference folders:**
```text
reference/recommander/
reference/cedhdata_simulator/
reference/rhystic_simulator_traces/
reference/moxfield/
reference/ddb/
reference/topdeck/
reference/edhtop16/
reference/mtgtop8/
reference/mtgdecks/
reference/hareruya/
reference/spellbook/
reference/github_repos/
reference/ux_references/
reference/old_code_archives/
```

Raw research is not production code. It is evidence, fixtures, traces, notes, screenshots, exports, and validation material.

### Rule 7 — Canonical Data Rule

**Required flow:**
```text
Source Data → Normalization → Canonical Records → Analytics
```

Raw provider data never powers analytics.

Provider data first becomes:
```text
source_events
source_decks
source_deck_cards
source_primers
source_combos
```

Then Codie derives:
```text
canonical_events
canonical_decks
canonical_deck_cards
canonical_deck_commanders
```

Only canonical records power analytics.

### Rule 8 — Documentation Requirement

Every subsystem must document:

```text
Purpose
Inputs
Outputs
Dependencies
Tables used
Acceptance tests
Failure modes
Data ownership
Import boundaries
```

### Rule 9 — Testing Requirement

Every feature requires:

```text
Unit tests
Parser tests
Database verification
Error handling verification
Fixture‑based regression tests
At least one negative/failure‑path test
```

### Rule 10 — Evidence First Rule

Codie stores, normalizes, links, calculates, and presents evidence.

**Allowed derived metrics:**
```text
Inclusion rate
Lift score
Confidence score
Similarity score
Placement weighting
Win‑rate delta
Top‑cut conversion rate
Tournament adoption rate
Regional usage
Recency‑weighted usage
Probability simulation results
Package completion against stored package definitions
Combo component presence from Commander Spellbook data
Meta share
Weighted meta share
Growth rate
Evidence counts
Historical trends
```

**Not allowed unless source‑provided, user‑provided, or curated‑registry‑provided:**
```text
Strategy inference
Archetype inference
Primer interpretation
AI strategic conclusions
"This deck is Turbo"
"This card fits your game plan"
"This deck wants to win through X"
"This primer teaches Y"
```

**Allowed phrasing:**
```text
DDB labels this list as X.
Moxfield tags include X.
User label: X.
Primer title includes X.
Tournament source reports X.
Commander Spellbook lists combo X.
Card appears in 73% of comparable decks.
Card has lift score 2.1 for this commander.
Card improves simulated target access by X percentage points under this model.
Evidence Stack shows 421 tournament decks, 17 primers, 4 packages, 18 simulations.
```

**Forbidden phrasing:**
```text
This is the correct card.
This card is wrong.
This deck is definitely midrange.
This proves the deck should mulligan aggressively.
```

### Rule 11 — Codie Is Not A Deckbuilder

**Out of scope:**
```text
Deck editing
Drag/drop builder
Collection management
Deck hosting
Deck publishing
Social features
Public deck‑sharing platform features
```

**In scope:**
```text
Deck import
Temporary deck analysis
Tournament intelligence
Evidence‑backed recommendations
Simulation
Primer discovery
Combo discovery
Package discovery
Card performance analytics
Evidence aggregation
Source linking
Metric calculation
Commander Intelligence Pages
Card Intelligence Pages
Evidence Stack visualization
Evidence Explorer
Deck Comparison
```

### Rule 12 — Crucial‑Only Roadmap Changes

Nothing should be added to the roadmap unless it solves a real project problem.

New roadmap additions must explain:

```text
Problem solved
System affected
Dependency unlocked
Why existing tools are insufficient
Acceptance test impact
```

### Rule 12A — Legacy Source Mining Is Reference‑Only

Legacy Codie folders, uploaded archives, old scripts, old local databases, and
old AI implementation attempts may be mined for:

```text
deck parser edge-case fixtures
commander alias candidates
provider fixture leads
UI workflow ideas
export/report formatting ideas
Obsidian vault export planning
innovation detection threshold candidates
simulator/rules reference material
```

Legacy material must not be copied into production modules directly.

Before any legacy idea becomes implementation work, it must pass the normal
contract gate:

```text
current architecture placement
files created or modified
schema impact
boundary impact
test cases
failure modes
license or source review if third-party material is involved
```

Old code remains quarantined reference material unless explicitly migrated
through Codie's current architecture. Legacy reports, strategy text, and old
analysis outputs are not evidence and must not be treated as analytics truth.

### Rule 13 — Raw Payload Preservation

Every externally sourced object must preserve its raw payload or raw source artifact reference.

**Minimum fields:**
```text
provider
provider_object_type
provider_id
source_url
retrieved_at
raw_payload_json or raw_file_path
payload_hash
```

### Rule 14 — Providers Never Write Directly To DB

Providers fetch and parse only.

**Allowed provider output:**
```text
SourceEventCandidate
SourceDeckCandidate
SourceDeckCardCandidate
SourcePrimerCandidate
SourceComboCandidate
RawPayload
```

**Forbidden:**
```text
providers importing repositories
providers opening SQLite connections
providers mutating canonical records
providers calculating analytics
```

### Rule 15 — Repository Layer Required

All persistence routes through repositories.

**Allowed direction:**
```text
ingestion pipeline → repository → SQLite
canonicalizer → repository → SQLite
analytics → repository read methods → SQLite
```

**Forbidden:**
```text
random SQL inside semantic systems
random SQL inside providers
random SQL inside UI
random SQL inside recommendation engine
```

### Rule 16 — Deck Identity Rule

**Source deck identity:**
```text
One URL/source submission/event entry = one source_deck record.
```

**Canonical deck identity:**
```text
One normalized cardlist hash + commander set + format profile = one canonical_deck record.
```

Therefore:
```text
Two identical lists from two different events = two source_decks linked to one canonical_deck.
One source URL edited later = new source snapshot if card contents change.
Any normalized card change = new deck_hash.
Deck hashes are immutable.
```

### Rule 17 — Card Identity Rule

Codie stores both:

```text
scryfall_id = primary printing/card object identifier for exact imported card records
oracle_id = functional identity for grouping printings and analytics where print variants should collapse
```

**Default references:**
```text
deck_cards.scryfall_id for exact normalized card
analytics grouped by oracle_id unless printing‑specific analysis is explicitly requested
cards.scryfall_id is the table primary key
cards.oracle_id is indexed and required when Scryfall provides it
```

### Rule 18 — Schema Freeze Rule

After Phase 1 (Schema and Repository Foundation) is complete and accepted, no table redesign shall occur without:

```text
Architecture review
Migration plan
Acceptance‑test impact review
Roadmap update
Explicit approval from ChatGPT (architecture hub)
```

This rule prevents the “schema churn” that plagues every AI‑driven project. Once the schema is frozen, changes must be additive (new columns with defaults, new tables) rather than destructive.

### Rule 19 — Provenance Rule

Every derived metric must be traceable. Every metric shown in the UI must provide:

```text
formula
input datasets
time window
sample size
generated_at
source attribution
```

No metric may exist without reproducible lineage. This is the philosophical core of Codie.

### Rule 20 — Implementation Quality Rule

Codie implementation must be **contract‑first, fixture‑tested, deterministic, and architecture‑compliant**.

No code is accepted merely because it runs once.

A task is complete only when it includes:
- Complete files (no stubs)
- Unit and integration tests
- Actual test validation output
- Architecture compliance notes
- A completion report

### Rule 43 - Tag Graph Lab

Codie supports a future Tag Graph Lab for graphing deck and commander data by
functional tags.

Primary tag source:

```text
Scryfall Tagger
```

Secondary tag sources:

```text
Curated Functional Registry
Role Fusion Engine
User corrections
```

Purpose:

```text
allow users to select one to six functional tags and graph frequency, adoption,
density, and trend across decks, commanders, time windows, regions, tournament
results, and frequency pools
```

Required rules:

```text
all tag graphs are generated from canonical card identities
Scryfall Tagger tags map to oracle_id
graphs expose underlying card lists
graphs expose underlying numeric tables
tags preserve source provenance
user decks never enter commander averages
frequency pool graphs show the deck pool used
low sample and low tag coverage are labeled
tag graphs do not produce strategic claims
LLMs may summarize tag graphs only in meta/report modes, not single-deck reports
```

Supported scopes:

```text
single analyzed deck
saved deck snapshot
commander average
exact partner-pair average
Top 16 commander pool
winner pool
regional pool
meta snapshot
frequency pool
personal deck history
```

Default comparison:

```text
Analyzed deck vs Commander Top 16 average
```

The selected-tag limit is:

```text
minimum: 1
maximum: 6
```

Any schema, repository, UI, Scryfall Tagger import, chart export, LLM summary,
or persistence work for Tag Graph Lab requires a future contract. This rule is
authoritative product direction, not immediate implementation approval.

---

## 4. SOURCE CLASSIFICATION MATRIX

This matrix codifies what each source is trusted for. It prevents AI sessions from treating DDB as tournament data or Moxfield as competitive truth.

| Source | Card Truth | Deck Truth | Tournament Truth | Primer Truth | Combo Truth | Analytics Eligible | Notes |
|--------|------------|------------|------------------|--------------|-------------|---------------------|-------|
| Scryfall | **Yes** | No | No | No | No | No | Canonical card truth |
| TopDeck | No | **Yes** | **Yes** | No | No | **Yes** | Primary tournament source |
| EDHTop16 | No | Aggregated | Aggregated | No | No | **Yes after canonicalization** | Secondary aggregator |
| MTGTop8 | No | **Yes** | **Yes** | No | No | **Yes after canonicalization** | Historical coverage |
| MTGDecks | No | **Yes** | **Yes** | No | No | **Yes after canonicalization** | Mirror risk, dedupe required |
| Hareruya | No | **Yes** | **Yes** | No | No | **Yes after canonicalization** | Regional source |
| Moxfield | No | User Decks | No | **Yes** | No | Primer only | Not tournament truth |
| cEDH DDB | No | No | No | **Yes** | No | No | Classification source |
| Commander Spellbook | No | No | No | No | **Yes** | Combo only | Combo truth |
| MTGJSON | Supplemental | No | No | No | No | No | Validation only |
| Archidekt | No | User Decks | No | **Yes** | No | Primer only | Secondary primer source |

**Enforcement:**
- Analytics pipelines must check `analytics_eligible` before using source data.
- Primer pipelines must use only `primer_truth` sources.
- Card truth pipelines must use only `card_truth` sources.

---

## 5. APPROVED SOURCE CATALOG

### 5.1 Scryfall

**URLs:**
```text
https://scryfall.com/
https://scryfall.com/docs/api
https://scryfall.com/docs/api/bulk-data
https://scryfall.com/docs/api/cards
https://scryfall.com/docs/api/rulings
https://scryfall.com/docs/syntax
https://scryfall.com/docs/tagger-tags
```

**Purpose:**
```text
Absolute card truth
Card names
Oracle IDs
Scryfall IDs
Oracle text
Mana costs
Mana value
Color identity
Type line
Legalities
Prices
Produced mana
Images
Rulings
Bulk data
Search syntax validation
```

**Allowed use:**
```text
Populate cards table
Normalize all card names
Validate all source deck cards
Support natural language → Scryfall query translator
Support optional rulings panel
Support simulator card definitions where possible
```

**Priority:** Card truth priority 1

**Storage:**
```text
reference/scryfall/
data/cache/scryfall/
```

**Adapter required:** Yes: `codie/providers/scryfall/`

**Implementation notes:**
```text
Use bulk data for initial local cache.
Use API only for refresh, autocomplete, rulings, and validation gaps.
Respect rate limits and cache aggressively.
```

### 5.2 MTGJSON

**URLs:**
```text
https://mtgjson.com/
https://mtgjson.com/getting-started/
https://mtgjson.com/faq/
https://github.com/mtgjson/mtgjson
```

**Purpose:**
```text
Supplemental local card metadata
Set metadata
Identifier cross‑reference
Validation support
Offline warehouse reference
```

**Allowed use:**
```text
Supplement Scryfall
Cross‑check identifiers
Support local set/printing metadata
Support future proxy/inventory workflows
```

**Prohibited use:**
```text
Overriding Scryfall card truth
Tournament analytics
Deck truth
```

**Priority:** Optional card dataset priority 2

**Storage:**
```text
reference/mtgjson/
data/cache/mtgjson/
```

**Adapter required:** Optional for V1.

### 5.3 Commander Spellbook

**URLs:**
```text
https://commanderspellbook.com/
https://backend.commanderspellbook.com/
https://backend.commanderspellbook.com/variants/
https://github.com/SpaceCowMedia/commander-spellbook-backend
```

**Purpose:**
```text
Combo evidence
Combo components
Combo outcomes
Combo links
Combo completion recommendations
Package seed evidence where appropriate
```

**Allowed use:**
```text
Store combo metadata
Link known combos to deck cards
Show present combo components
Show missing combo components
Link to official combo pages
Calculate combo completion percentage
```

**Priority:** Combo source priority 1

**Storage:**
```text
reference/spellbook/
data/cache/spellbook/
```

**Adapter required:** Yes: `codie/providers/spellbook/`

### 5.4 TopDeck

**URLs:**
```text
https://topdeck.gg/
https://topdeck.gg/docs/tournaments-v2
https://topdeck.gg/features/integrations
```

**Purpose:**
```text
Primary tournament and deck source
Structured event metadata
Tournament standings
Decklists
Round/match data where available
Placement records
```

**Priority:** Tournament priority 1

**Storage:**
```text
reference/topdeck/
data/raw/topdeck/
```

**Adapter required:** Yes: `codie/providers/topdeck/`

**Notes:** API may require a free key and attribution. This still satisfies zero‑cost, but the implementation must store config locally and never hard‑code credentials.

### 5.5 EDHTop16

**URLs:**
```text
https://edhtop16.com/
https://edhtop16.com/api/graphql
```

**Purpose:**
```text
Primary cEDH tournament aggregation reference
Commander metagame views
Tournament filters
Entries
Meta share
Commander pages
Top finish cross‑checking
```

**Priority:** Tournament priority 2

**Storage:**
```text
reference/edhtop16/
data/raw/edhtop16/
```

**Adapter required:** Yes: `codie/providers/edhtop16/`

### 5.6 MTGTop8

**URLs:**
```text
https://mtgtop8.com/
https://mtgtop8.com/format?f=cEDH
https://github.com/freeall/mtgtop8
https://github.com/kammradt/mtgtop8-scrapper
```

**Purpose:**
```text
Historical tournament coverage
Additional cEDH event discovery
Decklist backfill
International event coverage
Parser methodology reference
```

**Priority:** Tournament priority 3

**Storage:**
```text
reference/mtgtop8/
reference/github_repos/mtgtop8/
data/raw/mtgtop8/
```

**Adapter required:** Yes: `codie/providers/mtgtop8/`

### 5.7 MTGDecks

**URLs:**
```text
https://mtgdecks.net/
```

**Purpose:**
```text
Secondary tournament discovery
Deck import
Event enrichment
Cross‑source deduplication support
Source mirror detection
```

**Priority:** Tournament priority 4

**Storage:**
```text
reference/mtgdecks/
data/raw/mtgdecks/
```

**Adapter required:** Yes: `codie/providers/mtgdecks/`

**Critical rule:**
```text
MTGDecks event + TopDeck event can equal one canonical_event.
MTGDecks source records must not power analytics until canonical deduplication confirms uniqueness or merges them.
```

**Auxiliary card rule:**
```text
Sticker sheets and auxiliary pieces go to deck_auxiliary_cards, not canonical_deck_cards.
```

### 5.8 Hareruya

**URLs:**
```text
https://www.hareruyamtg.com/en/deck/7/metagame/
https://www.hareruyamtg.com/en/user_data/help_decksearch
```

**Purpose:**
```text
Japanese regional tournament/deck source
Japanese Commander and cEDH‑adjacent coverage
Regional meta analysis
Decklist import
Event discovery
```

**Priority:** Tournament priority 5, Japanese/regional priority 1

**Storage:**
```text
reference/hareruya/
data/raw/hareruya/
```

**Adapter required:** Yes: `codie/providers/hareruya/`

**Hareruya parser rule:**
```text
Deck page metadata first.
First isolated card line can be fallback commander candidate when Commander metadata confirms Commander.
Do not use MTGDecks‑style Sideboard splitting for Hareruya commander detection.
```

**Regional defaults:**
```text
source_site = hareruya
source_region = Japan
source_country = JP
source_language = en_or_ja
```

### 5.9 Moxfield

**URLs:**
```text
https://moxfield.com/
https://moxfield.com/decks/<deck_id>
https://moxfield.com/decks/<deck_id>/primer
```

**Purpose:**
```text
Deck import
User workflow integration
Primer discovery
Primer metadata
Popular deck metadata
Commander/partner primer matching
Source‑provided tags/titles/sections as evidence
```

**Priority:** Primer priority 1, Deck import workflow priority 1

**Storage:**
```text
reference/moxfield/
data/raw/moxfield/
```

**Adapter required:** Yes: `codie/providers/moxfield/`

### 5.10 cEDH Decklist Database / DDB

**URLs:**
```text
https://cedh-decklist-database.com/
https://github.com/averagewagon/cEDH-Decklist-Database
```

**Purpose:**
```text
Primer links
Source‑provided classifications
Community curation
Commander mapping
Deck/resource links
Status labels
```

**Priority:** Primer priority 2, Archetype evidence priority 1, Analytics priority 0 / prohibited for V1

**Storage:**
```text
reference/ddb/
data/raw/ddb/
```

**Adapter required:** Yes for primer/classification metadata. No for tournament analytics.

### 5.11 Archidekt

**URLs:**
```text
https://archidekt.com/
```

**Purpose:**
```text
Deck import
Primer/description discovery where available
Secondary deckbuilder workflow support
```

**Priority:** Primer priority 3, Deck import priority 2

**Storage:**
```text
reference/archidekt/
data/raw/archidekt/
```

**Adapter required:** Later V1 or V1.5 depending on Moxfield completeness.

### 5.12 EDHREC

**URLs:**
```text
https://edhrec.com/
```

**Purpose:**
```text
Recommendation UX reference only
Category organization reference
```

**Storage:**
```text
reference/ux_references/edhrec/
```

**Adapter required:** No.

### 5.13 cEDH.io

**URLs:**
```text
https://cedh.io/
https://www.cedh.io/faq
```

**Purpose:**
```text
UX/product reference
Deck analysis presentation reference
Evidence dashboard comparison
```

**Storage:**
```text
reference/ux_references/cedh_io/
```

**Adapter required:** No.

### 5.14 cEDHData / Rhystic Simulator

**URLs:**
```text
https://www.cedhdata.com/simulator
```

**Purpose:**
```text
Simulation architecture reference
Target‑based simulation reference
Mulligan policy reference
Mana/action trace reference
Result percentage validation reference
```

**Priority:** Simulation reference priority 1

**Storage:**
```text
reference/cedhdata_simulator/
reference/rhystic_simulator_traces/
```

**Adapter required:** No production adapter for V1. Production module is `codie/probability_engine/`.

### 5.15 cEDHStats

**URLs:**
```text
https://cedhstats.com/
```

**Purpose:**
```text
Commander page design reference
Card page design reference
Statistical presentation reference
Historical trends reference
Sortable evidence tables reference
```

**Usage:**
```text
Use as UI/UX inspiration for evidence presentation
Do NOT copy archetype inference
Do NOT copy strategic conclusions
Do NOT copy AI explanations
```

**Storage:**
```text
reference/ux_references/cedhstats/
```

**Adapter required:** No.

### 5.16 Eldrazi.gg

**URLs:**
```text
https://eldrazi.gg/
https://mulligan.eldrazi.dev/
```

**Purpose:**
```text
Mulligan trainer UX reference
Opening hand simulator reference
Pod‑generation reference
Real tournament data UX comparison
```

**Storage:**
```text
reference/ux_references/eldrazi/
```

**Adapter required:** No.

### 5.17 MullAgain

**URLs:**
```text
https://mullagain.vercel.app/
```

**Purpose:**
```text
Mulligan decision UX reference
Opening hand evaluation reference
```

**Storage:**
```text
reference/ux_references/mullagain/
```

**Adapter required:** No.

### 5.18 Removed / Inactive Sources

Removed from active V1 roadmap:

```text
Spicerack.gg
MTGMelee
Melee.gg
```

Reason: Unavailable, inaccessible, unstable, or not worth V1 implementation time.

They may live only in:
```text
reference/inactive_sources/
```

---

## 6. GITHUB REFERENCE CATALOG

All GitHub repositories are reference‑only unless explicitly promoted after license review. No repo code may be copied into Codie production without license review, explicit approval, roadmap update, and native Codie implementation plan.

### 6.1 Approved Reference Repos

#### SpaceCowMedia/commander-spellbook-backend

**Use for:**
```text
Combo schema
Combo components
Variant structure
REST API behavior
Combo‑link authority
```

**Status:** Approved Spellbook reference. Possible API integration reference.

**Do not use for:**
```text
Card truth
Tournament truth
Deck truth
```

**Store under:**
```text
reference/github_repos/commander_spellbook_backend/
reference/spellbook/
```

#### mtgjson/mtgjson

**Use for:**
```text
Supplemental local validation
Offline dataset comparison
Identifier mapping support
```

**Status:** Approved supplemental dataset

**Rule:** Never overrides Scryfall

**Store under:**
```text
reference/github_repos/mtgjson/
```

#### NandaScott/Scrython

**Use for:**
```text
Scryfall API wrapper reference only
```

**Status:** Optional reference

**Rule:** Prefer direct Scryfall bulk‑data ingestion for Codie core

**Store under:**
```text
reference/github_repos/scrython/
```

#### MTGTop8 Scraper Repos

**Repos:**
```text
freeall/mtgtop8
tstrimple/mtgtop8-scraper
jaypeeZero/mtgtop8-scraper
```

**Use for:**
```text
MTGTop8 parser‑pattern research
Event/deck extraction reference
```

**Status:** Reference only

**Store under:**
```text
reference/github_repos/mtgtop8_scrapers/
```

#### cEDH-Decklist-Database/cEDH-Decklist-Database

**Use for:**
```text
Primer links
Community classification
Commander mapping
Source‑provided archetype labels
```

**Status:** Approved primer/classification reference

**Do not use for:**
```text
Tournament analytics
Meta population statistics
```

**Store under:**
```text
reference/github_repos/cedh_decklist_database/
reference/ddb/
```

#### KonradHoeffner/cedh

**Use for:**
```text
Staples methodology
Deck correlation ideas
Clustering inspiration
Heatmap inspiration
Validation reference
```

**Status:** Research reference only

**Store under:**
```text
reference/github_repos/konradhoeffer_cedh/
```

#### Moxfield Scraper Repos

**Repos:**
```text
Joshua-Farr/moxfield-deck-scraper
Jorazon/moxfield-scraper
cduym622/moxfield-scraper
KarmaKamikaze/Moxfield-Price-Scraper
```

**Use for:**
```text
Endpoint discovery
Request behavior reference
```

**Status:** Weak reference only

**Store under:**
```text
reference/github_repos/moxfield_scrapers/
```

#### linkian209/pyrchidekt

**Use for:**
```text
Archidekt import reference
```

**Status:** Optional future reference

**Store under:**
```text
reference/github_repos/pyrchidekt/
```

#### Investigamer/Proxyshop

**Use for:**
```text
Proxy rendering workflow
Photoshop automation reference
Template behavior reference
```

**Status:** Approved proxy subsystem reference

**Store under:**
```text
reference/github_repos/proxyshop/
```

#### chilli-axe/mpc-autofill

**Use for:**
```text
Print‑order workflow reference
```

**Status:** Optional proxy adjunct reference

**Store under:**
```text
reference/github_repos/mpc_autofill/
```

### 6.2 Low Priority / Ignore Unless Needed

**Generic MTG Simulator Repos:**
```text
Robmoru23/MTG_Simulator
the-astronot/mtg_sim
```
Reason: Codie already has stronger cEDHData/Rhystic simulator reference material.

**Generic Obsidian Export Repos:**
Reason: Obsidian export is simple Markdown/YAML generation and should be implemented directly in Codie.

### 6.3 Priority Verdict

**Useful Now:**
```text
Commander Spellbook backend
MTGJSON
cEDH Decklist Database repo
KonradHoeffner/cEDH
Proxyshop
MTGTop8 parser repos
```

**Useful Later:**
```text
pyrchidekt
MPC Autofill
Scrython
Moxfield scraper fragments
```

**Ignore Unless Desperate:**
```text
Generic MTG simulator repos
Generic Obsidian converters
Tiny or empty scraper repos
Abandoned forks
```

---

## 7. PACKAGE STRUCTURE

This is the canonical package tree for the rebuild.

```text
codie/
│
├── main.py
├── pyproject.toml
├── requirements.txt
│
├── db/
│   ├── connection.py
│   ├── pragmas.py
│   ├── bootstrap.py
│   ├── migrations/
│   ├── schema/
│   │   ├── core.sql
│   │   ├── source.sql
│   │   ├── canonical.sql
│   │   ├── curated.sql
│   │   ├── user.sql
│   │   ├── simulation.sql
│   │   ├── analytics.sql
│   │   └── indexes.sql
│   └── repositories/
│       ├── cards_repo.py
│       ├── source_repo.py
│       ├── canonical_repo.py
│       ├── decks_repo.py
│       ├── tournaments_repo.py
│       ├── primers_repo.py
│       ├── combos_repo.py
│       ├── packages_repo.py
│       ├── simulation_repo.py
│       ├── performance_repo.py
│       ├── historical_repo.py
│       ├── evidence_repo.py
│       ├── regional_repo.py
│       └── user_repo.py
│
├── cards/
│   ├── scryfall_loader.py
│   ├── oracle_cache.py
│   ├── card_lookup.py
│   ├── printings.py
│   ├── action_deriver.py
│   └── rulings.py
│
├── providers/
│   ├── base.py
│   ├── models.py
│   ├── errors.py
│   ├── scryfall/
│   ├── topdeck/
│   ├── edhtop16/
│   ├── mtgtop8/
│   ├── mtgdecks/
│   ├── hareruya/
│   ├── moxfield/
│   ├── ddb/
│   ├── archidekt/
│   └── spellbook/
│
├── ingestion/
│   ├── pipelines/
│   │   ├── scryfall_pipeline.py
│   │   ├── tournament_pipeline.py
│   │   ├── deck_pipeline.py
│   │   ├── primer_pipeline.py
│   │   └── combo_pipeline.py
│   ├── transforms/
│   ├── validation/
│   └── run_log.py
│
├── canonical/
│   ├── canonicalizer.py
│   ├── event_deduper.py
│   ├── deck_deduper.py
│   ├── alias_engine.py
│   ├── fuzzy_resolver.py
│   ├── normalization.py
│   ├── deck_hashing.py
│   └── signature.py         # commander signature generation
│
├── curated/
│   ├── commander_registry.py
│   ├── alias_registry.py
│   ├── primer_registry.py
│   ├── package_registry.py
│   └── archetype_labels.py
│
├── analytics/
│   ├── tournament_intelligence/
│   │   ├── meta_analysis.py
│   │   ├── placement_weighting.py
│   │   ├── trend_analysis.py
│   │   ├── regional_analysis.py
│   │   └── matchup_analysis.py
│   ├── card_performance/
│   │   ├── performance_metrics.py
│   │   ├── inclusion_rates.py
│   │   ├── win_deltas.py
│   │   └── trend_calculator.py
│   ├── historical/
│   │   ├── snapshot_manager.py
│   │   ├── commander_growth.py
│   │   └── card_growth.py
│   └── evidence/
│       ├── evidence_counter.py
│       └── evidence_aggregator.py
│
├── recommendations/
│   ├── engine/
│   │   ├── recommender.py
│   │   ├── scoring.py
│   │   └── filters.py
│   ├── statistics/
│   │   ├── inclusion_rates.py
│   │   ├── lift.py
│   │   ├── confidence.py
│   │   └── frequency.py
│   ├── similarity/
│   │   ├── deck_similarity.py
│   │   ├── commander_similarity.py
│   │   └── overlap.py
│   ├── source_recommendations.py
│   └── explanations/
│       ├── explanation_builder.py
│       └── templates.py
│
├── primers/
│   ├── discovery.py
│   ├── ranking.py
│   ├── metadata.py
│   └── validation.py
│
├── combos/
│   ├── spellbook_sync.py
│   ├── combo_detector.py
│   ├── combo_completion.py
│   └── combo_models.py
│
├── packages/
│   ├── package_detector.py
│   ├── package_completion.py
│   ├── package_models.py
│   └── definitions/
│
├── probability_engine/
│   ├── __init__.py
│   ├── deck_parser.py
│   ├── card_models.py
│   ├── mana.py
│   ├── game_state.py
│   ├── actions.py
│   ├── mulligans.py
│   ├── search.py
│   ├── monte_carlo.py
│   ├── batch_runner.py
│   ├── result_models.py
│   └── trace_logger.py
│
├── pages/
│   ├── commander_pages.py
│   ├── card_pages.py
│   ├── staples_explorer.py
│   ├── evidence_explorer.py
│   └── deck_comparison.py
│
├── evidence/
│   ├── evidence_bundle.py
│   ├── evidence_ranker.py
│   ├── source_attribution.py
│   ├── unified_evidence_layer.py
│   └── evidence_stack.py
│
├── query_helper/
│   ├── nl_to_scryfall.py
│   ├── syntax_validator.py
│   └── examples.py
│
├── exports/
│   ├── markdown_exporter.py
│   ├── csv_exporter.py
│   ├── json_exporter.py
│   ├── obsidian_exporter.py
│   └── templates/
│       ├── commander_staples_report.md.j2
│       ├── deck_evidence_report.md.j2
│       ├── tournament_meta_report.md.j2
│       ├── commander_page.md.j2
│       └── card_page.md.j2
│
├── inventory/
│   ├── staples.py
│   ├── inventory_compare.py
│   ├── acquisition_paths.py
│   └── proxy_planning.py
│
├── proxy/
│   ├── proxyshop.py
│   ├── rendering.py
│   ├── exports.py
│   └── cache_manager.py
│
├── assets/
│   ├── cache/
│   ├── renders/
│   ├── exports/
│   └── templates/
│
├── data/
│   ├── aliases/
│   ├── seeds/
│   ├── fixtures/
│   └── samples/
│
├── docs/
│   ├── CODIE_V1_CONSTITUTION.md
│   ├── SCHEMA_SPEC.md
│   ├── DEPENDENCY_RULES.md
│   ├── INGESTION_CONTRACTS.md
│   ├── SOURCE_CLASSIFICATION.md
│   ├── PROVIDER_PRIORITY_LIST.md
│   ├── MASTER_STATE.md
│   └── UNRESOLVED.md
│
├── reference/
│
└── tests/
    ├── fixtures/
    ├── test_schema.py
    ├── test_scryfall_loader.py
    ├── test_card_lookup.py
    ├── test_providers_*.py
    ├── test_canonicalization.py
    ├── test_recommendations.py
    ├── test_tournament_weighting.py
    ├── test_primers.py
    ├── test_combos.py
    ├── test_performance_metrics.py
    ├── test_historical_snapshots.py
    ├── test_evidence_counts.py
    ├── test_commander_pages.py
    ├── test_card_pages.py
    ├── test_evidence_explorer.py
    ├── test_deck_comparison.py
    └── test_probability_engine.py
```

---

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

---

## 9. FOUR‑LAYER DATA ARCHITECTURE

```text
Source Layer
→ Canonical Layer
→ Curated Registry Layer
→ User Layer
→ Analytics Layer (derived from Canonical)
```

### 9.1 Source Layer

Stores raw/imported provider data.

**Tables:**
```text
source_events
source_decks
source_deck_cards
source_primers
source_combos
ingestion_runs
provider_objects
```

**Rules:**
```text
Never powers analytics directly.
Always preserves raw payloads.
May contain duplicate events/decks across providers.
May contain provider‑specific labels and fields.
```

### 9.2 Canonical Layer

Deduplicated analytics layer.

**Tables:**
```text
canonical_events
canonical_event_sources
canonical_decks
canonical_deck_sources
canonical_deck_cards
canonical_deck_commanders
event_deck_entries
tournament_rounds
match_results
```

**Rules:**
```text
Only this layer powers analytics.
Every canonical object must link back to one or more source records.
Canonical records must never delete source disagreement.
Deduplication must be explainable.
Commander signatures generated from canonical commanders.
```

### 9.3 Curated Registry Layer

Maintainer‑controlled data.

**Tables:**
```text
primer_registry
package_registry
package_cards
commander_registry
alias_registry
archetype_label_registry
```

**Rules:**
```text
Curated data can label or define packages.
Curated data cannot rewrite Scryfall truth.
Curated archetype labels must be visibly attributed as curated/user/source labels.
```

### 9.4 User Layer

User‑owned data.

**Tables:**
```text
user_decks
user_deck_cards
saved_analysis
user_labels
custom_packages
analysis_sessions
```

**Rules:**
```text
User data never modifies canonical source data.
Casual/user‑submitted decks are temporary or user‑owned unless imported from approved source pipelines.
User labels are valid evidence but must be labeled as user‑provided.
```

### 9.5 Analytics Layer

Derived metrics from canonical data.

**Tables:**
```text
card_performance_metrics
historical_snapshots
historical_commander_metrics
historical_card_metrics
evidence_counts
regional_commander_metrics
regional_card_metrics
regional_package_metrics
card_statistics_snapshots
card_statistics
recommendation_runs
recommendation_candidates
```

---

## 10. DATABASE SPECIFICATION

This is a first‑pass schema contract. DeepSeek implements this as structured SQL files, not redesign it mid‑flight.

### 10.1 Core Card Tables

#### `cards`

```sql
CREATE TABLE cards (
    scryfall_id TEXT PRIMARY KEY,
    oracle_id TEXT,
    name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    mana_cost TEXT,
    mana_value REAL,
    type_line TEXT,
    oracle_text TEXT,
    colors_json TEXT,
    color_identity_json TEXT,
    legalities_json TEXT,
    produced_mana_json TEXT,
    keywords_json TEXT,
    layout TEXT,
    card_faces_json TEXT,
    image_uris_json TEXT,
    prices_json TEXT,
    set_code TEXT,
    collector_number TEXT,
    rarity TEXT,
    released_at TEXT,
    is_reserved INTEGER DEFAULT 0,
    is_digital INTEGER DEFAULT 0,
    is_legal_commander INTEGER DEFAULT 0,
    is_commander_candidate INTEGER DEFAULT 0,
    raw_json TEXT NOT NULL,
    imported_at TEXT NOT NULL
);
```

**Indexes:**
```sql
CREATE INDEX idx_cards_oracle_id ON cards(oracle_id);
CREATE INDEX idx_cards_normalized_name ON cards(normalized_name);
CREATE INDEX idx_cards_color_identity ON cards(color_identity_json);
```

#### `commanders`

```sql
CREATE TABLE commanders (
    commander_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scryfall_id TEXT NOT NULL,
    oracle_id TEXT,
    canonical_name TEXT NOT NULL,
    normalized_name TEXT NOT NULL,
    color_identity_json TEXT NOT NULL,
    is_partner INTEGER DEFAULT 0,
    is_background_compatible INTEGER DEFAULT 0,
    is_doctor_companion INTEGER DEFAULT 0,
    is_friends_forever INTEGER DEFAULT 0,
    legal_status TEXT,
    raw_source TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

### 10.2 Source Tables

#### `ingestion_runs`

```sql
CREATE TABLE ingestion_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    pipeline_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,
    objects_processed INTEGER DEFAULT 0,
    objects_inserted INTEGER DEFAULT 0,
    objects_updated INTEGER DEFAULT 0,
    objects_failed INTEGER DEFAULT 0,
    log_path TEXT,
    config_json TEXT,
    error_summary TEXT
);
```

#### `provider_objects`

```sql
CREATE TABLE provider_objects (
    provider_object_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    object_type TEXT NOT NULL,
    provider_id TEXT,
    source_url TEXT,
    retrieved_at TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    raw_payload_json TEXT,
    raw_file_path TEXT,
    run_id INTEGER,
    UNIQUE(provider, object_type, provider_id, payload_hash),
    FOREIGN KEY(run_id) REFERENCES ingestion_runs(run_id)
);
```

#### `source_events`

```sql
CREATE TABLE source_events (
    source_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_event_id TEXT,
    source_url TEXT,
    original_source TEXT,
    original_source_url TEXT,
    event_name TEXT,
    normalized_event_name TEXT,
    event_date TEXT,
    format TEXT,
    source_region TEXT,
    source_country TEXT,
    source_store_tag TEXT,
    source_language TEXT,
    source_reported_player_count INTEGER,
    source_reported_deck_count INTEGER,
    source_participants INTEGER,
    tournament_size_bucket TEXT,
    raw_json TEXT,
    provider_object_id INTEGER,
    imported_at TEXT NOT NULL,
    canonical_event_id INTEGER,
    dedupe_status TEXT DEFAULT 'pending',
    FOREIGN KEY(provider_object_id) REFERENCES provider_objects(provider_object_id)
);
```

#### `source_decks`

```sql
CREATE TABLE source_decks (
    source_deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_deck_id TEXT,
    source_event_id INTEGER,
    source_url TEXT,
    source_download_url TEXT,
    source_visual_url TEXT,
    source_export_urls_json TEXT,
    source_same_tournament_url TEXT,
    source_same_archetype_url TEXT,
    deck_title TEXT,
    commander_text TEXT,
    source_archetype_name TEXT,
    source_player_name TEXT,
    source_rank INTEGER,
    source_rank_label TEXT,
    source_score_label TEXT,
    source_record TEXT,
    source_win_rate REAL,
    source_price_paper REAL,
    source_price_mtgo REAL,
    source_store_tag TEXT,
    deck_hash TEXT,
    raw_json TEXT,
    provider_object_id INTEGER,
    imported_at TEXT NOT NULL,
    canonical_deck_id INTEGER,
    dedupe_status TEXT DEFAULT 'pending',
    FOREIGN KEY(source_event_id) REFERENCES source_events(source_event_id),
    FOREIGN KEY(provider_object_id) REFERENCES provider_objects(provider_object_id)
);
```

#### `source_deck_cards`

```sql
CREATE TABLE source_deck_cards (
    source_deck_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_deck_id INTEGER NOT NULL,
    raw_name TEXT NOT NULL,
    normalized_name TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    source_zone TEXT DEFAULT 'mainboard',
    source_order INTEGER,
    scryfall_id TEXT,
    oracle_id TEXT,
    resolution_status TEXT NOT NULL DEFAULT 'pending',
    resolution_note TEXT,
    raw_entry TEXT,
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

#### `deck_auxiliary_cards`

```sql
CREATE TABLE deck_auxiliary_cards (
    auxiliary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_deck_id INTEGER NOT NULL,
    canonical_deck_id INTEGER,
    name TEXT NOT NULL,
    normalized_name TEXT,
    auxiliary_type TEXT NOT NULL,
    source_zone TEXT,
    is_game_piece INTEGER DEFAULT 0,
    is_deck_card INTEGER DEFAULT 0,
    scryfall_id TEXT,
    oracle_id TEXT,
    mtgjson_id TEXT,
    legality_profile_json TEXT,
    raw_entry TEXT,
    validation_status TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id)
);
```

**Supported auxiliary types:**
```text
commander_candidate
companion
sticker_sheet
attraction
real_sideboard_card
unknown_auxiliary
```

**Auxiliary game pieces never count toward:**
```text
Mainboard inclusion
Staple detection
Recommendation scoring
Deck similarity
Package detection
Card frequency stats
```

### 10.3 Canonical Tables

#### `canonical_events`

```sql
CREATE TABLE canonical_events (
    canonical_event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    normalized_event_name TEXT NOT NULL,
    event_date TEXT,
    format TEXT,
    region TEXT,
    country TEXT,
    venue_or_store TEXT,
    player_count INTEGER,
    deck_count INTEGER,
    event_size_bucket TEXT,
    confidence_score REAL DEFAULT 0,
    dedupe_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(dedupe_key)
);
```

#### `canonical_event_sources`

```sql
CREATE TABLE canonical_event_sources (
    canonical_event_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    source_event_id INTEGER NOT NULL,
    provider TEXT NOT NULL,
    source_url TEXT,
    source_confidence REAL DEFAULT 1.0,
    merge_reason TEXT,
    created_at TEXT NOT NULL,
    UNIQUE(canonical_event_id, source_event_id),
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id),
    FOREIGN KEY(source_event_id) REFERENCES source_events(source_event_id)
);
```

#### `canonical_decks`

```sql
CREATE TABLE canonical_decks (
    canonical_deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_hash TEXT NOT NULL UNIQUE,
    commander_hash TEXT NOT NULL,
    format TEXT DEFAULT 'commander',
    card_count INTEGER NOT NULL,
    commander_count INTEGER NOT NULL,
    color_identity_json TEXT,
    first_seen_at TEXT,
    last_seen_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

#### `canonical_deck_sources`

```sql
CREATE TABLE canonical_deck_sources (
    canonical_deck_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_deck_id INTEGER NOT NULL,
    source_deck_id INTEGER NOT NULL,
    source_event_id INTEGER,
    provider TEXT NOT NULL,
    source_url TEXT,
    pilot_name TEXT,
    placement INTEGER,
    placement_label TEXT,
    record_text TEXT,
    source_confidence REAL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    UNIQUE(canonical_deck_id, source_deck_id),
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id),
    FOREIGN KEY(source_event_id) REFERENCES source_events(source_event_id)
);
```

#### `canonical_deck_cards`

```sql
CREATE TABLE canonical_deck_cards (
    canonical_deck_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_deck_id INTEGER NOT NULL,
    scryfall_id TEXT NOT NULL,
    oracle_id TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    zone TEXT NOT NULL DEFAULT 'mainboard',
    is_commander INTEGER DEFAULT 0,
    is_companion INTEGER DEFAULT 0,
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id),
    UNIQUE(canonical_deck_id, scryfall_id, zone)
);
```

#### `canonical_deck_commanders`

```sql
CREATE TABLE canonical_deck_commanders (
    canonical_deck_commander_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_deck_id INTEGER NOT NULL,
    scryfall_id TEXT NOT NULL,
    oracle_id TEXT,
    commander_order INTEGER DEFAULT 1,
    commander_role TEXT DEFAULT 'commander',
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id),
    UNIQUE(canonical_deck_id, scryfall_id)
);
```

#### `event_deck_entries`

```sql
CREATE TABLE event_deck_entries (
    event_deck_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    canonical_deck_id INTEGER NOT NULL,
    source_deck_id INTEGER,
    pilot_name TEXT,
    placement INTEGER,
    placement_label TEXT,
    record_text TEXT,
    wins INTEGER,
    losses INTEGER,
    draws INTEGER,
    top_cut_made INTEGER DEFAULT 0,
    final_pod INTEGER DEFAULT 0,
    winner INTEGER DEFAULT 0,
    entry_weight REAL DEFAULT 1.0,
    created_at TEXT NOT NULL,
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id),
    FOREIGN KEY(canonical_deck_id) REFERENCES canonical_decks(canonical_deck_id),
    FOREIGN KEY(source_deck_id) REFERENCES source_decks(source_deck_id)
);
```

#### `tournament_rounds`

```sql
CREATE TABLE tournament_rounds (
    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
    canonical_event_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    round_type TEXT,
    raw_json TEXT,
    FOREIGN KEY(canonical_event_id) REFERENCES canonical_events(canonical_event_id)
);
```

#### `match_results`

```sql
CREATE TABLE match_results (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    player_a_entry_id INTEGER,
    player_b_entry_id INTEGER,
    player_c_entry_id INTEGER,
    player_d_entry_id INTEGER,
    winner_entry_id INTEGER,
    result TEXT,
    raw_json TEXT,
    FOREIGN KEY(round_id) REFERENCES tournament_rounds(round_id)
);
```

### 10.4 Primer Tables

#### `source_primers`

```sql
CREATE TABLE source_primers (
    source_primer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    deck_url TEXT,
    primer_url TEXT NOT NULL,
    commander_text TEXT,
    partner_text TEXT,
    deck_title TEXT,
    primer_title TEXT,
    author TEXT,
    author_url TEXT,
    published_at TEXT,
    modified_at TEXT,
    source_tags_json TEXT,
    raw_metadata_json TEXT,
    imported_at TEXT NOT NULL
);
```

#### `primer_registry`

```sql
CREATE TABLE primer_registry (
    primer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    deck_url TEXT,
    primer_url TEXT NOT NULL UNIQUE,
    commander_key TEXT,
    partner_key TEXT,
    deck_title TEXT,
    primer_title TEXT,
    author TEXT,
    author_url TEXT,
    published_at TEXT,
    modified_at TEXT,
    primer_updated_at_text TEXT,
    primer_updated_at_parsed TEXT,
    likes INTEGER,
    views INTEGER,
    comments INTEGER,
    bracket TEXT,
    has_primer_route INTEGER DEFAULT 0,
    primer_content_present INTEGER DEFAULT 0,
    primer_toc_present INTEGER DEFAULT 0,
    primer_heading_count INTEGER DEFAULT 0,
    primer_section_names_json TEXT,
    primer_external_link_count INTEGER DEFAULT 0,
    primer_video_count INTEGER DEFAULT 0,
    primer_image_count INTEGER DEFAULT 0,
    cedh_title_signal INTEGER DEFAULT 0,
    cedh_tag_signal INTEGER DEFAULT 0,
    competitive_tag_signal INTEGER DEFAULT 0,
    tournament_title_signal INTEGER DEFAULT 0,
    content_length_estimate INTEGER,
    primer_quality_score REAL,
    raw_metadata_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### 10.5 Combo And Package Tables

#### `source_combos`

```sql
CREATE TABLE source_combos (
    source_combo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    provider_combo_id TEXT,
    combo_url TEXT,
    combo_name TEXT,
    components_json TEXT,
    outputs_json TEXT,
    raw_json TEXT,
    imported_at TEXT NOT NULL
);
```

#### `combos`

```sql
CREATE TABLE combos (
    combo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL DEFAULT 'commander_spellbook',
    provider_combo_id TEXT,
    combo_url TEXT NOT NULL,
    combo_name TEXT,
    normalized_name TEXT,
    outputs_json TEXT,
    raw_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    UNIQUE(provider, provider_combo_id)
);
```

#### `combo_cards`

```sql
CREATE TABLE combo_cards (
    combo_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    combo_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    card_name TEXT NOT NULL,
    role TEXT,
    required INTEGER DEFAULT 1,
    FOREIGN KEY(combo_id) REFERENCES combos(combo_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

#### `package_registry`

```sql
CREATE TABLE package_registry (
    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL UNIQUE,
    package_type TEXT NOT NULL,
    source TEXT NOT NULL,
    source_url TEXT,
    description TEXT,
    is_curated INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

#### `package_cards`

```sql
CREATE TABLE package_cards (
    package_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    card_name TEXT NOT NULL,
    role TEXT,
    required INTEGER DEFAULT 0,
    weight REAL DEFAULT 1.0,
    FOREIGN KEY(package_id) REFERENCES package_registry(package_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

### 10.6 Analytics Tables

#### `card_performance_metrics`

```sql
CREATE TABLE card_performance_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    oracle_id TEXT NOT NULL,
    scryfall_id TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    raw_inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    winner_inclusion_rate REAL,
    topcut_inclusion_rate REAL,
    winrate_with_card REAL,
    winrate_without_card REAL,
    winrate_delta REAL,
    topcut_delta REAL,
    confidence_score REAL,
    sample_size INTEGER,
    trend_30d REAL,
    trend_90d REAL,
    trend_180d REAL,
    trend_365d REAL,
    updated_at TEXT NOT NULL,
    UNIQUE(oracle_id, time_window, window_end_date),
    FOREIGN KEY(oracle_id) REFERENCES cards(oracle_id)
);
```

#### `historical_snapshots`

```sql
CREATE TABLE historical_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL,
    window_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(snapshot_date, window_type)
);
```

#### `historical_commander_metrics`

```sql
CREATE TABLE historical_commander_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    commander_signature TEXT NOT NULL,
    meta_share REAL,
    weighted_meta_share REAL,
    deck_count INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES historical_snapshots(snapshot_id)
);
```

#### `historical_card_metrics`

```sql
CREATE TABLE historical_card_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    oracle_id TEXT NOT NULL,
    inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    sample_size INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES historical_snapshots(snapshot_id),
    FOREIGN KEY(oracle_id) REFERENCES cards(oracle_id)
);
```

#### `evidence_counts`

```sql
CREATE TABLE evidence_counts (
    evidence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    tournament_evidence_count INTEGER DEFAULT 0,
    primer_evidence_count INTEGER DEFAULT 0,
    combo_evidence_count INTEGER DEFAULT 0,
    package_evidence_count INTEGER DEFAULT 0,
    simulation_evidence_count INTEGER DEFAULT 0,
    updated_at TEXT NOT NULL,
    UNIQUE(entity_type, entity_id)
);
```

#### `card_statistics_snapshots`

```sql
CREATE TABLE card_statistics_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope_type TEXT NOT NULL,
    scope_key TEXT,
    time_window TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    config_json TEXT,
    source_count INTEGER,
    canonical_event_count INTEGER,
    canonical_deck_count INTEGER
);
```

#### `card_statistics`

```sql
CREATE TABLE card_statistics (
    card_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    inclusion_count INTEGER DEFAULT 0,
    inclusion_rate REAL,
    placement_weighted_usage REAL,
    top_cut_count INTEGER DEFAULT 0,
    top_cut_rate REAL,
    winner_count INTEGER DEFAULT 0,
    win_rate_with_card REAL,
    win_rate_without_card REAL,
    win_rate_delta REAL,
    p_value REAL,
    confidence REAL,
    sample_size INTEGER,
    FOREIGN KEY(snapshot_id) REFERENCES card_statistics_snapshots(snapshot_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

#### `recommendation_runs`

```sql
CREATE TABLE recommendation_runs (
    recommendation_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_deck_hash TEXT NOT NULL,
    commander_hash TEXT,
    generated_at TEXT NOT NULL,
    config_json TEXT,
    source_snapshot_id INTEGER,
    notes TEXT
);
```

#### `recommendation_candidates`

```sql
CREATE TABLE recommendation_candidates (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recommendation_run_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    candidate_type TEXT NOT NULL,
    recommendation_score REAL,
    inclusion_rate REAL,
    lift_score REAL,
    confidence_score REAL,
    similarity_score REAL,
    package_completion_score REAL,
    generic_staple_penalty REAL,
    evidence_json TEXT NOT NULL,
    explanation_text TEXT,
    FOREIGN KEY(recommendation_run_id) REFERENCES recommendation_runs(recommendation_run_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

#### `innovation_snapshot_runs`

```sql
CREATE TABLE innovation_snapshot_runs (
    innovation_snapshot_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    generated_at TEXT NOT NULL,
    config_hash TEXT NOT NULL,
    config_json TEXT NOT NULL,
    notes TEXT,
    UNIQUE(generated_at, config_hash)
);
```

#### `innovation_snapshot_items`

```sql
CREATE TABLE innovation_snapshot_items (
    innovation_snapshot_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    innovation_snapshot_run_id INTEGER NOT NULL,
    innovation_id TEXT NOT NULL,
    oracle_id TEXT NOT NULL,
    scryfall_id TEXT,
    commander_signature TEXT,
    region_code TEXT,
    innovation_type TEXT NOT NULL,
    recent_window TEXT NOT NULL,
    baseline_window TEXT NOT NULL,
    recent_inclusion_rate REAL,
    baseline_inclusion_rate REAL,
    usage_delta REAL,
    recent_topcut_count INTEGER DEFAULT 0,
    recent_winner_count INTEGER DEFAULT 0,
    first_recent_seen_at TEXT NOT NULL,
    last_seen_before_recent_window TEXT,
    card_released_at TEXT,
    is_new_release INTEGER DEFAULT 0,
    sample_size INTEGER DEFAULT 0,
    confidence_score REAL,
    source_event_ids_json TEXT NOT NULL,
    source_deck_ids_json TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    UNIQUE(innovation_snapshot_run_id, innovation_id),
    FOREIGN KEY(innovation_snapshot_run_id) REFERENCES innovation_snapshot_runs(innovation_snapshot_run_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

### 10.7 Regional Metrics Tables

#### `regional_commander_metrics`

```sql
CREATE TABLE regional_commander_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_code TEXT NOT NULL,
    country_code TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    commander_signature TEXT NOT NULL,
    meta_share REAL,
    weighted_meta_share REAL,
    sample_size INTEGER,
    updated_at TEXT NOT NULL,
    UNIQUE(region_code, country_code, time_window, window_end_date, commander_signature)
);
```

#### `regional_card_metrics`

```sql
CREATE TABLE regional_card_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_code TEXT NOT NULL,
    country_code TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    oracle_id TEXT NOT NULL,
    inclusion_rate REAL,
    weighted_inclusion_rate REAL,
    sample_size INTEGER,
    updated_at TEXT NOT NULL,
    UNIQUE(region_code, country_code, time_window, window_end_date, oracle_id),
    FOREIGN KEY(oracle_id) REFERENCES cards(oracle_id)
);
```

#### `regional_package_metrics`

```sql
CREATE TABLE regional_package_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_code TEXT NOT NULL,
    country_code TEXT,
    time_window TEXT NOT NULL,
    window_end_date TEXT NOT NULL,
    package_id INTEGER NOT NULL,
    adoption_rate REAL,
    performance_score REAL,
    sample_size INTEGER,
    updated_at TEXT NOT NULL,
    UNIQUE(region_code, country_code, time_window, window_end_date, package_id),
    FOREIGN KEY(package_id) REFERENCES package_registry(package_id)
);
```

**Region codes:**
```text
global
north_america
europe
japan
other
```

### 10.8 Simulation Tables

#### `simulation_batches`

```sql
CREATE TABLE simulation_batches (
    batch_id TEXT PRIMARY KEY,
    deck_hash TEXT NOT NULL,
    decklist_source TEXT,
    games_requested INTEGER NOT NULL,
    games_completed INTEGER NOT NULL DEFAULT 0,
    min_mulligan_keep INTEGER NOT NULL,
    mulligan_mode TEXT,
    elapsed_ms INTEGER,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    completed_at TEXT,
    raw_config_json TEXT
);
```

#### `simulation_batch_results`

```sql
CREATE TABLE simulation_batch_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL,
    target_card TEXT NOT NULL,
    target_card_id TEXT,
    target_zone TEXT NOT NULL,
    turn INTEGER NOT NULL,
    win_count INTEGER NOT NULL,
    win_rate REAL NOT NULL,
    margin_of_error REAL,
    missing_cards_json TEXT,
    raw_payload_json TEXT,
    FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id)
);
```

#### `simulation_traces`

```sql
CREATE TABLE simulation_traces (
    trace_id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL,
    result_id INTEGER,
    game_index INTEGER,
    success INTEGER,
    mulligan_count INTEGER,
    opening_hand_json TEXT,
    final_state_json TEXT,
    action_trace_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(batch_id) REFERENCES simulation_batches(batch_id),
    FOREIGN KEY(result_id) REFERENCES simulation_batch_results(result_id)
);
```

### 10.9 User Tables

#### `user_decks`

```sql
CREATE TABLE user_decks (
    user_deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
    deck_name TEXT,
    source_url TEXT,
    deck_hash TEXT NOT NULL,
    commander_hash TEXT,
    raw_input TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    is_temporary INTEGER DEFAULT 1
);
```

#### `user_deck_cards`

```sql
CREATE TABLE user_deck_cards (
    user_deck_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_deck_id INTEGER NOT NULL,
    scryfall_id TEXT,
    oracle_id TEXT,
    raw_name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    zone TEXT DEFAULT 'mainboard',
    resolution_status TEXT,
    FOREIGN KEY(user_deck_id) REFERENCES user_decks(user_deck_id),
    FOREIGN KEY(scryfall_id) REFERENCES cards(scryfall_id)
);
```

#### `saved_analysis`

```sql
CREATE TABLE saved_analysis (
    saved_analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_deck_id INTEGER,
    deck_hash TEXT NOT NULL,
    analysis_type TEXT NOT NULL,
    generated_at TEXT NOT NULL,
    summary_json TEXT NOT NULL,
    report_path TEXT,
    FOREIGN KEY(user_deck_id) REFERENCES user_decks(user_deck_id)
);
```

#### `user_labels`

```sql
CREATE TABLE user_labels (
    user_label_id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_type TEXT NOT NULL,
    target_id TEXT NOT NULL,
    label TEXT NOT NULL,
    notes TEXT,
    created_at TEXT NOT NULL
);
```

#### `custom_packages`

```sql
CREATE TABLE custom_packages (
    custom_package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL,
    package_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

---

## 11. COMMANDER SIGNATURE DEFINITION

### 11.1 Purpose

`commander_signature` is used in canonical, historical, and regional tables to uniquely identify a commander or partner pair.

### 11.2 Rule

**Single commander:**
```text
etali_primal_conqueror
```

**Partners (two commanders):**
```text
tymna_the_weaver|kraum_ludevics_opus
```

**Rules:**
- Use normalized names from the `cards` table (lowercase, underscores for spaces).
- For partners, sort alphabetically by normalized name.
- Use pipe (`|`) as separator.
- The signature is immutable for a given commander set.

### 11.3 Implementation

Generate via:
```python
def make_commander_signature(commander_names):
    normalized = [normalize_name(n) for n in commander_names]
    return "|".join(sorted(normalized))
```

---

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

---

## 13. TOURNAMENT WEIGHTING MODEL

Tournament analytics must be reproducible. No mysterious "power score" harvested from the mist.

### 13.1 Core Principle

Analytics weight canonical event/deck entries, not providers. Provider priority affects ingestion confidence and deduplication, not independent event count.

### 13.2 Event Eligibility

**Default V1 filters:**
```text
Format: cEDH / Commander tournament sources only
Minimum player count: configurable, default 16+
Decklist completeness: required for card‑level analytics
Placement data: required for placement‑weighted metrics
Date known: required for recency‑window metrics
```

**Unknown player count:**
```text
Allowed for historical display.
Excluded from event‑size‑weighted analytics unless manually approved.
```

### 13.3 Event Size Weight

**Default:**
```text
event_size_weight = clamp(log2(player_count) / log2(128), 0.25, 1.50)
```

**Interpretation:**
```text
16 players ≈ 0.571
32 players ≈ 0.714
64 players ≈ 0.857
128 players ≈ 1.00
256 players ≈ 1.143

Formula is authoritative. Regenerate examples from:
log2(player_count) / log2(128)
```

### 13.4 Placement Weight

**Exact Placement Weights:**
```text
1st = 1.00
2nd = 0.90
3rd‑4th = 0.80
5th‑16th = 0.60
17+ = 0.30
```

**Fallback Weights:**
```text
Winner = 1.00
Top 4 = 0.80
Top 16 = 0.60
Participant = 0.30
```

**Required Usage:**
```text
Recommendation Engine
Card Performance
Commander Performance
Package Performance
Trend Analysis
Meta Share
Historical Intelligence
```

### 13.5 Recency Weight

For current‑meta windows:

```text
recency_weight = 0.5 ^ (days_old / half_life_days)
```

**Defaults:**
```text
30‑day view: half_life_days = 30
90‑day view: half_life_days = 60
1‑year view: half_life_days = 180
all‑time view: recency_weight = 1.0 unless user enables decay
```

### 13.6 Source Confidence Weight

Source confidence measures data completeness, not provider popularity.

**Default:**
```text
complete structured source with decklist + placement + date + player count: 1.00
complete decklist but weak placement metadata: 0.85
mirror/enrichment source with original link: 0.75
missing player count: 0.60
missing exact date: 0.50
manual/imported fixture: 0.50 unless validated
```

**Provider‑specific defaults after validation:**
```text
TopDeck structured API: 1.00
EDHTop16 aggregation: 0.95
MTGTop8 parsed historical page: 0.85
MTGDecks mirror/enrichment: 0.75 until deduped
Hareruya regional source: 0.85 after parser validation
```

### 13.7 Final Entry Weight

```text
entry_weight = event_size_weight
             * placement_weight
             * recency_weight
             * source_confidence_weight
             * decklist_completeness_weight
```

### 13.8 Required Analytics Outputs

**Tournament Intelligence must support:**

*Commander Metrics:*
```text
Meta Share
Weighted Meta Share
Growth Rate
Placement Rate
```

*Card Metrics:*
```text
Inclusion Rate
Weighted Inclusion
Winner Inclusion
Top Cut Inclusion
Win Rate Delta
Top Cut Delta
```

*Package Metrics:*
```text
Adoption
Performance
Growth
```

*Regional Metrics:*
```text
Global
North America
Europe
Japan
Other
```

### 13.9 Sample Size Guardrails

**Default display rules:**
```text
n < 10: hide from ranked claims, show as anecdotal evidence only
10 ≤ n < 30: show with low‑confidence warning
30 ≤ n < 100: show with medium confidence
n ≥ 100: eligible for high‑confidence display
```

### 13.10 Deduplication Guardrail

If the same event appears in TopDeck and MTGDecks:
```text
One canonical_event
Multiple canonical_event_sources
One analytic event contribution
```

If same deck appears in multiple source records:
```text
One canonical_deck
Multiple canonical_deck_sources
Event entries preserved individually only when they represent distinct tournament entries
```

---

## 14. CARD PERFORMANCE METRICS LAYER

### 14.1 Purpose

Provide a reusable evidence layer for all card‑level analytics. This subsystem becomes a dependency for:

```text
Tournament Intelligence
Recommendation Engine
Commander Pages
Card Pages
Historical Intelligence
Unified Analysis Layer
```

### 14.2 Required Outputs

For every card:

```text
Raw Inclusion
Weighted Inclusion
Winner Inclusion
Top Cut Inclusion
Win Rate Delta
Top Cut Delta
Confidence
Sample Size
Historical Trend
```

### 14.3 Trends Supported

```text
trend_30d
trend_90d
trend_180d
trend_365d
```

---

## 15. HISTORICAL SNAPSHOT SYSTEM

### 15.1 Purpose

Store historical tournament‑state snapshots. Required for:

```text
Trend detection
Historical commander growth
Historical card growth
Historical meta analysis
```

### 15.2 Supported Windows

```text
30 Days
90 Days
180 Days
365 Days
All Time
```

### 15.3 Required Outputs

**Commander Growth:**
```text
Fastest Growing Commanders
Fastest Declining Commanders
```

**Card Growth:**
```text
Fastest Growing Cards
Emerging Staples
Declining Staples
```

**Meta Growth:**
```text
Meta Share Changes
Regional Changes
```

---

## 16. EVIDENCE COUNT AGGREGATION LAYER

### 16.1 Purpose

Track how many evidence sources support an item. This becomes a core Codie differentiator.

### 16.2 Example

**Mystic Remora:**
```text
Tournament Evidence: 421 Decks
Primer Evidence: 17 Primers
Combo Evidence: 0
Package Evidence: 4 Packages
Simulation Evidence: 18 Relevant Simulations
```

### 16.3 Required Usage

```text
Recommendations
Card Pages
Commander Pages
Unified Analysis
Evidence Explorer
Evidence Stack
```

---

## 17. RECOMMENDATION ENGINE

Codie has two recommendation systems.

### 17.1 Evidence Recommendation Engine

**Purpose:** Generate card candidates from canonical tournament/deck evidence.

**Inputs:**
```text
User deck or source deck
Commander identity
Color identity
Selected time window
Selected region
Selected source filters
Canonical tournament/deck statistics
Package definitions
Combo component data
Simulation deltas when available
```

**Outputs:**
```text
Card candidates
Low‑evidence/outlier cards
Package completion candidates
Combo completion candidates
Evidence explanation bundles
```

**Candidate categories:**
```text
commander‑specific
source‑label‑specific
package‑specific
combo‑completion
generic staple
meta tech
budget replacement
upgrade candidate
low‑evidence card
outlier card
```

**V1 Score:**
```text
recommendation_score =
    commander_lift_score
  + inclusion_rate_score
  + confidence_score
  + similarity_score
  + package_completion_score
  + combo_completion_score
  + tournament_performance_score
  + simulation_delta_score
  - generic_staple_penalty
  - low_sample_penalty
```

**Required explanation style:**
```text
Card appears in 73% of comparable canonical decks.
Card has lift 2.1 for this commander compared to color baseline.
Card appears in 41% of top‑cut lists using this commander.
Card is part of Commander Spellbook combo X.
Card completes 7/9 cards in selected package Y.
Simulation improved target access by 5.4 percentage points under config Z.
Evidence Stack shows 421 decks, 17 primers, 4 packages, 18 simulations.
```

### 17.2 Source Recommendation Engine

**Purpose:** Surface source‑backed recommendations and resources.

**Inputs:**
```text
Primer metadata
DDB labels
Moxfield tags/titles/primer metadata
Commander Spellbook combos
Curated package registry
User‑selected package labels
Manual registry entries
```

**Outputs:**
```text
Relevant primers
Sourced archetype labels
Known combo links
Package definitions
Commander resources
Source‑provided recommendations when present
```

**Rules:**
```text
Do not summarize primer body.
Do not infer strategy from source text.
Do not store long copied primer sections.
Always link back to source.
```

### 17.3 Similarity Metrics

**V1 deck similarity:**
```text
Jaccard similarity over oracle_ids
Weighted Jaccard by card role where roles are sourced/curated
Commander identity exact match first
Color identity baseline second
Partner‑pair exact match before individual commander match
```

**V1 commander similarity:**
```text
Shared card overlap
Shared package definitions
Shared color identity
Shared source‑provided labels
Tournament co‑occurrence patterns
```

### 17.4 Generic Staple Control

A card is a generic staple candidate when:

```text
High inclusion across many commanders
Low commander‑specific lift
High color‑identity baseline
High generic frequency
```

Generic staples can still be shown, but must not drown commander‑specific evidence.

---

## 18. PROBABILITY SIMULATION ENGINE

### 18.1 Purpose

Codie's probability engine must be a lightweight action‑based simulator, not merely a hypergeometric draw calculator.

It models:
```text
Opening hands
London mulligans
Mana production
Lands
Fetchlands
Artifacts
Rituals
Tutors
Pregame effects
Cast actions
Board abilities
Restricted mana
Turn progression
Target card access
Action traces
```

### 18.2 Out Of Scope For MVP

```text
Full multiplayer game engine
Opponent interaction modeling
Complete Magic rules engine
Priority stack realism beyond target access
Combat
All replacement effects
All triggered abilities
Full Oracle text interpreter
```

### 18.3 Module Mapping

```text
reference simulator cards.json     → codie/probability_engine/card_models.py
reference sim-worker parseDecklist  → deck_parser.py
mana payment model                  → mana.py
game state model                    → game_state.py
legal action generation             → actions.py
simulateMulliganForSeed             → mulligans.py
findWinningLine/playKeptHand        → search.py
runSimulation                       → monte_carlo.py
worker batching                     → batch_runner.py
trace output                        → trace_logger.py
```

### 18.4 Supported MVP Cards / Effects

**Initial support:**
```text
Basic lands
Duals/shocks/fetchable lands as mana sources
Fetchlands
Sol Ring
Mana Crypt
Mana Vault
Chrome Mox
Mox Diamond
Mox Opal
Lotus Petal
Jeweled Lotus
Gemstone Caverns
Dark Ritual
Cabal Ritual
Rite of Flame
Demonic Tutor
Vampiric Tutor
Mystical Tutor
Enlightened Tutor
Rhystic Study
Mystic Remora
Esper Sentinel
Smothering Tithe
```

### 18.5 Target Conditions

**Examples:**
```text
Cast Rhystic Study by turn 2
Cast Mystic Remora by turn 1
Cast Esper Sentinel by turn 1
Cast Smothering Tithe by turn 3
Access Ad Nauseam by turn 3
Access Rhystic Study OR Mystic Remora by turn 2
Access draw engine + blue protection by turn 2
Cast commander by turn 2 + hold interaction
```

**Target condition object:**
```json
{
  "target_card": "Rhystic Study",
  "target_zone": "stack",
  "turn": 2,
  "condition_type": "cast_or_access",
  "required_support_tags": [],
  "notes": "MVP target"
}
```

### 18.6 Batch Multi‑Target Simulation

Codie improvement over one‑target‑at‑a‑time tools:

```text
Simulate game histories once.
Evaluate many target conditions against the same histories.
```

**Example batch:**
```json
{
  "deck_id": "blue_farm_example",
  "games": 10000,
  "mulligan_mode": "policy",
  "min_mulligan_keep": 3,
  "targets": [
    {"card": "Rhystic Study", "zone": "stack", "turn": 1},
    {"card": "Rhystic Study", "zone": "stack", "turn": 2},
    {"card": "Mystic Remora", "zone": "stack", "turn": 1},
    {"card": "Mystic Remora", "zone": "stack", "turn": 2},
    {"card": "Esper Sentinel", "zone": "stack", "turn": 1},
    {"card": "Smothering Tithe", "zone": "stack", "turn": 3}
  ]
}
```

### 18.7 Required Outputs

```text
games_requested
games_completed
win_count per target
win_rate per target
margin_of_error per target
elapsed_ms
missing_cards
card contribution histograms
sample successful traces
sample failed traces
mulligan distribution
config JSON
```

### 18.8 Simulation Evidence Integration

Simulation results become evidence only when:

```text
games_completed >= configured minimum (default 500)
margin_of_error <= configured threshold (default 0.05)
configuration is fully stored
batch is reproducible (seed and deck hash recorded)
```

**Storage:**
Simulation evidence is aggregated into the `evidence_counts` table with `entity_type = 'card'` or `'deck'` and `simulation_evidence_count`. The detailed results remain in `simulation_batch_results`. The Evidence Stack will reflect simulation evidence counts when these criteria are met.

**Rule:** Simulation evidence shall not appear in the Evidence Stack unless the above conditions are satisfied. This prevents noisy, low‑confidence simulation results from polluting the evidence layer.

---

## 19. PRIMER DISCOVERY & INDEXING

### 19.1 Purpose

Primer discovery surfaces human‑written resources. Codie does not become the primer.

### 19.2 Sources

**Priority:**
```text
1. Moxfield primer discovery
2. cEDH Decklist Database
3. Archidekt descriptions/primers where available
4. Manual primer registry
```

### 19.3 Stored Metadata

**Allowed:**
```text
Primer URL
Deck URL
Source
Author
Commander
Partner
Source‑provided archetype
Deck title
Primer title
Last updated
Views
Likes
Comments
Primer route exists
Primer content exists
Table of contents exists
Heading count
Section names
External link count
Video count
Image count
Length estimate
Objective quality score
Raw metadata JSON
```

**Not allowed for permanent storage:**
```text
Full primer body
Long copied sections
Strategy text
Mulligan guide text
Combo explanations copied from primer
Card‑by‑card strategic explanations copied from primer
```

### 19.4 Moxfield Primer Ranking V1

**Signals:**
```text
Exact commander match
Exact partner‑pair match
Primer route exists
Primer content present
Last updated recency
Likes
Views
Comments
Heading count
External link count
Video/image count
cEDH title/tag signal
Competitive tag signal
Tournament title signal
Wrong partner penalty
Stale content penalty
```

**Output:** Top 5 primer candidates per commander or partner pair.

---

## 20. COMBO & PACKAGE INTELLIGENCE

### 20.1 Combo Intelligence

**Source:** Commander Spellbook

**Codie may:**
```text
Detect combo components in a deck.
Show missing combo components.
Show known combo outcomes from source data.
Link to Commander Spellbook combo page.
Calculate combo completion percentage.
```

**Codie may not:**
```text
Invent combo lines.
Invent sequencing.
Claim a deck is a combo archetype unless sourced.
```

### 20.2 Package Intelligence

**Valid package sources:**
```text
Commander Spellbook clusters where explicit
User‑defined package registry
Curated Codie package registry
Known public package lists after license/source review
Moxfield tags or deck section names when stored as source evidence
```

**Allowed output:**
```text
This deck contains 7 of 9 cards from the stored Dockside/Breach package definition.
```

**Forbidden output:**
```text
This deck is a Breach deck.
```
(Unless the label comes from source/user/curated registry.)

### 20.3 Package Completion Score

```text
package_completion = present_required_cards / total_required_cards
weighted_completion = sum(present_card_weight) / sum(total_card_weight)
```

Package recommendation candidates may be generated only when:

```text
User selected package, or
Package is sourced/curated and commander/deck evidence threshold is met, or
Commander Spellbook combo relationship explicitly supports it.
```

---

## 21. COMMANDER INTELLIGENCE PAGES

### 21.1 Purpose

Provide comprehensive intelligence on commanders in the cEDH meta.

### 21.2 Page URLs

```text
/commanders/thrasios-tymna
/commanders/ishai-rograkh
/commanders/tymna-kraum
```

### 21.3 Required Sections

```text
Overview
Meta Share
Historical Trends
Card Usage
Card Performance
Primer Discovery
Combo Discovery
Package Discovery
Evidence Explorer
```

### 21.4 Required Data

**Overview:**
```text
Commander identity
Color identity
Meta share
Weighted meta share
Growth rate
Placement rate
Total decks in dataset
Source distribution
```

**Card Usage:**
```text
Cards most frequently played with this commander
Inclusion rates
Weighted inclusion rates
Historical trends
```

**Card Performance:**
```text
Win rate with card
Win rate without card
Win rate delta
Top cut delta
Confidence
Sample size
```

### 21.5 UI Inspiration

Use cEDHStats as inspiration for commander pages, but maintain Evidence First compliance.

---

## 22. CARD INTELLIGENCE PAGES

### 22.1 Purpose

Provide comprehensive intelligence on individual cards in the cEDH meta.

### 22.2 Page URLs

```text
/cards/mystic-remora
/cards/fierce-guardianship
```

### 22.3 Required Sections

```text
Inclusion Rates
Weighted Inclusion
Winner Inclusion
Top Cut Inclusion
Commander Usage
Historical Trends
Price
Related Packages
Related Combos
Evidence Sources
```

### 22.4 Required Data

**Inclusion Rates:**
```text
Raw inclusion rate
Weighted inclusion rate
Winner inclusion rate
Top cut inclusion rate
By time window (30/90/180/365/all‑time)
```

**Commander Usage:**
```text
Which commanders play this card
How frequently
With what performance
```

**Historical Trends:**
```text
Growth or decline over time
Emerging or declining status
```

### 22.5 UI Inspiration

Use cEDHStats as inspiration for card pages, but maintain Evidence First compliance.

---

## 23. COMMANDER STAPLES EXPLORER

### 23.1 Purpose

Given a commander or partner pair, show the cards that appear in canonical top‑performing decks for that commander within a selected time window.

This is a locked V1 evidence feature. It is not a casual staples page. It is a reproducible commander‑specific card usage report built from canonical tournament records.

### 23.2 Default Query Behavior

```text
Commander / partner input: exact commander identity or partner pair
Default time window: last 6 months
Default placement scope: Top 16 finishes
Default source scope: canonical tournament decks only
Default display sort: frequency descending, then placement‑weighted frequency descending
Default export formats: Markdown, CSV, JSON, Obsidian vault Markdown
```

### 23.3 Example User Query

```text
Show Tymna / Kraum staples from top 16 decks in the last 6 months.
```

### 23.4 Required Output Fields

```text
Card name
Scryfall ID
Oracle ID
Card type line
Color identity
Number of matching decks using the card
Total matching decks
Inclusion percentage
Total copies observed
Average copies per deck
Placement‑weighted usage
Best finish observed
Top 16 count
Winner count
Most recent appearance date
First appearance date in selected window
Source deck links
Source event links
Provider breakdown
Region breakdown
```

### 23.5 Allowed Wording

```text
Card appears in 84% of Tymna/Kraum top 16 canonical decks over the last 6 months.
Card appears in 27 of 32 matching decks.
Card has 41 placement‑weighted points in the selected window.
```

### 23.6 Forbidden Wording

```text
This card is required.
This card is correct for the strategy.
This deck must play this card.
```

### 23.7 Required Filters

```text
Commander / partner pair
Date range
Placement range
Top N finish scope
Provider
Region / country
Card type
Color identity
Include/exclude generic staples
Minimum sample size
Minimum inclusion percentage
```

### 23.8 Required Exports

```text
Markdown report
CSV table
JSON evidence object
Obsidian vault note
```

### 23.9 Obsidian Export

**Example Obsidian path:**
```text
Codie/Commander Staples/Tymna the Weaver + Kraum, Ludevic's Opus.md
```

**Example Obsidian frontmatter:**
```yaml
type: commander_staples_report
commander_pair:
  - Tymna the Weaver
  - Kraum, Ludevic's Opus
time_window: last_6_months
placement_scope: top_16
generated_at: 2026-06-20
source_layer: canonical_tournament_decks
```

### 23.10 Recommended Report Sections

```text
Summary
Dataset Scope
Top Staples
High‑Frequency Interaction
High‑Frequency Mana
High‑Frequency Win Conditions
High‑Frequency Tutors
High‑Frequency Lands
Recent Additions
Declining Cards
Provider Coverage
Source Deck Links
Source Event Links
Methodology
```

### 23.11 Implementation Notes

```text
Use canonical_decks and canonical_deck_cards only.
Use canonical_deck_commanders for commander matching.
Never query source_deck_cards directly for analytics.
Source links are attached only as attribution after canonical records are selected.
Partner matching must require both commanders unless the user explicitly requests partial partner matching.
Use oracle_id for functional card grouping when multiple printings share identity.
Display canonical Scryfall name from cards table.
```

---

## 24. DECK COMPARISON SYSTEM

### 24.1 Purpose

Allow users to compare a deck against reference decks (canonical decks, commander baseline, or another user deck).

### 24.2 Compare Targets

```text
User deck vs canonical deck
User deck vs commander baseline
User deck vs another user deck
Two canonical decks
```

### 24.3 Outputs

```text
Shared cards (overlap)
Missing staples (cards that appear in reference but not in user deck)
Missing packages
Missing combos
Card performance differences (inclusion rates, win‑rate deltas)
Evidence differences (evidence counts, source coverage)
Similarity score
```

### 24.4 Implementation Notes

- Use canonical decks for reference baselines.
- Commander baseline = aggregated statistics from all canonical decks with the same commander signature.
- Use Oracle IDs for card identity.
- Display differences with source attribution.

---

## 25. EVIDENCE EXPLORER

### 25.1 Purpose

Inspect every evidence object linked to a card, commander, package, combo, deck, or recommendation.

### 25.2 Required Filters

```text
Source Type (tournament, primer, combo, package, simulation)
Provider (TopDeck, Moxfield, etc.)
Date Range
Region
Evidence Type (inclusion, win‑rate, combo, etc.)
Confidence Threshold
```

### 25.3 Required Output

```text
Evidence Record
Source Attribution (URL, record ID)
Metrics (value, unit, sample size)
Underlying Formula (if derived)
Linked Source Records (source_event, source_deck, etc.)
Generated timestamp
Reproducibility notes
```

### 25.4 Interface

Provide a dedicated page or modal that lists all evidence items matching filters. Each item is expandable to show full provenance, satisfying the Provenance Rule.

---

## 26. UNIFIED EVIDENCE LAYER

### 26.1 Purpose

The Unified Evidence Layer combines:

```text
Tournament evidence
Recommendation metrics
Primer links and metadata
Source‑provided archetype labels
Combo evidence
Package evidence
Probability simulation results
Card performance analytics
Historical meta intelligence
Regional meta intelligence
```

### 26.2 Evidence Bundle

Every evidence item must include:

```text
claim_type
claim_text
source_type
source_name
source_url or source_record_id
metric_value
metric_unit
sample_size
confidence
recency_window
generated_at
reproducibility_notes
```

### 26.3 Deck Analysis Output

**Tabs:**
```text
Overview
Recommendations
Tournament Meta
Card Performance
Primers
Combos
Packages
Probability Lab
Compare
Query Helper
Search
```

**Overview card:**
```text
Commander identity
Sourced labels
Meta standing
Last 30/90/365/all‑time evidence toggles
Top evidence‑backed card candidates
Top low‑evidence/outlier cards
Top card performance leaders
Probability highlights
Primer highlights
Combo highlights
Package highlights
Source coverage summary
Deduplication confidence summary
Evidence Stack visualization
Evidence Explorer link
Deck Comparison link
```

### 26.4 No Unsupported Strategic Summary

**Forbidden overview text:**
```text
This deck is trying to...
The game plan is...
This deck should...
```

**Allowed overview text:**
```text
Comparable canonical decks most frequently include...
Top tournament sources report...
Known primers found...
Commander Spellbook combos detected...
Simulation config X produced...
Evidence Stack shows...
```

---

## 27. EVIDENCE STACK UI CONCEPT

### 27.1 Purpose

Every recommendation should expose source support in a visual format.

### 27.2 Example

```text
Mystic Remora
Tournament Evidence ██████████
Primer Evidence ███████
Package Evidence █████
Simulation Evidence ██████
Total Evidence Score
```

### 27.3 Rules

The score is not an AI score. It is a visualization of evidence volume.

### 27.4 Required Use Cases

```text
Recommendations
Card Pages
Commander Pages
Unified Analysis
Evidence Explorer
```

---

## 28. NATURAL LANGUAGE QUERY HELPER

### 28.1 Purpose

High priority feature:

```text
Natural language → Scryfall syntax
```

**Examples:**
```text
"MDFCs that can enter untapped" → Scryfall query
"Activated abilities that do not tap" → Scryfall query
"Blue interaction under two mana legal in commander" → Scryfall query
```

### 28.2 Rules

```text
Scryfall query helper does not invent card truth.
Generated syntax must be shown to user.
Scryfall validation should be available when online.
Offline mode uses local Scryfall cache where possible.
```

### 28.3 Module

```text
codie/query_helper/nl_to_scryfall.py
codie/query_helper/syntax_validator.py
codie/query_helper/examples.py
```

---

## 29. EXPORT & OBSIDIAN INTEGRATION

### 29.1 Purpose

Allow Codie evidence outputs to be saved as portable files and Obsidian‑ready notes.

### 29.2 Required Supported Exports

```text
Commander staples report
Deck evidence report
Recommendation evidence bundle
Tournament meta report
Primer index report
Combo/package report
Simulation batch report
Commander Intelligence Page
Card Intelligence Page
```

### 29.3 Obsidian Export Requirements

```text
Markdown output with YAML frontmatter
Stable note paths
Commander notes grouped under commander folders
Deck reports grouped under deck folders
Source links preserved
Tables rendered in standard Markdown
Optional Dataview‑friendly fields
No plugin dependency required
```

### 29.4 Default Obsidian Folder Structure

```text
Codie/
├── Commander Staples/
├── Deck Reports/
├── Tournament Meta/
├── Primers/
├── Combos and Packages/
├── Simulation Reports/
├── Commander Intelligence/
└── Card Intelligence/
```

### 29.5 Acceptance

```text
Commander staples report exports to Obsidian Markdown.
CSV export opens cleanly in Excel/LibreOffice.
JSON export preserves source attribution.
Markdown export preserves formulas and methodology.
No export depends on cloud services.
```

### 29.6 Deferred Mobile Report Access

Codie should eventually support low-priority mobile viewing of reports while the
actual program continues to run on the user's PC.

Purpose:

```text
Run Codie locally on the PC.
Generate a phone-readable evidence report.
Let the user view the finished report on a phone without making the phone run Codie.
```

Allowed delivery options:

```text
static HTML report file
Markdown report file
PDF report file
QR code linking to a generated report
local network read-only report URL
manual file transfer to phone
Discord message or webhook notification with summary/link
optional external PDF-to-link service for manually approved uploads
```

Required rules:

```text
PC remains the execution host.
Mobile access is read-only.
Reports must preserve source attribution and generated_at metadata.
Reports must use evidence-only language.
No mobile path may expose write access to the database.
No cloud delivery is required for V1.
Discord or other message delivery must be optional and explicitly configured.
Any webhook/token must live in local config or environment variables, never in code.
External link services must never receive private deck data unless the user explicitly chooses that export.
```

Preferred V1 shape:

```text
Generate a static HTML/Markdown/PDF report.
Generate a QR code to the local file or local read-only URL.
Optionally send a Discord notification containing only a short summary and link/file.
Optionally allow manual export to a PDF-to-link service outside Codie.
```

This is a convenience feature, not a recommendation feature, analytics source,
or provider integration.

---

## 30. UI TECHNOLOGY DECISION

### 30.1 Locked Stack for V1

**Frontend Framework:** React with TypeScript  
**Build Tool:** Vite  
**Styling:** Tailwind CSS  
**UI Component Library:** shadcn/ui (Radix UI primitives)  
**Charts:** Recharts (or Chart.js if Recharts licensing issues)  
**Backend:** Python (FastAPI or Flask) – serves API and static files  
**Database:** SQLite (via `sqlite3` and `aiosqlite` for async)  
**Desktop Packaging:** Electron or Tauri (target: Windows, macOS, Linux) – decision deferred until UI is functional, but local‑first means no cloud.

### 30.2 Rationale

- React + TypeScript is widely understood and has strong ecosystem.
- Tailwind + shadcn/ui provides a clean, customizable component library without heavy dependencies.
- Python backend matches the existing codebase and AI assistant strengths.
- SQLite keeps everything local and zero‑cost.
- Electron/Tauri will be added as a packaging layer; the core will be a local web app.

---

## 31. FIXTURE CATALOG

### 31.1 Purpose

All tests must use stable fixtures to avoid breakage from external changes.

### 31.2 Fixture Directory Structure

```text
tests/fixtures/
├── scryfall/
│   ├── bulk_oracle_cards_sample.json
│   └── card_lookup_samples.json
├── topdeck/
│   ├── event_12345.json
│   └── deck_67890.json
├── edhtop16/
│   ├── graphql_query_result.json
│   └── commander_meta_sample.json
├── mtgtop8/
│   ├── event_page_123.html
│   └── decklist_page_456.html
├── mtgdecks/
│   ├── event_page_789.html
│   └── deck_export.txt
├── hareruya/
│   ├── deck_page_101.html
│   └── metagame_page_202.html
├── moxfield/
│   ├── deck_abcdef.json
│   └── primer_ghijkl.html
├── spellbook/
│   ├── combos_variants.json
│   └── combo_123.json
├── simulation/
│   ├── known_traces/ (precomputed deterministic outputs)
│   └── card_definitions_sample.json
├── canonicalization/
│   ├── event_dedupe_cases.json
│   └── deck_hash_cases.json
└── curated/
    ├── commander_aliases.json
    └── package_definitions.json
```

### 31.3 Fixture Policy

- Each fixture must include a `source-notes.md` describing its origin and date.
- Fixtures are read‑only; never modified by tests.
- When external data changes, fixtures are updated manually and tests are re‑validated.

---

## 32. ACCEPTANCE TEST MATRIX

### 32.1 Database

```text
Bootstraps from empty SQLite file.
Foreign keys reject invalid references.
Required indexes exist.
Repository tests cover insert/read/update.
Raw JSON can be stored and retrieved.
```

### 32.2 Scryfall

```text
Loads bulk data fixture.
Resolves exact name.
Resolves fuzzy name.
Stores scryfall_id and oracle_id.
Handles MDFCs/card faces.
Extracts commander legality.
Extracts produced mana.
```

### 32.3 Providers

```text
Provider never writes DB directly.
Provider emits candidate models.
Parser handles missing optional fields.
Parser fails cleanly on invalid payload.
Raw payload is preserved.
```

### 32.4 Canonicalization

```text
Same event across sources dedupes.
Distinct events with similar names do not dedupe incorrectly.
Same decklist hashes identically.
One‑card difference changes deck_hash.
Auxiliary cards excluded from deck_hash.
Commander signature generation works.
```

### 32.5 Tournament Weighting

```text
Event size formula deterministic.
Placement weights deterministic.
Recency decay deterministic.
Source confidence applied.
Duplicate source event does not double count.
Sample size warnings display.
```

### 32.6 Card Performance Metrics

```text
Raw inclusion rate calculates correctly.
Weighted inclusion rate applies placement weights.
Winner inclusion rate filters winners.
Top cut inclusion rate filters top cut.
Win rate delta calculates with sample size guardrails.
Trend values update for all time windows.
```

### 32.7 Historical Snapshots

```text
Snapshot generation creates consistent state.
Commander growth detects fastest growers.
Card growth detects emerging staples.
Meta share changes calculate correctly.
Regional changes tracked.
```

### 32.8 Evidence Counts

```text
Tournament evidence counts match canonical deck counts.
Primer evidence counts match primer registry matches.
Combo evidence counts match detected combos.
Package evidence counts match package matches.
Simulation evidence counts match relevant simulations.
Evidence Stack displays correctly.
```

### 32.9 Recommendations

```text
Calculates inclusion rate.
Calculates lift.
Calculates confidence.
Applies generic staple penalty.
Produces evidence text with source attribution.
Rejects unsupported strategy language in templates.
```

### 32.10 Primers

```text
Finds exact commander.
Finds exact partner pair.
Detects primer route.
Detects primer content presence.
Captures objective metadata.
Ranks top 5.
Does not store primer body.
```

### 32.11 Combos / Packages

```text
Syncs Spellbook fixture.
Maps combo cards through Scryfall.
Detects present components.
Detects missing components.
Calculates package completion.
Does not invent combo lines.
```

### 32.12 Simulation

```text
Seeded shuffle deterministic.
Mulligan policy deterministic.
Mana cost payment works.
Fast mana acceleration affects target timing.
Tutors can find supported targets.
Batch multi‑target evaluates shared histories.
Margin of error calculated.
Action traces emitted.
Simulation evidence appears only when threshold met.
```

### 32.13 Commander Pages

```text
Meta share displays correctly.
Historical trends show growth/decline.
Card usage shows most played cards.
Card performance shows win rate deltas.
Primer discovery shows top primers.
Evidence Stack displays.
```

### 32.14 Card Pages

```text
Inclusion rates display for all windows.
Winner and top cut inclusion display.
Commander usage shows which commanders play the card.
Historical trends show growth/decline.
Evidence Stack displays.
```

### 32.15 Commander Staples Explorer

```text
Tymna/Kraum query defaults to last 6 months and Top 16 scope.
Partner‑pair matching requires both commanders.
Staples are calculated from canonical decks only.
Frequency, inclusion percentage, and observed quantity display correctly.
Source deck/event links are attached as attribution.
CSV, Markdown, JSON, and Obsidian exports work.
Generic staple filter works.
Date‑range filter changes result set deterministically.
```

### 32.16 Deck Comparison

```text
Compares user deck vs canonical deck.
Shows shared cards, missing staples, missing packages, missing combos.
Displays card performance differences.
Similarity score calculated.
```

### 32.17 Evidence Explorer

```text
Filters by source type, provider, date range, region, evidence type.
Displays evidence record with source attribution, metrics, formula, and links.
Every evidence item satisfies Provenance Rule.
```

### 32.18 Export And Obsidian

```text
Markdown reports contain YAML frontmatter.
Obsidian paths are stable and human‑readable.
Tables render correctly in standard Markdown.
Dataview‑friendly fields are present but not required to use.
Exports do not mutate canonical data.
```

### 32.19 Unified Evidence

```text
Every evidence item has source or formula attribution.
Evidence bundle exports to Markdown.
Unsupported claims blocked by templates.
User labels are displayed as user labels.
Source labels are displayed as source labels.
Evidence Stack visualizes evidence volume.
```

### 32.20 Source Classification

```text
Matrix correctly identifies card truth, deck truth, tournament truth, primer truth, combo truth.
Analytics pipelines reject non‑eligible sources.
Primer pipelines use only primer sources.
```

### 32.21 Regional Metrics

```text
Regional commander metrics store region, time window, meta share.
Regional card metrics store region, time window, inclusion rates.
Regional package metrics store region, time window, adoption rates.
Filters by region work in Commander Pages and Card Pages.
```

### 32.22 Commander Signature

```text
Single commander generates signature correctly.
Partners sort alphabetically and use pipe separator.
Signature is consistent across all tables.
Historical snapshots use signature for grouping.
```

### 32.23 Schema Freeze

```text
No schema changes after Phase 1 without architecture review and migration plan.
```

### 32.24 Provenance

```text
Every metric displayed in UI includes formula, input datasets, time window, sample size, generated_at, source attribution.
No metric without lineage.
```

### 32.25 Implementation Quality Gate

```text
Contract defined before coding.
Complete files only.
Tests and test results included.
Architecture compliance check passed.
Completion report provided.
```

---

## 33. IMPLEMENTATION QUALITY GATE

No implementation is accepted unless it passes all gates below.

### 33.1 Contract First

Before coding, each task must define:

- files created
- files modified
- public functions/classes
- table/schema impact
- dependencies
- test cases
- failure modes

### 33.2 Complete File Rule

DeepSeek must return **complete files only**.

**Forbidden:**
- partial snippets
- TODO stubs
- placeholder imports
- “continue from here”
- untested helper functions
- hidden assumptions

### 33.3 Test Before Report

Every implementation must include:

- unit tests
- integration tests where relevant
- negative‑path tests
- fixture‑based tests
- command used to run tests
- actual test result

### 33.4 Architecture Compliance Check

Each task must verify:

- providers do not write DB
- no raw SQL outside repositories/bootstrap
- analytics use canonical tables only
- Scryfall remains card truth
- source payloads are preserved
- evidence claims have provenance
- no strategy inference language appears

### 33.5 Schema Safety

After Phase 1:

- no destructive schema changes
- migrations required for every schema change
- schema changes must update tests
- schema changes must update `SCHEMA_SPEC.md`

### 33.6 Fixture Requirement

Any parser/provider feature must include fixtures.

**Required:**
- successful fixture
- malformed fixture
- missing optional field fixture
- missing required field fixture

### 33.7 Repository Quality

Repositories must:

- use parameterized SQL only
- expose clear read/write methods
- validate required fields
- return typed/domain objects where possible
- handle missing rows cleanly
- avoid leaking sqlite‑specific details upward

### 33.8 Error Handling

Every subsystem must define expected failures.

**Required:**
- clear exception type
- useful message
- logged context
- retryable/non‑retryable flag where relevant
- no silent failure

### 33.9 Determinism

Analytics and simulation must be reproducible.

**Required:**
- stable sorting
- stored config JSON
- stored timestamps
- stored seed for simulations
- deterministic fixture tests

### 33.10 Completion Report Required

Every implementation response must end with:

- Task Name
- Objective
- Files Created
- Files Modified
- Work Completed
- Tests Added
- Tests Run
- Test Results
- Architecture Compliance Check
- Issues Found
- Recommended Next Step
- Roadmap Impact

### 33.11 Phase Packet And Handoff Rule

Work must proceed in bounded phase packets. A packet is not accepted unless it contains:

- locked contract document
- complete implementation files
- required fixtures or test data
- tests for success, failure, and boundary behavior
- exact test command and actual output
- static architecture compliance checks when relevant
- completion report
- updated handoff or next-phase document
- clean commit boundary when validation passes

The handoff document must be updated after each accepted packet and must include:

- current phase status
- files created or modified
- public functions/classes added
- schema impact, or explicit no-schema-impact statement
- tests added and full validation command
- known caveats or review notes
- recommended next packet
- explicit do-not-do list for the next packet

If validation cannot be executed locally, the packet must remain uncommitted until validation succeeds or the handoff records the exact missing runtime/tooling blocker.

Large phases must be split into separately validated packets. Each packet should be small enough to review independently and must preserve the same shape:

```text
contract -> code -> tests -> validation -> completion report -> handoff -> commit
```
---

## 34. BUILD ORDER

### Phase 0 — Reference Preservation And Roadmap Freeze

**Deliverables:**
```text
docs/CODIE_V1_CONSTITUTION.md
reference/ folder tree
old code archive manifest
source catalog notes
```

**Acceptance:**
```text
All uploaded research has a destination.
Old docs are reference‑only.
Conflicts are resolved in master document.
DeepSeek does not need prior chat context.
```

### Phase 1 — Schema And Repository Foundation

**Deliverables:**
```text
db/schema/*.sql (includes all tables: core, source, canonical, curated, user, simulation, analytics, regional)
db/bootstrap.py
db/connection.py
db/pragmas.py
db/repositories/*.py
canonical/signature.py
tests/test_schema.py
```

**Acceptance:**
```text
SQLite database boots from scratch.
Foreign keys enabled.
All tables created.
Indexes created.
Repository layer passes basic insert/read tests.
Commander signature generation works.
No raw SQL outside db/repositories and db/bootstrap.
Quality Gate passed.
```

### Phase 2 — Scryfall Truth Layer

*(Build order continues as previously defined, with all new subsystems inserted at appropriate places.)*

---

## 35. IMMEDIATE NEXT TASKS

### Task 1 — Save Constitution

Save this file as:

```text
docs/CODIE_V1_CONSTITUTION.md
```

### Task 2 — Create Reference Folder Tree

Create:

```text
reference/recommander/
reference/cedhdata_simulator/
reference/rhystic_simulator_traces/
reference/moxfield/
reference/ddb/
reference/topdeck/
reference/edhtop16/
reference/mtgtop8/
reference/mtgdecks/
reference/hareruya/
reference/spellbook/
reference/github_repos/
reference/ux_references/
reference/old_code_archives/
```

Each folder gets:

```text
source-notes.md
raw/
fixtures/
```

### Task 3 — Freeze Schema Spec

Split Section 10 into:

```text
docs/SCHEMA_SPEC.md
db/schema/core.sql
db/schema/source.sql
db/schema/canonical.sql
db/schema/curated.sql
db/schema/user.sql
db/schema/simulation.sql
db/schema/analytics.sql
db/schema/indexes.sql
```

### Task 4 — Freeze Dependency Rules

Create:

```text
docs/DEPENDENCY_RULES.md
```

Use Section 8.

### Task 5 — Freeze Ingestion Contracts

Create:

```text
docs/INGESTION_CONTRACTS.md
```

Use Section 12.

### Task 6 — DeepSeek Implementation Handoff

Send DeepSeek only after Tasks 1 through 5 are complete.

**First implementation target:**

```text
Phase 1 — Schema And Repository Foundation
```

**The Quality Gate is enforced for all submissions.**

---

## 36. AI HANDOFF INSTRUCTIONS

### 36.1 New ChatGPT Session Handoff

**Role:**
```text
You are the Codie architecture and roadmap hub.
```

**Primary responsibility:**
```text
Preserve this constitution.
Prevent scope drift.
Generate precise subsystem contracts.
Prepare implementation prompts.
Do not invent implementation details that conflict with this document.
```

**Rules:**
```text
Evidence‑first correction overrides older strategic‑inference language.
DeepSeek implements locked contracts.
Claude validates architecture.
Old code is reference only.
No paid dependencies.
No roadmap additions unless crucial.
Quality Gate enforced for all implementations.
```

**Immediate context:**
```text
The next actual build artifact is schema + repositories.
Do not start provider adapters before the schema and repository layer exist.
```

### 36.2 Claude Validation Handoff

**Role:**
```text
You are the architecture validation and continuity layer.
```

**Validate:**
```text
Schema consistency
Dependency direction
Provider isolation
Canonical/source separation
Evidence‑first compliance
Zero‑cost compliance
Build‑order sanity
Old‑code contamination risk
Card Performance Metrics Layer integration
Historical Snapshot System integration
Evidence Count Aggregation integration
Commander/Card Pages integration
Source Classification Matrix respect
Commander Signature generation consistency
Regional tables population
Evidence Explorer provenance
Deck Comparison canonical‑data usage
Simulation evidence integration thresholds
Schema Freeze adherence
Provenance Rule enforcement
Quality Gate compliance
```

**Reject if:**
```text
Providers write DB directly.
Analytics read source tables directly.
DeepSeek is asked to design schema semantics.
Any implementation introduces paid services.
Any module invents strategic conclusions.
Evidence counts are missing.
Commander pages include unsupported strategy claims.
Card pages include unsupported strategy claims.
Quality Gate checks are not satisfied.
```

### 36.3 DeepSeek Implementation Handoff

**Role:**
```text
You are the implementation engine.
You do not own architecture.
```

**Implement:**
```text
Complete runnable files.
No pseudocode.
No TODO stubs.
No undefined imports.
No raw SQL outside db/bootstrap and db/repositories.
No provider DB writes.
No schema redesign unless asked by ChatGPT after Claude validation.
```

**First assignment:**
```text
Create package tree.
Create db/schema SQL files from SCHEMA_SPEC.md.
Create db/connection.py, pragmas.py, bootstrap.py.
Create repository classes for core/source/canonical/analytics/regional tables.
Create canonical/signature.py.
Create tests/test_schema.py.
Run tests.
Return completion report.
```

**Completion report format must follow Quality Gate requirements.**

### 36.4 Quality Gate Validation

Claude and ChatGPT must verify that each implementation response includes:
- Contract definition before coding
- Complete files only
- Tests and test results
- Architecture compliance check
- Completion report

---

## 37. CONFLICT RESOLUTION LOG

| Conflict | Decision | Reason |
|---|---|---|
| "Unified Analysis Layer" vs "Unified Evidence Layer" | Use **Unified Evidence Layer** | Later evidence‑first correction overrides AI strategy language. |
| "Archetype Detection" vs "Archetype Evidence Indexing" | Use **Archetype Evidence Indexing** | Codie may store sourced labels, not infer archetypes. |
| "Primer Intelligence" vs "Primer Discovery and Indexing" | Use **Primer Discovery and Indexing** | Codie links to primers, stores metadata, and avoids copying strategy content. |
| `scryfall_id` vs `oracle_id` as canonical | Store both; `scryfall_id` PK, `oracle_id` analytics grouping | Scryfall object identity and functional card identity solve different problems. |
| "One URL = one deck" vs immutable deck hashes | Source deck = URL/submission; canonical deck = deck hash | Prevents duplicate analytics while preserving source fidelity. |
| DeepSeek designs schema vs implements schema | DeepSeek implements locked schema | Schema semantics belong to architecture layer, not implementation improvisation. |
| Old code reuse vs remaster/rebuild | Old code is reference‑only unless explicitly migrated through new architecture | Prevents legacy entropy from infecting the rebuild. |
| Legacy project archives as upgrade sources | Mine only for fixtures, aliases, workflow ideas, export formats, threshold candidates, and simulator/rules references | Preserves useful history without allowing stale architecture, copied scraper code, or old analysis claims into Codie. |
| User workflow extension patches | Deck memory, Moxfield-compatible export, ratio-aware confidence, and LLM-assisted naming are deferred contract-first roadmap items | Preserves useful product direction while blocking private deck leakage, unsupported uploads, LLM-as-truth behavior, and premature schema churn. |
| LLM naming reliability | Use separate writer and auditor roles before human/deterministic approval | Reduces hallucinated aliases and prevents a single model output from becoming project truth. |
| Interactive Intelligence Layer | Deferred contract-first roadmap item; chat must use Codie tools, evidence graphs, citations, and uncertainty before LLM language | Preserves the value of an in-app assistant while blocking generic LLM guessing, primer body retention, private deck leakage, provider/source bypasses, and unsupported recommendation claims. |
| Tag Graph Lab | Deferred contract-first roadmap item; functional tag graphs must use canonical card identities, provenance, numeric tables, underlying card lists, and low-sample/coverage caveats | Preserves the value of functional deck visualization while blocking strategic claims, user-deck leakage into commander averages, and premature schema/UI work. |
| Recommendation/cut language | Evidence candidates and low‑evidence/outlier cards only | Codie must not become an AI coach making unsupported claims. |
| cEDHStats patch integration | Full merge of Card Performance Metrics, Historical Snapshots, Evidence Counts, Commander/Card Pages, Evidence Stack | Required for Codie's core differentiators. |
| Evidence Stack source | Visual evidence volume, not AI score | Maintains Evidence First Rule compliance. |
| Commander staples explorer | V1 locked evidence feature; calculated from canonical records | Prevents manual staple lists and unsupported claims. |
| Source Classification ambiguity | Full matrix created | Prevents AI sessions from misusing sources. |
| Commander signature formats | Alphabetical normalized names with pipe | Single, enforceable rule. |
| Regional metrics storage | New dedicated tables | Avoids recomputation on every query. |
| Evidence Explorer scope | Dedicated section with filters and provenance | Required for transparency. |
| Deck Comparison scope | Explicit section with outputs | Already implied; now locked. |
| Simulation evidence integration | Conditional inclusion in Evidence Stack | Prevents noisy simulation results from polluting evidence. |
| Provenance requirement | New governance rule | Core to Codie's identity. |
| Schema changes after Phase 1 | Freeze rule | Prevents churn. |
| Implementation quality expectations | Formal Quality Gate introduced | Prevents incomplete, untested, or architecture‑violating code from entering the codebase. |

---

## 38. UNRESOLVED ITEMS

These are not blockers for Phase 1.

### 38.1 TopDeck API Key Handling

TopDeck API appears free but may require API key and attribution. Implementation must use local config and document attribution requirements.

### 38.2 DDB Parser Details

DDB is approved for primer/classification evidence, but exact parser structure still needs validation fixtures.

### 38.3 Moxfield Stability

Moxfield primer discovery is V1‑ready from research, but any unofficial endpoint or rendered‑page parser must be fixture‑tested and isolated behind provider contracts.

### 38.4 Archidekt Timing

Archidekt is approved but lower priority than Moxfield and DDB. Implement only after primary primer workflow works.

### 38.5 Simulator Card Coverage

The probability engine MVP covers a limited card/effect set. Expanding card definitions must be incremental and fixture‑driven.

### 38.6 License Review

All GitHub repos and uploaded archives are reference‑only until license review.

### 38.7 UI Framework Packaging

Electron vs Tauri decision deferred until UI is functional.

### 38.8 Fixture Maintenance Process

Manual updates required when external sources change; process to be defined later.

### 38.9 Regional Country Codes

ISO 3166‑1 alpha‑2 codes will be used; region mapping to be curated.

---

## 39. FINAL BUILD DIRECTIVE

The next real implementation task is:

```text
Phase 1 — Schema And Repository Foundation
```

**Implementation order:**
1. Package tree
2. SQL schema files (including all additions: regional tables, signature support)
3. SQLite bootstrap
4. Repository layer
5. Schema tests
6. Completion report with all quality gate checks satisfied.

**Do not build recommendation engine first. Do not build simulator first. Do not build UI first. Do not let a provider write to SQLite because "it was faster."**

Codie must be rebuilt from the architecture outward:

```text
Schema
→ Repositories
→ Scryfall truth
→ Provider contracts
→ Source ingestion
→ Canonicalization
→ Analytics (Tournament, Card Performance, Historical, Evidence Counts)
→ Commander & Card Pages
→ Evidence presentation
```

**This document is the definitive source of truth. It replaces all previous roadmaps, governance files, patches, and handoffs.**

**Implementation may now begin with Phase 1, subject to the Implementation Quality Gate.**

---

*End of Codie V1 Constitution — Implementation Ready*
