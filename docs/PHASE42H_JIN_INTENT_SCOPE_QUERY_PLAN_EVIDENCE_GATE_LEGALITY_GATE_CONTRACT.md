# Phase 42H - Jin Intent, Scope, Query-Plan, Evidence-Gate, and Legality-Gate Contract

Status: contract only; implementation not authorized

## Validation Tuple

```text
phase_id: Phase42H
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42I
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42I is reserved for the Jin Writer, Auditor, Deterministic Finalizer, and
Answer-Packet Contract. It remains blocked until Phase 42H outside validation
returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42H defines the deterministic orchestration boundary between a sanitized
Jin request and the packet set that a future writer may receive.

This contract governs:

```text
request normalization boundary
typed primary and secondary intent resolution
immutable analytical scope binding
deterministic query planning
ordered retrieval requirements
applicable correction resolution inputs
Rules and legality check requests
evidence-gate sequence and claim permissions
partial, blocked, and abstention behavior
```

It does not retrieve evidence, calculate metrics, invoke models, write answer
text, audit drafts, finalize answer packets, persist data, or generate
recommendations.

## Authority

This contract is governed by:

1. `docs/CODIE_V2_CONSTITUTION.md`;
2. `docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md`;
3. the accepted Phase 42A cross-specification boundary;
4. the accepted Phase 42B fixed regression-corpus contract;
5. the accepted Phase 42C Rules authority contract;
6. the accepted Phase 42D model-profile, redaction, consent, and routing
   contract;
7. the accepted Phase 42E Correction Ledger core contract;
8. the accepted Phase 42F Theory source and citation contract;
9. the accepted Phase 42G reviewed claim, graph, translation, contradiction,
   and retrieval contract;
10. the accepted Phase 20 query-planner surface;
11. `docs/design_inputs/v2_intelligence_program/JIN_GITAXIAS_STRATEGIST_SUBSYSTEM_PROPOSAL.md`
    and `docs/design_inputs/v2_intelligence_program/JIN_CHAT_EXPERIENCE_PROPOSAL.md`
    as preserved design input only.

## Governing Invariants

```text
Intent classification does not answer the question.
Scope binding never broadens a narrow observation or correction.
Authority cannot be disabled for a material Rules or legality dependency.
Query plans request already-governed packets, not raw provider data.
Retrieval order defines precedence, not truth by position or implementation order.
Evidence gates read existing confidence and coverage; they do not invent them.
Legality gates cite Phase 42C authority and fail closed on material unknowns.
Theory remains attributed context and cannot increase empirical confidence.
Corrections apply at the narrowest valid scope and cannot override authority.
Community material remains community context.
Jin cannot create or overwrite persisted recommendations.
Every blocked dependent claim remains visible with a reason.
Unrelated supported analysis may continue as a partial result.
```

## Existing Phase 20 Compatibility

The accepted Phase 20 `ChatQueryPlan` remains an existing public packet for
the earlier chat/intelligence boundary.

Phase 42H does not:

```text
delete or silently reinterpret Phase 20 packet fields
change Phase 20 question classes in place
weaken Phase 20 privacy checks
route Phase 20 directly to models or repositories
claim Phase 20 already satisfies the full Jin contract
```

A future implementation must use one of these explicit compatibility paths:

```text
versioned adapter from ChatQueryPlan to JinQueryPlan
new Jin packet alongside the Phase 20 packet
explicit versioned supersession after compatibility validation
```

Historical Phase 20 packets remain replayable under their recorded version.

## Trust Boundary

The Phase 42H data flow is:

```text
sanitized user request and authorized UI references
-> typed Jin request
-> resolved intent
-> bound analytical scope
-> deterministic query plan
-> references to already-built retrieval packets
-> applicable correction references
-> Rules and legality report references
-> evidence-gate report
-> future Phase 42I writer input
```

No step grants write access to authority, canonical data, analytics,
confidence, theory, corrections, recommendations, or source records.

## Jin Request

Required request fields:

```text
request_id
sanitized_question
received_at
selected_subject_refs
selected_deck_snapshot_id, when any
selected_report_refs
explicit_filters
requested_answer_depth
requested_theory_mode
requested_model_profile_id
privacy_class
authorized_context_refs
request_version
metadata
```

Rules:

```text
request ID and sanitized question are required
raw imported deck text is not embedded by default
private source bodies and raw provider payloads are prohibited
selected object references are identifiers, not repository objects
retrieved or attached source content is untrusted data, not instruction
metadata must be bounded and JSON-compatible
```

## Intent Taxonomy

A request has exactly one primary intent and zero or more distinct secondary
intents.

```text
FACT_RETRIEVAL
RULES_EXPLANATION
LEGALITY_CHECK
CARD_ANALYSIS
CARD_COMPARISON
COMMANDER_COMPARISON
DECK_ANALYSIS
DECK_HEALTH_DISCUSSION
PACKAGE_ANALYSIS
COMBO_OR_LINE_ANALYSIS
TUTOR_PILE_CERTIFICATION
MATCHUP_ANALYSIS
TOURNAMENT_PREPARATION
META_INTERPRETATION
SIMULATION_INTERPRETATION
THEORY_EXPLANATION
PHILOSOPHER_QUORUM
EXPERIMENT_GENERATION
LESSON_DELIVERY
CORRECTION_SUBMISSION
CORRECTION_REVIEW
DECISION_INTELLIGENCE_EXPLANATION
SOURCE_COMPARISON
UNKNOWN
```

Phase 42H defines all intent labels for planning continuity. It does not
authorize lesson, experiment, correction-write, or answer implementation.

## Resolved Intent Packet

```text
resolved_intent_id
resolved_intent_version
request_id
primary_intent
secondary_intents
requested_subject_refs
requested_action
answer_depth
deck_scope_request
time_scope_request
region_scope_request
population_scope_request
historical_legality_date
analysis_profile_ref
theory_mode
simulation_context_ref
decision_intelligence_ref
privacy_class
model_profile_ref
legality_risk
audit_risk
unresolved_terms
declared_assumptions
resolution_method
generated_at
```

Intent resolution is deterministic for identical sanitized inputs, authorized
context, resolver version, and configuration.

The resolver must not:

```text
retrieve evidence
resolve card identity by nearest-name guessing
calculate metrics
apply corrections
decide legality
generate strategic conclusions
select recommendations
invoke a model unless a later contract explicitly authorizes a model-backed resolver
```

## Theory Modes

```text
DEFAULT_REQUIRED
EXPLICITLY_REQUIRED
EXPLICITLY_SUPPRESSED
NOT_APPLICABLE
UNAVAILABLE
```

Rules:

```text
substantive strategic analysis defaults to DEFAULT_REQUIRED
pure factual, Rules, legality, navigation, or administrative requests may use NOT_APPLICABLE
explicit user suppression is recorded, not inferred
retrieval failure produces UNAVAILABLE rather than silent omission
theory never substitutes for missing evidence or Rules authority
```

## Ambiguity Behavior

Presentation-only ambiguity may proceed with a visible declared assumption.

Ambiguity affecting any of the following blocks dependent claims:

```text
card identity
commander or partner identity
deck identity
deck snapshot
format
historical legality date
population
region
event
Rules object or interaction
```

Unrelated supported work may continue with a partial status. The unresolved
term and every blocked dependency remain visible.

## Scope Types

Hierarchical scopes:

```text
FORMAT
COMMANDER
PARTNER_PAIR
ARCHETYPE
DECK_IDENTITY
DECK_SNAPSHOT
EXPERIMENTAL_VARIANT
```

Orthogonal scopes:

```text
GLOBAL
REGIONAL
LOCAL_META
EVENT
DATE_WINDOW
HISTORICAL_DATE
SELECTED_POPULATION
SIMULATION_RUN
THEORY_SOURCE_SET
```

Scope values are explicit. `UNKNOWN`, `UNAVAILABLE`, `NOT_APPLICABLE`, and an
empty population are distinct.

## Scope Precedence

For user-context selection:

```text
1. explicit scope in the current request
2. explicitly selected UI object
3. selected immutable deck snapshot
4. applicable snapshot-level correction
5. applicable deck-level context
6. commander, partner-pair, or archetype context
7. format context
8. global context
```

This precedence orders user context only. It cannot override Class 0
authority, canonical identity, measured-evidence scope, or source provenance.

## Bound Scope Packet

```text
bound_scope_id
bound_scope_version
request_id
resolved_intent_id
primary_scope_type
primary_scope_key
format
commander_key
partner_key
archetype_key
deck_identity
deck_snapshot_id
deck_hash
commander_signature
snapshot_time
snapshot_source_ref
newer_snapshot_id, when any
region
event_id
date_window
historical_date
population_ref
simulation_run_id
theory_source_set_id
applicable_correction_scope_refs
unresolved_scope_items
provisional_scope
scope_caveats
generated_at
```

Every deck-specific answer plan binds to an immutable snapshot. When no
immutable snapshot exists, the plan is provisional or list-text analysis and
may not present snapshot-specific claims as replayable deck evidence.

## Scope Isolation

The binder must reject or caveat:

```text
deck correction applied commander-wide
local observation described globally
single event described as the metagame
partial partner match described as exact pair
commander aggregate described as one deck
current legality applied to a historical date
simulation run described as tournament evidence
theory source set described as measured population
```

## Jin Query Plan

Required fields:

```text
plan_id
plan_version
plan_hash
request_id
resolved_intent_id
bound_scope_id
required_retrievals
optional_retrievals
authority_checks
identity_checks
metric_refs_requested
unified_evidence_refs_requested
theory_queries
correction_scopes
conflict_queries
legality_checks
unsupported_dependency_checks
decision_intelligence_reads
simulation_reads
privacy_policy_ref
model_route_request
future_writer_profile_ref
future_auditor_policy_ref
expected_output_sections
allowed_claim_classes
failure_policy
generated_at
```

The plan hash is calculated from canonical semantic inputs and version refs.
Volatile timestamps do not alter semantic plan identity.

## Required Retrieval Precedence

```text
1. card and object identity
2. Rules and legality authority
3. immutable deck snapshot
4. canonical observations
5. measured evidence and Unified Evidence
6. existing Decision Intelligence output, when explicitly referenced
7. source conflicts
8. simulator reports
9. user context
10. applicable corrections
11. primer and community context
12. reviewed Theory Corpus packet
```

This list defines authority and interpretation precedence. A future
implementation may batch independent reads but may not weaken the precedence
or permit a lower class to override a higher one.

## Retrieval Request Boundary

The plan requests immutable packet references from accepted services.

It must not request:

```text
raw provider payloads
source or analytics tables
repository objects
SQL
private source bodies
unbounded filesystem content
live provider access
new analytics calculations
new simulator execution
new Decision Intelligence output
graph mutation
correction activation
recommendation generation
```

Provider acquisition and live retrieval require their own accepted contracts.

## Retrieval Bundle References

A future orchestration input may reference:

```text
authority_refs
card_identity_refs
legality_refs
canonical_observation_refs
measured_evidence_refs
unified_evidence_refs
decision_intelligence_refs
simulator_refs
source_conflict_refs
user_context_refs
correction_refs
primer_context_refs
community_context_refs
theory_retrieval_packet_refs
missing_required_refs
missing_optional_refs
source_coverage
retrieval_timestamp
```

Each reference retains its evidence class, version, scope, provenance, and
caveats. Bare dashboard values or copied prose are not sufficient.

## Measured-Evidence Reference Requirements

Every metric reference needed by the plan exposes:

```text
metric name and formula version
canonical population
date window
region
commander, partner, or deck scope
placement scope
sample size
matching records
available eligible records
coverage ratio
filters and exclusions
generated time
known caveats
```

Phase 42H reads existing confidence, coverage, and source-agreement records.
It does not calculate or raise them.

## Correction Resolution Inputs

Applicable correction references come from Phase 42E and preserve:

```text
correction ID and version
status
category
target and scope
authority class
evidence refs
affected subsystem
effective time
review or revalidation state
```

Rules:

```text
narrowest valid scope applies
deck correction does not become global theory
user preference does not become factual correction
correction cannot override Oracle, Rules, or identity without authority
disputed or stale correction remains visible
runtime application never mutates the corrected source object
```

Phase 42H does not create, review, activate, or persist corrections.

## Legality Check Request

The query plan names every material authority check:

```text
card identity
format legality
date-aware ban status
historical release availability
commander color identity
commander eligibility
zone legality
deck-construction legality
card-face identity
declared interaction legality
cost, target, and timing requirements
summoning sickness
ability ownership
supported Rules coverage
```

## Legality Report Reference

The accepted Phase 42C service owns the authoritative result. Phase 42H
requires a report reference exposing:

```text
legality_report_id
legality_report_version
status
format
effective_date
cards_checked
unresolved_cards
banned_cards
unavailable_cards
color_identity_violations
deck_construction_violations
interaction_checks
unsupported_rules_questions
authority_package_refs
blocked_claim_ids
warnings
generated_at
```

Statuses:

```text
LEGAL
LEGAL_WITH_WARNINGS
ILLEGAL
UNRESOLVED
NOT_APPLICABLE
```

Phase 42H does not calculate a legality verdict or paraphrase Rules text as
authority.

## Legality Blocking Rules

Dependent claims are blocked when they rely on:

```text
illegal deck additions presented as legal
banned or unavailable cards under the selected historical date
off-color identity
unresolved object identity
unsupported card behavior
unsupported simulator action
interaction claims without sufficient authority
unknown or stale authority packages
```

The system may explain a block later. It may not silently repair an illegal or
unsupported line by substituting another card, action, or rule.

## Evidence Gate Sequence

```text
G0 Identity Gate
G1 Scope Gate
G2 Authority Gate
G3 Provenance Gate
G4 Coverage Gate
G5 Legality Gate
G6 Conflict Gate
G7 Claim-Class Gate
G8 Recommendation-Boundary Gate
G9 Privacy Gate
```

Each gate returns:

```text
PASS
WARN
BLOCK
NOT_APPLICABLE
```

Each gate result preserves:

```text
gate_id
gate_version
status
checked_claim_ids
allowed_claim_ids
blocked_claim_ids
reason_codes
required_labels
mandatory_caveat_ids
required_conflict_ids
authority_refs
evidence_refs
generated_at
```

## G0 Identity Gate

Blocks dependent claims for unresolved:

```text
card
commander
partner
deck
snapshot
alias
Rules object
```

## G1 Scope Gate

Blocks or requires narrower wording when evidence scope differs from the claim
scope.

It prevents local, historical, commander-wide, partner-pair, event, deck, and
snapshot scopes from being presented as interchangeable.

## G2 Authority Gate

Requires the appropriate Class 0 packet for:

```text
Oracle text and canonical identity
Rules behavior
legality and ban status
recognized Commander Spellbook combo records
Scryfall Tagger labels within scoped ontology authority
```

Agreement among lower classes cannot override Class 0.

## G3 Provenance Gate

Blocks:

```text
untraceable metric references
orphaned source summaries
unattributed theory claims
missing correction provenance
unsupported community restatements
```

## G4 Coverage Gate

Warns or blocks according to the source metric's own declared policy when:

```text
sample size is below its declared minimum
coverage is materially incomplete
unsupported cards affect the result
eligible population is unknown
one narrow source supports a broad claim
source freshness is insufficient
```

This gate does not invent confidence or substitute an arbitrary threshold.

## G5 Legality Gate

Uses the accepted Legality Report reference to block illegal, unresolved, or
authority-unsupported dependent claims.

## G6 Conflict Gate

Requires visible disclosure of material:

```text
source conflicts
measured-evidence conflicts
theory disagreements
correction conflicts
Rules conflicts
scope conflicts
```

It blocks only when the conflict prevents a defensible scoped statement.

## G7 Claim-Class Gate

Every material future claim receives one class:

```text
AUTHORITY_FACT
CANONICAL_OBSERVATION
MEASURED_EVIDENCE
DECISION_INTELLIGENCE_RESULT
ATTRIBUTED_CONTEXT
THEORY_APPLICATION
USER_CONTEXT
INFERENCE
SPECULATION
UNSUPPORTED
```

`UNSUPPORTED` cannot enter a future direct answer. `INFERENCE` and
`SPECULATION` require explicit labels and cannot be persisted as evidence.

## G8 Recommendation-Boundary Gate

Permitted future references:

```text
Decision Intelligence recommends X under profile Y.
X is a test candidate based on these observations.
The available evidence favors testing X.
```

Blocked:

```text
Jin recommends X without a Decision Intelligence record.
X is the correct card.
This metric proves X caused the deck to win.
Theory proves X belongs in the deck.
```

Phase 42H does not generate these sentences. It defines the permission
boundary that Phase 42I must enforce.

## G9 Privacy Gate

Blocks any planned route that exceeds:

```text
Phase 42F source rights
Phase 42D profile policy
explicit user consent
authorized data classification
local-only requirements
```

A cloud route is denied when any required item is not cloud-eligible. The
planner may select an eligible local fallback; it may not weaken redaction or
rights policy.

## Evidence Gate Report

```text
evidence_gate_report_id
evidence_gate_report_version
request_id
plan_id
bound_scope_id
gate_results
overall_status
allowed_claim_classes
blocked_claim_ids
mandatory_caveat_ids
required_conflict_ids
confidence_ceiling_refs
legality_report_ref
missing_required_refs
unsupported_dependency_refs
privacy_route_status
future_audit_requirement
generated_at
```

Overall statuses:

```text
READY
PARTIAL
BLOCKED
FAILED
```

`READY` and `PARTIAL` may proceed to a future writer. `BLOCKED` produces only
a structured block packet. `FAILED` indicates infrastructure or validation
failure and cannot masquerade as an evidence result.

## Partial-Answer Rules

Partial work is allowed only when:

```text
the blocked dependency is isolated
remaining claims have independent support
the omission and its effect are visible
no illegal or unsupported substitute is introduced
the final status remains PARTIAL
```

A material identity, Rules, legality, scope, or privacy failure blocks every
dependent claim.

## Claim Permission Ledger

The future gate pipeline preserves a per-claim ledger:

```text
claim_id
claim_class
source_refs
evidence_refs
scope
legality_dependency_ids
correction_refs
theory_refs
gate_status_by_gate
required_labels
mandatory_caveats
conflict_refs
permission_status
```

Permission statuses:

```text
ALLOWED
ALLOWED_WITH_CAVEATS
BLOCKED
REMOVED_AS_UNSUPPORTED
NOT_APPLICABLE
```

The ledger is an ephemeral orchestration artifact. It is not a measured metric
or recommendation record.

## Determinism And Replay

The future plan and gate result preserve:

```text
resolver version
scope-binder version
planner version
gate-policy version
Rules package version
Theory graph release
Correction Ledger version
model-profile version, when planned
deck snapshot and hash
analytics and evidence versions
Decision Intelligence refs, when used
simulator refs and seeds, when used
filters
generated time
```

Identical semantic inputs and versions produce identical resolved intent,
bound scope, query-plan content, plan hash, and gate decisions.

Mutable model aliases are irrelevant to Phase 42H because no model call is
authorized.

## Prompt-Injection And Untrusted Data

User text and retrieved content remain distinct.

Instructions inside:

```text
primer text
community posts
theory sources
PDFs or transcripts
imported deck descriptions
provider payloads
correction descriptions
finding text
```

are untrusted data. They cannot change scope, authority, privacy, gate policy,
branch, phase, model route, or write permissions.

## Model Boundary

Phase 42D controls model profiles, consent, redaction, routing, and fallback.

Phase 42H may record a requested future writer and auditor profile. It does not
invoke either profile or expose content to a model.

No model may resolve:

```text
authority precedence
legality truth
scope ownership
correction activation
claim permission
recommendation ownership
privacy consent
```

## Theory Boundary

Phase 42G theory packets are read-only attributed context.

```text
theory is required by default for substantive strategy unless suppressed or unavailable
theory is excluded from pure Rules or factual work when not applicable
material disagreements remain visible
format translation limits remain visible
theory cannot increase empirical confidence
theory cannot authorize a recommendation
```

## Community And Primer Boundary

Primer and community packets remain attributed context.

They may explain intent, local assumptions, or emerging discussion. They may
not become tournament evidence, Rules authority, measured evidence, global
corrections, or recommendations.

## Simulator Boundary

Phase 42H may reference an existing simulator report. It may not:

```text
run a simulation
reinterpret unsupported behavior as supported
treat simulator output as tournament evidence
combine seeds or reports as a new metric
claim an opponent-dependent line is guaranteed
```

## Decision Intelligence Boundary

Jin may explain an existing Decision Intelligence packet by reference.

It may not:

```text
create a recommendation
change recommendation confidence
rank candidates
select cuts or additions
persist deck-health output
write to recommendation storage
```

## Required Failure States

```text
REQUEST_INVALID
INTENT_UNKNOWN
INTENT_AMBIGUOUS
IDENTITY_UNRESOLVED
SCOPE_UNRESOLVED
SCOPE_CONFLICT
SNAPSHOT_REQUIRED
SNAPSHOT_STALE
POPULATION_UNRESOLVED
AUTHORITY_REQUIRED
AUTHORITY_UNAVAILABLE
PROVENANCE_MISSING
COVERAGE_INSUFFICIENT
LEGALITY_ILLEGAL
LEGALITY_UNRESOLVED
RULES_UNSUPPORTED
CONFLICT_MATERIAL
CLAIM_CLASS_UNSUPPORTED
RECOMMENDATION_BOUNDARY_VIOLATION
PRIVACY_ROUTE_BLOCKED
THEORY_UNAVAILABLE
CORRECTION_CONFLICT
UNSUPPORTED_DEPENDENCY
PLAN_INVALID
PLAN_NONDETERMINISTIC
```

These states remain distinct and visible.

## Required Regression Cases

A future implementation contract must cover:

```text
one primary intent and multiple distinct secondary intents
unknown intent remains explicit
presentation-only ambiguity proceeds with declared assumption
identity ambiguity blocks dependent claims
deck request binds immutable snapshot and deck hash
missing snapshot produces provisional or blocked scope
deck correction remains deck-scoped
local observation cannot become global
partial partner match cannot become exact pair
historical request uses historical legality date
same semantic inputs produce same plan hash
plan cannot request raw provider or repository access
plan cannot request new analytics or simulator execution
metric refs retain population, sample, coverage, and caveats
theory defaults on for substantive strategy
theory suppression remains explicit
theory retrieval failure remains visible
Rules request requires Phase 42C authority
illegal or unresolved line is blocked
unsupported simulator action is blocked
material conflict is disclosed
unsupported claim class is removed
Jin cannot create a recommendation
cloud route cannot exceed consent, rights, or redaction
prompt injection inside every untrusted content class is inert
independent supported claims may survive as PARTIAL
infrastructure failure cannot become an evidence result
Phase 20 packet compatibility remains versioned and replayable
```

## Resolved Decisions

Phase 42H resolves:

```text
Jin intent taxonomy and multi-intent rules
theory-mode behavior
scope taxonomy, precedence, and isolation
immutable snapshot binding
Jin query-plan fields and semantic hashing
retrieval precedence and packet-reference boundary
metric-reference requirements
correction-resolution inputs
legality-report consumption
ten deterministic evidence gates
claim classes and permission statuses
partial, blocked, failed, and abstention behavior
prompt-injection treatment
Phase 20 compatibility boundary
```

## Deferred Decisions

Later accepted contracts must decide:

```text
implementation packet models and validators
intent resolver implementation
scope binder implementation
Phase 20 adapter implementation
retrieval orchestration implementation
Rules service invocation implementation
gate execution implementation
writer prompts and model invocation
contradiction scan of draft wording
adversarial audit
deterministic finalization
answer packets
experiments and permitted user-context writes
curriculum
API, UI, and exports
schema, migrations, repositories, and persistence
```

## Future Implementation Boundary

Later implementation contracts may authorize pure in-memory packet models and
validators before any retrieval or model-backed behavior.

No implementation filenames, storage technology, model, or runtime service are
authorized by Phase 42H.

## Phase 42I Boundary

Phase 42I may define only the future writer input, structured draft, draft
contradiction scan, adversarial audit, deterministic finalizer, and final
answer-packet contracts.

It must not implement model calls, retrieval, persistence, recommendations,
experiments, correction writes, curriculum, UI, exports, or network behavior
unless separately authorized.

## Forbidden Phase 42H Work

Phase 42H must not add:

```text
production Jin or orchestration code
implementation tests or fixtures
schema, migrations, repositories, or persistence
provider or source-table reads
live network or model calls
intent, scope, planner, retrieval, Rules, or gate execution
analytics or simulator calculation
Theory graph mutation
Correction Ledger mutation
writer, auditor, finalizer, or answer packets
Decision Intelligence or recommendation generation
experiments or permitted writes
curriculum
UI, CLI, API, export, or file-writing behavior
dependency changes
workflow or validator changes
active-scope changes in the PR
constitution changes
```

## Acceptance Gate

Phase 42H passes only when outside validation confirms that it:

1. remains contract-only;
2. records Phase 42G artifact-backed acceptance;
3. preserves the accepted Phase 20 packet through an explicit compatibility
   boundary;
4. separates intent resolution from retrieval and conclusions;
5. binds deck-specific work to immutable snapshot scope;
6. prevents scope leakage;
7. plans only governed packet references;
8. preserves authority and retrieval precedence;
9. consumes rather than calculates metrics, confidence, legality, theory, and
   corrections;
10. defines all ten evidence gates and per-claim permissions;
11. blocks illegal, unsupported, private, or untraceable dependent claims;
12. permits only visibly partial independent work;
13. preserves Theory, community, simulator, Decision Intelligence, and model
    boundaries;
14. treats all retrieved content as untrusted data; and
15. keeps Phase 42I blocked.

Phase 42I may begin only after Phase 42H outside validation returns PASS or
PASS WITH REVIEW NOTES.
