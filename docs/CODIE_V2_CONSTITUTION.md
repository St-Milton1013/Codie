# CODIE CONSTITUTION V2.0
## Ratified Master Constitution

**Version:** 2.0 Ratified
**Date:** 2026-07-20
**Last ratification amendment:** 2026-07-21
**Status:** RATIFIED — effective when the V2 adoption change is merged
**Authority:** Primary Codie constitution
**Supersedes prior documents:** Yes, for current constitutional governance
**Historical reference retained:** `docs/CODIE_V1_CONSTITUTION.md`
**Adoption basis:** V1/V2 comparison, live repository review, Codie/Jin handoff review, and explicit user decisions through 2026-07-20.

---

# PREAMBLE

Codie is a local-first competitive Commander intelligence system built to collect evidence, preserve provenance, calculate reproducible metrics, support controlled simulation, explain conclusions, and provide a grounded conversational strategy layer.

Codie is not a single model, a single database, a single recommender, or a collection of unrelated utilities. It is a governed system in which authority, observation, measurement, decision-making, theory, user context, and presentation remain distinct.

The project exists to answer four broad questions:

1. What is known?
2. What evidence supports it?
3. What can reasonably be concluded from that evidence?
4. What remains uncertain, speculative, unsupported, or worth testing?

Codie must remain useful without pretending uncertainty has disappeared. It must prefer traceable limits over polished invention.

---

# 1. DOCUMENT AUTHORITY AND CONSTITUTIONAL ORDER

## 1.1 Ratified status

This document is the ratified Codie V2 Constitution. It becomes the highest project authority when its adoption change is accepted and merged.

Ratification does not silently alter accepted implementation state:

- accepted phase contracts remain binding unless V2 explicitly conflicts with them;
- accepted validation findings and required fixes remain binding;
- active pull requests retain their recorded scope and validation state;
- roadmap and next-phase documents continue to govern implementation sequence;
- new V2 capabilities still require accepted contracts before implementation.

## 1.2 Ratification record

The adoption packet must preserve:

1. the V1/V2 change log;
2. the compatibility statement for accepted V1 phases and active pull requests;
3. architecture and adversarial validation evidence;
4. the prior constitution as an unchanged historical reference;
5. the effective date, adopted version, commit, and pull request identity.

## 1.3 Authority order after ratification

When governing documents conflict, the order shall be:

1. Ratified Codie Constitution.
2. Accepted architecture amendments.
3. Accepted phase contracts.
4. Accepted implementation contracts.
5. Accepted validation reports and required fixes.
6. Active roadmap and next-phase gate records.
7. Specifications and roadmap patches.
8. Research notes, references, and discussion records.

No lower document may silently override a higher document.

## 1.4 V1 preservation and carry-forward

`docs/CODIE_V1_CONSTITUTION.md` remains permanently available as historical architecture and decision context. It is not deleted, renamed, or rewritten by V2 adoption.

V1 product capabilities retain their V1 purpose, boundaries, and roadmap status unless V2 explicitly changes them. Two carry-forward exceptions are approved:

1. The standalone Natural Language Query Helper is folded into Jin query planning and the Scryfall/Tagger translation pipeline; the capability remains, but it is not a separate subsystem.
2. Mobile report delivery is deferred until separately contracted.

V1 text may clarify historical intent but may not override V2 after adoption.

---

# 2. PRODUCT IDENTITY

## 2.1 Codie is

Codie is a:

- local-first cEDH evidence platform;
- canonical tournament and deck intelligence system;
- reproducible analytics engine;
- controlled recommendation and deck-health system;
- probability and line-analysis environment;
- primer, archetype, combo, and package index;
- commander and card intelligence database;
- historical and regional metagame explorer;
- tournament-preparation system;
- grounded conversational theory partner through Jin-Gitaxias;
- research, teaching, and knowledge-vault system;
- private tool for approximately one to three trusted users.

## 2.2 Locked product equation

```text
Codie =
    Authority Layer
  + Canonical Data Foundation
  + Tournament Intelligence
  + Regional Intelligence
  + Measured Analytics
  + Frequency Pools
  + Functional Tag Intelligence
  + Relationship Intelligence
  + Co-occurrence and Co-dependence Metrics
  + Evidence Fusion
  + Decision Intelligence
  + Explainable Recommendations
  + Probability and Line Simulation
  + Primer and Theory Corpus
  + Jin-Gitaxias Strategist
  + Rules and Legality Support
  + Deck Memory and Snapshots
  + Reports, Exports, and Knowledge Vault
```

## 2.3 Codie is not

Codie is not:

- a public SaaS platform;
- a social network;
- a card marketplace;
- a collection manager unless separately approved as user context;
- a replacement for Moxfield or Archidekt;
- a fully autonomous deck editor;
- a source of ungrounded strategic certainty;
- a full multiplayer Magic rules engine;
- an opponent-playing game engine;
- a substitute for official rules, judges, or tournament policy;
- a system that treats community opinion as measured tournament truth;
- a system that lets an LLM modify canonical evidence;
- a system that hides uncertainty behind a single score.

## 2.4 Primary workflow

```text
Import or select deck
    ->
Normalize card and commander identity
    ->
Resolve snapshot and source lineage
    ->
Retrieve canonical evidence
    ->
Calculate approved metrics
    ->
Build Unified Evidence
    ->
Run Decision Intelligence where requested
    ->
Present action-first findings
    ->
Allow Jin to discuss, test, compare, and explain
    ->
Export evidence, notes, or experiments
```

The user remains the final decision-maker.

---

# 3. FOUNDATIONAL PRINCIPLES

## 3.1 Evidence before conclusion

Every conclusion must be traceable to evidence, user context, a declared model, or declared speculation.

## 3.2 Authority before observation

Official rules and canonical card identity override lower-level sources.

## 3.3 Canonical before analytics

Raw provider records never directly power analytics.

## 3.4 Measurement before recommendation

Recommendation output must consume measured evidence through approved evidence-fusion and decision-intelligence boundaries.

## 3.5 Explanation before persuasion

Codie must explain why an output exists before presenting it as useful.

## 3.6 Visible uncertainty

Confidence, sample size, coverage, conflicts, caveats, unsupported elements, and speculation must remain visible.

## 3.7 Local-first by default

Private decks, notes, traces, settings, and user context remain local unless the user explicitly exports or authorizes external processing.

## 3.8 Reproducibility

Equivalent inputs, versions, seeds, filters, and profiles must produce equivalent deterministic outputs where the subsystem is deterministic.

## 3.9 Separation of concerns

Providers collect. Repositories persist. Canonicalization resolves identity. Analytics measure. Evidence Fusion packages. Decision Intelligence concludes. Jin converses and theorizes. The UI presents.

## 3.10 No silent mutation

No subsystem may silently change:

- canonical identity;
- historical evidence;
- source records;
- user deck snapshots;
- recommendation history;
- simulator history;
- theory corpus provenance;
- validation status.

## 3.11 Unknown and abstention states

Codie must distinguish `zero`, `unknown`, `unavailable`, `unsupported`, `not applicable`, `insufficient coverage`, and `blocked by legality`.

Missing information must never silently become zero, false, or a negative recommendation. Downstream packets and reports must preserve the originating unknown or abstention state.

---

# 4. GOVERNANCE

## 4.1 Zero-cost rule

Codie must remain operable without additional recurring cost.

Forbidden by default:

- paid APIs;
- pay-per-request scraping;
- paid cloud databases;
- paid vector services;
- required subscriptions;
- metered LLM dependencies;
- commercial data licenses;
- mandatory hosted infrastructure.

A paid exception requires explicit user approval, documented free alternatives, cost limits, privacy impact, and an exit path.

An existing personal subscription does not automatically authorize Codie to depend on it.

## 4.2 No partial implementations

Implementation deliverables may not consist of:

- pseudocode presented as finished code;
- TODO-only modules;
- unresolved imports;
- placeholder persistence;
- untested stubs;
- hidden manual steps;
- broad promises without runnable behavior.

A complete implementation includes code, integration, tests, failure behavior, and a completion report.

## 4.3 Contract-first development

Before implementation, each phase must define:

- purpose;
- authorized scope;
- prohibited scope;
- public interfaces;
- files created or modified;
- schema impact;
- repository impact;
- dependencies;
- data flow;
- failure behavior;
- acceptance tests;
- validation packet;
- next allowed phase.

