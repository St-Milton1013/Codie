



# Codie V2 Knowledge Vault and Obsidian Export Contract

## 1. Contract status

**Document type:** Architecture and implementation contract
**Implementation authorization:** Schema, package planning, validation fixtures, and interface design only
**Explicitly excluded:** File writers, filesystem mutation, ZIP creation, Obsidian plugin development, synchronization services, and database migrations
**Constitutional status:** Derived from the Codie V2 comparison draft, which remains non-authoritative until ratified. Nothing here silently promotes that draft into governing authority. The draft nevertheless defines the intended Knowledge Vault categories, local-first privacy posture, versioned analyses, provenance requirements, and export boundaries. fileciteturn0file0

The Theory Corpus compilation supplies the initial node taxonomy, proposed Obsidian structure, shared YAML fields, disagreement handling, source attribution rules, format-translation records, lesson structure, and separation between theory, evidence, inference, and personal conclusions. fileciteturn0file1

---

# 2. Purpose

The Knowledge Vault is Codie V2’s durable, inspectable, local-first knowledge layer.

It converts selected Codie records into a portable collection of:

- UTF-8 Markdown notes;
- YAML front matter;
- JSON manifests;
- optional CSV and JSON evidence tables;
- relative links and Obsidian-compatible wikilinks;
- immutable analysis snapshots;
- mutable index notes;
- provenance records;
- privacy and export-scope declarations.

The vault must answer:

1. What object does this note describe?
2. Which Codie record and version produced it?
3. Which sources support it?
4. Which parts are measured evidence, attributed theory, user context, or inference?
5. What changed since the previous export?
6. Was anything omitted for privacy, licensing, or unsupported-data reasons?
7. Can a prior answer or analysis be reconstructed from the exported material?

The vault is not a second canonical database. Humans already invented enough opportunities for two copies of truth to disagree.

---

# 3. Governing principles

## 3.1 Exported, not canonical

The vault is a presentation and research artifact.

It may contain copies and summaries of canonical data, but it may not become the authoritative source for:

- Oracle text;
- legalities;
- tournament records;
- measured metrics;
- recommendation confidence;
- source records;
- simulator results;
- correction status.

Edits made inside Obsidian do not mutate Codie unless a separately governed import contract later exists.

## 3.2 Stable identity before readable naming

Every exported entity receives a stable `node_id`.

Titles and slugs may change. The stable ID may not.

## 3.3 Immutable history, mutable indexes

Historical reports, deck snapshots, simulation runs, lesson revisions, and correction revisions are immutable export records.

Mutable index notes may point to the newest immutable record.

## 3.4 No silent overwrite

Generated files must never overwrite user-authored changes without conflict detection.

## 3.5 Provenance survives summarization

A condensed note must still identify the records, source observations, calculations, versions, and exclusions behind it.

## 3.6 Privacy is explicit

Every export uses a declared privacy profile. “It was probably safe” is not a privacy model.

## 3.7 Plugin independence

The base vault must function in plain Obsidian without Dataview, Templater, Canvas, or community plugins.

Plugin-specific enhancements may be exported only as optional supplementary material.

---

# 4. Export modes

## 4.1 Full vault export

Produces a complete selected vault state.

Required root artifacts:

```text
CODIE_VAULT/
├── README.md
├── VAULT_MANIFEST.json
├── EXPORT_REPORT.md
├── PROVENANCE.jsonl
├── LINK_INDEX.json
├── 00 Maps/
├── 01 Commanders/
├── 02 Decks/
├── 03 Tournament Meta/
├── 04 Primers/
├── 05 Combos and Packages/
├── 06 Simulations/
├── 07 Theory/
├── 08 Lessons/
├── 09 Corrections/
├── 10 Experiments/
├── 90 Attachments/
├── 98 Conflicts/
└── 99 Archive/
```

## 4.2 Package export

Exports one or more selected package types without requiring the complete vault.

Examples:

```text
codie-export-commander-staples-20260723/
codie-export-deck-report-rog-ish-20260723/
codie-export-theory-tempo-pilot-20260723/
```

Every package remains self-describing and contains its own manifest.

## 4.3 Incremental export

Contains only:

- added files;
- changed files;
- supersession records;
- tombstones;
- conflict records;
- an incremental manifest;
- the base export ID required for application.

An incremental package must never pretend to be a complete standalone vault.

## 4.4 Shareable export

Applies a restrictive privacy and licensing profile.

It excludes private decks, user notes, raw traces, secret paths, private corrections, private local-meta material, and copyrighted source bodies unless redistribution rights are recorded.

## 4.5 Local private export

May contain explicitly selected private material.

It remains local-first and must be marked:

```yaml
privacy_tier: private-local
shareable: false
```

---

# 5. Root folder contract

```text
CODIE_VAULT/
│
├── README.md
├── VAULT_MANIFEST.json
├── EXPORT_REPORT.md
├── PROVENANCE.jsonl
├── LINK_INDEX.json
│
├── 00 Maps/
│   ├── Home.md
│   ├── Commander Index.md
│   ├── Deck Index.md
│   ├── Tournament Meta Index.md
│   ├── Primer Index.md
│   ├── Combo and Package Index.md
│   ├── Simulation Index.md
│   ├── Theory Index.md
│   ├── Lesson Index.md
│   ├── Correction Index.md
│   └── Experiment Queue.md
│
├── 01 Commanders/
│   └── <commander-signature-id>/
│       ├── Commander Overview.md
│       ├── Staples/
│       ├── Meta/
│       ├── Decks/
│       └── Intelligence/
│
├── 02 Decks/
│   └── <deck-id>/
│       ├── Deck Overview.md
│       ├── Snapshots/
│       ├── Reports/
│       ├── Changes/
│       ├── Experiments/
│       └── User Notes/
│
├── 03 Tournament Meta/
│   ├── Global/
│   ├── Regions/
│   ├── Stores/
│   ├── Organizers/
│   └── Events/
│
├── 04 Primers/
│   ├── Sources/
│   ├── Claims/
│   ├── Archetypes/
│   └── Comparisons/
│
├── 05 Combos and Packages/
│   ├── Combos/
│   ├── Packages/
│   ├── Lines/
│   └── Tutor Piles/
│
├── 06 Simulations/
│   ├── Runs/
│   ├── Comparisons/
│   ├── Targets/
│   └── Validation/
│
├── 07 Theory/
│   ├── 00 Maps/
│   ├── 01 Topics/
│   ├── 02 Theorists/
│   ├── 03 Claims/
│   ├── 04 Sources/
│   │   ├── Books/
│   │   ├── Articles/
│   │   ├── Forums/
│   │   ├── Videos/
│   │   └── Podcasts/
│   ├── 05 Disagreements/
│   ├── 06 Format Translations/
│   ├── 07 Deck Applications/
│   └── 10 Personal Conclusions/
│
├── 08 Lessons/
│   ├── Curricula/
│   ├── Lessons/
│   ├── Assessments/
│   └── Progress/
│
├── 09 Corrections/
│   ├── Global/
│   ├── Commander/
│   ├── Deck/
│   ├── Simulator/
│   ├── Parser/
│   └── Superseded/
│
├── 10 Experiments/
│   ├── Queue/
│   ├── Active/
│   ├── Completed/
│   ├── Cancelled/
│   └── Results/
│
├── 90 Attachments/
│   ├── Images/
│   ├── Tables/
│   └── Licensed Private/
│
├── 98 Conflicts/
└── 99 Archive/
    ├── Superseded/
    └── Tombstones/
```

