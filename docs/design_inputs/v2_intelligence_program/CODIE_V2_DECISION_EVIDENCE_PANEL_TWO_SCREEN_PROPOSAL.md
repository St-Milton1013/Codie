



# Codie V2 Decision Evidence Panel and Two-Screen Workflow

## 1. Design status and governing boundaries

This specification is derived from the Codie Constitution V2 comparison draft. That document is explicitly non-authoritative until ratified, so this design is implementation-ready as a proposed contract but does not authorize implementation by itself. Humanity has apparently discovered constitutional law for deck analytics, which is excessive but preferable to letting a chat box invent database writes. fileciteturn0file0

The design preserves these boundaries:

1. **Decision Intelligence owns conclusions.**
   The interface displays recommendation objects. It does not calculate, rewrite, strengthen, or independently generate them.

2. **Evidence Fusion owns evidence packets.**
   The panel consumes Unified Evidence. It does not query providers, rerun metrics, resolve conflicts, or execute simulations.

3. **Jin discusses conclusions but does not become a second recommender.**
   Jin may interpret, challenge, compare, and propose experiments. Persisted recommendation changes must return through Decision Intelligence.

4. **Every displayed conclusion is bound to an immutable deck snapshot.**

5. **Desktop is the execution environment.**

6. **Mobile execution is deferred.**
   Future mobile delivery is read-only and outside the immediate implementation scope.

7. **The interface must expose uncertainty without forcing every user to read an evidentiary autopsy before seeing the conclusion.**

---

# 2. Product structure

Codie has two primary workspaces:

```text
SCREEN 1: DECK WORKSPACE
Deck contents, snapshot identity, staged changes, role coverage, and analysis controls.

SCREEN 2: ANALYSIS WORKSPACE
Attention queue, Decision Evidence Panel, experiments, reports, and Jin discussion.
```

The preferred arrangement uses two desktop displays, but the architecture must not require two monitors.

```text
Dual-display mode:
Display A = Deck Workspace
Display B = Analysis Workspace

Single-display fallback:
Top-level workspace switcher
[Deck] [Analysis]
```

“Two-screen” is therefore an information-architecture contract, not a hardware dependency.

## 2.1 Shared session state

Both workspaces share only stable identifiers and UI selection state:

```text
activeDeckId
activeDeckSnapshotId
activeAnalysisRunId
activeDecisionId
activeCardId
activeExperimentId
activeJinThreadId
analysisProfileId
weightProfileId
comparisonSnapshotId
```

They do not share mutable evidence objects through ad hoc component state.

Cross-screen synchronization occurs through a typed local event bus or centralized application store:

```text
CARD_SELECTED
DECISION_SELECTED
SNAPSHOT_SELECTED
STAGED_CHANGE_UPDATED
ANALYSIS_RUN_SELECTED
JIN_EVIDENCE_LINK_SELECTED
EXPERIMENT_SELECTED
```

---

# 3. Information hierarchy

Codie should not begin with a dashboard containing eighteen gauges, six gradients, and a pie chart explaining that blue cards are blue.

The hierarchy is:

```text
Level 0: Attention Queue
What deserves attention?

Level 1: Decision Summary
What is Codie concluding?

Level 2: Decision Evidence Panel
Why is Codie concluding it?

Level 3: Evidence Detail
What metrics, simulations, sources, and assumptions contributed?

Level 4: Provenance and Reproducibility
Exactly where did the evidence come from and how can it be replayed?
```

## 3.1 Default visibility

| Information | Default state |
|---|---|
| Conclusion | Visible |
| Proposed action or experiment | Visible |
| Confidence label | Visible |
| Source-agreement label | Visible |
| Deck snapshot | Visible |
| Primary reason | Visible |
| Major warning | Visible |
| Replacement tradeoffs | Collapsed summary |
| Evidence contributions | Collapsed |
| Simulation details | Collapsed unless decisive |
| Conflicts | Expanded when material |
| Caveats | Expanded when confidence-limiting |
| Raw formulas | Collapsed |
| Source records | Collapsed |
| Reproducibility metadata | Collapsed |
| Jin theory lenses | Separate discussion surface |

A material conflict must never be hidden merely because the user has not expanded the provenance drawer.

---

# 4. Screen 1: Deck Workspace

## 4.1 Responsibilities

The Deck Workspace handles:

- deck import or selection;
- canonical commander and card display;
- snapshot identity;
- mainboard and zone separation;
- local edits;
- locked and ignored cards;
- role and package labels;
- unsupported-card warnings;
- staged replacement experiments;
- snapshot comparison;
- analysis launch and status.

It is not intended to replace Moxfield or Archidekt. Its job is to supply a controlled analytical deck state, not provide animated sleeves and seventeen social reactions.

## 4.2 Desktop wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ CODIE   Deck Workspace                                                       │
│ Rograkh / Ishai     Snapshot: 2026-07-22 23:41     Hash: 8A4F…C91           │
│ Source: Moxfield    Source status: Changed since prior snapshot              │
│ [Compare snapshots] [Refresh source] [Analyze]                               │
├──────────────────────────────────────────────────────────────────────────────┤
│ COMMANDERS                 │ DECK STATUS                                      │
│ Rograkh, Son of Rohgahh    │ 98/98 mainboard                                  │
│ Ishai, Ojutai Dragonspeaker│ 0 unresolved cards                              │
│                            │ 3 partially supported simulator cards            │
│                            │ Analysis: stale after 2 staged changes            │
├────────────────────────────┴─────────────────────────────────────────────────┤
│ FILTERS: [All] [Mana] [Interaction] [Engines] [Packages] [Unsupported]       │
│ SEARCH: [_____________________________________________]                       │
├───────────────────────────────────────────────────────┬──────────────────────┤
│ DECK LIST                                             │ INSPECTOR            │
│                                                       │                      │
│ Mana                                                  │ Selected card        │
│  Ancient Tomb                                         │ Ledger Shredder      │
│  Arcane Signet                                        │                      │
│  ...                                                  │ Roles                │
│                                                       │ • selection          │
│ Interaction                                           │ • pitch utility      │
│  An Offer You Can't Refuse                            │ • creature body      │
│  Force of Will                                        │                      │
│  ...                                                  │ Package links        │
│                                                       │ • draw engine        │
│ Engines                                               │ • blue pitch density │
│  Mystic Remora                                        │                      │
│  Rhystic Study                                        │ [Open evidence]      │
│                                                       │ [Lock card]          │
│                                                       │ [Ignore suggestion]  │
├───────────────────────────────────────────────────────┴──────────────────────┤
│ STAGED CHANGES                                                               │
│ − Card A    + Card B    Reason: test replacement recommendation DEC-204      │
│ Estimated analysis impact: mana, pitch density, simulator target             │
│ [Discard staged changes] [Create candidate snapshot]                          │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 4.3 Deck editing rules

