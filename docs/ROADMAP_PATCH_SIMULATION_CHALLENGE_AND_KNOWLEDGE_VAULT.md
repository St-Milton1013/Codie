# Roadmap Patch - Simulation Challenge And Knowledge Vault

Date: 2026-06-25

Status: Accepted for future roadmap planning. Implementation deferred.

## Governance

This packet records potential future work only. It does not authorize schema
changes, implementation, dependency additions, or changes to the current phase
contract.

Before any item begins:

- create a phase-specific implementation contract
- confirm dependencies and build order
- define schema impact and migrations
- define immutable records and annotation boundaries
- define public interfaces, failure modes, and acceptance tests
- complete the Implementation Quality Gate

The probability engine remains reproducible and evidence-oriented. Human review
is QA annotation, not tournament evidence or recommendation evidence.

## Roadmap Placement

Recommended sequence after the core Probability Simulation Engine is validated:

1. Simulation Challenge Mode
2. Challenge Mode Line Review / Veto System
3. Simulation Trace Review Export System
4. Obsidian Knowledge Vault Integration
5. Research Journals and longitudinal query support

Challenge Mode and all review features must reuse the same simulator, target
model, action trace, and seed/config semantics as the Probability Simulation
Engine. The knowledge vault consumes completed outputs and must not become a
second source of canonical truth.

---

## Patch A - Simulation Challenge Mode

### Purpose

Add an interactive training mode tied to the Probability Simulation Engine.
Codie generates an opening hand from a selected deck and target condition. The
user predicts whether the exact hand can reach the target by the required turn.
Codie then runs the simulator against that exact hand and compares the result
with the user's answer.

This is a training and validation tool, not a recommendation system.

### Example Workflow

```text
Target: Cast Rhystic Study by Turn 2

Opening hand:
- Tropical Island
- Chrome Mox
- Brainstorm
- Polluted Delta
- Mystic Remora
- Force of Will
- Lotus Petal

User answer:
Yes / No

Optional:
The user records the line they believe works.

Codie result:
- simulator success or failure
- reachable line, when found
- turn reached
- actions taken
- mana generated
- cards used
- whether the user's answer matched the simulator
```

### Required Outputs

- opening hand
- target condition
- user answer
- optional user line
- simulator result
- success/failure
- shortest found line, when available
- action trace
- comparison between user answer and simulator result
- unsupported cards

### Required Rules

- Use the same simulation engine as the Probability Simulation Engine.
- Do not invent separate hand-evaluation logic.
- Store the seed and complete simulation config for reproducibility.
- Store `deck_hash`, target condition, seed, and generation timestamp.
- Run the simulator against the exact displayed opening hand.
- Disclose every unsupported card.
- Never silently ignore unsupported cards or actions.
- Do not generate recommendation or strategy language.

### Suggested Schema

Potential table: `simulation_challenges`

Suggested fields:

```text
challenge_id
deck_hash
target_card
target_zone
target_turn
opening_hand_json
seed
user_answer
user_line_text
simulator_success
simulator_line_json
unsupported_cards_json
generated_at
completed_at
```

Schema remains a proposal until a dedicated contract and migration review are
approved.

### Suggested Module Placement

```text
codie/probability_engine/challenge_mode.py
```

Future UI placement:

```text
Probability Lab -> Challenge Mode
```

### Acceptance Tests

- challenge hand generation is deterministic from seed
- target condition is stored
- user answer is recorded
- simulator runs against the exact hand
- reachable line is returned when found
- failure is returned when unreachable
- unsupported cards are reported
- no recommendation or strategy language is generated

---

## Patch B - Challenge Mode Line Review / Veto System

### Purpose

Allow users to review simulator-generated success lines and flag lines that are
incorrectly modeled, unrealistic, unsupported, or poorly sequenced.

Challenge Mode tests both directions:

```text
user prediction -> simulator verification
simulator line -> user QA review
```

### Review Statuses

- Accepted
- Incorrect
- Unrealistic
- Unsupported Card Behavior
- Bad Sequencing
- Mana Modeling Error
- Tutor/Search Error
- Other

### Required Outputs

- immutable simulator line
- full action trace
- user review status
- review reason
- optional review note
- review timestamp
- affected cards
- affected action types

### Annotation Rule

User review creates an annotation over simulator output. It must not rewrite,
delete, or replace the original result or action trace.

### Required Workflow

1. Simulator produces a line.
2. User reviews the full action trace.
3. User accepts or vetoes the line.
4. Codie stores the review annotation.
5. Reviewed lines may later become regression cases or correction backlog
   entries.

### Allowed Uses

- simulator QA
- rule refinement
- unsupported-card identification
- impractical-line review
- regression fixture generation
- card behavior refinement backlog

