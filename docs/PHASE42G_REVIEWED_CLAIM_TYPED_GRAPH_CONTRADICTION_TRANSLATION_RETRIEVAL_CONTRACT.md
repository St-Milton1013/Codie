# Phase 42G - Reviewed Claim, Typed Graph, Contradiction, Translation, and Retrieval Contract

Status: contract only; implementation not authorized

## Validation Tuple

```text
phase_id: Phase42G
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42H
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42H is reserved for the Jin Intent, Scope, Query-Plan,
Evidence-Gate, and Legality-Gate Contract. It remains blocked until Phase 42G
outside validation returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42G defines how approved Phase 42F provenance may support reviewed,
attributed theory objects without turning theory into authority, measured
evidence, or recommendation output.

This contract governs:

```text
atomic theory claims and claim review
source-specific definitions and normalized concepts
typed, provenance-bearing graph relationships
format transferability and reviewed translations
material disagreement and contradiction records
scoped empirical support or conflict references
immutable graph releases
deterministic, ephemeral retrieval packets
```

It does not implement source acquisition, extraction, graph storage,
embeddings, retrieval ranking, models, Jin, curriculum, UI, exports, or
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
8. the accepted Phase 42F source, rights, immutable version, and citation
   contract;
9. `docs/design_inputs/v2_intelligence_program/CODIE_V2_THEORY_CORPUS_ATTRIBUTED_KNOWLEDGE_GRAPH_PROPOSAL.md`
   as preserved design input only.

## Governing Invariants

```text
Theory contextualizes evidence; it does not replace authority or measurement.
Authors are attribution subjects, not canonical truth authorities.
Every approved claim resolves to an accepted source version and exact anchor.
Claims are atomic and preserve modality, assumptions, scope, and limitations.
Definitions remain source-specific even when concepts are normalized.
Every substantive graph edge is typed, versioned, reviewed, and sourced.
Historical or cross-format theory requires explicit transferability review.
Contradictions remain visible and are never resolved by fame or author count.
Empirical links retain population, time, metric, and coverage scope.
Retrieval is deterministic, rights-aware, scope-aware, and mutation-free.
Insufficient coverage produces abstention rather than invented commentary.
Theory records never directly produce recommendations.
```

## Trust Boundary

The governed sequence is:

```text
accepted Phase 42F source version and exact citation anchor
-> candidate atomic claim
-> attribution review
-> citation review
-> scope review
-> translation review, when required
-> contradiction review
-> approve, approve with limits, reject, defer, or supersede
-> immutable graph release
-> deterministic ephemeral retrieval packet
-> future Jin gates and answer assembly
```

Phase 42G defines this sequence but implements none of it.

## Reviewed Claim Types

Claim labels remain distinct:

```text
DIRECT_THEORY
DEMONSTRATED_APPLICATION
LATER_SYNTHESIS
JIN_INFERENCE
FORMAT_TRANSLATION
EMPIRICAL_SUPPORT
EMPIRICAL_CONFLICT
UNRESOLVED
```

Rules:

```text
DIRECT_THEORY requires a reviewed primary-theory or primary-definition source.
DEMONSTRATED_APPLICATION records what a source demonstrates, not a universal rule.
LATER_SYNTHESIS preserves the synthesis source and material predecessor refs.
JIN_INFERENCE is never an approved attributed author claim.
FORMAT_TRANSLATION remains separate from its source claim.
EMPIRICAL_SUPPORT and EMPIRICAL_CONFLICT reference scoped measured evidence.
UNRESOLVED cannot support an unqualified factual or strategic assertion.
```

## Atomic Claim Packet

Every future claim packet preserves:

```text
claim_id
claim_version
claim_text
claim_type
polarity
modality
subject_concept_ids
source_version_ids
citation_anchor_ids
source_role_by_anchor
attributed_person_ids
attribution_chain_id, when any
source_scope
format_scope
deck_scope, when any
time_scope
assumption_ids
limitation_ids
example_ids
counterexample_ids
translation_ids
disagreement_ids
supporting_evidence_refs
conflicting_evidence_refs
review_status
review_decision_ids
created_at
supersedes_claim_id, when any
record_version
metadata
```

Claim text contains one independently reviewable proposition. Definitions,
applications, limitations, and conclusions are separate objects when they can
be reviewed independently.

Modality must preserve the source's strength:

```text
IS
MAY
CAN
USUALLY
SHOULD
MUST
EXAMPLE_ONLY
HYPOTHESIS
```

No extractor, reviewer, model, or serializer may strengthen a source's
modality.

## Claim Review Lifecycle

Sequential review states:

```text
CANDIDATE
ATTRIBUTION_REVIEW
CITATION_REVIEW
SCOPE_REVIEW
TRANSLATION_REVIEW
CONTRADICTION_REVIEW
APPROVED
PUBLISHED_IN_GRAPH
```

Alternate states:

```text
NEEDS_SOURCE
NEEDS_PRIMARY_SOURCE
NEEDS_RIGHTS_CLEARANCE
LIMITED
REJECTED
SUPERSEDED
WITHDRAWN
REVALIDATION_REQUIRED
```

Invariants:

```text
candidate does not mean approved
approved does not mean transferable
published does not mean automatically retrievable
superseded records remain queryable for historical provenance
discovery-only material cannot support DIRECT_THEORY
unavailable or withdrawn source state triggers the Phase 42F policy
```

Required review decision fields:

```text
review_id
reviewed_object_type
reviewed_object_id
review_type
decision
reason
required_changes
reviewer_ref
reviewed_at
source_version_ids
target_graph_release_id
review_version
```

Allowed decisions:

```text
approve
approve_with_limits
reject
defer
supersede
require_revalidation
```

## Claim Extraction Prohibitions

A future implementation must not:

```text
rewrite an author into a stronger position
treat a rhetorical question as a claim without context
infer a universal rule from one example
merge distinct definitions into a synthetic consensus
infer a complete philosophy from a decklist
use a source map or bibliography as proof of a discovered claim
approve title-only or discovery-only material
invent missing dates, speakers, or attribution
merge pseudonyms or identities without evidence
create direct quotations from machine summaries
assign target-format applicability without transferability review
promote model output or Jin inference into an attributed source claim
```

## Theory Node Types

Phase 42G governs these theory nodes:

```text
Claim
Definition
Concept
Framework
Example
Counterexample
Limitation
Assumption
FormatTranslation
Disagreement
AttributionChain
Application
Hypothesis
EmpiricalEvaluation
ReviewDecision
GraphRelease
```

Phase 42F person, organization, work, edition, source asset, source version,
segment, citation-anchor, and rights records are referenced by ID. Phase 42G
does not recreate or mutate them.

Curriculum nodes and user-learning records are outside Phase 42G.

## Concepts And Definitions

Normalized concepts support lookup and comparison. They do not erase
source-specific meanings.

Required concept fields:

```text
concept_id
concept_version
preferred_name
aliases
description
parent_concept_ids
child_concept_ids
router_tags
definition_ids
disagreement_ids
format_translation_ids
status
ontology_version
```

Required definition fields:

```text
definition_id
definition_version
concept_id
definition_text
claim_id
attributed_person_ids
source_version_ids
citation_anchor_ids
format_scope
time_scope
distinguishing_features
known_conflict_ids
review_status
```

Definitions from different sources remain distinct. A normalized concept may
connect them for retrieval, but it may not emit a blended definition unless a
separately attributed synthesis claim has been reviewed.

## Typed Graph Relationships

Substantive relationships use an explicit edge type.

### Provenance And Attribution

```text
ASSERTED_IN
DEFINED_IN
DEMONSTRATED_IN
ORIGINATED_BY
EXPOUNDED_BY
LATER_SYNTHESIZED_BY
ATTRIBUTED_TO
MISATTRIBUTED_TO
DERIVED_FROM
SUMMARIZES
RESTATES
```

### Conceptual

```text
INSTANCE_OF
PART_OF
REQUIRES
ASSUMES
ENABLES
CONVERTS_TO
QUALIFIES
LIMITS
GENERALIZES
SPECIALIZES
OVERLAPS_WITH
DISTINCT_FROM
PRECEDES
FOLLOWS
```

### Evidence And Disagreement

```text
SUPPORTS
CONTRADICTS
EMPIRICALLY_SUPPORTS
EMPIRICALLY_CONFLICTS
APPARENTLY_CONFLICTS
REFINES
SUPERSEDES
REJECTS
UNRESOLVED_WITH
```

### Translation And Application

```text
APPLIES_TO_FORMAT
TRANSLATED_FROM
TRANSLATED_TO
VALIDATED_IN_FORMAT
REJECTED_IN_FORMAT
APPLIED_TO_DECK
APPLIED_TO_CARD
APPLIED_TO_PACKAGE
EXEMPLIFIES
COUNTEREXAMPLE_TO
```

An untyped `RELATED_TO` relationship cannot carry a substantive claim.

Every edge preserves:

```text
edge_id
edge_version
edge_type
from_node_id
to_node_id
source_claim_id
citation_anchor_ids
scope
format_scope
deck_scope
time_scope
evidence_class
confidence
review_status
review_decision_ids
created_in_graph_release_id
deprecated_in_graph_release_id, when any
reviewed_by
reviewed_at
metadata
```

An edge with no source claim, citation, review, or scope cannot enter an
approved graph release.

## Attribution Chains

Attribution roles remain distinct:

```text
originator
published_expositor
later_synthesizer
translator
demonstrated_application
curator
unresolved
```

The earliest locally known source does not automatically identify the
originator. Primary source outranks synthesis for attribution, but not
automatically for strategic correctness.

## Transferability States

```text
NATIVE
DIRECTLY_APPLICABLE
TRANSLATION_REQUIRED
TRANSLATION_PROPOSED
TRANSLATION_REVIEWED
EMPIRICALLY_SUPPORTED
EMPIRICALLY_CONFLICTED
REJECTED
INSUFFICIENT
```

Transfer state is target-format specific. Approval of a source claim does not
grant automatic cEDH applicability.

## Format Translation

Every translation packet preserves:

```text
translation_id
translation_version
source_claim_id
source_formats
target_format
translated_claim_text
preserved_elements
changed_assumptions
new_assumptions
multiplayer_effects
commander_zone_effects
singleton_effects
mulligan_effects
tutor_effects
free_interaction_effects
turn_order_effects
priority_effects
shared_policing_effects
table_politics_effects
win_window_effects
rules_or_card_pool_changes
deck_specific_conversion_requirements
required_evidence
supporting_evidence_refs
conflicting_evidence_refs
limitation_ids
review_status
review_decision_ids
reviewed_by
reviewed_at
```

No historical or cross-format claim enters automatic target-format retrieval
at full relevance until a translation is reviewed. A proposed translation may
be retrieved only through an explicit lens with visible limitations.

Rules and legality dependencies resolve through Phase 42C. A Rules conflict
blocks the affected application; it does not silently rewrite the historical
claim.

## Limitations

Limitations may apply to:

```text
work
source version
claim
definition
framework
example
translation
application
retrieval
rights
```

Required fields:

```text
limitation_id
limitation_version
limitation_type
description
applies_to_node_ids
severity
scope
blocks_retrieval
blocks_format_translation
citation_anchor_ids
review_status
```

Severity:

```text
INFORMATIONAL
MATERIAL
BLOCKING
```

Material and blocking limitations remain visible in every affected retrieval
packet.

## Disagreement And Contradiction

Disagreement types:

```text
DEFINITIONAL
CONTEXTUAL
EMPIRICAL
FORMAT_SPECIFIC
PRIORITY_BASED
APPARENT
ATTRIBUTION
TEMPORAL
UNRESOLVED
```

Required fields:

```text
disagreement_id
disagreement_version
topic_id
claim_a_id
claim_b_id
conflict_type
overlapping_scope
differing_assumptions
format_scope
time_scope
materiality
resolution_status
resolution_note
supporting_evidence_refs
review_status
review_decision_ids
```

Resolution states:

```text
PRESERVED
SCOPE_PARTITIONED
APPARENTLY_RECONCILED
EMPIRICALLY_FAVORS_A
EMPIRICALLY_FAVORS_B
SUPERSEDED
UNRESOLVED
```

Resolution rules:

```text
Rules authority defeats theory on Rules facts.
Current Oracle text defeats historical card interpretation.
Primary source outranks synthesis for attribution, not strategic correctness.
Empirical support applies only within its recorded population and time scope.
Author count, fame, followers, and prestige never resolve a disagreement.
Definitional conflicts remain definitional.
Different game-state assumptions are scope-partitioned when supported.
Unresolved material conflicts remain visible.
```

A future contradiction scanner may propose candidates. It may not approve,
resolve, suppress, or rewrite them autonomously.

## Empirical Evaluation Boundary

Theory may reference approved measured-evidence objects through:

```text
EMPIRICALLY_SUPPORTS
EMPIRICALLY_CONFLICTS
```

Each reference preserves:

```text
evidence_object_id
metric_id and version
population or deck-snapshot scope
time window
sample size
coverage ratio
filters
caveat_ids
agreement or conflict direction
```

An empirical link does not convert theory into measured evidence. It also does
not prove causation or strategic optimality.

## Graph Releases

Approved theory becomes retrievable only through an immutable graph release.

Required release fields:

```text
graph_release_id
graph_release_version
parent_graph_release_id, when any
claim_version_ids
node_version_ids
edge_version_ids
translation_version_ids
disagreement_version_ids
review_decision_ids
rights_snapshot_refs
ontology_version
router_compatibility_version
content_hash
generated_at
release_status
validation_report_id
```

Graph releases are deterministic for identical ordered inputs and versions.
Corrections, new review decisions, rights changes, or source changes create a
new release or block publication. Historical releases remain identifiable.

Phase 42E Correction Ledger records do not overwrite attributed theory.
Accepted claim corrections create new claim versions and graph releases with
the correction reference visible.

## Retrieval Inputs

A future retrieval request may contain:

```text
query_id
question
intent
topic_ids
target_format
deck_snapshot_id
card_refs
commander_refs
package_refs
rules_dependency_ids
requested_theorist_ids
excluded_theorist_ids
requested_mode
time_scope
theory_opt_out
graph_release_id
router_profile_id
```

Requested modes:

```text
automatic
explicit_lens
council
debate
```

Curriculum mode is deferred to a curriculum contract.

## Retrieval Stages

```text
intent and scope input
-> topic and format matching
-> exact concept and claim lookup
-> review-status eligibility
-> format-transfer eligibility
-> rights and privacy filter
-> deck-context applicability filter
-> contradiction expansion
-> diversity and duplicate control
-> deterministic theory packet assembly
```

Phase 42G defines this future pipeline but does not implement it.

## Retrieval Eligibility

Automatic retrieval may include only:

```text
approved or approved-with-limits claim versions
published graph-release members
rights-eligible source references
native or reviewed-transfer claims for the target format
claims whose blocking limitations do not apply
scoped empirical refs that remain available
```

Explicit-lens retrieval may include limited or translation-proposed material
only when its review state and limitations remain visible.

Automatic retrieval excludes:

```text
candidate, deferred, rejected, withdrawn, or revalidation-required claims
title-only or discovery-only material
untranslated historical claims presented as target-format guidance
rights-blocked content
unknown or invalid citation anchors
Jin inference presented as source theory
community material presented as reviewed theory
```

## Retrieval Ordering And Diversity

Future router configuration must be versioned, deterministic, inspectable, and
testable.

Ordering may consider:

```text
topic match
target-format fit
review fitness
application fit
citation quality
framework diversity
material contradiction coverage
```

Ordering may not consider fame, popularity, follower count, author count, or
prestige.

Duplicate restatements collapse into an attribution chain without erasing the
individual source records. A materially different framework or known
contradiction is included when eligible and relevant.

Numeric weights and ranking implementation are deferred.

## Retrieval Packet

Every future theory retrieval packet preserves:

```text
retrieval_packet_id
retrieval_packet_version
query_id
graph_release_id
router_profile_id and version
target_format
deck_snapshot_id, when used
selected_claim_version_ids
selected_definition_ids
selected_concept_ids
selected_translation_ids
selected_disagreement_ids
selected_limitation_ids
selected_source_version_ids
selected_citation_anchor_ids
empirical_evidence_refs
excluded_candidate_reasons
insufficient_coverage_topics
rights_and_redaction_summary
generated_at
```

The packet is ephemeral and read-only. It never mutates the graph, source
registry, Correction Ledger, evidence, or user deck.

The packet preserves why items were included or excluded. It must not contain
restricted source text, private notes, model prompts, credentials, or
unbounded repository content.

## Retrieval Failure And Abstention

Required states:

```text
INSUFFICIENT_CORPUS_COVERAGE
NO_RIGHTS_ELIGIBLE_SOURCE
NO_REVIEWED_CLAIM
FORMAT_TRANSLATION_REQUIRED
MATERIAL_CONTRADICTION_UNRESOLVED
RULES_DEPENDENCY_BLOCKED
SOURCE_REVALIDATION_REQUIRED
GRAPH_RELEASE_INVALID
```

These states remain visible. They do not trigger invented claims, hidden
fallback theory, or automatic recommendation language.

## Community Boundary

Community and RSS material remains community context or discovery until its
linked work, identity, rights, attribution, claim, and transferability pass
the applicable reviews.

Popularity, votes, repost count, and discussion volume do not promote a
candidate or resolve a disagreement.

## Rules Boundary

Phase 42C remains authoritative for current Rules, Oracle, and legality facts.

Theory records may cite historical rules context. They may not override a
current Rules package. A failed Rules dependency blocks the affected
translation or application and remains visible.

## Correction Ledger Boundary

Phase 42E corrections remain separately attributed and scoped.

```text
user correction is not an author claim
correction confidence is not theory confidence
deck-scoped correction does not change global theory
accepted correction creates a new version rather than silent mutation
correction history remains visible
```

## Model And Jin Boundary

Phase 42D controls every model route. Phase 42H will define Jin's consumption
of theory packets.

No model or Jin process may:

```text
approve a claim
change attribution
alter source or rights identity
publish a graph release
resolve a disagreement
approve a translation
mutate a retrieval packet
turn theory into authority, measured evidence, or recommendation output
```

Prompt injection or executable instructions inside source or finding text are
treated as untrusted quoted data.

## Privacy And Rights

Retrieval is constrained by the Phase 42F rights snapshot and Phase 42D route.

```text
private source text remains local
unknown-rights text is not indexed or transmitted
cloud use requires rights eligibility and explicit profile consent
retrieval packets minimize source text
logs do not expose source text, private paths, or account identifiers
exports require a later contract and explicit rights eligibility
```

## Recommendation And Evidence Boundary

Theory retrieval cannot directly produce:

```text
recommendations
deck-health findings
replacement suggestions
candidate ranking for deck changes
confidence as measured evidence
tournament or frequency metrics
rules conclusions
simulator conclusions
```

Future Jin output must pass the accepted evidence, legality, confidence, and
Decision Intelligence boundaries before decision-bearing output is possible.

## Required Validation States

```text
CLAIM_NOT_ATOMIC
CLAIM_MODALITY_STRENGTHENED
CLAIM_SOURCE_MISSING
CLAIM_ANCHOR_MISSING
CLAIM_ATTRIBUTION_UNRESOLVED
CLAIM_SCOPE_UNRESOLVED
CLAIM_REVALIDATION_REQUIRED
DEFINITION_MERGE_PROHIBITED
EDGE_TYPE_INVALID
EDGE_PROVENANCE_MISSING
EDGE_SCOPE_MISSING
TRANSLATION_REQUIRED
TRANSLATION_UNREVIEWED
TRANSLATION_RULES_BLOCKED
DISAGREEMENT_MATERIAL
DISAGREEMENT_UNRESOLVED
EMPIRICAL_SCOPE_MISSING
GRAPH_RELEASE_INVALID
GRAPH_RELEASE_NONDETERMINISTIC
RETRIEVAL_RIGHTS_BLOCKED
RETRIEVAL_SCOPE_BLOCKED
INSUFFICIENT_CORPUS_COVERAGE
MUTATION_PROHIBITED
RECOMMENDATION_BOUNDARY_VIOLATION
```

Unknown states remain visible and fail closed for approval, publication, or
automatic retrieval.

## Required Regression Cases

A future implementation contract must cover:

```text
compound claim is rejected as non-atomic
source modality is not strengthened
approved claim requires accepted source version and exact anchor
source map cannot support DIRECT_THEORY
decklist application cannot become universal author theory
machine summary cannot become a direct quotation
definitions remain source-specific under one normalized concept
substantive untyped edge is rejected
edge without claim, anchor, scope, or review is rejected
earliest local source does not automatically establish originator
untranslated historical claim is excluded from automatic cEDH retrieval
reviewed translation preserves changed assumptions and limitations
Rules conflict blocks affected translation or application
definition conflict remains definitional
different game states can be scope-partitioned
author count and popularity cannot resolve disagreement
material unresolved disagreement remains in retrieval
empirical support retains population, time, sample, and coverage scope
theory remains distinct from measured evidence
graph release is deterministic and immutable
claim correction creates a new version and release
rights-blocked material is excluded
limited explicit lens remains visibly limited
duplicate restatements preserve attribution chain
insufficient coverage returns abstention
identical graph, router, and query inputs produce identical packets
retrieval packet cannot mutate source, graph, correction, or evidence state
retrieval never emits recommendation language
```

## Resolved Decisions

Phase 42G resolves:

```text
atomic claim fields, labels, modality, and lifecycle
source-specific definition handling
theory node and substantive edge taxonomies
edge provenance and review requirements
attribution-chain role separation
transferability states and translation requirements
disagreement types and resolution states
scoped empirical-reference boundary
immutable graph-release identity
retrieval eligibility, ordering boundaries, and abstention
ephemeral theory packet visibility
community, Rules, correction, model, privacy, and recommendation boundaries
```

## Deferred Decisions

Later accepted contracts must decide:

```text
schema, migrations, repositories, and indexes
extraction implementation
human review UI and workflow
graph storage technology
contradiction scanning implementation
translation implementation
router weights and retrieval implementation
embeddings or semantic index
graph release publishing implementation
Jin intent, query planning, evidence, and legality gates
answer writing and auditing
curriculum
exports and Knowledge Vault
initial approved source set
```

## Future Implementation Boundary

Later implementation contracts may authorize pure packets and validators in
small slices. No implementation filename or storage technology is authorized
by Phase 42G.

Implementation must remain contract-first and may not combine source
acquisition, claim extraction, graph persistence, retrieval, Jin writing, and
curriculum into one packet.

## Phase 42H Boundary

Phase 42H may define only Jin intent resolution, query-plan packets,
evidence-gate behavior, theory-packet consumption, and legality-gate behavior.

It must not implement models, live retrieval, graph mutation, recommendation
generation, UI, exports, or curriculum unless separately authorized.

## Forbidden Phase 42G Work

Phase 42G must not add:

```text
production Theory Corpus code
implementation tests or fixtures
schema, migrations, repositories, or graph database
source acquisition, scraping, transcription, or embeddings
claim extraction, review, or approval implementation
graph construction or persistence
contradiction scanner
translation engine
retrieval ranking or semantic search
model or Jin behavior
curriculum
Rules duplication
Correction Ledger mutation
Decision Intelligence or recommendations
UI, CLI, API, export, or file-writing behavior
live network calls
dependency changes
workflow or validator changes
active-scope changes in the PR
constitution changes
```

## Acceptance Gate

Phase 42G passes only when outside validation confirms that it:

1. remains contract-only;
2. records Phase 42F artifact-backed acceptance;
3. requires atomic, attributed, anchored claims with preserved modality;
4. keeps definitions source-specific;
5. requires typed, sourced, scoped, reviewed graph edges;
6. separates attribution authority from strategic correctness;
7. gates cross-format retrieval on reviewed translation;
8. preserves material disagreement without fame or author-count resolution;
9. keeps empirical links scoped and distinct from theory;
10. defines deterministic immutable graph releases;
11. defines rights-aware, scope-aware, ephemeral retrieval packets;
12. returns abstention for insufficient coverage;
13. preserves Rules, correction, model, privacy, evidence, and recommendation
    boundaries; and
14. keeps Phase 42H blocked.

Phase 42H may begin only after Phase 42G outside validation returns PASS or
PASS WITH REVIEW NOTES.