The `07 Theory` subtree preserves the corpus compilation’s planned separation between topics, theorists, claims, sources, disagreements, translations, applications, lessons, and personal conclusions. fileciteturn0file1

---

# 6. Stable identity and filenames

## 6.1 Global node ID

Format:

```text
codie:<node-type>:<stable-identifier>
```

Examples:

```text
codie:commander-signature:rograkh-ishai
codie:deck:8f28c9b0-7d26-4a7e-b5a8-58f112d39289
codie:deck-snapshot:8f28c9b0-20260722-a41e283d
codie:simulation-run:sim-20260722-000184
codie:theory-claim:engines-require-conversion
codie:correction:corr-000043
codie:experiment:exp-000128
```

Stable identifiers must come from Codie-owned IDs, canonical source IDs, Oracle IDs, or deterministic compound identities.

Display names must not be used as the sole identifier.

## 6.2 Filename pattern

```text
<node-type>-<stable-short-id>-<readable-slug>.md
```

Examples:

```text
commander-rograkh-ishai-overview.md
staples-rograkh-ishai-2026h1.md
deck-8f28c9b0-overview.md
snapshot-8f28c9b0-20260722-a41e283d.md
simulation-sim-20260722-000184-rhystic-turn-two.md
theory-claim-engines-require-conversion.md
correction-corr-000043-paradise-mantle-trace-legality.md
experiment-exp-000128-ledger-shredder-test.md
```

## 6.3 Filename restrictions

Filenames must:

- use ASCII lowercase slugs;
- preserve stable IDs;
- use hyphens instead of spaces;
- avoid Windows-reserved characters;
- avoid trailing periods or spaces;
- remain under a configured path-length ceiling;
- use deterministic collision suffixes;
- never depend on locale-specific sorting;
- preserve Unicode names in front matter and note headings rather than filenames.

## 6.4 Immutable file naming

Immutable notes must include either:

- date plus content hash;
- run ID;
- revision ID;
- snapshot ID.

Mutable overview notes may omit a version suffix because their identity is stable and their contents point to versioned records.

---

# 7. Link contract

## 7.1 Obsidian links

Generated notes use wikilinks:

```markdown
[[deck-8f28c9b0-overview|Rograkh / Ishai]]
[[simulation-sim-20260722-000184-rhystic-turn-two|Rhystic Study by turn two]]
```

Links must target stable filenames, not display-title guesses.

## 7.2 Link registry

`LINK_INDEX.json` maps:

```json
{
  "codie:deck:8f28c9b0-7d26-4a7e-b5a8-58f112d39289": {
    "path": "02 Decks/8f28c9b0/deck-8f28c9b0-overview.md",
    "title": "Rograkh / Ishai",
    "aliases": ["Rog Ish", "Benedikta Harman / Joshua Rosfield"]
  }
}
```

## 7.3 Alias behavior

Aliases appear in YAML:

```yaml
aliases:
  - Rograkh / Ishai
  - Rog Ish
  - Benedikta Harman / Joshua Rosfield
```

Aliases aid search. They do not establish identity.

## 7.4 Source links

External sources use normal Markdown links in note bodies and normalized source records in provenance data.

Source URLs must be preserved exactly unless removed by a privacy profile.

## 7.5 Broken-link policy

An export fails validation when a generated wikilink targets no exported or explicitly external node.

Permitted unresolved links must be marked:

```yaml
link_status: intentionally-unresolved
```

and listed in the manifest.

---

# 8. Common YAML front matter

Every Markdown node must contain:

```yaml
---
node_id: "codie:deck:8f28c9b0-7d26-4a7e-b5a8-58f112d39289"
node_type: "deck"
title: "Rograkh / Ishai"
aliases:
  - "Rog Ish"
schema_version: "1.0.0"
record_version: 4
status: "active"
created_at: "2026-07-16T14:12:00-05:00"
updated_at: "2026-07-23T00:30:00-05:00"
generated_at: "2026-07-23T00:31:14-05:00"
codie_managed: true
immutable: false
privacy_tier: "private-local"
shareable: false
source_record_ids: []
provenance_ids:
  - "prov-000812"
analysis_versions:
  analytics: "analytics-2.1.0"
  ontology: "tagger-map-2026-07-18"
  decision_profile: "competitive-default-1.3"
content_hash: "sha256:..."
supersedes: null
superseded_by: null
related_nodes: []
tags:
  - "codie/deck"
  - "format/cedh"
---
```

## 8.1 Required shared fields

- `node_id`
- `node_type`
- `title`
- `schema_version`
- `record_version`
- `status`
- `created_at`
- `updated_at`
- `generated_at`
- `codie_managed`
- `immutable`
- `privacy_tier`
- `shareable`
- `provenance_ids`
- `content_hash`

## 8.2 Optional shared fields

- `aliases`
- `source_record_ids`
- `analysis_versions`
- `supersedes`
- `superseded_by`
- `related_nodes`
- `formats`
- `commanders`
- `deck_snapshot_id`
- `confidence`
- `coverage`
- `conflicts`
- `caveats`
- `tags`
- `user_scope`
- `rights_status`
- `export_omissions`