## 4.4 PR-only governed flow

Governed implementation should use reviewable branches and pull requests.

Direct changes to the protected mainline are prohibited unless an emergency process is explicitly invoked and later reviewed.

## 4.5 Validation model

Each governed phase should use:

1. deterministic validation;
2. architecture validation;
3. adversarial validation;
4. aggregate validation;
5. outside-validation decision;
6. unresolved-finding check.

Automated repair may be attempted up to the approved limit. Repair must not broaden scope.

## 4.6 Advancement rule

A phase may advance when:

- required validation returns an allowed passing verdict;
- required fixes are applied and revalidated;
- no unresolved blocking finding remains;
- the next-phase contract is designated;
- governance records are updated.

Nonblocking review notes do not prevent advancement unless the validation packet says otherwise.

## 4.7 Scope stabilization

When the user declares a stabilization period, such as “no more adjustments until working order,” new feature work must be logged without disrupting the active implementation chain.

## 4.8 Completion reports

Every completed task must record:

- task name;
- objective;
- scope;
- files created;
- files modified;
- work completed;
- design decisions;
- validation performed;
- results;
- issues and caveats;
- roadmap impact;
- next allowed step.

---

# 5. RESPONSIBILITY MODEL

## 5.1 User

The user:

- defines product intent;
- approves constitutional changes;
- approves source classifications;
- resolves ambiguous strategic priorities;
- provides corrections;
- controls private data release;
- accepts or rejects recommendations;
- determines when experimental findings become project requirements.

## 5.2 Architecture and research hub

The architecture hub:

- consolidates requirements;
- maintains conceptual consistency;
- identifies conflicts;
- prepares comparison and handoff documents;
- preserves source attribution;
- separates research findings from implementation authority.

## 5.3 Implementation agent

The implementation agent:

- implements accepted contracts;
- does not invent schema or architecture;
- provides complete files;
- writes tests;
- reports validation;
- does not broaden scope because a nearby feature seems convenient.

## 5.4 Validators

Validators:

- inspect only the declared packet;
- distinguish blocking findings from informational notes;
- verify constitutional and contract boundaries;
- do not implement unrelated improvements;
- provide reproducible evidence for verdicts.

## 5.5 Jin-Gitaxias

Jin is a first-class conversational subsystem, not a source of canonical truth and not an alternate recommendation engine.

Jin’s responsibilities are defined in Section 24.

---

# 6. SYSTEM ARCHITECTURE AND EVIDENCE CLASSES

## 6.1 Constitutional layer model

```text
Class 0: Authority
Class 1: Source Observations
Class 2: Measured Evidence
Context Layer: Primers, Theory, and Community Material
Evidence Fusion
Class 3: Decision Intelligence
Class 4: User Context
Jin-Gitaxias Strategist
Presentation and Export
```

## 6.2 Class 0A: Rules and card authority

Approved authority includes:

- official Comprehensive Rules;
- official Oracle text and rulings;
- official release notes;
- official ban and restricted announcements;
- official tournament policy where relevant;
- Scryfall card identity and legality data.

Scryfall is authoritative inside Codie for:

- canonical card names;
- Oracle IDs;
- Scryfall IDs;
- Oracle text;
- type line;
- mana cost;
- color identity;
- legalities;
- rulings;
- card faces;
- print relationships;
- supported search syntax.

Official sources override Scryfall where an official update has not yet propagated.

## 6.3 Class 0B: Combo authority

Commander Spellbook is authoritative for recognized combo records, requirements, outcomes, variants, and source links.

Codie may identify a listed combo. Codie may not claim Commander Spellbook is exhaustive.

## 6.4 Class 0C: Functional ontology authority

Scryfall Tagger is the primary functional-tag source.

Its authority is scoped:

- authoritative for the imported Tagger labels and their provenance;
- not proof that a label is philosophically complete;
- not proof that untagged cards lack the function;
- not permitted to override Oracle text;
- subject to versioning, alias normalization, and user-visible corrections.

Curated functional labels and user corrections must remain separately attributed.

## 6.5 Class 1: Observational sources

Class 1 stores source claims without independent reasoning.

Approved or proposed injection sources include:

- TopDeck;
- EDHTop16;
- MTGTop8;
- MTGDecks;
- Hareruya;
- cEDH.jp after acquisition validation;
- approved direct event records;
- approved user-supplied event imports.

Moxfield user deck imports are observations but are not tournament truth unless linked to a canonical tournament record.

## 6.6 Class 2: Measured evidence

Class 2 includes reproducible metrics such as:

- inclusion rate;
- weighted inclusion;
- meta share;
- weighted meta share;
- win rate;
- win-rate delta;
- top-cut conversion;
- placement weighting;
- adoption rate;
- trend delta;
- lift;
- support;
- confidence;
- coverage ratio;
- similarity;
- co-occurrence;
- co-dependence;
- package frequency;
- tag density;
- frequency pools;
- commander staples;
- simulator statistics;
- matchup and encounter exposure.

Class 2 may measure. It may not recommend.

## 6.7 Context layer

Context sources may explain evidence but may not override authority or measured evidence.

Examples:

- Moxfield primers;
- cEDH Decklist Database;
- Archidekt descriptions;
- Lotus Refinery only after research-candidate admission;
- curated strategy articles;
- Substack writers;
- books;
- videos;
- podcasts;
- Reddit discussions;
- user notes;
- deck primers;
- theory corpus material.

## 6.8 Class 3: Decision Intelligence

Decision Intelligence is the only subsystem authorized to produce persisted recommendation conclusions, deck-health conclusions, replacement proposals, and recommendation confidence.

## 6.9 Class 4: User context

User context includes:

- selected deck;
- owned cards;
- budget;
- local metagame;
- ignored cards;
- locked cards;
- testing notes;
- matchup experience;
- preferred play style;
- deck-specific principles;
- user corrections;
- experimental goals.

User context personalizes output. It does not rewrite global evidence.

---

# 7. SOURCE POLICY

## 7.1 Source roles must remain explicit

Each source must declare whether it is approved for:

- card authority;
- rules authority;
- combo authority;
- tournament observation;
- deck observation;
- regional discovery;
- primer context;
- archetype labels;
- theory corpus;
- UI reference;
- implementation reference;
- analytics eligibility.

## 7.2 Injection-source policy

TopDeck, EDHTop16, MTGTop8, MTGDecks, Hareruya, and any approved regional event source are injection sources.

Injection records must be normalized, deduplicated, and canonicalized before analytics.

## 7.3 cEDH.jp policy

cEDH.jp is proposed as:

- Japanese regional discovery;
- tournament article ingestion;
- source-lineage enrichment;
- event metadata enrichment;
- decklist import where present;
- analytics input only after canonical deduplication.

It must preserve original linked sources and distinguish discovery source from originating source.

## 7.4 cEDHStats policy

cEDHStats and similar products are:

- methodology references;
- UI references;
- cross-check surfaces;
- discovery aids.

They are not independent evidence when their underlying data derives from another source already ingested.

## 7.5 Primer-source policy

Primer sources may supply:

- title;
- author;
- date;
- commander identity;
- source-provided labels;
- section names;
- links;
- summary context;
- strategic claims attributed to the author.

Primer claims must remain attributed and may conflict with measured evidence.

## 7.6 Community-source policy

Reddit, Discord, social posts, and informal discussion are not tournament evidence.

They may be used by Jin for:

- hypothesis discovery;
- matchup anecdotes;
- terminology;
- disputed interactions;
- emerging technology;
- community questions.

Community retrieval has no fixed recency window. It must select material by relevance and temporal context, preserve publication dates, and label whether the material is current discussion or historical context.

## 7.7 Reddit RSS Community Signal Monitor

Reddit RSS or Atom retrieval is an approved post-checkpoint discovery capability, subject to a separate implementation contract.

Its constitutional classification is:

```text
Source role: Community Context / Discovery
Tournament injection: prohibited
Measured analytics: prohibited
Jin retrieval: permitted
Theory Corpus discovery: permitted
Default confidence: low
Permanent evidence: prohibited without separate validation and source promotion
```

The monitor may discover:

