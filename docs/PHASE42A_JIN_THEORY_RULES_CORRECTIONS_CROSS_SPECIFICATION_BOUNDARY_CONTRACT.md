# Phase 42A - Jin / Theory / Rules / Corrections Cross-Specification Boundary and Decision Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase42A
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42B
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42B is reserved for the Fixed Jin Regression Corpus Schema and
Deterministic Evaluation Contract. It remains blocked until Phase 42A outside
validation returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42A establishes the cross-specification boundary for Program B:

```text
Jin
Theory Corpus
Rules Layer
Model Profiles
User Correction Ledger
Fixed Jin Regression Corpus
```

The program coordinates those systems without collapsing their authority,
privacy, lifecycle, storage, or decision boundaries.

Phase 42A is documentation-only. It does not implement production code,
tests, fixtures, schema, repositories, model invocation, source acquisition,
retrieval, Jin answers, corrections, rules answers, theory claims, UI, file
writing, or network behavior.

## Authority

The governing sources are:

```text
docs/CODIE_V2_CONSTITUTION.md, Sections 1, 5, 6, 20 through 27, 32 through 35
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md, Program B
```

The following are preserved design inputs only:

```text
docs/design_inputs/v2_intelligence_program/README.md
docs/design_inputs/v2_intelligence_program/SOURCE_MANIFEST.md
docs/design_inputs/v2_intelligence_program/JIN_GITAXIAS_STRATEGIST_SUBSYSTEM_PROPOSAL.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_FIXED_JIN_REGRESSION_CORPUS_PROPOSAL.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_RULES_LAYER_JUDGE_TRAINING_PROPOSAL.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_MODEL_PROFILE_PROPOSAL.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_USER_CORRECTION_LEDGER_PROPOSAL.md
docs/design_inputs/v2_intelligence_program/CODIE_V2_THEORY_CORPUS_ATTRIBUTED_KNOWLEDGE_GRAPH_PROPOSAL.md
```

Design inputs may inform future contracts. They do not authorize
implementation, and any historical statement that V2 is unratified is
superseded by the adopted constitution.

## Program Ownership

Each subsystem owns one bounded responsibility.

| Subsystem | Owns | Must not own |
|---|---|---|
| Rules Layer | Versioned official rules, Oracle/ruling references, legality validation, bounded interaction verdicts | Strategy, recommendations, popularity, model confidence |
| Fixed Regression Corpus | Versioned fixtures, expected outcomes, deterministic evaluation records, release-gate evidence | Runtime truth, user memory, production answers |
| Model Profiles | Local/cloud routing policy, capability declarations, privacy classes, consent, redaction, audit metadata | Evidence, legality, corrections, strategic truth |
| Correction Ledger | Versioned user corrections, lifecycle, narrow scope, authority ceiling, application receipts | Official truth, canonical facts, measured evidence, global promotion by default |
| Theory Corpus | Rights-reviewed sources, immutable source versions, attributed claims, limitations, contradictions, translations | Canonical truth, measured evidence, author-as-authority scoring |
| Jin | Intent, scope, query planning, governed retrieval orchestration, evidence gates, answer packets, permitted user-context writes | Canonical evidence, measurements, confidence tables, legality truth, persisted recommendations |
| Decision Intelligence | Persisted decision-bearing conclusions and recommendations | Raw-provider reasoning, authority mutation, theory-source ownership |
| UI and exports | Presentation of accepted packets and explicit staged user actions | Evidence calculation, correction resolution, confidence strengthening |

No subsystem may assume another subsystem's ownership merely because its
packet is unavailable.

## Trust Classes

The program preserves these distinct classes:

```text
authority
canonical truth
observational data
measured evidence
attributed theory or community context
user context and corrections
model-generated inference
persisted decision output
```

They must remain separately labeled in retrieval, model input, answers,
storage, evaluation, and exports.

Authority and canonical truth outrank theory, community context, user
corrections, and model output. Measured evidence cannot be replaced by theory
or corrections. A model-generated statement gains no authority from fluency,
agreement, repetition, or a high numeric score.