A recommendation must never directly alter the active snapshot.

The replacement flow is:

```text
Decision selected
    ->
User chooses “Stage replacement”
    ->
Local staged-change record created
    ->
Original snapshot remains immutable
    ->
Candidate snapshot generated
    ->
Affected analyses rerun against candidate snapshot
    ->
Original and candidate results compared
    ->
User may save candidate as a new snapshot
```

There is no “Apply recommendation everywhere” control. Civilization is not ready.

## 4.4 Snapshot bar

The snapshot bar must always expose:

- deck name;
- commander signature;
- snapshot timestamp;
- source identity;
- deck hash abbreviation;
- analysis freshness;
- staged-change count;
- comparison state.

Snapshot status values:

```text
CURRENT
SOURCE_CHANGED
LOCAL_CHANGES_STAGED
ANALYSIS_STALE
PARTIAL_SUPPORT
HISTORICAL
CANDIDATE
```

The snapshot ID must remain visible in every report and Jin answer packet.

---

# 5. Screen 2: Analysis Workspace

## 5.1 Responsibilities

The Analysis Workspace handles:

- attention-ranked findings;
- Decision Evidence Panel;
- deck-health findings;
- replacement comparisons;
- simulation summaries;
- snapshot comparisons;
- conflict inspection;
- experiment queue;
- Jin discussion;
- export and provenance access.

## 5.2 Desktop wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ CODIE   Analysis Workspace                                                   │
│ Deck: Rograkh / Ishai   Snapshot: 8A4F…C91   Profile: Competitive Default    │
│ Analysis run: 2026-07-23 00:34   Status: Complete with 2 caveats             │
│ [Snapshot comparison] [Reports] [Export]                                     │
├───────────────────────┬──────────────────────────────────┬───────────────────┤
│ ATTENTION QUEUE       │ DECISION EVIDENCE PANEL          │ JIN-GITAXIAS      │
│                       │                                  │                   │
│ 1 High                │ Recommendation DEC-204           │ Thread bound to:  │
│ Missing conversion    │                                  │ DEC-204           │
│ outlet                │ Replace Card A with Card B       │ Snapshot 8A4F…C91 │
│                       │                                  │                   │
│ 2 Medium              │ Confidence: MODERATE             │ [Ask about this   │
│ Narrow protection     │ Source agreement: MIXED          │ decision]         │
│ slot                  │ Legality: VALIDATED              │                   │
│                       │ Snapshot: 8A4F…C91                │ Jin summary       │
│ 3 Medium              │                                  │ The candidate has │
│ Simulation coverage   │ Primary reason                   │ stronger overlap  │
│ incomplete            │ Card B covers the selected role  │ under the chosen  │
│                       │ while preserving two secondary   │ profile, but the  │
│ [All findings]        │ functions.                       │ simulation result │
│ [Conflicts only]      │                                  │ is model-limited. │
│ [Low confidence]      │ Expected tradeoff                │                   │
│                       │ Lose narrow matchup utility.      │ Evidence links    │
│                       │                                  │ • Inclusion data  │
│                       │ [Stage replacement]               │ • Simulation      │
│                       │ [Create experiment]               │ • Theory lenses   │
│                       │                                  │                   │
│                       │ ▼ Replacement logic              │ [Open full thread]│
│                       │ ▼ Evidence contributions          │                   │
│                       │ ▼ Simulation result               │                   │
│                       │ ▼ Conflicts and caveats           │                   │
│                       │ ▸ Sources and reproducibility     │                   │
└───────────────────────┴──────────────────────────────────┴───────────────────┘
```

## 5.3 Resizable regions

Desktop layout:

```text
Attention Queue:       240–320 px
Decision Panel:        flexible, minimum 600 px
Jin Dock:              320–480 px
```

At narrower desktop widths:

1. Jin collapses into a right-side drawer.
2. Attention Queue collapses into a selectable list above the panel.
3. The Decision Evidence Panel remains the central surface.
4. No substantive evidence is removed.

---

# 6. Attention Queue

## 6.1 Purpose

The queue answers only:

```text
What deserves attention now?
```

It does not attempt to summarize every metric Codie has calculated.

## 6.2 Finding categories

```text
RECOMMENDATION
REPLACEMENT
DECK_HEALTH
LEGALITY
SIMULATION_WARNING
SOURCE_CONFLICT
UNSUPPORTED_CARD
MISSING_PACKAGE
MISSING_CONVERSION
SNAPSHOT_CHANGE
EXPERIMENT_RESULT
```

## 6.3 Ranking inputs

Queue order may consume already-produced priority metadata from Decision Intelligence, but the UI must not invent its own strategic ranking.

Allowed presentation sorting:

1. blocking legality or invalid evidence;
2. high-impact decisions;
3. confidence-limiting conflicts;
4. stale snapshot or analysis status;
5. deck-health concerns;
6. optional experiments;
7. informational findings.

## 6.4 Queue limits

Default view:

- maximum five open findings;
- one line of explanation each;
- severity;
- confidence;
- conflict marker;
- affected card or package;
- snapshot scope.

Additional findings live under **All findings**.

Low-value confirmations, such as “Sol Ring is commonly played,” remain suppressed unless directly relevant to a decision.

---

# 7. Decision Evidence Panel

## 7.1 Core purpose

The panel is the single explanation surface where these converge:

- recommendation conclusion;
- confidence;
- source agreement;
- legality;
- replacement logic;
- evidence contributions;
- simulation results;
- conflicts;
- caveats;
- snapshot identity;
- Jin discussion links;
- experiment creation;
- provenance.

This directly implements the constitution’s requirement that these elements converge in one expandable surface. fileciteturn0file0

The panel displays one decision object at a time. It must not combine unrelated findings into one synthetic score.

## 7.2 Panel anatomy

### A. Identity header

Always visible:

```text
Decision ID
Decision type
Subject card/package/deck
Deck snapshot
Analysis run
Analysis profile
Weight profile
Generated timestamp
Decision status
```

### B. Conclusion block

Always visible:

```text
Observed concern
Conclusion
Candidate action
Expected impact
Primary tradeoff
```

Preferred wording:

```text
Observed concern:
The deck has weak conversion for the measured excess-mana package.