- newly discussed cards, commanders, decks, and community terminology;
- primers, articles, tools, websites, and repositories;
- tournament reports and local-metagame anecdotes that require independent verification;
- unusual interactions and frequently raised rules questions;
- potential Theory Corpus authors and works;
- contradiction, research, rules-review, tool-evaluation, and experiment candidates.

Feed acquisition should use a small governed registry and narrowly scoped temporary searches rather than indiscriminate subreddit harvesting. Illustrative patterns include:

```text
r/CompetitiveEDH/new.rss
r/CompetitiveEDH/top.rss?t=week
r/CompetitiveEDH/search.rss?q=primer&restrict_sr=1&sort=new
r/CompetitiveEDH/search.rss?q=tournament+report&restrict_sr=1&sort=new
r/CompetitiveEDH/search.rss?q=metagame&restrict_sr=1&sort=new
r/mtgrules/search.rss?q=commander&restrict_sr=1&sort=new
```

Eligible feed types may include chronological subreddit, time-bounded top, search, combined-community, attributed-user, and comment streams. User- or comment-specific monitoring requires an explicit research purpose and the same relevance and storage gates as post retrieval.

Temporary search feeds may be created for a commander, newly spoiled card, disputed combo, tournament, deck, archetype, or research term such as `primer`, `tournament report`, `deck tech`, or `GitHub`.

The intake path is:

```text
RSS or Atom item
  -> metadata intake
  -> Reddit post-ID deduplication
  -> card, commander, deck, tool, and topic detection
  -> transparent relevance tagging or scoring
  -> Community Signal Queue
  -> human or Jin review
  -> research, theory-candidate, rules-review, tool-evaluation, or experiment queue
```

Initial storage is limited to:

- Reddit post ID;
- subreddit;
- title;
- attributed author;
- publication time;
- canonical URL;
- discovering feed or search;
- a short compliant excerpt or generated summary;
- detected cards, commanders, and entities;
- relevance tags and score inputs;
- review status.

Full post or comment retrieval may occur only after a relevance gate and must remain purpose-limited. Codie must not build a permanent Reddit mirror or copy full posts and comment trees by default.

The monitor must:

- poll conservatively, normally every 30–60 minutes or on command;
- use conditional requests, caching, exponential backoff, and visible source-health state;
- pass current access-policy, terms, reuse, and acquisition review before implementation and whenever those conditions materially change;
- identify itself honestly where the transport permits;
- preserve attribution and links;
- honor deleted or removed content in stored discovery records;
- avoid bulk historical harvesting;
- keep community material separate from measured evidence;
- never use Reddit content to train Jin or another model;
- treat access changes, throttling, and source unavailability as expected provider states.

RSS discovery may not directly create tournament observations, measured analytics, recommendations, canonical evidence, or permanent Theory Corpus authority. Promotion requires separate review against the destination's governing source and evidence rules.

## 7.8 Research attribution

Research output must identify which source supports each material claim. Aggregated summaries must still preserve source-level provenance.

## 7.9 Reference implementation policy

Reference implementations may inform architecture or testing without becoming dependencies.

Examples:

- MTG Layer Inspector for continuous-effect and layer reasoning;
- Forge for rules-behavior validation;
- Delvefall for semantic-search ideas;
- graph libraries for visualization;
- external simulator bundles for behavior study;
- metagame exposure tools for analytical concepts.

No reference implementation becomes production authority without license, security, maintenance, and boundary review.

---

# 8. PROVENANCE AND SOURCE LINEAGE

## 8.1 No metric without lineage

Every displayed metric must be able to expose:

- formula;
- metric version;
- source datasets;
- canonical record identifiers;
- time window;
- region;
- placement scope;
- sample size;
- coverage ratio;
- generated timestamp;
- exclusions;
- known caveats.

## 8.2 Source lineage graph

Codie should preserve relationships such as:

```text
Canonical Event
  -> TopDeck record
  -> Hareruya page
  -> cEDH.jp article
  -> store page
  -> organizer announcement
  -> linked decklist
```

Discovery, mirror, and originating sources must not be conflated.

## 8.3 Conflict preservation

Conflicting values must remain visible until resolved by a defined rule or human review.

Codie must not silently discard:

- participant-count conflicts;
- date conflicts;
- pilot-name conflicts;
- commander conflicts;
- decklist differences;
- placement differences;
- provider attribution conflicts.

## 8.4 Raw-source preservation

Raw provider payloads, HTML, exports, and fixtures may be preserved under approved storage rules.

Raw source data must not leak into public or cloud outputs without authorization.

---

# 9. CANONICAL DATA PIPELINE

## 9.1 Required flow

```text
Acquire
  -> Preserve raw source
  -> Parse candidate records
  -> Normalize card and commander identity
  -> Validate required fields
  -> Persist source records
  -> Canonicalize and deduplicate
  -> Calculate analytics
  -> Build evidence
```

## 9.2 Provider boundary

Providers:

- fetch;
- parse;
- emit candidate models;
- preserve source metadata.

Providers never write directly to canonical tables.

## 9.3 Repository boundary

Database reads and writes occur through approved repositories except schema bootstrap and migration tooling.

## 9.4 Canonicalization boundary

Canonicalization determines whether source observations represent the same event, deck, commander signature, or card identity.

Canonicalization may not calculate strategic recommendations.

## 9.5 Analytics boundary

Analytics consume canonical records only.

Source records may be attached later for attribution but may not be counted directly.

---

# 10. CARD IDENTITY, ALIASES, AND LEGALITY

## 10.1 Card identity

Oracle ID is the primary functional identity for analytics.

Scryfall ID identifies a specific card object or face relationship where necessary.

## 10.2 Aliases

Aliases, nicknames, OCR variants, punctuation variants, and partner shorthand must resolve through an attributed alias registry.

LLMs may propose aliases but may not approve or persist them.

## 10.3 Unresolved names

An unresolved card name must:

- remain unresolved;
- appear in an unsupported or review queue;
- never be silently mapped to a guessed card;
- never enter canonical analytics.

## 10.4 Date-aware legality

Legality and ban checks must be date-aware when evaluating historical decks, simulations, or recommendations.

A card legal today must not be treated as legal in an earlier event if it was unavailable or banned, and vice versa.

## 10.5 Natural-language Scryfall translation

Codie may translate user language into Scryfall syntax.

It must show the generated query and validate against Scryfall or the local Scryfall cache.

This capability is owned by Jin query planning and the shared Scryfall/Tagger translation boundary. It is not a standalone Natural Language Query Helper subsystem.

---

# 11. DECK IDENTITY AND SNAPSHOTS

## 11.1 Immutable deck snapshots

Every analyzed deck may have an immutable snapshot containing:

- canonical commander signature;
- normalized mainboard;
- zones;
- source URL;
- source modified time where available;
- import time;
- deck hash;
- card-support status;
- user labels;
- analysis version.

## 11.2 Moxfield identity policy

On first analysis of a Moxfield deck:

1. Save the canonical URL and initial snapshot.
2. Record source identity and modified metadata.
3. On later analysis, recheck the source.
4. Diff against the prior snapshot.
5. Reuse cached analysis when unchanged.
6. Rerun affected analyses when changed.
7. Preserve prior snapshots.

## 11.3 Zone separation

Commanders, mainboard cards, companions, sideboards, sticker sheets, attractions, and auxiliary objects must remain separate.

Commander cards do not enter mainboard frequency pools.

Sideboard-only copies do not inflate mainboard frequency.

Auxiliary objects do not enter normal card analytics unless an explicit metric includes them.

## 11.4 User decks versus population evidence

A private user deck may be compared against canonical populations but must never enter commander averages, tournament frequencies, or global evidence unless explicitly imported as an approved observation.

---

# 12. TOURNAMENT AND EVENT INTELLIGENCE

## 12.1 Event identity

Canonical events should preserve:

- event name;
- date;
- organizer;
- store;
- city;
- region;
- country;
- format;
- player count;
- rounds;
- cut structure;
- source lineage;
- confidence;
- deduplication rationale.

## 12.2 Deck-instance identity

A tournament deck instance should preserve:

- event;
- pilot;
- commander signature;
- placement;
- record;
- deck hash;
- source links;
- region;
- date;
- provider lineage.

## 12.3 Historical retention

Tournament history does not decay out of storage.

Recency weighting affects selected metrics, not historical preservation.

