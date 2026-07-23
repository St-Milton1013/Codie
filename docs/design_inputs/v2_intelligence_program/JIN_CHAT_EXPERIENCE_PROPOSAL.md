



# Jin Chat Experience for Codie

## 1. Product definition

Jin is Codie’s governed conversational interface for deck analysis, theory application, rules-supported reasoning, simulation interpretation, experiment design, and correction capture. It is not a generic chatbot, a second analytics engine, or an alternate path for generating persisted recommendations.

The interface must preserve four distinctions that ordinary chat products cheerfully blur because apparently provenance is considered optional decoration:

1. **What Codie measured**
2. **What external sources claimed**
3. **What Jin inferred**
4. **What the user concluded or corrected**

Jin may read canonical evidence, Unified Evidence, theory material, simulations, deck snapshots, user context, and corrections. It may not mutate canonical card data, tournament records, measured metrics, confidence tables, or persisted recommendations. fileciteturn0file0

The theory experience must retrieve topic-relevant frameworks, apply them independently where useful, preserve disagreements, and avoid fabricating consensus or impersonating theorists. The theory corpus already defines evidence-packet assembly, topic routing, framework selection, independent analysis, evidence comparison, disagreement preservation, and a neutral issue map as the intended operating sequence. fileciteturn0file1

---

# 2. Experience principles

## 2.1 Deck context is always explicit

Every answer concerning a deck must identify:

- deck name;
- commander signature;
- snapshot date;
- deck hash or abbreviated snapshot identifier;
- source URL when applicable;
- whether the snapshot matches the current external deck;
- analysis profile;
- local-meta context, when included.

There is no invisible “current deck” state. Invisible context is how old decklists become new conclusions while everyone stares at the screen wondering why the software is confidently discussing a card cut three revisions ago.

## 2.2 Answers are action-first, evidence-second, detail-on-demand

The default answer order is:

```text
Direct conclusion
Confidence and uncertainty
Material caveat or contradiction
Evidence summary
Theory interpretation
Suggested test or experiment
Expandable citations and methodology
```

This follows the constitutional action-first structure while keeping underlying evidence inspectable. fileciteturn0file0

## 2.3 Theory is active by default

Jin should ordinarily include relevant theory-corpus interpretation unless the user selects:

- Evidence only
- Rules only
- Simulation only
- No theory for this answer

Theory must be labeled separately from measured evidence. A theory lens cannot increase empirical confidence merely because its author is famous.

## 2.4 Contradictions are surfaced, not averaged away

Jin must distinguish:

- authority conflicts;
- source-observation conflicts;
- empirical conflicts;
- simulation versus tournament conflicts;
- theory disagreements;
- user-context conflicts;
- correction-ledger conflicts.

Different theories may disagree definitionally, contextually, empirically, by format, or by priority. The corpus explicitly requires preserving these disagreements rather than manufacturing consensus. fileciteturn0file1

## 2.5 Every persisted conclusion is replayable

A saved answer must retain:

- question;
- resolved intent;
- deck snapshot;
- selected evidence scope;
- evidence packet identifier;
- source versions;
- analysis profile;
- model profile;
- generated date;
- final answer packet;
- citations;
- contradictions;
- applied corrections;
- simulation references;
- answer supersession status.

Reopening an answer displays the original result. Re-evaluating produces a new answer linked to the original. Historical answers are not silently rewritten.

---

# 3. Primary information architecture

Codie retains the two-screen model:

```text
SCREEN A: DECK WORKSPACE
- Deck editor/import
- Snapshot history
- Composition and package views
- Selection of cards, packages, or findings
- “Discuss in Jin” handoff

SCREEN B: JIN WORKSPACE
- Conversation history
- Active deck context
- Question composer
- Evidence-scope controls
- Answer stream
- Evidence and citation inspector
- Contradiction panel
- Simulation and experiment tools
- Correction workflow
```

Mobile remains read-only. Full mobile execution, editing, simulation control, and correction submission remain outside immediate implementation scope. The desktop output must still use mobile-readable content structure so reports can later be delivered without redesigning every answer from scratch.

---