## 8.3 Evidence classification

Notes containing analysis must distinguish:

```yaml
evidence_classes:
  authority: true
  observations: true
  measured: true
  theory: true
  user_context: false
  inference: true
```

Theory nodes additionally use the corpus classifications:

```yaml
claim_labels:
  - direct-theory
  - format-translation
  - empirical-support
```

The corpus explicitly requires direct theory, demonstrated application, later synthesis, Jin inference, format translation, empirical support, empirical conflict, and unresolved status to remain distinct. fileciteturn0file1

---

# 9. Package specifications

## 9.1 Commander staples package

### Purpose

Export exact-commander or partner-pair frequency evidence without turning absence into an automatic recommendation.

### Folder

```text
01 Commanders/<signature-id>/Staples/
```

### Files

```text
staples-<signature-id>-current.md
staples-<signature-id>-<window>-<hash8>.md
staples-<signature-id>-<window>.csv
staples-<signature-id>-<window>.json
```

### Required front matter

```yaml
node_type: commander-staples
commander_signature_id: "rograkh-ishai"
commander_match_mode: exact-pair
population_type: canonical-tournament-decks
date_start: "2026-01-23"
date_end: "2026-07-23"
placement_scope: top-16
zone_scope: mainboard
sample_size: 84
available_decks: 84
coverage_ratio: 1.0
metric_version: "commander-staples-1.2"
```

### Required body sections

1. Scope
2. Population
3. Ranked staples
4. Placement-weighted frequency
5. Missing-card evidence flags
6. Sample size and coverage
7. Source lineage
8. Caveats
9. Related deck reports
10. Previous versions

### Restrictions

- Commander cards are excluded from mainboard frequencies.
- Sideboard and auxiliary objects remain separate.
- Partial partner matching must be visibly labeled.
- Missing-card flags are evidence, not recommendations.

---

## 9.2 Deck report package

### Folder

```text
02 Decks/<deck-id>/
```

### Files

```text
deck-<deck-id>-overview.md
Snapshots/snapshot-<deck-id>-<date>-<hash8>.md
Reports/report-<deck-id>-<analysis-date>-<hash8>.md
Changes/change-<deck-id>-<from-hash>-<to-hash>.md
```

Optional evidence tables:

```text
Reports/report-<...>-cards.csv
Reports/report-<...>-evidence.json
```

### Deck overview

Mutable index containing:

- deck identity;
- commander signature;
- source URL;
- current snapshot;
- snapshot history;
- locked cards;
- ignored cards;
- deck-specific principles;
- latest reports;
- active experiments;
- applied corrections;
- privacy status.

### Snapshot note

Immutable and must contain:

- normalized commanders;
- normalized mainboard;
- zones;
- unsupported names;
- source modified time;
- import time;
- deck hash;
- parser version;
- canonicalization version;
- support status.

### Report note

Immutable and must contain:

1. Executive findings
2. Deck identity and snapshot used
3. Measured evidence
4. Decision Intelligence conclusions, when present
5. Confidence and source agreement
6. Conflicts and caveats
7. Package and combo state
8. Mana-sink and conversion analysis
9. Simulator references
10. Theory lenses used
11. Suggested experiments
12. Corrections applied
13. Reproducibility metadata

### Privacy default

Private decklists are excluded from shareable exports unless explicitly selected.

A redacted report may retain aggregate findings while omitting the full list.

---

## 9.3 Tournament meta package

### Folder

```text
03 Tournament Meta/<scope>/
```

### Filename examples

```text
meta-global-2026h1.md
meta-region-japan-2026q2.md
meta-store-example-store-20260401-20260701.md
event-evt-000183-codie-open-20260718.md
```

### Required fields

```yaml
node_type: tournament-meta
scope_type: region
scope_id: japan
date_start: "2026-04-01"
date_end: "2026-06-30"
event_size_filter: all
canonical_event_count: 31
deck_count: 614
coverage_ratio: 0.92
deduplication_version: "event-canonicalization-2.0"
```

### Required body

- scope and filters;
- commander and partner-pair shares;
- archetype shares;
- card, package, and tag observations;
- winner and top-cut comparisons;
- regional or local deltas;
- sample and coverage;
- source conflicts;
- event lineage;
- methodology;
- limitations.

### Conflict rule

Conflicting player counts, dates, placements, pilots, or decklists remain visible. The export may show a resolved canonical value only alongside the conflict record and resolution rationale.

---

## 9.4 Primer package

### Folder

```text
04 Primers/Sources/
```

### Files

```text
primer-<source-id>-<slug>.md
primer-claim-<claim-id>-<slug>.md
primer-comparison-<commander-signature>-<date>.md
```

### Required primer metadata

```yaml
node_type: primer-source
author: "..."
publication: "..."
published_at: "..."
source_url: "..."
commander_signature_ids: []
source_type: "moxfield-primer"
rights_status: "linked-summary-only"
retrieval_status: "complete"
claim_extraction_version: "1.0"
```

### Permitted content

- source metadata;
- section map;
- concise summary;
- attributed claims;
- cited excerpts within lawful limits;
- deck and commander references;
- disagreements with evidence;
- stale or unsupported claims;
- retrieval status.

### Prohibited default content

- full mirrored primer text;
- full copyrighted articles;
- paid material;
- private author content;
- unattributed paraphrases treated as Codie truth.

Primer context may explain evidence but may not overwrite measured tournament results.

---

## 9.5 Combo and package package

### Folder

```text
05 Combos and Packages/
```

### Combo filename

```text
combo-spellbook-<combo-id>-<slug>.md
```

### Experimental line filename

```text
line-user-<line-id>-<slug>.md
```

### Required combo fields

```yaml
node_type: combo
authority_class: class-0b
spellbook_combo_id: "..."
pieces: []
requirements: []
outputs: []
commander_requirements: []
source_url: "..."
present_in_deck_snapshots: []
```

### Required body

- recognized pieces;
- prerequisites;
- outputs;
- variants;
- deck presence;
- actual conversion outlets;
- commander mana-sink relevance;
- legality status;
- source link;
- known limitations.

### User-supplied line behavior

User-supplied or Jin-generated lines must be marked:

```yaml
authority_class: user-context
validation_status: unvalidated
```

They must not be exported as Commander Spellbook truth.

### Tutor piles