## 12.4 Regional intelligence

Regional filtering should support:

- global;
- continent;
- country;
- state or province where available;
- city;
- store;
- organizer;
- tournament series.

Low regional sample sizes must be disclosed.

## 12.5 Event-size segmentation

Analyses may distinguish:

- local weekly;
- small event;
- medium event;
- major event;
- custom attendance bands.

Thresholds must be configurable and versioned.

---

# 13. TOURNAMENT EXPOSURE ANALYZER

## 13.1 Purpose

The Tournament Exposure Analyzer estimates the chance of encountering specific commanders, archetypes, cards, packages, or functional tags during a selected event structure.

## 13.2 Required inputs

- region;
- store or organizer;
- date window;
- expected attendance;
- number of rounds;
- event-size class;
- commander or partner pair;
- card, package, or functional tag;
- canonical metagame share;
- confidence and sample coverage;
- optional pairing model.

## 13.3 Required outputs

- per-round exposure estimate;
- tournament-wide encounter probability;
- commander exposure;
- archetype exposure;
- card exposure;
- package exposure;
- functional-tag exposure;
- regional comparison;
- local-organizer comparison;
- sample size;
- coverage;
- confidence;
- modeling assumptions.

## 13.4 Approximation disclosure

Simple independent-seat estimates must be labeled as approximations.

The core V2 analyzer begins with a labeled independent-seat approximation. It must expose its formula, source population, sample size, coverage, and an explicit warning that it is not a Swiss-pairing model.

Advanced versions may account for:

- three opponents per pod;
- Swiss pairing;
- repeat opponents;
- byes;
- pods formed from standings;
- event attendance;
- commander clustering;
- pilot and deck dependence.

## 13.5 Recommendation boundary

Exposure estimates are measured evidence. They do not directly generate tech recommendations.

Decision Intelligence may use them only through Unified Evidence.

---

# 14. ANALYTICS CONSTITUTION

## 14.1 Metric discipline

Every metric must define:

- numerator;
- denominator;
- inclusion and exclusion rules;
- grouping identity;
- time scope;
- region scope;
- placement scope;
- minimum sample;
- confidence method;
- version.

## 14.2 Approved metric families

- raw and weighted inclusion;
- commander and card meta share;
- placement-weighted usage;
- winner and top-cut inclusion;
- win rate and win-rate delta;
- conversion rates;
- adoption and trend;
- lift and support;
- generic-staple score;
- similarity;
- co-occurrence;
- co-dependence;
- package completion;
- tag density and coverage;
- source agreement;
- exposure probability;
- simulation rates.

## 14.3 No causal overclaim

Observational association does not prove a card caused better performance.

Language must distinguish:

- correlation;
- association;
- lift;
- observed delta;
- simulated difference;
- causal claim.

Causal claims require an approved design and must remain rare.

## 14.4 Low-sample handling

Low sample may:

- lower confidence;
- trigger caveats;
- restrict ranking;
- prevent recommendation confidence from reaching high.

Low sample may not be hidden.

---

# 15. FREQUENCY POOLS AND COMMANDER STAPLES

## 15.1 Frequency pools

Frequency pools may be built from:

- canonical tournament decks;
- approved Moxfield deck groups;
- manual decklist groups;
- user-selected source sets.

The source pool must always remain visible.

## 15.2 Commander staples

Default commander-staples behavior:

- exact commander or partner pair;
- last six months;
- Top 16 canonical tournament decks;
- mainboard only;
- frequency descending;
- placement-weighted frequency as secondary sort;
- exportable to Markdown, CSV, JSON, and Obsidian.

## 15.3 Partner matching

Exact partner-pair analysis requires both commanders.

Partial partner matching must be explicitly selected.

## 15.4 Missing-card flag

Codie may flag cards above a configurable frequency threshold, including the proposed 80% threshold, when absent from the analyzed deck.

This is an evidence flag, not an automatic recommendation.

## 15.5 Quantity handling

Commander normally uses one copy per deck, but quantity fields must remain correct for formats, companions, basic lands, and unusual source exports.

---

# 16. FUNCTIONAL TAGS AND TAG GRAPH LAB

## 16.1 Purpose

Functional tags allow Codie to compare what cards do rather than merely what card types they have.

## 16.2 Tag sources

- Scryfall Tagger;
- curated functional registry;
- explicit user corrections;
- source-provided labels where separately attributed.

## 16.3 Tag Graph Lab

The user may select one to six tags and compare:

- an analyzed deck;
- saved snapshot;
- commander baseline;
- partner-pair baseline;
- Top 16 pool;
- winner pool;
- regional pool;
- frequency pool;
- historical snapshot.

## 16.4 Required metrics

- raw tag count;
- tag density;
- tag inclusion rate;
- average tagged cards per matching deck;
- placement-weighted tag usage;
- winner frequency;
- Top 16 frequency;
- trend delta;
- matching decks;
- available decks;
- coverage ratio;
- confidence.

## 16.5 Transparency

Every tag graph must expose:

- contributing cards;
- numeric table;
- tag source;
- mapping version;
- coverage;
- exclusions.

## 16.6 Strategic boundary

Tag graphs are evidence and comparison tools.

Jin may discuss strategic implications with visible speculation, but tag graphs themselves do not issue strategic conclusions.

---

# 17. RELATIONSHIP INTELLIGENCE, CO-OCCURRENCE, AND CO-DEPENDENCE

## 17.1 Co-occurrence

Co-occurrence measures how often cards, tags, packages, or commanders appear together in an approved population.

## 17.2 Typed relationship graph

Relationship Intelligence represents evidence-bearing relationships among cards, tags, packages, combos, outputs, converters, commanders, decks, tournaments, regions, and attributed theory claims.

Every edge must declare its relationship type and evidence class. Statistical co-occurrence must not be confused with Tagger membership, Spellbook combo membership, a rules interaction, a curated package, or a theory claim.

## 17.3 Co-dependence metric family

For a selected canonical population, a card or element pair `A` and `B` must preserve:

```text
N   = population deck count
nA  = decks containing A
nB  = decks containing B
nAB = decks containing both A and B
```

Approved measured outputs are:

```text
support                    = nAB / N
directional confidence A→B = nAB / nA
directional confidence B→A = nAB / nB
dependence delta A→B       = P(B|A) - P(B)
dependence delta B→A       = P(A|B) - P(A)
lift                       = P(A,B) / (P(A) × P(B))
leverage                   = P(A,B) - P(A)P(B)
Jaccard similarity         = nAB / (nA + nB - nAB)
PMI                        = log2(lift)
```

Codie must not collapse these measurements into one opaque synergy score.

## 17.4 Population controls and disclosures

Every relationship result must expose:

- commander or exact partner-pair scope;
- mainboard, commander, sideboard, or auxiliary-zone scope;
- date range;
- region, store, organizer, event-size, and placement filters where applicable;
- canonical and deduplicated population size;
- `N`, `nA`, `nB`, and `nAB`;
- expected and observed co-occurrence;
- source references and metric version;
- coverage and low-sample caveats;
- known confounders and interpretation limits.

The calculation must control or visibly caveat color identity, commander restrictions, generic-staple prevalence, repeated deck snapshots, pilot concentration, regional effects, release recency, missing coverage, and known combo/package membership.

## 17.5 Metric-only boundary

Co-dependence is measured evidence only. It may enter Unified Evidence and may be discussed by Jin with explicit caveats, but the metric itself must not produce recommendations, causal claims, package truth, rules claims, or strategic conclusions.

Core V2 includes deterministic pair metrics, card-to-tag aggregation, filters, provenance, caveats, and table/pair-detail outputs. Automated package discovery, embeddings, replacement prediction, causal inference, and a dedicated graph database remain later contract work.

---

# 18. COMBO, PACKAGE, AND LINE INTELLIGENCE

## 18.1 Combo recognition

Commander Spellbook-recognized combos are accepted as known combo records.

Codie may also store user-supplied experimental lines as user context, not as Class 0 combo truth.

## 18.2 Package definitions

Packages must have explicit definitions and provenance.

A package may define:

- required cards;
- optional cards;
- enablers;
- payoffs;
- substitutes;
- outputs;
- constraints.

## 18.3 Mana-sink detection

When evaluating infinite or excess mana, Codie and Jin must check whether:

- a commander is a mana sink;
- the current deck contains a suitable sink;
- the line directly converts to an existing win condition;
- the generated resource is actually usable.

Abstract infinite mana is not automatically valuable.

## 18.4 Tutor-pile best-line analysis

For Gifts Ungiven, Intuition, and similar choice-based piles, Codie may analyze the strongest supported legal line using:

- the exact pile;
- the favorable branch being analyzed;
- resource requirements;
- legality;
- supported card behavior;
- known opponent choices that can interrupt or alter the result.

An opponent-dependent best line must be labeled non-guaranteed. It may not be called deterministic unless every relevant opponent choice produces the stated minimum outcome.

## 18.5 Line legality

Card-connection claims must track which permanent owns an activated ability, what untaps, summoning sickness, timing, costs, and zones.

A superficially similar card is not interchangeable when the rules object performing the action differs.

---

# 19. SIMULATION CONSTITUTION

## 19.1 Role

Simulation is a controlled evidence source under explicit assumptions.

Simulation does not prove real-world tournament performance.

## 19.2 Supported questions

Examples include:

- cast a target by turn N;
- access one of several engines by turn N;
- cast a target while retaining interaction;
- cast a commander while retaining interaction;
- preserve a required permanent for a later line;
- compare candidate card changes;
- inspect successful action traces.

## 19.3 SIM-R boundary

SIM-R may improve state, resources, legal transitions, and card behaviors.

It must not silently become:

- a full Magic engine;
- an opponent AI;
- a combat simulator;
- an LLM-generated execution engine;
- an unbounded Oracle interpreter.

## 19.4 Unsupported cards

Simulation output must disclose:

- unsupported cards;
- partially supported cards;
- ignored text;
- approximated behavior;
- affected result scope.

Unsupported relevant cards enter a review queue.

## 19.5 Trace validity

A trace is evidence only when every relied-upon action is supported and legal under the declared model.

Known invalid or suspect trace patterns must be excluded.

## 19.6 Paradise Mantle correction

A trace using Paradise Mantle for mana is invalid unless it explicitly records:

- paying equip cost;
- the equipped creature;
- legal equip timing;
- the creature tapping for mana;
- summoning-sickness legality;
- the resulting mana.

The equipment itself does not tap for mana.

## 19.7 Springleaf Drum correction

Springleaf Drum remains the object activating its mana ability.

Untapping a creature used to pay the Drum’s cost does not untap the Drum.

It must not be treated as the same loop structure as Paradise Mantle granting a tap ability to the creature.

## 19.8 Target-turn interpretation

Target-turn runs must be treated as separate experiments unless the engine explicitly guarantees cumulative “by turn N” semantics.

Later-turn success rates may decrease under target-specific policy behavior.

The UI must not imply monotonic cumulative probability without proof.

## 19.9 Retained-interaction analysis

Retained interaction may be reported only after reconstruction of:

- final hand;
- battlefield;
- graveyard and exile where relevant;
- commander state;
- available mana;
- pitch-card requirements;
- timing restrictions;
- target restrictions;
- cards discarded to costs.

## 19.10 Reproducibility

Simulation records should preserve:

- deck hash;
- simulator version;
- card-definition version;
- seed or seed policy;
- mulligan policy;
- target condition;
- turn;
- games;
- wins;
- margin of error;
- missing cards;
- warnings;
- elapsed time;
- sample traces.

## 19.11 Provider-derived simulator artifacts

External simulator bundles and traces may be preserved as reference and validation material.

Reverse engineering must stop when sufficient architecture and validation evidence has been captured, unless a new blocker requires further study.

---

# 20. EVIDENCE FUSION

## 20.1 Purpose

Evidence Fusion packages approved references into Unified Evidence Objects.

## 20.2 Inputs

- authority references;
- source observations;
- measured metrics;
- primer context;
- simulator references;
- conflicts;
- caveats;
- source agreement;
- user context references where allowed.

## 20.3 Prohibitions

Evidence Fusion may not:

- query raw providers;
- recalculate analytics;
- execute simulations;
- generate recommendations;
- call LLMs;
- resolve conflicts by invention;
- persist private raw inputs;
- hide caveats;
- write files unless a separate export contract consumes its output.

## 20.4 Required behavior

Unified Evidence must preserve:

- subject identity;
- authority;
- observations;
- metrics;
- sample size;
- coverage;
- context;
- simulation limits;
- conflicts;
- caveats;
- source agreement;
- speculation level where present;
- deterministic serialization.

---

# 21. DECISION INTELLIGENCE

## 21.1 Exclusive reasoning boundary

Persisted recommendations, deck-health conclusions, replacement proposals, and recommendation confidence flow through Decision Intelligence.

No provider, parser, analytics builder, simulator, primer extractor, chat builder, UI component, or export writer may generate an independent recommendation path.

## 21.2 Inputs

Decision Intelligence consumes:

- Unified Evidence;
- versioned analysis profile;
- versioned weight profile;
- approved user context;
- declared objective;
- legality results.

## 21.3 Outputs

- recommendation candidate;
- replacement candidate;
- deck-health finding;
- confidence;
- expected impact;
- evidence summary;
- conflict summary;
- caveats;
- source agreement;
- analysis profile;
- version;
- reproducibility metadata.

## 21.4 Weight profiles

Weights must be configurable, versioned, inspectable, and replayable.

Possible profiles include:

- Competitive Default;
- Tournament Heavy;
- Simulation Heavy;
- Primer Aware;
- Budget Aware;
- Regional Prep;
- User Testing.

## 21.5 Confidence ceiling

Recommendation confidence may not exceed the quality, coverage, and agreement of its evidence.

## 21.6 No universal “correct card” claim

Codie may say:

- “This replacement has stronger evidence under the selected profile.”
- “This card appears in 84% of the selected baseline.”
- “The simulation improved the target rate under this model.”

Codie may not present an evidence-based candidate as universally correct.

---

# 22. RECOMMENDATIONS, REPLACEMENTS, AND DECK HEALTH

## 22.1 Action-first framing

Recommendations should prefer:

```text
Observed concern
  ->
Candidate replacement or test
  ->
Evidence
  ->
Tradeoffs
  ->
Confidence
  ->
Suggested experiment
```

## 22.2 Replacement Knowledge Base

The replacement system should store evidence about:

- functional overlap;
- role coverage;
- color and pitch utility;
- package relationships;
- mana requirements;
- simulator impact;
- matchup coverage;
- opportunity cost;
- user corrections.

## 22.3 Functional overlap

Functional overlap must include secondary uses.

Example categories include:

- blue-card pitch utility;
- free-interaction requirements;
- commander-dependence;
- card type;
- body or permanent presence;
- repeatability;
- package connections.

## 22.4 Deck-health surface

Deck health may summarize:

- role imbalance;
- unsupported packages;
- missing high-frequency cards;
- narrow cards;
- mana-base concerns;
- insufficient conversion outlets;
- low-confidence recommendations;
- unresolved simulator coverage;
- source conflicts.

It must expose underlying evidence.

## 22.5 Chekhov’s-gun analysis

“Every card needs a meaningful scene” may be used as a deck-specific user analysis profile.

It is not a universal rule.

A card can justify itself through:

- engine contribution;
- tutor-pile role;
- resource conversion;
- protection;
- matchup coverage;
- win package;
- flexible overlap;
- long-game value;
- pitch or cost utility.

## 22.6 Change Impact Analysis

Codie should compare deck snapshot A to deck snapshot B, or a current deck to a proposed swap, and report deterministic impact on:

- combos, packages, outputs, and conversion outlets;
- functional tags and relationship measurements;
- frequency and comparison baselines;
- simulator targets and supported-card coverage;
- recommendation evidence and confidence.

Change Impact Analysis explains affected evidence. It does not automatically recommend the change.

---

# 23. CONFIDENCE, AGREEMENT, AND CONFLICTS

## 23.1 Confidence inputs

Confidence may include:

- sample size;
- coverage ratio;
- provider diversity;
- source agreement;
- recency;
- regional relevance;
- model support;
- simulator support;
- unresolved conflicts;
- unsupported-card count;
- user-context specificity.

## 23.2 Source agreement

Agreement labels may include:

- Strong;
- Mixed;
- Weak;
- Insufficient.