# 4. Desktop textual wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ CODIE / JIN                                                                  │
│ Deck: Rograkh + Ishai  | Snapshot: Jul 22, 23:41 | Current ✓ | Profile: Comp │
├──────────────────┬──────────────────────────────────────┬────────────────────┤
│ CONVERSATIONS    │ CHAT                                 │ EVIDENCE INSPECTOR │
│                  │                                      │                    │
│ + New discussion │ [Context notice]                     │ Scope              │
│                  │ Using snapshot RI-2026-07-22-07       │ ● Current snapshot │
│ Today            │ 98 cards supported, 2 partial        │ ● Tournament data  │
│ • Ledger vs ...  │                                      │ ● Theory corpus    │
│ • Rhystic test   │ User                                 │ ○ Local meta       │
│                  │ How does Ledger Shredder compare...  │ ○ Reddit context   │
│ Yesterday        │                                      │                    │
│ • Snapshot diff  │ Jin                                  │ Sources            │
│ • Tutor pile     │ Ledger Shredder provides... [1][2]   │ 12 material        │
│                  │                                      │ 4 supporting       │
│ Experiments      │ Confidence: Moderate                 │ 2 contradictory    │
│ • Engine test    │ Agreement: Mixed                     │                    │
│ • Land swap      │ Legality: Verified                   │ Contradictions     │
│                  │ Snapshot: RI-2026-07-22-07            │ ⚠ 2 unresolved     │
│                  │                                      │                    │
│                  │ [Why] [Evidence] [Theory] [Conflicts]│ Citations          │
│                  │ [Create experiment] [Correct answer] │ [1] Tournament...  │
│                  │                                      │ [2] Menendian...   │
│                  │ ──────────────────────────────────── │                    │
│                  │ Ask Jin                              │                    │
│                  │ ┌──────────────────────────────────┐ │                    │
│                  │ │ Type a question...               │ │                    │
│                  │ └──────────────────────────────────┘ │                    │
│                  │ Scope: Deck + Evidence + Theory       │                    │
│                  │ [Attach card] [Compare] [Simulate]    │                    │
└──────────────────┴──────────────────────────────────────┴────────────────────┘
```

## Layout behavior

- Left rail width: 240–300 px.
- Center conversation column: minimum 620 px.
- Evidence inspector: 320–420 px.
- Inspector may collapse to a drawer.
- Conversation text should not stretch beyond roughly 80 characters per line.
- Resizing must not hide confidence, snapshot identity, or contradiction status.
- On narrower desktop windows, the left rail collapses before the evidence inspector.
- Citations open in the inspector without replacing the answer.

---

# 5. Read-only mobile layout

```text
┌──────────────────────────────┐
│ Jin                          │
│ Rograkh + Ishai              │
│ Snapshot Jul 22 • Current ✓  │
├──────────────────────────────┤
│ Question                     │
│ Ledger Shredder compared...  │
├──────────────────────────────┤
│ Answer                       │
│ Direct conclusion...         │
│                              │
│ Confidence: Moderate         │
│ Agreement: Mixed             │
│ Legality: Verified           │
│                              │
│ ⚠ 2 contradictions           │
│ [View evidence]              │
│ [View theory]                │
│ [View citations]             │
├──────────────────────────────┤
│ Historical answer            │
│ Generated Jul 22, 23:48      │
│ Snapshot RI-...              │
└──────────────────────────────┘
```

Read-only mobile permits:

- viewing conversations;
- opening citations;
- viewing uncertainty and contradictions;
- reading snapshot comparisons;
- reading simulation reports;
- reading experiments and correction status.

It does not initially permit:

- starting simulations;
- editing experiments;
- submitting corrections;
- changing deck context;
- altering evidence profiles.

---

# 6. End-to-end workflow

## 6.1 Opening a deck context

### Entry points

A Jin session can begin from:

- deck editor: **Discuss this deck**
- selected card: **Ask Jin about this card**
- deck-health finding: **Explain in Jin**
- snapshot history: **Compare in Jin**
- simulation report: **Discuss results**
- conversation history: reopen prior answer
- Jin home: select a deck manually

### Context-resolution flow

```text
Entry request
  -> Resolve deck identity
  -> Resolve requested snapshot
  -> Check source freshness
  -> Validate canonical card identities
  -> Load correction scope
  -> Load available analyses
  -> Display context summary
  -> Ready for question
```

### Context summary

```text
DECK CONTEXT

Rograkh, Son of Rohgahh + Ishai, Ojutai Dragonspeaker

Snapshot
RI-2026-07-22-07
Imported: Jul 22, 2026, 11:41 PM
Source: Moxfield
Source status: Current
Changes since previous snapshot: 3 cards

Coverage
96 fully supported
2 partially supported
0 unresolved