Conclusion:
The package has insufficient present conversion support under this snapshot.

Candidate action:
Test removal of Package X or add a verified outlet.

Expected impact:
Reduce unsupported package cost or improve resource conversion.

Tradeoff:
Removing it loses its secondary tempo use.
```

Forbidden wording:

```text
This is the correct card.
This card is objectively bad.
The deck must make this change.
```

### C. Confidence block

Always visible:

```text
Confidence: Moderate
Confidence ceiling: Moderate
Primary limit: simulator coverage incomplete
```

Confidence and source agreement must remain separate.

```text
Confidence = reliability of this conclusion under its declared model.
Agreement  = concurrence among eligible sources.
```

Strong agreement does not imply high confidence when sample size is weak. High confidence does not require broad agreement when a higher-authority source resolves the matter.

Numeric confidence should remain hidden unless:

- the confidence model is calibrated;
- its scale is documented;
- the number has an interpretable meaning;
- the user opens methodological detail.

A decorative “82% confident” label based on arbitrary internal weighting would be numerology wearing a badge.

### D. Source-agreement block

Values:

```text
STRONG
MIXED
WEAK
INSUFFICIENT
NOT_APPLICABLE
```

Expanded content:

- eligible source count;
- agreeing source count;
- disagreeing source count;
- authority differences;
- whether conflicts are empirical, definitional, contextual, or temporal.

Class 0 authority is not counted as one vote among community sources.

### E. Legality status

Values:

```text
VALIDATED
VALIDATED_WITH_ASSUMPTIONS
UNRESOLVED
INVALID
NOT_APPLICABLE
```

An invalid recommendation cannot expose a staging action.

### F. Replacement logic

The default summary shows:

```text
What is removed
What is added
Primary role preserved or gained
Primary role lost
Secondary overlaps
Package effects
Mana effects
Pitch or cost utility
Matchup effects
```

Expanded matrix:

| Dimension | Current card | Candidate | Net effect |
|---|---|---|---|
| Primary role | Interaction | Interaction | Preserved |
| Secondary role | Narrow hate | Card selection | Changed |
| Pitch utility | No | Blue | Gained |
| Package support | None | Draw package | Gained |
| Mana requirement | 2 | 2 | Neutral |
| Permanent type | Artifact | Creature | Changed |
| Simulator support | Full | Partial | Confidence penalty |

Replacement logic must include secondary function, not merely matching one Tagger label.

### G. Evidence contributions

Each contribution displays:

- evidence category;
- raw observation;
- normalization method;
- selected profile weight;
- signed contribution;
- sample size;
- coverage;
- confidence;
- provenance link.

Example:

```text
Tournament inclusion
Raw result: 34 of 46 eligible decks
Coverage: 46 of 52 known decks
Profile weight: 0.25
Contribution: Supports candidate

Functional overlap
Raw result: 3 preserved roles, 2 gained, 1 lost
Profile weight: 0.20
Contribution: Supports candidate

Simulation
Raw result: +3.8 percentage points
MoE: ±2.1 points
Profile weight: 0.20
Contribution: Weak support

Regional exposure
Raw result: Relevant effect seen in 6 of 18 local decks
Profile weight: 0.15
Contribution: Mixed

User context
Raw result: Current card locked for matchup testing
Profile weight: profile-controlled
Contribution: Opposes replacement
```

The panel must clearly distinguish:

```text
Evidence value: what was measured.
Evidence weight: how the chosen profile values that category.
Decision contribution: how the weighted item affected this decision.
```

Changing a weight profile changes the conclusion model, not the underlying evidence.

### H. Simulation result

Summary:

```text
Experiment:
Target:
Baseline snapshot:
Candidate snapshot:
Games:
Baseline rate:
Candidate rate:
Difference:
Margin of error:
Supported-card coverage:
Trace validity:
Warnings:
```

The display must not imply cumulative “by turn N” behavior unless the simulator contract guarantees it.

Example:

```text
Target: Cast engine on target turn 2
Baseline: 41.2%
Candidate: 45.0%
Difference: +3.8 percentage points
Games: 20,000 per variant
MoE: ±2.1 points
Interpretation: weak directional support
Warning: one relevant candidate card is partially modeled
```

A simulation result cannot be compressed into “Candidate is 3.8% better.” It is better only for the declared target under the declared model.

### I. Conflicts

Conflicts are displayed above ordinary caveats when material.

Conflict categories:

```text
AUTHORITY_CONFLICT
PROVIDER_CONFLICT
METRIC_CONFLICT
SIMULATION_CONFLICT
THEORY_CONFLICT
USER_CONTEXT_CONFLICT
TEMPORAL_CONFLICT
REGIONAL_CONFLICT
MODEL_CONFLICT
```

Example:

```text
Material conflict