Agreement measures concurrence, not authority. Many weak sources cannot outvote Class 0.

## 23.3 Conflict visibility

Every recommendation or Jin answer must preserve material contradictory evidence.

## 23.4 Ratio-aware confidence

Confidence should consider both matching records and available eligible records.

A result based on 20 of 20 eligible decks differs from a result based on 20 of 2,000.

## 23.5 Recency

Recency affects relevance, not truth.

Historical records remain available and may be selected explicitly.

---

# 24. JIN-GITAXIAS STRATEGIST CONSTITUTION

## 24.1 First-class subsystem

Jin-Gitaxias is a governed conversational cEDH theory engine.

Jin is not merely a chat tab and is not a second recommendation engine.

## 24.2 Purpose

Jin supports:

- deck discussion;
- commander comparison;
- package analysis;
- card-connection reasoning;
- archetype blending;
- matchup preparation;
- tournament preparation;
- theory exploration;
- experiment design;
- primer and source comparison;
- simulator interpretation;
- rules-supported interaction explanation;
- lesson delivery.

## 24.3 Data access

Jin may read:

- Authority Layer;
- canonical observations through approved retrieval;
- measured evidence;
- Unified Evidence;
- primer context;
- theory corpus;
- user context;
- deck snapshots;
- simulation reports;
- source conflicts;
- correction ledger.

Jin may never write to:

- canonical tournament evidence;
- measured metrics;
- confidence tables;
- commander staples;
- package statistics;
- persisted recommendations;
- source records.

## 24.4 Permitted writes

Subject to future contracts, Jin may write:

- theory notes;
- experiment queue items;
- user testing notes;
- correction candidates;
- lesson progress;
- deck-specific hypotheses;
- structured conversation summaries.

These outputs must remain labeled as user context or theory.

## 24.5 Answer pipeline

```text
User question
  ->
Intent and scope resolution
  ->
Retrieval plan
  ->
Evidence retrieval
  ->
Theory retrieval
  ->
Primary answer draft
  ->
Authority and legality validation
  ->
Evidence gate
  ->
Contradiction scan
  ->
Optional adversarial auditor
  ->
Final answer packet
```

## 24.6 Required answer packet

A substantive Jin answer should be able to expose:

- direct answer;
- evidence level;
- speculation level;
- source coverage;
- material sources;
- contradictory evidence;
- legality status;
- unsupported claims removed;
- illegal suggestions blocked;
- confidence ceiling;
- suggested experiment;
- deck snapshot used;
- analysis date.

The default UI may collapse these fields, but they must remain available.

## 24.7 Factual claims

Every factual claim must be attributable to:

- Class 0;
- canonical data;
- measured evidence;
- a named source;
- user context;
- explicit inference.

Inference must be labeled as inference.

## 24.8 Strategic claims

Jin may make strategic arguments when:

- evidence and assumptions are shown;
- the claim is not persisted as measured truth;
- uncertainty is visible;
- contradictory evidence is addressed;
- legality is checked;
- the user’s deck context is explicit.

## 24.9 Corrections have priority

User corrections are high-priority signals.

They may override prior Jin reasoning and user-context assumptions.

They may not override official rules or canonical card text without authoritative evidence.

## 24.10 Correction categories

Corrections must be classifiable as:

- factual correction;
- rules correction;
- source-policy correction;
- reasoning failure;
- missing capability;
- simulator-model correction;
- deck-specific principle;
- UI/output preference;
- acceptable low-confidence result;
- terminology correction;
- data-parsing correction.

## 24.11 Deck-specific memory

Jin must distinguish:

- universal format knowledge;
- commander-level knowledge;
- archetype-level knowledge;
- deck-snapshot knowledge;
- user-local-meta knowledge;
- experimental hypothesis.

A correction for one deck must not silently become a universal rule.

## 24.12 Auditor use

An adversarial auditor is recommended for:

- complex combo claims;
- complex tutor-pile best-line claims;
- contentious card comparisons;
- novel rules interactions;
- high-impact recommendations;
- low-evidence strategic claims.

Routine factual retrieval should not require an expensive multi-model council.

## 24.13 Model policy

Every user profile must select a local or cloud-capable model policy. Local execution is the default and remains a required viable path.

A persistent cloud profile is informed opt-in only after privacy disclosure. Cloud availability may improve optional output quality but may not become a required paid dependency.

The system must remain functional without a paid LLM.

---

# 25. THEORY CORPUS AND KNOWLEDGE GRAPH

## 25.1 Purpose

The Theory Corpus stores attributed strategic frameworks that Jin can retrieve and compare.

It does not convert authors into canonical authorities.

## 25.2 Source types

- books;
- articles;
- primers;
- Substack posts;
- videos;
- podcasts;
- transcripts;
- forum threads;
- curated user notes;
- historical Magic theory;
- Commander-specific theory;
- judge and rules training material.

## 25.3 Theory-source treatment

Each source should preserve:

- author;
- title;
- publication;
- date;
- format;
- URL or local reference;
- concepts;
- applicable formats;
- limitations;
- extracted claims;
- direct source citations;
- user notes.

A Reddit RSS item enters only a Theory Corpus candidate queue. The linked work, author, attribution, relevance, storage rights, and transferability must be reviewed separately before promotion. A Reddit post remains community context unless it independently qualifies under the Theory Corpus source policy.

## 25.4 Transferability

Vintage, Legacy, constructed, and casual Commander theory may be included when transferable concepts are separated from format-specific claims.

Examples of transferable concepts:

- resource advantage;
- role assignment;
- intermediate and ultimate objectives;
- engine inputs and outputs;
- sequencing;
- flexibility;
- redundancy;
- package budgeting;
- conversion of drawbacks into advantages.

## 25.5 Framework examples

The corpus may include frameworks such as:

- Stephen Menendian’s strategic concepts from *Understanding Gush*;
- 8x8 Theory as a package and slot-budgeting heuristic;
- source-attributed cEDH articles and primers;
- user-developed Chekhov’s-gun deck analysis;
- matchup and table-politics frameworks;
- fallacy identification;
- judge-style rules reasoning.

Literal heuristics must not be promoted beyond their source context.

## 25.6 Knowledge graph

Theory nodes may represent:

- concepts;
- claims;
- authors;
- works;
- examples;
- counterexamples;
- decks;
- cards;
- packages;
- rules;
- lessons;
- corrections.

Edges must preserve the relationship type and source.

## 25.7 On-command deep analysis

Theory-corpus analysis should run on command for a selected deck or question rather than requiring nightly execution.

It may be included in longer deck-research workflows.

## 25.8 Educational curriculum

Core V2 education supports:

- cEDH fundamentals;
- resource and tempo theory;
- table politics;
- threat assessment;
- priority and stack mechanics;
- judge-program-style rules;
- common logical fallacies;
- how to identify and use rhetorical pressure;
- why strategic tools such as wheels are strong in some decks and poor in others;
- package and conversion analysis.

Lessons must distinguish rules facts, theory, examples, and opinion.

---

# 26. USER CORRECTION LEDGER

## 26.1 Purpose

The correction ledger turns user feedback into structured project-learning data.

## 26.2 Required fields

- correction ID;
- date;
- deck or global scope;
- original claim;
- corrected claim;
- category;
- supporting reason;
- source or user authority;
- affected subsystem;
- reusable rule;
- exceptions;
- validation status.

Each correction must also preserve its lifecycle state, authority scope, effective date where applicable, supporting source, superseded correction ID where applicable, and revalidation triggers.

## 26.3 Application rules

A correction should be applied at the narrowest valid scope.

Examples:

- Paradise Mantle trace legality: simulator-wide.
- Springleaf Drum and Valley Floodcaller: interaction-wide.
- “No good mana sink” in a specific WrongSi list: deck-snapshot scope.
- Chekhov’s-gun analysis: selected deck profile.
- Sideboard-only copies excluded from mainboard frequency: parser and analytics-wide.

## 26.4 Review

Corrections that imply architecture, schema, source-policy, or constitutional changes require explicit governance review.

Approved lifecycle states are:

```text
proposed
verified
active
superseded
rejected
revalidation_required
```

Corrections apply at the narrowest valid scope. User corrections may override prior Jin reasoning and user-context assumptions, but may not override current official rules or canonical card truth without authoritative evidence.

---