### Forbidden Uses

- automatically retraining strategy
- treating a veto as tournament evidence
- treating a review as recommendation evidence
- silently deleting results
- modifying historical simulation records
- overwriting raw traces

### Suggested Schema

Potential table: `simulation_line_reviews`

Suggested fields:

```text
review_id
challenge_id
batch_id
result_id
trace_id
deck_hash
target_card
target_turn
simulator_success
action_trace_json
review_status
review_reason
review_note
affected_cards_json
affected_actions_json
created_at
```

Schema remains a proposal until a dedicated contract and migration review are
approved.

### Acceptance Tests

- user can accept a simulator line
- user can veto a simulator line
- veto stores reason and note
- original trace remains unchanged
- reviewed line can be exported as a regression fixture
- rejected reviewed line is excluded from accepted-success accuracy
- review annotations do not affect raw simulation history

---

## Patch C - Simulation Trace Review Export System

### Purpose

Export large simulation trace sets for human review in Obsidian or another
Markdown editor, then re-import structured review annotations.

Raw simulator output remains immutable. Human review remains a separate
annotation layer.

### Required Features

- export simulation batch traces
- export Challenge Mode traces
- export successful and failed lines
- export unsupported-card traces
- export suspicious or impractical lines
- emit Markdown review files
- emit JSON sidecar files
- re-import edited review annotations
- preserve original batch, result, and trace IDs
- never overwrite raw simulation history

### Recommended Vault Structure

```text
Codie/
+-- Simulation Review/
    +-- Batches/
    |   +-- batch_<batch_id>/
    |       +-- index.md
    |       +-- traces/
    |       |   +-- trace_000001.md
    |       |   +-- trace_000002.md
    |       +-- reviewed/
    |       +-- data/
    |           +-- batch_manifest.json
    |           +-- trace_000001.json
    |           +-- trace_000002.json
    +-- Challenge Mode/
        +-- challenge_<challenge_id>/
            +-- index.md
            +-- trace.md
            +-- trace.json
```

### Markdown Review Frontmatter

```yaml
---
type: simulation_trace_review
batch_id: batch_2026_06_24_001
trace_id: trace_000123
deck_hash: sha256:...
target_card: Rhystic Study
target_turn: 2
simulator_success: true
review_status: unreviewed
review_reason:
affected_cards: []
affected_actions: []
reviewed_at:
reviewer:
---
```

Allowed `review_status` values:

```text
unreviewed
accepted
vetoed
unrealistic
incorrect
unsupported_card_behavior
bad_sequencing
mana_model_error
tutor_search_error
other
```

### Required Import Behavior

On import, Codie must:

- locate the immutable original trace by `trace_id`
- validate `batch_id` and `deck_hash`
- validate the review status
- store a separate review annotation
- leave `simulation_traces` unchanged
- leave `simulation_batch_results` unchanged
- update reviewed-accuracy reports only

### Suggested Schema

Potential table: `simulation_trace_review_exports`

```text
export_id
batch_id
challenge_id
export_root
exported_trace_count
exported_at
manifest_path
status
```

Potential extension of `simulation_line_reviews`:

```text
review_id
batch_id
challenge_id
result_id
trace_id
deck_hash
target_card
target_turn
simulator_success
action_trace_hash
review_status
review_reason
review_note
affected_cards_json
affected_actions_json
review_source_path
reviewed_at
imported_at
```

Schema remains a proposal until a dedicated contract and migration review are
approved.

### Suggested Modules

```text
codie/probability_engine/trace_export.py
codie/probability_engine/trace_review_import.py
codie/probability_engine/review_models.py
codie/exports/simulation_trace_review.py
```

### Suggested CLI

```text
codie-sim export-review-batch
codie-sim import-review-batch
codie-sim export-challenge-review
codie-sim reviewed-accuracy-report
```

### Required Reports

- total traces
- reviewed traces
- accepted lines
- vetoed lines
- unrealistic lines
- unsupported-card errors
- mana-model errors
- tutor/search errors
- reviewed simulator accuracy

### Evidence-First Rules

- Reviews are QA annotations.
- Reviews are not tournament evidence.
- Reviews are not recommendation evidence.
- Reviews do not rewrite raw simulator output.
- Reviews may create correction backlog items.
- Reviews may create regression fixtures.

### Acceptance Tests

- exports a batch manifest
- exports trace Markdown
- exports trace JSON sidecar
- preserves trace IDs
- imports edited Markdown review
- imports JSON sidecar review
- rejects unknown trace IDs
- rejects mismatched `deck_hash`
- rejects invalid review status
- stores annotation without changing raw trace
- reviewed accuracy excludes vetoed lines from accepted-success count
- Obsidian export requires no plugin