Tutor-pile notes require:

- exact pile;
- all opponent branches;
- worst-case branch;
- recovery path;
- costs;
- timing;
- legality;
- certification status.

---

## 9.6 Simulation package

### Folder

```text
06 Simulations/Runs/
```

### Files

```text
simulation-<run-id>-summary.md
simulation-<run-id>-results.json
simulation-<run-id>-samples.csv
```

Full traces are optional private attachments:

```text
90 Attachments/Private Traces/<run-id>/
```

### Required front matter

```yaml
node_type: simulation-run
run_id: "sim-20260722-000184"
deck_snapshot_id: "..."
simulator_version: "..."
card_definition_version: "..."
seed_policy: "recorded-seeds"
mulligan_policy: "..."
target_condition: "cast-rhystic-by-turn-2"
target_turn: 2
games: 10000
wins: 7124
success_rate: 0.7124
margin_of_error: 0.0089
unsupported_cards: []
trace_validity: supported
```

### Required body

1. Question tested
2. Declared model
3. Result
4. Margin of error
5. Supported and unsupported cards
6. Trace validity
7. Warnings
8. Sample successful traces
9. Sample failure categories
10. Comparison references
11. Reproduction metadata

### Mandatory corrections

Exports must preserve known simulator warnings, including:

- Paradise Mantle traces are invalid without explicit equip and creature-tap sequencing.
- Springleaf Drum does not untap when the creature used for its cost untaps.
- Target-turn experiments are not cumulative unless the simulator explicitly guarantees cumulative semantics.

These corrections are constitutional regression requirements in the comparison draft. fileciteturn0file0

---

## 9.7 Theory notes package

### Folder

```text
07 Theory/
```

### Node types

- theorist;
- topic;
- source;
- claim;
- disagreement;
- format translation;
- deck application;
- personal conclusion.

### Claim filename

```text
theory-claim-<claim-id>-<slug>.md
```

### Required fields

```yaml
node_type: theory-claim
claim_id: "engines-require-conversion"
theorists:
  - stephen-menendian
topics:
  - engine-design
  - conversion-outlets
formats:
  - vintage
  - cedh
sources:
  - source-understanding-gush-3e
direct_evidence: true
inference: false
confidence: medium
transfer_status: translated-with-warning
disagreements: []
deck_applications:
  - wrongsi-infinite-mana-without-outlet
last_reviewed: "2026-07-23"
```

### Required body

- claim statement;
- documented source meaning;
- source citations;
- attribution chain;
- format scope;
- cEDH translation;
- supporting evidence;
- conflicting evidence;
- applicable decks;
- related claims;
- known limitations.

### Rights handling

Privately supplied licensed works may contribute private summaries and derived claim nodes.

Their full contents must not be redistributed. The theory compilation explicitly separates private analysis rights from redistribution rights. fileciteturn0file1

---

## 9.8 Lessons package

### Folder

```text
08 Lessons/
```

### Files

```text
curriculum-cedh-foundations-v1.md
lesson-<lesson-id>-<slug>.md
assessment-<assessment-id>-<slug>.md
progress-<user-profile-id>.md
```

### Required lesson fields

```yaml
node_type: lesson
lesson_id: "lesson-tempo-001"
curriculum_id: "cedh-foundations-v1"
revision: 2
topics:
  - tempo
  - progress-theory
formats:
  - cedh
source_nodes: []
claim_nodes: []
prerequisites: []
estimated_minutes: 25
assessment_ids:
  - assessment-tempo-001
rules_content: false
theory_content: true
opinion_content: false
```

### Required body structure

1. Objective
2. Rules facts
3. Theory
4. Competing definitions
5. Format limitations
6. Example
7. Deck application
8. Assessment
9. Reflection prompt
10. Sources

The theory corpus defines the learning cycle as listen, read, compare, apply, assess, and reflect. Exported lessons should retain that distinction rather than becoming one undifferentiated slab of educational oatmeal. fileciteturn0file1

---

## 9.9 Correction record package

### Folder

```text
09 Corrections/
```

### Filename

```text
correction-<correction-id>-<slug>.md
```

### Required fields

```yaml
node_type: correction
correction_id: "corr-000043"
category: simulator-model-correction
scope_type: simulator-wide
scope_ids: []
original_claim: "Paradise Mantle taps for mana."
corrected_claim: "The equipped creature receives and activates the mana ability."
authority_level: user-correction-supported-by-rules
validation_status: accepted
effective_at: "2026-07-19"
affected_subsystems:
  - simulator
  - jin
  - trace-validator
supersedes: null
exceptions: []
private_reasoning_included: false
```

### Required body

- original claim;
- corrected claim;
- correction category;
- scope;
- supporting evidence;
- authority level;
- affected subsystems;
- effective date;
- validation state;
- exceptions;
- supersession history;
- linked regression cases;
- application examples.

### Privacy behavior

Correction records are private-local by default.

Shareable exports may include only:

- correction ID;
- reusable corrected rule;
- authority basis;
- subsystem scope;
- validation state.

Private conversation text and identifying user commentary remain excluded.

---

## 9.10 Experiment queue package

### Folder

```text
10 Experiments/
```

### Filename

```text
experiment-<experiment-id>-<slug>.md
```

### Required fields

```yaml
node_type: experiment
experiment_id: "exp-000128"
status: queued
priority: normal
deck_snapshot_id: "..."
hypothesis: "Ledger Shredder provides better functional overlap than Artist's Talent."
independent_variable: "card substitution"
dependent_metrics:
  - engine-access-rate
  - retained-blue-pitch-count
  - card-selection-rate
control_snapshot_id: "..."
candidate_snapshot_ids: []
simulation_required: true
real-game-observation_required: false
created_by: user
created_at: "..."
```

### Required body

1. Question
2. Hypothesis
3. Evidence motivating the experiment
4. Control
5. Candidate change
6. Variables
7. Metrics
8. Success and failure thresholds
9. Confounders
10. Required runs or observations
11. Results
12. Interpretation
13. Decision status
14. Linked correction or report

### Lifecycle states

```text
draft
queued
ready
running
blocked
completed
inconclusive
cancelled
superseded
```

Experiment results do not become measured tournament evidence or global correction rules merely because the user liked the graph.

---

# 10. Provenance model

## 10.1 Central provenance ledger

`PROVENANCE.jsonl` stores one record per provenance item:

```json
{
  "provenance_id": "prov-000812",
  "source_class": "class-2-measured",
  "source_type": "commander-staples-metric",
  "source_record_ids": ["metric-11923"],
  "originating_sources": ["topdeck:event:5521", "edhtop16:event:884"],
  "canonical_record_ids": ["event:2191", "deck-instance:88211"],
  "formula_id": "commander-staples-frequency-v1.2",
  "date_window": {
    "start": "2026-01-23",
    "end": "2026-07-23"
  },
  "region": "global",
  "sample_size": 84,
  "coverage_ratio": 1.0,
  "generated_at": "2026-07-23T00:31:14-05:00",
  "exclusions": [],
  "caveats": []
}
```

## 10.2 Provenance requirements by evidence type

### Authority

- official or approved authority source;
- retrieval date;
- source version or effective date;
- canonical object ID.

### Source observation

- provider;
- raw source record ID;
- originating URL;
- discovery source;
- canonicalization result.

### Measured evidence

- metric ID;
- formula version;
- canonical population;
- filters;
- numerator;
- denominator;
- sample size;
- coverage;
- exclusions.

### Theory

- author;
- work;
- publication;
- date;
- source location;
- direct claim or later synthesis;
- transfer status;
- rights status.

### User context

- scope;
- privacy tier;
- correction or note ID;
- effective date.

### Inference

- supporting evidence IDs;
- assumptions;
- uncertainty;
- Jin or Decision Intelligence version.

## 10.3 Source disagreement

Competing source claims receive separate provenance records.

The note references both and identifies any canonical resolution without deleting the disagreement.

---

# 11. Privacy and licensing profiles

## 11.1 Privacy tiers

```text
public-safe
shareable-redacted
private-local
restricted-local
secret-never-export
```

## 11.2 Always excluded

The following must never enter an export:

- API tokens;
- passwords;
- session cookies;
- authentication headers;
- secret environment variables;
- database credentials;
- private model keys;
- hidden system prompts;
- unredacted local absolute paths containing user identity;
- internal security configuration;
- material explicitly marked `secret-never-export`.

## 11.3 Excluded by default

- private decklists;
- full simulator traces;
- private user notes;
- correction conversation transcripts;
- local metagame identities;
- personally identifying tournament notes;
- raw provider payloads;
- cloud prompt logs;
- private licensed source bodies;
- unpublished primers;
- user contact information.

The constitution specifically treats private decks, notes, traces, settings, tokens, theory annotations, and local-meta material as local by default. fileciteturn0file0

## 11.4 Explicit-selection material

The following may be included only through itemized consent:

- a named private deck snapshot;
- selected full traces;
- selected correction evidence;
- selected user notes;
- licensed private theory summaries;
- local tournament preparation notes.

A broad `include_private: true` switch is prohibited. It is too easy to misunderstand and too convenient for disaster.

## 11.5 Copyright treatment

Exports may contain:

- bibliographic metadata;
- links;
- short lawful excerpts;
- user-authored notes;
- model-generated summaries;
- attributed claim extraction;
- public-domain or permissively licensed source content.

Exports must not contain complete copyrighted works without recorded redistribution rights.

---

# 12. Incremental update behavior

## 12.1 Change detection

Each managed file has:

- stable `node_id`;
- prior `content_hash`;
- current generated hash;
- manifest path;
- record version.

The exporter compares the new generated state against the prior manifest.

## 12.2 Change classes

```text
added
updated
unchanged
superseded
tombstoned
relocated
conflicted
omitted
```

## 12.3 Immutable records

An immutable record is never rewritten for ordinary updates.

A new revision must:

- receive a new versioned node ID or revision suffix;
- identify the prior record in `supersedes`;
- cause the prior note to receive `superseded_by` only through a new index or metadata overlay;
- remain reproducible.

## 12.4 Mutable indexes

Mutable overview notes may be regenerated when their prior hash matches the manifest.

If the user changed the note, conflict behavior applies.

## 12.5 Deletions

Default behavior is non-destructive.

A removed Codie object produces a tombstone:

```yaml
status: tombstoned
tombstoned_at: "..."
reason: "source record withdrawn"
prior_path: "..."
```

The existing file is moved or represented under:

```text
99 Archive/Tombstones/
```

Hard deletion requires a separate explicit destructive operation.

## 12.6 Renames

A title or slug change creates:

- a new path;
- a relocation entry;
- an alias or redirect note at the old path when supported;
- updated `LINK_INDEX.json`;
- no change to `node_id`.

---

# 13. Conflict behavior

## 13.1 Machine-owned notes

Generated notes use:

```yaml
codie_managed: true
```

Their last exported hash appears in the manifest.

## 13.2 User-owned notes

User note folders and notes use:

```yaml
codie_managed: false
```

They are never overwritten or deleted.

## 13.3 Modified generated note

When the current file hash differs from the previous generated hash:

1. Preserve the user-edited file.
2. Generate the proposed new version into `98 Conflicts/`.
3. Create a conflict record.
4. Mark the original node as unresolved in the manifest.
5. Do not update the manifest hash as though the export succeeded.

Conflict filename:

```text
conflict-<node-short-id>-<timestamp>-generated.md
```

Conflict record:

```yaml
node_type: export-conflict
conflict_type: modified-managed-file
original_path: "..."
proposed_path: "..."
base_hash: "..."
observed_hash: "..."
proposed_hash: "..."
resolution_status: unresolved
```

## 13.4 Source-data conflict

Source disagreements are not filesystem conflicts.

They remain inside the relevant note and provenance ledger as evidence conflicts.

## 13.5 Duplicate node ID

Duplicate `node_id` values are fatal.

No export may complete with two files claiming the same stable identity.

## 13.6 Filename collision

Filename collisions are resolved deterministically with stable-ID suffixes, never by random numbering.

---

# 14. Manifest contract

## 14.1 Root manifest

`VAULT_MANIFEST.json`:

```json
{
  "manifest_schema_version": "1.0.0",
  "vault_id": "vault-codie-primary",
  "export_id": "export-20260723-0001",
  "export_mode": "full",
  "base_export_id": null,
  "generated_at": "2026-07-23T00:31:14-05:00",
  "codie_version": "2.x",
  "constitution_reference": {
    "version": "2.0-comparison-draft",
    "authoritative": false
  },
  "export_profile": "private-local",
  "packages": [
    "commander-staples",
    "deck-reports",
    "tournament-meta",
    "primers",
    "combos",
    "simulations",
    "theory",
    "lessons",
    "corrections",
    "experiments"
  ],
  "analysis_versions": {
    "analytics": "2.1.0",
    "simulator": "sim-r-0.9",
    "ontology": "tagger-map-2026-07-18",
    "theory_schema": "1.0.0",
    "correction_schema": "1.0.0"
  },
  "file_count": 814,
  "files": [],
  "conflicts": [],
  "omissions": [],
  "warnings": [],
  "source_snapshots": [],
  "manifest_hash": "sha256:..."
}
```

## 14.2 File manifest entry

```json
{
  "node_id": "codie:correction:corr-000043",
  "path": "09 Corrections/Simulator/correction-corr-000043-paradise-mantle-trace-legality.md",
  "content_hash": "sha256:...",
  "size_bytes": 3812,
  "record_version": 2,
  "immutable": true,
  "privacy_tier": "private-local",
  "change_status": "added"
}
```

## 14.3 Package manifest

Every standalone package contains:

```text
PACKAGE_MANIFEST.json
PACKAGE_README.md
PROVENANCE.jsonl
LINK_INDEX.json
```

The package manifest must identify external node dependencies not included in the package.

## 14.4 Export report

`EXPORT_REPORT.md` provides a human-readable summary:

- export ID;
- profile;
- included packages;
- record counts;
- changed items;
- omissions;
- conflicts;
- unresolved links;
- privacy warnings;
- validation results.

---

# 15. Obsidian compatibility requirements

## 15.1 Required compatibility

- UTF-8;
- Markdown;
- YAML front matter;
- relative file paths;
- Obsidian wikilinks;
- Markdown links for external sources;
- standard headings;
- standard lists and tables;
- no required community plugins.

## 15.2 Optional enhancements

May be generated only under a separate `Optional` folder:

- Dataview queries;
- Canvas files;
- graph-group configuration;
- CSS snippets;
- Bases definitions;
- templates.

The core notes must remain usable without them.

## 15.3 Front matter restrictions

YAML must:

- parse with a standard YAML parser;
- avoid duplicate keys;
- use ISO 8601 timestamps;
- quote ambiguous strings;
- use arrays rather than comma-packed strings;
- avoid unsupported custom tags;
- keep large evidence arrays outside front matter.

## 15.4 Markdown restrictions

Generated Markdown must not depend on:

- embedded JavaScript;
- HTML forms;
- remote scripts;
- executable code;
- unsafe iframe content.

## 15.5 Searchability

Every note begins with an H1 title and a compact summary paragraph.

Tags use a controlled namespace:

```text
codie/deck
codie/simulation
format/cedh
theory/tempo
status/active
privacy/private-local
```

---

# 16. UI requirements

These define user-facing behavior. They do not dictate filesystem implementation.

## 16.1 Export selection

The export screen must allow selection of:

- package types;
- decks and snapshots;
- commander signatures;
- tournament windows and regions;
- simulation runs;
- theory topics and sources;
- correction scopes;
- experiment states;
- privacy profile;
- full or incremental mode.

## 16.2 Export preview

Before execution, the UI must show:

- estimated file count;
- selected packages;
- private items included;
- copyrighted or restricted sources omitted;
- full traces included;
- expected conflicts;
- base manifest for incremental export;
- destination status;
- validation warnings.

## 16.3 Privacy confirmation

Explicit confirmation is required when exporting:

- private decks;
- full traces;
- private corrections;
- local-meta notes;
- restricted theory material.

## 16.4 Conflict review

The UI must distinguish:

- user-edited generated file;
- source-data conflict;
- unresolved link;
- obsolete file;
- duplicate identity.

It must not present all of them as “sync error,” the traditional software phrase for “something happened and we refuse to explain it.”

## 16.5 Post-export report

The UI must display:

- export ID;
- manifest path;
- added, updated, unchanged, conflicted, and omitted counts;
- validation result;
- privacy profile;
- warnings;
- files requiring manual review.

---

# 17. Backend contract boundaries

## 17.1 Permitted future components

```text
knowledge_vault/
├── models/
├── schemas/
├── planners/
├── serializers/
├── renderers/
├── provenance/
├── privacy/
├── diff/
├── conflicts/
├── validators/
└── repositories/
```

## 17.2 Proposed modules

### `VaultExportPlanner`

Responsibilities:

- resolve selected package scope;
- identify dependencies;
- apply privacy and rights filters;
- construct an export plan;
- perform no file writes.

### `VaultNodeAssembler`

Responsibilities:

- transform approved domain objects into export nodes;
- preserve IDs and provenance;
- perform no recommendation reasoning.

### `MarkdownRenderer`

Responsibilities:

- render deterministic Markdown from export nodes;
- contain no filesystem access.

### `ManifestBuilder`

Responsibilities:

- construct full and incremental manifests;
- calculate expected file records;
- contain no filesystem access.

### `VaultDiffEngine`

Responsibilities:

- compare desired export state with a previous manifest;
- classify changes;
- identify conflicts;
- perform no writes.

### `PrivacyFilter`

Responsibilities:

- apply privacy profile;
- apply explicit-selection rules;
- generate omission records.

### `RightsFilter`

Responsibilities:

- enforce redistribution permissions;
- prevent full-source export where rights are absent.

### `LinkResolver`

Responsibilities:

- resolve stable node IDs to paths;
- produce link index;
- detect broken links and duplicate IDs.

### `VaultValidator`

Responsibilities:

- validate schemas;
- validate links;
- validate deterministic rendering;
- validate privacy boundaries;
- validate manifests;
- validate Obsidian-safe paths.

## 17.3 Prohibited architectural behavior

No export component may:

- query raw providers directly;
- recalculate analytics;
- run simulations;
- create recommendations;
- alter corrections;
- modify canonical records;
- import Obsidian edits;
- infer missing card identity;
- silently redact without recording the omission.

---

# 18. Interface contracts

These are logical interfaces, not implementation code.

## 18.1 Plan export

```text
plan_export(request, prior_manifest?) -> ExportPlan
```

Inputs:

- package selections;
- entity selections;
- date and region filters;
- export mode;
- privacy profile;
- rights profile;
- prior manifest reference.