Tournament evidence supports the candidate.
Local-meta notes favor retaining the current card.
Simulation support is weak because one relevant behavior is approximated.

Effect on conclusion:
Confidence capped at Moderate.
```

Conflicts must not be “resolved” by averaging unrelated evidence together.

### J. Caveats

Caveats describe limitations that do not constitute contradictory evidence:

- small sample;
- incomplete coverage;
- stale source;
- unsupported cards;
- approximated simulator behavior;
- historical format translation;
- incomplete regional data;
- missing primer context;
- user objective not specified;
- source not independently verified.

Each caveat declares its effect:

```text
Informational
Limits scope
Lowers confidence
Blocks action
Requires revalidation
```

### K. Jin handoff

The panel exposes:

```text
Discuss this decision
Challenge this conclusion
Compare theory lenses
Explain the evidence
Design an experiment
Explain the rules interaction
```

The handoff packet includes stable references rather than flattened prose:

```text
decisionId
deckSnapshotId
analysisRunId
unifiedEvidenceId
simulationReportIds
conflictIds
sourceIds
theoryTopicIds
legalityResultId
```

Jin’s theory handling should route by topic, preserve disagreements, distinguish direct theory from inference, and avoid forcing consensus. That behavior follows the shared corpus architecture rather than allowing the chat model to improvise a famous-person séance. fileciteturn0file1

### L. Provenance drawer

Lowest disclosure level:

- formula;
- metric version;
- source datasets;
- canonical record IDs;
- date window;
- region;
- placement scope;
- exclusions;
- generated timestamp;
- simulator version;
- ontology version;
- analysis profile;
- weight profile;
- serialization hash;
- replay command or local action.

---

# 8. Progressive disclosure model

## 8.1 Disclosure levels

### Level 1: Summary

Visible immediately:

```text
Conclusion
Action
Confidence
Agreement
Snapshot
Primary reason
Primary tradeoff
Blocking warning
```

Target reading time: under 20 seconds.

### Level 2: Reasoning

Expanded on demand:

```text
Replacement logic
Expected impact
Major evidence groups
Material conflicts
Material caveats
```

Target reading time: one to three minutes.

### Level 3: Evidence

```text
Individual metrics
Weights
Samples
Coverage
Simulation details
Source comparisons
Theory references
```

### Level 4: Audit

```text
Formulas
Canonical identifiers
Version metadata
Exclusions
Raw source references
Replay metadata
Deterministic serialization
```

## 8.2 Expansion behavior

- Material conflicts begin expanded.
- Blocking legality failures begin expanded.
- Ordinary provenance begins collapsed.
- Expansion state may persist per user and component type.
- Expansion state must not persist across a different decision when that persistence could hide a new warning.
- Opening an evidence link from Jin automatically expands and focuses the referenced evidence item.
- Browser history must preserve the selected decision and disclosure level.

## 8.3 Deep-link format

Conceptual route:

```text
/decks/{deckId}/snapshots/{snapshotId}/analysis/{runId}/decisions/{decisionId}
```

Optional fragment:

```text
#simulation-SIM-381
#conflict-CON-44
#source-SRC-208
#evidence-EV-991
```

---

# 9. Jin integration

## 9.1 Placement

Jin remains visible in the Analysis Workspace, normally as a docked right-side panel.

It must not cover the active Decision Evidence Panel.

## 9.2 Thread binding

Every substantive thread is bound to:

```text
deckSnapshotId
analysisRunId
optional decisionId
analysisProfileId
theoryRetrievalVersion
```

When the active snapshot changes, Jin displays:

```text
This discussion used snapshot 8A4F…C91.
The active deck is now snapshot D32B…119.
```

The user may inspect the old thread, but the interface must not silently treat it as current.

## 9.3 Jin answer card

```text
┌─────────────────────────────────────────────┐
│ JIN ANSWER                                  │
│ Bound to DEC-204 / Snapshot 8A4F…C91       │
├─────────────────────────────────────────────┤
│ Direct answer                               │
│ The replacement is better supported under  │
│ the selected profile, but the evidence does │
│ not justify a universal replacement claim. │
├─────────────────────────────────────────────┤
│ Evidence level: Measured + inferred         │
│ Speculation: Limited                        │
│ Legality: Validated                         │
│ Confidence ceiling: Moderate                │
│ Contradiction: Local-meta preference        │
├─────────────────────────────────────────────┤
│ Evidence links                              │
│ [Tournament inclusion]                      │
│ [Replacement overlap]                       │
│ [Simulation SIM-381]                        │
│ [Theory: Engine conversion]                 │
└─────────────────────────────────────────────┘
```

## 9.4 Jin actions

Jin may create:

- an experiment proposal;
- a theory note;
- a correction candidate;
- a deck-specific hypothesis;
- a structured comparison;
- an explanation.

Jin may not:

- alter evidence weight;
- raise recommendation confidence;
- mark a conflict resolved;
- stage a deck edit without an explicit user action;
- write a new persisted recommendation;
- change canonical card or event data.

## 9.5 Theory visibility

Theory must not occupy the primary recommendation header.

The default panel may show:

```text
Theory context available: 3 applicable lenses, 1 disagreement
```

Expanding it reveals:

- applicable theory concepts;
- direct-source status;
- format-translation warning;
- empirical support or conflict;
- Jin inference;
- disagreements.

Theory explains evidence. It does not receive a hidden “famous author bonus.”

---

# 10. Navigation flows

## 10.1 Import and analyze

```text
Open Deck Workspace
    ->
Import URL or select saved deck
    ->
Resolve canonical identities
    ->
Create or reuse immutable snapshot
    ->
Display unsupported or unresolved cards
    ->
Run approved analyses
    ->
Open Analysis Workspace
    ->
Populate Attention Queue
    ->
Select highest-priority finding
    ->
Open Decision Evidence Panel
```

## 10.2 Unchanged source deck

```text
Open saved deck
    ->
Check source modified state
    ->
Deck hash unchanged
    ->
Reuse compatible cached analysis
    ->