Available evidence
Tournament population: 63 eligible decks
Simulations: 4 current, 2 stale
Theory topics detected: tempo, engine conversion, interaction density
Corrections applied: 7 deck-specific, 3 global
```

### Context warnings

The user must see a blocking or nonblocking notice when:

- the external deck changed after the selected snapshot;
- the snapshot includes unresolved cards;
- relevant metrics were generated using an older deck hash;
- simulation support is incomplete;
- the local-meta profile is stale;
- a correction has not been revalidated;
- the snapshot predates a legality change.

The user may continue with an older snapshot, but the answer must retain that snapshot identity.

---

## 6.2 Asking a question

The composer supports:

- natural-language question;
- card attachment;
- package attachment;
- deck finding attachment;
- prior answer attachment;
- simulation result attachment;
- snapshot comparison attachment.

### Composer wireframe

```text
┌────────────────────────────────────────────────────────────┐
│ Ask Jin                                                    │
│                                                            │
│ How does Ledger Shredder compare with Artist's Talent in   │
│ this exact snapshot?                                       │
│                                                            │
│ Attached: [Ledger Shredder] [Artist's Talent]               │
│                                                            │
│ Scope: [Deck + Evidence + Theory ▾]                         │
│ Snapshot: [Current RI-2026-07-22-07 ▾]                      │
│ Output: [Decision brief ▾]                                  │
│                                                            │
│                                            [Send]           │
└────────────────────────────────────────────────────────────┘
```

### Intent resolution

Jin classifies the request as one or more of:

- factual retrieval;
- rules interaction;
- card comparison;
- deck construction;
- package analysis;
- replacement discussion;
- snapshot comparison;
- simulation request;
- simulation interpretation;
- experiment design;
- theory explanation;
- tournament preparation;
- correction submission;
- prior-answer review.

Ambiguity is handled by showing the resolved interpretation before or inside the answer:

```text
INTERPRETED REQUEST

Compare the two cards as candidate inclusions in snapshot RI-2026-07-22-07,
using functional overlap, tournament evidence, current deck requirements,
simulation evidence, and applicable theory.
```

Jin should not interrupt with a clarification unless unresolved ambiguity would materially change the result.

---

## 6.3 Selecting evidence scope

### Default scope

```text
Deck snapshot
+ Canonical card and rules truth
+ Approved tournament evidence
+ Existing measured analytics
+ Applicable theory corpus
+ Applied user corrections
```

### Presets

| Preset | Included |
|---|---|
| Deck grounded | Snapshot, card truth, analytics, corrections |
| Evidence + theory | Deck grounded plus theory corpus; default |
| Evidence only | No theory interpretation or community context |
| Rules first | Oracle text, rules, rulings, legality references |
| Local meta | Deck grounded plus selected local and regional context |
| Broad research | Approved evidence, primers, theory, attributed community context |
| Snapshot comparison | Two snapshots and analyses valid for each |
| Custom | Individually selected evidence classes |

### Custom scope panel

```text
EVIDENCE SCOPE

Deck
[x] Current deck snapshot
[ ] Prior snapshot
[ ] Compare two snapshots

Authority
[x] Oracle text and legality
[x] Comprehensive Rules and rulings
[x] Commander Spellbook
[x] Functional tags

Measured evidence
[x] Tournament records
[x] Frequency and inclusion
[x] Relationships and packages
[x] Existing simulations
[ ] Regional exposure

Context
[x] Theory corpus
[x] Primers
[ ] Community discussions
[ ] Local-meta notes

Time window: [Last 6 months ▾]
Region:      [Global ▾]
Placement:   [Top 16 ▾]

[Reset to default]                                 [Apply]
```

### Scope rules

- Authority cannot be disabled when legality or rules are material.
- User corrections relevant to the selected deck are always evaluated, though the user may inspect the uncorrected result separately.
- Community material is never mislabeled as tournament evidence.
- Theory is excluded only through an explicit preset or toggle.
- Evidence scope is stored with the answer.
- Changing scope after an answer creates a new answer version.

---

# 7. Answer presentation

## 7.1 Default answer card

```text
┌──────────────────────────────────────────────────────────────┐
│ JIN ANSWER                                                   │
│ Snapshot RI-2026-07-22-07 • Generated Jul 22, 11:48 PM       │
├──────────────────────────────────────────────────────────────┤
│ CONCLUSION                                                   │
│ Ledger Shredder has the stronger floor in this snapshot...   │
│                                                              │
│ Confidence: MODERATE        Source agreement: MIXED          │
│ Legality: VERIFIED          Evidence coverage: 74%           │
│                                                              │
│ ⚠ Material contradiction                                    │
│ Tournament frequency favors X, while deck-specific role      │
│ coverage favors Y.                                           │
│                                                              │
│ WHY                                                          │
│ • Functional overlap... [1][2]                               │
│ • Pitch utility... [3]                                       │
│ • Simulation evidence... [4]                                 │
│                                                              │
│ THEORY INTERPRETATION                                        │
│ Menendian: engine inputs and conversion... [5]               │
│ Verhey: deck cohesion and overlap... [6]                     │
│                                                              │
│ TEST                                                         │
│ Compare 5,000 opening-hand simulations across both cards...  │
│                                                              │
│ [Evidence] [Contradictions] [Citations] [Method]              │
│ [Create experiment] [Submit correction] [Compare answer]     │
└──────────────────────────────────────────────────────────────┘
```

## 7.2 Confidence display

Confidence is never shown as an unexplained percentage.

The summary displays:

- label: High, Moderate, Low, Insufficient;
- evidence coverage;
- source agreement;
- sample warning;
- confidence ceiling reason.

Expanded view:

```text
CONFIDENCE: MODERATE

Positive factors
- 63 eligible tournament decks
- Current canonical card support
- Two independent measured-evidence families
- Relevant deck-specific simulation available

Limiting factors
- Only 74% of eligible decks had complete lists
- Simulation does not model opponent actions
- Relevant theory is format-translated from 60-card Magic
- Two user-local observations conflict with population evidence

Ceiling
Confidence cannot exceed Moderate until simulator support and
regional sample coverage improve.
```

## 7.3 Required answer metadata

Every substantive answer packet must retain:

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
analysis_date
```

These fields derive directly from the Jin answer-safety contract in the Constitution. fileciteturn0file0

---

# 8. Citations and source inspection

## 8.1 Inline citations

- Factual claims receive sentence-level citation markers.
- Multiple claims in one sentence must not share a citation unless the source supports all of them.
- Inferences are marked as **Inference** and cite the supporting evidence.
- User-context claims are labeled **Your observation**.
- Theory claims identify the theorist and source.
- Citation markers are keyboard focusable.

## 8.2 Citation inspector

```text
CITATION [4]

Type
Simulation evidence

Claim supported
“Candidate A increased target-turn access by 3.8 percentage points.”

Source
Simulation SIM-2026-07-22-14

Inputs
Snapshot: RI-2026-07-22-07
Games: 5,000 per variant
Target: Cast engine by turn 2
Mulligan policy: London v3
Simulator version: 0.18.2

Limitations
- Target-turn runs are independent experiments
- Opponent behavior is not modeled
- Two cards are partially supported

[Open full simulation report]
```

## 8.3 Source grouping

Sources are grouped as:

- Authority
- Measured evidence
- Simulation
- Theory
- Primer context
- Community context
- User context

The source list must not flatten them into one undifferentiated bibliography.

---

# 9. Contradiction experience

## 9.1 Contradiction banner

A material contradiction appears above detailed evidence.

```text
⚠ MIXED EVIDENCE

Tournament inclusion supports Card A.
Deck-specific simulation supports Card B.
Theory lenses disagree on whether flexibility or ceiling is more important.

[Inspect contradictions]
```

## 9.2 Contradiction panel

```text
CONTRADICTION C-204

Question
Which card better serves the current snapshot?

Position A
Card A has higher tournament inclusion.
Source type: Measured tournament evidence
Strength: Moderate
Coverage: 38 / 52 eligible decks

Position B
Card B improves simulated target access.
Source type: Controlled simulation
Strength: Moderate
Model limitation: No opponent interaction

Position C
Deck-specific correction says Card A's pitch utility is undercounted.
Source type: User correction
Scope: This deck only
Status: Applied

Conflict type
Different outcome measures

Resolution
Unresolved. The sources measure different objectives.

Effect on answer
Confidence ceiling reduced from High to Moderate.
```

## 9.3 Contradiction categories

- **Authority conflict:** blocking until resolved or clearly declared unknown.
- **Legality conflict:** illegal recommendation blocked.
- **Data conflict:** both observations retained.
- **Metric conflict:** explain differing populations or formulas.
- **Theory conflict:** preserve separate frameworks.
- **User-context conflict:** apply narrowest valid correction scope.
- **Temporal conflict:** show source dates and snapshot versions.

---

# 10. Comparing snapshots

## 10.1 Entry points

- context-header snapshot menu;
- “Compare snapshot” composer action;
- answer-history action;
- deck editor handoff;
- stale-answer warning.

## 10.2 Comparison wireframe

```text
SNAPSHOT COMPARISON

A: RI-2026-07-18-04                 B: RI-2026-07-22-07
Imported Jul 18                     Imported Jul 22
────────────────────────────────────────────────────────

Cards added
+ Ledger Shredder
+ Fellwar Stone
+ Thundering Falls

Cards removed
- Artist's Talent
- Storm-Kiln Artist
- Training Center

Affected systems
✓ Mana-source analysis
✓ Functional-role coverage
✓ Pitch-card count
✓ Simulation targets
⚠ Tournament comparison unchanged
⚠ Two prior simulations are stale

Jin summary
The new snapshot gains...

[Ask about these changes]
[Run comparison simulation]
[Create experiment from diff]
```

## 10.3 Comparison rules

- Compare exact snapshots, never mutable deck identities.
- Separate direct card diff from inferred strategic effect.
- Mark analyses that remain valid.
- Mark analyses invalidated by the change.
- Do not claim improvement merely because the newer snapshot exists.
- Show corrections applicable to each snapshot.
- Preserve legality according to each snapshot date where historical analysis requires it.

---

# 11. Launching simulations

## 11.1 Simulation launch flow

```text
Answer or composer
  -> Select simulation question
  -> Validate deck snapshot
  -> Check supported-card coverage
  -> Configure parameters
  -> Show limitations
  -> Submit job
  -> Stream status
  -> Validate results and traces
  -> Attach report to conversation
  -> Optionally rerun answer with new evidence
```

## 11.2 Simulation launcher

```text
CREATE SIMULATION

Snapshot
RI-2026-07-22-07

Question
[Cast target by turn N ▾]

Target
[Rhystic Study]

Turn
[2]

Additional condition
[x] Retain live interaction
[ ] Commander in play
[ ] Required permanent survives
[ ] Compare card substitutions

Variants
A: Current snapshot
B: Artist's Talent -> Ledger Shredder

Games
[5,000 per variant]

Seed policy
[Recorded deterministic seeds ▾]

Coverage
96 fully supported
2 partially supported

Warnings
- Opponent behavior is not modeled
- Target-turn runs are separate experiments
- Partial card support may affect retained-interaction classification

[Cancel]                                   [Launch]
```

## 11.3 Job states

```text
DRAFT
VALIDATING
BLOCKED_UNSUPPORTED
QUEUED
RUNNING
VALIDATING_RESULTS
COMPLETED
COMPLETED_WITH_WARNINGS
FAILED
CANCELLED
STALE
```

## 11.4 Simulation result card

```text
SIMULATION COMPLETE

Variant A: 41.2% ± 1.4%
Variant B: 44.9% ± 1.4%
Observed delta: +3.7 percentage points

Result status
Completed with warnings

Trace validation
4,486 successful traces
4,441 accepted
45 excluded as unsupported or illegal

Interpretation
The simulation supports improved target access under this model.
It does not establish a tournament-performance improvement.

[Inspect methods] [Inspect valid traces] [Ask Jin to interpret]
```

Jin does not write the result directly into measured evidence. It references the validated simulation record through the approved evidence boundary.

---

# 12. Creating experiments

Experiments convert discussion into a testable user-context object. They are not recommendations pretending to wear a lab coat.

## 12.1 Experiment builder

```text
CREATE EXPERIMENT

Title
Ledger Shredder versus Artist's Talent

Hypothesis
Ledger Shredder improves flexible interaction coverage without materially
reducing engine access.

Snapshot
RI-2026-07-22-07

Controlled change
- Artist's Talent
+ Ledger Shredder

Primary measure
[Target-turn engine access ▾]

Secondary measures
[x] Blue pitch-card availability
[x] Card seen by turn 3
[x] Retained interaction
[ ] Tournament placement

Method
[x] Simulation
[x] Goldfish testing notes
[ ] Tournament observation
[ ] Local-game logging

Success condition
At least +2 percentage points in target access with no reduction greater
than 1 percentage point in retained interaction.

Stop condition
5,000 valid runs per variant or unsupported-card rate above 5%.

Status
Draft

[Save draft] [Queue simulation]
```

## 12.2 Experiment lifecycle

```text
DRAFT
  -> READY
  -> RUNNING
  -> PARTIALLY_COMPLETE
  -> COMPLETE
  -> INTERPRETED
  -> ACCEPTED
  -> REJECTED
  -> SUPERSEDED
  -> ABANDONED
```

## 12.3 Experiment boundaries

Experiments may write:

- user hypotheses;
- testing notes;
- simulation requests;
- expected outcomes;
- observed outcomes;
- interpretation;
- final user judgment.

Experiments may not:

- overwrite canonical evidence;
- alter global card metrics;
- mark a card universally better;
- silently update a deck;
- become persisted recommendations without Decision Intelligence.

---

# 13. Submitting corrections

## 13.1 Entry points

- answer action: **Submit correction**
- citation action: **Source does not support this**
- simulation trace: **Trace is illegal**
- contradiction panel: **Add user evidence**
- deck context: **Correct deck-specific assumption**
- prior answer: **This conclusion was wrong**

## 13.2 Correction form

```text
SUBMIT CORRECTION

Claim being corrected
“Springleaf Drum can repeatedly produce mana when Valley Floodcaller untaps.”

Corrected claim
Springleaf Drum remains tapped because the mana ability belongs to the Drum.
Untapping Valley Floodcaller does not untap the Drum.

Category
[Rules / interaction correction ▾]

Scope
[Global interaction rule ▾]

Affected systems
[x] Jin reasoning
[x] Simulator validation
[x] Rules explanation
[x] Regression tests
[ ] Tournament analytics

Supporting basis
[Oracle text and rules explanation...]

Evidence
[Attach source] [Attach trace] [Attach prior answer]

Effective date
[Immediately after validation ▾]

Exceptions
[None]

[Save candidate]
```

## 13.3 Correction states

```text
CANDIDATE
UNDER_REVIEW
NEEDS_EVIDENCE
VALIDATED
APPLIED
APPLIED_WITH_EXCEPTIONS
REJECTED
SUPERSEDED
REVALIDATION_REQUIRED
```

## 13.4 Correction application rules

- Apply at the narrowest valid scope.
- Deck-specific principles remain deck-specific.
- Simulator legality corrections may apply simulator-wide.
- UI preferences do not alter evidence.
- User corrections may override prior Jin reasoning.
- User corrections cannot override Oracle text, official rules, or canonical identity without authoritative support.
- Existing answers remain historically intact and display that a later correction superseded part of them.
- Revalidation triggers identify affected answers, simulations, experiments, and tests.

---

# 14. Revisiting prior answers

## 14.1 Conversation-history card

```text
LEDGER SHREDDER VS ARTIST'S TALENT
Jul 22, 2026 • Rograkh/Ishai snapshot RI-2026-07-22-07

Status
Superseded by newer evidence

Original confidence
Moderate

Changes since answer
- Deck snapshot changed
- One correction applied
- Tournament population increased from 52 to 63 decks
- New simulation available

[Open original] [Compare with current evidence]
```

## 14.2 Revisit modes

### Open original

Displays the exact saved answer and evidence packet.

### Re-evaluate

Runs a new answer using:

- current deck snapshot or selected historical snapshot;
- current evidence;
- current corrections;
- current analysis profile.

### Compare answers

```text
ANSWER COMPARISON

Original: Jul 18                     Current: Jul 22
Snapshot RI-07-18-04                 Snapshot RI-07-22-07

Conclusion
Card A preferred                    Card B preferred

Why it changed
- Functional-role correction applied
- New simulation contradicted earlier assumption
- Deck removed a separate blue pitch card

Confidence
Low                                 Moderate

Unchanged
- Rules status
- Tournament population definition
- Theory disagreement
```

### Fork discussion

Creates a new conversation branch while preserving the original context.

## 14.3 Staleness rules

An answer becomes potentially stale when:

- deck snapshot changes;
- source population changes materially;
- a cited source is removed or corrected;
- a correction becomes applicable;
- simulator version changes;
- ontology or tag version changes;
- legality changes;
- analysis profile changes.

Stale does not mean false. It means the original conclusion may no longer apply to current conditions.

---

# 15. State-transition model

## 15.1 Conversation state

```text
NO_CONTEXT
  -> RESOLVING_CONTEXT
  -> CONTEXT_READY
  -> QUESTION_DRAFT
  -> PLANNING
  -> RETRIEVING
  -> VALIDATING_AUTHORITY
  -> BUILDING_EVIDENCE
  -> SCANNING_CONTRADICTIONS
  -> BUILDING_ANSWER
  -> ANSWER_READY
```

Alternative terminal and degraded states:

```text
CONTEXT_ERROR
PARTIAL_CONTEXT
RETRIEVAL_DEGRADED
AUTHORITY_UNKNOWN
EVIDENCE_INSUFFICIENT
ANSWER_BLOCKED
MODEL_UNAVAILABLE
ANSWER_READY_WITH_WARNINGS
```

## 15.2 Answer lifecycle

```text
GENERATING
  -> VALIDATING
  -> READY
  -> SAVED
  -> STALE
  -> SUPERSEDED
  -> CORRECTED
  -> ARCHIVED
```

## 15.3 Simulation lifecycle

```text
CONFIGURING
  -> VALIDATING_REQUEST
  -> QUEUED
  -> RUNNING
  -> VALIDATING_TRACES
  -> COMPLETE
  -> ATTACHED_TO_ANSWER
```

Failure branches:

```text
BLOCKED_UNSUPPORTED
FAILED_ENGINE
FAILED_VALIDATION
CANCELLED
STALE_RESULT
```

## 15.4 Correction lifecycle

```text
DRAFT
  -> CANDIDATE
  -> REVIEW
  -> VALIDATED
  -> APPLIED
  -> REVALIDATION
  -> ACTIVE
  -> SUPERSEDED
```

---

# 16. User stories

## Deck pilot

**As a deck pilot**, I can open Jin from the active deck and immediately see which immutable snapshot is being discussed, so conclusions cannot drift across deck revisions.

**As a deck pilot**, I can ask whether a card belongs in this particular list and receive deck-specific reasoning rather than generic format popularity.

**As a deck pilot**, I can turn a comparison into a structured experiment without manually copying the relevant cards, snapshot, and hypothesis.

## Evidence reviewer

**As an evidence reviewer**, I can inspect every factual claim’s source type, population, date, coverage, and caveats.

**As an evidence reviewer**, I can distinguish tournament evidence, simulation evidence, theory, primer claims, community discussion, and user observations.

**As an evidence reviewer**, I can see why confidence was limited and which missing evidence would alter the ceiling.

## Theory learner

**As a theory learner**, I can see applicable frameworks separately rather than receiving an invented composite opinion.

**As a theory learner**, I can inspect disagreements between lenses and identify whether the disagreement is definitional, contextual, empirical, format-specific, or unresolved.

## Simulator user

**As a simulator user**, I can launch a supported test from an answer, inspect assumptions before execution, and see invalid traces excluded.

**As a simulator user**, I am warned that target-turn runs may be separate experiments and are not automatically cumulative.

## Correction submitter

**As a correction submitter**, I can select the exact claim that failed, assign the narrowest scope, attach evidence, and see which systems require revalidation.

**As a correction submitter**, I can confirm that a deck-specific principle was not incorrectly promoted into global strategy.

## Historical reviewer

**As a historical reviewer**, I can reopen an original answer exactly as generated and compare it against a newer answer without losing the old evidence packet.

---

# 17. UI requirements versus backend implementation

| Requirement | UI responsibility | Backend responsibility |
|---|---|---|
| Deck context | Display selected immutable snapshot and freshness | Resolve deck identity, snapshot, hash, source status |
| Evidence scope | Present presets and custom controls | Validate scope and build retrieval plan |
| Question interpretation | Display resolved intent | Perform intent resolution and query planning |
| Citations | Render markers and source inspector | Return claim-to-source mappings and provenance |
| Confidence | Show label, ceiling, factors, coverage | Calculate confidence inputs through governed services |
| Contradictions | Display grouped conflicts | Detect, classify, and preserve contradictions |
| Recommendations | Display approved conclusion | Route persisted conclusions through Decision Intelligence |
| Theory | Separate framework analyses | Retrieve claims, apply routing, preserve attribution |
| Rules | Show verified, disputed, or unknown status | Validate Oracle text, rules, rulings, legality |
| Snapshot comparison | Render card and analysis diffs | Compute canonical snapshot diff and invalidation map |
| Simulations | Configure and monitor jobs | Validate, execute, store, and verify simulation results |
| Experiments | Collect hypothesis and criteria | Persist user-context experiment records |
| Corrections | Collect structured correction candidate | Store ledger entry, validate scope, trigger revalidation |
| Answer history | Display original and comparison views | Persist immutable answer packets and supersession links |
| Error handling | Explain actionable failure | Return typed errors and safe degraded states |

The UI must not:

- calculate metrics;
- infer legality;
- generate confidence;
- resolve source conflicts;
- create recommendations;
- alter correction scope;
- determine whether a trace is valid;
- decide that an old answer is superseded.

Those are backend decisions. Otherwise a React component eventually becomes the unofficial rules engine because a developer needed a quick boolean, and civilization declines another millimeter.

---

# 18. Backend modules required

## Context and identity

- `DeckContextResolver`
- `DeckSnapshotRepository`
- `SnapshotFreshnessService`
- `DeckDiffService`
- `CardSupportResolver`

## Jin orchestration

- `IntentResolver`
- `QueryPlanner`
- `EvidenceScopeValidator`
- `EvidenceRetriever`
- `TheoryRetriever`
- `RulesValidator`
- `EvidenceGate`
- `ContradictionScanner`
- `AnswerBuilder`
- `AnswerAuditor`
- `ConversationRepository`

## Evidence and provenance

- `UnifiedEvidenceService`
- `CitationResolver`
- `SourceLineageRepository`
- `ConfidenceExplanationService`

## Decision boundary

- `DecisionIntelligenceService`
- `RecommendationRepository`
- `AnalysisProfileRepository`

## Simulation and experiments

- `SimulationRequestValidator`
- `SimulationOrchestrator`
- `TraceValidationService`
- `SimulationRepository`
- `ExperimentRepository`

## Corrections

- `CorrectionLedgerRepository`
- `CorrectionScopeResolver`
- `CorrectionApplicationService`
- `CorrectionRevalidationPlanner`

No UI implementation should bypass these services by reading provider payloads or database tables directly.

---

# 19. Error handling

| Failure | UI behavior | Allowed continuation |
|---|---|---|
| Deck source unavailable | Use cached snapshot; mark source check failed | Yes |
| Deck changed externally | Show diff and require snapshot selection | Yes |
| Snapshot missing | Block deck-specific answer | No |
| Card unresolved | Identify unresolved card; exclude dependent claims | Partial |
| Canonical authority unavailable | Mark legality unknown; block rules-dependent conclusion | Partial or no |
| Tournament retrieval fails | Answer from remaining evidence with reduced coverage | Yes |
| Theory retrieval fails | Answer without theory; disclose omission | Yes |
| Community source fails | Omit community context | Yes |
| Contradiction scan fails | Do not label answer fully validated | Partial |
| Model unavailable | Preserve draft and retrieval packet | No generated answer |
| Simulation has unsupported cards | Show impact; block or permit with warning by policy | Conditional |
| Simulation trace invalid | Exclude trace and recalculate affected totals | Yes |
| Correction conflicts with authority | Reject application; preserve candidate and explanation | No application |
| Correction conflicts with correction | Show both, require scope or supersession resolution | No automatic application |
| Historical source removed | Preserve citation metadata; mark source unavailable | Yes |
| Database write fails | Do not claim answer, experiment, or correction was saved | Read-only continuation |

Error messages must contain:

- what failed;
- what remains usable;
- whether the answer is incomplete;
- which confidence fields changed;
- whether any data was saved;
- a stable error identifier for logs.

---

# 20. Loading and empty states

## Empty Jin home

```text
NO DECK CONTEXT

Select a saved deck, import a deck, or open Jin from the deck workspace.

Recent discussions without active context remain available below.
```

## Context loading

```text
Preparing deck context

✓ Resolved commander identity
✓ Loaded snapshot
✓ Applied corrections
• Checking source freshness
• Loading available evidence
```

## Answer generation

```text
Building answer

✓ Interpreted question
✓ Retrieved authority sources
✓ Retrieved measured evidence
✓ Retrieved theory claims
• Checking contradictions
• Validating legality
• Building citations
```

The loading display reflects real backend states. It must not show fictional progress percentages.

## Insufficient evidence

```text
INSUFFICIENT EVIDENCE

Jin cannot support a deck-specific conclusion.

Available:
- Canonical card text
- Two applicable theory claims

Missing:
- Valid deck snapshot
- Eligible tournament population
- Supported simulation data

No recommendation was produced.
```

---

# 21. Accessibility requirements

## Standards

- WCAG 2.2 AA target.
- Full keyboard operation.
- Logical heading hierarchy.
- Visible focus indicators.
- Screen-reader labels for every icon-only control.
- No color-only confidence or conflict indicators.
- Minimum 4.5:1 text contrast.
- Minimum 3:1 contrast for large text and interface boundaries.
- Respect reduced-motion settings.
- Zoom to 200% without loss of content or function.
- Content reflow at 320 CSS pixels for read-only views.

## Chat-specific requirements

- New answers announced through a polite live region.
- Streaming text must not repeatedly steal screen-reader focus.
- Generation status is available as text.
- Citation markers include source type in accessible names.
- Collapsed sections announce expanded or collapsed state.
- Contradictions appear in reading order before supporting detail.
- Confidence labels include text, not only icons or meters.
- Data visualizations have equivalent numeric tables.
- Source previews do not trap keyboard focus.
- Escape closes drawers and dialogs.
- Focus returns to the initiating control after dialog closure.

## Simulation accessibility

- Progress states are textual.
- Result charts include tables.
- Margin of error is announced with the estimate.
- Invalid traces are distinguished by label and explanation.
- Large trace logs use virtualized rendering without breaking screen-reader navigation.

---

# 22. Component-level acceptance criteria

## 22.1 `DeckContextHeader`

**UI criteria**

- Displays commander signature, snapshot date, freshness, and analysis profile.
- Shows stale or changed status without relying on color.
- Opens snapshot selector by keyboard.
- Never truncates the snapshot identity beyond recoverability.

**Backend dependency**

- Receives a resolved immutable `DeckContextPacket`.
- Does not infer freshness locally.

**Acceptance**

- Changing snapshot starts a new context transition.
- Existing answers retain their original snapshot.
- Failure to check the source displays `Freshness unknown`.

---

## 22.2 `ConversationRail`

**UI criteria**

- Groups conversations by date and deck.
- Displays stale, corrected, superseded, or active state.
- Supports keyboard navigation and search.
- Does not expose internal database identifiers.

**Acceptance**

- Opening a historical conversation restores its original context.
- Forking creates a linked new conversation.
- Deleted or unavailable evidence does not remove the historical answer.

---

## 22.3 `EvidenceScopePicker`

**UI criteria**

- Provides named presets and custom mode.
- Explains what each scope includes.
- Shows forced authority sources when legally required.
- Warns when community or local-meta context is selected.

**Acceptance**

- Scope is serialized with the question.
- Reopening an answer restores the exact scope.
- Scope changes create a new answer version.
- UI cannot disable required legality validation.

---

## 22.4 `QuestionComposer`

**UI criteria**

- Accepts natural language and structured attachments.
- Shows selected snapshot and scope.
- Supports card, package, answer, simulation, and snapshot attachments.
- Preserves draft text after recoverable failures.

**Acceptance**

- Sending creates one immutable question record.
- Duplicate submission is prevented.
- Attachments retain canonical identities.
- Unresolved cards are flagged before generation.

---

## 22.5 `AnswerCard`

**UI criteria**

- Presents direct answer first.
- Displays confidence, agreement, legality, coverage, and snapshot.
- Separates evidence, theory, inference, and user context.
- Exposes contradictions before secondary detail.

**Acceptance**

- No substantive factual claim lacks a citation or explicit inference label.
- No persisted recommendation bypasses Decision Intelligence.
- Unsupported claims removed by the evidence gate are not rendered.
- Illegal suggestions are blocked and reported.

---

## 22.6 `ConfidencePanel`

**UI criteria**

- Shows label, evidence factors, limiting factors, and ceiling.
- Includes sample size and coverage where applicable.
- Avoids unexplained composite percentages.

**Acceptance**

- Displayed confidence matches the answer packet.
- A lower evidence ceiling cannot be visually overridden.
- Missing confidence inputs produce `Insufficient`, not a guessed value.

---

## 22.7 `CitationMarker` and `CitationInspector`

**UI criteria**

- Keyboard focusable.
- Provides source type, title, date, supported claim, and limitations.
- Opens without navigating away from the answer.
- Indicates unavailable or archived sources.

**Acceptance**

- Citation resolves to the exact supporting record.
- Source class is always visible.
- Citation does not imply authority beyond the source’s approved role.
- User-context citations are clearly distinguished from external evidence.

---

## 22.8 `ContradictionPanel`

**UI criteria**

- Groups positions rather than blending them.
- Displays conflict type, source class, strength, and consequence.
- Shows resolution status and effect on confidence.

**Acceptance**

- Material contradictory evidence cannot be collapsed by default without a visible warning.
- Authority conflicts are treated differently from theory disagreements.
- Unresolved contradictions remain unresolved across answer reloads.

---

## 22.9 `SnapshotComparePanel`

**UI criteria**

- Shows added, removed, and unchanged cards.
- Shows affected and unaffected analyses.
- Marks stale simulations and recommendations.
- Provides a text summary and full diff.

**Acceptance**

- Comparison uses immutable snapshots.
- Sideboard and auxiliary zones remain separate.
- Strategic effects are labeled as inference unless measured.
- Historical legality uses the appropriate snapshot date.

---

## 22.10 `SimulationLauncher`

**UI criteria**

- Displays target, turn, conditions, games, seed policy, and support coverage.
- Shows model limitations before launch.
- Prevents impossible or unsupported configuration where policy requires.

**Acceptance**

- Request includes deck hash and simulator version.
- Duplicate jobs are detected.
- Unsupported relevant cards are disclosed.
- Target-turn semantics are explicit.
- No job is labeled complete before result validation.

---

## 22.11 `SimulationJobCard`

**UI criteria**

- Displays current state and elapsed time.
- Provides cancel action where supported.
- Shows result warnings, excluded traces, and margin of error.
- Links to the full report.

**Acceptance**

- Invalid traces are excluded from accepted totals.
- Failed validation cannot produce a success card.
- Result attaches to the correct deck snapshot.
- Stale results remain viewable but visibly stale.

---

## 22.12 `ExperimentBuilder`

**UI criteria**

- Captures hypothesis, controlled change, measures, success criteria, and stop criteria.
- Prefills from the answer or snapshot comparison.
- Separates simulation measures from real-game observations.

**Acceptance**

- Experiment writes only to user-context storage.
- Deck changes are not applied automatically.
- Results do not become global evidence.
- Accepted or rejected conclusions retain their evidentiary basis.

---

## 22.13 `CorrectionDialog`

**UI criteria**

- Prefills original claim and answer reference.
- Requires category and scope.
- Supports evidence, exceptions, and affected systems.
- Warns when the correction conflicts with authority.

**Acceptance**

- Correction is stored as a candidate before application.
- Scope is never broadened automatically.
- Application generates an audit record.
- Superseded answers remain historically accessible.
- Revalidation targets are listed before activation.

---

## 22.14 `AnswerHistoryPanel`

**UI criteria**

- Shows original generation date, snapshot, evidence version, and status.
- Supports original view, re-evaluation, comparison, and fork.
- Explains why an answer became stale or superseded.

**Acceptance**

- Re-evaluation creates a separate answer.
- Original answer content is immutable.
- Comparison identifies changed evidence, corrections, context, and conclusions.
- Missing historical resources are marked rather than silently replaced.

---

# 23. System-level acceptance criteria

The Jin chat experience is acceptable when all of the following hold:

1. Every deck-specific answer is bound to an immutable snapshot.
2. Every substantive factual claim is cited or labeled as inference.
3. Evidence classes remain visually and structurally distinct.
4. Theory is applied by topic relevance, not author fame.
5. Theory disagreement remains visible.
6. User corrections apply at the narrowest valid scope.
7. Jin cannot mutate canonical evidence or measured metrics.
8. Persisted recommendations pass through Decision Intelligence.
9. Simulation requests expose support limits before execution.
10. Invalid simulation traces cannot contribute to accepted results.
11. Historical answers remain reproducible and immutable.
12. Re-evaluation creates a linked new answer.
13. Confidence displays its limiting factors and ceiling.
14. Authority conflicts can block an answer.
15. Partial retrieval produces a visibly degraded answer rather than fabricated completeness.
16. All primary operations are keyboard accessible.
17. Read-only mobile layouts preserve citations, uncertainty, and contradictions.
18. UI components consume typed backend state and do not independently reproduce business logic.
19. Every write operation clearly identifies whether it affects user context, an experiment, a correction candidate, or a governed recommendation.
20. No chat response can silently become canonical truth.
> [!IMPORTANT]
> Repository intake note: This is a preserved pre-ratification design
> proposal. `docs/CODIE_V2_CONSTITUTION.md` is now ratified and is the
> governing authority. Statements below that call V2 a non-authoritative
> comparison draft are historical. This proposal does not authorize
> implementation.