Output:

- planned nodes;
- planned files;
- dependencies;
- omissions;
- warnings;
- expected conflicts;
- validation blockers.

## 18.2 Assemble node

```text
assemble_node(domain_record, export_context) -> VaultNode
```

Must preserve:

- domain identity;
- record version;
- evidence classes;
- provenance;
- privacy;
- relationships;
- version links.

## 18.3 Render node

```text
render_markdown(vault_node) -> RenderedArtifact
```

Must be deterministic for identical inputs.

## 18.4 Build manifest

```text
build_manifest(export_plan, rendered_artifacts) -> VaultManifest
```

## 18.5 Diff export

```text
diff_export(prior_manifest, desired_manifest, observed_files?) -> ExportDiff
```

`observed_files` is required to detect user modification of managed notes.

## 18.6 Validate export

```text
validate_export(manifest, artifacts, policy) -> ValidationReport
```

---

# 19. Failure behavior

## 19.1 Fatal failures

Export must not proceed when:

- duplicate node IDs exist;
- manifest schema is invalid;
- a selected private item lacks explicit authorization;
- a secret-bearing field survives filtering;
- a generated path is unsafe;
- deterministic rendering fails;
- a required source ID cannot be resolved;
- an incremental export lacks its base manifest;
- a managed file conflict would otherwise be overwritten.

## 19.2 Nonfatal warnings

Export may proceed with warnings when:

- optional linked nodes are omitted;
- a source URL is stale;
- sample coverage is incomplete;
- theory transfer status is unresolved;
- a source conflict remains;
- an unsupported simulation card is disclosed;
- an optional attachment is absent.

## 19.3 Partial package failure

A package must not be marked successful when required files failed.

Other independent packages may complete only when:

- the manifest records the failed package;
- cross-package dependencies remain valid;
- no privacy or identity invariant was violated.

---

# 20. Test fixtures

## 20.1 Core fixture set

### Fixture A: Exact partner staples

- Commanders: Rograkh and Ishai.
- Eight canonical decks.
- One sideboard-only card.
- One commander card incorrectly present in provider mainboard.
- Expected result: both excluded from mainboard frequency.

### Fixture B: Partial partner query

- Rograkh paired with three commanders.
- Exact-pair and partial-pair exports.
- Expected result: distinct IDs, labels, populations, and filenames.

### Fixture C: Deck snapshots

- Initial snapshot.
- Second unchanged retrieval.
- Third retrieval with one card changed.
- Expected result: cached current report for unchanged snapshot; new immutable snapshot and diff for changed list.

### Fixture D: Duplicate tournament event

- TopDeck and Hareruya records for one event.
- Conflicting player count.
- Expected result: one canonical event, two source records, visible conflict.

### Fixture E: Private deck shareable export

- Private deck selected under `public-safe`.
- Expected result: deck omitted, omission recorded, no deck text present anywhere.

### Fixture F: Explicit private deck export

- Same deck under `private-local`.
- Explicit item authorization.
- Expected result: included and marked non-shareable.

### Fixture G: Licensed theory source

- Private copy of *Understanding Gush*.
- Expected result: metadata, private summary, and derived claims allowed; source body excluded.

### Fixture H: Primer rights

- Public primer with no redistribution grant.
- Expected result: metadata, link, section map, attributed summary; no mirrored full text.

### Fixture I: Modified generated note

- Prior manifest hash differs from observed file.
- Expected result: original preserved, proposed note placed in conflict output, unresolved conflict recorded.

### Fixture J: User note

- `codie_managed: false`.
- Expected result: never overwritten, moved, or deleted.

### Fixture K: Simulation correction

- Trace treats Paradise Mantle as tapping directly.
- Expected result: trace marked invalid and warning exported.

### Fixture L: Target-turn simulations

- Turn-two rate exceeds turn-three rate.
- Expected result: separate experiments; no cumulative-probability language.

### Fixture M: Global correction and deck correction

- Paradise Mantle correction: simulator-wide.
- No mana sink: one WrongSi snapshot.
- Expected result: scopes remain separate.

### Fixture N: Correction supersession

- Correction revision two supersedes revision one.
- Expected result: both retained; index points to revision two.

### Fixture O: Experiment lifecycle

- Queued, blocked, completed, and superseded experiments.
- Expected result: correct folder and status links without losing history.

### Fixture P: Unicode titles

- Names with apostrophes, diacritics, commas, and partner separators.
- Expected result: safe ASCII filename and exact Unicode title.

### Fixture Q: Filename collision

- Two primers with identical title and author display name but different source IDs.
- Expected result: unique deterministic filenames.

### Fixture R: Broken theory link

- Claim references omitted source node.
- Expected result: declared external dependency or validation failure.

### Fixture S: Tombstone

- Primer source removed from Codie.
- Expected result: tombstone and archive state, not silent deletion.

### Fixture T: Incremental base mismatch

- Increment references the wrong base export ID.
- Expected result: fatal validation failure.

---

# 21. Required test families

## 21.1 Schema tests

- every node type validates;
- missing required fields fail;
- unknown fields follow declared compatibility policy;
- duplicate YAML keys fail;
- invalid timestamps fail.

## 21.2 Determinism tests

Identical domain records, versions, filters, and profiles must produce byte-identical:

- Markdown;
- JSON;
- CSV ordering;
- manifests;
- link indexes.

Generated timestamps must be injected as controlled inputs during tests.

## 21.3 Link tests

- every generated internal link resolves;
- aliases do not create ambiguous identity;
- relocation redirects resolve;
- omitted dependencies are disclosed.

## 21.4 Privacy tests

- secrets never export;
- private material requires explicit item authorization;
- shareable exports contain no private deck text;
- omission records reveal categories without leaking excluded content.

## 21.5 Rights tests

- private books are not copied;
- full primer text is withheld without rights;
- source citations and summaries remain available.

## 21.6 Incremental tests

- added;
- changed;
- unchanged;
- renamed;
- superseded;
- tombstoned;
- user-conflicted;
- base-manifest mismatch.

## 21.7 Obsidian compatibility tests

- vault opens without plugins;
- YAML parses;
- Markdown renders;
- filenames work on Windows;
- links resolve;
- no path exceeds configured limit;
- no forbidden filename exists.

## 21.8 Evidence integrity tests