## Dependency Order

Program B follows this contract order:

```text
Phase 42A: cross-specification boundary and decision contract
Phase 42B+: fixed regression corpus schema and deterministic evaluation
then Rules authority, legality, and bounded interaction
then local-first model profiles, redaction, consent, and routing
then minimal User Correction Ledger
then Theory source registry, rights, source versions, and citations
then reviewed claims, typed graph, contradictions, translation, and retrieval
then Jin intent, scope, query planning, evidence gates, and legality gates
then Jin writer, auditor, finalizer, and answer packets
then experiments and permitted user-context writes
then judge-training and curriculum
then program checkpoint and release acceptance
```

A later contract may split an item into contract, implementation-contract,
implementation, and checkpoint packets. It may not reorder a dependency
without an accepted architecture amendment.

## Release Prerequisites

```text
model-backed Jin output requires the accepted fixed regression corpus
rules-validated or legality-validated output requires an accepted Rules Layer
model invocation requires an accepted model profile and local-first route
correction application requires authority ceilings and narrow-scope resolution
attributed theory use requires rights-reviewed, versioned, cited claims
Jin writing requires accepted intent, scope, retrieval, and evidence gates
permitted writes require explicit confirmation and subsystem-owned write APIs
Jin release requires deterministic finalization and recorded regression evidence
```

Missing prerequisites cause a visible unavailable, unsupported, blocked, or
human-review state. They never trigger a silent fallback to model knowledge.

## Read Boundaries

Future Jin orchestration may consume only approved packet projections and
bounded references from:

```text
Class 0 authority
canonical observations through approved retrieval
measured evidence
Unified Evidence
accepted Relationship Intelligence bundles
accepted Tournament Exposure bundles
primer context
Theory Corpus retrieval packets
User Correction Ledger resolution packets
deck snapshots
simulation reports
source conflicts
user context
```

Jin and model runners must not receive unrestricted database access, raw
provider payloads, secrets, unselected private source text, unrestricted
repository text, or mutable subsystem internals.

Relationship Intelligence and Tournament Exposure remain labeled measured
evidence. Jin may explain them but may not strengthen, recalculate, or relabel
them as tournament truth.

## Write Boundaries

Jin may never write:

```text
official authority
canonical card, combo, deck, event, or source records
observational tournament evidence
measured metrics
confidence tables
Commander staple or package statistics
legality truth
Theory Corpus approved claims or source versions
active correction records without the ledger lifecycle
persisted recommendations or Decision Intelligence records
validator or governance state
```

Subject to later accepted contracts and explicit confirmation, Jin may request
writes of:

```text
theory notes
experiment queue items
user testing notes
correction candidates
lesson progress
deck-specific hypotheses
structured conversation summaries
```

Those records remain user context, theory, or experiment data and are written
through the owning subsystem. Jin never writes them directly.

## Rules Boundary

The Rules Layer is categorical authority support, not probabilistic strategy.

Future rules packets must:

```text
bind to versioned official authority snapshots
distinguish confirmed, unsupported, unresolved, stale, and conflicting states
preserve evaluation date for legality
cite authority
remain independent of recommendation scoring
avoid treating community tools as authority
avoid claiming a full general-purpose rules engine
```

Jin must block or qualify any answer whose required rules or legality premise
is not supported by the accepted Rules Layer.

## Correction Boundary

Corrections apply at the narrowest valid scope and retain immutable semantic
history.

```text
user corrections may override prior Jin reasoning and user-context assumptions
corrections may not override official authority or canonical truth
corrections may not rewrite measured evidence
deck-snapshot corrections do not become commander or global rules
authority-sensitive corrections require verification and governance
conflicting corrections remain visible rather than being averaged
model output may propose a correction candidate but may not activate it
```

## Theory Boundary

Theory explains, compares, questions, and contextualizes. It does not replace
authority, canonical truth, measured evidence, or user judgment.

Future theory packets must preserve:

```text
author and work identity
immutable source version
rights and access state
claim attribution
citation anchors
applicable formats
transferability state
limitations
review status
contradictions
translation or application status
```

Author reputation is not a truth score. Community material remains community
context until separately admitted under an accepted source policy.

## Model Boundary

Model routing is local-first and cloud-deny-by-default.

```text
Codie must remain functional without a paid LLM
deterministic and retrieval functionality may not depend on cloud access
private data transmission requires profile-specific explicit consent
redaction and minimization occur before any permitted cloud request
model output is untrusted until schema, authority, legality, and evidence gates pass
models may not execute code or mutate protected records
models may not fabricate missing citations or structured fields
```

Exact runtimes, models, quantization tiers, cloud providers, retention terms,
and consent duration remain decisions for the future model-profile contract.

## Answer And Recommendation Boundary

Jin is not a second recommendation engine.

Jin may produce labeled strategic discussion, inference, comparison,
challenge, or experiment proposals after its future gates are accepted. Those
outputs remain conversational answer packets.

Any persisted recommendation must flow through:

```text
Canonical Truth
-> Measured Evidence
-> Evidence Fusion
-> Decision Intelligence
-> Recommendation Output
```

Jin may cite an existing decision packet. It may not persist its own answer as
a recommendation or bypass Decision Intelligence.

## Regression Boundary

The Fixed Jin Regression Corpus is release evidence, not production evidence.

It must eventually cover at least:

```text
citation accuracy
legality blocking
unsupported-claim removal
evidence, theory, and community separation
correction-scope isolation
contradiction disclosure
local-only execution
cloud redaction
strategic-claim labeling
authority immutability
```

Phase 42A does not choose corpus size, file layout, scoring thresholds, model
matrix, or release criteria beyond requiring deterministic, versioned,
artifact-backed evaluation. Phase 42B owns those decisions.

## Unknown And Conflict Handling

Unknown, unsupported, unavailable, stale, blocked, conflicting, and zero are
distinct states.

No future subsystem may:

```text
convert missing authority into model inference
convert retrieval failure into negative evidence
hide theory or correction conflicts
silently select the newest correction
silently widen scope
silently substitute current legality for historical legality
silently fall back from local to cloud
silently omit required citations or provenance
```

## Reproducibility

Every substantive future Jin answer must retain an analysis manifest with the
versions required by Constitution Section 33.4, including applicable deck,
source, analytics, simulator, ontology, Spellbook, Correction Ledger, Theory
Corpus, model, prompt-policy, filter, profile, and timestamp identities.

Mutable cloud aliases may not be described as exactly reproducible.

## Resolved Cross-Specification Decisions

Phase 42A resolves only these boundary decisions:

```text
Rules owns authority and legality verdicts.
The regression corpus owns evaluation fixtures and release evidence.
Model Profiles own routing, privacy, consent, and redaction.
The Correction Ledger owns scoped correction lifecycle and resolution.
The Theory Corpus owns attributed, rights-reviewed strategic context.
Jin owns governed orchestration and conversational answer packets.
Decision Intelligence remains the sole persisted recommendation owner.
UI and export systems remain downstream projections.
```

Detailed schema, persistence, source, model, scoring, retention, and UI
decisions remain with their ordered future contracts.

## Phase 42B Boundary

Phase 42B may define only the Fixed Jin Regression Corpus Schema and
Deterministic Evaluation Contract.

It must remain contract-only and may not implement corpus files, evaluators,
models, prompts, Rules Layer behavior, model routing, corrections, Theory
Corpus ingestion, Jin answers, UI, schema, repositories, or dependencies.

## Forbidden Phase 42A Work

Phase 42A must not add production code, implementation tests, fixtures,
schema, migrations, repositories, providers, live network calls, model
downloads, model invocation, LLM prompts, theory ingestion, source
acquisition, correction activation, Jin answers, recommendation generation,
UI, file writing, dependencies, workflow changes, active-scope changes, or
constitution changes.

## Gate

Phase 42B may begin only after Phase 42A outside validation returns PASS or
PASS WITH REVIEW NOTES.