Display prior analysis timestamp and version
```

## 10.3 Changed source deck

```text
Check source
    ->
Change detected
    ->
Create new source snapshot
    ->
Show snapshot diff
    ->
Mark prior decisions historical
    ->
Rerun affected analysis
    ->
Retain prior reports
```

## 10.4 Inspect recommendation

```text
Select recommendation
    ->
Read summary
    ->
Inspect replacement logic
    ->
Inspect material conflicts
    ->
Inspect evidence contributions
    ->
Inspect simulation where relevant
    ->
Open Jin discussion or stage an experiment
```

## 10.5 Stage replacement experiment

```text
Select “Stage replacement”
    ->
Open replacement confirmation sheet
    ->
Show removed and added card
    ->
Show affected packages and roles
    ->
Create staged change
    ->
Generate candidate snapshot
    ->
Run selected affected analyses
    ->
Display baseline versus candidate decision comparison
```

## 10.6 Jin challenge flow

```text
Select “Challenge this conclusion”
    ->
Jin receives decision references
    ->
Jin retrieves material contradictory evidence
    ->
Jin retrieves applicable theory lenses
    ->
Jin performs legality and contradiction checks
    ->
Jin returns an issue map
    ->
Evidence links open exact panel sections
```

## 10.7 Snapshot comparison

```text
Choose baseline snapshot
    ->
Choose comparison snapshot
    ->
Show card diff
    ->
Show analysis-version compatibility
    ->
Show changed findings
    ->
Show resolved findings
    ->
Show newly introduced caveats
```

---

# 11. Empty states

## 11.1 No deck selected

```text
No deck selected

Import a deck URL, paste a list, or open a saved snapshot.
No analysis can run without a canonical deck snapshot.
```

Primary controls:

```text
[Import deck]
[Open saved deck]
[Paste deck list]
```

## 11.2 Deck contains unresolved cards

```text
Analysis blocked

3 card names could not be resolved.
Unresolved cards will not be guessed or included in analytics.

[Review unresolved cards]
```

## 11.3 No findings

```text
No actionable findings under this profile

Codie completed the selected analysis and produced no recommendation,
legality warning, material conflict, or deck-health concern above the
current display threshold.

This does not mean the deck is objectively complete.
```

## 11.4 No simulation evidence

```text
No relevant simulation result

The current decision does not have a compatible simulation experiment.
The conclusion relies on other evidence categories.
```

## 11.5 No Jin model available

```text
Jin unavailable

No configured local model is available.
Evidence panels and deterministic reports remain functional.
```

## 11.6 No source agreement calculation

```text
Source agreement not applicable

This conclusion is based on a single authoritative source or a
deterministic legality result rather than multiple eligible observations.
```

---

# 12. Loading states

## 12.1 Analysis progress

Loading must expose the actual pipeline stage:

```text
1. Resolving snapshot
2. Retrieving canonical evidence
3. Calculating approved metrics
4. Building Unified Evidence
5. Running Decision Intelligence
6. Preparing presentation model
```

The UI must not display fake percentages unless progress is measurable.

Preferred:

```text
Building Unified Evidence
Completed 4 of 7 evidence groups
```

Not preferred:

```text
Almost there… 93%
```

Humanity has suffered enough fraudulent loading bars.

## 12.2 Partial availability

Completed evidence may display while slower optional work continues:

```text
Decision summary available
Simulation still running
Jin discussion available without simulation evidence
```

The decision must be labeled provisional when pending evidence can materially alter it.

## 12.3 Simulation progress

```text
Simulation SIM-381
12,000 / 20,000 games complete
Current estimate is provisional
Canceling preserves no final result
```

## 12.4 Snapshot refresh

```text
Checking source identity
Fetching source metadata
Comparing deck hash
```

No new snapshot is created until a change is confirmed.

---

# 13. Error and degraded states

## 13.1 Error taxonomy

```text
USER_INPUT_ERROR
CANONICALIZATION_ERROR
SOURCE_UNAVAILABLE
SOURCE_CONFLICT
REPOSITORY_ERROR
ANALYTICS_ERROR
EVIDENCE_FUSION_ERROR
DECISION_ERROR
SIMULATION_ERROR
JIN_ERROR
VERSION_MISMATCH
PRIVACY_BLOCK
```

## 13.2 Error presentation contract

Every error message includes:

- what failed;
- what remains valid;
- whether retry is safe;
- whether cached results exist;
- which result sections are affected;
- diagnostic reference;
- no raw stack trace in the default interface.

Example:

```text
Simulation unavailable

The simulator could not model 2 cards relevant to this target.
Tournament, tag, package, and replacement evidence remain available.
The decision confidence has been capped at Low.

Diagnostic: SIM-UNSUPPORTED-204
```

## 13.3 Source unavailable

```text
Source refresh failed

The saved snapshot remains intact.
Cached analysis from 2026-07-22 is still available.
Freshness-sensitive metrics are marked stale.
```

## 13.4 Version mismatch

```text
Report version mismatch

This decision used analytics version 4.2.
The current installation uses version 4.4.
The historical result remains viewable but cannot be compared directly
until replayed under a common version.
```

## 13.5 Evidence Fusion failure

No recommendation may display as complete when its Unified Evidence packet failed assembly.

```text
Decision unavailable

Evidence assembly failed before Decision Intelligence completed.
No partial recommendation has been retained.
```

## 13.6 Jin failure

A Jin failure must not affect deterministic evidence surfaces.

```text
Jin response failed