- formulas and metric versions are present;
- source lineage survives export;
- source conflicts remain visible;
- low sample and coverage remain visible;
- theory never appears as Class 0 authority;
- user conclusions remain separate from theorist attribution.

---

# 22. Acceptance criteria

The Knowledge Vault export contract is accepted only when all of the following are demonstrably specified and later validated:

1. Every exported entity has one stable `node_id`.
2. Human-readable names may change without changing identity.
3. Immutable records are never silently rewritten.
4. User-authored notes are never overwritten.
5. Modified managed notes produce conflicts rather than replacement.
6. Every package contains a manifest and provenance records.
7. Full and incremental exports are distinguishable.
8. Incremental exports identify their required base export.
9. Internal links resolve deterministically.
10. Duplicate node IDs are fatal.
11. File paths are Windows-safe and Obsidian-compatible.
12. Private decks are excluded from shareable exports by default.
13. Full traces are excluded by default.
14. Secrets are never exportable.
15. Restricted theory and primer bodies are excluded without redistribution rights.
16. Source attribution survives summaries and derived notes.
17. Source conflicts remain visible.
18. Commander, mainboard, sideboard, and auxiliary zones remain distinct.
19. Missing staple flags are not rendered as automatic recommendations.
20. Simulation limitations and invalid trace patterns remain visible.
21. Correction scope remains as narrow as justified.
22. Theory claims preserve author, source, translation status, and disagreements.
23. Lesson notes distinguish rules, theory, example, and opinion.
24. Experiment records preserve hypothesis, controls, metrics, and lifecycle.
25. Tombstones preserve historical link integrity.
26. Manifests include analysis, ontology, simulator, schema, and source versions.
27. Identical inputs produce deterministic output.
28. Export components perform no canonical writes.
29. No export component creates an independent recommendation path.
30. The final validation report lists all omissions, conflicts, warnings, and failures.

---

# 23. Explicit exclusions

This contract does not authorize:

- implementation of filesystem writers;
- ZIP or archive generation;
- automatic Obsidian synchronization;
- import of edited notes into Codie;
- bidirectional merge behavior;
- cloud vault hosting;
- Git synchronization;
- mobile editing;
- Obsidian plugin development;
- Dataview as a required dependency;
- PDF generation;
- copying complete primers or licensed books;
- retention of every simulator trace;
- mutation of canonical records from exported notes;
- treating the comparison draft as ratified authority.

---

# 24. Proposed delivery phases

## Phase KV-0: Contract ratification

Deliverables:

- accepted folder taxonomy;
- accepted node types;
- accepted privacy profiles;
- accepted rights policy;
- accepted conflict policy;
- accepted manifest schema.

No writers.

## Phase KV-1: Export domain schemas

Deliverables:

- `VaultNode`;
- package-specific node schemas;
- provenance schema;
- manifest schema;
- conflict schema;
- omission schema;
- test fixtures.

No rendering or writers.

## Phase KV-2: Deterministic planning and rendering

Deliverables:

- export planner;
- Markdown rendering;
- CSV and JSON rendering;
- link resolution;
- deterministic serialization;
- in-memory validation.

No filesystem writes.

## Phase KV-3: Diff and conflict engine

Deliverables:

- prior-manifest comparison;
- content-hash handling;
- change classification;
- tombstone planning;
- conflict planning.

No filesystem writes.

## Phase KV-4: File-writer contract

A separate contract must define:

- destination validation;
- atomic writes;
- temporary directories;
- rollback;
- backup behavior;
- path traversal defense;
- collision handling;
- partial failure;
- file permissions;
- archive packaging.

This phase is deliberately outside the present authorization.

---

# 25. Codex handoff

```text
TASK:
Design and validate the Codie V2 Knowledge Vault export domain without implementing filesystem writers.

AUTHORIZED:
- Export package schemas.
- Stable node identifiers.
- Deterministic filename rules.
- Obsidian Markdown front matter schemas.
- Provenance records.
- Full and incremental manifest schemas.
- Privacy and rights filtering contracts.
- Link resolution contracts.
- Diff and conflict planning.
- In-memory serializers and validators only if separately authorized by an implementation phase.
- Fixtures and tests.

NOT AUTHORIZED:
- Writing, moving, renaming, deleting, or archiving real files.
- ZIP creation.
- Obsidian synchronization.
- Importing Obsidian edits.
- Canonical database mutation.
- New recommendation logic.
- New analytics.
- Simulation execution.
- Provider access.
- Copying restricted source content.

REQUIRED PACKAGE TYPES:
1. Commander staples.
2. Deck reports and snapshots.
3. Tournament meta.
4. Primers.
5. Combos, packages, lines, and tutor piles.
6. Simulations.
7. Theory notes and attributed knowledge graph nodes.
8. Lessons and assessments.
9. Correction records.
10. Experiment queues and results.

REQUIRED INVARIANTS:
- One stable node_id per exported entity.
- Immutable historical records.
- Mutable indexes only.
- No silent overwrite.
- User notes never mutated.
- Explicit private-item authorization.
- Secrets never exported.
- Rights restrictions enforced.
- Provenance preserved.
- Source conflicts preserved.
- Deterministic serialization.
- Broken links detected.
- Incremental exports identify their base.
- Tombstones instead of silent deletion.
- Export remains non-canonical.

VALIDATION:
- Schema tests.
- Determinism tests.
- Privacy tests.
- Rights tests.
- Link tests.
- Conflict tests.
- Incremental-update tests.
- Windows path tests.
- Obsidian compatibility tests.
- Evidence-classification tests.
- Regression fixtures for known simulator and correction rules.

COMPLETION REPORT:
- Files proposed or created.
- Schemas defined.
- Interfaces defined.
- Fixtures added.
- Tests executed.
- Validation results.
- Unresolved decisions.
- Confirmation that no file writer or canonical mutation was implemented.
```

This contract authorizes the Knowledge Vault’s structure, identity model, package schemas, privacy rules, provenance, manifests, incremental semantics, conflicts, and validation requirements. It does not authorize file-writer implementation.
> [!IMPORTANT]
> Repository intake note: This is a preserved pre-ratification design
> proposal. `docs/CODIE_V2_CONSTITUTION.md` is now ratified and is the
> governing authority. Statements below that call V2 a non-authoritative
> comparison draft are historical. This proposal does not authorize
> implementation.