# 27. RULES, JUDGE SUPPORT, AND REFERENCE ENGINES

## 27.1 Rules Layer

The Rules Layer is independent of recommendation scoring.

It supports:

- legality validation;
- simulator action validation;
- interaction explanation;
- Jin answers;
- lesson content;
- regression tests.

## 27.2 Authority

Official rules and Oracle text remain authoritative.

Community rules tools are references, not authority.

## 27.3 MTG Layer Inspector

MTG Layer Inspector is retained as a reference implementation for:

- continuous effects;
- layer ordering;
- dependency handling;
- timestamps;
- human-readable rules explanations;
- regression-case design.

It is not a runtime dependency or data-injection source without later approval.

## 27.4 Full-engine boundary

Codie may borrow test cases and architecture ideas from larger engines.

Codie should not absorb a full engine merely because one difficult interaction exists.

## 27.5 Judge-training mode

Core V2 lesson and explanation systems may use judge-style issue spotting:

1. identify objects and zones;
2. identify rules and effects;
3. identify timestamps and dependencies;
4. identify costs and targets;
5. apply effects;
6. explain the result;
7. cite authority.

---

# 28. RESEARCH ACQUISITION POLICY

## 28.1 Research states

Every researched tool or source should be classified as:

- approved provider;
- proposed provider;
- context source;
- theory source;
- validation reference;
- UI reference;
- implementation reference;
- rejected;
- deferred;
- unavailable.

## 28.2 Acquisition testing

Before approving a provider, test:

- access stability;
- robots and terms;
- API or page structure;
- required authentication;
- rate limits;
- payload completeness;
- historical coverage;
- overlap with existing sources;
- deduplication needs;
- licensing;
- failure behavior.

## 28.3 No endless reverse engineering

Research stops when sufficient evidence exists to implement, reject, or defer.

Additional reverse engineering requires a specific unresolved blocker.

## 28.4 Research source list additions

V2 recognizes the following recent candidates:

- cEDH.jp: proposed regional discovery and injection;
- MTG Layer Inspector: rules reference implementation;
- Lotus Refinery: research candidate for attributed strategy and primer context;
- Warlord1986pl metagame tool concept: tournament exposure analytics reference;
- Delvefall: semantic-search reference;
- Penpot: UI prototyping candidate;
- Pake: packaging or acquisition research candidate, not approved by default.
- Reddit RSS Community Signal Monitor: approved post-checkpoint discovery candidate for Jin and governed research queues, never a tournament injection source.

## 28.5 Source health and freshness

Every active provider must expose:

- last successful retrieval;
- newest observed source-data date;
- parser version;
- source coverage and deduplication status;
- acquisition state and recent failures;
- licensing or storage restrictions;
- downstream analyses affected by stale or unavailable data.

Stale or failing sources must reduce confidence or create visible caveats rather than fail silently.

---

# 29. UI AND OUTPUT PHILOSOPHY

## 29.1 Action first

The primary interface should answer:

```text
What deserves attention?
Why?
How confident is Codie?
What evidence can I inspect?
```

## 29.2 Suppress trivia

Do not fill the dashboard with:

- obvious staples already present;
- redundant confirmation panels;
- decorative metrics with no decision value;
- duplicate confidence widgets;
- hidden methodology.

## 29.3 Decision Evidence Panel

Recommendation, confidence, source agreement, simulation, replacement logic, evidence weights, conflicts, and caveats should converge in one expandable explanation surface.

## 29.4 Two-screen workflow

Codie should continue to support:

- deck editor on one screen;
- Codie analysis and Jin on another.

## 29.5 Chat visibility

The Jin chat interface is part of the primary UI, not an unrelated add-on.

Chat answers should link to the exact evidence, report, deck snapshot, simulation, or theory source used.

## 29.6 Accessibility

Reports and controls should use:

- readable typography;
- meaningful labels;
- keyboard access;
- clear error messages;
- non-color-only distinctions;
- mobile-readable report layouts.

---

# 30. INTEGRATIONS

## 30.1 Stream Deck

Long-term Codie UI design should support Stream Deck integration for common actions and navigation.

Potential actions:

- analyze current deck;
- open Jin;
- run selected simulation;
- compare snapshot;
- export report;
- open frequency pool;
- open Tag Graph Lab;
- switch analysis profile.

Stream Deck integration must not bypass safety or validation boundaries.

## 30.2 Discord

Discord may support:

- optional report delivery;
- shared shopping-style or team workflows where separately approved;
- local league inputs;
- notifications;
- links to local reports.

Tokens remain local and optional.

## 30.3 Mobile

Mobile report delivery is deferred until separately contracted.

When implemented, mobile access is read-only by default and the PC remains the execution host.

## 30.4 MCP and plugins

External tool protocols may be used only when:

- permissions are explicit;
- data boundaries are documented;
- local-first operation remains possible;
- failure does not corrupt canonical data;
- no paid dependency is introduced without approval.

---

# 31. EXPORTS AND KNOWLEDGE VAULT

## 31.1 Supported formats

- Markdown;
- CSV;
- JSON;
- Obsidian Markdown;
- static HTML;
- PDF where approved.

## 31.2 Export rules

Exports must preserve:

- source attribution;
- generated time;
- analysis version;
- deck snapshot;
- filters;
- confidence;
- caveats;
- methodology.

## 31.3 Obsidian

The Knowledge Vault may contain:

- commander staples;
- deck reports;
- tournament meta;
- primers;
- combos and packages;
- simulations;
- commander intelligence;
- card intelligence;
- theory notes;
- lessons;
- correction records;
- experiment queue.

## 31.4 Private content

Private deck text, full traces, private notes, and tokens are excluded unless explicitly selected.

## 31.5 Storage economy

Long full traces should not be retained indefinitely when summaries, winning traces, failure categories, and reproducibility metadata are sufficient.

---

# 32. PRIVACY, SECURITY, AND LOCAL-FIRST OPERATION

## 32.1 Local data

By default, the following remain local:

- private decks;
- user notes;
- correction ledger;
- simulator traces;
- theory annotations;
- tokens;
- model prompts containing private data;
- local meta notes.

## 32.2 Cloud consent

Cloud processing requires explicit per-profile opt-in and disclosure of what data leaves the machine.

Cloud-capable operations must declare:

- the data classes transmitted;
- whether private deck text, notes, corrections, or theory excerpts are included;
- redactions applied;
- the receiving provider and model;
- whether local execution is available.

A cloud profile is not blanket consent for every local data class. Private deck data remains local unless the selected profile explicitly authorizes that class.

## 32.3 Secrets

Secrets must use environment variables or local protected configuration.

They may not be committed to source control or exported in reports.

## 32.4 Read/write separation

Read-only report access must not expose database mutation endpoints.

## 32.5 Defensive parsing

External payloads are untrusted.

Parsers must validate type, size, encoding, required fields, URLs, and unexpected content.

---

# 33. STORAGE, PERFORMANCE, AND VERSIONING

## 33.1 SQLite

SQLite remains the default local database.

## 33.2 Repository ownership

Every persisted object has one approved repository owner.

## 33.3 Migrations

Schema changes require:

- architecture contract;
- migration;
- rollback or recovery plan;
- index review;
- repository updates;
- schema documentation;
- tests.

The earlier absolute schema-freeze concept is replaced by governed migration discipline.

## 33.4 Versioned analyses

Every analysis run and substantive Jin answer must preserve an analysis manifest containing:

- deck snapshot ID and deck hash;
- source snapshot IDs and retrieval windows;
- analytics version;
- weight profile version;
- simulator version;
- simulator seed where applicable;
- ontology version;
- Commander Spellbook snapshot/version;
- Correction Ledger version;
- Theory Corpus version where used;
- Jin model and prompt-policy version where used;
- filters and analysis profile;
- generated timestamp.

The manifest governs reproducibility, cache identity, and incremental invalidation.

## 33.5 Cache policy

Caching is permitted when:

- cache identity is deterministic;
- stale behavior is documented;
- source changes are detectable;
- invalidation is safe;
- prior results remain reproducible.

---

# 34. TESTING AND VALIDATION

## 34.1 Required test families

- unit;
- integration;
- parser fixtures;
- malformed input;
- missing fields;
- negative path;
- deterministic serialization;
- privacy boundary;
- import boundary;
- schema migration;
- reproducibility;
- adversarial strategic-language checks;
- legality checks;
- regression corrections.