The Decision Evidence Panel remains valid.
No recommendation or evidence record was changed.
```

---

# 14. Mobile-readable future layout

## 14.1 Scope boundary

Immediate implementation excludes:

- mobile application;
- mobile deck editing;
- mobile source refresh;
- mobile analysis execution;
- mobile simulation execution;
- mobile Jin execution;
- mobile correction approval;
- mobile recommendation staging;
- write-enabled remote APIs.

The current phase may define responsive content order and export-compatible view models. It must not build mobile execution infrastructure under the excuse that “the component was already nearby.”

## 14.2 Future read-only mobile wireframe

```text
┌──────────────────────────────┐
│ CODIE REPORT                 │
│ Rograkh / Ishai              │
│ Snapshot 8A4F…C91            │
│ Generated 2026-07-23         │
├──────────────────────────────┤
│ ATTENTION                    │
│ 1 High · Missing conversion  │
│ 2 Medium · Narrow slot       │
│ 3 Medium · Coverage warning  │
├──────────────────────────────┤
│ DECISION DEC-204             │
│                              │
│ Test Card B over Card A      │
│                              │
│ Confidence: Moderate         │
│ Agreement: Mixed             │
│ Legality: Validated          │
│                              │
│ Primary reason               │
│ Card B preserves the primary │
│ role and adds two relevant   │
│ secondary functions.         │
│                              │
│ Main tradeoff                │
│ Loses narrow matchup utility.│
│                              │
│ [Replacement logic ▾]        │
│ [Evidence ▾]                 │
│ [Simulation ▾]               │
│ [Conflicts ▾]                │
│ [Sources ▾]                  │
├──────────────────────────────┤
│ JIN DISCUSSION SNAPSHOT      │
│ Read-only answer excerpt     │
│ [Evidence links]             │
└──────────────────────────────┘
```

## 14.3 Mobile content order

1. report identity;
2. snapshot and freshness;
3. conclusion;
4. confidence and agreement;
5. blocking warnings;
6. primary reason;
7. tradeoff;
8. conflicts;
9. replacement logic;
10. simulation;
11. evidence contributions;
12. Jin discussion snapshot;
13. provenance.

No side-by-side tables are required on mobile. Comparison matrices become stacked rows:

```text
Primary role
Current: Interaction
Candidate: Interaction
Effect: Preserved
```

## 14.4 Mobile security boundary

Future read-only delivery should use a separate read model and endpoint surface. It must not expose mutation routes and merely hide their buttons with CSS, the standard web-development ritual of pretending an unlocked door is secure because the sign says “Staff Only.”

---

# 15. Accessibility requirements

## 15.1 Keyboard operation

All functionality must be usable by keyboard:

```text
Tab / Shift+Tab     Move through controls
Enter / Space       Activate
Arrow keys          Navigate queue and tabs
Escape              Close drawer or modal
Ctrl+1              Deck Workspace
Ctrl+2              Analysis Workspace
Ctrl+J              Focus Jin
Ctrl+K              Global deck/card search
```

Shortcuts must be discoverable and remappable where conflicts occur.

## 15.2 Focus management

- Opening a decision moves focus to its heading.
- Expanding a section preserves logical focus.
- Closing a drawer returns focus to the control that opened it.
- Validation errors move focus to the error summary.
- Cross-screen updates do not steal focus.
- Jin evidence links move focus to the referenced evidence heading.

## 15.3 Semantic structure

- One page-level heading.
- Ordered heading hierarchy.
- Accordion controls use real buttons.
- `aria-expanded` reflects state.
- Tables use headers and captions.
- Severity is expressed in text, not color alone.
- Icons have accessible names or are hidden from assistive technology.
- Loading updates use non-disruptive live regions.
- Blocking errors use assertive announcements.

## 15.4 Visual requirements

- Text remains usable at 200% zoom.
- No horizontal scrolling for ordinary text content.
- Confidence and severity use text labels plus visual styling.
- Focus indicator remains clearly visible.
- Dense tables provide a stacked alternative.
- Charts provide equivalent textual values.
- Reduced-motion preferences disable animated transitions.
- No flashing or pulsing loading indicators.
- Tooltips do not contain required information unavailable elsewhere.

## 15.5 Plain-language labels

Use:

```text
Source agreement
Evidence coverage
Simulation limitation
Deck snapshot
Replacement tradeoff
```

Avoid presenting internal jargon without explanation:

```text
UEO variance quotient
Weighted source entropy
Decision convergence coefficient
```

If such a metric genuinely exists, it belongs behind the methodology drawer with a definition.

---

# 16. Data contracts

## 16.1 Decision evidence packet

```ts
type DecisionEvidencePacket = {
  decisionId: string;
  decisionType:
    | "recommendation"
    | "replacement"
    | "deck_health"
    | "legality"
    | "experiment_result";

  status:
    | "provisional"
    | "complete"
    | "blocked"
    | "superseded"
    | "historical";

  subject: {
    subjectType: "deck" | "card" | "package" | "combo" | "tag";
    canonicalId: string;
    displayName: string;
  };

  deckContext: {
    deckId: string;
    snapshotId: string;
    snapshotHash: string;
    commanderSignature: string[];
    snapshotCreatedAt: string;
    sourceUrl?: string;
  };

  analysisContext: {
    analysisRunId: string;
    analysisProfileId: string;
    analysisProfileVersion: string;
    weightProfileId: string;
    weightProfileVersion: string;
    generatedAt: string;
  };

  conclusion: {
    observedConcern: string;
    statement: string;
    proposedAction?: string;
    expectedImpact?: string;
    primaryTradeoff?: string;
  };

  confidence: {
    label: "high" | "moderate" | "low" | "insufficient";
    calibratedValue?: number;
    ceiling: "high" | "moderate" | "low" | "insufficient";
    ceilingReasons: string[];
  };

  sourceAgreement: {
    label:
      | "strong"
      | "mixed"
      | "weak"
      | "insufficient"
      | "not_applicable";
    eligibleSourceCount: number;
    supportingSourceCount: number;
    opposingSourceCount: number;
    summary: string;
  };

  legality: {
    status:
      | "validated"
      | "validated_with_assumptions"
      | "unresolved"
      | "invalid"
      | "not_applicable";
    resultId?: string;
    assumptions: string[];
    blockingReasons: string[];
  };

  replacement?: ReplacementComparison;
  contributions: EvidenceContribution[];
  simulations: SimulationEvidenceReference[];
  conflicts: EvidenceConflict[];
  caveats: EvidenceCaveat[];

  jinContext: {
    permitted: boolean;
    theoryTopicIds: string[];
    existingThreadIds: string[];
  };

  provenance: ProvenanceSummary;
};
```

## 16.2 Evidence contribution

```ts
type EvidenceContribution = {
  contributionId: string;
  category:
    | "authority"
    | "tournament"
    | "regional"
    | "functional_overlap"
    | "package"
    | "co_dependence"
    | "simulation"
    | "primer"
    | "theory"
    | "user_context";

  label: string;
  rawObservation: string;
  normalizedValue?: number;
  normalizationMethod?: string;
  selectedWeight?: number;

  direction:
    | "supports"
    | "opposes"
    | "mixed"
    | "neutral"
    | "not_scored";

  sampleSize?: number;
  eligiblePopulation?: number;
  coverageRatio?: number;

  confidence:
    | "high"
    | "moderate"
    | "low"
    | "insufficient";

  evidenceIds: string[];
  caveatIds: string[];
  conflictIds: string[];
};
```

## 16.3 Replacement comparison

```ts
type ReplacementComparison = {
  currentCardId: string;
  candidateCardId: string;

  dimensions: Array<{
    dimensionId: string;
    label: string;
    currentValue: string;
    candidateValue: string;
    effect:
      | "gained"
      | "preserved"
      | "improved"
      | "reduced"
      | "lost"
      | "changed"
      | "unknown";
    evidenceIds: string[];
  }>;

  affectedPackageIds: string[];
  affectedComboIds: string[];
  affectedTagIds: string[];
};
```

## 16.4 Conflict

```ts
type EvidenceConflict = {
  conflictId: string;
  category:
    | "authority"
    | "provider"
    | "metric"
    | "simulation"
    | "theory"
    | "user_context"
    | "temporal"
    | "regional"
    | "model";

  severity: "blocking" | "material" | "informational";
  statementA: string;
  statementB: string;
  effectOnDecision: string;
  resolutionStatus:
    | "preserved"
    | "resolved_by_authority"
    | "resolved_by_scope"
    | "requires_review";
  evidenceIds: string[];
};
```

## 16.5 Caveat

```ts
type EvidenceCaveat = {
  caveatId: string;
  category:
    | "sample_size"
    | "coverage"
    | "staleness"
    | "unsupported_card"
    | "simulation_approximation"
    | "format_translation"
    | "regional_gap"
    | "missing_context"
    | "version_mismatch";

  message: string;
  effect:
    | "informational"
    | "limits_scope"
    | "lowers_confidence"
    | "blocks_action"
    | "requires_revalidation";
};
```

---

# 17. Component specifications

| Component | Responsibility | Required inputs | Must not do |
|---|---|---|---|
| `CodieAppShell` | Workspace routing and shared identity | Active deck, snapshot, route | Calculate evidence |
| `WorkspaceSwitcher` | Deck/Analysis navigation | Current workspace | Change analysis state |
| `SnapshotBar` | Display snapshot identity and freshness | Snapshot view model | Modify snapshots |
| `DeckListView` | Render normalized zones and cards | Canonical deck view model | Guess unresolved cards |
| `StagedChangeTray` | Manage local proposed edits | Staged-change records | Modify source deck automatically |
| `AttentionQueue` | Present prioritized findings | Presentation-ready finding list | Re-rank strategically |
| `DecisionSummaryCard` | Show conclusion and top warnings | Decision packet summary | Hide material conflicts |
| `DecisionEvidencePanel` | Coordinate all decision detail | Full decision packet | Recompute recommendation |
| `ConfidenceIndicator` | Display confidence and ceiling | Confidence object | Blend agreement into confidence |
| `SourceAgreementIndicator` | Display concurrence | Agreement object | Treat source count as authority |
| `ReplacementComparisonView` | Show role and package deltas | Replacement comparison | Infer missing roles |
| `EvidenceContributionList` | Show raw evidence and weights | Contribution records | Alter profile weights |
| `SimulationEvidenceCard` | Show experiment result and limitations | Simulation reference | Present model result as reality |
| `ConflictBanner` | Surface material contradictions | Conflict records | Dismiss without state change |
| `CaveatList` | Show limitations and effects | Caveat records | Collapse blocking caveats |
| `ProvenanceDrawer` | Audit and replay metadata | Provenance object | Fetch providers directly |
| `JinDock` | Bound conversation and evidence links | Thread and reference IDs | Persist recommendations |
| `SnapshotComparisonView` | Compare immutable states | Two snapshot view models | Compare incompatible versions silently |
| `AnalysisStatusPanel` | Loading, partial, stale, and error status | Pipeline status | Display invented progress |
| `ReadOnlyReportView` | Future static responsive rendering | Serialized report packet | Expose execution controls |

---

# 18. View-model boundary

The UI should consume presentation-ready read models.

```text
Canonical repositories
    ->