---

## Patch D - Obsidian Knowledge Vault Integration

### Purpose

Make every meaningful Codie analysis optionally produce a permanent,
human-readable Markdown knowledge base. The vault becomes a historical research
notebook and export surface, not an authoritative database.

### Supported Document Types

- deck analyses
- recommendation snapshots
- simulator runs
- Challenge Mode sessions
- tournament reports
- commander reports
- card reports
- package reports
- metagame snapshots
- innovation alerts
- review notes
- research journals

### Immutability Rule

Historical reports are append-only snapshots. New analysis creates a new dated
document. Existing evidence, traces, and reports are not silently overwritten.

### Recommended Vault Structure

```text
Codie Vault/
+-- Inbox/
+-- Commander Reports/
+-- Card Reports/
+-- Deck Reports/
+-- Simulation/
|   +-- Batch Reviews/
|   +-- Challenge Mode/
+-- Innovations/
+-- Tournament Reports/
+-- Meta Reports/
+-- Recommendation Reports/
+-- Historical Snapshots/
+-- Research Journals/
+-- Attachments/
+-- Templates/
```

### Required Frontmatter

```yaml
---
type: deck_report
deck_hash: ...
analysis_id: ...
analysis_date: ...
commander_signature: tymna_the_weaver|kraum_ludevics_opus
time_window: 6_months
region: global
codie_version: 1.0
simulation_version: ...
recommendation_version: ...
linked_reports: []
tags:
  - codie
  - deck
  - cedh
---
```

Every exported note must include stable identity, generation timestamp,
applicable engine/config versions, and links back to source evidence where
available.

### Internal Linking

Reports should emit stable Obsidian links for:

- commanders and partner pairs
- cards
- tournaments
- innovation reports
- simulation batches
- Challenge Mode sessions
- recommendation reports
- related historical snapshots

The links are presentation relationships. They do not replace canonical
database relationships.

### Historical Snapshots And Diffs

Each analysis creates a dated snapshot. When a prior compatible snapshot exists,
Codie may generate a deterministic change summary covering:

- card additions and removals
- metric changes
- recommendation drift
- metagame drift
- staple confidence changes
- innovation appearance or disappearance
- simulator version or result changes
- evidence growth

Every diff must identify both compared snapshot IDs and must not present
correlation as strategic truth.

### Obsidian Canvas Support

Future Canvas export may visualize:

- commander ecosystems
- package relationships
- combo maps
- tournament evolution
- innovation timelines
- recommendation evolution

Canvas files remain generated views over existing records.

### Longitudinal Research

The vault should support questions such as:

- When did a card first appear?
- When did its confidence cross a threshold?
- Which tournaments contributed to a metric change?
- Which simulator batches evaluated it?
- Which user reviews rejected related lines?
- How has a deck or recommendation changed over time?

### Local RAG Boundary

The vault may later serve as a local retrieval source for a user-controlled AI
assistant. This is deferred and requires its own privacy, provenance, indexing,
and stale-document contract.

Vault text must never silently become canonical tournament evidence,
recommendation evidence, or simulator truth.

### Research Journals

Research journals link:

- original hypothesis
- analyzed deck
- simulator batches
- Challenge Mode attempts
- innovation reports
- tournament evidence
- user conclusions
- unresolved questions

User-authored conclusions must be labeled as notes or hypotheses. They are not
promoted into Codie's evidence layers without a separate validated process.

### Acceptance Direction

A future implementation contract should require:

- stable human-readable paths
- valid YAML frontmatter
- deterministic internal links
- append-only historical snapshots
- reproducible diff inputs
- no mutation of canonical records
- no Obsidian plugin dependency
- safe filename/path handling
- explicit export root containment
- round-trip trace review annotations without raw-trace mutation

---

## Shared Risks And Guardrails

### Risks

- schema growth before the simulator data model is stable
- duplicated review semantics between Challenge Mode and batch review
- treating human opinion as evidence
- export paths escaping the configured vault root
- unstable filenames breaking internal links
- edited Markdown being mistaken for canonical data
- stale vault notes being presented as current analysis
- unsupported simulator actions being hidden

### Guardrails

- one shared review model for challenge and batch traces
- immutable raw simulation records
- separate annotation persistence
- content hashes for exported traces and imported review validation
- explicit engine/config/version metadata
- output-root containment
- stable path and slug rules
- clear generated-at and reviewed-at timestamps
- evidence classification on every imported annotation
- no implementation before dedicated contracts are approved

## Current Decision

These patches solve real project problems and are accepted into the future
roadmap. They are intentionally deferred until the core simulator, trace model,
and export boundaries are stable.

No current implementation phase is displaced by this patch.