## 34.2 Provider fixtures

Each provider should have:

- successful fixture;
- malformed fixture;
- missing optional field fixture;
- missing required field fixture;
- duplicate event fixture;
- source-lineage fixture.

## 34.3 Analytics tests

Metrics must have hand-verifiable fixtures and edge cases.

## 34.4 Jin tests

Jin validation should test:

- unsupported claim removal;
- citations;
- legality;
- contradiction visibility;
- deck-scope isolation;
- correction application;
- confidence ceiling;
- theory-versus-evidence labeling;
- refusal to mutate canonical data.

Jin releases must also run a fixed regression corpus covering citation accuracy, legality blocking, evidence/theory/community separation, correction-scope isolation, contradiction disclosure, local-only execution, cloud redaction, and strategic-claim labeling. The tested model, prompt-policy version, corpus version, results, and artifact identity must be recorded.

## 34.5 Simulator tests

Simulator tests should include known legal and illegal traces, especially user-corrected interactions.

## 34.6 Release evidence

A release or phase acceptance must record the tested commit, commands, results, and artifact identity.

---

# 35. RELEASE AND PHASE GATING

## 35.1 Current-state separation

The constitution defines permanent behavior.

The roadmap defines sequence.

The validation index defines accepted state.

The next-phase contract defines immediate authorization.

## 35.2 No retroactive authority

A later roadmap idea does not retroactively authorize earlier code.

## 35.3 Deferred features

Deferred features may be researched and logged but not implemented until contracted.

## 35.4 Experimental track

Experiments must be isolated from canonical production behavior.

A proof of concept must not become production code merely because it produces plausible output.

## 35.5 V2 transition sequencing

V2 adoption does not invalidate completed V1 phases or accepted contracts. The compatibility statement controls any identified conflict.

The active Phase 37 track must close through its established pull-request and validation gates. Subsequent roadmap work must be checked against V2 before implementation begins.

---

# 36. EXPERIMENTAL AND DEFERRED SYSTEMS

The following may remain deferred until separately contracted:

- mobile report delivery, QR delivery, Discord delivery, and LocalSend delivery;
- Stream Deck controls;
- Swiss and pairing-aware tournament exposure modeling;
- automated relationship package discovery, graph embeddings, causal inference, replacement prediction, and a dedicated graph database;
- full Deep Deck Analysis job orchestration;
- a full multiplayer Magic rules engine and broad arbitrary-card behavior coverage;
- optional MCP and external-plugin integrations;
- reference implementation adapters.
- Reddit RSS Community Signal Monitor implementation and any notification delivery attached to it.

The standalone Stream Deck Game Tracker remains outside Codie. Voice input and output remain removed from active scope.

Theory Corpus, its attributed knowledge graph, the minimal Correction Ledger, judge-style education, the labeled independent-seat Tournament Exposure Analyzer, the core Relationship Intelligence metric family, and the required local model path are core V2 capabilities and are not deferred by this section.

Each remains subject to zero-cost, privacy, licensing, and boundary review.

---

# 37. CORE V2 TOURNAMENT EXPOSURE REQUIREMENT

## Tournament Exposure Intelligence

Implement through separately accepted core V2 contracts:

**Module:** Tournament Exposure Analyzer

**Required scopes:**

- global;
- region;
- country;
- store;
- organizer;
- tournament size;
- date range;
- commander;
- partner pair;
- archetype;
- card;
- package;
- functional tag.

**Required outputs:**

- estimated encounter probability;
- event-wide exposure;
- local versus global delta;
- regional versus global delta;
- source population;
- sample size;
- confidence;
- assumptions;
- preparation brief.

**Boundary:** Evidence only until consumed by Decision Intelligence.

---

# 38. GLOSSARY

**Authority:** A source permitted to define rules, card identity, legality, or recognized combo data within its scope.

**Canonical record:** A normalized, deduplicated representation used by analytics.

**Context:** Attributed human explanation, theory, primer material, or community discussion.

**Decision Intelligence:** Exclusive subsystem for persisted recommendation conclusions.

**Evidence Fusion:** Deterministic assembly of evidence references into a common packet.

**Injection source:** Provider that contributes observations to the source layer.

**Jin-Gitaxias:** Grounded conversational theory subsystem.

**Measured evidence:** Reproducible analytics calculated from canonical inputs.

**Source agreement:** Degree to which eligible sources support compatible observations.

**Speculation:** Reasoning not directly established by evidence and labeled accordingly.

**Theory corpus:** Attributed collection of strategic frameworks and educational material.

**Unified Evidence:** Standard downstream evidence packet.

**User context:** Personal preferences, local observations, corrections, and testing goals.

---

# APPENDIX A: SOURCE CLASSIFICATION SUMMARY

| Source | Role | Analytics eligibility | Jin eligibility |
|---|---|---:|---:|
| Official rules and announcements | Class 0A authority | N/A | Yes |
| Scryfall | Class 0A card authority | Identity support | Yes |
| Commander Spellbook | Class 0B combo authority | Combo-derived metrics | Yes |
| Scryfall Tagger | Class 0C functional ontology | Tag metrics | Yes |
| TopDeck | Injection source | After canonicalization | Yes |
| EDHTop16 | Injection source | After canonicalization | Yes |
| MTGTop8 | Historical injection | After canonicalization | Yes |
| MTGDecks | Discovery and enrichment | After dedupe | Yes |
| Hareruya | Japanese regional injection | After canonicalization | Yes |
| cEDH.jp | Proposed regional discovery/injection | After validation and dedupe | Yes |
| Moxfield | User deck and primer context | Tournament only when linked | Yes |
| cEDH DDB | Primer/archetype context | No population analytics | Yes |
| Lotus Refinery | Research candidate for strategy context | No | Only after admission |
| Reddit and community discussion | Community context | No | Yes, attributed |
| cEDHStats | UI/methodology cross-check | No independent counting | Yes, as reference |
| MTG Layer Inspector | Rules reference implementation | No | Yes, as reference |
| Delvefall | Semantic-search reference | No | Reference only |

---

# APPENDIX B: JIN ANSWER SAFETY FIELDS

```text
evidence_level
speculation_level
source_coverage
material_sources
contradictory_evidence
legality_status
unsupported_claims_removed
illegal_suggestions_blocked
confidence_ceiling_applied
deck_snapshot_id
analysis_profile
suggested_experiment
```

---

# APPENDIX C: RATIFIED CONSTITUTIONAL DECISIONS

1. Jin becomes a first-class subsystem.
2. Controlled strategic reasoning becomes permitted inside Jin.
3. Scryfall Tagger receives Class 0C scoped authority.
4. cEDH.jp becomes an audit-gated proposed injection source.
5. Lotus Refinery remains a research candidate until admitted by source review.
6. Theory Corpus and educational curriculum become constitutional systems.
7. User Correction Ledger becomes a governed system.
8. A labeled independent-seat Tournament Exposure Analyzer becomes a core V2 capability; Swiss modeling is deferred.
9. Stream Deck integration returns as a long-term UI goal.
10. Absolute schema freeze is replaced by governed migrations.
11. Full-primer-storage restrictions are separated from local theory notes and attributed extraction.
12. Simulation corrections become constitutional regression rules.
13. Regional, store, organizer, and event-size analysis become core capabilities.
14. Relationship Intelligence and measured co-dependence become core evidence capabilities; co-dependence remains metric-only.
15. Tutor piles use best-line analysis and label opponent-dependent lines non-guaranteed.
16. Community retrieval has no fixed recency window.
17. Model selection is per profile, with local execution as the default and required fallback.
18. A minimal structured Correction Ledger is core V2.
19. Theory Corpus and judge-style education are core V2.
20. V1 remains available as historical reference; its capabilities carry forward except that the standalone Natural Language Query Helper is folded into Jin and mobile report delivery is deferred.

---

# APPENDIX D: ADOPTION NOTICE

The user approved V2 adoption on 2026-07-20 after review of the V1/V2 comparison, the comprehensive Codie/Jin handoff, the live repository, and the explicit decision record.

V2 becomes the official current constitution when the adoption pull request is accepted and merged. V1 remains unchanged at `docs/CODIE_V1_CONSTITUTION.md` for historical reference.