Analytics
    ->
Evidence Fusion
    ->
Decision Intelligence
    ->
Decision presentation assembler
    ->
Read-only view models
    ->
UI components
```

The presentation assembler may:

- group evidence;
- generate display labels from enums;
- order already-ranked findings;
- create accessible summaries;
- determine default expanded sections based on severity.

It may not:

- reinterpret strategic meaning;
- change weights;
- suppress contradictory evidence;
- raise confidence;
- resolve legality;
- recalculate metrics.

---

# 19. Proposed module structure

```text
src/
├── application/
│   ├── analysis-session/
│   ├── workspace-routing/
│   └── selection-sync/
├── domain/
│   ├── decision-evidence/
│   │   ├── decision-evidence-packet.ts
│   │   ├── evidence-contribution.ts
│   │   ├── evidence-conflict.ts
│   │   └── evidence-caveat.ts
│   ├── deck-snapshots/
│   └── staged-changes/
├── presentation/
│   ├── assemblers/
│   │   ├── decision-panel-assembler.ts
│   │   ├── attention-queue-assembler.ts
│   │   └── snapshot-status-assembler.ts
│   └── view-models/
├── ui/
│   ├── shell/
│   ├── deck-workspace/
│   ├── analysis-workspace/
│   ├── decision-evidence-panel/
│   ├── jin-dock/
│   ├── snapshot-comparison/
│   ├── states/
│   └── accessibility/
└── tests/
    ├── fixtures/
    │   ├── decision-evidence/
    │   ├── conflicts/
    │   ├── simulations/
    │   └── snapshots/
    ├── component/
    ├── integration/
    ├── accessibility/
    └── visual-regression/
```

---

# 20. Test fixtures

Minimum fixtures:

1. **High-confidence recommendation with strong agreement**
2. **Moderate recommendation with mixed agreement**
3. **Strong source agreement but low sample**
4. **High-quality authority result with agreement not applicable**
5. **Invalid legality result blocking staging**
6. **Simulation improvement with overlapping margins of error**
7. **Simulation result with unsupported relevant card**
8. **Target-turn experiment that is not cumulative**
9. **Replacement preserving primary role but losing secondary function**
10. **User-context conflict opposing measured evidence**
11. **Regional evidence conflicting with global evidence**
12. **Stale snapshot with historical decision**
13. **Candidate snapshot versus baseline**
14. **No actionable findings**
15. **Evidence Fusion failure**
16. **Jin unavailable while deterministic UI remains functional**
17. **Source conflict requiring review**
18. **Material conflict expanded by default**
19. **Keyboard-only complete workflow**
20. **Screen-reader traversal of all panel levels**

---

# 21. Progressive implementation plan

## Phase 1: Contracts and read models

Deliver:

- Decision Evidence Packet schema;
- contribution, conflict, caveat, replacement, and simulation reference schemas;
- presentation assembler contracts;
- immutable fixture packets;
- deterministic serialization tests.

Exclusions:

- full visual implementation;
- Jin execution;
- mobile delivery;
- recommendation logic changes.

## Phase 2: Desktop application shell

Deliver:

- Deck Workspace;
- Analysis Workspace;
- workspace switching;
- dual-display route support;
- shared selection state;
- snapshot bar;
- loading and error shell.

## Phase 3: Decision Evidence Panel

Deliver:

- conclusion header;
- confidence;
- source agreement;
- legality;
- replacement logic;
- evidence contributions;
- simulation section;
- conflicts;
- caveats;
- provenance drawer;
- accessibility behavior.

## Phase 4: Staged experiment workflow

Deliver:

- stage replacement;
- candidate snapshot;
- affected-analysis rerun request;
- baseline/candidate comparison;
- immutable original snapshot preservation.

This phase must not push edits back to Moxfield or another provider.

## Phase 5: Jin evidence linking

Deliver:

- decision-bound threads;
- stable evidence links;
- stale-thread warnings;
- theory-context summary;
- correction and experiment candidate output boundaries.

The theory corpus’s independent-lens and disagreement-preservation design should be reused rather than rebuilt inside the chat UI. fileciteturn0file1

## Phase 6: Accessibility and adversarial validation

Deliver:

- keyboard workflow;
- screen-reader semantics;
- zoom and reflow tests;
- non-color status tests;
- material-conflict visibility tests;
- stale-snapshot tests;
- UI mutation-boundary tests.

## Deferred phase: Read-only mobile delivery

May later deliver:

- responsive static report;
- read-only evidence panel;
- read-only Jin transcript;
- secure report delivery;
- separate read endpoint surface.

Explicitly excluded now:

- mobile execution;
- remote writes;
- mobile analysis controls;
- mobile Jin invocation;
- mobile deck mutation.

---

# 22. Acceptance criteria

The design is accepted only when all of the following are demonstrably true:

1. The user can identify the highest-priority concern without opening raw evidence.
2. Every recommendation visibly identifies its deck snapshot.
3. Confidence and source agreement appear as separate concepts.
4. The reason for a confidence ceiling is inspectable.
5. Material conflicts are visible without opening provenance.
6. Evidence weights are distinguishable from evidence values.
7. Changing display state cannot change a recommendation.
8. Changing a weight profile requires a new or replayed decision result.
9. The interface never calculates recommendations independently.
10. Simulation output includes target, model, sample size, uncertainty, support status, and warnings.
11. Non-cumulative target-turn simulations are not displayed as cumulative probabilities.
12. Unsupported relevant simulator cards lower or block confidence according to the supplied packet.
13. Invalid legality blocks replacement staging.
14. A recommendation cannot directly mutate the active deck snapshot.
15. Staged changes create a candidate snapshot.
16. Original and candidate snapshots remain independently reproducible.
17. Jin answers are bound to the exact snapshot and decision used.
18. Jin evidence links open the exact evidence section.
19. Jin cannot edit canonical evidence, confidence, weights, conflicts, or recommendations.
20. Empty, loading, partial, stale, and error states are explicit.
21. The deterministic evidence interface remains usable when Jin is unavailable.
22. Keyboard users can complete the full inspect-and-stage workflow.
23. Status distinctions remain understandable without color.
24. At 200% zoom, primary content remains readable without two-dimensional scrolling.
25. The desktop implementation contains no mobile execution endpoints.
26. Mobile layout work remains a documented read-only future contract, not scope leakage.
27. The interface does not fill unused space with irrelevant metrics merely because those metrics exist.
28. All audit-level information remains reachable through progressive disclosure.
29. Historical decisions remain viewable but are clearly marked when their snapshot or analysis version is stale.
30. The UI preserves the constitutional separation among evidence, conclusions, user context, theory, and presentation. fileciteturn0file0
> [!IMPORTANT]
> Repository intake note: This is a preserved pre-ratification design
> proposal. `docs/CODIE_V2_CONSTITUTION.md` is now ratified and is the
> governing authority. Statements below that call V2 a non-authoritative
> comparison draft are historical. This proposal does not authorize
> implementation.
